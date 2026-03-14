---
summary: "Journalisation OpenClaw : journal de fichier de diagnostics roulant + drapeaux de confidentialité de journal unifié"
read_when:
  - Capturing macOS logs or investigating private data logging
  - Debugging voice wake/session lifecycle issues
title: "Journalisation macOS"
---

# Journalisation (macOS)

## Journal de fichier de diagnostics roulant (volet Débogage)

OpenClaw achemine les journaux d'application macOS via swift-log (journalisation unifiée par défaut) et peut écrire un journal de fichier local et rotatif sur le disque lorsque vous avez besoin d'une capture durable.

- Verbosité : **Volet Débogage → Journaux → Journalisation d'application → Verbosité**
- Activer : **Volet Débogage → Journaux → Journalisation d'application → « Écrire le journal de diagnostics roulant (JSONL) »**
- Emplacement : `~/Library/Logs/OpenClaw/diagnostics.jsonl` (rotation automatique ; les anciens fichiers sont suffixés par `.1`, `.2`, …)
- Effacer : **Volet Débogage → Journaux → Journalisation d'application → « Effacer »**

Remarques :

- Cette option est **désactivée par défaut**. Activez-la uniquement lors du débogage actif.
- Traitez le fichier comme sensible ; ne le partagez pas sans révision.

## Données privées de journalisation unifiée sur macOS

La journalisation unifiée masque la plupart des charges utiles à moins qu'un sous-système n'opte pour `privacy -off`. Selon l'article de Peter sur les [bizarreries de confidentialité de journalisation](https://steipete.me/posts/2025/logging-privacy-shenanigans) macOS (2025), ceci est contrôlé par un plist dans `/Library/Preferences/Logging/Subsystems/` indexé par le nom du sous-système. Seules les nouvelles entrées de journal récupèrent le drapeau, donc activez-le avant de reproduire un problème.

## Activer pour OpenClaw (`ai.openclaw`)

- Écrivez d'abord le plist dans un fichier temporaire, puis installez-le de manière atomique en tant que root :

```bash
cat <<'EOF' >/tmp/ai.openclaw.plist
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
sudo install -m 644 -o root -g wheel /tmp/ai.openclaw.plist /Library/Preferences/Logging/Subsystems/ai.openclaw.plist
```

- Aucun redémarrage n'est requis ; logd remarque le fichier rapidement, mais seules les nouvelles lignes de journal incluront les charges utiles privées.
- Affichez la sortie plus riche avec l'assistant existant, par exemple `./scripts/clawlog.sh --category WebChat --last 5m`.

## Désactiver après le débogage

- Supprimez le remplacement : `sudo rm /Library/Preferences/Logging/Subsystems/ai.openclaw.plist`.
- Exécutez éventuellement `sudo log config --reload` pour forcer logd à abandonner le remplacement immédiatement.
- N'oubliez pas que cette surface peut inclure des numéros de téléphone et des corps de messages ; gardez le plist en place uniquement lorsque vous avez activement besoin du détail supplémentaire.
