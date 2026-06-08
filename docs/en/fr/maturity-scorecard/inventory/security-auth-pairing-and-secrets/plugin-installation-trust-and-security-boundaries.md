---
title: "Sécurité, authentification, appairage et secrets - Note de maturité de confiance des plugins"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Sécurité, authentification, appairage et secrets - Note de maturité de confiance des plugins

## Résumé

OpenClaw dispose d'un modèle de confiance des plugins significatif : les manifestes sont inspectés avant le chargement à l'exécution, les schémas de configuration et les métadonnées sont déclaratifs, des analyses de sécurité à l'installation existent, les permissions des plugins utilisent des flux d'approbation Gateway, et l'audit de sécurité avertit sur le code des plugins et l'état d'installation. La couverture est Beta car les tests de manifeste/permission/analyse d'installation sont larges, mais les scénarios réels d'installation, mise à jour, restauration, permission et compatibilité de tiers restent moins éprouvés que le comportement des plugins groupés. La qualité est Beta car la conception est solide, mais les listes blanches de plugins, l'intégrité d'installation, les préoccupations de chargement automatique et l'accès à la conversation de manifeste sont toujours des domaines de maturité actifs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Confiance d'installation des plugins : couvre la confiance d'installation des plugins sur la confiance du manifeste du plugin, les analyses de sécurité d'installation/mise à jour des plugins, les listes blanches de plugins, les métadonnées d'authentification/secret détenues par le manifeste, et le comportement de confiance et de limites de sécurité d'installation de plugins associé.
- Limites de sécurité : couvre les limites de sécurité sur la confiance du manifeste du plugin, les analyses de sécurité d'installation/mise à jour des plugins, les listes blanches de plugins, les métadonnées d'authentification/secret détenues par le manifeste, et le comportement de confiance et de limites de sécurité d'installation de plugins associé.

## Fonctionnalités

