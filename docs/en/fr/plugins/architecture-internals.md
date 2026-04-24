---
summary: "Internes de l'architecture des plugins : pipeline de chargement, registre, hooks d'exécution, routes HTTP et tables de référence"
read_when:
  - Implementing provider runtime hooks, channel lifecycle, or package packs
  - Debugging plugin load order or registry state
  - Adding a new plugin capability or context engine plugin
title: "Internes de l'architecture des plugins"
---

Pour le modèle de capacité public, les formes de plugins et les contrats de propriété/exécution, voir [Architecture des plugins](/fr/plugins/architecture). Cette page est la référence pour la mécanique interne : pipeline de chargement, registre, hooks d'exécution, routes HTTP Gateway, chemins d'importation et tables de schéma.

## Pipeline de chargement

Au démarrage, OpenClaw fait à peu près ceci :

1. découvrir les racines de plugins candidates
2. lire les manifestes de bundles natifs ou compatibles et les métadonnées de paquets
3. rejeter les candidats non sécurisés
4. normaliser la configuration des plugins (`plugins.enabled`, `allow`, `deny`, `entries`,
   `slots`, `load.paths`)
5. décider de l'activation pour chaque candidat
6. charger les modules natifs activés : les modules bundlés construits utilisent un chargeur natif ;
   les plugins natifs non construits utilisent jiti
7. appeler les hooks natifs `register(api)` et collecter les enregistrements dans le registre des plugins
8. exposer le registre aux surfaces de commandes/runtime

<Note>
`activate` est un alias hérité pour `register` — le chargeur résout lequel est présent (`def.register ?? def.activate`) et l'appelle au même point. Tous les plugins bundlés utilisent `register` ; préférez `register` pour les nouveaux plugins.
</Note>

Les portes de sécurité se produisent **avant** l'exécution du runtime. Les candidats sont bloqués
lorsque l'entrée s'échappe de la racine du plugin, le chemin est accessible en écriture au monde, ou la propriété du chemin semble suspecte pour les plugins non bundlés.

### Comportement basé sur le manifeste

Le manifeste est la source de vérité du plan de contrôle. OpenClaw l'utilise pour :

- identifier le plugin
- découvrir les canaux/compétences/schéma de configuration déclarés ou les capacités du bundle
- valider `plugins.entries.<id>.config`
- augmenter les étiquettes/espaces réservés de l'interface utilisateur de contrôle
- afficher les métadonnées d'installation/catalogue
- préserver les descripteurs d'activation et de configuration bon marché sans charger le runtime du plugin

Pour les plugins natifs, le module runtime est la partie du plan de données. Il enregistre
le comportement réel tel que les hooks, les outils, les commandes ou les flux de fournisseurs.

Les blocs optionnels `activation` et `setup` du manifeste restent sur le plan de contrôle.
Ce sont des descripteurs de métadonnées uniquement pour la planification d'activation et la découverte de configuration ;
ils ne remplacent pas l'enregistrement du runtime, `register(...)` ou `setupEntry`.
Les premiers consommateurs d'activation en direct utilisent maintenant les indices de commande, canal et fournisseur du manifeste
pour réduire le chargement des plugins avant une matérialisation plus large du registre :

- le chargement CLI se réduit aux plugins qui possèdent la commande primaire demandée
- la configuration du canal/résolution des plugins se réduit aux plugins qui possèdent l'ID de
  canal demandé
- la configuration/résolution du runtime du fournisseur explicite se réduit aux plugins qui possèdent l'ID de
  fournisseur demandé

Le planificateur d'activation expose à la fois une API d'IDs uniquement pour les appelants existants et une
API de plan pour les nouveaux diagnostics. Les entrées du plan rapportent pourquoi un plugin a été sélectionné,
en séparant les indices du planificateur `activation.*` explicites de la propriété du manifeste
fallback telle que `providers`, `channels`, `commandAliases`, `setup.providers`,
`contracts.tools` et hooks. Cette séparation de raison est la limite de compatibilité :
les métadonnées de plugin existantes continuent de fonctionner, tandis que le nouveau code peut détecter des indices larges
ou un comportement fallback sans modifier la sémantique de chargement du runtime.

La découverte de configuration préfère maintenant les IDs possédés par le descripteur tels que `setup.providers` et
`setup.cliBackends` pour réduire les plugins candidats avant de revenir à
`setup-api` pour les plugins qui ont encore besoin de hooks d'exécution au moment de la configuration. Si plus d'un
plugin découvert revendique le même ID de fournisseur de configuration ou de backend CLI normalisé,
la recherche de configuration refuse le propriétaire ambigu au lieu de s'appuyer sur l'ordre de découverte.

### Ce que le chargeur met en cache

OpenClaw conserve des caches courts en processus pour :

- les résultats de découverte
- les données du registre du manifeste
- les registres de plugins chargés

Ces caches réduisent le démarrage en rafales et la surcharge de commandes répétées. Ils sont sûrs
à considérer comme des caches de performance à courte durée de vie, pas de persistance.

Note de performance :

- Définissez `OPENCLAW_DISABLE_PLUGIN_DISCOVERY_CACHE=1` ou
  `OPENCLAW_DISABLE_PLUGIN_MANIFEST_CACHE=1` pour désactiver ces caches.
- Ajustez les fenêtres de cache avec `OPENCLAW_PLUGIN_DISCOVERY_CACHE_MS` et
  `OPENCLAW_PLUGIN_MANIFEST_CACHE_MS`.

## Modèle de registre

Les plugins chargés ne mutent pas directement les globals aléatoires du noyau. Ils s'enregistrent dans un
registre de plugins central.

Le registre suit :

- les enregistrements de plugins (identité, source, origine, statut, diagnostics)
- les outils
- les hooks hérités et les hooks typés
- les canaux
- les fournisseurs
- les gestionnaires RPC de la passerelle
- les routes HTTP
- les enregistreurs CLI
- les services en arrière-plan
- les commandes possédées par les plugins

Les fonctionnalités principales lisent ensuite à partir de ce registre au lieu de parler directement aux modules de plugins.
Cela maintient le chargement unidirectionnel :

- module de plugin -> enregistrement du registre
- runtime principal -> consommation du registre

Cette séparation est importante pour la maintenabilité. Cela signifie que la plupart des surfaces principales n'ont besoin que d'un
point d'intégration : « lire le registre », pas « cas spécial pour chaque module de plugin ».

