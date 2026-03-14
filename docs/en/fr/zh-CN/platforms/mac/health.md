---
read_when:
  - 调试 Mac 应用健康指示器
summary: macOS 应用如何报告 Gateway 网关/Baileys 健康状态
title: 健康检查
x-i18n:
  generated_at: "2026-02-03T07:52:40Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0560e96501ddf53a499f8960cfcf11c2622fcb9056bfd1bcc57876e955cab03d
  source_path: platforms/mac/health.md
  workflow: 15
---

# Vérification de santé sur macOS

Comment vérifier depuis l'application de barre de menu si les canaux associés sont sains.

## Barre de menu

- Le point d'état reflète désormais l'état de santé de Baileys :
  - Vert : associé + socket ouvert récemment.
  - Orange : connexion/nouvelle tentative en cours.
  - Rouge : déconnecté ou échec de la sonde.
- La deuxième ligne affiche « linked · auth 12m » ou affiche la raison de l'échec.
- L'élément de menu « Run Health Check » déclenche une sonde à la demande.

## Paramètres

- L'onglet Général contient une nouvelle carte de santé affichant : heure d'authentification associée, chemin/nombre de stockage de session, heure de la dernière vérification, dernier code d'erreur/statut, ainsi que les boutons Exécuter la vérification de santé/Afficher les journaux.
- Utilise un snapshot en cache, donc l'interface utilisateur se charge immédiatement et se dégrade gracieusement hors ligne.
- **L'onglet Canaux** affiche l'état du canal + contrôles pour WhatsApp/Telegram (code QR de connexion, déconnexion, sonde, dernière déconnexion/erreur).

## Fonctionnement de la sonde

- L'application exécute `openclaw health --json` via `ShellExecutor` environ toutes les 60 secondes et à la demande. La sonde charge les identifiants et rapporte l'état sans envoyer de messages.
- Met en cache séparément le dernier snapshot réussi et la dernière erreur pour éviter le scintillement ; affiche l'horodatage de chacun.

## En cas de doute

- Vous pouvez toujours utiliser les processus CLI de [Santé de la passerelle](/gateway/health) (`openclaw status`, `openclaw status --deep`, `openclaw health --json`), et suivre `web-heartbeat` / `web-reconnect` dans `/tmp/openclaw/openclaw-*.log`.
