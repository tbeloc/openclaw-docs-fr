---
summary: "Plan de suppression en premier lieu pour déplacer la colle d'entrée de canal répétée dans le noyau."
read_when:
  - Auditing why the channel ingress refactor added too much code
  - Moving route, command, event, activation, or access-group policy from bundled plugins into core
  - Reviewing whether a channel ingress helper actually deletes bundled plugin code
title: "Plan de suppression du noyau d'entrée"
sidebarTitle: "Suppression du noyau d'entrée"
---

# Plan de suppression du noyau d'entrée

La refonte d'entrée n'est pas saine tant qu'elle ajoute des milliers de lignes nettes. La centralisation du noyau ne compte que lorsque le code de production des plugins groupés devient plus petit et que la compatibilité ancienne du SDK tiers est mise en quarantaine dans les shims SDK/noyau.

Forme d'exécution souhaitée :

```text
événement du plugin groupé
  -> extraire les faits de la plateforme localement
  -> résoudre l'entrée partagée une fois que les faits sont disponibles
  -> brancher sur les projections/résultats d'entrée génériques
  -> effectuer les effets secondaires de la plateforme localement

ancien assistant tiers
  -> shim de compatibilité SDK
  -> projection compatible avec l'entrée partagée si possible
  -> ancienne forme de retour préservée
```

Les plugins groupés ne doivent pas traduire l'entrée en formes locales `AccessResult`,
`GroupAccessDecision`, `CommandAuthDecision`, `DmCommandAccess`, ou
`{ allowed, reasonCode }` à moins que ce type ne soit une API de plugin public.

## Budget

Mesuré par rapport à la base de fusion PR avec `origin/main`, y compris les fichiers non suivis.

```text
merge-base            1671e7532adb

current:
core production       +3,922 / -546    = +3,376
docs                  +601 / -17       = +584
other                 +145 / -2        = +143
plugin production     +4,148 / -5,388  = -1,240
tests                 +2,326 / -2,414  = -88
total                 +11,142 / -8,367 = +2,775

required:
plugin production     <= -1,500
core production       <= +1,500, or paid for by larger plugin deletion
tests                 <= +1,000
total                 <= +2,000

stretch:
plugin production     <= -2,500
core production       <= +1,200
total                 <= 0
```

Nettoyage minimum restant :

```text
plugin production     needs 260 more net deleted lines
total                 needs 775 more net deleted lines
core production       still +1,876 over standalone budget, unless paid down by plugin deletion
```

La suppression de commentaires uniquement ne compte pas comme nettoyage. La passe de budget précédente était trop généreuse car elle incluait les commentaires explicatifs QQBot restaurés ; ce document suit uniquement le déplacement du code exécutable/docs/test.

Remesurer après chaque vague de nettoyage :

```sh
base=$(git merge-base HEAD origin/main)
git diff --shortstat "$base"
git diff --numstat "$base" -- src/channels/message-access src/plugin-sdk extensions | sort -nr -k1 | head -n 80
pnpm lint:extensions:no-deprecated-channel-access
```

## Diagnostic

La première passe a ajouté le noyau d'entrée partagé, puis a laissé trop d'autorisation locale au plugin à côté :

```text
faits de la plateforme
  -> état et décision d'entrée partagée
  -> DTO local au plugin ou projection héritée
  -> échelle if/else locale au plugin
```

Cela duplique le modèle. La production du noyau a augmenté d'environ 3 376 lignes, tandis que la production du plugin groupé est 1 240 lignes plus petite. C'est mieux que la première passe, mais ce n'est pas dans le budget minimum. La correction reste la suppression en premier lieu :

- supprimer les DTO de plugin qui ne font que renommer les champs d'entrée
- supprimer les tests qui ne font que vérifier la forme du wrapper
- ajouter des assistants du noyau uniquement lorsque le même patch supprime le code du plugin groupé
- garder la compatibilité ancienne du SDK dans les shims SDK/noyau uniquement
- repacker le noyau après que la suppression du wrapper expose la forme stable

## Points chauds

Fichiers de production groupés positifs qui doivent encore rétrécir :

