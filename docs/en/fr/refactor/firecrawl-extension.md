---
summary: "Design for an opt-in Firecrawl extension that adds search/scrape value without hardwiring Firecrawl into core defaults"
read_when:
  - Designing Firecrawl integration work
  - Evaluating web_search/web_fetch plugin seams
  - Deciding whether Firecrawl belongs in core or as an extension
title: "Firecrawl Extension Design"
---

# Conception de l'extension Firecrawl

## Objectif

Livrer Firecrawl en tant qu'**extension opt-in** qui ajoute :

- des outils Firecrawl explicites pour les agents,
- une intégration `web_search` optionnelle basée sur Firecrawl,
- le support auto-hébergé,
- des paramètres de sécurité plus robustes que le chemin de secours actuel du cœur,

sans pousser Firecrawl dans le chemin de configuration/onboarding par défaut.

## Pourquoi cette forme

Les problèmes/PR Firecrawl récents se regroupent en trois catégories :

1. **Dérive de schéma/version**
   - Plusieurs versions ont rejeté `tools.web.fetch.firecrawl` même si la documentation et le code d'exécution le supportaient.
2. **Renforcement de la sécurité**
   - Le `fetchFirecrawlContent()` actuel envoie toujours des données au point de terminaison Firecrawl avec `fetch()` brut, tandis que le chemin web-fetch principal utilise la protection SSRF.
3. **Pression produit**
   - Les utilisateurs veulent des flux de recherche/scrape natifs Firecrawl, en particulier pour les configurations auto-hébergées/privées.
   - Les mainteneurs ont explicitement rejeté l'intégration profonde de Firecrawl dans les paramètres par défaut du cœur, le flux de configuration et le comportement du navigateur.

Cette combinaison plaide en faveur d'une extension, et non d'une logique Firecrawl supplémentaire dans le chemin par défaut du cœur.

## Principes de conception

- **Opt-in, scoped par fournisseur** : pas d'activation automatique, pas de détournement de configuration, pas d'élargissement du profil d'outils par défaut.
- **L'extension possède la configuration spécifique à Firecrawl** : préférer la configuration du plugin à l'expansion continue de `tools.web.*`.
- **Utile dès le premier jour** : fonctionne même si les coutures `web_search` / `web_fetch` du cœur restent inchangées.
- **Sécurité d'abord** : les récupérations de points de terminaison utilisent la même posture de réseau gardée que les autres outils web.
- **Convivial pour l'auto-hébergement** : configuration + secours env, URL de base explicite, pas d'hypothèses réservées à l'hébergement.

## Extension proposée

ID du plugin : `firecrawl`

### Capacités MVP

Enregistrer des outils explicites :

- `firecrawl_search`
- `firecrawl_scrape`

Optionnel ultérieurement :

- `firecrawl_crawl`
- `firecrawl_map`

Ne pas ajouter l'automatisation du navigateur Firecrawl dans la première version. C'était la partie de la PR #32543 qui a poussé Firecrawl trop loin dans le comportement du cœur et a soulevé le plus de préoccupations en matière de maintenance.

## Forme de configuration

Utiliser la configuration scoped du plugin :

```json5
{
  plugins: {
    entries: {
      firecrawl: {
        enabled: true,
        config: {
          apiKey: "FIRECRAWL_API_KEY",
          baseUrl: "https://api.firecrawl.dev",
          timeoutSeconds: 60,
          maxAgeMs: 172800000,
          proxy: "auto",
          storeInCache: true,
          onlyMainContent: true,
          search: {
            enabled: true,
            defaultLimit: 5,
            sources: ["web"],
            categories: [],
            scrapeResults: false,
          },
          scrape: {
            formats: ["markdown"],
            fallbackForWebFetchLikeUse: false,
          },
        },
      },
    },
  },
}
```

### Résolution des identifiants

Ordre de priorité :

1. `plugins.entries.firecrawl.config.apiKey`
2. `FIRECRAWL_API_KEY`

Ordre de priorité de l'URL de base :

1. `plugins.entries.firecrawl.config.baseUrl`
2. `FIRECRAWL_BASE_URL`
3. `https://api.firecrawl.dev`

### Pont de compatibilité

Pour la première version, l'extension peut également **lire** la configuration du cœur existante à `tools.web.fetch.firecrawl.*` comme source de secours afin que les utilisateurs existants n'aient pas besoin de migrer immédiatement.

Le chemin d'écriture reste local au plugin. Ne pas continuer à élargir les surfaces de configuration Firecrawl du cœur.

## Conception des outils

### `firecrawl_search`

Entrées :

- `query`
- `limit`
- `sources`
- `categories`
- `scrapeResults`
- `timeoutSeconds`

Comportement :

- Appelle Firecrawl `v2/search`
- Retourne des objets de résultat normalisés et conviviaux pour OpenClaw :
  - `title`
  - `url`
  - `snippet`
  - `source`
  - `content` optionnel
- Enveloppe le contenu du résultat en tant que contenu externe non fiable
- La clé de cache inclut la requête + les paramètres du fournisseur pertinents

Pourquoi un outil explicite d'abord :

- Fonctionne aujourd'hui sans modifier `tools.web.search.provider`
- Évite les contraintes actuelles de schéma/chargeur
- Donne aux utilisateurs la valeur Firecrawl immédiatement

