---
summary: "Référence CLI pour le provisionnement et la gestion de cellules OpenClaw isolées par locataire"
read_when:
  - You host multiple tenant trust domains on one machine
  - You need to create, inspect, upgrade, or remove fleet cells
title: "Fleet"
---

# `openclaw fleet`

`openclaw fleet` gère des instances OpenClaw complètes appelées **cells**. Chaque cell possède sa propre Gateway, son état, ses credentials, ses comptes de canal, son conteneur et son port hôte loopback uniquement. Utilisez une cell pour chaque limite de confiance de locataire ; n'utilisez pas une Gateway partagée comme limite multi-locataire hostile.

Fleet est **expérimental**. Les noms de commandes, les drapeaux, les formes de sortie et le profil de conteneur peuvent changer entre les versions sans fenêtre de dépréciation pendant que la surface se stabilise.

Fleet supporte Docker et Podman. L'image par défaut est `ghcr.io/openclaw/openclaw:latest`.

## Démarrage rapide

```bash
openclaw fleet create acme
openclaw fleet status acme
openclaw fleet list
```

`fleet create` affiche le jeton Gateway généré une seule fois avec l'URL de la cell. Stockez le jeton immédiatement, puis configurez les comptes de canal de chaque locataire à l'intérieur de la cell de ce locataire.

## IDs de locataire

Les IDs de locataire doivent correspondre à :

```text
^[a-z0-9](?:[a-z0-9-]{0,38}[a-z0-9])?$
```

Cela permet 1 à 40 lettres minuscules, chiffres et tirets internes. Un ID doit commencer et se terminer par une lettre ou un chiffre. Les lettres majuscules, les traits de soulignement, les barres obliques, les points, les espaces et les chaînes de traversée telles que `../acme` sont rejetés.

L'ID devient partie du nom du conteneur : `openclaw-cell-<tenant>`.

## `fleet create`

Créer une cell et la démarrer :

```bash
openclaw fleet create acme
```

Créer une cell Podman sur un port fixe sans la démarrer :

```bash
openclaw fleet create acme \
  --runtime podman \
  --port 19125 \
  --no-start
```

Passez des variables d'environnement spécifiques au locataire en répétant `--env` :

```bash
openclaw fleet create acme \
  --env TZ=America/Los_Angeles \
  --env OPENCLAW_DISABLE_BONJOUR=1
```

Les clés d'environnement utilisent des lettres, des chiffres et des traits de soulignement et ne peuvent pas commencer par un chiffre. Les valeurs doivent être sur une seule ligne car Fleet les transmet via un fichier d'environnement d'exécution protégé. Fleet rejette les tentatives de remplacement des variables de chemin de conteneur gérées et de jeton Gateway listées sous [Stockage et disposition du conteneur](#storage-and-container-layout).

### Options de création

| Option                    | Par défaut                            | Description                                                                                    |
| ------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `--image <ref>`           | `ghcr.io/openclaw/openclaw:latest`    | Image de conteneur pour la cell.                                                               |
| `--runtime <runtime>`     | `docker`                              | CLI de conteneur : `docker` ou `podman`.                                                       |
| `--port <number>`         | Alloué automatiquement à partir de `19100`  | Port hôte loopback. Un port explicitement sélectionné ne doit pas appartenir à une autre cell enregistrée.    |
| `--memory <value>`        | `2g`                                  | Limite de mémoire du conteneur en syntaxe Docker/Podman.                                       |
| `--cpus <value>`          | `2`                                   | Limite CPU du conteneur.                                                                       |
| `--pids-limit <number>`   | `512`                                 | Nombre maximum de processus dans le conteneur.                                                 |
| `--env <KEY=VALUE>`       | Aucun                                 | Passer une variable d'environnement à la cell. Répétez pour plusieurs valeurs.                 |
| `--gateway-token <value>` | Jeton hexadécimal aléatoire de 32 caractères | Utiliser un jeton Gateway fourni au lieu d'en générer un. Voir [Gestion des jetons](#token-handling). |
| `--no-start`              | La cell démarre                       | Créer le conteneur sans le démarrer.                                                           |
| `--json`                  | Sortie lisible par l'homme            | Imprimer la sortie lisible par machine.                                                        |

L'allocation automatique sélectionne le premier port de registre inutilisé à partir de `19100` ou au-dessus. Fleet rejette les IDs de locataire en double et les ports explicites déjà assignés à une autre cell.

