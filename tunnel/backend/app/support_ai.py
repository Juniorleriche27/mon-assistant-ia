import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

class ManuscriptIndex:
    def __init__(self, manuscript_path: Path):
        self.manuscript_path = manuscript_path
        self.sections: List[Dict[str, Any]] = []
        self._load_and_index()

    def _load_and_index(self):
        if not self.manuscript_path.exists():
            logger.warning("Manuscrit introuvable au chemin : %s", self.manuscript_path)
            return

        content = self.manuscript_path.read_text(encoding="utf-8", errors="ignore")
        
        # Découpage par chapitres et sections (titres Markdown ## et ###)
        raw_chapters = re.split(r'\n(?=##\s+)', content)
        
        for idx, ch_text in enumerate(raw_chapters):
            lines = ch_text.strip().split("\n")
            header = lines[0].replace("##", "").strip() if lines else f"Section {idx+1}"
            body = "\n".join(lines[1:]).strip()
            
            # Déterminer le numéro et titre du chapitre
            chap_match = re.search(r'Chapitre\s+(\d+)\s*[-—:]\s*(.+)', header)
            chap_num = int(chap_match.group(1)) if chap_match else (0 if "Ouverture" in header else idx)
            chap_title = chap_match.group(2).strip() if chap_match else header

            self.sections.append({
                "chapter_number": chap_num,
                "title": header,
                "clean_title": chap_title,
                "content": body[:4000],  # Extrait représentatif
                "full_text": ch_text
            })

        logger.info("Indexation terminée : %d chapitres et sections chargés.", len(self.sections))

    def search_relevant_sections(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_words = set(re.findall(r'\b[a-zA-Z0-9éèàùçêâôî]{3,}\b', query.lower()))
        if not query_words:
            return self.sections[:top_k]

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for sec in self.sections:
            text = (sec["title"] + " " + sec["content"]).lower()
            score = 0.0
            for word in query_words:
                if word in sec["title"].lower():
                    score += 5.0
                score += text.count(word) * 1.0
            
            # Bonus pour les mots techniques exacts
            for tech in ["cohere", "fastapi", "rag", "docker", "eval", "question", "devis", "corpus", "sqlite", "next"]:
                if tech in query.lower() and tech in text:
                    score += 3.0

            scored.append((score, sec))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [sec for score, sec in scored[:top_k]]

manuscript_index = ManuscriptIndex(settings.MANUSCRIPT_PATH)

async def ask_cohere_support(query: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    return await ask_ai_support(query, history)

async def ask_ai_support(query: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Assistant Support IA KORYXA propulsé par KNOWLIA (avec fallback Cohere et local).
    Fondé sur le manuscrit officiel du livre.
    Cite toujours ses sources et demande les informations de diagnostic si anomalie.
    """
    relevant_sections = manuscript_index.search_relevant_sections(query, top_k=2)
    citations = [f"Chapitre {s['chapter_number']} : {s['clean_title']}" for s in relevant_sections]
    
    # Détection de problème technique / bug
    is_bug_report = bool(re.search(
        r'(erreur|bug|marche pas|échoue|exception|error|failed|traceback|introuvable|modulenotfound|500)',
        query,
        re.IGNORECASE
    ))

    context_text = "\n\n---\n\n".join([f"### {s['title']}\n{s['content']}" for s in relevant_sections])

    # 1. Priorité au moteur IA KNOWLIA si configuré
    if getattr(settings, "KNOWLIA_BASE_URL", "") and getattr(settings, "KNOWLIA_API_KEY", ""):
        try:
            system_prompt = (
                "Tu es l'assistant de support technique officiel du livre « Créer et livrer son premier assistant IA » (KORYXA).\n"
                "Tu t'adresses à un développeur ou freelance. Ton rôle est de l'aider à concevoir, tester, lancer et livrer le projet.\n\n"
                "Consignes impératives :\n"
                "1. Fonde ta réponse UNIQUEMENT sur le contexte officiel fourni ci-dessous issu du manuscrit du livre.\n"
                "2. Cite explicitement le chapitre concerné (ex: « D'après le Chapitre X : ... »).\n"
                "3. Si la question signale une erreur technique ou un bug, demande impérativement le système d'exploitation, la version de Python (`python --version`) et les logs d'erreur du terminal.\n"
                "4. Ne promets jamais de réponse humaine instantanée.\n\n"
                f"CONTEXTE OFFICIEL DU LIVRE :\n{context_text}"
            )

            messages = [{"role": "system", "content": system_prompt}]
            if history:
                for h in history[-4:]:
                    role = h.get("role")
                    content = h.get("content")
                    if role in ("user", "assistant") and content:
                        messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": query})

            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(
                    f"{settings.KNOWLIA_BASE_URL}/public/v1/generate",
                    headers={
                        "Content-Type": "application/json",
                        "X-Knowlia-Api-Key": settings.KNOWLIA_API_KEY
                    },
                    json={
                        "messages": messages,
                        "tenant_id": getattr(settings, "KNOWLIA_TENANT_ID", "mon-assistant-ia")
                    }
                )
                if res.status_code == 200:
                    resp_json = res.json()
                    data = resp_json.get("data", {})
                    ans_text = data.get("content", "").strip()
                    if ans_text:
                        return {
                            "answer": ans_text,
                            "citations": citations,
                            "suggest_ticket": is_bug_report,
                            "engine": "knowlia"
                        }
        except Exception as exc:
            logger.warning("Erreur lors de l'appel au moteur KNOWLIA : %s - repli sur les fournisseurs secondaires", exc)

    # 2. Si clé Cohere configurée et KNOWLIA non disponible
    if settings.COHERE_API_KEY and not settings.COHERE_API_KEY.startswith("sim_"):
        try:
            prompt = (
                "Tu es l'assistant de support technique officiel du livre « Créer et livrer son premier assistant IA » (KORYXA).\n"
                "Tu t'adresses à un développeur ou freelance. Ton rôle est de l'aider à concevoir, lancer et livrer le projet.\n\n"
                "Consignes impératives :\n"
                "1. Fonde ta réponse UNIQUEMENT sur le contexte fourni ci-dessous issu du manuscrit du livre.\n"
                "2. Cite explicitement le chapitre concerné (ex: « D'après le Chapitre X : ... »).\n"
                "3. Si la question signale une erreur technique ou un bug, demande impérativement le système d'exploitation, la version de Python (`python --version`) et les logs d'erreur du terminal.\n"
                "4. Ne promets jamais de réponse humaine instantanée.\n\n"
                f"CONTEXTE DU LIVRE :\n{context_text}\n\n"
                f"QUESTION DE L'APPRENANT :\n{query}\n\n"
                "RÉPONSE CLAIRE ET CITÉE :"
            )

            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(
                    "https://api.cohere.com/v1/chat",
                    headers={
                        "Authorization": f"Bearer {settings.COHERE_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.COHERE_MODEL,
                        "message": prompt,
                    }
                )
                if res.status_code == 200:
                    ans_text = res.json().get("text", "")
                    return {
                        "answer": ans_text,
                        "citations": citations,
                        "suggest_ticket": is_bug_report,
                        "engine": "cohere"
                    }
        except Exception as exc:
            logger.error("Erreur lors de l'appel à Cohere API : %s", exc)

    # Réponse de référence basée directement sur le manuscrit (mode local ou hors ligne)
    top_sec = relevant_sections[0] if relevant_sections else None
    
    diagnostic_prompt = ""
    if is_bug_report:
        diagnostic_prompt = (
            "\n\n> 🔍 **Pour vous aider à diagnostiquer cette anomalie :**\n"
            "- Quel est votre système d'exploitation (Windows / Linux / macOS) ?\n"
            "- Quelle est votre version exacte de Python (`python --version`) ?\n"
            "- Pouvez-vous copier les 10 dernières lignes du message d'erreur affiché dans le terminal ?"
        )

    if top_sec:
        summary_intro = f"D'après le **Chapitre {top_sec['chapter_number']} : {top_sec['clean_title']}** du livre officiel KORYXA :"
        # Sélection d'un paragraphe significatif
        paragraphs = [p.strip() for p in top_sec["content"].split("\n\n") if len(p.strip()) > 80]
        excerpt = paragraphs[0] if paragraphs else top_sec["content"][:300]
        
        answer = f"{summary_intro}\n\n{excerpt}{diagnostic_prompt}\n\nConsultez le fichier source correspondant dans le pack de code fourni pour voir l'implémentation complète."
    else:
        answer = (
            "D'après le guide pratique KORYXA, assurez-vous que votre environnement virtuel Python est activé "
            "et que votre fichier `.env` comporte bien votre clé `COHERE_API_KEY`." + diagnostic_prompt
        )

    return {
        "answer": answer,
        "citations": citations,
        "suggest_ticket": is_bug_report
    }
