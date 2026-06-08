---
title: "Channel framework - Channel Setup Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Channel framework - Channel Setup Maturity Note

## Résumé

La surface de configuration de canal est largement implémentée et activement utilisée. Elle dispose d'un index de documentation pour les canaux pris en charge, d'un catalogue piloté par manifeste pour les plugins de canal groupés et externes, d'un filtrage de catalogue de confiance, de flux d'installation au moment de la configuration, de sélection de canal au premier lancement, d'adaptateurs de configuration de compte, et de surfaces CLI de statut/liste qui distinguent les canaux configurés, disponibles et installables.

La principale limite de maturité n'est pas l'absence d'un cadre. C'est que la surface a encore plusieurs arêtes vives opérationnelles actives : la relation docs/catalogue n'est pas entièrement générée ou appliquée, les limites de métadonnées sûres pour la configuration sont toujours en cours de renforcement, et le comportement d'installation à la demande/configuration de canal a un historique récent de régressions ou de confusion des responsables.

## Portée de la catégorie

Inclus dans cette catégorie :

- Catalogue de canaux pris en charge : Catalogue de canaux pris en charge et index de documentation
- Taxonomie de statut de canal dans la liste des canaux : Taxonomie de statut de canal dans la liste des canaux, statut des canaux et sortie de statut de configuration
- Flux de configuration/intégration : Flux de configuration/intégration, y compris la sélection de canal au premier lancement et la configuration du compte de canal
- Installation à la demande : Installation à la demande, distinctions téléchargeables, groupées, externes officielles, locales, npm et ClawHub
- Métadonnées de l'assistant de configuration : Métadonnées de l'assistant de configuration et points d'entrée de plugin sûrs pour la configuration

## Fonctionnalités

- Catalogue de canaux pris en charge : Catalogue de canaux pris en charge et index de documentation
- Taxonomie de statut de canal dans la liste des canaux : Taxonomie de statut de canal dans la liste des canaux, statut des canaux et sortie de statut de configuration
- Flux de configuration/intégration : Flux de configuration/intégration, y compris la sélection de canal au premier lancement et la configuration du compte de canal
- Installation à la demande : Installation à la demande, distinctions téléchargeables, groupées, externes officielles, locales, npm et ClawHub
- Métadonnées de l'assistant de configuration : Métadonnées de l'assistant de configuration et points d'entrée de plugin sûrs pour la configuration

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs :
  - L'index de documentation énumère l'ensemble des canaux pris en charge et marque explicitement plusieurs distinctions de livraison/installation, y compris l'installation à la demande WhatsApp et les étiquettes de canal groupé/téléchargeable/externe (`docs/channels/index.md:18`, `docs/channels/index.md:28`, `docs/channels/index.md:30`).
  - La couverture source s'étend à la construction de catalogue, aux catalogues de secours officiels/externes, aux compartiments de configuration installés/installables, au secours d'espace de travail de confiance, à la sélection de l'assistant de configuration au premier lancement, `channels add`, `channels list` et `channels status` (`src/channels/plugins/catalog.ts:418`, `src/commands/channel-setup/discovery.ts:69`, `src/commands/channel-setup/trusted-catalog.ts:82`, `src/wizard/setup.ts:783`, `src/flows/channel-setup.ts:112`, `src/commands/channels/list.ts:144`, `src/commands/channels/status.ts:78`).
  - La couverture E2E Docker vérifie l'intégration de tarball npm, `channels add`, les surfaces de statut, `doctor` et un tour d'agent pour Telegram/Discord/Slack (`scripts/e2e/npm-onboard-channel-agent-docker.sh:147`, `scripts/e2e/npm-onboard-channel-agent-docker.sh:164`, `scripts/e2e/npm-onboard-channel-agent-docker.sh:168`, `scripts/e2e/npm-onboard-channel-agent-docker.sh:184`).
  - Un test de fumée Docker de plugin groupé exerce les points d'entrée de balayage d'installation/désinstallation de plugin groupé (`scripts/e2e/bundled-plugin-install-uninstall-docker.sh:33`, `scripts/e2e/bundled-plugin-install-uninstall-docker.sh:40`).
