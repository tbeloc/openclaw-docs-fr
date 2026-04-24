---
summary: "FAQ: modèles par défaut, sélection, alias, commutation, basculement et profils d'authentification"
read_when:
  - Choisir ou changer de modèle, configurer des alias
  - Déboguer le basculement de modèle / "Tous les modèles ont échoué"
  - Comprendre les profils d'authentification et comment les gérer
title: "FAQ: modèles et authentification"
sidebarTitle: "FAQ Modèles"
---

Q&A sur les modèles et les profils d'authentification. Pour la configuration, les sessions, la passerelle, les canaux et le dépannage, consultez la [FAQ](/fr/help/faq) principale.

## Modèles : valeurs par défaut, sélection, alias, commutation

<AccordionGroup>
  <Accordion title='Qu\'est-ce que le « modèle par défaut » ?'>
    Le modèle par défaut d'OpenClaw est celui que vous définissez comme :

    ```
    agents.defaults.model.primary
    ```

    Les modèles sont référencés comme `provider/model` (exemple : `openai/gpt-5.4` ou `openai-codex/gpt-5.5`). Si vous omettez le fournisseur, OpenClaw essaie d'abord un alias, puis une correspondance de fournisseur configuré unique pour cet ID de modèle exact, et ne revient au fournisseur par défaut configuré que comme chemin de compatibilité déprécié. Si ce fournisseur n'expose plus le modèle par défaut configuré, OpenClaw revient au premier fournisseur/modèle configuré au lieu de présenter un défaut de fournisseur supprimé obsolète. Vous devriez toujours **explicitement** définir `provider/model`.

  </Accordion>

  <Accordion title="Quel modèle recommandez-vous ?">
    **Défaut recommandé :** utilisez le modèle de dernière génération le plus puissant disponible dans votre pile de fournisseurs.
    **Pour les agents avec outils activés ou entrées non fiables :** privilégiez la puissance du modèle par rapport au coût.
    **Pour le chat routinier/faible enjeu :** utilisez des modèles de secours moins chers et routez par rôle d'agent.

    MiniMax a sa propre documentation : [MiniMax](/fr/providers/minimax) et
    [Modèles locaux](/fr/gateway/local-models).

    Règle générale : utilisez le **meilleur modèle que vous pouvez vous permettre** pour les travaux à enjeux élevés, et un modèle moins cher pour le chat routinier ou les résumés. Vous pouvez router les modèles par agent et utiliser des sous-agents pour paralléliser les tâches longues (chaque sous-agent consomme des jetons). Voir [Modèles](/fr/concepts/models) et
    [Sous-agents](/fr/tools/subagents).

    Avertissement important : les modèles plus faibles/sur-quantifiés sont plus vulnérables à l'injection de prompts et aux comportements non sécurisés. Voir [Sécurité](/fr/gateway/security).

    Plus de contexte : [Modèles](/fr/concepts/models).

  </Accordion>

  <Accordion title="Comment puis-je changer de modèle sans effacer ma configuration ?">
    Utilisez les **commandes de modèle** ou modifiez uniquement les champs **model**. Évitez les remplacements de configuration complets.

    Options sûres :

    - `/model` en chat (rapide, par session)
    - `openclaw models set ...` (met à jour uniquement la configuration du modèle)
    - `openclaw configure --section model` (interactif)
    - modifiez `agents.defaults.model` dans `~/.openclaw/openclaw.json`

    Évitez `config.apply` avec un objet partiel sauf si vous avez l'intention de remplacer toute la configuration.
    Pour les modifications RPC, inspectez d'abord avec `config.schema.lookup` et préférez `config.patch`. La charge utile de recherche vous donne le chemin normalisé, la documentation/contraintes du schéma superficiel, et les résumés des enfants immédiats.
    pour les mises à jour partielles.
    Si vous avez écrasé la configuration, restaurez à partir d'une sauvegarde ou réexécutez `openclaw doctor` pour réparer.

    Documentation : [Modèles](/fr/concepts/models), [Configurer](/fr/cli/configure), [Config](/fr/cli/config), [Doctor](/fr/gateway/doctor).

  </Accordion>

  <Accordion title="Puis-je utiliser des modèles auto-hébergés (llama.cpp, vLLM, Ollama) ?">
    Oui. Ollama est le chemin le plus facile pour les modèles locaux.

    Configuration la plus rapide :

    1. Installez Ollama depuis `https://ollama.com/download`
    2. Tirez un modèle local tel que `ollama pull gemma4`
    3. Si vous voulez aussi des modèles cloud, exécutez `ollama signin`
    4. Exécutez `openclaw onboard` et choisissez `Ollama`
    5. Choisissez `Local` ou `Cloud + Local`

    Notes :

    - `Cloud + Local` vous donne les modèles cloud plus vos modèles Ollama locaux
    - les modèles cloud tels que `kimi-k2.5:cloud` n'ont pas besoin d'un tirage local
    - pour la commutation manuelle, utilisez `openclaw models list` et `openclaw models set ollama/<model>`

    Note de sécurité : les modèles plus petits ou fortement quantifiés sont plus vulnérables à l'injection de prompts. Nous recommandons fortement les **grands modèles** pour tout bot qui peut utiliser des outils.
    Si vous voulez toujours des petits modèles, activez le sandboxing et les listes d'outils strictes.

    Documentation : [Ollama](/fr/providers/ollama), [Modèles locaux](/fr/gateway/local-models),
    [Fournisseurs de modèles](/fr/concepts/model-providers), [Sécurité](/fr/gateway/security),
    [Sandboxing](/fr/gateway/sandboxing).

  </Accordion>

  <Accordion title="Qu'est-ce qu'OpenClaw, Flawd et Krill utilisent pour les modèles ?">
    - Ces déploiements peuvent différer et peuvent changer au fil du temps ; il n'y a pas de recommandation de fournisseur fixe.
    - Vérifiez le paramètre d'exécution actuel sur chaque passerelle avec `openclaw models status`.
    - Pour les agents sensibles à la sécurité/avec outils activés, utilisez le modèle de dernière génération le plus puissant disponible.
  </Accordion>

  <Accordion title="Comment puis-je changer de modèle à la volée (sans redémarrer) ?">
    Utilisez la commande `/model` comme message autonome :

    ```
    /model sonnet
    /model opus
    /model gpt
    /model gpt-mini
    /model gemini
    /model gemini-flash
    /model gemini-flash-lite
    ```

    Ce sont les alias intégrés. Les alias personnalisés peuvent être ajoutés via `agents.defaults.models`.

    Vous pouvez lister les modèles disponibles avec `/model`, `/model list`, ou `/model status`.

    `/model` (et `/model list`) affiche un sélecteur compact numéroté. Sélectionnez par numéro :

    ```
    /model 3
    ```

    Vous pouvez également forcer un profil d'authentification spécifique pour le fournisseur (par session) :

    ```
    /model opus@anthropic:default
    /model opus@anthropic:work
    ```

    Conseil : `/model status` affiche quel agent est actif, quel fichier `auth-profiles.json` est utilisé, et quel profil d'authentification sera essayé ensuite.
    Il affiche également le point de terminaison du fournisseur configuré (`baseUrl`) et le mode API (`api`) le cas échéant.

    **Comment puis-je désépingler un profil que j'ai défini avec @profile ?**

    Réexécutez `/model` **sans** le suffixe `@profile` :

    ```
    /model anthropic/claude-opus-4-6
    ```

    Si vous voulez revenir à la valeur par défaut, choisissez-la dans `/model` (ou envoyez `/model <default provider/model>`).
    Utilisez `/model status` pour confirmer quel profil d'authentification est actif.

  </Accordion>

  <Accordion title="Puis-je utiliser GPT 5.5 pour les tâches quotidiennes et Codex 5.5 pour le codage ?">
    Oui. Définissez l'un comme défaut et changez selon les besoins :

    - **Commutation rapide (par session) :** `/model openai/gpt-5.4` pour les tâches actuelles d'API OpenAI directe ou `/model openai-codex/gpt-5.5` pour les tâches OAuth GPT-5.5 Codex.
    - **Défaut :** définissez `agents.defaults.model.primary` sur `openai/gpt-5.4` pour l'utilisation de clé API ou `openai-codex/gpt-5.5` pour l'utilisation OAuth GPT-5.5 Codex.
    - **Sous-agents :** routez les tâches de codage vers des sous-agents avec un modèle par défaut différent.

    L'accès direct par clé API pour `openai/gpt-5.5` est supporté une fois qu'OpenAI active
    GPT-5.5 sur l'API publique. Jusqu'à présent, GPT-5.5 est abonnement/OAuth uniquement.

    Voir [Modèles](/fr/concepts/models) et [Commandes slash](/fr/tools/slash-commands).

  </Accordion>

  <Accordion title="Comment configurer le mode rapide pour GPT 5.5 ?">
    Utilisez soit un basculement de session, soit une configuration par défaut :

    - **Par session :** envoyez `/fast on` tandis que la session utilise `openai/gpt-5.4` ou `openai-codex/gpt-5.5`.
    - **Par défaut du modèle :** définissez `agents.defaults.models["openai/gpt-5.4"].params.fastMode` ou `agents.defaults.models["openai-codex/gpt-5.5"].params.fastMode` sur `true`.

    Exemple :

    ```json5
    {
      agents: {
        defaults: {
          models: {
            "openai/gpt-5.4": {
              params: {
                fastMode: true,
              },
            },
          },
        },
      },
    }
    ```

    Pour OpenAI, le mode rapide correspond à `service_tier = "priority"` sur les demandes de réponses natives supportées. Les remplacements de session `/fast` battent les défauts de configuration.

    Voir [Réflexion et mode rapide](/fr/tools/thinking) et [Mode rapide OpenAI](/fr/providers/openai#fast-mode).

  </Accordion>

  <Accordion title='Pourquoi je vois « Model ... is not allowed » et puis pas de réponse ?'>
    Si `agents.defaults.models` est défini, il devient la **liste d'autorisation** pour `/model` et tout remplacement de session. Choisir un modèle qui n'est pas dans cette liste retourne :

    ```
    Model "provider/model" is not allowed. Use /model to list available models.
    ```

    Cette erreur est retournée **à la place** d'une réponse normale. Correction : ajoutez le modèle à
    `agents.defaults.models`, supprimez la liste d'autorisation, ou choisissez un modèle dans `/model list`.

  </Accordion>

  <Accordion title='Pourquoi je vois « Unknown model: minimax/MiniMax-M2.7 » ?'>
    Cela signifie que le **fournisseur n'est pas configuré** (aucune configuration de fournisseur MiniMax ou profil d'authentification n'a été trouvé), donc le modèle ne peut pas être résolu.

    Liste de contrôle de correction :

    1. Mettez à niveau vers une version actuelle d'OpenClaw (ou exécutez depuis la source `main`), puis redémarrez la passerelle.
    2. Assurez-vous que MiniMax est configuré (assistant ou JSON), ou que l'authentification MiniMax
       existe dans les profils env/auth afin que le fournisseur correspondant puisse être injecté
       (`MINIMAX_API_KEY` pour `minimax`, `MINIMAX_OAUTH_TOKEN` ou OAuth MiniMax stocké
       pour `minimax-portal`).
    3. Utilisez l'ID de modèle exact (sensible à la casse) pour votre chemin d'authentification :
       `minimax/MiniMax-M2.7` ou `minimax/MiniMax-M2.7-highspeed` pour la configuration de clé API,
       ou `minimax-portal/MiniMax-M2.7` /
       `minimax-portal/MiniMax-M2.7-highspeed` pour la configuration OAuth.
    4. Exécutez :

       ```bash
       openclaw models list
       ```

       et choisissez dans la liste (ou `/model list` en chat).

    Voir [MiniMax](/fr/providers/minimax) et [Modèles](/fr/concepts/models).

  </Accordion>

  <Accordion title="Puis-je utiliser MiniMax comme défaut et OpenAI pour les tâches complexes ?">
    Oui. Utilisez **MiniMax comme défaut** et changez de modèles **par session** selon les besoins.
    Les secours sont pour les **erreurs**, pas les « tâches difficiles », donc utilisez `/model` ou un agent séparé.

    **Option A : changer par session**

    ```json5
    {
      env: { MINIMAX_API_KEY: "sk-...", OPENAI_API_KEY: "sk-..." },
      agents: {
        defaults: {
          model: { primary: "minimax/MiniMax-M2.7" },
          models: {
            "minimax/MiniMax-M2.7": { alias: "minimax" },
            "openai/gpt-5.4": { alias: "gpt" },
          },
        },
      },
    }
    ```

    Puis :

    ```
    /model gpt
    ```

    **Option B : agents séparés**

    - Agent A défaut : MiniMax
    - Agent B défaut : OpenAI
    - Routez par agent ou utilisez `/agent` pour changer

    Documentation : [Modèles](/fr/concepts/models), [Routage multi-agent](/fr/concepts/multi-agent), [MiniMax](/fr/providers/minimax), [OpenAI](/fr/providers/openai).

  </Accordion>

  <Accordion title="Les opus / sonnet / gpt sont-ils des raccourcis intégrés ?">
    Oui. OpenClaw expédie quelques raccourcis par défaut (appliqués uniquement lorsque le modèle existe dans `agents.defaults.models`) :

    - `opus` → `anthropic/claude-opus-4-6`
    - `sonnet` → `anthropic/claude-sonnet-4-6`
    - `gpt` → `openai/gpt-5.4` pour les configurations de clé API, ou `openai-codex/gpt-5.5` lorsque configuré pour OAuth Codex
    - `gpt-mini` → `openai/gpt-5.4-mini`
    - `gpt-nano` → `openai/gpt-5.4-nano`
    - `gemini` → `google/gemini-3.1-pro-preview`
    - `gemini-flash` → `google/gemini-3-flash-preview`
    - `gemini-flash-lite` → `google/gemini-3.1-flash-lite-preview`

    Si vous définissez votre propre alias avec le même nom, votre valeur gagne.

  </Accordion>

  <Accordion title="Comment définir/remplacer les raccourcis de modèle (alias) ?">
    Les alias proviennent de `agents.defaults.models.<modelId>.alias`. Exemple :

    ```json5
    {
      agents: {
        defaults: {
          model: { primary: "anthropic/claude-opus-4-6" },
          models: {
            "anthropic/claude-opus-4-6": { alias: "opus" },
            "anthropic/claude-sonnet-4-6": { alias: "sonnet" },
            "anthropic/claude-haiku-4-5": { alias: "haiku" },
          },
        },
      },
    }
    ```

    Puis `/model sonnet` (ou `/<alias>` lorsque supporté) se résout à cet ID de modèle.

  </Accordion>

  <Accordion title="Comment ajouter des modèles d'autres fournisseurs comme OpenRouter ou Z.AI ?">
    OpenRouter (paiement à la demande ; nombreux modèles) :

    ```json5
    {
      agents: {
        defaults: {
          model: { primary: "openrouter/anthropic/claude-sonnet-4-6" },
          models: { "openrouter/anthropic/claude-sonnet-4-6": {} },
        },
      },
      env: { OPENROUTER_API_KEY: "sk-or-..." },
    }
    ```

    Z.AI (modèles GLM) :

    ```json5
    {
      agents: {
        defaults: {
          model: { primary: "zai/glm-5" },
          models: { "zai/glm-5": {} },
        },
      },
      env: { ZAI_API_KEY: "..." },
    }
    ```

    Si vous référencez un fournisseur/modèle mais que la clé de fournisseur requise est manquante, vous obtiendrez une erreur d'authentification d'exécution (par exemple `No API key found for provider "zai"`).

    **Aucune clé API trouvée pour le fournisseur après l'ajout d'un nouvel agent**

    Cela signifie généralement que le **nouvel agent** a un magasin d'authentification vide. L'authentification est par agent et
    stockée dans :

    ```
    ~/.openclaw/agents/<agentId>/agent/auth-profiles.json
    ```

    Options de correction :

    - Exécutez `openclaw agents add <id>` et configurez l'authentification pendant l'assistant.
    - Ou copiez `auth-profiles.json` depuis le `agentDir` de l'agent principal dans le `agentDir` du nouvel agent.

    Ne **réutilisez pas** `agentDir` entre les agents ; cela cause des collisions d'authentification/session.

  </Accordion>
</AccordionGroup>

## Basculement de modèle et "Tous les modèles ont échoué"

<AccordionGroup>
  <Accordion title="Comment fonctionne le basculement ?">
    Le basculement se fait en deux étapes :

    1. **Rotation du profil d'authentification** au sein du même fournisseur.
    2. **Secours du modèle** vers le modèle suivant dans `agents.defaults.model.fallbacks`.

    Les délais d'attente s'appliquent aux profils défaillants (backoff exponentiel), de sorte qu'OpenClaw peut continuer à répondre même lorsqu'un fournisseur est limité en débit ou défaillant temporairement.

    Le compartiment de limite de débit inclut plus que les simples réponses `429`. OpenClaw traite également les messages comme `Too many concurrent requests`,
    `ThrottlingException`, `concurrency limit reached`,
    `workers_ai ... quota limit exceeded`, `resource exhausted`, et les limites périodiques de fenêtre d'utilisation (`weekly/monthly limit reached`) comme des limites de débit justifiant un basculement.

    Certaines réponses ressemblant à la facturation ne sont pas `402`, et certaines réponses HTTP `402` restent également dans ce compartiment transitoire. Si un fournisseur retourne un texte de facturation explicite sur `401` ou `403`, OpenClaw peut toujours le garder dans la voie de facturation, mais les appariements de texte spécifiques au fournisseur restent limités au fournisseur qui les possède (par exemple, OpenRouter `Key limit exceeded`). Si un message `402` ressemble plutôt à une fenêtre d'utilisation renouvelable ou à une limite de dépenses d'organisation/espace de travail (`daily limit reached, resets tomorrow`,
    `organization spending limit exceeded`), OpenClaw le traite comme `rate_limit`, et non comme une désactivation de facturation longue.

    Les erreurs de débordement de contexte sont différentes : les signatures telles que
    `request_too_large`, `input exceeds the maximum number of tokens`,
    `input token count exceeds the maximum number of input tokens`,
    `input is too long for the model`, ou `ollama error: context length
    exceeded` restent sur le chemin de compaction/nouvelle tentative au lieu d'avancer le basculement du modèle.

    Le texte d'erreur serveur générique est intentionnellement plus étroit que « tout ce qui contient unknown/error ». OpenClaw traite les formes transitoires limitées au fournisseur telles que Anthropic bare `An unknown error occurred`, OpenRouter bare
    `Provider returned error`, les erreurs de raison d'arrêt comme `Unhandled stop reason:
    error`, les charges utiles JSON `api_error` avec du texte serveur transitoire
    (`internal server error`, `unknown error, 520`, `upstream error`, `backend
    error`), et les erreurs de fournisseur occupé telles que `ModelNotReadyException` comme des signaux de timeout/surcharge justifiant un basculement lorsque le contexte du fournisseur correspond.
    Le texte de secours interne générique comme `LLM request failed with an unknown
    error.` reste conservateur et ne déclenche pas le basculement du modèle par lui-même.

  </Accordion>

  <Accordion title='Que signifie "No credentials found for profile anthropic:default" ?'>
    Cela signifie que le système a tenté d'utiliser l'ID de profil d'authentification `anthropic:default`, mais n'a pas pu trouver les identifiants correspondants dans le magasin d'authentification attendu.

    **Liste de contrôle de correction :**

    - **Confirmez où vivent les profils d'authentification** (chemins nouveaux vs hérités)
      - Actuel : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
      - Hérité : `~/.openclaw/agent/*` (migré par `openclaw doctor`)
    - **Confirmez que votre variable d'environnement est chargée par la passerelle**
      - Si vous définissez `ANTHROPIC_API_KEY` dans votre shell mais exécutez la passerelle via systemd/launchd, elle peut ne pas l'hériter. Mettez-la dans `~/.openclaw/.env` ou activez `env.shellEnv`.
    - **Assurez-vous que vous modifiez le bon agent**
      - Les configurations multi-agents signifient qu'il peut y avoir plusieurs fichiers `auth-profiles.json`.
    - **Vérifiez l'état du modèle/authentification**
      - Utilisez `openclaw models status` pour voir les modèles configurés et si les fournisseurs sont authentifiés.

    **Liste de contrôle de correction pour "No credentials found for profile anthropic"**

    Cela signifie que l'exécution est épinglée à un profil d'authentification Anthropic, mais la passerelle
    ne peut pas le trouver dans son magasin d'authentification.

    - **Utilisez Claude CLI**
      - Exécutez `openclaw models auth login --provider anthropic --method cli --set-default` sur l'hôte de la passerelle.
    - **Si vous préférez utiliser une clé API**
      - Mettez `ANTHROPIC_API_KEY` dans `~/.openclaw/.env` sur l'**hôte de la passerelle**.
      - Effacez tout ordre épinglé qui force un profil manquant :

        ```bash
        openclaw models auth order clear --provider anthropic
        ```

    - **Confirmez que vous exécutez les commandes sur l'hôte de la passerelle**
      - En mode distant, les profils d'authentification vivent sur la machine de la passerelle, pas sur votre ordinateur portable.

  </Accordion>

  <Accordion title="Pourquoi a-t-il aussi essayé Google Gemini et échoué ?">
    Si votre configuration de modèle inclut Google Gemini comme secours (ou si vous avez basculé vers un raccourci Gemini), OpenClaw l'essaiera lors du basculement du modèle. Si vous n'avez pas configuré les identifiants Google, vous verrez `No API key found for provider "google"`.

    Correction : fournissez soit l'authentification Google, soit supprimez/évitez les modèles Google dans `agents.defaults.model.fallbacks` / alias afin que le basculement ne s'y achemine pas.

    **LLM request rejected: thinking signature required (Google Antigravity)**

    Cause : l'historique de session contient **des blocs de réflexion sans signatures** (souvent d'un flux interrompu/partiel). Google Antigravity nécessite des signatures pour les blocs de réflexion.

    Correction : OpenClaw supprime maintenant les blocs de réflexion non signés pour Google Antigravity Claude. S'il apparaît toujours, démarrez une **nouvelle session** ou définissez `/thinking off` pour cet agent.

  </Accordion>
</AccordionGroup>

## Profils d'authentification : ce qu'ils sont et comment les gérer

Connexe : [/concepts/oauth](/fr/concepts/oauth) (flux OAuth, stockage des jetons, modèles multi-comptes)

<AccordionGroup>
  <Accordion title="Qu'est-ce qu'un profil d'authentification ?">
    Un profil d'authentification est un enregistrement d'identifiants nommé (OAuth ou clé API) lié à un fournisseur. Les profils vivent dans :

    ```
    ~/.openclaw/agents/<agentId>/agent/auth-profiles.json
    ```

  </Accordion>

  <Accordion title="Quels sont les ID de profil typiques ?">
    OpenClaw utilise des ID préfixés par le fournisseur comme :

    - `anthropic:default` (courant quand aucune identité e-mail n'existe)
    - `anthropic:<email>` pour les identités OAuth
    - des ID personnalisés que vous choisissez (par exemple `anthropic:work`)

  </Accordion>

  <Accordion title="Puis-je contrôler quel profil d'authentification est essayé en premier ?">
    Oui. La configuration supporte des métadonnées optionnelles pour les profils et un ordre par fournisseur (`auth.order.<provider>`). Cela ne stocke **pas** les secrets ; il mappe les ID au fournisseur/mode et définit l'ordre de rotation.

    OpenClaw peut temporairement ignorer un profil s'il est dans un court **délai d'attente** (limites de débit/timeouts/échecs d'authentification) ou un état **désactivé** plus long (facturation/crédits insuffisants). Pour inspecter cela, exécutez `openclaw models status --json` et vérifiez `auth.unusableProfiles`. Réglage : `auth.cooldowns.billingBackoffHours*`.

    Les délais d'attente de limite de débit peuvent être limités au modèle. Un profil qui refroidit
    pour un modèle peut toujours être utilisable pour un modèle frère sur le même fournisseur,
    tandis que les fenêtres de facturation/désactivation bloquent toujours le profil entier.

    Vous pouvez également définir un **ordre de remplacement par agent** (stocké dans le `auth-state.json` de cet agent) via la CLI :

    ```bash
    # Par défaut l'agent par défaut configuré (omettez --agent)
    openclaw models auth order get --provider anthropic

    # Verrouillez la rotation sur un seul profil (essayez seulement celui-ci)
    openclaw models auth order set --provider anthropic anthropic:default

    # Ou définissez un ordre explicite (secours au sein du fournisseur)
    openclaw models auth order set --provider anthropic anthropic:work anthropic:default

    # Effacez le remplacement (revenez à config auth.order / round-robin)
    openclaw models auth order clear --provider anthropic
    ```

    Pour cibler un agent spécifique :

    ```bash
    openclaw models auth order set --provider anthropic --agent main anthropic:default
    ```

    Pour vérifier ce qui sera réellement essayé, utilisez :

    ```bash
    openclaw models status --probe
    ```

    Si un profil stocké est omis de l'ordre explicite, la sonde rapporte
    `excluded_by_auth_order` pour ce profil au lieu de l'essayer silencieusement.

  </Accordion>

  <Accordion title="OAuth vs clé API - quelle est la différence ?">
    OpenClaw supporte les deux :

    - **OAuth** exploite souvent l'accès par abonnement (le cas échéant).
    - **Les clés API** utilisent la facturation au paiement à l'utilisation.

    L'assistant supporte explicitement Anthropic Claude CLI, OpenAI Codex OAuth, et les clés API.

  </Accordion>
</AccordionGroup>

## Connexe

- [FAQ](/fr/help/faq) — la FAQ principale
- [FAQ — démarrage rapide et configuration de première exécution](/fr/help/faq-first-run)
- [Sélection du modèle](/fr/concepts/model-providers)
- [Basculement du modèle](/fr/concepts/model-failover)
