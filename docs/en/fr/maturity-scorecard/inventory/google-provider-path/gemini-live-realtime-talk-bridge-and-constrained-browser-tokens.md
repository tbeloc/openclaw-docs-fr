---
title: "Chemin du fournisseur Google - Note de maturité Gemini Live Talk"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Google - Note de maturité Gemini Live Talk

## Résumé

Le support Gemini Live est un vrai chemin de fournisseur Google avec un
fournisseur de voix en temps réel, une intégration de relais de passerelle Talk,
des jetons de session de navigateur contraints, la gestion des événements
audio/transcription/appel d'outil, les reconnexions et un script de smoke live
de développement. La couverture est Beta car le pont dispose de preuves source,
unitaires, UI et smoke. La qualité est Alpha car les preuves d'archive signalent
un comportement de consultation d'appel live fragile et des corrections de
schéma en temps réel actives.

## Portée de la catégorie

Cette catégorie couvre le comportement du fournisseur de voix en temps réel
Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur
contraints, la mise en file d'attente audio, les événements de transcription,
les appels d'outil Live, la reprise de session, les reconnexions et l'exécution
locale du smoke live. Elle exclut le transport texte Google non-temps réel et
les fonctionnalités médias adaptateur uniquement.

## Fonctionnalités

- Sessions de voix en temps réel : Couvre les sessions de voix en temps réel sur le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio et le comportement gemini live talk associé.
- Jetons de navigateur contraints : Couvre les jetons de navigateur contraints sur le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio et le comportement gemini live talk associé.
- Événements audio et transcription : Couvre les événements audio et transcription sur le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio et le comportement gemini live talk associé.
- Appels d'outil live : Couvre les appels d'outil live sur le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio et le comportement gemini live talk associé.
- Reconnexions de session : Couvre les reconnexions de session sur le comportement du fournisseur de voix en temps réel Gemini Live, l'intégration du relais Talk, les jetons websocket de navigateur contraints, la mise en file d'attente audio et le comportement gemini live talk associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : La source couvre la normalisation de la configuration du
  fournisseur, les charges utiles de connexion Live, la mise en file d'attente
  audio, la gestion de la transcription, la continuation d'appel d'outil, la
  création de jetons de navigateur et l'intégration du relais de passerelle ;
  les tests unitaires/UI et un script de smoke live couvrent les chemins clés.
- Signaux négatifs : L'exécution réelle du smoke Google Live et du relais de
  passerelle est optionnelle et dépend des identifiants.
- Lacunes d'intégration : Aucune matrice live toujours activée large n'a été
  trouvée pour les appels lourds en consultation, l'expiration des jetons de
  navigateur, les reconnexions et la continuation d'appel d'outil.

## Score de qualité

- Score : `Alpha (65%)`
- Rapports Gitcrawl : #79572 est une RP Google realtime ouverte pour utiliser
  `parameters` plutôt que `parametersJsonSchema` dans les
  FunctionDeclarations en temps réel.
- Rapports Discrawl : `Google Live Talk Gemini realtime` a trouvé #71849,
  signalant que la consultation vocale en temps réel est trop lente ou fragile
  pour les appels live, avec des questions de contexte mémoire et la gestion
  des appels d'outil/consultation Google Live signalées.
- Bonnes qualités : La source utilise des jetons de navigateur contraints à
  usage unique, des contrats audio explicites, une configuration Live scoped au
  fournisseur, une planification de reconnexion, une reprise de session et une
  gestion des appels d'outil côté relais.
- Mauvaises qualités : La qualité vocale live dépend de la latence du
  fournisseur, de la continuation de la consultation, de la durée de vie du
  jeton de navigateur, du comportement websocket et des détails de schéma qui
  sont encore en évolution.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration,
  e2e, live et de flux d'exécution réel ; ceux-ci sont des entrées de couverture
  uniquement.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à
  `references/completeness/google-provider-path.md`.
- Signaux positifs : les preuves de docs archivées, source, test, Gitcrawl et
  Discrawl couvrent la portée de la taxonomie pour les sessions de voix en temps
  réel, les jetons de navigateur contraints, les événements audio et
  transcription, les appels d'outil live, les reconnexions de session.