- Signaux négatifs :
  - Les preuves de flux Docker réel sont concentrées sur un petit ensemble de canaux courants plutôt que sur le catalogue complet.
  - La large matrice de configuration est principalement couverte par des tests unitaires/harnais E2E plutôt que par une configuration de service externe en direct pour chaque canal externe officiel.
  - La taxonomie de statut et la correction du chemin de documentation sont testées par morceaux, mais il n'y a aucune preuve de bout en bout unique que chaque chemin de documentation de catalogue a une page de documentation correspondante et un chemin de configuration au premier lancement.
- Lacunes d'intégration :
  - Aucun balayage de catalogue complet en direct qui tente la configuration/liste/statut pour chaque canal externe officiel installable.
  - Aucune preuve que chaque page de documentation par canal est générée ou vérifiée directement à partir des métadonnées du catalogue.

## Score de qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl :
  - L'archive montre des ajouts de catalogue de canaux actifs et un travail de renforcement de la configuration, y compris la PR #81736 pour une nouvelle entrée de catalogue de canaux externes officiels et la PR #86953 pour le chargement de canaux de configuration uniquement d'espace de travail non approuvé.
  - Les résultats de recherche montrent également un travail adjacent d'inadéquation d'intégration/catalogue et un problème de canal WhatsApp, mais aucun large cluster actuel uniquement sur le cadre de catalogue/configuration.
- Rapports Discrawl :
  - La discussion des responsables le 2026-04-24 a souligné que les charges de découverte/statut/catalogue de configuration doivent rester légères, tandis que l'intégration/configuration sélectionnée explicite peut nécessiter une préparation de dépendance d'exécution pour WhatsApp.
  - Les commentaires d'examen sur la PR #62934 et la PR #50596 ont signalé des pages de documentation manquantes pour les métadonnées `docsPath` annoncées, causant des liens « En savoir plus » de catalogue/configuration vers 404.
  - La discussion de sécurité sur la PR #86953 a décrit une lacune d'exécution de plugin de configuration uniquement d'espace de travail désactivée et le chemin de renforcement de fermeture d'échec.
- Bonnes qualités :
  - La résolution de catalogue est soutenue par un manifeste et fusionne les entrées de catalogue découvertes, de secours officielles et externes avec des règles de priorité explicites (`src/channels/plugins/catalog.ts:421`, `src/channels/plugins/catalog.ts:452`, `src/channels/plugins/catalog.ts:460`).
  - Les assistants de catalogue de confiance empêchent les ombres d'espace de travail non approuvé d'être sélectionnées par les flux de configuration/ajout normaux tout en préservant la découverte de configuration où approprié (`src/commands/channel-setup/trusted-catalog.ts:17`, `src/commands/channel-setup/trusted-catalog.ts:56`, `src/commands/channel-setup/trusted-catalog.ts:90`).
  - Les choix d'installation sont explicitement modélisés comme ClawHub, npm, local et ignorer, avec masquage de chemin local groupé pour éviter les invites de téléchargement trompeuses (`src/commands/onboarding-plugin-install.ts:42`, `src/commands/onboarding-plugin-install.ts:345`, `src/commands/onboarding-plugin-install.ts:361`).
  - La documentation de l'assistant de configuration indique aux auteurs de plugins d'utiliser des points d'entrée sûrs pour la configuration et des surfaces d'installation optionnelle plutôt que des charges de canal lourdes d'exécution (`docs/plugins/sdk-channel-plugins.md:199`, `docs/plugins/sdk-channel-plugins.md:218`, `docs/plugins/sdk-channel-plugins.md:241`).
- Mauvaises qualités :
  - La relation entre l'index de documentation et le chemin de documentation par canal reste partiellement pilotée par convention ; les preuves d'archive montrent les examinateurs détectant les pages de documentation manquantes après l'introduction des métadonnées.
  - Les limites de plan de contrôle sûres pour la configuration sont toujours en cours de raffinement, en particulier pour le chargement de plugin de configuration uniquement, la préparation de dépendance d'exécution et la confiance d'espace de travail.
  - Les concepts de statut d'opérateur sont utiles mais dispersés dans les formateurs de documentation, source, instantanés de plugin et champs JSON CLI plutôt que présentés comme une taxonomie canonique unique.
