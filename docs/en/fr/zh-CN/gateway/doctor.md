---
read_when:
  - Ajout ou modification des migrations doctor
  - Introduction de modifications de configuration avec rupture de compatibilité
summary: Commande Doctor : vérifications de santé, migrations de configuration et étapes de correction
title: Doctor
x-i18n:
  generated_at: "2026-02-03T07:49:03Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: df7b25f60fd08d508f4c6abfc8e7e06f29bd4bbb34c3320397f47eb72c8de83f
  source_path: gateway/doctor.md
  workflow: 15
---

# Doctor

`openclaw doctor` est l'outil de correction + migration d'OpenClaw. Il corrige les configurations/états obsolètes, vérifie la santé et fournit des étapes de correction exploitables.

## Démarrage rapide

```bash
openclaw doctor
```

### Mode sans interface/automatisé

```bash
openclaw doctor --yes
```

Accepte les valeurs par défaut sans invite (y compris les étapes de correction de redémarrage/service/sandbox le cas échéant).

```bash
openclaw doctor --repair
```

Applique les corrections recommandées sans invite (correction sécurisée + redémarrage).

```bash
openclaw doctor --repair --force
```

Applique également les corrections agressives (remplace les configurations supervisor personnalisées).

```bash
openclaw doctor --non-interactive
```

S'exécute sans invite, applique uniquement les migrations sécurisées (normalisation de configuration + déplacements d'état disque). Ignore les opérations de redémarrage/service/sandbox nécessitant une confirmation manuelle.
Exécute automatiquement les migrations d'état hérité lorsqu'elles sont détectées.

```bash
openclaw doctor --deep
```

Analyse les services système pour trouver des installations Gateway supplémentaires (launchd/systemd/schtasks).

Si vous souhaitez voir les modifications avant l'écriture, ouvrez d'abord le fichier de configuration :

```bash
cat ~/.openclaw/openclaw.json
```

## Aperçu des fonctionnalités

- Vérification préalable de mise à jour optionnelle pour les installations git (mode interactif uniquement).
- Vérification de fraîcheur du protocole UI (reconstruction de l'interface de contrôle lorsque le schéma de protocole est plus récent).
- Vérifications de santé + invites de redémarrage.
- Résumé de l'état des Skills (admissibles/manquants/bloqués).
- Normalisation de configuration pour les valeurs héritées.
- Avertissement de remplacement du fournisseur OpenCode Zen (`models.providers.opencode`).
- Migrations d'état disque hérité (sessions/répertoires d'agents/authentification WhatsApp).
- Vérifications d'intégrité et de permissions d'état (sessions, journaux, répertoires d'état).
- Vérifications de permissions de fichiers de configuration pour les runtimes locaux (chmod 600).
- Santé de l'authentification du modèle : vérification de l'expiration OAuth, actualisation des tokens sur le point d'expirer, et rapport sur l'état de refroidissement/désactivation des fichiers de configuration d'authentification.
- Détection de répertoires d'espace de travail supplémentaires (`~/openclaw`).
- Correction d'image sandbox lors de l'activation de l'isolation sandbox.
- Migration de service hérité et détection de Gateway supplémentaire.
- Vérifications du runtime Gateway (service installé mais non exécuté ; étiquettes launchd en cache).
- Avertissements d'état du canal (sondage depuis le Gateway en cours d'exécution).
- Audit de configuration Supervisor (launchd/systemd/schtasks) et correction optionnelle.
- Vérifications des meilleures pratiques du runtime Gateway (Node vs Bun, chemins du gestionnaire de versions).
- Diagnostic de conflit de port Gateway (par défaut `18789`).
- Avertissements de sécurité pour les politiques de messages privés ouverts.
- Avertissement d'authentification Gateway lorsque `gateway.auth.token` n'est pas défini (mode local ; fourniture de génération de token).
- Vérification de systemd linger sur Linux.
- Vérifications d'installation à partir du code source (incompatibilité d'espace de travail pnpm, ressources UI manquantes, binaire tsx manquant).
- Écriture de configuration mise à jour + métadonnées de l'assistant.

## Comportement détaillé et principes

### 0) Mise à jour optionnelle (installation git)

Si c'est un checkout git et que doctor s'exécute en mode interactif, il propose une mise à jour (fetch/rebase/build) avant d'exécuter doctor.

### 1) Normalisation de configuration

Si la configuration contient des formes de valeurs héritées (par exemple `messages.ackReaction` sans remplacements spécifiques au canal), doctor les normalise au schéma actuel.

### 2) Migration de clés de configuration héritées

