---
summary: "Drapeaux de diagnostic pour les journaux de débogage ciblés"
read_when:
  - Vous avez besoin de journaux de débogage ciblés sans augmenter les niveaux de journalisation globaux
  - Vous devez capturer les journaux spécifiques aux sous-systèmes pour le support
title: "Drapeaux de diagnostic"
---

# Drapeaux de diagnostic

Les drapeaux de diagnostic vous permettent d'activer les journaux de débogage ciblés sans activer la journalisation détaillée partout. Les drapeaux sont optionnels et n'ont aucun effet à moins qu'un sous-système ne les vérifie.

## Fonctionnement

- Les drapeaux sont des chaînes de caractères (insensibles à la casse).
- Vous pouvez activer les drapeaux dans la configuration ou via un remplacement d'env.
- Les caractères génériques sont pris en charge :
  - `telegram.*` correspond à `telegram.http`
  - `*` active tous les drapeaux

## Activer via la configuration

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Plusieurs drapeaux :

```json
{
  "diagnostics": {
    "flags": ["telegram.http", "gateway.*"]
  }
}
```

Redémarrez la passerelle après avoir modifié les drapeaux.

## Remplacement d'env (ponctuel)

```bash
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Désactiver tous les drapeaux :

```bash
OPENCLAW_DIAGNOSTICS=0
```

## Où vont les journaux

Les drapeaux émettent les journaux dans le fichier journal de diagnostic standard. Par défaut :

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

Si vous définissez `logging.file`, utilisez ce chemin à la place. Les journaux sont au format JSONL (un objet JSON par ligne). La rédaction s'applique toujours en fonction de `logging.redactSensitive`.

## Extraire les journaux

Sélectionnez le fichier journal le plus récent :

```bash
ls -t /tmp/openclaw/openclaw-*.log | head -n 1
```

Filtrer pour les diagnostics HTTP Telegram :

```bash
rg "telegram http error" /tmp/openclaw/openclaw-*.log
```

Ou suivre en direct lors de la reproduction :

```bash
tail -f /tmp/openclaw/openclaw-$(date +%F).log | rg "telegram http error"
```

Pour les passerelles distantes, vous pouvez également utiliser `openclaw logs --follow` (voir [/cli/logs](/cli/logs)).

## Remarques

- Si `logging.level` est défini à un niveau supérieur à `warn`, ces journaux peuvent être supprimés. Le `info` par défaut convient.
- Les drapeaux sont sûrs à laisser activés ; ils n'affectent que le volume de journalisation pour le sous-système spécifique.
- Utilisez [/logging](/logging) pour modifier les destinations des journaux, les niveaux et la rédaction.
