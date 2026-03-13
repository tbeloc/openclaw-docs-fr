---
read_when:
  - Configurer l'approbation d'exécution ou les listes blanches
  - Implémenter l'expérience utilisateur d'approbation d'exécution dans les applications macOS
  - Examiner les conseils d'échappement de sandbox et leurs impacts
summary: Approbation d'exécution, listes blanches et conseils d'échappement de sandbox
title: Approbation d'exécution
x-i18n:
  generated_at: "2026-02-03T08:19:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 97736427752eb905bb5d1f5b54bddbdea38eb5ac5824e2bf99258fcf44ee393c
  source_path: tools/exec-approvals.md
  workflow: 15
---

# Approbation d'exécution

L'approbation d'exécution est **un garde-fou de sécurité pour les applications/hôtes nœuds compagnons** qui permet aux agents isolés en sandbox d'exécuter des commandes sur l'hôte réel (`gateway` ou `node`). Pensez-y comme un verrouillage de sécurité : une commande n'est autorisée à s'exécuter que si la politique + la liste blanche + (optionnellement) l'approbation de l'utilisateur sont tous d'accord.

L'approbation d'exécution s'ajoute à la politique des outils et aux contrôles d'escalade de privilèges (sauf si elevated est défini sur `full`, ce qui contourne l'approbation).

La politique en vigueur prend la plus stricte entre `tools.exec.*` et les valeurs par défaut d'approbation ; si le champ d'approbation est omis, la valeur de `tools.exec` est utilisée.

Si l'interface utilisateur de l'application compagnon **n'est pas disponible**, toute demande nécessitant une invite sera décidée par **ask fallback** (par défaut : deny).

## Portée

L'approbation d'exécution est appliquée localement sur l'hôte d'exécution :

- **Hôte gateway** → processus `openclaw` sur la machine gateway
- **Hôte nœud** → exécuteur de nœud (application compagnon macOS ou hôte nœud sans interface)

Division du travail macOS :

- **Service hôte nœud** transfère `system.run` à l'**application macOS** via IPC local.
- **Application macOS** effectue l'approbation et exécute la commande dans le contexte de l'interface utilisateur.

## Configuration et stockage

Les informations d'approbation sont stockées dans un fichier JSON local sur l'hôte d'exécution :

`~/.openclaw/exec-approvals.json`

Exemple de structure :

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

## Options de politique

### Security (`exec.security`)

- **deny** : Bloque toutes les demandes d'exécution sur l'hôte.
- **allowlist** : Autorise uniquement les commandes dans la liste blanche.
- **full** : Autorise toutes les commandes (équivalent au mode escalade).

### Ask (`exec.ask`)

- **off** : Ne jamais demander.
- **on-miss** : Demander uniquement si la liste blanche ne correspond pas.
- **always** : Demander pour chaque commande.

### Ask fallback (`askFallback`)

Si une invite est nécessaire mais que l'interface utilisateur n'est pas accessible, le fallback décide :

- **deny** : Bloquer.
- **allowlist** : Autoriser uniquement si la liste blanche correspond.
- **full** : Autoriser.

## Liste blanche (par agent)

La liste blanche est configurée **par agent**. S'il existe plusieurs agents, basculez vers l'agent à éditer dans l'application macOS. La correspondance de motif **ne tient pas compte de la casse**.

Les motifs doivent se résoudre en **chemins binaires** (les entrées contenant uniquement le nom de base sont ignorées).

Les anciennes entrées `agents.default` sont migrées vers `agents.main` lors du chargement.

Exemples :

- `~/Projects/**/bin/bird`
- `~/.local/bin/*`
- `/opt/homebrew/bin/rg`

Chaque entrée de liste blanche suit :

- **id** UUID stable pour l'identification de l'interface utilisateur (optionnel)
- **last used** horodatage
- **last used command**
- **last resolved path**

## Autorisation automatique des CLI de compétences

Lorsque **Auto-allow skill CLIs** est activé, les exécutables référencés par les compétences connues sont traités comme étant dans la liste blanche sur le nœud (nœud macOS ou hôte nœud sans interface). Ceci récupère la liste des binaires de compétences via `skills.bins` du RPC Gateway. Si vous souhaitez une liste blanche manuelle stricte, désactivez cette option.

## Binaires sécurisés (stdin uniquement)

`tools.exec.safeBins` définit un petit ensemble de binaires **stdin uniquement** (par exemple `jq`) qui peuvent s'exécuter en mode liste blanche **sans** entrée de liste blanche explicite. Les binaires sécurisés rejettent les paramètres de fichier positionnels et les drapeaux de type chemin, ils ne peuvent donc opérer que sur les flux entrants.

En mode liste blanche, les chaînes shell et les redirections ne sont pas automatiquement autorisées.

Les chaînes shell (`&&`, `||`, `;`) sont autorisées lorsque chaque segment de niveau supérieur satisfait la liste blanche (y compris les binaires sécurisés ou l'autorisation automatique de compétences). Les redirections restent non supportées en mode liste blanche.

La substitution de commande (`$()` / backticks) est rejetée lors de l'analyse de la liste blanche, y compris entre guillemets doubles ; si vous avez besoin du texte littéral `$()`, utilisez des guillemets simples.

Binaires sécurisés par défaut : `jq`, `grep`, `cut`, `sort`, `uniq`, `head`, `tail`, `tr`, `wc`.

## Édition de l'interface utilisateur de contrôle

Utilisez la carte **Control UI → Nodes → Exec approvals** pour éditer les valeurs par défaut, les paramètres de remplacement par agent et la liste blanche. Sélectionnez une portée (Defaults ou un agent), ajustez la politique, ajoutez/supprimez des motifs de liste blanche, puis cliquez sur **Save**. L'interface utilisateur affiche les métadonnées **last used** pour chaque motif afin que vous puissiez garder la liste propre.

Le sélecteur de cible peut choisir **Gateway** (approbations locales) ou **Node**. Le nœud doit annoncer `system.execApprovals.get/set` (application macOS ou hôte nœud sans interface).

Si le nœud n'a pas encore annoncé les approbations d'exécution, éditez directement son `~/.openclaw/exec-approvals.json` local.

CLI : `openclaw approvals` supporte l'édition gateway ou node (voir [Approvals CLI](/cli/approvals)).

## Flux d'approbation

Lorsqu'une invite est nécessaire, la gateway diffuse `exec.approval.requested` aux clients opérateurs.

Control UI et l'application macOS traitent via `exec.approval.resolve`, puis la gateway transfère la demande approuvée à l'hôte nœud.

Lorsqu'une approbation est nécessaire, l'outil exec retourne immédiatement un id d'approbation. Utilisez cet id pour associer les événements système ultérieurs (`Exec finished` / `Exec denied`). Si aucune décision n'est reçue avant le délai d'expiration, la demande est traitée comme un délai d'approbation et affichée comme raison du refus.

La boîte de dialogue de confirmation inclut :

- Commande + arguments
- cwd
- id de l'agent
- Chemin exécutable résolu
- Métadonnées hôte + politique

Actions :

- **Allow once** → Exécuter immédiatement
- **Always allow** → Ajouter à la liste blanche + exécuter
- **Deny** → Bloquer

## Transfert d'approbation vers les canaux de chat

Vous pouvez transférer les invites d'approbation d'exécution vers n'importe quel canal de chat (y compris les canaux de plugin) et approuver avec `/approve`. Ceci utilise le pipeline de livraison sortante normal.

Configuration :

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring or regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

Répondre dans le chat :

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

### Flux IPC macOS

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

Considérations de sécurité :

- Mode socket Unix `0600`, token stocké dans `exec-approvals.json`.
- Vérification de l'UID pair.
- Défi/réponse (nonce + token HMAC + hachage de demande) + TTL court.

## Événements système

Le cycle de vie d'exécution est présenté sous forme de messages système :

- `Exec running` (uniquement si la commande dépasse le seuil de notification d'exécution)
- `Exec finished`
- `Exec denied`

Ces messages sont publiés dans la session de l'agent après que le nœud ait signalé l'événement.

Les approbations d'exécution de l'hôte gateway émettent les mêmes événements de cycle de vie à la fin de la commande (et optionnellement lorsque le temps d'exécution dépasse le seuil).

L'exécution passée par le contrôle d'approbation réutilise l'id d'approbation comme `runId` dans ces messages pour faciliter l'association.

## Impacts

- Les permissions **full** sont puissantes ; préférez les listes blanches autant que possible.
- **ask** vous tient informé tout en permettant une approbation rapide.
- Les listes blanches par agent empêchent les approbations d'un agent de fuir vers d'autres.
- L'approbation s'applique uniquement aux demandes d'exécution sur l'hôte provenant d'**expéditeurs autorisés**. Les expéditeurs non autorisés ne peuvent pas émettre `/exec`.
- `/exec security=full` est une commodité au niveau de la session pour les opérateurs autorisés, conçue pour contourner l'approbation.
  Pour bloquer complètement l'exécution sur l'hôte, définissez la sécurité d'approbation sur `deny`, ou refusez l'outil `exec` via la politique des outils.

Contenu connexe :

- [Outil Exec](/tools/exec)
- [Mode escalade](/tools/elevated)
- [Compétences](/tools/skills)
