# Ressources i18n de la documentation OpenClaw

Ce dossier stocke les fichiers **générés** et de **configuration** pour les traductions de documentation.

## Fichiers

- `glossary.<lang>.json` — mappages de termes préférés (utilisés dans les conseils d'invite).
- `<lang>.tm.jsonl` — mémoire de traduction (cache) indexée par flux de travail + modèle + hash de texte.

## Format du glossaire

`glossary.<lang>.json` est un tableau d'entrées :

```json
{
  "source": "troubleshooting",
  "target": "故障排除",
  "ignore_case": true,
  "whole_word": false
}
```

Champs :

- `source` : phrase anglaise (ou source) à préférer.
- `target` : sortie de traduction préférée.

## Remarques

- Les entrées du glossaire sont transmises au modèle comme **conseils d'invite** (pas de réécriture déterministe).
- La mémoire de traduction est mise à jour par `scripts/docs-i18n`.
