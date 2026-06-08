---
title: "Chemin du fournisseur Anthropic - Note de maturité de la sélection du modèle et du runtime"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Anthropic - Note de maturité de la sélection du modèle et du runtime

## Résumé

La couverture du catalogue de modèles Anthropic est Stable. Le manifeste fourni publie les lignes de modèles Anthropic directs et Claude CLI, le remplissage source des variantes Claude 4.x actuelles, normalise les métadonnées d'image et de contexte 1M, et mappe l'authentification Claude CLI sélectionnée à la politique de runtime à portée de modèle. La qualité est Beta car les utilisateurs rencontrent toujours une confusion entre la liste d'autorisation et le catalogue des modèles, et la dénomination/métadonnées actuelles du modèle Claude nécessitent une maintenance fréquente de la compatibilité prospective.

## Portée de la catégorie

Inclus dans cette catégorie :

- Catalogue Claude fourni : Couvre le catalogue Claude fourni dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Références anthropic canoniques : Couvre les références anthropic canoniques dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Compatibilité Claude CLI : Couvre la compatibilité Claude CLI dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Disponibilité du sélecteur de modèles : Couvre la disponibilité du sélecteur de modèles dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Métadonnées de capacité : Couvre les métadonnées de capacité dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Sélection du runtime : Couvre la sélection du runtime dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Continuité de session : Couvre la continuité de session dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Pont MCP/outils : Couvre le pont MCP/outils dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Mappage des modes de permission : Couvre le mappage des modes de permission dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Prélude de secours : Couvre le prélude de secours dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.

## Fonctionnalités

- Catalogue Claude fourni : Couvre le catalogue Claude fourni dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Références anthropic canoniques : Couvre les références anthropic canoniques dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Compatibilité Claude CLI : Couvre la compatibilité Claude CLI dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Disponibilité du sélecteur de modèles : Couvre la disponibilité du sélecteur de modèles dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Métadonnées de capacité : Couvre les métadonnées de capacité dans le catalogue de modèles Anthropic et la couche de politique : lignes de modèles fournis, alias de modèles, normalisation actuelle et future des identifiants de modèles Claude, sélection du runtime-fournisseur, et comportement associé du catalogue de modèles et de la politique.
- Sélection du runtime : Couvre la sélection du runtime dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Continuité de session : Couvre la continuité de session dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Pont MCP/outils : Couvre le pont MCP/outils dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Mappage des modes de permission : Couvre le mappage des modes de permission dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.
- Prélude de secours : Couvre le prélude de secours dans le chemin Claude CLI local à l'hôte d'OpenClaw après que l'authentification soit disponible : le backend `claude-cli`, ses valeurs par défaut de commande/args/env, le pont d'outils MCP, le mode d'outils natif, et le comportement associé du backend claude cli.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : Le manifeste fourni inclut les modèles Anthropic directs et Claude CLI ; la documentation décrit les références canoniques et la politique de runtime ; la source a une résolution de modèle compatible prospective, une normalisation de contexte 1M, une normalisation de capacité d'image, et une migration d'alias ; les tests épinglent le comportement clé des métadonnées de modèle.
- Signaux négatifs : Le catalogue reste statique/léger en découverte pour Anthropic direct et s'appuie sur la compatibilité prospective maintenue par la source pour les nouveaux identifiants Claude.
- Lacunes d'intégration : La preuve de version pour la dérive du catalogue en amont frais est plus faible que la preuve source/test unitaire.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : La PR #75157 traite les noms d'affichage du catalogue pour les modèles d'agent ; la PR #72404 définit par défaut les modèles capables de vision explicites uniquement comme capables d'image ; la PR #80394 ajoute des listes d'autorisation de modèles par agent ; la PR #67731 épingle la résolution de variante Opus 4.7 et la couverture de régression par défaut de réflexion.
- Rapports Discrawl : L'archive Discord inclut `claude-cli models not in catalog` et les fils de support "only Sonnet available" liés à la configuration de la liste d'autorisation/catalogue et à la confusion de refroidissement.
- Bonnes qualités : Les références canoniques, la gestion des alias, le secours dynamique de modèle, les métadonnées de contexte 1M, la normalisation d'entrée d'image, et le remplissage de runtime Claude CLI sélectionné sont centralisés dans le fournisseur fourni.
- Mauvaises qualités : Les opérateurs peuvent toujours confondre l'état d'authentification/profil, les listes d'autorisation de modèles configurées, les lignes du catalogue du fournisseur, et la sélection du runtime lorsqu'un modèle Claude souhaité n'apparaît pas ou n'est pas disponible.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct, et de flux de runtime réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/anthropic-provider-path.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour le catalogue Claude fourni, les références anthropic canoniques, la compatibilité Claude CLI, la disponibilité du sélecteur de modèles, les métadonnées de capacité, la sélection du runtime, la continuité de session, le pont MCP/outils, le mappage des modes de permission, le prélude de secours.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connus utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les nouveaux identifiants de modèles Claude et les variantes datées nécessitent une maintenance continue de la compatibilité prospective.
- La documentation et les conseils de configuration ont migré des références `claude-cli/*` vers les références canoniques `anthropic/*` plus la politique de runtime, tandis que les configurations héritées existent toujours.
- L'UX de disponibilité des modèles peut toujours faire ressembler les problèmes de catalogue, de liste d'autorisation, de refroidissement et d'authentification.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` documente les références `anthropic/*`, le remplacement du runtime Claude CLI, les paramètres par défaut de la réflexion Claude 4.6, la mise en cache des invites, le support des médias et le comportement du contexte de 1M.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-agents.md` documente la précédence de la politique runtime et recommande le `anthropic/claude-opus-4-7` canonique plus `agentRuntime.id: "claude-cli"`.
- `/Users/kevinlin/code/openclaw/docs/concepts/models.md` documente la sélection des références fournisseur/modèle et le comportement de secours utilisé par les lignes Anthropic.

