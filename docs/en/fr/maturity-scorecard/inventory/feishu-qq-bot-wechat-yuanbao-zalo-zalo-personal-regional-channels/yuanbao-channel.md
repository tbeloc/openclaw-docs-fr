---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Yuanbao Channel Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Yuanbao Channel Maturity Note

## Résumé

La documentation Yuanbao décrit un canal externe prêt pour la production pour les DM de bot et les chats de groupe sur WebSocket, avec des menus de commandes slash natifs, l'historique de groupe, le streaming de blocs, la configuration multi-compte et l'ajustement de la livraison des messages. Le noyau OpenClaw contient l'entrée de catalogue externe officielle et les tests d'installation/statut/contrat, mais la source d'exécution Yuanbao ne se trouve pas dans ce référentiel. La couverture est donc Expérimentale pour cet audit, même si la documentation est beaucoup plus riche que la source visible. La qualité est quelque peu meilleure que la couverture car la documentation et les métadonnées du catalogue sont cohérentes, mais les preuves d'archive montrent un couplage catalog-id/version et un risque de chargement/refactorisation de plugin externe.

## Portée de la catégorie

- Canal externe Tencent Yuanbao `openclaw-plugin-yuanbao`.
- Configuration AppKey/AppSecret, assistant de connexion, configuration multi-compte et routage de compte par défaut.
- DM, groupes, exigences de mention, mode réponse, contexte d'historique de groupe, menus de commandes slash et réponses de secours.
- Stratégie de file d'attente sortante, ajustement du texte fusionné, nombre maximum de caractères, limites de médias, comportement de débordement et streaming au niveau des blocs.
- Catalogue externe officiel côté noyau, métadonnées d'installation, alias, textes d'assistant et contrats de catalogue de canaux.

## Fonctionnalités

- Canal externe Tencent Yuanbao : Canal externe Tencent Yuanbao openclaw-plugin-yuanbao
- Configuration AppKey/AppSecret : Configuration AppKey/AppSecret, assistant de connexion, configuration multi-compte et routage de compte par défaut
- DM : DM, groupes, exigences de mention, mode réponse, contexte d'historique de groupe, menus de commandes slash et réponses de secours
- Stratégie de file d'attente sortante : Stratégie de file d'attente sortante, ajustement du texte fusionné, nombre maximum de caractères, limites de médias, comportement de débordement et streaming au niveau des blocs
- Catalogue externe officiel côté noyau : Catalogue externe officiel côté noyau, métadonnées d'installation, alias, textes d'assistant et contrats de catalogue de canaux

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimentale (47%)`
- Signaux positifs : la documentation est détaillée et les tests principaux prouvent les métadonnées du catalogue externe officiel, la spécification d'installation, les contrats de catalogue de canaux, les avertissements de configuration, les textes d'assistant et la plomberie de réparation/installation.
- Signaux négatifs : la source d'exécution Yuanbao et les tests d'exécution sont externes à ce référentiel ; aucun scénario d'application Yuanbao en direct actuel n'a été trouvé ici.
- Lacunes d'intégration : aucune preuve en repo pour la connexion WebSocket Yuanbao, l'approbation de l'application, la livraison DM/groupe, la synchronisation des commandes slash natives, le streaming de blocs, l'historique de groupe, les réponses de secours, les médias ou le comportement multi-compte par rapport à la plateforme réelle.

Étiquettes de couverture :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Bêta` : 70-80
- `Alpha` : 50-70
- `Expérimentale` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Alpha (55%)`
- Rapports Gitcrawl : la recherche large `Yuanbao` a retourné la RP liée au catalogue `#81736` utilisant Yuanbao comme précédent de catalogue externe officiel existant ; la source d'archive/changelog montre également des augmentations de version et des corrections de catalog-id.
- Rapports Discrawl : la recherche `Yuanbao` a retourné une discussion de version/rétroport autour d'une correction de catalog-id Yuanbao, des entrées Freshbits pour l'emplacement GitHub du plugin Yuanbao et l'entrée de documentation, et des commentaires de mainteneur sur Yuanbao et WeCom tirant du code Matrix/Mattermost qui devait être découplé.
- Bonnes qualités : la documentation définit clairement les attentes d'installation/configuration/opération, énumère les clés de configuration et les valeurs par défaut, et identifie les contrôles de livraison des messages ; le catalogue externe officiel épingle la spécification npm `openclaw-plugin-yuanbao@2.13.1` et marque les alias incluant `元宝`.
- Mauvaises qualités : opacité d'exécution, couplage de catalogue/version externe et preuves d'archive de réparations de catalog-id et de couplage de dépendances signifient que le support dépend de l'hygiène du plugin et du catalogue en amont.
- Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel ; ce sont uniquement des entrées de couverture.

