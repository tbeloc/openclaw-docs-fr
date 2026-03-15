---
summary: "Assistant d'intégration CLI : configuration guidée pour la passerelle, l'espace de travail, les canaux et les compétences"
read_when:
  - Running or configuring the onboarding wizard
  - Setting up a new machine
title: "Assistant d'intégration (CLI)"
sidebarTitle: "Intégration : CLI"
---

# Assistant d'intégration (CLI)

L'assistant d'intégration est le moyen **recommandé** de configurer OpenClaw sur macOS,
Linux ou Windows (via WSL2 ; fortement recommandé).
Il configure une passerelle locale ou une connexion à une passerelle distante, ainsi que les canaux, les compétences
et les paramètres par défaut de l'espace de travail dans un flux guidé unique.

```bash
openclaw onboard
```

<Info>
Chat le plus rapide : ouvrez l'interface de contrôle (aucune configuration de canal nécessaire). Exécutez
`openclaw dashboard` et discutez dans le navigateur. Documentation : [Tableau de bord](/fr/web/dashboard).
</Info>

Pour reconfigurer ultérieurement :

```bash
openclaw configure
openclaw agents add <name>
```

<Note>
`--json` n'implique pas le mode non-interactif. Pour les scripts, utilisez `--non-interactive`.
</Note>

<Tip>
L'assistant d'intégration comprend une étape de recherche web où vous pouvez choisir un fournisseur
(Perplexity, Brave, Gemini, Grok ou Kimi) et coller votre clé API pour que l'agent
puisse utiliser `web_search`. Vous pouvez également configurer cela ultérieurement avec
`openclaw configure --section web`. Documentation : [Outils web](/fr/tools/web).
</Tip>

## Démarrage rapide vs Avancé

L'assistant commence par **Démarrage rapide** (paramètres par défaut) vs **Avancé** (contrôle total).

