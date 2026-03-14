---
summary: "Aperçu de la journalisation : journaux de fichiers, sortie console, suivi CLI et interface utilisateur de contrôle"
read_when:
  - You need a beginner-friendly overview of logging
  - You want to configure log levels or formats
  - You are troubleshooting and need to find logs quickly
title: "Journalisation"
---

# Journalisation

OpenClaw enregistre les journaux à deux endroits :

- **Journaux de fichiers** (JSON lines) écrits par la passerelle.
- **Sortie console** affichée dans les terminaux et l'interface utilisateur de contrôle.

Cette page explique où se trouvent les journaux, comment les lire et comment configurer les niveaux et formats de journalisation.

## Où se trouvent les journaux

Par défaut, la passerelle écrit un fichier journal roulant sous :

`/tmp/openclaw/openclaw-YYYY-MM-DD.log`

La date utilise le fuseau horaire local de l'hôte de la passerelle.

Vous pouvez remplacer cela dans `~/.openclaw/openclaw.json` :

```json
{
  "logging": {
    "file": "/path/to/openclaw.log"
  }
}
```

## Comment lire les journaux

### CLI : suivi en direct (recommandé)

Utilisez la CLI pour suivre le fichier journal de la passerelle via RPC :

```bash
openclaw logs --follow
```

Modes de sortie :

- **Sessions TTY** : lignes de journal structurées, jolies et colorisées.
- **Sessions non-TTY** : texte brut.
- `--json` : JSON délimité par des lignes (un événement de journal par ligne).
- `--plain` : forcer le texte brut dans les sessions TTY.
- `--no-color` : désactiver les couleurs ANSI.

En mode JSON, la CLI émet des objets étiquetés par `type` :

- `meta` : métadonnées de flux (fichier, curseur, taille)
- `log` : entrée de journal analysée
- `notice` : indices de troncature / rotation
- `raw` : ligne de journal non analysée

Si la passerelle est inaccessible, la CLI affiche un court indice pour exécuter :

```bash
openclaw doctor
```

### Interface utilisateur de contrôle (web)

L'onglet **Logs** de l'interface utilisateur de contrôle suit le même fichier en utilisant `logs.tail`.
Voir [/web/control-ui](/web/control-ui) pour savoir comment l'ouvrir.

### Journaux réservés aux canaux

Pour filtrer l'activité des canaux (WhatsApp/Telegram/etc), utilisez :

```bash
openclaw channels logs --channel whatsapp
```

## Formats de journalisation

### Journaux de fichiers (JSONL)

Chaque ligne du fichier journal est un objet JSON. La CLI et l'interface utilisateur de contrôle analysent ces entrées pour afficher une sortie structurée (heure, niveau, sous-système, message).

### Sortie console

Les journaux de console sont **conscients du TTY** et formatés pour la lisibilité :

- Préfixes de sous-système (par exemple `gateway/channels/whatsapp`)
- Coloration des niveaux (info/warn/error)
- Mode compact ou JSON optionnel

Le formatage de la console est contrôlé par `logging.consoleStyle`.

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

Vous pouvez remplacer les deux via la variable d'environnement **`OPENCLAW_LOG_LEVEL`** (par exemple `OPENCLAW_LOG_LEVEL=debug`). La variable d'environnement a la priorité sur le fichier de configuration, vous pouvez donc augmenter la verbosité pour une seule exécution sans modifier `openclaw.json`. Vous pouvez également passer l'option CLI globale **`--log-level <level>`** (par exemple, `openclaw --log-level debug gateway run`), qui remplace la variable d'environnement pour cette commande.

`--verbose` affecte uniquement la sortie console ; il ne modifie pas les niveaux de journalisation des fichiers.

### Styles de console

`logging.consoleStyle` :

- `pretty` : convivial, coloré, avec horodatages.
- `compact` : sortie plus serrée (meilleure pour les longues sessions).
- `json` : JSON par ligne (pour les processeurs de journaux).

### Rédaction

Les résumés d'outils peuvent rédiger les jetons sensibles avant qu'ils ne frappent la console :

- `logging.redactSensitive` : `off` | `tools` (par défaut : `tools`)
- `logging.redactPatterns` : liste de chaînes regex pour remplacer l'ensemble par défaut

La rédaction affecte **la sortie console uniquement** et ne modifie pas les journaux de fichiers.

## Diagnostics + OpenTelemetry

