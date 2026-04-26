---
summary: "Exposer les diagnostics OpenClaw en tant que métriques texte Prometheus via le plugin diagnostics-prometheus"
title: "Métriques Prometheus"
sidebarTitle: "Prometheus"
read_when:
  - You want Prometheus, Grafana, VictoriaMetrics, or another scraper to collect OpenClaw Gateway metrics
  - You need the Prometheus metric names and label policy for dashboards or alerts
  - You want metrics without running an OpenTelemetry collector
---

OpenClaw peut exposer les métriques de diagnostics via le plugin `diagnostics-prometheus` fourni. Il écoute les diagnostics internes de confiance et rend un point de terminaison texte Prometheus à :

```text
GET /api/diagnostics/prometheus
```

Le type de contenu est `text/plain; version=0.0.4; charset=utf-8`, le format d'exposition Prometheus standard.

<Warning>
La route utilise l'authentification Gateway (portée opérateur). Ne l'exposez pas comme un point de terminaison public non authentifié `/metrics`. Récupérez-le via le même chemin d'authentification que vous utilisez pour les autres API opérateur.
</Warning>

Pour les traces, les journaux, la transmission OTLP et les attributs sémantiques OpenTelemetry GenAI, voir [Exportation OpenTelemetry](/fr/gateway/opentelemetry).

## Démarrage rapide

<Steps>
  <Step title="Activer le plugin">
    <Tabs>
      <Tab title="Config">
        ```json5
        {
          plugins: {
            allow: ["diagnostics-prometheus"],
            entries: {
              "diagnostics-prometheus": { enabled: true },
            },
          },
          diagnostics: {
            enabled: true,
          },
        }
        ```
      </Tab>
      <Tab title="CLI">
        ```bash
        openclaw plugins enable diagnostics-prometheus
        ```
      </Tab>
    </Tabs>
  </Step>
  <Step title="Redémarrer la Gateway">
    La route HTTP est enregistrée au démarrage du plugin, donc rechargez après activation.
  </Step>
  <Step title="Récupérer la route protégée">
    Envoyez la même authentification gateway que vos clients opérateur utilisent :

    ```bash
    curl -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
      http://127.0.0.1:18789/api/diagnostics/prometheus
    ```

  </Step>
  <Step title="Configurer Prometheus">
    ```yaml
    # prometheus.yml
    scrape_configs:
      - job_name: openclaw
        scrape_interval: 30s
        metrics_path: /api/diagnostics/prometheus
        authorization:
          credentials_file: /etc/prometheus/openclaw-gateway-token
        static_configs:
          - targets: ["openclaw-gateway:18789"]
    ```
  </Step>
</Steps>

<Note>
`diagnostics.enabled: true` est requis. Sans cela, le plugin enregistre toujours la route HTTP mais aucun événement de diagnostic ne circule dans l'exportateur, donc la réponse est vide.
</Note>

## Métriques exportées

