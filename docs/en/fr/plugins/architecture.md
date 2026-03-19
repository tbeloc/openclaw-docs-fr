---
summary: "Internes de l'architecture des plugins : modèle de capacité, propriété, contrats, pipeline de chargement, assistants d'exécution"
read_when:
  - Construire ou déboguer des plugins OpenClaw natifs
  - Comprendre le modèle de capacité des plugins ou les limites de propriété
  - Travailler sur le pipeline de chargement des plugins ou le registre
  - Implémenter des hooks d'exécution de fournisseur ou des plugins de canal
title: "Architecture des plugins"
---

# Architecture des plugins

Cette page couvre l'architecture interne du système de plugins OpenClaw. Pour
la configuration, la découverte et la configuration orientées utilisateur, voir [Plugins](/fr/tools/plugin).

## Modèle de capacité public

Les capacités sont le modèle **plugin natif** public à l'intérieur d'OpenClaw. Chaque
plugin OpenClaw natif s'enregistre auprès d'un ou plusieurs types de capacité :

| Capacité            | Méthode d'enregistrement                       | Exemples de plugins       |
| ------------------- | --------------------------------------------- | ------------------------- |
| Inférence de texte  | `api.registerProvider(...)`                   | `openai`, `anthropic`     |
| Parole              | `api.registerSpeechProvider(...)`             | `elevenlabs`, `microsoft` |
| Compréhension média | `api.registerMediaUnderstandingProvider(...)` | `openai`, `google`        |
| Génération d'image  | `api.registerImageGenerationProvider(...)`    | `openai`, `google`        |
| Recherche web       | `api.registerWebSearchProvider(...)`          | `google`                  |
| Canal / messagerie  | `api.registerChannel(...)`                    | `msteams`, `matrix`       |

Un plugin qui enregistre zéro capacité mais fournit des hooks, des outils ou
des services est un **plugin legacy hook-only**. Ce modèle est toujours entièrement supporté.

### Position de compatibilité externe

Le modèle de capacité est implémenté dans le noyau et utilisé par les plugins
groupés/natifs aujourd'hui, mais la compatibilité des plugins externes nécessite
toujours une barre plus stricte que « c'est exporté, donc c'est figé ».

Recommandations actuelles :

- **plugins externes existants :** maintenir le fonctionnement des intégrations basées sur les hooks ; traiter
  ceci comme la ligne de base de compatibilité
- **nouveaux plugins groupés/natifs :** préférer l'enregistrement explicite des capacités aux
  accès spécifiques aux fournisseurs ou aux nouveaux designs hook-only
- **plugins externes adoptant l'enregistrement des capacités :** autorisé, mais traiter les
  surfaces d'assistance spécifiques aux capacités comme évolutives sauf si la documentation marque explicitement un
  contrat comme stable

Règle pratique :

- les API d'enregistrement des capacités sont la direction prévue
- les hooks legacy restent le chemin le plus sûr sans rupture pour les plugins externes pendant
  la transition
- les sous-chemins d'assistance exportés ne sont pas tous égaux ; préférer le contrat documenté étroit, pas les exports d'assistance accidentels

### Formes de plugins

OpenClaw classe chaque plugin chargé dans une forme basée sur son comportement
d'enregistrement réel (pas seulement les métadonnées statiques) :

- **plain-capability** -- enregistre exactement un type de capacité (par exemple un
  plugin provider-only comme `mistral`)
