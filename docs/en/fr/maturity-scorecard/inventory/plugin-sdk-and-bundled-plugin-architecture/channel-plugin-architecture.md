---
title: Plugins - Channel Plugins Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Channel Plugins Maturity Note

## Summary

L'architecture des plugins de canal reste `Stable (82%)` pour la couverture et `Beta (78%)`
pour la qualité. OpenClaw dispose d'une véritable architecture au niveau des catégories ici : la documentation actuelle
divise les préoccupations de réception, d'envoi et d'entrée sur des chemins SDK ciblés ; le code source expose
des contrats de plugins de canal typés, des assistants d'entrée canoniques, des contrats d'entrée groupés, un chargement groupé paresseux et des recherches de registre légères ; et les preuves d'exécution couvrent l'intégration groupée, l'installation/désinstallation groupée et la livraison MCP en forme de canal.

La catégorie n'est pas plus élevée car la preuve d'exécution la plus forte s'arrête toujours avant un flux de plugin externe unique construit à partir de la documentation SDK publique et exercé via un comportement d'entrée réel plus un comportement de sortie durable. La qualité reste également en dessous de Stable car l'entrée est toujours explicitement expérimentale, les alias de compatibilité hérités restent partie de la surface de l'opérateur, et les preuves d'archive montrent toujours une confusion ouverte autour des ID de plugin par rapport aux ID de canal, la messagerie de liste d'autorisation et la sécurité relationnelle de sortie.

## Category Scope

Cette catégorie couvre l'architecture des plugins de canal à l'intérieur du SDK Plugin et
la surface d'architecture des plugins groupés :

- Documentation SDK de canal publique et chemins pour `channel-inbound`,
  `channel-outbound`, `channel-ingress-runtime`, et redirections de compatibilité
  depuis les anciens points d'entrée `channel-message` et `channel-turn`.
- Le contrat `ChannelPlugin` typé plus les assistants SDK tels que
  `defineChannelPluginEntry`, `createChatChannelPlugin`, et
  `createChannelPluginBase`.
- Contrats d'entrée de canal groupés et contrats d'entrée de configuration, chargement groupé paresseux, setters d'exécution,
  et recherches de registre pour les plugins de canal groupés et chargés.
- Preuves d'exécution pour l'intégration groupée, le cycle de vie des plugins groupés, et
  les surfaces de livraison Gateway ou MCP en forme de canal qui valident l'architecture de la catégorie.

Hors de portée : maturité du produit par canal, fiabilité de l'API en amont pour tout
transport spécifique, maturité de la distribution ClawHub en dehors de son effet sur le chargement de canal, et
familles de plugins non-canal sauf où elles façonnent directement les limites des plugins de canal.

## Features

- Gestion des événements entrants : Les plugins de canal enregistrent les hooks entrants et normalisent les événements entrants.
- Livraison sortante : Les adaptateurs sortants traduisent la sortie du modèle en charges utiles spécifiques au canal.
- Autorisation d'entrée : L'exécution d'entrée de canal applique la limite d'autorisation entrante partagée.
- Résolution de destination : La résolution de cible mappe les utilisateurs, les threads et les conversations en destinations de canal.
- Invites d'approbation natives : Les actions de canal natives peuvent acheminer les invites d'approbation et les réponses via le système d'approbation.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` a réussi avec
  `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`,
  `open_thread_count=11181`,
  `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`.
- discrawl: `discrawl status --json` a réussi avec
  `generated_at=2026-05-30T00:38:20Z`, `state=current`,
  `summary=1487536 messages across 25831 channels`,
  `last_sync_at=2026-05-29T19:27:40Z`.

## Coverage Score

- Score: `Stable (82%)`
- Signaux positifs :
  - La documentation publique et la source SDK décrivent maintenant clairement une division réception/envoi :
    `channel-inbound` possède la normalisation et l'orchestration entrantes,
    `channel-outbound` possède le comportement d'envoi et de reçu durable, et
    `channel-ingress-runtime` définit une limite d'autorisation entrante partagée.
  - Les flux d'exécution Docker couvrent l'intégration groupée, l'activation de canal, l'état du canal,
    la réparation du docteur, l'installation/désinstallation des plugins groupés, le smoke d'exécution groupé, et la livraison Gateway ou MCP en forme de canal.
  - La couverture des contrats au niveau unitaire est large pour les chemins SDK, les façades de compatibilité,
    les gardes de forme d'entrée groupée, et le comportement d'actualisation du registre, ce qui augmente les preuves de soutien que les limites de catégorie documentées sont délibérées
    et maintenues.
