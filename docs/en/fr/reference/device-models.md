---
summary: "Comment OpenClaw fournit les identifiants de modèles d'appareils Apple sous forme de noms conviviaux dans l'application macOS."
read_when:
  - Updating device model identifier mappings or NOTICE/license files
  - Changing how Instances UI displays device names
title: "Device Model Database"
---

# Base de données des modèles d'appareils (noms conviviaux)

L'application compagnon macOS affiche les noms conviviaux des appareils Apple dans l'interface utilisateur **Instances** en mappant les identifiants de modèles Apple (par exemple `iPad16,6`, `Mac16,6`) à des noms lisibles par l'homme.

Le mapping est fourni en tant que JSON sous :

- `apps/macos/Sources/OpenClaw/Resources/DeviceModels/`

## Source de données

Nous fournissons actuellement le mapping à partir du référentiel sous licence MIT :

- `kyle-seongwoo-jun/apple-device-identifiers`

Pour maintenir des builds déterministes, les fichiers JSON sont épinglés à des commits en amont spécifiques (enregistrés dans `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`).

## Mise à jour de la base de données

1. Choisissez les commits en amont auxquels vous souhaitez vous épingler (un pour iOS, un pour macOS).
2. Mettez à jour les hachages de commit dans `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`.
3. Retéléchargez les fichiers JSON, épinglés à ces commits :

```bash
IOS_COMMIT="<commit sha for ios-device-identifiers.json>"
MAC_COMMIT="<commit sha for mac-device-identifiers.json>"

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${IOS_COMMIT}/ios-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/ios-device-identifiers.json

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${MAC_COMMIT}/mac-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/mac-device-identifiers.json
```

4. Assurez-vous que `apps/macos/Sources/OpenClaw/Resources/DeviceModels/LICENSE.apple-device-identifiers.txt` correspond toujours à la version en amont (remplacez-le si la licence en amont change).
5. Vérifiez que l'application macOS se compile correctement (sans avertissements) :

```bash
swift build --package-path apps/macos
```
