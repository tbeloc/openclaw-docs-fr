---
summary: "Héberger plusieurs domaines de confiance de locataires en tant que cellule OpenClaw Gateway isolée par locataire"
read_when:
  - You are hosting OpenClaw for multiple users or organizations
  - You need to choose an isolation boundary for tenant workloads
title: "Hébergement multi-locataire"
---

# Hébergement multi-locataire

Le modèle de sécurité par défaut d'OpenClaw est une limite d'opérateur de confiance par Gateway, et non une isolation multi-locataire hostile au sein d'une Gateway partagée unique. L'hébergement d'utilisateurs ou d'organisations qui ne partagent pas une limite de confiance signifie donc l'exécution d'une instance OpenClaw complète et séparée pour chaque locataire.

`openclaw fleet` appelle chaque instance isolée une **cellule**. Une cellule est une Gateway complète dans un conteneur renforcé avec son propre état, ses identifiants, son espace de travail, ses comptes de canal, son jeton et son port d'hôte en boucle locale uniquement.

Fleet est **expérimental** : ses commandes, ses drapeaux et son profil de conteneur peuvent changer entre les versions sans fenêtre de dépréciation pendant que la surface se stabilise.

## Pourquoi chaque locataire a besoin d'une cellule

Un opérateur authentifié au sein d'une Gateway a un rôle de plan de contrôle de confiance. Les ID de session sélectionnent le routage ; ils n'autorisent pas un locataire par rapport à un autre. L'isolation des agents peut réduire l'effet du contenu non fiable et de l'exécution d'outils, mais elle ne transforme pas une Gateway partagée unique en limite d'autorisation de locataire.

Utilisez une cellule par locataire afin que chaque domaine de confiance ait un processus Gateway séparé, un conteneur, un arbre d'état persistant et une identité Gateway. Cela suit le [modèle de sécurité Gateway](/fr/gateway/security) : ne co-localisez pas les utilisateurs mutuellement non fiables dans un processus OpenClaw unique ou un utilisateur OS unique.

## Architecture

La CLI Fleet est un superviseur de cycle de vie côté hôte. Elle enregistre les cellules dans la base de données d'état OpenClaw et demande à un runtime Docker ou Podman local de créer, inspecter, démarrer, arrêter, remplacer et supprimer leurs conteneurs. Les points de terminaison de runtime distants sont rejetés car les chemins de liaison et les URL de boucle locale de Fleet appartiennent à l'hôte local ; les hôtes de cellules distantes sont reportés jusqu'à ce qu'ils aient un contrat de stockage et de point de terminaison explicite. Fleet ne fait pas de proxy des messages de locataire et n'ajoute pas de chemin de données partagé au niveau de l'application entre les cellules.

Chaque cellule exécute l'image officielle `ghcr.io/openclaw/openclaw` sur son propre réseau de pont défini par l'utilisateur. Les ponts séparés empêchent le trafic IP direct entre les conteneurs tout en conservant l'accès NAT sortant pour les fournisseurs et les canaux. Ce n'est pas un pare-feu de sortie ; appliquez une politique de réseau d'hôte ou de runtime lorsqu'un locataire a besoin de restrictions de sortie. La Gateway de cellule écoute sur le port `18789` à l'intérieur du conteneur, tandis que le runtime le publie uniquement sur `127.0.0.1:<allocated-port>` sur l'hôte. Un opérateur peut placer un proxy inverse approuvé, un tunnel SSH ou un tailnet devant ce point de terminaison de boucle locale lorsqu'un accès distant est nécessaire.

L'état persistant de Gateway provient de `<state-dir>/fleet/cells/<tenant>/` et est monté sur `/home/node/.openclaw`. Les clés de chiffrement du profil d'authentification proviennent du chemin d'hôte séparé `<state-dir>/fleet/auth-profile-secrets/<tenant>/` et sont montées sur `/home/node/.config/openclaw`, correspondant à la [disposition de persistance Docker](/fr/install/docker#storage-and-persistence) officielle. La clé n'est pas imbriquée sous le montage d'état ordinaire. Les comptes de canal par locataire se terminent à l'intérieur de la cellule qui les possède, il n'y a donc pas de compte de canal partagé ou de routeur de messages entrants partagé dans le MVP Fleet.

L'image officielle utilise par défaut l'utilisateur non-root `node` avec UID 1000. Fleet utilise des mappages d'utilisateurs compatibles avec l'hôte afin que les montages de liaison privés restent accessibles en écriture : Podman utilise `keep-id`, Docker rootful utilise l'identité non-root appelante, et Docker rootless mappe la racine du conteneur à l'utilisateur du démon non privilégié. Docker et Podman appliquent une réétiquette `:Z` privée lorsque SELinux d'hôte est actif. Le profil de conteneur évite les fonctionnalités d'hôte privilégiées et est convivial pour rootless, mais l'opération rootless est un choix et une condition préalable du runtime d'hôte, pas quelque chose que Fleet active automatiquement.