- **hybrid-capability** -- enregistre plusieurs types de capacité (par exemple
  `openai` possède l'inférence de texte, la parole, la compréhension média et la
  génération d'image)
- **hook-only** -- enregistre uniquement des hooks (typés ou personnalisés), pas de capacités,
  outils, commandes ou services
- **non-capability** -- enregistre des outils, commandes, services ou routes mais pas de
  capacités

Utilisez `openclaw plugins inspect <id>` pour voir la forme et la répartition des capacités d'un plugin. Voir [Référence CLI](/fr/cli/plugins#inspect) pour les détails.

### Hooks legacy

Le hook `before_agent_start` reste supporté comme chemin de compatibilité pour
les plugins hook-only. Les plugins legacy du monde réel en dépendent toujours.

Direction :

- le maintenir fonctionnel
- le documenter comme legacy
- préférer `before_model_resolve` pour le travail de remplacement de modèle/fournisseur
- préférer `before_prompt_build` pour le travail de mutation de prompt
- supprimer uniquement après que l'utilisation réelle baisse et que la couverture des fixtures prouve la sécurité de la migration

### Signaux de compatibilité

Lorsque vous exécutez `openclaw doctor` ou `openclaw plugins inspect <id>`, vous pouvez voir
l'une de ces étiquettes :

| Signal                     | Signification                                                      |
| -------------------------- | ------------------------------------------------------------ |
| **config valid**           | La config s'analyse correctement et les plugins se résolvent                       |
| **compatibility advisory** | Le plugin utilise un modèle supporté mais plus ancien (par ex. `hook-only`) |
| **legacy warning**         | Le plugin utilise `before_agent_start`, qui est déprécié        |
| **hard error**             | La config est invalide ou le plugin n'a pas pu se charger                   |

Ni `hook-only` ni `before_agent_start` ne casseront votre plugin aujourd'hui --
`hook-only` est consultatif, et `before_agent_start` déclenche uniquement un avertissement. Ces
signaux apparaissent également dans `openclaw status --all` et `openclaw plugins doctor`.

## Aperçu de l'architecture

Le système de plugins OpenClaw a quatre couches :

1. **Manifeste + découverte**
   OpenClaw trouve les plugins candidats à partir des chemins configurés, des racines d'espace de travail,
   des racines d'extensions globales et des extensions groupées. La découverte lit d'abord les manifestes
   `openclaw.plugin.json` natifs plus les manifestes de bundle supportés.
2. **Activation + validation**
   Le noyau décide si un plugin découvert est activé, désactivé, bloqué ou
   sélectionné pour un emplacement exclusif comme la mémoire.
3. **Chargement d'exécution**
   Les plugins OpenClaw natifs sont chargés en processus via jiti et enregistrent
   les capacités dans un registre central. Les bundles compatibles sont normalisés en
   enregistrements de registre sans importer le code d'exécution.
4. **Consommation de surface**
   Le reste d'OpenClaw lit le registre pour exposer les outils, canaux, configuration de fournisseur,
   hooks, routes HTTP, commandes CLI et services.

La limite de conception importante :

- la découverte + la validation de config doivent fonctionner à partir des **métadonnées de manifeste/schéma**
  sans exécuter le code du plugin
- le comportement d'exécution natif provient du chemin `register(api)` du module du plugin

Cette séparation permet à OpenClaw de valider la config, d'expliquer les plugins manquants/désactivés et de
construire des indices UI/schéma avant que l'exécution complète soit active.

### Plugins de canal et l'outil de message partagé

Les plugins de canal n'ont pas besoin d'enregistrer un outil d'envoi/édition/réaction séparé pour
les actions de chat normales. OpenClaw garde un outil `message` partagé dans le noyau, et
les plugins de canal possèdent la découverte spécifique au canal et l'exécution derrière.

La limite actuelle est :

- le noyau possède l'hôte d'outil `message` partagé, le câblage du prompt, la
  tenue de registre de session/thread et la dispatch d'exécution
- les plugins de canal possèdent la découverte d'action scoped, la découverte de capacité et tout
  fragment de schéma spécifique au canal
- les plugins de canal exécutent l'action finale via leur adaptateur d'action

Pour les plugins de canal, la surface SDK est
`ChannelMessageActionAdapter.describeMessageTool(...)`. Cet appel de découverte unifié
permet à un plugin de retourner ses actions visibles, capacités et contributions de schéma
ensemble afin que ces pièces ne dérivent pas.

Le noyau passe la portée d'exécution dans cette étape de découverte. Les champs importants incluent :

- `accountId`
- `currentChannelId`
- `currentThreadTs`
- `currentMessageId`
- `sessionKey`
- `sessionId`
- `agentId`
- `requesterSenderId` entrant de confiance

C'est important pour les plugins sensibles au contexte. Un canal peut masquer ou exposer
les actions de message en fonction du compte actif, de la salle/thread/message actuelle ou de
l'identité du demandeur de confiance sans coder en dur les branches spécifiques au canal dans
l'outil `message` du noyau.

C'est pourquoi les changements de routage du runner intégré sont toujours du travail de plugin : le runner est
responsable de transférer l'identité actuelle de chat/session dans la limite de
découverte du plugin afin que l'outil `message` partagé expose la surface appropriée détenue par le canal pour le tour actuel.

Pour les assistants d'exécution détenus par le canal, les plugins groupés doivent garder l'exécution
d'exécution à l'intérieur de leurs propres modules d'extension. Le noyau ne possède plus les runtimes
d'action de message Discord, Slack, Telegram ou WhatsApp sous `src/agents/tools`.
Nous ne publions pas de sous-chemins `plugin-sdk/*-action-runtime` séparés, et les plugins
groupés doivent importer directement leur propre code d'exécution local à partir de leurs
modules détenus par l'extension.

Pour les sondages spécifiquement, il y a deux chemins d'exécution :

- `outbound.sendPoll` est la ligne de base partagée pour les canaux qui correspondent au modèle
  de sondage commun
- `actions.handleAction("poll")` est le chemin préféré pour la sémantique de sondage spécifique au canal ou les paramètres de sondage supplémentaires

Le noyau diffère maintenant l'analyse de sondage partagée jusqu'après que la dispatch de sondage du plugin décline
l'action, afin que les gestionnaires de sondage détenus par le plugin puissent accepter des champs de sondage spécifiques au canal
sans être bloqués par le parseur de sondage générique en premier.

Voir [Pipeline de chargement](#load-pipeline) pour la séquence de démarrage complète.

## Modèle de propriété des capacités

OpenClaw traite un plugin natif comme une limite de propriété pour une **entreprise** ou une **fonctionnalité**, et non comme un fourre-tout d'intégrations sans rapport.

Cela signifie :

- un plugin d'entreprise devrait généralement posséder toutes les surfaces orientées OpenClaw de cette entreprise
- un plugin de fonctionnalité devrait généralement posséder la surface complète de la fonctionnalité qu'il introduit
- les canaux doivent consommer les capacités principales partagées au lieu de réimplémenter le comportement du fournisseur de manière ad hoc

Exemples :

- le plugin `openai` fourni possède le comportement du fournisseur de modèles OpenAI et le comportement de la parole, de la compréhension des médias et de la génération d'images OpenAI
- le plugin `elevenlabs` fourni possède le comportement de la parole ElevenLabs
- le plugin `microsoft` fourni possède le comportement de la parole Microsoft
- le plugin `google` fourni possède le comportement du fournisseur de modèles Google plus la compréhension des médias, la génération d'images et la recherche web Google
- les plugins `minimax`, `mistral`, `moonshot` et `zai` fournis possèdent leurs backends de compréhension des médias
- le plugin `voice-call` est un plugin de fonctionnalité : il possède le transport des appels, les outils, l'interface de ligne de commande, les routes et l'exécution, mais il consomme la capacité TTS/STT principale au lieu d'inventer une deuxième pile de parole

L'état final prévu est :

- OpenAI vit dans un plugin même s'il s'étend sur les modèles de texte, la parole, les images et la vidéo future
- un autre fournisseur peut faire de même pour sa propre surface
- les canaux ne se soucient pas du plugin fournisseur qui possède le fournisseur ; ils consomment le contrat de capacité partagée exposé par le noyau

C'est la distinction clé :

- **plugin** = limite de propriété
- **capacité** = contrat principal que plusieurs plugins peuvent implémenter ou consommer

Donc si OpenClaw ajoute un nouveau domaine comme la vidéo, la première question n'est pas « quel fournisseur devrait coder en dur la gestion vidéo ? » La première question est « quel est le contrat de capacité vidéo principal ? » Une fois ce contrat en place, les plugins fournisseurs peuvent s'y enregistrer et les plugins de canal/fonctionnalité peuvent le consommer.

Si la capacité n'existe pas encore, le bon mouvement est généralement :

1. définir la capacité manquante dans le noyau
2. l'exposer via l'API du plugin/l'exécution de manière typée
3. connecter les canaux/fonctionnalités à cette capacité
4. laisser les plugins fournisseurs enregistrer les implémentations

Cela maintient la propriété explicite tout en évitant le comportement principal qui dépend d'un seul fournisseur ou d'un chemin de code spécifique à un plugin unique.

### Stratification des capacités

Utilisez ce modèle mental pour décider où le code appartient :

- **couche de capacité principale** : orchestration partagée, politique, secours, règles de fusion de configuration, sémantique de livraison et contrats typés
- **couche de plugin fournisseur** : API spécifiques au fournisseur, authentification, catalogues de modèles, synthèse vocale, génération d'images, backends vidéo futurs, points de terminaison d'utilisation
- **couche de plugin de canal/fonctionnalité** : intégration Slack/Discord/voice-call/etc. qui consomme les capacités principales et les présente sur une surface

Par exemple, TTS suit cette forme :

- le noyau possède la politique TTS au moment de la réponse, l'ordre de secours, les préférences et la livraison par canal
- `openai`, `elevenlabs` et `microsoft` possèdent les implémentations de synthèse
- `voice-call` consomme l'assistant d'exécution TTS de la téléphonie

Ce même modèle devrait être préféré pour les capacités futures.

### Exemple de plugin d'entreprise multi-capacité

Un plugin d'entreprise devrait sembler cohérent de l'extérieur. Si OpenClaw a des contrats partagés pour les modèles, la parole, la compréhension des médias et la recherche web, un fournisseur peut posséder toutes ses surfaces en un seul endroit :

```ts
import type { OpenClawPluginDefinition } from "openclaw/plugin-sdk";
import {
  buildOpenAISpeechProvider,
  createPluginBackedWebSearchProvider,
  describeImageWithModel,
  transcribeOpenAiCompatibleAudio,
} from "openclaw/plugin-sdk";

const plugin: OpenClawPluginDefinition = {
  id: "exampleai",
  name: "ExampleAI",
  register(api) {
    api.registerProvider({
      id: "exampleai",
      // auth/model catalog/runtime hooks
    });

    api.registerSpeechProvider(
      buildOpenAISpeechProvider({
        id: "exampleai",
        // vendor speech config
      }),
    );

    api.registerMediaUnderstandingProvider({
      id: "exampleai",
      capabilities: ["image", "audio", "video"],
      async describeImage(req) {
        return describeImageWithModel({
          provider: "exampleai",
          model: req.model,
          input: req.input,
        });
      },
      async transcribeAudio(req) {
        return transcribeOpenAiCompatibleAudio({
          provider: "exampleai",
          model: req.model,
          input: req.input,
        });
      },
    });

    api.registerWebSearchProvider(
      createPluginBackedWebSearchProvider({
        id: "exampleai-search",
        // credential + fetch logic
      }),
    );
  },
};

export default plugin;
```

Ce qui importe n'est pas les noms exacts des assistants. La forme importe :

- un plugin possède la surface du fournisseur
- le noyau possède toujours les contrats de capacité
- les canaux et les plugins de fonctionnalité consomment les assistants `api.runtime.*`, pas le code du fournisseur
- les tests de contrat peuvent affirmer que le plugin a enregistré les capacités qu'il prétend posséder

### Exemple de capacité : compréhension vidéo

OpenClaw traite déjà la compréhension des images/audio/vidéo comme une capacité partagée. Le même modèle de propriété s'applique là :

1. le noyau définit le contrat de compréhension des médias
2. les plugins fournisseurs enregistrent `describeImage`, `transcribeAudio` et `describeVideo` selon les cas
3. les canaux et les plugins de fonctionnalité consomment le comportement principal partagé au lieu de se connecter directement au code du fournisseur

Cela évite de cuire les hypothèses vidéo d'un fournisseur dans le noyau. Le plugin possède la surface du fournisseur ; le noyau possède le contrat de capacité et le comportement de secours.

Si OpenClaw ajoute un nouveau domaine plus tard, comme la génération vidéo, utilisez la même séquence à nouveau : définissez d'abord la capacité principale, puis laissez les plugins fournisseurs enregistrer les implémentations contre elle.

Besoin d'une liste de contrôle de déploiement concrète ? Voir [Capability Cookbook](/fr/tools/capability-cookbook).

## Contrats et application

La surface de l'API du plugin est intentionnellement typée et centralisée dans `OpenClawPluginApi`. Ce contrat définit les points d'enregistrement pris en charge et les assistants d'exécution sur lesquels un plugin peut compter.

Pourquoi cela importe :

- les auteurs de plugins obtiennent une norme interne stable
- le noyau peut rejeter la propriété dupliquée comme deux plugins enregistrant le même id de fournisseur
- le démarrage peut afficher des diagnostics exploitables pour les enregistrements mal formés
- les tests de contrat peuvent appliquer la propriété du plugin fourni et prévenir la dérive silencieuse

Il y a deux niveaux d'application :

1. **application d'enregistrement d'exécution**
   Le registre de plugins valide les enregistrements au fur et à mesure que les plugins se chargent. Les exemples incluent les ids de fournisseur dupliqués, les ids de fournisseur de parole dupliqués et les enregistrements mal formés qui produisent des diagnostics de plugin au lieu d'un comportement indéfini.
2. **tests de contrat**
   Les plugins fournis sont capturés dans les registres de contrat lors des exécutions de test afin qu'OpenClaw puisse affirmer la propriété explicitement. Aujourd'hui, ceci est utilisé pour les fournisseurs de modèles, les fournisseurs de parole, les fournisseurs de recherche web et la propriété d'enregistrement fournie.

L'effet pratique est qu'OpenClaw sait, à l'avance, quel plugin possède quelle surface. Cela permet au noyau et aux canaux de se composer de manière transparente car la propriété est déclarée, typée et testable plutôt qu'implicite.

### Ce qui appartient à un contrat

Les bons contrats de plugin sont :

- typés
- petits
- spécifiques à la capacité
- possédés par le noyau
- réutilisables par plusieurs plugins
- consommables par les canaux/fonctionnalités sans connaissance du fournisseur

Les mauvais contrats de plugin sont :

- politique spécifique au fournisseur cachée dans le noyau
- échappatoires de plugin unique qui contournent le registre
- code de canal accédant directement à une implémentation de fournisseur
- objets d'exécution ad hoc qui ne font pas partie de `OpenClawPluginApi` ou `api.runtime`

En cas de doute, élevez le niveau d'abstraction : définissez d'abord la capacité, puis laissez les plugins s'y brancher.

## Modèle d'exécution

Les plugins OpenClaw natifs s'exécutent **en processus** avec la passerelle. Ils ne sont pas isolés. Un plugin natif chargé a la même limite de confiance au niveau du processus que le code principal.

Implications :

- un plugin natif peut enregistrer des outils, des gestionnaires réseau, des crochets et des services
- un bug de plugin natif peut bloquer ou déstabiliser la passerelle
- un plugin natif malveillant équivaut à une exécution de code arbitraire à l'intérieur du processus OpenClaw

Les bundles compatibles sont plus sûrs par défaut car OpenClaw les traite actuellement comme des packs de métadonnées/contenu. Dans les versions actuelles, cela signifie principalement les compétences fournies.

Utilisez des listes blanches et des chemins d'installation/chargement explicites pour les plugins non fournis. Traitez les plugins d'espace de travail comme du code au moment du développement, pas comme des valeurs par défaut de production.

Note de confiance importante :

- `plugins.allow` fait confiance aux **ids de plugin**, pas à la provenance de la source.
- Un plugin d'espace de travail avec le même id qu'un plugin fourni masque intentionnellement la copie fournie lorsque ce plugin d'espace de travail est activé/autorisé.
- C'est normal et utile pour le développement local, les tests de correctifs et les correctifs d'urgence.

## Limite d'exportation

OpenClaw exporte les capacités, pas la commodité d'implémentation.

Gardez l'enregistrement des capacités public. Réduisez les exportations d'assistants non-contrat :

- chemins d'assistants spécifiques aux plugins fournis
- chemins de plomberie d'exécution non destinés à être une API publique
- assistants de commodité spécifiques au fournisseur
- assistants de configuration/intégration qui sont des détails d'implémentation

## Pipeline de chargement

Au démarrage, OpenClaw fait à peu près ceci :

1. découvrir les racines de plugin candidates
2. lire les manifestes de bundle natif ou compatible et les métadonnées de package
3. rejeter les candidats non sûrs
4. normaliser la configuration du plugin (`plugins.enabled`, `allow`, `deny`, `entries`, `slots`, `load.paths`)
5. décider de l'activation pour chaque candidat
6. charger les modules natifs activés via jiti
7. appeler les crochets natifs `register(api)` et collecter les enregistrements dans le registre de plugins
8. exposer le registre aux surfaces de commandes/exécution

Les portes de sécurité se produisent **avant** l'exécution d'exécution. Les candidats sont bloqués lorsque l'entrée s'échappe de la racine du plugin, le chemin est accessible en écriture par tous, ou la propriété du chemin semble suspecte pour les plugins non fournis.

### Comportement d'abord le manifeste

Le manifeste est la source de vérité du plan de contrôle. OpenClaw l'utilise pour :

- identifier le plugin
- découvrir les canaux/compétences/schéma de configuration déclarés ou les capacités de bundle
- valider `plugins.entries.<id>.config`
- augmenter les étiquettes/espaces réservés de l'interface utilisateur de contrôle
- afficher les métadonnées d'installation/catalogue

Pour les plugins natifs, le module d'exécution est la partie plan de données. Il enregistre le comportement réel comme les crochets, les outils, les commandes ou les flux de fournisseur.

### Ce que le chargeur met en cache

OpenClaw conserve des caches courts en processus pour :

- résultats de découverte
- données du registre de manifeste
- registres de plugins chargés

Ces caches réduisent le démarrage en rafales et la surcharge de commandes répétées. Ils sont sûrs à considérer comme des caches de performance à courte durée de vie, pas de persistance.

Note de performance :

- Définissez `OPENCLAW_DISABLE_PLUGIN_DISCOVERY_CACHE=1` ou `OPENCLAW_DISABLE_PLUGIN_MANIFEST_CACHE=1` pour désactiver ces caches.
- Ajustez les fenêtres de cache avec `OPENCLAW_PLUGIN_DISCOVERY_CACHE_MS` et `OPENCLAW_PLUGIN_MANIFEST_CACHE_MS`.

## Modèle de registre

Les plugins chargés ne mutent pas directement les globales principales aléatoires. Ils s'enregistrent dans un registre de plugins central.

Le registre suit :

- enregistrements de plugins (identité, source, origine, statut, diagnostics)
- outils
- crochets hérités et crochets typés
- canaux
- fournisseurs
- gestionnaires RPC de passerelle
- routes HTTP
- enregistreurs CLI
- services d'arrière-plan
- commandes possédées par les plugins

Les fonctionnalités principales lisent ensuite à partir de ce registre au lieu de parler directement aux modules de plugins. Cela maintient le chargement unidirectionnel :

- module de plugin -> enregistrement de registre
- exécution principale -> consommation de registre

Cette séparation importe pour la maintenabilité. Cela signifie que la plupart des surfaces principales n'ont besoin que d'un point d'intégration : « lire le registre », pas « cas spécial pour chaque module de plugin ».

## Rappels de liaison de conversation

Les plugins qui lient une conversation peuvent réagir lorsqu'une approbation est résolue.

Utilisez `api.onConversationBindingResolved(...)` pour recevoir un rappel après qu'une demande de liaison soit approuvée ou refusée :

```ts
export default {
  id: "my-plugin",
  register(api) {
    api.onConversationBindingResolved(async (event) => {
      if (event.status === "approved") {
        // A binding now exists for this plugin + conversation.
        console.log(event.binding?.conversationId);
        return;
      }

      // The request was denied; clear any local pending state.
      console.log(event.request.conversation.conversationId);
    });
  },
};
```

Champs de la charge utile du rappel :

- `status` : `"approved"` ou `"denied"`
- `decision` : `"allow-once"`, `"allow-always"`, ou `"deny"`
- `binding` : la liaison résolue pour les demandes approuvées
- `request` : le résumé de la demande d'origine, l'indice de détachement, l'identifiant de l'expéditeur et les métadonnées de conversation

Ce rappel est à titre informatif uniquement. Il ne change pas qui est autorisé à lier une conversation et s'exécute après la fin de la gestion de l'approbation principale.

## Crochets d'exécution du fournisseur

Les plugins de fournisseur ont maintenant deux couches :

- métadonnées du manifeste : `providerAuthEnvVars` pour une recherche d'authentification par env bon marché avant le chargement du runtime, plus `providerAuthChoices` pour les étiquettes d'intégration/choix d'authentification bon marché et les métadonnées d'indicateur CLI avant le chargement du runtime
- crochets au moment de la configuration : `catalog` / `discovery` hérité
- crochets d'exécution : `resolveDynamicModel`, `prepareDynamicModel`, `normalizeResolvedModel`, `capabilities`, `prepareExtraParams`, `wrapStreamFn`, `formatApiKey`, `refreshOAuth`, `buildAuthDoctorHint`, `isCacheTtlEligible`, `buildMissingAuthMessage`, `suppressBuiltInModel`, `augmentModelCatalog`, `isBinaryThinking`, `supportsXHighThinking`, `resolveDefaultThinkingLevel`, `isModernModelRef`, `prepareRuntimeAuth`, `resolveUsageAuth`, `fetchUsageSnapshot`

OpenClaw conserve toujours la boucle d'agent générique, le basculement, la gestion des transcriptions et la politique des outils. Ces crochets constituent la surface d'extension pour le comportement spécifique au fournisseur sans avoir besoin d'un transport d'inférence personnalisé complet.

Utilisez le manifeste `providerAuthEnvVars` lorsque le fournisseur dispose d'identifiants basés sur l'environnement que les chemins d'authentification/statut/sélecteur de modèle génériques doivent voir sans charger le runtime du plugin. Utilisez le manifeste `providerAuthChoices` lorsque les surfaces CLI d'intégration/choix d'authentification doivent connaître l'ID de choix du fournisseur, les étiquettes de groupe et le câblage d'authentification simple à un indicateur sans charger le runtime du fournisseur. Conservez le `envVars` du runtime du fournisseur pour les indices destinés à l'opérateur, tels que les étiquettes d'intégration ou les variables de configuration client-id/client-secret OAuth.

### Ordre et utilisation des crochets

Pour les plugins de modèle/fournisseur, OpenClaw appelle les crochets dans cet ordre approximatif.
La colonne « Quand l'utiliser » est le guide de décision rapide.

| #   | Crochet                       | Ce qu'il fait                                                                            | Quand l'utiliser                                                                     |
| --- | ----------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 1   | `catalog`                     | Publier la configuration du fournisseur dans `models.providers` lors de la génération de `models.json` | Le fournisseur possède un catalogue ou des valeurs par défaut d'URL de base           |
| --  | _(recherche de modèle intégrée)_ | OpenClaw essaie d'abord le chemin normal du registre/catalogue                        | _(pas un crochet de plugin)_                                                        |
| 2   | `resolveDynamicModel`         | Secours synchrone pour les ID de modèle appartenant au fournisseur pas encore dans le registre local | Le fournisseur accepte les ID de modèle en amont arbitraires                         |
| 3   | `prepareDynamicModel`         | Échauffement asynchrone, puis `resolveDynamicModel` s'exécute à nouveau                 | Le fournisseur a besoin de métadonnées réseau avant de résoudre les ID inconnus      |
| 4   | `normalizeResolvedModel`      | Réécriture finale avant que le runner intégré utilise le modèle résolu                  | Le fournisseur a besoin de réécritures de transport mais utilise toujours un transport principal |
| 5   | `capabilities`                | Métadonnées de transcription/outillage appartenant au fournisseur utilisées par la logique principale partagée | Le fournisseur a besoin de particularités de transcription/famille de fournisseurs   |
| 6   | `prepareExtraParams`          | Normalisation des paramètres de requête avant les wrappers d'options de flux génériques | Le fournisseur a besoin de paramètres de requête par défaut ou de nettoyage de paramètres par fournisseur |
| 7   | `wrapStreamFn`                | Wrapper de flux après l'application des wrappers génériques                             | Le fournisseur a besoin de wrappers de compatibilité d'en-têtes/corps/modèle de requête sans transport personnalisé |
| 8   | `formatApiKey`                | Formateur de profil d'authentification : le profil stocké devient la chaîne `apiKey` du runtime | Le fournisseur stocke des métadonnées d'authentification supplémentaires et a besoin d'une forme de jeton runtime personnalisée |
| 9   | `refreshOAuth`                | Remplacement de l'actualisation OAuth pour les points de terminaison d'actualisation personnalisés ou la politique d'échec d'actualisation | Le fournisseur ne correspond pas aux actualisateurs `pi-ai` partagés                 |
| 10  | `buildAuthDoctorHint`         | Conseil de réparation ajouté en cas d'échec de l'actualisation OAuth                    | Le fournisseur a besoin de conseils de réparation d'authentification appartenant au fournisseur après l'échec de l'actualisation |
| 11  | `isCacheTtlEligible`          | Politique de cache de requête pour les fournisseurs proxy/backhaul                      | Le fournisseur a besoin d'une limitation TTL de cache spécifique au proxy            |
| 12  | `buildMissingAuthMessage`     | Remplacement du message de récupération d'authentification manquante générique           | Le fournisseur a besoin d'un conseil de récupération d'authentification manquante spécifique au fournisseur |
| 13  | `suppressBuiltInModel`        | Suppression de modèle en amont obsolète plus conseil d'erreur optionnel destiné à l'utilisateur | Le fournisseur a besoin de masquer les lignes en amont obsolètes ou de les remplacer par un conseil du fournisseur |
| 14  | `augmentModelCatalog`         | Lignes de catalogue synthétiques/finales ajoutées après la découverte                   | Le fournisseur a besoin de lignes de compatibilité directe synthétiques dans `models list` et les sélecteurs |
| 15  | `isBinaryThinking`            | Basculement de raisonnement activé/désactivé pour les fournisseurs de raisonnement binaire | Le fournisseur expose uniquement le raisonnement binaire activé/désactivé            |
| 16  | `supportsXHighThinking`       | Support du raisonnement `xhigh` pour les modèles sélectionnés                           | Le fournisseur souhaite `xhigh` uniquement sur un sous-ensemble de modèles           |
| 17  | `resolveDefaultThinkingLevel` | Niveau `/think` par défaut pour une famille de modèles spécifique                      | Le fournisseur possède la politique `/think` par défaut pour une famille de modèles  |
| 18  | `isModernModelRef`            | Correspondant de modèle moderne pour les filtres de profil en direct et la sélection de fumée | Le fournisseur possède la correspondance de modèle préféré en direct/fumée           |
| 19  | `prepareRuntimeAuth`          | Échanger une identité configurée contre le jeton/clé runtime réel juste avant l'inférence | Le fournisseur a besoin d'un échange de jeton ou d'une identité de requête à courte durée de vie |
| 20  | `resolveUsageAuth`            | Résoudre les identifiants d'utilisation/facturation pour `/usage` et les surfaces d'état connexes | Le fournisseur a besoin d'une analyse de jeton de quota/utilisation personnalisée ou d'une identité d'utilisation différente |
| 21  | `fetchUsageSnapshot`          | Récupérer et normaliser les instantanés d'utilisation/quota spécifiques au fournisseur après la résolution de l'authentification | Le fournisseur a besoin d'un point de terminaison d'utilisation spécifique au fournisseur ou d'un analyseur de charge utile |

Si le fournisseur a besoin d'un protocole de câblage entièrement personnalisé ou d'un exécuteur de requête personnalisé,
c'est une classe d'extension différente. Ces crochets sont pour le comportement du fournisseur
qui s'exécute toujours sur la boucle d'inférence normale d'OpenClaw.

### Exemple de fournisseur

```ts
api.registerProvider({
  id: "example-proxy",
  label: "Example Proxy",
  auth: [],
  catalog: {
    order: "simple",
    run: async (ctx) => {
      const apiKey = ctx.resolveProviderApiKey("example-proxy").apiKey;
      if (!apiKey) {
        return null;
      }
      return {
        provider: {
          baseUrl: "https://proxy.example.com/v1",
          apiKey,
          api: "openai-completions",
          models: [{ id: "auto", name: "Auto" }],
        },
      };
    },
  },
  resolveDynamicModel: (ctx) => ({
    id: ctx.modelId,
    name: ctx.modelId,
    provider: "example-proxy",
    api: "openai-completions",
    baseUrl: "https://proxy.example.com/v1",
    reasoning: false,
    input: ["text"],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 128000,
    maxTokens: 8192,
  }),
  prepareRuntimeAuth: async (ctx) => {
    const exchanged = await exchangeToken(ctx.apiKey);
    return {
      apiKey: exchanged.token,
      baseUrl: exchanged.baseUrl,
      expiresAt: exchanged.expiresAt,
    };
  },
  resolveUsageAuth: async (ctx) => {
    const auth = await ctx.resolveOAuthToken();
    return auth ? { token: auth.token } : null;
  },
  fetchUsageSnapshot: async (ctx) => {
    return await fetchExampleProxyUsage(ctx.token, ctx.timeoutMs, ctx.fetchFn);
  },
});
```

### Exemples intégrés

- Anthropic utilise `resolveDynamicModel`, `capabilities`, `buildAuthDoctorHint`,
  `resolveUsageAuth`, `fetchUsageSnapshot`, `isCacheTtlEligible`,
  `resolveDefaultThinkingLevel` et `isModernModelRef` car il possède la compatibilité directe Claude
  4.6, les conseils spécifiques à la famille de fournisseurs, les conseils de réparation d'authentification, l'intégration du point de terminaison d'utilisation, l'admissibilité du cache de requête et la politique de raisonnement par défaut/adaptatif de Claude.
- OpenAI utilise `resolveDynamicModel`, `normalizeResolvedModel` et
  `capabilities` plus `buildMissingAuthMessage`, `suppressBuiltInModel`,
  `augmentModelCatalog`, `supportsXHighThinking` et `isModernModelRef`
  car il possède la compatibilité directe GPT-5.4, la normalisation directe OpenAI
  `openai-completions` -> `openai-responses`, les conseils d'authentification conscients de Codex,
  la suppression de Spark, les lignes de liste OpenAI synthétiques et la politique de raisonnement/modèle en direct GPT-5.
- OpenRouter utilise `catalog` plus `resolveDynamicModel` et
  `prepareDynamicModel` car le fournisseur est un pass-through et peut exposer de nouveaux
  ID de modèle avant les mises à jour du catalogue statique d'OpenClaw ; il utilise également
  `capabilities`, `wrapStreamFn` et `isCacheTtlEligible` pour conserver
  les en-têtes de requête spécifiques au fournisseur, les métadonnées de routage, les correctifs de raisonnement et
  la politique de cache de requête en dehors du noyau.
- GitHub Copilot utilise `catalog`, `auth`, `resolveDynamicModel` et
  `capabilities` plus `prepareRuntimeAuth` et `fetchUsageSnapshot` car il
  a besoin de la connexion d'appareil appartenant au fournisseur, du comportement de secours du modèle, des particularités de transcription Claude, d'un échange de jeton GitHub -> jeton Copilot et d'un
  point de terminaison d'utilisation appartenant au fournisseur.
- OpenAI Codex utilise `catalog`, `resolveDynamicModel`,
  `normalizeResolvedModel`, `refreshOAuth` et `augmentModelCatalog` plus
  `prepareExtraParams`, `resolveUsageAuth` et `fetchUsageSnapshot` car il
  s'exécute toujours sur les transports OpenAI principaux mais possède sa normalisation de transport/URL de base,
  la politique de secours d'actualisation OAuth, le choix de transport par défaut,
  les lignes de catalogue Codex synthétiques et l'intégration du point de terminaison d'utilisation ChatGPT.
- Google AI Studio et Gemini CLI OAuth utilisent `resolveDynamicModel` et
  `isModernModelRef` car ils possèdent le secours de compatibilité directe Gemini 3.1 et
  la correspondance de modèle moderne ; Gemini CLI OAuth utilise également `formatApiKey`,
  `resolveUsageAuth` et `fetchUsageSnapshot` pour le formatage de jeton, l'analyse de jeton et
  le câblage du point de terminaison de quota.
- Moonshot utilise `catalog` plus `wrapStreamFn` car il utilise toujours le
  transport OpenAI partagé mais a besoin de la normalisation de charge utile de raisonnement appartenant au fournisseur.
- Kilocode utilise `catalog`, `capabilities`, `wrapStreamFn` et
  `isCacheTtlEligible` car il a besoin des en-têtes de requête appartenant au fournisseur,
  de la normalisation de charge utile de raisonnement, des conseils de transcription Gemini et
  de la limitation TTL de cache Anthropic.
- Z.AI utilise `resolveDynamicModel`, `prepareExtraParams`, `wrapStreamFn`,
  `isCacheTtlEligible`, `isBinaryThinking`, `isModernModelRef`,
  `resolveUsageAuth` et `fetchUsageSnapshot` car il possède le secours GLM-5,
  les valeurs par défaut `tool_stream`, l'UX de raisonnement binaire, la correspondance de modèle moderne et
  l'authentification d'utilisation + la récupération de quota.
- Mistral, OpenCode Zen et OpenCode Go utilisent uniquement `capabilities` pour conserver
  les particularités de transcription/outillage en dehors du noyau.
- Les fournisseurs groupés uniquement par catalogue tels que `byteplus`, `cloudflare-ai-gateway`,
  `huggingface`, `kimi-coding`, `modelstudio`, `nvidia`, `qianfan`,
  `synthetic`, `together`, `venice`, `vercel-ai-gateway` et `volcengine` utilisent
  uniquement `catalog`.
- Le portail Qwen utilise `catalog`, `auth` et `refreshOAuth`.
- MiniMax et Xiaomi utilisent `catalog` plus les crochets d'utilisation car leur comportement `/usage`
  appartient au plugin même si l'inférence s'exécute toujours via les
  transports partagés.

## Assistants d'exécution

Les plugins peuvent accéder aux assistants principaux sélectionnés via `api.runtime`. Pour TTS :

```ts
const clip = await api.runtime.tts.textToSpeech({
  text: "Hello from OpenClaw",
  cfg: api.config,
});

const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});

const voices = await api.runtime.tts.listVoices({
  provider: "elevenlabs",
  cfg: api.config,
});
```

Notes :

- `textToSpeech` retourne la charge utile de sortie TTS principale pour les surfaces de fichier/note vocale.
- Utilise la configuration `messages.tts` principale et la sélection du fournisseur.
- Retourne un tampon audio PCM + taux d'échantillonnage. Les plugins doivent rééchantillonner/encoder pour les fournisseurs.
- `listVoices` est optionnel par fournisseur. Utilisez-le pour les sélecteurs de voix propriétaires ou les flux de configuration.
- Les listes de voix peuvent inclure des métadonnées plus riches telles que la locale, le sexe et les balises de personnalité pour les sélecteurs conscients du fournisseur.
- OpenAI et ElevenLabs supportent la téléphonie aujourd'hui. Microsoft ne le fait pas.

Les plugins peuvent également enregistrer des fournisseurs de parole via `api.registerSpeechProvider(...)`.

```ts
api.registerSpeechProvider({
  id: "acme-speech",
  label: "Acme Speech",
  isConfigured: ({ config }) => Boolean(config.messages?.tts),
  synthesize: async (req) => {
    return {
      audioBuffer: Buffer.from([]),
      outputFormat: "mp3",
      fileExtension: ".mp3",
      voiceCompatible: false,
    };
  },
});
```

Notes :

- Conservez la politique TTS, le repli et la livraison des réponses dans le cœur.
- Utilisez les fournisseurs de parole pour le comportement de synthèse propriétaire du fournisseur.
- L'entrée Microsoft `edge` héritée est normalisée vers l'ID de fournisseur `microsoft`.
- Le modèle de propriété préféré est orienté vers l'entreprise : un plugin fournisseur peut posséder des fournisseurs de texte, de parole, d'image et de futurs médias à mesure qu'OpenClaw ajoute ces contrats de capacité.

Pour la compréhension d'image/audio/vidéo, les plugins enregistrent un fournisseur de compréhension de média typé au lieu d'un sac générique clé/valeur :

```ts
api.registerMediaUnderstandingProvider({
  id: "google",
  capabilities: ["image", "audio", "video"],
  describeImage: async (req) => ({ text: "..." }),
  transcribeAudio: async (req) => ({ text: "..." }),
  describeVideo: async (req) => ({ text: "..." }),
});
```

Notes :

- Conservez l'orchestration, le repli, la configuration et le câblage des canaux dans le cœur.
- Conservez le comportement du fournisseur dans le plugin du fournisseur.
- L'expansion additive doit rester typée : nouvelles méthodes optionnelles, nouveaux champs de résultat optionnels, nouvelles capacités optionnelles.
- Si OpenClaw ajoute une nouvelle capacité telle que la génération vidéo ultérieurement, définissez d'abord le contrat de capacité principal, puis laissez les plugins fournisseurs s'enregistrer contre lui.

Pour les assistants d'exécution de compréhension de média, les plugins peuvent appeler :

```ts
const image = await api.runtime.mediaUnderstanding.describeImageFile({
  filePath: "/tmp/inbound-photo.jpg",
  cfg: api.config,
  agentDir: "/tmp/agent",
});

const video = await api.runtime.mediaUnderstanding.describeVideoFile({
  filePath: "/tmp/inbound-video.mp4",
  cfg: api.config,
});
```

Pour la transcription audio, les plugins peuvent utiliser soit l'assistant d'exécution de compréhension de média, soit l'alias STT plus ancien :

```ts
const { text } = await api.runtime.mediaUnderstanding.transcribeAudioFile({
  filePath: "/tmp/inbound-audio.ogg",
  cfg: api.config,
  // Optionnel quand MIME ne peut pas être déduit de manière fiable :
  mime: "audio/ogg",
});
```

Notes :

- `api.runtime.mediaUnderstanding.*` est la surface partagée préférée pour la compréhension d'image/audio/vidéo.
- Utilise la configuration audio de compréhension de média principale (`tools.media.audio`) et l'ordre de repli du fournisseur.
- Retourne `{ text: undefined }` quand aucune sortie de transcription n'est produite (par exemple entrée ignorée/non supportée).
- `api.runtime.stt.transcribeAudioFile(...)` reste comme un alias de compatibilité.

Les plugins peuvent également lancer des exécutions de sous-agent en arrière-plan via `api.runtime.subagent` :

```ts
const result = await api.runtime.subagent.run({
  sessionKey: "agent:main:subagent:search-helper",
  message: "Expand this query into focused follow-up searches.",
  provider: "openai",
  model: "gpt-4.1-mini",
  deliver: false,
});
```

Notes :

- `provider` et `model` sont des remplacements optionnels par exécution, pas des changements de session persistants.
- OpenClaw honore uniquement ces champs de remplacement pour les appelants de confiance.
- Pour les exécutions de repli propriétaires du plugin, les opérateurs doivent accepter avec `plugins.entries.<id>.subagent.allowModelOverride: true`.
- Utilisez `plugins.entries.<id>.subagent.allowedModels` pour restreindre les plugins de confiance à des cibles `provider/model` canoniques spécifiques, ou `"*"` pour autoriser explicitement n'importe quelle cible.
- Les exécutions de sous-agent de plugin non fiables fonctionnent toujours, mais les demandes de remplacement sont rejetées au lieu de revenir silencieusement.

Pour la recherche web, les plugins peuvent consommer l'assistant d'exécution partagé au lieu d'accéder au câblage de l'outil d'agent :

```ts
const providers = api.runtime.webSearch.listProviders({
  config: api.config,
});

const result = await api.runtime.webSearch.search({
  config: api.config,
  args: {
    query: "OpenClaw plugin runtime helpers",
    count: 5,
  },
});
```

Les plugins peuvent également enregistrer des fournisseurs de recherche web via `api.registerWebSearchProvider(...)`.

Notes :

- Conservez la sélection du fournisseur, la résolution des identifiants, et la sémantique des demandes partagées dans le cœur.
- Utilisez les fournisseurs de recherche web pour les transports de recherche spécifiques au fournisseur.
- `api.runtime.webSearch.*` est la surface partagée préférée pour les plugins de fonctionnalité/canal qui ont besoin d'un comportement de recherche sans dépendre du wrapper d'outil d'agent.

## Routes HTTP de la passerelle

Les plugins peuvent exposer des points de terminaison HTTP avec `api.registerHttpRoute(...)`.

```ts
api.registerHttpRoute({
  path: "/acme/webhook",
  auth: "plugin",
  match: "exact",
  handler: async (_req, res) => {
    res.statusCode = 200;
    res.end("ok");
    return true;
  },
});
```

Champs de route :

- `path` : chemin de route sous le serveur HTTP de la passerelle.
- `auth` : requis. Utilisez `"gateway"` pour exiger l'authentification normale de la passerelle, ou `"plugin"` pour l'authentification gérée par le plugin/vérification du webhook.
- `match` : optionnel. `"exact"` (par défaut) ou `"prefix"`.
- `replaceExisting` : optionnel. Permet au même plugin de remplacer son propre enregistrement de route existant.
- `handler` : retournez `true` quand la route a traité la demande.

Notes :

- `api.registerHttpHandler(...)` est obsolète. Utilisez `api.registerHttpRoute(...)`.
- Les routes de plugin doivent déclarer `auth` explicitement.
- Les conflits exacts `path + match` sont rejetés sauf si `replaceExisting: true`, et un plugin ne peut pas remplacer la route d'un autre plugin.
- Les routes qui se chevauchent avec différents niveaux `auth` sont rejetées. Conservez les chaînes de secours `exact`/`prefix` au même niveau d'authentification uniquement.

## Chemins d'importation du SDK de plugin

Utilisez les sous-chemins du SDK au lieu de l'importation monolithique `openclaw/plugin-sdk` lors de la création de plugins :

- `openclaw/plugin-sdk/plugin-entry` pour les primitives d'enregistrement de plugin.
- `openclaw/plugin-sdk/core` pour le contrat partagé générique face au plugin.
- Les primitives de canal stables telles que `openclaw/plugin-sdk/channel-setup`,
  `openclaw/plugin-sdk/channel-pairing`,
  `openclaw/plugin-sdk/channel-reply-pipeline`,
  `openclaw/plugin-sdk/secret-input`, et
  `openclaw/plugin-sdk/webhook-ingress` pour le câblage partagé de configuration/authentification/réponse/webhook.
- Les sous-chemins de domaine tels que `openclaw/plugin-sdk/channel-config-helpers`,
  `openclaw/plugin-sdk/channel-config-schema`,
  `openclaw/plugin-sdk/channel-policy`,
  `openclaw/plugin-sdk/channel-runtime`,
  `openclaw/plugin-sdk/config-runtime`,
  `openclaw/plugin-sdk/agent-runtime`,
  `openclaw/plugin-sdk/lazy-runtime`,
  `openclaw/plugin-sdk/reply-history`,
  `openclaw/plugin-sdk/routing`,
  `openclaw/plugin-sdk/runtime-store`, et
  `openclaw/plugin-sdk/directory-runtime` pour les assistants partagés de runtime/configuration.
- Les sous-chemins de canal-cœur étroits tels que `openclaw/plugin-sdk/discord-core`,
  `openclaw/plugin-sdk/telegram-core`, et `openclaw/plugin-sdk/whatsapp-core`
  pour les primitives spécifiques au canal qui doivent rester plus petites que les barils d'assistant de canal complets.
- Les internes d'extension groupés restent privés. Les plugins externes doivent utiliser uniquement les sous-chemins `openclaw/plugin-sdk/*`. Le code principal/test d'OpenClaw peut utiliser les points d'entrée publics du référentiel sous `extensions/<id>/index.js`, `api.js`, `runtime-api.js`,
  `setup-entry.js`, et les fichiers étroitement délimités tels que `login-qr-api.js`. N'importez jamais `extensions/<id>/src/*` depuis le cœur ou depuis une autre extension.
- Division du point d'entrée du référentiel :
  `extensions/<id>/api.js` est le baril d'assistant/types,
  `extensions/<id>/runtime-api.js` est le baril réservé à l'exécution,
  `extensions/<id>/index.js` est l'entrée du plugin groupé,
  et `extensions/<id>/setup-entry.js` est l'entrée du plugin de configuration.
- `openclaw/plugin-sdk/telegram` pour les types de plugin de canal Telegram et les assistants partagés face au canal. Les internes d'implémentation Telegram groupés restent privés à l'extension groupée.
- `openclaw/plugin-sdk/discord` pour les types de plugin de canal Discord et les assistants partagés face au canal. Les internes d'implémentation Discord groupés restent privés à l'extension groupée.
- `openclaw/plugin-sdk/slack` pour les types de plugin de canal Slack et les assistants partagés face au canal. Les internes d'implémentation Slack groupés restent privés à l'extension groupée.
- `openclaw/plugin-sdk/imessage` pour les types de plugin de canal iMessage et les assistants partagés face au canal. Les internes d'implémentation iMessage groupés restent privés à l'extension groupée.
- `openclaw/plugin-sdk/whatsapp` pour les types de plugin de canal WhatsApp et les assistants partagés face au canal. Les internes d'implémentation WhatsApp groupés restent privés à l'extension groupée.
- `openclaw/plugin-sdk/bluebubbles` reste public car il porte une petite surface d'assistant focalisée qui est partagée intentionnellement.

Note de compatibilité :

- Évitez le baril racine `openclaw/plugin-sdk` pour le nouveau code.
- Préférez d'abord les primitives stables étroites. Les sous-chemins de configuration/appairage/réponse/entrée-secrète/webhook plus récents sont le contrat prévu pour le travail de plugin groupé et externe nouveau.
- Les barils d'assistant spécifiques à l'extension groupée ne sont pas stables par défaut. Si un assistant n'est nécessaire que pour une extension groupée, conservez-le derrière la couche locale `api.js` ou `runtime-api.js` de l'extension au lieu de le promouvoir dans `openclaw/plugin-sdk/<extension>`.
- Les sous-chemins spécifiques à la capacité tels que `image-generation`,
  `media-understanding`, et `speech` existent car les plugins groupés/natifs les utilisent aujourd'hui. Leur présence ne signifie pas en soi que chaque assistant exporté est un contrat externe gelé à long terme.

## Résolution de cible de canal

Les plugins de canal doivent posséder la sémantique de cible spécifique au canal. Conservez l'hôte sortant partagé générique et utilisez la surface d'adaptateur de messagerie pour les règles du fournisseur :

- `messaging.inferTargetChatType({ to })` décide si une cible normalisée doit être traitée comme `direct`, `group`, ou `channel` avant la recherche d'annuaire.
- `messaging.targetResolver.looksLikeId(raw, normalized)` indique au cœur si une entrée doit ignorer directement la résolution de type id au lieu de la recherche d'annuaire.
- `messaging.targetResolver.resolveTarget(...)` est le repli du plugin quand le cœur a besoin d'une résolution finale propriétaire du fournisseur après normalisation ou après un manque d'annuaire.
- `messaging.resolveOutboundSessionRoute(...)` possède la construction de route de session spécifique au fournisseur une fois qu'une cible est résolue.

Division recommandée :

- Utilisez `inferTargetChatType` pour les décisions de catégorie qui doivent se produire avant de rechercher les pairs/groupes.
- Utilisez `looksLikeId` pour les vérifications "traiter ceci comme une cible id explicite/native".
- Utilisez `resolveTarget` pour le repli de normalisation spécifique au fournisseur, pas pour la recherche d'annuaire large.
- Conservez les ids natifs du fournisseur comme les ids de chat, les ids de thread, les JID, les poignées et les ids de salle à l'intérieur des valeurs `target` ou des paramètres spécifiques au fournisseur, pas dans les champs SDK génériques.

## Répertoires soutenus par la configuration

Les plugins qui dérivaient les entrées de répertoire de la configuration doivent conserver cette logique dans le plugin et réutiliser les assistants partagés de `openclaw/plugin-sdk/directory-runtime`.

Utilisez ceci quand un canal a besoin de pairs/groupes soutenus par la configuration, tels que :

- pairs DM basés sur liste blanche
- cartes de canal/groupe configurées
- replis de répertoire statique limités au compte

Les assistants partagés dans `directory-runtime` ne gèrent que les opérations génériques :

- filtrage des requêtes
- application des limites
- assistants de déduplication/normalisation
- construction de `ChannelDirectoryEntry[]`

L'inspection de compte spécifique au canal et la normalisation des identifiants doivent rester dans l'implémentation du plugin.

## Catalogues de fournisseurs

Les plugins de fournisseur peuvent définir des catalogues de modèles pour l'inférence avec `registerProvider({ catalog: { run(...) { ... } } })`.

`catalog.run(...)` retourne la même forme qu'OpenClaw écrit dans `models.providers` :

- `{ provider }` pour une entrée de fournisseur
- `{ providers }` pour plusieurs entrées de fournisseur

Utilisez `catalog` quand votre plugin possède des identifiants de modèle spécifiques au fournisseur, des valeurs par défaut d'URL de base, ou des métadonnées de modèle protégées par authentification.

`catalog.order` contrôle quand le catalogue d'un plugin se fusionne par rapport aux fournisseurs implicites intégrés d'OpenClaw :

- `simple` : fournisseurs simples basés sur clé API ou environnement
- `profile` : fournisseurs qui apparaissent quand des profils d'authentification existent
- `paired` : fournisseurs qui synthétisent plusieurs entrées de fournisseur connexes
- `late` : dernier passage, après les autres fournisseurs implicites

Les fournisseurs ultérieurs gagnent en cas de collision de clé, donc les plugins peuvent intentionnellement remplacer une entrée de fournisseur intégrée avec le même identifiant de fournisseur.

Compatibilité :

- `discovery` fonctionne toujours comme alias hérité
- si à la fois `catalog` et `discovery` sont enregistrés, OpenClaw utilise `catalog`

## Inspection de canal en lecture seule

Si votre plugin enregistre un canal, préférez implémenter `plugin.config.inspectAccount(cfg, accountId)` aux côtés de `resolveAccount(...)`.

Pourquoi :

- `resolveAccount(...)` est le chemin d'exécution. Il est autorisé à supposer que les identifiants sont entièrement matérialisés et peut échouer rapidement quand les secrets requis manquent.
- Les chemins de commande en lecture seule tels que `openclaw status`, `openclaw status --all`, `openclaw channels status`, `openclaw channels resolve`, et les flux de réparation doctor/config ne doivent pas avoir besoin de matérialiser les identifiants d'exécution juste pour décrire la configuration.

Comportement recommandé de `inspectAccount(...)` :

- Retournez uniquement l'état du compte descriptif.
- Préservez `enabled` et `configured`.
- Incluez les champs de source/statut des identifiants quand pertinent, tels que :
  - `tokenSource`, `tokenStatus`
  - `botTokenSource`, `botTokenStatus`
  - `appTokenSource`, `appTokenStatus`
  - `signingSecretSource`, `signingSecretStatus`
- Vous n'avez pas besoin de retourner les valeurs de jeton brutes juste pour signaler la disponibilité en lecture seule. Retourner `tokenStatus: "available"` (et le champ source correspondant) est suffisant pour les commandes de style statut.
- Utilisez `configured_unavailable` quand un identifiant est configuré via SecretRef mais indisponible dans le chemin de commande actuel.

Cela permet aux commandes en lecture seule de signaler « configuré mais indisponible dans ce chemin de commande » au lieu de planter ou de mal signaler le compte comme non configuré.

## Packs de paquets

Un répertoire de plugin peut inclure un `package.json` avec `openclaw.extensions` :

```json
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"],
    "setupEntry": "./src/setup-entry.ts"
  }
}
```

Chaque entrée devient un plugin. Si le pack liste plusieurs extensions, l'identifiant du plugin devient `name/<fileBase>`.

Si votre plugin importe des dépendances npm, installez-les dans ce répertoire pour que `node_modules` soit disponible (`npm install` / `pnpm install`).

Garde-fou de sécurité : chaque entrée `openclaw.extensions` doit rester à l'intérieur du répertoire du plugin après résolution des liens symboliques. Les entrées qui s'échappent du répertoire du paquet sont rejetées.

Note de sécurité : `openclaw plugins install` installe les dépendances du plugin avec `npm install --ignore-scripts` (pas de scripts de cycle de vie). Gardez les arbres de dépendances du plugin « pur JS/TS » et évitez les paquets qui nécessitent des constructions `postinstall`.

Optionnel : `openclaw.setupEntry` peut pointer vers un module léger réservé à la configuration.
Quand OpenClaw a besoin de surfaces de configuration pour un plugin de canal désactivé, ou quand un plugin de canal est activé mais toujours non configuré, il charge `setupEntry` au lieu de l'entrée complète du plugin. Cela allège le démarrage et la configuration quand votre entrée de plugin principal câble aussi des outils, des hooks, ou d'autres codes réservés à l'exécution.

Optionnel : `openclaw.startup.deferConfiguredChannelFullLoadUntilAfterListen` peut opter un plugin de canal dans le même chemin `setupEntry` pendant la phase de démarrage pré-écoute de la passerelle, même quand le canal est déjà configuré.

Utilisez ceci uniquement quand `setupEntry` couvre complètement la surface de démarrage qui doit exister avant que la passerelle commence à écouter. En pratique, cela signifie que l'entrée de configuration doit enregistrer chaque capacité détenue par le canal dont le démarrage dépend, telle que :

- l'enregistrement du canal lui-même
- toutes les routes HTTP qui doivent être disponibles avant que la passerelle commence à écouter
- toutes les méthodes de passerelle, outils, ou services qui doivent exister pendant cette même fenêtre

Si votre entrée complète possède toujours une capacité de démarrage requise, n'activez pas cet indicateur. Gardez le plugin sur le comportement par défaut et laissez OpenClaw charger l'entrée complète pendant le démarrage.

Exemple :

```json
{
  "name": "@scope/my-channel",
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "startup": {
      "deferConfiguredChannelFullLoadUntilAfterListen": true
    }
  }
}
```

### Métadonnées du catalogue de canaux

Les plugins de canal peuvent annoncer les métadonnées de configuration/découverte via `openclaw.channel` et les indices d'installation via `openclaw.install`. Cela garde les données du catalogue libres du noyau.

Exemple :

```json
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "extensions": ["./index.ts"],
    "channel": {
      "id": "nextcloud-talk",
      "label": "Nextcloud Talk",
      "selectionLabel": "Nextcloud Talk (self-hosted)",
      "docsPath": "/channels/nextcloud-talk",
      "docsLabel": "nextcloud-talk",
      "blurb": "Self-hosted chat via Nextcloud Talk webhook bots.",
      "order": 65,
      "aliases": ["nc-talk", "nc"]
    },
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "extensions/nextcloud-talk",
      "defaultChoice": "npm"
    }
  }
}
```

OpenClaw peut aussi fusionner des **catalogues de canaux externes** (par exemple, une exportation de registre MPM). Déposez un fichier JSON à l'un de :

- `~/.openclaw/mpm/plugins.json`
- `~/.openclaw/mpm/catalog.json`
- `~/.openclaw/plugins/catalog.json`

Ou pointez `OPENCLAW_PLUGIN_CATALOG_PATHS` (ou `OPENCLAW_MPM_CATALOG_PATHS`) vers un ou plusieurs fichiers JSON (délimités par virgule/point-virgule/`PATH`). Chaque fichier doit contenir `{ "entries": [ { "name": "@scope/pkg", "openclaw": { "channel": {...}, "install": {...} } } ] }`.

## Plugins du moteur de contexte

Les plugins du moteur de contexte possèdent l'orchestration du contexte de session pour l'ingestion, l'assemblage et la compaction. Enregistrez-les depuis votre plugin avec `api.registerContextEngine(id, factory)`, puis sélectionnez le moteur actif avec `plugins.slots.contextEngine`.

Utilisez ceci quand votre plugin a besoin de remplacer ou d'étendre le pipeline de contexte par défaut plutôt que juste d'ajouter une recherche de mémoire ou des hooks.

```ts
export default function (api) {
  api.registerContextEngine("lossless-claw", () => ({
    info: { id: "lossless-claw", name: "Lossless Claw", ownsCompaction: true },
    async ingest() {
      return { ingested: true };
    },
    async assemble({ messages }) {
      return { messages, estimatedTokens: 0 };
    },
    async compact() {
      return { ok: true, compacted: false };
    },
  }));
}
```

Si votre moteur ne possède **pas** l'algorithme de compaction, gardez `compact()` implémenté et déléguez-le explicitement :

```ts
import { delegateCompactionToRuntime } from "openclaw/plugin-sdk/core";

export default function (api) {
  api.registerContextEngine("my-memory-engine", () => ({
    info: {
      id: "my-memory-engine",
      name: "My Memory Engine",
      ownsCompaction: false,
    },
    async ingest() {
      return { ingested: true };
    },
    async assemble({ messages }) {
      return { messages, estimatedTokens: 0 };
    },
    async compact(params) {
      return await delegateCompactionToRuntime(params);
    },
  }));
}
```

## Ajouter une nouvelle capacité

Quand un plugin a besoin d'un comportement qui ne correspond pas à l'API actuelle, ne contournez pas le système de plugin avec une intrusion privée. Ajoutez la capacité manquante.

Séquence recommandée :

1. définir le contrat principal
   Décidez quel comportement partagé le noyau doit posséder : politique, repli, fusion de configuration, cycle de vie, sémantique face au canal, et forme d'assistant d'exécution.
2. ajouter des surfaces de plugin typées d'enregistrement/exécution
   Étendez `OpenClawPluginApi` et/ou `api.runtime` avec la plus petite surface de capacité typée utile.
3. câbler les consommateurs noyau + canal/fonctionnalité
   Les canaux et plugins de fonctionnalité doivent consommer la nouvelle capacité via le noyau, pas en important directement une implémentation de fournisseur.
4. enregistrer les implémentations de fournisseur
   Les plugins de fournisseur enregistrent ensuite leurs backends par rapport à la capacité.
5. ajouter la couverture du contrat
   Ajoutez des tests pour que la propriété et la forme d'enregistrement restent explicites au fil du temps.

C'est ainsi qu'OpenClaw reste opinionné sans devenir codé en dur pour la vision du monde d'un seul fournisseur. Voir le [Capability Cookbook](/fr/tools/capability-cookbook) pour une liste de fichiers concrète et un exemple travaillé.

### Liste de contrôle des capacités

Quand vous ajoutez une nouvelle capacité, l'implémentation doit généralement toucher ces surfaces ensemble :

- types de contrat principal dans `src/<capability>/types.ts`
- assistant d'exécution/runtime principal dans `src/<capability>/runtime.ts`
- surface d'enregistrement d'API de plugin dans `src/plugins/types.ts`
- câblage du registre de plugin dans `src/plugins/registry.ts`
- exposition d'exécution de plugin dans `src/plugins/runtime/*` quand les plugins de fonctionnalité/canal ont besoin de la consommer
- assistants de capture/test dans `src/test-utils/plugin-registration.ts`
- assertions de propriété/contrat dans `src/plugins/contracts/registry.ts`
- docs d'opérateur/plugin dans `docs/`

Si l'une de ces surfaces manque, c'est généralement un signe que la capacité n'est pas encore complètement intégrée.

### Modèle de capacité

Motif minimal :

```ts
// contrat principal
export type VideoGenerationProviderPlugin = {
  id: string;
  label: string;
  generateVideo: (req: VideoGenerationRequest) => Promise<VideoGenerationResult>;
};

// API de plugin
api.registerVideoGenerationProvider({
  id: "openai",
  label: "OpenAI",
  async generateVideo(req) {
    return await generateOpenAiVideo(req);
  },
});

// assistant d'exécution partagé pour les plugins de fonctionnalité/canal
const clip = await api.runtime.videoGeneration.generateFile({
  prompt: "Show the robot walking through the lab.",
  cfg,
});
```

Motif de test de contrat :

```ts
expect(findVideoGenerationProviderIdsForPlugin("openai")).toEqual(["openai"]);
```

Cela garde la règle simple :

- le noyau possède le contrat de capacité + orchestration
- les plugins de fournisseur possèdent les implémentations de fournisseur
- les plugins de fonctionnalité/canal consomment les assistants d'exécution
- les tests de contrat gardent la propriété explicite
