---
title: "Rapport de maturité du canal Voice Call"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du canal Voice Call

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Experimental (49%)`
- Qualité : `Alpha (58%)`
- Complétude : `Experimental (49%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `voice-call-channel` depuis `/Users/kevinlin/tmp/maturity/voice-call-channel` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                      | LTS | Couverture           | Qualité       | Complétude           | Fonctionnalités à évaluer                  |
| ------------------------------------------------------------------------------ | --- | -------------------- | ------------- | -------------------- | ------------------------------------------ |
| [Configuration et opérations du canal](setup-configuration-and-smoke.md)       | ❌  | `Experimental (42%)` | `Alpha (56%)` | `Experimental (42%)` | Voice Call Channel, Voice Call Channel     |
| [Accès et identité](webhook-exposure-and-security.md)                         | ❌  | `Alpha (60%)`        | `Alpha (62%)` | `Alpha (60%)`        | Voice Call Channel                         |
| [Routage et livraison des conversations](inbound-routing-sessions-and-lifecycle.md) | ❌  | `Alpha (52%)`        | `Alpha (58%)` | `Alpha (52%)`        | Voice Call Channel                         |
| [Médias et contenu enrichi](provider-transports-and-call-control.md)           | ❌  | `Experimental (48%)` | `Alpha (57%)` | `Experimental (48%)` | Voice Call Channel, Voice Call Channel     |
| [Voix en temps réel et appels](realtime-voice-and-agent-consult.md)            | ❌  | `Experimental (44%)` | `Alpha (55%)` | `Experimental (44%)` | Voice Call Channel, Voice Call Channel     |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une
  fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; ils
  ne modifient pas la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations du canal

Ancres de recherche : voice call channel voice call channel: cli, gateway rpc, and agent tool, voice call channel: cli, gateway rpc, and agent tool, voice call channel voice call channel: setup, configuration, and smoke, voice call channel: setup, configuration, and smoke.

Note de catégorie : [Configuration et opérations du canal](setup-configuration-and-smoke.md)

Décisions de notation :

- Couverture : `Experimental (42%)`
- Qualité : `Alpha (56%)`
- Complétude : `Experimental (42%)`
- LTS : ❌

Fonctionnalités :

- Voice Call Channel: Cli, Gateway Rpc, and Agent Tool
- Voice Call Channel: Setup, Configuration, and Smoke

Documentation principale :

- `docs/cli/voicecall.md`
- `docs/plugins/voice-call.md`
- `docs/gateway/protocol.md`

### 2. Accès et identité

Ancres de recherche : voice call channel voice call channel: webhook exposure and security, voice call channel: webhook exposure and security.

Note de catégorie : [Accès et identité](webhook-exposure-and-security.md)

Décisions de notation :

- Couverture : `Alpha (60%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (60%)`
- LTS : ❌

Fonctionnalités :

- Voice Call Channel: Webhook Exposure and Security

Documentation principale :

- `docs/plugins/voice-call.md`
- `docs/cli/voicecall.md`

### 3. Routage et livraison des conversations

Ancres de recherche : voice call channel voice call channel: inbound routing, sessions, and lifecycle, voice call channel: inbound routing, sessions, and lifecycle.

Note de catégorie : [Routage et livraison des conversations](inbound-routing-sessions-and-lifecycle.md)

Décisions de notation :

- Couverture : `Alpha (52%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (52%)`
- LTS : ❌

Fonctionnalités :

- Voice Call Channel: Inbound Routing, Sessions, and Lifecycle

Documentation principale :

- `docs/plugins/voice-call.md`

### 4. Médias et contenu enrichi

Ancres de recherche : voice call channel voice call channel: provider transports and call control, voice call channel: provider transports and call control, voice call channel voice call channel: telephony tts, playback, dtmf, and audio, voice call channel: telephony tts, playback, dtmf, and audio.

Note de catégorie : [Médias et contenu enrichi](provider-transports-and-call-control.md)

Décisions de notation :

- Couverture : `Experimental (48%)`
- Qualité : `Alpha (57%)`
- Complétude : `Experimental (48%)`
- LTS : ❌

Fonctionnalités :

- Voice Call Channel: Provider Transports and Call Control
- Voice Call Channel: Telephony Tts, Playback, Dtmf, and Audio

Documentation principale :

- `docs/plugins/voice-call.md`
- `docs/plugins/plugin-inventory.md`

### 5. Voix en temps réel et appels

Ancres de recherche : voice call channel voice call channel: realtime voice and agent consult, voice call channel: realtime voice and agent consult, voice call channel voice call channel: streaming transcription and auto-response, voice call channel: streaming transcription and auto-response.

Note de catégorie : [Voix en temps réel et appels](realtime-voice-and-agent-consult.md)

Décisions de notation :

- Couverture : `Experimental (44%)`
- Qualité : `Alpha (55%)`
- Complétude : `Experimental (44%)`
- LTS : ❌

Fonctionnalités :

- Voice Call Channel: Realtime Voice and Agent Consult
- Voice Call Channel: Streaming Transcription and Auto-response

Documentation principale :

- `docs/plugins/voice-call.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/voice-call-channel/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/voice-call-channel`.
