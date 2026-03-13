---
read_when:
  - 你想要 Firecrawl 支持的网页提取
  - 你需要 Firecrawl API 密钥
  - 你想要 web_fetch 的反机器人提取
summary: 用于 web_fetch 的 Firecrawl 回退（反机器人 + 缓存提取）
title: Firecrawl
x-i18n:
  generated_at: "2026-02-03T10:10:35Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 08a7ad45b41af41204e44d2b0be0f980b7184d80d2fa3977339e42a47beb2851
  source_path: tools/firecrawl.md
  workflow: 15
---

# Firecrawl

OpenClaw peut utiliser **Firecrawl** comme extracteur de secours pour `web_fetch`. C'est un service
d'extraction de contenu hébergé qui prend en charge l'évitement des robots et la mise en cache, ce qui aide à gérer
les sites intensifs en JavaScript ou les pages qui bloquent les requêtes HTTP ordinaires.

## Obtenir une clé API

1. Créez un compte Firecrawl et générez une clé API.
2. Stockez-la dans votre configuration ou définissez `FIRECRAWL_API_KEY` dans l'environnement de la passerelle.

## Configurer Firecrawl

```json5
{
  tools: {
    web: {
      fetch: {
        firecrawl: {
          apiKey: "FIRECRAWL_API_KEY_HERE",
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 172800000,
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

Remarques :

- `firecrawl.enabled` est défini par défaut à true lorsqu'une clé API est présente.
- `maxAgeMs` contrôle la durée pendant laquelle les résultats en cache peuvent être conservés (en millisecondes). La valeur par défaut est 2 jours.

## Mode furtif / Évitement des robots

Firecrawl fournit un paramètre **mode proxy** pour l'évitement des robots (`basic`, `stealth` ou `auto`).
OpenClaw utilise toujours `proxy: "auto"` plus `storeInCache: true` pour les requêtes Firecrawl.
Si le proxy est omis, Firecrawl utilise par défaut `auto`. `auto` réessaiera avec un proxy furtif si la tentative basique échoue, ce qui peut consommer plus de crédits que
l'utilisation exclusive du scraping basique.

## Comment `web_fetch` utilise Firecrawl

Ordre d'extraction de `web_fetch` :

1. Readability (local)
2. Firecrawl (si configuré)
3. Nettoyage HTML basique (dernier recours)

Consultez [Outil Web](/tools/web) pour la configuration complète de l'outil Web.
