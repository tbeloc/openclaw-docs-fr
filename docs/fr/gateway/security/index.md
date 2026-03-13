# Sécurité 🔒

> [!WARNING]
> **Modèle de confiance de l'assistant personnel :** ce guide suppose une limite de confiance d'un opérateur de confiance par passerelle (modèle d'assistant personnel/utilisateur unique).
> OpenClaw n'est **pas** une limite de sécurité multi-locataire hostile pour plusieurs utilisateurs adversaires partageant un agent/une passerelle.
> Si vous avez besoin d'une opération multi-confiance ou utilisateur adversaire, divisez les limites de confiance (passerelle séparée + identifiants, idéalement utilisateurs/hôtes OS séparés).

## Portée d'abord : modèle de sécurité de l'assistant personnel

Les conseils de sécurité OpenClaw supposent un déploiement d'**assistant personnel** : une limite d'opérateur de confiance, potentiellement de nombreux agents.

- Posture de sécurité prise en charge : un utilisateur/limite de confiance par passerelle (préférez un utilisateur OS/hôte/VPS par limite).
- Limite de sécurité non prise en charge : une passerelle/un agent partagé utilisé par des utilisateurs mutuellement non fiables ou adversaires.
- Si l'isolation des utilisateurs adversaires est requise, divisez par limite de confiance (passerelle séparée + identifiants, et idéalement utilisateurs/hôtes OS séparés).
- Si plusieurs utilisateurs non fiables peuvent envoyer des messages à un agent compatible avec les outils, traitez-les comme partageant la même autorité d'outil déléguée pour cet agent.

Cette page explique le renforcement **dans ce modèle**. Elle ne prétend pas à l'isolation multi-locataire hostile sur une passerelle partagée.

## Vérification rapide : `openclaw security audit`

Voir aussi : [Vérification formelle (Modèles de sécurité)](/security/formal-verification/)

Exécutez ceci régulièrement (surtout après avoir modifié la configuration ou exposé les surfaces réseau) :

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
openclaw security audit --json
```

Il signale les pièges courants (exposition de l'authentification de la passerelle, exposition du contrôle du navigateur, listes blanches élevées, permissions du système de fichiers).

OpenClaw est à la fois un produit et une expérience : vous câblez le comportement du modèle de pointe dans les surfaces de messagerie réelles et les outils réels. **Il n'existe pas de configuration « parfaitement sécurisée »**. L'objectif est d'être délibéré sur :

- qui peut parler à votre bot
- où le bot est autorisé à agir
- ce que le bot peut toucher

Commencez par l'accès le plus petit qui fonctionne toujours, puis élargissez-le au fur et à mesure que vous gagnez en confiance.

## Hypothèse de déploiement (important)

OpenClaw suppose que l'hôte et la limite de configuration sont de confiance :

- Si quelqu'un peut modifier l'état/la configuration de l'hôte Gateway (`~/.openclaw`, y compris `openclaw.json`), traitez-le comme un opérateur de confiance.
- L'exécution d'une Gateway pour plusieurs opérateurs mutuellement non fiables/adversaires n'est **pas une configuration recommandée**.
- Pour les équipes multi-confiance, divisez les limites de confiance avec des passerelles séparées (ou au minimum des utilisateurs/hôtes OS séparés).
- OpenClaw peut exécuter plusieurs instances de passerelle sur une machine, mais les opérations recommandées favorisent une séparation nette des limites de confiance.
- Recommandation par défaut : un utilisateur par machine/hôte (ou VPS), une passerelle pour cet utilisateur, et un ou plusieurs agents dans cette passerelle.
- Si plusieurs utilisateurs veulent OpenClaw, utilisez un VPS/hôte par utilisateur.

### Conséquence pratique (limite de confiance de l'opérateur)

Au sein d'une instance Gateway, l'accès de l'opérateur authentifié est un rôle du plan de contrôle de confiance, pas un rôle de locataire par utilisateur.

- Les opérateurs ayant accès au plan de contrôle en lecture/contrôle peuvent inspecter les métadonnées/l'historique de la session de la passerelle par conception.
- Les identifiants de session (`sessionKey`, ID de session, étiquettes) sont des sélecteurs de routage, pas des jetons d'autorisation.
- Exemple : s'attendre à une isolation par opérateur pour des méthodes comme `sessions.list`, `sessions.preview` ou `chat.history` est en dehors de ce modèle.
- Si vous avez besoin d'isolation des utilisateurs adversaires, exécutez des passerelles séparées par limite de confiance.
- Plusieurs passerelles sur une machine sont techniquement possibles, mais ne sont pas la base recommandée pour l'isolation multi-utilisateurs.

## Modèle d'assistant personnel (pas un bus multi-locataire)

OpenClaw est conçu comme un modèle de sécurité d'assistant personnel : une limite d'opérateur de confiance, potentiellement de nombreux agents.

- Si plusieurs personnes peuvent envoyer des messages à un agent compatible avec les outils, chacune d'elles peut diriger le même ensemble de permissions.
- L'isolation de session/mémoire par utilisateur aide à la confidentialité, mais ne convertit pas un agent partagé en autorisation d'hôte par utilisateur.
- Si les utilisateurs peuvent être adversaires les uns envers les autres, exécutez des passerelles séparées (ou des utilisateurs/hôtes OS séparés) par limite de confiance.

### Espace de travail Slack partagé : risque réel

Si « tout le monde dans Slack peut envoyer un message au bot », le risque principal est l'autorité d'outil déléguée :

- tout expéditeur autorisé peut induire des appels d'outils (`exec`, navigateur, outils réseau/fichier) dans la politique de l'agent ;
- l'injection de contenu/d'invite d'un expéditeur peut causer des actions qui affectent l'état partagé, les appareils ou les sorties ;
- si un agent partagé a des identifiants/fichiers sensibles, tout expéditeur autorisé peut potentiellement conduire l'exfiltration via l'utilisation d'outils.

Utilisez des agents/passerelles séparés avec des outils minimaux pour les flux de travail d'équipe ; gardez les agents de données personnelles privés.

### Agent partagé par l'entreprise : modèle acceptable

C'est acceptable lorsque tous les utilisateurs de cet agent sont dans la même limite de confiance (par exemple une équipe d'entreprise) et l'agent est strictement limité à l'entreprise.

- exécutez-le sur une machine/VM/conteneur dédiée ;
- utilisez un utilisateur OS dédié + un navigateur/profil/compte dédié pour ce runtime ;
- ne connectez pas ce runtime à des comptes Apple/Google personnels ou à des profils de gestionnaire de mots de passe/navigateur personnels.

Si vous mélangez les identités personnelles et professionnelles sur le même runtime, vous effondrez la séparation et augmentez le risque d'exposition des données personnelles.

## Concept de confiance de la passerelle et du nœud

Traitez Gateway et node comme un domaine de confiance d'un opérateur, avec des rôles différents :

- **Gateway** est le plan de contrôle et la surface de politique (`gateway.auth`, politique d'outils, routage).
- **Node** est la surface d'exécution à distance appairée à cette Gateway (commandes, actions d'appareil, capacités locales à l'hôte).
- Un appelant authentifié à la Gateway est de confiance à la portée de la Gateway. Après appairage, les actions de nœud sont des actions d'opérateur de confiance sur ce nœud.
- `sessionKey` est le routage/sélection de contexte, pas l'authentification par utilisateur.
- Les approbations d'exécution (liste blanche + demande) sont des garde-fous pour l'intention de l'opérateur, pas l'isolation multi-locataire hostile.
- Les approbations d'exécution lient le contexte exact de la demande et les opérandes de fichier local directs au meilleur effort ; elles ne modélisent pas sémantiquement chaque chemin de chargeur d'exécution/interpréteur. Utilisez le sandboxing et l'isolation d'hôte pour les limites fortes.

Si vous avez besoin d'isolation des utilisateurs hostiles, divisez les limites de confiance par utilisateur OS/hôte et exécutez des passerelles séparées.

## Matrice des limites de confiance

Utilisez ceci comme modèle rapide lors du triage des risques :

| Limite ou contrôle                          | Ce que cela signifie                                      | Mauvaise lecture courante                                                                     |
| ------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `gateway.auth` (jeton/mot de passe/auth d'appareil) | Authentifie les appelants aux API de passerelle             | « Nécessite des signatures par message sur chaque trame pour être sécurisé »                    |
| `sessionKey`                                | Clé de routage pour la sélection de contexte/session       | « La clé de session est une limite d'authentification utilisateur »                             |
| Garde-fous d'invite/contenu                 | Réduire le risque d'abus du modèle                         | « L'injection d'invite seule prouve le contournement d'authentification »                       |
| `canvas.eval` / évaluation du navigateur    | Capacité d'opérateur intentionnelle lorsqu'elle est activée | « Tout primitive d'évaluation JS est automatiquement une vulnérabilité dans ce modèle de confiance » |
| Shell TUI local `!`                         | Exécution locale explicite déclenchée par l'opérateur      | « La commande shell locale de commodité est l'injection à distance »                            |
| Appairage de nœud et commandes de nœud     | Exécution à distance au niveau de l'opérateur sur les appareils appairés | « Le contrôle d'appareil à distance doit être traité comme un accès utilisateur non fiable par défaut » |

## Pas des vulnérabilités par conception

Ces modèles sont couramment signalés et sont généralement fermés sans action sauf si un vrai contournement de limite est montré :

- Chaînes d'injection d'invite uniquement sans contournement de politique/authentification/sandbox.
- Réclamations qui supposent une opération multi-locataire hostile sur un hôte/config partagé.
- Réclamations qui classent l'accès au chemin de lecture normal de l'opérateur (par exemple `sessions.list`/`sessions.preview`/`chat.history`) comme IDOR dans une configuration de passerelle partagée.
- Résultats de déploiement localhost uniquement (par exemple HSTS sur une passerelle localhost uniquement).
- Résultats de signature de webhook entrant Discord pour les chemins entrants qui n'existent pas dans ce repo.
- Résultats « Autorisation par utilisateur manquante » qui traitent `sessionKey` comme un jeton d'authentification.

## Liste de contrôle de préparation du chercheur

Avant d'ouvrir un GHSA, vérifiez tous ces éléments :

1. La reproduction fonctionne toujours sur le dernier `main` ou la dernière version.
2. Le rapport inclut le chemin de code exact (`fichier`, fonction, plage de lignes) et la version/commit testée.
3. L'impact traverse une limite de confiance documentée (pas seulement l'injection d'invite).
4. La réclamation n'est pas listée dans [Hors de portée](https://github.com/openclaw/openclaw/blob/main/SECURITY.md#out-of-scope).
5. Les avis existants ont été vérifiés pour les doublons (réutilisez le GHSA canonique le cas échéant).
6. Les hypothèses de déploiement sont explicites (loopback/local vs exposé, opérateurs de confiance vs non fiables).

## Base de référence renforcée en 60 secondes

Utilisez cette base de référence en premier, puis réactivez sélectivement les outils par agent de confiance :

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "replace-with-long-random-token" },
  },
  session: {
    dmScope: "per-channel-peer",
  },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    fs: { workspaceOnly: true },
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
  channels: {
    whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } },
  },
}
```

Cela garde la Gateway locale uniquement, isole les DM et désactive les outils du plan de contrôle/runtime par défaut.

## Règle rapide de boîte de réception partagée

Si plus d'une personne peut envoyer un DM à votre bot :

- Définissez `session.dmScope: "per-channel-peer"` (ou `"per-account-channel-peer"` pour les canaux multi-comptes).
- Gardez `dmPolicy: "pairing"` ou des listes blanches strictes.
- Ne combinez jamais les DM partagés avec un large accès aux outils.
- Cela renforce les boîtes de réception coopératives/partagées, mais n'est pas conçu comme l'isolation des co-locataires hostiles lorsque les utilisateurs partagent l'accès en écriture à l'hôte/config.

### Ce que l'audit vérifie (haut niveau)

- **Accès entrant** (politiques DM, politiques de groupe, listes blanches) : les étrangers peuvent-ils déclencher le bot ?
- **Rayon d'explosion des outils** (outils élevés + salles ouvertes) : l'injection d'invite pourrait-elle se transformer en actions shell/fichier/réseau ?
- **Exposition réseau** (liaison/authentification Gateway, Tailscale Serve/Funnel, jetons d'authentification faibles/courts).
- **Exposition du contrôle du navigateur** (nœuds distants, ports de relais, points de terminaison CDP distants).
- **Hygiène du disque local** (permissions, liens symboliques, inclusions de config, chemins de « dossier synchronisé »).
- **Plugins** (les extensions existent sans liste blanche explicite).
- **Dérive de politique/mauvaise configuration** (paramètres docker sandbox configurés mais mode sandbox désactivé ; modèles `gateway.nodes.denyCommands` inefficaces car la correspondance est
