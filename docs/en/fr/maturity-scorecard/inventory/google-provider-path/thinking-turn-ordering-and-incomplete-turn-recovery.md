---
title: "Chemin du fournisseur Google - Note de maturité de la récupération des tours et de la réflexion"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Google - Note de maturité de la récupération des tours et de la réflexion

## Résumé

La réflexion Gemini, l'ordre des tours, la relecture de la signature de pensée et la récupération des tours incomplets sont implémentés avec des garde-fous forts spécifiques au fournisseur. La couverture est Stable car les preuves de source et de flux d'exécution couvrent les principaux chemins de relecture et de récupération. La qualité est Stable à la limite partagée car la source est robuste et délimitée par le fournisseur, mais les archives montrent toujours une pression active autour des signatures de pensée, du formatage des réponses de fonction et des tours Gemini incomplets.

## Portée de la catégorie

Cette catégorie couvre le mappage au niveau de la réflexion Gemini, la forme de demande de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google, la réparation des tours en premier assistant, la validation des tours Gemini et la relecture/récupération pour les tours Gemini vides, uniquement de raisonnement et uniquement de planification. Elle exclut les fonctionnalités non-Gemini de médias/TTS/recherche sauf si elles prouvent l'enregistrement du fournisseur ou l'exécution Google en direct.

## Fonctionnalités

- Mappage au niveau de la réflexion : Couvre le mappage au niveau de la réflexion sur le mappage au niveau de la réflexion Gemini, la forme de demande de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google et le comportement de réflexion et de récupération des tours associé.
- Relecture de la signature de pensée : Couvre la relecture de la signature de pensée sur le mappage au niveau de la réflexion Gemini, la forme de demande de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google et le comportement de réflexion et de récupération des tours associé.
- Ordre des tours d'outil : Couvre l'ordre des tours d'outil sur le mappage au niveau de la réflexion Gemini, la forme de demande de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google et le comportement de réflexion et de récupération des tours associé.
- Récupération des tours incomplets : Couvre la récupération des tours incomplets sur le mappage au niveau de la réflexion Gemini, la forme de demande de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google et le comportement de réflexion et de récupération des tours associé.
- Récupération des tours uniquement de planification : Couvre la récupération des tours uniquement de planification sur le mappage au niveau de la réflexion Gemini, la forme de demande de réflexion adaptative, la capture/relecture/assainissement de `thoughtSignature`, la politique de relecture Google et le comportement de réflexion et de récupération des tours associé.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : Les crochets de relecture appartenant au fournisseur, la réparation de l'ordre des tours, l'assainissement de la signature de pensée, la validation des tours Gemini et les portes de relecture des tours incomplets sont tous présents dans la source ; les tests de flux d'exécution couvrent la récupération sûre pour la relecture et le basculement Google en direct existe.
- Signaux négatifs : Aucun test en direct toujours actif n'a été trouvé pour la relecture directe de la signature de pensée Gemini multi-tours ou la récupération spécifique à Gemini par rapport à l'API réelle.
- Lacunes d'intégration : Certains scénarios d'assurance qualité utilisent des flux d'exécution du fournisseur fictif plutôt que des appels Gemini en direct.

## Score de qualité

- Score : `Stable (80%)`
- Rapports Gitcrawl : #84384 et #69220 couvrent les signatures de pensée Gemini/réflexion et le comportement vide après outil ; #49783 couvrait la compatibilité des réponses de fonction Gemini ; #73153, #85422 et #63188 se regroupaient autour du comportement de relecture des réponses incomplètes/uniquement de raisonnement/vides.
- Rapports Discrawl : Les recherches pour `Gemini thought signature`, `Gemini incomplete turn`, `functionResponse` et `Gemini turn ordering` ont trouvé des fils de discussion avec signature manquante, PR #71362, des échecs de format de réponse de fonction et des journaux de réparation de l'ordre des tours.
- Bonnes qualités : Le code du fournisseur délimite la relecture aux modèles Google de même route, filtre les signatures non sûres, valide les tours Gemini avant la validation Anthropic générique et rend la récupération Gemini explicite au lieu de générique.
- Mauvaises qualités : Les signatures opaques du fournisseur et la sémantique des tours incomplets sont toujours un comportement à fort taux de changement dans les archives, donc l'implémentation a besoin d'une validation récurrente.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-provider-path.md`.
- Signaux positifs : les preuves des docs archivées, de la source, des tests, de Gitcrawl et de Discrawl couvrent la portée de la taxonomie pour le mappage au niveau de la réflexion, la relecture de la signature de pensée, l'ordre des tours d'outil, la récupération des tours incomplets, la récupération des tours uniquement de planification.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve Gemini en direct pour la relecture multi-tours de `thoughtSignature` n'a pas été trouvée comme une porte toujours active.
- Les docs mentionnent les échecs de réflexion et de signature Google mais n'expliquent pas complètement la réparation de l'ordre des tours ou les diagnostics directs de relecture Gemini.
- La récupération des tours incomplets a des garde-fous de source forts, mais la preuve en direct est toujours plus mince que la couverture d'exécution fictive.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/google.md:139` répertorie le support de la réflexion/raisonnement Google.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:178` documente le mappage au niveau de la réflexion Gemini 3.
- `/Users/kevinlin/code/openclaw/docs/help/faq-models.md:459` documente l'échec requis de la signature de pensée et la récupération de l'opérateur.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:355` documente les commandes de fumée en direct axées sur Google et les distinctions de route.