- Exclu de la qualité :
  - Les preuves de test et E2E ont été notées uniquement sous Couverture.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/channel-framework.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de taxonomie pour le Catalogue de canaux pris en charge, la Taxonomie de statut de canal dans la liste des canaux, les Flux de configuration/intégration, l'Installation à la demande, les Métadonnées de l'assistant de configuration.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre d'écart connu utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les mises en garde visibles par l'opérateur.

## Lacunes connues

- Ajouter une porte de cohérence catalogue/documentation qui vérifie chaque `docsPath` de catalogue par rapport à une page réelle, ou générer l'index de documentation à partir des métadonnées du catalogue.
- Terminer la limite de configuration d'abord les métadonnées afin que les chemins de découverte/statut/catalogue de configuration n'aient pas besoin d'importations lourdes d'exécution sauf si le canal sélectionné les exige explicitement.
- Élargir la couverture de flux en direct ou Docker au-delà de Telegram/Discord/Slack et du balayage groupé aux canaux d'installation à la demande externes officiels représentatifs.
- Consolider la taxonomie de statut visible par l'opérateur pour installé/disponible/installable/configuré/activé/lié/en cours d'exécution/connecté dans un tableau de documentation lié aux champs JSON CLI.
- Rendre le comportement de configuration au premier lancement pour les sélections d'installation à la demande ignorées ou échouées visiblement cohérent entre les chemins de fournisseur et de canal.

## Preuves

### Docs

- `docs/channels/index.md:9` décrit les canaux comme des applications de chat connectées à la passerelle ; `docs/channels/index.md:18` documente WhatsApp comme installation à la demande ; `docs/channels/index.md:28` commence le catalogue de canaux pris en charge ; `docs/channels/index.md:30` à `docs/channels/index.md:54` listent Discord, Feishu, Google Chat, iMessage, IRC, LINE, Matrix, Mattermost, Teams, Nextcloud Talk, Nostr, QQ Bot, Signal, Slack, Synology Chat, Telegram, Tlon, Twitch, Voice Call, WebChat, WeChat, WhatsApp, Yuanbao, Zalo et Zalo Personal.
- `docs/channels/index.md:58` à `docs/channels/index.md:64` expliquent les canaux simultanés, les conseils de configuration la plus rapide, le comportement des groupes, l'application de l'appairage/liste blanche, le dépannage et la documentation des fournisseurs séparés.
- `docs/channels/pairing.md:18` à `docs/channels/pairing.md:48` documentent le comportement d'appairage DM, les commandes d'approbation du code d'appairage et les canaux d'appairage pris en charge.
- `docs/channels/troubleshooting.md:11` à `docs/channels/troubleshooting.md:29` définissent l'échelle de dépannage de canal de base et la ligne de base d'état sain ; `docs/channels/troubleshooting.md:49` à `docs/channels/troubleshooting.md:160` fournissent des signatures de dépannage par canal.
- `docs/plugins/sdk-channel-plugins.md:199` à `docs/plugins/sdk-channel-plugins.md:245` définissent les surfaces SDK sûres pour la configuration, `openclaw.setupEntry`, les surfaces de configuration de canal optionnelles et le comportement requis pour l'installation des surfaces de configuration.

### Source

