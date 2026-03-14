---
read_when: Vous avez atteint la 'sandbox jail' ou voyez un refus d'outil/élevé et voulez la clé de configuration exacte à modifier.
status: active
summary: Raisons pour lesquelles les outils sont bloqués : runtime sandbox, politiques d'autorisation/refus d'outils et restrictions exec élevées
title: Sandbox vs Politique d'outils vs Élévation
x-i18n:
  generated_at: "2026-02-03T07:48:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 863ea5e6d137dfb61f12bd686b9557d6df1fd0c13ba5f15861bf72248bc975f1
  source_path: gateway/sandbox-vs-tool-policy-vs-elevated.md
  workflow: 15
---

# Sandbox vs Politique d'outils vs Élévation

OpenClaw dispose de trois contrôles connexes (mais distincts) :

1. **Sandbox** (`agents.defaults.sandbox.*` / `agents.list[].sandbox.*`) détermine **où les outils s'exécutent** (Docker vs hôte).
2. **Politique d'outils** (`tools.*`, `tools.sandbox.tools.*`, `agents.list[].tools.*`) détermine **quels outils sont disponibles/autorisés**.
3. **Élévation** (`tools.elevated.*`, `agents.list[].tools.elevated.*`) est un **canal d'échappement réservé à exec**, permettant l'exécution sur l'hôte lors de l'isolation sandbox.

## Débogage rapide

Utilisez l'inspecteur pour voir ce qu'OpenClaw *fait réellement* :

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

Il affichera :

- Le mode/portée/accès à l'espace de travail sandbox en vigueur
- Si la session actuelle est actuellement isolée en sandbox (main vs non-main)
- La politique d'autorisation/refus d'outils sandbox en vigueur (et d'où elle provient : agent/global/défaut)
- Les restrictions d'élévation et les chemins de clés de correction

## Sandbox : où les outils s'exécutent

L'isolation sandbox est contrôlée par `agents.defaults.sandbox.mode` :

- `"off"` : tout s'exécute sur l'hôte.
- `"non-main"` : seules les sessions non-main sont isolées en sandbox (courant pour les groupes/canaux "accidentels").
- `"all"` : tout est isolé en sandbox.

Voir [Isolation sandbox](/gateway/sandboxing) pour la matrice complète (portée, montages d'espace de travail, images).

### Montages liés (vérification de sécurité rapide)

- `docker.binds` *perce* le système de fichiers sandbox : tout ce que vous montez est visible dans le conteneur dans le mode que vous définissez (`:ro` ou `:rw`).
- Si le mode est omis, il est par défaut en lecture-écriture ; préférez `:ro` pour le code source/les clés.
- `scope: "shared"` ignore les montages par agent (seuls les montages globaux s'appliquent).
- Monter `/var/run/docker.sock` cède effectivement le contrôle de l'hôte au sandbox ; ne le faites que si c'est intentionnel.
- L'accès à l'espace de travail (`workspaceAccess: "ro"`/`"rw"`) est indépendant du mode de montage.

## Politique d'outils : quels outils existent/sont appelables

Deux niveaux sont importants :

- **Profil d'outils** : `tools.profile` et `agents.list[].tools.profile` (liste d'autorisation de base)
- **Profil d'outils par fournisseur** : `tools.byProvider[provider].profile` et `agents.list[].tools.byProvider[provider].profile`
- **Politique d'outils globale/par agent** : `tools.allow`/`tools.deny` et `agents.list[].tools.allow`/`agents.list[].tools.deny`
- **Politique d'outils par fournisseur** : `tools.byProvider[provider].allow/deny` et `agents.list[].tools.byProvider[provider].allow/deny`
- **Politique d'outils sandbox** (s'applique uniquement lors de l'isolation sandbox) : `tools.sandbox.tools.allow`/`tools.sandbox.tools.deny` et `agents.list[].tools.sandbox.tools.*`

Règle empirique :

- `deny` a toujours la priorité.
- Si `allow` n'est pas vide, tout le reste est traité comme bloqué.
- La politique d'outils est un arrêt définitif : `/exec` ne peut pas contourner un outil `exec` refusé.
- `/exec` modifie uniquement les valeurs par défaut de session pour les expéditeurs autorisés ; il n'accorde pas l'accès aux outils.
  Les clés d'outils fournisseur acceptent `provider` (par exemple `google-antigravity`) ou `provider/model` (par exemple `openai/gpt-5.2`).

### Groupes d'outils (raccourci)

Les politiques d'outils (globale, agent, sandbox) supportent les entrées `group:*`, qui se développent en plusieurs outils :

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
- `group:openclaw` : tous les outils OpenClaw intégrés (à l'exclusion des plugins fournisseurs)

## Élévation : "exécuter sur l'hôte" réservé à exec

L'élévation **n'accorde pas** d'outils supplémentaires ; elle affecte uniquement `exec`.

- Si vous êtes isolé en sandbox, `/elevated on` (ou `exec` avec `elevated: true`) s'exécute sur l'hôte (l'approbation peut toujours s'appliquer).
- Utilisez `/elevated full` pour ignorer l'approbation exec pour cette session.
- Si vous exécutez déjà directement, l'élévation est effectivement une opération nulle (toujours limitée).
- L'élévation **n'est pas** limitée par portée de compétence, **ne contournera pas** les autorisations/refus d'outils.
- `/exec` est séparé de l'élévation. Il ajuste uniquement les valeurs par défaut exec par session pour les expéditeurs autorisés.

Restrictions :

- Activation : `tools.elevated.enabled` (et optionnellement `agents.list[].tools.elevated.enabled`)
- Liste d'autorisation d'expéditeurs : `tools.elevated.allowFrom.<provider>` (et optionnellement `agents.list[].tools.elevated.allowFrom.<provider>`)

Voir [Mode d'élévation](/tools/elevated).

## Corrections courantes du "dilemme sandbox"

### "L'outil X est bloqué par la politique d'outils sandbox"

Clés de correction (choisissez-en une) :

- Désactiver sandbox : `agents.defaults.sandbox.mode=off` (ou par agent `agents.list[].sandbox.mode=off`)
- Autoriser l'outil dans le sandbox :
  - Le supprimer de `tools.sandbox.tools.deny` (ou par agent `agents.list[].tools.sandbox.tools.deny`)
  - Ou l'ajouter à `tools.sandbox.tools.allow` (ou par agent allow)

### "Je pensais que c'était une session main, pourquoi est-elle isolée en sandbox ?"

En mode `"non-main"`, les clés de groupe/canal *ne sont pas* des sessions main. Utilisez la clé de session main (affichée par `sandbox explain`) ou changez le mode en `"off"`.
