---
title: Proposition de catégorie LTS
version: 1
---

# Proposition de catégorie LTS

Cette proposition identifie un ensemble minimal de catégories de scorecard de maturité qui
devraient être éligibles pour la première promesse de support LTS orientée entreprise.

Les scores sont affichés sous la forme `Coverage/Quality` à partir des fichiers
`inventory/<surface>/scores.yaml` actuels. Ils fournissent un contexte utile, mais l'éligibilité LTS
ici est une décision de support produit humain et ne nécessite pas le
seuil mécanique actuel de `coverage > 90` et `quality > 80`.
Les chiffres de Coverage et Quality sont générés par Codex et nécessitent toujours une
vérification humaine avant d'être traités comme faisant autorité.
La complétude est intentionnellement omise jusqu'à ce que ce score soit prêt à être utilisé.
Les noms de catégories renvoient à la note de preuve correspondante par catégorie.

Légende :

- `Surface` : un produit de haut niveau ou une zone opérationnelle dans la taxonomie, telle que `Gateway runtime`, `CLI`, `Slack`, ou `Linux Gateway host`.
- `Category` : une zone de capacité notée au sein d'une surface, utilisée comme unité pour les décisions de maturité et d'inclusion LTS.
- `✅` : la catégorie est incluse dans la tranche LTS initiale proposée.
- `➡️` : la catégorie est reportée de la tranche LTS initiale proposée.

## Surfaces LTS initiales proposées

### Runtime de passerelle (12/13)

| Statut | Catégorie                                                                                              | Score (Couverture/Qualité) |
| ------ | ----------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Cycle de vie de la passerelle](inventory/gateway-runtime/runtime-lifecycle-and-supervision.md)                   | `86/82`                  |
| ✅     | [Connexion WebSocket](inventory/gateway-runtime/websocket-handshake-and-session-establishment.md)    | `84/76`                  |
| ✅     | [Authentification et appairage des appareils](inventory/gateway-runtime/device-identity-auth-and-pairing.md)              | `88/72`                  |
| ✅     | [Contrôles de sécurité](inventory/gateway-runtime/security-and-hardening-posture.md)                      | `84/74`                  |
| ✅     | [Approbations et exécution à distance](inventory/gateway-runtime/approval-and-execution-safety.md)          | `88/72`                  |
| ✅     | [Rôles et permissions](inventory/gateway-runtime/roles-scopes-and-operator-policy.md)                | `85/62`                  |
| ✅     | [Santé, diagnostics et réparation](inventory/gateway-runtime/observability-health-and-repair.md)       | `68/62`                  |
| ✅     | [API HTTP](inventory/gateway-runtime/http-apis.md)                                                   | `88/74`                  |
| ✅     | [Surface web hébergée](inventory/gateway-runtime/hosted-web-surface.md)                                 | `88/74`                  |
| ✅     | [API RPC et événements de passerelle](inventory/gateway-runtime/core-rpc-coverage.md)                         | `68/57`                  |
| ✅     | [Accès réseau et découverte](inventory/gateway-runtime/network-exposure-and-transport-selection.md) | `68/62`                  |
| ➡️     | [Nœuds et capacités distantes](inventory/gateway-runtime/node-transport-and-capability-relay.md)     | `84/63`                  |
| ✅     | [Compatibilité des protocoles](inventory/gateway-runtime/protocol-typing-and-compatibility.md)              | `72/70`                  |

### Sécurité, authentification, appairage et secrets (5/6)

