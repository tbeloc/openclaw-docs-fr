---
title: "Compréhension des médias et génération de médias - Note de maturité de la compréhension des médias"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Compréhension des médias et génération de médias - Note de maturité de la compréhension des médias

## Résumé

La compréhension des images a un véritable chemin produit à travers les pièces jointes entrantes, `openclaw infer image`, le routage actif du modèle de vision, et les références `media://inbound`. Ce n'est pas stable car les problèmes archivés montrent toujours des régressions de sélection de route, de mode d'authentification, de dépendance et de capacité du fournisseur autour du même chemin utilisateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Sélection de pièce jointe audio : Couvre la sélection de pièce jointe audio à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Fournisseur STT par lot et solution de secours CLI : Couvre le fournisseur STT par lot et la solution de secours CLI à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Vérification préalable de la mention de note vocale : Couvre la vérification préalable de la mention de note vocale à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Insertion et écho de transcription : Couvre l'insertion et l'écho de transcription à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Gestion du proxy audio et des limites : Couvre la gestion du proxy audio et des limites à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Résumé des images entrantes : Couvre le résumé des images entrantes à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Contournement du modèle de vision actif : Couvre le contournement du modèle de vision actif à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Déchargement des médias du modèle texte uniquement : Couvre le déchargement des médias du modèle texte uniquement à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Secours du fournisseur de vision : Couvre le secours du fournisseur de vision à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Routage des entrées image et PDF : Couvre le routage des entrées image et PDF à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Compréhension vidéo : Couvre la compréhension vidéo à travers le résumé vidéo avant le routage des réponses, les entrées de médias vidéo du fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction des demandes vidéo, et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.
- Analyse vidéo directe : Couvre l'analyse vidéo directe à travers le résumé vidéo avant le routage des réponses, les entrées de médias vidéo du fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction des demandes vidéo, et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.

## Fonctionnalités

