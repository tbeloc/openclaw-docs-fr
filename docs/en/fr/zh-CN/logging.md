---
read_when:
  - Vous avez besoin d'un aperçu des journaux adapté aux débutants
  - Vous souhaitez configurer le niveau ou le format des journaux
  - Vous dépannez et avez besoin de trouver rapidement les journaux
summary: Aperçu des journaux : journaux de fichiers, sortie console, suivi CLI et interface utilisateur de contrôle
title: Journalisation
x-i18n:
  generated_at: "2026-02-03T07:50:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 884fcf4a906adff34d546908e22abd283cb89fe0845076cf925c72384ec3556b
  source_path: logging.md
  workflow: 15
---

# Journalisation

OpenClaw enregistre les journaux dans deux endroits :

- **Journaux de fichiers** (lignes JSON) écrits par la passerelle Gateway.
- **Sortie console** affichée dans le terminal et l'interface utilisateur de contrôle.

Cette page explique où se trouvent les journaux, comment les lire et comment configurer le niveau et le format des journaux.

## Emplacement des journaux

Par défaut, la passerelle Gateway écrit les fichiers journaux rotatifs à l'emplacement suivant :

`/tmp/openclaw/openclaw-YYYY-MM-DD.log`

La date utilise le fuseau horaire local de l'hôte Gateway.

Vous pouvez remplacer ce paramètre dans `~/.openclaw/openclaw.json` :

```json
{
  "logging": {
    "file": "/path/to/openclaw.log"
  }
}
```

## Comment lire les journaux

### CLI : suivi en temps réel (recommandé)

Utilisez la CLI pour suivre le fichier journal de la passerelle Gateway via RPC :

```bash
openclaw logs --follow
```

Modes de sortie :

- **Session TTY** : lignes de journal belles, colorées et structurées.
- **Session non-TTY** : texte brut.
- `--json` : JSON délimité par des lignes (un événement de journal par ligne).
- `--plain` : force le texte brut dans les sessions TTY.
- `--no-color` : désactive les couleurs ANSI.

En mode JSON, la sortie CLI produit des objets avec une étiquette `type` :

- `meta` : métadonnées de flux (fichier, curseur, taille)
- `log` : entrée de journal analysée
- `notice` : avis de troncature/rotation
- `raw` : ligne de journal non analysée

Si la passerelle Gateway est inaccessible, la CLI affiche un court message suggérant d'exécuter :

```bash
openclaw doctor
```

### Interface utilisateur de contrôle (Web)

L'onglet **Journaux** de l'interface utilisateur de contrôle utilise `logs.tail` pour suivre le même fichier.
Voir [/web/control-ui](/web/control-ui) pour savoir comment l'ouvrir.

### Journaux de canal uniquement

Pour filtrer l'activité des canaux (WhatsApp/Telegram, etc.), utilisez :

```bash
openclaw channels logs --channel whatsapp
```

## Format des journaux

### Journaux de fichiers (JSONL)

Chaque ligne du fichier journal est un objet JSON. La CLI et l'interface utilisateur de contrôle analysent ces entrées pour afficher une sortie structurée (heure, niveau, sous-système, message).

### Sortie console

Les journaux console **sont conscients du TTY** et formatés pour une meilleure lisibilité :

- Préfixes de sous-système (par exemple `gateway/channels/whatsapp`)
- Coloration du niveau (info/warn/error)
- Mode compact ou JSON optionnel

Le format console est contrôlé par `logging.consoleStyle`.

## Configuration de la journalisation

Toute la configuration de journalisation se trouve sous `logging` dans `~/.openclaw/openclaw.json`.

```json
{
  "logging": {
    "level": "info",
    "file": "/tmp/openclaw/openclaw-YYYY-MM-DD.log",
    "consoleLevel": "info",
    "consoleStyle": "pretty",
    "redactSensitive": "tools",
    "redactPatterns": ["sk-.*"]
  }
}
```

### Niveaux de journalisation

- `logging.level` : niveau des **journaux de fichiers** (JSONL).
- `logging.consoleLevel` : niveau de verbosité de la **console**.

`--verbose` affecte uniquement la sortie console ; il ne change pas le niveau de journalisation des fichiers.

### Style de console

`logging.consoleStyle` :