- `src/channels/plugins/catalog.ts:23` à `src/channels/plugins/catalog.ts:50` définissent les formes d'entrée UI/catalogue, les métadonnées d'installation, l'origine et les drapeaux de source de confiance.
- `src/channels/plugins/catalog.ts:78` à `src/channels/plugins/catalog.ts:129` résolvent les chemins de catalogue externe à partir des valeurs par défaut env/config ; `src/channels/plugins/catalog.ts:189` à `src/channels/plugins/catalog.ts:223` résolvent les candidats de fichier catalogue officiel et les entrées externes officielles intégrées.
- `src/channels/plugins/catalog.ts:255` à `src/channels/plugins/catalog.ts:323` déduisent les valeurs par défaut de la source d'installation et les métadonnées du chemin npm/ClawHub/local ; `src/channels/plugins/catalog.ts:325` à `src/channels/plugins/catalog.ts:371` construisent les entrées de catalogue à partir des manifestes de plugin.
- `src/channels/plugins/catalog.ts:418` à `src/channels/plugins/catalog.ts:483` fusionnent les entrées de catalogue découvertes, de secours officiel et externes avec la priorité d'origine/secours et le tri d'affichage.
- `src/channels/bundled-channel-catalog-read.ts:36` à `src/channels/bundled-channel-catalog-read.ts:60` lisent les métadonnées du package d'extension groupé en mode dégradé ; `src/channels/bundled-channel-catalog-read.ts:122` à `src/channels/bundled-channel-catalog-read.ts:141` fusionnent les métadonnées du package groupé avec le secours du catalogue officiel.
- `src/channels/chat-meta-shared.ts:36` à `src/channels/chat-meta-shared.ts:54` construisent la carte de métadonnées de canal de chat groupée à partir des entrées de catalogue de canal groupé.
- `src/channels/plugins/types.core.ts:178` à `src/channels/plugins/types.core.ts:201` définissent les champs `ChannelMeta` utilisés par les docs, les sélecteurs et les surfaces de configuration ; `src/channels/plugins/types.core.ts:203` à `src/channels/plugins/types.core.ts:269` définissent les champs d'instantané d'état.
- `src/commands/channel-setup/discovery.ts:69` à `src/commands/channel-setup/discovery.ts:178` résolvent les entrées de catalogue installées et installables et fusionnent les métadonnées groupées/plugin/catalogue dans les entrées du sélecteur de configuration.
- `src/commands/channel-setup/trusted-catalog.ts:17` à `src/commands/channel-setup/trusted-catalog.ts:53` contrôlent les entrées de catalogue d'espace de travail non fiables ; `src/commands/channel-setup/trusted-catalog.ts:82` à `src/commands/channel-setup/trusted-catalog.ts:96` exposent les listes de catalogue de confiance et de découverte de configuration.
- `src/wizard/setup.ts:783` à `src/wizard/setup.ts:803` appellent la configuration de canal lors de l'intégration au premier lancement, avec les valeurs par défaut de démarrage rapide et le comportement d'état différé.
- `src/flows/channel-setup.ts:112` à `src/flows/channel-setup.ts:254` préchargent les plugins externes configurés, collectent l'état de configuration, confirment la configuration et affichent un guide de canal ; `src/flows/channel-setup.ts:323` à `src/flows/channel-setup.ts:358` ajoutent des indices de sélection de catalogue installable ; `src/flows/channel-setup.ts:580` à `src/flows/channel-setup.ts:713` gèrent l'installation du catalogue, la récupération de canal externe obsolète et l'activation du plugin groupé.
- `src/commands/onboarding-plugin-install.ts:303` à `src/commands/onboarding-plugin-install.ts:342` résolvent les valeurs par défaut d'installation ; `src/commands/onboarding-plugin-install.ts:345` à `src/commands/onboarding-plugin-install.ts:441` construisent les invites d'installation ClawHub/npm/local/skip et masquent les options distantes pour les sources locales groupées.
- `src/commands/channels/list.ts:125` à `src/commands/channels/list.ts:142` formatent l'état installé/configuré/activé du catalogue uniquement ; `src/commands/channels/list.ts:238` à `src/commands/channels/list.ts:300` distinguent les origines de canal configurées, disponibles et installables.
- `src/commands/channels/status.ts:78` à `src/commands/channels/status.ts:212` formatent les bits d'état de canal de passerelle en direct ; `src/commands/channels/status-config-format.ts:34` à `src/commands/channels/status-config-format.ts:143` formatent l'état de secours du catalogue uniquement et les indices de réparation de plugin externe officiel manquant.

### Tests d'intégration