### Source

- `/Users/kevinlin/code/openclaw/extensions/google/provider-hooks.ts:10` câble les crochets de la famille de relecture Gemini Google.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/provider-model-shared.ts:217` fournit la politique de relecture Google et le mode de raisonnement balisé.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-replay-helpers.ts:174` définit l'assainissement de relecture Google, les identifiants d'appel d'outil stricts, le filtrage de signature, la correction de l'ordre en premier assistant et les résultats d'outil synthétiques.
- `/Users/kevinlin/code/openclaw/src/shared/google-turn-ordering.ts:5` ajoute un amorçage utilisateur quand l'historique de relecture commence par un tour assistant.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-helpers/turns.ts:339` valide les séquences de tours Gemini.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/replay-history.ts:879` applique la validation Gemini avant la validation Anthropic.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run/incomplete-turn.ts:129` active la récupération des tours incomplets pour les modèles Gemini sur les fournisseurs Google.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run/incomplete-turn.ts:596` définit les portes de relecture uniquement de raisonnement et de réponse vide.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:98` inclut les clés de modèle Gemini en direct.
- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:2541` force une lecture de passerelle réelle et un appel d'outil d'écho nonce.
- `/Users/kevinlin/code/openclaw/src/agents/google-gemini-switch.live.test.ts:12` teste en direct le basculement de l'historique d'appel d'outil Antigravity non signé vers les modèles Gemini directs.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/empty-response-recovery-replay-safe-read.md:12` couvre la récupération de réponse vide d'exécution avec des lectures sûres pour la relecture.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/reasoning-only-recovery-replay-safe-read.md:12` couvre la récupération uniquement de raisonnement d'exécution avec des lectures sûres pour la relecture.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.test.ts:966` couvre la relecture de signature de pensée du même modèle.
- `/Users/kevinlin/code/openclaw/extensions/google/transport-stream.test.ts:1234` couvre le rejet de signature entre fournisseurs.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-helpers.validate-turns.test.ts:74` couvre `validateGeminiTurns`.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run.incomplete-turn.test.ts:1536` couvre la relecture Gemini uniquement de raisonnement.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run.incomplete-turn.test.ts:2551` couvre les tours Gemini vides.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner/run.incomplete-turn.test.ts:2642` couvre la porte de récupération uniquement de planification Gemini.
- `/Users/kevinlin/code/openclaw/src/agents/openai-transport-stream.test.ts:5636` couvre le aller-retour de signature de pensée Gemini sur les complétions compatibles OpenAI.

### Requêtes Gitcrawl

Requête : `gitcrawl search issues "thoughtSignature" -R openclaw/openclaw --state all`

Résultats :

- Retourné les #84384 et #69220 ouverts autour des signatures de pensée Gemini/réflexion et du comportement vide après outil.

Requête : `gitcrawl search issues "functionResponse" -R openclaw/openclaw --state all`

Résultats :

- Retourné #49783 fermé sur la compatibilité appel de fonction/réponse de fonction Gemini.

Requête : `gitcrawl search issues "Gemini incomplete turn reasoning-only empty response" -R openclaw/openclaw --state all`

Résultats :

- Retourné #73153, #85422 et #63188 autour du comportement de relecture incomplet, uniquement de raisonnement et de réponse vide.

### Requêtes Discrawl

Requête : `discrawl search --mode fts "Gemini thought signature"`

Résultats :

- Trouvé les fils de discussion des mainteneurs/utilisateurs d'avril et mai pour les signatures manquantes, PR #79827, PR #84855 et problème #71725.

Requête : `discrawl search --mode fts "Gemini incomplete turn"`

Résultats :

- Trouvé #69220, #71126, PR #71362, fermeture #71074 et références de commit pour la récupération des tours incomplets Gemini.

Requête : `discrawl search --mode fts "Gemini turn ordering"`

Résultats :

- Trouvé les journaux utilisateur montrant `google turn ordering fixup: prepended user bootstrap` et #27862 liant les signatures de pensée manquantes aux conflits d'ordre.