<Tabs>
  <Tab title="Démarrage rapide (paramètres par défaut)">
    - Passerelle locale (loopback)
    - Espace de travail par défaut (ou espace de travail existant)
    - Port de la passerelle **18789**
    - Authentification de la passerelle **Jeton** (généré automatiquement, même sur loopback)
    - Politique d'outils par défaut pour les nouvelles configurations locales : `tools.profile: "coding"` (le profil explicite existant est conservé)
    - Isolation DM par défaut : l'intégration CLI locale écrit `session.dmScope: "per-channel-peer"` lorsqu'il n'est pas défini. Détails : [Référence d'intégration CLI](/fr/start/wizard-cli-reference#outputs-and-internals)
    - Exposition Tailscale **Désactivée**
    - Les DM Telegram + WhatsApp utilisent par défaut une **liste d'autorisation** (vous serez invité à entrer votre numéro de téléphone)
  </Tab>
  <Tab title="Avancé (contrôle total)">
    - Expose chaque étape (mode, espace de travail, passerelle, canaux, démon, compétences).
  </Tab>
</Tabs>

## Ce que configure l'assistant

**Mode local (par défaut)** vous guide à travers ces étapes :

1. **Modèle/Authentification** — choisissez n'importe quel fournisseur/flux d'authentification pris en charge (clé API, OAuth ou jeton de configuration), y compris le fournisseur personnalisé
   (compatible OpenAI, compatible Anthropic ou détection automatique inconnue). Choisissez un modèle par défaut.
   Note de sécurité : si cet agent exécutera des outils ou traitera du contenu webhook/hooks, préférez le modèle de dernière génération le plus puissant disponible et maintenez une politique d'outils stricte. Les niveaux plus faibles/plus anciens sont plus faciles à injecter par prompt.
   Pour les exécutions non-interactives, `--secret-input-mode ref` stocke les références soutenues par env dans les profils d'authentification au lieu des valeurs de clé API en texte brut.
   En mode non-interactif `ref`, la variable d'environnement du fournisseur doit être définie ; passer des drapeaux de clé en ligne sans cette variable d'environnement échoue rapidement.
   Dans les exécutions interactives, choisir le mode de référence secrète vous permet de pointer vers une variable d'environnement ou une référence de fournisseur configurée (`file` ou `exec`), avec une validation préalable rapide avant l'enregistrement.
2. **Espace de travail** — Emplacement des fichiers d'agent (par défaut `~/.openclaw/workspace`). Amorce les fichiers de démarrage.
3. **Passerelle** — Port, adresse de liaison, mode d'authentification, exposition Tailscale.
   En mode jeton interactif, choisissez le stockage de jeton en texte brut par défaut ou optez pour SecretRef.
   Chemin SecretRef de jeton non-interactif : `--gateway-token-ref-env <ENV_VAR>`.
4. **Canaux** — WhatsApp, Telegram, Discord, Google Chat, Mattermost, Signal, BlueBubbles ou iMessage.
5. **Démon** — Installe un LaunchAgent (macOS) ou une unité utilisateur systemd (Linux/WSL2).
   Si l'authentification par jeton nécessite un jeton et que `gateway.auth.token` est géré par SecretRef, l'installation du démon le valide mais ne persiste pas le jeton résolu dans les métadonnées d'environnement du service superviseur.
   Si l'authentification par jeton nécessite un jeton et que la SecretRef de jeton configurée n'est pas résolue, l'installation du démon est bloquée avec des conseils exploitables.
   Si `gateway.auth.token` et `gateway.auth.password` sont tous deux configurés et que `gateway.auth.mode` n'est pas défini, l'installation du démon est bloquée jusqu'à ce que le mode soit défini explicitement.
6. **Vérification de santé** — Démarre la passerelle et vérifie qu'elle s'exécute.
7. **Compétences** — Installe les compétences recommandées et les dépendances optionnelles.

<Note>
Réexécuter l'assistant ne **supprime** rien à moins que vous ne choisissiez explicitement **Réinitialiser** (ou que vous passiez `--reset`).
CLI `--reset` utilise par défaut la configuration, les identifiants et les sessions ; utilisez `--reset-scope full` pour inclure l'espace de travail.
Si la configuration est invalide ou contient des clés héritées, l'assistant vous demande d'exécuter d'abord `openclaw doctor`.
</Note>

**Mode distant** configure uniquement le client local pour se connecter à une passerelle ailleurs.
Il n'installe ni ne change rien sur l'hôte distant.

## Ajouter un autre agent

Utilisez `openclaw agents add <name>` pour créer un agent séparé avec son propre espace de travail,
ses sessions et ses profils d'authentification. L'exécution sans `--workspace` lance l'assistant.

Ce qu'il définit :

- `agents.list[].name`
- `agents.list[].workspace`
- `agents.list[].agentDir`

Notes :

- Les espaces de travail par défaut suivent `~/.openclaw/workspace-<agentId>`.
- Ajoutez `bindings` pour router les messages entrants (l'assistant peut le faire).
- Drapeaux non-interactifs : `--model`, `--agent-dir`, `--bind`, `--non-interactive`.

## Référence complète

Pour des ventilations détaillées étape par étape et les résultats de configuration, consultez
[Référence d'intégration CLI](/fr/start/wizard-cli-reference).
Pour des exemples non-interactifs, consultez [Automatisation CLI](/fr/start/wizard-cli-automation).
Pour la référence technique plus approfondie, y compris les détails RPC, consultez
[Référence de l'assistant](/fr/reference/wizard).

## Documentation connexe

- Référence de commande CLI : [`openclaw onboard`](/fr/cli/onboard)
- Aperçu de l'intégration : [Aperçu de l'intégration](/fr/start/onboarding-overview)
- Intégration de l'application macOS : [Intégration](/fr/start/onboarding)
- Rituel de première exécution de l'agent : [Amorçage de l'agent](/fr/start/bootstrapping)