- `pretty` : convivial, coloré, avec horodatage.
- `compact` : sortie plus compacte (idéale pour les longues sessions).
- `json` : JSON par ligne (pour les processeurs de journaux).

### Rédaction

Les résumés d'outils peuvent être édités pour masquer les jetons sensibles avant leur sortie sur la console :

- `logging.redactSensitive` : `off` | `tools` (par défaut : `tools`)
- `logging.redactPatterns` : liste de chaînes d'expressions régulières pour remplacer l'ensemble par défaut

La rédaction affecte uniquement la **sortie console** et ne modifie pas les journaux de fichiers.

## Diagnostics + OpenTelemetry

Les diagnostics sont des événements structurés et lisibles par machine pour la télémétrie des **exécutions de modèles** et des **flux de messages** (webhooks, files d'attente, état de session). Ils ne **remplacent pas** les journaux ; ils existent pour fournir des données aux métriques, traces et autres exportateurs.

Les événements de diagnostic sont émis en processus, mais les exportateurs ne s'attachent que lorsque les diagnostics + le plugin exportateur sont activés.

### OpenTelemetry vs OTLP

- **OpenTelemetry (OTel)** : modèle de données + SDK pour les traces, métriques et journaux.
- **OTLP** : protocole filaire pour exporter les données OTel vers un collecteur/backend.
- OpenClaw exporte actuellement via **OTLP/HTTP (protobuf)**.

### Signaux exportés

- **Métriques** : compteurs + histogrammes (utilisation de jetons, flux de messages, files d'attente).
- **Traces** : utilisation de modèles + spans pour le traitement des webhooks/messages.
- **Journaux** : exportés via OTLP lorsque `diagnostics.otel.logs` est activé. Le volume de journaux peut être important ; attention à `logging.level` et aux filtres d'exportateur.

### Catalogue des événements de diagnostic

Utilisation de modèles :

- `model.usage` : jetons, coût, durée, contexte, fournisseur/modèle/canal, ID de session.

Flux de messages :

- `webhook.received` : entrée webhook par canal.
- `webhook.processed` : webhook traité + durée.
- `webhook.error` : erreur du gestionnaire webhook.
- `message.queued` : message mis en file d'attente pour traitement.
- `message.processed` : résultat + durée + erreur optionnelle.

File d'attente + session :

- `queue.lane.enqueue` : mise en file d'attente de la voie de commande + profondeur.
- `queue.lane.dequeue` : retrait de la file d'attente de la voie de commande + temps d'attente.
- `session.state` : transition d'état de session + raison.
- `session.stuck` : avertissement de session bloquée + durée.
- `run.attempt` : métadonnées de nouvelle tentative/tentative d'exécution.
- `diagnostic.heartbeat` : compteurs agrégés (webhooks/files d'attente/sessions).

### Activation des diagnostics (sans exportateur)

Si vous souhaitez que les événements de diagnostic soient disponibles pour les plugins ou les récepteurs personnalisés, utilisez cette configuration :

```json
{
  "diagnostics": {
    "enabled": true
  }
}
```

### Drapeaux de diagnostic (journalisation ciblée)

Utilisez les drapeaux pour activer des journaux de débogage ciblés supplémentaires sans augmenter `logging.level`.
Les drapeaux ne sont pas sensibles à la casse et supportent les caractères génériques (par exemple `telegram.*` ou `*`).

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Remplacement par variable d'environnement (une seule fois) :

```
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Remarques :

- Les journaux des drapeaux vont dans le fichier journal standard (même que `logging.file`).
- La sortie est toujours éditée selon `logging.redactSensitive`.
- Guide complet : [/diagnostics/flags](/diagnostics/flags).

### Exportation vers OpenTelemetry

Les diagnostics peuvent être exportés via le plugin `diagnostics-otel` (OTLP/HTTP). Cela fonctionne avec n'importe quel collecteur/backend OpenTelemetry acceptant OTLP/HTTP.

```json
{
  "plugins": {
    "allow": ["diagnostics-otel"],
    "entries": {
      "diagnostics-otel": {
        "enabled": true
      }
    }
  },
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "endpoint": "http://otel-collector:4318",
      "protocol": "http/protobuf",
      "serviceName": "openclaw-gateway",
      "traces": true,
      "metrics": true,
      "logs": true,
      "sampleRate": 0.2,
      "flushIntervalMs": 60000
    }
  }
}
```

Remarques :

- Vous pouvez également activer le plugin avec `openclaw plugins enable diagnostics-otel`.
- `protocol` ne supporte actuellement que `http/protobuf`. `grpc` est ignoré.
- Les métriques incluent l'utilisation de jetons, le coût, la taille du contexte, la durée d'exécution et les compteurs/histogrammes de flux de messages (webhooks, files d'attente, état de session, profondeur/attente de file d'attente).
- Les traces/métriques peuvent être basculées via `traces` / `metrics` (par défaut : activé). Lorsqu'activées, les traces incluent les spans d'utilisation de modèles plus les spans de traitement des webhooks/messages.
- Définissez `headers` lorsque votre collecteur nécessite une authentification.
- Variables d'environnement supportées : `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_PROTOCOL`.

### Métriques exportées (nom + type)

Utilisation de modèles :

- `openclaw.tokens` (compteur, attributs : `openclaw.token`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
- `openclaw.cost.usd` (compteur, attributs : `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
- `openclaw.run.duration_ms` (histogramme, attributs : `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
- `openclaw.context.tokens` (histogramme, attributs : `openclaw.context`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`)

Flux de messages :

- `openclaw.webhook.received` (compteur, attributs : `openclaw.channel`, `openclaw.webhook`)
- `openclaw.webhook.error` (compteur, attributs : `openclaw.channel`, `openclaw.webhook`)
- `openclaw.webhook.duration_ms` (histogramme, attributs : `openclaw.channel`, `openclaw.webhook`)
- `openclaw.message.queued` (compteur, attributs : `openclaw.channel`, `openclaw.source`)
- `openclaw.message.processed` (compteur, attributs : `openclaw.channel`, `openclaw.outcome`)
- `openclaw.message.duration_ms` (histogramme, attributs : `openclaw.channel`, `openclaw.outcome`)

File d'attente + session :

- `openclaw.queue.lane.enqueue` (compteur, attributs : `openclaw.lane`)
- `openclaw.queue.lane.dequeue` (compteur, attributs : `openclaw.lane`)
- `openclaw.queue.depth` (histogramme, attributs : `openclaw.lane` ou `openclaw.channel=heartbeat`)
- `openclaw.queue.wait_ms` (histogramme, attributs : `openclaw.lane`)
- `openclaw.session.state` (compteur, attributs : `openclaw.state`, `openclaw.reason`)
- `openclaw.session.stuck` (compteur, attributs : `openclaw.state`)
- `openclaw.session.stuck_age_ms` (histogramme, attributs : `openclaw.state`)
- `openclaw.run.attempt` (compteur, attributs : `openclaw.attempt`)

### Spans exportées (nom + attributs clés)

- `openclaw.model.usage`
  - `openclaw.channel`, `openclaw.provider`, `openclaw.model`
  - `openclaw.sessionKey`, `openclaw.sessionId`
  - `openclaw.tokens.*` (input/output/cache_read/cache_write/total)
- `openclaw.webhook.processed`
  - `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`
- `openclaw.webhook.error`
  - `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`, `openclaw.error`
- `openclaw.message.processed`
  - `openclaw.channel`, `openclaw.outcome`, `openclaw.chatId`, `openclaw.messageId`, `openclaw.sessionKey`, `openclaw.sessionId`, `openclaw.reason`
- `openclaw.session.stuck`
  - `openclaw.state`, `openclaw.ageMs`, `openclaw.queueDepth`, `openclaw.sessionKey`, `openclaw.sessionId`

### Échantillonnage + vidage

- Échantillonnage des traces : `diagnostics.otel.sampleRate` (0.0–1.0, spans racine uniquement).
- Intervalle d'exportation des métriques : `diagnostics.otel.flushIntervalMs` (minimum 1000ms).

### Notes sur le protocole

- Le point de terminaison OTLP/HTTP peut être défini via `diagnostics.otel.endpoint` ou `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Si le point de terminaison inclut déjà `/v1/traces` ou `/v1/metrics`, il est utilisé tel quel.
- Si le point de terminaison inclut déjà `/v1/logs`, il est utilisé tel quel pour les journaux.
- `diagnostics.otel.logs` active l'exportation des journaux OTLP pour la sortie du logger principal.

### Comportement d'exportation des journaux

- Les journaux OTL
