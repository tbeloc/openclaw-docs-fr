---
title: "OpenAI / Codex provider path - Codex Oauth Profiles and Subscription Usage Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# OpenAI / Codex provider path - Codex Oauth Profiles and Subscription Usage Maturity Note

## Résumé

Codex OAuth et l'utilisation des abonnements bénéficient d'un support d'implémentation substantiel : OAuth navigateur, connexion par code d'appareil, sauvegarde par clé API, réparation d'ID de profil, extraction d'ID de compte, découverte CLI externe, refroidissements de profil et sondage d'utilisation WHAM sont tous représentés dans le code source et la documentation. La couverture est Beta plutôt que Stable car de nombreux flux sont difficiles à exercer sans comptes actifs et états de quota. La qualité est Alpha car l'historique du support archivé montre une confusion récurrente autour de plusieurs comptes, refroidissements, noms de fournisseurs et si une demande est facturée contre l'abonnement ChatGPT/Codex ou les crédits OpenAI Platform.

## Portée de la catégorie

Cette catégorie couvre les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation d'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.

## Fonctionnalités

- Codex OAuth Profiles : Couvre les profils OAuth Codex dans les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation d'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.
- Subscription Usage : Couvre l'utilisation des abonnements dans les profils d'authentification `openai-codex`, l'ordre des profils, la réparation des métadonnées de profil, l'actualisation des jetons, la propagation d'ID de compte, la gestion de l'utilisation/refroidissement et la sélection d'authentification pour les tours d'agent OpenAI soutenus par Codex.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (79%)`
- Signaux positifs : La documentation fournit des commandes directes pour la connexion OAuth, la connexion par code d'appareil, l'ordre d'authentification, le statut/sondage et la récupération ; le code source couvre la réparation du magasin d'authentification, l'actualisation des jetons, les sondages d'utilisation WHAM et l'isolation de l'environnement.
- Signaux négatifs : La preuve en direct pour les limites d'utilisation, plusieurs comptes ChatGPT et l'inadéquation du contexte de compte sont intrinsèquement spécifiques au compte et ne font pas partie d'une seule voie de sortie standard.
- Lacunes d'intégration : Plus de preuves en direct/sondage sont nécessaires pour la rotation de profil à travers les limites d'abonnement et pour la parité navigateur/code d'appareil sur les hôtes sans interface graphique.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : La première requête spécifique à l'authentification n'a retourné aucune ligne, mais la requête route/doctor a retourné plusieurs problèmes adjacents à l'authentification incluant #83223 et #84252.
- Rapports Discrawl : Les discussions des 2026-04-18, 2026-03-12, 2026-02-25 et 2026-02-20 discutent de plusieurs comptes `openai-codex`, fenêtres d'utilisation/limite de débit, inadéquation d'ID de compte, états de refroidissement/désactivation et inadéquation de fournisseur/modèle.
- Bonnes qualités : La gestion du refroidissement et de l'utilisation est explicite et appartient au code source ; la documentation fournit des commandes de statut et d'ordre d'authentification au lieu de masquer l'état.
- Mauvaises qualités : Les utilisateurs doivent toujours comprendre les ID de profil, les ID de compte, les fenêtres d'abonnement, la facturation Platform et la sélection à l'exécution pour déboguer les défaillances.
- Exclu de la qualité : La quantité de tests et le type de tests n'ont pas été utilisés pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Beta (79%)`
- Instructions de surface : évaluées par rapport à `references/completeness/openai-codex-provider-path.md`.
- Signaux positifs : les preuves archivées, le code source, les tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Codex OAuth Profiles, Subscription Usage.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La sortie de `models status --probe` doit continuer à distinguer le fournisseur d'authentification, l'exécution, l'ID de compte et le compartiment de facturation.
- La solution de secours multi-compte a besoin d'une preuve d'opérateur plus claire et de moins d'étapes d'interprétation manuelle.
- La réparation du profil OAuth a un historique d'archive visible d'échecs partiels de side-car et de profil obsolète.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/openai.md` documente Codex OAuth, la connexion par code d'appareil, l'utilisation d'ID de profil, les exemples d'ordre d'authentification, les commandes de statut/sondage et les avertissements de compte/facturation.
- `/Users/kevinlin/code/openclaw/docs/concepts/oauth.md` documente la sémantique du profil OAuth pour les fournisseurs.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness-reference.md` documente la précédence d'authentification et l'isolation de l'environnement pour les lancements locaux d'app-server stdio.

