---
title: Plugins - Plugin Approvals Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Plugin Approvals Maturity Note

## Résumé

Cette catégorie reste `Stable` en termes de couverture et de qualité. OpenClaw dispose désormais d'un modèle de limite d'approbation partagée plus clair que celui capturé dans la note précédente : les approbations de plugins, les approbations d'exécution, les relais de permissions natifs de Codex, l'autorisation de secours dans le même chat, la livraison native de canal et les exports d'aides de sécurité sont tous documentés et implémentés via des coutures SDK/runtime partagées au lieu de solutions ponctuelles par canal. La principale faiblesse restante est la largeur de la preuve plutôt que la conception des limites : les preuves du référentiel actuel sont solides pour le comportement de la passerelle/runtime et de l'adaptateur, mais la validation multi-canal en direct est toujours plus mince que la documentation et les commandes de validation détenues par la taxonomie sont localement bloquées par des défaillances d'authentification du registre avant de pouvoir valider la surface packagée.

## Portée de la catégorie

Cette catégorie couvre les limites d'approbation et de sécurité dans la surface Plugins :

- Les demandes d'approbation détenues par les plugins via `plugin.approval.*`, y compris la génération d'ID, l'application des décisions autorisées, les métadonnées de routage et la résolution.
- La séparation entre les approbations de plugins, les approbations d'exécution, les relais de permissions natifs de Codex, les élicitations d'approbation MCP et l'exposition optionnelle d'outils.
- Les coutures `approvalCapability`/`nativeRuntime` qui permettent aux plugins de canal bundlés d'exprimer l'authentification d'approbation, la disponibilité, la livraison native, la suppression de secours et le comportement exec-vs-plugin sans forks de noyau spécifiques au canal.
- Les protections d'exécution autour de la relecture d'approbation, de la portée des décisions, de la liaison appareil/nœud et de la suppression de cible transférée.
- Les aides publiques de sécurité/runtime exposées aux plugins et aux extensions bundlées, y compris les wrappers sûrs pour le système de fichiers, les gardes SSRF, les gardes de chemin, la rédaction, l'expansion des groupes d'accès, le stockage de fichiers privés et la comparaison de secrets sûre en termes de temps.

Hors de portée : l'authentification générique de la passerelle, le comportement de canal non-approbation, l'authentification spécifique au fournisseur et la compatibilité de distribution/version en dehors de la surface de limite d'approbation/sécurité.

## Fonctionnalités

- Demandes d'approbation : Les actions initiées par les plugins peuvent demander et résoudre les approbations via le flux standard.
- Livraison d'approbation native : Les actions de plugin privilégiées peuvent router les approbations via des invites et des réponses natives du canal.
- Secours dans le même chat : La livraison d'approbation peut revenir à des avis d'autorisation dans le même chat lorsque le routage natif n'est pas disponible.
- Séparation exec et plugin : Les approbations exec restent distinctes des chemins d'approbation de plugin et des relais de permissions natifs.
- Protection contre la relecture d'approbation : Les décisions d'approbation restent limitées à la demande d'origine, à la cible et à la liaison appareil ou nœud.
- Aides de sécurité : Les exports d'aides de sécurité fournissent des primitives approuvées sans élargir les limites de confiance.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` réussi ; `last_sync_at` `2026-05-28T19:09:52.784704Z` ; `thread_count` `29810` ; `open_thread_count` `11181` ; `db_path` `/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db` ; `version` `0.2.1`.
- discrawl : `discrawl status --json` réussi ; réexécution en direct `generated_at` `2026-05-30T00:38:20Z` ; `state` `current` ; `summary` `1487536 messages across 25831 channels` ; `last_sync_at` `2026-05-29T19:27:40Z`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : Les preuves d'exécution réelles couvrent le chemin d'approbation principal de bout en bout : approbations d'exécution hébergées par la passerelle sur des connexions séparées, scoping de token d'exécution d'approbation d'opérateur, liaison anti-contournement et relecture d'invocation de nœud, fixtures de liaison d'exécution système, planification de livraison native partagée et comportement d'adaptateur natif du canal sur Slack, Discord, Matrix, Telegram, WhatsApp, Signal et iMessage.
- Signaux négatifs : Les preuves inter-canaux sont toujours inégales. La preuve la plus solide est la passerelle/runtime plus les tests au niveau de l'adaptateur, tandis que les preuves en direct ou de smoke de version vérifiées pour les approbations natives de plugin et d'exécution sur plusieurs fournisseurs de chat réels restent rares.
- Lacunes d'intégration : Ajouter une couverture de smoke de version ou CI récurrente et exécutable pour la livraison et la résolution d'approbation native sur au moins Slack, Matrix, Telegram, Discord et un client piloté par réaction, y compris les approbations de plugin, les approbations d'exécution, le routage DM d'approbateur, les avis de secours dans le même chat, l'expiration et les tentatives d'approbateur mal limitées.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux d'exécution réel sur
la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par
eux-mêmes.

