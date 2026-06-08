---
title: "Fournisseurs hébergés long-tail - Note de maturité des fournisseurs LLM hébergés régionaux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs hébergés long-tail - Note de maturité des fournisseurs LLM hébergés régionaux

## Résumé

Les fournisseurs LLM hébergés régionaux sont en Alpha. OpenClaw dispose d'une couverture large des manifestes/docs et de chemins en direct sélectionnés pour Kimi, MiniMax, BytePlus et Xiaomi, mais les plans de compte régionaux, les variantes de points de terminaison, les ID de modèles et les fonctionnalités spécifiques aux fournisseurs maintiennent une preuve d'exécution inégale.

## Portée de la catégorie

Cette note couvre les familles de fournisseurs hébergés Qwen, Alibaba, Tencent, Qianfan, ZAI, Moonshot/Kimi, StepFun, MiniMax, BytePlus, Volcengine et Xiaomi.

Hors de portée : accès hébergé par OpenRouter aux mêmes modèles, routes de modèles locaux et fournisseurs génériques de génération de médias sauf si le fournisseur régional possède le chemin du fournisseur.

## Fonctionnalités

- Configuration du fournisseur régional : couvre la configuration du fournisseur régional sur Qwen, Alibaba, Tencent, Qianfan et le comportement des fournisseurs llm hébergés régionaux connexes.
- Routage régional et par plan : couvre le routage régional et par plan sur Qwen, Alibaba, Tencent, Qianfan et le comportement des fournisseurs llm hébergés régionaux connexes.
- Smoke test régional en direct : couvre le smoke test régional en direct sur Qwen, Alibaba, Tencent, Qianfan et le comportement des fournisseurs llm hébergés régionaux connexes.
- Diagnostics des prérequis de compte : couvre les diagnostics des prérequis de compte sur Qwen, Alibaba, Tencent, Qianfan et le comportement des fournisseurs llm hébergés régionaux connexes.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs :
  - Les docs et manifestes des fournisseurs existent pour de nombreux fournisseurs régionaux.
  - `docs/concepts/model-providers.md` répertorie les ID de fournisseurs régionaux, les variables d'env d'authentification et les exemples pour BytePlus, Kimi, MiniMax, Moonshot, Qianfan, Qwen, StepFun, Volcengine, Xiaomi et ZAI.
  - Les tests en direct Moonshot/Kimi et MiniMax couvrent les outils de recherche web appartenant au fournisseur.
  - Les tests en direct BytePlus et Xiaomi couvrent les routes hébergées spécifiques au fournisseur.
  - Les suites de médias partagées en direct incluent Alibaba, BytePlus, MiniMax, Qwen et les fournisseurs hébergés connexes.
- Signaux négatifs :
  - Plusieurs fournisseurs ont une couverture de manifeste/source sans preuve en direct équivalente de génération de texte.
  - Les variantes de plan et les choix de points de terminaison régionaux créent un comportement d'authentification/configuration non uniforme.
  - Les requêtes d'archive pour la phrase exacte du fournisseur régional ont retourné peu de preuves GitHub directes.

## Score de qualité

- Score : `Alpha (60%)`
- Bonnes qualités :
  - Les fournisseurs régionaux utilisent des manifestes appartenant au plugin et des métadonnées de configuration/authentification au lieu de la configuration utilisateur personnalisée seule.
  - Les docs d'intégration préfiltrent les choix de fournisseur et reviennent en arrière quand aucun modèle n'est chargé.
  - MiniMax, Moonshot/Kimi, BytePlus et Xiaomi maintiennent le routage spécifique au fournisseur et le comportement des fonctionnalités dans des plugins dédiés.
- Mauvaises qualités :
  - Les fournisseurs régionaux ont une variance élevée dans la disponibilité des plans, la région, le point de terminaison, l'ID de modèle, la forme OAuth/clé API et le comportement des fonctionnalités hébergées.
  - Certains fournisseurs partagent des familles de modèles entre les fournisseurs, OpenRouter, les routes de plan et les chemins locaux/proxy, ce qui rend le routage visible par l'utilisateur facile à confondre.
  - Les preuves Discord montrent les listes de clés du registre des fournisseurs et la confusion des paramètres d'authentification/modèle autour des fournisseurs régionaux.
- Exclues de la qualité :
  - Les preuves unitaires, d'intégration et en direct ont été utilisées uniquement pour le score de couverture.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/long-tail-hosted-providers.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration du fournisseur régional, le routage régional et par plan, le smoke test régional en direct, les diagnostics des prérequis de compte.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un smoke test en direct de texte récurrent représentatif par famille de fournisseur régional.
