---
title: "Rapport de maturité du framework de canal"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du framework de canal

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les
scores numériques des catégories dans
`scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Beta (77%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (77%)`
- Fonctionnalités LTS : `5/8`

## Résumé

Ce rapport promeut les preuves de maturité archivées du `channel-framework` de `/Users/kevinlin/tmp/maturity/channel-framework` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                              | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Commandes, actions et approbations de canal](channel-actions-commands-and-approvals.md)   | ❌  | `Alpha (68%)`  | `Beta (72%)`  | `Alpha (68%)`  | Commandes natives du canal, Cible de session de commande native, Actions de message, Découverte d'API d'outil de message, Invites d'approbation natives du canal                                                                                                                                                     |
| [Configuration du canal](channel-setup.md)                                                     | ✅  | `Stable (84%)` | `Beta (78%)`  | `Stable (84%)` | Catalogue de canaux pris en charge, Taxonomie d'état du canal dans la liste des canaux, Flux de configuration/intégration, Installation à la demande, Métadonnées de l'assistant de configuration                                                                                                                                                    |
| [Comportement des groupes, threads et salons ambiants](group-thread-and-ambient-room-behavior.md)   | ❌  | `Beta (72%)`   | `Alpha (68%)` | `Beta (72%)`   | Isolation de session groupe/canal, Mention requise, Threads natifs, Groupes de diffusion, Protection contre les boucles de bot                                                                                                                                                                                 |
| [Portes d'accès entrant et d'identité](inbound-access-and-identity-gates.md)             | ✅  | `Stable (80%)` | `Beta (76%)`  | `Stable (80%)` | Appairage MP, Listes blanches groupe/canal, Expansion du groupe d'accès, Mention gating, Projections d'identité/route entrantes assainies                                                                                                                                                               |
| [Pièces jointes médias et données de canal enrichies](media-attachments-and-rich-channel-data.md) | ❌  | `Alpha (68%)`  | `Beta (70%)`  | `Alpha (68%)`  | Normalisation des médias entrants, Envois directs de texte/médias sortants, channelData spécifique au fournisseur, Racines de médias                                                                                                                                                                                |
| [Pipeline de livraison sortante et de réponse](outbound-delivery-and-reply-pipeline.md)       | ✅  | `Stable (82%)` | `Beta (75%)`  | `Stable (82%)` | Livraison automatique de réponse finale, Orchestration d'envoi sortant durable, Transformations du pipeline de réponse, Pont d'adaptateur sortant du fournisseur                                                                                                                                                         |
| [Routage et livraison des conversations](conversation-routing-and-delivery.md)             | ✅  | `Beta (77%)`   | `Beta (71%)`  | `Beta (77%)`   | Routage des conversations entrantes, Construction de clé de session, Précédence de sélection d'agent, Routage des conversations à l'exécution, Placement parent-enfant/thread, Résolution du registre de plugins, Démarrage du compte de canal, Contrôles du cycle de vie du canal entier, Interactions de rechargement de config/secrets, Redémarrage automatique |
| [Contrôles de santé, d'état et d'opérateur](status-health-and-operator-controls.md)         | ✅  | `Stable (82%)` | `Beta (78%)`  | `Stable (82%)` | channels.status, Politique de santé du canal, Contrôles CLI d'opérateur, Modèle de lecture d'état                                                                                                                                                                                                         |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves du flux serveur/exécution
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une
  fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et du flux d'exécution réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre l'ensemble complet de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'
  étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Commandes et approbations des actions de canal

Ancres de recherche : commandes natives de canal, actions de message, invites d'approbation natives de canal.

