---
summary: "Exporter les diagnostics OpenClaw vers n'importe quel collecteur OpenTelemetry via le plugin diagnostics-otel (OTLP/HTTP)"
title: "Export OpenTelemetry"
read_when:
  - You want to send OpenClaw model usage, message flow, or session metrics to an OpenTelemetry collector
  - You are wiring traces, metrics, or logs into Grafana, Datadog, Honeycomb, New Relic, Tempo, or another OTLP backend
  - You need the exact metric names, span names, or attribute shapes to build dashboards or alerts
---

OpenClaw exporte les diagnostics via le plugin `diagnostics-otel` fourni
en utilisant **OTLP/HTTP (protobuf)**. N'importe quel collecteur ou backend
acceptant OTLP/HTTP fonctionne sans modification de code. Pour les journaux
locaux et comment les lire, voir [Logging](/fr/logging).

## Comment cela s'articule

- **Les événements de diagnostics** sont des enregistrements structurés,
  in-process émis par la Gateway et les plugins fournis pour les exécutions
  de modèles, le flux de messages, les sessions, les files d'attente et exec.
- **Le plugin `diagnostics-otel`** s'abonne à ces événements et les exporte
  en tant que **métriques**, **traces** et **journaux** OpenTelemetry sur OTLP/HTTP.
- Les exportateurs ne s'attachent que lorsque la surface de diagnostics et
  le plugin sont tous deux activés, donc le coût in-process reste proche de
  zéro par défaut.

## Démarrage rapide

```json5
{
  plugins: {
    allow: ["diagnostics-otel"],
    entries: {
      "diagnostics-otel": { enabled: true },
    },
  },
  diagnostics: {
    enabled: true,
    otel: {
      enabled: true,
      endpoint: "http://otel-collector:4318",
      protocol: "http/protobuf",
      serviceName: "openclaw-gateway",
      traces: true,
      metrics: true,
      logs: true,
      sampleRate: 0.2,
      flushIntervalMs: 60000,
    },
  },
}
```

Vous pouvez également activer le plugin depuis la CLI :

```bash
openclaw plugins enable diagnostics-otel
```

<Note>
`protocol` supporte actuellement `http/protobuf` uniquement. `grpc` est ignoré.
</Note>

## Signaux exportés

| Signal      | Contenu                                                                                                                                                                                                                                   |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Métriques** | Compteurs et histogrammes pour l'utilisation des tokens, le coût, la durée d'exécution, le flux de messages, les files d'attente, l'état des sessions, exec et la pression mémoire. |
| **Traces**  | Spans pour l'utilisation du modèle, les appels de modèle, l'exécution d'outils, exec, le traitement des webhooks/messages, l'assemblage du contexte et les boucles d'outils.           |
| **Journaux**    | Enregistrements structurés `logging.file` exportés via OTLP lorsque `diagnostics.otel.logs` est activé.                                                                                     |

Basculez `traces`, `metrics` et `logs` indépendamment. Les trois sont activés
par défaut lorsque `diagnostics.otel.enabled` est true.

## Référence de configuration

```json5
{
  diagnostics: {
    enabled: true,
    otel: {
      enabled: true,
      endpoint: "http://otel-collector:4318",
      protocol: "http/protobuf", // grpc is ignored
      serviceName: "openclaw-gateway",
      headers: { "x-collector-token": "..." },
      traces: true,
      metrics: true,
      logs: true,
      sampleRate: 0.2, // root-span sampler, 0.0..1.0
      flushIntervalMs: 60000, // metric export interval (min 1000ms)
      captureContent: {
        enabled: false,
        inputMessages: false,
        outputMessages: false,
        toolInputs: false,
        toolOutputs: false,
        systemPrompt: false,
      },
    },
  },
}
```

### Variables d'environnement

