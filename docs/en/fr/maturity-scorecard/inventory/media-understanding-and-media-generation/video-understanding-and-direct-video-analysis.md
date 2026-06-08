---
title: "Compréhension des médias et génération de médias - Note de maturité de la compréhension vidéo et de l'analyse vidéo directe"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de la compréhension vidéo et de l'analyse vidéo directe

## Résumé

La compréhension vidéo existe en tant que capacité partagée de compréhension des médias avec enregistrement des fournisseurs, chemins de description de style CLI, support des fournisseurs Qwen/Google/Moonshot, limites de taille et insertion du contexte de réponse. Elle reste de qualité alpha car la parité de téléchargement vidéo direct et le support du chemin client sont explicitement encore inégaux dans les archives.

## Portée de la catégorie

Cette catégorie couvre le résumé vidéo avant le routage des réponses, les entrées de médias vidéo fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction des demandes vidéo et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.

## Fonctionnalités

- Compréhension vidéo : couvre la compréhension vidéo sur le résumé vidéo avant le routage des réponses, les entrées de médias vidéo fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction des demandes vidéo et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.
- Analyse vidéo directe : couvre l'analyse vidéo directe sur le résumé vidéo avant le routage des réponses, les entrées de médias vidéo fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction des demandes vidéo et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : la documentation et le code source décrivent les modèles de compréhension des médias vidéo, le support des fournisseurs, les limites de taille, le support du proxy et le comportement de secours. Les tests couvrent le comportement vidéo du runner et la construction des demandes des fournisseurs.
- Signaux négatifs : la vidéo est plus récente et plus étroite que l'image/audio ; le téléchargement vidéo direct via les surfaces de téléchargement de chat/message n'est explicitement pas uniformément implémenté.
- Lacunes d'intégration : la preuve la plus solide provient du code source et des tests ciblés, avec moins de preuve de scénario récurrent sur l'interface utilisateur de contrôle, WebChat, les téléchargements de canal et les modèles vidéo spécifiques aux fournisseurs.

## Score de qualité

- Score : `Alpha (62%)`
- Rapports Gitcrawl : #27482 reste ouvert pour le téléchargement vidéo direct via chat/message ; #38623 a été fermé comme implémenté pour l'analyse vidéo partagée des fournisseurs ; #78797 suit la compréhension audio/vidéo native ; #72092/#72031 montrent des problèmes de cohérence du mode d'authentification sur les chemins image/audio/vidéo.
- Rapports Discrawl : le résultat d'archive sur #27482 indique que le main actuel dispose de la plomberie de compréhension des médias vidéo et du CLI `video describe`, mais les chemins d'interface utilisateur de contrôle et de pièce jointe de passerelle restent orientés image et suppriment ou convertissent les pièces jointes non-image.
- Bonnes qualités : le support des fournisseurs est explicite, le comportement de secours/saut est partagé avec le runner de médias, et la fonctionnalité réutilise la sémantique de compréhension des médias au meilleur effort au lieu de bloquer les réponses.
- Mauvaises qualités : le comportement vidéo côté utilisateur est fragmenté : l'analyse des fournisseurs existe, mais les surfaces de téléchargement/pièce jointe et la parité client sont à la traîne par rapport au runner principal.
- Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les archives de documentation, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la compréhension vidéo et l'analyse vidéo directe.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le téléchargement vidéo direct via les surfaces de chat/message n'est toujours pas uniformément disponible.
- Les contraintes spécifiques aux fournisseurs et les formulaires de téléchargement ne sont pas encore masqués derrière un chemin utilisateur stable.
- La documentation explique la configuration, mais elle ne présente pas un large tableau de bord d'opérateur pour le support des pièces jointes vidéo par client/canal.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/nodes/media-understanding.md` documente `tools.media.video`, les entrées fournisseur/CLI, les valeurs par défaut de maxBytes vidéo, la matrice de support des fournisseurs et le support du proxy.
- `/Users/kevinlin/code/openclaw/docs/tools/media-overview.md` répertorie la compréhension des médias vidéo dans la matrice des capacités.
- `/Users/kevinlin/code/openclaw/docs/nodes/images.md` décrit les descriptions image/vidéo préservant les légendes pour l'analyse des commandes dans le pipeline de médias entrants.

### Code source

- `/Users/kevinlin/code/openclaw/src/media-understanding/video.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/openai-compatible-video.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.video.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/entry-capabilities.ts`
- `/Users/kevinlin/code/openclaw/src/media/video-dimensions.ts`
- `/Users/kevinlin/code/openclaw/src/media/ffmpeg-exec.ts`

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/get-reply-run.media-only.test.ts` inclut la gestion des exécutions de réponse uniquement pour les médias pertinente à la préservation des pièces jointes vidéo.
- `/Users/kevinlin/code/openclaw/src/cli/program.nodes-media.e2e.test.ts` couvre les chemins des nœuds de médias CLI.
- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-assistant-media.e2e.test.ts` couvre les médias de l'assistant de l'interface utilisateur de contrôle, bien que les preuves d'archive indiquent que le téléchargement vidéo direct reste plus faible que l'image.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.video.test.ts`
- `/Users/kevinlin/code/openclaw/src/media/video-dimensions.test.ts`
- `/Users/kevinlin/code/openclaw/src/media/ffmpeg-exec.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/provider-capability-registry.test.ts`

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "video media understanding" --json
```

Résultats :

- A retourné #78797 compréhension audio/vidéo native, #75005 fournisseurs de médias plugin/sans authentification, #73817 points de terminaison privés, #27482 téléchargement vidéo direct, #72092 mode d'authentification pour image et audio/vidéo, #62924 rapport du modèle choisi et #38623 contexte de support de téléchargement/modèle vidéo direct.

### Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "video media understanding" --limit 5
```

Résultats :

- A retourné #38623 fermé comme implémenté pour l'analyse vidéo partagée des fournisseurs de compréhension des médias et l'enregistrement de Qwen.
- A retourné #27482 examen indiquant que la compréhension des médias vidéo et le CLI `video describe` existent, mais les chemins d'interface utilisateur de contrôle et de pièce jointe de passerelle restent orientés image pour le téléchargement direct.