```text
extensions/telegram/src/ingress.ts                        +126
extensions/discord/src/monitor/dm-command-auth.ts         +101
extensions/signal/src/monitor/access-policy.ts             +92
extensions/feishu/src/policy.ts                            +85
extensions/slack/src/monitor/auth.ts                       +64
extensions/googlechat/src/monitor-access.ts                +59
extensions/nextcloud-talk/src/inbound.ts                   +51
extensions/matrix/src/matrix/monitor/access-state.ts       +49
extensions/irc/src/inbound.ts                              +44
extensions/imessage/src/monitor/inbound-processing.ts      +36
extensions/qa-channel/src/inbound.ts                       +34
extensions/qqbot/src/bridge/sdk-adapter.ts                 +33
extensions/tlon/src/monitor/utils.ts                       +30
extensions/twitch/src/access-control.ts                    +22
extensions/qqbot/src/engine/commands/slash-command-handler.ts +20
extensions/telegram/src/bot-handlers.runtime.ts            +19
```

La branche n'est pas encore dans le budget minimum. Le travail pertinent pour l'examen restant devrait supprimer le flux d'autorisation répété, tourner l'échafaudage, ou les tests de wrapper avant d'ajouter une autre abstraction du noyau.

## Lecture du code actuel

La couture du noyau saine existe déjà dans `src/channels/message-access/runtime.ts` :
elle possède les adaptateurs d'identité, les listes blanches effectives, les lectures du magasin d'appairage, les descripteurs de route, les présets de commande/événement, les groupes d'accès, et la projection `ResolvedChannelMessageIngress` résolue finale.

La croissance restante est principalement de la colle de plugin en couches au-dessus de cette couture :

- `extensions/telegram/src/ingress.ts` enveloppe les décisions du noyau dans des assistants de commande/événement spécifiques à Telegram, puis les sites d'appel passent toujours des listes blanches normalisées et des listes de propriétaires précalculées.
- `extensions/discord/src/monitor/dm-command-auth.ts`,
  `extensions/feishu/src/policy.ts`, `extensions/googlechat/src/monitor-access.ts`,
  et `extensions/matrix/src/matrix/monitor/access-state.ts` gardent toujours des DTO de politique locaux ou des noms de décision hérités à côté de l'entrée.
- `extensions/signal/src/monitor/access-policy.ts` garde correctement la normalisation d'identité Signal et les réponses d'appairage locales, mais a toujours une couture de wrapper qui devrait s'effondrer en consommation d'entrée directe.
- `extensions/nextcloud-talk/src/inbound.ts`, `extensions/irc/src/inbound.ts`,
  `extensions/qa-channel/src/inbound.ts`, `extensions/zalo/src/monitor.ts`, et
  `extensions/zalouser/src/monitor.ts` répètent toujours l'assemblage de route/enveloppe/tour qui peut se déplacer vers des assistants de tour partagés en dehors du noyau d'entrée.

Conclusion : déplacer plus de code dans le noyau n'est utile que s'il supprime ces couches de wrapper de plugin dans le même patch. Ajouter une autre abstraction tout en laissant les retours de wrapper en place répète l'erreur.

## Limite

Le noyau possède la politique générique :

- normalisation et correspondance de la liste blanche
- expansion du groupe d'accès et diagnostics
- lectures de la liste blanche DM du magasin d'appairage
- portes de route, expéditeur, commande, événement et activation
- mappage d'admission : dispatch, drop, skip, observe, pairing
- état, décisions, diagnostics et projections de compatibilité SDK redactés
- descripteurs génériques réutilisables pour l'identité, la route, la commande, l'événement, l'activation et les résultats

Les plugins possèdent les faits de transport et les effets secondaires :

- authenticité du webhook/socket/requête
- extraction d'identité de plateforme et recherches API
- valeurs par défaut de politique spécifiques au canal
- livraison de défi d'appairage, réponses, accusés de réception, réactions, saisie, média, historique, configuration, docteur, statut, journaux et copie orientée utilisateur

Le noyau doit rester agnostique au canal : pas de Discord, Slack, Telegram, Matrix, room, guild, space, client API, ou défaut spécifique au plugin dans `src/channels/message-access`.

