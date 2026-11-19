# Créer et livrer son premier assistant IA

## Le guide pratique du RAG pour les développeurs et freelances : des documents de l’entreprise au déploiement

**LAMADOKOU Yayra**

Édition Cohere - projet accompagné de son code source

## Ouverture - Un projet que vous pouvez expliquer

Une organisation possède souvent les réponses à ses propres questions. Elles se trouvent dans un catalogue, un règlement, une grille de prix ou une FAQ. Pourtant, un visiteur doit parfois ouvrir plusieurs fichiers, identifier la bonne version et comprendre seul quelles conditions s’appliquent à son cas. Un assistant documentaire peut raccourcir ce parcours : il cherche les passages utiles et prépare une réponse dont l’utilisateur peut consulter les sources.

Ce livre vous accompagne dans la réalisation d’un tel assistant. Le projet suivi est celui d’Horizon Numérique, un centre de formation fictif. Ses visiteurs veulent connaître le programme d’un parcours, le coût d’une inscription, les horaires ou les conditions d’annulation. Son équipe veut pouvoir remplacer une grille de tarifs sans demander une intervention de développement à chaque modification.

Votre résultat sera une application avec deux espaces : une discussion pour les visiteurs et une administration documentaire. Vous construirez le moteur de recherche, la génération avec Cohere, l’API, l’interface et la procédure de livraison. Vous apprendrez également à distinguer une réponse convaincante d’une réponse effectivement soutenue par le document cité.

Le parcours s’adresse aux développeurs juniors et aux freelances qui possèdent les bases de Python. Il suppose que vous savez créer un dossier de projet, installer une dépendance et exécuter une commande. Les notions nécessaires de SQL, de HTTP et de JavaScript sont introduites à partir de leur rôle dans l’application. Vous pouvez suivre une première fois le projet fourni, puis le reproduire avec un nouveau corpus.

Le fournisseur de cette édition est Cohere. Command R7B prépare les réponses ; Embed v4 transforme les passages et les questions en vecteurs. Les modèles sont définis dans la configuration du serveur. Il s’agit d’un choix de référence pour ce projet, dont la disponibilité et les conditions d’utilisation sont à vérifier sur votre compte. Aucune dépendance OpenAI n’est nécessaire.

Les documents d’Horizon Numérique ont été écrits pour les exercices. Les prix, les programmes, les horaires et les adresses ne correspondent pas à un établissement réel. Cette distinction vous permet de travailler sur un corpus contrôlé : lorsqu’une réponse est fausse, vous pouvez retrouver exactement le passage qui aurait dû la corriger.

### Comment progresser

Chaque chapitre présente un objectif, une réalisation et une vérification. Lisez l’explication, ouvrez le fichier correspondant, puis effectuez le contrôle avant de continuer. Le dépôt fourni contient les fichiers complets. Les extraits reproduits dans le livre servent à comprendre une décision ou un mécanisme précis.

Trois résultats sont à conserver pendant le parcours : le cahier des charges, le jeu de questions et le rapport de validation. Ils feront le lien entre ce que vous avez construit et ce que vous présentez au client. Une application qui s’ouvre correctement ne suffit pas à démontrer que ses réponses sont justes.

Le fichier `VALIDATION.md` du projet indique les contrôles réellement exécutés lors de la préparation de cette édition. Les tests automatisés du logiciel utilisent des doubles de test et ne prétendent pas mesurer les modèles distants. Lorsque vous activez votre clé Cohere, exécutez aussi le jeu documentaire avec le véritable fournisseur et conservez ce rapport séparément.

# Partie I - Comprendre et cadrer

## Chapitre 1 - Transformer une demande en projet livrable

### Partir de la question que le visiteur se pose

« Je veux un chatbot » décrit un objet, mais ne précise pas encore son utilité. Pour cadrer le projet, demandez quel effort doit disparaître. Dans notre cas, une personne intéressée par une formation doit pouvoir connaître son tarif et ses conditions d’inscription sans parcourir toute la documentation. Le secrétariat doit aussi pouvoir retirer une information obsolète.

Choisissez quelques situations concrètes. Une première personne demande le prix total d’Analyse de Données. Une deuxième veut savoir si elle sera remboursée en annulant cinq jours avant la rentrée. Une troisième écrit seulement « Combien coûte la formation ? ». Ces trois demandes ne nécessitent pas le même comportement. La première attend un montant, la deuxième une règle et ses conditions, la troisième une précision.

Le cahier des charges doit donc décrire les comportements, et pas seulement nommer les technologies. Écrire « interface Next.js et moteur RAG » ne permet pas au client de juger si le résultat répond au besoin. Écrire « le visiteur obtient le montant total, le détail des tranches et le document source » fournit un résultat vérifiable.

### Définir qui valide les informations

Le développeur organise le traitement des documents ; le responsable du centre valide leur contenu métier. Avant l’indexation, identifiez la personne qui fait foi sur les prix, les dates et les règlements. Un assistant ne résout pas une contradiction entre deux fichiers simplement parce qu’il utilise une IA. Le client doit choisir quelle version est actuelle.

Dans Horizon Numérique, le corpus comprend un catalogue, une grille de tarifs, un règlement, un calendrier et une FAQ. Les originaux sont conservés dans la base. Cette décision facilitera la consultation des sources et la sauvegarde de l’ensemble documentaire. L’administrateur est chargé des remplacements ; les visiteurs disposent seulement de fonctions de lecture et de discussion.

Précisez également les actions autorisées. Notre assistant informe, cite et oriente vers le secrétariat. Il ne confirme ni paiement, ni place, ni exception de remboursement. Ces opérations exigeraient des intégrations et des règles métier supplémentaires. Le parcours proposé correspond à une application documentaire pour une seule organisation.

### Choisir des critères de réception

Un critère utile comprend une situation, un comportement attendu et une manière de le vérifier. Pour le tarif d’Analyse de Données, le montant attendu est 650 euros. Les tranches sont 220, 220 puis 210 euros. Les frais administratifs de 40 euros sont inclus. Une réponse qui ajoute ces frais au total échoue au contrôle, même si elle cite correctement la grille tarifaire.

Pour l’annulation cinq jours avant la rentrée, la réponse doit tenir compte de la règle des sept jours et de l’absence de remboursement dans ce cas. Elle peut expliquer qu’un report pour force majeure est examiné par le secrétariat, sans le présenter comme automatique. Pour la question ambiguë sur « la formation », le bon résultat est une demande de précision.

Mesurez aussi le temps de réponse dans des conditions décrites : machine, connexion, nombre de requêtes et modèle. Une moyenne de quatre secondes dans un devis est un objectif à vérifier, pas un résultat déjà obtenu. Évitez de transformer un nombre choisi au cadrage en garantie technique sans mesure.

### Réalisation et vérification

Ouvrez `modeles_clients/01_cahier_des_charges_modele.md`. Complétez l’objectif, les utilisateurs, le corpus et le responsable documentaire. Écrivez dix demandes représentatives avant d’ajouter une fonctionnalité. Puis classez chaque demande : réponse factuelle, précision nécessaire, information absente ou demande d’action.

Vérifiez que le client comprend ce classement. Si la même demande appelle deux résultats incompatibles selon les personnes interrogées, le besoin doit encore être clarifié. Une difficulté repérée à ce stade coûte moins de travail qu’une règle changée au moment de la livraison.

### Exercice

Le client demande : « L’assistant doit s’occuper des inscriptions ». Reformulez cette phrase en trois comportements précis. Proposition de correction : expliquer les pièces à fournir ; afficher la date limite du premier paiement ; orienter vers le secrétariat pour confirmer la place. Ces comportements correspondent au périmètre documentaire du livre.

## Chapitre 2 - Comprendre le RAG à partir d’une question

### Donner au modèle les informations nécessaires

Un modèle de langage peut produire un texte fluide sans connaître les documents actuels de votre client. Le prix d’une formation fictive ne peut pas être déduit de la manière dont d’autres centres fixent leurs tarifs. L’application doit d’abord retrouver l’information pertinente, puis la présenter au modèle avec une consigne claire.

Le RAG, pour Retrieval-Augmented Generation, organise cette association entre recherche et génération. Dans le projet, la recherche sélectionne des passages du corpus. Cohere reçoit ces passages et prépare une réponse. Le serveur contrôle ensuite le format de cette réponse et la relie aux sources conservées dans la base.

Il existe deux circuits. Le premier prépare les documents lors de leur ajout ou de leur remplacement. Le second traite une question posée par un utilisateur. Séparer ces circuits évite d’extraire et de réindexer tous les fichiers à chaque conversation.

### Le circuit documentaire

Un PDF est lu page par page. Le texte est découpé en fragments assez courts pour être retrouvés et transmis au modèle. Chaque fragment garde le nom de son document et sa page. Pour le Markdown, la provenance correspond à une section. Une information de provenance doit être conservée au moment de l’extraction ; la reconstituer ensuite à partir du texte généré serait fragile.

Les fragments sont envoyés au modèle d’embeddings avec `input_type=search_document`. Un embedding est une liste de nombres qui représente des propriétés du texte pour la recherche. Il ne s’agit ni d’un résumé lisible, ni d’une preuve de vérité. Deux passages proches dans cet espace peuvent parler d’un sujet similaire sans répondre à la même question.