| Métrique                                      | Type      | Étiquettes                                                                                |
| --------------------------------------------- | --------- | ----------------------------------------------------------------------------------------- |
| `openclaw_run_completed_total`                | counter   | `channel`, `model`, `outcome`, `provider`, `trigger`                                      |
| `openclaw_run_duration_seconds`               | histogram | `channel`, `model`, `outcome`, `provider`, `trigger`                                      |
| `openclaw_model_call_total`                   | counter   | `api`, `error_category`, `model`, `outcome`, `provider`, `transport`                      |
| `openclaw_model_call_duration_seconds`        | histogram | `api`, `error_category`, `model`, `outcome`, `provider`, `transport`                      |
| `openclaw_model_tokens_total`                 | counter   | `agent`, `channel`, `model`, `provider`, `token_type`                                     |
| `openclaw_gen_ai_client_token_usage`          | histogram | `model`, `provider`, `token_type`                                                         |
| `openclaw_model_cost_usd_total`               | counter   | `agent`, `channel`, `model`, `provider`                                                   |
| `openclaw_tool_execution_total`               | counter   | `error_category`, `outcome`, `params_kind`, `tool`                                        |
| `openclaw_tool_execution_duration_seconds`    | histogram | `error_category`, `outcome`, `params_kind`, `tool`                                        |
| `openclaw_harness_run_total`                  | counter   | `channel`, `error_category`, `harness`, `model`, `outcome`, `phase`, `plugin`, `provider` |
| `openclaw_harness_run_duration_seconds`       | histogram | `channel`, `error_category`, `harness`, `model`, `outcome`, `phase`, `plugin`, `provider` |
| `openclaw_message_processed_total`            | counter   | `channel`, `outcome`, `reason`                                                            |
| `openclaw_message_processed_duration_seconds` | histogram | `channel`, `outcome`, `reason`                                                            |
| `openclaw_message_delivery_total`             | counter   | `channel`, `delivery_kind`, `error_category`, `outcome`                                   |
| `openclaw_message_delivery_duration_seconds`  | histogram | `channel`, `delivery_kind`, `error_category`, `outcome`                                   |
| `openclaw_queue_lane_size`                    | gauge     | `lane`                                                                                    |
| `openclaw_queue_lane_wait_seconds`            | histogram | `lane`                                                                                    |
| `openclaw_session_state_total`                | counter   | `reason`, `state`                                                                         |
| `openclaw_session_queue_depth`                | gauge     | `state`                                                                                   |
| `openclaw_memory_bytes`                       | gauge     | `kind`                                                                                    |
| `openclaw_memory_rss_bytes`                   | histogram | aucun                                                                                     |
| `openclaw_memory_pressure_total`              | counter   | `level`, `reason`                                                                         |
| `openclaw_telemetry_exporter_total`           | counter   | `exporter`, `reason`, `signal`, `status`                                                  |
| `openclaw_prometheus_series_dropped_total`    | counter   | aucun                                                                                     |

## Politique d'étiquetage

<AccordionGroup>
  <Accordion title="Étiquettes bornées et de faible cardinalité">
    Les étiquettes Prometheus restent bornées et de faible cardinalité. L'exportateur n'émet pas d'identifiants de diagnostic bruts tels que `runId`, `sessionKey`, `sessionId`, `callId`, `toolCallId`, les ID de message, les ID de chat ou les ID de requête du fournisseur.

    Les valeurs d'étiquette sont expurgées et doivent correspondre à la politique de caractères de faible cardinalité d'OpenClaw. Les valeurs qui ne respectent pas la politique sont remplacées par `unknown`, `other` ou `none`, selon la métrique.

  </Accordion>
  <Accordion title="Plafond de séries et comptabilité de débordement">
    L'exportateur plafonne les séries temporelles conservées en mémoire à **2048** séries dans les compteurs, jauges et histogrammes combinés. Les nouvelles séries au-delà de ce plafond sont supprimées, et `openclaw_prometheus_series_dropped_total` s'incrémente d'un à chaque fois.

    Surveillez ce compteur comme un signal dur qu'un attribut en amont fuit des valeurs de haute cardinalité. L'exportateur ne relève jamais le plafond automatiquement ; s'il augmente, corrigez la source plutôt que de désactiver le plafond.

  </Accordion>
  <Accordion title="Ce qui n'apparaît jamais dans la sortie Prometheus">
    - texte d'invite, texte de réponse, entrées d'outil, sorties d'outil, invites système
    - ID de requête de fournisseur bruts (uniquement des hachages bornés, le cas échéant, sur les spans — jamais sur les métriques)
    - clés de session et ID de session
    - noms d'hôte, chemins de fichiers, valeurs secrètes
  </Accordion>
</AccordionGroup>

## Recettes PromQL