- Signaux négatifs :
  - Le smoke Docker MCP définit explicitement `OPENCLAW_SKIP_CHANNELS=1`, donc il
    prouve le comportement de conversation et de notification en forme de canal sans prouver
    le démarrage complet du plugin dans cette voie.
  - La voie d'intégration groupée valide le comportement d'installation/configuration/état/docteur/agent
    par rapport à l'exécution du modèle simulée, pas la réception de réseau en amont en direct et la livraison de sortie finale durable pour une plateforme de canal réelle.
  - Aucune preuve de flux d'exécution unique n'a été trouvée qui commence à partir de la documentation SDK publique actuelle, construit un plugin de canal tiers, l'installe en externe, exécute la gestion entrante réelle, et complète la livraison de réponse sortante durable via les adaptateurs entrants et sortants documentés.
  - `channel-ingress-runtime` est toujours documenté comme expérimental, et son
    support reste plus fort dans le code source et les contrats unitaires que dans les preuves de migration en direct réutilisables sur plusieurs familles de canaux.
- Lacunes d'intégration :
  - Ajouter un E2E de plugin de canal externe réutilisable qui suit la documentation SDK publique
    et prouve la réception, l'autorisation d'entrée, la livraison sortante durable,
    les reçus, et l'état via Gateway.
  - Ajouter au moins une voie de relecture en direct ou enregistrée en amont pour un canal groupé
    qui exerce le chemin SDK générique entrant et sortant plutôt que seulement la logique de moniteur local du canal.
  - Lier les revendications de compatibilité de catégorie aux preuves de version afin que les chemins de plugins de canal groupés,
    téléchargeables et externes soient prouvés à la même révision.

## Quality Score

- Score: `Beta (78%)`
- Rapports Gitcrawl :
  - `gitcrawl search openclaw/openclaw --query "channel plugin sdk inbound outbound" --json`
    a retourné 20 résultats ouverts. Les résultats pertinents au niveau de la catégorie incluent `#85175`
    demandant la sécurité relationnelle sortante
    (`sendPolicy.peerEquals: "inboundPeer"`), `#87141` renforçant les limites de normalisation du SDK/canal du plugin, `#82039` séparant les listes d'autorisation entrantes et sortantes WhatsApp, et `#61521` reportant la validation de configuration jusqu'à l'assemblage de configuration.
  - `gitcrawl search openclaw/openclaw --query "channel plugin configuration bundled" --json`
    a retourné 20 résultats ouverts. Les résultats de qualité de catégorie les plus pertinents restent
    `#68352` et `#68780` sur la confusion entre ID de plugin et ID de canal et les avertissements de liste d'autorisation non exploitables, plus le travail de renforcement ou de clarification connexe dans
    `#68389` et `#86138`.
  - `gitcrawl threads openclaw/openclaw --numbers 68780,68352,87141,85175 --include-closed --json`
    a confirmé que `#68352` et `#68780` sont toujours des problèmes de configuration ouverts visibles par l'utilisateur, `#85175` est toujours une demande de sécurité ouverte, et `#87141` est une RP de renforcement ouverte sur les limites de normalisation du SDK du plugin ou du canal.
- Rapports Discrawl :
  - `discrawl search --limit 5 "channel plugin sdk"` a retourné des discussions de mainteneur adjacentes plutôt qu'un thread de défaut utilisateur direct pour cette catégorie. Les résultats échantillonnés incluaient un thread `maintainer-security-ops` du 2026-05-27 discutant du renforcement du chargement des plugins de configuration uniquement pour `#86953`, et un thread `maintainers` du 2026-05-26 suggérant que les flux d'approbation d'exécution devraient s'aligner via un SDK de plugin au lieu d'être maintenus indépendamment par chaque canal.
  - Ces résultats Discord sont une pression de catégorie pertinente et une discussion de conception, mais
    ils sont plus faibles que les preuves GitHub pour les problèmes de qualité directs visibles par l'opérateur.
