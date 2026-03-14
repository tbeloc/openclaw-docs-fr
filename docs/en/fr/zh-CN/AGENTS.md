# AGENTS.md - Espace de travail de traduction de documentation fr-FR

## À lire quand

- Maintenance de `docs/fr-FR/**`
- Mise à jour du pipeline de traduction français (glossaire/TM/prompt)
- Traitement des retours de traduction français ou régressions

## Pipeline（docs-i18n）

- Document source : `docs/**/*.md`
- Document cible : `docs/fr-FR/**/*.md`
- Glossaire : `docs/.i18n/glossary.fr-FR.json`
- Mémoire de traduction : `docs/.i18n/fr-FR.tm.jsonl`
- Règles de prompt : `scripts/docs-i18n/translator.go`

Modes d'exécution courants :

```bash
# Lot (mode doc, peut être parallélisé)
go run scripts/docs-i18n/main.go -mode doc -parallel 6 docs/**/*.md

# Fichier unique

go run scripts/docs-i18n/main.go -mode doc docs/channels/matrix.md

# Correctif de petite portée (mode segment, utilise TM ; pas de parallélisation)
go run scripts/docs-i18n/main.go -mode segment docs/channels/matrix.md
```

Points importants :

- Le mode doc est utilisé pour la traduction de pages entières ; le mode segment pour les petits correctifs (dépend de TM).
- Pour les très gros fichiers en cas de timeout, privilégier les **remplacements ciblés** ou diviser avant d'exécuter.
- Après traduction, vérifier les guillemets français, l'espacement CJK-Latin et la cohérence terminologique.

## Règles de style fr-FR

- Espacement CJK-Latin : suivre W3C CLREQ (ex. `Gateway passerelle`, `Skills configuration`).
- Guillemets français : utiliser `« »` dans le corps du texte/titres ; conserver les guillemets ASCII pour le code/CLI/clés.
- Termes conservés en anglais : `Skills`, `local loopback`, `Tailscale`.
- Blocs de code/code inline : conserver l'original, ne pas insérer d'espaces ou remplacer les guillemets dans le code.

## Termes clés (#6995 correction)

- `Gateway passerelle`
- `Skills configuration`
- `bac à sable`
- `clé attendue`
- `application complémentaire`
- `streaming par chunks`
- `découverte d'appareils`

## Retours et historique des modifications

- Source des retours : GitHub issue #6995
- Utilisateurs ayant donné des retours : @AaronWander、@taiyi747、@Explorer1092、@rendaoyuan
- Points clés des modifications : mise à jour des règles de prompt, expansion du glossaire, nettoyage de TM, régénération en lot + corrections ciblées
- Lien de référence : https://github.com/openclaw/openclaw/issues/6995