Note de catégorie : [Commandes et approbations des actions de canal](channel-actions-commands-and-approvals.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Beta (72%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Commandes natives de canal : Commandes natives de canal et portes d'autorisation de commande
- Résolution de cible de session de commande native : Résolution de cible de session de commande native
- Actions de message : Actions de message, dispatch d'action et vérifications de demandeur de confiance
- Découverte d'API d'outil de message : Découverte d'API d'outil de message pour les actions de canal
- Invites d'approbation natives de canal : Invites d'approbation natives de canal et routage d'approbation plugin/exec

Documentation principale :

- `docs/channels/groups.md`
- `docs/channels/discord.md`
- `docs/channels/googlechat.md`
- `docs/channels/signal.md`
- `docs/channels/matrix.md`

### 2. Configuration du canal

Ancres de recherche : liste des canaux, configuration des canaux, métadonnées de l'assistant de configuration.

Note de catégorie : [Configuration du canal](channel-setup.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (84%)`
- LTS : ✅

Fonctionnalités :

- Catalogue de canaux pris en charge : Catalogue de canaux pris en charge et index de documentation
- Taxonomie de statut de canal dans la liste des canaux : Taxonomie de statut de canal dans la liste des canaux, statut des canaux et sortie de statut de configuration
- Flux de configuration/intégration : Flux de configuration/intégration, y compris la sélection de canal au premier lancement et la configuration du compte de canal
- Installation à la demande : Installation à la demande, téléchargeable, fourni, officiel externe, local, npm et distinctions ClawHub
- Métadonnées de l'assistant de configuration : Métadonnées de l'assistant de configuration et points d'entrée de plugin sûrs pour la configuration

Documentation principale :

- `docs/channels/index.md`
- `docs/channels/pairing.md`
- `docs/channels/troubleshooting.md`
- `docs/plugins/sdk-channel-plugins.md`

### 3. Comportement des fils de groupe et des salons ambiants

Ancres de recherche : mentionRequired, événements de salle ambiante, groupes de diffusion.

Note de catégorie : [Comportement des fils de groupe et des salons ambiants](group-thread-and-ambient-room-behavior.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Isolation de session de groupe/canal : Isolation de session de groupe/canal et contexte d'historique de groupe
- Mention requise : Mention requise, toujours activé et modes d'événement de salle ambiante
- Fils natifs : Fils natifs, sujets, liaisons parent-enfant et comportement de génération de fil
- Groupes de diffusion : Groupes de diffusion et routage de groupe multi-agent
- Protection contre les boucles de bot : Protection contre les boucles de bot pour le comportement de salle

Documentation principale :

- `docs/channels/groups.md`
- `docs/channels/group-messages.md`
- `docs/channels/ambient-room-events.md`
- `docs/channels/broadcast-groups.md`
- `docs/channels/discord.md`

### 4. Portes d'accès entrant et d'identité

Ancres de recherche : appairage DM, allowFrom, groupes d'accès.

Note de catégorie : [Portes d'accès entrant et d'identité](inbound-access-and-identity-gates.md)

Décisions de score :

- Couverture : `Stable (80%)`
- Qualité : `Beta (76%)`
- Complétude : `Stable (80%)`
- LTS : ✅

Fonctionnalités :

- Appairage DM : Appairage DM et contrôles d'expéditeur allowFrom
- Listes blanches de groupe/canal : Listes blanches de groupe/canal et listes blanches d'expéditeur
- Expansion du groupe d'accès : Expansion du groupe d'accès et assistants d'autorisation d'expéditeur
- Gating par mention : Gating par mention, mentions implicites, contournement de commande et admission consciente des boucles de bot
- Projections d'identité/route entrantes assainies : Projections d'identité/route entrantes assainies pour le dispatch en aval

Documentation principale :

- `docs/channels/access-groups.md`
- `docs/channels/groups.md`
- `docs/channels/discord.md`
- `docs/channels/line.md`

### 5. Pièces jointes multimédias et données de canal enrichies

Ancres de recherche : normalisation des médias entrants, channelData, racines multimédias.

Note de catégorie : [Pièces jointes multimédias et données de canal enrichies](media-attachments-and-rich-channel-data.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Beta (70%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Normalisation des médias entrants : Normalisation des médias entrants, persistance des pièces jointes et contexte des médias d'historique
- Envois directs de texte/médias sortants : Envois directs de texte/médias sortants et support d'adaptateur de charge utile enrichie
- channelData spécifique au fournisseur : channelData spécifique au fournisseur, réponses rapides, emplacements, sondages, réactions et gestion des notes vocales
- Racines multimédias : Racines multimédias et sécurité des chemins de fichiers pour le stockage entrant de canal

Documentation principale :

- `docs/channels/line.md`
- `docs/channels/signal.md`
- `docs/channels/googlechat.md`
- `docs/channels/matrix.md`
- `docs/channels/discord.md`

### 6. Pipeline de livraison et de réponse sortants

Ancres de recherche : livraison de réponse finale automatique, livraison d'outil de message, rappels de saisie.

Note de catégorie : [Pipeline de livraison et de réponse sortants](outbound-delivery-and-reply-pipeline.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (75%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Livraison de réponse finale automatique : Livraison de réponse finale automatique et livraison visible strictement réservée à l'outil de message
- Orchestration d'envoi sortant durable : Orchestration d'envoi sortant durable, reçus, défaillances partielles et chemins de secours
- Transformations du pipeline de réponse : Transformations du pipeline de réponse, rappels de saisie, diffusion en continu de brouillon et réactions de statut
- Pont d'adaptateur sortant du fournisseur : Pont d'adaptateur sortant du fournisseur et capacités de message

Documentation principale :

- `docs/channels/groups.md`
- `docs/channels/ambient-room-events.md`
- `docs/channels/discord.md`
- `docs/channels/matrix.md`
- `docs/gateway/config-channels.md`

### 7. Routage et livraison des conversations

Ancres de recherche : routage de canal, construction de clé de session, précédence de liaison d'agent, channels.start, channels.stop, démarrage du compte de canal, redémarrage de santé.

Note de catégorie : [Routage et livraison des conversations](conversation-routing-and-delivery.md)

Décisions de score :

- Couverture : `Beta (77%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (77%)`
- LTS : ✅

Fonctionnalités :

- Routage de conversation entrant : Résolution de conversation entrante et de commande entre les sessions, les fils et les cibles détenues par le fournisseur.
- Construction de clé de session : Construction de clé de session et enregistrement des métadonnées de session
- Précédence de sélection d'agent : Précédence de liaison d'agent et dispatch de groupe de diffusion
- Routage de conversation à l'exécution : Liaisons de conversation à l'exécution et routes de liaison de session ACP
- Placement parent-enfant/fil : Placement parent-enfant/fil et normalisation de cible détenue par le fournisseur
- Résolution du registre de plugin : Résolution du registre de plugin et création de runtime de canal délimité
- Démarrage du compte de canal : Démarrage du compte de canal, arrêt, déconnexion, abandon et état d'arrêt manuel
- Contrôles de cycle de vie de canal entier : Fanout de cycle de vie de canal entier et par compte pour démarrage, arrêt, déconnexion, redémarrage et snapshots d'exécution.
- Interactions de rechargement de configuration/secrets : Interactions de rechargement de configuration/secrets avec cibles de rechargement de plugin de canal
- Redémarrage automatique : Redémarrage automatique, backoff, plafonds de boucle de crash et rapports de snapshot d'exécution

Documentation principale :

- `docs/channels/channel-routing.md`
- `docs/channels/groups.md`
- `docs/channels/discord.md`
- `docs/channels/matrix.md`
- `docs/channels/troubleshooting.md`
- `docs/gateway/configuration-reference.md`

### 8. Santé du statut et contrôles de l'opérateur

Ancres de recherche : channels status --probe, politique de santé du canal, contrôles CLI de l'opérateur.

Note de catégorie : [Santé du statut et contrôles de l'opérateur](status-health-and-operator-controls.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- channels.status : channels.status, sondes, snapshots de compte et avertissements
- Politique de santé du canal : Politique de santé du canal, redémarrages du moniteur de santé, détection de socket obsolète, refroidissements et plafonds de redémarrage
- Contrôles CLI de l'opérateur : Contrôles CLI de l'opérateur pour démarrage, arrêt, déconnexion, statut, redémarrage et dépannage
- Modèle de lecture de statut : Modèle de lecture de statut et snapshots de statut de plugin

Documentation principale :

- `docs/gateway/health.md`
- `docs/gateway/configuration-reference.md`
- `docs/channels/troubleshooting.md`
- `docs/channels/discord.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/channel-framework/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuve archivée :
  `/Users/kevinlin/tmp/maturity/channel-framework`.
