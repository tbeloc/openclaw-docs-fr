---
read_when:
  - Capturer les journaux macOS ou enquêter sur la journalisation des données de confidentialité
  - Déboguer les problèmes d'activation vocale/cycle de vie de session
summary: Journaux OpenClaw : journaux de fichiers de diagnostic en roulement + drapeau de confidentialité de journalisation unifié
title: Journaux macOS
x-i18n:
  generated_at: "2026-02-01T21:32:54Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c4c201d154915e0eb08bf5e32bac98fa93766f50f2a24bf56ab4424eb7781526
  source_path: platforms/mac/logging.md
  workflow: 15
---

# Journaux (macOS)

## Journaux de fichiers de diagnostic en roulement (Panneau de débogage)

OpenClaw achemine les journaux d'application macOS via swift-log (utilisant la journalisation unifié par défaut), et peut écrire des journaux de fichiers en rotation locale sur le disque lorsqu'une capture persistante est nécessaire.

- Niveau de détail : **Panneau de débogage → Logs → App logging → Verbosity**
- Activation : **Panneau de débogage → Logs → App logging → "Write rolling diagnostics log (JSONL)"**
- Emplacement : `~/Library/Logs/OpenClaw/diagnostics.jsonl` (rotation automatique ; les anciens fichiers sont suffixés par `.1`, `.2`, …)
- Effacement : **Panneau de débogage → Logs → App logging → "Clear"**

Points importants :

- Cette fonctionnalité est **désactivée par défaut**. Activez-la uniquement lors du débogage actif.
- Ce fichier contient des informations sensibles ; veuillez examiner le contenu avant de le partager.

## Données de confidentialité dans la journalisation unifié sur macOS

La journalisation unifié masque la plupart des charges utiles, sauf si le sous-système choisit d'activer `privacy -off`. Selon l'article de Peter sur les [mécanismes de confidentialité de la journalisation macOS](https://steipete.me/posts/2025/logging-privacy-shenanigans) (2025), ceci est contrôlé via des fichiers plist dans `/Library/Preferences/Logging/Subsystems/` avec le nom du sous-système comme clé. Seules les nouvelles entrées de journal appliqueront le drapeau, donc activez-le avant de reproduire le problème.

## Activation pour OpenClaw (`bot.molt`)

- Écrivez d'abord le plist dans un fichier temporaire, puis installez-le de manière atomique en tant que root :

```bash
cat <<'EOF' >/tmp/bot.molt.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DEFAULT-OPTIONS</key>
    <dict>
        <key>Enable-Private-Data</key>
        <true/>
    </dict>
</dict>
</plist>
EOF
sudo install -m 644 -o root -g wheel /tmp/bot.molt.plist /Library/Preferences/Logging/Subsystems/bot.molt.plist
```

- Aucun redémarrage n'est nécessaire ; logd détectera le fichier rapidement, mais seules les nouvelles lignes de journal contiendront les charges utiles privées.
- Utilisez le script auxiliaire existant pour voir une sortie plus riche, par exemple `./scripts/clawlog.sh --category WebChat --last 5m`.

## Désactivation après débogage

- Supprimez la configuration de remplacement : `sudo rm /Library/Preferences/Logging/Subsystems/bot.molt.plist`.
- Vous pouvez optionnellement exécuter `sudo log config --reload` pour forcer logd à abandonner immédiatement la configuration de remplacement.
- Veuillez noter que ces données peuvent contenir des numéros de téléphone et le corps des messages ; conservez le fichier plist uniquement si vous avez vraiment besoin de détails supplémentaires.
