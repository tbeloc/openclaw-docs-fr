---
title: "Chemin du fournisseur OpenAI / Codex - Note de maturité des diagnostics du docteur et de la réparation de l'opérateur"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur OpenAI / Codex - Note de maturité des diagnostics du docteur et de la réparation de l'opérateur

## Résumé

Les diagnostics et la réparation sont fortement représentés dans la documentation et le code source, mais ils constituent également la principale faiblesse visible du chemin du fournisseur OpenAI/Codex. `openclaw doctor --fix`, `/status`, `models status`, `models auth list`, les sondes de fournisseur, la réparation du sidecar OAuth, le nettoyage des épingles de route/session obsolètes et la protection des métadonnées du profil d'authentification existent tous. La couverture est Beta car les flux de réparation ont des tests et une documentation réels mais s'étendent sur de nombreux magasins de configuration/session. La qualité est Alpha car les preuves récentes de GitHub et Discord montrent que doctor/status peut toujours laisser les utilisateurs avec des incompatibilités fournisseur/runtime ou un état OAuth partiellement réparé.

## Portée de la catégorie

Cette catégorie couvre la réparation et le diagnostic orientés vers l'opérateur pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles de runtime, sidecars de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.

## Fonctionnalités

- Diagnostics du docteur : couvre les diagnostics du docteur pour la réparation et le diagnostic orientés vers l'opérateur pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles de runtime, sidecars de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.
- Réparation de l'opérateur : couvre la réparation de l'opérateur pour la réparation et le diagnostic orientés vers l'opérateur pour les problèmes du chemin du fournisseur OpenAI/Codex : migration de route obsolète, épingles de session persistantes, épingles de runtime, sidecars de profil d'authentification, métadonnées de profil, sortie de statut/sonde et commandes de récupération.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : la documentation de réparation nomme les commandes exactes ; la source du docteur analyse la configuration, les modèles, les sessions, les profils d'authentification, les sidecars obsolètes et la politique de runtime ; les tests couvrent des cas de réparation spécifiques.
- Signaux négatifs : la réparation s'étend sur les fichiers de configuration, les magasins de session, les magasins d'authentification, l'état d'installation du plugin et l'état externe du serveur d'application Codex/compte.
- Lacunes d'intégration : il n'existe aucune preuve de version unique qui exerce les références `openai-codex/*` obsolètes, les épingles de runtime obsolètes, les ombres OAuth du sidecar et la réparation du plugin du serveur d'application Codex dans un scénario de mise à niveau.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : les problèmes ouverts #87436, #80628, #87650, #84252 et #84038 montrent que le comportement de réparation doctor/status/update est toujours un risque actif.
- Rapports Discrawl : la discussion du 2026-05-17 indique que la sélection directe des réponses OpenAI pour `openai/gpt-5.5` devrait déclencher des vérifications des épingles de session, des épingles de profil d'authentification et de la réparation planifiée du docteur ; les notes du 2026-05-09 indiquent que le docteur a corrigé les épingles de runtime d'agent entier obsolètes mais pas une défaillance de route OAuth restante.
- Bonnes qualités : la réparation est explicite, détenue par la source et principalement en échec fermé ; la documentation donne des commandes concrètes pour vérifier le modèle, le runtime, la route d'authentification et la configuration obsolète.
- Mauvaises qualités : la sortie de réparation actuelle peut toujours nécessiter une interprétation du responsable sur plusieurs magasins d'état.
- Exclu de la qualité : la couverture des tests du docteur et du statut a été utilisée uniquement pour la couverture.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les diagnostics du docteur et la réparation de l'opérateur.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Doctor/status devrait signaler le fournisseur effectif exact, le profil d'authentification, le runtime et la source d'épingle de session pour le tour actuel.
- La réparation de mise à niveau a besoin de plus de couverture de fixture de bout en bout pour les installations OAuth uniquement.
- La réparation de route obsolète devrait éviter de réécrire silencieusement les routes intentionnellement protégées.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente `openclaw models status`, `models auth list`, `config get`, `doctor --fix`, `config validate` et le comportement de l'indicateur de statut pour le runtime Codex.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness.md` documente `/status`, `/codex status`, `/codex models`, `/new`, `/reset` et les points d'entrée de dépannage.
- `/Users/kevinlin/code/openclaw/docs/automation/auth-monitoring.md` documente la surveillance et les surfaces de réparation de l'authentification.

