---
title: "Taxonomie de maturité"
summary: "Référence détaillée pour les domaines de produit et les vérifications derrière la fiche de pointage de maturité OpenClaw."
---

# Taxonomie de maturité

Cette page explique les domaines de produit et les groupes de capacités derrière la fiche de pointage de maturité.

## Niveaux de maturité

| Niveau | Étiquette    | Signification                                                                               | Barre de promotion                                                                                                     |
| ------ | ------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `M0`   | Planifié     | La direction est connue, mais aucun chemin utilisateur pris en charge n'existe.             | Un problème de conception, un propriétaire et une surface cible existent.                                              |
| `M1`   | Expérimental | Implémenté derrière des avertissements, des drapeaux, des builds source ou des flux réservés aux responsables. | Le responsable peut exécuter le scénario à partir de la branche principale actuelle.                                   |
| `M2`   | Alpha        | Les vrais utilisateurs peuvent l'essayer, mais des modifications importantes et une UX incomplète sont attendues. | Configuration documentée, tests de base, avertissements connus et au moins une preuve en environnement réel.           |
| `M3`   | Bêta         | Un chemin public existe et le flux de travail principal est utilisable avec des avertissements limités.            | Docs d'installation/mise à jour, tests de régression, runbook de support et preuve de scénario réussi dans l'environnement attendu. |
| `M4`   | Stable       | Chemin recommandé pour les utilisateurs normaux. Les défaillances sont traitées comme des régressions.            | Porte de publication, chemin de diagnostic/dépannage, documentation large et preuve répétée dans le monde réel.       |
| `M5`   | Adorable     | Poli, délicieux, bien instrumenté et compétitif avec le meilleur flux de travail comparable. | Stable plus passage de la fiche de pointage utilisateur auprès des utilisateurs représentatifs.                       |

## Domaines de produit

### Surfaces principales

