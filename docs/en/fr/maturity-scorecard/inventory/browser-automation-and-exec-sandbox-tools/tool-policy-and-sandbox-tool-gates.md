---
title: "Automatisation des navigateurs et outils exec/sandbox - Note de maturité sur la politique des outils et les portes des outils sandbox"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation des navigateurs et outils exec/sandbox - Note de maturité sur la politique des outils et les portes des outils sandbox

## Résumé

La politique des outils et les portes des outils sandbox sont stables. La documentation et le code source définissent un pipeline de politique en couches : profils, politique du fournisseur, politique globale/agent, politique de groupe et d'expéditeur, politique des outils sandbox, politique des sous-agents et politique héritée. Le principal risque de qualité n'est pas une implémentation manquante ; c'est la complexité de la politique et la mauvaise compréhension des opérateurs, en particulier pour les outils plugin/MCP à l'intérieur des tours en sandbox et pour l'exécution shell restant mutante même lorsque les outils de fichiers sont refusés.

## Portée de la catégorie

Cette note couvre les profils d'outils, les groupes d'outils, la politique d'autorisation/refus, la politique du fournisseur, la politique de l'expéditeur, la politique de groupe/canal, la politique des outils sandbox, les entrées de porte sandbox plugin/MCP, la projection d'outils effective, les outils hérités des sous-agents, les conseils sur les outils bloqués sandbox, et les diagnostics `tools.effective`/`sandbox explain`.

## Fonctionnalités

- Politique des outils : couvre la politique des outils sur les profils d'outils, les groupes d'outils, la politique d'autorisation/refus, la politique du fournisseur, et le comportement associé de la politique des outils et des portes des outils sandbox.
- Portes des outils sandbox : couvre les portes des outils sandbox sur les profils d'outils, les groupes d'outils, la politique d'autorisation/refus, la politique du fournisseur, et le comportement associé de la politique des outils et des portes des outils sandbox.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (86%)`
- Signaux positifs :
  - La documentation décrit clairement les profils d'outils, les groupes, la politique du fournisseur, la politique de l'expéditeur, la politique des outils sandbox, les portes sandbox MCP/plugin, et la précédence.
  - Le code source normalise les entrées de politique, développe les groupes core/plugin, analyse les entrées de liste blanche inconnues, gère `alsoAllow`, et applique la politique d'outils effective finale aux outils plugin/bundled.
  - Les tests couvrent la fusion de la politique des outils sandbox, la précédence du refus, les conseils bloqués, l'alignement du résolveur sandbox effective, et la politique d'invocation d'outils HTTP/RPC directs.
  - La documentation de sécurité avertit que la politique des outils contrôle les outils appelables, pas les effets secondaires arbitraires à l'intérieur d'un shell autorisé.
- Signaux négatifs :
  - Les rapports d'archive montrent que les outils MCP/plugin disparaissent des sessions en sandbox et que les opérateurs confondent la politique des outils avec le runtime du plugin ou l'isolation du shell.
  - Les entrées de liste blanche d'outils inconnues peuvent rendre la configuration plus sûre qu'elle ne l'est réellement.
- Lacunes d'intégration :
  - Ajouter une matrice de visibilité des outils MCP/plugin en sandbox de bout en bout pour `bundle-mcp`, l'id du plugin, `group:plugins`, l'outil serveur exact, et les entrées glob du serveur.
  - Ajouter un inspecteur de politique orienté utilisateur qui explique l'étape de politique exacte qui a supprimé chaque outil important.

## Score de qualité

- Score : `Stable (83%)`
- Rapports Gitcrawl :
  - `tools sandbox tool policy` a retourné la PR #86715 pour ajouter `message` à la politique sandbox par défaut, le problème #75124 pour les commandes slash de compétence contournant la politique d'outils effective, la PR #60981 pour le contrôle d'accès au système de fichiers PathGuard, le problème #85030 pour les outils MCP non injectés dans les sessions des sous-agents, et le problème #44484 sur les outils déclarés ne correspondant pas aux outils de session effective.
- Rapports Discrawl :
  - `tool policy sandbox tools` a retourné les conseils du 2026-04-28 recommandant la politique sandbox/outils pour l'isolation stricte et expliquant que les espaces de travail ne sont pas un sandbox strict par eux-mêmes.
  - La même requête a retourné les conseils de support companion/Joi expliquant que refuser `exec` supprime l'exec/processus appelable par le modèle mais n'arrête pas le code plugin/service de confiance de faire des appels shell en interne.
- Bonnes qualités :
  - Les couches de politique sont ordonnées et documentées.
  - Le refus gagne et les listes blanches restrictives échouent bruyamment quand aucun outil appelable ne reste.
  - Les outils appartenant aux plugins ont une logique d'expansion de groupe/plugin explicite.
  - La politique d'outils effective utilise le contexte de groupe dérivé de session de confiance au lieu des champs model/tool-call non fiables.
  - Les messages d'outils bloqués sandbox incluent des clés de correction et un formatage sûr pour le shell.