| Variable                        | Objectif                                                                                                                                                                                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OTEL_EXPORTER_OTLP_ENDPOINT`   | Remplace `diagnostics.otel.endpoint`. Si la valeur contient déjà `/v1/traces`, `/v1/metrics` ou `/v1/logs`, elle est utilisée telle quelle.                                                                                                          |
| `OTEL_SERVICE_NAME`             | Remplace `diagnostics.otel.serviceName`.                                                                                                                                                                                                   |
| `OTEL_EXPORTER_OTLP_PROTOCOL`   | Remplace le protocole de transmission (seul `http/protobuf` est honoré aujourd'hui).                                                                                                                                                        |
| `OTEL_SEMCONV_STABILITY_OPT_IN` | Définissez sur `gen_ai_latest_experimental` pour émettre le dernier attribut de span GenAI expérimental (`gen_ai.provider.name`) au lieu du `gen_ai.system` hérité. Les métriques GenAI utilisent toujours des attributs sémantiques bornés et de faible cardinalité indépendamment. |
| `OPENCLAW_OTEL_PRELOADED`       | Définissez sur `1` lorsqu'un autre préchargement ou processus hôte a déjà enregistré le SDK OpenTelemetry global. Le plugin ignore alors son propre cycle de vie NodeSDK mais câble toujours les écouteurs de diagnostic et honore `traces`/`metrics`/`logs`.                |

## Confidentialité et capture de contenu

Le contenu brut du modèle/outil n'est **pas** exporté par défaut. Les spans
portent des identifiants bornés (canal, fournisseur, modèle, catégorie d'erreur,
IDs de requête basés sur hash uniquement) et n'incluent jamais le texte de
l'invite, le texte de réponse, les entrées d'outils, les sorties d'outils ou
les clés de session.

Définissez `diagnostics.otel.captureContent.*` sur `true` uniquement lorsque
votre collecteur et votre politique de rétention sont approuvés pour le texte
d'invite, de réponse, d'outil ou de système-prompt. Chaque sous-clé est
opt-in indépendamment :

- `inputMessages` — contenu de l'invite utilisateur.
- `outputMessages` — contenu de la réponse du modèle.
- `toolInputs` — charges utiles des arguments d'outil.
- `toolOutputs` — charges utiles des résultats d'outil.
- `systemPrompt` — invite système/développeur assemblée.

Lorsqu'une sous-clé est activée, les spans de modèle et d'outil obtiennent
des attributs `openclaw.content.*` bornés et édités pour cette classe uniquement.

## Échantillonnage et vidage

- **Traces :** `diagnostics.otel.sampleRate` (root-span uniquement, `0.0`
  supprime tout, `1.0` conserve tout).
- **Métriques :** `diagnostics.otel.flushIntervalMs` (minimum `1000`).
- **Journaux :** Les journaux OTLP respectent `logging.level` (niveau de
  journalisation des fichiers). La rédaction de la console ne s'applique
  **pas** aux journaux OTLP. Les installations à haut volume devraient
  préférer l'échantillonnage/filtrage du collecteur OTLP à l'échantillonnage local.

## Métriques exportées

### Utilisation du modèle

- `openclaw.tokens` (compteur, attrs: `openclaw.token`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
- `openclaw.cost.usd` (compteur, attrs: `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
- `openclaw.run.duration_ms` (histogramme, attrs: `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
- `openclaw.context.tokens` (histogramme, attrs: `openclaw.context`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`)
- `gen_ai.client.token.usage` (histogramme, métrique de conventions sémantiques GenAI, attrs: `gen_ai.token.type` = `input`/`output`, `gen_ai.provider.name`, `gen_ai.operation.name`, `gen_ai.request.model`)
- `gen_ai.client.operation.duration` (histogramme, secondes, métrique de conventions sémantiques GenAI, attrs: `gen_ai.provider.name`, `gen_ai.operation.name`, `gen_ai.request.model`, `error.type` optionnel)

### Flux de messages