- `scripts/e2e/npm-onboard-channel-agent-docker.sh:27` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:33` paramètrent le E2E Docker sur Telegram, Discord et Slack.
- `scripts/e2e/npm-onboard-channel-agent-docker.sh:147` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:171` exécutent l'intégration non-interactive, vérifient l'absence/présence de dépendance en mode package, exécutent `openclaw channels add` et vérifient les surfaces `channels status`/`status`.
- `scripts/e2e/npm-onboard-channel-agent-docker.sh:173` à `scripts/e2e/npm-onboard-channel-agent-docker.sh:201` exécutent le docteur, configurent un modèle simulé et vérifient un tour d'agent local après la configuration du canal.
- `scripts/e2e/bundled-plugin-install-uninstall-docker.sh:33` à `scripts/e2e/bundled-plugin-install-uninstall-docker.sh:47` exécutent le balayage Docker d'installation/désinstallation du plugin groupé.
- `src/commands/onboard-channels.e2e.test.ts:624` à `src/commands/onboard-channels.e2e.test.ts:660` vérifient que la configuration de Telegram continue lorsque le registre de plugin est vide ; `src/commands/onboard-channels.e2e.test.ts:827` à `src/commands/onboard-channels.e2e.test.ts:872` gardent les canaux de plugin externe configurés visibles ; `src/commands/onboard-channels.e2e.test.ts:919` à `src/commands/onboard-channels.e2e.test.ts:945` traitent les canaux de plugin externe installés comme installés sans invites de réinstallation.

### Tests unitaires

- `src/channels/plugins/contracts/channel-catalog.contract.test.ts:7` à `src/channels/plugins/contracts/channel-catalog.contract.test.ts:50` vérifient les entrées de catalogue pour Teams, WhatsApp, WeCom et Yuanbao ; `src/channels/plugins/contracts/test-helpers/channel-catalog-contract.ts:31` à `src/channels/plugins/contracts/test-helpers/channel-catalog-contract.ts:49` vérifient l'alignement du catalogue expédié et l'énumération.
- `src/channels/plugins/contracts/test-helpers/channel-catalog-contract.ts:52` à `src/channels/plugins/contracts/test-helpers/channel-catalog-contract.ts:101` couvrent les entrées de catalogue groupées de métadonnées uniquement ; `src/channels/plugins/contracts/test-helpers/channel-catalog-contract.ts:104` à `src/channels/plugins/contracts/test-helpers/channel-catalog-contract.ts:260` couvrent les entrées de secours officielles, le remplacement du catalogue externe et les avertissements de dérive de nom de package.
- `src/channels/bundled-channel-catalog-read.test.ts:99` à `src/channels/bundled-channel-catalog-read.test.ts:244` couvrent les lectures de métadonnées groupées, le secours du catalogue officiel, la précédence des métadonnées générées obsolètes et le secours du répertoire groupé vide/manquant ; `src/channels/bundled-channel-catalog-read.fail-soft.test.ts:9` à `src/channels/bundled-channel-catalog-read.fail-soft.test.ts:25` vérifient la découverte en mode dégradé.
- `src/commands/channel-setup/discovery.test.ts:57` à `src/commands/channel-setup/discovery.test.ts:102` vérifient la découverte de manifeste activée automatiquement ; `src/commands/channel-setup/discovery.test.ts:104` à `src/commands/channel-setup/discovery.test.ts:180` couvrent les entrées de configuration masquées et la préservation des métadonnées.
- `src/commands/channel-setup/plugin-install.test.ts:471` à `src/commands/channel-setup/plugin-install.test.ts:651` couvrent les valeurs par défaut d'installation pour dev/beta, le comportement du chemin local groupé, l'installation groupée non-interactive, le remplacement du catalogue externe et les invites de source d'installation ClawHub-first ; `src/commands/channel-setup/plugin-install.test.ts:681` à `src/commands/channel-setup/plugin-install.test.ts:719` couvrent l'installation à source unique confirmée automatiquement.
- `src/commands/channels.list.test.ts:345` à `src/commands/channels.list.test.ts:538` vérifient le comportement texte/JSON par défaut/`--all` pour les canaux de catalogue configurés, disponibles et installables ; `src/commands/channels.list.test.ts:540` à `src/commands/channels.list.test.ts:580` vérifient que les canaux de catalogue installés sur disque restent visibles lorsqu'aucun objet de plugin n'est chargé.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "channel catalog setup onboarding" --json --limit 10`

Résultats :

- A retourné la PR #81736, « feat(catalog): add DingTalk to official external channel catalog », montrant l'expansion continue du catalogue.
- A retourné la PR #86953, « fix(plugins): block untrusted workspace setup-only channel loads », montrant le renforcement actif autour du filtrage du catalogue de confiance et de la configuration du canal de configuration uniquement.
- A retourné indirectement la PR #70012 via des termes adjacents à l'archive dans d'autres recherches et le problème #73496 pour un blocage d'exécution WhatsApp après l'intégration ; aucun large cluster de bugs utilisateur du catalogue uniquement n'a émergé.

Requête : `gitcrawl search openclaw/openclaw --query "docsPath channel catalog setup" --json --limit 10`

Résultats :

- A retourné uniquement la PR #81736, suggérant que les problèmes de configuration docsPath/catalogue ne sont pas un large cluster gitcrawl autonome, bien que discrawl ait trouvé des commentaires d'examen sur les pages de docs manquantes.

Requête : `gitcrawl search openclaw/openclaw --query "install on demand channel setup wizard plugin not available" --json --limit 10`

Résultats :

- N'a retourné aucun résultat, ce qui est neutre après les vérifications de fraîcheur ; il n'a pas surfacé un cluster de problèmes ouvert actuel pour ce libellé d'échec de configuration exact.

Requête : `gitcrawl search openclaw/openclaw --query "channels list installable not installed catalog" --json --limit 10`

Résultats :

- A retourné la PR #86953, avec un extrait indiquant que les appelants de catalogue doivent résoudre les canaux via des assistants de confiance afin que les flux de configuration/ajout ne sélectionnent pas les ombres d'espace de travail non fiables.

Requête : `gitcrawl search openclaw/openclaw --query "setup-only channel loads untrusted workspace" --json --limit 10`

Résultats :

- A retourné la PR #86953, confirmant que le problème de chargement de canal de configuration uniquement d'espace de travail non fiable est un signal de qualité spécifique à la fonctionnalité.

### Requêtes Discrawl

Requête : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "channel catalog setup onboarding"`