Étiquettes de qualité :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Bêta` : 70-80
- `Alpha` : 50-70
- `Expérimentale` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel comme entrée de notation.

## Score de complétude

- Score : `Expérimentale (47%)`
- Instructions de surface : évaluées par rapport à `references/completeness/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels.md`.
- Signaux positifs : les preuves de documentation, source, test, Gitcrawl et Discrawl archivées couvrent la portée de la taxonomie pour le canal externe Tencent Yuanbao, la configuration AppKey/AppSecret, les DM, la stratégie de file d'attente sortante, le catalogue externe officiel côté noyau.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter ou lier une fiche d'évaluation d'exécution Yuanbao actuelle couvrant l'approbation de l'application, la connexion WebSocket, les DM, les groupes, les commandes slash natives, le streaming de blocs, les réponses de secours, les médias et le comportement multi-compte.
- Maintenir la spécification npm du catalogue, l'intégrité, le chemin de documentation et l'id de canal alignés avec la version du plugin externe.
- Documenter la propriété d'exécution externe et les limites de support aussi clairement que la documentation WeChat le fait.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/yuanbao.md` décrit Tencent Yuanbao comme un canal WebSocket externe pour les DM et les chats de groupe, avec configuration appKey/appSecret, assistant de connexion, politique DM, mentions de groupe, comportement de réponse, menus de commandes slash, réponses de secours, configuration multi-compte, limites de messages, streaming de blocs, historique de groupe, liaisons de routage de canal et référence de configuration complète.
- `/Users/kevinlin/code/openclaw/docs/channels/index.md` énumère Yuanbao comme plugin externe du bot Tencent Yuanbao.

### Source

- `/Users/kevinlin/code/openclaw/scripts/lib/official-external-channel-catalog.json` définit `openclaw-plugin-yuanbao`, id de canal `yuanbao`, alias `yuanbao`, `yb`, `tencent-yuanbao` et `元宝`, outils `query_group_info`, `query_session_members` et `yuanbao_remind`, et spécification npm `openclaw-plugin-yuanbao@2.13.1`.
- `/Users/kevinlin/code/openclaw/src/wizard/i18n/locales/en.ts`, `zh-CN.ts` et `zh-TW.ts` incluent les textes de configuration Yuanbao.
- `/Users/kevinlin/code/openclaw/src/logging/subsystem.ts`, `src/config/config.plugin-validation.test.ts` et `src/channels/plugins/catalog.ts` incluent le comportement du catalogue/statut Yuanbao côté noyau.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/plugins/official-external-plugin-catalog.test.ts`, `src/channels/plugins/contracts/channel-catalog.contract.test.ts`, `src/channels/plugins/contracts/test-helpers/channel-plugin-catalog-contract-suites.ts`, `src/channels/plugins/catalog.test.ts`, `src/cli/plugins-cli.install.test.ts` et `src/commands/channels.status.command-flow.test.ts` exercent le catalogue, l'installation et le comportement de statut utilisés par Yuanbao.
- Aucun scénario de plateforme Yuanbao en direct actuel en repo n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/config/config.plugin-validation.test.ts`, `src/channels/plugins/catalog.test.ts`, `src/plugins/official-external-plugin-catalog.test.ts` et `src/channels/plugins/contracts/channel-catalog.contract.test.ts` couvrent le comportement du catalogue et de la validation Yuanbao ciblé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Yuanbao sourceReplyDeliveryMode group chat fallback reply block streaming" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "Yuanbao" --json --limit 8`

Résultats :

- La requête spécifique aux fonctionnalités n'a retourné aucun résultat.
- La requête large Yuanbao a retourné la RP ouverte `#81736` ajoutant DingTalk au catalogue de canaux externes officiels tout en citant les entrées externes WeCom, Yuanbao et Weixin existantes.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "Yuanbao"`

Résultats :

- A retourné une discussion de version/rétroport identifiant la correction de catalog-id Yuanbao `#75003`/commit `099037c` comme importante si la bêta incluait l'entrée de catalogue cassée, les entrées Freshbits pour l'emplacement GitHub du plugin Yuanbao et l'entrée de documentation, et la discussion du mainteneur que Yuanbao et WeCom chargeant du code Matrix/Mattermost devait être découplé.