- `openclaw.webhook.received` (compteur, attrs: `openclaw.channel`, `openclaw.webhook`)
- `openclaw.webhook.error` (compteur, attrs: `openclaw.channel`, `openclaw.webhook`)
- `openclaw.webhook.duration_ms` (histogramme, attrs: `openclaw.channel`, `openclaw.webhook`)
- `openclaw.message.queued` (compteur, attrs: `openclaw.channel`, `openclaw.source`)
- `openclaw.message.processed` (compteur, attrs: `openclaw.channel`, `openclaw.outcome`)
- `openclaw.message.duration_ms` (histogramme, attrs: `openclaw.channel`, `openclaw.outcome`)
- `openclaw.message.delivery.started` (compteur, attrs: `openclaw.channel`, `openclaw.delivery.kind`)
- `openclaw.message.delivery.duration_ms` (histogramme, attrs: `openclaw.channel`, `openclaw.delivery.kind`, `openclaw.outcome`, `openclaw.errorCategory`)

### Files d'attente et sessions

- `openclaw.queue.lane.enqueue` (compteur, attrs: `openclaw.lane`)
- `openclaw.queue.lane.dequeue` (compteur, attrs: `openclaw.lane`)
- `openclaw.queue.depth` (histogramme, attrs: `openclaw.lane` ou `openclaw.channel=heartbeat`)
- `openclaw.queue.wait_ms` (histogramme, attrs: `openclaw.lane`)
- `openclaw.session.state` (compteur, attrs: `openclaw.state`, `openclaw.reason`)
- `openclaw.session.stuck` (compteur, attrs: `openclaw.state`)
- `openclaw.session.stuck_age_ms` (histogramme, attrs: `openclaw.state`)
- `openclaw.run.attempt` (compteur, attrs: `openclaw.attempt`)

### Exec

- `openclaw.exec.duration_ms` (histogramme, attrs: `openclaw.exec.target`, `openclaw.exec.mode`, `openclaw.outcome`, `openclaw.failureKind`)

### Diagnostics internes (mémoire et boucle d'outils)

- `openclaw.memory.heap_used_bytes` (histogramme, attrs: `openclaw.memory.kind`)
- `openclaw.memory.rss_bytes` (histogramme)
- `openclaw.memory.pressure` (compteur, attrs: `openclaw.memory.level`)
- `openclaw.tool.loop.iterations` (compteur, attrs: `openclaw.toolName`, `openclaw.outcome`)
- `openclaw.tool.loop.duration_ms` (histogramme, attrs: `openclaw.toolName`, `openclaw.outcome`)

## Spans exportés

- `openclaw.model.usage`
  - `openclaw.channel`, `openclaw.provider`, `openclaw.model`
  - `openclaw.tokens.*` (input/output/cache_read/cache_write/total)
  - `gen_ai.system` par défaut, ou `gen_ai.provider.name` lorsque les dernières conventions sémantiques GenAI sont activées
  - `gen_ai.request.model`, `gen_ai.operation.name`, `gen_ai.usage.*`
