---
title: "Migration du SDK Plugin"
sidebarTitle: "Migration du SDK"
summary: "Migrer depuis l'import deprecated openclaw/plugin-sdk/compat vers des imports de sous-chemins ciblés"
read_when:
  - You see the OPENCLAW_PLUGIN_SDK_COMPAT_DEPRECATED warning
  - You are updating a plugin from the monolithic import to scoped subpaths
  - You maintain an external OpenClaw plugin
---

# Migration du SDK Plugin

L'import `openclaw/plugin-sdk/compat` est déprécié. Tous les plugins doivent utiliser
des **imports de sous-chemins ciblés** (`openclaw/plugin-sdk/\<subpath\>`) à la place.

<Info>
  L'import compat fonctionne toujours à l'exécution. C'est un avertissement de
  dépréciation, pas encore un changement cassant. Mais les nouveaux plugins **ne doivent pas**
  l'utiliser, et les plugins existants doivent migrer avant que la prochaine version majeure le supprime.
</Info>

## Pourquoi cela a changé

L'ancien import monolithique `openclaw/plugin-sdk/compat` réexportait tout depuis un
seul point d'entrée. Cela causait un démarrage lent (importer un helper chargeait des dizaines de
modules non liés), un risque de dépendance circulaire, et une surface API peu claire.

Les sous-chemins ciblés résolvent les trois problèmes : chaque sous-chemin est un petit module
autonome avec un objectif clair.

## Étapes de migration

<Steps>
  <Step title="Trouver les imports dépréciés">
    Recherchez dans votre plugin les imports depuis le chemin compat :

    ```bash
    grep -r "plugin-sdk/compat" my-plugin/
    ```

  </Step>

  <Step title="Remplacer par des sous-chemins ciblés">
    Chaque export correspond à un sous-chemin spécifique. Remplacez la source d'import :

    ```typescript
    // Avant (déprécié)
    import {
      createChannelReplyPipeline,
      createPluginRuntimeStore,
      resolveControlCommandGate,
    } from "openclaw/plugin-sdk/compat";

    // Après (sous-chemins ciblés)
    import { createChannelReplyPipeline } from "openclaw/plugin-sdk/channel-reply-pipeline";
    import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
    import { resolveControlCommandGate } from "openclaw/plugin-sdk/command-auth";
    ```

    Consultez la [référence des sous-chemins](#subpath-reference) ci-dessous pour le mappage complet.

  </Step>

  <Step title="Construire et tester">
    ```bash
    pnpm build
    pnpm test -- my-plugin/
    ```
  </Step>
</Steps>

## Référence des sous-chemins

<Accordion title="Tableau complet des sous-chemins">
  | Sous-chemin | Objectif | Exports clés |
  | --- | --- | --- |
  | `plugin-sdk/core` | Définitions d'entrée de plugin, types de base | `defineChannelPluginEntry`, `definePluginEntry` |
  | `plugin-sdk/channel-setup` | Adaptateurs d'assistant de configuration | `createOptionalChannelSetupSurface` |
  | `plugin-sdk/channel-pairing` | Primitives d'appairage DM | `createChannelPairingController` |
  | `plugin-sdk/channel-reply-pipeline` | Câblage de préfixe de réponse + saisie | `createChannelReplyPipeline` |
  | `plugin-sdk/channel-config-helpers` | Usines d'adaptateurs de configuration | `createHybridChannelConfigAdapter` |
  | `plugin-sdk/channel-config-schema` | Constructeurs de schéma de configuration | Types de schéma de configuration de canal |
  | `plugin-sdk/channel-policy` | Résolution de politique groupe/DM | `resolveChannelGroupRequireMention` |
  | `plugin-sdk/channel-lifecycle` | Suivi du statut du compte | `createAccountStatusSink` |
  | `plugin-sdk/channel-runtime` | Assistants de câblage d'exécution | Utilitaires d'exécution de canal |
  | `plugin-sdk/channel-send-result` | Types de résultat d'envoi | Types de résultat de réponse |
  | `plugin-sdk/runtime-store` | Stockage persistant du plugin | `createPluginRuntimeStore` |
  | `plugin-sdk/allow-from` | Formatage de liste blanche | `formatAllowFromLowercase` |
  | `plugin-sdk/allowlist-resolution` | Mappage d'entrée de liste blanche | `mapAllowlistResolutionInputs` |
  | `plugin-sdk/command-auth` | Contrôle de commande | `resolveControlCommandGate` |
  | `plugin-sdk/secret-input` | Analyse d'entrée secrète | Assistants d'entrée secrète |
  | `plugin-sdk/webhook-ingress` | Assistants de requête webhook | Utilitaires de cible webhook |
  | `plugin-sdk/reply-payload` | Types de réponse de message | Types de charge utile de réponse |
  | `plugin-sdk/provider-onboard` | Correctifs d'intégration de fournisseur | Assistants de configuration d'intégration |
  | `plugin-sdk/keyed-async-queue` | File d'attente asynchrone ordonnée | `KeyedAsyncQueue` |
  | `plugin-sdk/testing` | Utilitaires de test | Assistants et mocks de test |
</Accordion>

Utilisez le sous-chemin le plus étroit qui correspond à la tâche. Si vous ne trouvez pas un export,
consultez la source à `src/plugin-sdk/` ou posez une question sur Discord.

## Calendrier de suppression

| Quand                  | Ce qui se passe                                                 |
| ---------------------- | --------------------------------------------------------------- |
| **Maintenant**         | L'import compat émet un avertissement de dépréciation à l'exécution |
| **Prochaine version majeure** | L'import compat sera supprimé ; les plugins l'utilisant échoueront |

Tous les plugins principaux ont déjà été migrés. Les plugins externes doivent migrer
avant la prochaine version majeure.

## Supprimer temporairement l'avertissement

Définissez cette variable d'environnement pendant que vous travaillez sur la migration :

```bash
OPENCLAW_SUPPRESS_PLUGIN_SDK_COMPAT_WARNING=1 openclaw gateway run
```

C'est une échappatoire temporaire, pas une solution permanente.

## Connexes

- [Building Plugins](/fr/plugins/building-plugins)
- [Plugin Architecture](/fr/plugins/architecture)
- [Plugin Manifest](/fr/plugins/manifest)
