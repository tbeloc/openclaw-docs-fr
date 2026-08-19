---
summary: "Connectez OpenClaw à un llama-server llama.cpp existant"
read_when:
  - You already run llama-server locally or on a private model host
  - You want automatic model, context, and tool-capability discovery
  - You use llama-server router mode
  - You are choosing between managed and external llama.cpp setup
sidebarTitle: "llama-server"
title: "Fournisseur llama-server"
---

`llama-server` est le serveur HTTP autonome de llama.cpp. Le fournisseur
`llama-server` connecte OpenClaw à un processus que vous exécutez et gérez
déjà. OpenClaw découvre les modèles et les capacités exposés par le serveur et
envoie les demandes de chat via son API compatible OpenAI.

Le même [plugin `llama-cpp`](/fr/plugins/llama-cpp) fournit également le
fournisseur `llama-cpp` géré. Le fournisseur géré installe et exécute un
serveur vérifié. Les nouvelles configurations externes n'installent, ne
démarrent, n'arrêtent, ne téléchargent ou ne reconfigurent jamais rien. Les
configurations existantes avec un bloc `localService` explicite conservent leur
comportement de superviseur précédent pour la compatibilité.

| Propriété        | Valeur                            |
| ---------------- | --------------------------------- |
| ID du fournisseur| `llama-server`                    |
| API              | `openai-completions`              |
| URL de base par défaut | `http://127.0.0.1:8080/v1`        |
| Authentification | `LLAMA_SERVER_API_KEY` optionnel  |
| Découverte de modèles | Points de terminaison de liste de modèles et de propriétés |
| Propriétaire du processus | Utilisateur ou superviseur externe |

## Démarrage rapide

<Steps>
  <Step title="Démarrer llama-server">
    Démarrez un serveur llama.cpp officiel avec un alias de modèle stable :

    ```bash
    llama-server \
      --model /path/to/model.gguf \
      --alias my-model \
      --host 127.0.0.1 \
      --port 8080
    ```

    Choisissez le contexte, le GPU, l'emplacement, le traitement par lots et les
    drapeaux de modèle de chat pour votre déploiement. OpenClaw ne les change
    pas.

  </Step>
  <Step title="Exécuter la configuration OpenClaw">
    ```bash
    openclaw onboard
    ```

    Dans le groupe **Local llama.cpp**, choisissez **Existing llama-server**.
    Acceptez l'URL par défaut ou entrez un autre point de terminaison local ou
    privé. Laissez l'authentification par clé API désactivée sauf si le serveur
    ou son proxy inverse l'exige.

  </Step>
  <Step title="Sélectionner le modèle découvert">
    ```bash
    openclaw models list --provider llama-server
    openclaw models set llama-server/my-model
    ```
  </Step>
</Steps>

Un `--alias` stable maintient la référence du modèle OpenClaw indépendante du
chemin du fichier GGUF.

## Fournisseurs gérés et externes

Installez le plugin `llama-cpp` une fois pour l'un ou l'autre fournisseur :

```bash
openclaw plugins install @openclaw/llama-cpp-provider
```

| Référence du modèle    | Propriétaire du serveur | Comportement de configuration |
| ---------------------- | ----------------------- | ----------------------------- |
| `llama-cpp/<model>`    | OpenClaw                | Installe et gère le runtime   |
| `llama-server/<model>` | Utilisateur             | Se connecte à un point de terminaison existant |

Les deux fournisseurs peuvent être configurés en même temps. Utilisez
`llama-cpp` quand vous voulez qu'OpenClaw gère le processus. Utilisez
`llama-server` quand un autre terminal, conteneur, gestionnaire d'hôte ou
machine possède le processus.

Les configurations `llama-server` manuelles existantes qui utilisent
`localService` continuent de fonctionner. Les nouvelles configurations doivent
utiliser le fournisseur `llama-cpp` géré quand OpenClaw doit posséder le
processus serveur.

## Découverte

La découverte lit ces points de terminaison :

- `/health`
- `/models`, avec `/v1/models` comme secours de compatibilité
- `/props` pour un modèle chargé unique
- `/props?model=<id>&autoload=false` en mode routeur

La découverte ne charge, ne réveille, ne décharge, ne télécharge ou ne recharge
pas un modèle. Les demandes de propriété du routeur définissent `autoload=false`,
et les demandes de liste de modèles ne définissent pas `reload=1`.

