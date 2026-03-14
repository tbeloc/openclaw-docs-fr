---
summary: "Liste de contrôle de publication macOS OpenClaw (flux Sparkle, empaquetage, signature)"
read_when:
  - Création ou validation d'une publication macOS OpenClaw
  - Mise à jour du flux appcast ou des ressources Sparkle
title: "Publication macOS"
---

# Publication macOS OpenClaw (Sparkle)

Cette application est désormais livrée avec les mises à jour automatiques Sparkle. Les versions de publication doivent être signées avec Developer ID, compressées et publiées avec une entrée appcast signée.

## Prérequis

- Certificat Developer ID Application installé (exemple : `Developer ID Application: <Developer Name> (<TEAMID>)`).
- Chemin de la clé privée Sparkle défini dans l'environnement sous `SPARKLE_PRIVATE_KEY_FILE` (chemin vers votre clé privée ed25519 Sparkle ; clé publique intégrée dans Info.plist). S'il est manquant, vérifiez `~/.profile`.
- Identifiants de notarisation (profil Keychain ou clé API) pour `xcrun notarytool` si vous souhaitez une distribution DMG/zip sûre pour Gatekeeper.
  - Nous utilisons un profil Keychain nommé `openclaw-notary`, créé à partir des variables d'environnement de la clé API App Store Connect dans votre profil shell :
    - `APP_STORE_CONNECT_API_KEY_P8`, `APP_STORE_CONNECT_KEY_ID`, `APP_STORE_CONNECT_ISSUER_ID`
    - `echo "$APP_STORE_CONNECT_API_KEY_P8" | sed 's/\\n/\n/g' > /tmp/openclaw-notary.p8`
    - `xcrun notarytool store-credentials "openclaw-notary" --key /tmp/openclaw-notary.p8 --key-id "$APP_STORE_CONNECT_KEY_ID" --issuer "$APP_STORE_CONNECT_ISSUER_ID"`
- Dépendances `pnpm` installées (`pnpm install --config.node-linker=hoisted`).
- Les outils Sparkle sont récupérés automatiquement via SwiftPM à `apps/macos/.build/artifacts/sparkle/Sparkle/bin/` (`sign_update`, `generate_appcast`, etc.).

## Compilation et empaquetage

Remarques :

- `APP_BUILD` correspond à `CFBundleVersion`/`sparkle:version` ; gardez-le numérique + monotone (pas de `-beta`), sinon Sparkle le compare comme égal.
- Si `APP_BUILD` est omis, `scripts/package-mac-app.sh` dérive une valeur sûre pour Sparkle à partir de `APP_VERSION` (`YYYYMMDDNN` : les versions stables par défaut à `90`, les préversions utilisent une voie dérivée du suffixe) et utilise la valeur la plus élevée entre celle-ci et le nombre de commits git.
- Vous pouvez toujours remplacer `APP_BUILD` explicitement lorsque l'ingénierie de publication a besoin d'une valeur monotone spécifique.
- Pour `BUILD_CONFIG=release`, `scripts/package-mac-app.sh` utilise désormais par défaut universal (`arm64 x86_64`) automatiquement. Vous pouvez toujours remplacer avec `BUILD_ARCHS=arm64` ou `BUILD_ARCHS=x86_64`. Pour les compilations locales/dev (`BUILD_CONFIG=debug`), il utilise par défaut l'architecture actuelle (`$(uname -m)`).
- Utilisez `scripts/package-mac-dist.sh` pour les artefacts de publication (zip + DMG + notarisation). Utilisez `scripts/package-mac-app.sh` pour l'empaquetage local/dev.

```bash
# Depuis la racine du dépôt ; définissez les ID de publication pour que le flux Sparkle soit activé.
# Cette commande compile les artefacts de publication sans notarisation.
# APP_BUILD doit être numérique + monotone pour la comparaison Sparkle.
# La valeur par défaut est dérivée automatiquement de APP_VERSION si omise.
SKIP_NOTARIZE=1 \
BUNDLE_ID=ai.openclaw.mac \
APP_VERSION=2026.3.13 \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-dist.sh

# `package-mac-dist.sh` crée déjà le zip + DMG.
# Si vous avez utilisé `package-mac-app.sh` directement à la place, créez-les manuellement :
# Si vous souhaitez la notarisation/agrafage à cette étape, utilisez la commande NOTARIZE ci-dessous.
ditto -c -k --sequesterRsrc --keepParent dist/OpenClaw.app dist/OpenClaw-2026.3.13.zip

# Optionnel : créer un DMG stylisé pour les humains (glisser vers /Applications)
scripts/create-dmg.sh dist/OpenClaw.app dist/OpenClaw-2026.3.13.dmg

# Recommandé : compiler + notariser/agrafer zip + DMG
# D'abord, créez un profil Keychain une fois :
#   xcrun notarytool store-credentials "openclaw-notary" \
#     --apple-id "<apple-id>" --team-id "<team-id>" --password "<app-specific-password>"
NOTARIZE=1 NOTARYTOOL_PROFILE=openclaw-notary \
BUNDLE_ID=ai.openclaw.mac \
APP_VERSION=2026.3.13 \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-dist.sh

# Optionnel : livrer dSYM aux côtés de la publication
ditto -c -k --keepParent apps/macos/.build/release/OpenClaw.app.dSYM dist/OpenClaw-2026.3.13.dSYM.zip
```

## Entrée appcast

Utilisez le générateur de notes de publication pour que Sparkle affiche les notes HTML formatées :

```bash
SPARKLE_PRIVATE_KEY_FILE=/path/to/ed25519-private-key scripts/make_appcast.sh dist/OpenClaw-2026.3.13.zip https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml
```

Génère les notes de publication HTML à partir de `CHANGELOG.md` (via [`scripts/changelog-to-html.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/changelog-to-html.sh)) et les intègre dans l'entrée appcast.
Validez le `appcast.xml` mis à jour aux côtés des artefacts de publication (zip + dSYM) lors de la publication.

## Publication et vérification

- Téléchargez `OpenClaw-2026.3.13.zip` (et `OpenClaw-2026.3.13.dSYM.zip`) vers la publication GitHub pour la balise `v2026.3.13`.
- Assurez-vous que l'URL appcast brute correspond au flux intégré : `https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml`.
- Vérifications de cohérence :
  - `curl -I https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml` retourne 200.
  - `curl -I <enclosure url>` retourne 200 après le téléchargement des ressources.
  - Sur une version publique antérieure, exécutez « Vérifier les mises à jour… » depuis l'onglet À propos et vérifiez que Sparkle installe la nouvelle version correctement.

Définition de la fin : l'application signée + appcast sont publiés, le flux de mise à jour fonctionne à partir d'une version installée antérieure, et les artefacts de publication sont attachés à la publication GitHub.
