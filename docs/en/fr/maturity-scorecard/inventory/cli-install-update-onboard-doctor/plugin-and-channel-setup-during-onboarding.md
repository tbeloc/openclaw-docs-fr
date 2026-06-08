---
title: CLI - Note de maturité de la configuration des plugins et des canaux
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# CLI - Note de maturité de la configuration des plugins et des canaux

## Résumé

L'interface CLI supporte l'installation guidée des sources de plugins, la configuration des comptes de canaux et les vérifications de statut et de capacités post-configuration. La couverture est forte en raison d'une large surface d'implémentation et de test, mais la qualité est modérée car l'installation de plugins et le comportement des canaux externalisés continuent de créer de la confusion chez les opérateurs.

## Portée de la catégorie

Cette catégorie couvre les sources d'installation de plugins, la configuration des canaux et des comptes, ainsi que la vérification post-configuration pendant ou après l'intégration. Elle ne couvre pas l'authentification du modèle de fournisseur ni la création du SDK de plugins non-canaux.

## Fonctionnalités

- Sélecteur de canaux : L'intégration peut guider l'opérateur dans le choix des canaux à configurer.
- Sources d'installation de plugins : La configuration des plugins supporte les sources d'installation groupées, npm, ClawHub, marketplace, git et locales.
- Configuration des comptes de canaux : Les commandes de canaux supportent la configuration interactive et basée sur des drapeaux pour les transports de chat supportés.
- Sondes post-configuration : Les opérateurs peuvent vérifier le statut et les capacités des canaux après la configuration pour vérifier que le compte configuré fonctionne.
- Avertissement de passerelle distante : La documentation d'intégration distante indique que l'installation de plugins ne se fait pas localement lorsque la passerelle s'exécute ailleurs.

## Fraîcheur de l'archive

- gitcrawl: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`, `api_supported=false`, `github_token_present=false`.
- discrawl: `generated_at=2026-05-30T01:10:41Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - `docs/cli/onboard.md`, `docs/cli/plugins.md` et `docs/cli/channels.md` décrivent les sources d'installation de plugins, la configuration des canaux et la vérification à l'exécution.
  - Les flux d'installation de plugins sont implémentés dans `src/cli/plugins-install-command.ts` et `src/commands/onboarding-plugin-install.ts`.
  - La configuration des canaux, le statut, les capacités, les journaux et les flux de résolution sont implémentés dans `src/commands/channels/add.ts`, `src/commands/channels/list.ts`, `src/commands/channels/status.ts`, `src/commands/channels/capabilities.ts` et `src/commands/channels/resolve.ts`.
  - Le dépôt contient des tests larges pour l'installation de plugins et les commandes de canaux.
- Signaux négatifs :
  - La surface globale est large et traverse l'état d'installation des paquets, les écritures de configuration et le comportement des plugins par canal.
  - Les plugins de canaux externalisés et optionnels créent toujours une complexité d'utilisabilité.
- Lacunes d'intégration :
  - Aucun test de fumée d'intégration de bout en bout n'a été trouvé qui installe un plugin de canal externe et prouve ensuite un chemin complet de connexion de compte et de sonde de capacité.

## Score de qualité

- Score : `Beta (72%)`
- Rapports de Gitcrawl :
  - La requête `gitcrawl search issues "plugins install channels add channels status" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné des résultats ouverts incluant `#68782 Add selective installation for plugins, skills, and channels`, `#79738 u4s-openclaw restart rewrites openclaw.json and breaks WhatsApp allowFrom / owner config` et `#78493 sudo openclaw update can create mixed ownership, then doctor overwrites config after EACCES/read failure`.
- Rapports de Discrawl :
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "plugins install channels add status"` a mis en évidence les notes de version concernant les travaux de réparation de plugins et de canaux, ainsi que la confusion des utilisateurs autour de l'installation du plugin WhatsApp, la découverte de canaux et `channels status`.
- Bonnes qualités :
  - L'interface CLI supporte plusieurs types de sources de plugins au lieu d'un seul chemin caché.
  - Les commandes de canaux exposent les surfaces de configuration, de statut, de capacité et de journaux plutôt que de forcer les modifications manuelles de configuration.
  - L'interface CLI d'installation de plugins dispose de tests extensifs de politique et de cas limites.
- Mauvaises qualités :
  - Les règles d'installation et d'activation des plugins de canaux externes sont toujours difficiles à comprendre pour les utilisateurs.
  - L'état du plugin/canal s'étend sur la configuration, les racines d'installation et les actualisations du registre à l'exécution, ce qui augmente le risque de dérive.
- Exclus de la qualité :
  - Les tests d'installation de plugins et de commandes de canaux ci-dessous sont des preuves de couverture uniquement.

## Lacunes connues

- Aucune preuve complète d'intégration de bout en bout de l'intégration au compte en direct pour les plugins de canaux externes n'a été trouvée.
- La sémantique d'empaquetage de canaux externalisés et d'installation sélective est toujours en flux.

## Preuves

### Docs

- `docs/cli/onboard.md`
- `docs/cli/plugins.md`
- `docs/cli/channels.md`

### Source

- `src/cli/plugins-install-command.ts`
- `src/commands/onboarding-plugin-install.ts`
- `src/commands/channels/add.ts`
- `src/commands/channels/list.ts`
- `src/commands/channels/status.ts`
- `src/commands/channels/capabilities.ts`
- `src/commands/channels/resolve.ts`

### Tests d'intégration

- Aucun trouvé pour un flux complet d'installation de plugin externe plus connexion de canal en direct.

### Tests unitaires

- `src/commands/onboarding-plugin-install.test.ts`
- `src/cli/plugins-cli.install.test.ts`
- `src/commands/channels.list.test.ts`
- `src/commands/channels.status.command-flow.test.ts`
- `src/commands/channels/capabilities.test.ts`
- `src/commands/channels.resolve.test.ts`

### Commandes de validation de surface

- `none declared in taxonomy`: `pass` - La surface CLI ne déclare pas de commandes de validation supplémentaires pour la notation.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "plugins install channels add channels status" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`

Résultats :

- `[{"number":68782,"state":"open","title":"Add selective installation for plugins, skills, and channels — reduce install size and startup overhead","url":"https://github.com/openclaw/openclaw/issues/68782"},{"number":79738,"state":"open","title":"u4s-openclaw restart rewrites openclaw.json and breaks WhatsApp allowFrom / owner config","url":"https://github.com/openclaw/openclaw/issues/79738"},{"number":86612,"state":"open","title":"Docker gateway container restart loop when OPENCLAW_SANDBOX=1 and OPENCLAW_HOME=/mnt/...","url":"https://github.com/openclaw/openclaw/issues/86612"},{"number":83223,"state":"open","title":"v2026.5.16-beta.5 audit: migrated openai/gpt-5.5 route still looks up openai-codex auth before fallback","url":"https://github.com/openclaw/openclaw/issues/83223"},{"number":78493,"state":"open","title":"sudo openclaw update can create mixed ownership, then doctor overwrites config after EACCES/read failure","url":"https://github.com/openclaw/openclaw/issues/78493"}]`

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "plugins install channels add status"`

Résultats :

- Les discussions de version et de support montrent un travail actif sur la réparation de plugins/canaux et une confusion répétée des opérateurs autour de l'installation de plugins externes, la découverte de canaux et les attentes de `channels status`.
