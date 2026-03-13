---
read_when:
  - 制作或验证 OpenClaw macOS 发布版本
  - 更新 Sparkle appcast 或订阅源资源
summary: OpenClaw macOS 发布清单（Sparkle 订阅源、打包、签名）
title: macOS 发布
x-i18n:
  generated_at: "2026-02-01T21:33:17Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 703c08c13793cd8c96bd4c31fb4904cdf4ffff35576e7ea48a362560d371cb30
  source_path: platforms/mac/release.md
  workflow: 15
---

# Sortie macOS OpenClaw (Sparkle)

L'application supporte désormais les mises à jour automatiques Sparkle. Les versions de production doivent être signées avec Developer ID, compressées et publiées avec une entrée appcast signée.

## Prérequis

- Certificat Developer ID Application installé (exemple : `Developer ID Application: <Developer Name> (<TEAMID>)`).
- Variable d'environnement `SPARKLE_PRIVATE_KEY_FILE` définie sur le chemin de la clé privée Sparkle ed25519 (la clé publique est intégrée dans Info.plist). Si manquante, vérifiez `~/.profile`.
- Identifiants de notarisation pour `xcrun notarytool` (profil de trousseau ou clé API) pour la distribution sécurisée via Gatekeeper des DMG/zip.
  - Nous utilisons un profil de trousseau nommé `openclaw-notary`, créé à partir des variables d'environnement de clé API App Store Connect dans votre profil shell :
    - `APP_STORE_CONNECT_API_KEY_P8`, `APP_STORE_CONNECT_KEY_ID`, `APP_STORE_CONNECT_ISSUER_ID`
    - `echo "$APP_STORE_CONNECT_API_KEY_P8" | sed 's/\\n/\n/g' > /tmp/openclaw-notary.p8`
    - `xcrun notarytool store-credentials "openclaw-notary" --key /tmp/openclaw-notary.p8 --key-id "$APP_STORE_CONNECT_KEY_ID" --issuer "$APP_STORE_CONNECT_ISSUER_ID"`
- Dépendances `pnpm` installées (`pnpm install --config.node-linker=hoisted`).
- Outils Sparkle récupérés automatiquement via SwiftPM, situés dans `apps/macos/.build/artifacts/sparkle/Sparkle/bin/` (`sign_update`, `generate_appcast`, etc.).

## Construction et empaquetage

Points importants :

- `APP_BUILD` correspond à `CFBundleVersion`/`sparkle:version` ; doit être numérique pur et strictement croissant (pas de `-beta`), sinon Sparkle le considérera comme la même version.
- Par défaut, l'architecture actuelle (`$(uname -m)`). Pour les versions de production/universelles, définissez `BUILD_ARCHS="arm64 x86_64"` (ou `BUILD_ARCHS=all`).
- Utilisez `scripts/package-mac-dist.sh` pour générer les artefacts de production (zip + DMG + notarisation). Utilisez `scripts/package-mac-app.sh` pour l'empaquetage local/développement.

```bash
# Exécutez depuis la racine du dépôt ; définissez l'ID de version pour activer l'appcast Sparkle.
# APP_BUILD doit être numérique pur et strictement croissant pour que Sparkle compare correctement.
BUNDLE_ID=bot.molt.mac \
APP_VERSION=2026.1.27-beta.1 \
APP_BUILD="$(git rev-list --count HEAD)" \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-app.sh

# Empaquetez le zip pour la distribution (inclut les branches de ressources pour les mises à jour incrémentielles Sparkle)
ditto -c -k --sequesterRsrc --keepParent dist/OpenClaw.app dist/OpenClaw-2026.1.27-beta.1.zip

# Optionnel : construisez également un DMG stylisé pour les utilisateurs (glisser-déposer vers /Applications)
scripts/create-dmg.sh dist/OpenClaw.app dist/OpenClaw-2026.1.27-beta.1.dmg

# Recommandé : construisez + notarisez/agrafez zip + DMG
# D'abord, créez une fois le profil de trousseau :
#   xcrun notarytool store-credentials "openclaw-notary" \
#     --apple-id "<apple-id>" --team-id "<team-id>" --password "<app-specific-password>"
NOTARIZE=1 NOTARYTOOL_PROFILE=openclaw-notary \
BUNDLE_ID=bot.molt.mac \
APP_VERSION=2026.1.27-beta.1 \
APP_BUILD="$(git rev-list --count HEAD)" \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-dist.sh

# Optionnel : fournissez dSYM avec la version
ditto -c -k --keepParent apps/macos/.build/release/OpenClaw.app.dSYM dist/OpenClaw-2026.1.27-beta.1.dSYM.zip
```

## Entrée Appcast

Utilisez le générateur de notes de version pour que Sparkle rende les notes HTML formatées :

```bash
SPARKLE_PRIVATE_KEY_FILE=/path/to/ed25519-private-key scripts/make_appcast.sh dist/OpenClaw-2026.1.27-beta.1.zip https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml
```

Générez les notes de version HTML à partir de `CHANGELOG.md` (via [`scripts/changelog-to-html.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/changelog-to-html.sh)) et intégrez-les dans l'entrée appcast.
Lors de la publication, validez le `appcast.xml` mis à jour avec les artefacts de version (zip + dSYM).

## Publication et vérification

- Téléchargez `OpenClaw-2026.1.27-beta.1.zip` (et `OpenClaw-2026.1.27-beta.1.dSYM.zip`) vers la version GitHub correspondant à la balise `v2026.1.27-beta.1`.
- Assurez-vous que l'URL appcast brute correspond à la source intégrée : `https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml`.
- Vérifications d'intégrité :
  - `curl -I https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml` retourne 200.
  - `curl -I <enclosure url>` retourne 200 après le téléchargement des artefacts.
  - Sur une version de production précédente, exécutez « Vérifier les mises à jour… » depuis l'onglet À propos et vérifiez que Sparkle installe correctement la nouvelle version.

Définition de l'achèvement : application signée + appcast publié, flux de mise à jour depuis les anciennes versions fonctionnant correctement, et artefacts de version attachés à la version GitHub.
