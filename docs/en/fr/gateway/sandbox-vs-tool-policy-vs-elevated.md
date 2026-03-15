---
title: Sandbox vs Tool Policy vs Elevated
summary: "Pourquoi un outil est bloqué : runtime sandbox, politique d'autorisation/refus d'outil, et portes d'accès exec élevées"
read_when: "Vous avez rencontré une 'sandbox jail' ou un refus d'outil/élevé et voulez la clé de configuration exacte à modifier."
status: active
---

# Sandbox vs Tool Policy vs Elevated

OpenClaw dispose de trois contrôles connexes (mais différents) :

1. **Sandbox** (`agents.defaults.sandbox.*` / `agents.list[].sandbox.*`) décide **où les outils s'exécutent** (Docker vs hôte).
2. **Politique d'outil** (`tools.*`, `tools.sandbox.tools.*`, `agents.list[].tools.*`) décide **quels outils sont disponibles/autorisés**.
3. **Elevated** (`tools.elevated.*`, `agents.list[].tools.elevated.*`) est une **échappatoire exec uniquement** pour s'exécuter sur l'hôte quand vous êtes en sandbox.

## Débogage rapide

Utilisez l'inspecteur pour voir ce qu'OpenClaw fait _réellement_ :

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

Il affiche :

- le mode/portée/accès à l'espace de travail sandbox effectif
- si la session est actuellement en sandbox (main vs non-main)
- l'autorisation/refus d'outil sandbox effectif (et s'il provient d'agent/global/défaut)
- les portes élevées et les chemins de clés de correction

## Sandbox : où les outils s'exécutent

Le sandboxing est contrôlé par `agents.defaults.sandbox.mode` :

- `"off"` : tout s'exécute sur l'hôte.
- `"non-main"` : seules les sessions non-main sont en sandbox (surprise courante pour les groupes/canaux).
- `"all"` : tout est en sandbox.

Voir [Sandboxing](/fr/gateway/sandboxing) pour la matrice complète (portée, montages d'espace de travail, images).

### Montages de liaison (vérification de sécurité rapide)

- `docker.binds` _perce_ le système de fichiers sandbox : tout ce que vous montez est visible à l'intérieur du conteneur avec le mode que vous définissez (`:ro` ou `:rw`).
- La valeur par défaut est lecture-écriture si vous omettez le mode ; préférez `:ro` pour source/secrets.
- `scope: "shared"` ignore les montages par agent (seuls les montages globaux s'appliquent).
- Monter `/var/run/docker.sock` donne effectivement le contrôle de l'hôte au sandbox ; ne le faites que intentionnellement.
- L'accès à l'espace de travail (`workspaceAccess: "ro"`/`"rw"`) est indépendant des modes de montage.

## Politique d'outil : quels outils existent/sont appelables

Deux couches importent :

- **Profil d'outil** : `tools.profile` et `agents.list[].tools.profile` (liste d'autorisation de base)
- **Profil d'outil du fournisseur** : `tools.byProvider[provider].profile` et `agents.list[].tools.byProvider[provider].profile`
- **Politique d'outil globale/par agent** : `tools.allow`/`tools.deny` et `agents.list[].tools.allow`/`agents.list[].tools.deny`
- **Politique d'outil du fournisseur** : `tools.byProvider[provider].allow/deny` et `agents.list[].tools.byProvider[provider].allow/deny`
- **Politique d'outil sandbox** (s'applique uniquement en sandbox) : `tools.sandbox.tools.allow`/`tools.sandbox.tools.deny` et `agents.list[].tools.sandbox.tools.*`

Règles empiriques :

- `deny` gagne toujours.
- Si `allow` est non vide, tout le reste est traité comme bloqué.
- La politique d'outil est l'arrêt définitif : `/exec` ne peut pas contourner un outil `exec` refusé.
- `/exec` change uniquement les défauts de session pour les expéditeurs autorisés ; il n'accorde pas l'accès aux outils.
  Les clés d'outil du fournisseur acceptent soit `provider` (par ex. `google-antigravity`) soit `provider/model` (par ex. `openai/gpt-5.2`).

### Groupes d'outils (raccourcis)

Les politiques d'outil (globale, agent, sandbox) supportent les entrées `group:*` qui se développent en plusieurs outils :

```json5
{
  tools: {
    sandbox: {
      tools: {
        allow: ["group:runtime", "group:fs", "group:sessions", "group:memory"],
      },
    },
  },
}
```

Groupes disponibles :

- `group:runtime` : `exec`, `bash`, `process`
- `group:fs` : `read`, `write`, `edit`, `apply_patch`
- `group:sessions` : `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory` : `memory_search`, `memory_get`
- `group:ui` : `browser`, `canvas`
- `group:automation` : `cron`, `gateway`
- `group:messaging` : `message`
- `group:nodes` : `nodes`
- `group:openclaw` : tous les outils OpenClaw intégrés (exclut les plugins du fournisseur)

## Elevated : exec uniquement "exécuter sur l'hôte"

Elevated n'accorde **pas** d'outils supplémentaires ; il affecte uniquement `exec`.

- Si vous êtes en sandbox, `/elevated on` (ou `exec` avec `elevated: true`) s'exécute sur l'hôte (les approbations peuvent toujours s'appliquer).
- Utilisez `/elevated full` pour ignorer les approbations exec pour la session.
- Si vous exécutez déjà directement, elevated est effectivement un non-opération (toujours contrôlé).
- Elevated n'est **pas** limité à la compétence et ne **remplace pas** l'autorisation/refus d'outil.
- `/exec` est séparé de elevated. Il ajuste uniquement les défauts exec par session pour les expéditeurs autorisés.

Portes :

- Activation : `tools.elevated.enabled` (et optionnellement `agents.list[].tools.elevated.enabled`)
- Listes blanches d'expéditeurs : `tools.elevated.allowFrom.<provider>` (et optionnellement `agents.list[].tools.elevated.allowFrom.<provider>`)

Voir [Elevated Mode](/fr/tools/elevated).

## Corrections courantes de "sandbox jail"

### "Outil X bloqué par la politique d'outil sandbox"

Clés de correction (choisissez-en une) :

- Désactiver sandbox : `agents.defaults.sandbox.mode=off` (ou par agent `agents.list[].sandbox.mode=off`)
- Autoriser l'outil à l'intérieur du sandbox :
  - le supprimer de `tools.sandbox.tools.deny` (ou par agent `agents.list[].tools.sandbox.tools.deny`)
  - ou l'ajouter à `tools.sandbox.tools.allow` (ou par agent allow)

### "Je pensais que c'était main, pourquoi est-ce en sandbox ?"

En mode `"non-main"`, les clés de groupe/canal ne sont _pas_ main. Utilisez la clé de session main (affichée par `sandbox explain`) ou changez le mode en `"off"`.
