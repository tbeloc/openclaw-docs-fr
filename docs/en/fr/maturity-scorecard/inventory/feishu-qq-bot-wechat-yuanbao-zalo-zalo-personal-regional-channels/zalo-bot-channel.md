---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Zalo Bot Channel Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Zalo Bot Channel Maturity Note

## Résumé

Le canal bot Zalo est documenté comme expérimental et la documentation est honnête sur les limites des bots Marketplace : les DM fonctionnent, le support des groupes n'est pas disponible pour les bots Marketplace actuels, le comportement des médias est limité, les aperçus de liens et les médias non-texte ne sont pas fiables, et le streaming est bloqué par la limite d'API de 2000 caractères. La source et les tests couvrent le polling, les webhooks, la protection contre la relecture, l'appairage, les portes de politique de groupe, la gestion des charges utiles de médias, la configuration de compte, les problèmes de statut et les envois sortants. Le score reste Alpha car le support d'exécution est utile mais limité en portée, et la preuve publique en direct est plus faible que la surface source/test.

## Portée de la catégorie

- Canal DM du créateur de bot Zalo / bot Marketplace.
- Mode de polling long par défaut et mode webhook HTTPS optionnel.
- Jeton bot, fichier de jeton, multi-compte, appairage DM et comportement de liste d'autorisation.
- Schéma de politique de groupe et portes de groupe fermées même où les groupes Marketplace ne sont pas utilisables.
- Texte, espaces réservés de médias, chunking sortant, déduplication de relecture, limitation de débit, secrets webhook et support proxy.
- Sondes de statut et dépannage pour les problèmes de jeton/config/webhook.

## Fonctionnalités

- Créateur de bot Zalo / bot Marketplace : Canal DM du créateur de bot Zalo / bot Marketplace
- Mode de polling long par défaut : Mode de polling long par défaut et mode webhook HTTPS optionnel
- Jeton bot : Jeton bot, fichier de jeton, multi-compte, appairage DM et comportement de liste d'autorisation
- Schéma de politique de groupe : Schéma de politique de groupe et portes de groupe fermées même où les groupes Marketplace ne sont pas utilisables
- Texte : Texte, espaces réservés de médias, chunking sortant, déduplication de relecture, limitation de débit, secrets webhook et support proxy
- Sondes de statut : Sondes de statut et dépannage pour les problèmes de jeton/config/webhook

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (60%)`
- Signaux positifs : les tests d'extension couvrent le polling, le webhook, la gestion durable, l'appairage, la politique de groupe, la réponse aux médias, les contrats de charge utile sortante, la configuration, le statut, les jetons, les comptes et l'autorisation d'approbation.
- Signaux négatifs : la documentation indique que le comportement actuel des bots Marketplace est orienté vers les DM, les groupes ne sont pas disponibles en pratique, le comportement des médias et des aperçus de liens est limité, et aucun scénario actuel de Marketplace/OA Zalo en direct n'a été trouvé.
- Lacunes d'intégration : la preuve en direct manque pour la configuration du jeton du bot Marketplace, l'enregistrement du webhook, l'appairage de l'expéditeur, le comportement des médias, la gestion de la relecture/limitation de débit et toute surface de produit Zalo alternative comme le comportement du compte officiel.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux frontières partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel sur le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Alpha (56%)`
- Rapports Gitcrawl : la recherche large `Zalo` a retourné des résultats ouverts pour les ID de chat non numériques, les valeurs par défaut max des médias Zalo, l'analyse response.ok, la visibilité des erreurs de livraison et plusieurs éléments zalouser adjacents ; les recherches spécifiques de relecture/requête n'ont retourné aucun résultat.
- Rapports Discrawl : la recherche Zalo a retourné une discussion d'archive sur le comportement fermé par défaut du rejet de fichier symlink secret, le contexte de refactorisation du canal d'entrée listant Zalo parmi les arbres de politique dupliqués, la fermeture obsolète d'un ancien rapport d'exposition de credentials Nostr/Zalo et les commits récents pour accélérer le polling Zalo et affiner les imports du moniteur.
- Bonnes qualités : la documentation énonce directement les limites et évite de surprometteur le support des groupes/médias ; la source inclut les vérifications de secret webhook, l'exigence HTTPS, la déduplication de relecture, la limitation de débit, le rejet de symlink de fichier de jeton, les valeurs par défaut d'appairage DM et le signalement des problèmes de statut.
- Mauvaises qualités : la surface du produit est fragmentée entre les bots Marketplace et d'autres produits Zalo, la configuration de groupe existe sans support pratique de groupe Marketplace et le comportement des médias/aperçu de lien reste explicitement incertain.
- Exclu de la qualité : la présence ou l'absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ce sont uniquement des entrées de couverture.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux frontières partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score de complétude

