---
title: "Gateway Web App - Hosted Media and Embed Safety Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - Hosted Media and Embed Safety Maturity Note

## Résumé

Control UI dispose de contrôles de sécurité explicites du navigateur pour les embeds hébergés, les médias d'assistant, les routes d'avatar authentifiées, CSP, les tickets médias, les vérifications de racine locale et l'authentification des routes d'image/média. La couverture est Stable car les tests serveur ciblent CSP, les médias d'assistant, l'authentification d'avatar et le comportement des routes HTTP. La qualité est Beta car la conception est défensive, mais les preuves d'archive montrent que les problèmes de rendu d'avatar et d'image restent visibles pour les utilisateurs et le comportement CSP/framing a créé des tensions produit.

## Portée de la catégorie

Cette catégorie couvre la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'embed externes, CSP et refus de frame, les routes de métadonnées/ticket médias d'assistant, les routes d'avatar authentifiées, la suppression d'avatar distant, les vérifications de racine de média local et la sécurité du rendu médias natif du navigateur.

## Fonctionnalités

- Embeds hébergés : Couvre les embeds hébergés dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'embed externes, CSP et refus de frame, et le comportement de sécurité des médias et embeds hébergés associés.
- Contrôle d'accès aux embeds externes : Couvre le contrôle d'accès aux embeds externes dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'embed externes, CSP et refus de frame, et le comportement de sécurité des médias et embeds hébergés associés.
- Tickets médias d'assistant : Couvre les tickets médias d'assistant dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'embed externes, CSP et refus de frame, et le comportement de sécurité des médias et embeds hébergés associés.
- Avatars authentifiés : Couvre les avatars authentifiés dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'embed externes, CSP et refus de frame, et le comportement de sécurité des médias et embeds hébergés associés.
- Politique d'image CSP : Couvre la politique d'image CSP dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'accès aux URL d'embed externes, CSP et refus de frame, et le comportement de sécurité des médias et embeds hébergés associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : Les tests Gateway couvrent les médias d'assistant e2e, CSP, le comportement HTTP de control-ui, le rendu/authentification d'avatar et la projection médias de chat ; les tests UI couvrent l'affichage d'avatar, le rendu markdown/médias et les assistants sandbox d'embed.
- Signaux négatifs : La preuve du navigateur réel est plus faible pour les embeds hébergés en externe, les modes sandbox de même origine, les médias volumineux, les tickets médias authentifiés à l'intérieur des éléments médias natifs et les différences CSP entre navigateurs.
- Lacunes d'intégration : Ajouter un smoke test du navigateur pour les modes sandbox d'embed de même origine, les URL d'embed externes bloquées, la récupération d'avatar authentifiée, les tickets médias image/audio/vidéo d'assistant et la suppression d'URL distante.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : La requête avatar a retourné #85750, #41201, #38439, #42504 et #68248. La requête CSP/embed n'a retourné aucune ligne, tandis que la requête Control UI large a retourné #78577 pour l'opt-in de framing same-origin CSP/X-Frame-Options et #50779 pour les images retournées par l'outil ne s'affichant pas en ligne.
- Rapports Discrawl : La requête exacte embed/média/CSP n'a retourné aucune ligne ; le trafic Control UI large incluait des plaintes utilisateur visibles concernant l'espace écran des images générées et des embeds.
- Bonnes qualités : CSP est serré par défaut, les ancêtres de frame sont refusés, les récupérations d'images distantes sont bloquées/supprimées, les médias d'assistant utilisent des tickets scoped à courte durée de vie et les modes sandbox d'embed sont explicites.
- Mauvaises qualités : Les visuels médias et identité sont des bords produit très visibles, et les utilisateurs expérimentent les régressions d'authentification de route ou CSP comme un chat cassé plutôt que comme un renforcement de sécurité.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux runtime réel affectent uniquement la couverture.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les embeds hébergés, le contrôle d'accès aux embeds externes, les tickets médias d'assistant, les avatars authentifiés, la politique d'image CSP.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La politique d'opt-in d'embed de même origine a besoin de clarté produit.
- Les routes d'avatar et de médias d'assistant ont besoin de preuves récurrentes sous authentification par token, authentification par proxy et contraintes d'élément médias du navigateur.
- Le rendu d'image retourné par l'outil reste une lacune connue visible par l'utilisateur dans les problèmes d'archive.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente les embeds hébergés, `embedSandbox`, `allowExternalEmbedUrls`, la politique d'image CSP, l'authentification de route d'avatar et le comportement de ticket médias d'assistant.
- `/Users/kevinlin/code/openclaw/docs/web/webchat.md` documente les suppléments de transcription médias et la projection d'affichage.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/secure-file-operations.md` documente le contexte de sécurité médias local qui sous-tend la gestion des routes médias.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/control-ui.ts` implémente la ticketisation médias d'assistant, la résolution d'avatar, les vérifications d'accès aux médias locaux et les routes médias Control UI authentifiées.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-csp.ts` construit le CSP Control UI.
- `/Users/kevinlin/code/openclaw/ui/src/ui/embed-sandbox.ts` normalise la politique sandbox d'embed.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/chat-avatar.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/app-render.assistant-avatar.test.ts` supportent les avatars de chat.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat-webchat-media.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat-reply-media.ts` normalisent les médias pour WebChat.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-assistant-media.e2e.test.ts` couvre le comportement de la route médias d'assistant.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui.http.test.ts` couvre la route HTTP Control UI et le comportement des assets.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-csp.test.ts` couvre le comportement CSP.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/chat-webchat-media.test.ts` couvre les payloads médias WebChat.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/app-render.assistant-avatar.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/chat/chat-avatar.test.ts` couvrent le comportement UI d'avatar.
- `/Users/kevinlin/code/openclaw/ui/src/ui/markdown.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/styles/markdown-preview.test.ts` couvrent les assistants de rendu de message.
- `/Users/kevinlin/code/openclaw/src/gateway/chat-attachments.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/managed-image-attachments.test.ts` couvrent les assistants médias côté serveur.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "avatar Control UI"`

Résultats :

- A retourné l'issue ouverte #85750, `Control UI avatar endpoint returns 401 Unauthorized for authenticated webchat sessions`.
- A retourné l'issue ouverte #41201, `Control UI Avatar not displaying`.
- A retourné l'issue ouverte #38439, WebChat avatar endpoint 404.
- A retourné les demandes de fonctionnalité #42504 et #68248 pour le téléchargement/personnalisation d'avatar.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "avatar Control UI"`

Résultats :

- A retourné la PR ouverte #83235, `fix(control-ui): avoid protected local avatar image URLs`.
- A retourné la PR #62727 pour l'analyse d'avatar d'identité descriptive.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Control UI avatar assistant media embed CSP"`

Résultats :

- A retourné `[]`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI avatar assistant media embed CSP"`

Résultats :

- N'a retourné aucune ligne.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 20 "Control UI"`

Résultats :

- A trouvé une demande de mainteneur pour supprimer les embeds d'un rapport car ils prenaient trop d'espace écran.
- A trouvé un rapport utilisateur où la sortie d'image générée dans Control UI a produit du texte mais aucune pièce jointe d'image visible.
