---
summary: "Référence CLI pour les vérifications de conformité des canaux `openclaw policy`"
read_when:
  - You want to check OpenClaw settings against an authored policy.jsonc
  - You want policy findings in doctor lint
  - You need a policy attestation hash for audit evidence
title: "Policy"
---

# `openclaw policy`

`openclaw policy` est fourni par le plugin Policy intégré. Policy est une
couche de conformité d'entreprise sur les paramètres OpenClaw existants : `policy.jsonc`
définit les exigences rédigées, OpenClaw observe l'espace de travail actif comme
preuve, et les vérifications de santé de la politique signalent la dérive via `doctor --lint`.

Cette première tranche de politique gère les canaux configurés. Par exemple, le service informatique peut enregistrer
que Telegram n'est pas approuvé, puis `doctor --lint` signale tout canal Telegram activé
et `doctor --fix` peut le désactiver lorsque les réparations d'espace de travail sont explicitement
activées.

## Démarrage rapide

Activez le plugin Policy intégré avant la première utilisation :

```bash
openclaw plugins enable policy
```

Lorsque la politique est activée, doctor peut charger les vérifications de santé de la politique sans activer
des plugins arbitraires. Le plugin reste activé si `policy.jsonc` est manquant, donc
doctor peut signaler l'artefact manquant.

La politique est rédigée, non générée à partir des paramètres actuels de l'utilisateur. Une politique de canal minimale
ressemble à ceci :

```jsonc
{
  "channels": {
    "denyRules": [
      {
        "id": "no-telegram",
        "when": { "provider": "telegram" },
        "reason": "Telegram is not approved for this workspace.",
      },
    ],
  },
}
```

Les règles font autorité. Un bloc de catégorie n'est qu'un espace de noms ; les vérifications s'exécutent
lorsqu'une règle concrète est présente. OpenClaw lit les paramètres `channels.*` actuels
et signale les paramètres qui ne sont pas conformes.

Exécutez les vérifications uniquement de politique lors de la rédaction :

```bash
openclaw policy check
openclaw policy check --json
openclaw policy check --severity-min error
```

`policy check` exécute uniquement l'ensemble de vérifications de politique et émet des preuves, des résultats et
des hachages d'attestation. Les mêmes résultats apparaissent également dans `openclaw doctor --lint`
lorsque le plugin Policy est activé.

Un exemple de sortie JSON propre inclut des hachages stables qui peuvent être enregistrés par un
opérateur ou superviseur :

```json
{
  "ok": true,
  "attestation": {
    "policy": {
      "path": "policy.jsonc",
      "hash": "sha256:..."
    },
    "workspace": {
      "scope": "policy",
      "hash": "sha256:..."
    },
    "findingsHash": "sha256:...",
    "attestationHash": "sha256:..."
  },
  "checksRun": 5,
  "checksSkipped": 0,
  "findings": []
}
```

## Configurer la politique

La configuration de la politique se trouve sous `plugins.entries.policy.config`.

```jsonc
{
  "plugins": {
    "entries": {
      "policy": {
        "enabled": true,
        "config": {
          "enabled": true,
          "path": "policy.jsonc",
          "workspaceRepairs": false,
          "expectedHash": "sha256:...",
          "expectedAttestationHash": "sha256:...",
        },
      },
    },
  },
}
```

| Paramètre                 | Objectif                                                            |
| ------------------------- | ------------------------------------------------------------------- |
| `enabled`                 | Activez les vérifications de politique même avant que `policy.jsonc` n'existe. |
| `workspaceRepairs`        | Permettez à `doctor --fix` de modifier les paramètres d'espace de travail gérés par la politique. |
| `expectedHash`            | Verrouillage de hachage optionnel pour l'artefact de politique approuvé. |
| `expectedAttestationHash` | Verrouillage de hachage optionnel pour la dernière vérification de politique propre acceptée. |
| `path`                    | Emplacement relatif à l'espace de travail de l'artefact de politique. |

Définissez `plugins.entries.policy.config.enabled` sur `false` pour désactiver les vérifications de politique
pour un espace de travail tout en laissant le plugin installé.

## Accepter l'état de la politique

Le hachage d'attestation identifie la réclamation stable : hachage de politique, hachage de preuve,
hachage de résultats, et si le résultat était propre. Il n'inclut intentionnellement pas
`checkedAt`, donc le même état de politique produit la même attestation
lors de vérifications répétées.

Si une passerelle ultérieure ou un superviseur utilise la politique pour bloquer, approuver ou annoter une
action d'exécution, il doit enregistrer le hachage d'attestation de la dernière vérification de politique propre. `checkedAt` reste dans la sortie JSON pour les journaux d'audit, mais ne fait pas partie du
hachage d'attestation stable.

Utilisez ce cycle de vie lors de l'acceptation de l'état de la politique :

1. Rédigez ou examinez `policy.jsonc`.
2. Exécutez `openclaw policy check --json`.
3. Si le résultat est propre, enregistrez `attestation.policy.hash` comme `expectedHash`.
4. Enregistrez `attestation.attestationHash` comme `expectedAttestationHash`.
5. Réexécutez `openclaw doctor --lint` dans les portes CI ou de publication.

Si les règles de politique changent intentionnellement, mettez à jour les deux hachages acceptés à partir d'une vérification propre. Si les paramètres d'espace de travail changent intentionnellement mais que la politique reste la même,
seul `expectedAttestationHash` change généralement.

## Résultats

La politique vérifie actuellement :

| ID de vérification                 | Résultat                                                            |
| ---------------------------------- | ------------------------------------------------------------------- |
| `policy/policy-jsonc-missing`      | La politique est activée mais `policy.jsonc` est manquant.          |
| `policy/policy-jsonc-invalid`      | La politique ne peut pas être analysée ou a des règles malformées.  |
| `policy/policy-hash-mismatch`      | La politique ne correspond pas à `expectedHash` configuré.          |
| `policy/attestation-hash-mismatch` | La preuve de politique actuelle ne correspond plus à l'attestation acceptée. |
| `policy/channels-denied-provider`  | Un canal activé correspond à une règle de refus de canal.           |

Les résultats de politique peuvent inclure `target` et `requirement` : la
chose d'espace de travail observée qui ne se conforme pas, et la règle rédigée qui en a fait un résultat.

## Réparation

`doctor --lint` et `policy check` sont en lecture seule.

`doctor --fix` ne modifie les paramètres d'espace de travail gérés par la politique que lorsque
`workspaceRepairs` est explicitement activé. Sans cet opt-in, les vérifications de politique
signalent ce qu'elles répareraient et laissent les paramètres inchangés.

Dans cette version, la réparation peut désactiver les canaux qui sont activés dans la configuration OpenClaw
mais refusés par `channels.denyRules`. Activez `workspaceRepairs` uniquement après que
le fichier de politique a été examiné, car une règle de refus valide peut désactiver un
canal configuré :

```jsonc
{
  "plugins": {
    "entries": {
      "policy": {
        "config": {
          "workspaceRepairs": true,
        },
      },
    },
  },
}
```

## Codes de sortie

`policy check` quitte avec `0` lorsqu'il n'y a pas de résultats au seuil, `1` lorsque
des résultats sont présents, et `2` pour les défaillances d'argument ou d'exécution.