### `firecrawl_scrape`

Entrées :

- `url`
- `formats`
- `onlyMainContent`
- `maxAgeMs`
- `proxy`
- `storeInCache`
- `timeoutSeconds`

Comportement :

- Appelle Firecrawl `v2/scrape`
- Retourne markdown/texte plus métadonnées :
  - `title`
  - `finalUrl`
  - `status`
  - `warning`
- Enveloppe le contenu extrait de la même manière que `web_fetch`
- Partage la sémantique du cache avec les attentes des outils web où pratique

Pourquoi un outil de scrape explicite :

- Contourne le bug d'ordre non résolu `Readability -> Firecrawl -> nettoyage HTML basique` dans le `web_fetch` du cœur
- Donne aux utilisateurs un chemin déterministe "toujours utiliser Firecrawl" pour les sites lourds en JS/protégés par bot

## Ce que l'extension ne doit pas faire

- Pas d'ajout automatique de `browser`, `web_search` ou `web_fetch` à `tools.alsoAllow`
- Pas d'étape d'onboarding par défaut dans `openclaw setup`
- Pas de cycle de vie de session de navigateur spécifique à Firecrawl dans le cœur
- Pas de modification de la sémantique de secours `web_fetch` intégrée dans le MVP de l'extension

## Plan de phase

### Phase 1 : extension uniquement, pas de modifications du schéma du cœur

Implémenter :

- `extensions/firecrawl/`
- schéma de configuration du plugin
- `firecrawl_search`
- `firecrawl_scrape`
- tests pour la résolution de configuration, la sélection de point de terminaison, la mise en cache, la gestion des erreurs et l'utilisation de la protection SSRF

Cette phase est suffisante pour livrer une vraie valeur utilisateur.

### Phase 2 : intégration optionnelle du fournisseur `web_search`

Supporter `tools.web.search.provider = "firecrawl"` uniquement après correction de deux contraintes du cœur :

1. `src/plugins/web-search-providers.ts` doit charger les plugins de fournisseur de recherche web configurés/installés au lieu d'une liste groupée codée en dur.
2. `src/config/types.tools.ts` et `src/config/zod-schema.agent-runtime.ts` doivent arrêter de coder en dur l'énumération du fournisseur d'une manière qui bloque les ID enregistrés par le plugin.

Forme recommandée :

- garder les fournisseurs intégrés documentés,
- permettre tout ID de fournisseur de plugin enregistré à l'exécution,
- valider la configuration spécifique au fournisseur via le plugin du fournisseur ou un sac de fournisseur générique.

### Phase 3 : couture optionnelle du fournisseur `web_fetch`

Faire cela uniquement si les mainteneurs veulent que les backends de récupération spécifiques au fournisseur participent à `web_fetch`.

Ajout du cœur nécessaire :

- `registerWebFetchProvider` ou équivalent de couture de backend de récupération

Sans cette couture, l'extension doit garder `firecrawl_scrape` comme un outil explicite plutôt que d'essayer de corriger le `web_fetch` intégré.

## Exigences de sécurité

L'extension doit traiter Firecrawl comme un **point de terminaison configuré par l'opérateur de confiance**, mais doit toujours renforcer le transport :

- Utiliser la récupération gardée SSRF pour l'appel du point de terminaison Firecrawl, pas `fetch()` brut
- Préserver la compatibilité du réseau auto-hébergé/privé en utilisant la même politique de point de terminaison des outils web de confiance utilisée ailleurs
- Ne jamais enregistrer la clé API
- Garder la résolution du point de terminaison/URL de base explicite et prévisible
- Traiter le contenu retourné par Firecrawl comme du contenu externe non fiable

Cela reflète l'intention derrière les PR de renforcement SSRF sans supposer que Firecrawl est une surface multi-locataire hostile.

## Pourquoi pas une compétence

Le dépôt a déjà fermé une PR de compétence Firecrawl en faveur de la distribution ClawHub. C'est bien pour les flux de travail de prompt optionnels installés par l'utilisateur, mais cela ne résout pas :

- la disponibilité déterministe des outils,
- la gestion de configuration/identifiants de qualité fournisseur,
- le support du point de terminaison auto-hébergé,
- la mise en cache,
- les sorties typées stables,
- l'examen de sécurité sur le comportement du réseau.

Cela appartient à une extension, pas à une compétence de prompt uniquement.

## Critères de succès

- Les utilisateurs peuvent installer/activer une extension et obtenir une recherche/scrape Firecrawl fiable sans toucher aux paramètres par défaut du cœur.
- Firecrawl auto-hébergé fonctionne avec configuration/secours env.
- Les récupérations de point de terminaison de l'extension utilisent le réseau gardé.
- Pas de nouveau comportement d'onboarding/par défaut spécifique à Firecrawl du cœur.
- Le cœur peut adopter ultérieurement les coutures `web_search` / `web_fetch` natives du plugin sans redessiner l'extension.

## Ordre d'implémentation recommandé

1. Construire `firecrawl_scrape`
2. Construire `firecrawl_search`
3. Ajouter la documentation et les exemples
4. Si souhaité, généraliser le chargement du fournisseur `web_search` afin que l'extension puisse sauvegarder `web_search`
5. Seulement ensuite envisager une vraie couture du fournisseur `web_fetch`
