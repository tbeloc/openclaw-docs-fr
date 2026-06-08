---
title: "Discord - Realtime Voice and Calls Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Realtime Voice and Calls Maturity Note

## Summary

Les canaux vocaux Discord en temps réel ont une implémentation substantielle et une suite de flux d'exécution simulés large couvrant `/vc`, auto-join, `followUsers`, STT/TTS, `agent-proxy`/`bidi` en temps réel, noms de réveil, barge-in, récupération DAVE, et `libopus-wasm`. La preuve en direct est plus étroite : la voie QA en direct vérifie l'auto-join vocal Discord par rapport à l'API d'état vocal de Discord, mais je n'ai pas trouvé de boucle vocale Discord en direct qui prouve la capture réelle du microphone, la transcription du fournisseur en temps réel, l'activation du nom de réveil, le barge-in, et la lecture ensemble.

Le composant est donc bêta sur Coverage et alpha sur Quality. La qualité est limitée par les problèmes GitHub actifs et les rapports de support Discord pour les échecs de connexion, les échecs de réception DAVE/déchiffrement, les lacunes de l'adaptateur de sortie vocale, et la confusion des utilisateurs autour de `/vc`.

## Normalization

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Realtime Voice and Calls`
- Fusionnée à partir de : `Realtime Voice`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Category Scope

Inclus dans cette catégorie :

- Voice Channel Lifecycle : Couvre le cycle de vie des canaux vocaux sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Auto-join and follow-users : Couvre l'auto-join et follow-users sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Realtime voice modes : Couvre les modes vocaux en temps réel sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Wake, barge-in, and echo handling : Couvre le réveil, le barge-in, et la gestion de l'écho sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Voice codec and DAVE recovery : Couvre le codec vocal et la récupération DAVE sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.

## Features

- Voice Channel Lifecycle : Couvre le cycle de vie des canaux vocaux sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Auto-join and follow-users : Couvre l'auto-join et follow-users sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Realtime voice modes : Couvre les modes vocaux en temps réel sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Wake, barge-in, and echo handling : Couvre le réveil, le barge-in, et la gestion de l'écho sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.
- Voice codec and DAVE recovery : Couvre le codec vocal et la récupération DAVE sur les sessions de canaux vocaux Discord contrôlées par `/vc join`, `/vc status`, et `/vc leave` ; `autoJoin` piloté par configuration ; `followUsers` ; listes blanches de canaux vocaux/stage ; gestion de la connexion/reconnexion et DAVE ; comportement des canaux vocaux en temps réel `stt-tts`, `agent-proxy`, et associés.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score : `Beta (74%)`
- Signaux positifs :
  - La preuve du flux d'exécution est large. `extensions/discord/src/voice/manager.e2e.test.ts` exerce la configuration désactivée, les flux du gestionnaire `/vc` join/status/leave, l'auto-join dupliqué, la suppression de l'auto-join fatal, les listes blanches, `followUsers`, les mouvements de bot, le barge-in en temps réel, les options et la récupération DAVE, le nettoyage de session en temps réel, `agent-proxy` par défaut, les appels d'outils de contrôle d'agent, les remplacements de modèle/voix, le gating du nom de réveil, la correspondance floue du nom de réveil, le forçage du recours à la consultation, `bidi`, le contexte du haut-parleur, l'autorisation avant l'abonnement, le nettoyage `libopus-wasm`, le TTS en continu, l'aperçu de la transcription, et l'auto-join Ready/Resumed.
  - La couverture Discord en direct existe pour la présence des canaux vocaux. `extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts` définit `discord-voice-autojoin`, mute la configuration de la passerelle avec `channels.discord.voice.enabled=true` et `autoJoin`, résout un canal vocal/stage explicite ou visible, et interroge `/guilds/{guildId}/voice-states/@me` de Discord jusqu'à ce que le bot soit dans le canal attendu.
- Signaux négatifs :
  - Je n'ai pas trouvé de preuve en direct qu'un utilisateur Discord réel peut parler dans un canal vocal et compléter la boucle complète microphone-agent-lecture via `agent-proxy` ou `bidi` en temps réel.
  - La voie QA en direct valide la résidence d'état vocal, pas la réception audio réelle, STT, les événements du fournisseur en temps réel, l'activation du nom de réveil, la récupération de réception DAVE, la suppression d'écho, le barge-in, ou la lecture sortante.
  - Le comportement de la commande `/vc` est couvert par la preuve du flux d'exécution simulé et au niveau unitaire, mais je n'ai pas trouvé de scénario de commande slash Discord end-to-end en direct pour `/vc join`, `/vc status`, et `/vc leave`.
  - Les défaillances Windows/event-loop et Discord voice websocket restent ouvertes dans Gitcrawl, ce qui suggère que certains chemins d'exécution ne sont pas entièrement couverts par des portes en direct répétables.
- Lacunes d'intégration :
  - Ajouter un scénario de parole Discord en direct qui rejoint un canal vocal, injecte ou joue de l'audio déterministe, vérifie la transcription/réponse de l'agent, et observe la lecture Discord.
  - Ajouter une couverture en direct pour les conversations requises par nom de réveil, le barge-in pendant que le bot parle, la suppression d'écho, et le forçage du recours à la consultation.
  - Ajouter une couverture en direct de récupération DAVE/déchiffrement qui prouve le chemin actuel `libopus-wasm` et de récupération de réception sous le comportement vocal actuel de Discord.
  - Ajouter une couverture en direct de commande `/vc join/status/leave` séparée de l'auto-join piloté par configuration.

## Score de Qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl :
  - Les problèmes ouverts incluent `/vc join` échouant sur Windows avec `AggregateError` plus timeout de heartbeat de passerelle/famine de boucle d'événements (#80344), fermeture de websocket vocal avant poignée de main UDP (#65039), `/voice list` ne retournant aucune voix utilisable et audio sortant uniquement statut (#80010), échecs de réception DAVE avec `UnencryptedWhenPassthroughDisabled` (#81518), et une demande de fonctionnalité voix-en-tant-qu'IO/routage de session toujours ouverte (#73699).
  - Les PR ouvertes autour de ce domaine incluent groupes vocaux à portée de compte plus filet de sécurité d'auto-join retardé (#87530), secours lorsque l'adaptateur vocal est indisponible (#84965), comportement audio dégradé en tant que voix lorsque l'adaptateur vocal est indisponible (#85173), préservation de l'assistant vocal sortant Discord (#85529), et un `/vc switch` de transfert proposé (#60902).
  - Aucun résultat Gitcrawl n'a été trouvé pour `libopus wasm discord voice` ou `discord voice realtime wake barge`, donc l'archive a une traçabilité limitée des problèmes/PR pour certains des mécanismes de qualité les plus récents.
- Rapports Discrawl :
  - La recherche Discord pour `discord voice` montre une discussion récente de version/support autour du choix plus net de voix/modèle Discord et du suivi Talk/voix, mais aussi le routage du support pour les problèmes spécifiques à la voix Discord.
  - La recherche Discord pour `vc join` inclut la confusion des utilisateurs selon laquelle la commande `/vc` était manquante et une réponse du mainteneur/bot selon laquelle un runtime donné ne pouvait pas rejoindre VC car seules les actions texte/message Discord étaient exposées.
  - La recherche Discord pour `libopus` montre une note du mainteneur selon laquelle OpenClaw a créé `openclaw/libopus-wasm` car la qualité de dépendance Discord était faible, ce qui est une atténuation positive mais aussi une preuve que cette surface dépendait d'un emballage de codec en amont fragile.
  - La recherche Discord pour `UnencryptedWhenPassthroughDisabled` montre plusieurs fils de support autour de la rupture de réception vocale, `/vc status` signalant prêt alors qu'aucune réponse STT n'arrive, boucles de reconnexion, bugs de réception DAVE/E2EE, et échecs de chargement de dépendance.
- Bonnes qualités :
  - La voix est optionnelle, et `voice/config.ts` ne l'active que lorsqu'une configuration vocale explicite est présente ou activée.
  - La gestion de la commande `/vc` contrôle l'accès via `authorizeDiscordVoiceIngress`, valide le type de canal, vérifie l'accès au canal, et signale les résultats clairs de join/status/leave.
  - `voice/manager.ts` sérialise les joins, déduplique l'auto-join, applique `allowedChannels`, gère les mouvements de bot en dehors des canaux autorisés, réconcilie `followUsers`, et limite certains travaux de recherche de guilde/membre.
  - DAVE et la récupération de réception sont de première classe dans la source : la config porte les options DAVE, les erreurs de réception sont classifiées, les échecs de déchiffrement répétés déclenchent la récupération, et l'état de préchauffage/passthrough est suivi.
  - `libopus-wasm` supprime la dépendance aux packages Opus natifs pour le chemin principal de réception/décodage et est également utilisé pour l'encodage de lecture.
  - La source en temps réel a des noms de réveil explicites par défaut et des noms de réveil configurés, des seuils de barge-in, le suivi de l'activité de sortie, le secours de consultation forcé, les aperçus de transcription limités, et les contrôles de politique de sortie vocale.
  - Les docs sont inhabituellement détaillées pour cette surface, couvrant la configuration, `/vc`, l'auto-join, les modes, les noms de réveil, DAVE, `followUsers`, `libopus-wasm`, STT/TTS, et l'automatisation QA en direct.
- Mauvaises qualités :
  - Les problèmes actifs montrent un comportement de join et de réception fragile dans les déploiements réels, incluant la famine Windows/boucle d'événements, la fermeture précoce de websocket vocal, les échecs de réception DAVE, et l'audio sortant uniquement statut.
  - L'ensemble de PR adaptateur/assistant sortant suggère que l'emballage et la disponibilité du runtime de la sortie vocale sont toujours en cours de durcissement.
  - La documentation n'est pas parfaitement alignée : `docs/gateway/config-channels.md` dit que la lecture n'est pas interrompue par les événements de démarrage du haut-parleur, tandis que les docs/source Discord plus récentes décrivent le comportement de barge-in en temps réel ; `docs/providers/openai.md` décrit toujours la voix Discord utilisant la transcription par lot de segment court dans une section qui peut lire obsolète à côté des docs `agent-proxy` en temps réel.
  - La découverte de commande visible par l'utilisateur semble fragile selon les rapports de support Discord pour `/vc` manquant et les runtimes qui exposent uniquement les actions texte.
- Exclu de la qualité :
  - Les tests unitaires, tests d'intégration, tests e2e, tests en direct, et la couverture du flux d'exécution n'ont pas été utilisés pour augmenter ou diminuer ce score de Qualité.

## Score de Complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl, et les preuves Discrawl couvrent la portée de la taxonomie pour Cycle de vie du canal vocal, Auto-join et follow-users, Modes vocaux en temps réel, Réveil, barge-in, et gestion de l'écho, Codec vocal et récupération DAVE.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- La validation complète de la parole Discord en direct est manquante pour la promesse en temps réel de base : audio utilisateur en entrée, transcription/événements du fournisseur, consultation d'agent, sortie TTS ou lecture en temps réel.
- L'automatisation réelle de la commande Discord `/vc join/status/leave` n'est pas visible dans la voie QA en direct ; la voie en direct visible utilise l'auto-join piloté par configuration et l'interrogation de l'état vocal Discord.
- La récupération DAVE/déchiffrement est implémentée et simulée, mais l'archive contient toujours des échecs d'utilisateurs réels récents autour du comportement de réception Discord actuel.
- Les docs ont besoin d'une passe d'alignement sur les pages Discord, fournisseur OpenAI, et configuration de passerelle afin que les utilisateurs puissent dire quand le chemin est en temps réel `agent-proxy`/`bidi` par rapport à la transcription/TTS par lot de segment court.
- La disponibilité de l'adaptateur vocal et l'emballage semblent toujours être des domaines de durcissement actifs selon les problèmes ouverts et les PR.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1163` documente les canaux vocaux Discord comme surface vocale prise en charge et distingue les canaux vocaux en temps réel des pièces jointes de messages vocaux.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1178` documente `/vc join channel:<voice-channel-id>`, `/vc status`, `/vc leave`, et la détection de capacités.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1190` documente la configuration `channels.discord.voice` avec `enabled`, `model`, `autoJoin`, `allowedChannels`, DAVE, les délais de connexion/reconnexion, et les paramètres du fournisseur/modèle/voix en temps réel.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1228` documente `voice.mode`, par défaut `agent-proxy`, `stt-tts`, `bidi`, `voice.agentSession`, `followUsers`, la politique de consultation/outil, les fichiers de contexte d'amorçage, et les noms de réveil.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1238` documente la compatibilité des alias d'événements en temps réel, l'interruption, la durée minimale d'interruption, la voix TTS, l'invite système, les listes blanches, l'opt-in `GuildVoiceStates`, les valeurs par défaut DAVE, `libopus-wasm`, le comportement de rétroaction STT/TTS, la gestion de l'écho, l'aperçu des transcriptions, et la gestion des fragments de consultation forcée.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1263` documente `followUsers`, le comportement auto-join par rapport à `/vc` par rapport au suivi, et `libopus-wasm` pour la réception, la lecture en temps réel, et la lecture de fichiers.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1310` documente le pipeline STT plus TTS via PCM-to-WAV, `tools.media.audio`, l'entrée/routage Discord, et la politique de sortie vocale.
- `/Users/kevinlin/code/openclaw/docs/providers/openai.md:654` documente OpenAI STT pour les segments de canaux vocaux Discord et les pièces jointes, tandis que les lignes ultérieures décrivent le chemin Discord comme des segments courts et la transcription par lot.
- `/Users/kevinlin/code/openclaw/docs/providers/elevenlabs.md:49` documente ElevenLabs streaming TTS pour les canaux vocaux Discord lorsqu'il est sélectionné.
- `/Users/kevinlin/code/openclaw/docs/concepts/qa-e2e-automation.md:411` documente `OPENCLAW_QA_DISCORD_VOICE_CHANNEL_ID` et `discord-voice-autojoin`, qui vérifie l'état vocal Discord du bot SUT.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:354` documente la configuration vocale, DAVE, les reconnexions, et la récupération de décryptage, mais inclut la déclaration d'apparence obsolète selon laquelle les événements de démarrage du haut-parleur n'interrompent pas la lecture.
- `/Users/kevinlin/code/openclaw/CHANGELOG.md:90` enregistre la réutilisation du SDK en temps réel partagé pour l'attribution du haut-parleur Discord, la lecture/interruption, la correspondance de consultation, et la correspondance du nom d'activation.
- `/Users/kevinlin/code/openclaw/CHANGELOG.md:1657` enregistre l'implémentation majeure du canal vocal en temps réel Discord, y compris `agent-proxy`, la session cible, la gestion de l'interruption/écho, le repli de consultation forcée, et l'aperçu des transcriptions.

