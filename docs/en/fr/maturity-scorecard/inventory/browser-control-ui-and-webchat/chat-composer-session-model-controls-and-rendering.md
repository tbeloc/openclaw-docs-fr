---
title: "Gateway Web App - WebChat Conversations Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - WebChat Conversations Maturity Note

## Résumé

L'expérience de chat Control UI a une large surface produit : contrôles de composition, comportement de file d'attente/direction/arrêt, sélecteurs de session et d'agent, sélecteurs de modèle et de réflexion, pièces jointes, cartes d'outils, messages groupés, markdown, avatars, utilisation du contexte et mise en page réactive. La couverture est Beta car il y a de nombreux tests UI et E2E ciblés, mais la matrice produit est large et la preuve multi-navigateurs est inégale. La qualité est Alpha car les preuves d'archive montrent des régressions UI fréquentes autour du rendu, des sélecteurs, des avatars, des images, de l'état visible des outils et de l'état en cours.

## Portée de la catégorie

Inclus dans cette catégorie :

- Envoyer et abandonner : Couvre Envoyer et abandonner dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Sélecteur de session et d'agent : Couvre Sélecteur de session et d'agent dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Contrôles de modèle/réflexion : Couvre Contrôles de modèle/réflexion dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Pièces jointes : Couvre Pièces jointes dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Rendu Markdown/outil/média : Couvre Rendu Markdown/outil/média dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Projection chat.history : Couvre Projection chat.history dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Cycle de vie chat.send : Couvre Cycle de vie chat.send dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Abandon/rétention partielle : Couvre Abandon/rétention partielle dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Notes d'assistant injectées : Couvre Notes d'assistant injectées dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Continuité de reconnexion : Couvre Continuité de reconnexion dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Intégrations hébergées : Couvre Intégrations hébergées dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Contrôle d'accès aux intégrations externes : Couvre Contrôle d'accès aux intégrations externes dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Tickets de média d'assistant : Couvre Tickets de média d'assistant dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Avatars authentifiés : Couvre Avatars authentifiés dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Politique d'image CSP : Couvre Politique d'image CSP dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.

## Fonctionnalités

- Envoyer et abandonner : Couvre Envoyer et abandonner dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Sélecteur de session et d'agent : Couvre Sélecteur de session et d'agent dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Contrôles de modèle/réflexion : Couvre Contrôles de modèle/réflexion dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Pièces jointes : Couvre Pièces jointes dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Rendu Markdown/outil/média : Couvre Rendu Markdown/outil/média dans la composition de chat du navigateur et l'UX d'affichage après l'existence d'une connexion Gateway authentifiée : contrôles de composition, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion et comportement de rendu de compositeur de chat et de message associé.
- Projection chat.history : Couvre Projection chat.history dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Cycle de vie chat.send : Couvre Cycle de vie chat.send dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Abandon/rétention partielle : Couvre Abandon/rétention partielle dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Notes d'assistant injectées : Couvre Notes d'assistant injectées dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Continuité de reconnexion : Couvre Continuité de reconnexion dans le contrat RPC/runtime Gateway WebChat, la projection de transcript durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement de runtime webchat et de continuité de session associé.
- Intégrations hébergées : Couvre Intégrations hébergées dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Contrôle d'accès aux intégrations externes : Couvre Contrôle d'accès aux intégrations externes dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Tickets de média d'assistant : Couvre Tickets de média d'assistant dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Avatars authentifiés : Couvre Avatars authentifiés dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.
- Politique d'image CSP : Couvre Politique d'image CSP dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'intégration externes, CSP et refus de cadre, et le comportement de média hébergé et de sécurité d'intégration associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : Les tests UI controller, view, chat helper, style et E2E du navigateur couvrent l'état du compositeur, l'envoi/abandon, la pagination du sélecteur de session, le sélecteur de modèle, le markdown, le rendu groupé, les cartes d'outils, les pièces jointes, la mise en page réactive et l'affichage des avatars.
- Signaux négatifs : La matrice réelle du navigateur, la mise en page mobile, les longs transcripts, les formes de streaming spécifiques au fournisseur et les pièces jointes multimédias ont plus d'exposition aux régressions que la preuve de scénario de bout en bout.
- Lacunes d'intégration : Ajouter des tests de fumée multi-navigateurs/mobiles pour les longs transcripts, les pièces jointes image/fichier, le changement de modèle lors de l'envoi, les suites en file d'attente, le menu slash, la relecture des cartes d'outils et les contrôles réactifs.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : Les recherches larges Control UI/WebChat ont retourné #50779 pour les images retournées par les outils, #85750 pour l'authentification des avatars, #74354 pour le formatage des messages numériques, #61661 pour la restauration de session routée historique, #81760 pour les mauvaises valeurs par défaut de réflexion, #73836 pour la régression de réactivité, et les PR #87673, #79747, #74274, #81795 et #49511.
- Rapports Discrawl : La recherche Discord a trouvé des rapports de mainteneurs et d'utilisateurs autour des régressions Control UI/chat, les images générées n'apparaissant pas visiblement dans Control UI, le comportement de la modale d'approbation et le trafic de version autour des réponses visibles plus rapides et des correctifs d'interface de chat.
- Bonnes qualités : Le code UI a des machines d'état explicites pour les envois optimistes, les ACK en attente, les promesses de changement de modèle, l'état du sélecteur de session, la rétention de la charge utile des pièces jointes, la normalisation du rendu et l'affichage des cartes d'outils.
- Mauvaises qualités : La surface des fonctionnalités est dense et change fréquemment ; les petites régressions peuvent faire diverger l'état visible du chat de l'état Gateway/session sous-jacent.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux runtime réel affectent uniquement la couverture.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent l'étendue taxonomique pour Envoyer et abandonner, Sélecteur de session et d'agent, Contrôles de modèle/réflexion, Pièces jointes, Rendu markdown/outil/média, projection chat.history, cycle de vie chat.send, Abandon/rétention partielle, Notes d'assistant injectées, Continuité de reconnexion, Embeds hébergés, Gating d'embed externe, Tickets média d'assistant, Avatars authentifiés, Politique d'image CSP.
- Signaux négatifs : la note archivée a précédé le score de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve de mise en page mobile et PWA accuse du retard par rapport à la preuve Chromium de bureau.
- Les pièces jointes de chat et le rendu de médias générés restent des sources récurrentes de problèmes visibles par l'utilisateur.
- Les interactions du sélecteur de modèle/réflexion/session nécessitent des scénarios de version plus larges pour les catalogues multi-agents et à portée de fournisseur.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente les contrôles de chat, le comportement de téléchargement, l'effondrement des doublons, les sélecteurs de modèle/réflexion, le filtrage de session, `/new`, `/reset`, `/stop`, l'utilisation du contexte et les contrôles adjacents Talk.
- `/Users/kevinlin/code/openclaw/docs/web/webchat.md` documente la normalisation d'affichage, l'exclusion du raisonnement, les suppléments de transcription média et le comportement en lecture seule lors de la déconnexion.
- `/Users/kevinlin/code/openclaw/docs/start/getting-started.md` présente le chat Control UI comme le chemin utilisateur de première exécution.

