---
title: Claw Supervisor
description: Plan de supervision de flotte pour les sessions Codex app-server contrôlées par OpenClaw.
readWhen:
  - Designing Codex fleet supervision
  - Building OpenClaw tools that read, steer, or spawn Codex sessions
  - Choosing between local, Cloudflare, and VPS deployment for supervised Codex
---

# Claw Supervisor

## Objectif

Claw Supervisor permet à une instance OpenClaw toujours active de surveiller et de piloter une flotte de sessions Codex sans modifier l'expérience utilisateur normale de Codex. Un utilisateur peut se connecter en SSH à un hôte, démarrer Codex, travailler dans l'interface TUI, et le superviseur peut toujours lire la session, la piloter, l'interrompre, créer des sessions connexes et accepter les transferts. Les sessions Codex peuvent également rappeler OpenClaw via MCP.

## Modèle de produit

Codex reste la surface de travail principale. OpenClaw supervise Codex plutôt que de cacher Codex dans un sous-agent OpenClaw opaque.

Le plugin OpenClaw s'appelle `codex-supervisor`. `crabfleet` reste le profil de déploiement et de flotte d'hôtes pour les machines CRAB plutôt que le nom du plugin réutilisable.

Le modèle comporte trois rôles :

- Codex attaché à l'humain : une interface TUI Codex interactive normale lancée via un app-server partagé.
- Codex autonome : un thread app-server Codex créé par le superviseur auquel un humain peut se connecter ultérieurement.
- Supervisor Claw : un agent OpenClaw toujours actif avec des outils pour l'état de la flotte, les lectures de transcription, le pilotage, l'interruption, la création et le transfert.

OpenClaw peut utiliser sa machinerie de sous-agent existante en interne, mais le contrat externe est une session Codex attachable avec un identifiant de thread Codex.

## Architecture

```text
user SSH session
  -> codex --remote unix://... or ws://...
      -> local codex app-server daemon
          <-> host sidecar / supervisor connector
              <-> OpenClaw fleet supervisor
                  <-> supervisor MCP exposed back to Codex
```

Chaque hôte compatible Codex exécute :

- Daemon app-server Codex.
- Un lanceur qui démarre toujours Codex interactif avec `--remote`.
- Un connecteur qui enregistre les points de terminaison app-server et les threads actifs auprès du superviseur.

Le superviseur exécute :

- Registre de points de terminaison.
- Registre de sessions.
- Pool de clients JSON-RPC app-server Codex.
- Serveur MCP pour les appels Codex-to-Claw.
- Outils OpenClaw pour le contrôle Claw-to-Codex.
- Moteur de politique pour les actions autonomes, les approbations et la prévention des boucles.

## Contrat Codex App-Server

Utilisez les API app-server Codex comme plan de contrôle canonique :

- `initialize`, `initialized`
- `thread/loaded/list`
- `thread/list`
- `thread/read`
- `thread/resume`
- `thread/start`
- `turn/start`
- `turn/steer`
- `turn/interrupt`
- `model/list`

Codex interactif doit être lancé avec `codex --remote <endpoint>` pour que l'interface TUI et le superviseur se connectent au même app-server. Le `codex exec` autonome n'est pas une session partagée en direct aujourd'hui ; utilisez les API app-server pour le travail autonome jusqu'à ce que Codex supporte `exec --remote`.

## Registre de sessions

Le superviseur stocke un enregistrement par thread Codex observé :

```json
{
  "sessionId": "codex-thread-id",
  "endpointId": "host-a",
  "host": "host-a.example",
  "workspace": "/workspace/repo",
  "repo": "owner/repo",
  "branch": "feature/example",
  "source": "vscode",
  "status": "idle",
  "humanAttached": true,
  "lastSeenAt": "2026-05-28T10:00:00.000Z",
  "summary": "Short working-state summary"
}
```

L'implémentation locale peut dériver la plupart des champs à partir des métadonnées du thread Codex. Le déploiement de flotte doit enrichir les enregistrements avec l'identité de l'hôte, l'état d'attachement de l'utilisateur, l'état git et la santé du sidecar.