Les vecteurs sont enregistrés avec les fragments. Dans cette édition, les vecteurs d’Embed v4 ont 1024 dimensions. Le schéma de la base et les réponses reçues de l’API sont contrôlés pour conserver cette cohérence. Changer de modèle implique de réexaminer et de réindexer le corpus.

### Le circuit d’une question

Prenons « Quel est le tarif total d’Analyse de Données ? ». L’application produit un embedding de requête avec `input_type=search_query`. Elle compare ce vecteur aux fragments et effectue aussi une recherche par mots-clés. Les résultats sont réunis et classés ; quelques passages sont transmis au modèle de génération.

Le modèle reçoit des données et une consigne : répondre à partir des passages, demander une précision si nécessaire et signaler l’absence d’information. Il doit aussi indiquer les identifiants des passages utilisés. Le serveur vérifie que ces identifiants appartiennent bien aux résultats récupérés avant d’afficher les sources.

Cette vérification rend la provenance contrôlable. Elle ne démontre pas à elle seule que chaque phrase de la réponse est correctement soutenue. Un passage contenant « 650 euros » et « 40 euros inclus » pourrait être mal interprété. C’est la raison pour laquelle l’évaluation distingue le document trouvé et la réponse formulée.

### Diagnostiquer trois types d’erreurs

Si le bon prix n’est pas dans le corpus, la correction porte sur le document. Si le document est présent mais que la recherche remonte un autre parcours, la correction porte sur la récupération. Si le passage est correct mais que la réponse ajoute les frais inclus, la correction porte sur l’interprétation et les consignes.

Évitez de changer simultanément le découpage, le nombre de résultats et le prompt lorsque vous enquêtez sur une erreur. Conservez la question, les passages obtenus et la réponse. Modifiez un élément, puis rejouez le même cas. Vous pourrez expliquer ce qui a effectivement amélioré le résultat.

### Exercice

Une réponse annonce 720 euros pour Analyse de Données. Le corpus indique pourtant 650 euros pour ce parcours et 720 euros pour Automatisation & IA. Avant de réécrire le prompt, consultez les fragments récupérés. Si seul le tarif d’Automatisation & IA est présent, le premier problème est la recherche. Si les deux prix sont présents, examinez la formulation de la question et le contexte transmis.

# Partie II - Construire le moteur documentaire

## Chapitre 3 - Préparer un environnement reproductible

### Comprendre les quatre services

Le projet associe une base PostgreSQL, un backend FastAPI, un frontend Next.js et, en production, Caddy. La base stocke les documents et les fragments. Le backend extrait les fichiers, appelle Cohere et expose les routes HTTP. Le frontend fournit les écrans. Caddy reçoit les connexions HTTPS et les oriente vers le bon service.

Le fichier de développement publie les ports sur l’adresse locale de la machine. Le fichier de production expose les ports de Caddy et garde les autres services sur le réseau Docker. Utilisez chaque fichier dans son contexte ; les fusionner sans vérifier les ports pourrait modifier l’exposition prévue.

Le dépôt livre aussi un adaptateur SQLite pour les essais et les tests automatisés. Cet adaptateur permet d’exécuter la logique sans installer PostgreSQL. Il ne reproduit pas les index pgvector et GIN du déploiement cible. Le résultat d’un test SQLite doit donc être présenté comme tel.

### Préparer la configuration

Depuis la racine du projet, exécutez `python scripts/setup_env.py`. Le script crée un fichier `.env`, génère les secrets de base et d’administration et laisse vide la variable Cohere. Il conserve un fichier existant au lieu de l’écraser. Ouvrez ensuite ce fichier local et renseignez votre clé dans `COHERE_API_KEY`.

La clé Cohere reste sur le serveur. Elle n’apparaît dans aucun composant React et ne doit pas être préfixée par `NEXT_PUBLIC_`. Cette règle évite d’inclure un secret de fournisseur dans le JavaScript téléchargé par les visiteurs. L’interface appelle votre backend ; votre backend appelle Cohere.

Voici les paramètres du fournisseur utilisés par l’édition :

```dotenv
COHERE_API_KEY=
COHERE_CHAT_MODEL=command-r7b-12-2024
COHERE_EMBED_MODEL=embed-v4.0
EMBEDDING_DIMENSION=1024
```

Les valeurs de modèle sont des choix explicites, pas des alias « latest ». Le nombre de dimensions fait partie de l’identité d’indexation. Le code inclut aussi un identifiant de version du découpage. Deux corpus produits avec des paramètres incompatibles ne doivent pas être comparés comme s’ils appartenaient au même espace.

### Démarrer et vérifier

Avec Docker et Compose disponibles, lancez `docker compose up --build`. Le service de base doit répondre à son contrôle de santé avant le démarrage du backend. FastAPI crée ensuite les tables nécessaires et vérifie le type de la colonne vectorielle. L’interface devient disponible sur `http://localhost:3000`.

Consultez `http://localhost:8000/health`. Le champ `database_ok` indique l’accès à la base ; `pgvector_enabled` distingue PostgreSQL du stockage de test. `cohere_configured` indique seulement qu’une clé est présente. Il ne remplace pas un appel réel au fournisseur et n’affirme pas que cette clé est valide.

Si PostgreSQL ne démarre pas, consultez ses journaux avant de changer le backend. Si le backend ne répond pas, vérifiez la chaîne de connexion, puis ses journaux. Si seule l’interface échoue, vérifiez le service frontend. Ce diagnostic par service est plus efficace qu’une réinstallation générale.

### Reproduire l’installation sans Docker

Créez un environnement Python et installez `backend/requirements.txt`. Pour une exploration locale avec SQLite, placez `DATABASE_URL=sqlite:///local.db` dans `.env`. Sous PowerShell, définissez `$env:PYTHONPATH = "backend"`, puis lancez `python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000`. Dans un second terminal, ouvrez `frontend`, exécutez `npm ci`, puis `npm run dev`.

Cette variante reste connectée à Cohere lorsque vous indexez ou posez une question sur un corpus rempli. Elle ne simule pas une IA en l’absence de clé. Les doubles de test sont réservés à la suite logicielle.

### Exercice et résultat attendu

Relevez les quatre informations de santé sans copier de secret. Notez quel mode de stockage est utilisé. Arrêtez et redémarrez l’application, puis vérifiez que les données ne disparaissent pas. Vous obtenez une fiche d’environnement qui permettra de reproduire vos observations.

### Atelier de code - La configuration du serveur

Fichier : `backend/app/config.py`. Les valeurs sont validées dès la construction des paramètres. Le type SecretStr évite un affichage accidentel dans la représentation de l’objet.

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )
    database_url: str = (
        "postgresql://rag_user:change-me@localhost:5432/rag_horizon"
    )
    cohere_api_key: SecretStr = SecretStr("")
    cohere_chat_model: str = "command-r7b-12-2024"
    cohere_embed_model: str = "embed-v4.0"
    embedding_dimension: int = Field(default=1024, ge=1, le=1536)
    admin_api_key: SecretStr = SecretStr("")
    allowed_origins: str = "http://localhost:3000"
    corpus_dir: Path = Path("corpus")
    max_upload_bytes: int = 10 * 1024 * 1024
    max_document_characters: int = 250_000
    chat_limit_per_minute: int = Field(default=20, ge=1, le=1000)
    minimum_similarity: float = Field(default=0.35, ge=-1, le=1)
    contact: str = "le secrétariat du centre"

    @model_validator(mode="after")
    def validate_embedding_configuration(self):
        if self.cohere_embed_model != "embed-v4.0":
            raise ValueError(
                "Cette édition utilise embed-v4.0. Un changement de"
                " modèle demande une migration et une réindexation."
            )
        if self.embedding_dimension not in (256, 512, 1024, 1536):
            raise ValueError(
                "Dimension non prise en charge pour embed-v4.0."
            )
        return self

    @property
    def embedding_identity(self):
        return (
            "cohere:"
            f"{self.cohere_embed_model}:"
            f"{self.embedding_dimension}:"
            "chunk-v1"
        )
