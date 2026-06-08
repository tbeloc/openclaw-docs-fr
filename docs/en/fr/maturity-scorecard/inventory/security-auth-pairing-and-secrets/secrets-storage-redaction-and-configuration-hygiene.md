---
title: "Sécurité, authentification, appairage et secrets - Note de maturité de l'hygiène des identifiants et des secrets"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de maturité de l'hygiène des identifiants et des secrets

## Résumé

OpenClaw dispose d'un système robuste de SecretRef et de masquage : les identifiants pris en charge peuvent sortir de la configuration en texte brut, le démarrage et le rechargement utilisent des instantanés d'exécution résolus, les rapports d'audit signalent les résidus en texte brut/non résolus/masqués, et les instantanés d'interface utilisateur/configuration utilisent des sentinelles de masquage. La couverture est Stable car la documentation et les sources sont larges et la preuve d'exécution couvre la résolution, les audits, le masquage, les surfaces d'authentification de passerelle, les cibles de plugin/canal et les flux d'application/configuration. La qualité est Beta car les opérateurs découvrent encore fréquemment des résidus en texte brut, les résidus OAuth hérités sont intentionnellement hors de portée, et certaines surfaces non prises en charge nécessitent une interprétation prudente.

## Portée de la catégorie

Inclus dans cette catégorie :

- Profils d'authentification du fournisseur : couvre les profils d'authentification du fournisseur sur les identifiants du fournisseur et la santé de l'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportements connexes des profils d'authentification du fournisseur et de la santé des clés API.
- Santé des clés API : couvre la santé des clés API sur les identifiants du fournisseur et la santé de l'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportements connexes des profils d'authentification du fournisseur et de la santé des clés API.
- Stockage des secrets : couvre le stockage des secrets sur le contrat SecretRef et les fournisseurs, les instantanés de secrets d'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré, et les comportements connexes de stockage des secrets, de masquage et d'hygiène de configuration.
- Masquage : couvre le masquage sur le contrat SecretRef et les fournisseurs, les instantanés de secrets d'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré, et les comportements connexes de stockage des secrets, de masquage et d'hygiène de configuration.
- Hygiène de la configuration : couvre l'hygiène de la configuration sur le contrat SecretRef et les fournisseurs, les instantanés de secrets d'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré, et les comportements connexes de stockage des secrets, de masquage et d'hygiène de configuration.

## Fonctionnalités

- Profils d'authentification du fournisseur : couvre les profils d'authentification du fournisseur sur les identifiants du fournisseur et la santé de l'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportements connexes des profils d'authentification du fournisseur et de la santé des clés API.
- Santé des clés API : couvre la santé des clés API sur les identifiants du fournisseur et la santé de l'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportements connexes des profils d'authentification du fournisseur et de la santé des clés API.
- Stockage des secrets : couvre le stockage des secrets sur le contrat SecretRef et les fournisseurs, les instantanés de secrets d'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré, et les comportements connexes de stockage des secrets, de masquage et d'hygiène de configuration.
- Masquage : couvre le masquage sur le contrat SecretRef et les fournisseurs, les instantanés de secrets d'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré, et les comportements connexes de stockage des secrets, de masquage et d'hygiène de configuration.
- Hygiène de la configuration : couvre l'hygiène de la configuration sur le contrat SecretRef et les fournisseurs, les instantanés de secrets d'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré, et les comportements connexes de stockage des secrets, de masquage et d'hygiène de configuration.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : la documentation des secrets est détaillée ; la source inclut un système d'instantané d'exécution dédié, un scanner d'audit, un registre de cibles, un schéma SecretRef, une masquage de configuration et des méthodes de passerelle ; les tests couvrent de nombreuses cibles d'identifiants et modes de défaillance.
- Signaux négatifs : la couverture des gestionnaires d'identifiants externes et des intégrations réelles du fournisseur SecretRef exec est moins visible que les chemins env/file/static, et le modèle d'audit ne peut intentionnellement pas couvrir les fichiers non pris en charge arbitraires.
- Lacunes d'intégration : ajouter une preuve de scénario d'opérateur récurrente pour migrer l'authentification de passerelle, les jetons de canal, les clés de fournisseur, les secrets de configuration de plugin, les résidus de modèles générés et le rechargement d'exécution sur macOS/Linux/Docker.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : la requête de problème exacte n'a retourné aucune ligne de problème local. Les preuves pertinentes d'archive PR/commentaire apparaissent plutôt dans Discord, y compris l'examen des faux négatifs de type URL SecretRef en texte brut.
- Rapports Discrawl : la requête Discord exacte a trouvé plusieurs sorties `secrets audit` réelles avec des jetons de passerelle en texte brut, des jetons de canal, des clés API de modèle généré, des clés `.env`, des refs non résolues et des résidus OAuth hérités ; les responsables expliquent l'ordre de migration et les avertissements.
- Bonnes qualités : les SecretRefs échouent rapidement pour les refs non résolues actives, le rechargement est atomique, l'audit a des résultats structurés et des codes de sortie, les instantanés de configuration utilisent des sentinelles de masquage, et la documentation indique explicitement que les SecretRefs ne sont pas l'isolation de processus.
- Mauvaises qualités : les opérateurs doivent toujours comprendre les résidus en texte brut, les fichiers de modèles générés, les résidus OAuth, les surfaces non prises en charge et la disponibilité du fournisseur SecretRef ; les faux négatifs d'audit pour les identifiants intégrés dans les valeurs de type URL étaient toujours en cours d'examen.
- Exclu de la qualité : la largeur de couverture, la largeur des tests unitaires et la profondeur des tests d'intégration ne sont notées que sous Couverture.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les profils d'authentification du fournisseur, la santé des clés API, le stockage des secrets, le masquage et l'hygiène de la configuration.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La migration SecretRef est optionnelle et ne rend pas les fichiers en texte brut lisibles sûrs.
- Les identifiants OAuth restent une classe de résidu distincte en dehors de la migration SecretRef statique.
- Certaines formes d'identifiants de type URL ou spécifiques aux plugins nécessitent des mises à jour continues du registre de cibles et de l'audit.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/gateway/secrets.md` documente les instantanés d'exécution SecretRef, le filtrage de surface active, les contrats de fournisseur, les diagnostics d'authentification de passerelle, la sécurité du fournisseur file/exec et les limites de migration.
- `/Users/kevinlin/code/openclaw/docs/cli/secrets.md` documente l'audit, la configuration, l'application, le rechargement, les codes de sortie, le comportement du plan et le nettoyage en texte brut sans restauration.
- `/Users/kevinlin/code/openclaw/docs/reference/secretref-credential-surface.md` et `/Users/kevinlin/code/openclaw/docs/reference/secret-placeholder-conventions.md` documentent les cibles d'identifiants prises en charge et les conventions de placeholder.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/audit-checks.md` documente la configuration, le profil d'authentification, le répertoire des identifiants, le fichier journal, le jeton de hook et les vérifications de masquage de journalisation.

