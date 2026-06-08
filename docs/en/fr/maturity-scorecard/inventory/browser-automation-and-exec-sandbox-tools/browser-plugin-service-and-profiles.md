---
title: "Automatisation des navigateurs et outils exec/sandbox - Note de maturité du service de plugin de navigateur et des profils"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation des navigateurs et outils exec/sandbox - Note de maturité du service de plugin de navigateur et des profils

## Résumé

Le service de plugin de navigateur et les profils constituent un composant Stable. Le plugin fourni dispose de contrats de manifeste explicites, d'une enregistrement CLI et Gateway, d'un service de contrôle lazy, de CRUD de profils, d'une résolution de profils par défaut/openclaw/utilisateur/distant, et d'une couverture de rechargement à chaud. Le risque restant concerne la fragilité opérationnelle des profils autour des sessions Chrome existantes, du comportement des profils WSL/macOS, et de la disponibilité du CDP distant.

## Portée des catégories

Cette note couvre l'activation du plugin de navigateur fourni, l'enregistrement CLI du navigateur, le routage Gateway `browser.request`, le démarrage du service de contrôle, l'énumération des profils connus, la résolution du profil par défaut, la création/suppression de profils, les profils gérés localement, les profils `user`/session existante, les profils CDP attach-only et distants, et le rechargement à chaud des profils.

## Fonctionnalités

