---
summary: "Plugin Webhooks : ingress TaskFlow authentifié pour l'automatisation externe de confiance"
read_when:
  - You want to trigger or drive TaskFlows from an external system
  - You are configuring the bundled webhooks plugin
title: "Plugin Webhooks"
---

# Webhooks (plugin)

Le plugin Webhooks ajoute des routes HTTP authentifiées qui lient l'automatisation externe aux TaskFlows OpenClaw.

Utilisez-le quand vous voulez qu'un système de confiance tel que Zapier, n8n, un job CI, ou un service interne crée et pilote des TaskFlows gérés sans écrire d'abord un plugin personnalisé.

## Où il s'exécute

Le plugin Webhooks s'exécute à l'intérieur du processus Gateway.

Si votre Gateway s'exécute sur une autre machine, installez et configurez le plugin sur cet hôte Gateway, puis redémarrez le Gateway.

## Configurer les routes

Définissez la configuration sous `plugins.entries.webhooks.config` :

```json5
{
  plugins: {
    entries: {
      webhooks: {
        enabled: true,
        config: {
          routes: {
            zapier: {
              path: "/plugins/webhooks/zapier",
              sessionKey: "agent:main:main",
              secret: {
                source: "env",
                provider: "default",
                id: "OPENCLAW_WEBHOOK_SECRET",
              },
              controllerId: "webhooks/zapier",
              description: "Zapier TaskFlow bridge",
            },
          },
        },
      },
    },
  },
}
```

Champs de route :

- `enabled` : optionnel, par défaut `true`
- `path` : optionnel, par défaut `/plugins/webhooks/<routeId>`
- `sessionKey` : session requise qui possède les TaskFlows liés
- `secret` : secret partagé requis ou SecretRef
- `controllerId` : identifiant de contrôleur optionnel pour les flux gérés créés
- `description` : note d'opérateur optionnelle

Entrées `secret` supportées :

- Chaîne de caractères simple
- SecretRef avec `source: "env" | "file" | "exec"`

Si une route soutenue par un secret ne peut pas résoudre son secret au démarrage, le plugin ignore cette route et enregistre un avertissement au lieu d'exposer un endpoint cassé.

## Modèle de sécurité

Chaque route est de confiance pour agir avec l'autorité TaskFlow de sa `sessionKey` configurée.

Cela signifie que la route peut inspecter et muter les TaskFlows possédés par cette session, donc vous devriez :

- Utiliser un secret unique et fort par route
- Préférer les références de secret aux secrets en texte brut intégré
- Lier les routes à la session la plus étroite qui convient au flux de travail
- Exposer uniquement le chemin webhook spécifique dont vous avez besoin

Le plugin applique :

- Authentification par secret partagé
- Gardes de taille de corps de requête et de délai d'expiration
- Limitation de débit à fenêtre fixe
- Limitation des requêtes en vol
- Accès TaskFlow lié au propriétaire via `api.runtime.taskFlow.bindSession(...)`

## Format de requête

Envoyez des requêtes `POST` avec :

- `Content-Type: application/json`
- `Authorization: Bearer <secret>` ou `x-openclaw-webhook-secret: <secret>`

Exemple :

```bash
curl -X POST https://gateway.example.com/plugins/webhooks/zapier \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_SHARED_SECRET' \
  -d '{"action":"create_flow","goal":"Review inbound queue"}'
```

## Actions supportées

Le plugin accepte actuellement ces valeurs JSON `action` :

- `create_flow`
- `get_flow`
- `list_flows`
- `find_latest_flow`
- `resolve_flow`
- `get_task_summary`
- `set_waiting`
- `resume_flow`
- `finish_flow`
- `fail_flow`
- `request_cancel`
- `cancel_flow`
- `run_task`

### `create_flow`

Crée un TaskFlow géré pour la session liée de la route.

Exemple :

```json
{
  "action": "create_flow",
  "goal": "Review inbound queue",
  "status": "queued",
  "notifyPolicy": "done_only"
}
```

### `run_task`

Crée une tâche enfant gérée à l'intérieur d'un TaskFlow géré existant.

Les runtimes autorisés sont :

- `subagent`
- `acp`

Exemple :

```json
{
  "action": "run_task",
  "flowId": "flow_123",
  "runtime": "acp",
  "childSessionKey": "agent:main:acp:worker",
  "task": "Inspect the next message batch"
}
```

## Forme de réponse

Les réponses réussies retournent :

```json
{
  "ok": true,
  "routeId": "zapier",
  "result": {}
}
```

Les requêtes rejetées retournent :

```json
{
  "ok": false,
  "routeId": "zapier",
  "code": "not_found",
  "error": "TaskFlow not found.",
  "result": {}
}
```

Le plugin efface intentionnellement les métadonnées de propriétaire/session des réponses webhook.

## Documentation connexe

- [Plugin runtime SDK](/fr/plugins/sdk-runtime)
- [Hooks and webhooks overview](/fr/automation/hooks)
- [CLI webhooks](/fr/cli/webhooks)