Les références d'image sont passées comme un argument de conteneur-runtime. Les références vides et les valeurs commençant par `-` sont rejetées afin qu'une image ne puisse pas être interprétée comme une option Docker ou Podman.

Le point de terminaison Docker ou Podman sélectionné doit être local. Fleet rejette les contextes Docker distants, les points de terminaison `DOCKER_HOST` et les services Podman distants avant de réserver un port ou de créer un état local ; les hôtes de cell distants nécessitent un contrat de stockage et de point de terminaison séparé et sont reportés de ce MVP.

Le résultat de création inclut l'ID de locataire, le nom du conteneur, le port hôte, le jeton Gateway et l'URL locale. Même en sortie JSON, traitez le résultat comme porteur de secret car il contient le jeton.

## `fleet list`

Lister les cells dans l'ordre des IDs de locataire :

```bash
openclaw fleet list
openclaw fleet ls
openclaw fleet list --json
```

Le tableau contient :

| Colonne   | Signification                                                                                                                                                                                                                                                                         |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tenant`  | ID de locataire.                                                                                                                                                                                                                                                                      |
| `state`   | État du conteneur en direct à partir de l'inspection Docker ou Podman. `unknown` signifie que le runtime était indisponible, ou qu'un conteneur avec le nom de la cell existe mais ses étiquettes de propriété Fleet ne correspondent pas à l'enregistrement du registre (une collision ou un signal de falsification — inspectez-le manuellement avant d'agir). |
| `port`    | Port hôte loopback mappé à la Gateway de la cell.                                                                                                                                                                                                                                      |
| `image`   | Image de conteneur enregistrée.                                                                                                                                                                                                                                                       |
| `created` | Heure de création de la cell.                                                                                                                                                                                                                                                         |

Les lignes du registre restent visibles quand Docker ou Podman est indisponible ; seul l'état en direct devient `unknown`.

## `fleet status`

Inspecter une cell :

```bash
openclaw fleet status acme
openclaw fleet status acme --json
```

Le statut combine la ligne du registre fleet, l'inspection du conteneur en direct et une courte demande au meilleur effort à :

```text
http://127.0.0.1:<host-port>/healthz
```

Le résultat de santé est `ok`, `failed` ou `skipped`. `/healthz` prouve la vivacité de la Gateway, pas la pleine disponibilité de chaque canal ou plugin configuré. La sonde est ignorée quand il n'y a pas de point de terminaison local utilisable à vérifier.

## `fleet start`, `fleet stop` et `fleet restart`

Contrôler une cell existante avec son runtime enregistré :

```bash
openclaw fleet start acme
openclaw fleet stop acme
openclaw fleet restart acme
```

Ces commandes opèrent sur le nom du conteneur enregistré. Elles échouent si le locataire est inconnu ou si le runtime enregistré ne peut pas effectuer l'opération.

## `fleet upgrade`

Re-tirer l'image enregistrée et remplacer le conteneur de la cell :

```bash
openclaw fleet upgrade acme
```

Déplacer la cell vers une autre image :

```bash
openclaw fleet upgrade acme --image ghcr.io/openclaw/openclaw:<version>
```

La mise à niveau tire l'image cible, inspecte le conteneur existant et le réseau par cell, arrête et supprime le conteneur, puis le recrée et le démarre. Le remplacement préserve le même port hôte, les répertoires de données, le réseau de pont par cell, le profil d'exécution, les limites de ressources, la politique de redémarrage, l'environnement géré par Fleet et les valeurs initialement fournies avec `--env`. L'état monté survit au remplacement du conteneur ; l'environnement par défaut de l'image peut changer avec l'image cible.

Le remplacement n'est validé qu'après que sa Gateway répond à `/healthz` sur le port loopback de la cell, correspondant au contrat de santé que le fichier compose officiel utilise. Un remplacement qui se termine, boucle en crash ou ne devient pas sain dans environ une minute est supprimé et le conteneur précédent est restauré, donc une image cassée ne désactive pas une cell fonctionnelle.

Le jeton Gateway n'est intentionnellement pas stocké dans le registre fleet. Avant de supprimer l'ancien conteneur, Fleet lit son environnement et porte `OPENCLAW_GATEWAY_TOKEN` dans le remplacement. Ne supprimez pas manuellement l'ancien conteneur avant une mise à niveau si le jeton n'existe nulle part ailleurs que vous contrôlez.

## `fleet rm`

Supprimer une cell arrêtée du runtime et du registre tout en conservant les données du locataire :

```bash
openclaw fleet rm acme
```

Un conteneur en cours d'exécution nécessite `--force` :

```bash
openclaw fleet rm acme --force
```

Supprimer définitivement les données de la cell également :

```bash
openclaw fleet rm acme --purge-data --force
```

Fleet supprime le conteneur de la cell avant de supprimer son réseau de pont dédié. `--purge-data` nécessite `--force`. Avant la suppression récursive, Fleet résout les deux racines détenues par Fleet et les deux répertoires par locataire. Chaque cible doit être la feuille de locataire exactement attendue, strictement à l'intérieur de sa racine et non un lien symbolique. Ces vérifications de confinement empêchent un chemin de registre corrompu ou un lien symbolique inter-locataire de rediriger la suppression ailleurs.

La purge est réessayable quand un répertoire de locataire exactement attendu est déjà absent. Cela permet à une invocation ultérieure de terminer le nettoyage après une défaillance partielle du système de fichiers sans assouplir les vérifications de chemin pour les répertoires qui existent toujours.

## Disposition du stockage et des conteneurs

L'état des cellules et les clés de chiffrement des profils d'authentification utilisent des chemins d'hôte distincts par locataire sous le répertoire d'état OpenClaw actif :

```text
<state-dir>/fleet/cells/<tenant>/
<state-dir>/fleet/auth-profile-secrets/<tenant>/
```

Le premier répertoire est monté à `/home/node/.openclaw`. Le second est monté à `/home/node/.config/openclaw`, correspondant au montage de la clé de chiffrement de la configuration Docker officielle. La clé de chiffrement n'est donc pas exposée sous le montage d'état ordinaire et n'est pas incluse lors d'une sauvegarde ou d'un partage du répertoire d'état des cellules uniquement. Les deux répertoires survivent à la suppression et à la mise à niveau normales ; `fleet rm --purge-data --force` supprime les deux après des vérifications de confinement distinctes.

Avant le premier démarrage, Fleet initialise la configuration de la cellule avec `gateway.mode=local`, l'authentification par jeton, la liaison du conteneur LAN et les origines de l'interface utilisateur de contrôle pour le port d'hôte alloué. La valeur du jeton n'est pas écrite dans cette configuration ; elle reste dans l'environnement du conteneur.

Fleet épingle les chemins de conteneur de l'image officielle avec ces valeurs d'environnement :

| Variable                 | Valeur du conteneur                  |
| ------------------------ | ------------------------------------ |
| `HOME`                   | `/home/node`                         |
| `OPENCLAW_HOME`          | `/home/node`                         |
| `OPENCLAW_STATE_DIR`     | `/home/node/.openclaw`               |
| `OPENCLAW_CONFIG_PATH`   | `/home/node/.openclaw/openclaw.json` |
| `OPENCLAW_WORKSPACE_DIR` | `/home/node/.openclaw/workspace`     |
| `OPENCLAW_GATEWAY_TOKEN` | Jeton de cellule généré ou fourni    |

L'image officielle utilise par défaut l'utilisateur non-root `node` avec l'UID 1000. Fleet maintient les montages de liaison privés `0700` accessibles en écriture sans les rendre accessibles au monde. Docker rootful exécute la cellule avec l'UID et le GID non-root de l'appelant ; Docker rootless utilise l'UID de conteneur 0, qui correspond à l'utilisateur d'hôte non-privilégié de l'appelant à l'intérieur de l'espace de noms utilisateur du démon. Podman utilise `keep-id` avec l'UID et le GID de l'appelant. Lorsque Fleet lui-même s'exécute en tant que root par rapport à un runtime rootful, il conserve l'utilisateur de l'image et assigne les fichiers de montage initiaux à l'UID/GID 1000.

Sur les hôtes SELinux, les montages Docker et Podman reçoivent une réétiquetage privé `:Z`. Si vous restaurez ou relocalisez les données de cellule, gardez les chemins montés en liaison accessibles en écriture par l'utilisateur de conteneur effectif. Le profil est compatible avec rootless, mais Docker ou Podman doit déjà être configuré pour l'opération rootless sur l'hôte ; Fleet ne convertit pas un démon rootful en un démon rootless.

## Profil de sécurité

Fleet applique le profil suivant à chaque cellule :

| Contrôle             | Profil appliqué                                      | Raison                                                                                                                      |
| -------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Capacités Linux      | `--cap-drop=ALL`                                     | La passerelle est un processus Node.js et n'a besoin d'aucune capacité Linux supplémentaire.                                |
| Escalade de privilèges | `--security-opt no-new-privileges`                   | Empêche les processus de gagner des privilèges via des binaires setuid ou setgid.                                           |
| Processus init       | `--init`                                             | Récolte les processus descendants et transfère les signaux du cycle de vie du conteneur.                                    |
| Limite de processus  | `--pids-limit 512` par défaut                        | Limite le fork et l'épuisement des processus.                                                                               |
| Limite de mémoire    | `--memory 2g` par défaut                             | Limite l'utilisation de la mémoire de la cellule.                                                                           |
| Limite CPU           | `--cpus 2` par défaut                                | Limite l'utilisation du CPU de la cellule.                                                                                  |
| Politique de redémarrage | `--restart unless-stopped`                           | Redémarre une cellule défaillante sans remplacer un arrêt intentionnel.                                                     |
| Publication d'hôte   | `127.0.0.1:<host-port>:18789` uniquement             | Garde la passerelle hors des interfaces d'hôte génériques.                                                                  |
| Réseau de cellule    | Un pont défini par l'utilisateur par cellule        | Empêche le trafic direct entre les adresses IP des conteneurs tout en conservant l'accès NAT sortant.                      |
| Identité du conteneur | Mappage utilisateur correspondant à l'hôte           | Garde les montages de liaison privés accessibles en écriture sans accorder l'accès au monde.                                |
| État persistant      | Montages par cellule ; aucun montage d'état partagé  | Garde la configuration du locataire, les identifiants, les sessions et les espaces de travail dans l'arborescence de données de ce locataire. |
| Commande du conteneur | `node dist/index.js gateway --bind lan --port 18789` | Écoute sur le réseau du conteneur pour que le mappage de port d'hôte en boucle locale puisse l'atteindre.                 |

Fleet ne monte jamais `/var/run/docker.sock`, n'utilise pas `--privileged` ou le réseau d'hôte, et n'ajoute pas de capacités. Le pont par cellule est une limite de séparation entre cellules, pas un pare-feu sortant : les cellules conservent l'accès réseau sortant nécessaire pour les fournisseurs et les canaux. Placez le port de boucle locale devant un proxy, un tunnel SSH ou une configuration tailnet qui correspond à votre déploiement. `http://127.0.0.1:<port>` n'est directement accessible que depuis l'hôte Fleet.

