---
read_when:
  - 更新设备型号标识符映射或 NOTICE/许可证文件
  - 更改实例 UI 中设备名称的显示方式
summary: OpenClaw 如何内置 Apple 设备型号标识符以在 macOS 应用中显示友好名称。
title: 设备型号数据库
x-i18n:
  generated_at: "2026-02-01T21:37:07Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1d99c2538a0d8fdd80fa468fa402f63479ef2522e83745a0a46527a86238aeb2
  source_path: reference/device-models.md
  workflow: 15
---

# Base de données des modèles d'appareils (noms conviviaux)

L'application complémentaire macOS affiche des noms conviviaux de modèles d'appareils Apple dans l'interface utilisateur des **instances** en mappant les identifiants de modèle Apple (par exemple `iPad16,6`, `Mac16,6`) à des noms lisibles par l'homme.

Ce mappage est intégré au format JSON dans :

- `apps/macos/Sources/OpenClaw/Resources/DeviceModels/`

## Source des données

Le mappage actuellement intégré provient du référentiel sous licence MIT :

- `kyle-seongwoo-jun/apple-device-identifiers`

Pour maintenir la déterminabilité de la construction, les fichiers JSON sont épinglés à un commit en amont spécifique (enregistré dans `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`).

## Mettre à jour la base de données

1. Sélectionnez les commits en amont à épingler (un pour iOS et un pour macOS).
2. Mettez à jour les hachages de commit dans `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`.
3. Retéléchargez les fichiers JSON épinglés à ces commits :

```bash
IOS_COMMIT="<commit sha for ios-device-identifiers.json>"
MAC_COMMIT="<commit sha for mac-device-identifiers.json>"

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${IOS_COMMIT}/ios-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/ios-device-identifiers.json

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${MAC_COMMIT}/mac-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/mac-device-identifiers.json
```

4. Assurez-vous que `apps/macos/Sources/OpenClaw/Resources/DeviceModels/LICENSE.apple-device-identifiers.txt` reste cohérent avec l'amont (remplacez ce fichier si la licence en amont a changé).
5. Vérifiez que l'application macOS se construit correctement (sans avertissements) :

```bash
swift build --package-path apps/macos
```