### Source

- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/codex-route-warnings.ts` détecte et répare les références de modèle héritées, les épingles de runtime obsolètes, les remplacements de compaction Codex non pris en charge et l'état de route de session persistant.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/stale-oauth-profile-shadows.ts` analyse et répare les magasins d'ombre de profil OAuth obsolètes.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-auth-profile-config.ts` protège les métadonnées du profil d'authentification actif lors de la réparation de la configuration.
- `/Users/kevinlin/code/openclaw/src/commands/models/list.status-command.ts` et `src/commands/models/list.auth-overview.ts` soutiennent la sortie de statut du modèle et d'aperçu d'authentification.
- `/Users/kevinlin/code/openclaw/src/commands/provider-auth-guidance.ts` fournit des conseils d'authentification du fournisseur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre le comportement de liste/statut du modèle et la disponibilité du catalogue de fournisseurs.
- `/Users/kevinlin/code/openclaw/src/commands/onboard-non-interactive.gateway-health-auth.test.ts` couvre le comportement d'intégration/santé de la passerelle liée à l'authentification.
- `/Users/kevinlin/code/openclaw/src/commands/configure.gateway-auth.test.ts` couvre le comportement de configuration de l'authentification de la passerelle.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/codex-route-warnings.test.ts` couvre le comportement de réparation de route Codex.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/stale-oauth-profile-shadows.test.ts` couvre la détection/réparation d'ombre de profil OAuth obsolète.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-auth.profile-health.test.ts` couvre la gestion de la santé du profil d'authentification.
- `/Users/kevinlin/code/openclaw/src/commands/models/list.status.test.ts` couvre la sortie de la commande de statut.
- `/Users/kevinlin/code/openclaw/src/commands/models/auth-list.test.ts` couvre le comportement de la liste d'authentification.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "openai gpt-5.5 codex runtime openai/gpt openai-codex route doctor"`

Résultats :

- A retourné les problèmes ouverts #87436, #80628, #84637, #87650, #84200, #84038, #83223, #84252 et #81213, incluant la recréation de route après docteur, la dérive de route protégée, la confusion runtime/modèle, l'incompatibilité fournisseur/runtime après mise à jour et la réparation partielle du sidecar OAuth.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "openai-codex doctor route auth profile Codex harness"`

Résultats :

- A retourné la PR #81700, `fix(auth): drop stale Codex OAuth routing`.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "openai gpt-5.5 codex runtime openai/gpt openai-codex route doctor"`

Résultats :

- A retourné les conseils de diagnostic du 2026-05-17 pour vérifier `/status`, l'état de route de session persistant, `providerOverride/modelOverride`, `agentHarnessId`, `agentRuntimeOverride`, la liaison CLI, les épingles de profil d'authentification et la réparation du docteur quand `openai/gpt-5.5` s'achemine de manière inattendue vers les réponses OpenAI directes.
- A retourné la note du 2026-05-09 indiquant que le docteur a corrigé les épingles de runtime d'agent entier obsolètes mais une route `openai/gpt-5.5` migrée OAuth uniquement a toujours échoué via l'authentification directe par clé API OpenAI.

Requête : `discrawl search --limit 10 "openai-codex oauth auth order usage limit profile"`

Résultats :

- A retourné des discussions où `models status --json`, les identifiants de profil, l'ordre d'authentification et l'état de refroidissement/désactivé étaient nécessaires pour diagnostiquer les défaillances de limite de taux/utilisation.