- Service de plugin de navigateur : Couvre le service de plugin de navigateur dans l'activation du plugin de navigateur fourni, l'enregistrement CLI du navigateur, le routage Gateway `browser.request`, le démarrage du service de contrôle, et le comportement associé du service de plugin de navigateur et des profils.
- Profils : Couvre les profils dans l'activation du plugin de navigateur fourni, l'enregistrement CLI du navigateur, le routage Gateway `browser.request`, le démarrage du service de contrôle, et le comportement associé du service de plugin de navigateur et des profils.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (86%)`
- Signaux positifs :
  - La documentation de configuration et de profils du navigateur couvre l'activation du plugin, les listes blanches d'outils, la sélection du profil par défaut, le comportement du profil openclaw/utilisateur, le CDP distant, et les commandes de cycle de vie.
  - L'enregistrement des sources est basé sur le manifeste et connecte l'outil, CLI, Gateway, proxy node-host, service de plugin, et surfaces d'audit de sécurité.
  - Les tests d'exécution couvrent le démarrage lazy du plugin, le routage des demandes de profil, le CRUD de profils, le nettoyage du cycle de vie, et le rechargement à chaud après les modifications de configuration.
  - L'instantané CDP du navigateur Docker E2E atteint une fixture Gateway/navigateur en direct et vérifie le docteur du navigateur, l'ouverture d'onglets, et les assertions d'instantané.
- Signaux négatifs :
  - Les flux de session existante et de profil utilisateur ont des bugs d'archive actuels autour du comportement macOS, WSL, et des délais d'expiration.
  - Les demandes MCP Chrome DevTools du navigateur distant se résolvent principalement en dehors du cœur de première partie, laissant une limite plus nette entre les profils CDP du cœur et le travail de l'écosystème de plugins.
- Lacunes d'intégration :
  - Ajouter une matrice E2E du cycle de vie des profils sur les profils gérés, utilisateur/session existante, CDP distant, attach-only, macOS, WSL, et Linux sans interface graphique.
  - Ajouter un scénario de routage de profil browser.request de porte de version qui exerce la sélection de profil à partir de la chaîne de requête et du corps.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl :
  - `browser plugin profiles browser.request openclaw browser command missing` a retourné la PR ouverte #81076 pour le remplissage du champ act de niveau supérieur, la PR ouverte #85993 étendant les capacités web MCP Chrome, et la PR ouverte #74411 pour les actions de téléchargement.
  - `browser profile` a retourné la PR ouverte #80143 pour honorer `cdpUrl` sur le profil par défaut de l'utilisateur, le problème #80036 pour le délai d'expiration MCP Chrome de session existante sur macOS, le problème #62288 pour l'attachement de session existante fragile, et le problème #43803 pour le routage de rechargement à chaud du profil de navigateur.
- Rapports Discrawl :
  - `browser profiles openclaw browser` a retourné des messages de version/archive autour des sondes d'état de session existante du navigateur, du travail du chemin de plugin MCP du navigateur distant, de la configuration du proxy, et des correctifs de délai d'expiration du navigateur géré.
- Bonnes qualités :
  - Le plugin est autonome et est activé par défaut via un contrat de manifeste clair.
  - La résolution des profils est centralisée, prend en charge les profils d'exécution connus, et actualise la configuration lors de la sélection/énumération des profils.
  - Le CRUD des profils valide les paramètres CDP du réseau distant/privé et évite de supprimer les données du navigateur distant ou de session existante.
  - Le démarrage lazy évite de démarrer le serveur de contrôle lors du démarrage de Gateway tout en prenant en charge le nettoyage d'exécution à la demande.
- Mauvaises qualités :
  - La surface du produit combine plusieurs modèles de profils avec un comportement différent : géré, session existante, attach-only, CDP distant, et proxy node-host.
  - Les utilisateurs peuvent observer un profil comme « prêt » alors que les outils de page ultérieurs expirent si la couche de navigateur/MCP Chrome/CDP externe est défaillante.
  - Le rechargement à chaud et la réconciliation des profils sont forts mais suffisamment subtils pour que l'état d'exécution obsolète reste un thème opérationnel actuel.
- Exclu de la qualité :
  - Les preuves des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution affectaient uniquement la couverture.

## Score de complétude

- Score : `Stable (86%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves archivées des docs, sources, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le service de plugin de navigateur, les profils.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le comportement du profil de session existante a besoin de plus de preuves multiplateforme et d'une taxonomie d'échec plus claire.
- Les voies de profil CDP distant et MCP Chrome ont besoin de diagnostics d'opérateur plus forts avant que ce composant ne soit considéré comme Lovable.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/tools/browser.md:10` : l'outil de navigateur utilise un profil isolé dédié par défaut et peut contrôler un profil Chrome existant via MCP Chrome.
- `/Users/kevinlin/code/openclaw/docs/tools/browser.md:21` : les fonctionnalités documentées incluent un profil séparé, un contrôle d'onglet déterministe, des actions, des instantanés, des captures d'écran, PDF, et un support multi-profil.
- `/Users/kevinlin/code/openclaw/docs/tools/browser.md:67` : la désactivation du plugin supprime les commandes CLI, la méthode Gateway, l'outil d'agent, et le service de contrôle.
- `/Users/kevinlin/code/openclaw/docs/tools/browser.md:119` : les docs distinguent le profil géré openclaw du profil de session existante de l'utilisateur.
- `/Users/kevinlin/code/openclaw/docs/tools/browser.md:138` : les docs décrivent les champs de configuration du navigateur et la configuration du profil.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-control.md:14` : l'API de contrôle du navigateur expose l'état, les onglets, l'ouverture, la mise au point, la fermeture, la capture d'écran, l'instantané, la console, les erreurs, les demandes, PDF, le corps de la réponse, et l'action.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-control.md:32` : le paramètre de requête de profil sélectionne le profil et l'authentification de loopback suit l'authentification de gateway.
- `/Users/kevinlin/code/openclaw/docs/tools/browser-control.md:125` : le service de contrôle est un serveur loopback interne soutenu par CDP/Playwright.

### Source

- `/Users/kevinlin/code/openclaw/extensions/browser/openclaw.plugin.json:1` : le manifeste du plugin de navigateur déclare l'id, l'activation par défaut, les hooks de démarrage/configuration, le contrat d'outil, les alias CLI, et les compétences.
- `/Users/kevinlin/code/openclaw/extensions/browser/register.runtime.ts:1` : l'exécution exporte l'outil de navigateur, le gestionnaire de demande Gateway, le proxy node-host, le service de plugin, et l'audit de sécurité.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server-context.ts:40` : les noms de profils connus sont fusionnés à partir de la configuration et de l'état d'exécution.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server-context.ts:51` : le contexte du profil câble le cycle de vie du profil, les opérations d'onglet, et la disponibilité.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server-context.ts:143` : la sélection du profil actualise la configuration et résout le profil par défaut/actuel.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server-context.ts:161` : l'énumération des profils inclut la disponibilité MCP Chrome et CDP.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/profiles-service.ts:48` : le service de profil valide et gère les opérations de liste/création/suppression de profils.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser-tool.ts:213` : la résolution de la cible de nœud du navigateur utilise les capacités, les commandes, et les nœuds connectés compatibles avec le navigateur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/browser-cdp-snapshot-docker.sh:84` : Docker E2E exécute le docteur du navigateur, ouvre la fixture, crée un instantané, et affirme le résultat.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/browser-cdp-snapshot/assert-snapshot.mjs:6` : l'assertion d'instantané vérifie le texte de la page, le lien de docs, l'URL, et les références iframe.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/browser-runtime.ts:111` : l'assistant d'exécution du navigateur QA exerce les flux `browser.request`, open, snapshot, et act.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/browser-runtime.ts:185` : l'assistant attend l'état activé/en cours d'exécution/CDP-prêt.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/browser/src/plugin-service.test.ts:54` : vérifie que le service de contrôle du navigateur ne démarre pas lors du démarrage de la gateway par défaut.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/plugin-service.test.ts:101` : vérifie que l'exécution du navigateur à la demande s'arrête même lorsque le démarrage était lazy.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server-context.hot-reload-profiles.test.ts:86` : vérifie que les nouveaux profils sont rechargés à chaud à partir de la configuration.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/server-context.hot-reload-profiles.test.ts:177` : vérifie que l'énumération des profils actualise la configuration avant d'énumérer les profils.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/browser/profiles-service.test.ts:204` : vérifie que les profils Chrome distants acceptent `cdpUrl`.
- `/Users/kevinlin/code/openclaw/extensions/browser/src/gateway/browser-request.profile-from-body.test.ts:95` : vérifie que `browser.request` peut utiliser le profil du corps de la demande.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "browser plugin profiles browser.request openclaw browser command missing" --json`

Résultats :

- PR ouverte #81076 : `fix(browser): backfill top-level act fields into nested request`.
- PR ouverte #85993 : `feat(browser): expand Chrome MCP web capabilities`.
- PR ouverte #74411 : `feat(browser): add agent download actions`.

Requête :

`gitcrawl search openclaw/openclaw --query "browser profile" --json`

Résultats :

- PR ouverte #80143 : `fix(browser): honor cdpUrl for user default profile`.
- Problème ouvert #80036 : MCP Chrome de session existante `profile=user` signale prêt mais les outils de page expirent sur macOS.
- Problème ouvert #62288 : l'attachement de session existante est fragile et a besoin d'un meilleur repli/diagnostics.
- Problème ouvert #43803 : le chemin de rechargement à chaud du profil de navigateur a toujours un risque de mode de rechargement.

### Requêtes Discrawl

Requête :

`discrawl search --mode fts --limit 5 "browser profiles openclaw browser"`

Résultats :

- Entrée d'archive des responsables/version du 2026-05-10 inclut l'extension de sonde d'état de session existante du navigateur.
- Les commentaires d'archive OpenClaw du 2026-04-26 discutent de la configuration du proxy du navigateur, du travail du chemin de plugin MCP du navigateur distant, et des correctifs de délai d'expiration du navigateur géré.
