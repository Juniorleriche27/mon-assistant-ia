# Kit de lancement KORYXA - Assistants IA

## Lire et présenter

- Dossier_lancement_KORYXA_Assistants_IA.pdf : synthèse de l’offre, du message et du lancement.
- Dossier_lancement_KORYXA_Assistants_IA.md : dossier détaillé modifiable.
- KORYXA_Assistant_IA_Extrait.pdf : extrait de découverte ; couverture, chapitres 1 et 2 du guide actuel et présentation de la suite.
- Page_presentation_KORYXA_Assistants_IA.md : texte de présentation à intégrer à une page.
- Textes_lancement_KORYXA.md : publication, vidéo courte et pitch.

Le tarif et le parcours d’achat sont à fixer pour la mise en vente. Les supports ont été préparés pour relecture.

## Répéter la démonstration

Utiliser le projet assistant-rag-horizon déjà fourni avec le guide. Configurer Cohere sur la machine de démonstration et indexer le corpus.

1. Envoyer demo/avant/02_tarifs_et_financements.pdf dans l’administration.
2. Dans une conversation neuve, demander le tarif total d’Analyse de Données : attendu 650 euros, source grille tarifaire.
3. Ouvrir la source et vérifier le passage.
4. Poser « Combien coûte la formation ? » : une précision sur la formation est attendue.
5. Envoyer demo/apres/02_tarifs_et_financements.pdf. Le nom reste identique pour remplacer le document.
6. Attendre la fin de l’indexation, vérifier le nouveau hash, puis actualiser l’écran de conversation.
7. Reposer la question : attendu 700 euros et la nouvelle source. Les tranches de la nouvelle grille sont 250, 250 et 200 euros.

Les deux versions sont fictives. Les montants attendus sont des critères d’essai, pas un compte rendu d’exécution réelle. demo/versions_documents.json identifie chaque fichier par son hash SHA-256.

## Recréer les supports

Placer ce dossier à côté du projet assistant-rag-horizon. Installer requirements-supports.txt, puis lancer :

python preparer_supports.py --book ../assistant-rag-horizon/book/Creer_et_livrer_son_premier_assistant_IA_Cohere.pdf

Le générateur utilise les polices du projet et le manuscrit de présentation fourni ici. Les PDF à lire sont déjà inclus dans l’archive.
