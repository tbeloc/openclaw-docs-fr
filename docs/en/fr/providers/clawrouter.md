---
summary: "Acheminer les modèles à portée de credential via ClawRouter et afficher les quotas gérés"
title: "ClawRouter"
read_when:
  - You want one managed key for multiple model providers
  - You need ClawRouter model discovery or quota reporting in OpenClaw
---

ClawRouter donne à OpenClaw une clé à portée de politique pour plusieurs fournisseurs de modèles en amont. Le plugin fourni découvre uniquement les modèles autorisés pour cette clé, achemine chaque modèle via son protocole déclaré et rapporte le budget et l'utilisation agrégée de la clé sur les surfaces d'utilisation d'OpenClaw.

Vous n'installez ni n'authentifiez chaque plugin de fournisseur en amont sur l'hôte OpenClaw. Les credentials en amont et le routage spécifique au fournisseur restent dans ClawRouter. OpenClaw a besoin uniquement du plugin `@openclaw/clawrouter` fourni et d'une credential ClawRouter émise.

| Propriété     | Valeur                                   |
| ------------- | ---------------------------------------- |
| Fournisseur   | `clawrouter`                             |
| Package       | `@openclaw/clawrouter`                   |
| Auth          | `CLAWROUTER_API_KEY`                     |
| URL par défaut| `https://clawrouter.openclaw.ai`         |
| Catalogue de modèles | À portée de credential via `/v1/catalog`      |
| Quotas        | Budget mensuel et utilisation via `/v1/usage` |

## Démarrage

<Steps>
  <Step title="Obtenir une credential à portée">
    Demandez à votre administrateur ClawRouter une credential dont la politique inclut
    les fournisseurs, modèles et budget mensuel que vous devez utiliser. Les credentials sont
    révélées une seule fois lors de leur émission.
  </Step>
  <Step title="Configurer OpenClaw">
    ```bash
    export CLAWROUTER_API_KEY="..."
    openclaw onboard --auth-choice clawrouter-api-key
    ```

    Le plugin est inclus avec OpenClaw et activé par défaut. Pour un
    déploiement personnalisé, définissez `models.providers.clawrouter.baseUrl` sur l'origine ClawRouter ; la valeur par défaut est `https://clawrouter.openclaw.ai`.

  </Step>
  <Step title="Lister les modèles accordés">
    ```bash
    openclaw models list --all --provider clawrouter
    ```

    Utilisez les références de modèle retournées exactement comme indiqué. Elles conservent l'espace de noms en amont, tel que `clawrouter/openai/...`, `clawrouter/anthropic/...`, ou
    `clawrouter/google/...`.

  </Step>
  <Step title="Sélectionner un modèle">
    ```bash
    openclaw models set clawrouter/<provider>/<model>
    ```

    Vous pouvez également sélectionner un modèle retourné pour une seule exécution avec
    `openclaw agent --model clawrouter/<provider>/<model> --message "..."`.

  </Step>
</Steps>

## Découverte de modèles

`GET /v1/catalog` est la source de vérité. OpenClaw ne fournit pas une deuxième liste fixe de modèles ClawRouter. Un modèle configuré dans ClawRouter apparaît quand :

- la politique de la credential accorde son fournisseur ;
- la connexion du fournisseur est activée et prête ;
- le modèle du catalogue annonce une capacité LLM supportée ; et
- le catalogue expose un contrat de transport supporté par le plugin.

Ajouter un autre modèle à un fournisseur ClawRouter supporté ne nécessite donc pas une version d'OpenClaw ou un autre plugin de fournisseur. Le prochain rafraîchissement du catalogue le découvre. Un modèle qui nécessite un nouveau protocole de fil nécessite un support dans le plugin ClawRouter avant qu'OpenClaw l'annonce.

## Protocole et plugins de fournisseur

Vous n'avez pas besoin d'installer le plugin d'authentification de chaque entreprise en amont. ClawRouter possède les credentials en amont ; son catalogue indique à OpenClaw quel transport utiliser.
Le plugin supporte :

| Route du catalogue                  | Transport OpenClaw     |
| ------------------------------ | ---------------------- |
| Chat compatible OpenAI         | `openai-completions`   |
| Réponses compatibles OpenAI    | `openai-responses`     |
| Messages Anthropic natifs      | `anthropic-messages`   |
| Streaming Gemini Google natif | `google-generative-ai` |

Le plugin applique également les politiques de relecture et de schéma d'outil correspondantes pour ces familles. Les lignes du catalogue utilisant un autre format de requête/flux ne sont intentionnellement pas annoncées comme modèles de texte OpenClaw. Normalisez ces fournisseurs à l'un des contrats supportés dans ClawRouter plutôt que d'envoyer une charge utile incompatible.

## Quotas et utilisation

La réponse `/v1/usage` de ClawRouter alimente les surfaces normales d'utilisation du fournisseur OpenClaw. `/status` et les statuts de tableau de bord connexes affichent la fenêtre de budget mensuel quand la clé a une limite, plus les totaux de requête, de jeton et de dépense. Les clés non mesurées affichent toujours l'utilisation agrégée sans fenêtre de pourcentage.

La recherche de quota utilise la même clé à portée que la découverte de modèles. Une recherche de quota échouée ne bloque pas l'exécution du modèle.

Vérifiez l'instantané en direct avec :

```bash
openclaw status --usage
openclaw models status
```

Le même instantané de fournisseur est disponible pour `/status` dans le chat et l'interface utilisateur d'utilisation d'OpenClaw. Le budget est à l'échelle de la politique, donc les requêtes faites par un autre client utilisant la même politique ClawRouter peuvent modifier le pourcentage restant.

## Dépannage

| Symptôme                                  | Vérifier                                                                                                                                                 |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aucun modèle ClawRouter                     | Confirmez que la credential est active, sa politique accorde au moins un fournisseur de modèle prêt, et `CLAWROUTER_API_KEY` est disponible pour le processus OpenClaw. |
| Un modèle ClawRouter configuré est manquant | Inspectez sa capacité `/v1/catalog` et son format de route. Les contrats de transport non supportés sont intentionnellement filtrés.                                    |
| `401` ou `403` du catalogue ou de l'utilisation     | Réémettez ou redéfinissez la portée de la credential ClawRouter ; OpenClaw ne revient pas aux clés de fournisseur en amont.                                                 |
| L'appel de modèle échoue après la découverte         | Vérifiez la connexion du fournisseur et la santé en amont dans ClawRouter, puis réessayez après la récupération de son état de disponibilité.                                       |
| L'utilisation a des totaux mais pas de pourcentage       | La politique n'est pas mesurée ; ajoutez un budget mensuel dans ClawRouter pour exposer une fenêtre de pourcentage.                                                            |

## Comportement de sécurité

- La découverte du catalogue est à portée de la clé proxy configurée et mise en cache par clé.
- La clé proxy n'est attachée qu'à la dispatch de requête ; elle n'est pas stockée dans les métadonnées du modèle.
- Les identifiants de modèle Anthropic et Gemini natifs sont réécrits à leurs identifiants en amont uniquement à la dispatch.
- Les lignes du catalogue non supportées ou non accordées échouent fermées et ne sont pas sélectionnables.

## Connexes

<CardGroup cols={2}>
  <Card title="Fournisseurs de modèles" href="/fr/concepts/model-providers" icon="layers">
    Configuration du fournisseur et sélection du modèle.
  </Card>
  <Card title="Suivi de l'utilisation" href="/fr/concepts/usage-tracking" icon="chart-line">
    Surfaces d'utilisation et de statut d'OpenClaw.
  </Card>
</CardGroup>