## Limite de confiance

La multi-location protège les locataires les uns des autres. L'opérateur Fleet et l'hôte sont de confiance pour chaque locataire. La résistance à un hôte compromis n'est pas un objectif.

Cela signifie qu'un administrateur d'hôte peut inspecter la configuration et l'environnement du conteneur, lire les données de cellule montées, remplacer les images ou entrer dans les conteneurs. Les jetons Gateway et les valeurs transmises avec `--env` sont visibles à un administrateur via l'inspection Docker ou Podman. Utilisez les contrôles d'hôte, la politique d'accès administratif, la surveillance, les sauvegardes et un gestionnaire de secrets approuvé en conséquence.

La ligne de base empêche l'exposition de réseau générique accidentelle et supprime les primitives d'escalade de conteneur courantes, mais elle ne rend pas un hôte non fiable sûr.

## Échelle d'isolation

Choisissez la limite qui correspond aux locataires que vous hébergez :

1. **Ligne de base de conteneur renforcé.** Fleet supprime toutes les capacités Linux, active `no-new-privileges`, applique des limites PID, mémoire et CPU, utilise des montages persistants et des réseaux de pont séparés, et publie uniquement sur la boucle locale d'hôte. C'est le profil MVP pour les locataires qui font confiance à l'opérateur et à l'hôte.
2. **Isolation de conteneur ou VM plus forte.** Pour les charges de travail à risque plus élevé, configurez Docker ou Podman pour utiliser un runtime d'isolation OCI plus fort tel que gVisor ou Kata Containers, ou placez les cellules dans des microVMs. C'est une configuration de runtime ou d'infrastructure ; l'option `--runtime docker|podman` de Fleet choisit la CLI de conteneur, pas le backend d'isolation OCI. Voir les [runtimes de conteneur alternatifs](https://docs.docker.com/engine/daemon/alternative-runtimes/) de Docker et le [guide de runtime Docker VM](/fr/install/docker-vm-runtime).
3. **Machines séparées pour les locataires hostiles.** Ne co-localisez pas les locataires hostiles dans un processus OpenClaw unique ou un utilisateur OS unique. Lorsque les locataires ne font pas confiance au même opérateur d'hôte ou ont besoin d'une limite administrative plus forte, utilisez des VMs ou des hôtes physiques séparés avec une administration de runtime séparée.

Aucun échelon de cette échelle ne change le modèle de confiance d'application OpenClaw : une Gateway reste un domaine d'opérateur de confiance unique.

## Démarrage rapide

Créez une cellule. La commande imprime un jeton Gateway généré une seule fois, alors stockez-le immédiatement :

```bash
openclaw fleet create acme
```

Ouvrez l'URL `http://127.0.0.1:<port>` signalée sur l'hôte Fleet, authentifiez-vous avec le jeton de ce locataire, et configurez les identifiants du fournisseur et les comptes de canal à l'intérieur de la cellule.

Vérifiez l'état du conteneur et la vivacité de Gateway :

```bash
openclaw fleet status acme
```

Mettez à niveau tout en préservant le port d'hôte, les données montées, le profil de ressource, l'environnement fourni par l'utilisateur et le jeton Gateway :

```bash
openclaw fleet upgrade acme
```

Supprimez le conteneur et la ligne de registre tout en conservant les données de locataire :

```bash
openclaw fleet rm acme --force
```

Pour supprimer également les données de locataire persistantes, ajoutez `--purge-data`. Purge nécessite `--force`, est irréversible et effectue une vérification de confinement de chemin résolu avant de supprimer quoi que ce soit :

```bash
openclaw fleet rm acme --purge-data --force
```

Voir la [référence CLI `openclaw fleet`](/fr/cli/fleet) pour chaque commande et option.

## Reporté du MVP

La première version de Fleet laisse délibérément ces surfaces à des conceptions ultérieures :

- Comptes de canal partagés ou routeur d'entrée partagé
- Processus d'hôte allégés par locataire au lieu d'instances OpenClaw complètes
- Hôtes de cellules distants gérés par un superviseur unique
- Un portail libre-service de locataire, un plan de facturation ou une interface utilisateur d'administration déléguée

Ces fonctionnalités nécessitent des contrats explicites d'identité, de routage, d'autorisation et de domaine de défaillance. Elles ne doivent pas être approximées en partageant une Gateway unique ou ses identifiants entre les locataires. Elles ne sont pas non plus la responsabilité de Fleet : Fleet reste un superviseur de cycle de vie à hôte unique, et les flottes multi-machines gouvernées par l'identité appartiennent à une couche de plan de contrôle dédiée au-dessus.

## Connexes

- [`openclaw fleet`](/fr/cli/fleet)
- [Sécurité Gateway](/fr/gateway/security)
- [Plusieurs gateways](/fr/gateway/multiple-gateways)
- [Docker](/fr/install/docker)
- [Podman](/fr/install/podman)
