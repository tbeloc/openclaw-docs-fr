---
read_when:
  - 将 Gmail 收件箱触发器接入 OpenClaw
  - 为智能体唤醒设置 Pub/Sub 推送
summary: 通过 gogcli 将 Gmail Pub/Sub 推送接入 OpenClaw webhooks
title: Gmail PubSub
x-i18n:
  generated_at: "2026-02-03T07:43:25Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: dfb92133b69177e4e984b7d072f5dc28aa53a9e0cf984a018145ed811aa96195
  source_path: automation/gmail-pubsub.md
  workflow: 15
---

# Gmail Pub/Sub -> OpenClaw

Objectif : Gmail watch -> Pub/Sub push -> `gog gmail watch serve` -> OpenClaw webhook.

## Prérequis

- `gcloud` installé et authentifié ([guide d'installation](https://docs.cloud.google.com/sdk/docs/install-sdk)).
- `gog` (gogcli) installé et autorisé pour votre compte Gmail ([gogcli.sh](https://gogcli.sh/)).
- OpenClaw hooks activés (voir [Webhooks](/automation/webhook)).
- Authentifié sur `tailscale` ([tailscale.com](https://tailscale.com/)). La configuration supportée utilise Tailscale Funnel comme point de terminaison HTTPS public.
  D'autres services de tunnel peuvent être utilisés, mais nécessitent une configuration manuelle/ne sont pas supportés et doivent être intégrés manuellement.
  Actuellement, nous supportons Tailscale.

Exemple de configuration hook (avec mappage de préset Gmail activé) :

```json5
{
  hooks: {
    enabled: true,
    token: "OPENCLAW_HOOK_TOKEN",
    path: "/hooks",
    presets: ["gmail"],
  },
}
```

Pour livrer les résumés Gmail à l'interface de chat, remplacez le préset avec un mappage configuré avec `deliver` et optionnellement `channel`/`to` :

```json5
{
  hooks: {
    enabled: true,
    token: "OPENCLAW_HOOK_TOKEN",
    presets: ["gmail"],
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "New email from {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}\n{{messages[0].body}}",
        model: "openai/gpt-5.2-mini",
        deliver: true,
        channel: "last",
        // to: "+15551234567"
      },
    ],
  },
}
```

Si vous souhaitez utiliser un canal fixe, définissez `channel` + `to`. Sinon, `channel: "last"` utilisera la dernière route de livraison (par défaut, retour à WhatsApp).

Pour forcer l'utilisation d'un modèle moins cher pour Gmail, définissez `model` dans le mappage (`provider/model` ou alias). Si vous avez forcé `agents.defaults.models`, incluez-le.

Pour définir le modèle par défaut et le niveau de réflexion spécifiquement pour les hooks Gmail, ajoutez `hooks.gmail.model` / `hooks.gmail.thinking` à votre configuration :

```json5
{
  hooks: {
    gmail: {
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      thinking: "off",
    },
  },
}
```

Remarques :

- `model`/`thinking` pour chaque hook dans les mappages remplacent toujours ces valeurs par défaut.
- Ordre de secours : `hooks.gmail.model` → `agents.defaults.model.fallbacks` → modèle principal (authentification/limite de débit/délai d'expiration).
- Si `agents.defaults.models` est défini, le modèle Gmail doit être dans la liste d'autorisation.
- Le contenu du hook Gmail est enveloppé par défaut avec une limite de sécurité du contenu externe.
  Pour désactiver (dangereux), définissez `hooks.gmail.allowUnsafeExternalContent: true`.

Pour personnaliser davantage le traitement des charges utiles, ajoutez `hooks.mappings` ou des modules de transformation JS/TS sous `hooks.transformsDir` (voir [Webhooks](/automation/webhook)).

## Assistant (recommandé)

Utilisez l'assistant OpenClaw pour tout connecter (installez les dépendances via brew sur macOS) :

```bash
openclaw webhooks gmail setup \
  --account openclaw@gmail.com
```

Paramètres par défaut :

- Utilise Tailscale Funnel comme point de terminaison push public.
- Écrit la configuration `hooks.gmail` pour `openclaw webhooks gmail run`.
- Active le préset hook Gmail (`hooks.presets: ["gmail"]`).

Remarque sur les chemins : Lorsque `tailscale.mode` est activé, OpenClaw définit automatiquement `hooks.gmail.serve.path` sur `/` et maintient le chemin public dans `hooks.gmail.tailscale.path` (par défaut `/gmail-pubsub`), car Tailscale supprime le préfixe de chemin défini avant le proxy.
Si vous avez besoin que le backend reçoive le chemin avec le préfixe, définissez `hooks.gmail.tailscale.target` (ou `--tailscale-target`) sur l'URL complète, comme `http://127.0.0.1:8788/gmail-pubsub`, et faites correspondre `hooks.gmail.serve.path`.

Vous voulez personnaliser le point de terminaison ? Utilisez `--push-endpoint <url>` ou `--tailscale off`.

Remarque sur les plateformes : Sur macOS, l'assistant installe `gcloud`, `gogcli` et `tailscale` via Homebrew ; sur Linux, veuillez les installer manuellement d'abord.

Démarrage automatique de la passerelle (recommandé) :

- Lorsque `hooks.enabled=true` et `hooks.gmail.account` est défini, la passerelle exécute `gog gmail watch serve` au démarrage et renouvelle automatiquement la surveillance.
- Définissez `OPENCLAW_SKIP_GMAIL_WATCHER=1` pour refuser (utile si vous exécutez vous-même un daemon).
- N'exécutez pas simultanément un daemon manuel, sinon vous obtiendrez `listen tcp 127.0.0.1:8788: bind: address already in use`.

Daemon manuel (démarrer `gog gmail watch serve` + renouvellement automatique) :

```bash
openclaw webhooks gmail run
```

## Configuration unique

1. Sélectionnez le **projet GCP qui possède le client OAuth utilisé par `gog`**.

```bash
gcloud auth login
gcloud config set project <project-id>
```

Remarque : Gmail watch nécessite que le sujet Pub/Sub soit dans le même projet que le client OAuth.

2. Activez les API :

```bash
gcloud services enable gmail.googleapis.com pubsub.googleapis.com
```

3. Créez un sujet :

```bash
gcloud pubsub topics create gog-gmail-watch
```

4. Autorisez Gmail à publier :

```bash
gcloud pubsub topics add-iam-policy-binding gog-gmail-watch \
  --member=serviceAccount:gmail-api-push@system.gserviceaccount.com \
  --role=roles/pubsub.publisher
```

## Démarrer la surveillance

```bash
gog gmail watch start \
  --account openclaw@gmail.com \
  --label INBOX \
  --topic projects/<project-id>/topics/gog-gmail-watch
```

Enregistrez le `history_id` de la sortie (utile pour le débogage).

## Exécuter le gestionnaire push

Exemple local (authentification par token partagé) :

```bash
gog gmail watch serve \
  --account openclaw@gmail.com \
  --bind 127.0.0.1 \
  --port 8788 \
  --path /gmail-pubsub \
  --token <shared> \
  --hook-url http://127.0.0.1:18789/hooks/gmail \
  --hook-token OPENCLAW_HOOK_TOKEN \
  --include-body \
  --max-bytes 20000
```

Remarques :

- `--token` sécurise le point de terminaison push (`x-gog-token` ou `?token=`).
- `--hook-url` pointe vers `/hooks/gmail` d'OpenClaw (mappé ; exécution isolée + résumé envoyé au thread principal).
- `--include-body` et `--max-bytes` contrôlent les fragments de corps envoyés à OpenClaw.

Recommandé : `openclaw webhooks gmail run` encapsule le même processus et renouvelle automatiquement la surveillance.

## Exposer le gestionnaire (avancé, non supporté)

Si vous avez besoin d'un tunnel non-Tailscale, intégrez manuellement et utilisez une URL publique dans l'abonnement push (non supporté, sans protections) :

```bash
cloudflared tunnel --url http://127.0.0.1:8788 --no-autoupdate
```

Utilisez l'URL générée comme point de terminaison push :

```bash
gcloud pubsub subscriptions create gog-gmail-watch-push \
  --topic gog-gmail-watch \
  --push-endpoint "https://<public-url>/gmail-pubsub?token=<shared>"
```

Production : Utilisez un point de terminaison HTTPS stable et configurez Pub/Sub OIDC JWT, puis exécutez :

```bash
gog gmail watch serve --verify-oidc --oidc-email <svc@...>
```

## Test

Envoyez un message à la boîte de réception surveillée :

```bash
gog gmail send \
  --account openclaw@gmail.com \
  --to openclaw@gmail.com \
  --subject "watch test" \
  --body "ping"
```

Vérifiez l'état et l'historique de la surveillance :

```bash
gog gmail watch status --account openclaw@gmail.com
gog gmail history --account openclaw@gmail.com --since <historyId>
```

## Dépannage

- `Invalid topicName` : Les projets ne correspondent pas (le sujet n'est pas dans le projet du client OAuth).
- `User not authorized` : Le sujet manque `roles/pubsub.publisher`.
- Messages vides : Gmail push fournit uniquement `historyId` ; récupérez-le via `gog gmail history`.

## Nettoyage

```bash
gog gmail watch stop --account openclaw@gmail.com
gcloud pubsub subscriptions delete gog-gmail-watch-push
gcloud pubsub topics delete gog-gmail-watch
```