- Bonnes qualités :
  - La documentation explique clairement la limite de propriété : les plugins possèdent la configuration,
    la sécurité, l'appairage, la grammaire de session, le transport sortant, le threading et la saisie de battement cardiaque, tandis que le noyau possède l'outil `message` partagé et la distribution générique.
  - La division réception/envoi est explicite dans la documentation et le code, avec les surfaces entrantes et sortantes séparées au lieu d'une API d'exécution de canal surdimensionnée.
  - Le type `ChannelPlugin` est large mais explicite sur les adaptateurs possédés,
    incluant la configuration, la sécurité, les groupes, les commandes, le cycle de vie, les listes d'autorisation,
    les liaisons, le threading, la messagerie, le résolveur, les actions, le battement cardiaque et les outils d'agent.
  - `defineChannelPluginEntry` et les assistants d'entrée groupés rendent les modes d'enregistrement explicites et évitent de forcer le travail d'exécution complet dans les chemins de métadonnées CLI ou de découverte.
  - Les assistants de registre évitent intentionnellement les importations de canal impatientes et normalisent la recherche de plugins groupés et chargés via des assistants légers.
- Mauvaises qualités :
  - `channel-ingress-runtime` est toujours explicitement expérimental, donc la limite d'autorisation entrante partagée prévue n'est pas encore un contrat stable ennuyeux.
  - Les redirections de compatibilité restent actives pour `channel-message`,
    `channel-message-runtime`, `channel-reply-pipeline`, et `channel-turn`,
    ce qui préserve la sécurité de migration mais augmente la surface conceptuelle pour les auteurs de plugins.
  - Les preuves d'archive montrent toujours une confusion de l'opérateur autour des ID de plugin par rapport aux ID de canal, des avertissements de provenance groupés et de la messagerie de liste d'autorisation.
  - La demande de sécurité relationnelle sortante ouverte dans `#85175` montre que la surface de politique déclarative actuelle ne peut toujours pas exprimer un invariant d'identité inter-canal important de manière centralisée.
- Exclu de la qualité :
  - Présence ou absence de tests unitaires, d'intégration, e2e, en direct ou de flux d'exécution.
  - Le bloqueur de validation locale partagé causé par les échecs d'installation de dépendances
    et les erreurs d'authentification du registre ; c'est un problème d'environnement, pas une preuve de produit pour cette catégorie.
  - Comportement de l'API en amont par canal sauf où il révèle un problème d'architecture de plugin de canal générique.

## Known Gaps

- Publier un fixture de plugin de canal externe minimal canonique qui suit la
  documentation SDK publique et est réutilisé par la validation de compatibilité et de version.
- Réduire l'ambiguïté visible par l'utilisateur entre les ID de canal, les ID de plugin, les ID de plugin groupés, les noms de package et les spécifications d'installation.
- Promouvoir l'entrée hors du statut expérimental seulement après que plusieurs familles de canaux prouvent un comportement d'autorisation cohérent via la surface d'exécution partagée.
- Ajouter une sécurité relationnelle sortante documentée de manière centralisée afin que les plugins de canal n'aient pas besoin de réimplémenter la même garde de correspondance de pair individuellement.
- Produire une matrice de version au niveau de la catégorie qui lie la documentation, le registre, le chargement groupé et la preuve d'exécution ensemble à une révision.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-plugins.md:21`
  définit comment les plugins de canal divisent la propriété entre les adaptateurs de plugins et l'outil `message` partagé.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-plugins.md:37`
  documente l'attente de l'adaptateur `message` sur
  `openclaw/plugin-sdk/channel-outbound`.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-plugins.md:77`
  documente le chemin de migration expérimental `channel-ingress-runtime`.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-inbound.md:16`
  documente `openclaw/plugin-sdk/channel-inbound` comme surface de réception/contexte et d'orchestration.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-outbound.md:10`
  documente `openclaw/plugin-sdk/channel-outbound` comme surface d'envoi durable, de réception et d'aperçu en direct.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-ingress.md:13`
  documente l'entrée de canal comme limite de contrôle d'accès expérimentale.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-message.md:6` conserve
  `channel-message` et `channel-message-runtime` comme alias de compatibilité dépréciés.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-turn.md:6` redirige
  les anciens documents nommés turn vers l'API inbound.
- `/Users/kevinlin/code/openclaw/docs/channels/index.md:18` documente le chargement de canal externe à la demande d'installation.
- `/Users/kevinlin/code/openclaw/docs/channels/index.md:30` documente les états du catalogue de canal groupés, téléchargeables et externes.

### Source

- `/Users/kevinlin/code/openclaw/src/channels/plugins/types.plugin.ts:61`
  définit le contrat typé `ChannelPlugin` et ses surfaces d'adaptateur possédées.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/core.ts:525` implémente
  `defineChannelPluginEntry` et ses modes d'enregistrement explicites.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/core.ts:786` implémente
  `createChatChannelPlugin`.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/core.ts:813` implémente
  `createChannelPluginBase`.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/channel-entry-contract.ts:477`
  implémente les contrats d'entrée de canal groupés.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/channel-entry-contract.ts:575`
  implémente les contrats d'entrée de configuration de canal groupés.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/bundled.ts:31` définit
  les contrats d'exécution de canal groupés chargés paresseusement.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/bundled.ts:870` résout
  les plugins d'exécution et de configuration groupés par ID de canal.
