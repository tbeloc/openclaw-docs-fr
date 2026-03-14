---
summary: "Commande Doctor : vérifications de santé, migrations de configuration et étapes de réparation"
read_when:
  - Adding or modifying doctor migrations
  - Introducing breaking config changes
title: "Doctor"
---

# Doctor

`openclaw doctor` est l'outil de réparation + migration pour OpenClaw. Il corrige les configurations/états obsolètes, vérifie la santé et fournit des étapes de réparation exploitables.

## Démarrage rapide

```bash
openclaw doctor
```

### Sans interface / automatisation

```bash
openclaw doctor --yes
```

Accepte les valeurs par défaut sans demander (y compris les étapes de réparation de redémarrage/service/sandbox le cas échéant).

```bash
openclaw doctor --repair
```

Applique les réparations recommandées sans demander (réparations + redémarrages si sûr).

```bash
openclaw doctor --repair --force
```

Applique aussi les réparations agressives (écrase les configurations supervisor personnalisées).

```bash
openclaw doctor --non-interactive
```

Exécute sans invites et applique uniquement les migrations sûres (normalisation de configuration + déplacements d'état sur disque). Ignore les actions de redémarrage/service/sandbox qui nécessitent une confirmation humaine.
Les migrations d'état hérité s'exécutent automatiquement quand elles sont détectées.

```bash
openclaw doctor --deep
```

Analyse les services système pour les installations de passerelle supplémentaires (launchd/systemd/schtasks).

Si vous souhaitez examiner les modifications avant d'écrire, ouvrez d'abord le fichier de configuration :

```bash
cat ~/.openclaw/openclaw.json
```

## Ce qu'il fait (résumé)

- Mise à jour de pré-vol optionnelle pour les installations git (interactif uniquement).
- Vérification de la fraîcheur du protocole UI (reconstruit l'interface de contrôle quand le schéma de protocole est plus récent).
- Vérification de santé + invite de redémarrage.
- Résumé du statut des compétences (éligible/manquant/bloqué).
- Normalisation de configuration pour les valeurs héritées.
- Avertissements de remplacement du fournisseur OpenCode (`models.providers.opencode` / `models.providers.opencode-go`).
- Migration d'état hérité sur disque (sessions/répertoire agent/authentification WhatsApp).
- Migration du magasin cron hérité (`jobId`, `schedule.cron`, champs de livraison/charge utile de niveau supérieur, `provider` de charge utile, travaux webhook de secours `notify: true` simples).
- Vérifications d'intégrité et de permissions d'état (sessions, transcriptions, répertoire d'état).
- Vérifications de permissions de fichier de configuration (chmod 600) lors de l'exécution locale.
- Santé de l'authentification du modèle : vérifie l'expiration OAuth, peut actualiser les jetons arrivant à expiration et signale les états de refroidissement/désactivation du profil d'authentification.
- Détection de répertoire d'espace de travail supplémentaire (`~/openclaw`).
- Réparation d'image sandbox quand le sandboxing est activé.
- Migration de service hérité et détection de passerelle supplémentaire.
- Vérifications d'exécution de passerelle (service installé mais non exécuté ; étiquette launchd en cache).
- Avertissements de statut de canal (sondés à partir de la passerelle en cours d'exécution).
- Audit de configuration supervisor (launchd/systemd/schtasks) avec réparation optionnelle.
- Vérifications des meilleures pratiques d'exécution de passerelle (Node vs Bun, chemins du gestionnaire de version).
- Diagnostics de collision de port de passerelle (par défaut `18789`).
- Avertissements de sécurité pour les politiques DM ouvertes.
- Vérifications d'authentification de passerelle pour le mode de jeton local (offre la génération de jeton quand aucune source de jeton n'existe ; ne remplace pas les configurations SecretRef de jeton).
- Vérification de lingering systemd sur Linux.
- Vérifications d'installation source (incompatibilité d'espace de travail pnpm, ressources UI manquantes, binaire tsx manquant).
- Écrit la configuration mise à jour + métadonnées de l'assistant.

## Comportement détaillé et justification

### 0) Mise à jour optionnelle (installations git)

Si c'est un checkout git et que doctor s'exécute de manière interactive, il offre de mettre à jour (fetch/rebase/build) avant d'exécuter doctor.

### 1) Normalisation de configuration

Si la configuration contient des formes de valeurs héritées (par exemple `messages.ackReaction` sans remplacement spécifique au canal), doctor les normalise dans le schéma actuel.

### 2) Migrations de clés de configuration héritées

Quand la configuration contient des clés dépréciées, les autres commandes refusent de s'exécuter et vous demandent d'exécuter `openclaw doctor`.

Doctor va :

- Expliquer quelles clés héritées ont été trouvées.
- Afficher la migration qu'il a appliquée.
- Réécrire `~/.openclaw/openclaw.json` avec le schéma mis à jour.

La passerelle exécute aussi automatiquement les migrations doctor au démarrage quand elle détecte un format de configuration hérité, donc les configurations obsolètes sont réparées sans intervention manuelle.

Migrations actuelles :

- `routing.allowFrom` → `channels.whatsapp.allowFrom`
- `routing.groupChat.requireMention` → `channels.whatsapp/telegram/imessage.groups."*".requireMention`
- `routing.groupChat.historyLimit` → `messages.groupChat.historyLimit`
- `routing.groupChat.mentionPatterns` → `messages.groupChat.mentionPatterns`
- `routing.queue` → `messages.queue`
- `routing.bindings` → `bindings` de niveau supérieur
- `routing.agents`/`routing.defaultAgentId` → `agents.list` + `agents.list[].default`
- `routing.agentToAgent` → `tools.agentToAgent`
- `routing.transcribeAudio` → `tools.media.audio.models`
- `bindings[].match.accountID` → `bindings[].match.accountId`
- Pour les canaux avec `accounts` nommés mais sans `accounts.default`, déplacer les valeurs de canal de compte unique de niveau supérieur dans `channels.<channel>.accounts.default` quand présent
- `identity` → `agents.list[].identity`
- `agent.*` → `agents.defaults` + `tools.*` (tools/elevated/exec/sandbox/subagents)
- `agent.model`/`allowedModels`/`modelAliases`/`modelFallbacks`/`imageModelFallbacks`
  → `agents.defaults.models` + `agents.defaults.model.primary/fallbacks` + `agents.defaults.imageModel.primary/fallbacks`
- `browser.ssrfPolicy.allowPrivateNetwork` → `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`

Les avertissements de Doctor incluent aussi des conseils de compte par défaut pour les canaux multi-comptes :

- Si deux ou plus d'entrées `channels.<channel>.accounts` sont configurées sans `channels.<channel>.defaultAccount` ou `accounts.default`, doctor avertit que le routage de secours peut choisir un compte inattendu.
- Si `channels.<channel>.defaultAccount` est défini sur un ID de compte inconnu, doctor avertit et liste les ID de compte configurés.

### 2b) Remplacements du fournisseur OpenCode

Si vous avez ajouté `models.providers.opencode`, `opencode-zen` ou `opencode-go` manuellement, cela remplace le catalogue OpenCode intégré de `@mariozechner/pi-ai`.
Cela peut forcer les modèles sur la mauvaise API ou annuler les coûts. Doctor avertit pour que vous puissiez supprimer le remplacement et restaurer le routage API par modèle + les coûts.

### 3) Migrations d'état hérité (disposition du disque)

Doctor peut migrer les dispositions sur disque plus anciennes dans la structure actuelle :

- Magasin de sessions + transcriptions :
  - de `~/.openclaw/sessions/` à `~/.openclaw/agents/<agentId>/sessions/`
- Répertoire agent :
  - de `~/.openclaw/agent/` à `~/.openclaw/agents/<agentId>/agent/`
- État d'authentification WhatsApp (Baileys) :
  - de `~/.openclaw/credentials/*.json` hérité (sauf `oauth.json`)
  - à `~/.openclaw/credentials/whatsapp/<accountId>/...` (ID de compte par défaut : `default`)

Ces migrations sont au mieux et idempotentes ; doctor émettra des avertissements quand il laisse des dossiers hérités en tant que sauvegardes. La passerelle/CLI migre aussi automatiquement les sessions héritées + le répertoire agent au démarrage pour que l'historique/authentification/modèles se retrouvent dans le chemin par agent sans exécution manuelle de doctor. L'authentification WhatsApp est intentionnellement migrée uniquement via `openclaw doctor`.

### 3b) Migrations du magasin cron hérité

Doctor vérifie aussi le magasin de travaux cron (`~/.openclaw/cron/jobs.json` par défaut, ou `cron.store` quand remplacé) pour les anciennes formes de travaux que le planificateur accepte toujours pour la compatibilité.

Les nettoyages cron actuels incluent :

- `jobId` → `id`
- `schedule.cron` → `schedule.expr`
- champs de charge utile de niveau supérieur (`message`, `model`, `thinking`, ...) → `payload`
- champs de livraison de niveau supérieur (`deliver`, `channel`, `to`, `provider`, ...) → `delivery`
- alias de livraison `provider` de charge utile → `delivery.channel` explicite
- travaux webhook de secours `notify: true` simples hérités → `delivery.mode="webhook"` explicite avec `delivery.to=cron.webhook`

Doctor migre automatiquement uniquement les travaux `notify: true` quand il peut le faire sans changer le comportement. Si un travail combine le secours de notification hérité avec un mode de livraison non-webhook existant, doctor avertit et laisse ce travail pour examen manuel.

### 4) Vérifications d'intégrité d'état (persistance de session, routage et sécurité)

Le répertoire d'état est le tronc cérébral opérationnel. S'il disparaît, vous perdez les sessions, les identifiants, les journaux et la configuration (sauf si vous avez des sauvegardes ailleurs).

Doctor vérifie :

- **Répertoire d'état manquant** : avertit de la perte d'état catastrophique, invite à recréer le répertoire et vous rappelle qu'il ne peut pas récupérer les données manquantes.
- **Permissions du répertoire d'état** : vérifie la capacité d'écriture ; offre de réparer les permissions (et émet un indice `chown` quand une incompatibilité propriétaire/groupe est détectée).
- **Répertoire d'état synchronisé par le cloud macOS** : avertit quand l'état se résout sous iCloud Drive (`~/Library/Mobile Documents/com~apple~CloudDocs/...`) ou `~/Library/CloudStorage/...` car les chemins synchronisés peuvent causer des E/S plus lentes et des courses de verrouillage/synchronisation.
- **Répertoire d'état SD ou eMMC Linux** : avertit quand l'état se résout sur une source de montage `mmcblk*`, car les E/S aléatoires SD ou eMMC peuvent être plus lentes et s'user plus vite sous les écritures de session et d'identifiants.
- **Répertoires de session manquants** : `sessions/` et le répertoire du magasin de sessions sont nécessaires pour persister l'historique et éviter les plantages `ENOENT`.
- **Incompatibilité de transcription** : avertit quand les entrées de session récentes ont des fichiers de transcription manquants.
- **Session principale "1-line JSONL"** : signale quand la transcription principale n'a qu'une seule ligne (l'historique ne s'accumule pas).
- **Répertoires d'état multiples** : avertit quand plusieurs dossiers `~/.openclaw` existent dans les répertoires personnels ou quand `OPENCLAW_STATE_DIR` pointe ailleurs (l'historique peut se diviser entre les installations).
- **Rappel du mode distant** : si `gateway.mode=remote`, doctor vous rappelle de l'exécuter sur l'hôte distant (l'état y vit).
- **Permissions du fichier de configuration** : avertit si `~/.openclaw/openclaw.json` est lisible par le groupe/monde et offre de resserrer à `600`.

### 5) Santé de l'authentification du modèle (expiration OAuth)

Doctor inspecte les profils OAuth dans le magasin d'authentification, avertit quand les jetons expirent/sont expirés et peut les actualiser quand c'est sûr. Si le profil Claude Code Anthropic est obsolète, il suggère d'exécuter `claude setup-token` (ou de coller un setup-token).
Les invites d'actualisation n'apparaissent que lors de l'exécution interactive (TTY) ; `--non-interactive` ignore les tentatives d'actualisation.

Doctor signale aussi les profils d'authentification temporairement inutilisables en raison de :

- refroidissements courts (limites de débit/délais d'expiration/échecs d'authentification)
- désactivations plus longues (facturation/échecs de crédit)

### 6) Validation du modèle de hooks

Si `hooks.gmail.model` est défini, doctor valide la référence du modèle par rapport au catalogue et à la liste d'autorisation et avertit quand il ne se résoudra pas ou est interdit.

### 7) Réparation d'image sandbox

Quand le sandboxing est activé, doctor vérifie les images Docker et offre de construire ou de basculer vers des noms hérités si l'image actuelle est manquante.

### 8) Migrations de service de passerelle et conseils de nettoyage

Doctor détecte les services de passerelle hérités (launchd/systemd/schtasks) et offre de les supprimer et d'installer le service OpenClaw en utilisant le port de passerelle actuel. Il peut aussi analyser les services de type passerelle supplémentaires et imprimer des conseils de nettoyage.
Les services de passerelle OpenClaw nommés par profil sont considérés comme de première classe et ne sont pas signalés comme « supplémentaires ».

### 9) Avertissements de sécurité

Doctor é