## Rappels de liaison de conversation

Les plugins qui lient une conversation peuvent réagir lorsqu'une approbation est résolue.

Utilisez `api.onConversationBindingResolved(...)` pour recevoir un rappel après qu'une demande de liaison
soit approuvée ou refusée :

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
- `decision` : `"allow-once"`, `"allow-always"` ou `"deny"`
- `binding` : la liaison résolue pour les demandes approuvées
- `request` : le résumé de la demande d'origine, l'indice de détachement, l'ID de l'expéditeur et
  les métadonnées de conversation

Ce rappel est une notification uniquement. Il ne change pas qui est autorisé à lier une
conversation, et il s'exécute après la fin de la gestion d'approbation du noyau.

## Crochets d'exécution du fournisseur

Les plugins de fournisseur ont trois couches :

- **Métadonnées du manifeste** pour une recherche bon marché avant l'exécution : `providerAuthEnvVars`,
  `providerAuthAliases`, `providerAuthChoices`, et `channelEnvVars`.
- **Crochets au moment de la configuration** : `catalog` (ancien `discovery`) plus
  `applyConfigDefaults`.
- **Crochets d'exécution** : 40+ crochets optionnels couvrant l'authentification, la résolution de modèle,
  l'enveloppe de flux, les niveaux de réflexion, la politique de relecture, et les points de terminaison d'utilisation. Voir
  la liste complète sous [Ordre et utilisation des crochets](#hook-order-and-usage).

OpenClaw conserve toujours la boucle d'agent générique, le basculement, la gestion des transcriptions, et
la politique d'outils. Ces crochets constituent la surface d'extension pour le comportement spécifique au fournisseur
sans avoir besoin d'un transport d'inférence personnalisé complet.

Utilisez le manifeste `providerAuthEnvVars` lorsque le fournisseur a des identifiants basés sur l'environnement
que les chemins d'authentification/statut/sélecteur de modèle génériques doivent voir sans charger le plugin
d'exécution. Utilisez le manifeste `providerAuthAliases` lorsqu'un ID de fournisseur doit réutiliser
les variables d'environnement, les profils d'authentification, l'authentification soutenue par la configuration, et le choix d'intégration de clé API d'un autre ID de fournisseur. Utilisez le manifeste `providerAuthChoices` lorsque les surfaces CLI d'intégration/choix d'authentification
doivent connaître l'ID de choix du fournisseur, les étiquettes de groupe, et le câblage d'authentification simple à un drapeau
sans charger le plugin d'exécution du fournisseur. Conservez le `envVars` d'exécution du fournisseur
pour les indices destinés à l'opérateur, tels que les étiquettes d'intégration ou les variables de configuration du client OAuth
client-id/client-secret.

Utilisez le manifeste `channelEnvVars` lorsqu'un canal a une authentification ou une configuration basées sur l'environnement que
le secours shell-env générique, les vérifications de configuration/statut, ou les invites de configuration doivent voir
sans charger le plugin d'exécution du canal.

### Ordre et utilisation des crochets

Pour les plugins de modèle/fournisseur, OpenClaw appelle les crochets dans cet ordre approximatif.
La colonne « Quand l'utiliser » est le guide de décision rapide.

| #   | Crochet                           | Ce qu'il fait                                                                                                  | Quand l'utiliser                                                                                                                              |
| --- | --------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `catalog`                         | Publier la configuration du fournisseur dans `models.providers` lors de la génération de `models.json`         | Le fournisseur possède un catalogue ou des valeurs par défaut d'URL de base                                                                   |
| 2   | `applyConfigDefaults`             | Appliquer les valeurs par défaut de configuration globale détenues par le fournisseur lors de la matérialisation de la configuration | Les valeurs par défaut dépendent du mode d'authentification, de l'environnement, ou de la sémantique de la famille de modèles du fournisseur |
| --  | _(recherche de modèle intégrée)_  | OpenClaw essaie d'abord le chemin normal du registre/catalogue                                                 | _(pas un crochet de plugin)_                                                                                                                 |
| 3   | `normalizeModelId`                | Normaliser les alias d'ID de modèle hérités ou en aperçu avant la recherche                                    | Le fournisseur possède le nettoyage des alias avant la résolution du modèle canonique                                                        |
| 4   | `normalizeTransport`              | Normaliser l'`api` / `baseUrl` spécifique à la famille de fournisseurs avant l'assemblage du modèle générique   | Le fournisseur possède le nettoyage du transport pour les ID de fournisseur personnalisés dans la même famille de transport                 |
| 5   | `normalizeConfig`                 | Normaliser `models.providers.<id>` avant la résolution d'exécution/fournisseur                                  | Le fournisseur a besoin du nettoyage de la configuration qui devrait vivre avec le plugin ; les assistants Google intégrés soutiennent également les entrées de configuration Google prises en charge |
| 6   | `applyNativeStreamingUsageCompat` | Appliquer les réécritures de compatibilité d'utilisation de flux natif aux fournisseurs de configuration        | Le fournisseur a besoin de correctifs de métadonnées d'utilisation de flux natif basés sur le point de terminaison                           |
| 7   | `resolveConfigApiKey`             | Résoudre l'authentification marquée par env pour les fournisseurs de configuration avant le chargement d'authentification d'exécution | Le fournisseur a une résolution de clé API marquée par env détenue par le fournisseur ; `amazon-bedrock` a également un résolveur AWS marqué par env intégré ici |
| 8   | `resolveSyntheticAuth`            | Surface d'authentification locale/auto-hébergée ou soutenue par la configuration sans persister le texte brut   | Le fournisseur peut fonctionner avec un marqueur d'identifiant synthétique/local                                                             |
| 9   | `resolveExternalAuthProfiles`     | Superposer les profils d'authentification externe détenus par le fournisseur ; la `persistence` par défaut est `runtime-only` pour les identifiants détenus par CLI/app | Le fournisseur réutilise les identifiants d'authentification externe sans persister les jetons d'actualisation copiés ; déclarez `contracts.externalAuthProviders` dans le manifeste |
| 10  | `shouldDeferSyntheticProfileAuth` | Abaisser les espaces réservés de profil synthétique stockés derrière l'authentification soutenue par env/configuration | Le fournisseur stocke les profils d'espace réservé synthétique qui ne doivent pas gagner la priorité                                         |
| 11  | `resolveDynamicModel`             | Secours synchrone pour les ID de modèle détenus par le fournisseur pas encore dans le registre local            | Le fournisseur accepte les ID de modèle en amont arbitraires                                                                                  |
| 12  | `prepareDynamicModel`             | Échauffement asynchrone, puis `resolveDynamicModel` s'exécute à nouveau                                         | Le fournisseur a besoin de métadonnées réseau avant de résoudre les ID inconnus                                                              |
| 13  | `normalizeResolvedModel`          | Réécriture finale avant que le coureur intégré utilise le modèle résolu                                         | Le fournisseur a besoin de réécritures de transport mais utilise toujours un transport principal                                             |
| 14  | `contributeResolvedModelCompat`   | Contribuer les drapeaux de compatibilité pour les modèles de fournisseur derrière un autre transport compatible | Le fournisseur reconnaît ses propres modèles sur les transports proxy sans prendre en charge le fournisseur                                  |
| 15  | `capabilities`                    | Métadonnées de transcription/outillage détenues par le fournisseur utilisées par la logique principale partagée  | Le fournisseur a besoin de bizarreries de transcription/famille de fournisseur                                                               |
| 16  | `normalizeToolSchemas`            | Normaliser les schémas d'outils avant que le coureur intégré les voie                                           | Le fournisseur a besoin du nettoyage du schéma spécifique à la famille de transport                                                         |
| 17  | `inspectToolSchemas`              | Surface des diagnostics de schéma détenus par le fournisseur après normalisation                                | Le fournisseur veut des avertissements de mot-clé sans enseigner les règles spécifiques au fournisseur principal                             |
| 18  | `resolveReasoningOutputMode`      | Sélectionner le contrat de sortie de raisonnement natif ou étiqueté                                             | Le fournisseur a besoin du raisonnement étiqueté/sortie finale au lieu des champs natifs                                                     |
| 19  | `prepareExtraParams`              | Normalisation des paramètres de requête avant les enveloppes d'option de flux génériques                        | Le fournisseur a besoin de paramètres de requête par défaut ou du nettoyage des paramètres par fournisseur                                  |
| 20  | `createStreamFn`                  | Remplacer complètement le chemin de flux normal par un transport personnalisé                                   | Le fournisseur a besoin d'un protocole de fil personnalisé, pas seulement une enveloppe                                                      |
| 21  | `wrapStreamFn`                    | Enveloppe de flux après l'application des enveloppes génériques                                                 | Le fournisseur a besoin des enveloppes de compatibilité d'en-têtes/corps/modèle de requête sans transport personnalisé                      |
| 22  | `resolveTransportTurnState`       | Attacher les en-têtes ou métadonnées de transport natifs par tour                                               | Le fournisseur veut que les transports génériques envoient l'identité de tour native du fournisseur                                          |
| 23  | `resolveWebSocketSessionPolicy`   | Attacher les en-têtes WebSocket natifs ou la politique de refroidissement de session                            | Le fournisseur veut que les transports WS génériques accordent les en-têtes de session ou la politique de secours                            |
| 24  | `formatApiKey`                    | Formateur de profil d'authentification : le profil stocké devient la chaîne `apiKey` d'exécution               | Le fournisseur stocke les métadonnées d'authentification supplémentaires et a besoin d'une forme de jeton d'exécution personnalisée           |
| 25  | `refreshOAuth`                    | Remplacement d'actualisation OAuth pour les points de terminaison d'actualisation personnalisés ou la politique d'échec d'actualisation | Le fournisseur ne s'adapte pas aux actualisateurs `pi-ai` partagés                                                                          |
| 26  | `buildAuthDoctorHint`             | Conseil de réparation ajouté lorsque l'actualisation OAuth échoue                                              | Le fournisseur a besoin des conseils de réparation d'authentification détenus par le fournisseur après l'échec d'actualisation               |
| 27  | `matchesContextOverflowError`     | Correspondance de débordement de fenêtre contextuelle détenue par le fournisseur                                | Le fournisseur a des erreurs de débordement brutes que les heuristiques génériques manqueraient                                              |
| 28  | `classifyFailoverReason`          | Classification de la raison du basculement détenue par le fournisseur                                           | Le fournisseur peut mapper les erreurs API/transport brutes à limite de débit/surcharge/etc                                                  |
| 29  | `isCacheTtlEligible`              | Politique de cache de requête pour les fournisseurs proxy/backhaul                                              | Le fournisseur a besoin de la limitation TTL du cache spécifique au proxy                                                                    |
| 30  | `buildMissingAuthMessage`         | Remplacement du message de récupération d'authentification manquante générique                                   | Le fournisseur a besoin d'un conseil de récupération d'authentification manquante spécifique au fournisseur                                  |
| 31  | `suppressBuiltInModel`            | Suppression du modèle en amont obsolète plus conseil d'erreur optionnel destiné à l'utilisateur                 | Le fournisseur a besoin de masquer les lignes en amont obsolètes ou de les remplacer par un conseil du fournisseur                          |
| 32  | `augmentModelCatalog`             | Lignes de catalogue synthétique/final ajoutées après la découverte                                              | Le fournisseur a besoin de lignes de compatibilité directe dans `models list` et les sélecteurs                                             |
| 33  | `resolveThinkingProfile`          | Ensemble de niveau `/think` spécifique au modèle, étiquettes d'affichage, et défaut                             | Le fournisseur expose une échelle de réflexion personnalisée ou une étiquette binaire pour les modèles sélectionnés                          |
| 34  | `isBinaryThinking`                | Crochet de compatibilité de basculement de raisonnement activé/désactivé                                        | Le fournisseur expose uniquement le raisonnement binaire activé/désactivé                                                                    |
| 35  | `supportsXHighThinking`           | Crochet de compatibilité de support de raisonnement `xhigh`                                                     | Le fournisseur veut `xhigh` sur seulement un sous-ensemble de modèles                                                                        |
| 36  | `resolveDefaultThinkingLevel`     | Crochet de compatibilité du niveau `/think` par défaut                                                          | Le fournisseur possède la politique `/think` par défaut pour une famille de modèles                                                          |
| 37  | `isModernModelRef`                | Correspondance de modèle moderne pour les filtres de profil en direct et la sélection de fumée                  | Le fournisseur possède la correspondance de modèle préféré en direct/fumée                                                                    |
| 38  | `prepareRuntimeAuth`              | Échanger un identifiant configuré contre le jeton/clé d'exécution réel juste avant l'inférence                 | Le fournisseur a besoin d'un échange de jeton ou d'un identifiant de requête à courte durée de vie                                          |
| 39  | `resolveUsageAuth`                | Résoudre les identifiants d'utilisation/facturation pour les surfaces `/usage` et connexes                      | Le fournisseur a besoin d'une analyse de jeton d'utilisation/quota personnalisée ou d'un identifiant d'utilisation différent                 |
| 40  | `fetchUsageSnapshot`              | Récupérer et normaliser les instantanés d'utilisation/quota spécifiques au fournisseur après la résolution de l'authentification | Le fournisseur a besoin d'un point de terminaison d'utilisation spécifique au fournisseur ou d'un analyseur de charge utile                 |
| 41  | `createEmbeddingProvider`         | Construire un adaptateur d'intégration détenu par le fournisseur pour la mémoire/recherche                      | Le comportement d'intégration de mémoire appartient au plugin du fournisseur                                                                 |
| 42  | `buildReplayPolicy`               | Retourner une politique de relecture contrôlant la gestion des transcriptions pour le fournisseur               | Le fournisseur a besoin d'une politique de transcription personnalisée (par exemple, suppression de bloc de réflexion)                      |
| 43  | `sanitizeReplayHistory`           | Réécrire l'historique de relecture après le nettoyage de transcription générique                                | Le fournisseur a besoin de réécritures de relecture spécifiques au fournisseur au-delà des assistants de compaction partagés                |
| 44  | `validateReplayTurns`             | Validation ou remodelage final du tour de relecture avant le coureur intégré                                    | Le transport du fournisseur a besoin d'une validation de tour plus stricte après l'assainissement générique                                 |
| 45  | `onModelSelected`                 | Exécuter les effets secondaires post-sélection détenus par le fournisseur                                       | Le fournisseur a besoin de télémétrie ou d'état détenu par le fournisseur lorsqu'un modèle devient actif                                    |

`normalizeModelId`, `normalizeTransport`, et `normalizeConfig` vérifient d'abord le
plugin de fournisseur correspondant, puis passent par d'autres plugins de fournisseur capables de crochets
jusqu'à ce que l'un change réellement l'ID de modèle ou le transport/configuration. Cela maintient
les shims de fournisseur d'alias/compatibilité fonctionnant sans exiger que l'appelant sache quel
plugin intégré possède la réécriture. Si aucun crochet de fournisseur ne réécrit une entrée de configuration Google prise en charge,
le normalisateur de configuration Google intégré applique toujours ce nettoyage de compatibilité.

Si le fournisseur a besoin d'un protocole de fil entièrement personnalisé ou d'un exécuteur de requête personnalisé,
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

Les plugins de fournisseur intégrés combinent les crochets ci-dessus pour s'adapter au catalogue, à l'authentification, à la réflexion, à la relecture, et aux besoins d'utilisation de chaque fournisseur. L'ensemble de crochets faisant autorité vit avec
chaque plugin sous `extensions/` ; cette page illustre les formes plutôt que de refléter la liste.

<AccordionGroup>
  <Accordion title="Fournisseurs de catalogue de transmission directe">
    OpenRouter, Kilocode, Z.AI, xAI enregistrent `catalog` plus
    `resolveDynamicModel` / `prepareDynamicModel` afin qu'ils puissent afficher les ID de modèle en amont avant le catalogue statique d'OpenClaw.
  </Accordion>
  <Accordion title="Fournisseurs de point de terminaison OAuth et d'utilisation">
    GitHub Copilot, Gemini CLI, ChatGPT Codex, MiniMax, Xiaomi, z.ai associent
    `prepareRuntimeAuth` ou `formatApiKey` avec `resolveUsageAuth` +
    `fetchUsageSnapshot` pour posséder l'échange de jeton et l'intégration `/usage`.
  </Accordion>
  <Accordion title="Familles de nettoyage de relecture et de transcription">
    Les familles nommées partagées (`google-gemini`, `passthrough-gemini`,
    `anthropic-by-model`, `hybrid-anthropic-openai`) permettent aux fournisseurs d'opter pour la politique de transcription via `buildReplayPolicy` au lieu que chaque plugin
    réimplémente le nettoyage.
  </Accordion>
  <Accordion title="Fournisseurs de catalogue uniquement">
    `byteplus`, `cloudflare-ai-gateway`, `huggingface`, `kimi-coding`, `nvidia`,
    `qianfan`, `synthetic`, `together`, `venice`, `vercel-ai-gateway`, et
    `volcengine` enregistrent juste `catalog` et utilisent la boucle d'inférence partagée.
  </Accordion>
  <Accordion title="Assistants de flux spécifiques à Anthropic">
    Les en-têtes bêta, `/fast` / `serviceTier`, et `context1m` vivent à l'intérieur de la
    couture publique du plugin Anthropic `api.ts` / `contract-api.ts`
    (`wrapAnthropicProviderStream`, `resolveAnthropicBetas`,
    `resolveAnthropicFastMode`, `resolveAnthropicServiceTier`) plutôt que dans
    le SDK générique.
  </Accordion>
</AccordionGroup>

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

- `textToSpeech` retourne la charge utile de sortie TTS principale normale pour les surfaces de fichier/note vocale.
- Utilise la configuration principale `messages.tts` et la sélection du fournisseur.
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

- Conservez la politique TTS, le secours et la livraison des réponses dans le cœur.
- Utilisez les fournisseurs de parole pour le comportement de synthèse propriétaire du fournisseur.
- L'entrée Microsoft `edge` héritée est normalisée vers l'ID de fournisseur `microsoft`.
- Le modèle de propriété préféré est orienté vers l'entreprise : un plugin de fournisseur peut posséder les fournisseurs de texte, de parole, d'image et de futurs médias à mesure qu'OpenClaw ajoute ces contrats de capacité.

Pour la compréhension d'image/audio/vidéo, les plugins enregistrent un fournisseur de compréhension de média typé unique au lieu d'un sac générique clé/valeur :

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

- Conservez l'orchestration, le secours, la configuration et le câblage des canaux dans le cœur.
- Conservez le comportement du fournisseur dans le plugin du fournisseur.
- L'expansion additive doit rester typée : nouvelles méthodes optionnelles, nouveaux champs de résultat optionnels, nouvelles capacités optionnelles.
- La génération vidéo suit déjà le même modèle :
  - le cœur possède le contrat de capacité et l'assistant d'exécution
  - les plugins de fournisseur enregistrent `api.registerVideoGenerationProvider(...)`
  - les plugins de fonctionnalité/canal consomment `api.runtime.videoGeneration.*`

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
- Utilise la configuration audio de compréhension de média principale (`tools.media.audio`) et l'ordre de secours du fournisseur.
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
- Pour les exécutions de secours détenues par le plugin, les opérateurs doivent accepter avec `plugins.entries.<id>.subagent.allowModelOverride: true`.
- Utilisez `plugins.entries.<id>.subagent.allowedModels` pour restreindre les plugins de confiance à des cibles `provider/model` canoniques spécifiques, ou `"*"` pour autoriser explicitement n'importe quelle cible.
- Les exécutions de sous-agent de plugin non fiables fonctionnent toujours, mais les demandes de remplacement sont rejetées au lieu de revenir silencieusement.

Pour la recherche web, les plugins peuvent consommer l'assistant d'exécution partagé au lieu d'accéder au câblage de l'outil agent :

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

- Conservez la sélection du fournisseur, la résolution des identifiants et la sémantique des demandes partagées dans le cœur.
- Utilisez les fournisseurs de recherche web pour les transports de recherche spécifiques au fournisseur.
- `api.runtime.webSearch.*` est la surface partagée préférée pour les plugins de fonctionnalité/canal qui ont besoin d'un comportement de recherche sans dépendre du wrapper d'outil agent.

### `api.runtime.imageGeneration`

```ts
const result = await api.runtime.imageGeneration.generate({
  config: api.config,
  args: { prompt: "A friendly lobster mascot", size: "1024x1024" },
});

const providers = api.runtime.imageGeneration.listProviders({
  config: api.config,
});
```

- `generate(...)` : générer une image en utilisant la chaîne de fournisseur de génération d'image configurée.
- `listProviders(...)` : lister les fournisseurs de génération d'image disponibles et leurs capacités.

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

- `api.registerHttpHandler(...)` a été supprimé et causera une erreur de chargement de plugin. Utilisez `api.registerHttpRoute(...)` à la place.
- Les routes de plugin doivent déclarer `auth` explicitement.
- Les conflits exacts `path + match` sont rejetés sauf si `replaceExisting: true`, et un plugin ne peut pas remplacer la route d'un autre plugin.
- Les routes qui se chevauchent avec différents niveaux `auth` sont rejetées. Conservez les chaînes de secours `exact`/`prefix` au même niveau d'authentification uniquement.
- Les routes `auth: "plugin"` ne reçoivent **pas** automatiquement les portées d'exécution de l'opérateur. Elles sont destinées aux webhooks gérés par le plugin/vérification de signature, pas aux appels d'assistant de passerelle privilégiés.
- Les routes `auth: "gateway"` s'exécutent dans une portée d'exécution de demande de passerelle, mais cette portée est intentionnellement conservatrice :
  - l'authentification par jeton secret partagé (`gateway.auth.mode = "token"` / `"password"`) maintient les portées d'exécution de route de plugin épinglées à `operator.write`, même si l'appelant envoie `x-openclaw-scopes`
  - les modes HTTP porteurs d'identité de confiance (par exemple `trusted-proxy` ou `gateway.auth.mode = "none"` sur une entrée privée) honorent `x-openclaw-scopes` uniquement quand l'en-tête est explicitement présent
  - si `x-openclaw-scopes` est absent sur ces demandes de route de plugin porteurs d'identité, la portée d'exécution revient à `operator.write`
- Règle pratique : ne supposez pas qu'une route de plugin avec authentification de passerelle est une surface implicitement administrateur. Si votre route a besoin d'un comportement réservé à l'administrateur, exigez un mode d'authentification porteur d'identité et documentez le contrat d'en-tête `x-openclaw-scopes` explicite.

## Chemins d'importation du SDK de plugin

Utilisez des sous-chemins SDK étroits au lieu du baril monolithique `openclaw/plugin-sdk` racine lors de la création de nouveaux plugins. Sous-chemins principaux :

| Sous-chemin                         | Objectif                                           |
| ----------------------------------- | -------------------------------------------------- |
| `openclaw/plugin-sdk/plugin-entry`  | Primitives d'enregistrement de plugin              |
| `openclaw/plugin-sdk/channel-core`  | Assistants d'entrée/construction de canal          |
| `openclaw/plugin-sdk/core`          | Assistants partagés génériques et contrat parapluie |
| `openclaw/plugin-sdk/config-schema` | Schéma Zod `openclaw.json` racine (`OpenClawSchema`) |

Les plugins de canal choisissent parmi une famille de coutures étroites — `channel-setup`, `setup-runtime`, `setup-adapter-runtime`, `setup-tools`, `channel-pairing`, `channel-contract`, `channel-feedback`, `channel-inbound`, `channel-lifecycle`, `channel-reply-pipeline`, `command-auth`, `secret-input`, `webhook-ingress`, `channel-targets` et `channel-actions`. Le comportement d'approbation doit se consolider sur un contrat `approvalCapability` unique plutôt que de mélanger les champs de plugin non liés. Voir [Plugins de canal](/fr/plugins/sdk-channel-plugins).

Les assistants d'exécution et de configuration vivent sous les sous-chemins `*-runtime` correspondants (`approval-runtime`, `config-runtime`, `infra-runtime`, `agent-runtime`, `lazy-runtime`, `directory-runtime`, `text-runtime`, `runtime-store`, etc.).

<Info>
`openclaw/plugin-sdk/channel-runtime` est déprécié — un shim de compatibilité pour les plugins plus anciens. Le nouveau code doit importer des primitives génériques plus étroites à la place.
</Info>

Points d'entrée internes du dépôt (par racine de package de plugin fourni) :

- `index.js` — entrée de plugin fournie
- `api.js` — baril d'assistant/types
- `runtime-api.js` — baril d'exécution uniquement
- `setup-entry.js` — entrée de plugin de configuration

Les plugins externes ne doivent importer que les sous-chemins `openclaw/plugin-sdk/*`. N'importez jamais `src/*` d'un autre package de plugin depuis le cœur ou depuis un autre plugin. Les points d'entrée chargés par façade préfèrent l'instantané de configuration d'exécution actif quand il en existe un, puis reviennent au fichier de configuration résolu sur le disque.

Les sous-chemins spécifiques à la capacité tels que `image-generation`, `media-understanding` et `speech` existent parce que les plugins fournis les utilisent aujourd'hui. Ce ne sont pas automatiquement des contrats externes gelés à long terme — vérifiez la page de référence SDK pertinente quand vous en dépendez.

## Schémas d'outil de message

Les plugins doivent posséder les contributions de schéma `describeMessageTool(...)` spécifiques au canal pour les primitives non-message telles que les réactions, les lectures et les sondages. La présentation d'envoi partagée doit utiliser le contrat `MessagePresentation` générique au lieu des champs de bouton, composant, bloc ou carte natifs du fournisseur. Voir [Présentation de message](/fr/plugins/message-presentation) pour le contrat, les règles de secours, le mappage du fournisseur et la liste de contrôle de l'auteur du plugin.

Les plugins compatibles avec l'envoi déclarent ce qu'ils peuvent rendre via les capacités de message :

- `presentation` pour les blocs de présentation sémantique (`text`, `context`, `divider`, `buttons`, `select`)
- `delivery-pin` pour les demandes de livraison épinglée

Le cœur décide s'il faut rendre la présentation nativement ou la dégrader en texte. N'exposez pas les échappatoires d'interface utilisateur natives du fournisseur à partir de l'outil de message générique. Les assistants SDK dépréciés pour les schémas natifs hérités restent exportés pour les plugins tiers existants, mais les nouveaux plugins ne doivent pas les utiliser.

## Résolution de cible de canal

Les plugins de canal doivent posséder la sémantique de cible spécifique au canal. Gardez l'hôte sortant partagé générique et utilisez la surface de l'adaptateur de messagerie pour les règles du fournisseur :

- `messaging.inferTargetChatType({ to })` décide si une cible normalisée doit être traitée comme `direct`, `group`, ou `channel` avant la recherche dans le répertoire.
- `messaging.targetResolver.looksLikeId(raw, normalized)` indique au cœur si une entrée doit ignorer la recherche dans le répertoire et passer directement à la résolution de type id.
- `messaging.targetResolver.resolveTarget(...)` est le recours du plugin lorsque le cœur a besoin d'une résolution finale détenue par le fournisseur après normalisation ou après un manque dans le répertoire.
- `messaging.resolveOutboundSessionRoute(...)` détient la construction de route de session spécifique au fournisseur une fois qu'une cible est résolue.

Division recommandée :

- Utilisez `inferTargetChatType` pour les décisions de catégorie qui doivent se produire avant de rechercher les pairs/groupes.
- Utilisez `looksLikeId` pour les vérifications « traiter ceci comme un id de cible explicite/natif ».
- Utilisez `resolveTarget` pour le recours de normalisation spécifique au fournisseur, pas pour une large recherche dans le répertoire.
- Gardez les ids natifs du fournisseur comme les ids de chat, ids de thread, JIDs, handles et ids de salle à l'intérieur des valeurs `target` ou des paramètres spécifiques au fournisseur, pas dans les champs SDK génériques.

## Répertoires soutenus par la configuration

Les plugins qui dérivent les entrées du répertoire de la configuration doivent garder cette logique dans le plugin et réutiliser les assistants partagés de `openclaw/plugin-sdk/directory-runtime`.

Utilisez ceci lorsqu'un canal a besoin de pairs/groupes soutenus par la configuration tels que :

- pairs DM pilotés par liste blanche
- cartes de canal/groupe configurées
- recours de répertoire statique à portée de compte

Les assistants partagés dans `directory-runtime` ne gèrent que les opérations génériques :

- filtrage des requêtes
- application des limites
- assistants de déduplication/normalisation
- construction de `ChannelDirectoryEntry[]`

L'inspection de compte spécifique au canal et la normalisation d'id doivent rester dans l'implémentation du plugin.

## Catalogues de fournisseurs

Les plugins de fournisseur peuvent définir des catalogues de modèles pour l'inférence avec `registerProvider({ catalog: { run(...) { ... } } })`.

`catalog.run(...)` retourne la même forme qu'OpenClaw écrit dans `models.providers` :

- `{ provider }` pour une entrée de fournisseur
- `{ providers }` pour plusieurs entrées de fournisseur

Utilisez `catalog` lorsque le plugin détient les ids de modèle spécifiques au fournisseur, les valeurs par défaut d'URL de base, ou les métadonnées de modèle contrôlées par authentification.

`catalog.order` contrôle quand le catalogue d'un plugin se fusionne par rapport aux fournisseurs implicites intégrés d'OpenClaw :

- `simple` : fournisseurs simples pilotés par clé API ou env
- `profile` : fournisseurs qui apparaissent lorsque des profils d'authentification existent
- `paired` : fournisseurs qui synthétisent plusieurs entrées de fournisseur connexes
- `late` : dernier passage, après les autres fournisseurs implicites

Les fournisseurs ultérieurs gagnent en cas de collision de clé, donc les plugins peuvent intentionnellement remplacer une entrée de fournisseur intégrée avec le même id de fournisseur.

Compatibilité :

- `discovery` fonctionne toujours comme alias hérité
- si à la fois `catalog` et `discovery` sont enregistrés, OpenClaw utilise `catalog`

## Inspection de canal en lecture seule

Si votre plugin enregistre un canal, préférez implémenter `plugin.config.inspectAccount(cfg, accountId)` aux côtés de `resolveAccount(...)`.

Pourquoi :

- `resolveAccount(...)` est le chemin d'exécution. Il est autorisé à supposer que les identifiants sont entièrement matérialisés et peut échouer rapidement lorsque les secrets requis manquent.
- Les chemins de commande en lecture seule tels que `openclaw status`, `openclaw status --all`, `openclaw channels status`, `openclaw channels resolve`, et les flux de réparation doctor/config ne doivent pas avoir besoin de matérialiser les identifiants d'exécution juste pour décrire la configuration.

Comportement recommandé de `inspectAccount(...)` :

- Retournez uniquement l'état du compte descriptif.
- Préservez `enabled` et `configured`.
- Incluez les champs de source/statut d'identifiant lorsqu'ils sont pertinents, tels que :
  - `tokenSource`, `tokenStatus`
  - `botTokenSource`, `botTokenStatus`
  - `appTokenSource`, `appTokenStatus`
  - `signingSecretSource`, `signingSecretStatus`
- Vous n'avez pas besoin de retourner les valeurs de token brutes juste pour signaler la disponibilité en lecture seule. Retourner `tokenStatus: "available"` (et le champ source correspondant) est suffisant pour les commandes de style statut.
- Utilisez `configured_unavailable` lorsqu'un identifiant est configuré via SecretRef mais indisponible dans le chemin de commande actuel.

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

Chaque entrée devient un plugin. Si le pack liste plusieurs extensions, l'id du plugin devient `name/<fileBase>`.

Si votre plugin importe des dépendances npm, installez-les dans ce répertoire pour que `node_modules` soit disponible (`npm install` / `pnpm install`).

Garde-fou de sécurité : chaque entrée `openclaw.extensions` doit rester à l'intérieur du répertoire du plugin après résolution des symlinks. Les entrées qui s'échappent du répertoire du paquet sont rejetées.

Note de sécurité : `openclaw plugins install` installe les dépendances du plugin avec `npm install --omit=dev --ignore-scripts` (pas de scripts de cycle de vie, pas de dépendances de développement à l'exécution). Gardez les arbres de dépendances du plugin « pur JS/TS » et évitez les paquets qui nécessitent des constructions `postinstall`.

Optionnel : `openclaw.setupEntry` peut pointer vers un module léger réservé à la configuration. Lorsqu'OpenClaw a besoin de surfaces de configuration pour un plugin de canal désactivé, ou lorsqu'un plugin de canal est activé mais toujours non configuré, il charge `setupEntry` au lieu de l'entrée complète du plugin. Cela rend le démarrage et la configuration plus légers lorsque votre entrée de plugin principal câble également des outils, des hooks ou d'autres codes réservés à l'exécution.

Optionnel : `openclaw.startup.deferConfiguredChannelFullLoadUntilAfterListen` peut opter un plugin de canal dans le même chemin `setupEntry` pendant la phase de démarrage pré-écoute de la passerelle, même lorsque le canal est déjà configuré.

Utilisez ceci uniquement lorsque `setupEntry` couvre complètement la surface de démarrage qui doit exister avant que la passerelle commence à écouter. En pratique, cela signifie que l'entrée de configuration doit enregistrer chaque capacité détenue par le canal dont le démarrage dépend, telle que :

- l'enregistrement du canal lui-même
- toutes les routes HTTP qui doivent être disponibles avant que la passerelle commence à écouter
- toutes les méthodes de passerelle, outils ou services qui doivent exister pendant cette même fenêtre

Si votre entrée complète détient toujours une capacité de démarrage requise, n'activez pas cet indicateur. Gardez le plugin sur le comportement par défaut et laissez OpenClaw charger l'entrée complète au démarrage.

Les canaux groupés peuvent également publier des assistants de surface de contrat réservés à la configuration que le cœur peut consulter avant le chargement complet du runtime du canal. La surface de promotion de configuration actuelle est :

- `singleAccountKeysToMove`
- `namedAccountPromotionKeys`
- `resolveSingleAccountPromotionTarget(...)`

Le cœur utilise cette surface lorsqu'il a besoin de promouvoir une configuration de canal à compte unique hérité en `channels.<id>.accounts.*` sans charger l'entrée complète du plugin. Matrix est l'exemple groupé actuel : il déplace uniquement les clés d'authentification/bootstrap dans un compte promu nommé lorsque des comptes nommés existent déjà, et il peut préserver une clé de compte par défaut non canonique configurée au lieu de toujours créer `accounts.default`.

Ces adaptateurs de patch de configuration gardent la découverte de surface de contrat groupée paresseuse. Le temps d'importation reste léger ; la surface de promotion est chargée uniquement à la première utilisation au lieu de réentrer le démarrage du canal groupé à l'importation du module.

Lorsque ces surfaces de démarrage incluent des méthodes RPC de passerelle, gardez-les sur un préfixe spécifique au plugin. Les espaces de noms d'administrateur du cœur (`config.*`, `exec.approvals.*`, `wizard.*`, `update.*`) restent réservés et se résolvent toujours en `operator.admin`, même si un plugin demande une portée plus étroite.

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

### Métadonnées du catalogue de canal

Les plugins de canal peuvent annoncer les métadonnées de configuration/découverte via `openclaw.channel` et les indices d'installation via `openclaw.install`. Cela garde les données du catalogue du cœur libres.

Exemple :

```json
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "extensions": ["./index.ts"],
    "channel": {
      "id": "nextcloud-talk",
      "label": "Nextcloud Talk",
      "selectionLabel": "Nextcloud Talk (auto-hébergé)",
      "docsPath": "/channels/nextcloud-talk",
      "docsLabel": "nextcloud-talk",
      "blurb": "Chat auto-hébergé via les bots webhook Nextcloud Talk.",
      "order": 65,
      "aliases": ["nc-talk", "nc"]
    },
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "<bundled-plugin-local-path>",
      "defaultChoice": "npm"
    }
  }
}
```

Champs `openclaw.channel` utiles au-delà de l'exemple minimal :

- `detailLabel` : étiquette secondaire pour les surfaces de catalogue/statut plus riches
- `docsLabel` : remplacer le texte du lien pour le lien de documentation
- `preferOver` : ids de plugin/canal de priorité inférieure que cette entrée de catalogue doit surclasser
- `selectionDocsPrefix`, `selectionDocsOmitLabel`, `selectionExtras` : contrôles de copie de surface de sélection
- `markdownCapable` : marque le canal comme capable de markdown pour les décisions de formatage sortant
- `exposure.configured` : masquer le canal des surfaces de liste de canal configuré lorsqu'il est défini sur `false`
- `exposure.setup` : masquer le canal des sélecteurs de configuration/configuration interactifs lorsqu'il est défini sur `false`
- `exposure.docs` : marquer le canal comme interne/privé pour les surfaces de navigation de documentation
- `showConfigured` / `showInSetup` : alias hérités toujours acceptés pour la compatibilité ; préférez `exposure`
- `quickstartAllowFrom` : opter le canal dans le flux `allowFrom` de démarrage rapide standard
- `forceAccountBinding` : exiger une liaison de compte explicite même lorsqu'un seul compte existe
- `preferSessionLookupForAnnounceTarget` : préférer la recherche de session lors de la résolution des cibles d'annonce

OpenClaw peut également fusionner les **catalogues de canal externes** (par exemple, une exportation de registre MPM). Déposez un fichier JSON à l'un de :

- `~/.openclaw/mpm/plugins.json`
- `~/.openclaw/mpm/catalog.json`
- `~/.openclaw/plugins/catalog.json`

Ou pointez `OPENCLAW_PLUGIN_CATALOG_PATHS` (ou `OPENCLAW_MPM_CATALOG_PATHS`) vers un ou plusieurs fichiers JSON (délimités par virgule/point-virgule/`PATH`). Chaque fichier doit contenir `{ "entries": [ { "name": "@scope/pkg", "openclaw": { "channel": {...}, "install": {...} } } ] }`. L'analyseur accepte également `"packages"` ou `"plugins"` comme alias hérités pour la clé `"entries"`.

Les entrées de catalogue de canal générées et les entrées de catalogue d'installation de fournisseur exposent les faits de source d'installation normalisés à côté du bloc `openclaw.install` brut. Les faits normalisés identifient si la spécification npm est une version exacte ou un sélecteur flottant, si les métadonnées d'intégrité attendues sont présentes, et si un chemin de source local est également disponible. Les consommateurs doivent traiter `installSource` comme un champ optionnel additif pour que les entrées construites à la main plus anciennes et les shims de compatibilité n'aient pas à le synthétiser. Cela permet à l'intégration et aux diagnostics d'expliquer l'état du plan source sans importer le runtime du plugin.

Les entrées npm externes officielles doivent préférer une `npmSpec` exacte plus `expectedIntegrity`. Les noms de paquets nus et les dist-tags fonctionnent toujours pour la compatibilité, mais ils exposent des avertissements du plan source pour que le catalogue puisse se diriger vers des installations épinglées et vérifiées par intégrité sans casser les plugins existants.

## Plugins de moteur de contexte

Les plugins de moteur de contexte orchestrent l'ingestion, l'assemblage et la compaction du contexte de session. Enregistrez-les depuis votre plugin avec `api.registerContextEngine(id, factory)`, puis sélectionnez le moteur actif avec `plugins.slots.contextEngine`.

Utilisez ceci quand votre plugin doit remplacer ou étendre le pipeline de contexte par défaut plutôt que simplement ajouter une recherche mémoire ou des hooks.

```ts
import { buildMemorySystemPromptAddition } from "openclaw/plugin-sdk/core";

export default function (api) {
  api.registerContextEngine("lossless-claw", () => ({
    info: { id: "lossless-claw", name: "Lossless Claw", ownsCompaction: true },
    async ingest() {
      return { ingested: true };
    },
    async assemble({ messages, availableTools, citationsMode }) {
      return {
        messages,
        estimatedTokens: 0,
        systemPromptAddition: buildMemorySystemPromptAddition({
          availableTools: availableTools ?? new Set(),
          citationsMode,
        }),
      };
    },
    async compact() {
      return { ok: true, compacted: false };
    },
  }));
}
```

Si votre moteur ne possède **pas** l'algorithme de compaction, gardez `compact()` implémenté et déléguez-le explicitement :

```ts
import {
  buildMemorySystemPromptAddition,
  delegateCompactionToRuntime,
} from "openclaw/plugin-sdk/core";

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
    async assemble({ messages, availableTools, citationsMode }) {
      return {
        messages,
        estimatedTokens: 0,
        systemPromptAddition: buildMemorySystemPromptAddition({
          availableTools: availableTools ?? new Set(),
          citationsMode,
        }),
      };
    },
    async compact(params) {
      return await delegateCompactionToRuntime(params);
    },
  }));
}
```

## Ajouter une nouvelle capacité

Quand un plugin a besoin d'un comportement qui ne correspond pas à l'API actuelle, ne contournez pas le système de plugins avec un accès privé. Ajoutez la capacité manquante.

Séquence recommandée :

1. définir le contrat principal
   Décidez quel comportement partagé le cœur doit posséder : politique, fallback, fusion de configuration, cycle de vie, sémantique côté canal et forme d'aide runtime.
2. ajouter des surfaces de plugin typées d'enregistrement/runtime
   Étendez `OpenClawPluginApi` et/ou `api.runtime` avec la plus petite surface de capacité typée utile.
3. câbler les consommateurs cœur + canal/fonctionnalité
   Les canaux et les plugins de fonctionnalité doivent consommer la nouvelle capacité via le cœur, pas en important directement une implémentation de fournisseur.
4. enregistrer les implémentations de fournisseur
   Les plugins de fournisseur enregistrent ensuite leurs backends par rapport à la capacité.
5. ajouter une couverture de contrat
   Ajoutez des tests pour que la propriété et la forme d'enregistrement restent explicites au fil du temps.

C'est ainsi qu'OpenClaw reste opinionné sans devenir codé en dur selon la vision d'un seul fournisseur. Consultez le [Capability Cookbook](/fr/tools/capability-cookbook) pour une liste de fichiers concrète et un exemple travaillé.

### Liste de contrôle des capacités

Quand vous ajoutez une nouvelle capacité, l'implémentation doit généralement toucher ces surfaces ensemble :

- types de contrat principal dans `src/<capability>/types.ts`
- aide runtime/runner principal dans `src/<capability>/runtime.ts`
- surface d'enregistrement d'API de plugin dans `src/plugins/types.ts`
- câblage du registre de plugins dans `src/plugins/registry.ts`
- exposition runtime de plugin dans `src/plugins/runtime/*` quand les plugins de fonctionnalité/canal doivent la consommer
- aides de capture/test dans `src/test-utils/plugin-registration.ts`
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

// aide runtime partagée pour les plugins de fonctionnalité/canal
const clip = await api.runtime.videoGeneration.generate({
  prompt: "Show the robot walking through the lab.",
  cfg,
});
```

Motif de test de contrat :

```ts
expect(findVideoGenerationProviderIdsForPlugin("openai")).toEqual(["openai"]);
```

Cela garde la règle simple :

- le cœur possède le contrat de capacité + orchestration
- les plugins de fournisseur possèdent les implémentations de fournisseur
- les plugins de fonctionnalité/canal consomment les aides runtime
- les tests de contrat gardent la propriété explicite

## Connexes

- [Architecture des plugins](/fr/plugins/architecture) — modèle de capacité publique et formes
- [Sous-chemins du SDK de plugin](/fr/plugins/sdk-subpaths)
- [Configuration du SDK de plugin](/fr/plugins/sdk-setup)
- [Construire des plugins](/fr/plugins/building-plugins)