| Statut | Catégorie                                                                                                                            | Score (Couverture/Qualité) |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Politique d'approbation et protections des outils dangereux](inventory/security-auth-pairing-and-secrets/approval-policy-and-dangerous-tool-safeguards.md) | `86/72`                  |
| ✅     | [Authentification de passerelle et accès à distance](inventory/security-auth-pairing-and-secrets/gateway-auth-and-network-exposure.md)                  | `82/68`                  |
| ✅     | [Appairage des appareils et des nœuds](inventory/security-auth-pairing-and-secrets/device-identity-and-operator-pairing.md)                      | `83/66`                  |
| ✅     | [Hygiène des identifiants et secrets](inventory/security-auth-pairing-and-secrets/secrets-storage-redaction-and-configuration-hygiene.md) | `78/62`                  |
| ✅     | [Contrôle d'accès aux canaux](inventory/security-auth-pairing-and-secrets/channel-identity-allowlists-and-sender-pairing.md)             | `78/66`                  |
| ➡️     | [Confiance des plugins](inventory/security-auth-pairing-and-secrets/plugin-installation-trust-and-security-boundaries.md)                    | `76/70`                  |

### Runtime d'agent (6/9)

| Statut | Catégorie                                                                                                                             | Score (Couverture/Qualité) |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| ✅     | [Exécution des tours d'agent](inventory/agent-runtime-and-provider-execution/agent-turn-orchestration-and-runtime-lifecycle.md)             | `82/74`                  |
| ✅     | [Sélection du modèle et routage du fournisseur](inventory/agent-runtime-and-provider-execution/model-selection-provider-routing-and-runtime-policy.md) | `84/72`                  |
| ✅     | [Exécution du fournisseur hébergé](inventory/agent-runtime-and-provider-execution/hosted-provider-adapters-and-payload-compatibility.md)    | `76/70`                  |
| ✅     | [Contrôles d'exécution des outils](inventory/agent-runtime-and-provider-execution/tool-execution-approvals-and-sandbox-policy.md)             | `86/74`                  |
| ✅     | [Authentification du fournisseur](inventory/agent-runtime-and-provider-execution/provider-auth-profiles-and-credential-health.md)                      | `80/66`                  |
| ➡️     | [Runtimes externes et sous-agents](inventory/agent-runtime-and-provider-execution/cli-harnesses-external-runtimes-and-subagents.md)   | `78/66`                  |
| ➡️     | [Fournisseurs locaux et auto-hébergés](inventory/agent-runtime-and-provider-execution/local-and-self-hosted-provider-execution.md)        | `70/60`                  |
| ➡️     | [Streaming et progression](inventory/agent-runtime-and-provider-execution/streaming-progress-and-preview-visibility.md)                | `84/70`                  |
| ✅     | [Appels d'outils et gestion des réponses](inventory/agent-runtime-and-provider-execution/streaming-tool-call-and-response-normalization.md) | `80/66`                  |

### Moteur de session, mémoire et contexte (6/9)

| Statut | Catégorie                                                                                                                          | Score (Couverture/Qualité) |
| ------ | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Routage des sessions](inventory/session-memory-and-context-engine/session-routing-and-conversation-binding.md)                        | `82/74`                  |
| ✅     | [Gestion des sessions et transcriptions CLI](inventory/session-memory-and-context-engine/cli-session-and-transcript-management.md)     | `74/68`                  |
| ✅     | [Moteur de contexte](inventory/session-memory-and-context-engine/context-engine-and-runtime-assembly.md)                              | `72/80`                  |
| ✅     | [Persistance des transcriptions](inventory/session-memory-and-context-engine/transcript-persistence-and-durability.md)                    | `78/58`                  |
| ✅     | [Gestion des jetons](inventory/session-memory-and-context-engine/compaction-pruning-and-token-pressure.md)                          | `78/60`                  |
| ➡️     | [Historique multi-client et parité des sessions](inventory/session-memory-and-context-engine/cross-client-history-and-session-parity.md) | `76/62`                  |
| ➡️     | [Diagnostics, maintenance et récupération](inventory/session-memory-and-context-engine/diagnostics-maintenance-and-recovery.md)     | `72/68`                  |
| ✅     | [Invites principales et contexte](inventory/session-memory-and-context-engine/instruction-profile-and-context-visibility.md)             | `68/70`                  |
| ➡️     | [Mémoire](inventory/session-memory-and-context-engine/memory-files-tools-and-active-memory.md)                                     | `66/58`                  |

### CLI (6/7)

| Statut | Catégorie                                                                                                              | Score (Couverture/Qualité) |
| ------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Configuration CLI](inventory/cli-install-update-onboard-doctor/package-install-and-cli-entrypoints.md)                       | `78/75`                  |
| ✅     | [Intégration et configuration d'authentification](inventory/cli-install-update-onboard-doctor/first-run-onboarding-and-auth-selection.md)   | `86/78`                  |
| ✅     | [Gestion du service de passerelle](inventory/cli-install-update-onboard-doctor/gateway-service-install-and-lifecycle.md)    | `88/66`                  |
| ✅     | [Observabilité CLI](inventory/cli-install-update-onboard-doctor/status-health-logs-and-diagnostics-support-path.md)   | `84/74`                  |
| ✅     | [Docteur](inventory/cli-install-update-onboard-doctor/doctor-config-auth-plugin-and-lint.md)                           | `80/68`                  |
| ✅     | [Mises à jour et améliorations](inventory/cli-install-update-onboard-doctor/update-channel-and-core-upgrade-flow.md)           | `82/68`                  |
| ➡️     | [Configuration des plugins et canaux](inventory/cli-install-update-onboard-doctor/plugin-and-channel-setup-during-onboarding.md) | `82/72`                  |

### Hôte de passerelle Linux (4/5)

| Statut | Catégorie                                                                                                              | Score (Couverture/Qualité) |
| ------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Configuration de l'hôte et mises à jour](inventory/linux-gateway-host/linux-cli-install-and-update-path.md)                           | `82/78`                  |
| ✅     | [Runtime de passerelle et contrôle des services](inventory/linux-gateway-host/foreground-gateway-runtime-and-process-control.md) | `83/78`                  |
| ✅     | [Accès à distance et sécurité](inventory/linux-gateway-host/remote-network-exposure-tls-and-tailscale.md)               | `78/74`                  |
| ✅     | [Diagnostics et réparation](inventory/linux-gateway-host/diagnostics-logs-doctor-and-repair.md)                          | `82/78`                  |
| ➡️     | [Cibles de déploiement](inventory/linux-gateway-host/vps-container-and-cloud-deployment-guidance.md)                     | `76/72`                  |

### Windows via WSL2 (5/6)

| Statut | Catégorie                                                                                          | Score (Couverture/Qualité) |
| ------ | ------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Configuration WSL](inventory/windows-via-wsl2/wsl2-install-and-runtime-prerequisites.md)                 | `76/70`                  |
| ✅     | [CLI](inventory/windows-via-wsl2/wsl2-cli.md)                                                     | `76/70`                  |
| ✅     | [Cycle de vie du service de passerelle](inventory/windows-via-wsl2/systemd-gateway-service-lifecycle.md)      | `64/66`                  |
| ✅     | [Accès à la passerelle et exposition](inventory/windows-via-wsl2/auth-secrets-and-exposure-posture.md)    | `70/65`                  |
| ✅     | [Diagnostics et réparation](inventory/windows-via-wsl2/diagnostics-doctor-logs-and-repair.md)        | `74/72`                  |
| ➡️     | [Navigateur et interface de contrôle](inventory/windows-via-wsl2/split-host-browser-and-control-ui-interop.md) | `72/70`                  |

### Windows natif (1/4)

| Statut | Catégorie                                                                                                                | Score (Couverture/Qualité) |
| ------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [CLI](inventory/native-windows-cli-and-gateway/native-powershell-install-and-cli-entrypoints.md)                        | `72/66`                  |
| ➡️     | [Gestion de la passerelle](inventory/native-windows-cli-and-gateway/native-gateway-foreground-runtime-and-process-control.md) | `68/62`                  |
| ➡️     | [Réseau](inventory/native-windows-cli-and-gateway/windows-host-networking-portproxy-and-remote-access.md)           | `58/56`                  |
| ➡️     | [Mises à jour](inventory/native-windows-cli-and-gateway/windows-update-restart-handoff-and-package-locks.md)                 | `74/68`                  |

### Observabilité (3/5)

| Statut | Catégorie                                                                                                           | Score (Couverture/Qualité) |
| ------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| ✅     | [Santé et réparation](inventory/telemetry-diagnostics-and-observability/health-status-probes.md)                     | `80/76`                  |
| ✅     | [Journalisation](inventory/telemetry-diagnostics-and-observability/logging-log-tail-and-redaction.md)                     | `82/84`                  |
| ✅     | [Diagnostics des sessions](inventory/telemetry-diagnostics-and-observability/session-run-and-usage-diagnostics.md)      | `82/78`                  |
| ➡️     | [Collecte de diagnostics](inventory/telemetry-diagnostics-and-observability/diagnostics-export-support-bundles.md)   | `76/74`                  |
| ➡️     | [Export de télémétrie](inventory/telemetry-diagnostics-and-observability/diagnostic-events-hooks-and-trace-context.md) | `78/78`                  |

### Framework de canaux (5/8)

| Statut | Catégorie                                                                                                          | Score (Couverture/Qualité) |
| ------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Configuration des canaux](inventory/channel-framework/channel-setup.md)                                                     | `84/78`                  |
| ✅     | [Accès entrant et portes d'identité](inventory/channel-framework/inbound-access-and-identity-gates.md)             | `80/76`                  |
| ✅     | [Routage et livraison des conversations](inventory/channel-framework/conversation-routing-and-delivery.md)             | `77/71`                  |
| ✅     | [Pipeline de livraison sortante et de réponse](inventory/channel-framework/outbound-delivery-and-reply-pipeline.md)       | `82/75`                  |
| ✅     | [Santé du statut et contrôles de l'opérateur](inventory/channel-framework/status-health-and-operator-controls.md)         | `82/78`                  |
| ➡️     | [Actions de canal, commandes et approbations](inventory/channel-framework/channel-actions-commands-and-approvals.md)   | `68/72`                  |
| ➡️     | [Comportement des groupes, threads et salons ambiants](inventory/channel-framework/group-thread-and-ambient-room-behavior.md)   | `76/68`                  |
| ➡️     | [Médias, pièces jointes et données de canaux enrichies](inventory/channel-framework/media-attachments-and-rich-channel-data.md) | `68/70`                  |

### Slack (5/5)

| Statut | Catégorie                                                                                             | Score (Couverture/Qualité) |
| ------ | ---------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Configuration et opérations des canaux](inventory/slack/app-install-auth-manifest-and-scopes.md)              | `74/68`                  |
| ✅     | [Accès et identité](inventory/slack/dm-pairing-and-sender-authorization.md)                        | `74/70`                  |
| ✅     | [Routage et livraison des conversations](inventory/slack/channel-thread-routing-and-session-isolation.md) | `64/66`                  |
| ✅     | [Médias et contenu enrichi](inventory/slack/media-attachments-files-and-vision.md)                      | `64/66`                  |
| ✅     | [Contrôles natifs et approbations](inventory/slack/slash-commands-and-native-command-routing.md)        | `72/70`                  |

### Discord (4/6)

| Statut | Catégorie                                                                                                         | Score (Couverture/Qualité) |
| ------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Configuration et opérations des canaux](inventory/discord/bot-setup-and-account-configuration.md)                         | `74/71`                  |
| ✅     | [Accès et identité](inventory/discord/dm-pairing-and-sender-authorization.md)                                  | `74/72`                  |
| ✅     | [Routage et livraison des conversations](inventory/discord/guild-channel-routing-and-session-isolation.md)            | `74/72`                  |
| ✅     | [Médias et contenu enrichi](inventory/discord/media-attachments-and-voice-message-handling.md)                      | `74/72`                  |
| ➡️     | [Contrôles natifs et approbations](inventory/discord/native-slash-commands-components-and-interactive-callbacks.md) | `58/72`                  |
| ➡️     | [Voix en temps réel et appels](inventory/discord/realtime-discord-voice-channels.md)                                 | `74/66`                  |

### Telegram (5/5)

| Statut | Catégorie                                                                                         | Score (Couverture/Qualité) |
| ------ | ------------------------------------------------------------------------------------------------ | ------------------------ |
| ✅     | [Configuration et opérations des canaux](inventory/telegram/bot-setup-and-account-configuration.md)        | `76/70`                  |
| ✅     | [Accès et identité](inventory/telegram/dm-pairing-and-sender-authorization.md)                 | `76/68`                  |
| ✅     | [Routage et livraison des conversations](inventory/telegram/group-forum-topic-and-session-routing.md) | `74/68`                  |
| ✅     | [Médias et contenu enrichi](inventory/telegram/media-location-polls-and-rich-inputs.md)             | `74/72`                  |
| ✅     | [Contrôles natifs et approbations](inventory/telegram/inline-buttons-approvals-and-actions.md)      | `74/72`                  |

### Chemin du fournisseur OpenAI / Codex (3/5)

| Statut | Catégorie                                                                                                                        | Score (Couverture/Qualité) |
| ------ | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Modèle et authentification](inventory/openai-codex-provider-path/canonical-openai-model-routing-and-catalog.md)                            | `78/66`                  |
| ✅     | [Réponses Codex et compatibilité des charges utiles](inventory/openai-codex-provider-path/codex-responses-transport-and-payload-compatibility.md) | `76/70`                  |
| ✅     | [Harnais Codex natif](inventory/openai-codex-provider-path/native-codex-app-server-harness-and-thread-lifecycle.md)            | `82/72`                  |
| ➡️     | [Génération d'images et entrée multimodale](inventory/openai-codex-provider-path/image-generation-editing-and-multimodal-input.md)             | `80/72`                  |
| ➡️     | [Voix et audio en temps réel](inventory/openai-codex-provider-path/realtime-voice-transcription-and-speech.md)                     | `72/68`                  |

### Outils d'automatisation de navigateur et d'exécution/sandbox (2/3)

| Statut | Catégorie                                                                                                                   | Score (Couverture/Qualité) |
| ------ | -------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Invocation et exécution des outils](inventory/browser-automation-and-exec-sandbox-tools/exec-routing-and-process-lifecycle.md) | `82/79`                  |
| ✅     | [Sandbox et politique des outils](inventory/browser-automation-and-exec-sandbox-tools/sandbox-backends-and-workspace-isolation.md) | `76/72`                  |
| ➡️     | [Automatisation de navigateur](inventory/browser-automation-and-exec-sandbox-tools/browser-actions-snapshots-and-artifacts.md)       | `78/74`                  |

