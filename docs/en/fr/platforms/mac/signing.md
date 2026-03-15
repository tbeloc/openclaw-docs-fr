---
summary: "Étapes de signature pour les builds de débogage macOS générés par les scripts d'empaquetage"
read_when:
  - Building or signing mac debug builds
title: "Signature macOS"
---

# Signature mac (builds de débogage)

Cette application est généralement construite à partir de [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh), qui maintenant :

- définit un identifiant de bundle de débogage stable : `ai.openclaw.mac.debug`
- écrit le Info.plist avec cet identifiant de bundle (à remplacer via `BUNDLE_ID=...`)
- appelle [`scripts/codesign-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/codesign-mac-app.sh) pour signer le binaire principal et le bundle d'application afin que macOS traite chaque reconstruction comme le même bundle signé et conserve les permissions TCC (notifications, accessibilité, enregistrement d'écran, micro, synthèse vocale). Pour des permissions stables, utilisez une véritable identité de signature ; ad-hoc est optionnel et fragile (voir [permissions macOS](/fr/platforms/mac/permissions)).
- utilise `CODESIGN_TIMESTAMP=auto` par défaut ; il active les horodatages de confiance pour les signatures Developer ID. Définissez `CODESIGN_TIMESTAMP=off` pour ignorer l'horodatage (builds de débogage hors ligne).
- injecte les métadonnées de construction dans Info.plist : `OpenClawBuildTimestamp` (UTC) et `OpenClawGitCommit` (hash court) afin que le volet À propos puisse afficher la construction, git et le canal de débogage/version.
- **L'empaquetage utilise par défaut Node 24** : le script exécute les builds TS et le build de l'interface utilisateur de contrôle. Node 22 LTS, actuellement `22.16+`, reste pris en charge pour la compatibilité.
- lit `SIGN_IDENTITY` à partir de l'environnement. Ajoutez `export SIGN_IDENTITY="Apple Development: Your Name (TEAMID)"` (ou votre certificat Developer ID Application) à votre rc shell pour toujours signer avec votre certificat. La signature ad-hoc nécessite un opt-in explicite via `ALLOW_ADHOC_SIGNING=1` ou `SIGN_IDENTITY="-"` (non recommandé pour les tests de permissions).
- exécute un audit d'identifiant d'équipe après la signature et échoue si un Mach-O à l'intérieur du bundle d'application est signé par un identifiant d'équipe différent. Définissez `SKIP_TEAM_ID_CHECK=1` pour contourner.

## Utilisation

```bash
# from repo root
scripts/package-mac-app.sh               # auto-selects identity; errors if none found
SIGN_IDENTITY="Developer ID Application: Your Name" scripts/package-mac-app.sh   # real cert
ALLOW_ADHOC_SIGNING=1 scripts/package-mac-app.sh    # ad-hoc (permissions will not stick)
SIGN_IDENTITY="-" scripts/package-mac-app.sh        # explicit ad-hoc (same caveat)
DISABLE_LIBRARY_VALIDATION=1 scripts/package-mac-app.sh   # dev-only Sparkle Team ID mismatch workaround
```

### Remarque sur la signature ad-hoc

Lors de la signature avec `SIGN_IDENTITY="-"` (ad-hoc), le script désactive automatiquement le **Hardened Runtime** (`--options runtime`). Ceci est nécessaire pour éviter les plantages lorsque l'application tente de charger des frameworks intégrés (comme Sparkle) qui ne partagent pas le même identifiant d'équipe. Les signatures ad-hoc cassent également la persistance des permissions TCC ; voir [permissions macOS](/fr/platforms/mac/permissions) pour les étapes de récupération.

## Métadonnées de construction pour À propos

`package-mac-app.sh` marque le bundle avec :

- `OpenClawBuildTimestamp` : ISO8601 UTC au moment de l'empaquetage
- `OpenClawGitCommit` : hash git court (ou `unknown` s'il n'est pas disponible)

L'onglet À propos lit ces clés pour afficher la version, la date de construction, le commit git et s'il s'agit d'un build de débogage (via `#if DEBUG`). Exécutez l'empaqueteur pour actualiser ces valeurs après les modifications du code.

## Pourquoi

Les permissions TCC sont liées à l'identifiant du bundle _et_ à la signature du code. Les builds de débogage non signés avec des UUID changeants causaient à macOS d'oublier les autorisations après chaque reconstruction. Signer les binaires (ad-hoc par défaut) et conserver un identifiant de bundle/chemin fixe (`dist/OpenClaw.app`) préserve les autorisations entre les builds, correspondant à l'approche VibeTunnel.