## Surface MCP pour Codex

Chaque Codex supervisé obtient un serveur MCP nommé `openclaw-codex-supervisor`.

Outils :

- `codex_sessions_list` : lister les sessions Codex visibles.
- `codex_session_read` : lire une transcription.
- `codex_session_send` : envoyer un message à un thread inactif ou piloter un thread actif.
- `codex_session_interrupt` : interrompre le tour actif.
- `codex_endpoint_probe` : vérifier la connectivité du point de terminaison.
- `claw_report_progress` : publier l'état actuel de la tâche auprès du superviseur.
- `claw_ask` : demander de l'aide ou une délégation au superviseur.
- `codex_spawn` : créer une nouvelle session Codex autonome.
- `codex_handoff` : demander une prise en charge humaine ou par les pairs.

Ressources :

- `codex://sessions`
- `codex://sessions/{sessionId}`
- `codex://sessions/{sessionId}/transcript`

## Surface de contrôle Claw

Le Claw toujours actif obtient les mêmes primitives que les outils internes :

- lister les sessions et les points de terminaison
- lire les transcriptions
- envoyer/piloter du texte
- interrompre le travail actif
- créer de nouvelles sessions
- résumer et assigner des sessions
- diffuser des instructions à un groupe filtré
- marquer les sessions comme bloquées, terminées ou abandonnées

Comportement des outils :

- Si un thread cible est inactif, `codex_session_send` correspond à `turn/start`.
- Si un thread cible est actif et qu'un identifiant de tour en cours est visible, il correspond à `turn/steer`.
- Si le tour actif ne peut pas être identifié, l'outil échoue de manière fermée au lieu de créer un tour non lié.
- Les contrôles d'écriture MCP exposés par Codex restent désactivés sauf si une politique de superviseur de confiance les active.
- Les lectures de transcription brutes restent désactivées sauf si une politique de superviseur de confiance les active.
- L'approbation autonome refuse par défaut les approbations d'outils/fichiers sauf si une politique explicite dit le contraire.

## Flux de lancement

Connexion interactive de l'hôte :

1. L'utilisateur se connecte en SSH à un hôte CRAB.
2. Le service SSH démarre ou vérifie `codex app-server daemon start`.
3. Le wrapper de connexion lance `codex --remote unix:// --cd <workspace>`.
4. Le connecteur d'hôte enregistre le point de terminaison et le thread chargé.
5. Le superviseur émet un événement de flotte de haute priorité : nouvelle session Codex, espace de travail, état d'attachement humain, aperçu de la tâche actuelle.
6. Le superviseur Claw peut lire et piloter immédiatement.

Création autonome :

1. Le superviseur sélectionne l'hôte et l'espace de travail.
2. Le connecteur d'hôte ouvre ou reprend un thread app-server Codex.
3. Le superviseur démarre le premier tour avec le texte de la tâche et la configuration MCP.
4. Le registre de sessions le marque comme autonome et attachable.
5. L'humain peut se connecter ultérieurement avec `codex --remote <endpoint> resume <threadId>` une fois que Codex supporte cette UX exacte, ou via le flux de reprise actuel sur le même app-server.

## Déploiement

Plan de contrôle préféré :

- Les connecteurs d'hôte maintiennent des connexions WebSocket sortantes vers le superviseur.
- L'état du superviseur réside dans le stockage OpenClaw Gateway.
- L'app-server Codex reste local à chaque hôte ; n'exposez jamais un app-server brut non authentifié à l'internet public.

Viabilité de Cloudflare :

- Bon pour le registre, les objets durables, le fan-in WebSocket, le routage d'événements léger et les points de terminaison MCP/gateway publics.
- Pas suffisant en soi pour le contrôle d'hôte privé direct car les Workers ne peuvent pas composer des sockets Unix privés arbitraires ou des app-servers de loopback locaux.
- Utilisez Cloudflare quand chaque connecteur d'hôte appelle à la maison via WebSocket sortant.

Secours VPS :

