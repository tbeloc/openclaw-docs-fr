---
title: "Chemin du fournisseur Anthropic - Note de maturité des diagnostics et de la récupération"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Anthropic - Note de maturité des diagnostics et de la récupération

## Résumé

Les diagnostics Anthropic couvrent `models status`, la santé du profil d'authentification, les fenêtres d'utilisation OAuth/token, les conseils du docteur, la résolution des problèmes 429 en contexte long, les refroidissements et les conseils de secours. La couverture est Beta car des diagnostics importants existent dans la documentation, le code source et les tests, mais la surface de diagnostic est répartie entre le statut du modèle, le docteur, l'utilisation du fournisseur et les flux de runbook utilisateur. La qualité est Beta car les archives montrent que les utilisateurs ont toujours du mal à distinguer la facturation par clé API Anthropic, l'utilisation du compte Claude, les refroidissements, les erreurs d'utilisation supplémentaire et l'état du magasin de profils.

## Portée de la catégorie

Cette catégorie couvre les diagnostics d'opérateur et la récupération pour les défaillances du fournisseur Anthropic : sortie de statut, fenêtres d'utilisation, rapports de source de profil d'authentification, rapports de profil refroidi et désactivé, conseils du docteur, atténuation des 429 en contexte long, conseils de credentials manquants, configuration de secours et classification des erreurs/facturation du fournisseur.

## Fonctionnalités

- Statut du modèle : Couvre le statut du modèle dans les diagnostics d'opérateur et la récupération pour les défaillances du fournisseur Anthropic : sortie de statut, fenêtres d'utilisation, rapports de source de profil d'authentification, rapports de profil refroidi et désactivé, et comportements de diagnostic et de récupération associés.
- Fenêtres d'utilisation : Couvre les fenêtres d'utilisation dans les diagnostics d'opérateur et la récupération pour les défaillances du fournisseur Anthropic : sortie de statut, fenêtres d'utilisation, rapports de source de profil d'authentification, rapports de profil refroidi et désactivé, et comportements de diagnostic et de récupération associés.
- Rapports de refroidissement/profil : Couvre les rapports de refroidissement/profil dans les diagnostics d'opérateur et la récupération pour les défaillances du fournisseur Anthropic : sortie de statut, fenêtres d'utilisation, rapports de source de profil d'authentification, rapports de profil refroidi et désactivé, et comportements de diagnostic et de récupération associés.
- Récupération en contexte long : Couvre la récupération en contexte long dans les diagnostics d'opérateur et la récupération pour les défaillances du fournisseur Anthropic : sortie de statut, fenêtres d'utilisation, rapports de source de profil d'authentification, rapports de profil refroidi et désactivé, et comportements de diagnostic et de récupération associés.
- Conseils de secours : Couvre les conseils de secours dans les diagnostics d'opérateur et la récupération pour les défaillances du fournisseur Anthropic : sortie de statut, fenêtres d'utilisation, rapports de source de profil d'authentification, rapports de profil refroidi et désactivé, et comportements de diagnostic et de récupération associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : La documentation couvre les erreurs de credentials Anthropic courantes et les 429 en contexte long ; le code source récupère les fenêtres d'utilisation Claude, rapporte les conseils du docteur et gère l'ordre des profils d'authentification du fournisseur/refroidissements ; les tests couvrent la récupération d'utilisation et le comportement du docteur.
- Signaux négatifs : La récupération est distribuée entre `models status`, `doctor`, la documentation de dépannage, la configuration de secours du modèle et les commandes de profil d'authentification plutôt qu'un flux de diagnostics Anthropic cohésif.
- Lacunes d'intégration : L'audit n'a pas trouvé un seul scénario de test de défaillance en direct pour la récupération d'authentification, d'utilisation, de refroidissement et de secours Anthropic.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : #80514 rapporte que l'avertissement de plafond Claude Pro Max est classé comme une défaillance de facturation ; #83268 rapporte l'orphelinage du profil de clé API ; #63145 demande la détection de santé par modèle sur les modèles configurés ; PR #85666 ignore les clés API Anthropic pour le statut d'utilisation ; PR #87697 efface les refroidissements de fournisseur obsolètes après réauthentification.
- Rapports Discrawl : Les résultats de l'archive Discord incluent des utilisateurs voyant « utilisation supplémentaire épuisée », jeton porteur invalide, confusion entre la facturation par clé API Anthropic et compte Claude, confusion de refroidissement de profil et décalages daemon/auth-store.
- Bonnes qualités : La documentation nomme les commandes concrètes, la récupération d'utilisation gère le secours OAuth/web, le docteur rapporte les profils OAuth obsolètes et les conseils d'actualisation, et le dépannage distingue l'éligibilité des credentials de la forme de configuration.
- Mauvaises qualités : Les utilisateurs doivent toujours mapper la sémantique de facturation et d'authentification Anthropic en amont au vocabulaire auth-store, refroidissement, secours et model-status d'OpenClaw.
- Exclu de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ceux-ci sont des entrées de couverture uniquement.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/anthropic-provider-path.md`.
- Signaux positifs : les archives de documentation, code source, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le statut du modèle, les fenêtres d'utilisation, les rapports de refroidissement/profil, la récupération en contexte long, les conseils de secours.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuve` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- `models status` aide, mais les utilisateurs ont souvent besoin d'une interprétation du mainteneur
  pour connecter la source auth-store, le statut de facturation et le comportement de secours du modèle.
