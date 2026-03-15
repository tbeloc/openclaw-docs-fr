---
summary: "Refactoriser les clusters avec le plus grand potentiel de réduction LOC"
read_when:
  - You want to reduce total LOC without changing behavior
  - You are choosing the next dedupe or extraction pass
title: "Refactor Cluster Backlog"
---

# Refactor Cluster Backlog

Classé par réduction probable de LOC, sécurité et portée.

## 1. Configuration du plugin de canal et échafaudage de sécurité

Cluster de plus haute valeur.

Formes répétées dans de nombreux plugins de canal :

- `config.listAccountIds`
- `config.resolveAccount`
- `config.defaultAccountId`
- `config.setAccountEnabled`
- `config.deleteAccount`
- `config.describeAccount`
- `security.resolveDmPolicy`

Exemples solides :

- `extensions/telegram/src/channel.ts`
- `extensions/googlechat/src/channel.ts`
- `extensions/slack/src/channel.ts`
- `extensions/discord/src/channel.ts`
- `extensions/matrix/src/channel.ts`
- `extensions/irc/src/channel.ts`
- `extensions/signal/src/channel.ts`
- `extensions/mattermost/src/channel.ts`

Forme d'extraction probable :

- `buildChannelConfigAdapter(...)`
- `buildMultiAccountConfigAdapter(...)`
- `buildDmSecurityAdapter(...)`

Économies attendues :

- ~250-450 LOC

Risque :

- Moyen. Chaque canal a des variantes légèrement différentes pour `isConfigured`, les avertissements et la normalisation.

## 2. Boilerplate singleton de runtime d'extension

Très sûr.

Presque chaque extension a le même détenteur de runtime :

- `let runtime: PluginRuntime | null = null`
- `setXRuntime`
- `getXRuntime`

Exemples solides :

- `extensions/telegram/src/runtime.ts`
- `extensions/matrix/src/runtime.ts`
- `extensions/slack/src/runtime.ts`
- `extensions/discord/src/runtime.ts`
- `extensions/whatsapp/src/runtime.ts`
- `extensions/imessage/src/runtime.ts`
- `extensions/twitch/src/runtime.ts`

Variantes de cas particuliers :

- `extensions/bluebubbles/src/runtime.ts`
- `extensions/line/src/runtime.ts`
- `extensions/synology-chat/src/runtime.ts`

Forme d'extraction probable :

- `createPluginRuntimeStore<T>(errorMessage)`

Économies attendues :

- ~180-260 LOC

Risque :

- Faible

## 3. Étapes d'invite d'intégration et de correctif de configuration

Grande surface.

De nombreux fichiers d'intégration répètent :

- résoudre l'ID de compte
- entrées de liste d'autorisation d'invite
- fusionner allowFrom
- définir la politique DM
- inviter les secrets
- corriger la configuration au niveau supérieur par rapport à celle limitée au compte

Exemples solides :

- `extensions/bluebubbles/src/onboarding.ts`
- `extensions/googlechat/src/onboarding.ts`
- `extensions/msteams/src/onboarding.ts`
- `extensions/zalo/src/onboarding.ts`
- `extensions/zalouser/src/onboarding.ts`
- `extensions/nextcloud-talk/src/onboarding.ts`
- `extensions/matrix/src/onboarding.ts`
- `extensions/irc/src/onboarding.ts`

Couture d'aide existante :

- `src/channels/plugins/onboarding/helpers.ts`

Forme d'extraction probable :

- `promptAllowFromList(...)`
- `buildDmPolicyAdapter(...)`
- `applyScopedAccountPatch(...)`
- `promptSecretFields(...)`

Économies attendues :

- ~300-600 LOC

Risque :

- Moyen. Facile de sur-généraliser ; gardez les aides étroites et composables.

## 4. Fragments de schéma de configuration multi-compte

Fragments de schéma répétés dans les extensions.

Modèles courants :