- Utilisez un service Hetzner quand le contrôle de processus de longue durée, les tunnels SSH, le routage de réseau privé ou l'accès au système de fichiers local est nécessaire.
- Conservez le même protocole : connecteurs d'hôte sortants, registre du superviseur central, app-server Codex local.

## Sécurité

- La liaison par défaut est une socket Unix locale.
- L'app-server distant utilise une authentification par jeton ou porteur signé.
- Le connecteur d'hôte s'authentifie auprès du superviseur avec un jeton d'hôte limité.
- Les outils du superviseur appliquent une politique par session : lecture, pilotage, interruption, création, approbation.
- Les messages entre agents incluent `originSessionId` ; l'auto-écho est supprimé.
- La diffusion nécessite un filtre explicite et un nombre de cibles limité.
- Les lectures de transcription masquent les secrets à la limite OpenClaw.
- Les demandes d'approbation refusent par défaut les tours d'origine du superviseur sauf si la politique les autorise.

## Plan de mise en œuvre

Phase 1 : MVP du superviseur local

- Ajouter un client JSON-RPC app-server Codex pour le proxy stdio et les points de terminaison WebSocket.
- Ajouter le registre de points de terminaison/sessions du superviseur.
- Ajouter les outils MCP : lister, lire, envoyer, interrompre, sonder.
- Ajouter la configuration env locale pour les points de terminaison.
- Ajouter des tests d'app-server factice et un test de fumée d'app-server local en direct.

Phase 2 : Intégration OpenClaw

- Enregistrer les outils du superviseur dans le plugin `codex-supervisor`.
- Injecter le MCP du superviseur dans la configuration du thread Codex.
- Ajouter des résumés de session au contexte de l'agent.
- Ajouter des notifications d'événements quand de nouveaux threads Codex apparaissent.
- Ajouter la configuration de politique pour l'envoi/interruption/création autonome.

Phase 3 : Connecteur de flotte

- Le sidecar d'hôte enregistre le point de terminaison app-server, les métadonnées d'hôte, les métadonnées git/espace de travail et l'état d'attachement humain.
- Ajouter un connecteur WebSocket sortant pour le plan de contrôle Cloudflare ou VPS.
- Ajouter la reconnexion, la pulsation et le nettoyage des sessions obsolètes.
- Ajouter le wrapper de lanceur SSH CRAB.

Phase 4 : Opération autonome

- Ajouter les flux de création/reprise/prise en charge.
- Ajouter la diffusion et la délégation.
- Ajouter les rapports de progression et les résumés d'état de tâche.
- Ajouter la prévention des boucles et les limites de débit.
- Ajouter les vues du tableau de bord.

Phase 5 : Multi-Claw

- Fragmenter les sessions par groupe.
- Ajouter le leadership/bail pour chaque session.
- Ajouter le journal d'audit et la relecture.
- Ajouter l'escalade entre les groupes Claw.

## Tests d'acceptation

- Un humain lance l'interface TUI Codex via un app-server partagé.
- Le superviseur liste le thread actif via `thread/loaded/list`.
- Le superviseur lit la transcription via `thread/read`.
- Le superviseur envoie du texte à un thread inactif via `turn/start`.
- Le superviseur pilote un thread actif via `turn/steer`.
- L'interruption du superviseur arrête un tour actif via `turn/interrupt`.
- Codex appelle le MCP du superviseur et liste les sessions homologues.
- Un Codex autonome est créé et attaché ultérieurement par un humain.
- Le connecteur d'hôte perdu marque les sessions comme obsolètes sans supprimer l'historique.

## Questions ouvertes

- UX d'attachement TUI Codex exact pour un thread app-server créé sans TUI.
- Si Codex doit ajouter `exec --remote` pour les exécutions partagées en direct sans interface.
- Propriétaire de l'état durable : OpenClaw Gateway DB, Cloudflare Durable Object ou base de données VPS.
- Granularité de la politique d'approbation pour les tours d'origine du superviseur.
- Combien de résumé de transcription doit être injecté dans le contexte Claw toujours actif par rapport à ce qui est conservé comme outil/ressource.