## Règle d'acceptation

Chaque nouvel assistant du noyau doit supprimer immédiatement le code de production du plugin groupé.

```text
un appelant groupé        rejeter ; garder local au plugin
deux appelants groupés       accepter uniquement si la production du plugin LOC baisse
trois appelants ou plus     la suppression du plugin doit être au moins 2x le nouveau LOC du noyau
assistant de compatibilité uniquement SDK/core shim ; jamais les chemins chauds groupés
```

Arrêtez et redesignez si :

- le LOC de production du plugin augmente
- les tests croissent plus vite que la production ne rétrécit
- un chemin chaud groupé retourne un DTO qui ne fait que renommer `ResolvedChannelMessageIngress`
- un assistant du noyau a besoin d'un id de canal, d'un objet de plateforme, d'un client API, ou d'une valeur par défaut spécifique au canal

## Packages de travail

1. Geler le budget.
   Mettez LOC dans la PR, gardez le lint d'entrée dépréciée vert, et incluez LOC avant/après dans les commits de nettoyage.

2. Supprimer les coutures DTO minces.
   Remplacez les retours de wrapper locaux au plugin par `ResolvedChannelMessageIngress`,
   `senderAccess`, `commandAccess`, `routeAccess`, ou `ingress` directement. Commencez par QQBot, Telegram, Slack, Discord, Signal, Feishu, Matrix, iMessage, et Tlon. Supprimez les tests de forme de wrapper ; gardez les tests de comportement.

3. Ajouter la classification des résultats uniquement avec les suppressions.
   Un classificateur générique peut exposer `dispatch`, `pairing-required`,
   `skip-activation`, `drop-command`, `drop-route`, `drop-sender`, et
   `drop-ingress`. Il doit dériver du graphe de décision, pas des chaînes de raison, et migrer au moins trois plugins dans le même patch.

4. Ajouter des constructeurs de descripteurs de route uniquement avec les suppressions.
   Les assistants de cible de route et d'expéditeur de route génériques sont acceptables uniquement s'ils rétrécissent immédiatement les plugins lourds en route : Google Chat, IRC, Microsoft Teams, Nextcloud Talk, Mattermost, Slack, Zalo, et Zalo Personal.

5. Ajouter des présets de commande/événement uniquement avec les suppressions.
   Centralisez les formes de commande texte, commande native, callback, et sujet d'origine.
   Les consommateurs de commande doivent par défaut être non autorisés quand aucune porte de commande n'a fonctionné ;
   les événements ne doivent pas démarrer l'appairage.

6. Ajouter des présets d'identité uniquement où ils suppriment le passe-partout.
   Les assistants d'id stable, id stable plus alias, téléphone/e164, et multi-identifiant sont autorisés quand les valeurs brutes n'entrent que dans l'entrée de l'adaptateur et l'état redacté garde les ids/comptes opaques.

7. Partager l'assemblage de tour autorisé.
   En dehors du noyau d'entrée, supprimez l'échafaudage de route/enveloppe/contexte/réponse répété de QA Channel, IRC, Nextcloud Talk, Zalo, et Zalo Personal.
   Le noyau peut posséder le séquençage de route/session/enveloppe/dispatch ; les plugins gardent la livraison et le contexte spécifique au canal.

8. Mettre en quarantaine la compatibilité.
   Les assistants SDK dépréciés restent source-compatibles, mais les chemins chauds groupés ne doivent pas importer les façades d'entrée ou d'authentification de commande dépréciées. Les tests de compatibilité doivent utiliser de faux plugins tiers, pas les internals du plugin groupé.

9. Repacker le noyau.
   Après la suppression du wrapper, réduisez les modules à usage unique, supprimez les exports inutilisés, déplacez la projection de compatibilité hors des chemins chauds, et gardez des tests ciblés pour l'identité, la route, la commande/événement, l'activation, les groupes d'accès, et les shims de compatibilité.

## Vagues de suppression

Exécutez-les dans l'ordre. Chaque vague doit réduire le LOC de production groupé.