- [Exécution de la passerelle](#gateway-runtime)
- [CLI](#cli)
- [Plugins](#plugins)
- [Exécution de l'agent](#agent-runtime)
- [Moteur de session, mémoire et contexte](#session-memory-and-context-engine)
- [Cadre de canal](#channel-framework)
- [Sécurité, authentification, appairage et secrets](#security-auth-pairing-and-secrets)
- [Observabilité](#observability)
- [Automatisation : cron, hooks, tâches, polling](#automation-cron-hooks-tasks-polling)
- [Compréhension et génération de médias](#media-understanding-and-media-generation)
- [Voix et conversation en temps réel](#voice-and-realtime-talk)
- [Application Web de la passerelle](#gateway-web-app)
- [TUI](#tui)
- [ClawHub](#clawhub)
- [SDK d'application OpenClaw](#openclaw-app-sdk)

### Surfaces de plateforme

- [Hôte de passerelle macOS](#macos-gateway-host)
- [Application compagnon macOS](#macos-companion-app)
- [Hôte de passerelle Linux](#linux-gateway-host)
- [Application compagnon Linux](#linux-companion-app)
- [Windows via WSL2](#windows-via-wsl2)
- [Windows natif](#native-windows)
- [Application compagnon Windows natif](#native-windows-companion-app)
- [Application Android](#android-app)
- [Application iOS](#ios-app)
- [Surfaces compagnon watchOS](#watchos-companion-surfaces)
- [Raspberry Pi et petits appareils Linux](#raspberry-pi-and-small-linux-devices)
- [Hébergement Docker et Podman](#docker-and-podman-hosting)
- [Hébergement Kubernetes](#kubernetes-hosting)
- [Chemin d'installation Nix](#nix-install-path)

### Surfaces de canal

- [Discord](#discord)
- [Telegram](#telegram)
- [WhatsApp](#whatsapp)
- [Slack](#slack)
- [iMessage et BlueBubbles](#imessage-and-bluebubbles)
- [Signal](#signal)
- [Google Chat](#google-chat)
- [Matrix](#matrix)
- [Microsoft Teams](#microsoft-teams)
- [Mattermost, LINE, IRC, Nextcloud Talk, Nostr, Twitch, Tlon, Synology Chat](#mattermost-line-irc-nextcloud-talk-nostr-twitch-tlon-synology-chat)
- [Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, canaux régionaux](#feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels)
- [Canal d'appel vocal](#voice-call-channel)

### Surfaces de fournisseur et d'outil

- [Chemin du fournisseur OpenAI et Codex](#openai-and-codex-provider-path)
- [Chemin du fournisseur Anthropic](#anthropic-provider-path)
- [Chemin du fournisseur Google](#google-provider-path)
- [Chemin du fournisseur OpenRouter](#openrouter-provider-path)
- [Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio](#local-model-providers-ollama-vllm-sglang-lm-studio)
- [Fournisseurs hébergés de longue traîne](#long-tail-hosted-providers)
- [Outils de recherche Web](#web-search-tools)
- [Outils d'automatisation de navigateur, d'exécution et de bac à sable](#browser-automation-exec-and-sandbox-tools)
- [Outils de génération d'images, vidéos et musique](#image-video-and-music-generation-tools)

## Détails

### Core

#### Gateway runtime

- Level: M4 Stable
- Rationale: Core architecture, auth, pairing, protocol docs, daemon docs, and CLI runbooks are broad and current.

| Area                            | Capabilities | Docs                                                                                                                                                                                                                                      | Coverage             | Quality        | Completeness   | Long-term support |
| ------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | -------------- | -------------- | ----------------- |
| Approvals and Remote Execution  | 6            | [Protocol](/fr/gateway/protocol), [Index](/fr/gateway/security/index)                                                                                                                                                                           | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| HTTP APIs                       | 4            | [Index](/fr/gateway/index), [Openai Http Api](/fr/gateway/openai-http-api), [Openresponses Http Api](/fr/gateway/openresponses-http-api), [Tools Invoke Http Api](/fr/gateway/tools-invoke-http-api), [Hooks](/fr/automation/hooks), [Index](/fr/web/index) | `Experimental (25%)` | `Stable (90%)` | `Stable (90%)` | Yes               |
| Hosted Web Surface              | 4            | [Index](/fr/gateway/index), [Architecture](/fr/concepts/architecture), [Control Ui](/fr/web/control-ui), [Webchat](/fr/web/webchat), [Canvas](/fr/refactor/canvas)                                                                                       | `Experimental (0%)`  | `Stable (89%)` | `Stable (90%)` | Yes               |
| Gateway RPC APIs and Events     | 20           | [Protocol](/fr/gateway/protocol), [Index](/fr/gateway/index), [Architecture](/fr/concepts/architecture)                                                                                                                                            | `Experimental (0%)`  | `Stable (90%)` | `Stable (90%)` | Yes               |
| Device Auth and Pairing         | 10           | [Protocol](/fr/gateway/protocol), [Pairing](/fr/gateway/pairing), [Index](/fr/gateway/security/index)                                                                                                                                              | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| Network Access and Discovery    | 6            | [Index](/fr/gateway/index), [Discovery](/fr/gateway/discovery), [Protocol](/fr/gateway/protocol)                                                                                                                                                   | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| Nodes and Remote Capabilities   | 8            | [Protocol](/fr/gateway/protocol), [Architecture](/fr/concepts/architecture), [Index](/fr/nodes/index)                                                                                                                                              | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | No                |
| Health, Diagnostics, and Repair | 7            | [Index](/fr/gateway/index), [Diagnostics](/fr/gateway/diagnostics), [Doctor](/fr/gateway/doctor)                                                                                                                                                   | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| Protocol Compatibility          | 7            | [Protocol](/fr/gateway/protocol), [Architecture](/fr/concepts/architecture), [Typebox](/fr/concepts/typebox), [Bridge Protocol](/fr/gateway/bridge-protocol)                                                                                          | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| Roles and Permissions           | 5            | [Protocol](/fr/gateway/protocol), [Index](/fr/gateway/security/index)                                                                                                                                                                           | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| Gateway Lifecycle               | 7            | [Index](/fr/gateway/index), [Architecture](/fr/concepts/architecture)                                                                                                                                                                           | `Experimental (0%)`  | `Stable (90%)` | `Stable (90%)` | Yes               |
| Security Controls               | 6            | [Index](/fr/gateway/security/index), [Protocol](/fr/gateway/protocol), [Discovery](/fr/gateway/discovery)                                                                                                                                          | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| WebSocket Connection            | 8            | [Protocol](/fr/gateway/protocol), [Architecture](/fr/concepts/architecture)                                                                                                                                                                     | `Experimental (13%)` | `Stable (90%)` | `Stable (90%)` | Yes               |

#### CLI

- Level: M4 Stable
- Rationale: Normal setup and repair paths are documented across install, CLI, and gateway docs. Platform-specific Windows paths are tracked in the Windows via WSL2 and Native Windows rows.

| Area                       | Capabilities | Docs                                                                                                                       | Coverage             | Quality        | Completeness   | Long-term support |
| -------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------- | -------------------- | -------------- | -------------- | ----------------- |
| CLI Setup                  | 6            | [Index](/fr/install/index), [Installer](/fr/install/installer), [Node](/fr/install/node), [Updating](/fr/install/updating)             | `Experimental (17%)` | `Stable (89%)` | `Stable (90%)` | Yes               |
| Onboarding and Auth Setup  | 5            | [Onboard](/fr/cli/onboard), [Configure](/fr/cli/configure), [Onboarding Overview](/fr/start/onboarding-overview)                    | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |
| Plugin and Channel Setup   | 5            | [Onboard](/fr/cli/onboard), [Plugins](/fr/cli/plugins), [Channels](/fr/cli/channels)                                                | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | No                |
| Gateway Service Management | 5            | [Gateway](/fr/cli/gateway), [Updating](/fr/install/updating), [Troubleshooting](/fr/gateway/troubleshooting)                        | `Experimental (0%)`  | `Stable (87%)` | `Stable (90%)` | Yes               |
| CLI Observability          | 5            | [Status](/fr/cli/status), [Health](/fr/cli/health), [Logs](/fr/cli/logs), [Diagnostics](/fr/gateway/diagnostics)                       | `Experimental (0%)`  | `Stable (89%)` | `Stable (90%)` | Yes               |
| Doctor                     | 10           | [Doctor](/fr/cli/doctor), [Doctor](/fr/gateway/doctor), [Secrets](/fr/gateway/secrets), [Troubleshooting](/fr/gateway/troubleshooting) | `Experimental (0%)`  | `Stable (89%)` | `Stable (90%)` | Yes               |
| Updates and Upgrades       | 5            | [Updating](/fr/install/updating), [Update](/fr/cli/update), [Troubleshooting](/fr/gateway/troubleshooting)                          | `Experimental (0%)`  | `Beta (75%)`   | `Stable (89%)` | Yes               |

#### Plugins

- Level: M3 Beta
- Rationale: Broad docs and strong internal runtime evidence exist across manifests, discovery, loading, provider/tool architecture, and approval boundaries. Keep the row at beta until public SDK API/subpaths and external distribution proof are stronger.

| Area                            | Capabilities | Docs                                                                                                                                                                                                                                     | Coverage             | Quality       | Completeness | Long-term support |
| ------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ------------- | ------------ | ----------------- |
| Authoring and Packaging plugins | 8            | [Building Plugins](/fr/plugins/building-plugins), [Sdk Overview](/fr/plugins/sdk-overview), [Sdk Entrypoints](/fr/plugins/sdk-entrypoints), [Sdk Subpaths](/fr/plugins/sdk-subpaths), [Manifest](/fr/plugins/manifest), [Reference](/fr/plugins/reference) | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Bundled plugins                 | 5            | [Plugin Inventory](/fr/plugins/plugin-inventory), [Plugins](/fr/cli/plugins), [Architecture Internals](/fr/plugins/architecture-internals)                                                                                                        | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Canvas plugin                   | 6            | [Canvas](/fr/plugins/reference/canvas), [Canvas](/fr/refactor/canvas), [Configuration Reference](/fr/gateway/configuration-reference)                                                                                                             | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | No                |
| Installing and running plugins  | 6            | [Architecture](/fr/plugins/architecture), [Architecture Internals](/fr/plugins/architecture-internals), [Plugins](/fr/cli/plugins)                                                                                                                | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Channel plugins                 | 5            | [Sdk Channel Plugins](/fr/plugins/sdk-channel-plugins), [Sdk Channel Inbound](/fr/plugins/sdk-channel-inbound), [Sdk Channel Outbound](/fr/plugins/sdk-channel-outbound)                                                                          | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Provider and tool plugins       | 6            | [Sdk Provider Plugins](/fr/plugins/sdk-provider-plugins), [Tool Plugins](/fr/plugins/tool-plugins), [Adding Capabilities](/fr/plugins/adding-capabilities)                                                                                        | `Experimental (17%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Plugin approvals                | 6            | [Plugin Permission Requests](/fr/plugins/plugin-permission-requests), [Exec Approvals](/fr/tools/exec-approvals), [Sdk Channel Plugins](/fr/plugins/sdk-channel-plugins)                                                                          | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Publishing plugins              | 6            | [Plugins](/fr/cli/plugins), [Compatibility](/fr/plugins/compatibility), [Publishing](/fr/clawhub/publishing)                                                                                                                                      | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Testing plugins                 | 6            | [Sdk Testing](/fr/plugins/sdk-testing), [Sdk Setup](/fr/plugins/sdk-setup), [Codex Harness](/fr/plugins/codex-harness)                                                                                                                            | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | No                |

#### Agent Runtime

- Level: M3 Beta
- Rationale: Main loop, models, provider routing, and tool streaming are first-class, but provider behavior shifts weekly and needs scenario proof per release.

| Area                             | Capabilities | Docs                                                                                                                                                                                               | Coverage             | Quality       | Completeness | Long-term support |
| -------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ------------- | ------------ | ----------------- |
| Agent Turn Execution             | 3            | [Agent Loop](/fr/concepts/agent-loop), [Agent](/fr/cli/agent), [Agent Runtimes](/fr/concepts/agent-runtimes)                                                                                                | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | Yes               |
| External Runtimes and Subagents  | 4            | [Agent Runtimes](/fr/concepts/agent-runtimes), [Anthropic](/fr/providers/anthropic), [Google](/fr/providers/google), [Subagents](/fr/tools/subagents)                                                          | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | No                |
| Hosted Provider Execution        | 5            | [Openai](/fr/providers/openai), [Anthropic](/fr/providers/anthropic), [Google](/fr/providers/google), [Models](/fr/concepts/models)                                                                            | `Experimental (20%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Local and Self-hosted Providers  | 5            | [Ollama](/fr/providers/ollama), [Models](/fr/concepts/models), [Agent](/fr/cli/agent)                                                                                                                       | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | No                |
| Model and Runtime Selection      | 4            | [Models](/fr/concepts/models), [Models](/fr/cli/models), [Openai](/fr/providers/openai), [Agent Runtimes](/fr/concepts/agent-runtimes)                                                                         | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Provider Auth                    | 10           | [Models](/fr/concepts/models), [Agent](/fr/cli/agent), [Models](/fr/cli/models), [Openai](/fr/providers/openai), [Anthropic](/fr/providers/anthropic), [Google](/fr/providers/google), [Subagents](/fr/tools/subagents) | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Streaming and Progress           | 2            | [Streaming](/fr/concepts/streaming), [Agent Loop](/fr/concepts/agent-loop)                                                                                                                               | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | No                |
| Tool Calls and Response Handling | 3            | [Agent Loop](/fr/concepts/agent-loop), [Ollama](/fr/providers/ollama)                                                                                                                                    | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Tool Execution Controls          | 6            | [Sandbox Vs Tool Policy Vs Elevated](/fr/gateway/sandbox-vs-tool-policy-vs-elevated), [Agent Loop](/fr/concepts/agent-loop), [Subagents](/fr/tools/subagents)                                               | `Experimental (0%)`  | `Beta (79%)`  | `Beta (79%)` | Yes               |

#### Session, memory, and context engine

- Level: M3 Beta
- Rationale: Strong docs and active implementation. Maturity depends on transcript durability, compaction quality, and cross-client parity.

| Area                                    | Capabilities | Docs                                                                                                                                         | Coverage            | Quality       | Completeness | Long-term support |
| --------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------ | ----------------- |
| CLI Session and Transcript Management   | 2            | [Session](/fr/concepts/session), [Session Management Compaction](/fr/reference/session-management-compaction), [Sessions](/fr/cli/sessions)           | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Token Management                        | 3            | [Compaction](/fr/concepts/compaction), [Context](/fr/concepts/context), [Session Management Compaction](/fr/reference/session-management-compaction)  | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Context Engine                          | 2            | [Context](/fr/concepts/context), [Context Engine](/fr/concepts/context-engine), [Codex Context Engine Harness](/fr/plan/codex-context-engine-harness) | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Cross-client History and Session Parity | 2            | [Webchat](/fr/web/webchat), [Android](/fr/platforms/android), [Channel Routing](/fr/channels/channel-routing)                                         | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Diagnostics, Maintenance, and Recovery  | 3            | [Diagnostics](/fr/gateway/diagnostics), [Session Management Compaction](/fr/reference/session-management-compaction), [Flags](/fr/diagnostics/flags)  | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Core Prompts and Context                | 2            | [Context](/fr/concepts/context), [Transcript Hygiene](/fr/reference/transcript-hygiene), [Discord](/fr/channels/discord)                              | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Memory                                  | 5            | [Memory Config](/fr/reference/memory-config), [Memory Qmd](/fr/concepts/memory-qmd), [Memory](/fr/concepts/memory), [Discord](/fr/channels/discord)      | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Session Routing                         | 2            | [Session](/fr/concepts/session), [Channel Routing](/fr/channels/channel-routing), [Discord](/fr/channels/discord)                                     | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Transcript Persistence                  | 2            | [Session Management Compaction](/fr/reference/session-management-compaction), [Transcript Hygiene](/fr/reference/transcript-hygiene)               | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | Yes               |

#### Channel framework

- Level: M3 Beta
- Rationale: Many channels share Gateway delivery and routing contracts, but channel behavior varies by upstream API and account-policy constraints.

| Area                                    | Capabilities | Docs                                                                                                                                                                                                                                          | Coverage            | Quality       | Completeness | Long-term support |
| --------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------ | ----------------- |
| Channel Actions Commands and Approvals  | 5            | [Groups](/fr/channels/groups), [Discord](/fr/channels/discord), [Googlechat](/fr/channels/googlechat), [Signal](/fr/channels/signal), [Matrix](/fr/channels/matrix)                                                                                          | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Channel Setup                           | 5            | [Index](/fr/channels/index), [Pairing](/fr/channels/pairing), [Troubleshooting](/fr/channels/troubleshooting), [Sdk Channel Plugins](/fr/plugins/sdk-channel-plugins)                                                                                     | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Group Thread and Ambient Room Behavior  | 5            | [Groups](/fr/channels/groups), [Group Messages](/fr/channels/group-messages), [Ambient Room Events](/fr/channels/ambient-room-events), [Broadcast Groups](/fr/channels/broadcast-groups), [Discord](/fr/channels/discord)                                    | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Inbound Access and Identity Gates       | 5            | [Access Groups](/fr/channels/access-groups), [Groups](/fr/channels/groups), [Discord](/fr/channels/discord), [Line](/fr/channels/line)                                                                                                                    | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Media Attachments and Rich Channel Data | 4            | [Line](/fr/channels/line), [Signal](/fr/channels/signal), [Googlechat](/fr/channels/googlechat), [Matrix](/fr/channels/matrix), [Discord](/fr/channels/discord)                                                                                              | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Outbound Delivery and Reply Pipeline    | 4            | [Groups](/fr/channels/groups), [Ambient Room Events](/fr/channels/ambient-room-events), [Discord](/fr/channels/discord), [Matrix](/fr/channels/matrix), [Config Channels](/fr/gateway/config-channels)                                                       | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Conversation Routing and Delivery       | 10           | [Channel Routing](/fr/channels/channel-routing), [Groups](/fr/channels/groups), [Discord](/fr/channels/discord), [Matrix](/fr/channels/matrix), [Troubleshooting](/fr/channels/troubleshooting), [Configuration Reference](/fr/gateway/configuration-reference) | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Status Health and Operator Controls     | 4            | [Health](/fr/gateway/health), [Configuration Reference](/fr/gateway/configuration-reference), [Troubleshooting](/fr/channels/troubleshooting), [Discord](/fr/channels/discord)                                                                            | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |

#### Security, auth, pairing, and secrets

- Level: M3 Beta
- Rationale: Good docs and hardening surfaces exist. Promote after regular upgrade/security scenario runs prove no setup regressions.

| Area                                | Capabilities | Docs                                                                                                                                                                                                                                                                                                                                                                                                                                           | Coverage            | Quality       | Completeness | Long-term support |
| ----------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------ | ----------------- |
| Approval Policy and Tool Safeguards | 2            | [Exec Approvals](/fr/tools/exec-approvals), [Approvals](/fr/cli/approvals), [Plugin Permission Requests](/fr/plugins/plugin-permission-requests), [Audit Checks](/fr/gateway/security/audit-checks)                                                                                                                                                                                                                                                        | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Gateway Auth and Remote Access      | 9            | [Index](/fr/gateway/security/index), [Exposure Runbook](/fr/gateway/security/exposure-runbook), [Trusted Proxy Auth](/fr/gateway/trusted-proxy-auth), [Tailscale](/fr/gateway/tailscale), [Remote](/fr/gateway/remote), [Configuration Reference](/fr/gateway/configuration-reference), [Gateway](/fr/cli/gateway), [Doctor](/fr/cli/doctor), [Control Ui](/fr/web/control-ui), [Browser Control](/fr/tools/browser-control), [Audit Checks](/fr/gateway/security/audit-checks) | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Channel Access Control              | 3            | [Pairing](/fr/channels/pairing), [Telegram](/fr/channels/telegram), [Access Groups](/fr/channels/access-groups), [Audit Checks](/fr/gateway/security/audit-checks)                                                                                                                                                                                                                                                                                         | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Device and Node Pairing             | 11           | [Protocol](/fr/gateway/protocol), [Devices](/fr/cli/devices), [Pairing](/fr/channels/pairing), [Pairing](/fr/gateway/pairing), [Operator Scopes](/fr/gateway/operator-scopes), [Control Ui](/fr/web/control-ui), [Webchat](/fr/web/webchat), [Approvals](/fr/cli/approvals)                                                                                                                                                                                            | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Plugin Trust                        | 2            | [Manifest](/fr/plugins/manifest), [Plugin Permission Requests](/fr/plugins/plugin-permission-requests), [Manage Plugins](/fr/plugins/manage-plugins), [Audit Checks](/fr/gateway/security/audit-checks)                                                                                                                                                                                                                                                    | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Credential and Secret Hygiene       | 5            | [Authentication](/fr/gateway/authentication), [Models](/fr/cli/models), [Openai](/fr/providers/openai), [Oauth](/fr/concepts/oauth), [Secrets](/fr/gateway/secrets), [Secrets](/fr/cli/secrets), [Secretref Credential Surface](/fr/reference/secretref-credential-surface), [Audit Checks](/fr/gateway/security/audit-checks)                                                                                                                                         | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |

#### Observability

- Level: M3 Beta
- Rationale: OTel, Prometheus, logging, and diagnostics docs exist. Needs a public "what operators should look at first" maturity pass.

| Area                  | Capabilities | Docs                                                                                                                                                                                                                                                                                          | Coverage             | Quality       | Completeness | Long-term support |
| --------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ------------- | ------------ | ----------------- |
| Health and Repair     | 12           | [Health](/fr/gateway/health), [Telegram](/fr/channels/telegram), [Doctor](/fr/cli/doctor), [Doctor](/fr/gateway/doctor), [Sdk Subpaths](/fr/plugins/sdk-subpaths), [Health](/fr/cli/health), [Protocol](/fr/gateway/protocol)                                                                                      | `Experimental (8%)`  | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Logging               | 5            | [Logging](/fr/logging), [Logging](/fr/gateway/logging), [Logs](/fr/cli/logs)                                                                                                                                                                                                                           | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | Yes               |
| Diagnostic Collection | 8            | [Diagnostics](/fr/gateway/diagnostics), [Health](/fr/gateway/health), [Codex Harness](/fr/plugins/codex-harness), [Protocol](/fr/gateway/protocol)                                                                                                                                                        | `Experimental (13%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Telemetry Export      | 13           | [Hooks](/fr/plugins/hooks), [Opentelemetry](/fr/gateway/opentelemetry), [Logging](/fr/logging), [Sdk Subpaths](/fr/plugins/sdk-subpaths), [Diagnostics Otel](/fr/plugins/reference/diagnostics-otel), [Prometheus](/fr/gateway/prometheus), [Diagnostics Prometheus](/fr/plugins/reference/diagnostics-prometheus) | `Experimental (8%)`  | `Beta (79%)`  | `Beta (79%)` | No                |
| Session Diagnostics   | 4            | [Opentelemetry](/fr/gateway/opentelemetry), [Prometheus](/fr/gateway/prometheus), [Diagnostics](/fr/gateway/diagnostics), [Protocol](/fr/gateway/protocol)                                                                                                                                                | `Experimental (0%)`  | `Alpha (68%)` | `Beta (79%)` | Yes               |

#### Automation: cron, hooks, tasks, polling

- Level: M3 Beta
- Rationale: Documented and usable, but scenario proof should cover unattended delivery, retries, and failure visibility.

| Area                       | Capabilities | Docs                                                                                                                                                                                                                                                                                                                                                                                                | Coverage            | Quality       | Completeness | Long-term support |
| -------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------ | ----------------- |
| Cron Jobs                  | 15           | [Cron Jobs](/fr/automation/cron-jobs), [Cron](/fr/cli/cron), [Protocol](/fr/gateway/protocol), [Tasks](/fr/automation/tasks), [Discord](/fr/channels/discord)                                                                                                                                                                                                                                                      | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Event Ingress              | 15           | [Telegram](/fr/channels/telegram), [Zalo](/fr/channels/zalo), [Troubleshooting](/fr/channels/troubleshooting), [Imessage From Bluebubbles](/fr/channels/imessage-from-bluebubbles), [Gmail Pubsub Integration](/fr/automation/cron-jobs#gmail-pubsub-integration), [Gmail Pubsub](/fr/automation/gmail-pubsub), [Webhooks](/fr/cli/webhooks), [Webhooks](/fr/automation/cron-jobs#webhooks), [Webhook](/fr/automation/webhook) | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Automation Hooks           | 11           | [Hooks](/fr/automation/hooks), [Hooks](/fr/cli/hooks), [Hooks](/fr/plugins/hooks), [Plugin Permission Requests](/fr/plugins/plugin-permission-requests), [Sdk Subpaths](/fr/plugins/sdk-subpaths)                                                                                                                                                                                                                  | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Background Tasks and Flows | 10           | [Tasks](/fr/automation/tasks), [Index](/fr/automation/index), [Tasks](/fr/cli/tasks), [Taskflow](/fr/automation/taskflow), [Sdk Runtime](/fr/plugins/sdk-runtime)                                                                                                                                                                                                                                                  | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Heartbeat                  | 5            | [Index](/fr/automation/index), [Heartbeat](/fr/gateway/heartbeat), [Commitments](/fr/concepts/commitments)                                                                                                                                                                                                                                                                                                   | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Polling Controls           | 10           | [Poll](/fr/automation/poll), [Message](/fr/cli/message), [Telegram](/fr/channels/telegram), [Msteams](/fr/channels/msteams), [Background Process](/fr/gateway/background-process)                                                                                                                                                                                                                                  | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |

#### Media understanding and media generation

- Level: M2 Alpha
- Rationale: Broad capability surface exists, but provider variance, file limits, and node/app parity make this not stable yet.

| Area                    | Capabilities | Docs                                                                                                                                                                                                                                                                                                  | Coverage            | Quality       | Completeness  | Long-term support |
| ----------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------- | ----------------- |
| Media Intake and Access | 8            | [Media Overview](/fr/tools/media-overview), [Media Understanding](/fr/nodes/media-understanding), [Secure File Operations](/fr/gateway/security/secure-file-operations), [Pdf](/fr/tools/pdf), [Image Generation](/fr/tools/image-generation), [Qr](/fr/cli/qr), [Line](/fr/channels/line), [Whatsapp](/fr/channels/whatsapp) | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Channel Media Handling  | 5            | [Images](/fr/nodes/images), [Media Overview](/fr/tools/media-overview), [Discord](/fr/channels/discord)                                                                                                                                                                                                        | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Media Configuration     | 1            | [Media Overview](/fr/tools/media-overview), [Image Generation](/fr/tools/image-generation), [Manifest](/fr/plugins/manifest), [Codex Harness](/fr/plugins/codex-harness)                                                                                                                                          | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Text-to-Speech Delivery | 2            | [Tts](/fr/tools/tts), [Media Overview](/fr/tools/media-overview), [Discord](/fr/channels/discord)                                                                                                                                                                                                              | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Media Understanding     | 12           | [Audio](/fr/nodes/audio), [Media Understanding](/fr/nodes/media-understanding), [Media Overview](/fr/tools/media-overview), [Whatsapp](/fr/channels/whatsapp), [Images](/fr/nodes/images), [Infer](/fr/cli/infer), [Pdf](/fr/tools/pdf)                                                                                    | `Experimental (0%)` | `Alpha (69%)` | `Alpha (69%)` | No                |
| Media Generation        | 17           | [Image Generation](/fr/tools/image-generation), [Media Overview](/fr/tools/media-overview), [Skills](/fr/tools/skills), [Music Generation](/fr/tools/music-generation), [Video Generation](/fr/tools/video-generation)                                                                                               | `Experimental (6%)` | `Alpha (69%)` | `Alpha (69%)` | No                |

#### Voice and realtime talk

- Level: M2 Alpha
- Rationale: Multiple implementations exist across Control UI, apps, and providers. Needs latency, failure-mode, and setup scorecards before beta.

| Area                     | Capabilities | Docs                                                                                                                                                                | Coverage            | Quality       | Completeness  | Long-term support |
| ------------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------- | ----------------- |
| Talk Providers           | 7            | [Openai](/fr/providers/openai), [Google](/fr/providers/google), [Sdk Provider Plugins](/fr/plugins/sdk-provider-plugins), [Talk](/fr/nodes/talk), [Control Ui](/fr/web/control-ui) | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Realtime Talk Sessions   | 11           | [Talk](/fr/nodes/talk), [Control Ui](/fr/web/control-ui)                                                                                                                  | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Speech and Transcription | 5            | [Talk](/fr/nodes/talk), [Openai](/fr/providers/openai), [Google](/fr/providers/google)                                                                                       | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Native App Talk          | 4            | [Talk](/fr/nodes/talk), [Voicewake](/fr/platforms/mac/voicewake)                                                                                                          | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Voice Wake and Routing   | 4            | [Voicewake](/fr/nodes/voicewake), [Voicewake](/fr/platforms/mac/voicewake), [Voice Overlay](/fr/platforms/mac/voice-overlay)                                                 | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Talk Observability       | 5            | [Control Ui](/fr/web/control-ui), [Voice Overlay](/fr/platforms/mac/voice-overlay), [Talk](/fr/nodes/talk)                                                                   | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |

#### Gateway Web App

- Level: M3 Beta
- Rationale: Web UI is documented with pairing, chat, PWA, Talk, push, and remote Gateway flows. Promote after cross-browser and mobile-PWA scorecards.

| Area                     | Capabilities | Docs                                                                                                                                                                                                                | Coverage            | Quality       | Completeness | Long-term support |
| ------------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------ | ----------------- |
| Browser Realtime Talk    | 5            | [Control Ui](/fr/web/control-ui), [Protocol](/fr/gateway/protocol), [Talk](/fr/nodes/talk)                                                                                                                                   | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Browser Access and Trust | 5            | [Control Ui](/fr/web/control-ui), [Dashboard](/fr/web/dashboard), [Tailscale](/fr/gateway/tailscale), [Remote](/fr/gateway/remote)                                                                                              | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Configuration            | 5            | [Control Ui](/fr/web/control-ui), [Configuration](/fr/gateway/configuration)                                                                                                                                              | `Experimental (0%)` | `Alpha (68%)` | `Beta (79%)` | No                |
| Browser UI               | 10           | [Control Ui](/fr/web/control-ui), [Index](/fr/web/index), [Dashboard](/fr/web/dashboard), [Protocol](/fr/gateway/protocol)                                                                                                      | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| WebChat Conversations    | 15           | [Control Ui](/fr/web/control-ui), [Webchat](/fr/web/webchat), [Getting Started](/fr/start/getting-started), [Channel Routing](/fr/channels/channel-routing), [Secure File Operations](/fr/gateway/security/secure-file-operations) | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |
| Operator Console         | 10           | [Control Ui](/fr/web/control-ui), [Health](/fr/gateway/health), [Protocol](/fr/gateway/protocol), [Dashboard](/fr/web/dashboard)                                                                                                | `Experimental (0%)` | `Beta (79%)`  | `Beta (79%)` | No                |

#### TUI

- Level: M2 Alpha
- Rationale: Present in docs and source, but less visible as a primary user workflow. Needs explicit scenario definition.

| Area                        | Capabilities | Docs                                                                             | Coverage            | Quality       | Completeness  | Long-term support |
| --------------------------- | ------------ | -------------------------------------------------------------------------------- | ------------------- | ------------- | ------------- | ----------------- |
| Runtime Modes               | 14           | [Tui](/fr/cli/tui), [Tui](/fr/web/tui), [Index](/fr/cli/index)                            | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Input and Commands          | 8            | [Tui](/fr/web/tui)                                                                  | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Session Management          | 3            | [Tui](/fr/web/tui), [Sessions](/fr/cli/sessions)                                       | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Local Shell Execution       | 4            | [Tui](/fr/web/tui), [Tui](/fr/cli/tui)                                                 | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Rendering and Output Safety | 4            | [Tui](/fr/web/tui), [Qr](/fr/cli/qr), [Logs](/fr/cli/logs), [Completion](/fr/cli/completion) | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |

#### ClawHub

- Level: M2 Alpha
- Rationale: Public docs and ecosystem concept exist. Needs install, trust, update, rollback, and compatibility scorecards.

| Area                        | Capabilities | Docs                                                                                                                                                                                                                                        | Coverage            | Quality       | Completeness  | Long-term support |
| --------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------- | ----------------- |
| Publishing                  | 7            | [Publishing](/fr/clawhub/publishing), [Creating Skills](/fr/tools/creating-skills), [Community](/fr/plugins/community)                                                                                                                               | `Experimental (0%)` | `Alpha (54%)` | `Alpha (55%)` | No                |
| Catalog Discovery           | 5            | [Plugin](/fr/tools/plugin), [Plugins](/fr/cli/plugins), [Skills](/fr/cli/skills), [Skills](/fr/tools/skills), [Community](/fr/plugins/community)                                                                                                           | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |
| Compatibility and Trust     | 12           | [Plugin](/fr/tools/plugin), [Plugins](/fr/cli/plugins), [Compatibility](/fr/plugins/compatibility), [Plugin Inventory](/fr/plugins/plugin-inventory), [Publishing](/fr/clawhub/publishing), [Skills](/fr/tools/skills), [Skills Config](/fr/tools/skills-config) | `Experimental (0%)` | `Alpha (55%)` | `Alpha (56%)` | No                |
| Plugin Lifecycle and Health | 26           | [Plugin](/fr/tools/plugin), [Plugins](/fr/cli/plugins), [Skills](/fr/cli/skills), [Skills](/fr/tools/skills), [Protocol](/fr/gateway/protocol), [Bundles](/fr/plugins/bundles), [Dependency Resolution](/fr/plugins/dependency-resolution)                       | `Experimental (0%)` | `Alpha (61%)` | `Alpha (68%)` | No                |

#### OpenClaw App SDK

- Level: M2 Alpha
- Rationale: OpenClaw App SDK is a distinct external app contract separate from Gateway runtime and Plugin SDK. Current scoring shows a real `@openclaw/sdk` path with gaps around public packaging, auto-discovery, approvals, helpers, and compatibility.

| Area                 | Capabilities | Docs                                                                                                                                                       | Coverage            | Quality       | Completeness  | Long-term support |
| -------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------- | ----------------- |
| Client API           | 4            | [Openclaw Sdk](/fr/gateway/external-apps), [Openclaw Sdk Api Design](/fr/gateway/external-apps)                                                                  | `Experimental (0%)` | `Alpha (51%)` | `Alpha (50%)` | No                |
| Gateway Access       | 5            | [Openclaw Sdk](/fr/gateway/external-apps), [Openclaw Sdk Api Design](/fr/gateway/external-apps), [Protocol](/fr/gateway/protocol), [Index](/fr/gateway/security/index) | `Experimental (0%)` | `Alpha (53%)` | `Alpha (54%)` | No                |
| Agent Conversations  | 6            | [Openclaw Sdk](/fr/gateway/external-apps), [Openclaw Sdk Api Design](/fr/gateway/external-apps), [Protocol](/fr/gateway/protocol)                                   | `Experimental (0%)` | `Alpha (52%)` | `Alpha (52%)` | No                |
| Events and Approvals | 5            | [Openclaw Sdk](/fr/gateway/external-apps), [Openclaw Sdk Api Design](/fr/gateway/external-apps), [Protocol](/fr/gateway/protocol)                                   | `Experimental (0%)` | `Alpha (52%)` | `Alpha (52%)` | No                |
| Resource Helpers     | 5            | [Openclaw Sdk](/fr/gateway/external-apps), [Openclaw Sdk Api Design](/fr/gateway/external-apps)                                                                  | `Experimental (0%)` | `Alpha (62%)` | `Alpha (53%)` | No                |
| Compatibility        | 5            | [Openclaw Sdk Api Design](/fr/gateway/external-apps), [Typebox](/fr/concepts/typebox), [Protocol](/fr/gateway/protocol)                                             | `Experimental (0%)` | `Alpha (54%)` | `Alpha (55%)` | No                |

### Platform

#### macOS Gateway host

- Level: M4 Stable
- Rationale: LaunchAgent service path, local/remote Gateway modes, CLI install, and app integration are documented.

| Area                                | Capabilities | Docs                                                                                                                                                                                                                                                               | Coverage            | Quality      | Completeness   | Long-term support |
| ----------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- | ------------ | -------------- | ----------------- |
| CLI Setup                           | 4            | [Macos](/fr/platforms/macos), [Bundled Gateway](/fr/platforms/mac/bundled-gateway), [Installer](/fr/install/installer), [Node](/fr/install/node)                                                                                                                               | `Experimental (0%)` | `Beta (74%)` | `Stable (88%)` | No                |
| Local Gateway Integration           | 9            | [Macos](/fr/platforms/macos), [Bundled Gateway](/fr/platforms/mac/bundled-gateway), [Remote](/fr/platforms/mac/remote), [Index](/fr/gateway/index), [Gateway](/fr/cli/gateway), [Bonjour](/fr/gateway/bonjour)                                                                       | `Experimental (0%)` | `Beta (74%)` | `Stable (88%)` | No                |
| Remote Gateway Mode                 | 5            | [Remote](/fr/platforms/mac/remote), [Remote](/fr/gateway/remote), [Tailscale](/fr/gateway/tailscale)                                                                                                                                                                        | `Experimental (0%)` | `Beta (74%)` | `Stable (88%)` | No                |
| Gateway Service Lifecycle           | 10           | [Macos](/fr/platforms/macos), [Bundled Gateway](/fr/platforms/mac/bundled-gateway), [Gateway](/fr/cli/gateway), [Index](/fr/gateway/index), [Update](/fr/cli/update), [Updating](/fr/install/updating), [Uninstall](/fr/install/uninstall), [Troubleshooting](/fr/gateway/troubleshooting) | `Experimental (0%)` | `Beta (74%)` | `Stable (88%)` | No                |
| Diagnostics and Observability       | 4            | [Bundled Gateway](/fr/platforms/mac/bundled-gateway), [Macos](/fr/platforms/macos), [Gateway](/fr/cli/gateway), [Doctor](/fr/gateway/doctor), [Troubleshooting](/fr/gateway/troubleshooting)                                                                                      | `Experimental (0%)` | `Beta (74%)` | `Stable (88%)` | No                |
| Permissions and Native Capabilities | 4            | [Macos](/fr/platforms/macos), [Remote](/fr/platforms/mac/remote)                                                                                                                                                                                                         | `Experimental (0%)` | `Beta (74%)` | `Stable (88%)` | No                |
| Profiles and Isolation              | 5            | [Multiple Gateways](/fr/gateway/multiple-gateways), [Index](/fr/gateway/index), [Gateway](/fr/cli/gateway)                                                                                                                                                                  | `Experimental (0%)` | `Beta (74%)` | `Stable (88%)` | No                |

#### macOS companion app

- Level: M3 Beta
- Rationale: Rich menu bar app, permissions, node mode, Canvas, voice wake, WebChat, and remote mode exist. Still fast-moving enough to avoid Stable.

| Area                | Capabilities | Docs                                                                                                                                                                                             | Coverage            | Quality       | Completeness | Long-term support |
| ------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- | ------------- | ------------ | ----------------- |
| Canvas              | 4            | [Canvas](/fr/platforms/mac/canvas), [Macos](/fr/platforms/macos), [Webchat](/fr/web/webchat)                                                                                                              | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |
| Local Setup         | 7            | [Bundled Gateway](/fr/platforms/mac/bundled-gateway), [Macos](/fr/platforms/macos), [Child Process](/fr/platforms/mac/child-process), [Dev Setup](/fr/platforms/mac/dev-setup)                               | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |
| Status and Settings | 5            | [Menu Bar](/fr/platforms/mac/menu-bar), [Icon](/fr/platforms/mac/icon), [Macos](/fr/platforms/macos), [Health](/fr/platforms/mac/health), [Logging](/fr/platforms/mac/logging), [Remote](/fr/platforms/mac/remote) | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |
| Native Capabilities | 5            | [Macos](/fr/platforms/macos), [Xpc](/fr/platforms/mac/xpc), [Permissions](/fr/platforms/mac/permissions), [Signing](/fr/platforms/mac/signing), [Peekaboo](/fr/platforms/mac/peekaboo)                          | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |
| Remote Connections  | 3            | [Remote](/fr/platforms/mac/remote), [Macos](/fr/platforms/macos), [Remote](/fr/gateway/remote)                                                                                                            | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |
| Voice and Talk      | 3            | [Voicewake](/fr/platforms/mac/voicewake), [Voice Overlay](/fr/platforms/mac/voice-overlay), [Talk](/fr/nodes/talk), [Macos](/fr/platforms/macos)                                                             | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |
| WebChat             | 3            | [Webchat](/fr/platforms/mac/webchat), [Macos](/fr/platforms/macos), [Webchat](/fr/web/webchat)                                                                                                            | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |
| Remote WebChat      | 5            | [Webchat](/fr/platforms/mac/webchat), [Remote](/fr/gateway/remote), [Remote](/fr/platforms/mac/remote)                                                                                                    | `Experimental (0%)` | `Alpha (66%)` | `Beta (78%)` | No                |

#### Linux Gateway host

- Level: M4 Stable
- Rationale: Node runtime is recommended, systemd user service is documented, and VPS/container guidance is broad.

| Area                                | Capabilities | Docs                                                                                                                                                                                       | Coverage            | Quality      | Completeness   | Long-term support |
| ----------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- | ------------ | -------------- | ----------------- |
| Host Setup and Updates              | 4            | [Index](/fr/install/index), [Updating](/fr/install/updating), [Linux](/fr/platforms/linux), [Index](/fr/platforms/index)                                                                               | `Experimental (0%)` | `Beta (75%)` | `Stable (89%)` | Yes               |
| Gateway Runtime and Service Control | 6            | [Index](/fr/gateway/index), [Gateway](/fr/cli/gateway), [Linux](/fr/platforms/linux), [Vps](/fr/vps)                                                                                                   | `Experimental (0%)` | `Beta (75%)` | `Stable (89%)` | Yes               |
| Remote Access and Security          | 6            | [Remote](/fr/gateway/remote), [Tailscale](/fr/gateway/tailscale), [Exposure Runbook](/fr/gateway/security/exposure-runbook), [Authentication](/fr/gateway/authentication), [Secrets](/fr/gateway/secrets) | `Experimental (0%)` | `Beta (75%)` | `Stable (89%)` | Yes               |
| Diagnostics and Repair              | 4            | [Status](/fr/cli/status), [Logs](/fr/cli/logs), [Doctor](/fr/cli/doctor), [Diagnostics](/fr/gateway/diagnostics), [Index](/fr/gateway/index)                                                              | `Experimental (0%)` | `Beta (75%)` | `Stable (89%)` | Yes               |
| Deployment Targets                  | 3            | [Vps](/fr/vps), [Docker](/fr/install/docker), [Hetzner](/fr/install/hetzner), [Digitalocean](/fr/install/digitalocean), [Kubernetes](/fr/install/kubernetes), [Podman](/fr/install/podman)                   | `Experimental (0%)` | `Beta (75%)` | `Stable (89%)` | No                |

#### Linux companion app

- Level: M0 Planned
- Rationale: Docs say native Linux companion apps are planned; Gateway is the supported Linux path today.

| Area                   | Capabilities | Docs                                                                                                                                                                                      | Coverage            | Quality              | Completeness         | Long-term support |
| ---------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | -------------------- | -------------------- | ----------------- |
| App Distribution       | 3            | [Linux](/fr/platforms/linux), [Index](/fr/platforms/index), [Index](/fr/install/index)                                                                                                             | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Gateway Connectivity   | 4            | [Linux](/fr/platforms/linux), [Index](/fr/gateway/index), [Pairing](/fr/gateway/pairing), [Remote](/fr/gateway/remote)                                                                                | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Chat and Sessions      | 3            | [Linux](/fr/platforms/linux), [Protocol](/fr/gateway/protocol), [Webchat](/fr/web/webchat)                                                                                                         | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Desktop Capabilities   | 9            | [Linux](/fr/platforms/linux), [Exec Approvals](/fr/tools/exec-approvals), [Secrets](/fr/gateway/secrets), [Index](/fr/nodes/index), [Exec](/fr/tools/exec), [Talk](/fr/nodes/talk), [Camera](/fr/nodes/camera) | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Status and Diagnostics | 7            | [Linux](/fr/platforms/linux), [Openclaw](/fr/start/openclaw), [Doctor](/fr/gateway/doctor)                                                                                                         | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |

#### Windows via WSL2

- Level: M3 Beta
- Rationale: Recommended Windows path with systemd/user-service guidance and boot-chain docs. Promote after repeated install/update scorecards.

| Area                        | Capabilities | Docs                                                                                                                                                                                              | Coverage             | Quality       | Completeness | Long-term support |
| --------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ------------- | ------------ | ----------------- |
| WSL Setup                   | 6            | [Windows](/fr/platforms/windows), [Getting Started](/fr/start/getting-started)                                                                                                                          | `Experimental (0%)`  | `Alpha (67%)` | `Beta (79%)` | Yes               |
| CLI                         | 8            | [Windows](/fr/platforms/windows), [Getting Started](/fr/start/getting-started), [Updating](/fr/install/updating), [Onboard](/fr/cli/onboard), [Doctor](/fr/cli/doctor), [Status](/fr/cli/status), [Logs](/fr/cli/logs) | `Experimental (0%)`  | `Alpha (67%)` | `Beta (79%)` | Yes               |
| Gateway Service Lifecycle   | 10           | [Windows](/fr/platforms/windows), [Index](/fr/gateway/index), [Doctor](/fr/gateway/doctor)                                                                                                                 | `Experimental (0%)`  | `Alpha (67%)` | `Beta (79%)` | Yes               |
| Gateway Access and Exposure | 11           | [Authentication](/fr/gateway/authentication), [Secrets](/fr/gateway/secrets), [Remote](/fr/gateway/remote), [Exposure Runbook](/fr/gateway/security/exposure-runbook), [Windows](/fr/platforms/windows)          | `Experimental (0%)`  | `Alpha (67%)` | `Beta (79%)` | Yes               |
| Diagnostics and Repair      | 6            | [Windows](/fr/platforms/windows), [Status](/fr/cli/status), [Logs](/fr/cli/logs), [Doctor](/fr/cli/doctor), [Doctor](/fr/gateway/doctor)                                                                         | `Experimental (17%)` | `Beta (79%)`  | `Beta (79%)` | Yes               |
| Browser and Control UI      | 6            | [Browser Wsl2 Windows Remote Cdp Troubleshooting](/fr/tools/browser-wsl2-windows-remote-cdp-troubleshooting), [Browser](/fr/tools/browser), [Control Ui](/fr/web/control-ui)                               | `Experimental (0%)`  | `Alpha (67%)` | `Beta (79%)` | No                |

#### Native Windows

- Level: M2 Alpha
- Rationale: Core CLI/Gateway flows work, but docs still recommend WSL2 for the full experience and list native caveats.

| Area               | Capabilities | Docs                                                                                                                                                        | Coverage            | Quality       | Completeness  | Long-term support |
| ------------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------- | ----------------- |
| CLI                | 9            | [Index](/fr/install/index), [Installer](/fr/install/installer), [Windows](/fr/platforms/windows), [Getting Started](/fr/start/getting-started), [Onboard](/fr/cli/onboard) | `Experimental (0%)` | `Alpha (54%)` | `Alpha (64%)` | Yes               |
| Gateway Management | 11           | [Windows](/fr/platforms/windows), [Index](/fr/gateway/index), [Gateway](/fr/cli/gateway), [Doctor](/fr/cli/doctor)                                                      | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Networking         | 4            | [Windows](/fr/platforms/windows), [Index](/fr/gateway/index), [Gateway](/fr/cli/gateway)                                                                             | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Updates            | 4            | [Updating](/fr/install/updating), [Ci](/fr/ci)                                                                                                                    | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |

#### Native Windows companion app

- Level: M0 Planned
- Rationale: Planned only.

| Area                          | Capabilities | Docs                                                                                                                                                 | Coverage            | Quality              | Completeness         | Long-term support |
| ----------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | -------------------- | -------------------- | ----------------- |
| Installation and Updates      | 4            | [Windows](/fr/platforms/windows), [Index](/fr/install/index)                                                                                               | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Gateway Connection            | 3            | [Windows](/fr/platforms/windows), [Index](/fr/gateway/index), [Pairing](/fr/gateway/pairing), [Remote](/fr/gateway/remote)                                       | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Chat Sessions                 | 2            | [Windows](/fr/platforms/windows), [Protocol](/fr/gateway/protocol)                                                                                         | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Status and Repair             | 5            | [Windows](/fr/platforms/windows), [Doctor](/fr/gateway/doctor), [Index](/fr/gateway/index)                                                                    | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |
| Desktop Tools and Permissions | 10           | [Windows](/fr/platforms/windows), [Index](/fr/nodes/index), [Exec](/fr/tools/exec), [Exec Approvals](/fr/tools/exec-approvals), [Index](/fr/gateway/security/index) | `Experimental (0%)` | `Experimental (19%)` | `Experimental (21%)` | No                |

#### Android app

- Level: M2 Alpha
- Rationale: Public Google Play path exists, but app docs still describe the rebuild as extremely alpha and call out release hardening work.

| Area             | Capabilities | Docs                                                                                                    | Coverage            | Quality       | Completeness  | Long-term support |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------- | ------------------- | ------------- | ------------- | ----------------- |
| Media Capture    | 1            | [Android](/fr/platforms/android), [Camera](/fr/nodes/camera)                                                  | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Mobile Chat      | 1            | [Android](/fr/platforms/android)                                                                           | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Connection Setup | 1            | [Android](/fr/platforms/android), [Bonjour](/fr/gateway/bonjour), [Pairing](/fr/gateway/pairing)                 | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Distribution     | 3            | [Android](/fr/platforms/android)                                                                           | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Settings         | 1            | [Android](/fr/platforms/android)                                                                           | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Voice            | 1            | [Android](/fr/platforms/android), [Talk](/fr/nodes/talk)                                                      | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |
| Device Runtime   | 2            | [Android](/fr/platforms/android), [Troubleshooting](/fr/nodes/troubleshooting), [Protocol](/fr/gateway/protocol) | `Experimental (0%)` | `Alpha (59%)` | `Alpha (66%)` | No                |

#### iOS app

- Level: M1 Experimental
- Rationale: Internal preview / super-alpha. TestFlight and relay-backed push flows exist, but no public distribution yet.

| Area                          | Capabilities | Docs                                                                                                    | Coverage            | Quality              | Completeness         | Long-term support |
| ----------------------------- | ------------ | ------------------------------------------------------------------------------------------------------- | ------------------- | -------------------- | -------------------- | ----------------- |
| Media and Sharing             | 1            | [Ios](/fr/platforms/ios), [Camera](/fr/nodes/camera)                                                          | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Canvas and Screen             | 1            | [Ios](/fr/platforms/ios), [Canvas](/fr/plugins/reference/canvas)                                              | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Chat and Sessions             | 1            | [Ios](/fr/platforms/ios), [Webchat](/fr/web/webchat), [Protocol](/fr/gateway/protocol)                           | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Gateway Setup and Diagnostics | 7            | [Ios](/fr/platforms/ios), [Pairing](/fr/channels/pairing)                                                     | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Distribution                  | 1            | [Ios](/fr/platforms/ios)                                                                                   | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Device Commands               | 2            | [Ios](/fr/platforms/ios), [Protocol](/fr/gateway/protocol)                                                    | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Notifications and Background  | 1            | [Ios](/fr/platforms/ios), [Configuration](/fr/gateway/configuration)                                          | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Voice                         | 1            | [Ios](/fr/platforms/ios), [Talk](/fr/nodes/talk)                                                              | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |

#### watchOS companion surfaces

- Level: M1 Experimental
- Rationale: Source has Watch app/extension surfaces; public docs do not yet present this as a user feature.

| Area                      | Capabilities | Docs                                                           | Coverage            | Quality              | Completeness         | Long-term support |
| ------------------------- | ------------ | -------------------------------------------------------------- | ------------------- | -------------------- | -------------------- | ----------------- |
| Delivery and Recovery     | 7            | [Ios](/fr/platforms/ios)                                          | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Exec Approvals            | 3            | [Exec Approvals](/fr/tools/exec-approvals), [Ios](/fr/platforms/ios) | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Distribution and Support  | 6            | [Ios](/fr/platforms/ios)                                          | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Notifications and Replies | 7            | [Ios](/fr/platforms/ios)                                          | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |
| Watch App UI              | 3            | [Ios](/fr/platforms/ios)                                          | `Experimental (0%)` | `Experimental (41%)` | `Experimental (44%)` | No                |

#### Raspberry Pi and small Linux devices

- Level: M3 Beta
-
