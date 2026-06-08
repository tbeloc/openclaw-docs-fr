---
title: "Native Windows - Networking Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Native Windows - Networking Maturity Note

## Résumé

La mise en réseau des hôtes Windows est documentée, mais c'est la partie la plus mince de cette surface. Les documents expliquent la mise en réseau virtuelle WSL2, le `netsh portproxy` Windows, les règles de pare-feu et les URL de passerelle accessibles. La couverture des sources provient principalement de la logique partagée de mise en réseau/statut de la passerelle plutôt que de flux de bout en bout spécifiques à Windows. Les preuves d'archive montrent que portproxy et la connectivité des nœuds WSL2-to-Windows restent confuses pour les opérateurs.

## Portée de la catégorie

Inclus dans cette catégorie :

- Liaison native de l'hôte Windows : comportement de liaison native de l'hôte Windows et exposition de la passerelle.
- netsh interface portproxy : netsh interface portproxy, règles du pare-feu Windows et actualisation IP WSL
- Statut de la passerelle et sortie de sonde : statut de la passerelle et sortie de sonde qui aident les opérateurs à vérifier la mise en réseau Windows.
- Loopback, LAN et limite WSL : limites entre les modes d'exposition loopback, LAN et WSL.

## Fonctionnalités

- Mise en réseau native de l'hôte Windows : comportement de liaison native de l'hôte Windows et exposition de la passerelle.
- netsh interface portproxy : netsh interface portproxy, règles du pare-feu Windows et actualisation IP WSL
- Statut de la passerelle et sortie de sonde : statut de la passerelle et sortie de sonde qui aident les opérateurs à vérifier la mise en réseau Windows.
- Loopback, LAN et limite WSL : limites entre les modes d'exposition loopback, LAN et WSL.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (58%)`
- Signaux positifs : les documents fournissent des commandes concrètes WSL2 portproxy et pare-feu ; la documentation de la passerelle couvre les modes de liaison, les gardes d'authentification, Tailscale, SSH et les commandes de statut/sonde ; la source inclut la logique partagée de mise en réseau/statut/sonde de la passerelle.
- Signaux négatifs : la preuve spécifique à Windows est principalement de la documentation et des rapports de support plutôt que des tests de scénario.
- Lacunes d'intégration : aucune preuve en direct n'a été trouvée pour l'accessibilité de la passerelle WSL2 depuis les hôtes de nœuds Windows natifs, les clients LAN via portproxy, la configuration des règles de pare-feu, l'actualisation de portproxy après le redémarrage de WSL ou l'appairage de nœuds distants sur ce chemin.

## Score de qualité

- Score : `Alpha (56%)`
- Rapports Gitcrawl : les requêtes WSL/portproxy ont retourné un signal de problème/PR selon lequel le `portproxy` Windows peut se casser silencieusement et que l'accessibilité de la passerelle nécessite une documentation plus claire sur les configurations WSL/VM/Tailscale.
- Rapports Discrawl : les threads de support WSL2 décrivent les hôtes de nœuds Windows qui ne parviennent pas à se connecter à une passerelle WSL2 même après les tentatives de portproxy, tunnel SSH et proxy de confiance.
- Bonnes qualités : la documentation ne cache pas le problème de mise en réseau virtuelle et fournit des commandes exécutables pour la redirection de ports et l'accès au pare-feu.
- Mauvaises qualités : les opérateurs doivent raisonner sur plusieurs espaces d'adressage et modes de sécurité ; la piste de support montre que la documentation actuelle ne suffit pas pour rendre les configurations de nœuds Windows/WSL mixtes prévisibles.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et flux d'exécution sont enregistrées uniquement sous Couverture et Preuves.

## Score de complétude

- Score : `Alpha (58%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-cli-and-gateway.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la mise en réseau native de l'hôte Windows, netsh interface portproxy, statut de la passerelle et sortie de sonde, Loopback, LAN et limite WSL.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario de réseau Windows/WSL2 couvrant la passerelle dans WSL2, l'hôte de nœud sur Windows, l'actualisation de portproxy, la règle de pare-feu, la sortie de statut et la connexion de nœud réussie.
- Ajouter des commandes de diagnostic qui indiquent à l'utilisateur si une URL de passerelle est accessible à partir des clients Windows natifs par rapport à seulement depuis l'intérieur de WSL2.

## Preuves

### Documents

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:138` explique que WSL a son propre réseau virtuel et peut nécessiter une redirection de port Windows.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:155` fournit la commande `netsh interface portproxy add`.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:159` fournit la règle du pare-feu Windows.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:176` clarifie que les nœuds distants ont besoin d'une URL de passerelle accessible, pas `127.0.0.1`.
- `/Users/kevinlin/code/openclaw/docs/gateway/index.md:111` documente la précédence du port et de la liaison de la passerelle.
- `/Users/kevinlin/code/openclaw/docs/cli/gateway.md:139` documente l'interrogation d'une passerelle en cours d'exécution sur WebSocket RPC.

### Source

- `/Users/kevinlin/code/openclaw/src/commands/gateway-status.ts:38` implémente le sondage de statut.
- `/Users/kevinlin/code/openclaw/src/commands/gateway-status/helpers.ts` résout les cibles de statut de la passerelle et les indices de réseau.
- `/Users/kevinlin/code/openclaw/src/gateway/net.ts` implémente les aides de mise en réseau de la passerelle, y compris les cas spécifiques à Windows.
- `/Users/kevinlin/code/openclaw/src/shared/gateway-bind-url.ts` gère la résolution de l'URL de liaison de la passerelle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/gateway-network-docker.sh` exerce le comportement partagé de mise en réseau de la passerelle dans Docker.
- `/Users/kevinlin/code/openclaw/test/scripts/gateway-network-client.test.ts` couvre le harnais du client de mise en réseau de la passerelle.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/gateway/net.test.ts` couvre le comportement de mise en réseau de la passerelle, y compris les branches de plateforme Windows.
- `/Users/kevinlin/code/openclaw/src/shared/gateway-bind-url.test.ts` couvre la résolution de l'URL de liaison.
- `/Users/kevinlin/code/openclaw/src/commands/status.gateway-connection.test.ts` couvre la messagerie de connexion de statut de la passerelle.
- `/Users/kevinlin/code/openclaw/src/gateway/server-discovery.test.ts` couvre le comportement de découverte de la passerelle.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows portproxy gateway remote access WSL" --mode keyword --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "WSL2 Windows gateway systemd portproxy" --mode keyword --limit 5 --json`

Résultats :

- Les deux requêtes ont retourné la PR #74163 avec des références de problèmes de plateforme Windows, y compris `portproxy v4tov4 breaks silently` et des rapports de déconnexion de passerelle Windows.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "Windows portproxy gateway remote access WSL"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 4 "WSL2 Windows gateway systemd portproxy"`

Résultats :

- La requête portproxy Windows n'a retourné aucun résultat direct.
- La requête WSL2 a retourné des rapports de support sur le besoin de portproxy/mise en réseau en miroir et un thread où un hôte de nœud Windows ne pouvait pas se connecter de manière fiable à une passerelle s'exécutant dans WSL2 malgré les tentatives de portproxy et tunnel SSH.
