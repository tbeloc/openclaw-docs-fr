---
title: "Rapport de Maturité Discord"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité Discord

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (71%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (71%)`
- Fonctionnalités LTS : `4/6`

## Résumé

Ce rapport promeut les preuves de maturité archivées `discord` de `/Users/kevinlin/tmp/maturity/discord` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                                       | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Configuration et Opérations des Canaux](bot-setup-and-account-configuration.md)                | ✅  | `Beta (74%)`  | `Beta (71%)`  | `Beta (74%)`  | Configuration de l'application et du bot, Configuration du jeton et de l'ID d'application, Assistant de configuration et inspection de compte, Vérifications de statut, doctor et intent, Configuration de bot multi-compte, Démarrage du moniteur de compte, Cycle de vie WebSocket de la passerelle, Gestion de la reconnexion et du heartbeat, Limites de débit et métadonnées de passerelle, Récupération de statut, sonde et moniteur de santé |
| [Accès et Identité](dm-pairing-and-sender-authorization.md)                                    | ✅  | `Beta (74%)`  | `Beta (72%)`  | `Beta (74%)`  | Modes de politique DM, Héritage de liste blanche, Approbation de code d'appairage, Autorisation de l'expéditeur, Autorisation du groupe d'accès, Autorisation de DM de groupe                                                                                                                                                                    |
| [Routage et Livraison des Conversations](guild-channel-routing-and-session-isolation.md)       | ✅  | `Beta (74%)`  | `Beta (72%)`  | `Beta (74%)`  | Admission de guilde et de canal, Gating de mention, Isolation de clé de session, Routage configuré et à l'exécution, Visibilité du contexte entrant, Publications de threads de canal forum et média, Actions de thread, Analyse de cible, Résolution du contexte de thread, Routage lié au thread, Routage de l'agent ACP, Cycle de vie du routage                |
| [Médias et Contenu Enrichi](media-attachments-and-voice-message-handling.md)                   | ✅  | `Beta (74%)`  | `Beta (72%)`  | `Beta (74%)`  | Médias et Contenu Enrichi                                                                                                                                                                                                                                                                                                                       |
| [Contrôles Natifs et Approbations](native-slash-commands-components-and-interactive-callbacks.md) | ❌  | `Alpha (58%)` | `Beta (72%)`  | `Alpha (58%)` | Enregistrement de commande slash native, Exécution de commande slash native, Commandes de sélecteur de modèle, Messages de composants v2, TTL de rappel                                                                                                                                                                                           |
| [Voix et Appels en Temps Réel](realtime-discord-voice-channels.md)                             | ❌  | `Beta (74%)`  | `Alpha (66%)` | `Beta (74%)`  | Cycle de vie du canal vocal, Rejoindre automatiquement et suivre les utilisateurs, Modes vocaux en temps réel, Gestion du réveil, de l'intrusion et de l'écho, Récupération du codec vocal et DAVE                                                                                                                                                |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, live, ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et de flux runtime réel sont des entrées de couverture
  uniquement ; elles ne relèvent ni n'abaissent la qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement
  l'ensemble de capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations des canaux

Ancres de recherche : Configuration de l'application et du bot, Configuration du jeton et de l'ID d'application, Assistant de configuration et inspection de compte, Vérifications de statut, doctor et intent, Configuration de bot multi-compte, Démarrage du moniteur de compte, Cycle de vie WebSocket de la passerelle, Gestion de la reconnexion et du heartbeat, Limites de débit et métadonnées de passerelle, Récupération de statut, probe et health-monitor.

Note de catégorie : [Configuration et opérations des canaux](bot-setup-and-account-configuration.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Configuration de l'application et du bot : Couvre la configuration de l'application et du bot dans les conseils de création d'application/bot Discord, la configuration du jeton du bot et de `applicationId`, la résolution des jetons env et SecretRef, l'assistant de configuration/inspection de compte, et le comportement associé de configuration du bot et du compte.
- Configuration du jeton et de l'ID d'application : Couvre la configuration du jeton et de l'ID d'application dans les conseils de création d'application/bot Discord, la configuration du jeton du bot et de `applicationId`, la résolution des jetons env et SecretRef, l'inspection de l'assistant de configuration/compte, et le comportement associé de configuration du bot et du compte.
- Assistant de configuration et inspection de compte : Couvre l'assistant de configuration et l'inspection de compte dans les conseils de création d'application/bot Discord, la configuration du jeton du bot et de `applicationId`, la résolution des jetons env et SecretRef, l'inspection de l'assistant de configuration/compte, et le comportement associé de configuration du bot et du compte.
- Vérifications de statut, doctor et intent : Couvre les vérifications de statut, doctor et intent dans les conseils de création d'application/bot Discord, la configuration du jeton du bot et de `applicationId`, la résolution des jetons env et SecretRef, l'inspection de l'assistant de configuration/compte, et le comportement associé de configuration du bot et du compte.
- Configuration de bot multi-compte : Couvre la configuration de bot multi-compte dans les conseils de création d'application/bot Discord, la configuration du jeton du bot et de `applicationId`, la résolution des jetons env et SecretRef, l'inspection de l'assistant de configuration/compte, et le comportement associé de configuration du bot et du compte.
- Démarrage du moniteur de compte : Couvre le démarrage du moniteur de compte dans le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/heartbeat, et le comportement associé du moniteur de passerelle et du cycle de vie d'exécution.
- Cycle de vie WebSocket de la passerelle : Couvre le cycle de vie WebSocket de la passerelle dans le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/heartbeat, et le comportement associé du moniteur de passerelle et du cycle de vie d'exécution.
- Gestion de la reconnexion et du heartbeat : Couvre la gestion de la reconnexion et du heartbeat dans le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/heartbeat, et le comportement associé du moniteur de passerelle et du cycle de vie d'exécution.
- Limites de débit et métadonnées de passerelle : Couvre les limites de débit et les métadonnées de passerelle dans le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/heartbeat, et le comportement associé du moniteur de passerelle et du cycle de vie d'exécution.
- Récupération de statut, probe et health-monitor : Couvre la récupération de statut, probe et health-monitor dans le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur d'exécution, le client de passerelle WebSocket, la gestion de la reconnexion/heartbeat, et le comportement associé du moniteur de passerelle et du cycle de vie d'exécution.

Documentation principale :

- `docs/channels/discord.md`
- `docs/plugins/reference/discord.md`
- `docs/install/fly.md`
- `docs/tools/slash-commands.md`
- `docs/gateway/health.md`
- `docs/cli/channels.md`
- `docs/gateway/config-channels.md`

### 2. Accès et identité

Ancres de recherche : Modes de politique DM, Héritage de liste d'autorisation, Approbation par code d'appairage, Autorisation de l'expéditeur, Autorisation du groupe d'accès, Autorisation de groupe DM.

Note de catégorie : [Accès et identité](dm-pairing-and-sender-authorization.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Modes de politique DM : Couvre les modes de politique DM dans les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open`, et `disabled`. Résolution canonique et héritée de `allowFrom` dans la configuration Discord de haut niveau, et le comportement associé d'appairage DM et d'autorisation de l'expéditeur.
- Héritage de liste d'autorisation : Couvre l'héritage de liste d'autorisation dans les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open`, et `disabled`. Résolution canonique et héritée de `allowFrom` dans la configuration Discord de haut niveau, et le comportement associé d'appairage DM et d'autorisation de l'expéditeur.
- Approbation par code d'appairage : Couvre l'approbation par code d'appairage dans les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open`, et `disabled`. Résolution canonique et héritée de `allowFrom` dans la configuration Discord de haut niveau, et le comportement associé d'appairage DM et d'autorisation de l'expéditeur.
- Autorisation de l'expéditeur : Couvre l'autorisation de l'expéditeur dans les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open`, et `disabled`. Résolution canonique et héritée de `allowFrom` dans la configuration Discord de haut niveau, et le comportement associé d'appairage DM et d'autorisation de l'expéditeur.
- Autorisation du groupe d'accès : Couvre l'autorisation du groupe d'accès dans les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open`, et `disabled`. Résolution canonique et héritée de `allowFrom` dans la configuration Discord de haut niveau, et le comportement associé d'appairage DM et d'autorisation de l'expéditeur.
- Autorisation de groupe DM : Couvre l'autorisation de groupe DM dans les modes `dmPolicy` de message direct Discord : `pairing`, `allowlist`, `open`, et `disabled`. Résolution canonique et héritée de `allowFrom` dans la configuration Discord de haut niveau, et le comportement associé d'appairage DM et d'autorisation de l'expéditeur.

Documentation principale :

- `docs/channels/discord.md`
- `docs/channels/pairing.md`
- `docs/channels/access-groups.md`
- `docs/channels/groups.md`

### 3. Routage et livraison des conversations

Ancres de recherche : Admission de guilde et de canal, Gating par mention, Isolation de clé de session, Liaisons configurées et d'exécution, Visibilité du contexte entrant, Publications de threads de canal forum et média, Actions de thread, Analyse de cible, Résolution du contexte de thread, Routage de session lié au thread, Liaisons ACP, Cycle de vie de liaison.

Note de catégorie : [Routage et livraison des conversations](guild-channel-routing-and-session-isolation.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Admission de guilde et de canal : Couvre l'admission de guilde et de canal dans la liste d'autorisation de guilde et l'admission de `groupPolicy` pour les canaux et threads de guilde Discord. `requireMention`, prévention de boucle de bot, contournements de commande/mention, et historique d'événement de salle sans mention. Canal, et le comportement associé de routage de canal de guilde et d'isolation de session.
- Gating par mention : Couvre le gating par mention dans la liste d'autorisation de guilde et l'admission de `groupPolicy` pour les canaux et threads de guilde Discord. `requireMention`, prévention de boucle de bot, contournements de commande/mention, et historique d'événement de salle sans mention. Canal, et le comportement associé de routage de canal de guilde et d'isolation de session.
- Isolation de clé de session : Couvre l'isolation de clé de session dans la liste d'autorisation de guilde et l'admission de `groupPolicy` pour les canaux et threads de guilde Discord. `requireMention`, prévention de boucle de bot, contournements de commande/mention, et historique d'événement de salle sans mention. Canal, et le comportement associé de routage de canal de guilde et d'isolation de session.
- Routage configuré et d'exécution : Couvre les liaisons configurées et d'exécution dans la liste d'autorisation de guilde et l'admission de `groupPolicy` pour les canaux et threads de guilde Discord. `requireMention`, prévention de boucle de bot, contournements de commande/mention, et historique d'événement de salle sans mention. Canal, et le comportement associé de routage de canal de guilde et d'isolation de session.
- Visibilité du contexte entrant : Couvre la visibilité du contexte entrant dans la liste d'autorisation de guilde et l'admission de `groupPolicy` pour les canaux et threads de guilde Discord. `requireMention`, prévention de boucle de bot, contournements de commande/mention, et historique d'événement de salle sans mention. Canal, et le comportement associé de routage de canal de guilde et d'isolation de session.
- Publications de threads de canal forum et média : Couvre les publications de threads de canal forum et média dans les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et d'outil de message : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et le comportement associé de threads, forums, et liaisons d'agent délégué.
- Actions de thread : Couvre les actions de thread dans les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et d'outil de message : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et le comportement associé de threads, forums, et liaisons d'agent délégué.
- Analyse de cible : Couvre l'analyse de cible dans les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et d'outil de message : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et le comportement associé de threads, forums, et liaisons d'agent délégué.
- Résolution du contexte de thread : Couvre la résolution du contexte de thread dans les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et d'outil de message : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et le comportement associé de threads, forums, et liaisons d'agent délégué.
- Routage de session lié au thread : Couvre le routage de session lié au thread dans les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et d'outil de message : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et le comportement associé de threads, forums, et liaisons d'agent délégué.
- Routage d'agent ACP : Couvre les liaisons ACP dans les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et d'outil de message : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et le comportement associé de threads, forums, et liaisons d'agent délégué.
- Cycle de vie de routage : Couvre le cycle de vie de liaison dans les publications de canal forum/média Discord créées en tant que threads à partir de cibles de canal parent. Actions de thread CLI et d'outil de message : `thread-create`, `thread-list`, et `thread-reply`. Analyse de cible Discord pour `channel:<id>`, cibles d'utilisateur, et le comportement associé de threads, forums, et liaisons d'agent délégué.

Documentation principale :

- `docs/channels/discord.md`
- `docs/channels/channel-routing.md`
- `docs/channels/groups.md`
- `docs/channels/access-groups.md`
- `docs/tools/acp-agents.md`
- `docs/tools/subagents.md`

### 4. Médias et contenu enrichi

Ancres de recherche : médias et contenu enrichi discord, médias et contenu enrichi.

Note de catégorie : [Médias et contenu enrichi](media-attachments-and-voice-message-handling.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Médias et contenu enrichi : Portée des preuves pour Médias et contenu enrichi.

Documentation principale :

- `docs/channels/discord.md`

### 5. Contrôles natifs et approbations

Ancres de recherche : commandes slash natives discord, composants et rappels interactifs, commandes slash natives, composants et rappels interactifs.

Note de catégorie : [Contrôles natifs et approbations](native-slash-commands-components-and-interactive-callbacks.md)

Décisions de score :

- Couverture : `Alpha (58%)`
- Qualité : `Beta (72%)`
- Complétude : `Alpha (58%)`
- LTS : ❌

Fonctionnalités :

- Enregistrement de commande slash native : Enregistrement et réconciliation de commande slash native pour les commandes d'application Discord
- Exécution de commande slash native : Exécution de commande slash native, autocomplétion, authz, et dispatch d'interaction
- Commandes de sélecteur de modèle : Couvre les commandes de sélecteur de modèle dans l'enregistrement et la réconciliation de commande slash native pour les commandes d'application Discord. Exécution de commande slash native, autocomplétion, authz, et dispatch d'interaction. Flux de sélecteur `/model` et `/models`, et le comportement associé de commandes slash natives, composants, et rappels interactifs.
- Messages de composants v2 : Messages de composants v2, boutons, sélecteurs de chaîne/utilisateur/rôle/mentionnable/canal, déclencheurs de modal, et soumissions de modal
- TTL de rappel : TTL de rappel, rappels réutilisables par rapport à usage unique, entrées de registre de rappel persistant, allowedUsers, authz de guilde/DM/groupe, et dispatch de rappel interactif de plugin

Documentation principale :

- `docs/channels/discord.md`
- `docs/tools/slash-commands.md`

### 6. Voix en temps réel et appels

Ancres de recherche : Cycle de vie /vc, Jointure automatique et suivi des utilisateurs, Modes de voix en temps réel, Réveil, barge-in et gestion de l'écho, Récupération de codec vocal et DAVE.

Note de catégorie : [Voix en temps réel et appels](realtime-discord-voice-channels.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Cycle de vie du canal vocal : Couvre le cycle de vie du canal vocal dans les sessions de canal vocal Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes d'autorisation de canal vocal/stage ; gestion de connexion/reconnexion et DAVE ; `stt-tts`, `agent-proxy`, et le comportement associé de canaux vocaux en temps réel.
- Jointure automatique et suivi des utilisateurs : Couvre la jointure automatique et le suivi des utilisateurs dans les sessions de canal vocal Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes d'autorisation de canal vocal/stage ; gestion de connexion/reconnexion et DAVE ; `stt-tts`, `agent-proxy`, et le comportement associé de canaux vocaux en temps réel.
- Modes de voix en temps réel : Couvre les modes de voix en temps réel dans les sessions de canal vocal Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes d'autorisation de canal vocal/stage ; gestion de connexion/reconnexion et DAVE ; `stt-tts`, `agent-proxy`, et le comportement associé de canaux vocaux en temps réel.
- Réveil, barge-in et gestion de l'écho : Couvre le réveil, barge-in et la gestion de l'écho dans les sessions de canal vocal Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes d'autorisation de canal vocal/stage ; gestion de connexion/reconnexion et DAVE ; `stt-tts`, `agent-proxy`, et le comportement associé de canaux vocaux en temps réel.
- Récupération de codec vocal et DAVE : Couvre la récupération de codec vocal et DAVE dans les sessions de canal vocal Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes d'autorisation de canal vocal/stage ; gestion de connexion/reconnexion et DAVE ; `stt-tts`, `agent-proxy`, et le comportement associé de canaux vocaux en temps réel.

Documentation principale :

- `docs/channels/discord.md`
- `docs/providers/openai.md`
- `docs/providers/elevenlabs.md`
- `docs/concepts/qa-e2e-automation.md`
- `docs/gateway/config-channels.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/discord/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/discord`.