Les diagnostics sont des événements structurés et lisibles par machine pour les exécutions de modèles **et** la télémétrie de flux de messages (webhooks, mise en file d'attente, état de session). Ils ne **remplacent pas** les journaux ; ils existent pour alimenter les métriques, les traces et autres exportateurs.

Les événements de diagnostic sont émis en processus, mais les exportateurs ne s'attachent que lorsque les diagnostics + le plugin d'exportateur sont activés.

### OpenTelemetry vs OTLP

- **OpenTelemetry (OTel)** : le modèle de données + SDKs pour les traces, les métriques et les journaux.
- **OTLP** : le protocole filaire utilisé pour exporter les données OTel vers un collecteur/backend.
- OpenClaw exporte via **OTLP/HTTP (protobuf)** aujourd'hui.

### Signaux exportés

- **Métriques** : compteurs + histogrammes (utilisation des jetons, flux de messages, mise en file d'attente).
- **Traces** : spans pour l'utilisation du modèle + traitement des webhooks/messages.
- **Journaux** : exportés via OTLP lorsque `diagnostics.otel.logs` est activé. Le volume de journaux peut être élevé ; gardez à l'esprit `logging.level` et les filtres d'exportateur.

### Catalogue des événements de diagnostic

Utilisation du modèle :

- `model.usage` : jetons, coût, durée, contexte, fournisseur/modèle/canal, identifiants de session.

Flux de messages :

- `webhook.received` : entrée webhook par canal.
- `webhook.processed` : webhook traité + durée.
- `webhook.error` : erreurs du gestionnaire webhook.
- `message.queued` : message mis en file d'attente pour traitement.
- `message.processed` : résultat + durée + erreur optionnelle.

File d'attente + session :

- `queue.lane.enqueue` : mise en file d'attente de la voie de commande + profondeur.
- `queue.lane.dequeue` : retrait de la file d'attente de la voie de commande + temps d'attente.
- `session.state` : transition d'état de session + raison.
- `session.stuck` : avertissement de session bloquée + âge.
- `run.attempt` : métadonnées de tentative/réessai d'exécution.
- `diagnostic.heartbeat` : compteurs agrégés (webhooks/file d'attente/session).

### Activer les diagnostics (sans exportateur)

Utilisez ceci si vous souhaitez que les événements de diagnostic soient disponibles pour les plugins ou les récepteurs personnalisés :

```json
{
  "diagnostics": {
    "enabled": true
  }
}
```

### Drapeaux de diagnostics (journaux ciblés)

Utilisez les drapeaux pour activer les journaux de débogage supplémentaires et ciblés sans augmenter `logging.level`.
Les drapeaux ne sont pas sensibles à la casse et supportent les caractères génériques (par exemple `telegram.*` ou `*`).

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Remplacement de l'environnement (ponctuel) :

```
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Notes :

- Les journaux des drapeaux vont au fichier journal standard (identique à `logging.file`).
- La sortie est toujours réduite selon `logging.redactSensitive`.
- Guide complet : [/diagnostics/flags](/diagnostics/flags).

### Exporter vers OpenTelemetry

Les diagnostics peuvent être exportés via le plugin `diagnostics-otel` (OTLP/HTTP). Cela fonctionne avec n'importe quel collecteur/backend OpenTelemetry qui accepte OTLP/HTTP.

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

Notes :

- Vous pouvez également activer le plugin avec `openclaw plugins enable diagnostics-otel`.
- `protocol` supporte actuellement `http/protobuf` uniquement. `grpc` est ignoré.
- Les métriques incluent l'utilisation des jetons, le coût, la taille du contexte, la durée d'exécution et les compteurs/histogrammes de flux de messages (webhooks, mise en file d'attente, état de session, profondeur/attente de file d'attente).
- Les traces/métriques peuvent être basculées avec `traces` / `metrics` (par défaut : activé). Les traces incluent les spans d'utilisation du modèle plus les spans de traitement des webhooks/messages lorsqu'ils sont activés.
- Définissez `headers` lorsque votre collecteur nécessite une authentification.
- Variables d'environnement supportées : `OTEL_EXPORTER_OTLP_ENDPOINT`,
  `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_PROTOCOL`.

### Métriques exportées (noms + types)

Utilisation du modèle :

- `openclaw.tokens` (compteur, attrs : `openclaw.token`, `openclaw.channel`,
  `openclaw.provider`, `openclaw.model`)
- `openclaw.cost.usd` (compteur, attrs : `openclaw.channel`, `openclaw.provider`,
  `openclaw.model`)
- `openclaw.run.duration_ms` (histogramme, attrs : `openclaw.channel`,
  `openclaw.provider`, `openclaw.model`)
- `openclaw.context.tokens` (histogramme, attrs : `openclaw.context`,
  `openclaw.channel`, `openclaw.provider`, `openclaw.model`)

Flux de messages :

- `openclaw.webhook.received` (compteur, attrs : `openclaw.channel`,
  `openclaw.webhook`)
- `openclaw.webhook.error` (compteur, attrs : `openclaw.channel`,
  `openclaw.webhook`)
- `openclaw.webhook.duration_ms` (histogramme, attrs : `openclaw.channel`,
  `openclaw.webhook`)
- `openclaw.message.queued` (compteur, attrs : `openclaw.channel`,
  `openclaw.source`)
- `openclaw.message.processed` (compteur, attrs : `openclaw.channel`,
  `openclaw.outcome`)
- `openclaw.message.duration_ms` (histogramme, attrs : `openclaw.channel`,
  `openclaw.outcome`)

Files d'attente + sessions :

- `openclaw.queue.lane.enqueue` (compteur, attrs : `openclaw.lane`)
- `openclaw.queue.lane.dequeue` (compteur, attrs : `openclaw.lane`)
- `openclaw.queue.depth` (histogramme, attrs : `openclaw.lane` ou
  `openclaw.channel=heartbeat`)
- `openclaw.queue.wait_ms` (histogramme, attrs : `openclaw.lane`)
- `openclaw.session.state` (compteur, attrs : `openclaw.state`, `openclaw.reason`)
- `openclaw.session.stuck` (compteur, attrs : `openclaw.state`)
- `openclaw.session.stuck_age_ms` (histogramme, attrs : `openclaw.state`)
- `openclaw.run.attempt` (compteur, attrs : `openclaw.attempt`)

### Spans exportés (noms + attributs clés)

- `openclaw.model.usage`
  - `openclaw.channel`, `openclaw.provider`, `openclaw.model`
  - `openclaw.sessionKey`, `openclaw.sessionId`
  - `openclaw.tokens.*` (input/output/cache_read/cache_write/total)
- `openclaw.webhook.processed`
  - `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`
- `openclaw.webhook.error`
  - `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`,
    `openclaw.error`
- `openclaw.message.processed`
  - `openclaw.channel`, `openclaw.outcome`, `openclaw.chatId`,
    `openclaw.messageId`, `openclaw.sessionKey`, `openclaw.sessionId`,
    `openclaw.reason`
- `openclaw.session.stuck`
  - `openclaw.state`, `openclaw.ageMs`, `openclaw.queueDepth`,
    `openclaw.sessionKey`, `openclaw.sessionId`

### Échantillonnage + vidage

- Échantillonnage des traces : `diagnostics.otel.sampleRate` (0.0–1.0, spans racine uniquement).
- Intervalle d'export des métriques : `diagnostics.otel.flushIntervalMs` (min 1000ms).

### Notes sur le protocole

- Les points de terminaison OTLP/HTTP peuvent être définis via `diagnostics.otel.endpoint` ou
  `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Si le point de terminaison contient déjà `/v1/traces` ou `/v1/metrics`, il est utilisé tel quel.
- Si le point de terminaison contient déjà `/v1/logs`, il est utilisé tel quel pour les journaux.
- `diagnostics.otel.logs` active l'export de journaux OTLP pour la sortie du logger principal.

### Comportement d'export des journaux

- Les journaux OTLP utilisent les mêmes enregistrements structurés écrits dans `logging.file`.
- Respectez `logging.level` (niveau de journalisation des fichiers). La rédaction de la console ne s'applique **pas**
  aux journaux OTLP.
- Les installations à haut volume devraient préférer l'échantillonnage/filtrage du collecteur OTLP.

## Conseils de dépannage

- **Passerelle inaccessible ?** Exécutez d'abord `openclaw doctor`.
- **Journaux vides ?** Vérifiez que la passerelle est en cours d'exécution et écrit dans le chemin de fichier
  dans `logging.file`.
- **Besoin de plus de détails ?** Définissez `logging.level` sur `debug` ou `trace` et réessayez.