### Source

- `/Users/kevinlin/code/openclaw/ui/src/ui/app-chat.ts` coordonne l'envoi/abandon du compositeur, les files d'attente, l'actualisation de session, les attentes de changement de modèle et l'actualisation de l'avatar de chat.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/chat.ts` rend la vue de chat, le compositeur, les contrôles Talk, les pièces jointes et la mise en page de la transcription.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/session-controls.ts` implémente les sélecteurs de session, d'agent, de modèle et de réflexion.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/attachment-payload-store.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/chat/attachment-support.ts` gèrent les charges utiles de pièces jointes du navigateur.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/tool-cards.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/chat/grouped-render.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/markdown.ts` rendent le contenu des outils et du markdown.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/ui/src/ui/e2e/chat-flow.e2e.test.ts` couvre l'envoi de chat du navigateur simulé, l'ACK retardé, les erreurs et le comportement de nouvelle tentative.
- `/Users/kevinlin/code/openclaw/ui/src/ui/e2e/chat-picker-pagination.e2e.test.ts` couvre la pagination du sélecteur.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat-webchat-media.test.ts` couvre les charges utiles d'affichage de médias utilisées par WebChat.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/app-chat.test.ts` couvre l'envoi, l'abandon, la file d'attente, le changement de modèle et le comportement de session.
- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/chat.test.ts` couvre l'état du chat côté client.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/chat.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/chat/run-controls.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/chat/grouped-render.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/chat/tool-cards.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/chat/chat-responsive.browser.test.ts` couvrent les détails du rendu.
- `/Users/kevinlin/code/openclaw/ui/src/ui/app-render.assistant-avatar.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/chat/chat-avatar.test.ts` couvrent le rendu de l'avatar.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Control UI"`

Résultats :

- Retourné les problèmes ouverts #50779, #85750, #74354, #61661, #81760, #73836, #83494, #80039, #68248 et autres problèmes Control UI.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "Control UI"`

Résultats :

- Retourné les PRs ouvertes #87673, #79747, #74274, #81795, #49511, #80192, #80388, #87147, #73894 et autres.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "control ui chat composer attachments model picker session picker"`

Résultats :

- Retourné `[]`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 20 "Control UI"`

Résultats :

- Trouvé un rapport utilisateur selon lequel les images générées dans Control UI se terminaient sans pièce jointe visible jusqu'à ce qu'elles soient explicitement liées.
- Trouvé le trafic des mainteneurs autour des cartes de compétences Control UI, du rejet de la modale d'approbation et des notes de version nommant les régressions Control UI/chat.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "control ui chat composer attachments model picker session picker"`

Résultats :

- Retourné aucune ligne.
