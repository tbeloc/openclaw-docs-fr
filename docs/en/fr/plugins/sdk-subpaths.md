---
summary: "Catalogue des sous-chemins du Plugin SDK : où vivent les imports, regroupés par domaine"
read_when:
  - Choisir le bon sous-chemin plugin-sdk pour un import de plugin
  - Auditer les sous-chemins bundled-plugin et les surfaces d'aide
title: "Sous-chemins du Plugin SDK"
---

Le Plugin SDK est exposé comme un ensemble de sous-chemins étroits sous `openclaw/plugin-sdk/`.
Cette page catalogue les sous-chemins couramment utilisés regroupés par objectif. La liste
complète générée de 200+ sous-chemins se trouve dans `scripts/lib/plugin-sdk-entrypoints.json` ;
les sous-chemins d'aide bundled-plugin réservés y apparaissent mais sont un détail d'implémentation
sauf si une page de documentation les promeut explicitement.

Pour le guide de création de plugins, voir [Aperçu du Plugin SDK](/fr/plugins/sdk-overview).

## Entrée du plugin

| Sous-chemin                 | Exports clés                                                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `plugin-sdk/plugin-entry`   | `definePluginEntry`                                                                                                                    |
| `plugin-sdk/core`           | `defineChannelPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase`, `defineSetupPluginEntry`, `buildChannelConfigSchema` |
| `plugin-sdk/config-schema`  | `OpenClawSchema`                                                                                                                       |
| `plugin-sdk/provider-entry` | `defineSingleProviderPluginEntry`                                                                                                      |