- Score : `Alpha (60%)`
- Instructions de surface : évaluées par rapport à `references/completeness/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le créateur de bot Zalo / bot Marketplace, le mode de polling long par défaut, le jeton bot, le schéma de politique de groupe, le texte, les sondes de statut.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve de scénario Zalo Marketplace-bot en direct pour la configuration du jeton, l'appairage DM, le polling, le webhook, les envois sortants, les médias et le comportement de relecture/retry.
- Diviser ou documenter tout comportement de compte officiel Zalo séparément du comportement du bot Marketplace.
- Maintenir les documents de médias/aperçu de lien et de comportement de groupe alignés avec les changements de produit Zalo en amont.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/zalo.md` étiquette Zalo comme expérimental, documente l'état du plugin fourni, la configuration du jeton/env/config, l'appairage DM, le polling long par défaut, le mode webhook, le chunking de texte de 2000 caractères, le plafond de médias de 5 MB, le blocage du streaming, les limites du schéma de groupe et le tableau des capacités du bot Marketplace.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/zalo.md` identifie le package `@openclaw/zalo`, la route d'installation `npm; ClawHub` et la surface `channels: zalo`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/zalo/src/channel.ts`, `channel.runtime.ts`, `runtime.ts`, `monitor.ts`, `monitor.webhook.ts` et `monitor-durable.ts` implémentent l'enregistrement du canal, l'exécution, le monitoring de polling/webhook et le comportement de réception durable.
- `/Users/kevinlin/code/openclaw/extensions/zalo/src/token.ts`, `accounts.ts`, `config-schema.ts`, `secret-input.ts`, `secret-contract.ts`, `setup-core.ts`, `setup-surface.ts` et `status-issues.ts` implémentent les chemins de credentials/config/setup/status.
- `/Users/kevinlin/code/openclaw/extensions/zalo/src/group-access.ts`, `setup-allow-from.ts`, `approval-auth.ts`, `session-route.ts`, `send.ts`, `outbound-media.ts`, `api.ts`, `proxy.ts` et `actions.ts` implémentent l'accès, l'appairage, le routage, les envois, les médias, l'API, le proxy et les actions.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/vitest/vitest.extension-zalo.config.ts` définit le projet de test Zalo dédié.
- `/Users/kevinlin/code/openclaw/extensions/zalo/src/monitor.lifecycle.test.ts`, `monitor.reply-once.lifecycle.test.ts`, `monitor.pairing.lifecycle.test.ts`, `monitor.webhook.test.ts`, `monitor-durable.test.ts`, `monitor.image.polling.test.ts`, `monitor.polling.media-reply.test.ts`, `channel.runtime.ts`, `channel.startup.test.ts` et `outbound-payload.contract.test.ts` couvrent le comportement du flux de canal.
- Aucun scénario actuel de Marketplace ou de plateforme OA Zalo n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/zalo/src/api.test.ts`, `token.test.ts`, `accounts.test.ts`, `config-schema.test.ts`, `setup-surface.test.ts`, `send.test.ts`, `outbound-media.test.ts`, `group-policy.test.ts`, `setup-status.test.ts`, `status-issues.test.ts` et `approval-auth.test.ts` couvrent le comportement focalisé de l'API, des credentials, de la config, de la configuration, de l'envoi, de la politique, du statut et de l'authentification.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Zalo webhook replay dedupe account path target scope marketplace bot" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "Zalo" --json --limit 8`

Résultats :

- La requête spécifique à la fonctionnalité n'a retourné aucun résultat.
- La requête large Zalo a retourné des résultats ouverts incluant `#57594` ID de chat sortant non numériques proactifs, `#57608` valeur par défaut max des médias Zalo, `#62740` gestion response.ok et éléments Zalo Personal adjacents tels que la surfacing des erreurs de livraison et les métadonnées de citation.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 6 "Zalo Marketplace bot group media webhook"`
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "Zalo"`

Résultats :

- La requête spécifique à la fonctionnalité n'a retourné aucun résultat.
- La requête large Zalo a retourné une discussion de mainteneur autour du rejet de symlink de credentials Zalo/autre canal, une note de refactorisation du canal d'entrée listant Zalo parmi les plugins avec la logique de politique en amont dupliquée, la fermeture obsolète d'un ancien rapport d'exposition de credentials Nostr/Zalo et les commits pour accélérer le polling Zalo et affiner les imports du moniteur.
