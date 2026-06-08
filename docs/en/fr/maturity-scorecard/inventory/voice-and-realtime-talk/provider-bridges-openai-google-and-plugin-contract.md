---
title: "Voice et conversation en temps réel - Ponts de fournisseurs pour Openai, Google et note de maturité des contrats de plugin"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voice et conversation en temps réel - Ponts de fournisseurs pour Openai, Google et note de maturité des contrats de plugin

## Résumé

OpenAI Realtime, Google Gemini Live et les fournisseurs de voix en temps réel enregistrés par plugin sont implémentés via des contrats de fournisseur partagés et des sessions de pont. La couverture est au niveau bêta. La qualité reste Alpha car la configuration du fournisseur, l'accès au modèle, la facturation et les changements de feuille de route du fournisseur sont les risques opérateurs les plus visibles.

## Portée de la catégorie

- Pont de backend de voix OpenAI Realtime et chemin d'authentification WebRTC du navigateur.
- Pont de backend Google Gemini Live et chemin de jeton/WebSocket du navigateur.
- Contrats SDK de fournisseur de voix en temps réel, métadonnées d'activation, registre de fournisseur et résolveur.
- Diagnostics de fournisseur, comportement de reconnexion, déclarations d'outils et cycle de vie de la session de pont.

## Fonctionnalités

- Pont de backend de voix OpenAI Realtime : Pont de backend de voix OpenAI Realtime et chemin d'authentification WebRTC du navigateur
- Pont de backend Google Gemini Live : Pont de backend Google Gemini Live et chemin de jeton/WebSocket du navigateur
- Contrats SDK de fournisseur de voix en temps réel : Contrats SDK de fournisseur de voix en temps réel, métadonnées d'activation, registre de fournisseur et résolveur
- Diagnostics de fournisseur : Diagnostics de fournisseur, comportement de reconnexion, déclarations d'outils et cycle de vie de la session de pont

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`

OpenAI et Google disposent de docs de fournisseur, de ponts source, de tests de fournisseur et de chemins de fumée en direct. Le contrat de plugin expose également l'enregistrement de fournisseur et les métadonnées de capacité. La couverture n'est pas stable car les fournisseurs non-OpenAI/Google et les variantes de déploiement de style Azure restent actifs.

## Score de qualité

- Score : `Alpha (68%)`

La qualité est améliorée par la configuration normalisée, la résolution d'authentification, la gestion des événements de pont, la logique de reconnexion, les déclarations d'outils et les capacités de fournisseur explicites. Elle reste Alpha car la configuration du fournisseur est fragile, l'accès à la facturation/au modèle OpenAI peut échouer et les preuves d'archive montrent des changements actifs de feuille de route du fournisseur.

Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : les preuves d'archive, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour le pont de backend de voix OpenAI Realtime, le pont de backend Google Gemini Live, les contrats SDK de fournisseur de voix en temps réel, les diagnostics de fournisseur.
- Signaux négatifs : la note d'archive a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture d'archive.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- OpenAI WebRTC peut échouer lorsque la facturation org/l'accès au modèle est manquant.
- Azure Foundry, ElevenLabs realtime, xAI et les travaux de fournisseur local ne sont pas réglés.
- Le support de cadre de caméra pour Talk en temps réel est toujours ouvert.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md:95` documente les exigences de configuration de voix OpenAI Realtime, les crédits Platform, la clé API et les avertissements OAuth Codex.
- `/Users/kevinlin/code/openclaw/docs/providers/openai.md:708` documente les paramètres de voix realtime OpenAI, les voix, la forme de session GA, les notes Azure, les secrets client WebRTC, le relais backend et la fumée en direct.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:335` documente les paramètres du fournisseur de voix realtime Google, Gemini Live WebSocket, les appels d'outils, les jetons Control UI contraints et la fumée en direct.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-provider-plugins.md:519` documente l'enregistrement de capacité du fournisseur de voix en temps réel et l'intégration du catalogue.

### Source

- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-voice-provider.ts:202` normalise la configuration du fournisseur de voix realtime OpenAI.
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-voice-provider.ts:347` résout l'authentification OpenAI via OAuth Codex, l'environnement ou les paramètres de clé API.
- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-voice-provider.ts:416` implémente la session de pont de voix realtime OpenAI.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:213` normalise la configuration du fournisseur de voix realtime Google.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:308` mappe la configuration Google et les déclarations d'outils.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:436` implémente le pont Google Live.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/realtime-voice.ts:1` exporte le contrat de fournisseur utilisé par les fournisseurs de plugin.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/openai/realtime-voice-provider.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.test.ts`
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/talk/provider-registry.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/provider-resolver.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/activation-name.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/talk-voice/index.test.ts`

### Requêtes Gitcrawl

- `gitcrawl search issues "OpenAI Realtime Talk Google Live" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #86425 pour le support de cadre de caméra et #83822 pour OpenAI WebRTC `model_not_found`.
- `gitcrawl search issues "talk realtime voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #86434 pour la voix realtime ElevenLabs, #87325 pour Azure Foundry GPT Realtime Talk et #73019 pour la proposition de voix realtime xAI.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "OpenAI Realtime Talk Google Live" --limit 5` a retourné les notes de version du 2026-05-03 indiquant que les erreurs realtime s'affichent dans Talk et un commentaire d'archive #7200 listant les chemins OpenAI Realtime expédiés, Google Gemini Live, Browser Talk WebRTC et Gateway relay.
- `/Users/kevinlin/.local/bin/discrawl search "talk realtime voice" --limit 5` a retourné les notes de version pour un Talk plus fort et un contrôle vocal dans l'interface utilisateur Web et la voix Discord.