```promql
# Jetons par minute, divisés par fournisseur
sum by (provider) (rate(openclaw_model_tokens_total[1m]))

# Dépenses (USD) au cours de la dernière heure, par modèle
sum by (model) (increase(openclaw_model_cost_usd_total[1h]))

# 95e percentile de la durée d'exécution du modèle
histogram_quantile(
  0.95,
  sum by (le, provider, model)
    (rate(openclaw_run_duration_seconds_bucket[5m]))
)

# SLO de temps d'attente en file d'attente (95p sous 2s)
histogram_quantile(
  0.95,
  sum by (le, lane) (rate(openclaw_queue_lane_wait_seconds_bucket[5m]))
) < 2

# Séries Prometheus supprimées (alarme de cardinalité)
increase(openclaw_prometheus_series_dropped_total[15m]) > 0
```

<Tip>
Préférez `gen_ai_client_token_usage` pour les tableaux de bord multi-fournisseurs : il suit les conventions sémantiques OpenTelemetry GenAI et est cohérent avec les métriques des services GenAI non-OpenClaw.
</Tip>

## Choisir entre l'exportation Prometheus et OpenTelemetry

OpenClaw supporte les deux surfaces indépendamment. Vous pouvez exécuter l'une, les deux ou aucune.

<Tabs>
  <Tab title="diagnostics-prometheus">
    - Modèle **Pull** : Prometheus récupère `/api/diagnostics/prometheus`.
    - Aucun collecteur externe requis.
    - Authentifié via l'authentification Gateway normale.
    - La surface est limitée aux métriques (pas de traces ou de journaux).
    - Idéal pour les piles déjà standardisées sur Prometheus + Grafana.
  </Tab>
  <Tab title="diagnostics-otel">
    - Modèle **Push** : OpenClaw envoie OTLP/HTTP à un collecteur ou un backend compatible OTLP.
    - La surface inclut les métriques, les traces et les journaux.
    - Bascule vers Prometheus via un Collecteur OpenTelemetry (exportateur `prometheus` ou `prometheusremotewrite`) quand vous avez besoin des deux.
    - Voir [Exportation OpenTelemetry](/fr/gateway/opentelemetry) pour le catalogue complet.
  </Tab>
</Tabs>

## Dépannage

<AccordionGroup>
  <Accordion title="Corps de réponse vide">
    - Vérifiez `diagnostics.enabled: true` dans la configuration.
    - Confirmez que le plugin est activé et chargé avec `openclaw plugins list --enabled`.
    - Générez du trafic ; les compteurs et histogrammes n'émettent des lignes qu'après au moins un événement.
  </Accordion>
  <Accordion title="401 / non autorisé">
    Le point de terminaison nécessite la portée opérateur Gateway (`auth: "gateway"` avec `gatewayRuntimeScopeSurface: "trusted-operator"`). Utilisez le même jeton ou mot de passe que Prometheus utilise pour toute autre route opérateur Gateway. Il n'y a pas de mode public non authentifié.
  </Accordion>
  <Accordion title="`openclaw_prometheus_series_dropped_total` augmente">
    Un nouvel attribut dépasse le plafond de **2048** séries. Inspectez les métriques récentes pour une étiquette de cardinalité anormalement élevée et corrigez-la à la source. L'exportateur supprime intentionnellement les nouvelles séries au lieu de réécrire silencieusement les étiquettes.
  </Accordion>
  <Accordion title="Prometheus affiche des séries obsolètes après un redémarrage">
    Le plugin ne conserve l'état qu'en mémoire. Après un redémarrage de la Gateway, les compteurs se réinitialisent à zéro et les jauges redémarrent à leur valeur suivante signalée. Utilisez PromQL `rate()` et `increase()` pour gérer les réinitialisations proprement.
  </Accordion>
</AccordionGroup>

## Connexes

- [Exportation de diagnostics](/fr/gateway/diagnostics) — zip de diagnostics locaux pour les bundles de support
- [Santé et disponibilité](/fr/gateway/health) — sondes `/healthz` et `/readyz`
- [Journalisation](/fr/logging) — journalisation basée sur fichier
- [Exportation OpenTelemetry](/fr/gateway/opentelemetry) — transmission OTLP pour les traces, métriques et journaux