```

Contrôle : démarrer le service puis consulter `/health`. Une dimension comme 768 est refusée par cette configuration Embed v4.

## Chapitre 4 - Préparer les documents sans perdre leur sens

### Accepter un format ne signifie pas pouvoir le lire

Le projet accepte les PDF texte, le Markdown et le TXT. Il contrôle le nom et la taille du fichier, puis son contenu. Une extension `.pdf` ne transforme pas un fichier arbitraire en PDF. Un document scanné peut être un PDF valide sans contenir le texte nécessaire à notre extraction ; il demandera un traitement OCR dans une étape supplémentaire.

Les documents fournis sont volontairement simples. Ils permettent d’observer les numéros de page et les sections sans mélanger immédiatement les difficultés des tableaux scannés ou des colonnes complexes. Avant d’utiliser les fichiers d’un client, testez l’extraction de leurs montants, titres, dates et règles dans un échantillon représentatif.

Le module `ingestion.py` conserve la provenance dès la lecture. Le PDF est parcouru page par page, et le Markdown est regroupé sous ses titres. Les fragments enregistrés contiennent `content`, `page` et `section`. Le document original est conservé séparément dans la même base.

### Découper une règle avec son exception

Une coupure située entre « aucun remboursement » et l’exception de force majeure peut changer l’interprétation d’une question. Le découpage cherche d’abord les frontières de paragraphes. Si un paragraphe est trop long, il utilise des fenêtres avec un recouvrement limité.

Les valeurs de 750 caractères et de 120 caractères de recouvrement donnent un point de départ reproductible. Elles ne sont pas une recette universelle. Un règlement dense peut nécessiter un regroupement par article ; un catalogue peut être plus clair avec un fragment par formation. Le jeu de questions permet de comparer ces choix.

Le recouvrement ne répare pas toutes les coupures. Une exception éloignée de plusieurs pages, un tableau ou une note de bas de page exige un traitement spécifique. Inspectez donc les fragments obtenus sur les passages qui portent une condition importante.

### Calculer les vecteurs Cohere

Les textes des fragments sont envoyés à l’endpoint Embed v2 avec le type `search_document`. Le code divise les requêtes en lots de 96 textes au maximum. Il demande les vecteurs flottants avec la dimension configurée et refuse une réponse dont le nombre ou la forme ne correspond pas à la demande.

Ce contrôle évite une erreur silencieuse : un vecteur associé au mauvais passage peut produire une réponse plausible à partir d’une provenance incorrecte. Les vecteurs nuls, non numériques ou non finis sont également rejetés. L’état ancien du document est conservé si l’appel embeddings échoue.

### Remplacer une version sans mélanger les fragments

Un hash SHA-256 représente les octets du document. Si le nom, le hash et l’identité d’indexation sont inchangés, le système ne recalcule pas les embeddings. Si le fichier a changé, il prépare d’abord tous les nouveaux fragments et vecteurs. La suppression des anciens fragments et l’enregistrement des nouveaux se font ensuite dans une transaction de base.

La transaction est importante pour le visiteur. Il doit retrouver une version complète et non une moitié de l’ancienne grille associée à une moitié de la nouvelle. Le code contrôle également qu’un autre remplacement n’a pas modifié le document pendant l’appel distant.

Le nom de fichier constitue ici l’identité fonctionnelle du document à remplacer. Si vous téléversez `tarifs_2028.pdf` après `tarifs_2027.pdf`, vous ajoutez deux documents. Si votre intention était de remplacer la grille active, retirez l’ancienne ou utilisez le même nom. L’administrateur doit comprendre cette règle dans son guide de livraison.

### Vérification et exercice

Indexez un fichier, envoyez-le une deuxième fois et observez le statut `unchanged`. Modifiez ensuite un montant dans une copie du document et renvoyez le même nom. Vérifiez que la liste contient toujours un document et que les sources reflètent la nouvelle version. Enfin, retirez-le et vérifiez que ses fragments ne sont plus retrouvés.

Le test `test_update_failure_rolls_back_old_corpus` simule un échec pendant le remplacement. Sa fonction est de vérifier la conservation de l’état précédent, un comportement utile pour toute application documentaire qui reçoit régulièrement des mises à jour.

### Atelier de code - Lire un document et conserver sa provenance

Fichier : `backend/app/ingestion.py`. L’extraction vérifie le contenu et conserve la page ou la section. Observez le moment où ces métadonnées sont attachées aux fragments.

```python
def extract_fragments(filename, data, settings):
    suffix = safe_filename(filename)
    if not data or len(data) > settings.max_upload_bytes:
        raise ValueError(
            "Fichier vide ou supérieur à la limite de taille."
        )
    fragments = []
    if suffix == ".pdf":
        if not data.startswith(b"%PDF-"):
            raise ValueError(
                "Le contenu ne correspond pas à un PDF."
            )
        try:
            reader = PdfReader(io.BytesIO(data))
            if reader.is_encrypted or len(reader.pages) > 200:
                raise ValueError(
                    "PDF chiffré ou supérieur à 200 pages."
                )
            for page_number, page in enumerate(reader.pages, 1):
                text = page.extract_text() or ""
                fragments.extend(
                    {
                        "page": page_number,
                        "section": None,
                        "content": c,
                    }
                    for c in split_into_chunks(text)
                )
        except ValueError:
            raise
        except Exception as error:
            raise ValueError("PDF illisible.") from error
    else:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise ValueError(
                "Le fichier texte doit être encodé en UTF-8."
            ) from error
        if "\x00" in text:
            raise ValueError(
                "Un fichier binaire ne peut pas être traité comme"
                " du texte."
            )
        section, body = "Introduction", []

        def flush():
            fragments.extend(
                {"page": None, "section": section, "content": c}
                for c in split_into_chunks("\n".join(body))
            )

        for line in text.splitlines():
            if suffix == ".md" and re.match(r"^#{1,6}\s+", line):
                flush()
                section = re.sub(r"^#{1,6}\s+", "", line).strip()
                body = []
            else:
                body.append(line)
        flush()
    total = sum(len(f["content"]) for f in fragments)
    if not fragments or total < 20:
        raise ValueError(
            "Aucun texte exploitable. Un PDF scanné nécessite un"
            " OCR préalable."
        )
    if total > settings.max_document_characters:
        raise ValueError(
            "Le document contient trop de texte pour cette édition."
        )
    return fragments
```

Vérification ciblée, depuis la racine du projet :

```bash
python -m unittest discover -s tests -v
```

## Chapitre 5 - Retrouver le passage utile

### Rechercher le sens et les termes exacts

Un visiteur peut écrire « combien coûte » alors que le document utilise « tarif total ». La recherche vectorielle vise à rapprocher des formulations de sens voisin. Une référence comme `HN-IA-01` pose une autre difficulté : ses caractères exacts sont déterminants. Le projet associe donc une recherche vectorielle et une recherche plein texte.

Dans PostgreSQL, pgvector enregistre et compare les vecteurs. Une colonne `tsvector` représente le texte pour la recherche en français. Un index HNSW accompagne la comparaison vectorielle et un index GIN accompagne la recherche textuelle. Ces index accélèrent les opérations ; ils ne remplacent pas l’évaluation de leur résultat.

L’adaptateur SQLite des tests calcule une proximité et un recouvrement de mots sur un petit corpus. Il vérifie la logique qui assemble les résultats. Il ne permet pas de conclure à la performance des index PostgreSQL sur un volume réel.

### Donner le bon type à l’embedding de requête

Pour une question, le fournisseur reçoit `input_type=search_query`. Le même modèle et la même dimension sont utilisés pour les documents et les questions, avec ce type d’entrée adapté. Le projet conserve cette distinction dans l’adaptateur et la vérifie par un test du contrat HTTP.

Avant la recherche, le serveur contrôle l’identité d’indexation des documents actifs. Si le corpus a été produit avec une autre configuration, il demande une réindexation. Réutiliser de vieux vecteurs après un changement de modèle rendrait les scores difficiles à interpréter, même si la taille des listes de nombres semble identique.

### Fusionner deux classements

La fonction de recherche récupère jusqu’à 25 candidats vectoriels et 25 candidats textuels. Leurs scores n’ont pas la même signification. Additionner directement un score de similarité et un rang de texte pourrait donner une influence arbitraire à l’un d’eux.

La fusion RRF utilise la place du candidat dans chaque classement. Dans cette édition, un fragment présent au rang r reçoit une contribution de `1 / (60 + r)`. S’il apparaît dans les deux listes, les deux contributions sont additionnées. Le serveur renvoie les cinq premiers résultats du classement final.

Le nombre 60 règle l’effet relatif des rangs ; il n’exprime pas un taux de confiance. Un score RRF élevé signifie qu’un passage se classe favorablement parmi les candidats. Il ne signifie pas que la réponse à la question se trouve nécessairement dans ce passage.

### Examiner la récupération avant la génération

La route `/search` renvoie les extraits et les scores. Elle est réservée à l’administration dans ce projet, car elle sert au diagnostic. Vous pouvez l’interroger via la documentation interactive du backend, en fournissant l’en-tête `X-Admin-Key`.

Examinez la recherche pour trois formulations d’une même demande : « Tarif Analyse de Données », « Combien coûte le parcours data ? » et « Prix HN-DA-01 ». Le bon document doit être présent, mais regardez aussi le passage exact. Un catalogue qui cite le nom du parcours n’est pas forcément la grille qui indique son montant.

Le réglage `MINIMUM_SIMILARITY` permet de filtrer des recherches trop faibles. Sa valeur initiale de 0,35 est une hypothèse d’essai. Un résultat textuel positif peut aussi conduire à l’étape suivante. La génération devra encore décider si les informations répondent effectivement à la demande.

### Exercice

Ajoutez une question sur un logement, information absente du corpus. Comparez-la à une question sur le coût de formation. Notez les cinq passages obtenus et leurs scores. Vous constaterez qu’une recherche retourne souvent les documents les moins éloignés, même lorsque le corpus ne contient pas la réponse. C’est un point essentiel pour comprendre le statut `not_found`.

### Atelier de code - Fusionner les résultats

Fichier : `backend/app/db.py`, méthode `Store.search`. Comparez les deux listes puis la boucle de fusion ; les contributions RRF portent sur le rang et non sur les scores bruts.

```python
def search(self, question, vector, identity, limit=5):
    if len(vector) != self.dimension or not all(
        math.isfinite(x) for x in vector
    ):
        raise ValueError("Vecteur de requête incompatible.")
    cols = "c.id,c.content,c.page,c.section,c.document_id,d.filename"
    with self.connect() as conn:
        incompatible = self.run(
            conn,
            "SELECT id FROM documents WHERE"
            " embedding_identity<>%s LIMIT 1",
            (identity,),
        ).fetchone()
        if incompatible:
            raise ConflictError(
                "Le corpus doit être réindexé avec la"
                " configuration embeddings actuelle."
            )
        if self.sqlite:
            all_rows = [
                dict(r)
                for r in self.run(
                    conn,
                    f"SELECT {cols}, c.embedding FROM chunks c"
                    " JOIN documents d ON c.document_id=d.id",
                ).fetchall()
            ]
            qterms = terms(question)
            for r in all_rows:
                emb = json.loads(r.pop("embedding"))
                norm = math.sqrt(
                    sum(x * x for x in emb)
                    * sum(x * x for x in vector)
                )
                r["vector_score"] = (
                    sum(a * b for a, b in zip(emb, vector))
                    / norm
                    if norm
                    else 0
                )
                r["keyword_score"] = len(
                    qterms & terms(r["content"])
                ) / max(1, len(qterms))
            vr = sorted(
                all_rows,
                key=lambda r: (-r["vector_score"], r["id"]),
            )[:25]
            kr = sorted(
                (r for r in all_rows if r["keyword_score"] > 0),
                key=lambda r: (-r["keyword_score"], r["id"]),
            )[:25]
        else:
            vs = json.dumps(vector)
            vr = [
                dict(r)
                for r in self.run(
                    conn,
                    f"""SELECT {cols}, 1-(c.embedding <=> %s::vector) AS vector_score,
                ts_rank_cd(c.content_tsv,plainto_tsquery('french',%s)) AS keyword_score
                FROM chunks c JOIN documents d ON c.document_id=d.id
                ORDER BY c.embedding <=> %s::vector LIMIT 25""",
                    (vs, question, vs),
                ).fetchall()
            ]
            kr = [
                dict(r)
                for r in self.run(
                    conn,
                    f"""SELECT {cols}, 1-(c.embedding <=> %s::vector) AS vector_score,
                ts_rank_cd(c.content_tsv,plainto_tsquery('french',%s)) AS keyword_score
                FROM chunks c JOIN documents d ON c.document_id=d.id
                WHERE c.content_tsv @@ plainto_tsquery('french',%s)
                ORDER BY keyword_score DESC,c.id LIMIT 25""",
                    (vs, question, question),
                ).fetchall()
            ]
    merged = {}
    for rows in (vr, kr):
        for rank, row in enumerate(rows, 1):
            item = merged.setdefault(
                row["id"], {**row, "rrf_score": 0.0}
            )
            item["rrf_score"] += 1 / (60 + rank)
    return sorted(
        merged.values(),
        key=lambda r: (-r["rrf_score"], r["id"]),
    )[:limit]