## Source

- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/command.ts:22` définit les types de canaux vocaux/scène ; les gestionnaires de commandes ultérieurs autorisent et implémentent `/vc join`, `/vc leave`, et `/vc status`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.ts:276` définit `DiscordVoiceManager`, y compris le suivi des sessions, `allowedChannels`, `followUsers`, et l'activation vocale opt-in.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.ts:339` gère l'auto-join, la configuration de guilde dupliquée, la suppression du démarrage fatal, et la réconciliation des utilisateurs suivis.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.ts:426` implémente la validation de jointure, la sérialisation, la configuration DAVE, les attentes Ready, la résolution d'itinéraire, la configuration de session/lecteur, et l'attachement de session en temps réel.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.ts:967` réagit aux mises à jour d'état vocal, aux mouvements de bot, aux mouvements d'utilisateurs suivis, et aux flux de départ/réunion.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.ts:1510` gère la capture de démarrage du haut-parleur, la suppression de lecture non-temps réel, et l'interruption en temps réel.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.ts:1565` gère les flux de réception, les chunks en temps réel, le décodage STT/TTS, le passage DAVE, et le traitement des segments.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.ts:1769` classe les erreurs de réception et déclenche la récupération lorsque les défaillances de réception répétées dépassent le seuil.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/realtime.ts:101` définit `stt-tts`, `agent-proxy`, et `bidi` ; le code ultérieur résout `agent-proxy` par défaut, les noms de réveil, les options de connexion, la politique de consultation, l'interruption, la lecture, la gestion des transcriptions, et le repli de consultation forcée.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/audio.ts:4` importe `libopus-wasm` ; le code ultérieur crée le décodeur, l'encodeur, le flux de lecture, et le flux de décodage.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/ingress.ts:64` autorise l'entrée vocale et achemine les tours vocaux via `agentCommandFromIngress`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/receive-recovery.ts:3` définit les seuils de défaillance de réception, les marqueurs DAVE, l'expiration du passage, et les décisions de récupération.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/realtime-voice.ts:53` exporte les primitives SDK en temps réel partagées pour les noms d'activation, la coordination de consultation forcée, le suivi de sortie, les outils de consultation, les contrôles de rétroaction, la santé, la transcription, et la suppression d'écho.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:554` couvre le rejet de jointure lorsque la configuration vocale est absente.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:1003` couvre la gestion de l'auto-join dupliqué ; `:1026` couvre la suppression répétée de l'auto-join fatal.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:1044` et `:1062` couvrent le rejet et l'acceptation des canaux sur liste blanche.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:1077` à `:1494` couvrent `followUsers`, les mouvements, les départs, les transferts, les canaux non autorisés, et la réconciliation bornée.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:1531` et `:1546` couvrent les listes blanches vides et les mouvements de bot en dehors des canaux autorisés.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:1616`, `:1637`, `:1690`, et `:1880` couvrent la suppression de lecture et le comportement d'interruption en temps réel.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:1913` à `:2186` couvrent les options DAVE, le comportement de délai d'attente/nouvelle tentative Ready, la grâce de reconnexion, et le nettoyage de session en temps réel.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:2209`, `:2306`, et `:2697` couvrent `agent-proxy` par défaut, les appels d'outils de contrôle d'agent, et les remplacements de modèle/voix en temps réel.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:2737` à `:4245` couvrent la transcription/contrôle d'exécution active, la consultation forcée, les exigences de nom de réveil, l'accusé de réception partiel du réveil, le nom de réveil OpenClaw par défaut, la correspondance/rejet flou du réveil, la réutilisation du repli forcé, et la prévention des réponses obsolètes.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:4461` à `:4817` couvrent `bidi`, le routage de session configuré, le contexte du haut-parleur, l'expiration du tour, et l'autorisation du haut-parleur avant l'abonnement.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:4889` à `:5112` couvrent le passage DAVE, la réunion de récupération, la préservation de la propriété de suivi, la réinitialisation audio en temps réel, le nettoyage `libopus-wasm`, la préservation de l'état de défaillance du décodeur, et les segments partiels non-temps réel après abandon.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/manager.e2e.test.ts:5225` à `:5730` couvrent la grâce du silence, les haut-parleurs sur liste blanche/politique ouverte, le contrôle STT/TTS, le remplacement de modèle, la politique de sortie vocale, l'aperçu des transcriptions, le TTS en continu, les remplacements d'invite système, le cache du haut-parleur/récupération de rôle, l'ordre des métadonnées de guilde, et l'auto-join Ready/Resumed.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:331` définit le scénario en direct `discord-voice-autojoin`.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:499` injecte la configuration d'auto-join vocal pour ce scénario.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:568` résout les canaux vocaux/scène pour le scénario en direct.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:615` interroge l'état vocal Discord pour le bot dans le canal cible.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:1622` mute la configuration de passerelle pour le scénario vocal, et `:1687` attend l'état vocal cible avant de passer.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/discord/src/config-schema.test.ts:166` valide le modèle vocal, `agentSession`, les champs de mode en temps réel, `followUsers`, le fournisseur/modèle/voix, les politiques d'outil et de consultation, les noms de réveil, les fichiers d'amorçage, et les paramètres d'interruption.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/config-schema.test.ts:240` rejette les modes invalides, les noms de réveil, les politiques d'outil, les politiques de consultation, les chemins d'amorçage non sécurisés, et les `followUsers` vides.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/config-schema.test.ts:260` valide la configuration de timing et de canal autorisé.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/doctor.test.ts:121` couvre la normalisation du docteur vocal pour la configuration de nom de réveil invalide.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/audio.test.ts:18` vérifie les valeurs par défaut de décodage de réception `libopus-wasm` et l'encodage PCM brut.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/command.test.ts:64` couvre l'enregistrement de la commande `/vc` et le comportement du statut.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/access.test.ts:207` couvre le comportement de la liste blanche de l'expéditeur vocal et protège contre la correspondance de nom dangereuse.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/receive-recovery.test.ts` couvre la classification et les seuils de récupération de réception.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/voice/transcripts-source.test.ts` couvre le comportement de la source de transcription pour les transcriptions vocales.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.test.ts:170` couvre l'injection de configuration d'auto-join vocal ; `:535` couvre la gestion des canaux vocaux/état vocal.

