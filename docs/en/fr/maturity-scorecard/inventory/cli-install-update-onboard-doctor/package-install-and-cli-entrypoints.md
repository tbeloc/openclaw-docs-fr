---
title: CLI - Note de maturité de la configuration CLI
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# CLI - Note de maturité de la configuration CLI

## Résumé

OpenClaw expose plusieurs chemins d'installation documentés pour les opérateurs normaux : scripts d'installation hébergés, installations avec préfixe local, installations via gestionnaire de paquets global, utilisation de checkout source, et conseils explicites sur le runtime Node. La couverture est solide pour les attentes du lanceur documenté et du runtime, mais le dépôt ne contient toujours pas de validation complète de bout en bout pour les combinaisons de matrice d'environnement et d'installateur publiés.

## Portée de la catégorie

Cette catégorie couvre la façon dont un utilisateur obtient la CLI sur une machine, satisfait les attentes de runtime supportées, et vérifie que la commande racine `openclaw` démarre, affiche l'aide, et rapporte la version. Elle ne couvre pas les choix d'intégration ou les opérations de service de passerelle gérée.

## Fonctionnalités

- Scripts d'installation : Les scripts d'installation hébergés configurent Node, installent OpenClaw, et optionnellement démarrent l'intégration.
- Installation avec préfixe local : L'installateur avec préfixe local garde Node et OpenClaw sous un répertoire OpenClaw dédié au lieu de dépendre d'un runtime système.
- Installations via gestionnaire de paquets : Les installations globales npm, pnpm et bun sont supportées quand l'opérateur gère Node directement, y compris les attentes de câblage PATH.
- Runtime Node supporté : OpenClaw documente les versions Node supportées et le runtime recommandé avant que les workflows CLI normaux ne continuent.
- Installation depuis checkout source : Les opérateurs peuvent exécuter OpenClaw depuis un checkout source pour les workflows de développement ou de récupération, et les flux de mise à jour distinguent ce chemin des installations de paquets.
- Point d'entrée CLI : Le lanceur openclaw empaqueté, openclaw --help, openclaw --version, vérification préalable du runtime, et les attentes de récupération basiques sont documentées.

## Fraîcheur de l'archive

- gitcrawl: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`, `api_supported=false`, `github_token_present=false`.
- discrawl: `generated_at=2026-05-30T01:10:41Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs :
  - La page d'accueil d'installation documente les installateurs hébergés, les installations avec préfixe local, les globals npm/pnpm/bun, et les flux de checkout source dans `docs/install/index.md`.
  - La référence d'installation documente `install.sh`, `install-cli.sh`, et `install.ps1`, y compris les drapeaux d'automatisation Windows, dans `docs/install/installer.md`.
  - `docs/install/node.md` documente Node 24 comme recommandé et Node 22.19+ comme supporté, plus les chemins de récupération PATH et permission.
  - `docs/install/updating.md` documente le passage entre les installations de paquets et les installations git/source.
  - Les chemins rapides du point d'entrée CLI racine sont couverts dans `src/entry.ts`, `src/entry.version-fast-path.ts`, `src/entry.test.ts`, et `src/version.test.ts`.
  - Le comportement de respawn qui préserve l'utilisabilité de l'aide/version dans les cas limites du lanceur est exercé dans `src/entry.respawn.test.ts`.
  - La logique de détection du type d'installation et du gestionnaire de paquets existe dans `src/cli/update-cli/shared.ts`, `src/cli/install-spec.ts`, `src/infra/install-target.ts`, et `src/bootstrap/node-extra-ca-certs.ts`.
- Signaux négatifs :
  - Aucun test d'intégration ou e2e local au dépôt n'a été trouvé pour les scripts d'installation hébergés depuis un état de machine propre.
  - Le comportement d'installation avec préfixe local est bien documenté, mais la preuve est principalement des docs plus des utilitaires de support plutôt qu'un flux automatisé dédié.
  - La plupart de la preuve du chemin runtime est des docs statiques plus des tests unitaires plutôt qu'une large matrice de combinaisons de gestionnaire de paquets et de gestionnaire de version.
- Lacunes d'intégration :
  - Aucun smoke macOS/Linux/Windows automatisé qui exécute les scripts d'installation publiés et valide que le binaire CLI résultant a été trouvé.
  - Aucune large matrice e2e n'a été trouvée validant les combinaisons npm/pnpm/bun plus gestionnaire de version sur macOS/Linux/Windows.

## Score de qualité

