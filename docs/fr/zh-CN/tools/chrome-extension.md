```markdown
---
read_when:
  - 你希望智能体驱动现有的 Chrome 标签页（工具栏按钮）
  - 你需要通过 Tailscale 实现远程 Gateway 网关 + 本地浏览器自动化
  - 你想了解浏览器接管的安全影响
summary: Chrome 扩展：让 OpenClaw 驱动你现有的 Chrome 标签页
title: Chrome 扩展
x-i18n:
  generated_at: "2026-02-03T07:55:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3b77bdad7d3dab6adb76ff25b144412d6b54b915993b1c1f057f36dea149938b
  source_path: tools/chrome-extension.md
  workflow: 15
---

# Extension Chrome (relais de navigateur)

L'extension Chrome OpenClaw vous permet de contrôler vos **onglets Chrome existants** (votre fenêtre Chrome normale) au lieu de lancer un profil Chrome séparé géré par openclaw.

L'attachement/détachement se fait via un **bouton de barre d'outils Chrome séparé**.

## Qu'est-ce que c'est (concept)

Il y a trois parties :

- **Service de contrôle du navigateur** (Gateway ou nœud) : API appelée par l'agent/outil (via Gateway)
- **Serveur relais local** (loopback CDP) : établit un pont entre le serveur de contrôle et l'extension (par défaut `http://127.0.0.1:18792`)
- **Extension Chrome MV3** : s'attache à l'onglet actif avec `chrome.debugger` et transmet les messages CDP au relais

OpenClaw contrôle ensuite l'onglet attaché via l'interface d'outil `browser` normal (en sélectionnant le bon profil).

## Installation/chargement (non empaqueté)

1. Installez l'extension dans un chemin local stable :

```bash
openclaw browser extension install
```

2. Imprimez le chemin du répertoire de l'extension installée :

```bash
openclaw browser extension path
```

3. Chrome → `chrome://extensions`

- Activez le "Mode développeur"
- "Charger l'extension non empaquetée" → sélectionnez le répertoire imprimé ci-dessus

4. Épinglez l'extension.

## Mise à jour (sans étape de construction)

L'extension est incluse en tant que fichiers statiques dans la version OpenClaw (package npm). Il n'y a pas d'étape de "construction" séparée.

Après la mise à niveau d'OpenClaw :

- Réexécutez `openclaw browser extension install` pour actualiser les fichiers installés sous le répertoire d'état OpenClaw.
- Chrome → `chrome://extensions` → cliquez sur "Recharger" sur l'extension.

## L'utiliser (sans configuration supplémentaire)

OpenClaw est livré avec un profil de navigateur intégré appelé `chrome` qui pointe vers le relais d'extension sur le port par défaut.

Pour l'utiliser :

- CLI : `openclaw browser --browser-profile chrome tabs`
- Outil d'agent : `browser` avec `profile="chrome"`

Si vous voulez un nom différent ou un port relais différent, créez votre propre profil :

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

## Attachement/détachement (bouton de barre d'outils)

- Ouvrez l'onglet que vous souhaitez qu'OpenClaw contrôle.
- Cliquez sur l'icône de l'extension.
  - Le badge affiche `ON` lorsqu'il est attaché.
- Cliquez à nouveau pour détacher.

## Quel onglet contrôle-t-il ?

- Il **ne** contrôle **pas** automatiquement "n'importe quel onglet que vous regardez".
- Il contrôle **uniquement** les onglets que vous **attachez explicitement** en cliquant sur le bouton de barre d'outils.
- Pour basculer : ouvrez un autre onglet et cliquez sur l'icône de l'extension là-bas.

## Badge + erreurs courantes

- `ON` : attaché ; OpenClaw peut piloter cet onglet.
- `…` : connexion au relais local en cours.
- `!` : relais inaccessible (plus courant : le serveur relais du navigateur n'est pas en cours d'exécution sur cette machine).

Si vous voyez `!` :

- Assurez-vous que Gateway s'exécute localement (paramètre par défaut), ou si Gateway s'exécute ailleurs, exécutez un hôte nœud sur cette machine.
- Ouvrez la page d'options de l'extension ; elle affichera si le relais est accessible.

