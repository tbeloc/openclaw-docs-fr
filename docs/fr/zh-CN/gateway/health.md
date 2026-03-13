---
read_when:
  - Diagnostiquer la santé du canal WhatsApp
summary: Étapes de vérification de santé pour la connexion du canal
title: Vérification de santé
x-i18n:
  generated_at: "2026-02-03T07:47:59Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 74f242e98244c135e1322682ed6b67d70f3b404aca783b1bb5de96a27c2c1b01
  source_path: gateway/health.md
  workflow: 15
---

# Vérification de santé (CLI)

Guide rapide pour vérifier la connexion du canal, sans deviner.

## Vérification rapide

- `openclaw status` — Résumé local : accessibilité/mode de la passerelle Gateway, conseils de mise à jour, durée d'authentification des canaux liés, sessions + activité récente.
- `openclaw status --all` — Diagnostic local complet (lecture seule, couleur, peut être collé en toute sécurité pour le débogage).
- `openclaw status --deep` — Sonde également la passerelle Gateway en cours d'exécution (sonde par canal si supportée).
- `openclaw health --json` — Demande un snapshot de santé complet à la passerelle Gateway en cours d'exécution (WS uniquement ; n'accède pas directement au socket Baileys).
- Envoyez un message `/status` seul dans WhatsApp/WebChat pour obtenir une réponse de statut sans invoquer l'agent.
- Journaux : suivez `/tmp/openclaw/openclaw-*.log` et filtrez `web-heartbeat`, `web-reconnect`, `web-auto-reply`, `web-inbound`.

## Diagnostic approfondi

- Identifiants sur disque : `ls -l ~/.openclaw/credentials/whatsapp/<accountId>/creds.json` (mtime devrait être récent).
- Stockage de session : `ls -l ~/.openclaw/agents/<agentId>/sessions/sessions.json` (le chemin peut être remplacé dans la configuration). Le nombre et les destinataires récents s'affichent via `status`.
- Flux de reconnexion : lorsque les codes de statut 409–515 ou `loggedOut` apparaissent dans les journaux, exécutez `openclaw channels logout && openclaw channels login --verbose`. (Remarque : le flux de connexion QR redémarre automatiquement une fois au statut 515 après l'appairage.)

## En cas de défaillance

- `logged out` ou statut 409–515 → Reconnectez-vous avec `openclaw channels logout` puis `openclaw channels login`.
- Passerelle Gateway inaccessible → Démarrez-la : `openclaw gateway --port 18789` (utilisez `--force` si le port est occupé).
- Pas de messages entrants → Confirmez que le téléphone lié est en ligne et que l'expéditeur est autorisé (`channels.whatsapp.allowFrom`) ; pour les groupes, assurez-vous que la liste d'autorisation + les règles de mention correspondent (`channels.whatsapp.groups`, `agents.list[].groupChat.mentionPatterns`).

## Commande "health" dédiée

`openclaw health --json` demande son snapshot de santé à la passerelle Gateway en cours d'exécution (le CLI n'accède pas directement aux sockets du canal). Elle rapporte les identifiants liés/durée d'authentification (si disponible), résumé de sonde par canal, résumé du stockage de session et durée de sonde. Si la passerelle Gateway est inaccessible ou si la sonde échoue/expire, elle se termine avec un code non nul. Utilisez `--timeout <ms>` pour remplacer le délai par défaut de 10 secondes.