### Source

- `/Users/kevinlin/code/openclaw/src/secrets/runtime.ts` prépare et active les instantanés d'exécution résolus.
- `/Users/kevinlin/code/openclaw/src/secrets/audit.ts` analyse la configuration, les profils d'authentification, les magasins de modèles générés, `.env`, les refs non résolues, l'ombrage et les résidus hérités.
- `/Users/kevinlin/code/openclaw/src/secrets/target-registry.ts` et `/Users/kevinlin/code/openclaw/src/secrets/target-registry-data.ts` définissent les surfaces porteuses de secrets prises en charge.
- `/Users/kevinlin/code/openclaw/src/config/redact-snapshot.ts` masque les valeurs de configuration sensibles et utilise `__OPENCLAW_REDACTED__` pour les allers-retours d'interface utilisateur sûrs.
- `/Users/kevinlin/code/openclaw/src/logging/redact.ts` et `/Users/kevinlin/code/openclaw/src/logging/diagnostic-support-redaction.ts` fournissent le masquage des journaux et des diagnostics.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/secrets/runtime.auth.integration.test.ts` et `/Users/kevinlin/code/openclaw/src/secrets/runtime.gateway-auth.integration.test.ts` couvrent l'activation des secrets d'exécution avec les surfaces d'authentification.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-config-collectors-channels.test.ts` et `/Users/kevinlin/code/openclaw/src/secrets/runtime-config-collectors-plugins.test.ts` couvrent les collecteurs de secrets de canal et de plugin.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-web-tools-public-artifacts.runtime.ts`, `/Users/kevinlin/code/openclaw/src/secrets/runtime-web-tools-manifest.runtime.ts` et `/Users/kevinlin/code/openclaw/src/secrets/runtime-manifest.runtime.ts` couvrent les surfaces de manifeste d'exécution/plugin.
- `/Users/kevinlin/code/openclaw/src/cli/secrets-cli.test.ts` couvre le comportement de la commande CLI secrète.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/secrets/audit.test.ts`, `/Users/kevinlin/code/openclaw/src/secrets/apply.test.ts`, `/Users/kevinlin/code/openclaw/src/secrets/configure.test.ts`, `/Users/kevinlin/code/openclaw/src/secrets/resolve.test.ts` et `/Users/kevinlin/code/openclaw/src/secrets/ref-contract.test.ts` couvrent l'audit, l'application, la configuration, la résolution et le schéma SecretRef.
- `/Users/kevinlin/code/openclaw/src/config/redact-snapshot.test.ts`, `/Users/kevinlin/code/openclaw/src/config/redact-snapshot.raw.test.ts` et `/Users/kevinlin/code/openclaw/src/config/sessions/transcript-append-redact.test.ts` couvrent le masquage.
- `/Users/kevinlin/code/openclaw/src/logging/log-tail-redaction.test.ts`, `/Users/kevinlin/code/openclaw/src/logging/logger-redaction-behavior.test.ts` et `/Users/kevinlin/code/openclaw/src/logging/redact.test.ts` couvrent le masquage des journaux.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/secrets.test.ts` couvre les méthodes de secrets de passerelle.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "SecretRef secrets audit plaintext credentials redaction"`

Résultats :

- A retourné `[]` dans l'archive de problèmes locale actuelle.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "SecretRef secrets audit plaintext credentials redaction"`

Résultats :

- A retourné `[]` dans l'archive PR locale actuelle.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "SecretRef secrets audit plaintext credentials redaction"`

Résultats :

- N'a retourné aucune ligne visible.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "SecretRef plaintext credentials audit"`

Résultats :

- A trouvé plusieurs cas d'assistance de mars-avril avec des résultats `secrets audit` en texte brut pour `gateway.auth.token`, les jetons de canal, les clés API de plugin, les clés `models.json` générées, les clés `.env`, les refs non résolues et les résidus OAuth hérités.
- A trouvé un commentaire d'examen sur la PR #69417 notant que les valeurs d'en-tête/env MCP de type URL avec des identifiants intégrés pourraient être manqués par l'audit s'ils sont vérifiés uniquement en tant qu'URL.
