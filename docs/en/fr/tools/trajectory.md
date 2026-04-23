---
summary: "Exporter des bundles de trajectoire réduits pour déboguer une session d'agent OpenClaw"
read_when:
  - Debugging why an agent answered, failed, or called tools a certain way
  - Exporting a support bundle for an OpenClaw session
  - Investigating prompt context, tool calls, runtime errors, or usage metadata
  - Disabling or relocating trajectory capture
title: "Trajectory Bundles"
---

# Bundles de trajectoire

La capture de trajectoire est l'enregistreur de vol par session d'OpenClaw. Elle enregistre
une chronologie structurée pour chaque exécution d'agent, puis `/export-trajectory` empaquète
la session actuelle dans un bundle de support réduit.

Utilisez-le quand vous avez besoin de répondre à des questions comme :

- Quel prompt, system prompt et outils ont été envoyés au modèle ?
- Quels messages de transcript et appels d'outils ont mené à cette réponse ?
- L'exécution a-t-elle expiré, s'est-elle interrompue, compactée ou a-t-elle rencontré une erreur de fournisseur ?
- Quel modèle, plugins, skills et paramètres runtime étaient actifs ?
- Quelles métadonnées d'utilisation et de cache de prompt le fournisseur a-t-il retournées ?

## Démarrage rapide

Envoyez ceci dans la session active :

```text
/export-trajectory
```

Alias :

```text
/trajectory
```

OpenClaw écrit le bundle sous l'espace de travail :

```text
.openclaw/trajectory-exports/openclaw-trajectory-<session>-<timestamp>/
```

Vous pouvez choisir un nom de répertoire de sortie relatif :

```text
/export-trajectory bug-1234
```

Le chemin personnalisé est résolu à l'intérieur de `.openclaw/trajectory-exports/`. Les chemins
absolus et les chemins `~` sont rejetés.

## Accès

L'export de trajectoire est une commande de propriétaire. L'expéditeur doit passer les vérifications
d'autorisation de commande normales et les vérifications de propriétaire pour le canal.

## Ce qui est enregistré

La capture de trajectoire est activée par défaut pour les exécutions d'agent OpenClaw.

Les événements runtime incluent :

- `session.started`
- `trace.metadata`
- `context.compiled`
- `prompt.submitted`
- `model.completed`
- `trace.artifacts`
- `session.ended`

Les événements de transcript sont également reconstruits à partir de la branche de session active :

- messages utilisateur
- messages assistant
- appels d'outils
- résultats d'outils
- compactions
- changements de modèle
- labels et entrées de session personnalisées

Les événements sont écrits en JSON Lines avec ce marqueur de schéma :

```json
{
  "traceSchema": "openclaw-trajectory",
  "schemaVersion": 1
}
```

## Fichiers du bundle

Un bundle exporté peut contenir :

| Fichier               | Contenu                                                                                        |
| --------------------- | ---------------------------------------------------------------------------------------------- |
| `manifest.json`       | Schéma du bundle, fichiers source, comptages d'événements et liste de fichiers générés         |
| `events.jsonl`        | Chronologie ordonnée du runtime et du transcript                                              |
| `session-branch.json` | Branche de transcript active réduite et en-tête de session                                    |
| `metadata.json`       | Version OpenClaw, OS/runtime, modèle, snapshot de config, plugins, skills et métadonnées de prompt |
| `artifacts.json`      | Statut final, erreurs, utilisation, cache de prompt, comptage de compaction, texte assistant et métadonnées d'outils |
| `prompts.json`        | Prompts soumis et détails sélectionnés de la construction de prompt                           |
| `system-prompt.txt`   | Dernier system prompt compilé, quand capturé                                                  |
| `tools.json`          | Définitions d'outils envoyées au modèle, quand capturées                                      |

`manifest.json` liste les fichiers présents dans ce bundle. Certains fichiers sont omis
quand la session n'a pas capturé les données runtime correspondantes.

## Localisation de la capture

Par défaut, les événements de trajectoire runtime sont écrits à côté du fichier de session :

```text
<session>.trajectory.jsonl
```

OpenClaw écrit également un fichier pointeur au meilleur effort à côté de la session :

```text
<session>.trajectory-path.json
```

Définissez `OPENCLAW_TRAJECTORY_DIR` pour stocker les sidecars de trajectoire runtime dans un
répertoire dédié :

```bash
export OPENCLAW_TRAJECTORY_DIR=/var/lib/openclaw/trajectories
```

Quand cette variable est définie, OpenClaw écrit un fichier JSONL par session id dans ce
répertoire.

## Désactiver la capture

Définissez `OPENCLAW_TRAJECTORY=0` avant de démarrer OpenClaw :

```bash
export OPENCLAW_TRAJECTORY=0
```

Cela désactive la capture de trajectoire runtime. `/export-trajectory` peut toujours exporter
la branche de transcript, mais les fichiers runtime uniquement tels que le contexte compilé,
les artefacts de fournisseur et les métadonnées de prompt peuvent être manquants.

## Confidentialité et limites

Les bundles de trajectoire sont conçus pour le support et le débogage, pas pour la publication publique.
OpenClaw réduit les valeurs sensibles avant d'écrire les fichiers d'export :

- credentials et champs de payload connus comme secrets
- données d'image
- chemins d'état local
- chemins d'espace de travail, remplacés par `$WORKSPACE_DIR`
- chemins du répertoire personnel, quand détectés

L'exportateur limite également la taille d'entrée :

- fichiers sidecars runtime : 50 MiB
- fichiers de session : 50 MiB
- événements runtime : 200 000
- événements exportés totaux : 250 000
- les lignes d'événements runtime individuels sont tronquées au-dessus de 256 KiB

Examinez les bundles avant de les partager en dehors de votre équipe. La réduction est au meilleur effort
et ne peut pas connaître tous les secrets spécifiques à l'application.

## Dépannage

Si l'export n'a pas d'événements runtime :

- confirmez qu'OpenClaw a été démarré sans `OPENCLAW_TRAJECTORY=0`
- vérifiez si `OPENCLAW_TRAJECTORY_DIR` pointe vers un répertoire accessible en écriture
- exécutez un autre message dans la session, puis exportez à nouveau
- inspectez `manifest.json` pour `runtimeEventCount`

Si la commande rejette le chemin de sortie :

- utilisez un nom relatif comme `bug-1234`
- ne passez pas `/tmp/...` ou `~/...`
- gardez l'export à l'intérieur de `.openclaw/trajectory-exports/`

Si l'export échoue avec une erreur de taille, la session ou le sidecar a dépassé les
limites de sécurité d'export. Démarrez une nouvelle session ou exportez une reproduction plus petite.