- Ajouter un tableau de route de fournisseur régional généré qui sépare les chemins natifs hébergés, par plan, OpenRouter et locaux/proxy.
- Ajouter les prérequis de compte/région à chaque doc de fournisseur régional.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/index.md:27` : les docs des fournisseurs incluent Alibaba Model Studio.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:33` : le répertoire des fournisseurs lie BytePlus aux concepts des fournisseurs de modèles.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:52` : les docs des fournisseurs incluent MiniMax.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:54` : les docs des fournisseurs incluent Moonshot AI.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:62` : les docs des fournisseurs incluent Qianfan.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:63` : les docs des fournisseurs incluent Qwen Cloud.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:67` : les docs des fournisseurs incluent StepFun.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:69` : les docs des fournisseurs incluent Tencent Cloud.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:74` : les docs des fournisseurs incluent Volcengine.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:77` : les docs des fournisseurs incluent Xiaomi.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:78` : les docs des fournisseurs incluent Z.AI.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:295` : le tableau des fournisseurs groupés répertorie les routes de style BytePlus, Kimi, MiniMax, Moonshot, Qianfan, Qwen, StepFun, Volcengine, Xiaomi et ZAI.
- `/Users/kevinlin/code/openclaw/docs/cli/onboard.md:216` : l'intégration préfiltre les choix de fournisseur et documente les variantes de plan Volcengine/BytePlus.

### Source

- `/Users/kevinlin/code/openclaw/extensions/qwen/openclaw.plugin.json:2` : Qwen est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/alibaba/openclaw.plugin.json:2` : Alibaba est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/tencent/openclaw.plugin.json:2` : Tencent est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/qianfan/openclaw.plugin.json:2` : Qianfan est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/zai/openclaw.plugin.json:2` : ZAI est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/moonshot/openclaw.plugin.json:2` : Moonshot est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/stepfun/openclaw.plugin.json:2` : StepFun est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/minimax/openclaw.plugin.json:2` : MiniMax est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/byteplus/openclaw.plugin.json:2` : BytePlus est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/volcengine/openclaw.plugin.json:2` : Volcengine est livré en tant que plugin de fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/xiaomi/openclaw.plugin.json:2` : Xiaomi est livré en tant que plugin de fournisseur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/moonshot/moonshot.live.test.ts:21` : le test en direct Moonshot exécute la recherche web Kimi via l'outil du fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/minimax/minimax.live.test.ts:37` : le test en direct MiniMax exécute la recherche web appartenant au fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/minimax/minimax.live.test.ts:53` : le test en direct MiniMax synthétise TTS via le fournisseur enregistré.
- `/Users/kevinlin/code/openclaw/extensions/byteplus/live.test.ts:25` : le test en direct BytePlus retourne le texte de l'assistant et gère les erreurs d'abonnement.
- `/Users/kevinlin/code/openclaw/extensions/xiaomi/xiaomi.live.test.ts:20` : le test en direct Xiaomi couvre le TTS du fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/video-generation-providers.live.test.ts:97` : les cas vidéo-génération en direct partagés incluent Alibaba, BytePlus, MiniMax, Qwen et les fournisseurs hébergés connexes.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/qwen/video-generation-provider.test.ts` : couverture unitaire pour le comportement du fournisseur vidéo-génération Qwen.
- `/Users/kevinlin/code/openclaw/extensions/zai/index.test.ts` : couverture unitaire pour le comportement du fournisseur ZAI.
- `/Users/kevinlin/code/openclaw/extensions/moonshot/index.test.ts` : couverture unitaire pour le comportement du fournisseur Moonshot.
- `/Users/kevinlin/code/openclaw/extensions/minimax/speech-provider.test.ts` : couverture unitaire pour le comportement du fournisseur de parole MiniMax.
- `/Users/kevinlin/code/openclaw/extensions/byteplus/index.test.ts` : couverture unitaire pour le comportement du fournisseur BytePlus.
- `/Users/kevinlin/code/openclaw/extensions/volcengine/tts.test.ts` : couverture unitaire pour le comportement TTS de Volcengine.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "Qwen ZAI Moonshot MiniMax provider"` a retourné `[]`.
- `gitcrawl --json search prs -R openclaw/openclaw "Qwen ZAI Moonshot MiniMax provider"` a retourné `[]`.
- `gitcrawl --json search prs -R openclaw/openclaw "provider metadata model catalog"` a retourné des PR de métadonnées/catalogue de fournisseur adjacentes, incluant les changements de métadonnées de modèle Qwen et de fournisseur tels que #69729 et #43493.

### Requêtes Discrawl

- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "Qwen ZAI Moonshot MiniMax provider" --limit 5` a retourné un rapport de problème Discord voix/STT où les clés du registre des fournisseurs incluaient Deepgram, Groq, MiniMax, Mistral, Moonshot, OpenRouter, Qwen et ZAI, et l'utilisateur a rencontré un problème de paramètre de modèle OpenAI STT.
- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "provider auth setup env vars" --limit 5` a retourné un commentaire d'examen où `QWEN_API_KEY` et `MOONSHOT_API_KEY` pourraient affecter la sélection automatique du fournisseur d'outil d'image.