- Le comportement du statut d'utilisation diffère selon le mode et la portée d'authentification.
- Le chemin 429 en contexte long est documenté, mais l'éligibilité en amont reste
  en dehors du contrôle d'OpenClaw.

## Preuve

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/anthropic.md` inclut des accordéons de dépannage pour l'invalidité du token, pas de clé API, pas de profil et tous les profils en refroidissement.
- `/Users/kevinlin/code/openclaw/docs/gateway/troubleshooting.md` documente le symptôme exact 429 en contexte long, les commandes pour inspecter les logs/statut/configuration, les causes et les options de correction.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md` documente le comportement d'expiration/actualisation OAuth, les suggestions de clé API Anthropic ou de token de configuration, et les rapports de refroidissement/désactivation de profil.
- `/Users/kevinlin/code/openclaw/docs/reference/prompt-caching.md` documente les compteurs de cache d'utilisation et le comportement du fournisseur Anthropic.

### Code source

- `/Users/kevinlin/code/openclaw/src/infra/provider-usage.fetch.claude.ts` récupère les fenêtres d'utilisation OAuth Anthropic, supporte le secours de session web claude.ai pour la portée `user:profile` manquante, et retourne des snapshots d'utilisation du fournisseur structurés.
- `/Users/kevinlin/code/openclaw/extensions/anthropic/register.runtime.ts` câble `fetchUsageSnapshot`, `resolveUsageAuth`, `buildAuthDoctorHint` et `isCacheTtlEligible`.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-claude-cli.ts` vérifie la commande Claude CLI, les credentials, les répertoires workspace/project et la santé du magasin de profils.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-helpers/provider-error-patterns.ts` et les aides de secours du fournisseur adjacentes classent les erreurs du fournisseur utilisées dans les décisions de récupération/secours.
- `/Users/kevinlin/code/openclaw/src/commands/models/list.status-command.ts` et les modules de liste/statut de modèle associés rendent la santé du fournisseur/authentification.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre la réactivité du catalogue fournisseur/authentification dans la surface de commande des modèles.
- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` vérifie les exigences de credentials Anthropic et le câblage de profil en direct dans l'acceptation du package.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/infra/provider-usage.fetch.claude.test.ts` couvre le comportement de récupération d'utilisation Claude.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-claude-cli.test.ts` couvre les diagnostics du docteur Claude CLI.
- `/Users/kevinlin/code/openclaw/src/commands/models/list.status.test.ts` et les tests de statut/liste de modèle associés couvrent le rendu du statut du fournisseur.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-helpers/provider-error-patterns.test.ts` couvre la classification des erreurs du fournisseur.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic usage status API key Claude"`

Résultats :

- #83268 rapporte l'orphelinage du fournisseur de l'assistant de clé API.
- #80514 rapporte que l'avertissement de plafond Claude Pro Max est classé comme une défaillance de facturation et crée un faux refroidissement.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic 429 long context extra usage required fallback"`

Résultats :

- N'a retourné aucun résultat direct pour cette requête de problème exacte.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "Anthropic No API key found provider anthropic models status"`

Résultats :

- A retourné les problèmes d'authentification/statut du fournisseur associés, y compris #63145 pour les vérifications de santé par modèle et les problèmes de profil d'authentification d'autres fournisseurs.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "Anthropic usage status Claude API key"`

Résultats :

- A retourné les fils de support sur la facturation par clé API par rapport à l'utilisation du compte Claude, les erreurs d'utilisation supplémentaire, le jeton porteur invalide, la source du profil du fournisseur et ce qu'il faut inspecter dans `openclaw models status`.

Requête : `discrawl search --limit 10 "Claude 4.6 1M context Anthropic 429"`

Résultats :

- A retourné les conseils de dépannage 429 en contexte long et les notes d'éligibilité d'utilisation supplémentaire.

Requête : `discrawl search --limit 10 "Anthropic API key no credentials profile"`

Résultats :

- A retourné les fils de décalage de profil/magasin, pas de clé/pas de profil et confusion de token de configuration.