- Score : `Beta (75%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl search issues "install.ps1 install.sh npm pnpm bun openclaw install" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné `[]`.
  - La requête `gitcrawl search issues "install.sh install.ps1 local prefix npm pnpm bun" -R openclaw/openclaw --state closed --json number,title,url,state --limit 5` a retourné `[]`.
  - La requête `gitcrawl search issues "Node version package manager pnpm bun npm runtime openclaw" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné `[]`.
  - La requête `gitcrawl search issues "node 24 pnpm bun install docs" -R openclaw/openclaw --state closed --json number,title,url,state --limit 5` a retourné `[]`.
- Rapports Discrawl :
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "install.ps1 openclaw install"` a retourné des conseils d'aide utilisateur récents pointant les gens vers `install.ps1` et les instructions d'installation du site.
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "Node pnpm bun npm openclaw"` a mis en surface une PR de docs et une discussion clarifiant le support d'installation Bun et les recommandations de runtime de passerelle.
- Bonnes qualités :
  - La matrice d'installation est explicite et orientée opérateur au lieu de forcer un chemin caché unique.
  - Les chemins rapides d'aide/version racine réduisent le coût de démarrage et gardent la CLI utilisable même quand l'arbre runtime complet n'est pas nécessaire.
  - Les chemins de checkout source et de gestionnaire de paquets sont tous deux de première classe dans les docs.
  - Les attentes de runtime supportées sont explicites au lieu d'implicites.
  - La logique de mise à jour/installation distingue les checkouts git des installations de paquets plutôt que de traiter toutes les racines de manière identique.
- Mauvaises qualités :
  - La qualité de l'installateur dépend toujours fortement de l'état de l'environnement shell, PATH, et gestionnaire de paquets externe.
  - La verbosité de l'installateur Windows est toujours limitée selon la documentation de l'installateur.
  - Les résultats de l'opérateur dépendent toujours des gestionnaires de runtime externes, de la configuration PATH, et du comportement du gestionnaire de paquets système.
- Exclu de la qualité :
  - `src/entry.test.ts`, `src/version.test.ts`, `src/entry.respawn.test.ts`, `src/bootstrap/node-extra-ca-certs.test.ts`, `src/infra/detect-package-manager.test.ts`, et `src/infra/install-target.test.ts` fournissent uniquement une corroboration de couverture.

## Lacunes connues

- Les scripts d'installation hébergés manquent de preuve e2e du dépôt principal.
- Le comportement d'installation avec préfixe local bénéficierait d'un chemin de smoke automatisé explicite.
- Aucune preuve d'intégration de matrice d'environnement pour les combinaisons de runtime et de gestionnaire de paquets.
- Le comportement de PATH et du gestionnaire de version est toujours principalement gardé par les docs et les tests utilitaires.

## Preuves

### Docs

- `docs/install/index.md`
- `docs/install/installer.md`
- `docs/install/node.md`
- `docs/install/updating.md`

### Source

- `src/entry.ts`
- `src/entry.version-fast-path.ts`
- `src/version.ts`
- `src/bootstrap/node-extra-ca-certs.ts`
- `src/cli/update-cli/shared.ts`
- `src/cli/install-spec.ts`
- `src/infra/install-target.ts`

### Tests d'intégration

- Aucun trouvé pour l'exécution de script d'installation publié ou la configuration de runtime multi-gestionnaire de paquets.

### Tests unitaires

- `src/entry.test.ts`
- `src/entry.respawn.test.ts`
- `src/version.test.ts`
- `src/bootstrap/node-extra-ca-certs.test.ts`
- `src/infra/detect-package-manager.test.ts`
- `src/infra/install-target.test.ts`

### Commandes de validation de surface

- `none declared in taxonomy`: `pass` - La surface CLI ne déclare pas de commandes de validation supplémentaires pour la notation.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "install.ps1 install.sh npm pnpm bun openclaw install" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`
- `gitcrawl search issues "install.sh install.ps1 local prefix npm pnpm bun" -R openclaw/openclaw --state closed --json number,title,url,state --limit 5`
- `gitcrawl search issues "Node version package manager pnpm bun npm runtime openclaw" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`
- `gitcrawl search issues "node 24 pnpm bun install docs" -R openclaw/openclaw --state closed --json number,title,url,state --limit 5`

Résultats :

- `[]`
- `[]`
- `[]`
- `[]`

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "install.ps1 openclaw install"`
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "Node pnpm bun npm openclaw"`

Résultats :

- Les conseils de fil d'aide récents pointent les utilisateurs vers `powershell -c "irm https://openclaw.ai/install.ps1 | iex"` et le flux d'installation du site.
- Les résultats d'archive Discord d'avril incluent le travail de docs pour clarifier le support d'installation Bun et que Node reste le runtime de passerelle recommandé.
