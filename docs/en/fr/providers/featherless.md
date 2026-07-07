---
summary: "Configuration de Featherless AI, sélection de modèle et appels d'outils"
title: "Featherless AI"
read_when:
  - You want to use Featherless AI with OpenClaw
  - You need the Featherless API key env var or model ref format
---

[Featherless AI](https://featherless.ai) sert des modèles ouverts via une API
compatible OpenAI. OpenClaw installe Featherless en tant que plugin de
fournisseur externe officiel et maintient le catalogue intégré petit tout en
acceptant les identifiants de modèle exacts de Featherless à l'exécution.

| Propriété       | Valeur                                   |
| --------------- | ---------------------------------------- |
| ID du fournisseur | `featherless`                            |
| Package         | `@openclaw/featherless-provider`         |
| Variable env d'authentification | `FEATHERLESS_API_KEY`                    |
| Drapeau d'intégration | `--auth-choice featherless-api-key`      |
| Drapeau CLI direct | `--featherless-api-key <key>`            |
| API             | Compatible OpenAI (`openai-completions`) |
| URL de base      | `https://api.featherless.ai/v1`          |
| Modèle par défaut | `featherless/Qwen/Qwen3-32B`             |

## Configuration

Installez le plugin et redémarrez la Gateway :

```bash
openclaw plugins install @openclaw/featherless-provider
openclaw gateway restart
```

Exécutez l'intégration :

```bash
openclaw onboard --auth-choice featherless-api-key
```

Pour une configuration non-interactive :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice featherless-api-key \
  --featherless-api-key "$FEATHERLESS_API_KEY"
```

Ou exposez la clé au processus Gateway :

```bash
export FEATHERLESS_API_KEY="<your-featherless-api-key>" # pragma: allowlist secret
```

Vérifiez le fournisseur :

```bash
openclaw models list --provider featherless
```

## Modèle par défaut

Le plugin utilise `Qwen/Qwen3-32B` comme défaut de configuration car Featherless
documente l'appel d'outils natif pour la famille Qwen 3. OpenClaw configure sa
fenêtre de contexte de 32 768 jetons, une limite de sortie conservatrice de
4 096 jetons, et les contrôles de réflexion du modèle de chat Qwen.

Les champs de coût du catalogue sont zéro car Featherless supporte plusieurs
modes de facturation et OpenClaw n'intègre pas les tarifs spécifiques au compte
ou les tarifs à la demande.

## Autres modèles Featherless

Utilisez l'identifiant exact du modèle Featherless après le préfixe du
fournisseur `featherless/` :

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "featherless/moonshotai/Kimi-K2-Instruct",
      },
    },
  },
}
```

OpenClaw ne copie délibérément pas l'index complet des modèles publics de
Featherless dans le sélecteur. L'index est volumineux et n'expose pas assez de
métadonnées de capacité structurées pour classer en toute sécurité tous les
modèles de texte, vision, intégration et raisonnement. Les identifiants inconnus
se résolvent donc avec des défauts conservateurs texte uniquement, sans
raisonnement : une fenêtre de contexte de 4 096 jetons et une limite de sortie
de 1 024 jetons.

Ajoutez une entrée de modèle de fournisseur explicite quand un modèle a besoin
de métadonnées différentes :

```json5
{
  models: {
    mode: "merge",
    providers: {
      featherless: {
        baseUrl: "https://api.featherless.ai/v1",
        apiKey: "${FEATHERLESS_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "google/gemma-3-27b-it",
            name: "Gemma 3 27B",
            input: ["text", "image"],
            reasoning: false,
            contextWindow: 32768,
            maxTokens: 4096,
          },
        ],
      },
    },
  },
}
```

Consultez le catalogue de modèles de Featherless pour la disponibilité actuelle
des modèles et les balises de capacité avant d'ajouter des métadonnées
personnalisées.

## Dépannage

- `401` ou `403` : confirmez que `FEATHERLESS_API_KEY` est visible au processus
  Gateway, ou exécutez à nouveau l'intégration.
- Modèle inconnu : utilisez l'identifiant exact sensible à la casse de Featherless
  après le préfixe `featherless/`.
- Appels d'outils retournés en tant que texte : choisissez une famille de modèles
  que Featherless documente pour l'appel de fonction natif, comme Qwen 3.
- Gateway gérée ne peut pas voir la clé : mettez-la dans `~/.openclaw/.env` ou
  une autre source d'environnement chargée par le service, puis redémarrez la
  Gateway.

## Connexes

- [Fournisseurs de modèles](/fr/concepts/model-providers)
- [Tous les fournisseurs](/fr/providers/index)
- [Modes de réflexion](/fr/tools/thinking)