1. Effondrement du wrapper, delta de plugin attendu : -400 à -600.
   Remplacez les types de résultats `resolveXAccess`, `resolveXCommandAccess` et
   `accessFromIngress` locaux au plugin par des lectures directes depuis
   `ResolvedChannelMessageIngress`. Premières cibles : authentification des commandes Discord DM,
   politique Feishu, état d'accès Matrix, ingestion Telegram, politique d'accès Signal,
   adaptateur SDK QQBot.

2. Assistants de résultats partagés, delta de plugin attendu : -200 à -350.
   Ajoutez un seul classificateur générique uniquement s'il supprime les
   `shouldBlockControlCommand`, appairage, saut d'activation, blocage de route et blocage d'expéditeur
   répétés sur au moins trois plugins.

3. Générateurs de descripteurs de route, delta de plugin attendu : -200 à -350.
   Déplacez l'assemblage répété des descripteurs de cible de route et d'expéditeur de route dans les
   assistants principaux. Premières cibles : Google Chat, IRC, Microsoft Teams, Nextcloud Talk,
   Mattermost, Slack, Zalo, Zalo Personal.

4. Partage d'assemblage de tour, delta de plugin attendu : -250 à -450.
   Utilisez le séquençage commun route/session/enveloppe/dispatch pour les plugins entrants simples.
   Premières cibles : QA Channel, IRC, Nextcloud Talk, Zalo, Zalo Personal.

5. Repack principal, delta principal attendu : -300 à -700.
   Après que les plugins consomment les projections d'exécution directement, supprimez les modules à usage unique,
   fusionnez les petits fichiers dans `runtime.ts` ou les frères et sœurs ciblés, et gardez les fichiers de compatibilité SDK
   séparés des chemins chauds groupés.

6. Élagage des tests, delta de test attendu : -300 à -600.
   Supprimez les tests qui affirment uniquement les formes de wrapper supprimées. Conservez les tests de comportement pour
   le refus de commande, le repli de groupe, la correspondance origine-sujet, le saut d'activation,
   les groupes d'accès, l'appairage et la rédaction.

Forme d'atterrissage minimale attendue après ces vagues :

```text
production plugin     <= -1 500
production principale environ +1 800 à +2 200 avant repack final
tests                 <= +500
total                 <= +2 000
```

## Ne pas déplacer

Ne déplacez pas les valeurs par défaut de la configuration de plateforme, l'UX de configuration, la copie doctor/fix, les recherches API,
les vérifications de présence du propriétaire Slack, la gestion des alias/vérification Matrix, l'analyse des rappels Telegram,
l'analyse de la syntaxe des commandes, l'enregistrement des commandes natives, l'analyse des charges utiles de réaction,
les réponses d'appairage, les réponses de commande, les accusés de réception, la saisie, les médias, l'historique,
ou les journaux.

## Vérification

Boucle locale ciblée :

```sh
pnpm lint:extensions:no-deprecated-channel-access
pnpm test src/channels/message-access/message-access.test.ts src/plugin-sdk/channel-ingress-runtime.test.ts src/plugin-sdk/access-groups.test.ts
pnpm test extensions/<changed-plugin>/src/...
pnpm plugin-sdk:api:check
pnpm config:docs:check
pnpm check:docs
git diff --check
```

Utilisez Testbox pour les portes larges modifiées/preuve de suite complète une fois que la tendance LOC est
dans le budget.

Chaque package de travail enregistre :

- LOC avant/après par catégorie
- wrappers de plugin supprimés
- LOC d'assistant principal nouveau, le cas échéant
- tests ciblés exécutés
- liste des points chauds restants

## Critères de sortie

- les importations de production groupées n'utilisent pas les façades channel-access ou command-auth dépréciées
- le code de compatibilité est isolé aux coutures SDK/core
- les plugins groupés consomment les projections d'ingestion ou les résultats génériques directement
- le LOC de production du plugin est au moins 1 500 net négatif par rapport à `origin/main`
- le LOC de production principal est `<= +1 500`, ou tout excédent est payé pendant que le total
  reste `<= +2 000`
- les tests représentatifs couvrent la rédaction, la route, la commande/événement, l'activation,
  le groupe d'accès et le comportement de repli spécifique au canal