- Signaux négatifs : la note archivée a précédé le score de complétude de la
  version 3 du processus, donc ce score est initialisé à partir de la même
  largeur de preuves et du registre des lacunes connues utilisés pour le score
  de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves`
  ci-dessous pour les branches manquantes enregistrées et les avertissements
  visibles par l'opérateur.

## Lacunes connues

- Les flux Gemini Live lourds en consultation ont besoin de preuves live
  récurrentes.
- Le comportement de reconnexion et de reprise de session est complexe et
  sensible au fournisseur.
- Les contraintes de jetons de navigateur sont une bonne posture de sécurité,
  mais elles augmentent le besoin de validation d'expiration et d'usage unique
  de bout en bout.
- Les preuves d'archive montrent que la dérive du schéma de déclaration de
  fonction peut casser les appels d'outil en temps réel.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/google.md:335` documente le
  support de la voix en temps réel Google et de l'API Live.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:350` documente les
  paramètres en temps réel Google, y compris le modèle, la voix, la clé API, la
  langue, la température et le format audio.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:377` documente le
  comportement websocket/appel de fonction Google Live.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:400` documente la
  commande smoke live Talk en temps réel.

### Source

- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:47`
  définit les valeurs par défaut Gemini Live.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:298`
  construit la réflexion, l'entrée en temps réel, les déclarations de fonction
  et la configuration de connexion Live.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:436`
  connecte le pont Google en temps réel avec les rappels de reprise et
  reconnexion.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:523`
  gère la mise en file d'attente audio et le comportement de fin de flux.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:584`
  soumet les résultats d'outil et gère la continuation de consultation.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:847`
  crée des sessions de navigateur contraintes.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.ts:908`
  expose les capacités du fournisseur et la création de session.
- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.ts:298`
  crée des sessions de relais Talk et câble les événements du pont.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts:306`
  crée des jetons Google Live contraints.
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts:340`
  teste la configuration websocket du navigateur Google Live.
- `/Users/kevinlin/code/openclaw/scripts/dev/realtime-talk-live-smoke.ts:435`
  teste l'adaptateur de navigateur du relais de passerelle.
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-google-live.test.ts`
  couvre le comportement de l'UI Google Live.
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-gateway-relay.test.ts`
  couvre le comportement de l'UI du relais de passerelle Talk.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.test.ts:118`
  couvre les capacités du fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.test.ts:139`
  couvre la normalisation de la configuration et le repli.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.test.ts:188`
  couvre la configuration de connexion Live et les déclarations d'outil.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.test.ts:299`
  couvre la gestion invalide de VAD/budget et la réflexion dynamique.
- `/Users/kevinlin/code/openclaw/extensions/google/realtime-voice-provider.test.ts:364`
  couvre les sessions de navigateur contraintes.

### Requêtes Gitcrawl

Requête : `gitcrawl search issues "Google Live Talk Gemini realtime" -R openclaw/openclaw --state all`

Résultats :

- La requête de problème exacte n'a retourné aucun résultat direct.

Requête : `gitcrawl search prs "Google Live Gemini realtime" -R openclaw/openclaw --state all`

Résultats :

- #79572 ouverte `fix(google): use parameters not parametersJsonSchema in realtime FunctionDeclarations`.
- Les autres résultats incluaient des RP adjacentes en temps réel et de
  transcription, pas toutes spécifiques à Google.

### Requêtes Discrawl

Requête : `discrawl search --limit 5 "Google Live Talk Gemini realtime"`

Résultats :

- A retourné #71849 décrivant la consultation vocale en temps réel comme trop
  lente/fragile pour les appels live, y compris les préoccupations concernant
  la gestion des appels d'outil/consultation Google Gemini Live.
- A retourné le contexte des notes de version et des fonctionnalités livrées
  pour les fournisseurs de médias en temps réel Twilio, OpenAI Realtime, Google
  Gemini Live, Browser Talk WebRTC et Google Meet/Chrome/Twilio en temps réel.