### Plugins (7/9)

| Statut | Catégorie                                                                                                                | Score (Couverture/Qualité) |
| ------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| ✅     | [Installation et exécution des plugins](inventory/plugin-sdk-and-bundled-plugin-architecture/runtime-loading-and-lifecycle.md) | `86/84`                  |
| ✅     | [Plugins groupés](inventory/plugin-sdk-and-bundled-plugin-architecture/bundled-plugin-discovery-and-inventory.md)       | `86/84`                  |
| ➡️     | [Plugin Canvas](inventory/plugin-sdk-and-bundled-plugin-architecture/canvas-plugin.md)                                  | `76/66`                  |
| ✅     | [Approbations des plugins](inventory/plugin-sdk-and-bundled-plugin-architecture/approval-and-security-boundaries.md)            | `84/86`                  |
| ✅     | [Plugins de fournisseur et d'outils](inventory/plugin-sdk-and-bundled-plugin-architecture/provider-tool-plugin-architecture.md)  | `84/82`                  |
| ✅     | [Plugins de canaux](inventory/plugin-sdk-and-bundled-plugin-architecture/channel-plugin-architecture.md)                  | `82/78`                  |
| ✅     | [Création et empaquetage des plugins](inventory/plugin-sdk-and-bundled-plugin-architecture/public-sdk-api-and-subpaths.md)  | `77/74`                  |
| ✅     | [Publication des plugins](inventory/plugin-sdk-and-bundled-plugin-architecture/distribution-release-and-compatibility.md)    | `79/82`                  |
| ➡️     | [Test des plugins](inventory/plugin-sdk-and-bundled-plugin-architecture/developer-testing-and-fixtures.md)               | `84/81`                  |

## Candidats non-LTS prioritaires

Cette section classe les paires surface/catégorie actuellement non-LTS qui devraient être
prioritaires pour une future éligibilité LTS. Elle est basée sur la taxonomie actuelle,
`inventory/**/scores.yaml`, et le sentiment provenant des archives locales `discrawl` et `gitcrawl`.

Base de scan actuelle :

- Tranche LTS initiale : `68` catégories.
- Taxonomie totale : `279` catégories.
- Portée de scan non-LTS : `211` catégories.
- Fraîcheur `gitcrawl` : synchronisée jusqu'au 2026-05-28.
- Fraîcheur `discrawl` : synchronisée jusqu'au 2026-05-29.

### Première vague

#### Hébergement Docker / Podman

- [Configuration des conteneurs](inventory/docker-podman-hosting/docker-install-compose-and-first-run-setup.md): `74/76`
- [Opérations des conteneurs](inventory/docker-podman-hosting/runtime-configuration-state-volumes-and-secrets.md): `76/70`
- [Publication et validation des images](inventory/docker-podman-hosting/image-build-release-packaging-and-attestations.md): `84/78`
- [Sandbox et outils des agents](inventory/docker-podman-hosting/containerized-agents-sandbox-and-tooling-support.md): `75/68`

Pourquoi : c'est l'écart de déploiement d'entreprise le plus important en dehors de la
tranche LTS initiale. Le sentiment du support Discord se concentre régulièrement autour de VPS, Docker, WSL,
persistance des volumes, secrets, mise à jour et confusion sur la restauration. GitHub a également un
problème actuel de boucle de redémarrage de passerelle Docker, `#86612`.

#### Microsoft Teams

- [Configuration et opérations des canaux](inventory/microsoft-teams/setup-app-registration-credentials-admin-install.md): `58/64`
- [Accès et identité](inventory/microsoft-teams/dm-pairing-sender-authorization-config-writes.md): `60/62`
- [Routage et livraison des conversations](inventory/microsoft-teams/team-channel-routing-mention-gates-sessions-thread-context.md): `68/66`
- [Médias et contenu enrichi](inventory/microsoft-teams/media-attachments-file-consent-graph-file-flows.md): `62/58`
- [Contrôles natifs et approbations](inventory/microsoft-teams/actions-reactions-polls-approvals-group-management.md): `64/66`

Pourquoi : Teams a des scores actuels faibles, mais c'est le deuxième canal de lieu de travail d'entreprise évident
après Slack. GitHub a un signal concret fort pour le comportement des sessions de canal,
le support multi-bot, la gestion des pièces jointes, l'identité gérée,
et la complexité de la configuration/administration : `#81084`, `#71058`, `#65329`, `#67177`, et
`#85149`.

#### Authentification multi-fournisseur

- Chemin du fournisseur Anthropic / [Authentification du fournisseur et récupération](inventory/anthropic-provider-path/auth-onboarding-and-credential-profile-health.md): `78/70`
- Chemin du fournisseur Google / [Configuration et identifiants du fournisseur](inventory/google-provider-path/provider-auth-credentials-and-operator-setup.md): `72/60`

Pourquoi : l'authentification du fournisseur est l'un des thèmes de support Discord les plus récurrents.
Les utilisateurs se bloquent sur l'authentification manquante, le routage de secours, les refroidissements, les profils obsolètes,
les secrets en texte brut, l'inadéquation du fournisseur et les commandes de récupération peu claires. Ces
catégories sont des prérequis pour rendre tout harnais d'entreprise multi-fournisseur
fiable.

#### Application Web Gateway

- [Accès au navigateur et confiance](inventory/browser-control-ui-and-webchat/gateway-connection-auth-device-pairing-and-origins.md): `84/68`
- [Configuration](inventory/browser-control-ui-and-webchat/config-schema-editing-and-safe-writes.md): `82/78`
- [Interface utilisateur du navigateur](inventory/browser-control-ui-and-webchat/control-ui-static-shell-routing-and-pwa.md): `74/72`
- [Conversations WebChat](inventory/browser-control-ui-and-webchat/chat-composer-session-model-controls-and-rendering.md): `78/66`
- [Console opérateur](inventory/browser-control-ui-and-webchat/diagnostics-logs-update-and-activity.md): `78/74`

Pourquoi : c'est la surface opérateur et administrateur pour un déploiement d'entreprise.
GitHub a des problèmes UX et runtime ouverts autour des portes d'authentification, de la perte de transcription,
des téléchargements, de l'entrée CJK et du streaming, et des rechargements partiels : `#85750`, `#72500`,
`#83344`, `#81606`, `#86035`, `#60247`, et `#86435`.

#### Automatisation : cron, hooks, tâches, polling

- [Tâches Cron](inventory/automation-cron-hooks-tasks-polling/cron-job-lifecycle.md): `82/73`
- [Tâches et flux en arrière-plan](inventory/automation-cron-hooks-tasks-polling/background-task-ledger.md): `73/68`
- [Ingestion d'événements](inventory/automation-cron-hooks-tasks-polling/channel-polling-webhooks.md): `65/58`
- [Hooks d'automatisation](inventory/automation-cron-hooks-tasks-polling/internal-hooks.md): `78/72`
- [Heartbeat](inventory/automation-cron-hooks-tasks-polling/heartbeat-commitments.md): `82/72`

Pourquoi : les agents d'entreprise ont besoin de travail planifié durable, d'alertes et de récupération.
GitHub a un signal actuel pour les courses au démarrage, les noms en doublon, la perte de données silencieuse,
la visibilité du statut, la portée élevée et le dépouillement des outils propriétaires : `#75889`,
`#76160`, `#83538`, `#51184`, `#41484`, et `#72954`.

#### TUI

- [Modes d'exécution](inventory/tui-and-terminal-ux/launch-modes-and-cli-entrypoints.md): `78/72`
- [Entrée et commandes](inventory/tui-and-terminal-ux/composer-keybindings-and-input-editing.md): `76/70`
- [Gestion des sessions](inventory/tui-and-terminal-ux/session-lifecycle-history-and-resume.md): `80/68`
- [Exécution du shell local](inventory/tui-and-terminal-ux/local-shell-execution-and-approval-boundary.md): `70/76`
- [Rendu et sécurité de la sortie](inventory/tui-and-terminal-ux/streaming-message-rendering-and-tool-cards.md): `76/70`

Pourquoi : TUI est une surface réelle orientée opérateur avec une documentation large et une couverture de base décente,
mais c'est toujours moins prouvé comme flux de travail principal supporté que le CLI et les chemins d'hôte Gateway
dans la tranche initiale. Promouvoir quand les modes de lancement,
le comportement des commandes/entrées, la reprise de session, les limites du shell local et le rendu du streaming
sont traités comme une promesse de support native du terminal.

### Deuxième vague

#### Hôte Gateway macOS

- [Cycle de vie du service Gateway](inventory/macos-gateway-host/launchagent-service-lifecycle.md): `82/76`
- [Intégration Gateway locale](inventory/macos-gateway-host/local-gateway-mode-host-configuration.md): `76/82`
- [Diagnostics et observabilité](inventory/macos-gateway-host/diagnostics-logs-operator-observability.md): `80/83`
- [Configuration CLI](inventory/macos-gateway-host/cli-install-runtime-prerequisites.md): `82/76`
- [Mode Gateway distant](inventory/macos-gateway-host/remote-gateway-mode-transport.md): `72/82`

Pourquoi : Linux est l'hôte LTS initial plus propre, mais macOS a un volume de support réel important
et une pertinence forte pour la passerelle de bureau. Les problèmes actuels incluent le signalement de LaunchAgent,
le comportement de liaison, la dérive des certificats et des mises à jour, les défaillances de volume externe,
la dérive Homebrew/runtime, les mises à niveau irrécupérables, les boucles de redémarrage et les défaillances d'installation :
`#81751`, `#65619`, `#86579`, `#87199`, `#75250`, `#85027`,
`#73673`, et `#60398`.

#### Automatisation du navigateur et outils exec/sandbox

- [Automatisation du navigateur](inventory/browser-automation-and-exec-sandbox-tools/browser-actions-snapshots-and-artifacts.md): `78/74`

Pourquoi : la tranche LTS initiale inclut déjà l'invocation d'outils principaux et la politique de sandbox,
mais l'exécution du navigateur fait partie d'un harnais d'agent d'entreprise pratique.
Les problèmes ouverts incluent l'inadéquation sandbox/runtime, le support de backend non-Docker,
le comportement noVNC/CJK, l'accès aux téléchargements, les délais d'expiration et la réactivité de l'interface de contrôle.

#### Outils de recherche Web

- [Sécurité réseau](inventory/web-search-tools/network-safety-ssrf-redirects-and-untrusted-content.md): `84/84`
- [Disponibilité des outils et récupération](inventory/web-search-tools/tool-exposure-policy-and-runtime-tool-wiring.md): `82/80`
- [Fournisseurs de recherche](inventory/web-search-tools/bundled-structured-search-providers.md): `76/72`
- [Configuration et diagnostics](inventory/web-search-tools/operator-setup-provider-selection-and-credential-repair.md): `74/70`

Pourquoi : la récupération web et la recherche structurée sont utiles pour les flux de travail de recherche d'entreprise,
mais elles sont en dehors de la promesse de support minimal initial. Promouvoir cette
surface quand la sécurité réseau, le câblage des outils runtime, la sélection du fournisseur, le comportement des délais d'expiration
et la réparation opérateur sont acceptés ensemble. GitHub a un signal de délai d'expiration de recherche,
d'outil natif du fournisseur, de suppression d'outil et d'option de fournisseur :
`#87505`, `#23353`, `#77826`, et `#84872`.

#### Runtime Gateway

- [Nœuds et capacités distantes](inventory/gateway-runtime/node-transport-and-capability-relay.md): `84/63`

Pourquoi : l'appairage de nœuds et le relais de capacité de nœud distant durcissent toujours le périmètre
autour de la promesse LTS Gateway existante et ont besoin d'une preuve opérationnelle séparée.

### Priorité inférieure pour LTS

L'observabilité devrait ajouter la collecte de diagnostics et
le durcissement de l'export de télémétrie après les priorités runtime et canal ci-dessus.
Le SDK de plugin devrait ajouter les plugins de test, l'empaquetage de plugins, puis la publication de plugins ;
cela importe pour la durabilité de l'écosystème, mais a un sentiment d'entreprise direct plus faible que Docker, Teams, Slack et l'authentification du fournisseur.

Continuer à différer les applications mobiles, la voix, la génération de médias, les canaux régionaux,
iMessage, Matrix, WhatsApp et les fournisseurs de longue traîne sauf si un engagement client spécifique
change la limite de support.

## Interprétation

Cette tranche LTS est intentionnellement conservatrice. Elle promet suffisamment pour qu'une entreprise
exécute un harnais d'agent utilisable avec Gateway, authentification et politique,
exécution de session/runtime, diagnostics opérationnels, hébergement Linux, Slack,
Discord, Telegram, le chemin du fournisseur OpenAI/Codex et les contrôles d'exécution des outils.

Les catégories en dehors de cette tranche peuvent continuer à être expédiées, mais ne doivent pas faire partie de la
garantie LTS initiale jusqu'à ce que leur propriétaire, limite de support, comportement de mise à niveau,
et modes de défaillance d'entreprise soient explicitement acceptés.
