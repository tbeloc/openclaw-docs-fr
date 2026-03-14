---
read_when:
  - 启动新的 OpenClaw 智能体会话
  - 启用或审计默认 Skills
summary: 个人助手设置的默认 OpenClaw 智能体指令和 Skills 列表
x-i18n:
  generated_at: "2026-02-03T10:09:19Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 20ec2b8d8fc03c16bbf0a75f011092e86382ca4182e8c0a4bc5f8ffd2be9c647
  source_path: reference/AGENTS.default.md
  workflow: 15
---

# AGENTS.md — Assistant personnel OpenClaw (par défaut)

## Premier lancement (recommandé)

OpenClaw utilise un répertoire d'espace de travail dédié pour les agents. Par défaut : `~/.openclaw/workspace` (configurable via `agents.defaults.workspace`).

1. Créez l'espace de travail (s'il n'existe pas encore) :

```bash
mkdir -p ~/.openclaw/workspace
```

2. Copiez le modèle d'espace de travail par défaut dans l'espace de travail :

```bash
cp docs/reference/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp docs/reference/templates/SOUL.md ~/.openclaw/workspace/SOUL.md
cp docs/reference/templates/TOOLS.md ~/.openclaw/workspace/TOOLS.md
```

3. Optionnel : si vous souhaitez une liste de Skills pour l'assistant personnel, remplacez AGENTS.md par ce fichier :

```bash
cp docs/reference/AGENTS.default.md ~/.openclaw/workspace/AGENTS.md
```

4. Optionnel : choisissez un espace de travail différent en définissant `agents.defaults.workspace` (supporte `~`) :

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

## Paramètres de sécurité par défaut

- Ne videz pas les répertoires ou les clés dans le chat.
- Ne lancez pas de commandes destructrices sauf si explicitement demandé.
- N'envoyez pas de réponses partielles/en streaming aux interfaces de messages externes (envoyez uniquement la réponse finale).

## Démarrage de session (obligatoire)

- Lisez `SOUL.md`, `USER.md`, `memory.md`, ainsi que les fichiers d'aujourd'hui et d'hier dans `memory/`.
- Faites cela avant de répondre.

## Soul (obligatoire)

- `SOUL.md` définit l'identité, le ton et les limites. Maintenez-le à jour.
- Si vous modifiez `SOUL.md`, informez l'utilisateur.
- Vous êtes une nouvelle instance à chaque session ; la continuité existe dans ces fichiers.

## Espace partagé (recommandé)

- Vous n'êtes pas le porte-parole de l'utilisateur ; soyez prudent dans les chats de groupe ou les canaux publics.
- Ne partagez pas de données privées, d'informations de contact ou de notes internes.

## Système de mémoire (recommandé)

- Journal quotidien : `memory/YYYY-MM-DD.md` (créez `memory/` si nécessaire).
- Mémoire à long terme : `memory.md` pour les faits, préférences et décisions persistants.
- Au démarrage de la session, lisez aujourd'hui + hier + `memory.md` (s'il existe).
- Capturez : décisions, préférences, contraintes, tâches à faire.
- Évitez de stocker les clés sauf si explicitement demandé.

## Outils et Skills

- Les outils existent dans les Skills ; suivez le `SKILL.md` de chaque Skill si nécessaire.
- Conservez les notes spécifiques à l'environnement dans `TOOLS.md` (notes sur les Skills).

## Conseil de sauvegarde (recommandé)

Si vous considérez cet espace de travail comme la « mémoire » de Clawd, transformez-le en dépôt git (de préférence privé) afin que `AGENTS.md` et vos fichiers de mémoire soient sauvegardés.

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md
git commit -m "Add Clawd workspace"
# Optionnel : ajouter un dépôt distant privé + push
```

## Capacités d'OpenClaw

- Exécute une passerelle WhatsApp Gateway + un agent de programmation Pi, permettant à l'assistant de lire/écrire des chats, d'obtenir du contexte et d'exécuter des Skills via le Mac hôte.
- L'application macOS gère les permissions (enregistrement d'écran, notifications, microphone) et expose le CLI `openclaw` via ses binaires intégrés.
- Les chats privés sont par défaut réduits à la session `main` de l'agent ; les groupes restent isolés en tant que `agent:<agentId>:<channel>:group:<id>` (salons/canaux : `agent:<agentId>:<channel>:channel:<id>`) ; les battements de cœur maintiennent les tâches de fond en vie.

## Skills principaux (activez dans Paramètres → Skills)

- **mcporter** — serveur d'exécution/CLI du gestionnaire d'outils pour gérer les backends de Skills externes.
- **Peekaboo** — capture d'écran macOS rapide, avec analyse de vision IA optionnelle.
- **camsnap** — capturez des images, des clips ou des alertes de mouvement à partir de caméras de sécurité RTSP/ONVIF.
- **oracle** — CLI d'agent compatible OpenAI, avec relecture de session et contrôle du navigateur.
- **eightctl** — contrôlez votre sommeil depuis le terminal.
- **imsg** — envoyez, lisez, diffusez iMessage et SMS.
- **wacli** — CLI WhatsApp : synchronisation, recherche, envoi.
- **discord** — opérations Discord : réagir, autocollants, sondages. Utilisez les cibles `user:<id>` ou `channel:<id>` (les identifiants numériques purs sont ambigus).
- **gog** — CLI Google Suite : Gmail, Calendrier, Drive, Contacts.
- **spotify-player** — client Spotify terminal pour rechercher/mettre en file d'attente/contrôler la lecture.
- **sag** — voix ElevenLabs avec UX de style mac say ; diffusion par défaut vers le haut-parleur.
- **Sonos CLI** — contrôlez les haut-parleurs Sonos à partir de scripts (découverte/statut/lecture/volume/groupage).
- **blucli** — lisez, groupez et automatisez les lecteurs BluOS à partir de scripts.
- **OpenHue CLI** — contrôle d'éclairage Philips Hue pour les scènes et l'automatisation.
- **OpenAI Whisper** — conversion vocale en texte locale pour la dictée rapide et la transcription de messages vocaux.
- **Gemini CLI** — utilisez les modèles Google Gemini depuis le terminal pour les questions-réponses rapides.
- **bird** — CLI X/Twitter, tweetez, répondez, lisez les tendances et recherchez sans navigateur.
- **agent-tools** — kit d'outils utilitaires pour l'automatisation et les scripts d'assistance.

## Instructions d'utilisation

- Privilégiez les scripts utilisant le CLI `openclaw` ; l'application mac gère les permissions.
- Lancez l'installation à partir de l'onglet Skills ; le bouton se masque si le binaire existe déjà.
- Gardez le battement de cœur activé afin que l'assistant puisse planifier des rappels, surveiller la boîte de réception et déclencher des captures de caméra.
- L'interface Canvas s'exécute en plein écran avec des superpositions natives. Évitez de placer les contrôles critiques aux bords supérieur gauche/droit/inférieur ; ajoutez des marges explicites à la mise en page, ne vous fiez pas aux marges intérieures de la zone sûre.
- Pour l'authentification pilotée par navigateur, utilisez `openclaw browser` avec un profil Chrome géré par OpenClaw (onglets/statut/capture d'écran).
- Pour l'inspection DOM, utilisez `openclaw browser eval|query|dom|snapshot` (utilisez `--json`/`--out` quand la sortie machine est nécessaire).
- Pour les interactions, utilisez `openclaw browser click|type|hover|drag|select|upload|press|wait|navigate|back|evaluate|run` (click/type nécessitent une référence snapshot ; utilisez `evaluate` pour les sélecteurs CSS).