```

## Chapitre 6 - Préparer une réponse dont la provenance est contrôlable

### Définir trois résultats possibles

Le serveur distingue trois statuts : `answered`, `clarify` et `not_found`. Une réponse factuelle doit être reliée à des passages. Une demande ambiguë doit conduire à une précision. Une information absente doit être annoncée comme telle, avec une orientation utile pour le visiteur.

Cette distinction évite de traiter tous les textes du modèle comme des réponses confirmées. Une phrase aimable demandant quelle formation intéresse le visiteur peut être un excellent résultat, même si elle ne contient aucun montant. À l’inverse, un prix fourni pour une formation non précisée peut être une erreur.

### Composer le contexte

La question, l’historique récent et les extraits sont sérialisés dans un objet JSON transmis comme contenu utilisateur. Les consignes principales sont placées dans un message système distinct. Elles précisent que les extraits sont des données et ne peuvent pas redéfinir les règles de l’assistant.

Le prompt demande un objet JSON contenant `status`, `answer` et `source_ids`. Le paramètre `response_format` active le mode JSON de Chat v2. Cette édition transmet le contexte dans les messages et n’utilise pas le paramètre natif `documents`, qui ne se combine pas avec ce mode de sortie dans la documentation consultée.

Le contenu reste soumis à une validation de l’application. Le code vérifie le statut, la longueur de la réponse, la liste des identifiants et le signal de fin de génération. Une sortie tronquée est une erreur de service, pas une réponse complète à afficher.

### Contrôler les sources côté serveur

Le modèle peut proposer un identifiant de source. Il ne peut pas décider librement quel fichier sera affiché au visiteur. Pour un statut `answered`, le serveur exige au moins un identifiant et vérifie chacun d’eux dans les résultats de recherche. Un identifiant inventé transforme le résultat en absence de réponse vérifiable.

Les noms, les pages, les sections et les extraits affichés proviennent ensuite de la base. L’interface propose le téléchargement de l’original. Cette chaîne permet de remonter de la réponse au document effectivement indexé.

Une source authentique ne prouve toujours pas une interprétation correcte. Si le modèle annonce que les frais de 40 euros s’ajoutent aux 650 euros, l’existence de la grille tarifaire ne rend pas cette phrase exacte. L’évaluation humaine doit comparer l’affirmation au passage, notamment pour les négations, les conditions et les exceptions.

### Historique, ambiguïté et demandes de contournement

L’interface transmet au maximum trois échanges récents. Le serveur limite également leur nombre et leur taille. L’historique aide à comprendre « Et pour le deuxième parcours ? », mais il ne constitue pas une nouvelle source documentaire. Une information formulée précédemment par l’utilisateur ne devient pas vraie parce qu’elle figure dans la conversation.

Un filtre repère quelques demandes explicites de contournement. Il permet de tester une réaction prévisible sur des cas simples, par exemple une demande d’ignorer les consignes pour créer une réduction. Ce filtre lexical est limité et ne constitue pas une protection générale contre toutes les formulations possibles.

### Exercice et correction

Comparez trois questions : « Quel est le prix d’Analyse de Données ? », « Combien coûte la formation ? » et « Proposez-vous une cantine ? ». Les résultats attendus sont respectivement `answered`, `clarify` et `not_found`. Le premier affiche une source ; les deux autres n’affichent pas une source comme si elle confirmait une réponse métier.

Ajoutez ensuite un test de réponse comportant un identifiant fictif. Vérifiez que l’application refuse de l’afficher comme réponse sourcée. Vous disposez ainsi d’une vérification logicielle indépendante du comportement réel du modèle.
### Atelier de code - Accepter une réponse et ses références

Fichier : `backend/app/rag.py`. La vérification des identifiants se fait après la génération et avant la construction des sources affichées.

```python
def answer_question(store, provider, settings, question, history):
    def response(status, answer, sources=None, usage=None):
        return {
            "status": status,
            "answer": answer,
            "sources": sources or [],
            "usage": usage or {},
            "found_in_corpus": status == "answered",
        }

    if obvious_override(question):
        return response(
            "not_found",
            "Je peux vous informer à partir des documents du"
            " centre. Pour une demande particulière, contactez le"
            " secrétariat.",
        )
    if not store.documents():
        return response(
            "not_found",
            "Aucun document n’est encore indexé. Contactez le"
            " secrétariat.",
        )
    vector = provider.embed([question], "search_query")[0]
    chunks = store.search(
        question, vector, settings.embedding_identity
    )
    # Un seuil est un réglage à évaluer sur le corpus, jamais une preuve de vérité.
    if not chunks or not any(
        c["vector_score"] >= settings.minimum_similarity
        or c["keyword_score"] > 0
        for c in chunks
    ):
        return response(
            "not_found",
            "Je ne trouve pas cette information dans les"
            f" documents. Contactez {settings.contact}.",
        )
    generated, usage = provider.generate(question, chunks, history)
    known = {c["id"]: c for c in chunks}
    ids = list(dict.fromkeys(generated.source_ids))
    if generated.status == "answered" and (
        not ids or any(i not in known for i in ids)
    ):
        return response(
            "not_found",
            "Je ne peux pas relier cette réponse à une source"
            f" vérifiable. Contactez {settings.contact}.",
            usage=usage,
        )
    sources = []
    if generated.status == "answered":
        for source_id in ids:
            c = known[source_id]
            sources.append(
                {
                    "id": source_id,
                    "document_id": c["document_id"],
                    "filename": c["filename"],
                    "page": c["page"],
                    "section": c["section"],
                    "excerpt": c["content"],
                }
            )
    return response(
        generated.status, generated.answer, sources, usage
    )