<AccordionGroup>
  <Accordion title="Sous-chemins de canal">
    | Sous-chemin | Exports clés |
    | --- | --- |
    | `plugin-sdk/channel-core` | `defineChannelPluginEntry`, `defineSetupPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase` |
    | `plugin-sdk/config-schema` | Export du schéma Zod racine `openclaw.json` (`OpenClawSchema`) |
    | `plugin-sdk/channel-setup` | `createOptionalChannelSetupSurface`, `createOptionalChannelSetupAdapter`, `createOptionalChannelSetupWizard`, plus `DEFAULT_ACCOUNT_ID`, `createTopLevelChannelDmPolicy`, `setSetupChannelEnabled`, `splitSetupEntries` |
    | `plugin-sdk/setup` | Assistants d'assistant de configuration partagés, invites de liste blanche, générateurs d'état de configuration |
    | `plugin-sdk/setup-runtime` | `createPatchedAccountSetupAdapter`, `createEnvPatchedAccountSetupAdapter`, `createSetupInputPresenceValidator`, `noteChannelLookupFailure`, `noteChannelLookupSummary`, `promptResolvedAllowFrom`, `splitSetupEntries`, `createAllowlistSetupWizardProxy`, `createDelegatedSetupWizardProxy` |
    | `plugin-sdk/setup-adapter-runtime` | `createEnvPatchedAccountSetupAdapter` |
    | `plugin-sdk/setup-tools` | `formatCliCommand`, `detectBinary`, `extractArchive`, `resolveBrewExecutable`, `formatDocsLink`, `CONFIG_DIR` |
    | `plugin-sdk/account-core` | Assistants de portail d'action/config multi-compte, assistants de secours de compte par défaut |
    | `plugin-sdk/account-id` | `DEFAULT_ACCOUNT_ID`, assistants de normalisation d'ID de compte |
    | `plugin-sdk/account-resolution` | Assistants de recherche de compte + secours par défaut |
    | `plugin-sdk/account-helpers` | Assistants étroits de liste de comptes/action de compte |
    | `plugin-sdk/channel-pairing` | `createChannelPairingController` |
    | `plugin-sdk/channel-reply-pipeline` | `createChannelReplyPipeline` |
    | `plugin-sdk/channel-config-helpers` | `createHybridChannelConfigAdapter` |
    | `plugin-sdk/channel-config-schema` | Types de schéma de configuration de canal |
    | `plugin-sdk/telegram-command-config` | Assistants de normalisation/validation de commande personnalisée Telegram avec secours de contrat fourni |
    | `plugin-sdk/command-gating` | Assistants étroits de portail d'autorisation de commande |
    | `plugin-sdk/channel-policy` | `resolveChannelGroupRequireMention` |
    | `plugin-sdk/channel-lifecycle` | `createAccountStatusSink`, assistants de cycle de vie/finalisation de flux de brouillon |
    | `plugin-sdk/inbound-envelope` | Assistants partagés de générateur d'enveloppe + itinéraire entrant |
    | `plugin-sdk/inbound-reply-dispatch` | Assistants partagés d'enregistrement et de distribution entrants |
    | `plugin-sdk/messaging-targets` | Assistants d'analyse/correspondance de cible |
    | `plugin-sdk/outbound-media` | Assistants partagés de chargement de média sortant |
    | `plugin-sdk/outbound-runtime` | Assistants d'identité sortante, délégué d'envoi et planification de charge utile |
    | `plugin-sdk/poll-runtime` | Assistants étroits de normalisation de sondage |
    | `plugin-sdk/thread-bindings-runtime` | Assistants de cycle de vie et d'adaptateur de liaison de fil |
    | `plugin-sdk/agent-media-payload` | Générateur de charge utile de média d'agent hérité |
    | `plugin-sdk/conversation-runtime` | Assistants de liaison de conversation/fil, d'appairage et de liaison configurée |
    | `plugin-sdk/runtime-config-snapshot` | Assistant d'instantané de configuration d'exécution |
    | `plugin-sdk/runtime-group-policy` | Assistants de résolution de politique de groupe d'exécution |
    | `plugin-sdk/channel-status` | Assistants partagés d'instantané/résumé d'état de canal |
    | `plugin-sdk/channel-config-primitives` | Primitives étroites de schéma de configuration de canal |
    | `plugin-sdk/channel-config-writes` | Assistants d'autorisation d'écriture de configuration de canal |
    | `plugin-sdk/channel-plugin-common` | Exports de prélude de plugin de canal partagés |
    | `plugin-sdk/allowlist-config-edit` | Assistants d'édition/lecture de configuration de liste blanche |
    | `plugin-sdk/group-access` | Assistants partagés de décision d'accès au groupe |
    | `plugin-sdk/direct-dm` | Assistants partagés d'authentification/garde DM direct |
    | `plugin-sdk/interactive-runtime` | Présentation de message sémantique, livraison et assistants de réponse interactive hérités. Voir [Présentation des messages](/fr/plugins/message-presentation) |
    | `plugin-sdk/channel-inbound` | Baril de compatibilité pour débounce entrant, correspondance de mention, assistants de politique de mention et assistants d'enveloppe |
    | `plugin-sdk/channel-mention-gating` | Assistants étroits de politique de mention sans la surface d'exécution entrant plus large |
    | `plugin-sdk/channel-location` | Assistants de contexte et de formatage d'emplacement de canal |
    | `plugin-sdk/channel-logging` | Assistants de journalisation de canal pour les chutes entrantes et les échecs de dactylographie/ack |
    | `plugin-sdk/channel-send-result` | Types de résultat de réponse |
    | `plugin-sdk/channel-actions` | Assistants d'action de message de canal, plus assistants de schéma natif hérités conservés pour la compatibilité des plugins |
    | `plugin-sdk/channel-targets` | Assistants d'analyse/correspondance de cible |
    | `plugin-sdk/channel-contract` | Types de contrat de canal |
    | `plugin-sdk/channel-feedback` | Câblage de rétroaction/réaction |
    | `plugin-sdk/channel-secret-runtime` | Assistants étroits de contrat secret tels que `collectSimpleChannelFieldAssignments`, `getChannelSurface`, `pushAssignment` et types de cible secret |
  </Accordion>

  <Accordion title="Sous-chemins de fournisseur">
    | Sous-chemin | Exports clés |
    | --- | --- |
    | `plugin-sdk/provider-entry` | `defineSingleProviderPluginEntry` |
    | `plugin-sdk/provider-setup` | Assistants de configuration de fournisseur local/auto-hébergé organisés |
    | `plugin-sdk/self-hosted-provider-setup` | Assistants de configuration de fournisseur auto-hébergé compatible OpenAI ciblés |
    | `plugin-sdk/cli-backend` | Valeurs par défaut du backend CLI + constantes de chien de garde |
    | `plugin-sdk/provider-auth-runtime` | Assistants de résolution de clé API d'exécution pour les plugins de fournisseur |
    | `plugin-sdk/provider-auth-api-key` | Assistants d'intégration de clé API/écriture de profil tels que `upsertApiKeyProfile` |
    | `plugin-sdk/provider-auth-result` | Générateur de résultat d'authentification OAuth standard |
    | `plugin-sdk/provider-auth-login` | Assistants de connexion interactive partagés pour les plugins de fournisseur |
    | `plugin-sdk/provider-env-vars` | Assistants de recherche de variable d'environnement d'authentification de fournisseur |
    | `plugin-sdk/provider-auth` | `createProviderApiKeyAuthMethod`, `ensureApiKeyFromOptionEnvOrPrompt`, `upsertAuthProfile`, `upsertApiKeyProfile`, `writeOAuthCredentials` |
    | `plugin-sdk/provider-model-shared` | `ProviderReplayFamily`, `buildProviderReplayFamilyHooks`, `normalizeModelCompat`, générateurs de politique de relecture partagés, assistants de point de terminaison de fournisseur et assistants de normalisation d'ID de modèle tels que `normalizeNativeXaiModelId` |
    | `plugin-sdk/provider-catalog-shared` | `findCatalogTemplate`, `buildSingleProviderApiKeyCatalog`, `supportsNativeStreamingUsageCompat`, `applyProviderNativeStreamingUsageCompat` |
    | `plugin-sdk/provider-http` | Assistants génériques de capacité HTTP/point de terminaison de fournisseur, y compris les assistants de formulaire multipart de transcription audio |
    | `plugin-sdk/provider-web-fetch-contract` | Assistants étroits de contrat de configuration/sélection de récupération Web tels que `enablePluginInConfig` et `WebFetchProviderPlugin` |
    | `plugin-sdk/provider-web-fetch` | Assistants d'enregistrement/cache de fournisseur de récupération Web |
    | `plugin-sdk/provider-web-search-config-contract` | Assistants étroits de configuration/identifiant de recherche Web pour les fournisseurs qui n'ont pas besoin de câblage d'activation de plugin |
    | `plugin-sdk/provider-web-search-contract` | Assistants étroits de contrat de configuration/identifiant de recherche Web tels que `createWebSearchProviderContractFields`, `enablePluginInConfig`, `resolveProviderWebSearchPluginConfig` et setters/getters d'identifiant délimité |
    | `plugin-sdk/provider-web-search` | Assistants d'enregistrement/cache/exécution de fournisseur de recherche Web |
    | `plugin-sdk/provider-tools` | `ProviderToolCompatFamily`, `buildProviderToolCompatFamilyHooks`, nettoyage de schéma Gemini + diagnostics et assistants de compatibilité xAI tels que `resolveXaiModelCompatPatch` / `applyXaiModelCompat` |
    | `plugin-sdk/provider-usage` | `fetchClaudeUsage` et similaires |
    | `plugin-sdk/provider-stream` | `ProviderStreamFamily`, `buildProviderStreamFamilyHooks`, `composeProviderStreamWrappers`, types d'enveloppe de flux et assistants d'enveloppe partagés Anthropic/Bedrock/Google/Kilocode/Moonshot/OpenAI/OpenRouter/Z.A.I/MiniMax/Copilot |
    | `plugin-sdk/provider-transport-runtime` | Assistants de transport de fournisseur natif tels que récupération gardée, transformations de message de transport et flux d'événements de transport inscriptibles |
    | `plugin-sdk/provider-onboard` | Assistants de correctif de configuration d'intégration |
    | `plugin-sdk/global-singleton` | Assistants de singleton/carte/cache locaux au processus |
  </Accordion>

  <Accordion title="Sous-chemins d'authentification et de sécurité">
    | Sous-chemin | Exports clés |
    | --- | --- |
    | `plugin-sdk/command-auth` | `resolveControlCommandGate`, assistants de registre de commande, assistants d'autorisation d'expéditeur |
    | `plugin-sdk/command-status` | Générateurs de message de commande/aide tels que `buildCommandsMessagePaginated` et `buildHelpMessage` |
    | `plugin-sdk/approval-auth-runtime` | Résolution d'approbateur et assistants d'authentification d'action de même chat |
    | `plugin-sdk/approval-client-runtime` | Assistants de profil/filtre d'approbation d'exécution natif |
    | `plugin-sdk/approval-delivery-runtime` | Adaptateurs natifs de capacité/livraison d'approbation |
    | `plugin-sdk/approval-gateway-runtime` | Assistant partagé de résolution de passerelle d'approbation |
    | `plugin-sdk/approval-handler-adapter-runtime` | Assistants légers de chargement d'adaptateur d'approbation natif pour les points d'entrée de canal chaud |
    | `plugin-sdk/approval-handler-runtime` | Assistants d'exécution d'approbateur plus larges ; préférez les coutures d'adaptateur/passerelle plus étroites quand elles suffisent |
    | `plugin-sdk/approval-native-runtime` | Assistants natifs de cible d'approbation + liaison de compte |
    | `plugin-sdk/approval-reply-runtime` | Assistants de charge utile de réponse d'approbation d'exécution/plugin |
    | `plugin-sdk/command-auth-native` | Authentification de commande native + assistants de cible de session natif |
    | `plugin-sdk/command-detection` | Assistants partagés de détection de commande |
    | `plugin-sdk/command-surface` | Normalisation de corps de commande et assistants de surface de commande |
    | `plugin-sdk/allow-from` | `formatAllowFromLowercase` |
    | `plugin-sdk/channel-secret-runtime` | Assistants étroits de collection de contrat secret pour les surfaces secrètes de canal/plugin |
    | `plugin-sdk/secret-ref-runtime` | Assistants étroits `coerceSecretRef` et de typage SecretRef pour l'analyse de contrat secret/configuration |
    | `plugin-sdk/security-runtime` | Assistants partagés de confiance, portail DM, contenu externe et collection secrète |
    | `plugin-sdk/ssrf-policy` | Assistants de politique SSRF de liste blanche d'hôte et de réseau privé |
    | `plugin-sdk/ssrf-dispatcher` | Assistants étroits de répartiteur épinglé sans la surface d'exécution d'infra large |
    | `plugin-sdk/ssrf-runtime` | Assistants de répartiteur épinglé, récupération gardée SSRF et politique SSRF |
    | `plugin-sdk/secret-input` | Assistants d'analyse d'entrée secrète |
    | `plugin-sdk/webhook-ingress` | Assistants de requête/cible webhook |
    | `plugin-sdk/webhook-request-guards` | Assistants de taille/délai d'expiration du corps de requête |
  </Accordion>

  <Accordion title="Sous-chemins d'exécution et de stockage">
    | Sous-chemin | Exports clés |
    | --- | --- |
    | `plugin-sdk/runtime` | Assistants larges d'exécution/journalisation/sauvegarde/installation de plugin |
    | `plugin-sdk/runtime-env` | Assistants étroits d'env d'exécution, enregistreur, délai d'expiration, nouvelle tentative et backoff |
    | `plugin-sdk/channel-runtime-context` | Assistants génériques d'enregistrement et de recherche de contexte d'exécution de canal |
    | `plugin-sdk/runtime-store` | `createPluginRuntimeStore` |
    | `plugin-sdk/plugin-runtime` | Assistants partagés de commande/hook/http/interactif de plugin |
    | `plugin-sdk/hook-runtime` | Assistants partagés de pipeline de hook/webhook interne |
    | `plugin-sdk/lazy-runtime` | Assistants d'importation/liaison d'exécution paresseux tels que `createLazyRuntimeModule`, `createLazyRuntimeMethod` et `createLazyRuntimeSurface` |
    | `plugin-sdk/process-runtime` | Assistants d'exécution de processus |
    | `plugin-sdk/cli-runtime` | Assistants de formatage, d'attente et de version CLI |
    | `plugin-sdk/gateway-runtime` | Client de passerelle et assistants de correctif d'état de canal |
    | `plugin-sdk/config-runtime` | Assistants de chargement/écriture de configuration et assistants de recherche de configuration de plugin |
    | `plugin-sdk/telegram-command-config` | Normalisation de nom/description de commande Telegram et vérifications de doublon/conflit, même quand la surface de contrat Telegram fournie n'est pas disponible |
    | `plugin-sdk/text-autolink-runtime` | Détection de lien automatique de référence de fichier sans le baril d'exécution de texte large |
    | `plugin-sdk/approval-runtime` | Assistants d'approbation d'exécution/plugin, générateurs de capacité d'approbation, assistants d'authentification/profil, assistants de routage/exécution natif |
    | `plugin-sdk/reply-runtime` | Assistants partagés d'exécution entrant/réponse, chunking, dispatch, heartbeat, planificateur de réponse |
    | `plugin-sdk/reply-dispatch-runtime` | Assistants étroits de dispatch/finalisation de réponse |
    | `plugin-sdk/reply-history` | Assistants partagés d'historique de réponse de fenêtre courte tels que `buildHistoryContext`, `recordPendingHistoryEntry` et `clearHistoryEntriesIfEnabled` |
    | `plugin-sdk/reply-reference` | `createReplyReferencePlanner` |
    | `plugin-sdk/reply-chunking` | Assistants étroits de chunking texte/markdown |
    | `plugin-sdk/session-store-runtime` | Assistants de chemin de magasin de session + mis à jour à |
    | `plugin-sdk/state-paths` | Assistants de chemin de répertoire d'état/OAuth |
    | `plugin-sdk/routing` | Assistants de liaison de route/clé de session/compte tels que `resolveAgentRoute`, `buildAgentSessionKey` et `resolveDefaultAgentBoundAccountId` |
    | `plugin-sdk/status-helpers` | Assistants partagés de résumé d'état de canal/compte, valeurs par défaut d'état d'exécution et assistants de métadonnées de problème |
    | `plugin-sdk/target-resolver-runtime` | Assistants partagés de résolveur de cible |
    | `plugin-sdk/string-normalization-runtime` | Assistants de normalisation de slug/chaîne |
    | `plugin-sdk/request-url` | Extraire les URL de chaîne des entrées de type récupération/requête |
    | `plugin-sdk/run-command` | Exécuteur de commande chronométré avec résultats stdout/stderr normalisés |
    | `plugin-sdk/param-readers` | Lecteurs de paramètres d'outil/CLI courants |
    | `plugin-sdk/tool-payload` | Extraire les charges utiles normalisées des objets de résultat d'outil |
    | `plugin-sdk/tool-send` | Extraire les champs de cible d'envoi canoniques des arguments d'outil |
    | `plugin-sdk/temp-path` | Assistants partagés de chemin de téléchargement temporaire |
    | `plugin-sdk/logging-core` | Enregistreur de sous-système et assistants de rédaction |
    | `plugin-sdk/markdown-table-runtime` | Assistants de mode de tableau markdown |
    | `plugin-sdk/json-store` | Petits assistants de lecture/écriture d'état JSON |
    | `plugin-sdk/file-lock` | Assistants de verrou de fichier réentrant |
    | `plugin-sdk/persistent-dedupe` | Assistants de cache de dédupe sauvegardé sur disque |
    | `plugin-sdk/acp-runtime` | Assistants d'exécution/session ACP et de dispatch de réponse |
    | `plugin-sdk/acp-binding-resolve-runtime` | Résolution de liaison ACP en lecture seule sans importations de démarrage de cycle de vie |
    | `plugin-sdk/agent-config-primitives` | Primitives étroites de schéma de configuration d'exécution d'agent |
    | `plugin-sdk/boolean-param` | Lecteur de paramètre booléen lâche |
    | `plugin-sdk/dangerous-name-runtime` | Assistants de résolution de correspondance de nom dangereux |
    | `plugin-sdk/device-bootstrap` | Assistants d'amorçage d'appareil et de jeton d'appairage |
    | `plugin-sdk/extension-shared` | Primitives partagées d'assistant de proxy ambiant, de statut et de canal passif |
    | `plugin-sdk/models-provider-runtime` | Assistants de réponse de commande/fournisseur `/models` |
    | `plugin-sdk/skill-commands-runtime` | Assistants d'énumération de commande de compétence |
    | `plugin-sdk/native-command-registry` | Assistants de registre/construction/sérialisation de commande natif |
    | `plugin-sdk/agent-harness` | Surface expérimentale de plugin de confiance pour les harnais d'agent de bas niveau : types de harnais, assistants de direction/abandon d'exécution actif, assistants de pont d'outil OpenClaw et utilitaires de résultat de tentative |
    | `plugin-sdk/provider-zai-endpoint` | Assistants de détection de point de terminaison Z.AI |
    | `plugin-sdk/infra-runtime` | Assistants d'événement système/heartbeat |
    | `plugin-sdk/collection-runtime` | Assistants de cache limité petit |
    | `plugin-sdk/diagnostic-runtime` | Assistants d'indicateur et d'événement de diagnostic |
    | `plugin-sdk/error-runtime` | Graphique d'erreur, formatage, assistants partagés de classification d'erreur, `isApprovalNotFoundError` |
    | `plugin-sdk/fetch-runtime` | Assistants de récupération enveloppée, proxy et recherche épinglée |
    | `plugin-sdk/runtime-fetch` | Récupération d'exécution consciente du répartiteur sans importations de proxy/récupération gardée |
    | `plugin-sdk/response-limit-runtime` | Lecteur de corps de réponse limité sans la surface d'exécution de média large |
    | `plugin-sdk/session-binding-runtime` | État de liaison de conversation actuelle sans routage de liaison configurée ou magasins d'appairage |
    | `plugin-sdk/session-store-runtime` | Assistants de lecture de magasin de session sans importations larges de maintenance/écritures de configuration |
    | `plugin-sdk/context-visibility-runtime` | Résolution de visibilité de contexte et filtrage de contexte supplémentaire sans importations larges de configuration/sécurité |
    | `plugin-sdk/string-coerce-runtime` | Assistants étroits de coercition/normalisation de record/chaîne primitif sans importations de markdown/journalisation |
    | `plugin-sdk/host-runtime` | Assistants de normalisation d'hôte SCP et de nom d'hôte |
    | `plugin-sdk/retry-runtime` | Assistants de configuration de nouvelle tentative et d'exécution de nouvelle tentative |
    | `plugin-sdk/agent-runtime` | Assistants de répertoire/identité/espace de travail d'agent |
    | `plugin-sdk/directory-runtime` | Requête de répertoire sauvegardée par configuration/dédupliquée |
    | `plugin-sdk/keyed-async-queue` | `KeyedAsyncQueue` |
  </Accordion>

  <Accordion title="Sous-chemins de capacité et de test">
    | Sous-chemin | Exports clés |
    | --- | --- |
    | `plugin-sdk/media-runtime` | Assistants partagés de récupération/transformation/stockage de média plus générateurs de charge utile de média |
    | `plugin-sdk/media-generation-runtime` | Assistants partagés de basculement de génération de média, sélection de candidat et messagerie de modèle manquant |
    | `plugin-sdk/media-understanding` | Types de fournisseur de compréhension de média plus exports d'assistant d'image/audio face au fournisseur |
    | `plugin-sdk/text-runtime` | Assistants partagés de texte/markdown/journalisation tels que dépouille de texte visible par assistant, assistants de rendu/chunking/tableau markdown, assistants de rédaction, assistants de balise de directive et utilitaires de texte sûr |
    | `plugin-sdk/text-chunking` | Assistant de chunking de texte sortant |
    | `plugin-sdk/speech` | Types de fournisseur de parole plus exports d'assistant de directive/registre/validation face au fournisseur |
    | `plugin-sdk/speech-core` | Types de fournisseur de parole partagés, registre, directive et assistants de normalisation |
    | `plugin-sdk/realtime-transcription` | Types de fournisseur de transcription en temps réel, assistants de registre et assistant partagé de session WebSocket |
    | `plugin-sdk/realtime-voice` | Types de fournisseur de voix en temps réel et assistants de registre |
    | `plugin-sdk/image-generation` | Types de fournisseur de génération d'image |
    | `plugin-sdk/image-generation-core` | Types de génération d'image partagés, basculement, authentification et assistants de registre |
    | `plugin-sdk/music-generation` | Types de fournisseur/requête/résultat de génération de musique |
    | `plugin-sdk/music-generation-core` | Types de génération de musique partagés, assistants de basculement, recherche de fournisseur et analyse de référence de modèle |
    | `plugin-sdk/video-generation` | Types de fournisseur/requête/résultat de génération de vidéo |
    | `plugin-sdk/video-generation-core` | Types de génération de vidéo partagés, assistants de basculement, recherche de fournisseur et analyse de référence de modèle |
    | `plugin-sdk/webhook-targets` | Registre de cible webhook et assistants d'installation d'itinéraire |
    | `plugin-sdk/webhook-path` | Assistants de normalisation de chemin webhook |
    | `plugin-sdk/web-media` | Assistants partagés de chargement de média distant/local |
    | `plugin-sdk/zod` | `zod` réexporté pour les consommateurs du SDK de plugin |
    | `plugin-sdk/testing` | `installCommonResolveTargetErrorCases`, `shouldAckReaction` |
  </Accordion>

  <Accordion title="Sous-chemins de mémoire">
    | Sous-chemin | Exports clés |
    | --- | --- |
    | `plugin-sdk/memory-core` | Surface d'assistant memory-core fournie pour les assistants de gestionnaire/configuration/fichier/CLI |
    | `plugin-sdk/memory-core-engine-runtime` | Façade d'exécution d'index/recherche de mémoire |
    | `plugin-sdk/memory-core-host-engine-foundation` | Exports du moteur de fondation d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-engine-embeddings` | Contrats d'intégration d'hôte de mémoire, accès au registre, fournisseur local et assistants génériques de lot/distant |
    | `plugin-sdk/memory-core-host-engine-qmd` | Exports du moteur QMD d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-engine-storage` | Exports du moteur de stockage d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-multimodal` | Assistants multimodaux d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-query` | Assistants de requête d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-secret` | Assistants secrets d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-events` | Assistants de journal d'événements d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-status` | Assistants d'état d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-runtime-cli` | Assistants d'exécution CLI d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-runtime-core` | Assistants d'exécution de base d'hôte de mémoire |
    | `plugin-sdk/memory-core-host-runtime-files` | Assistants de fichier/exécution d'hôte de mémoire |
    | `plugin-sdk/memory-host-core` | Alias neutre du fournisseur pour les assistants d'exécution de base d'hôte de mémoire |
    | `plugin-sdk/memory-host-events` | Alias neutre du fournisseur pour les assistants de journal d'événements d'hôte de mémoire |
    | `plugin-sdk/memory-host-files` | Alias neutre du fournisseur pour les assistants de fichier/exécution d'hôte de mémoire |
    | `plugin-sdk/memory-host-markdown` | Assistants markdown gérés partagés pour les plugins adjacents à la mémoire |
    | `plugin-sdk/memory-host-search` | Façade d'exécution de mémoire active pour l'accès au gestionnaire de recherche |
    | `plugin-sdk/memory-host-status` | Alias neutre du fournisseur pour les assistants d'état d'hôte de mémoire |
    | `plugin-sdk/memory-lancedb` | Surface d'assistant memory-lancedb fournie |
  </Accordion>

  <Accordion title="Sous-chemins d'assistant fourni réservés">
    | Famille | Sous-chemins actuels | Utilisation prévue |
    | --- | --- | --- |
    | Navigateur | `plugin-sdk/browser-cdp`, `plugin-sdk/browser-config-runtime`, `plugin-sdk/browser-config-support`, `plugin-sdk/browser-control-auth`, `plugin-sdk/browser-node-runtime`, `plugin-sdk/browser-profiles`, `plugin-sdk/browser-security-runtime`, `plugin-sdk/browser-setup-tools`, `plugin-sdk/browser-support` | Assistants de support de plugin de navigateur fournis (`browser-support` reste le baril de compatibilité) |
    | Matrix | `plugin-sdk/matrix`, `plugin-sdk/matrix-helper`, `plugin-sdk/matrix-runtime-heavy`, `plugin-sdk/matrix-runtime-shared`, `plugin-sdk/matrix-runtime-surface`, `plugin-sdk/matrix-surface`, `plugin-sdk/matrix-thread-bindings` | Surface d'assistant/exécution Matrix fournie |
    | Line | `plugin-sdk/line`, `plugin-sdk/line-core`, `plugin-sdk/line-runtime`, `plugin-sdk/line-surface` | Surface d'assistant/exécution LINE fournie |
    | IRC | `plugin-sdk/irc`, `plugin-sdk/irc-surface` | Surface d'assistant IRC fournie |
    | Assistants spécifiques au canal | `plugin-sdk/googlechat`, `plugin-sdk/zalouser`, `plugin-sdk/bluebubbles`, `plugin-sdk/bluebubbles-policy`, `plugin-sdk/mattermost`, `plugin-sdk/mattermost-policy`, `plugin-sdk/feishu-conversation`, `plugin-sdk/msteams`, `plugin-sdk/nextcloud-talk`, `plugin-sdk/nostr`, `plugin-sdk/tlon`, `plugin-sdk/twitch` | Coutures de compatibilité/assistant de canal fournis |
    | Assistants d'authentification/spécifiques au plugin | `plugin-sdk/github-copilot-login`, `plugin-sdk/github-copilot-token`, `plugin-sdk/diagnostics-otel`, `plugin-sdk/diffs`, `plugin-sdk/llm-task`, `plugin-sdk/thread-ownership`, `plugin-sdk/voice-call` | Coutures d'assistant de fonctionnalité/plugin fournies ; `plugin-sdk/github-copilot-token` exporte actuellement `DEFAULT_COPILOT_API_BASE_URL`, `deriveCopilotApiBaseUrlFromToken` et `resolveCopilotApiToken` |
  </Accordion>
</AccordionGroup>

## Connexes

- [Aperçu du SDK Plugin](/fr/plugins/sdk-overview)
- [Configuration du SDK Plugin](/fr/plugins/sdk-setup)
- [Création de plugins](/fr/plugins/building-plugins)
