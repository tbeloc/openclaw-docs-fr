---
read_when:
  - 构建或签名 Mac 调试构建
summary: 打包脚本生成的 macOS 调试构建的签名步骤
title: macOS 签名
x-i18n:
  generated_at: "2026-02-01T21:33:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 403b92f9a0ecdb7cb42ec097c684b7a696be3696d6eece747314a4dc90d8797e
  source_path: platforms/mac/signing.md
  workflow: 15
---

# Signature Mac (Builds de débogage)

Cette application est généralement construite à partir de [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh), qui effectue actuellement :

- Définit un identifiant de bundle de débogage stable : `ai.openclaw.mac.debug`
- Écrit dans Info.plist avec cet ID de bundle (peut être remplacé via `BUNDLE_ID=...`)
- Appelle [`scripts/codesign-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/codesign-mac-app.sh) pour signer le binaire principal et le paquet d'application, permettant à macOS de traiter chaque reconstruction comme le même paquet signé et de conserver les permissions TCC (notifications, accessibilité, enregistrement d'écran, microphone, reconnaissance vocale). Pour des permissions stables, utilisez une véritable identité de signature ; la signature ad hoc est optionnelle et instable (voir [Permissions macOS](/platforms/mac/permissions)).
- Utilise `CODESIGN_TIMESTAMP=auto` par défaut ; active les horodatages de confiance pour la signature Developer ID. Définissez `CODESIGN_TIMESTAMP=off` pour ignorer l'horodatage (builds de débogage hors ligne).
- Injecte les métadonnées de construction dans Info.plist : `OpenClawBuildTimestamp` (UTC) et `OpenClawGitCommit` (hash court), afin que le panneau "À propos" puisse afficher les informations de construction, les informations git et le canal de débogage/publication.
- **L'empaquetage nécessite Node 22+** : le script exécute la construction TS et la construction de l'interface utilisateur de contrôle.
- Lit `SIGN_IDENTITY` à partir des variables d'environnement. Ajoutez `export SIGN_IDENTITY="Apple Development: Your Name (TEAMID)"` (ou votre certificat Developer ID Application) à votre fichier de configuration shell pour toujours signer avec votre certificat. La signature ad hoc doit être explicitement activée via `ALLOW_ADHOC_SIGNING=1` ou `SIGN_IDENTITY="-"` (non recommandé pour les tests de permissions).
- Exécute un audit d'ID d'équipe après la signature, qui échoue si des fichiers Mach-O dans le paquet d'application sont signés par un ID d'équipe différent. Définissez `SKIP_TEAM_ID_CHECK=1` pour ignorer cette vérification.

## Utilisation

```bash
# À partir de la racine du dépôt
scripts/package-mac-app.sh               # Sélectionne automatiquement l'identité ; erreur si non trouvée
SIGN_IDENTITY="Developer ID Application: Your Name" scripts/package-mac-app.sh   # Certificat réel
ALLOW_ADHOC_SIGNING=1 scripts/package-mac-app.sh    # Signature ad hoc (les permissions ne persisteront pas)
SIGN_IDENTITY="-" scripts/package-mac-app.sh        # Signature ad hoc explicite (mêmes limitations)
DISABLE_LIBRARY_VALIDATION=1 scripts/package-mac-app.sh   # Solution de non-concordance d'ID d'équipe Sparkle réservée au développement
```

### Remarques sur la signature ad hoc

Lors de la signature avec `SIGN_IDENTITY="-"` (signature ad hoc), le script désactive automatiquement le **runtime renforcé** (`--options runtime`). Ceci est pour éviter que l'application ne plante en essayant de charger des frameworks intégrés qui ne partagent pas le même ID d'équipe (comme Sparkle). La signature ad hoc rompt également la persistance des permissions TCC ; voir [Permissions macOS](/platforms/mac/permissions) pour les étapes de récupération.

## Métadonnées de construction du panneau À propos

`package-mac-app.sh` marque les informations suivantes dans le paquet :

- `OpenClawBuildTimestamp` : heure UTC ISO8601 au moment de l'empaquetage
- `OpenClawGitCommit` : hash git court (`unknown` si non disponible)

L'onglet "À propos" lit ces clés pour afficher la version, la date de construction, le commit git et si c'est un build de débogage (via `#if DEBUG`). Exécutez l'empaqueteur après les modifications de code pour actualiser ces valeurs.

## Raison d'être

Les permissions TCC sont liées à l'identifiant de bundle *et* à la signature de code. Les builds de débogage non signés utilisant des UUID changeants font que macOS oublie les autorisations après chaque reconstruction. Signer les binaires (signature ad hoc par défaut) et maintenir un ID de bundle/chemin fixe (`dist/OpenClaw.app`) conserve les autorisations entre les builds, en accord avec le schéma de VibeTunnel.
