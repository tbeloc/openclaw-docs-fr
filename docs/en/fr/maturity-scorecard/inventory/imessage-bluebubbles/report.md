---
title: "Rapport de maturité iMessage / BlueBubbles"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité iMessage / BlueBubbles

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (71%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (71%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `imessage-bluebubbles` de `/Users/kevinlin/tmp/maturity/imessage-bluebubbles` dans le contrat d'inventaire actuel de la version 3 du processus.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                                  | LTS | Couverture    | Qualité      | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------- | --- | ------------- | ------------ | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration des canaux et opérations](setup-status-doctor-and-account-config.md)       | ❌  | `Alpha (62%)` | `Beta (70%)` | `Alpha (62%)` | Traduire la configuration héritée, Effectuer la transition en toute sécurité, Gérer les avertissements de migration, Exécuter imsg localement, Exécuter via le wrapper SSH, Accorder les autorisations macOS, Sonder la santé du runtime, Invites de configuration de compte, Vérifications d'état du compte, Vérifications de réparation du docteur, Configuration du compte |
| [Accès et identité](dm-pairing-access-and-session-routing.md)                            | ❌  | `Beta (75%)`  | `Beta (74%)` | `Beta (75%)`  | Autoriser les expéditeurs directs, Router les conversations directes, Lier les sessions ACP, Politique de groupe, Mentions, Invites système                                                                                                     |
| [Routage et livraison des conversations](inbound-monitoring-coalescing-catchup-and-history.md) | ❌  | `Beta (74%)`  | `Beta (73%)` | `Beta (74%)`  | Surveiller les messages en direct, Fusionner les messages directs divisés, Rejouer les messages manqués, Amorcer l'historique des conversations                                                                                                 |
| [Médias et contenu enrichi](media-attachments-remote-fetch-and-chunking.md)               | ❌  | `Beta (73%)`  | `Beta (71%)` | `Beta (73%)`  | Médias, Pièces jointes, Récupération à distance, Chunking, Actions natives, API privée, Outil de message                                                                                                                                       |
| [Contrôles natifs et approbations](native-approvals-reactions-and-operator-control.md)    | ❌  | `Beta (73%)`  | `Beta (71%)` | `Beta (73%)`  | Approbations natives, Réactions, Contrôle de l'opérateur                                                                                                                                                                                        |

## Barème de notation

- Couverture :
  évaluation du libellé de maturité pour l'intégration, e2e, en direct ou les
  preuves de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent
  fournir un contexte de soutien mais ne rendent jamais une fonctionnalité
  couverte par eux-mêmes.
- Qualité :
  évaluation du libellé de maturité pour la robustesse de l'implémentation et
  opérationnelle. La couverture des tests unitaires, d'intégration, e2e, en
  direct et du flux runtime réel sont des entrées de couverture uniquement ; ils
  ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation du libellé de maturité pour la façon dont la catégorie livre
  complètement l'ensemble de capacités spécifiques à la surface prévue. Utilisez
  les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez
  le libellé de maturité plus élevé.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des
  fonctionnalités plutôt que comme une dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations des canaux

Ancres de recherche : Traduire la configuration héritée, Migrer en toute sécurité, Gérer les avertissements de migration, Exécuter imsg localement, Exécuter via le wrapper SSH, Accorder les permissions macOS, Vérifier la santé du runtime, invites de configuration, écritures de politique, statut du compte, vérifications du docteur, Configuration du compte, configuration/statut/docteur imessage/bluebubbles et configuration du compte, configuration, statut, docteur et configuration du compte.

Note de catégorie : [Configuration et opérations des canaux](setup-status-doctor-and-account-config.md)

Décisions de score :

- Couverture : `Alpha (62%)`
- Qualité : `Beta (70%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Traduire la configuration héritée : Couvre Traduire la configuration héritée dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de basculement de l'opérateur.
- Migrer en toute sécurité : Couvre Migrer en toute sécurité dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de basculement de l'opérateur.
- Gérer les avertissements de migration : Couvre Gérer les avertissements de migration dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions et la liste de contrôle de basculement de l'opérateur.
- Exécuter imsg localement : Couvre Exécuter imsg localement dans les RPC imsg locaux et distants, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Exécuter via le wrapper SSH : Couvre Exécuter via le wrapper SSH dans les RPC imsg locaux et distants, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Accorder les permissions macOS : Couvre Accorder les permissions macOS dans les RPC imsg locaux et distants, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Vérifier la santé du runtime : Couvre Vérifier la santé du runtime dans les RPC imsg locaux et distants, `cliPath`, `dbPath`, `remoteHost` et le transport imsg associé, les exigences d'hôte et le comportement des permissions.
- Invites de configuration du compte : Couvre les invites de configuration, les écritures de politique, la fusion de comptes, la sélection du compte par défaut et le comportement de configuration du compte pour iMessage/BlueBubbles.
- Vérifications du statut du compte : Couvre la sortie du statut du compte, l'état de configuration, la fusion de comptes et la sélection du compte par défaut pour iMessage/BlueBubbles.
- Vérifications de réparation du docteur : Couvre les vérifications du docteur, les invites de réparation de configuration et la vérification de la politique pour la configuration du compte iMessage/BlueBubbles.
- Configuration du compte : Couvre Configuration du compte dans les invites de configuration, les écritures de politique, la fusion de comptes, la sélection du compte par défaut et le comportement associé de configuration, statut, docteur et configuration du compte.

Docs principaux :

- `docs/announcements/bluebubbles-imessage.md`
- `docs/channels/imessage-from-bluebubbles.md`
- `docs/gateway/config-channels.md`
- `docs/channels/imessage.md`

### 2. Accès et identité

Ancres de recherche : Autoriser les expéditeurs directs, Router les conversations directes, Lier les sessions ACP, Politique de groupe, Mentions, Invites système, politique de groupe/mentions/invites système imessage/bluebubbles et politique de groupe, mentions et invites système.

Note de catégorie : [Accès et identité](dm-pairing-access-and-session-routing.md)

Décisions de score :

- Couverture : `Beta (75%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (75%)`
- LTS : ❌

Fonctionnalités :

- Autoriser les expéditeurs directs : Couvre Autoriser les expéditeurs directs dans `dmPolicy`, `allowFrom`, l'appairage, la normalisation de l'identité de l'expéditeur et le comportement associé d'appairage DM, d'accès et de routage de session.
- Router les conversations directes : Couvre Router les conversations directes dans `dmPolicy`, `allowFrom`, l'appairage, la normalisation de l'identité de l'expéditeur et le comportement associé d'appairage DM, d'accès et de routage de session.
- Lier les sessions ACP : Couvre Lier les sessions ACP dans `dmPolicy`, `allowFrom`, l'appairage, la normalisation de l'identité de l'expéditeur et le comportement associé d'appairage DM, d'accès et de routage de session.
- Politique de groupe : Couvre Politique de groupe dans `groupPolicy`, `groupAllowFrom`, `groups`, les entrées du registre générique, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour la mauvaise configuration de la liste d'autorisation.
- Mentions : Couvre Mentions dans `groupPolicy`, `groupAllowFrom`, `groups`, les entrées du registre générique, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour la mauvaise configuration de la liste d'autorisation.
- Invites système : Couvre Invites système dans `groupPolicy`, `groupAllowFrom`, `groups`, les entrées du registre générique, `requireMention`, les modèles de mention, les outils par groupe, les invites système par groupe, les sessions de groupe et les avertissements pour la mauvaise configuration de la liste d'autorisation.

Docs principaux :

- `docs/channels/imessage.md`
- `docs/channels/imessage-from-bluebubbles.md`
- `docs/gateway/config-channels.md`

### 3. Routage et livraison des conversations

Ancres de recherche : Surveiller les messages en direct, Fusionner les DM à envoi divisé, Rejouer les messages manqués, Ensemencer l'historique des conversations.

Note de catégorie : [Routage et livraison des conversations](inbound-monitoring-coalescing-catchup-and-history.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (73%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Surveiller les messages en direct : Couvre Surveiller les messages en direct dans `watch.subscribe` entrant, l'analyse des notifications, les gardes d'écho et d'auto-chat, le cache des messages envoyés, la fusion des DM du même expéditeur, l'historique des DM, le routage des événements de réaction, le curseur de rattrapage/relecture et l'avancement du curseur en direct.
- Fusionner les DM à envoi divisé : Couvre Fusionner les DM à envoi divisé dans `watch.subscribe` entrant, l'analyse des notifications, les gardes d'écho et d'auto-chat, le cache des messages envoyés, la fusion des DM du même expéditeur, l'historique des DM, le routage des événements de réaction, le curseur de rattrapage/relecture et l'avancement du curseur en direct.
- Rejouer les messages manqués : Couvre Rejouer les messages manqués dans `watch.subscribe` entrant, l'analyse des notifications, les gardes d'écho et d'auto-chat, le cache des messages envoyés, la fusion des DM du même expéditeur, l'historique des DM, le routage des événements de réaction, le curseur de rattrapage/relecture et l'avancement du curseur en direct.
- Ensemencer l'historique des conversations : Couvre Ensemencer l'historique des conversations dans `watch.subscribe` entrant, l'analyse des notifications, les gardes d'écho et d'auto-chat, le cache des messages envoyés, la fusion des DM du même expéditeur, l'historique des DM, le routage des événements de réaction, le curseur de rattrapage/relecture et l'avancement du curseur en direct.

Docs principaux :

- `docs/channels/imessage.md`

### 4. Médias et contenu enrichi

Ancres de recherche : Médias, Pièces jointes, Récupération distante, Chunking, médias/pièces jointes/récupération distante/chunking imessage/bluebubbles et médias, pièces jointes, récupération distante et chunking, Actions natives, API privée, Outil de message, actions natives/API privée/outil de message imessage/bluebubbles et actions natives, API privée et outil de message.

Note de catégorie : [Médias et contenu enrichi](media-attachments-remote-fetch-and-chunking.md)

Décisions de score :

- Couverture : `Beta (73%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (73%)`
- LTS : ❌

Fonctionnalités :

- Médias : Couvre Médias dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les plafonds de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Pièces jointes : Couvre Pièces jointes dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les plafonds de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Récupération distante : Couvre Récupération distante dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les plafonds de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Chunking : Couvre Chunking dans `includeAttachments`, les listes blanches de racines de pièces jointes, les racines de pièces jointes distantes, les récupérations SCP `remoteHost`, la conversion HEIC, les plafonds de taille, les envois de médias sortants, `send-attachment`, le chunking de texte et les reçus de médias.
- Actions natives : Couvre Actions natives dans le sondage de l'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch des actions.
- API privée : Couvre API privée dans le sondage de l'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch des actions.
- Outil de message : Couvre Outil de message dans le sondage de l'API privée, la disponibilité des actions, les portes de configuration des actions, le mappage des tapbacks, l'édition/l'annulation/la réponse/les effets/la gestion de groupe, `send-rich --file`, la visibilité de l'outil de message/la grammaire cible et les erreurs de dispatch des actions.

Docs principaux :

- `docs/channels/imessage.md`
- `docs/channels/imessage-from-bluebubbles.md`
- `docs/gateway/config-channels.md`

### 5. Contrôles natifs et approbations

Ancres de recherche : Approbations natives, Réactions, Contrôle de l'opérateur, approbations natives/réactions/contrôle de l'opérateur imessage/bluebubbles et approbations natives, réactions et contrôle de l'opérateur.

Note de catégorie : [Contrôles natifs et approbations](native-approvals-reactions-and-operator-control.md)

Décisions de score :

- Couverture : `Beta (73%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (73%)`
- LTS : ❌

Fonctionnalités :

- Approbations natives : Couvre Approbations natives dans la livraison des approbations natives, le routage des approbations exec/plugin, les décisions d'approbation basées sur les réactions, les changements d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle de l'opérateur.
- Réactions : Couvre Réactions dans la livraison des approbations natives, le routage des approbations exec/plugin, les décisions d'approbation basées sur les réactions, les changements d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle de l'opérateur.
- Contrôle de l'opérateur : Couvre Contrôle de l'opérateur dans la livraison des approbations natives, le routage des approbations exec/plugin, les décisions d'approbation basées sur les réactions, les changements d'autorisation `/approve` et le comportement associé des approbations natives, réactions et contrôle de l'opérateur.

Docs principaux :

- `docs/channels/imessage.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, les docs et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/imessage-bluebubbles/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/imessage-bluebubbles`.