- Mauvaises qualités :
  - Les opérateurs doivent comprendre plusieurs couches de politique et leur précédence.
  - La porte plugin/MCP sandbox est une couche supplémentaire qui peut masquer les outils même après le chargement réussi du serveur/plugin.
  - Autoriser `exec` signifie que le modèle a toujours un shell ; refuser `write` ou `apply_patch` ne rend pas ce shell en lecture seule.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, live et runtime-flow n'ont affecté que la couverture.

## Score de complétude

- Score : `Stable (86%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la politique des outils et les portes des outils sandbox.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'inspecteur de politique devrait rendre les outils MCP/plugin manquants plus faciles à déboguer.
- Le comportement de la politique d'outils des sous-agents et hérités a besoin d'une meilleure visibilité orientée utilisateur directe.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:15` : les profils d'outils sont documentés.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:30` : les groupes d'outils sont documentés, y compris runtime, fs, sessions, memory, web, ui, automation, messaging, nodes, agents, media, openclaw, et plugins.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:48` : les outils MCP et plugin à l'intérieur de la politique sandbox nécessitent une porte sandbox supplémentaire.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:79` : la politique d'autorisation/refus globale est documentée et le refus gagne.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:97` : l'ordre de la politique spécifique au fournisseur est documenté.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:113` : toolsBySender est documenté comme défense en profondeur.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md:52` : la documentation distingue la politique des outils, la politique du fournisseur, la politique globale/agent, et la politique des outils sandbox.
- `/Users/kevinlin/code/openclaw/docs/tools/multi-agent-sandbox-tools.md:197` : la documentation énumère l'ordre de filtrage à travers la politique des outils sandbox et des sous-agents.
- `/Users/kevinlin/code/openclaw/docs/tools/multi-agent-sandbox-tools.md:309` : la documentation avertit que l'exécution du shell peut toujours écrire même lorsque les outils du système de fichiers sont désactivés.

### Code source

- `/Users/kevinlin/code/openclaw/src/agents/tool-policy.ts:63` : les listes blanches explicites sont collectées sur les couches de politique.
- `/Users/kevinlin/code/openclaw/src/agents/tool-policy.ts:107` : les groupes d'outils plugin sont construits à partir des métadonnées du plugin.
- `/Users/kevinlin/code/openclaw/src/agents/tool-policy.ts:131` : les entrées de groupe plugin se développent en outils appartenant au plugin.
- `/Users/kevinlin/code/openclaw/src/agents/tool-policy.ts:172` : l'analyse de la liste blanche détecte les entrées inconnues et plugin uniquement.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox-tool-policy.ts:31` : la politique des outils sandbox choisit les entrées allow, alsoAllow, et deny.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/effective-tool-policy.ts:23` : les entrées d'identité de groupe sont documentées comme des signaux d'autorisation qui doivent être dérivés du serveur.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/effective-tool-policy.ts:151` : le pipeline de politique final inclut la politique par défaut, les outils sandbox, les outils des sous-agents, et les outils hérités.
- `/Users/kevinlin/code/openclaw/src/gateway/tool-resolution.ts:177` : les outils à portée Gateway appliquent le pipeline de politique avant l'exposition.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/tools-invoke-http.test.ts:440` : les tests de type intégration d'invocation d'outils HTTP exercent le filtrage de politique.
- `/Users/kevinlin/code/openclaw/src/agents/openclaw-tools.browser-plugin.integration.test.ts:1` : la couverture d'intégration existe pour l'exposition des outils built-in/plugin.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/sandbox-tool-policy.test.ts:10` : vérifie le comportement de la politique des outils sandbox.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox-tool-policy.test.ts:11` : vérifie que sandbox `alsoAllow` fusionne dans la liste blanche sandbox par défaut.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox-tool-policy.test.ts:197` : vérifie la précédence du refus sandbox sur allow et alsoAllow.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox-tool-policy.test.ts:238` : vérifie que les conseils d'outils bloqués utilisent la politique sandbox effective.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox-tool-policy.test.ts:270` : vérifie que les conseils d'outils bloqués sont conscients des glob et sûrs pour le shell.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.buildembeddedsandboxinfo.test.ts:1` : les tests d'informations sandbox intégrées existent.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "tools sandbox tool policy" --json`

Résultats :

- PR ouverte #86715 : ajouter `message` à `DEFAULT_TOOL_ALLOW` dans la politique sandbox.
- Problème ouvert #75124 : les commandes slash de compétence contournent la politique d'outils effective.
- PR ouverte #60981 : contrôle d'accès au système de fichiers PathGuard.
- Problème ouvert #85030 : les outils MCP ne sont pas injectés dans les sessions des sous-agents.
- Problème ouvert #44484 : les outils déclarés ne correspondent pas aux outils de session effective.

### Requêtes Discrawl

Requête :

`discrawl search --mode fts --limit 5 "tool policy sandbox tools"`

Résultats :

- Conseils d'archive du 2026-04-28 recommandant la politique sandbox/outils pour l'isolation stricte, avec les espaces de travail et les magasins d'authentification traités séparément.
- Conseils d'archive du 2026-04-27 expliquant que refuser `exec` supprime l'exec/processus appelable par le modèle mais ne désactive pas le code plugin, hook ou service de confiance.
