# Instructions pour Antigravity — Tunnel de vente KORYXA

## Mission et offre

Construis le tunnel de vente et l’espace client de « Créer et livrer son premier assistant IA », dans l’environnement KORYXA existant.

Prix retenu : **11 000 F CFA (XOF), paiement unique**, pour le pack complet. Configure le montant côté serveur et conserve le prix payé sur chaque commande. Affiche ce prix sans fausse réduction, compteur artificiel ou témoignage inventé.

Public : développeurs et freelances francophones connaissant les bases de Python.
Promesse : « Créez un assistant IA que vous savez tester et livrer. »

Le pack existant contient le livre de 68 pages, le code du projet Cohere, les documents d’exercice, les questions d’évaluation, les scripts et les modèles de livraison client. L’espace client et l’assistance sont les fonctions à construire maintenant.

## Partir de l’existant

Inspecte d’abord le dépôt, ses instructions, son authentification, son intégration de paiement et ses conventions. Réutilise la stack, les composants et les services existants. Évite de reconstruire ce qui fonctionne.

L’utilisateur possède déjà son agrégateur de paiement : réutilise-le. Ne propose pas un nouvel agrégateur. Si la configuration ou la documentation est absente, prépare l’adaptateur et les tests, puis indique précisément les seules informations manquantes.

Pour l’IA, utilise Cohere côté serveur. Les clés restent dans les variables d’environnement.

## Ressources à joindre à ce brief

- `Page_presentation_KORYXA_Assistants_IA.md` : texte de présentation existant.
- `Creer_et_livrer_son_premier_assistant_IA_Cohere.pdf` : livre complet.
- `Assistant_IA_RAG_Cohere_Projet.zip` : projet et outils pratiques.
- `KORYXA_Assistant_IA_Extrait.pdf` : extrait gratuit.
- `Kit_lancement_KORYXA_Assistants_IA.zip` : supports de lancement.

Ne suppose pas que ces fichiers sont déjà présents dans le dépôt. Utilise les fichiers effectivement fournis et signale les ressources manquantes.

## Page de vente

Créer une page en français, soignée et adaptée au mobile, intégrée à KORYXA. Elle doit présenter :

1. La promesse et un bouton « Obtenir le pack — 11 000 F CFA ».
2. La vidéo de l’auteur avec sa démonstration sur PC.
3. Le résultat visé et les étapes d’apprentissage.
4. Le contenu exact du pack, avec aperçu.
5. Les prérequis Python et l’usage de Cohere.
6. L’extrait gratuit, les questions fréquentes et l’accès au paiement.

Prévoir un emplacement remplaçable pour la vidéo tant qu’elle n’est pas fournie. Les illustrations et captures doivent correspondre au produit réel. Les frais éventuels d’utilisation de Cohere ou d’hébergement du projet du lecteur ne sont pas inclus dans le prix du pack.

## Achat et activation

Limiter les étapes avant le paiement et recueillir l’adresse e-mail nécessaire à la livraison. Réutiliser le compte existant ou permettre son activation sécurisée après achat.

- Créer la commande côté serveur, puis ouvrir le paiement avec l’agrégateur existant.
- Gérer les états en attente, payé, échoué et annulé.
- Le retour du navigateur affiche l’état de la commande ; il ne constitue jamais une preuve de paiement.
- Activer l’accès uniquement après vérification serveur auprès de l’agrégateur, par son mécanisme officiel de notification et/ou de consultation.
- Vérifier l’authenticité de la notification, la référence, le bénéficiaire, le montant et la devise attendus.
- Rendre les notifications répétées sans effet supplémentaire : une transaction ne doit pas produire plusieurs achats, accès ou messages.
- Après validation, ouvrir l’espace client et envoyer le message d’accès. Une erreur d’envoi ne doit pas annuler un achat payé.

Conserver les ressources payantes hors des répertoires publics. Chaque téléchargement vérifie le compte et son droit d’accès ; les éventuels liens signés expirent. Un lien vers l’extrait gratuit peut être public.

## Espace client et accompagnement

L’acheteur doit retrouver son achat, télécharger les fichiers et suivre un parcours guidé :

1. Télécharger et préparer l’environnement.
2. Configurer Cohere.
3. Lancer le projet.
4. Charger les documents d’exemple.
5. Poser les questions et vérifier les sources.
6. Tester, adapter et préparer la livraison.

S’appuyer sur le README et le livre pour les commandes et prérequis exacts. Enregistrer les étapes réellement validées par le client, sans confondre téléchargement et installation réussie.

Créer une assistance avec Cohere, fondée sur le livre et la documentation du projet. Elle doit citer ses références, demander les informations utiles au diagnostic et permettre l’ouverture d’un ticket si elle ne résout pas le problème. Les clients doivent pouvoir consulter leurs tickets.

Ne promettre ni disponibilité humaine permanente, ni réponse instantanée d’un conseiller. Prévoir des limites d’usage configurables pour l’assistance automatisée.

## Automatisation et administration

Prévoir des messages de service : accès après achat, aide au démarrage, puis suivi selon la progression. Proposer des délais configurables, par exemple J+2, J+5 et J+10. Un client ayant terminé une étape ne doit pas recevoir une relance lui demandant de la commencer.

Exécuter ces tâches avec un mécanisme durable, doté de reprises et de protections contre les doublons. Réutiliser le service d’e-mail existant ; s’il manque, préparer l’interface et expliciter la configuration restante. Ne pas présenter un envoi simulé comme un envoi réel.

L’administration doit permettre de consulter commandes, paiements, droits d’accès, progression, messages et tickets. Protéger ces fonctions par le rôle administrateur.

Mesurer les visites, passages au paiement, paiements effectivement confirmés et téléchargements, sans journaliser les secrets ou le contenu confidentiel des échanges.

## Validation et livraison

Vérifier le parcours sur ordinateur et mobile. Ajouter les tests utiles aux fonctions de paiement et d’accès, notamment :

- paiement confirmé et livraison correcte ;
- notification répétée sans double activation ;
- montant incorrect, notification invalide ou simple retour navigateur sans activation ;
- téléchargement interdit à un visiteur et à un autre client ;
- reprise après échec d’e-mail et relances conditionnées à la progression.

Livrer le code, les migrations, un fichier d’exemple des variables d’environnement sans secrets, les instructions de configuration et un compte rendu court : fichiers modifiés, vérifications effectuées, intégrations réellement testées et éléments restant à connecter.

Avancer avec les informations disponibles. Garder une distinction explicite entre démonstration, intégration en environnement de test et fonctionnement réel.