Lorsque la configuration contient des clés dépréciées, d'autres commandes refusent de s'exécuter et vous demandent d'exécuter `openclaw doctor`.

Doctor va :

- Expliquer quelles clés héritées ont été trouvées.
- Afficher les migrations qu'il applique.
- Réécrire `~/.openclaw/openclaw.json` avec le schéma mis à jour.

Gateway exécute également automatiquement la migration doctor au démarrage lors de la détection d'un format de configuration hérité, de sorte que les configurations obsolètes sont corrigées sans intervention manuelle.

Migrations actuelles :

- `routing.allowFrom` → `channels.whatsapp.allowFrom`
- `routing.groupChat.requireMention` → `channels.whatsapp/telegram/imessage.groups."*".requireMention`
- `routing.groupChat.historyLimit` → `messages.groupChat.historyLimit`
- `routing.groupChat.mentionPatterns` → `messages.groupChat.mentionPatterns`
- `routing.queue` → `messages.queue`
- `routing.bindings` → `bindings` au niveau supérieur
- `routing.agents`/`routing.defaultAgentId` → `agents.list` + `agents.list[].default`
- `routing.agentToAgent` → `tools.agentToAgent`
- `routing.transcribeAudio` → `tools.media.audio.models`
- `bindings[].match.accountID` → `bindings[].match.accountId`
- `identity` → `agents.list[].identity`
- `agent.*` → `agents.defaults` + `tools.*`(tools/elevated/exec/sandbox/subagents)
- `agent.model`/`allowedModels`/`modelAliases`/`modelFallbacks`/`imageModelFallbacks`
  → `agents.defaults.models` + `agents.defaults.model.primary/fallbacks` + `agents.defaults.imageModel.primary/fallbacks`

### 2b) Remplacement du fournisseur OpenCode Zen

Si vous avez manuellement ajouté `models.providers.opencode` (ou `opencode-zen`), il remplace le répertoire OpenCode Zen intégré dans `@mariozechner/pi-ai`. Cela peut forcer chaque modèle sur une seule API ou annuler les coûts. Doctor émet un avertissement afin que vous puissiez supprimer le remplacement et restaurer le routage par modèle API + les coûts.

### 3) Migrations d'état hérité (disposition disque)

Doctor peut migrer les anciennes dispositions disque vers la structure actuelle :

- Stockage de sessions + journaux :
  - De `~/.openclaw/sessions/` à `~/.openclaw/agents/<agentId>/sessions/`
- Répertoire d'agents :
  - De `~/.openclaw/agent/` à `~/.openclaw/agents/<agentId>/agent/`
- État d'authentification WhatsApp (Baileys) :
  - Des `~/.openclaw/credentials/*.json` hérités (sauf `oauth.json`)
  - À `~/.openclaw/credentials/whatsapp/<accountId>/...` (ID de compte par défaut : `default`)

Ces migrations sont au mieux et idempotentes ; doctor émet un avertissement lorsqu'il conserve les dossiers hérités en tant que sauvegarde. Gateway/CLI migrent également automatiquement les sessions héritées + répertoires d'agents au démarrage, de sorte que l'historique/authentification/modèles se retrouvent dans le chemin par agent, sans avoir besoin d'exécuter manuellement doctor. L'authentification WhatsApp est intentionnellement migrée uniquement via `openclaw doctor`.

### 4) Vérifications d'intégrité d'état (persistance de session, routage et sécurité)

Le répertoire d'état est au cœur des opérations. S'il disparaît, vous perdez les sessions, les identifiants, les journaux et la configuration (sauf si vous avez une sauvegarde ailleurs).

Doctor vérifie :

