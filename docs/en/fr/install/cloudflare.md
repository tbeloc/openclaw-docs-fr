---
summary: "Déploiement expérimental de Cloudflare Worker et Container avec sauvegardes Litestream vers R2"
title: "Cloudflare Containers"
read_when:
  - You want to run OpenClaw on Cloudflare Containers
  - You are evaluating R2-backed SQLite recovery on ephemeral containers
  - You need to choose between webhook scale-to-zero and always-on channels
---

Exécutez une installation OpenClaw derrière un Cloudflare Worker et un Durable Object nommé, avec l'image OpenClaw officielle et la réplication Litestream vers R2.

<Warning>
  Cette cible de déploiement est expérimentale. Litestream protège les bases de données SQLite, pas le répertoire d'état complet d'OpenClaw. Lisez [Limites et récupération](#limites-et-récupération) avant d'utiliser des identifiants de production.
</Warning>

## Ce dont vous avez besoin

- Un compte Cloudflare avec Workers, Containers et R2 disponibles
- Docker Buildx avec support `linux/amd64`
- Un référentiel Docker Hub public pour l'image dérivée
- Node.js et npm
- Les identifiants de fournisseur et de canal pour votre configuration OpenClaw

Le modèle se trouve dans [`scripts/cloudflare`](https://github.com/openclaw/openclaw/tree/main/scripts/cloudflare). Il déploie un Container `standard-2` avec `max_instances: 1`.

## Comment ça fonctionne

Le Worker transfère chaque requête HTTP et WebSocket vers un nom Durable Object stable. Ce Durable Object possède une instance Container et est la barrière d'écrivain unique autour du réplica Litestream. Le Container expose OpenClaw sur le port `8080` ; `/startupz` est sa vérification de disponibilité du trafic.

Litestream surveille les deux racines SQLite :

- `/home/node/.openclaw/state/*.sqlite`
- `/home/node/.openclaw/agents/**/*.sqlite`

Au démarrage, le point d'entrée utilise l'API R2 S3 `ListObjectsV2` comme manifeste de restauration, rejette les chemins en dehors de ces racines, restaure chaque base de données découverte, et ne démarre la Gateway qu'ensuite.

## Déployer

<Steps>
  <Step title="Préparer le modèle">
    Clonez OpenClaw et entrez dans le répertoire du modèle :

    ```bash
    git clone https://github.com/openclaw/openclaw.git
    cd openclaw/scripts/cloudflare
    npm install
    npx wrangler login
    npx wrangler whoami
    ```

    Confirmez que Wrangler a sélectionné le compte Cloudflare prévu avant de créer des ressources.

  </Step>

  <Step title="Créer le stockage R2">
    Créez le bucket :

    ```bash
    npx wrangler r2 bucket create openclaw-backups
    ```

    Dans le tableau de bord Cloudflare, créez un jeton API R2 avec accès en lecture/écriture aux objets limité à ce bucket. Gardez l'ID de clé d'accès et la clé d'accès secrète en dehors du checkout.

    Dans `wrangler.jsonc`, remplacez `<account-id>` dans le point de terminaison. Si vous utilisez un autre nom de bucket, mettez à jour à la fois `LITESTREAM_BUCKET` et `r2_buckets[].bucket_name`.

    La liaison R2 est pour l'accès côté Worker et la complétude de la documentation. Litestream ne peut pas utiliser une liaison Worker depuis l'intérieur du Container ; il utilise le point de terminaison S3 de R2 et les identifiants transmis via les secrets du Worker.

  </Step>

  <Step title="Publier l'image Container">
    Remplacez `<official-openclaw-image-digest>` dans `Dockerfile` par un digest immuable du référentiel Docker Hub officiel [`openclaw/openclaw`](https://hub.docker.com/r/openclaw/openclaw).

    Construisez l'image dérivée pour l'architecture requise par Cloudflare et poussez-la vers un référentiel Docker Hub public :

    ```bash
    docker buildx build \
      --platform linux/amd64 \
      --tag docker.io/<docker-hub-user>/openclaw-cloudflare:<version> \
      --push \
      .
    docker buildx imagetools inspect \
      docker.io/<docker-hub-user>/openclaw-cloudflare:<version>
    ```

    Remplacez l'espace réservé `containers[].image` dans `wrangler.jsonc` par la référence immuable `docker.io/...@sha256:...` résultante. Cloudflare Containers peut extraire les images Docker Hub publiques directement ; GHCR n'est pas une source prise en charge pour ce modèle.

  </Step>

  <Step title="Déployer le Worker et le Container">
    Compilez le Worker et déployez-le :

    ```bash
    npm run check
    npm run deploy
    ```

    Le premier déploiement crée le Worker, la classe Durable Object sauvegardée par SQLite, l'application Container et la liaison R2.

  </Step>

  <Step title="Définir les secrets d'exécution">
    Ajoutez les identifiants R2 et Gateway via l'invite de secret de Wrangler :

    ```bash
    npx wrangler secret put LITESTREAM_ACCESS_KEY_ID
    npx wrangler secret put LITESTREAM_SECRET_ACCESS_KEY
    npx wrangler secret put OPENCLAW_GATEWAY_TOKEN
    ```

    Ajoutez les variables de fournisseur et de canal selon les besoins. Par exemple :

    ```bash
    npx wrangler secret put OPENAI_API_KEY
    npx wrangler secret put TELEGRAM_BOT_TOKEN
    ```

    `src/container.ts` transmet une liste d'autorisation explicite de variables d'environnement au Container. Ajoutez un autre nom là avant d'utiliser un identifiant différent sauvegardé par l'environnement.

  </Step>

  <Step title="Initialiser OpenClaw">
    Le premier démarrage nécessite une session interactive à l'intérieur du Container. L'accès SSH est désactivé par défaut ; activez-le temporairement en ajoutant ceci à l'entrée du container dans `wrangler.jsonc`, puis redéployez :

    ```jsonc
    "ssh": { "enabled": true }
    ```

    Ouvrez l'URL du Worker déployé une fois pour démarrer l'instance. Ensuite, localisez les ID d'application et d'instance et connectez-vous :

    ```bash
    npx wrangler containers list
    npx wrangler containers instances <application-id> --json
    npx wrangler containers ssh <instance-id>
    ```

    SSH est médiatisé par wrangler et limité aux comptes avec accès en écriture aux containers. Après l'initialisation, vous pouvez supprimer le bloc `ssh` et redéployer ; l'état restauré survit au remplacement via Litestream.

    À l'intérieur du Container, exécutez une configuration basée sur SecretRef. Cet exemple utilise OpenAI et Telegram :

    ```bash
    cd /app
    node openclaw.mjs onboard --non-interactive --accept-risk --skip-health \
      --mode local \
      --auth-choice openai-api-key \
      --secret-input-mode ref \
      --gateway-auth token \
      --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN \
      --skip-channels \
      --no-install-daemon
    node openclaw.mjs channels add --channel telegram --use-env
    node openclaw.mjs doctor --json
    ```

    Conservez votre recette d'initialisation exacte dans un runbook privé et reproductible. Un disque Container frais ne conserve pas la configuration générée.

  </Step>
</Steps>

## Choisir le mode de cycle de vie

`OPENCLAW_WEBHOOK_ONLY` est par défaut `false`, ce qui maintient le Container en cours d'exécution pendant les périodes d'inactivité. Conservez cette valeur par défaut pour les canaux qui maintiennent des sockets ou des processus de longue durée, notamment :

- Discord
- Slack Socket Mode
- WhatsApp

Définissez `OPENCLAW_WEBHOOK_ONLY` à `true` uniquement lorsque chaque canal activé reçoit du trafic via des webhooks HTTP. Dans ce mode, le Container s'arrête après dix minutes d'inactivité et démarre à froid à la prochaine requête.

<Warning>
  La mise à l'échelle à zéro commence par un disque frais. Activez-la uniquement lorsqu'un processus externe peut réappliquer votre initialisation déclarative. Litestream restaure SQLite mais ne peut pas recréer `openclaw.json`, les fichiers d'identifiants, les plugins installés ou les espaces de travail.
</Warning>

## Limites et récupération

- **Écrivain unique :** chaque requête résout le même nom Durable Object, et Cloudflare exécute une instance Durable Object active pour ce nom. N'augmentez pas `max_instances` ou n'introduisez pas de routage alternatif autour de cette barrière. Un bref chevauchement ancien/nouveau Container lors d'un remplacement de plateforme ou d'un déploiement est un compromis expérimental accepté.
- **Point de récupération :** l'intervalle de synchronisation Litestream d'une seconde produit normalement un RPO à l'échelle des secondes. Ce n'est pas une réplication synchrone, et une terminaison abrupte peut perdre les écritures qui n'ont pas atteint R2.
- **Disque éphémère :** chaque veille, remplacement ou redémarrage d'hôte commence par l'image plus les bases de données SQLite restaurées. Utilisez les [archives OpenClaw complètes](/fr/install/backups#full-archives) pour la configuration, les fichiers d'identifiants, les fichiers de plugins et les espaces de travail.
- **Restauration :** les octets de base de données plus anciens sont un voyage dans le temps. L'augmentation des identifiants de canal, en particulier WhatsApp, peut désynchroniser ; l'état d'approbation et de livraison/dédupliquage se restaure également. Reliez les canaux affectés et examinez les approbations en attente avant de reprendre. Voir [Restaurer](/fr/install/backups#restore).
- **WebSockets :** le proxying Worker et Container prend en charge les WebSockets. Cloudflare limite chaque message WebSocket reçu à 32 MiB.
- **Sortie :** les requêtes sortantes utilisent l'espace IP Cloudflare partagé. Cette cible ne fournit pas d'adresse de sortie fixe.
- **Limite du fournisseur :** c'est un modèle de déploiement, pas un fournisseur OpenClaw `cloudWorkers`. L'accès SSH de son opérateur n'implémente pas le contrat d'exécution SSH de ce fournisseur.

## Mettre à jour

Construisez une nouvelle image dérivée à partir d'un nouveau digest OpenClaw officiel immuable, poussez-la, mettez à jour le digest dérivé dans `wrangler.jsonc` et déployez :

```bash
npm run check
npm run deploy
```

Testez les mises à jour et les restaurations par rapport à un bucket R2 séparé en premier. Préservez l'état actuel avant d'activer les octets plus anciens.

## Connexes

- [Sauvegardes](/fr/install/backups)
- [Docker](/fr/install/docker)
- [Sécurité de la Gateway](/fr/gateway/security)
- [Gestion des secrets](/fr/gateway/secrets)
