---
title: "Gateway Web App - Browser Realtime Talk Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - Browser Realtime Talk Maturity Note

## Résumé

Browser Talk est implémenté dans le compositeur Control UI, les RPC Gateway Talk, la création de session navigateur du fournisseur, WebRTC, Google Live/WebSocket du fournisseur, et les transports de relais Gateway. La couverture est Beta car les tests locaux couvrent la logique de transport et les gestionnaires de serveur, mais la matrice réelle navigateur/fournisseur/audio est encore nouvelle. La qualité est Beta à la limite inférieure car l'implémentation a une séparation claire des identifiants et du relais, tandis que les preuves d'archive montrent des lacunes récemment corrigées et un problème actif où Talk peut parler une réponse différente du texte visible de Control UI.

## Portée de la catégorie

Inclus dans cette catégorie :

- Démarrage/arrêt de Browser Talk : Couvre le démarrage/arrêt de Browser Talk dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Sélection de session du fournisseur : Couvre la sélection de session du fournisseur dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Audio de relais Gateway : Couvre l'audio de relais Gateway dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Consultations d'appels d'outils : Couvre les consultations d'appels d'outils dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Direction et annulation : Couvre la direction et l'annulation dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.

## Fonctionnalités

- Démarrage/arrêt de Browser Talk : Couvre le démarrage/arrêt de Browser Talk dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Sélection de session du fournisseur : Couvre la sélection de session du fournisseur dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Audio de relais Gateway : Couvre l'audio de relais Gateway dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Consultations d'appels d'outils : Couvre les consultations d'appels d'outils dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.
- Direction et annulation : Couvre la direction et l'annulation dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/WebSocket du fournisseur, et le comportement de talk en temps réel du navigateur associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : Les tests UI couvrent WebRTC, Google Live, relais Gateway, consultation, annulation, et intégration de l'application Talk ; les tests Gateway couvrent `talk.client.*`, `talk.session.*`, relais, relais de transcription, résolution du fournisseur, et diagnostics Talk.
- Signaux négatifs : Le smoke test en direct du responsable existe, mais les permissions de microphone du navigateur, les appareils audio, l'authentification du fournisseur, la mise en réseau WebRTC, les jetons Google Live, et la latence du relais nécessitent une preuve répétée en environnement réel.
- Lacunes d'intégration : Ajouter un smoke test de version pour WebRTC du navigateur, WebSocket du fournisseur, relais Gateway, refus de microphone, échec d'authentification du fournisseur, barge-in, direction/annulation de run actif, et parité transcript/audio.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : Les requêtes Talk ont retourné le problème ouvert #85275, `Talk mode can speak a different answer than the Control UI when agent reply uses message_tool_only / delivery-mirror`, plus les demandes de fonctionnalités vocales et la PR #85990 pour la préférence de texte final Talk.
- Rapports Discrawl : La recherche Discord a trouvé des commentaires d'archive fermant les anciens problèmes #67465 et #40242 comme implémentés sur le main actuel, avec des notes indiquant que Browser Talk a maintenant une surface Control UI visible et un RPC de session en temps réel du navigateur.
- Bonnes qualités : Les sessions détenues par le navigateur évitent d'envoyer les clés API du fournisseur au navigateur, le relais Gateway garde les identifiants backend uniquement sur la Gateway, la sélection de transport est explicite, et les API de direction/annulation de run actif sont modélisées.
- Mauvaises qualités : La fonctionnalité est plus nouvelle que le WebChat texte principal, s'étend sur les API audio du navigateur plus les API en temps réel spécifiques au fournisseur, et la parité texte/audio visible est toujours un bord produit actif.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct, et de flux runtime réel affectent uniquement la couverture.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour le démarrage/arrêt de Browser Talk, la sélection de session du fournisseur, l'audio de relais Gateway, les consultations d'appels d'outils, la direction et l'annulation.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les environnements audio du navigateur, la lecture automatique, le refus de permission, et les changements d'appareil nécessitent une preuve opérationnelle plus forte.
- Le Talk en temps réel de salle gérée n'est pas encore disponible dans l'interface utilisateur du navigateur.
- La parité du texte final Talk et de la réponse visible de Control UI nécessite un suivi sur les problèmes d'archive.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente Browser Talk, les options de transport, OpenAI WebRTC, Google Live, relais Gateway, appels d'outils de consultation, contrôles Talk, smoke test en direct du responsable, et comportement des identifiants du fournisseur.
- `/Users/kevinlin/code/openclaw/docs/gateway/protocol.md` documente `talk.catalog`, `talk.config`, `talk.client.create`, `talk.client.toolCall`, `talk.client.steer`, `talk.session.*`, `talk.event`, et `talk.speak`.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md` documente les concepts plus larges du fournisseur Talk.

### Source

- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk.ts` sélectionne les transports Browser Talk et bascule vers le relais Gateway le cas échéant.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk-webrtc.ts` implémente les médias WebRTC du navigateur, les événements du fournisseur, les appels d'outils, et la sortie audio.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk-google-live.ts` implémente l'audio WebSocket du fournisseur.
- `/Users/kevinlin/code/openclaw/ui/src/ui/chat/realtime-talk-gateway-relay.ts` implémente le flux microphone/audio du relais Gateway authentifié.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-client.ts` et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-session.ts` implémentent les RPC Talk détenus par le navigateur et la Gateway.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-webrtc.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-google-live.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-gateway-relay.test.ts`, et `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-consult.test.ts` couvrent les transports Browser Talk et le comportement de consultation.
- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk.test.ts`, et `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-session.ts` couvrent les chemins Gateway Talk.
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts` est le smoke test en direct du responsable documenté pour la configuration OpenAI, Google Live, et relais Gateway.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/talk/talk-session-controller.test.ts`, `/Users/kevinlin/code/openclaw/src/talk/provider-resolver.test.ts`, `/Users/kevinlin/code/openclaw/src/talk/agent-run-control.test.ts`, et `/Users/kevinlin/code/openclaw/src/talk/diagnostics.test.ts` couvrent le comportement du runtime Talk de niveau inférieur.
- `/Users/kevinlin/code/openclaw/ui/src/ui/app.talk.test.ts` couvre l'état Talk au niveau de l'application.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Talk mode Control UI"`

Résultats :

- A retourné le problème ouvert #85275, `Talk mode can speak a different answer than the Control UI when agent reply uses message_tool_only / delivery-mirror`.
- A retourné les problèmes adjacents vocaux #68896 et #73019.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "Talk mode Control UI"`

Résultats :

- A retourné la PR ouverte #85990, `Prefer Talk source-reply final text`.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Control UI Talk realtime WebRTC Google Live gateway relay microphone"`

Résultats :

- A retourné `[]`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 12 "Talk mode Control UI WebChat realtime"`

Résultats :

- A trouvé des commentaires d'archive fermant les anciens problèmes #67465 et #40242 comme implémentés sur le main actuel, avec des notes indiquant que Browser Talk a maintenant une surface Control UI visible et un RPC de session en temps réel du navigateur.
