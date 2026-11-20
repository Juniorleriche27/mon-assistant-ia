import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

COMMERCIAL_FACTS = """
### INFORMATIONS COMMERCIALES ET PRODUIT OFFICIELLES (KORYXA) :
- **Marque** : KORYXA — Apprendre à construire. Savoir livrer.
- **Produit** : Pack complet « Mon premier assistant IA ».
- **Livre inclus** : « Créer et livrer son premier assistant IA » (68 pages, 12 chapitres pratiques en PDF).
- **Auteur** : Yayra LAMADOKOU, fondateur de KORYXA et ingénieur praticien en IA d'entreprise.
- **Prix officiel** : 11 000 F CFA (XOF), paiement unique sans aucun abonnement, accès garanti à vie.
- **Moyens de paiement acceptés** : KORYXA Pay (sécurisé SSL) acceptant Mobile Money (TMoney, Moov Money) et Cartes bancaires (Visa, Mastercard).
- **Contenu du pack** :
  1. Livre complet de 68 pages en 12 chapitres (PDF).
  2. Code source complet du projet Horizon Numérique (Cohere Command R + Embed v4, FastAPI, Next.js, SQLite/pgvector).
  3. 4 documents d'exercices et FAQ.
  4. 35 questions d'évaluation et de recette réelles.
  5. Kit contractuel et modèles de livraison (modèles de devis, cahier des charges type, procès-verbal de recette).
- **Prérequis réels** : Connaître les bases élémentaires de Python (variables, fonctions simples, exécuter un script, pip). Aucun prérequis en mathématiques ou ML complexe.
- **Fournisseur IA & Frais annexes** : Cohere est utilisé pour la recherche vectorielle et la génération. Cohere offre des clés d'essai gratuites pour apprendre et tester. En production réelle chez un client, les requêtes API Cohere et l'hébergement serveur restent distincts et sont facturés directement par les prestataires au client final.
- **Extrait gratuit** : Document PDF officiel de 15 pages (`KORYXA_Assistant_IA_Extrait.pdf`) téléchargeable immédiatement dans le chat.
- **Accompagnement après-vente** : Le chatbot guide l'acheteur pas à pas à travers les 6 étapes d'onboarding, répond aux questions techniques et permet d'ouvrir un ticket technique si besoin.
"""

