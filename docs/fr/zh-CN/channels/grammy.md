---
read_when:
  - Lors du développement de fonctionnalités liées à Telegram ou grammY
summary: Intégration de l'API Telegram Bot via grammY, avec instructions de configuration
title: grammY
x-i18n:
  generated_at: "2026-02-03T10:03:55Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: ea7ef23e6d77801f4ef5fc56685ef4470f79f5aecab448d644a72cbab53521b7
  source_path: channels/grammy.md
  workflow: 15
---

# Intégration grammY (API Telegram Bot)

# Pourquoi choisir grammY

- Client API Bot centré sur TypeScript, avec outils intégrés de long polling + webhook, middleware, gestion des erreurs et limiteur de débit.
- Les outils de traitement des médias sont plus simples que d'écrire manuellement fetch + FormData ; prend en charge toutes les méthodes de l'API Bot.
- Extensible : support des proxies via fetch personnalisé, middleware de session optionnel, contexte type-safe.

# Ce que nous avons publié

- **Chemin client unique :** suppression de l'implémentation basée sur fetch ; grammY est maintenant le seul client Telegram (envoi + passerelle Gateway), avec le throttler grammY activé par défaut.
- **Passerelle Gateway :** `monitorTelegramProvider` construit un `Bot` grammY, intègre le contrôle de passerelle mention/allowlist, télécharge les médias via `getFile`/`download`, et envoie les réponses avec `sendMessage/sendPhoto/sendVideo/sendAudio/sendDocument`. Support du long polling ou webhook via `webhookCallback`.
- **Proxy :** `channels.telegram.proxy` optionnel utilisant `undici.ProxyAgent` via `client.baseFetch` de grammY.
- **Support Webhook :** `webhook-set.ts` encapsule `setWebhook/deleteWebhook` ; `webhook.ts` héberge le callback, avec support des vérifications de santé et arrêt gracieux. La passerelle Gateway active le mode webhook lorsque `channels.telegram.webhookUrl` + `channels.telegram.webhookSecret` sont définis (sinon utilise le long polling).
- **Sessions :** les messages privés sont regroupés dans la session principale de l'agent (`agent:<agentId>:<mainKey>`) ; les groupes utilisent `agent:<agentId>:telegram:group:<chatId>` ; les réponses sont routées vers le même canal.
- **Options de configuration :** `channels.telegram.botToken`, `channels.telegram.dmPolicy`, `channels.telegram.groups` (valeurs par défaut allowlist + mention), `channels.telegram.allowFrom`, `channels.telegram.groupAllowFrom`, `channels.telegram.groupPolicy`, `channels.telegram.mediaMaxMb`, `channels.telegram.linkPreview`, `channels.telegram.proxy`, `channels.telegram.webhookSecret`, `channels.telegram.webhookUrl`.
- **Streaming de brouillons :** `channels.telegram.streamMode` optionnel utilisant `sendMessageDraft` dans les chats de sujets privés (Bot API 9.3+). Ceci est séparé du streaming par chunks du canal.
- **Tests :** les mocks grammY couvrent le contrôle de passerelle des messages privés + mentions de groupe et l'envoi sortant ; n'hésitez pas à ajouter d'autres cas de test pour les médias/webhooks.

Problèmes en attente

- En cas d'erreur Bot API 429, envisagez d'utiliser le plugin grammY optionnel (throttler).
- Ajouter plus de tests de médias structurés (autocollants, messages vocaux).
- Rendre le port d'écoute webhook configurable (actuellement fixé à 8787, sauf via la configuration de la passerelle Gateway).
