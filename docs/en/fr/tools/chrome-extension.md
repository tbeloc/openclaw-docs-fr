---
summary: "Extension Chrome : laissez OpenClaw piloter votre onglet Chrome existant"
read_when:
  - You want the agent to drive an existing Chrome tab (toolbar button)
  - You need remote Gateway + local browser automation via Tailscale
  - You want to understand the security implications of browser takeover
title: "Extension Chrome"
---

# Extension Chrome (relais de navigateur)

L'extension Chrome OpenClaw permet à l'agent de contrôler vos **onglets Chrome existants** (votre fenêtre Chrome normale) au lieu de lancer un profil Chrome séparé géré par openclaw.

L'attachement/détachement se fait via un **seul bouton de la barre d'outils Chrome**.

Si vous préférez le flux d'attachement MCP officiel de Chrome au lieu du relais d'extension OpenClaw, utilisez plutôt un profil de navigateur `existing-session`. Voir [Browser](/tools/browser#chrome-existing-session-via-mcp). Pour la documentation officielle de Chrome, voir [Chrome for Developers: Use Chrome DevTools MCP with your browser session](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session) et le [Chrome DevTools MCP README](https://github.com/ChromeDevTools/chrome-devtools-mcp).

## Qu'est-ce que c'est (concept)

Il y a trois parties :

- **Service de contrôle du navigateur** (Gateway ou nœud) : l'API que l'agent/outil appelle (via la Gateway)
- **Serveur relais local** (loopback CDP) : fait le lien entre le serveur de contrôle et l'extension (`http://127.0.0.1:18792` par défaut)
- **Extension MV3 Chrome** : s'attache à l'onglet actif en utilisant `chrome.debugger` et achemine les messages CDP vers le relais

OpenClaw contrôle ensuite l'onglet attaché via la surface d'outil `browser` normale (en sélectionnant le bon profil).

## Installation / chargement (non empaqueté)

1. Installez l'extension dans un chemin local stable :

```bash
openclaw browser extension install
```

2. Affichez le chemin du répertoire d'extension installé :

```bash
openclaw browser extension path
```

3. Chrome → `chrome://extensions`

- Activez le « Mode développeur »
- « Charger l'extension non empaquetée » → sélectionnez le répertoire affiché ci-dessus

4. Épinglez l'extension.

## Mises à jour (pas d'étape de compilation)

L'extension est fournie dans la version OpenClaw (package npm) sous forme de fichiers statiques. Il n'y a pas d'étape de « compilation » séparée.

Après la mise à niveau d'OpenClaw :

- Réexécutez `openclaw browser extension install` pour actualiser les fichiers installés dans votre répertoire d'état OpenClaw.
- Chrome → `chrome://extensions` → cliquez sur « Recharger » sur l'extension.

## L'utiliser (définir le jeton de la Gateway une fois)

Pour utiliser le relais d'extension, créez un profil de navigateur pour celui-ci :

Avant le premier attachement, ouvrez les Options de l'extension et définissez :

- `Port` (par défaut `18792`)
- `Gateway token` (doit correspondre à `gateway.auth.token` / `OPENCLAW_GATEWAY_TOKEN`)

Ensuite, créez un profil :

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

Utilisez-le :

- CLI : `openclaw browser --browser-profile my-chrome tabs`
- Outil d'agent : `browser` avec `profile="my-chrome"`

### Ports de Gateway personnalisés

Si vous utilisez un port de gateway personnalisé, le port du relais d'extension est automatiquement dérivé :

**Port du relais d'extension = Port de la Gateway + 3**

Exemple : si `gateway.port: 19001`, alors :

- Port du relais d'extension : `19004` (gateway + 3)

Configurez l'extension pour utiliser le port du relais dérivé dans la page Options de l'extension.

## Attachement / détachement (bouton de la barre d'outils)

- Ouvrez l'onglet que vous voulez qu'OpenClaw contrôle.
- Cliquez sur l'icône de l'extension.
  - Le badge affiche `ON` lorsqu'il est attaché.
- Cliquez à nouveau pour détacher.

## Quel onglet contrôle-t-il ?

- Il ne contrôle **pas** automatiquement « l'onglet que vous regardez ».
- Il contrôle **uniquement les onglets que vous avez explicitement attachés** en cliquant sur le bouton de la barre d'outils.
- Pour basculer : ouvrez l'autre onglet et cliquez sur l'icône de l'extension là-bas.

## Badge + erreurs courantes

- `ON` : attaché ; OpenClaw peut piloter cet onglet.
- `…` : connexion au relais local.
- `!` : relais non accessible/authentifié (plus courant : serveur relais non exécuté, ou jeton de gateway manquant/incorrect).

Si vous voyez `!` :

- Assurez-vous que la Gateway s'exécute localement (configuration par défaut), ou exécutez un hôte de nœud sur cette machine si la Gateway s'exécute ailleurs.
- Ouvrez la page Options de l'extension ; elle valide l'accessibilité du relais + l'authentification du jeton de gateway.

## Gateway distante (utiliser un hôte de nœud)

### Gateway locale (même machine que Chrome) — généralement **aucune étape supplémentaire**

Si la Gateway s'exécute sur la même machine que Chrome, elle démarre le service de contrôle du navigateur sur loopback et démarre automatiquement le serveur relais. L'extension communique avec le relais local ; les appels CLI/outil vont à la Gateway.

### Gateway distante (Gateway s'exécute ailleurs) — **exécuter un hôte de nœud**

Si votre Gateway s'exécute sur une autre machine, démarrez un hôte de nœud sur la machine qui exécute Chrome. La Gateway proxiera les actions du navigateur vers ce nœud ; l'extension + le relais restent locaux à la machine du navigateur.

Si plusieurs nœuds sont connectés, épinglez-en un avec `gateway.nodes.browser.node` ou définissez `gateway.nodes.browser.mode`.

## Sandboxing (conteneurs d'outils)

Si votre session d'agent est en sandbox (`agents.defaults.sandbox.mode != "off"`), l'outil `browser` peut être restreint :

- Par défaut, les sessions en sandbox ciblent souvent le **navigateur sandbox** (`target="sandbox"`), pas votre Chrome hôte.
- La prise de contrôle du relais d'extension Chrome nécessite de contrôler le **serveur de contrôle du navigateur hôte**.

Options :

- Le plus simple : utilisez l'extension à partir d'une session/agent **non sandboxée**.
- Ou autorisez le contrôle du navigateur hôte pour les sessions sandboxées :

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

Ensuite, assurez-vous que l'outil n'est pas refusé par la politique d'outil, et (si nécessaire) appelez `browser` avec `target="host"`.

Débogage : `openclaw sandbox explain`

## Conseils d'accès à distance

- Gardez la Gateway et l'hôte de nœud sur le même tailnet ; évitez d'exposer les ports du relais au LAN ou à Internet public.
- Appairez les nœuds intentionnellement ; désactivez le routage du proxy du navigateur si vous ne voulez pas de contrôle à distance (`gateway.nodes.browser.mode="off"`).
- Laissez le relais sur loopback sauf si vous avez un vrai besoin inter-namespace. Pour WSL2 ou des configurations similaires de partage d'hôte, définissez `browser.relayBindHost` sur une adresse de liaison explicite telle que `0.0.0.0`, puis gardez l'accès restreint avec l'authentification de la Gateway, l'appairage des nœuds et un réseau privé.

## Comment fonctionne le « chemin d'extension »

`openclaw browser extension path` affiche le répertoire **installé** sur disque contenant les fichiers d'extension.

La CLI n'affiche intentionnellement **pas** un chemin `node_modules`. Exécutez toujours `openclaw browser extension install` d'abord pour copier l'extension vers un emplacement stable dans votre répertoire d'état OpenClaw.

Si vous déplacez ou supprimez ce répertoire d'installation, Chrome marquera l'extension comme cassée jusqu'à ce que vous la rechargiez à partir d'un chemin valide.

## Implications de sécurité (lisez ceci)

C'est puissant et risqué. Traitez-le comme si vous donniez au modèle « les mains sur votre navigateur ».

- L'extension utilise l'API du débogueur de Chrome (`chrome.debugger`). Lorsqu'elle est attachée, le modèle peut :
  - cliquer/taper/naviguer dans cet onglet
  - lire le contenu de la page
  - accéder à tout ce que la session connectée de l'onglet peut accéder
- **Ce n'est pas isolé** comme le profil dédié géré par openclaw.
  - Si vous attachez à votre profil/onglet de tous les jours, vous accordez l'accès à cet état de compte.

Recommandations :

- Préférez un profil Chrome dédié (séparé de votre navigation personnelle) pour l'utilisation du relais d'extension.
- Gardez la Gateway et tous les hôtes de nœud tailnet uniquement ; fiez-vous à l'authentification de la Gateway + l'appairage des nœuds.
- Évitez d'exposer les ports du relais sur LAN (`0.0.0.0`) et évitez Funnel (public).
- Le relais bloque les origines non-extension et nécessite l'authentification du jeton de gateway pour `/cdp` et `/extension`.

Connexes :

- Aperçu de l'outil Browser : [Browser](/tools/browser)
- Audit de sécurité : [Security](/gateway/security)
- Configuration Tailscale : [Tailscale](/gateway/tailscale)
