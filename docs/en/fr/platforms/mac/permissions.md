---
summary: "Persistance des permissions macOS (TCC) et exigences de signature"
read_when:
  - Débogage des invites de permission macOS manquantes ou bloquées
  - Empaquetage ou signature de l'application macOS
  - Modification des identifiants de bundle ou des chemins d'installation de l'application
title: "Permissions macOS"
---

# Permissions macOS (TCC)

Les octrois de permissions macOS sont fragiles. TCC associe un octroi de permission à la signature de code de l'application, à l'identifiant de bundle et au chemin sur disque. Si l'un de ces éléments change, macOS traite l'application comme nouvelle et peut supprimer ou masquer les invites.

## Exigences pour des permissions stables

- Même chemin : exécutez l'application à partir d'un emplacement fixe (pour OpenClaw, `dist/OpenClaw.app`).
- Même identifiant de bundle : modifier l'ID de bundle crée une nouvelle identité de permission.
- Application signée : les builds non signées ou signées ad-hoc ne persistent pas les permissions.
- Signature cohérente : utilisez un vrai certificat Apple Development ou Developer ID pour que la signature reste stable entre les reconstructions.

Les signatures ad-hoc génèrent une nouvelle identité à chaque build. macOS oubliera les octrois précédents et les invites peuvent disparaître entièrement jusqu'à ce que les entrées obsolètes soient effacées.

## Liste de contrôle de récupération quand les invites disparaissent

1. Quittez l'application.
2. Supprimez l'entrée de l'application dans Paramètres système -> Confidentialité et sécurité.
3. Relancez l'application à partir du même chemin et accordez à nouveau les permissions.
4. Si l'invite n'apparaît toujours pas, réinitialisez les entrées TCC avec `tccutil` et réessayez.
5. Certaines permissions ne réapparaissent qu'après un redémarrage complet de macOS.

Exemples de réinitialisations (remplacez l'identifiant de bundle selon les besoins) :

```bash
sudo tccutil reset Accessibility ai.openclaw.mac
sudo tccutil reset ScreenCapture ai.openclaw.mac
sudo tccutil reset AppleEvents
```

## Permissions des fichiers et dossiers (Bureau/Documents/Téléchargements)

macOS peut également restreindre l'accès au Bureau, Documents et Téléchargements pour les processus de terminal/arrière-plan. Si les lectures de fichiers ou les listes de répertoires se bloquent, accordez l'accès au même contexte de processus qui effectue les opérations de fichiers (par exemple Terminal/iTerm, application lancée par LaunchAgent ou processus SSH).

Solution de contournement : déplacez les fichiers dans l'espace de travail OpenClaw (`~/.openclaw/workspace`) si vous voulez éviter les octrois par dossier.

Si vous testez les permissions, signez toujours avec un vrai certificat. Les builds ad-hoc ne sont acceptables que pour les exécutions locales rapides où les permissions n'ont pas d'importance.
