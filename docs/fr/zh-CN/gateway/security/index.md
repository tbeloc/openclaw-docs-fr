---
read_when:
  - Ajout de fonctionnalités élargissant les accès ou l'automatisation
summary: Considérations de sécurité et modèle de menace pour l'exécution d'une passerelle IA avec accès shell
title: Sécurité
x-i18n:
  generated_at: "2026-02-03T10:10:39Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: fedc7fabc4ecc486210cec646bf1e40cded6f0266867c4455a1998b7fd997f6b
  source_path: gateway/security/index.md
  workflow: 15
---

# Sécurité 🔒

## Vérification rapide : `openclaw security audit`

Voir aussi : [Vérification formelle (modèle de sécurité)](/security/formal-verification/)

Exécutez régulièrement cette commande (en particulier après avoir modifié la configuration ou exposé des interfaces réseau) :

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

Elle signale les failles de sécurité courantes (exposition de l'authentification de la passerelle, exposition du contrôle du navigateur, listes blanches d'escalade de privilèges, permissions du système de fichiers).

`--fix` applique les mesures de sécurité :

- Resserre `groupPolicy="open"` sur les canaux courants à `groupPolicy="allowlist"` (et variantes à compte unique).
- Restaure `logging.redactSensitive="off"` à `"tools"`.
- Resserre les permissions locales (`~/.openclaw` → `700`, fichiers de configuration → `600`, et fichiers d'état courants comme `credentials/*.json`, `agents/*/agent/auth-profiles.json` et `agents/*/sessions/sessions.json`).

Exécuter un agent IA avec accès shell sur votre machine est... _risqué_. Voici comment éviter d'être attaqué.

OpenClaw est à la fois un produit et une expérience : vous connectez le comportement de modèles de pointe à des plateformes de messagerie réelles et à des outils réels. **Il n'existe pas de configuration « parfaitement sécurisée ».** L'objectif est de réfléchir consciemment à :

- Qui peut discuter avec votre bot
- Où le bot est autorisé à exécuter des opérations
- Ce que le bot peut accéder

Commencez par l'accès minimal qui fonctionne, puis élargissez progressivement à mesure que votre confiance augmente.

### Ce que l'audit vérifie (aperçu de haut niveau)

- **Accès entrant** (politique de messages privés, politique de groupe, listes blanches) : les étrangers peuvent-ils déclencher le bot ?
- **Portée des outils** (outils d'escalade de privilèges + salons ouverts) : l'injection de prompt peut-elle se transformer en opérations shell/fichier/réseau ?
- **Exposition réseau** (liaison/authentification de la passerelle, Tailscale Serve/Funnel, jetons d'authentification faibles/courts).
- **Exposition du contrôle du navigateur** (nœuds distants, ports relais, points de terminaison CDP distants).
- **Hygiène du disque local** (permissions, liens symboliques, inclusions de configuration, chemins de « dossiers synchronisés »).
- **Plugins** (extensions présentes sans liste blanche explicite).
- **Hygiène du modèle** (avertissement lorsque le modèle configuré semble être une version antérieure ; ne bloque pas en dur).

Si vous exécutez `--deep`, OpenClaw tentera également de faire une sonde de passerelle en temps réel au mieux de ses efforts.

## Mappage du stockage des identifiants

À utiliser lors de l'audit des accès ou de la décision du contenu à sauvegarder :

- **WhatsApp** : `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- **Jetons de bot Telegram** : configuration/variables d'environnement ou `channels.telegram.tokenFile`
- **Jetons de bot Discord** : configuration/variables d'environnement (fichier de jeton pas encore supporté)
- **Jetons Slack** : configuration/variables d'environnement (`channels.slack.*`)
- **Listes blanches d'appairage** : `~/.openclaw/credentials/<channel>-allowFrom.json`
- **Configuration d'authentification du modèle** : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **Importation OAuth héritée** : `~/.openclaw/credentials/oauth.json`

## Liste de contrôle d'audit de sécurité

Lorsque vous auditez les résultats, traitez-les dans cet ordre de priorité :

1. **Tout « ouvert » + outils activés** : d'abord verrouiller les messages privés/groupes (appairage/listes blanches), puis resserrer la politique des outils/isolation en bac à sable.
2. **Exposition réseau publique** (liaison LAN, Funnel, authentification manquante) : corriger immédiatement.
3. **Exposition distante du contrôle du navigateur** : la traiter comme un accès opérateur (tailnet uniquement, nœuds appairés intentionnellement, éviter l'exposition publique).
4. **Permissions** : assurez-vous que les fichiers d'état/configuration/identifiants/authentification ne sont pas lisibles par le groupe/global.
5. **Plugins/Extensions** : charger uniquement le contenu en lequel vous avez confiance explicitement.
6. **Sélection du modèle** : pour tout bot avec outils, privilégier les modèles modernes et renforcés par instruction.

## Contrôle d'accès à l'interface utilisateur via HTTP

L'interface de contrôle nécessite un **contexte sécurisé** (HTTPS ou localhost) pour générer l'identité de l'appareil. Si vous activez `gateway.controlUi.allowInsecureAuth`, l'interface utilisateur revient à **authentification par jeton uniquement** et ignore l'appairage d'appareil lorsque l'identité de l'appareil est omise. C'est une dégradation de sécurité — privilégier HTTPS (Tailscale Serve) ou ouvrir l'interface utilisateur sur `127.0.0.1`.

Uniquement pour les urgences, `gateway.controlUi.dangerouslyDisableDeviceAuth` désactive complètement la vérification de l'identité de l'appareil. C'est une dégradation grave de la sécurité ; gardez-la désactivée sauf si vous déboguez activement et pouvez récupérer rapidement.

`openclaw security audit` émettra un avertissement lorsque ce paramètre est activé.

## Configuration du proxy inverse

Si vous exécutez la passerelle derrière un proxy inverse (nginx, Caddy, Traefik, etc.), vous devez configurer `gateway.trustedProxies` pour détecter correctement l'IP du client.

Lorsque la passerelle détecte des en-têtes de proxy (`X-Forwarded-For` ou `X-Real-IP`) à partir d'une adresse **non** dans `trustedProxies`, elle **ne** traitera pas la connexion comme un client local. Si l'authentification de la passerelle est désactivée, ces connexions seront rejetées. Cela empêche le contournement d'authentification où les connexions proxifiées semblerait provenir de localhost et obtiendraient une confiance automatique.

```yaml
gateway:
  trustedProxies:
    - "127.0.0.1" # si votre proxy s'exécute sur localhost
  auth:
    mode: password
    password: ${OPENCLAW_GATEWAY_PASSWORD}
```

Après avoir configuré `trustedProxies`, la passerelle utilisera l'en-tête `X-Forwarded-For` pour déterminer l'IP client réelle pour la détection de client local. Assurez-vous que votre proxy remplace (plutôt que d'ajouter) l'en-tête `X-Forwarded-For` entrant pour empêcher l'usurpation.

## Journaux de session locaux stockés sur le disque

OpenClaw stocke les journaux de session sur le disque sous `~/.openclaw/agents/<agentId>/sessions/*.jsonl`. Ceci est nécessaire pour la continuité de session et (optionnellement) l'indexation de la mémoire de session, mais cela signifie que **tout processus/utilisateur ayant accès au système de fichiers peut lire ces journaux**. Traitez l'accès au disque comme une limite de confiance et verrouillez les permissions de `~/.openclaw` (voir la section d'audit ci-dessous). Si vous avez besoin d'une isolation plus forte entre les agents, exécutez-les sous des utilisateurs du système d'exploitation séparés ou sur des hôtes séparés.

## Exécution de nœud (system.run)

Si un nœud macOS est appairé, la passerelle peut invoquer `system.run` sur ce nœud. C'est une **exécution de code à distance** sur Mac :

- Nécessite l'appairage du nœud (approbation + jeton).
- Contrôlé sur Mac via **Paramètres → Approbation Exec** (sécurité + demande + liste blanche).
- Si vous ne voulez pas d'exécution distante, définissez la sécurité sur **Refuser** et supprimez l'appairage du nœud pour ce Mac.

## Skills dynamiques (moniteur/nœuds distants)

OpenClaw peut actualiser la liste des Skills au cours d'une session :

- **Moniteur de Skills** : les modifications apportées à `SKILL.md` peuvent mettre à jour l'instantané des Skills au prochain tour de l'agent.
- **Nœuds distants** : la connexion d'un nœud macOS peut rendre disponibles les Skills macOS uniquement (basés sur la détection de bin).

Traitez le dossier Skills comme du **code de confiance** et limitez qui peut les modifier.

## Modèle de menace

Votre assistant IA peut :

- Exécuter des commandes shell arbitraires
- Lire et écrire des fichiers
- Accéder aux services réseau
- Envoyer des messages à n'importe qui (si vous lui donnez accès à WhatsApp)

Les personnes qui vous envoient des messages peuvent :

- Essayer de tromper votre IA pour qu'elle fasse du mal
- Ingénierie sociale pour obtenir l'accès à vos données
- Sonder les détails de l'infrastructure

## Concept fondamental : contrôle d'accès avant l'intelligence

La plupart des défaillances ici ne sont pas des exploits sophistiqués — c'est « quelqu'un a envoyé un message au bot, et le bot l'a fait ».

La position d'OpenClaw :

- **Identité d'abord :** décidez qui peut discuter avec le bot (appairage de messages privés/liste blanche/« ouvert » explicite).
- **Portée ensuite :** décidez où le bot est autorisé à exécuter des opérations (liste blanche de groupe + contrôle de mention, outils, isolation en bac à sable, permissions d'appareil).
- **Modèle en dernier :** supposez que le modèle peut être manipulé ; concevez pour que l'impact de la manipulation soit limité.

## Modèle d'autorisation des commandes

Les commandes slash et les instructions ne sont valides que pour les **expéditeurs autorisés**. L'autorisation provient de la liste blanche du canal/appairage plus `commands.useAccessGroups` (voir [Configuration](/gateway/configuration) et [Commandes slash](/tools/slash-commands)). Si la liste blanche du canal est vide ou contient `"*"`, les commandes sur ce canal sont effectivement ouvertes.

`/exec` est une fonction de commodité de session uniquement pour les opérateurs autorisés. Elle **ne** modifie pas la configuration ou ne change pas d'autres sessions.

## Plugins/Extensions

Les plugins s'exécutent **dans le même processus** que la passerelle. Traitez-les comme du code de confiance :

- Installez les plugins uniquement à partir de sources en lesquelles vous avez confiance.
- Privilégier une liste blanche explicite `plugins.allow`.
- Examinez la configuration du plugin avant de l'activer.
- Redémarrez la passerelle après les modifications de plugin.
- Si vous installez des plugins à partir de npm (`openclaw plugins install <npm-spec>`), traitez-le comme l'exécution de code non fiable :
  - Le chemin d'installation est `~/.openclaw/extensions/<pluginId>/` (ou `$OPENCLAW_STATE_DIR/extensions/<pluginId>/`).
  - OpenClaw utilise `npm pack` puis exécute `npm install --omit=dev` dans ce répertoire (les scripts de cycle de vie npm peuvent exécuter du code lors de l'installation).
  - Privilégier les versions exactes épinglées (`@scope/pkg@1.2.3`) et inspecter le code décompressé sur le disque avant d'activer.

Détails : [Plugins](/tools/plugin)

## Modèle d'accès aux messages privés (appairage/liste blanche/ouvert/désactivé)

Tous les canaux supportant actuellement les messages privés supportent la politique de messages privés (`dmPolicy` ou `*.dm.policy`), qui contrôle les messages privés entrants **avant** le traitement des messages :

- `pairing` (par défaut) : les expéditeurs inconnus reçoivent un code d'appairage court, et le bot ignore leurs messages jusqu'à approbation. Les codes d'appairage expirent après 1 heure ; les messages privés répétés ne renvoient pas le code d'appairage jusqu'à ce qu'une nouvelle demande soit créée. Les demandes en attente sont limitées par défaut à **3** par canal.
- `allowlist` : les expéditeurs inconnus sont bloqués (pas de poignée de main d'appairage).
- `open` : n'importe qui peut envoyer des messages privés (public). **Nécessite** que la liste blanche du canal contienne `"*"` (consentement explicite).
- `disabled` : ignorer complètement les messages privés entrants.

Approuver via CLI :

```bash
openclaw pairing list <channel>
openclaw pairing approve <channel> <code>
```

Détails + fichiers sur le disque : [Appairage](/channels/pairing)

## Isolation des sessions de messages privés (mode multi-utilisateur)

Par défaut, OpenClaw **achemine tous les messages privés vers la session principale** afin que votre assistant maintienne la continuité entre les appareils et les canaux. Si **plusieurs personnes** peuvent envoyer des messages privés au bot (messages privés ouverts ou liste blanche multi-utilisateurs), envisagez d'isoler les sessions de messages privés :

```json5
{
  session: { dmScope: "per-channel-peer" },