Résultats :

- A trouvé un message de mainteneur/contributeur du 2026-05-12 sur la PR #80645 ajoutant le support i18n pour l'assistant de configuration/intégration CLI et les invites de configuration de canal localisées.
- A trouvé une discussion de mainteneur du 2026-04-24 distinguant la découverte de configuration/statut/chargements de catalogue de l'intégration/configuration explicitement sélectionnée, avec des préoccupations concernant les dépendances d'exécution WhatsApp.
- A trouvé des commentaires d'examen sur la PR #70012 concernant la gestion des tentatives d'installation à la demande et un résumé de PR pour l'installation automatique des plugins de fournisseur/canal manquants lors de l'intégration.
- A trouvé une note de refactorisation d'architecture indiquant que les flux de configuration/plan de contrôle doivent devenir d'abord basés sur les métadonnées et que les chemins de configuration/config importent toujours le code de plugin dans les cas qui devraient être des métadonnées uniquement.
- A trouvé des commentaires d'examen sur les PR #67693, #62934 et #50596 concernant les métadonnées de canal/catalogue groupées, le renforcement des invites et les pages de docs manquantes pour les métadonnées `docsPath` annoncées.

Requête : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "setup-only channel loads untrusted workspace"`

Résultats :

- A trouvé une discussion de sécurité du mainteneur sur la PR #86953 expliquant que les plugins de canal d'espace de travail désactivés s'exécutaient toujours lors des chargements de portée de configuration et que la correction devrait échouer fermée.
- A trouvé des commentaires d'examen sur la PR #64154 concernant le fait de ne pas traiter les entrées de catalogue d'espace de travail non fiables comme des cibles d'ajout et de préserver la chargeabilité du plugin de configuration d'espace de travail de portée pour les flux d'ajout.

Requête : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "channel docsPath catalog setup 404"`

Résultats :

- A trouvé un commentaire d'examen de la PR #62934 indiquant que `openclaw.channel.docsPath` pointait vers `/channels/eclaw` sans page de docs correspondante, causant des erreurs 404 des liens « En savoir plus » du catalogue/configuration.
- A trouvé un commentaire d'examen de la PR #50596 avec le même problème de page de docs manquante pour une nouvelle entrée de métadonnées de canal Utopia.

Requête : `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 10 "install on demand channel setup wizard"`

Résultats :

- A trouvé un commentaire d'examen de la PR #70012 indiquant que la gestion des tentatives d'installation à la demande skip/failure pourrait laisser la configuration continuer incorrectement dans la boucle fournisseur/auth ; c'est une preuve adjacente pour le comportement du programme d'installation d'intégration partagée.
