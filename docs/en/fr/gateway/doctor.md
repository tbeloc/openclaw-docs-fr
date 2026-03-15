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

Accepte les valeurs par défaut sans demander de confirmation (y compris les étapes de réparation de redémarrage/service/sandbox le cas échéant).

```bash
openclaw doctor --repair
```

Applique les réparations recommandées sans demander de confirmation (réparations + redémarrages si sûr).

```bash
openclaw doctor --repair --force
```

Applique également les réparations agressives (écrase les configurations supervisor personnalisées).

```bash
openclaw doctor --non-interactive
```

Exécute sans invites et applique uniquement les migrations sûres (normalisation de configuration + déplacements d'état sur disque). Ignore les actions de redémarrage/service/sandbox qui nécessitent une confirmation humaine.
Les migrations d'état hérité s'exécutent automatiquement lorsqu'elles sont détectées.

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
- Vérification de la fraîcheur du protocole UI (reconstruit l'interface de contrôle lorsque le schéma de protocole est plus récent).
- Vérification de santé + invite de redémarrage.
- Résumé du statut des compétences (éligible/manquant/bloqué).
- Normalisation de la configuration pour les valeurs héritées.
- Avertissements de remplacement du fournisseur OpenCode (`models.providers.opencode` / `models.providers.opencode-go`).
- Migration d'état hérité sur disque (sessions/répertoire agent/authentification WhatsApp).
- Migration du magasin cron hérité (`jobId`, `schedule.cron`, champs de livraison/charge utile de niveau supérieur, `provider` de charge utile, travaux webhook de secours simples `notify: true`).
- Vérifications d'intégrité et de permissions d'état (sessions, transcriptions, répertoire d'état).
- Vérifications des permissions des fichiers de configuration (chmod 600) lors de l'exécution locale.
- Santé de l'authentification du modèle : vérifie l'expiration OAuth, peut actualiser les jetons arrivant à expiration et signale les états de refroidissement/désactivation du profil d'authentification.
- Détection de répertoire d'espace de travail supplémentaire (`~/openclaw`).
- Réparation de l'image sandbox lorsque le sandboxing est activé.
- Migration de service hérité et détection de passerelle supplémentaire.
- Vérifications du runtime de la passerelle (service installé mais non exécuté ; étiquette launchd mise en cache).
- Avertissements de statut du canal (sondés à partir de la passerelle en cours d'exécution).
- Audit de configuration supervisor (launchd/systemd/schtasks) avec réparation optionnelle.
- Vérifications des meilleures pratiques du runtime de la passerelle (Node vs Bun, chemins du gestionnaire de versions).
- Diagnostics de collision de port de passerelle (par défaut `18789`).
- Avertissements de sécurité pour les politiques DM ouvertes.
- Vérifications d'authentification de la passerelle pour le mode de jeton local (propose la génération de jeton lorsqu'aucune source de jeton n'existe ; ne remplace pas les configurations SecretRef de jeton).
- Vérification de linger systemd sur Linux.
- Vérifications d'installation source (incompatibilité d'espace de travail pnpm, ressources UI manquantes, binaire tsx manquant).
- Écrit la configuration mise à jour + métadonnées de l'assistant.

## Comportement détaillé et justification

### 0) Mise à jour optionnelle (installations git)

Si c'est un checkout git et que doctor s'exécute de manière interactive, il propose de
mettre à jour (fetch/rebase/build) avant d'exécuter doctor.

### 1) Normalisation de la configuration

Si la configuration contient des formes de valeurs héritées (par exemple `messages.ackReaction`
sans un remplacement spécifique au canal), doctor les normalise dans le schéma actuel.

### 2) Migrations de clés de configuration héritées

Lorsque la configuration contient des clés obsolètes, les autres commandes refusent de s'exécuter et vous demandent
d'exécuter `openclaw doctor`.

Doctor va :

- Expliquer quelles clés héritées ont été trouvées.
- Afficher la migration qu'il a appliquée.
- Réécrire `~/.openclaw/openclaw.json` avec le schéma mis à jour.

La Gateway exécute également automatiquement les migrations doctor au démarrage lorsqu'elle détecte un
format de configuration hérité, de sorte que les configurations obsolètes sont réparées sans intervention manuelle.

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
- Pour les canaux avec des `accounts` nommés mais sans `accounts.default`, déplacer les valeurs de canal à compte unique au niveau supérieur dans `channels.<channel>.accounts.default` si présentes
- `identity` → `agents.list[].identity`
- `agent.*` → `agents.defaults` + `tools.*` (tools/elevated/exec/sandbox/subagents)
- `agent.model`/`allowedModels`/`modelAliases`/`modelFallbacks`/`imageModelFallbacks`
  → `agents.defaults.models` + `agents.defaults.model.primary/fallbacks` + `agents.defaults.imageModel.primary/fallbacks`
- `browser.ssrfPolicy.allowPrivateNetwork` → `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`

Les avertissements de Doctor incluent également des conseils de compte par défaut pour les canaux multi-comptes :

- Si deux ou plusieurs entrées `channels.<channel>.accounts` sont configurées sans `channels.<channel>.defaultAccount` ou `accounts.default`, doctor avertit que le routage de secours peut choisir un compte inattendu.
- Si `channels.<channel>.defaultAccount` est défini sur un ID de compte inconnu, doctor avertit et liste les ID de compte configurés.

### 2b) Remplacements du fournisseur OpenCode

Si vous avez ajouté `models.providers.opencode`, `opencode-zen` ou `opencode-go`
manuellement, cela remplace le catalogue OpenCode intégré de `@mariozechner/pi-ai`.
Cela peut forcer les modèles sur la mauvaise API ou annuler les coûts. Doctor avertit afin que vous
puissiez supprimer le remplacement et restaurer le routage par modèle + les coûts.

### 3) Migrations d'état héritées (disposition du disque)

Doctor peut migrer les dispositions plus anciennes sur disque dans la structure actuelle :

- Magasin de sessions + transcriptions :
  - de `~/.openclaw/sessions/` à `~/.openclaw/agents/<agentId>/sessions/`
- Répertoire d'agent :
  - de `~/.openclaw/agent/` à `~/.openclaw/agents/<agentId>/agent/`
- État d'authentification WhatsApp (Baileys) :
  - de `~/.openclaw/credentials/*.json` hérité (sauf `oauth.json`)
  - à `~/.openclaw/credentials/whatsapp/<accountId>/...` (ID de compte par défaut : `default`)

Ces migrations sont au mieux et idempotentes ; doctor émettra des avertissements lorsqu'il
laisse des dossiers hérités en tant que sauvegardes. La Gateway/CLI migre également automatiquement
les sessions héritées + le répertoire d'agent au démarrage afin que l'historique/l'authentification/les modèles se retrouvent dans
le chemin par agent sans une exécution manuelle de doctor. L'authentification WhatsApp est intentionnellement migrée uniquement via `openclaw doctor`.

### 3b) Migrations du magasin cron hérité

Doctor vérifie également le magasin de tâches cron (`~/.openclaw/cron/jobs.json` par défaut,
ou `cron.store` en cas de remplacement) pour les anciennes formes de tâches que le planificateur accepte toujours
pour la compatibilité.

Les nettoyages cron actuels incluent :

- `jobId` → `id`
- `schedule.cron` → `schedule.expr`
- champs de charge utile au niveau supérieur (`message`, `model`, `thinking`, ...) → `payload`
- champs de livraison au niveau supérieur (`deliver`, `channel`, `to`, `provider`, ...) → `delivery`
- alias de fournisseur de charge utile → `delivery.channel` explicite
- tâches webhook de secours `notify: true` héritées simples → `delivery.mode="webhook"` explicite avec `delivery.to=cron.webhook`

Doctor migre automatiquement uniquement les tâches `notify: true` lorsqu'il peut le faire sans
modifier le comportement. Si une tâche combine le secours de notification hérité avec un mode de livraison
non-webhook existant, doctor avertit et laisse cette tâche pour examen manuel.

### 4) Vérifications d'intégrité d'état (persistance de session, routage et sécurité)

Le répertoire d'état est le tronc cérébral opérationnel. S'il disparaît, vous perdez
les sessions, les identifiants, les journaux et la configuration (sauf si vous avez des sauvegardes ailleurs).

Doctor vérifie :

- **Répertoire d'état manquant** : avertit d'une perte d'état catastrophique, invite à recréer
  le répertoire et vous rappelle qu'il ne peut pas récupérer les données manquantes.
- **Permissions du répertoire d'état** : vérifie la capacité d'écriture ; propose de réparer les permissions
  (et émet un indice `chown` lorsqu'une non-correspondance de propriétaire/groupe est détectée).
- **Répertoire d'état synchronisé par le cloud macOS** : avertit lorsque l'état se résout sous iCloud Drive
  (`~/Library/Mobile Documents/com~apple~CloudDocs/...`) ou
  `~/Library/CloudStorage/...` car les chemins sauvegardés peuvent causer des E/S plus lentes
  et des courses de verrouillage/synchronisation.
- **Répertoire d'état Linux SD ou eMMC** : avertit lorsque l'état se résout sur une source de montage `mmcblk*`,
  car les E/S aléatoires sauvegardées par SD ou eMMC peuvent être plus lentes et s'user
  plus rapidement lors des écritures de session et d'identifiants.
- **Répertoires de session manquants** : `sessions/` et le répertoire du magasin de sessions sont
  requis pour persister l'historique et éviter les plantages `ENOENT`.
- **Non-correspondance de transcription** : avertit lorsque les entrées de session récentes ont des fichiers
  de transcription manquants.
- **Transcription de session principale "1-line JSONL"** : signale lorsque la transcription principale n'a qu'une
  ligne (l'historique ne s'accumule pas).
- **Répertoires d'état multiples** : avertit lorsque plusieurs dossiers `~/.openclaw` existent dans
  les répertoires personnels ou lorsque `OPENCLAW_STATE_DIR` pointe ailleurs (l'historique peut
  se diviser entre les installations).
- **Rappel du mode distant** : si `gateway.mode=remote`, doctor vous rappelle de l'exécuter
  sur l'hôte distant (l'état y réside).
- **Permissions du fichier de configuration** : avertit si `~/.openclaw/openclaw.json` est
  lisible par le groupe/monde et propose de resserrer à `600`.

### 5) Santé de l'authentification du modèle (expiration OAuth)

Doctor inspecte les profils OAuth dans le magasin d'authentification, avertit lorsque les jetons
expirent/ont expiré, et peut les actualiser lorsque c'est sûr. Si le profil Anthropic Claude Code
est obsolète, il suggère d'exécuter `claude setup-token` (ou de coller un setup-token).
Les invites d'actualisation n'apparaissent que lors de l'exécution interactive (TTY) ; `--non-interactive`
ignore les tentatives d'actualisation.

Doctor signale également les profils d'authentification qui sont temporairement inutilisables en raison de :

- délais d'attente courts (limites de débit/délais d'expiration/échecs d'authentification)
- désactivations plus longues (facturation/échecs de crédit)

### 6) Validation du modèle des hooks

Si `hooks.gmail.model` est défini, doctor valide la référence du modèle par rapport au
catalogue et à la liste d'autorisation et avertit lorsqu'il ne se résoudra pas ou est interdit.

### 7) Réparation de l'image sandbox

Lorsque le sandboxing est activé, doctor vérifie les images Docker et propose de construire ou
de basculer vers des noms hérités si l'image actuelle est manquante.

### 8) Migrations de service Gateway et conseils de nettoyage

Doctor détecte les services gateway hérités (launchd/systemd/schtasks) et
propose de les supprimer et d'installer le service OpenClaw en utilisant le port gateway actuel. Il peut également
analyser les services supplémentaires de type gateway et imprimer des conseils de nettoyage.
Les services gateway OpenClaw nommés par profil sont considérés comme de première classe et ne sont pas
signalés comme "supplémentaires".

### 9) Avertissements de sécurité

Doctor émet des avertissements lorsqu'un fournisseur est ouvert aux DM sans liste d'autorisation, ou
lorsqu'une politique est configurée de manière dangereuse.

### 10) systemd linger (Linux)

S'il s'exécute en tant que service utilisateur systemd, doctor s'assure que lingering est activé afin que la
gateway reste active après la déconnexion.

### 11) Statut des compétences

Doctor imprime un résumé rapide des compétences éligibles/manquantes/bloquées pour l'espace de travail actuel.

### 12) Vérifications d'authentification Gateway (jeton local)

Doctor vérifie la disponibilité de l'authentification par jeton gateway local.

- Si le mode jeton a besoin d'un jeton et qu'aucune source de jeton n'existe, doctor propose d'en générer un.
- Si `gateway.auth.token` est géré par SecretRef mais indisponible, doctor avertit et ne le remplace pas par du texte brut.
- `openclaw doctor --generate-gateway-token` force la génération uniquement lorsqu'aucune SecretRef de jeton n'est configurée.

### 12b) Réparations conscientes de SecretRef en lecture seule

Certains flux de réparation doivent inspecter les identifiants configurés sans affaiblir le comportement de fail-fast à l'exécution.

- `openclaw doctor --fix` utilise maintenant le même modèle de résumé SecretRef en lecture seule que les commandes de la famille status pour les réparations de configuration ciblées.
- Exemple : la réparation `allowFrom` / `groupAllowFrom` Telegram `@username` tente d'utiliser les identifiants de bot configurés lorsqu'ils sont disponibles.
- Si le jeton de bot Telegram est configuré via SecretRef mais indisponible dans le chemin de commande actuel, doctor signale que l'identifiant est configuré mais indisponible et ignore l'auto-résolution au lieu de planter ou de signaler incorrectement le jeton comme manquant.

### 13) Vérification de santé Gateway + redémarrage

Doctor exécute une vérification de santé et propose de redémarrer la gateway lorsqu'elle semble
malsaine.

### 14) Avertissements d'état du canal

Si la gateway est saine, doctor exécute une sonde d'état du canal et signale
les avertissements avec les corrections suggérées.

### 15) Audit de configuration du superviseur + réparation

Doctor vérifie la configuration du superviseur installée (launchd/systemd/schtasks) pour
les valeurs par défaut manquantes ou obsolètes (par exemple, les dépendances network-online systemd et
le délai de redémarrage). Lorsqu'il trouve une non-correspondance, il recommande une mise à jour et peut
réécrire le fichier de service/tâche aux valeurs par défaut actuelles.

Notes :

- `openclaw doctor` invite avant de réécrire la configuration du superviseur.
- `openclaw doctor --yes` accepte les invites de réparation par défaut.
- `openclaw doctor --repair` applique les corrections recommandées sans invites.
- `openclaw doctor --repair --force` remplace les configurations de superviseur personnalisées.
- Si l'authentification par jeton nécessite un jeton et que `gateway.auth.token` est géré par SecretRef, doctor valide la SecretRef mais ne persiste pas les valeurs de jeton en texte brut résolues dans les métadonnées d'environnement du service de superviseur.
- Si l'authentification par jeton nécessite un jeton et que la SecretRef de jeton configurée n'est pas résolue, doctor bloque le chemin d'installation/réparation avec des conseils exploitables.
- Si `gateway.auth.token` et `gateway.auth.password` sont tous deux configurés et que `gateway.auth.mode` n'est pas défini, doctor bloque l'installation/réparation jusqu'à ce que le mode soit défini explicitement.
- Pour les unités systemd utilisateur Linux, les vérifications de dérive de jeton doctor incluent maintenant les sources `Environment=` et `EnvironmentFile=` lors de la comparaison des métadonnées d'authentification du service.
- Vous pouvez toujours forcer une réécriture complète via `openclaw gateway install --force`.

### 16) Diagnostics de runtime + port Gateway

Doctor inspecte le runtime du service (PID, dernier statut de sortie) et avertit lorsque le
service est installé mais ne s'exécute pas réellement. Il vérifie également les collisions de port
sur le port gateway (par défaut `18789`) et signale les causes probables (gateway déjà
en cours d'exécution, tunnel SSH).

### 17) Meilleures pratiques de runtime Gateway

Doctor avertit lorsque le service gateway s'exécute sur Bun ou un chemin géré par version
(`nvm`, `fnm`, `volta`, `asdf`, etc.). Les canaux WhatsApp + Telegram nécessitent Node,
et les chemins du gestionnaire de version peuvent se casser après les mises à niveau car le service ne charge pas votre init shell. Doctor propose de migrer vers une installation Node système lorsqu'elle est disponible (Homebrew/apt/choco).

### 18) Écriture de configuration + métadonnées de l'assistant

Doctor persiste toute modification de configuration et horodate les métadonnées de l'assistant pour enregistrer l'exécution de doctor.

### 19) Conseils d'espace de travail (sauvegarde + système de mémoire)

Doctor suggère un système de mémoire d'espace de travail lorsqu'il est manquant et imprime un conseil de sauvegarde
si l'espace de travail n'est pas déjà sous git.

Voir [/concepts/agent-workspace](/fr/concepts/agent-workspace) pour un guide complet de
la structure de l'espace de travail et de la sauvegarde git (recommandé GitHub ou GitLab privé).
