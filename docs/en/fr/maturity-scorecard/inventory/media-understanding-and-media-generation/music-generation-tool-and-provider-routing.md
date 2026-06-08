---
title: "Compréhension des médias et génération de médias - Note de maturité de l'outil de génération musicale et du routage des fournisseurs"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de l'outil de génération musicale et du routage des fournisseurs

## Résumé

La génération musicale est implémentée comme un outil de génération de médias asynchrone partagé avec sélection de fournisseur, secours, statut des tâches, modes d'édition d'images pour les fournisseurs capables, et secours en ligne direct en dehors des exécutions soutenues par session. Elle obtient un score inférieur à la génération d'images/vidéos car l'ensemble des fournisseurs est plus petit, la fonctionnalité a été livrée plus tard, et les archives montrent un détachement de livraison et une confusion antérieure « non livrée ».

## Portée de la catégorie

Cette catégorie couvre `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées de référence d'image où supportées, le secours du fournisseur, le cycle de vie des tâches en arrière-plan, le statut des tâches en double, la génération en ligne sans session, la persistance de l'audio généré, et l'enregistrement du fournisseur SDK.

## Fonctionnalités

- Invocation de l'outil de génération musicale : Couvre l'invocation de l'outil de génération musicale sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées de référence d'image où supportées, et le comportement associé de l'outil de génération musicale et du routage des fournisseurs.
- Sélection du fournisseur et du modèle : Couvre la sélection du fournisseur et du modèle sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées de référence d'image où supportées, et le comportement associé de l'outil de génération musicale et du routage des fournisseurs.
- Contrôles de paroles, instrumental, durée et format : Couvre les contrôles de paroles, instrumental, durée et format sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées de référence d'image où supportées, et le comportement associé de l'outil de génération musicale et du routage des fournisseurs.
- Entrées de référence où supportées : Couvre les entrées de référence où supportées sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées de référence d'image où supportées, et le comportement associé de l'outil de génération musicale et du routage des fournisseurs.
- Cycle de vie des tâches musicales et statut des doublons : Couvre le cycle de vie des tâches musicales et le statut des doublons sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées de référence d'image où supportées, et le comportement associé de l'outil de génération musicale et du routage des fournisseurs.
- Persistance et livraison de l'audio généré : Couvre la persistance et la livraison de l'audio généré sur `music_generate`, la configuration du fournisseur/modèle, les contrôles de paroles/instrumental/durée/format, les entrées de référence d'image où supportées, et le comportement associé de l'outil de génération musicale et du routage des fournisseurs.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : Les docs couvrent le démarrage rapide, les fournisseurs, la matrice de capacités, les paramètres, le cycle de vie asynchrone, les actions de statut/liste, l'ordre de secours, et les notes des fournisseurs. La source a un runtime dédié, la normalisation des capacités, le cycle de vie des tâches, le statut, et les surfaces SDK.
- Signaux négatifs : Le nombre de fournisseurs et les modes sont plus étroits que la génération d'images/vidéos, et la preuve en direct est moins visible.
- Lacunes d'intégration : La livraison musicale via les canaux a des preuves d'archives directes de problèmes de détachement et de remise de livraison.

## Score de qualité

- Score : `Alpha (64%)`
- Rapports Gitcrawl : #79535 dit que la génération vidéo OpenRouter a échoué silencieusement et la génération musicale n'avait pas été livrée à ce moment ; #84506 demande à la génération musicale MiniMax d'utiliser l'interrogation asynchrone ; #86034/#86279 montrent l'échec de la livraison de génération de médias partagée ; #87741 couvre le secours du verrou de remise de médias générés.
- Rapports Discrawl : Plusieurs messages d'archives de clawtributors/mainteneurs disent que `music_generate` s'est terminé mais la livraison Discord visible a échoué, la fin s'est détachée, ou l'artefact local `MEDIA:` n'a pas été transféré dans la livraison de pièce jointe de message.
- Bonnes qualités : L'outil bloque les appels actifs en double, expose le statut de la tâche, avertit l'agent d'achèvement des réponses finales privées, et utilise le secours/normalisation du fournisseur partagé.
- Mauvaises qualités : La sémantique de livraison reste fragile dans les sessions reprises/canaux, et la fonctionnalité est plus récente avec moins de fournisseurs et moins de mémoire musculaire de l'opérateur.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les archives docs, source, test, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour l'invocation de l'outil de génération musicale, la sélection du fournisseur et du modèle, les contrôles de paroles, instrumental, durée et format, les entrées de référence où supportées, le cycle de vie des tâches musicales et le statut des doublons, la persistance et la livraison de l'audio généré.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La livraison des médias d'achèvement reste la lacune la plus importante visible par l'utilisateur.
- La sémantique d'interrogation spécifique au fournisseur et des tâches longues sont toujours en cours de raffinement.
- Les docs sont adéquates pour la configuration, mais moins de fiches de score réelles fournisseur/canal existent que pour l'image/TTS.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/music-generation.md` documente `music_generate`, les fournisseurs, les paramètres, le cycle de vie asynchrone, le statut des tâches, le secours, et les notes des fournisseurs.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` documente la génération musicale et le comportement de génération de médias asynchrone.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/tools/music-generate-tool.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/music-generate-tool.actions.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/music-generate-background.ts`
- `/Users/kevinlin/code/openclaw/src/music-generation/runtime.ts`
- `/Users/kevinlin/code/openclaw/src/music-generation/capabilities.ts`
- `/Users/kevinlin/code/openclaw/src/music-generation/normalization.ts`
- `/Users/kevinlin/code/openclaw/src/music-generation/provider-registry.ts`
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/music-generation.ts`
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/music-generation-core.ts`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.generation.test-support.ts`
- `/Users/kevinlin/code/openclaw/src/media-generation/provider-capabilities.contract.test.ts`
- `/Users/kevinlin/code/openclaw/src/music-generation/live-test-helpers.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/tools/music-generate-tool.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/music-generate-tool.status.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/music-generate-background.test.ts`
- `/Users/kevinlin/code/openclaw/src/music-generation/runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/music-generation/capabilities.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-generation/runtime-shared.test.ts`

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "music generation never shipped" --json
```

Résultats :

- A retourné #79535 signalant que la génération vidéo OpenRouter échoue silencieusement et la génération musicale n'a pas été livrée à ce moment.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "media generation completion delivery" --json
```

Résultats :

- A retourné #86034/#86279 pour l'échec de livraison après une génération réussie et #87741 pour le secours du verrou de remise de médias générés.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "media generation completion delivery" --limit 5
```

Résultats :

- A retourné les rapports des clawtributors du 2026-05-23 et 2026-05-15 où une tâche de génération MP3 s'est terminée ou la notification a été retournée mais la session manquait/échouait la livraison visible de pièce jointe de message.
- A retourné le rapport du mainteneur du 2026-05-05 pour une tâche `music_generate` terminée dont l'agent d'achèvement n'a pas pu livrer via l'outil de message.