- Confiance d'installation des plugins : couvre la confiance d'installation des plugins sur la confiance du manifeste du plugin, les analyses de sécurité d'installation/mise à jour des plugins, les listes blanches de plugins, les métadonnées d'authentification/secret détenues par le manifeste, et le comportement de confiance et de limites de sécurité d'installation de plugins associé.
- Limites de sécurité : couvre les limites de sécurité sur la confiance du manifeste du plugin, les analyses de sécurité d'installation/mise à jour des plugins, les listes blanches de plugins, les métadonnées d'authentification/secret détenues par le manifeste, et le comportement de confiance et de limites de sécurité d'installation de plugins associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : le manifeste du plugin, l'éligibilité du contrat, l'analyse de sécurité d'installation, les approbations de plugins, les limites d'exécution et les permissions d'état des plugins ont tous des tests ciblés ; la documentation couvre clairement les manifestes et les demandes de permission.
- Signaux négatifs : la couverture est plus forte pour les métadonnées statiques et les contrats groupés/d'exécution que pour les scénarios réels d'installation/mise à jour/restauration de plugins externes et les sources de paquets malveillants.
- Lacunes d'intégration : ajouter des scénarios de version récurrents pour installer un plugin tiers, refuser les sources de paquets non sûres, activer les listes blanches de plugins explicites, demander les approbations de plugins, exposer les outils de plugins, mettre à jour/restaurer, et prouver que les métadonnées de secrets restent masquées.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : la requête de problème exacte n'a retourné aucune ligne de problème local. La requête de PR a retourné la PR ouverte #72690 pour l'accès à la conversation de manifeste et #81402 pour le stockage d'état d'exécution, tous deux adjacents à la confiance des plugins et à la maturité d'état d'exécution.
- Rapports Discrawl : la requête de plugin exacte n'a retourné aucune ligne visible, tandis que les preuves Discord de sécurité plus larges ont mis en évidence la désactivation du chargement automatique des plugins comme un changement pertinent pour la sécurité et les rapports d'audit de sécurité incluent les vérifications d'installation et de sécurité du code des plugins.
- Bonnes qualités : les manifestes sont lus avant l'exécution du code du plugin, les manifestes invalides bloquent la validation de la configuration, les invites de permission des plugins sont séparées des approbations d'exécution, et les analyses d'installation peuvent bloquer les sources non sûres.
- Mauvaises qualités : la confiance des plugins externes est toujours une limite en évolution rapide, les listes blanches de plugins ne sont pas toujours explicites, et les vérifications de métadonnées/intégrité/sécurité du code d'installation exigent que les opérateurs comprennent les avertissements.
- Exclu de la qualité : la largeur de la couverture, la largeur des tests unitaires et la profondeur des tests d'intégration ne sont notées que sous Couverture.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/security-auth-pairing-and-secrets.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la confiance d'installation des plugins et les limites de sécurité.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La preuve du cycle de vie des plugins tiers est plus mince que celle des plugins groupés.
- Les vérifications de liste blanche de plugins et d'intégrité d'installation ont besoin de preuves de scénario d'opérateur plus claires.
- Les sémantiques d'accès au niveau du manifeste sont toujours en expansion.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md` documente les manifestes déclaratifs, les schémas de configuration, les métadonnées d'authentification/configuration et les métadonnées de contrat statique qui peuvent être inspectées avant le chargement à l'exécution.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-permission-requests.md` documente les invites d'approbation de plugins, le comportement de décision, le routage et la séparation des approbations d'exécution.
- `/Users/kevinlin/code/openclaw/docs/plugins/manage-plugins.md`, `/Users/kevinlin/code/openclaw/docs/plugins/compatibility.md` et `/Users/kevinlin/code/openclaw/docs/plugins/install-overrides.md` couvrent le cycle de vie et la compatibilité des plugins.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/audit-checks.md` documente la liste blanche de plugins, l'intégrité d'installation, la dérive de version, la sécurité du code et les vérifications d'audit de réachabilité des outils de plugins.

### Source

- `/Users/kevinlin/code/openclaw/src/plugins/manifest.ts`, `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.ts` et `/Users/kevinlin/code/openclaw/src/plugins/manifest-contract-eligibility.ts` implémentent le comportement du manifeste et du contrat statique.
- `/Users/kevinlin/code/openclaw/src/plugins/install-security-scan.ts` distribue les analyses d'installation de source, paquet, arborescence de dépendances, fichier et compétence.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/plugin-approval.ts` et `/Users/kevinlin/code/openclaw/src/infra/plugin-approvals.ts` implémentent les flux d'approbation de plugins Gateway.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime/runtime-plugin-boundary.ts` et `/Users/kevinlin/code/openclaw/src/plugins/runtime/runtime-registry-loader.ts` implémentent le comportement de limite et de chargement de plugins d'exécution.
- `/Users/kevinlin/code/openclaw/src/plugin-state/plugin-state-store.permissions.test.ts` ancre le comportement de permission d'état de plugin.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/plugins/install-security-scan.runtime.ts` est couvert par les tests d'analyse d'exécution et les tests de version pour le comportement de sécurité d'installation.
- `/Users/kevinlin/code/openclaw/src/plugins/npm-install-security-scan.release.test.ts` couvre le comportement d'analyse de sécurité d'installation npm.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime-plugin-boundary.whatsapp.test.ts` couvre une limite de plugin d'exécution via un plugin de canal.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime-config-collectors-plugins.bundled.test.ts` et `/Users/kevinlin/code/openclaw/src/secrets/runtime.loadable-plugin-origins.test.ts` couvrent le comportement de métadonnées de secret de plugin/origine d'exécution.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/manifest-contract-runtime.test.ts`, `/Users/kevinlin/code/openclaw/src/plugins/manifest-contract-eligibility.test.ts`, `/Users/kevinlin/code/openclaw/src/plugins/manifest-registry.test.ts` et `/Users/kevinlin/code/openclaw/src/plugins/manifest-owner-policy.test.ts` couvrent les contrats de manifeste.
- `/Users/kevinlin/code/openclaw/src/plugins/bundle-manifest.test.ts`, `/Users/kevinlin/code/openclaw/src/plugins/manifest-metadata-scan.test.ts` et `/Users/kevinlin/code/openclaw/src/plugins/manifest.json5-tolerance.test.ts` couvrent l'analyse et les métadonnées du manifeste.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/plugin-approval.test.ts`, `/Users/kevinlin/code/openclaw/src/infra/plugin-approval-forwarder.test.ts` et `/Users/kevinlin/code/openclaw/src/plugin-sdk/approval-*.test.ts` couvrent le comportement d'approbation de plugins.
- `/Users/kevinlin/code/openclaw/src/plugin-state/plugin-state-store.permissions.test.ts` couvre les permissions d'état de plugin.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "plugin manifest permissions security install scan"`

Résultats :

- Retourné `[]` dans l'archive de problèmes locale actuelle.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "plugin approval manifest permissions security"`

Résultats :

- Retourné la PR ouverte #72690, `Feature/issue: 71428 manifest conversation access`, et la PR ouverte #81402, `refactor: move runtime state to SQLite`.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "plugin manifest permissions security install scan"`

Résultats :

- Retourné aucune ligne visible.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "plugin auto-load disabled manifest permissions"`

Résultats :

- Retourné aucune ligne visible pour cette requête exacte. La discussion de sécurité adjacente dans la recherche du navigateur/contrôle a résumé la désactivation du chargement automatique des plugins comme un changement pertinent pour la sécurité.
