---
title: "Rapport de maturité Voice and realtime talk"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité Voice and realtime talk

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Beta (73%)`
- Qualité : `Alpha (67%)`
- Complétude : `Beta (73%)`
- Fonctionnalités LTS : `0/6`

## Résumé

Ce rapport promeut les preuves de maturité archivées `voice-and-realtime-talk` de `/Users/kevinlin/tmp/maturity/voice-and-realtime-talk` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                      | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Talk Providers](talk-configuration-catalog-and-provider-selection.md)        | ❌  | `Beta (74%)`  | `Alpha (68%)` | `Beta (74%)`  | Pont backend OpenAI Realtime voice, pont backend Google Gemini Live, contrats SDK de fournisseur de voix en temps réel, diagnostics de fournisseur, catalogue Talk, configuration du fournisseur Talk, analyse de configuration native partagée                                                                                  |
| [Realtime Talk Sessions](gateway-relay-and-realtime-session-runtime.md)       | ❌  | `Beta (72%)`  | `Alpha (68%)` | `Beta (72%)`  | Transfert de consultation d'agent, statut d'exécution d'agent Talk actif, comportement d'exécution Talkback, planification de consultation forcée, interface utilisateur de démarrage/arrêt Talk du navigateur, sessions WebRTC du navigateur, mode relais du navigateur, transfert d'appel d'outil du navigateur, contrôles de session en temps réel, sessions de relais de passerelle, limites de trames audio |
| [Speech and Transcription](speech-transcription-directives-and-talk-speak.md) | ❌  | `Beta (72%)`  | `Alpha (68%)` | `Beta (72%)`  | Directives vocales, lecture de parole Talk, sessions de relais de transcription, fournisseurs de transcription en temps réel, analyse de directive native                                                                                                                                                        |
| [Native App Talk](native-app-talk-loops-ios-android-macos.md)                 | ❌  | `Alpha (68%)` | `Alpha (64%)` | `Alpha (68%)` | Mode Talk natif macOS, mode Talk iOS, mode Talk Android, configuration Talk partagée                                                                                                                                                                                                            |
| [Voice Wake and Routing](voice-wake-push-to-talk-and-routing.md)              | ❌  | `Beta (74%)`  | `Alpha (66%)` | `Beta (74%)`  | Paramètres de mot de réveil, routage de réveil, exécution Voice Wake macOS, préférences de réveil mobile                                                                                                                                                                                                     |
| [Talk Observability](observability-diagnostics-session-health-and-latency.md) | ❌  | `Beta (76%)`  | `Beta (70%)`  | `Beta (76%)`  | Journalisation des événements Talk, santé du journal de session, sortie de fumée en direct, compteurs de diagnostic Prometheus, visibilité de l'opérateur sur la configuration                                                                                                                                                               |

## Rubrique de notation

- Couverture :
  évaluation du libellé de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/exécution
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation du libellé de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux d'exécution réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation du libellé de maturité pour la façon dont la catégorie fournit complètement l'ensemble de capacités
  spécifique à la surface. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  libellé de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire de fonctionnalités détaillé plutôt que comme
  dimension notée séparée.

## Inventaire de fonctionnalités détaillé

### 1. Talk Providers

Ancres de recherche : OpenAI Realtime, Google Gemini Live, fournisseur de voix en temps réel, talk.catalog, talk.config.

Note de catégorie : [Talk Providers](talk-configuration-catalog-and-provider-selection.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Pont backend OpenAI Realtime voice : Pont backend OpenAI Realtime voice et chemin d'authentification WebRTC du navigateur
- Pont backend Google Gemini Live : Pont backend Google Gemini Live et chemin token/WebSocket du navigateur
- Contrats SDK de fournisseur de voix en temps réel : Contrats SDK de fournisseur de voix en temps réel, métadonnées d'activation, registre de fournisseur et résolveur
- Diagnostics de fournisseur : Diagnostics de fournisseur, comportement de reconnexion, déclarations d'outils et cycle de vie de session de pont
- Catalogue Talk : Découverte du catalogue Talk pour les fournisseurs de transport, cerveau, parole, voix en temps réel et transcription.
- Configuration du fournisseur Talk : Sélection du fournisseur Talk, paramètres en temps réel spécifiques au fournisseur et règles d'exposition des secrets.
- Analyse de configuration native partagée : Analyse de configuration native partagée pour macOS, iOS et Android

Docs principaux :

- `docs/providers/openai.md`
- `docs/providers/google.md`
- `docs/plugins/sdk-provider-plugins.md`
- `docs/nodes/talk.md`
- `docs/web/control-ui.md`

### 2. Realtime Talk Sessions

Ancres de recherche : Statut d'exécution d'agent Talk, talkback, transfert de consultation, démarrage/arrêt Talk du navigateur, OpenAI WebRTC, mode relais du navigateur, talk.session.create, appendAudio, cancelTurn, submitToolResult.

Note de catégorie : [Realtime Talk Sessions](gateway-relay-and-realtime-session-runtime.md)

Décisions de notation :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Transfert de consultation d'agent : Comportement de transfert de consultation entre les sessions Talk actives et les exécutions d'agent.
- Statut d'exécution d'agent Talk actif : Statut d'exécution d'agent Talk actif, annulation, direction et contrôles de suivi
- Comportement d'exécution Talkback : Comportement d'exécution Talkback et coordination de la parole de l'assistant
- Planification de consultation forcée : Planification de consultation forcée et propagation d'événement de contrôle
- Interface utilisateur de démarrage/arrêt Talk du navigateur : Interface utilisateur de démarrage/arrêt Talk du navigateur et affichage du statut
- Sessions WebRTC du navigateur : Sessions WebRTC du navigateur pour les fournisseurs OpenAI Realtime et Google Live.
- Mode relais du navigateur : Mode relais du navigateur pour les fournisseurs de voix en temps réel backend uniquement.
- Transfert d'appel d'outil du navigateur : Transfert d'appel d'outil du navigateur, événements de transcription et lecture audio
- Contrôles de session en temps réel : Création de session en temps réel, ajout audio, annulation de tour, direction, soumission de résultat d'outil et contrôles de fermeture.
- Sessions de relais de passerelle : Sessions de relais de passerelle pour les flux de voix en temps réel et de transcription.
- Limites de trames audio : Limites de trames audio, TTL de session, limites par connexion/globales, événements de transcription et nettoyage de relais

Docs principaux :

- `docs/nodes/talk.md`
- `docs/web/control-ui.md`

### 3. Speech and Transcription

Ancres de recherche : talk.speak, directives vocales, sessions de relais de transcription.

Note de catégorie : [Speech and Transcription](speech-transcription-directives-and-talk-speak.md)

Décisions de notation :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Directives vocales : Directives vocales et suppression de directive avant la lecture TTS.
- Lecture de parole Talk : Passerelle talk.speak et comportement TTS de secours.
- Sessions de relais de transcription : Sessions de relais de transcription de passerelle, événements de transcription et comportement de nettoyage.
- Fournisseurs de transcription en temps réel : Sélection de fournisseur de transcription en temps réel, diagnostics et comportement de pont spécifique au fournisseur.
- Analyse de directive native : Analyse de directive native et comportement de locale de parole Talk

Docs principaux :

- `docs/nodes/talk.md`
- `docs/providers/openai.md`
- `docs/providers/google.md`

### 4. Native App Talk

Ancres de recherche : Mode Talk natif macOS, mode Talk iOS, mode Talk Android.

Note de catégorie : [Native App Talk](native-app-talk-loops-ios-android-macos.md)

Décisions de notation :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (64%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Mode Talk natif macOS : Mode Talk natif macOS, reconnaissance vocale, lecture TTS et transfert push-to-talk
- Mode Talk iOS : Mode Talk iOS, sessions WebRTC, sessions de relais en temps réel et préférences de réveil
- Mode Talk Android : Mode Talk Android, mode de reconnaissance vocale, relais en temps réel, capture de micro et récepteur E2E de débogage
- Configuration Talk partagée : Configuration Talk partagée et analyse de commande

Docs principaux :

- `docs/nodes/talk.md`
- `docs/platforms/mac/voicewake.md`

### 5. Voice Wake and Routing

Ancres de recherche : Voice Wake, push-to-talk, paramètres de mot de réveil.

Note de catégorie : [Voice Wake and Routing](voice-wake-push-to-talk-and-routing.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Paramètres de mot de réveil : Paramètres de mot de réveil et préférences de routage appartenant à la passerelle.
- Routage de réveil : Méthodes de routage par défaut, dernière application active, application locale et nœud spécifique.
- Exécution Voice Wake macOS : Exécution Voice Wake macOS, hotkey push-to-talk, adoption de superposition, comportement pause/reprise et transfert
- Préférences de réveil mobile : Préférences de réveil iOS et Android et extraction de commande.

Docs principaux :

- `docs/nodes/voicewake.md`
- `docs/platforms/mac/voicewake.md`
- `docs/platforms/mac/voice-overlay.md`

### 6. Talk Observability

Ancres de recherche : Journalisation des événements Talk, santé du journal de session, visibilité de la latence.

Note de catégorie : [Talk Observability](observability-diagnostics-session-health-and-latency.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Journalisation des événements Talk : Journalisation des événements Talk et mappage des événements de diagnostic
- Santé du journal de session : Santé du journal de session, enregistrements de transcription, événements de pont et suppression d'écho/sortie
- Sortie de fumée en direct : Sortie de fumée en direct et inspection des événements de fournisseur
- Compteurs de diagnostic Prometheus : Compteurs de diagnostic Prometheus pour les événements Talk
- Visibilité de l'opérateur sur la configuration : Visibilité de l'opérateur sur la configuration, la latence et les modes de défaillance

Docs principaux :

- `docs/web/control-ui.md`
- `docs/platforms/mac/voice-overlay.md`
- `docs/nodes/talk.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les documents, les ancres de recherche et les fonctionnalités.

## Provenance d'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/voice-and-realtime-talk/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/voice-and-realtime-talk`.