- `const allowFromEntry = z.union([z.string(), z.number()])`
- schéma de compte plus :
  - `accounts: z.object({}).catchall(accountSchema).optional()`
  - `defaultAccount: z.string().optional()`
- champs DM/groupe répétés
- champs de politique markdown/outil répétés

Exemples solides :

- `extensions/bluebubbles/src/config-schema.ts`
- `extensions/zalo/src/config-schema.ts`
- `extensions/zalouser/src/config-schema.ts`
- `extensions/matrix/src/config-schema.ts`
- `extensions/nostr/src/config-schema.ts`

Forme d'extraction probable :

- `AllowFromEntrySchema`
- `buildMultiAccountChannelSchema(accountSchema)`
- `buildCommonDmGroupFields(...)`

Économies attendues :

- ~120-220 LOC

Risque :

- Faible à moyen. Certains schémas sont simples, d'autres sont spéciaux.

## 5. Cycle de vie du webhook et du moniteur au démarrage

Bon cluster de valeur moyenne.

Modèles répétés de `startAccount` / configuration du moniteur :

- résoudre le compte
- calculer le chemin du webhook
- enregistrer le démarrage
- démarrer le moniteur
- attendre l'abandon
- nettoyage
- mises à jour du puits d'état

Exemples solides :

- `extensions/googlechat/src/channel.ts`
- `extensions/bluebubbles/src/channel.ts`
- `extensions/zalo/src/channel.ts`
- `extensions/telegram/src/channel.ts`
- `extensions/nextcloud-talk/src/channel.ts`

Couture d'aide existante :

- `src/plugin-sdk/channel-lifecycle.ts`

Forme d'extraction probable :

- aide pour le cycle de vie du moniteur de compte
- aide pour le démarrage du compte soutenu par webhook

Économies attendues :

- ~150-300 LOC

Risque :

- Moyen à élevé. Les détails de transport divergent rapidement.

## 6. Nettoyage des petits clones exacts

Compartiment de nettoyage à faible risque.

Exemples :

- détection de gateway argv dupliquée :
  - `src/infra/gateway-lock.ts`
  - `src/cli/daemon-cli/lifecycle.ts`
- rendu des diagnostics de port dupliqué :
  - `src/cli/daemon-cli/restart-health.ts`
- construction de clé de session dupliquée :
  - `src/web/auto-reply/monitor/broadcast.ts`

Économies attendues :

- ~30-60 LOC

Risque :

- Faible

## Clusters de test

### Fixtures d'événement webhook LINE

Exemples solides :

- `src/line/bot-handlers.test.ts`

Extraction probable :

- `makeLineEvent(...)`
- `runLineEvent(...)`
- `makeLineAccount(...)`

Économies attendues :

- ~120-180 LOC

### Matrice d'authentification des commandes natives Telegram

Exemples solides :

- `src/telegram/bot-native-commands.group-auth.test.ts`
- `src/telegram/bot-native-commands.plugin-auth.test.ts`

Extraction probable :

- constructeur de contexte de forum
- aide d'assertion de message refusé
- cas d'authentification pilotés par tableau

Économies attendues :

- ~80-140 LOC

### Configuration du cycle de vie Zalo

Exemples solides :

- `extensions/zalo/src/monitor.lifecycle.test.ts`

Extraction probable :

- harnais de configuration de moniteur partagé

Économies attendues :

- ~50-90 LOC

### Tests d'option non supportée du contexte llm Brave

Exemples solides :

- `src/agents/tools/web-tools.enabled-defaults.test.ts`

Extraction probable :

- matrice `it.each(...)`

Économies attendues :

- ~30-50 LOC

## Ordre suggéré

1. Boilerplate singleton de runtime
2. Nettoyage des petits clones exacts
3. Extraction du générateur de configuration et de sécurité
4. Extraction d'aide de test
5. Extraction d'étape d'intégration
6. Extraction d'aide du cycle de vie du moniteur