- `/Users/kevinlin/code/openclaw/src/channels/registry.ts:18` conserve la normalisation générique de canal et la recherche de registre légères pour éviter les importations impatientes.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/registry.ts:32` résout
  la recherche de plugin chargé ou groupé via un seul assistant.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-onboard-channel-agent-docker.sh:147`
  exécute l'intégration non-interactive, l'activation de canal, les vérifications de statut, la réparation du docteur et un tour d'agent local simulé pour les canaux empaquetés.
- `/Users/kevinlin/code/openclaw/scripts/e2e/bundled-plugin-install-uninstall-docker.sh:33`
  exécute la voie E2E Docker du cycle de vie du plugin groupé.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:40`
  installe les plugins groupés, sonde la fumée d'exécution et vérifie le nettoyage de la désinstallation.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:678`
  sonde `channels.status` et la visibilité des commandes d'exécution pour les plugins groupés.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker.sh:23`
  exécute la fumée Gateway plus MCP channel tout en ignorant explicitement le démarrage complet du canal dans cette voie.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:50`
  attend les conversations Gateway et MCP ensemencées avec contexte de livraison de canal.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:170`
  vérifie la visibilité de la transcription et des pièces jointes via les outils MCP.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:254`
  injecte des messages en forme de canal et vérifie la livraison d'événements Gateway et MCP.
- `/Users/kevinlin/code/openclaw/scripts/e2e/mcp-channels-docker-client.ts:311`
  vérifie les surfaces de notification de canal et de permission.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-subpaths.test.ts:915`
  vérifie les limites de sous-chemin d'assistant d'exécution de canal dédié.
- `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-subpaths.test.ts:1013`
  vérifie la forme d'exportation `channel-inbound`.
- `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-subpaths.test.ts:1336`
  vérifie que les sous-chemins d'entrée d'exécution représentatifs restent importables.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/channel-message.test.ts:6`
  vérifie que les nouveaux et anciens sous-chemins SDK de canal restent alignés.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/inbound-reply-dispatch.test.ts:153`
  vérifie que les options de livraison de réponse durable circulent via l'enveloppe de commodité SDK.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/bundled.shape-guard.test.ts:196`
  vérifie la découverte d'entrée groupée et le comportement de protection de forme.
- `/Users/kevinlin/code/openclaw/src/channels/plugins/contracts/plugins-core.registry.contract.test.ts:7`
  vérifie l'ordre du registre de canal et le comportement d'actualisation.
- `/Users/kevinlin/code/openclaw/test/helpers/infra/heartbeat-runner-channel-plugins.ts:51`
  définit les accessoires de plugin de canal Slack, Telegram et WhatsApp utilisés par les tests liés à l'exécution et au battement cardiaque.
- Ces tests ont été utilisés uniquement comme preuves d'implémentation ; ils n'ont pas été utilisés pour augmenter la qualité et ne rendent pas la catégorie couverte par eux-mêmes.

### Commandes de validation de surface