- `openclaw.run`
  - `openclaw.outcome`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`, `openclaw.errorCategory`
- `openclaw.model.call`
  - `gen_ai.system` par défaut, ou `gen_ai.provider.name` lorsque les dernières conventions sémantiques GenAI sont activées
  - `gen_ai.request.model`, `gen_ai.operation.name`, `openclaw.provider`, `openclaw.model`, `openclaw.api`, `openclaw.transport`
  - `openclaw.provider.request_id_hash` (hash basé sur SHA borné de l'ID de requête du fournisseur en amont ; les IDs bruts ne sont pas exportés)
- `openclaw.tool.execution`
  - `gen_ai.tool.name`, `openclaw.toolName`, `openclaw.errorCategory`, `openclaw.tool.params.*`
- `openclaw.exec`
  - `openclaw.exec.target`, `openclaw.exec.mode`, `openclaw.outcome`, `openclaw.failureKind`, `openclaw.exec.command_length`, `openclaw.exec.exit_code`, `openclaw.exec.timed_out`
- `openclaw.webhook.processed`
  - `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`
- `openclaw.webhook.error`
  - `openclaw.channel`, `openclaw.webhook`, `openclaw.chatId`, `openclaw.error`
- `openclaw.message.processed`
  - `openclaw.channel`, `openclaw.outcome`, `openclaw.chatId`, `openclaw.messageId`, `openclaw.reason`
- `openclaw.message.delivery`
  - `openclaw.channel`, `openclaw.delivery.kind`, `openclaw.outcome`, `openclaw.errorCategory`, `openclaw.delivery.result_count`
- `openclaw.session.stuck`
  - `openclaw.state`, `openclaw.ageMs`, `openclaw.queueDepth`
- `openclaw.context.assembled`
  - `openclaw.prompt.size`, `openclaw.history.size`, `openclaw.context.tokens`, `openclaw.errorCategory` (pas de contenu d'invite, d'historique, de réponse ou de clé de session)
- `openclaw.tool.loop`
  - `openclaw.toolName`, `openclaw.outcome`, `openclaw.iterations`, `openclaw.errorCategory` (pas de messages de boucle, de paramètres ou de sortie d'outil)
- `openclaw.memory.pressure`
  - `openclaw.memory.level`, `openclaw.memory.heap_used_bytes`, `openclaw.memory.rss_bytes`

Lorsque la capture de contenu est explicitement activée, les spans de modèle
et d'outil peuvent également inclure des attributs `openclaw.content.*` bornés
et édités pour les classes de contenu spécifiques pour lesquelles vous avez
opté.

## Catalogue d'événements de diagnostic

Les événements ci-dessous soutiennent les métriques et les spans ci-dessus. Les plugins peuvent également s'y abonner directement sans export OTLP.

**Utilisation du modèle**

- `model.usage` — tokens, coût, durée, contexte, fournisseur/modèle/canal,
  identifiants de session. `usage` est la comptabilité fournisseur/tour pour le coût et la télémétrie ;
  `context.used` est l'instantané actuel du prompt/contexte et peut être inférieur à
  `usage.total` du fournisseur lorsque des entrées mises en cache ou des appels de boucle d'outils sont impliqués.

**Flux de messages**

- `webhook.received` / `webhook.processed` / `webhook.error`
- `message.queued` / `message.processed`
- `message.delivery.started` / `message.delivery.completed` / `message.delivery.error`

**File d'attente et session**

- `queue.lane.enqueue` / `queue.lane.dequeue`
- `session.state` / `session.stuck`
- `run.attempt`
- `diagnostic.heartbeat` (compteurs agrégés : webhooks/queue/session)

**Exec**

- `exec.process.completed` — résultat terminal, durée, cible, mode, code de sortie
  et type d'échec. Le texte de la commande et les répertoires de travail ne sont pas
  inclus.

## Sans exportateur

Vous pouvez garder les événements de diagnostic disponibles pour les plugins ou les récepteurs personnalisés sans
exécuter `diagnostics-otel` :

```json5
{
  diagnostics: { enabled: true },
}
```

Pour une sortie de débogage ciblée sans augmenter `logging.level`, utilisez les drapeaux de diagnostic. Les drapeaux ne sont pas sensibles à la casse et supportent les caractères génériques (par exemple `telegram.*` ou
`*`) :

```json5
{
  diagnostics: { flags: ["telegram.http"] },
}
```

Ou comme un remplacement d'env ponctuel :

```bash
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload openclaw gateway
```

La sortie des drapeaux va au fichier journal standard (`logging.file`) et est toujours
expurgée par `logging.redactSensitive`. Guide complet :
[Drapeaux de diagnostic](/fr/diagnostics/flags).

## Désactiver

```json5
{
  diagnostics: { otel: { enabled: false } },
}
```

Vous pouvez également laisser `diagnostics-otel` en dehors de `plugins.allow`, ou exécuter
`openclaw plugins disable diagnostics-otel`.

## Connexes

- [Journalisation](/fr/logging) — journaux de fichiers, sortie console, suivi CLI et onglet Logs de l'interface utilisateur de contrôle
- [Internals de journalisation de passerelle](/fr/gateway/logging) — styles de journal WS, préfixes de sous-système et capture de console
- [Drapeaux de diagnostic](/fr/diagnostics/flags) — drapeaux de journal de débogage ciblés
- [Export de diagnostic](/fr/gateway/diagnostics) — outil de bundle de support d'opérateur (séparé de l'export OTEL)
- [Référence de configuration](/fr/gateway/configuration-reference#diagnostics) — référence complète du champ `diagnostics.*`
