---
title: "Session, memory, and context engine - Core Prompts and Context Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Session, memory, and context engine - Core Prompts and Context Maturity Note

## Résumé

Le comportement de visibilité des instructions et du contexte est documenté dans les docs de contexte, les docs d'agent, les docs de canal et l'hygiène des transcriptions. La source dispose de filtres de visibilité explicites, d'assistants de prompt d'amorçage, de contexte de compétences groupées et de désinfectants orientés utilisateur pour le contexte d'exécution divulgué. La couverture est plus mince que le stockage de session principal car une grande partie du comportement est exercée par des tests unitaires et des tests de canal plutôt que par des scénarios complets multi-clients.

## Portée de la catégorie

Cette catégorie couvre `AGENTS.md`, `USER.md`, `IDENTITY.md`, `SOUL.md`, l'injection de contexte de projet, la troncature d'amorçage, le contexte supplémentaire non fiable, la configuration de visibilité du contexte et la prévention des fuites de contexte d'exécution.

## Fonctionnalités

- Profil d'instruction : Couvre le profil d'instruction dans `AGENTS.md`, `USER.md`, `IDENTITY.md`, `SOUL.md`, l'injection de contexte de projet, la troncature d'amorçage, le contexte supplémentaire non fiable, la configuration de visibilité du contexte et la prévention des fuites de contexte d'exécution.
- Visibilité du contexte : Couvre la visibilité du contexte dans `AGENTS.md`, `USER.md`, `IDENTITY.md`, `SOUL.md`, l'injection de contexte de projet, la troncature d'amorçage, le contexte supplémentaire non fiable, la configuration de visibilité du contexte et la prévention des fuites de contexte d'exécution.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (68%)`
- Signaux positifs : les docs expliquent les fichiers injectés et la visibilité ; la source filtre le contexte supplémentaire et supprime les fuites de contexte d'exécution ; les tests couvrent les modes de visibilité et le comportement du désinfectant.
- Signaux négatifs : moins de tests de flux de session complets prouvent l'injection de fichiers de profil, la troncature, le contexte supplémentaire du canal et la rédaction de l'historique ensemble.
- Lacunes d'intégration : ajouter un scénario multi-canal qui injecte des fichiers de profil, du contexte cité, des métadonnées de thread et du contexte généré à l'exécution, puis vérifie le prompt du modèle, la transcription, l'historique WebChat et la sortie de réponse du canal.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : la requête de visibilité exacte n'a retourné aucun résultat ; une requête d'amorçage plus large a retourné l'ouverture `#63216` concernant les boucles de réessai de réinitialisation réinjectant le contexte d'amorçage.
- Rapports Discrawl : les requêtes de visibilité exactes n'ont retourné aucune ligne.
- Bonnes qualités : les docs distinguent clairement la mémoire du contexte, les fichiers injectés des schémas d'outils et le contexte d'exécution du contenu de transcription visible.
- Mauvaises qualités : la troncature d'amorçage et le contexte supplémentaire du canal restent assez subtils pour causer une confusion chez l'opérateur.
- Exclus de la qualité : profondeur des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Alpha (68%)`
- Instructions de surface : évaluées par rapport à `references/completeness/session-memory-and-context-engine.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le profil d'instruction et la visibilité du contexte.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les opérateurs ont toujours besoin d'un moyen plus clair de prouver quels fichiers de profil/contexte ont atteint une exécution spécifique sur tous les clients.
- Les limites du contexte supplémentaire sont explicites dans les docs, mais pas une limite de rédaction complète pour chaque canal.

## Preuves

### Docs

- `docs/concepts/context.md:100` décrit la construction du prompt système ; `docs/concepts/context.md:113` énumère les fichiers d'espace de travail injectés ; `docs/concepts/context.md:125` documente les plafonds de troncature d'amorçage.
- `docs/reference/transcript-hygiene.md:32` indique que le contexte d'exécution/système n'est pas la transcription utilisateur.
- `docs/channels/discord.md:285` explique le comportement de `MEMORY.md`, `AGENTS.md` et `USER.md` pour les canaux de guilde ; `docs/channels/discord.md:756` marque les sujets des canaux comme contexte non fiable.

### Source

- `src/security/context-visibility.ts:16` évalue la visibilité du contexte supplémentaire.
- `src/config/context-visibility.ts:25` résout le mode de visibilité du contexte par canal.
- `src/agents/bootstrap-prompt.ts:1` construit les conseils d'amorçage complets et `src/agents/bootstrap-prompt.ts:15` construit les conseils limités.
- `src/agents/embedded-agent-helpers/sanitize-user-facing-text.ts:403` désinfecte le texte orienté utilisateur et supprime le contexte d'exécution interne.

### Tests d'intégration

- `src/gateway/openai-http.test.ts:130` vérifie le routage du contexte historique/actuel pour les requêtes compatibles OpenAI.
- `src/agents/embedded-agent-runner/run/attempt.spawn-workspace.context-injection.test.ts` couvre l'injection de contexte de l'espace de travail de génération.
- `src/gateway/sessions-history-http.test.ts:512` désinfecte les entrées d'historique d'assistant par phases avant de les retourner.

### Tests unitaires

- `src/security/context-visibility.test.ts:37` conserve tout le contexte en tous les modes et `src/security/context-visibility.test.ts:47` applique le mode liste blanche.
- `src/config/context-visibility.test.ts:33` teste le repli compte/canal/défaut.
- `src/agents/embedded-agent-helpers.sanitizeuserfacingtext.test.ts:552` supprime les préfaces de contexte d'exécution copiées.

### Requêtes Gitcrawl

Requête :

`gitcrawl search issues "AGENTS.md USER.md context visibility transcript hygiene" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- Retourné `[]`.

Requête :

`gitcrawl search issues "context visibility AGENTS.md bootstrapMaxChars USER.md" -R openclaw/openclaw --state all --json number,title,url,state`

Résultats :

- Retourné l'ouverture `#63216 Repeated hard resets on same session key despite high reserveTokensFloor; retry loop re-injects bootstrap context`.

### Requêtes Discrawl

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "AGENTS.md USER.md context visibility transcript hygiene"`

Résultats :

- Aucune ligne correspondante retournée.

Requête :

`DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "context visibility AGENTS.md bootstrapMaxChars USER.md"`

Résultats :

- Aucune ligne correspondante retournée.