- `pnpm plugin-sdk:check-exports`: `bloqué` - valide que l'inventaire d'exportation SDK public enregistré correspond toujours aux points d'entrée actuels, y compris les sous-chemins de canal. Tenté depuis `/Users/kevinlin/code/openclaw`, mais la validation locale a été bloquée avant l'exécution réelle car l'installation des dépendances a échoué avec des erreurs d'authentification de registre 403 pour `@microsoft/teams.cards` et `@microsoft/teams.api` plus `No authorization header was set for the request`.
- `pnpm plugin-sdk:api:check`: `bloqué` - valide la dérive de base de l'API Plugin SDK public. Bloqué par le même échec d'authentification de dépendance locale, donc traité comme du bruit environnemental plutôt que comme preuve de produit.
- `pnpm plugin-sdk:surface:check`: `bloqué` - valide les budgets de taille de surface SDK public et les limites d'exportation dépréciée pour le SDK orienté canal. Bloqué par le même échec d'authentification de dépendance locale avant la validation réelle.
- `pnpm plugins:boundary-report:ci`: `bloqué` - valide la discipline d'importation réservée et de limite de compatibilité sur les surfaces de plugin, y compris les bords d'architecture de canal. Bloqué par le même échec d'authentification de dépendance locale avant la validation réelle.
- `pnpm release:plugins:npm:check`: `bloqué` - valide la préparation à la publication npm pour les plugins publiables et détecterait la dérive des métadonnées de package de canal. Bloqué par le même échec d'authentification de dépendance locale avant la validation réelle.
- `pnpm release:plugins:clawhub:check`: `bloqué` - valide la préparation à la publication ClawHub pour les plugins publiables et exercerait les métadonnées de distribution utilisées par certains canaux téléchargeables. Bloqué par le même échec d'authentification de dépendance locale avant la validation réelle.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "channel plugin sdk inbound outbound" --json`

Résultats :

- A retourné 20 résultats ouverts en mode mot-clé.
- Les résultats pertinents de qualité de catégorie incluaient `#85175` sur la sécurité des pairs sortants relationnels, `#87141` sur le durcissement de normalisation de canal ou de plugin, `#82039` sur les listes blanches entrantes et sortantes séparées, et `#61521` sur la séquençage de validation de configuration.
- Les autres résultats étaient principalement des défauts spécifiques au canal ou des travaux d'exécution adjacents, utilisés comme contexte mais non notés comme des défaillances de catégorie directes sauf s'ils exposaient une limite d'architecture partagée.

Requête :

`gitcrawl search openclaw/openclaw --query "channel plugin configuration bundled" --json`

Résultats :

- A retourné 20 résultats ouverts en mode mot-clé.
- Les résultats de qualité d'opérateur les plus forts restaient `#68352` et `#68780` sur la non-concordance ID de plugin par rapport à ID de canal et les avertissements de liste blanche non exploitables.
- Le travail ouvert connexe `#68389` et `#86138` montre que la zone est toujours en cours de durcissement plutôt que complètement réglée.

Requête :

`gitcrawl threads openclaw/openclaw --numbers 68780,68352,87141,85175 --include-closed --json`

Résultats :

- Confirmé que `#68352` et `#68780` restent des problèmes de configuration visibles par l'utilisateur ouverts.
- Confirmé que `#85175` reste une demande de sécurité au niveau de la catégorie ouverte.
- Confirmé que `#87141` reste une RP de durcissement ouverte touchant le SDK de plugin ou les limites de normalisation de canal.

### Requêtes Discrawl

Requête :

`discrawl search --limit 5 "channel plugin sdk"`

Résultats :

- A retourné des discussions de mainteneur adjacentes plutôt qu'un fil de défaut utilisateur direct pour cette catégorie dans les résultats échantillonnés.
- Un résultat `maintainer-security-ops` du 2026-05-27 a discuté du durcissement du chargement de plugin réservé à la configuration pour `#86953`, qui est adjacent aux limites de chargement de canal.
- Un résultat `maintainers` du 2026-05-26 a suggéré que les flux d'approbation devraient s'aligner via un SDK de plugin au lieu de rester spécifiques au canal, ce qui est une pression de conception de catégorie pertinente mais pas une preuve de bogue direct.