## Requêtes Gitcrawl

Requête :

```
gitcrawl search issues "discord voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Retourné 20 problèmes. Les résultats ouverts clés incluent #80344 `/vc join` échouant sur Windows avec `AggregateError` et délai d'attente de battement de cœur de passerelle, #65039 fermeture du websocket vocal avant la poignée de main UDP, #80010 `/voice list` et `/voice chat` défaillance audio en lecture seule, #81518 défaillance de réception DAVE avec `UnencryptedWhenPassthroughDisabled`, #73699 voix-comme-IO/routage de session, #53562 `sessionChannelId` pour le routage des transcriptions auto-join, et #84952 adaptateur sortant vocal indisponible.

Requête :

```
gitcrawl search issues "voice channel" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Retourné les problèmes ouverts chevauchants pour le comportement d'exécution vocal Discord, y compris #73699, #53562, #80344, #80010, #65039, #81518, et les travaux adjacents de complétion de canal asynchrone.

Requête :

```
gitcrawl search issues "discord voice realtime" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Retourné #73699 et les travaux d'appel vocal adjacents, sans archive de problème prouvant le chemin vocal Discord en temps réel complet.

Requête :

```
gitcrawl search issues "libopus wasm discord voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Aucun résultat retourné.

Requête :

```
gitcrawl search issues "Discord voice UnencryptedWhenPassthroughDisabled DAVE" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Retourné #81518, un rapport de défaillance de réception DAVE ouvert mis à jour le 2026-05-28.

Requête :

```
gitcrawl search issues "Discord voice followUsers" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Aucun résultat retourné.