def detect_commercial_intent(query: str) -> Optional[Dict[str, Any]]:
    """
    Détecte si la question de l'utilisateur porte sur une information commerciale, tarifaire ou organisationnelle.
    Retourne la réponse officielle validée pour éviter toute hallucination ou citation hors contexte.
    """
    q = query.lower()

    # 1. Prix et tarif
    if any(k in q for k in ["prix", "tarif", "combien", "coût", "cout", "payer combien", "valeur"]):
        return {
            "answer": (
                "Le pack complet **« Mon premier assistant IA »** est proposé au tarif officiel de **11 000 F CFA (XOF)**.\n\n"
                "Il s'agit d'un **paiement unique** (aucun abonnement récurrent), donnant droit à un **accès à vie** "
                "au livre de 68 pages, au code source complet, aux 35 questions d'évaluation et à la boîte à outils contractuelle."
            ),
            "citations": ["Offre officielle KORYXA — 11 000 F CFA"],
            "suggest_ticket": False
        }

    # 2. Moyens de paiement
    if any(k in q for k in ["moyen de paiement", "moyens de paiement", "comment payer", "tmoney", "moov", "flooz", "carte", "visa", "mastercard", "mode de paiement"]):
        return {
            "answer": (
                "Le règlement s'effectue en toute sécurité via la passerelle officielle **KORYXA Pay** (chiffrement SSL).\n\n"
                "Sont acceptés :\n"
                "- **Mobile Money** : TMoney et Moov Money\n"
                "- **Cartes bancaires** : Visa et Mastercard\n\n"
                "Dès la validation de votre paiement, l'accès à tous vos livrables est débloqué instantanément dans cette conversation."
            ),
            "citations": ["Passerelle KORYXA Pay"],
            "suggest_ticket": False
        }

    # 3. Auteur
    if any(k in q for k in ["auteur", "qui a écrit", "qui a ecrit", "qui est yayra", "lamadokou", "qui êtes-vous", "qui est l'auteur"]):
        return {
            "answer": (
                "Le livre et la méthode sont créés par **Yayra LAMADOKOU**, fondateur de **KORYXA** et ingénieur praticien en intelligence artificielle.\n\n"
                "Son approche privilégie le pragmatisme : concevoir des assistants documentaires robustes, maîtrisés, testés et réellement livrables à des entreprises clientes."
            ),
            "citations": ["Yayra LAMADOKOU — Fondateur de KORYXA"],
            "suggest_ticket": False
        }

    # 4. Prérequis et niveau Python
    if any(k in q for k in ["prérequis", "prerequis", "débutant", "debutant", "niveau", "faut-il connaître", "faut-il connaitre", "expert", "difficile"]):
        return {
            "answer": (
                "**Non, vous n'avez pas besoin d'être un expert en IA.**\n\n"
                "Seules les **bases de Python** sont utiles : savoir installer un package avec `pip`, lancer un script et comprendre des variables et fonctions simples.\n\n"
                "Le guide vous accompagne pas à pas pour configurer votre environnement virtuel, préparer vos documents PDF et connecter les modèles Cohere sans complexité inutile."
            ),
            "citations": ["Présentation KORYXA — Prérequis & Public cible"],
            "suggest_ticket": False
        }

    # 5. Frais annexes (Cohere / Hébergement)
    if any(k in q for k in ["frais", "caché", "cache", "cohere payant", "hébergement", "hebergement", "frais supplémentaire", "frais supplementaire", "abonnement"]):
        return {
            "answer": (
                "L'accès au pack KORYXA est à **paiement unique de 11 000 F CFA** sans aucun abonnement.\n\n"
                "Concernant les technologies :\n"
                "- **Cohere** offre des clés d'essai gratuites permettant de développer, tester et indexer vos documents sans frais.\n"
                "- En **production chez un client**, les éventuels frais de requêtes API Cohere (quelques centimes) et d'hébergement serveur sont distincts et directement pris en charge par l'entreprise cliente finale."
            ),
            "citations": ["Conditions d'exploitation & Frais annexes"],
            "suggest_ticket": False
        }

    # 6. Extrait gratuit
    if any(k in q for k in ["extrait", "échantillon", "echantillon", "aperçu", "apercu", "gratuit", "lire un extrait"]):
        return {
            "answer": (
                "Vous pouvez télécharger immédiatement et gratuitement l'**extrait officiel de 15 pages** "
                "(couverture, introduction et chapitres 1 et 2) pour découvrir la méthode et le style pratique du guide avant de commander."
            ),
            "citations": ["Extrait gratuit — KORYXA_Assistant_IA_Extrait.pdf"],
            "suggest_ticket": False
        }

    return None

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
    Fondé sur le manuscrit officiel du livre et les informations commerciales validées.
    Cite toujours ses sources et demande les informations de diagnostic si anomalie.
    """
    # 0. Vérification immédiate des intentions commerciales et produit officielles
    commercial_ans = detect_commercial_intent(query)
    if commercial_ans:
        return commercial_ans

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
                "Tu es l'assistant officiel du pack « Mon premier assistant IA » (KORYXA).\n"
                "Tu t'adresses à des apprenants, développeurs ou freelances avec bienveillance, clarté et professionnalisme.\n\n"
                f"{COMMERCIAL_FACTS}\n\n"
                "Consignes impératives :\n"
                "1. Fonde ta réponse sur les informations officielles fournies ci-dessus et le contexte du manuscrit ci-dessous.\n"
                "2. Si la question est d'ordre technique, cite explicitement le chapitre concerné (ex: « D'après le Chapitre X : ... »).\n"
                "3. Si la question porte sur le prix, rappelle impérativement le tarif officiel de 11 000 F CFA en paiement unique.\n"
                "4. Si la question signale une erreur technique ou un bug, demande impérativement le système d'exploitation, la version de Python (`python --version`) et les logs d'erreur du terminal.\n"
                "5. Ne promets jamais de réponse humaine instantanée.\n\n"
                f"CONTEXTE TECHNIQUE DU LIVRE :\n{context_text}"
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