### Code source

- `/Users/kevinlin/code/openclaw/extensions/openai/openai-codex-provider.ts` enregistre les méthodes d'authentification OAuth, code d'appareil et sauvegarde par clé API, réparation des métadonnées d'ID de profil, récupération d'utilisation et actualisation des jetons.
- `/Users/kevinlin/code/openclaw/src/plugins/provider-openai-codex-oauth.ts` relie le hook d'authentification du plugin OpenAI aux appelants OAuth hérités.
- `/Users/kevinlin/code/openclaw/src/llm/utils/oauth/openai-codex.ts` implémente la connexion OAuth héritée et l'actualisation du pontage.
- `/Users/kevinlin/code/openclaw/src/llm/utils/oauth/openai-codex-jwt.ts` extrait le `chatgpt_account_id` des JWT Codex.
- `/Users/kevinlin/code/openclaw/src/agents/auth-profiles/usage.ts` sonde l'utilisation WHAM et applique l'état de refroidissement/blocage pour les défaillances `openai-codex`.
- `/Users/kevinlin/code/openclaw/src/agents/auth-profiles/repair.ts` répare les ID de profil OAuth `openai-codex:default` hérités.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-runner.run-embedded-agent.auth-profile-rotation.e2e.test.ts` couvre la rotation du profil d'authentification et le comportement de refroidissement dans les exécutions intégrées.
- `/Users/kevinlin/code/openclaw/src/commands/models.list.e2e.test.ts` couvre le comportement de liste de modèles conscient de l'authentification.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-auth-profiles-oauth-policy.test.ts` couvre les limites de la politique OAuth à l'exécution.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/openai/openai-codex-oauth-flow.runtime.test.ts` couvre le comportement du flux OAuth OpenAI Codex.
- `/Users/kevinlin/code/openclaw/extensions/openai/openai-codex-device-code.test.ts` couvre le comportement de la connexion par code d'appareil.
- `/Users/kevinlin/code/openclaw/extensions/openai/openai-codex-auth-identity.test.ts` couvre l'extraction d'identité de l'authentification Codex.
- `/Users/kevinlin/code/openclaw/src/llm/utils/oauth/openai-codex.test.ts` couvre le comportement du helper OAuth.
- `/Users/kevinlin/code/openclaw/src/agents/auth-profiles/usage.test.ts` couvre l'utilisation et l'état de refroidissement.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "openai-codex oauth auth.order usage limit wham profile"`

Résultats :

- N'a retourné aucune ligne correspondante. Ceci a été traité comme neutre après des vérifications de fraîcheur réussies, pas comme une preuve de qualité positive.

Requête : `gitcrawl --json search issues -R openclaw/openclaw "openai gpt-5.5 codex runtime openai/gpt openai-codex route doctor"`

Résultats :

- A retourné les problèmes ouverts adjacents à l'authentification #83223 et #84252 concernant `openai/gpt-5.5` migré recherchant toujours l'authentification `openai-codex` avant le repli et l'authentification du side-car OAuth restant partiellement réparée.

### Requêtes Discrawl

Requête : `discrawl search --limit 10 "openai-codex oauth auth order usage limit profile"`

Résultats :

- A retourné des discussions sur plusieurs comptes `openai-codex`, ordre de profil, adhérence de session, `weekly/monthly limit reached`, inadéquation d'ID de compte et états de profil de refroidissement/désactivation.

Requête : `discrawl search --limit 10 "openai gpt-5.5 codex runtime openai/gpt openai-codex route doctor"`

Résultats :

- A retourné une discussion du 2026-05-17 où `openai/gpt-5.5` pourrait atteindre les réponses OpenAI directes lorsque des épingles d'exécution/authentification obsolètes étaient présentes, plus des notes que le docteur devrait réparer `openai-codex/*`, les épingles d'exécution obsolètes et les épingles de fournisseur/modèle/authentification.
