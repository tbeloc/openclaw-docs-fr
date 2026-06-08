---
title: "Outils de recherche Web - Note de Maturité de Sécurité Réseau"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Outils de recherche Web - Note de Maturité de Sécurité Réseau

## Résumé

Cette note migre les preuves de maturité archivées pour `Outils de recherche Web` / `Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé` dans l'inventaire de scorecard actuel de la version-3 du processus.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Sécurité Réseau : Définit l'autorisation de Sécurité Réseau, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.
- SSRF : Définit l'autorisation SSRF, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.
- Redirections : Définit l'autorisation des Redirections, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.
- Contenu Non Approuvé : Définit l'autorisation du Contenu Non Approuvé, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.

## Fonctionnalités

- Sécurité Réseau : Définit l'autorisation de Sécurité Réseau, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.
- SSRF : Définit l'autorisation SSRF, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.
- Redirections : Définit l'autorisation des Redirections, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.
- Contenu Non Approuvé : Définit l'autorisation du Contenu Non Approuvé, la confiance, les limites de sécurité et les contrôles d'opérateur pour Sécurité Réseau, SSRF, Redirections et Contenu Non Approuvé.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (84%)`

La couverture est Stable car la documentation et le code source couvrent la politique SSRF, la récupération gardée, les listes blanches d'adresses IP factices, les vérifications de redirection, la politique de point de terminaison auto-hébergé, le proxy d'environnement approuvé, les redirections de citations et l'encapsulation de contenu non approuvé externe. Le score est limité par les demandes actives concernant l'opt-in de réseau privé, la gestion des adresses IPv6 à usage spécial, la parité exec et le renforcement de l'injection de contenu récupéré.

## Score de Qualité

- Score : `Stable (84%)`

La qualité est Stable car les contrôles de sécurité sont centralisés et conservateurs : l'accès réseau passe par la récupération gardée, le comportement DNS et les redirections sont revérifiés, les hôtes privés/internes sont bloqués par défaut, et le contenu récupéré/recherché est explicitement marqué comme non approuvé. Le risque restant se situe dans les exceptions de politique, les opt-ins de réseau local/privé et les exigences de contournement spécifiques au fournisseur.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/web-search-tools.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Sécurité Réseau, SSRF, Redirections, Contenu Non Approuvé.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version-3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/tools/web.md:156` documente le comportement de récupération gardée, les listes blanches d'adresses IP factices, le blocage privé/métadonnées et les vérifications de redirection.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:40` documente les blocages privés/internes et les vérifications de redirection.
- `/Users/kevinlin/code/openclaw/docs/tools/web-fetch.md:146` documente le proxy d'environnement approuvé et ses limites.
- `/Users/kevinlin/code/openclaw/docs/tools/firecrawl.md:139` documente les considérations de sécurité de Firecrawl.
- `/Users/kevinlin/code/openclaw/docs/tools/searxng-search.md:112` documente la configuration du point de terminaison auto-hébergé SearXNG.

### Code Source

- `/Users/kevinlin/code/openclaw/src/agents/tools/web-guarded-fetch.ts:13` définit la politique de point de terminaison auto-hébergé.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-guarded-fetch.ts:41` choisit le comportement de récupération gardée strict ou d'environnement approuvé.
- `/Users/kevinlin/code/openclaw/src/infra/net/fetch-guard.ts:383` implémente les boucles de redirection avec vérifications de politique.
- `/Users/kevinlin/code/openclaw/src/infra/net/fetch-guard.ts:500` épingle les résultats DNS.
- `/Users/kevinlin/code/openclaw/src/infra/net/fetch-guard.ts:594` enregistre les blocages SSRF.
- `/Users/kevinlin/code/openclaw/src/infra/net/ssrf.ts:185` implémente les listes blanches de noms d'hôtes d'adresses IP factices.
- `/Users/kevinlin/code/openclaw/src/infra/net/ssrf.ts:294` bloque les adresses IP privées et à usage spécial.
- `/Users/kevinlin/code/openclaw/src/infra/net/ssrf.ts:535` épingle et revérifie DNS.
- `/Users/kevinlin/code/openclaw/src/security/external-content.ts:13` marque le contenu Web comme non approuvé en externe.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search-citation-redirect.ts:1` résout les redirections de citations via des demandes HEAD gardées.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-fetch.md:11` couvre le comportement d'exécution web_fetch avec les modes d'échec.
- `/Users/kevinlin/code/openclaw/qa/scenarios/runtime/tools/web-search.md:11` couvre le comportement d'exécution web_search avec les modes d'échec.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch.ssrf.test.ts:103` couvre les protections SSRF de web_fetch.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-search.redirect.test.ts:23` couvre le comportement de redirection de citation.
- `/Users/kevinlin/code/openclaw/src/agents/tools/web-fetch-visibility.test.ts:214` couvre le comportement de visibilité autour du contenu récupéré.
- `/Users/kevinlin/code/openclaw/extensions/firecrawl/src/firecrawl-tools.test.ts:606` couvre les cas de sécurité d'URL de Firecrawl.
- `/Users/kevinlin/code/openclaw/extensions/searxng/src/searxng-client.test.ts:160` couvre le comportement de sécurité du point de terminaison SearXNG.
- `/Users/kevinlin/code/openclaw/extensions/google/web-search-provider.test.ts:253` couvre la gestion des redirections Gemini.

### Requêtes Gitcrawl

Fraîcheur : `gitcrawl doctor --json` a signalé la version `0.2.1`, `last_sync_at` `2026-05-28T19:09:52.784704Z`, `29,810` threads, `11,181` threads ouverts et `18,594` clusters.

- `gitcrawl --json search issues -R openclaw/openclaw "SSRF web_fetch"` a retourné #39604 opt-in de réseau privé, #76260 parité exec avec blocage SSRF web_fetch, #39685 pare-feu de sortie, #41993 échecs IPv6 à usage spécial et #87505 régression de délai d'attente.
- `gitcrawl --json search prs -R openclaw/openclaw "web_fetch"` a retourné #67421 politique SSRF par agent, #39630 allowPrivateNetwork, #87758 renforcement de l'injection de contenu récupéré, #55485 politique SSRF et #61961 travail de sécurité connexe.
- `gitcrawl --json search prs -R openclaw/openclaw "provider-web-search"` a retourné #85317 contournement SSRF de réseau privé Gemini et #87758 renforcement de l'injection de contenu récupéré.

### Requêtes Discrawl

Fraîcheur : `discrawl status --json` a signalé l'état `current`, `generated_at` `2026-05-29T17:44:19Z`, `last_sync_at` `2026-05-29T15:59:50Z`, `1,487,061` messages, `25,819` canaux et zéro arriéré d'intégration.

- `discrawl search --mode hybrid --limit 12 "web_fetch ssrf private internal redirect injection"` a trouvé des conseils de support indiquant que web_fetch est plus sûr que l'automatisation exec/navigateur mais reste à haut risque car il extrait du contenu externe non approuvé, bloque les hôtes privés/internes et revérifie les redirections.
