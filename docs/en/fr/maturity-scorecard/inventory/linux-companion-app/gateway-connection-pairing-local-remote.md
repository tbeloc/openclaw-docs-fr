---
title: "Application compagne Linux - Note de maturité de connectivité Gateway"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Linux - Note de maturité de connectivité Gateway

## Résumé

La connexion Gateway sous-jacente, l'appairage du navigateur, l'accès distant SSH/Tailscale et les chemins du service Gateway systemd Linux sont bien documentés, mais ils ne sont pas assemblés en une application compagne Linux native prise en charge. Les preuves des PR ouvertes et Discord montrent un travail en cours en mode distant Linux, tandis que la source actuelle n'a toujours pas de client d'application native Linux.

## Portée de la catégorie

Inclus dans cette catégorie :

- Attachement et statut Gateway local : comportement d'attachement, de démarrage et de statut Gateway local à partir d'une application Linux.
- Appairage et authentification Gateway : authentification Gateway et appairage d'appareil à partir d'un client Linux natif.
- Mode distant : mode distant via URL directe, tunnel SSH ou Tailscale
- Limites des ressources locales et distantes : limites des ressources locales et distantes pour un client compagne Linux.

## Fonctionnalités

- Attachement et statut Gateway local : comportement d'attachement, de démarrage et de statut Gateway local à partir d'une application Linux.
- Appairage et authentification Gateway : authentification Gateway et appairage d'appareil à partir d'un client Linux natif.
- Mode distant : mode distant via URL directe, tunnel SSH ou Tailscale
- Limites des ressources locales et distantes : limites des ressources locales et distantes pour un client compagne Linux.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (8%)`
- Signaux positifs : l'authentification Gateway, l'appairage, le service systemd Linux, l'interface de contrôle et le mode distant macOS ont une documentation actuelle et une couverture d'exécution adjacente.
- Signaux négatifs : aucune application compagne Linux enregistrée n'implémente la connexion native, l'appairage, le mode local ou le mode distant.
- Lacunes d'intégration : aucun test de fumée de connexion/appairage/mode-distant natif Linux n'existe dans l'arborescence source actuelle.

## Score de qualité

- Score : `Expérimental (35%)`
- Rapports Gitcrawl : la recherche directe `Linux companion gateway pairing remote local mode` a retourné uniquement une PR de suivi large non liée ; les problèmes #75 et PR #59859/#61576 contiennent des revendications de connexion d'application Linux ouvertes.
- Rapports Discrawl : les commentaires du problème #75 incluent une étape importante du mode de connexion distante compagne Linux, mais aucune preuve de version prise en charge.
- Bonnes qualités : le modèle Gateway et d'authentification du navigateur sous-jacent est suffisamment mature pour qu'une future application Linux le réutilise.
- Mauvaises qualités : la documentation n'indique pas comment une application Linux native doit gérer l'URL distante directe, le cycle de vie du tunnel SSH, l'identité Tailscale, l'accès aux ressources locales ou la persistance de l'identité de l'appareil.
- Exclus de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Expérimental (8%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'attachement et le statut Gateway local, l'appairage et l'authentification Gateway, le mode distant, les limites des ressources locales et distantes.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Définir si l'application Linux démarre une Gateway locale, s'attache uniquement ou reflète la division locale/distante macOS.
- Définir le transport distant UX et le repli de ressource locale pour un client Linux natif.
- Ajouter une documentation native Linux pour l'appairage, l'authentification, la reconnexion, le jeton obsolète et le mode distant.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:36` : l'installation du service Gateway Linux est pilotée par CLI via `openclaw onboard --install-daemon`, `openclaw gateway install` ou `openclaw configure`.
- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:64` : la configuration du service utilisateur systemd Linux est documentée.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:34` : la première connexion de l'interface de contrôle du navigateur nécessite généralement l'approbation de l'appairage de l'appareil.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:61` : les connexions du navigateur en boucle locale sont approuvées automatiquement tandis que les profils Tailnet/LAN/navigateur ont un comportement d'appairage explicite.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md:24` : les modes local et distant compagne macOS sont documentés ; Linux n'a pas de page native équivalente.

### Source

- Aucune source de client Gateway `apps/linux` ou mode distant au niveau de l'application n'existe dans l'extraction actuelle.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw` : macOS a une source de connexion Gateway et de tunnel distant ; c'est une référence adjacente, pas une source d'application Linux.
- `src/gateway` et `docs/web/control-ui.md` prennent en charge l'accès navigateur/Gateway indépendamment d'une application native Linux.

### Tests d'intégration

- Aucun test d'intégration de connexion, d'appairage ou de mode distant d'application native Linux n'a été trouvé.
- Les tests Gateway et interface de contrôle existants couvrent la surface de protocole sous-jacente, pas un client d'application Linux.

### Tests unitaires

- Aucune cible de test unitaire de connexion ou d'appairage d'application Linux n'a été trouvée.
- Les tests OpenClawKit partagés adjacents couvrent le support client mobile/macOS, pas la source native Linux.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Linux companion gateway pairing remote local mode" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "Linux Windows Clawdbot Apps issue 75" --mode keyword --limit 8 --json`
- `gitcrawl gh pr view 59859 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`
- `gitcrawl gh pr view 61576 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`

Résultats :

- La requête gateway/pairing/remote a retourné uniquement la PR de suivi large non liée #74163, pas un résultat compagne Linux atterri.
- La requête du problème #75 a retourné des preuves de suivi d'application Linux/Windows larges.
- La PR #59859 revendique l'intégration systemd, le sondage de santé HTTP, la connexion WebSocket authentifiée et la gestion des ressources local-vs-distant, mais reste ouverte.
- La PR #61576 revendique un client WebSocket Gateway typé et une identité d'appareil avec signature de défi ed25519, mais reste ouverte et précoce.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux companion gateway pairing remote local mode"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux Windows Clawdbot Apps issue 75"`

Résultats :

- La requête gateway/pairing/remote n'a retourné aucun résultat direct.
- La requête du problème #75 a retourné un commentaire du 25 avril indiquant qu'une étape importante du mode de connexion distante compagne Linux était en cours de déploiement dans une piste de contributeur, incluant l'URL de passerelle distante directe, la passerelle distante transférée localement SSH, l'analyse, la validation, la normalisation et la propagation du statut.