## Gateway distante (utilisation d'un hôte nœud)

### Gateway locale (avec Chrome sur la même machine) — généralement **aucune étape supplémentaire requise**

Si Gateway s'exécute sur la même machine que Chrome, il démarre le service de contrôle du navigateur sur loopback et lance automatiquement le serveur relais. L'extension communique avec le relais local ; les appels CLI/outil sont envoyés à Gateway.

### Gateway distante (Gateway s'exécute ailleurs) — **exécutez un hôte nœud**

Si votre Gateway s'exécute sur une autre machine, lancez un hôte nœud sur la machine exécutant Chrome. Gateway proxiera les opérations du navigateur vers ce nœud ; l'extension + relais restent locaux sur la machine du navigateur.

Si plusieurs nœuds sont connectés, utilisez `gateway.nodes.browser.node` pour en épingler un ou définissez `gateway.nodes.browser.mode`.

## Isolation sandbox (conteneur d'outils)

Si votre session d'agent s'exécute dans un sandbox (`agents.defaults.sandbox.mode != "off"`), l'outil `browser` peut être restreint :

- Par défaut, les sessions isolées par sandbox pointent généralement vers le **navigateur sandbox** (`target="sandbox"`), pas votre Chrome hôte.
- Le relais d'extension Chrome nécessite de contrôler le **serveur de contrôle du navigateur hôte**.

Options :

- Le plus simple : utilisez l'extension à partir d'une session/agent **non isolée par sandbox**.
- Ou autorisez le contrôle du navigateur hôte pour les sessions isolées par sandbox :

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

Assurez-vous ensuite que l'outil n'est pas rejeté par la politique d'outils et appelez `browser` avec `target="host"` si nécessaire.

Débogage : `openclaw sandbox explain`

## Conseils d'accès à distance

- Gardez Gateway et l'hôte nœud sur le même tailnet ; évitez d'exposer le port relais au LAN ou à Internet public.
- Appairez les nœuds intentionnellement ; si vous ne voulez pas de contrôle à distance, désactivez le routage du proxy du navigateur (`gateway.nodes.browser.mode="off"`).

## Comment fonctionne "extension path"

`openclaw browser extension path` imprime le répertoire disque **installé** contenant les fichiers d'extension.

Le CLI **ne** imprime intentionnellement **pas** le chemin `node_modules`. Exécutez toujours d'abord `openclaw browser extension install` pour copier l'extension vers un emplacement stable sous le répertoire d'état OpenClaw.

Si vous déplacez ou supprimez ce répertoire d'installation, Chrome marquera l'extension comme corrompue jusqu'à ce que vous la rechargiez à partir d'un chemin valide.

## Implications de sécurité (veuillez lire ceci)

C'est puissant et risqué. Considérez-le comme donnant au modèle "les mains libres sur votre navigateur".

- L'extension utilise l'API de débogage de Chrome (`chrome.debugger`). Lorsqu'elle est attachée, le modèle peut :
  - Cliquer/taper/naviguer dans cet onglet
  - Lire le contenu de la page
  - Accéder à tout ce que les sessions connectées de l'onglet peuvent accéder
- **Ce n'est pas comme** un profil dédié géré par openclaw.
  - Si vous attachez à votre profil/onglet d'utilisation quotidienne, vous accordez l'accès à l'état de ce compte.

Recommandations :

- Pour l'utilisation du relais d'extension, préférez un profil Chrome dédié (séparé de votre navigation personnelle).
- Gardez Gateway et tout hôte nœud sur tailnet uniquement ; dépendez de l'authentification Gateway + appairage de nœud.
- Évitez d'exposer le port relais sur LAN (`0.0.0.0`), évitez d'utiliser Funnel (public).
- Le relais bloque les sources non-extension et nécessite un jeton d'authentification interne du client CDP.

Connexes :

- Aperçu de l'outil navigateur : [Navigateur](/tools/browser)
- Audit de sécurité : [Sécurité](/gateway/security)
- Configuration Tailscale : [Tailscale](/gateway/tailscale)
```