Ce profil sépare les conteneurs de locataires, mais il ne protège pas les locataires de l'opérateur Fleet, de l'administrateur du runtime de conteneur ou d'un hôte compromis. Consultez [Hébergement multi-locataire](/fr/gateway/multi-tenant-hosting) pour le modèle de confiance complet et les options d'isolation plus fortes.

## Gestion des jetons

Par défaut, `fleet create` génère un jeton de passerelle hexadécimal aléatoire cryptographiquement sécurisé de 32 caractères et l'affiche une seule fois dans le résultat de création. Stockez-le dans votre gestionnaire de secrets approuvé et évitez de capturer la sortie de création dans les journaux.

`--gateway-token` place un jeton personnalisé dans les arguments du processus local, qui peuvent être conservés dans l'historique du shell ou visibles dans les listes de processus. Préférez le jeton généré sauf si un flux de gestion des secrets existant nécessite une valeur fournie.

Le jeton et chaque valeur passée avec `--env` vivent dans l'environnement du conteneur. Fleet les écrit dans un fichier d'environnement de mode `0600` de courte durée, transmet uniquement le chemin de ce fichier à Docker ou Podman, et le supprime après la fin de la commande du runtime. Les valeurs explicitement tapées dans `openclaw fleet create --gateway-token ...` ou `--env KEY=VALUE` peuvent toujours être visibles dans les arguments du processus `openclaw` externe et l'historique du shell.

Les valeurs d'environnement du conteneur ne sont pas cachées de l'opérateur d'hôte de confiance : les administrateurs Docker ou Podman peuvent les lire avec l'inspection du conteneur. La note « affichée une seule fois » de Fleet décrit la sortie CLI normale, pas la résistance à un administrateur d'hôte.

## Connexes

- [Hébergement multi-locataire](/fr/gateway/multi-tenant-hosting)
- [Docker](/fr/install/docker)
- [Podman](/fr/install/podman)
- [Sécurité de la passerelle](/fr/gateway/security)