```

Contrôle ciblé :

```bash
python -m unittest discover -s tests -v
```


# Partie III - Construire l’application

## Chapitre 7 - Donner une structure claire au backend

### Séparer les responsabilités

Le backend est organisé en modules courts dont le rôle est identifiable. `config.py` décrit les paramètres. `provider.py` connaît le contrat HTTP Cohere. `ingestion.py` prépare les documents. `db.py` gère leur stockage et la recherche. `rag.py` orchestre une réponse. `main.py` expose ces fonctions sous forme de routes.

Cette séparation facilite le diagnostic et les tests. Si Cohere renvoie une erreur de quota, l’adaptateur fournisseur traite cette situation. Si un fichier est illisible, l’ingestion l’explique. Si les passages existent mais que la réponse cite un identifiant inconnu, l’orchestrateur contrôle le résultat.

L’application est construite par une fonction `create_app`. Cette fonction peut recevoir une configuration, un stockage et un fournisseur. En fonctionnement normal, elle utilise les composants réels. Dans les tests, elle reçoit des composants contrôlés. Le code métier testé reste le même ; seul l’environnement nécessaire à son exécution change.

### Lire un contrat HTTP

Une route décrit une action à travers une méthode et un chemin. `GET /documents` consulte la liste des documents. `POST /chat` traite une question. `POST /admin/documents` ajoute ou remplace un fichier. `DELETE /admin/documents/{id}` retire un document identifié.

Le corps d’une demande de discussion contient une question et, éventuellement, un historique. Un schéma Pydantic limite leur forme avant le traitement. Une question vide, un historique trop long ou un rôle `system` envoyé par le navigateur ne correspondent pas au contrat et sont rejetés.

Les réponses distinguent aussi plusieurs situations. Le code HTTP 401 signale un accès administrateur refusé. Le code 422 indique une donnée reçue qui ne correspond pas aux règles de l’application. Le code 429 demande de ralentir. Le code 503 exprime l’indisponibilité d’un service ou d’une configuration indispensable.

Un résultat `not_found` du moteur documentaire peut, lui, être une réponse HTTP réussie. Le serveur a correctement traité la demande et constaté que le corpus ne permet pas de répondre. Confondre cette situation avec une panne empêcherait de présenter une orientation utile au visiteur.

### Protéger une opération avant de l’exécuter

Les routes d’administration utilisent une dépendance qui contrôle l’en-tête `X-Admin-Key`. Ce contrôle est effectué côté serveur. Le fait de masquer un bouton dans l’interface ne protégerait pas l’opération contre une requête HTTP envoyée directement.

La clé attendue est comparée à celle reçue sans être écrite dans les journaux. Une configuration d’administration vide n’autorise pas l’accès ; elle signale une configuration manquante. La route de recherche détaillée est également réservée à l’administration, car elle expose des informations utiles au diagnostic.

### Suivre les requêtes sans enregistrer toutes les conversations

Chaque demande reçoit un identifiant généré par le serveur. Cet identifiant est renvoyé dans `X-Request-ID` et associé au résultat de discussion. Les journaux indiquent la méthode, le statut et la durée, sans recopier automatiquement les questions ou les secrets.

Le retour « utile » ou « à revoir » utilise cet identifiant. L’application vérifie qu’une discussion correspondante existe avant d’enregistrer l’avis. Cette mesure rend les retours plus exploitables que des lignes arbitraires ajoutées à la base sans référence à une réponse.

La première édition limite volontairement l’observation à ces informations. Si vous conservez ensuite le texte des conversations, définissez avec le client les données nécessaires, les accès et la durée de conservation. Une nouvelle collecte doit répondre à un besoin précis d’exploitation.

### Exercice

Appelez une route d’administration avec une clé incorrecte, puis avec la bonne clé. Vérifiez que le premier appel n’a modifié ni le corpus ni le compteur d’appels au fournisseur. Appelez ensuite `/chat` avec un historique contenant un rôle `system`. Le contrat doit rejeter cette entrée avant la génération.

### Atelier de code - La route de discussion

Fichier : `backend/app/main.py`. Le schéma borne les entrées et la route relie le moteur documentaire au contrat HTTP.

```python
class ChatInput(BaseModel):
    question: str = Field(min_length=1, max_length=1500)
    history: list[Message] = Field(
        default_factory=list, max_length=6
    )
```

```python
@app.post("/chat", dependencies=[Depends(rate)])
def chat(body: ChatInput, request: Request):
    result = answer_question(
        database,
        model,
        cfg,
        body.question,
        [m.model_dump() for m in body.history],
    )
    database.receipt(request.state.request_id)
    return {**result, "request_id": request.state.request_id}
