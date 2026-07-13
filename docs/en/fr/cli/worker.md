---
summary: "Référence d'opérateur interne pour le runtime du worker cloud restreint"
read_when:
  - Operating or debugging gateway-launched cloud workers
  - Verifying worker admission, session assignment, or local tool isolation
title: "Worker"
---

# `openclaw worker`

`openclaw worker` est le point d'entrée du runtime restreint pour un orchestrateur de worker cloud à lancer dans un environnement worker préparé. Ce n'est pas une commande à usage général pour l'enregistrement manuel de workers.

La passerelle installe le bundle OpenClaw correspondant et ouvre le tunnel SSH inverse épinglé par clé d'hôte. Le lanceur de worker démarre cette commande avec une affectation préparée. La commande se connecte via la socket locale transférée par le tunnel et s'authentifie avec le rôle dédié `worker`.

## Contrat de lancement

La commande lit exactement une enveloppe de lancement JSON délimitée depuis l'entrée standard. L'enveloppe contient l'emplacement de la socket locale, les identifiants de worker émis, l'identité du bundle et du protocole, l'époque du propriétaire, et la session et le tour assignés uniques. Les identifiants ne sont jamais acceptés via les arguments de ligne de commande, et cette page ne fournit intentionnellement aucun exemple d'identifiant ou d'enveloppe rédigée à la main.

L'authentification échoue de manière fermée si l'enveloppe est invalide, les identifiants sont rejetés, les fonctionnalités du bundle ou du protocole ne correspondent pas, ou la session et l'époque du propriétaire ne sont plus actuelles. Les opérateurs doivent démarrer les workers via l'orchestrateur de worker cloud plutôt que d'invoquer directement ce point d'entrée.

## Limite du runtime

Le processus exécute la boucle d'agent intégrée normale avec un backend restreint :

- Les outils de codage `read`, `write`, `edit`, `apply_patch`, `exec` et `process` s'exécutent localement dans l'espace de travail du worker.
- Les appels de modèle utilisent le proxy d'inférence de la passerelle. Aucun profil d'authentification de modèle local n'est chargé.
- Les écritures de transcription utilisent l'RPC de validation de transcription de la passerelle.
- Les mises à jour de streaming et de cycle de vie des outils utilisent l'RPC d'événement en direct de la passerelle.
- Seule la session et le tour assignés sont acceptés.

Le mode worker ne démarre pas les canaux, les surfaces HTTP de la passerelle ou le démarrage automatique des plugins au-delà de l'ensemble d'outils de session assigné. Il utilise un répertoire d'état jetable et n'a pas d'identifiants de fournisseur ou de forge permanents.

La répartition de session worker-à-worker n'est pas exposée dans ce mode. La répartition d'agent et le placement restent des surfaces de jalon 3 appartenant à la passerelle.

L'affectation préparée contient le contexte de transcription, la feuille de base acceptée, la séquence de validation et le curseur d'événement en direct. Lors d'une reconnexion de tunnel, le processus se réauthentifie avec les mêmes identifiants et époque du propriétaire, conserve la base de transcription acceptée, rejoue la queue d'événement en direct non reconnue et réattache un tour d'inférence en cours avec la même identité. Le message d'inférence terminal est autoritaire si les deltas en streaming ont été manqués. Une époque de propriétaire remplaçante clôture le processus et provoque une sortie propre.

Un rejet de transcription `stale-base-leaf` arrête le run actuel. Le mode worker ne réessaie pas la séquence rejetée contre une feuille différente, donc aucun doublon de validation n'est produit ; toute queue en mémoire non validée de ce run est perdue. Le relancement appartient au propriétaire de placement de jalon 3, qui doit créer une nouvelle affectation à partir de la transcription autoritaire de la passerelle et du registre de validation. De même, un redémarrage du processus de passerelle termine un tour d'inférence en attente avec une erreur de fournisseur ; seule une reconnexion de tunnel ou de WebSocket de worker peut se réattacher à un flux d'inférence actif du même processus.

Voir [Protocole de passerelle](/fr/gateway/protocol#worker-role-and-closed-protocol) pour la surface RPC fermée du worker et [Plan des workers cloud](/fr/plan/cloud-workers) pour l'architecture et le modèle de sécurité.
