---
summary: "FAQ: démarrage rapide et configuration initiale — installation, intégration, authentification, abonnements, défaillances initiales"
read_when:
  - Nouvelle installation, intégration bloquée ou erreurs au premier lancement
  - Choix de l'authentification et des abonnements aux fournisseurs
  - Impossible d'accéder à docs.openclaw.ai, impossible d'ouvrir le tableau de bord, installation bloquée
title: "FAQ: configuration initiale"
sidebarTitle: "FAQ premier lancement"
---

Questions et réponses sur le démarrage rapide et la configuration initiale. Pour les opérations quotidiennes, les modèles, l'authentification, les sessions et le dépannage, consultez la [FAQ](/fr/help/faq) principale.

## Démarrage rapide et configuration initiale

<AccordionGroup>
  <Accordion title="Je suis bloqué, quel est le moyen le plus rapide de me débloquer">
    Utilisez un agent IA local qui peut **voir votre machine**. C'est beaucoup plus efficace que de demander sur Discord, car la plupart des cas « je suis bloqué » sont des **problèmes de configuration locale ou d'environnement** que les assistants distants ne peuvent pas inspecter.

    - **Claude Code**: [https://www.anthropic.com/claude-code/](https://www.anthropic.com/claude-code/)
    - **OpenAI Codex**: [https://openai.com/codex/](https://openai.com/codex/)

    Ces outils peuvent lire le dépôt, exécuter des commandes, inspecter les journaux et aider à corriger votre configuration au niveau de la machine (PATH, services, permissions, fichiers d'authentification). Donnez-leur l'**intégralité du dépôt source** via l'installation modifiable (git) :

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
    ```

    Cela installe OpenClaw **à partir d'un dépôt git**, afin que l'agent puisse lire le code + la documentation et raisonner sur la version exacte que vous exécutez. Vous pouvez toujours revenir à la version stable plus tard en réexécutant l'installateur sans `--install-method git`.

    Conseil : demandez à l'agent de **planifier et superviser** la correction (étape par étape), puis exécutez uniquement les commandes nécessaires. Cela maintient les modifications petites et plus faciles à auditer.

    Si vous découvrez un vrai bug ou une correction, veuillez déposer un problème GitHub ou envoyer une PR :
    [https://github.com/openclaw/openclaw/issues](https://github.com/openclaw/openclaw/issues)
    [https://github.com/openclaw/openclaw/pulls](https://github.com/openclaw/openclaw/pulls)

    Commencez par ces commandes (partagez les résultats quand vous demandez de l'aide) :

    ```bash
    openclaw status
    openclaw models status
    openclaw doctor
    ```

    Ce qu'elles font :

    - `openclaw status` : aperçu rapide de la santé de la passerelle/agent + configuration de base.
    - `openclaw models status` : vérifie l'authentification du fournisseur + la disponibilité du modèle.
    - `openclaw doctor` : valide et répare les problèmes courants de configuration/état.

    Autres vérifications CLI utiles : `openclaw status --all`, `openclaw logs --follow`,
    `openclaw gateway status`, `openclaw health --verbose`.

    Boucle de débogage rapide : [Premières 60 secondes si quelque chose est cassé](#first-60-seconds-if-something-is-broken).
    Docs d'installation : [Install](/fr/install), [Drapeaux de l'installateur](/fr/install/installer), [Mise à jour](/fr/install/updating).

  </Accordion>

  <Accordion title="Le battement de cœur continue de sauter. Que signifient les raisons du saut ?">
    Raisons courantes du saut du battement de cœur :

    - `quiet-hours` : en dehors de la fenêtre d'heures actives configurée
    - `empty-heartbeat-file` : `HEARTBEAT.md` existe mais ne contient que des échafaudages vides/en-tête uniquement
    - `no-tasks-due` : le mode tâche `HEARTBEAT.md` est actif mais aucun des intervalles de tâche n'est dû
    - `alerts-disabled` : toute la visibilité du battement de cœur est désactivée (`showOk`, `showAlerts` et `useIndicator` sont tous désactivés)

    En mode tâche, les horodatages dus ne sont avancés qu'après qu'une exécution réelle du battement de cœur se termine. Les exécutions ignorées ne marquent pas les tâches comme terminées.

    Docs : [Heartbeat](/fr/gateway/heartbeat), [Automation & Tasks](/fr/automation).

  </Accordion>

  <Accordion title="Façon recommandée d'installer et de configurer OpenClaw">
    Le dépôt recommande d'exécuter à partir de la source et d'utiliser l'intégration :

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash
    openclaw onboard --install-daemon
    ```

    L'assistant peut également créer les ressources de l'interface utilisateur automatiquement. Après l'intégration, vous exécutez généralement la passerelle sur le port **18789**.

    À partir de la source (contributeurs/dev) :

    ```bash
    git clone https://github.com/openclaw/openclaw.git
    cd openclaw
    pnpm install
    pnpm build
    pnpm ui:build
    openclaw onboard
    ```

    Si vous n'avez pas encore d'installation globale, exécutez-la via `pnpm openclaw onboard`.

  </Accordion>

  <Accordion title="Comment ouvrir le tableau de bord après l'intégration ?">
    L'assistant ouvre votre navigateur avec une URL de tableau de bord propre (non tokenisée) immédiatement après l'intégration et imprime également le lien dans le résumé. Gardez cet onglet ouvert ; s'il ne s'est pas lancé, copiez/collez l'URL imprimée sur la même machine.
  </Accordion>

  <Accordion title="Comment authentifier le tableau de bord sur localhost par rapport à distant ?">
    **Localhost (même machine) :**

    - Ouvrez `http://127.0.0.1:18789/`.
    - S'il demande une authentification par secret partagé, collez le jeton configuré ou le mot de passe dans les paramètres de l'interface de contrôle.
    - Source du jeton : `gateway.auth.token` (ou `OPENCLAW_GATEWAY_TOKEN`).
    - Source du mot de passe : `gateway.auth.password` (ou `OPENCLAW_GATEWAY_PASSWORD`).
    - Si aucun secret partagé n'est configuré, générez un jeton avec `openclaw doctor --generate-gateway-token`.

    **Pas sur localhost :**

    - **Tailscale Serve** (recommandé) : gardez la liaison en boucle, exécutez `openclaw gateway --tailscale serve`, ouvrez `https://<magicdns>/`. Si `gateway.auth.allowTailscale` est `true`, les en-têtes d'identité satisfont l'authentification de l'interface de contrôle/WebSocket (pas de secret partagé collé, suppose un hôte de passerelle de confiance) ; les API HTTP nécessitent toujours une authentification par secret partagé sauf si vous utilisez délibérément l'entrée privée `none` ou l'authentification HTTP de proxy de confiance.
      Les mauvaises tentatives d'authentification Serve concurrentes du même client sont sérialisées avant que le limiteur d'authentification échouée les enregistre, donc la deuxième tentative échouée peut déjà afficher `retry later`.
    - **Liaison tailnet** : exécutez `openclaw gateway --bind tailnet --token "<token>"` (ou configurez l'authentification par mot de passe), ouvrez `http://<tailscale-ip>:18789/`, puis collez le secret partagé correspondant dans les paramètres du tableau de bord.
    - **Proxy inverse conscient de l'identité** : gardez la passerelle derrière un proxy de confiance non-boucle, configurez `gateway.auth.mode: "trusted-proxy"`, puis ouvrez l'URL du proxy.
    - **Tunnel SSH** : `ssh -N -L 18789:127.0.0.1:18789 user@host` puis ouvrez `http://127.0.0.1:18789/`. L'authentification par secret partagé s'applique toujours sur le tunnel ; collez le jeton ou le mot de passe configuré si vous y êtes invité.

    Voir [Dashboard](/fr/web/dashboard) et [Web surfaces](/fr/web) pour les modes de liaison et les détails d'authentification.

  </Accordion>

  <Accordion title="Pourquoi y a-t-il deux configurations d'approbation exec pour les approbations de chat ?">
    Elles contrôlent différentes couches :

    - `approvals.exec` : transfère les invites d'approbation aux destinations de chat
    - `channels.<channel>.execApprovals` : fait agir ce canal comme un client d'approbation natif pour les approbations exec

    La politique d'exécution de l'hôte est toujours la vraie porte d'approbation. La configuration de chat contrôle uniquement où les invites d'approbation apparaissent et comment les gens peuvent y répondre.

    Dans la plupart des configurations, vous n'avez **pas besoin des deux** :

    - Si le chat supporte déjà les commandes et les réponses, le `/approve` dans le même chat fonctionne via le chemin partagé.
    - Si un canal natif supporté peut déduire les approbateurs en toute sécurité, OpenClaw active maintenant automatiquement les approbations natives en priorité DM quand `channels.<channel>.execApprovals.enabled` n'est pas défini ou est `"auto"`.
    - Quand les cartes/boutons d'approbation natifs sont disponibles, cette interface utilisateur native est le chemin principal ; l'agent ne devrait inclure une commande `/approve` manuelle que si le résultat de l'outil indique que les approbations de chat ne sont pas disponibles ou que l'approbation manuelle est le seul chemin.
    - Utilisez `approvals.exec` uniquement quand les invites doivent aussi être transférées à d'autres chats ou salles d'opérations explicites.
    - Utilisez `channels.<channel>.execApprovals.target: "channel"` ou `"both"` uniquement quand vous voulez explicitement que les invites d'approbation soient affichées dans la salle/le sujet d'origine.
    - Les approbations de plugin sont à nouveau séparées : elles utilisent `/approve` dans le même chat par défaut, le transfert optionnel `approvals.plugin`, et seuls certains canaux natifs conservent la gestion native des approbations de plugin en plus.

    Version courte : le transfert est pour le routage, la configuration du client natif est pour une interface utilisateur plus riche spécifique au canal.
    Voir [Exec Approvals](/fr/tools/exec-approvals).

  </Accordion>

  <Accordion title="Quel runtime ai-je besoin ?">
    Node **>= 22** est requis. `pnpm` est recommandé. Bun n'est **pas recommandé** pour la passerelle.
  </Accordion>

  <Accordion title="Fonctionne-t-il sur Raspberry Pi ?">
    Oui. La passerelle est légère - la documentation liste **512 Mo-1 Go de RAM**, **1 cœur** et environ **500 Mo** de disque comme suffisant pour un usage personnel, et note qu'un **Raspberry Pi 4 peut l'exécuter**.

    Si vous voulez plus de marge (journaux, médias, autres services), **2 Go est recommandé**, mais ce n'est pas un minimum strict.

    Conseil : un petit Pi/VPS peut héberger la passerelle, et vous pouvez associer des **nœuds** sur votre ordinateur portable/téléphone pour l'accès à l'écran/caméra/canevas local ou l'exécution de commandes. Voir [Nodes](/fr/nodes).

  </Accordion>

  <Accordion title="Des conseils pour les installations Raspberry Pi ?">
    Version courte : ça marche, mais attendez-vous à des aspérités.

    - Utilisez un **système d'exploitation 64 bits** et gardez Node >= 22.
    - Préférez l'**installation modifiable (git)** pour pouvoir voir les journaux et mettre à jour rapidement.
    - Commencez sans canaux/compétences, puis ajoutez-les un par un.
    - Si vous rencontrez des problèmes binaires bizarres, c'est généralement un problème de **compatibilité ARM**.

    Docs : [Linux](/fr/platforms/linux), [Install](/fr/install).

  </Accordion>

  <Accordion title="C'est bloqué au réveil mon ami / l'intégration ne va pas éclore. Et maintenant ?">
    Cet écran dépend de la passerelle étant accessible et authentifiée. L'interface utilisateur textuelle envoie également « Wake up, my friend ! » automatiquement au premier éclosion. Si vous voyez cette ligne avec **pas de réponse** et les jetons restent à 0, l'agent n'a jamais fonctionné.

    1. Redémarrez la passerelle :

    ```bash
    openclaw gateway restart
    ```

    2. Vérifiez l'état + l'authentification :

    ```bash
    openclaw status
    openclaw models status
    openclaw logs --follow
    ```

    3. S'il reste bloqué, exécutez :

    ```bash
    openclaw doctor
    ```

    Si la passerelle est distante, assurez-vous que la connexion tunnel/Tailscale est active et que l'interface utilisateur pointe vers la bonne passerelle. Voir [Remote access](/fr/gateway/remote).

  </Accordion>

  <Accordion title="Puis-je migrer ma configuration vers une nouvelle machine (Mac mini) sans refaire l'intégration ?">
    Oui. Copiez le **répertoire d'état** et l'**espace de travail**, puis exécutez Doctor une fois. Cela garde votre bot « exactement le même » (mémoire, historique de session, authentification et état du canal) tant que vous copiez **les deux** emplacements :

    1. Installez OpenClaw sur la nouvelle machine.
    2. Copiez `$OPENCLAW_STATE_DIR` (par défaut : `~/.openclaw`) de l'ancienne machine.
    3. Copiez votre espace de travail (par défaut : `~/.openclaw/workspace`).
    4. Exécutez `openclaw doctor` et redémarrez le service de passerelle.

    Cela préserve la configuration, les profils d'authentification, les identifiants WhatsApp, les sessions et la mémoire. Si vous êtes en mode distant, rappelez-vous que l'hôte de la passerelle possède le magasin de sessions et l'espace de travail.

    **Important :** si vous ne validez/poussez que votre espace de travail vers GitHub, vous sauvegardez **la mémoire + les fichiers d'amorçage**, mais **pas** l'historique de session ou l'authentification. Ceux-ci vivent sous `~/.openclaw/` (par exemple `~/.openclaw/agents/<agentId>/sessions/`).

    Connexe : [Migrating](/fr/install/migrating), [Where things live on disk](#where-things-live-on-disk),
    [Agent workspace](/fr/concepts/agent-workspace), [Doctor](/fr/gateway/doctor),
    [Remote mode](/fr/gateway/remote).

  </Accordion>

  <Accordion title="Où puis-je voir ce qui est nouveau dans la dernière version ?">
    Vérifiez le journal des modifications GitHub :
    [https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

    Les entrées les plus récentes sont en haut. Si la section supérieure est marquée **Unreleased**, la section datée suivante est la dernière version expédiée. Les entrées sont groupées par **Highlights**, **Changes** et **Fixes** (plus les sections docs/autres si nécessaire).

  </Accordion>

  <Accordion title="Impossible d'accéder à docs.openclaw.ai (erreur SSL)">
    Certaines connexions Comcast/Xfinity bloquent incorrectement `docs.openclaw.ai` via Xfinity Advanced Security. Désactivez-le ou mettez en liste blanche `docs.openclaw.ai`, puis réessayez.
    Aidez-nous à le débloquer en signalant ici : [https://spa.xfinity.com/check_url_status](https://spa.xfinity.com/check_url_status).

    Si vous ne pouvez toujours pas accéder au site, la documentation est en miroir sur GitHub :
    [https://github.com/openclaw/openclaw/tree/main/docs](https://github.com/openclaw/openclaw/tree/main/docs)

  </Accordion>

  <Accordion title="Différence entre stable et bêta">
    **Stable** et **bêta** sont des **balises de distribution npm**, pas des lignes de code séparées :

    - `latest` = stable
    - `beta` = version précoce pour les tests

    Généralement, une version stable arrive d'abord sur **bêta**, puis une étape de promotion explicite déplace cette même version vers `latest`. Les responsables peuvent aussi publier directement sur `latest` si nécessaire. C'est pourquoi bêta et stable peuvent pointer vers la **même version** après promotion.

    Voir ce qui a changé :
    [https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

    Pour les one-liners d'installation et la différence entre bêta et dev, voir l'accordéon ci-dessous.

  </Accordion>

  <Accordion title="Comment installer la version bêta et quelle est la différence entre bêta et dev ?">
    **Bêta** est la balise de distribution npm `beta` (peut correspondre à `latest` après promotion).
    **Dev** est la tête mobile de `main` (git) ; quand elle est publiée, elle utilise la balise de distribution npm `dev`.

    One-liners (macOS/Linux) :

    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --beta
    ```

    ```bash
    curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git
    ```

    Installateur Windows (PowerShell) :
    [https://openclaw.ai/install.ps1](https://openclaw.ai/install.ps1)

    Plus de détails : [Development channels](/fr/install/development-channels) et [Installer flags](/fr/install/installer).

  </Accordion>

  <Accordion title="Comment essayer les derniers bits ?">
    Deux options :

    1. **Canal Dev (dépôt git) :**

    ```bash
    openclaw update --channel dev
    ```

    Cela bascule vers la branche `main` et met à jour à partir de la source.

    2. **Installation modifiable (à partir du site de l'installateur) :**

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
    ```

    Cela vous donne un dépôt local que vous pouvez modifier, puis mettre à jour via git.

    Si vous préférez un clone propre manuellement, utilisez :

    ```bash
    git clone https://github.com/openclaw/openclaw.git
    cd openclaw
    pnpm install
    pnpm build
    ```

    Docs : [Update](/fr/cli/update), [Development channels](/fr/install/development-channels),
    [Install](/fr/install).

  </Accordion>

  <Accordion title="Combien de temps prennent généralement l'installation et l'intégration ?">
    Guide approximatif :

    - **Installation :** 2-5 minutes
    - **Intégration :** 5-15 minutes selon le nombre de canaux/modèles que vous configurez

    S'il se bloque, utilisez [Installer stuck](#quick-start-and-first-run-setup)
    et la boucle de débogage rapide dans [I am stuck](#quick-start-and-first-run-setup).

  </Accordion>

  <Accordion title="L'installateur est bloqué ? Comment obtenir plus de retours ?">
    Réexécutez l'installateur avec **sortie détaillée** :

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose
    ```

    Installation bêta avec détails :

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash -s -- --beta --verbose
    ```

    Pour une installation modifiable (git) :

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --verbose
    ```

    Équivalent Windows (PowerShell) :

    ```powershell
    # install.ps1 n'a pas encore de drapeau -Verbose dédié.
    Set-PSDebug -Trace 1
    & ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
    Set-PSDebug -Trace 0
    ```

    Plus d'options : [Installer flags](/fr/install/installer).

  </Accordion>

  <Accordion title="L'installation Windows dit que git n'est pas trouvé ou openclaw n'est pas reconnu">
    Deux problèmes courants sous Windows :

    **1) erreur npm spawn git / git non trouvé**

    - Installez **Git for Windows** et assurez-vous que `git` est sur votre PATH.
    - Fermez et rouvrez PowerShell, puis réexécutez l'installateur.

    **2) openclaw n'est pas reconnu après l'installation**

    - Votre dossier bin global npm n'est pas sur PATH.
    - Vérifiez le chemin :

      ```powershell
      npm config get prefix
      ```

    - Ajoutez ce répertoire à votre PATH utilisateur (pas de suffixe `\bin` nécessaire sous Windows ; sur la plupart des systèmes c'est `%AppData%\npm`).
    - Fermez et rouvrez PowerShell après la mise à jour de PATH.

    Si vous voulez la configuration Windows la plus fluide, utilisez **WSL2** à la place de Windows natif.
    Docs : [Windows](/fr/platforms/windows).

  </Accordion>

  <Accordion title="La sortie exec Windows affiche du texte chinois brouillé - que dois-je faire ?">
    C'est généralement une incompatibilité de page de code de console sur les shells Windows natifs.

    Symptômes :

    - La sortie `system.run`/`exec` affiche le chinois comme du charabia
    - La même commande semble correcte dans un autre profil de terminal

    Contournement rapide dans PowerShell :

    ```powershell
    chcp 65001
    [Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    ```

    Puis redémarrez la passerelle et réessayez votre commande :

    ```powershell
    openclaw gateway restart
    ```

    Si vous reproduisez toujours cela sur la dernière version d'OpenClaw, suivez/signalez-le dans :

    - [Issue #30640](https://github.com/openclaw/openclaw/issues/30640)

  </Accordion>

  <Accordion title="La documentation n'a pas répondu à ma question - comment obtenir une meilleure réponse ?">
    Utilisez l'**installation modifiable (git)** pour avoir la source complète et la documentation localement, puis demandez à votre bot (ou Claude/Codex) _à partir de ce dossier_ pour qu'il puisse lire le dépôt et répondre précisément.

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git
    ```

    Plus de détails : [Install](/fr/install) et [Installer flags](/fr/install/installer).

  </Accordion>

  <Accordion title="Comment installer OpenClaw sur Linux ?">
    Réponse courte : suivez le guide Linux, puis exécutez l'intégration.

    - Chemin rapide Linux + installation du service : [Linux](/fr/platforms/linux).
    - Procédure complète : [Getting Started](/fr/start/getting-started).
    - Installateur + mises à jour : [Install & updates](/fr/install/updating).

  </Accordion>

  <Accordion title="Comment installer OpenClaw sur un VPS ?">
    N'importe quel VPS Linux fonctionne. Installez sur le serveur, puis utilisez SSH/Tailscale pour atteindre la passerelle.

    Guides : [exe.dev](/fr/install/exe-dev), [Hetzner](/fr/install/hetzner), [Fly.io](/fr/install/fly).
    Accès distant : [Gateway remote](/fr/gateway/remote).

  </Accordion>

  <Accordion title="Où sont les guides d'installation cloud/VPS ?">
    Nous maintenons un **hub d'hébergement** avec les fournisseurs courants. Choisissez-en un et suivez le guide :

    - [VPS hosting](/fr/vps) (tous les fournisseurs en un seul endroit)
    - [Fly.io](/fr/install/fly)
    - [Hetzner](/fr/install/hetzner)
    - [exe.dev](/fr/install/exe-dev)

    Comment ça marche dans le cloud : la **passerelle s'exécute sur le serveur**, et vous y accédez depuis votre ordinateur portable/téléphone via l'interface utilisateur de contrôle (ou Tailscale/SSH). Votre état + espace de travail vivent sur le serveur, donc traitez l'hôte comme la source de vérité et sauvegardez-le.

    Vous pouvez associer des **nœuds** (Mac/iOS/Android/headless) à cette passerelle cloud pour accéder à l'écran/caméra/canevas local ou exécuter des commandes sur votre ordinateur portable tout en gardant la passerelle dans le cloud.

    Hub : [Platforms](/fr/platforms). Accès distant : [Gateway remote](/fr/gateway/remote).
    Nœuds : [Nodes](/fr/nodes), [Nodes CLI](/fr/cli/nodes).

  </Accordion>

  <Accordion title="Puis-je demander à OpenClaw de se mettre à jour lui-même ?">
    Réponse courte : **possible, non recommandé**. Le flux de mise à jour peut redémarrer la passerelle (ce qui abandonne la session active), peut nécessiter un dépôt git propre et peut demander une confirmation. Plus sûr : exécutez les mises à jour à partir d'un shell en tant qu'opérateur.

    Utilisez l'interface de ligne de commande :

    ```bash
    openclaw update
    openclaw update status
    openclaw update --channel stable|beta|dev
    openclaw update --tag <dist-tag|version>
    openclaw update --no-restart
    ```

    Si vous devez automatiser à partir d'un agent :

    ```bash
    openclaw update --yes --no-restart
    openclaw gateway restart
    ```

    Docs : [Update](/fr/cli/update), [Updating](/fr/install/updating).

  </Accordion>

  <Accordion title="Que fait exactement l'intégration ?">
    `openclaw onboard` est le chemin de configuration recommandé. En **mode local**, il vous guide à travers :

    - **Configuration du modèle/authentification** (OAuth du fournisseur, clés API, jeton de configuration Anthropic, plus les options de modèles locaux comme LM Studio)
    - **Emplacement de l'espace de travail** + fichiers d'amorçage
    - **Paramètres de la passerelle** (liaison/port/authentification/tailscale)
    - **Canaux** (WhatsApp, Telegram, Discord, Mattermost, Signal, iMessage, plus les plugins de canal groupés comme QQ Bot)
    - **Installation du démon** (LaunchAgent sur macOS ; unité utilisateur systemd sur Linux/WSL2)
    - **Vérifications de santé** et sélection des **compétences**

    Il avertit également si votre modèle configuré est inconnu ou manque d'authentification.

  </Accordion>

  <Accordion title="Ai-je besoin d'un abonnement Claude ou OpenAI pour exécuter ceci ?">
    Non. Vous pouvez exécuter OpenClaw avec des **clés API** (Anthropic/OpenAI/autres) ou avec des **modèles locaux uniquement** pour que vos données restent sur votre appareil. Les abonnements (Claude Pro/Max ou OpenAI Codex) sont des façons optionnelles de s'authentifier auprès de ces fournisseurs.

    Pour Anthropic dans OpenClaw, la division pratique est :

    - **Clé API Anthropic** : facturation API Anthropic normale
    - **Claude CLI / authentification d'abonnement Claude dans OpenClaw** : le personnel d'Anthropic nous a dit que cette utilisation est à nouveau autorisée, et OpenClaw traite l'utilisation `claude -p` comme sanctionnée pour cette intégration sauf si Anthropic publie une nouvelle politique

    Pour les hôtes de passerelle de longue durée, les clés API Anthropic restent la configuration la plus prévisible. L'authentification OAuth OpenAI Codex est explicitement supportée pour les outils externes comme OpenClaw.

    OpenClaw supporte également d'autres options de style abonnement hébergées, notamment **Qwen Cloud Coding Plan**, **MiniMax Coding Plan** et **Z.AI / GLM Coding Plan**.

    Docs : [Anthropic](/fr/providers/anthropic), [OpenAI](/fr/providers/openai),
    [Qwen Cloud](/fr/providers/qwen),
    [MiniMax](/fr/providers/minimax), [GLM Models](/fr/providers/glm),
    [Local models](/fr/gateway/local-models), [Models](/fr/concepts/models).

  </Accordion>

  <Accordion title="Puis-je utiliser l'abonnement Claude Max sans clé API ?">
    Oui.

    Le personnel d'Anthropic nous a dit que l'utilisation de Claude CLI de style OpenClaw est à nouveau autorisée, donc OpenClaw traite l'authentification d'abonnement Claude et l'utilisation `claude -p` comme sanctionnées pour cette intégration sauf si Anthropic publie une nouvelle politique. Si vous voulez la configuration côté serveur la plus prévisible, utilisez une clé API Anthropic à la place.

  </Accordion>

  <Accordion title="Supportez-vous l'authentification d'abonnement Claude (Claude Pro ou Max) ?">
    Oui.

    Le personnel d'Anthropic nous a dit que cette utilisation est à nouveau autorisée, donc OpenClaw traite la réutilisation de Claude CLI et l'utilisation `claude -p` comme sanctionnées pour cette intégration sauf si Anthropic publie une nouvelle politique.

    Le jeton de configuration Anthropic est toujours disponible comme chemin de jeton OpenClaw supporté, mais OpenClaw préfère maintenant la réutilisation de Claude CLI et `claude -p` quand disponibles.
    Pour les charges de travail de production ou multi-utilisateurs, l'authentification par clé API Anthropic reste le choix plus sûr et plus prévisible. Si vous voulez d'autres options de style abonnement hébergées dans OpenClaw, voir [OpenAI](/fr/providers/openai), [Qwen / Model Cloud](/fr/providers/qwen), [MiniMax](/fr/providers/minimax) et [GLM Models](/fr/providers/glm).

  </Accordion>

</AccordionGroup>

<a id="why-am-i-seeing-http-429-ratelimiterror-from-anthropic"></a>

<AccordionGroup>
  <Accordion title="Pourquoi je vois HTTP 429 rate_limit_error d'Anthropic ?">
    Cela signifie que votre **quota/limite de débit Anthropic** est épuisé pour la fenêtre actuelle. Si vous utilisez **Claude CLI**, attendez que la fenêtre se réinitialise ou mettez à niveau votre plan. Si vous utilisez une **clé API Anthropic**, vérifiez la console Anthropic pour l'utilisation/la facturation et augmentez les limites si nécessaire.

    Si le message est spécifiquement :
    `Extra usage is required for long context requests`, la demande essaie d'utiliser la bêta de contexte long d'Anthropic (`context1m: true`). Cela ne fonctionne que quand votre identifiant est éligible pour la facturation de contexte long (facturation par clé API ou le chemin de connexion Claude d'OpenClaw avec Extra Usage activé).

    Conseil : définissez un **modèle de secours** pour qu'OpenClaw puisse continuer à répondre pendant qu'un fournisseur est limité en débit.
    Voir [Models](/fr/cli/models), [OAuth](/fr/concepts/oauth) et
    [/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context](/fr/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context).

  </Accordion>

  <Accordion title="AWS Bedrock est-il supporté ?">
    Oui. OpenClaw a un fournisseur **Amazon Bedrock (Converse)** groupé. Avec les marqueurs d'environnement AWS présents, OpenClaw peut découvrir automatiquement le catalogue Bedrock de streaming/texte et le fusionner en tant que fournisseur implicite `amazon-bedrock` ; sinon vous pouvez explicitement activer `plugins.entries.amazon-bedrock.config.discovery.enabled` ou ajouter une entrée de fournisseur manuelle. Voir [Amazon Bedrock](/fr/providers/bedrock) et [Model providers](/fr/providers/models). Si vous préférez un flux de clé géré, un proxy compatible OpenAI devant Bedrock est toujours une option valide.
  </Accordion>

  <Accordion title="Comment fonctionne l'authentification Codex ?">
    OpenClaw supporte **OpenAI Code (Codex)** via OAuth (connexion ChatGPT). Utilisez `openai-codex/gpt-5.5` pour Codex OAuth via le runner PI par défaut. Utilisez `openai/gpt-5.4` pour l'accès direct à l'API OpenAI actuelle. L'accès direct à l'API OpenAI pour GPT-5.5 est supporté une fois qu'OpenAI l'active sur l'API publique ; aujourd'hui GPT-5.5 utilise l'abonnement/OAuth via `openai-codex/gpt-5.5` ou les exécutions natives du serveur d'applications Codex avec `openai/gpt-5.5` et `embeddedHarness.runtime: "codex"`.
    Voir [Model providers](/fr/concepts/model-providers) et [Onboarding (CLI)](/fr/start/wizard).
  </Accordion>

  <Accordion title="Pourquoi OpenClaw mentionne-t-il toujours openai-codex ?">
    `openai-codex` est l'ID du fournisseur et du profil d'authentification pour OAuth ChatGPT/Codex.
    C'est aussi le préfixe de modèle PI explicite pour Codex OAuth :

    - `openai/gpt-5.4` = route API directe OpenAI actuelle dans PI
    - `openai/gpt-5.5` = route API directe future une fois qu'OpenAI active GPT-5.5 sur l'API
    - `openai-codex/gpt-5.5` = route OAuth Codex dans PI
    - `openai/gpt-5.5` + `embeddedHarness.runtime: "codex"` = route serveur d'applications Codex natif
    - `openai-codex:...` = ID du profil d'authentification, pas une référence de modèle

    Si vous voulez la route de facturation/limite de plateforme OpenAI directe, définissez `OPENAI_API_KEY`. Si vous voulez l'authentification d'abonnement ChatGPT/Codex, connectez-vous avec `openclaw models auth login --provider openai-codex` et utilisez les références de modèle `openai-codex/*` pour les exécutions PI.

  </Accordion>

  <Accordion title="Pourquoi les limites Codex OAuth peuvent-elles différer de ChatGPT web ?">
    Codex OAuth utilise des fenêtres de quota gérées par OpenAI, dépendantes du plan. En pratique, ces limites peuvent différer de l'expérience du site web/application ChatGPT, même quand les deux sont liés au même compte.

    OpenClaw peut afficher les fenêtres d'utilisation/quota du fournisseur actuellement visibles dans `openclaw models status`, mais il n'invente pas ou ne normalise pas les droits web ChatGPT en accès API direct. Si vous voulez la route de facturation/limite de plateforme OpenAI directe, utilisez `openai/*` avec une clé API.

  </Accordion>

  <Accordion title="Supportez-vous l'authentification d'abonnement OpenAI (Codex OAuth) ?">
    Oui. OpenClaw supporte entièrement **OpenAI Code (Codex) OAuth d'abonnement**.
    OpenAI autorise explicitement l'utilisation d'OAuth d'abonnement dans les outils/flux de travail externes comme OpenClaw. L'intégration peut exécuter le flux OAuth pour vous.

    Voir [OAuth](/fr/concepts/oauth), [Model providers](/fr/concepts/model-providers) et [Onboarding (CLI)](/fr/start/wizard).

  </Accordion>

  <Accordion title="Comment configurer Gemini CLI OAuth ?">
    Gemini CLI utilise un **flux d'authentification de plugin**, pas un ID client ou un secret dans `openclaw.json`.

    Étapes :

    1. Installez Gemini CLI localement pour que `gemini` soit sur `PATH`
       - Homebrew : `brew install gemini-cli`
       - npm : `npm install -g @google/gemini-cli`
    2. Activez le plugin : `openclaw plugins enable google`
    3. Connectez-vous : `openclaw models auth login --provider google-gemini-cli --set-default`
    4. Modèle par défaut après la connexion : `google-gemini-cli/gemini-3-flash-preview`
    5. Si les demandes échouent, définissez `GOOGLE_CLOUD_PROJECT` ou `GOOGLE_CLOUD_PROJECT_ID` sur l'hôte de la passerelle

    Cela stocke les jetons OAuth dans les profils d'authentification sur l'hôte de la passerelle. Détails : [Model providers](/fr/concepts/model-providers).

  </Accordion>

  <Accordion title="Un modèle local est-il correct pour les chats occasionnels ?">
    Généralement non. OpenClaw a besoin d'un grand contexte + une sécurité forte ; les petites cartes se tronquent et fuient. Si vous devez, exécutez la **plus grande** version de modèle que vous pouvez localement (LM Studio) et voir [/gateway/local-models](/fr/gateway/local-models). Les modèles plus petits/quantifiés augmentent le risque d'injection de prompt - voir [Security](/fr/gateway/security).
  </Accordion>

  <Accordion title="Comment garder le trafic du modèle hébergé dans une région spécifique ?">
    Choisissez des points de terminaison épinglés à la région. OpenRouter expose des options hébergées aux États-Unis pour MiniMax, Kimi et GLM ; choisissez la variante hébergée aux États-Unis pour garder les données dans la région. Vous pouvez toujours lister Anthropic/OpenAI à côté de ceux-ci en utilisant `models.mode: "merge"` pour que les secours restent disponibles tout en respectant le fournisseur régionné que vous sélectionnez.
  </Accordion>

  <Accordion title="Dois-je acheter un Mac Mini pour installer ceci ?">
    Non. OpenClaw s'exécute sur macOS ou Linux (Windows via WSL2). Un Mac mini est optionnel - certaines personnes en achètent un comme hôte toujours actif, mais un petit VPS, un serveur domestique ou une boîte de classe Raspberry Pi fonctionne aussi.

    Vous n'avez besoin d'un Mac **que pour les outils macOS uniquement**. Pour iMessage, utilisez [BlueBubbles](/fr/channels/bluebubbles) (recommandé) - le serveur BlueBubbles s'exécute sur n'importe quel Mac, et la passerelle peut s'exécuter sur Linux ou ailleurs. Si vous voulez d'autres outils macOS uniquement, exécutez la passerelle sur un Mac ou associez un nœud macOS.

    Docs : [BlueBubbles](/fr/channels/bluebubbles), [Nodes](/fr/nodes), [Mac remote mode](/fr/platforms/mac/remote).

  </Accordion>

  <Accordion title="Ai-je besoin d'un Mac mini pour le support iMessage ?">
    Vous avez besoin d'**un appareil macOS** connecté à Messages. Ce n'est **pas** obligatoirement un Mac mini - n'importe quel Mac fonctionne. **Utilisez [BlueBubbles](/fr/channels/bluebubbles)** (recommandé) pour iMessage - le serveur BlueBubbles s'exécute sur macOS, tandis que la passerelle peut s'exécuter sur Linux ou ailleurs.

    Configurations courantes :

    - Exécutez la passerelle sur Linux/VPS et exécutez le serveur BlueBubbles sur n'importe quel Mac connecté à Messages.
    - Exécutez tout sur le Mac si vous voulez la configuration la plus simple sur une seule machine.

    Docs : [BlueBubbles](/fr/channels/bluebubbles), [Nodes](/fr/nodes),
    [Mac remote mode](/fr/platforms/mac/remote).

  </Accordion>

  <Accordion title="Si j'achète un Mac mini pour exécuter OpenClaw, puis-je le connecter à mon MacBook Pro ?">
    Oui. Le **Mac mini peut exécuter la passerelle**, et votre MacBook Pro peut se connecter en tant que **nœud** (appareil compagnon). Les nœuds n'exécutent pas la passerelle - ils fournissent des capacités supplémentaires comme l'écran/caméra/canevas et `system.run` sur cet appareil.

    Modèle courant :

    - Passerelle sur le Mac mini (toujours actif).
    - MacBook Pro exécute l'application macOS ou un hôte de nœud et s'associe à la passerelle.
    - Utilisez `openclaw nodes status` / `openclaw nodes list` pour le voir.

    Docs : [Nodes](/fr/nodes), [Nodes CLI](/fr/cli/nodes).

  </Accordion>

  <Accordion title="Puis-je utiliser Bun ?">
    Bun n'est **pas recommandé**. Nous voyons des bugs d'exécution, en particulier avec WhatsApp et Telegram.
    Utilisez **Node** pour les passerelles stables.

    Si vous voulez toujours expérimenter avec Bun, faites-le sur une passerelle non-production sans WhatsApp/Telegram.

  </Accordion>

  <Accordion title="Telegram : qu'est-ce qui va dans allowFrom ?">
    `channels.telegram.allowFrom` est **l'ID utilisateur Telegram numérique de l'expéditeur humain**. Ce n'est pas le nom d'utilisateur du bot.

    La configuration demande uniquement les ID utilisateurs numériques. Si vous avez déjà des entrées `@username` héritées dans la configuration, `openclaw doctor --fix` peut essayer de les résoudre.

    Plus sûr (pas de bot tiers) :

    - Envoyez un DM à votre bot, puis exécutez `openclaw logs --follow` et lisez `from.id`.

    API Bot officielle :

    - Envoyez un DM à votre bot, puis appelez `https://api.telegram.org/bot<bot_token>/getUpdates` et lisez `message.from.id`.

    Tiers (moins privé) :

    - Envoyez un DM à `@userinfobot` ou `@getidsbot`.

    Voir [/channels/telegram](/fr/channels/telegram#access-control-and-activation).

  </Accordion>

  <Accordion title="Plusieurs personnes peuvent-elles utiliser un numéro WhatsApp avec différentes instances OpenClaw ?">
    Oui, via **routage multi-agent**. Liez chaque DM de l'expéditeur WhatsApp (pair `kind: "direct"`, expéditeur E.164 comme `+15551234567`) à un `agentId` différent, pour que chaque personne obtienne son propre espace de travail et magasin de sessions. Les réponses viennent toujours du **même compte WhatsApp**, et le contrôle d'accès DM (`channels.whatsapp.dmPolicy` / `channels.whatsapp.allowFrom`) est global par compte WhatsApp. Voir [Multi-Agent Routing](/fr/concepts/multi-agent) et [WhatsApp](/fr/channels/whatsapp).
  </Accordion>

  <Accordion title='Puis-je exécuter un agent « chat rapide » et un agent « Opus pour le codage » ?'>
    Oui. Utilisez le routage multi-agent : donnez à chaque agent son modèle par défaut, puis liez les routes entrantes (compte fournisseur ou pairs spécifiques) à chaque agent. Un exemple de configuration se trouve dans [Multi-Agent Routing](/fr/concepts/multi-agent). Voir aussi [Models](/fr/concepts/models) et [Configuration](/fr/gateway/configuration).
  </Accordion>

  <Accordion title="Homebrew fonctionne-t-il sur Linux ?">
    Oui. Homebrew supporte Linux (Linuxbrew). Configuration rapide :

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    brew install <formula>
    ```

    Si vous exécutez OpenClaw via systemd, assurez-vous que le PATH du service inclut `/home/linuxbrew/.linuxbrew/bin` (ou votre préfixe brew) pour que les outils installés par brew se résolvent dans les shells sans connexion.
    Les versions récentes prépendent également les répertoires bin utilisateur courants sur les services systemd Linux (par exemple `~/.local/bin`, `~/.npm-global/bin`, `~/.local/share/pnpm`, `~/.bun/bin`) et honorent `PNPM_HOME`, `NPM_CONFIG_PREFIX`, `BUN_INSTALL`, `VOLTA_HOME`, `ASDF_DATA_DIR`, `NVM_DIR` et `FNM_DIR` quand définis.

  </Accordion>

  <Accordion title="Différence entre l'installation git modifiable et l'installation npm">
    - **Installation git modifiable :** dépôt source complet, modifiable, meilleur pour les contributeurs.
      Vous exécutez les builds localement et pouvez corriger le code/la documentation.
    - **Installation npm :** installation CLI globale, pas de dépôt, meilleur pour « juste l'exécuter ».
      Les mises à jour viennent des balises de distribution npm.

    Docs : [Getting started](/fr/start/getting-started), [Updating](/fr/install/updating).

  </Accordion>

  <Accordion title="Puis-je basculer entre les installations npm et git plus tard ?">
    Oui. Installez l'autre saveur, puis exécutez Doctor pour que le service de passerelle pointe vers le nouveau point d'entrée.
    Cela **ne supprime pas vos données** - cela change uniquement l'installation du code OpenClaw. Votre état (`~/.openclaw`) et espace de travail (`~/.openclaw/workspace`) restent intacts.

    De npm à git :

    ```bash
    git clone https://github.com/openclaw/openclaw.git
    cd openclaw
    pnpm install
    pnpm build
    openclaw doctor
    openclaw gateway restart
    ```

    De git à npm :

    ```bash
    npm install -g openclaw@latest
    openclaw doctor
    openclaw gateway restart
    ```

    Doctor détecte une incompatibilité de point d'entrée du service de passerelle et propose de réécrire la configuration du service pour correspondre à l'installation actuelle (utilisez `--repair` en automatisation).

    Conseils de sauvegarde : voir [Backup strategy](#where-things-live-on-disk).

  </Accordion>

  <Accordion title="Dois-je exécuter la passerelle sur mon ordinateur portable ou un VPS ?">
    Réponse courte : **si vous voulez une fiabilité 24/7, utilisez un VPS**. Si vous voulez la friction la plus basse et que vous êtes d'accord avec le sommeil/les redémarrages, exécutez-la localement.

    **Ordinateur portable (passerelle locale)**

    - **Avantages :** pas de coût serveur, accès direct aux fichiers locaux, fenêtre de navigateur en direct.
    - **Inconvénients :** sommeil/chutes réseau = déconnexions, les mises à jour du système d'exploitation/redémarrages interrompent, doit rester actif.

    **VPS / cloud**

    - **Avantages :** toujours actif, réseau stable, pas de problèmes de sommeil d'ordinateur portable, plus facile à garder en cours d'exécution.
    - **Inconvénients :** souvent exécuté sans tête (utiliser des captures d'écran), accès aux fichiers distants uniquement, vous devez SSH pour les mises à jour.

    **Note spécifique à OpenClaw :** WhatsApp/Telegram/Slack/Mattermost/Discord fonctionnent tous bien à partir d'un VPS. Le vrai compromis est **navigateur sans tête** vs une fenêtre visible. Voir [Browser](/fr/tools/browser).

    **Par défaut recommandé :** VPS si vous aviez des déconnexions de passerelle avant. Local est excellent quand vous utilisez activement le Mac et voulez l'accès aux fichiers locaux ou l'automatisation de l'interface utilisateur avec un navigateur visible.

  </Accordion>

  <Accordion title="Quelle est l'importance d'exécuter OpenClaw sur une machine dédiée ?">
    Non requis, mais **recommandé pour la fiabilité et l'isolation**.

    - **Hôte dédié (VPS/Mac mini/Pi) :** toujours actif, moins d'interruptions de sommeil/redémarrage, permissions plus propres, plus facile à garder en cours d'exécution.
    - **Ordinateur portable/bureau partagé :** totalement correct pour les tests et l'utilisation active, mais attendez-vous à des pauses quand la machine dort ou se met à jour.

    Si vous voulez le meilleur des deux mondes, gardez la passerelle sur un hôte dédié et associez votre ordinateur portable en tant que **nœud** pour les outils d'écran/caméra/exec locaux. Voir [Nodes](/fr/nodes).
    Pour les conseils de sécurité, lisez [Security](/fr/gateway/security).

  </Accordion>

  <Accordion title="Quelles sont les exigences VPS minimales et le système d'exploitation recommandé ?">
    OpenClaw est léger. Pour une passerelle de base + un canal de chat :

    - **Minimum absolu :** 1 vCPU, 1 Go de RAM, ~500 Mo de disque.
    - **Recommandé :** 1-2 vCPU, 2 Go de RAM ou plus pour la marge (journaux, médias, plusieurs canaux). Les outils de nœud et l'automatisation du navigateur peuvent être gourmands en ressources.

    Système d'exploitation : utilisez **Ubuntu LTS** (ou n'importe quel Debian/Ubuntu moderne). Le chemin d'installation Linux y est le mieux testé.

    Docs : [Linux](/fr/platforms/linux), [VPS hosting](/fr/vps).

  </Accordion>

  <Accordion title="Puis-je exécuter OpenClaw dans une VM et quelles sont les exigences ?">
    Oui. Traitez une VM de la même manière qu'un VPS : elle doit être toujours actif, accessible et avoir suffisamment de RAM pour la passerelle et tous les canaux que vous activez.

    Conseils de base :

    - **Minimum absolu :** 1 vCPU, 1 Go de RAM.
    - **Recommandé :** 2 Go de RAM ou plus si vous exécutez plusieurs canaux, l'automatisation du navigateur ou les outils multimédias.
    - **Système d'exploitation :** Ubuntu LTS ou un autre Debian/Ubuntu moderne.

    Si vous êtes sous Windows, **WSL2 est la configuration de style VM la plus facile** et a la meilleure compatibilité des outils.
    Voir [Windows](/fr/platforms/windows), [VPS hosting](/fr/vps).
    Si vous exécutez macOS dans une VM, voir [macOS VM](/fr/install/macos-vm).

  </Accordion>
</AccordionGroup>

## Liens connexes

- [FAQ](/fr/help/faq) — la FAQ principale (modèles, sessions, passerelle, sécurité, et plus)
- [Aperçu de l'installation](/fr/install)
- [Prise en main](/fr/start/getting-started)
- [Dépannage](/fr/help/troubleshooting)