Pour chaque modèle, OpenClaw utilise les métadonnées du serveur pour le contexte
actif, la sortie maximale, les types d'entrée, le nombre d'emplacements, les
informations de construction, l'état et les capacités du modèle de chat. Il
active les outils uniquement quand le serveur signale à la fois
`supports_tools` et `supports_tool_calls`.

Les entrées de modèle explicites dans `openclaw.json` ont priorité sur les
lignes découvertes avec le même ID de modèle.

## Authentification

Définissez `LLAMA_SERVER_API_KEY` quand llama-server ou son proxy inverse
nécessite un jeton porteur :

```bash
export LLAMA_SERVER_API_KEY="your-key"
openclaw onboard
```

La configuration guidée peut enregistrer la clé dans un profil d'authentification
OpenClaw. Les clés API du fournisseur, les valeurs SecretRef et les en-têtes
d'autorisation explicites sont également pris en charge. Un en-tête
d'autorisation explicite a priorité sur la résolution de clé porteur.

Ne mettez pas les identifiants dans l'URL du point de terminaison. OpenClaw
rejette les URL qui contiennent un nom d'utilisateur ou un mot de passe.

## Configuration non interactive

Un serveur local non authentifié a besoin de son URL :

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice llama-server \
  --custom-base-url http://127.0.0.1:8080/v1
```

Sélectionnez explicitement un modèle annoncé si nécessaire :

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice llama-server \
  --custom-base-url http://127.0.0.1:8080/v1 \
  --custom-model-id my-model
```

Passez `--llama-server-api-key` ou définissez `LLAMA_SERVER_API_KEY` pour un
point de terminaison authentifié. Quand vous remplacez un point de terminaison
existant, passez `--llama-server-api-key` explicitement. OpenClaw ne réutilise
pas l'environnement, le profil, l'en-tête ou les identifiants configurés du
point de terminaison précédent. La configuration non interactive vérifie le
point de terminaison et le modèle sélectionné avant d'écrire la configuration.

## Configuration manuelle

La configuration guidée est recommandée car elle découvre et vérifie les
métadonnées du modèle. Un fournisseur minimal manuel a cette forme :

```json5
{
  models: {
    mode: "merge",
    providers: {
      "llama-server": {
        baseUrl: "http://127.0.0.1:8080/v1",
        api: "openai-completions",
        request: { allowPrivateNetwork: true },
        models: [],
      },
    },
  },
}
```

L'option de réseau privé est requise pour les points de terminaison de boucle
locale et privés. OpenClaw épingle toujours les demandes à l'origine configurée
et bloque les métadonnées cloud et les redirections non sécurisées.

## Dépannage

### Le serveur n'est pas disponible

Vérifiez les points de terminaison de santé publique et de modèle :

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/models
```

HTTP 503 de `/health` signifie que le modèle est toujours en cours de
chargement. Attendez que le processus externe soit prêt. OpenClaw ne le
redémarre pas.

### Les outils sont désactivés

Inspectez les propriétés du modèle actif :

```bash
curl http://127.0.0.1:8080/props
```

Vérifiez `chat_template_caps.supports_tools` et
`chat_template_caps.supports_tool_calls`. Démarrez llama-server avec Jinja
activé et un modèle capable d'outils. OpenClaw ne devine pas le support des
outils à partir du nom du modèle.

### La découverte du routeur a chargé un modèle

Les demandes de propriété OpenClaw incluent `autoload=false`, et les demandes
de liste de modèles n'incluent pas `reload=1`. Vérifiez les autres clients et
le paramètre `--models-autoload` du serveur si un modèle se charge en dehors
d'une demande d'inférence.

### L'authentification échoue lors de l'inférence

Les points de terminaison de santé et de liste de modèles peuvent rester publics
tandis que l'inférence de chat nécessite une clé. Définissez
`LLAMA_SERVER_API_KEY` sur la valeur attendue par llama-server ou son proxy
inverse, puis réexécutez la configuration ou redémarrez la passerelle pour
qu'elle puisse lire la nouvelle valeur d'environnement.

### La sortie structurée échoue

Utilisez une version officielle actuelle de llama.cpp. OpenClaw mappe les
demandes JSON Schema à la forme de schéma `json_object` de llama-server afin
que la sortie structurée fonctionne également avec les versions de serveur
externe plus anciennes.

## Connexes

- [Plugin llama.cpp](/fr/plugins/llama-cpp)
- [Services de modèles locaux](/fr/gateway/local-model-services)
- [Fournisseurs de modèles](/fr/concepts/model-providers)
- [LM Studio](/fr/providers/lmstudio)