## Score de qualité

- Score : `Stable (86%)`
- Rapports Gitcrawl : Les requêtes d'archive actuelles font surface au travail UX d'approbation actif et de durcissement plutôt qu'à une rupture de limite concrète : travail ouvert sur resume-behind-plugin-approval (`#82906`), approbations de plugin en langage clair (`#81864`), routage d'enveloppe de consentement MCP (`#78303`), contexte d'approbation de plugin de forme longue (`#81901`) et formatage d'invite d'approbation iMessage (`#85954`). Ceux-ci indiquent une pression de polissage et d'expansion en cours, pas une preuve que le modèle de limite d'approbation/sécurité partagée échoue.
- Rapports Discrawl : Les hits d'archive Discord actuels incluent des preuves de version/responsable que le durcissement de la limite d'approbation a été expédié récemment (durcissement des approbations de rôle d'appareil non-administrateur, correction du correctif d'invite d'approbation native iMessage en double) plus des questions d'opérateur sur l'application de couches d'approbation non-LLM. Cela soutient l'utilisation réelle de l'opérateur, mais cela montre également que le modèle mental d'approbation a toujours besoin d'une communication claire.
- Bonnes qualités : La surface a une séparation de porte nette dans les docs, des ID d'approbation de plugin générés par le serveur, la validation des décisions par rapport aux décisions autorisées de la demande, des coutures d'authentification d'approbation partagées, des aides de livraison/runtime natifs partagés et un ensemble large d'exports d'aides de sécurité que les plugins bundlés consomment déjà pour le travail fs-safe, SSRF, secret et path-boundary.
- Mauvaises qualités : Le modèle mental est toujours distribué sur plusieurs docs et pages de canal ; la durabilité de `allow-always` du plugin est intentionnellement déléguée à l'appelant/runtime du plugin ; et le barrel `security-runtime` large déprécié reste public, ce qui maintient la commodité héritée mais augmente le risque de dérive et de sur-importation.
- Exclu de la qualité : La profondeur de la couverture des tests est exclue par la politique, et les commandes de validation de taxonomie bloquées sont traitées comme un problème d'environnement local plutôt que comme une preuve de qualité du produit.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou d'exécution réel
comme entrée de notation.

## Lacunes connues

- La preuve la plus solide est toujours la passerelle/runtime plus la couverture d'adaptateur/unité ; il n'y a pas encore assez de validation croisée en direct récurrente pour traiter la livraison d'approbation native comme largement prouvée sur chaque fournisseur documenté.
- Les auteurs de plugins doivent toujours comprendre et implémenter ce que `allow-always` signifie pour leur propre runtime ; le flux d'approbation de plugin partagé n'établit intentionnellement pas la confiance automatiquement.
- L'histoire d'approbation/sécurité s'étend sur plusieurs docs (`plugin-permission-requests`, `exec-approvals`, `sdk-channel-plugins` et pages spécifiques au canal), donc la dérive de l'opérateur et de l'auteur de plugin est toujours plausible.
- Les commandes de validation détenues par la taxonomie n'ont pas pu s'exécuter localement car l'installation des dépendances a échoué avant la validation avec des erreurs d'authentification du registre 403 pour `@microsoft/teams.cards` / `@microsoft/teams.api` et `No authorization header was set for the request`.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-permission-requests.md:11` définit les demandes de permission de plugin comme le flux `plugin.approval.*` ; les lignes 16-30 les séparent des approbations exec, des outils optionnels, de l'examen des permissions natif de Codex et des élicitations MCP ; les lignes 90-109 documentent la sémantique des décisions et la nature détenue par le plugin de la persistance `allow-always` ; les lignes 118-165 documentent le routage `approvals.plugin` et les relais de permission natifs de Codex.
- `/Users/kevinlin/code/openclaw/docs/tools/exec-approvals.md:11` définit les approbations exec comme des garde-fous d'hôte superposés à la politique d'outils ; les lignes 18-23 décrivent la fusion de politique effective plus stricte ; les lignes 42-45 documentent les affordances natives du client ; les lignes 57-63 documentent la liaison canonique cwd/argv/env/file et le comportement de refus en cas de dérive.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-channel-plugins.md:142` rend `approvalCapability` la couture d'approbation canonique ; les lignes 146-168 attribuent l'authentification du même chat, la livraison native, la suppression de route, la normalisation de cible, les avis de reroutage et la préservation du type exec-vs-plugin aux assistants SDK partagés plutôt qu'à la logique ad hoc par canal.
- `/Users/kevinlin/code/openclaw/docs/channels/slack.md:1340` documente la livraison d'approbation exec et plugin native de Slack, les approbateurs de plugin séparés par rapport aux approbateurs exec, et la suppression native du fallback partagé uniquement lorsque Slack peut gérer l'approbation nativement.
- `/Users/kevinlin/code/openclaw/docs/channels/matrix.md:680`, `/Users/kevinlin/code/openclaw/docs/channels/imessage.md:576` et `/Users/kevinlin/code/openclaw/docs/channels/telegram.md:915` documentent la sémantique d'approbation native du canal, les exigences explicites d'approbateur, les mises en garde de salle de confiance et le comportement de routage spécifique au type d'approbation sur plusieurs canaux groupés.

## Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/plugin-approval.ts:28` implémente les gestionnaires de passerelle `plugin.approval.*` ; les lignes 110-117 génèrent les IDs `plugin:` côté serveur et lient les métadonnées du demandeur ; les lignes 197-205 appliquent les décisions autorisées spécifiques à la demande lors de la résolution.
- `/Users/kevinlin/code/openclaw/src/infra/channel-approval-auth.ts:12` rend `approvalCapability.authorizeActorAction` et `getActionAvailabilityState` le chemin d'autorisation d'approbation canonique, tout en préservant le fallback implicite du même chat séparé de l'autorisation explicite d'approbateur.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/approval-native-helpers.ts:123` centralise la correspondance de cible sur `{ to, accountId, threadId }` ; les lignes 144-218 contrôlent la suppression de prompt exec native locale sur le type d'approbation, la route native active, le mode de configuration et les filtres de demande ; les lignes 244-280 construisent le suppresseur de fallback de forwarding partagé qui préserve `approvalKind` et la portée du compte.
- `/Users/keviewlin/code/openclaw/src/infra/approval-native-runtime.ts:37` livre les demandes d'approbation via une route native planifiée avec déduplication et gestion d'erreur par cible ; les lignes 173-260 enfilent `approvalKind`, le rapport de route, le contenu en attente et le cycle de vie de la passerelle via le runtime natif partagé.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/security-runtime.ts:1` garde le baril de sécurité large déprécié public tout en exportant toujours les wrappers sûrs pour fs, les gardes SSRF, les gardes de chemin, les assistants de fichiers privés, les écritures de temp frère, la rédaction, l'expansion du groupe d'accès et `safeEqualSecret`.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/agents/bash-tools.exec-gateway-approval.e2e.test.ts:51` exerce les approbations exec hébergées par la passerelle sur des connexions opérateur/demandeur séparées et attend l'approbation avant la fin de la commande.
- `/Users/kevinlin/code/openclaw/src/gateway/operator-approvals-client.e2e.test.ts:50` prouve que l'autorité du runtime d'approbation opérateur ne fonctionne que pour les URL de passerelle locale générées et non pour une configuration de loopback distant.
- `/Users/kevinlin/code/openclaw/src/gateway/server.node-invoke-approval-bypass.test.ts:432` rejette les drapeaux d'approbation mal formés avant le forwarding ; les lignes 503-572 lient les approbations à la décision/appareil et bloquent la relecture entre appareils ; les lignes 581-673 relient les approbations de chat uniquement pour la même source de tour ; les lignes 681-727 bloquent la relecture entre nœuds.
- `/Users/kevinlin/code/openclaw/src/gateway/system-run-approval-binding.contract.test.ts:72` évalue les cas de fixture vérifiés pour l'accord de liaison argv/cwd/agent/session/env et le rejet de non-concordance.
- `/Users/kevinlin/code/openclaw/src/infra/approval-native-runtime.test.ts:35` couvre la déduplication de livraison native et la gestion des défaillances par cible ; les lignes 123-226 vérifient que le type d'approbation de plugin, le contenu en attente, la résolution de cible DM et les mises à jour résolues circulent tous via le runtime natif partagé.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugin-sdk/approval-native-helpers.test.ts:18` couvre la résolution d'origine-cible partagée et la correspondance de cible ; les lignes 277-359 couvrent les règles de suppression de fallback ; les lignes 362-420 couvrent les portes de suppression de prompt exec natif local.
- `/Users/kevinlin/code/openclaw/src/infra/channel-approval-auth.test.ts:18` couvre l'autorisation par défaut, les remplacements d'approbation de canal explicites et la distinction entre l'authentification d'approbateur explicite et le fallback implicite du même chat.
- `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-subpaths.test.ts:573` garde le sous-chemin d'assistant d'exécution d'authentification d'approbation exporté avec l'ensemble d'assistants attendu.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/approval-native.test.ts:34`, `/Users/kevinlin/code/openclaw/extensions/slack/src/approval-native.test.ts:924` et `/Users/kevinlin/code/openclaw/extensions/matrix/src/approval-native.test.ts:180` couvrent la disponibilité d'approbation native, les conseils de configuration et l'invariant selon lequel l'authentification d'approbation de plugin reste indépendante des approbateurs exec.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/approval-native.test.ts:82`, `/Users/kevinlin/code/openclaw/extensions/signal/src/approval-native.test.ts:107`, `/Users/kevinlin/code/openclaw/extensions/imessage/src/approval-native.test.ts:107` et `/Users/kevinlin/code/openclaw/extensions/telegram/src/approval-native.test.ts:34` couvrent les approbations natives pilotées par réaction/bouton, la gestion d'origine-cible et le comportement de routage plugin-vs-exec sur les canaux groupés lourds en réactions.

## Commandes de validation de surface

- `pnpm plugin-sdk:check-exports` : `bloqué` - tenté depuis `/Users/kevinlin/code/openclaw`, mais l'installation des dépendances a échoué avant une validation significative avec des erreurs d'authentification de registre 403 pour `@microsoft/teams.cards` / `@microsoft/teams.api` et `No authorization header was set for the request` ; s'il avait fonctionné, il aurait vérifié que les exports SDK publics générés pour les sous-chemins d'approbation/sécurité correspondent toujours à l'inventaire de point d'entrée vérifié.
- `pnpm plugin-sdk:api:check` : `bloqué` - même bloqueur d'authentification de registre local ; cela validerait la dérive d'API publique empaquetée dans les exports d'approbation/runtime/sécurité.
- `pnpm plugin-sdk:surface:check` : `bloqué` - même bloqueur d'authentification de registre local ; cela validerait les budgets de taille de surface et d'export déprécié, ce qui est directement pertinent pour le baril `security-runtime` large toujours public.
- `pnpm plugins:boundary-report:ci` : `bloqué` - même bloqueur d'authentification de registre local ; cela validerait les limites d'import réservé et de compatibilité sur les coutures SDK de plugin/plugin groupé.
- `pnpm release:plugins:npm:check` : `bloqué` - même bloqueur d'authentification de registre local ; cela validerait les métadonnées npm publiables et la préparation à la publication pour la surface de plugin qui porte ces limites d'approbation/sécurité.
- `pnpm release:plugins:clawhub:check` : `bloqué` - même bloqueur d'authentification de registre local ; cela validerait les métadonnées ClawHub publiables et la préparation à la publication pour les chemins de distribution de plugin groupé qui dépendent de la même surface SDK empaquetée.

## Requêtes Gitcrawl

Requête :

```bash
gitcrawl search openclaw/openclaw --query "plugin approval native security" --json
```

Résultats :

- La recherche par mot-clé a retourné le travail de limite d'approbation plutôt qu'un incident de défaillance de limite directe.
- Le problème ouvert `#81901` (« Allow plugin approvals to carry long-form context (Telegram, Slack, Discord) ») montre la pression UX actuelle sur les limites de charge utile d'approbation de plugin.
- La PR ouverte `#81864` (« feat(approvals): add plain-language plugin approvals ») et la PR ouverte `#78303` (« feat(mcp): channel-mediated approval for MCP tool calls (consent envelope) ») montrent l'investissement continu dans le rendu et le routage d'approbation.
- La PR ouverte `#86079` (« fix(codex): verify plugin elicitation source ») et la PR ouverte `#87141` (« fix(plugin): harden schema and metadata fuzz boundaries ») sont des preuves de durcissement adjacent plutôt que la preuve d'un modèle d'approbation partagé cassé.

Requête :

```bash
gitcrawl search openclaw/openclaw --query "plugin approval allow-always" --json
```

Résultats :

- La recherche par mot-clé a retourné le travail de raffinement UX d'approbation active autour de `allow-always`, du texte de fallback et du rendu.
- La PR ouverte `#82906` (« fix(codex): gate CLI session resume behind plugin approval ») montre les limites d'approbation étendues à des flux supplémentaires de haute confiance.
- La PR ouverte `#80141` (« fix(approvals): summarize long approval prompts ») et la PR ouverte `#78793` (« fix(approvals): interpolate request id into \"Reply with:\" line ») montrent le travail de polissage concret sur la messagerie d'approbation.
- Le problème ouvert `#85954` (formatage d'approbation iMessage) et le problème ouvert `#78308` (suivi d'enveloppe de consentement) indiquent les lacunes de polissage de produit restantes, pas un effondrement de la limite d'approbation/sécurité elle-même.

## Requêtes Discrawl

Requête :

```bash
discrawl --json search "plugin approval" --limit 5
```

Résultats :

- Les meilleurs résultats étaient des messages de publication/annonce plutôt que des fils de confusion d'utilisateur.
- Les publications `releases` et `general` pour `OpenClaw 2026.5.27` appellent explicitement le durcissement de limite d'approbation (« approbations de rôle d'appareil non-administrateur ») et demandent aux utilisateurs de tester les régressions de canal/runtime.
- Traité comme une preuve opérationnelle légèrement positive que les modifications d'approbation/sécurité sont expédiées et exercées, mais pas comme une preuve de profondeur de validation multi-canal large.

Requête :

```bash
discrawl --json search "native approval" --limit 5
```

Résultats :

- Un message de mainteneur dans `maintainers` référence le portage d'un correctif pour les invites d'approbation exec native iMessage en double et les assistants d'approbation basés sur réaction partagée.
- Un message d'utilisateur dans `general` demande si OpenClaw a une couche d'approbation native non-LLM, ce qui est une preuve de la demande d'opérateur pour cette limite et pour une messagerie plus claire autour de celle-ci.
- Les messages récents `clawtributors`/`releases` décrivent la stabilité du relais de crochet natif et les améliorations de limite d'approbation, ce qui est un contexte opérationnel utile mais toujours pas un substitut à la validation multi-canal exécutable.