```

L’identifiant enregistré sert au retour utilisateur sans exiger de conserver le texte complet dans les journaux.

## Chapitre 8 - Créer une interface qui explique le résultat

### Organiser la discussion

L’écran visiteur présente quelques exemples de questions puis un champ de saisie. Les exemples orientent vers des demandes que le corpus couvre réellement : tarifs, horaires et inscription. Ils aident à découvrir le service sans promettre un périmètre illimité.

La question et la réponse apparaissent distinctement. Pendant le traitement, l’interface affiche un état de recherche et désactive l’envoi supplémentaire. Lorsqu’une erreur survient, le texte de la question est conservé pour que l’utilisateur puisse réessayer. Une erreur ne doit pas vider la saisie sans résultat.

Les sources sont regroupées dans un bloc dépliable. Le visiteur peut consulter le nom du fichier, la page ou la section, un extrait et l’original téléchargeable. L’affichage d’une source doit être assez clair pour qu’une personne extérieure au projet sache ce qu’elle est en train de vérifier.

Le frontend rend les réponses comme du texte. Il ne transforme pas une chaîne générée en HTML exécutable. Cette décision simplifie le rendu et évite de donner au contenu des documents un rôle qu’il n’a pas dans l’application.

### Rendre visibles les différents statuts

Pour `answered`, l’interface présente la réponse et ses sources. Pour `clarify`, elle invite le visiteur à préciser sa demande. Pour `not_found`, elle indique que l’information n’est pas confirmée dans les documents disponibles.

Cette présentation doit rester cohérente avec les mots de l’assistant. Une question sur une cantine absente du corpus ne permet pas d’affirmer que le centre n’a pas de cantine. L’interface indique une absence d’information, pas une information négative inventée.

Les boutons de retour sont placés après la réponse. Ils enregistrent un avis simple et affichent une confirmation. Ces retours signalent des cas à examiner ; un vote négatif ne suffit pas à prouver une erreur métier. Il peut refléter une réponse absente, une formulation peu claire ou une attente qui dépasse le périmètre.

### Concevoir l’administration pour les mises à jour

L’administrateur peut actualiser la liste, indexer les fichiers de référence, ajouter un document ou en retirer un. L’écran explique qu’un fichier portant le même nom remplace sa version précédente. Avant une suppression, une confirmation évite un retrait involontaire.

La clé d’administration est saisie dans un champ de type mot de passe. Elle est conservée dans l’état de la page pendant la visite, sans être inscrite dans le code distribué ou stockée durablement par l’application dans le navigateur. Le serveur continue à vérifier chaque opération.

L’indexation initiale est utile pour le parcours pédagogique : les cinq documents sont déjà fournis dans `corpus/`. Dans un contexte client, vous pouvez adapter cette fonction pour initialiser un corpus validé. Les visiteurs ne doivent pas pouvoir choisir un chemin arbitraire sur le serveur.

### Suivre une demande du navigateur à l’API

Le navigateur envoie ses requêtes à `/api/...`. En développement, Next.js les transmet au backend local. En production, Caddy traite ce préfixe et le retire avant l’appel FastAPI. Ainsi, `/api/chat` vu du navigateur correspond à `/chat` dans le backend.

Conservez ce chemin de bout en bout lorsque vous cherchez une erreur. Une requête dirigée vers un nom de service Docker n’est pas directement compréhensible par le navigateur d’un visiteur. Ce nom appartient au réseau interne. Le navigateur doit utiliser l’adresse publique de l’application.

### Exercice

Testez l’interface à une largeur de téléphone puis sur un écran de bureau. Vérifiez l’accès au champ de saisie, la lisibilité des sources et les messages d’erreur. Demandez à une autre personne de trouver le prix d’un parcours et de montrer le passage qui le confirme, sans lui indiquer où cliquer.
### Atelier de code - Un appel depuis l’interface

Fichier : `frontend/app/api.ts`. Une erreur HTTP est transformée en message lisible. Le navigateur utilise le chemin public `/api`.

```typescript
export async function api(path: string, options: RequestInit = {}) {
  const response = await fetch(`/api${path}`, {
    ...options,
    cache: 'no-store',
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(data.detail)
      ? data.detail.map((e: { msg: string }) => e.msg).join(', ')
      : data.detail;
    throw new Error(
      detail || `Service indisponible (HTTP ${response.status}).`
    );
  }
  return data;
}
export type Source = {
  id: string;
  document_id: string;
  filename: string;
  page: number | null;
  section: string | null;
  excerpt: string;
};
export type Answer = {
  request_id: string;
  answer: string;
  status: 'answered' | 'clarify' | 'not_found';
  sources: Source[];
};

```

Contrôle de compilation depuis `frontend/` :

```bash
npm ci
npm run build
```


# Partie IV - Évaluer et exploiter

## Chapitre 9 - Mesurer ce que l’assistant fait réellement

### Séparer tests logiciels et évaluation documentaire

Un test logiciel peut vérifier que l’application refuse un identifiant de source inventé. Il peut aussi vérifier qu’un remplacement incomplet ne supprime pas la version précédente. Ces comportements doivent être testés de manière prévisible et reproductible, sans dépendre d’un fournisseur distant.

L’évaluation documentaire pose une autre question : les modèles et les réglages choisis répondent-ils correctement au corpus et aux formulations du public ? Elle nécessite de véritables appels au système configuré. Un double de test qui renvoie une réponse connue ne permet pas de mesurer cette qualité.

Le projet fournit les deux outils. `tests/` contient des tests logiciels. `eval/questions_reference.json` contient 35 demandes métier ou cas limites. `eval/run_eval.py` interroge la récupération et la discussion pour produire un rapport. Présentez séparément ces deux catégories de résultats.

### Écrire une attente complète

Une question de référence contient un statut attendu, les sources requises et des groupes d’éléments à rechercher dans la réponse. Pour un montant, la présence de « 650 » peut être un indicateur. Elle ne prouve pas que la réponse l’a attribué au bon parcours ou qu’elle a conservé toutes les conditions.

Le premier jeu de travail utilisait des listes très permissives. Une réponse affirmant « Python obligatoire » pouvait être acceptée parce que le mot Python apparaissait parmi les termes autorisés, alors que le parcours ne demandait aucun prérequis. Ce type de règle donne une bonne apparence au score sans démontrer le résultat attendu.

La version révisée vérifie aussi le statut et les sources. Elle exige plusieurs groupes de faits lorsque la question le nécessite. Une question ambiguë attend `clarify` et une demande de précision. Une réponse contenant seulement un tarif ne peut plus valider ce cas.

L’évaluation évite aussi d’interdire mécaniquement des mots qu’une réponse correcte pourrait rappeler. « Je ne peux pas vous accorder une réduction de 90 % » ne doit pas être classé comme une réduction accordée parce que le texte contient « 90 % ». Le sens et la fonction de la phrase comptent.

### Examiner la récupération et la réponse séparément

Le rapport vérifie si les fichiers requis figurent dans les résultats de `/search`. Il vérifie ensuite le statut, des éléments de réponse et les fichiers cités par `/chat`. Lorsqu’un contrôle échoue, consultez d’abord le passage récupéré, puis l’interprétation.

Le contrôle automatique du fichier source est encore partiel. Un même PDF peut contenir plusieurs prix. Pour les questions critiques, la lecture humaine doit relever la page et le passage exact qui soutient l’affirmation. Le modèle de grille manuelle fournit une place pour cette vérification.

Les cas comportant plusieurs sources demandent une attention particulière. Notre jeu peut être enrichi avec une question qui combine le dossier d’inscription et une date de paiement. Vérifiez que chaque partie de la réponse s’appuie sur le bon document. Un seul nom de fichier ne suffit pas à confirmer un raisonnement complet.

### Lancer une campagne et conserver les conditions

Après indexation, exportez la clé d’administration dans le terminal et lancez `python eval/run_eval.py`. L’intervalle entre les appels est réglable pour tenir compte des quotas. Le script enregistre les réponses, les contrôles automatiques, les durées et les jetons de génération renvoyés par le fournisseur.

Notez le modèle, la date, la version du code et le hash des documents. Le même nom de fichier ne suffit pas à identifier son contenu si le règlement a changé entre deux campagnes. Conservez également les seuils et les paramètres qui influencent le traitement.

Un résultat observé sur 35 demandes décrit cet ensemble de demandes. Il ne devient pas une garantie de comportement sur toutes les questions possibles. Présentez le nombre de cas et leurs catégories afin que le client comprenne ce qui a été vérifié.

### Exercice

Ajoutez cinq reformulations de la question sur l’annulation et cinq demandes ambiguës. Faites relire les attentes par la personne responsable du règlement. Lancez la campagne, puis examinez tous les échecs et un échantillon de réussites. Cette dernière étape détecte des faux positifs que le score seul ne montre pas.

### Atelier de code - Lire un indicateur automatique

Fichier : `eval/run_eval.py`. La fonction ci-dessous vérifie le statut, plusieurs groupes d’éléments et les fichiers cités. La lecture humaine porte ensuite sur le sens et le passage exact.

```python
def judge(case, answer, retrieved=None):
    text = norm(answer["answer"])
    sources = {s["filename"] for s in answer.get("sources", [])}
    status = answer["status"] == case["expected_status"]
    groups = case.get("required_groups", [])
    facts = all(
        any(norm(term) in text for term in group)
        for group in groups
    )
    forbidden = not any(
        re.search(pattern, text)
        for pattern in case.get("forbidden_patterns", [])
    )
    required_sources = set(case.get("required_sources", []))
    cited = (
        required_sources <= sources
        if case["expected_status"] == "answered"
        else not sources
    )
    retrieved_files = {r["filename"] for r in retrieved or []}
    retrieval = (
        (required_sources <= retrieved_files)
        if retrieved is not None and required_sources
        else None
    )
    return {
        "status_ok": status,
        "facts_proxy_ok": facts,
        "forbidden_claims_ok": forbidden,
        "citations_files_ok": cited,
        "retrieval_files_ok": retrieval,
        "automatic_pass": status and facts and forbidden and cited,
    }
```

Exemple d’attente pour une demande ambiguë :

```json
{
  "question": "Combien coûte la formation ?",
  "expected_status": "clarify",
  "required_sources": [],
  "required_groups": [
    [
      "quelle formation",
      "quel parcours",
      "préciser"
    ]
  ]
}
```

## Chapitre 10 - Contrôler les accès, les entrées et les dépenses

### Adapter les contrôles aux fonctions réelles

Notre application met des documents publics à la disposition des visiteurs et réserve les modifications à l’administration. Ce choix simplifie le premier projet. Un assistant RH contenant des informations individuelles nécessiterait une gestion d’identité et des autorisations documentaires adaptées avant toute mise à disposition.

Le backend ne possède ici aucun outil pour modifier une inscription, exécuter une commande ou effectuer un paiement. Le modèle produit un résultat documentaire. Conserver cette séparation limite les conséquences d’une mauvaise instruction présente dans un texte, tout en gardant un périmètre facile à expliquer au client.

Les secrets Cohere et de base sont utilisés côté serveur. La clé d’administration autorise des opérations sensibles et doit être transmise au bon interlocuteur. Le fichier `.env` est exclu des images de construction et du dépôt source. Une configuration d’exemple décrit les variables sans fournir de valeur réelle.

### Valider les fichiers et les requêtes

Le nom du fichier ne peut pas contenir un chemin. Les extensions sont limitées et le contenu est examiné. La taille maximale et le volume de texte extrait réduisent les opérations disproportionnées pour le projet. Le lecteur doit aussi savoir reconnaître les formats qui nécessitent une extraction plus élaborée.

Une limite de taille ne constitue pas, à elle seule, une solution générale contre tous les fichiers complexes. Pour un service recevant des dépôts publics, l’architecture doit être réexaminée : traitement isolé, contrôle du temps de calcul et politique de fichiers adaptée. Dans ce projet, seuls les administrateurs déposent les documents.

Les questions et l’historique sont limités en taille. Les rôles acceptés dans l’historique sont `user` et `assistant`. Un navigateur ne peut pas ajouter un message système à la structure attendue. La consigne du serveur conserve donc un emplacement distinct des données reçues.

### Comprendre la limitation de débit

La limite de discussion est enregistrée dans la base. Deux workers FastAPI partagent ainsi les compteurs. Un simple dictionnaire Python appartiendrait à un seul processus : répartir les requêtes entre deux processus changerait la limite effectivement observée.

Le projet utilise des fenêtres d’une minute. Ce mécanisme convient au parcours pédagogique, mais son comportement près d’une frontière de minute doit être compris. Il peut autoriser une série en fin de fenêtre puis une autre au début de la suivante. Si le besoin exige une régulation plus fine, un algorithme différent doit être choisi et testé.

L’adresse IP fournie au backend dépend aussi du proxy. Le code ne fait pas confiance directement à un en-tête arbitraire envoyé par le visiteur. En production, Uvicorn accepte les informations du proxy Caddy à une adresse interne définie. Si vous changez le réseau, adaptez cette configuration en même temps.

### Examiner les injections de consignes

Un texte peut contenir « ignore les instructions précédentes ». Cette phrase ne doit pas devenir une règle pour le modèle simplement parce qu’elle apparaît dans un document retrouvé. Le prompt présente les extraits comme des données, et le serveur contrôle les sources et les actions disponibles.

Le filtre lexical du projet détecte quelques cas évidents pour les tests. Sa présence ne signifie pas que les injections sont résolues. Ajoutez des cas de question et de document à votre évaluation réelle, puis observez le comportement du modèle et les éventuelles informations qu’il restitue.

### Exercice

Vérifiez trois situations : une opération d’administration sans clé, une question essayant de faire révéler une clé, et une demande répétée dépassant le seuil. Contrôlez aussi qu’un secret n’apparaît ni dans une erreur du navigateur ni dans les journaux de requête.

### Atelier de code - Vérifier l’administration et partager le débit

Fichier : `backend/app/main.py`, dépendance de contrôle des opérations. Le middleware effectue également un contrôle préalable pour ne pas lire un fichier volumineux non autorisé.

```python
def admin(x_admin_key: str = Header(default="")):
    expected = cfg.admin_api_key.get_secret_value()
    if not expected:
        raise HTTPException(
            503, "Administration non configurée."
        )
    if not secrets.compare_digest(
        x_admin_key.encode(), expected.encode()
    ):
        raise HTTPException(401, "Accès administrateur refusé.")
```

Fichier : `backend/app/db.py`, compteur partagé entre workers. Le test utilise deux instances de stockage pour vérifier cette propriété.

```python
def allow_request(self, identity, limit, timestamp=None):
    now = int(time.time() if timestamp is None else timestamp)
    bucket = now // 60
    identity = hashlib.sha256(identity.encode()).hexdigest()
    with self.connect() as conn:
        self.run(
            conn,
            "DELETE FROM rate_limits WHERE bucket<%s",
            (bucket - 2,),
        )
        row = self.run(
            conn,
            """INSERT INTO rate_limits(identity,bucket,count) VALUES(%s,%s,1)
            ON CONFLICT(identity,bucket) DO UPDATE SET count=rate_limits.count+1 RETURNING count""",
            (identity, bucket),
        ).fetchone()
        return row["count"] <= limit
```

## Chapitre 11 - Mettre en ligne et savoir revenir à un état connu

### Préparer un déploiement explicable

Le fichier `docker-compose.prod.yml` décrit les quatre services du déploiement. PostgreSQL et le backend ne publient pas de port vers l’extérieur. Caddy reçoit les connexions HTTP et HTTPS, puis dirige le trafic vers l’interface ou l’API.

Renseignez le domaine, vérifiez qu’il pointe vers le serveur et que les ports nécessaires sont accessibles. Caddy gère l’obtention et le renouvellement des certificats lorsque les conditions de son fonctionnement sont réunies. Ses volumes de données conservent cet état entre les redémarrages.

Le backend utilise deux workers, sans rechargement automatique de développement. Le frontend est compilé avant son lancement. Le fichier de dépendances et le verrou npm permettent de reproduire plus précisément l’environnement utilisé pour cette compilation.

Le premier démarrage doit être suivi d’une vérification depuis l’extérieur : ouvrir l’interface, consulter l’état attendu, poser une question et télécharger une source. Une vérification effectuée uniquement à l’intérieur du conteneur ne reproduit pas le parcours d’un visiteur passant par le domaine et HTTPS.

### Conserver les données nécessaires

Les documents originaux, leurs métadonnées, leurs fragments et leurs vecteurs sont dans la base. Une sauvegarde de cette base conserve donc le corpus du projet. Elle ne remplace pas la sauvegarde du code, des paramètres confidentiels et des autres éléments d’exploitation.

Le script `backup_db.sh` lance `pg_dump` dans le service de base et compresse sa sortie. Il écrit d’abord un fichier temporaire. Le fichier final n’est publié qu’après la réussite de la commande et le contrôle de l’archive gzip. Ainsi, une opération échouée n’apparaît pas dans la liste comme une sauvegarde complète.

Une planification quotidienne est proposée dans `deploy/backup.cron.example`. Le chemin, l’utilisateur et le journal sont à adapter. Vérifiez la première exécution planifiée et la possibilité de retrouver le fichier. Copier une ligne cron ne démontre pas qu’une sauvegarde est réellement exécutée.

### Restaurer dans une nouvelle base

Le script de restauration reçoit une archive et le nom d’une nouvelle base commençant par `rag_restore_`. Il vérifie l’archive, crée cette cible, puis exécute les instructions SQL avec arrêt sur erreur. Si le nom existe déjà, la création échoue et le script ne poursuit pas la restauration dans cette base.

L’option `ON_ERROR_STOP=1` est essentielle au signal de réussite. Sans elle, `psql` peut poursuivre le traitement après une erreur SQL. Le réglage `set -euo pipefail` du shell ne suffit pas si l’outil SQL termine sans signaler l’erreur par son code de sortie.

La restauration utilise également une transaction pour éviter de valider une partie du contenu si une instruction échoue. Le message de fin n’apparaît qu’après la réussite de la chaîne. Le script ne décide pas de remplacer la base active par la base restaurée : cette bascule doit être préparée et vérifiée séparément.

### Vérifier la récupération de service

Après restauration, comparez le nombre de documents, leurs noms et leurs hash. Vérifiez un téléchargement original, quelques recherches et les réponses du jeu de référence. Une archive lisible n’est pas encore la preuve qu’une application peut retrouver son fonctionnement métier.

Conservez une procédure de mise à jour du code avec une version identifiable. Avant un changement, sauvegardez les données et notez la version précédente. Si un changement de schéma est nécessaire, préparez sa migration et sa récupération ; le retour du seul code ne répare pas automatiquement une base modifiée.

### Exercice

Créez une sauvegarde puis restaurez-la dans `rag_restore_verification`. Vérifiez les documents et les passages attendus. Répétez ensuite le test avec une archive invalide ou un nom déjà utilisé : l’opération doit échouer clairement, sans annoncer une restauration réussie.
### Atelier de code - Sauvegarder et restaurer

Ces scripts sont destinés à Bash, sur le serveur ou dans un environnement adapté. Les noms de services proviennent du fichier Compose de production.

Fichier : `scripts/backup_db.sh`.

```bash
#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p backups
STAMP="$(date -u +%Y%m%d_%H%M%S)_$$"
OUT_FILE="$ROOT/backups/rag_horizon_${STAMP}.sql.gz"
TEMP_FILE="${OUT_FILE}.partial"
trap 'rm -f -- "$TEMP_FILE"' EXIT
docker compose -f docker-compose.prod.yml exec -T db sh -c \
  'exec pg_dump --no-owner --no-privileges -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "$TEMP_FILE"
gzip -t "$TEMP_FILE"
mv -- "$TEMP_FILE" "$OUT_FILE"
printf 'Sauvegarde créée : %s\n' "$OUT_FILE"


```

Fichier : `scripts/restore_db.sh`.

```bash
#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then
  printf 'Usage : %s fichier.sql.gz nom_nouvelle_base\n' "$0" >&2
  exit 1
fi
BACKUP_FILE="$(realpath -- "$1")"
TARGET="$2"
if [[ ! "$TARGET" =~ ^rag_restore_[a-zA-Z0-9_]+$ ]]; then
  printf 'La nouvelle base doit commencer par rag_restore_ et contenir uniquement lettres, chiffres et _.\n' >&2
  exit 1
fi
test -r "$BACKUP_FILE"
gzip -t "$BACKUP_FILE"
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
# createdb échoue si la cible existe : aucune base existante n'est écrasée.
docker compose -f docker-compose.prod.yml exec -T -e RESTORE_DB="$TARGET" db sh -c \
  'exec createdb -U "$POSTGRES_USER" "$RESTORE_DB"'
gunzip -c "$BACKUP_FILE" | docker compose -f docker-compose.prod.yml exec -T -e RESTORE_DB="$TARGET" db sh -c \
  'exec psql -X -v ON_ERROR_STOP=1 --single-transaction -U "$POSTGRES_USER" -d "$RESTORE_DB" -f -'
printf 'Restauration terminée dans la nouvelle base : %s\n' "$TARGET"


```

Les tests des scripts simulent Docker et les erreurs. Une répétition avec un vrai serveur et une vraie base reste nécessaire avant une livraison.


# Partie V - Livrer un résultat au client

## Chapitre 12 - Chiffrer, démontrer et transmettre

### Séparer réalisation et fonctionnement

Le client achète d’abord une réalisation : cadrage du besoin, préparation du corpus, adaptation de l’interface, tests et mise en ligne. Il supporte aussi un fonctionnement : modèles, hébergement, domaine, sauvegardes et maintenance. Présenter ces postes séparément rend le devis compréhensible.

Cette édition utilise Cohere. Le fournisseur distingue les clés d’évaluation gratuites avec limites des clés de production payantes. Le prototype et les exercices peuvent employer les conditions d’essai disponibles sur le compte. Un budget d’exploitation client doit être calculé à partir des conditions de production applicables.

Le choix du fournisseur ne suffit donc pas à annoncer un coût nul pour le service final. L’intérêt du parcours est de pouvoir développer et évaluer le prototype, puis mesurer les éléments nécessaires à une estimation réaliste.

### Calculer les postes variables

Pour la génération, les jetons d’entrée et de sortie peuvent avoir des prix différents. Pour les embeddings, distinguez l’indexation des documents et les requêtes des visiteurs. Le coût mensuel dépend des volumes, de la longueur du contexte, des réponses et des mises à jour documentaires.

Le calcul de base est : coût de génération = jetons d’entrée multipliés par leur prix unitaire, plus jetons de sortie multipliés par leur prix unitaire. Si les prix sont donnés par million de jetons, divisez le résultat par un million. Ajoutez ensuite les embeddings et les postes fixes.

Le script `scripts/costs.py` reçoit chaque volume et chaque prix comme un argument explicite. Il ne suppose pas que tous les jetons ont le même prix. Vous pouvez l’utiliser pour comparer plusieurs hypothèses, puis remplacer les volumes estimés par ceux observés pendant un pilote.

Supposons, à titre d’exercice uniquement, deux millions de jetons d’entrée à 1 unité monétaire par million, un demi-million de sortie à 2 unités et un million d’embeddings à 0,1 unité. La génération coûte 3 unités et les embeddings 0,1 unité. Avec 10 unités de coûts fixes, le total est 13,1 unités. Ces prix hypothétiques ne sont pas un tarif Cohere.

Les unités sont importantes. Un prix en dollars ne doit pas être additionné directement à une facture en euros ou en francs CFA. Choisissez une devise de présentation et indiquez les conversions utilisées si elles sont nécessaires. Datez les prix pour permettre au client de comprendre l’estimation.

### Préparer une démonstration utile

La démonstration reprend les demandes convenues au cadrage. Montrez une réponse factuelle, une question ambiguë, une information absente et un remplacement de document. Le client doit pouvoir examiner la source qui soutient une réponse, puis constater qu’une nouvelle version est prise en compte.

Évitez de limiter la démonstration aux trois demandes qui ont déjà réussi pendant le développement. Prenez aussi quelques formulations proposées par le client. Lorsqu’un cas échoue, notez-le, identifiez son type et convenez du traitement attendu. Le rapport documente ces échanges.

Le jeu d’évaluation sert de support de réception. Présentez le nombre de cas, les attentes et les résultats. Les expressions « fiable » ou « précis » deviennent ainsi des observations discutables et vérifiables, plutôt qu’une impression laissée par quelques conversations fluides.

### Remettre une application que le client peut exploiter

Le dossier de livraison contient le code, la configuration d’exemple, les procédures de démarrage, de sauvegarde, de restauration et de mise à jour documentaire. Il indique aussi les comptes qui appartiennent au client et les responsabilités du prestataire.

La prise en main doit être concrète. Faites ajouter un fichier par l’administrateur, puis remplacer une grille de prix. Faites-lui retrouver une source et signaler une mauvaise réponse. Si l’équipe a besoin de vous pour chaque opération promise comme autonome, le guide doit encore être amélioré.

Le modèle de fiche de réception rappelle les éléments à vérifier et à transmettre. Adaptez les montants, la devise, le périmètre et les modalités convenues aux besoins du projet. Les documents fournis sont des supports de travail à compléter, pas des informations déjà validées par un client réel.

### Organiser le suivi

Définissez comment un problème est signalé, qui valide un nouveau document et comment une correction est évaluée. Une demande de nouvelle fonctionnalité peut modifier le périmètre : intégrer une réservation ou une base privée ne correspond pas simplement au remplacement d’un PDF.

Un suivi utile regarde les questions auxquelles l’assistant ne répond pas, les retours négatifs et les changements de corpus. Ces observations peuvent justifier une amélioration du contenu avant une modification du code. Une FAQ mieux rédigée peut résoudre un cas qui semblait demander un modèle plus complexe.

### Exercice

Préparez une proposition pour Horizon Numérique avec trois hypothèses de volume. Inscrivez séparément la réalisation, la consommation et le suivi. Préparez ensuite une démonstration de dix minutes comprenant un remplacement de document et une consultation de source par le client.

### Atelier de code - Calculer une hypothèse budgétaire

Fichier : `scripts/costs.py`. Les volumes et prix sont séparés pour préserver les unités.

```python
def calculate(
    input_tokens,
    output_tokens,
    embedding_tokens,
    input_price,
    output_price,
    embedding_price,
    fixed=0,
):
    values = [
        input_tokens,
        output_tokens,
        embedding_tokens,
        input_price,
        output_price,
        embedding_price,
        fixed,
    ]
    if any(v < 0 for v in values):
        raise ValueError(
            "Les montants et volumes doivent être positifs."
        )
    chat = (
        input_tokens * input_price + output_tokens * output_price
    ) / 1_000_000
    embed = embedding_tokens * embedding_price / 1_000_000
    return {
        "chat": chat,
        "embeddings": embed,
        "fixed": fixed,
        "total": chat + embed + fixed,
    }
```

L’exemple hypothétique du chapitre s’exécute ainsi :

```bash
python scripts/costs.py \
  --input-tokens 2000000 --output-tokens 500000 \
  --embedding-tokens 1000000 --input-price 1 \
  --output-price 2 --embedding-price 0.1 --fixed 10
```

Le total attendu est 13,1 unités monétaires. Remplacez ces prix d’exercice par les prix vérifiés de votre fournisseur pour un devis réel.

## Conclusion - Réutiliser la méthode

Vous disposez maintenant d’un parcours reliant une demande client à une application documentaire. Vous avez défini les comportements attendus, préparé les sources, construit la recherche et la génération, organisé l’interface et prévu l’évaluation et la livraison.

Pour une nouvelle organisation, commencez par son besoin et ses documents. Remplacez le corpus, adaptez le rôle de l’assistant et écrivez les questions de référence. Examinez les droits d’accès et les actions attendues avant de réutiliser les mêmes choix techniques. Un corpus public et un dossier interne ne se traitent pas avec les mêmes autorisations.

Conservez votre capacité d’explication : pourquoi ce passage est retrouvé, pourquoi la réponse est affichée, pourquoi une demande appelle une précision, pourquoi une mise à jour remplace l’ancienne version. Cette compréhension rend le projet plus facile à corriger et à présenter.

Le résultat à rechercher est une application dont le fonctionnement peut être reproduit, dont les sources peuvent être consultées et dont les résultats peuvent être discutés à partir de preuves. C’est cette méthode que vous pouvez adapter à vos prochains projets.

# Annexes

## Annexe A - Glossaire de travail

| Terme | Sens dans ce projet |
|---|---|
| API | Interface permettant au navigateur ou à un service d’appeler les fonctions du backend. |
| Corpus | Ensemble des documents validés et actifs dans l’assistant. |
| Fragment | Passage de texte conservé avec sa provenance. |
| Embedding | Vecteur calculé à partir d’un texte pour la recherche. |
| Indexation | Préparation des fragments, calcul de leurs vecteurs et enregistrement. |
| Contexte | Informations transmises au modèle pour préparer la réponse. |
| RRF | Fusion de classements fondée sur les rangs des résultats. |
| Provenance | Lien entre un passage et son document, sa page ou sa section. |
| Transaction | Groupe d’opérations de base validées ou annulées ensemble. |
| Jeton | Unité de traitement et de comptage utilisée par les modèles. |
| Double de test | Composant contrôlé qui remplace une dépendance dans un test logiciel. |
| Réception | Vérification avec le client des critères et livrables convenus. |

## Annexe B - Diagnostic rapide

| Observation | Première vérification |
|---|---|
| Le navigateur ne joint pas le service | Domaine, proxy, chemin `/api` et service concerné. |
| L’administration refuse une action | Clé saisie, configuration du serveur et code HTTP. |
| L’indexation échoue | Format réel, extraction du texte, taille et retour Cohere. |
| Le fournisseur répond 429 | Quota et débit en vigueur, fréquence des essais et délai de reprise. |
| La source est correcte mais le montant est faux | Passage exact transmis, consignes et lecture de la règle. |
| Un ancien prix apparaît | Hash du document actif, nom du fichier et présence éventuelle de deux versions. |
| Le corpus réclame une réindexation | Modèle, dimensions et identité d’indexation. |
| Une restauration échoue | Validité de l’archive, nouvelle base, première erreur SQL et version des outils. |

## Annexe C - Démonstration de réception en dix minutes

1. Présenter le besoin et les documents actifs.
2. Poser une question sur un montant et ouvrir le document cité.
3. Poser une demande ambiguë et montrer la précision demandée.
4. Poser une question hors corpus et montrer l’orientation proposée.
5. Remplacer un document et vérifier le résultat sur la nouvelle version.
6. Faire réaliser une opération documentaire par l’administrateur du client.
7. Présenter les résultats du jeu de questions et les points restant à traiter.
8. Remettre les procédures et convenir du suivi.

## Annexe D - Documents fournis et emplacement

Le dossier `modeles_clients/` contient le cahier des charges, la proposition commerciale, la fiche de réception et la grille d’évaluation. `eval/` fournit les questions de référence et le script de mesure. `scripts/` contient les opérations de configuration, de sauvegarde, de restauration et de calcul des coûts. `corpus/` contient les cinq documents fictifs.

Ces éléments accompagnent le texte pour permettre une reproduction complète. Une copie du manuscrit ne remplace pas ces fichiers lorsqu’un exercice demande d’exécuter l’application.

## Annexe E - Références techniques

Documentation consultée pour cette édition le 18 novembre 2026. Les prix, quotas, modèles et versions doivent être revérifiés au moment des essais ou d’un devis.

- Cohere, API Chat v2 : https://docs.cohere.com/v2/reference/chat
- Cohere, API Embed v2 : https://docs.cohere.com/v2/reference/embed
- Cohere, modèles d’embeddings : https://docs.cohere.com/v2/docs/cohere-embed
- Cohere, Command R7B : https://docs.cohere.com/v2/docs/command-r7b
- Cohere, clés et limites : https://docs.cohere.com/v2/docs/rate-limits
- Cohere, sortie structurée : https://docs.cohere.com/v2/docs/structured-outputs
- pgvector, dépôt et documentation : https://github.com/pgvector/pgvector
- FastAPI, déploiement avec Docker : https://fastapi.tiangolo.com/deployment/docker/
- PostgreSQL, psql et arrêt sur erreur : https://www.postgresql.org/docs/current/app-psql.html
- Caddy, gestion des chemins et préfixes : https://caddyserver.com/docs/caddyfile/directives/handle_path