- **Répertoire d'état manquant** : avertit de la perte d'état catastrophique, propose de recréer le répertoire et vous rappelle qu'il ne peut pas récupérer les données perdues.
- **Permissions du répertoire d'état** : vérifie la capacité d'écriture ; fournit une correction des permissions (et émet une invite `chown` lors de la détection d'une incompatibilité de propriétaire/groupe).
- **Répertoire de sessions manquant** : `sessions/` et les répertoires de stockage de sessions sont nécessaires pour persister l'historique et éviter les plantages `ENOENT`.
- **Incompatibilité de journaux** : avertit lorsque les entrées de session récentes manquent de fichiers journaux.
- **Session principale "1 ligne JSONL"** : signale lorsque l'enregistrement principal n'a qu'une ligne (l'historique ne s'accumule pas).
- **Répertoires d'état multiples** : avertit lorsque plusieurs dossiers `~/.openclaw` existent dans différents répertoires home ou lorsque `OPENCLAW_STATE_DIR` pointe ailleurs (l'historique peut être divisé entre les installations).
- **Rappel du mode distant** : si `gateway.mode=remote`, doctor vous rappelle de l'exécuter sur l'hôte distant (l'état y est).
- **Permissions du fichier de configuration** : avertit lorsque `~/.openclaw/openclaw.json` est lisible par le groupe/autres et fournit une option pour le resserrer à `600`.

### 5) Santé de l'authentification du modèle (expiration OAuth)

Doctor vérifie les fichiers de configuration OAuth dans le magasin d'authentification, émet des avertissements lorsque les tokens sont sur le point d'expirer/ont expiré, et les actualise lorsque c'est sécurisé. Si le fichier de configuration Anthropic Claude Code est obsolète, il suggère d'exécuter `claude setup-token` (ou de coller setup-token).
Les invites d'actualisation n'apparaissent que lors d'une exécution interactive (TTY) ; `--non-interactive` ignore les tentatives d'actualisation.

Doctor rapporte également les fichiers de configuration d'authentification temporairement indisponibles en raison de :

- Refroidissement court (limitation de débit/délai d'expiration/échec d'authentification)
- Désactivation longue (facturation/échec de crédit)

### 6) Validation du modèle Hooks

Si `hooks.gmail.model` est défini, doctor valide la référence du modèle par rapport au répertoire et à la liste d'autorisation, et émet un avertissement s'il ne peut pas être résolu ou n'est pas autorisé.

### 7) Correction d'image sandbox

Lorsque l'isolation sandbox est activée, doctor vérifie les images Docker et fournit une option pour construire ou basculer vers un nom hérité lorsque l'image actuelle est manquante.

### 8) Migration de service Gateway et invites de nettoyage

Doctor détecte les services Gateway hérités (launchd/systemd/schtasks) et fournit une option pour les supprimer et installer le service OpenClaw avec le port Gateway actuel. Il peut également analyser les services de type Gateway supplémentaires et imprimer les invites de nettoyage.
Les services Gateway nommés par fichier de configuration sont traités comme des citoyens de première classe et ne sont pas marqués comme "supplémentaires".

### 9) Avertissements de sécurité

Lorsqu'un fournisseur est ouvert aux messages privés sans liste d'autorisation, ou lorsque la politique est configurée de manière dangereuse, Doctor émet un avertissement.

### 10) systemd linger (Linux)

S'il s'exécute en tant que service utilisateur systemd, doctor s'assure que lingering est activé afin que Gateway reste actif après la déconnexion.

### 11) État des Skills

Doctor imprime un résumé rapide des Skills admissibles/manquants/bloqués de l'espace de travail actuel.

### 12) Vérification d'authentification Gateway (token local)

Lorsque le Gateway local manque `gateway.auth`, Doctor émet un avertissement et fournit une option pour générer un token. Utilisez `openclaw doctor --generate-gateway-token` pour forcer la création de token dans l'automatisation.

### 13) Vérification de santé Gateway + redémarrage

Doctor exécute une vérification de santé et fournit une option de redémarrage lorsque Gateway semble malsain.

### 14) Avertissements d'état du canal

Si Gateway est sain, doctor exécute des sondes d'état de canal et rapporte les avertissements et les corrections suggérées.

### 15) Audit de configuration Supervisor + correction

Doctor vérifie les configurations supervisor installées (launchd/systemd/schtasks) pour les valeurs par défaut manquantes ou obsolètes (par exemple, la dépendance network-online systemd et le délai de redémarrage). Lorsqu'une incompatibilité est trouvée, il recommande une mise à jour et peut réécrire les fichiers de service/tâches aux valeurs par défaut actuelles.

Points à noter :

- `openclaw doctor` invite avant de réécrire la configuration supervisor.
- `openclaw doctor --yes` accepte les invites de correction par défaut.
- `openclaw doctor --repair` applique les corrections recommandées sans invite.
- `openclaw doctor --repair --force` remplace les configurations supervisor personnalisées.
- Vous pouvez toujours forcer une réécriture complète via `openclaw gateway install --force`.

### 16) Diagnostic du runtime Gateway + port

Doctor vérifie le runtime du service (PID, dernier état de sortie) et émet un avertissement lorsque le service est installé mais ne s'exécute pas réellement. Il vérifie également les conflits de port sur le port Gateway (par défaut `18789`) et rapporte les causes possibles (Gateway déjà en cours d'exécution, tunnel SSH).

### 17) Meilleures pratiques du runtime Gateway

L