- Sélection de pièce jointe audio : Couvre la sélection de pièce jointe audio à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Fournisseur STT par lot et solution de secours CLI : Couvre le fournisseur STT par lot et la solution de secours CLI à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Vérification préalable de la mention de note vocale : Couvre la vérification préalable de la mention de note vocale à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Insertion et écho de transcription : Couvre l'insertion et l'écho de transcription à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Gestion du proxy audio et des limites : Couvre la gestion du proxy audio et des limites à travers la compréhension des médias audio/STT par lot, les solutions de secours CLI locales, la transcription du fournisseur, la vérification préalable des notes vocales avant les portes de mention, et le comportement associé de compréhension des notes vocales et de transcription audio.
- Résumé des images entrantes : Couvre le résumé des images entrantes à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Contournement du modèle de vision actif : Couvre le contournement du modèle de vision actif à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Déchargement des médias du modèle texte uniquement : Couvre le déchargement des médias du modèle texte uniquement à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Secours du fournisseur de vision : Couvre le secours du fournisseur de vision à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Routage des entrées image et PDF : Couvre le routage des entrées image et PDF à travers le résumé des images avant le routage des réponses, le comportement de contournement de la vision du modèle actif, le déchargement des modèles texte uniquement via `MediaPaths`/`media://inbound`, la résolution du secours du modèle d'image, et le comportement associé de compréhension des images et de routage de la vision.
- Compréhension vidéo : Couvre la compréhension vidéo à travers le résumé vidéo avant le routage des réponses, les entrées de médias vidéo du fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction des demandes vidéo, et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.
- Analyse vidéo directe : Couvre l'analyse vidéo directe à travers le résumé vidéo avant le routage des réponses, les entrées de médias vidéo du fournisseur/CLI, les contrôles de taille et de délai d'expiration, le support du proxy, la construction des demandes vidéo, et les chemins d'analyse vidéo directe. Elle ne note pas la génération vidéo.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation publique décrit la compréhension des images, le contournement du modèle de vision actif, le déchargement texte uniquement, les valeurs par défaut du modèle d'image, le routage du fournisseur Ollama/personnalisé, et la description d'image CLI. La source a un runtime d'image ciblé, un registre de fournisseurs, une sélection de pièce jointe, un ordre de prompt, et des chemins d'hydratation `media://inbound`.
- Signaux négatifs : Le chemin utilisateur principal s'étend sur Gateway/WebChat, la réponse automatique, le magasin de médias, la sélection du modèle, et les plugins de fournisseur ; la preuve en direct est plus mince que la couverture source/unité pour les combinaisons spécifiques au fournisseur.
- Lacunes d'intégration : La parité entre clients pour les téléchargements d'images WebChat, le secours de l'outil PDF/image, et `agents.defaults.imageModel` sans fournisseur reste largement couverte par les régressions ciblées et l'examen d'archive plutôt que par les balayages de scénarios récurrents.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : Les problèmes/PR ouverts pertinents incluent le contournement de route via la sélection automatique directe d'OpenAI (#87168), la compréhension des médias-core manquant `sharp` après l'installation globale (#77760), les défaillances d'authentification Bedrock/aws-sdk (#72031), le routage silencieux vers des modèles de vision non déclarés (#81525), et les boucles de délai serré (#80771).
- Rapports Discrawl : L'archive du responsable enregistre explicitement la régression de la gestion des images WebChat : #82524 a contourné `MediaPaths`/media-understanding par étapes pour les sessions texte uniquement, a cassé les formes de demande Moonshot/Kimi/opencode-go, et #85501 a restauré le routage media-understanding.
- Bonnes qualités : La route préserve intentionnellement les pièces jointes originales, évite les blocs de résumé redondants lorsque le modèle principal supporte les images, résout `imageModel` dans la couche media-understanding, et expose les raisons d'échec du fournisseur/modèle.
- Mauvaises qualités : Le comportement visible par l'utilisateur est sensible à la sélection du profil d'authentification, à la mise en scène des dépendances d'exécution, aux métadonnées de capacité du modèle, et à si la route active est Gateway/WebChat, CLI, plugin, ou ACP.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct, et de flux d'exécution.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/media-understanding-and-media-generation.md`.
- Signaux positifs : les documents archivés, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour la sélection de pièce jointe audio, le fournisseur STT par lot et la solution de secours CLI, la vérification préalable de la mention de note vocale, l'insertion et l'écho de transcription, la gestion du proxy audio et des limites, le résumé des images entrantes, le contournement du modèle de vision actif, le déchargement des médias du modèle texte uniquement, le secours du fournisseur de vision, le routage des entrées image et PDF, la compréhension vidéo, l'analyse vidéo directe.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les enregistrements d'archive récurrents montrent que de petits changements de routage peuvent contourner le chemin de médias prévu et produire des défaillances spécifiques au fournisseur.
- La mise en scène des dépendances pour le chemin d'image core media-understanding a causé des défaillances d'installation/exécution.
- La parité directe de téléchargement vidéo/PDF/image est adjacente et toujours pas entièrement régularisée sur chaque surface client.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/nodes/media-understanding.md` documente la collecte de médias image, `tools.media.image`, le saut de modèle de vision actif, la préservation de `media://inbound` pour les modèles Gateway/WebChat texte uniquement, `agents.defaults.imageModel`, l'ordre de secours du fournisseur, et les matrices de capacité.
- `/Users/kevinlin/code/openclaw/docs/nodes/images.md` documente les règles de gestion des images/médias, le modèle de commande, l'insertion de compréhension des médias, et les plafonds de taille par défaut.
- `/Users/kevinlin/code/openclaw/docs/cli/infer.md` documente `image describe`/`describe-many`, les remplacements de prompt, les modèles de vision Ollama locaux, et les délais d'expiration.
- `/Users/kevinlin/code/openclaw/docs/tools/pdf.md` documente les références `media://inbound/<id>` entrantes et le comportement de secours de vision image/PDF.

## Source

- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.ts` sélectionne les pièces jointes, résout `agents.defaults.imageModel`, ignore la compréhension des images lorsque le modèle actif supporte la vision, et applique les décisions médias dans le contexte de réponse.
- `/Users/kevinlin/code/openclaw/src/media-understanding/image.ts` et `/Users/kevinlin/code/openclaw/src/media-understanding/image-runtime.ts` implémentent l'exécution du fournisseur d'images.
- `/Users/kevinlin/code/openclaw/src/media-understanding/provider-capability-registry.ts`, `/Users/kevinlin/code/openclaw/src/media-understanding/provider-registry.ts`, et `/Users/kevinlin/code/openclaw/src/media-understanding/provider-supports.ts` définissent l'enregistrement des capacités/fournisseurs.
- `/Users/kevinlin/code/openclaw/src/media/prompt-image-order.ts`, `/Users/kevinlin/code/openclaw/src/media/media-reference.ts`, et `/Users/kevinlin/code/openclaw/src/media/store.ts` supportent l'ordre des images et les références entrantes gérées.
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-tool.ts` hydrate les entrées de l'outil image, y compris les références `media://inbound`.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/control-ui-assistant-media.e2e.test.ts` exerce les chemins médias de l'assistant Control UI.
- `/Users/kevinlin/code/openclaw/src/cli/program.nodes-media.e2e.test.ts` couvre le comportement du nœud média CLI.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/get-reply-run.media-only.test.ts` couvre l'hydratation `MediaPaths` du tour actuel et l'interaction de la compréhension des images avec les tours d'agent.
- `/Users/kevinlin/code/openclaw/src/auto-reply/reply/dispatch-acp.test.ts` couvre les chemins de dispatch de compréhension des médias ACP.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/media-understanding/image.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/runner.vision-skip.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/provider-capability-registry.test.ts`
- `/Users/kevinlin/code/openclaw/src/media-understanding/media-understanding-url-fallback.test.ts`
- `/Users/kevinlin/code/openclaw/src/agents/tools/image-tool.test.ts`

## Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "image media understanding" --json
```

Résultats :

- A retourné les threads ouverts pertinents incluant #57259 pour le support du fournisseur d'images GitHub Copilot, #77760 pour `sharp` manquant dans `media-understanding-core`, #87185 pour la compréhension des médias image/PDF Codex bornée, #72031 pour l'échec d'authentification aws-sdk, #81525 pour les capacités d'image déclarées non validées, #80771 pour l'effondrement du délai d'image, et #79626 pour la détection MIME d'image.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "media understanding" --json
```

Résultats :

- A retourné les problèmes plus larges d'enregistrement/routage et de sélection de modèle, incluant l'isolation du module fournisseur cassée (#77843), la déclaration du modèle choisi (#62924), et les cas de contournement de route image texte uniquement.

## Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl search "image media understanding" --limit 5
```

Résultats :

- Le résultat d'archive des mainteneurs du 2026-05-23 décrit #82524 changeant les téléchargements d'images WebChat texte uniquement de `MediaPaths` mis en scène/compréhension des médias à la substitution du modèle d'image en ligne, cassant les formes de requête Moonshot/Kimi et opencode-go ; #85501 a restauré le routage de compréhension des médias.
- Le résultat Clawtributors du 2026-04-29 décrit une régression de dépendance `sharp` de `media-understanding-core` après que la mise en scène des dépendances d'exécution ait été déplacée.
- Un digest de mainteneur du 2026-04-29 appelle les délais d'expiration de compréhension des médias et l'agitation des dépendances d'exécution des plugins comme des incendies actifs de passerelle/perf.
