---
read_when:
  - Vous devez diriger les journaux de débogage sans augmenter le niveau de journalisation global
  - Vous devez capturer les journaux d'un sous-système spécifique pour le personnel d'assistance
summary: Drapeaux de diagnostic pour diriger les journaux de débogage
title: Drapeaux de diagnostic
x-i18n:
  generated_at: "2026-02-03T10:05:34Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: daf0eca0e6bd1cbc2c400b2e94e1698709a96b9cdba1a8cf00bd580a61829124
  source_path: diagnostics/flags.md
  workflow: 15
---

# Drapeaux de diagnostic

Les drapeaux de diagnostic vous permettent d'activer les journaux de débogage dirigés sans activer la journalisation détaillée partout. Les drapeaux sont activés de manière optionnelle et n'ont aucun effet à moins que les sous-systèmes ne les vérifient.

## Fonctionnement

- Les drapeaux sont des chaînes de caractères (insensibles à la casse).
- Vous pouvez activer les drapeaux dans la configuration ou via des remplacements de variables d'environnement.
- Les caractères génériques sont pris en charge :
  - `telegram.*` correspond à `telegram.http`
  - `*` active tous les drapeaux

## Activation via la configuration

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

Redémarrez la passerelle après modification des drapeaux.

## Remplacement par variable d'environnement (une seule fois)

```bash
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Désactiver tous les drapeaux :

```bash
OPENCLAW_DIAGNOSTICS=0
```

## Emplacement de stockage des journaux

Les drapeaux envoient les journaux vers le fichier de journalisation de diagnostic standard. Emplacement par défaut :

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

Si vous avez défini `logging.file`, ce chemin est utilisé. Les journaux sont au format JSONL (un objet JSON par ligne). La rédaction est toujours appliquée selon `logging.redactSensitive`.

## Extraction des journaux

Sélectionnez le fichier journal le plus récent :

```bash
ls -t /tmp/openclaw/openclaw-*.log | head -n 1
```

Filtrez les diagnostics HTTP Telegram :

```bash
rg "telegram http error" /tmp/openclaw/openclaw-*.log
```

Ou utilisez tail lors de la reproduction :

```bash
tail -f /tmp/openclaw/openclaw-$(date +%F).log | rg "telegram http error"
```

Pour une passerelle distante, vous pouvez également utiliser `openclaw logs --follow` (voir [/cli/logs](/cli/logs)).

## Remarques

- Si `logging.level` est défini à un niveau supérieur à `warn`, ces journaux peuvent être supprimés. Le niveau par défaut `info` convient.
- Les drapeaux peuvent rester activés en toute sécurité ; ils n'affectent que le volume de journalisation des sous-systèmes spécifiques.
- Utilisez [/logging](/logging) pour modifier les cibles de journalisation, les niveaux et les paramètres de rédaction.