Requête :

```
gitcrawl search prs "discord voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Retourné 20 PR. Les résultats ouverts clés incluent #87530 groupes vocaux à portée de compte plus filet de sécurité d'auto-join retardé, #84965 repli lorsque l'adaptateur vocal est indisponible, #85173 dégradation de l'audio-comme-voix en pièce jointe multimédia lorsque l'adaptateur vocal est indisponible, #60902 `/vc switch`, #85529 préserver l'assistant sortant vocal Discord, et #82105 dépendances du plugin de canal vocal du bundle.

Requête :

```
gitcrawl search prs "discord voice realtime wake barge" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 20
```

Résultats :

- Aucun résultat retourné.

## Requêtes Discrawl

Requête :

```
DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search --limit 10 "discord voice /vc agent-proxy realtime wake barge libopus followUsers"
```

Résultats :

- Retourné `null` ; la phrase ciblée combinée n'avait pas de résultat direct dans l'archive Discord.

Requête :

```
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "discord voice"
```

Résultats :

- Retourné les messages récents de version/support sur la sélection plus nette de voix/modèle Discord et les contrôles Talk/voix, plus le routage du support du responsable autour des problèmes vocaux Discord.

Requête :

```
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "vc join"
```

Résultats :

- Retourné un extrait de configuration de mai 2026 couvrant `channels.discord.voice.enabled`, `GuildVoiceStates`, `/vc join/status/leave`, le comportement auto-join, et les permissions.
- Également retourné les messages utilisateur/support selon lesquels `/vc` semblait manquant et qu'un runtime spécifique ne pouvait pas rejoindre VC car seules les actions de texte/message Discord étaient exposées.

Requête :

```
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "libopus"
```

Résultats :

- Retourné une note du responsable selon laquelle OpenClaw a créé `openclaw/libopus-wasm` car l'état de dépendance Discord était mauvais, ce qui soutient l'atténuation du codec actuelle et l'historique des risques de qualité.

Requête :

```
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "UnencryptedWhenPassthroughDisabled"
```

Résultats :

- Retourné les fils de support pour la défaillance de réception vocale Discord, `/vc status` affichant prêt alors qu'aucune réponse STT n'est arrivée, les boucles de reconnexion, les défaillances de réception DAVE/E2EE, les défaillances de chargement de dépendance, et les conseils pour s'appuyer sur les valeurs par défaut DAVE et rejoindre après les défaillances de décryptage répétées.