## Source

- `/Users/kevinlin/code/openclaw/extensions/anthropic/openclaw.plugin.json` publie les lignes du catalogue de modèles statiques pour `claude-cli` et `anthropic`, y compris Opus 4.7, Sonnet 4.6, Opus 4.6, les drapeaux de raisonnement, les métadonnées d'entrée d'image, les fenêtres de contexte, les jetons max, les points de terminaison du fournisseur, la normalisation des alias et la famille de requêtes du fournisseur.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/register.runtime.ts` résout les identifiants de modèle Claude modernes, applique les fenêtres de contexte GA 1M, normalise l'entrée de médias image, publie les entrées du catalogue Claude CLI et expose les profils de réflexion.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/claude-model-refs.ts` canonicalise les alias de la famille Claude, met à niveau les anciennes références Claude 3/4 et mappe les anciennes références `claude-cli/*` aux références Anthropic canoniques.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/config-defaults.ts` collecte les références runtime Claude CLI et remplit `agentRuntime.id: "claude-cli"` lorsque l'authentification Claude CLI ou la sélection de modèle est active.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre les lignes du catalogue du fournisseur et le comportement de la liste des modèles.
- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` vérifie les entrées de profil de modèle Anthropic en direct telles que `OPENCLAW_LIVE_GATEWAY_MODELS=anthropic/claude-opus-4-7` et les listes de modèles Sonnet/Haiku.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/anthropic/index.test.ts` couvre la valeur par défaut de l'API de modèle, le remplissage de la liste d'autorisation Claude CLI, les références abrégées, les futures références Anthropic, la résolution d'Opus 4.7 à partir de modèles, les métadonnées de médias image, la normalisation du contexte 1M et l'authentification synthétique.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/provider-policy-api.test.ts` couvre la normalisation de la politique du fournisseur public et l'exposition du profil de réflexion.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/cli-migration.test.ts` couvre le comportement de migration à partir de l'authentification Claude CLI.
- `/Users/kevinlin/code/openclaw/src/agents/model-catalog-lookup.ts` et les tests adjacents couvrent la recherche du catalogue de modèles utilisée par la sélection du runtime de l'agent.

## Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic model catalog claude opus sonnet haiku models list"`

Résultats :

- Aucun résultat direct retourné pour cette requête de problème exacte.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "Anthropic model catalog Claude Opus 4.7 Sonnet 4.6"`

Résultats :

- #75157 `fix(ui): use catalog display names for agent models`.
- #72404 `fix(models): default input=[text,image] for vision-capable explicit-only models`.
- #80394 `feat(agents): per-agent model allowlist (with fallback to global)`.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "Anthropic thinking"`

Résultats :

- #67731 `test(anthropic): pin Opus 4.7 variant resolution + thinking-default regression coverage`.
- #70584 `fix: clamp effort=low/minimal to medium for claude-opus-4.7`.

## Requêtes Discrawl

Requête : `discrawl search --limit 10 "Anthropic model catalog claude opus sonnet OpenClaw"`

Résultats :

- Threads de support retournés pour `claude-cli models not in catalog`, configuration des listes d'autorisation de modèles Opus/Sonnet et utilisateurs confondant le délai de limitation de débit avec les modifications du catalogue.

Requête : `discrawl search --limit 10 "Claude CLI OpenClaw auth login claude-cli"`

Résultats :

- Notes de délégation Claude CLI implémentées retournées et threads de support utilisateur où la politique de modèle/runtime différait entre les chemins de session.
