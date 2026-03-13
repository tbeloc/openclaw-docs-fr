---
read_when:
  - Déboguer les invites de permissions macOS manquantes ou bloquées
  - Empaqueter ou signer une application macOS
  - Modifier le Bundle ID ou le chemin d'installation de l'application
summary: Persistance des permissions macOS (TCC) et exigences de signature
title: Permissions macOS
x-i18n:
  generated_at: "2026-02-01T21:32:58Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: d012589c0583dd0b3792d695f3f71a6ff265704cf02a3b79f8c4a5b14712e6aa
  source_path: platforms/mac/permissions.md
  workflow: 15
---

# Permissions macOS (TCC)

L'octroi de permissions macOS est fragile. TCC associe les permissions accordées à la signature de code, l'identifiant de bundle et le chemin disque de l'application. Si l'un de ces éléments change, macOS traite l'application comme nouvelle et peut supprimer ou masquer les invites de permission.

## Exigences pour stabiliser les permissions

- Chemin identique : exécutez l'application depuis un emplacement fixe (pour OpenClaw, `dist/OpenClaw.app`).
- Identifiant de bundle identique : modifier le Bundle ID crée une nouvelle identité de permission.
- Application signée : les builds non signés ou temporairement signés ne persistent pas les permissions.
- Signature cohérente : utilisez un vrai certificat Apple Development ou Developer ID pour garantir que la signature reste stable entre les builds.

La signature temporaire génère une nouvelle identité à chaque build. macOS oublie les autorisations précédentes et les invites peuvent disparaître complètement jusqu'à ce que les entrées expirées soient effacées.

## Liste de contrôle de récupération lorsque les invites de permission disparaissent

1. Quittez l'application.
2. Supprimez l'entrée de l'application dans Paramètres système -> Confidentialité et sécurité.
3. Redémarrez l'application depuis le même chemin et accordez à nouveau les permissions.
4. Si l'invite n'apparaît toujours pas, réinitialisez l'entrée TCC avec `tccutil` puis réessayez.
5. Certaines permissions ne réapparaissent qu'après un redémarrage complet de macOS.

Exemple de réinitialisation (remplacez le Bundle ID selon vos besoins) :

```bash
sudo tccutil reset Accessibility bot.molt.mac
sudo tccutil reset ScreenCapture bot.molt.mac
sudo tccutil reset AppleEvents
```

Si vous testez les permissions, signez toujours avec un vrai certificat. Les builds temporairement signés conviennent uniquement pour les exécutions locales rapides qui ne nécessitent pas de permissions.
