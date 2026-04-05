---
summary: "Configuration Fireworks (authentification + sélection du modèle)"
read_when:
  - You want to use Fireworks with OpenClaw
  - You need the Fireworks API key env var or default model id
---

# Fireworks

[Fireworks](https://fireworks.ai) expose des modèles open-weight et routés via une API compatible OpenAI. OpenClaw inclut désormais un plugin fournisseur Fireworks intégré.

- Fournisseur : `fireworks`
- Authentification : `FIREWORKS_API_KEY`
- API : chat/completions compatible OpenAI
- URL de base : `https://api.fireworks.ai/inference/v1`
- Modèle par défaut : `fireworks/accounts/fireworks/routers/kimi-k2p5-turbo`

## Démarrage rapide

Configurez l'authentification Fireworks via l'intégration :

```bash
openclaw onboard --auth-choice fireworks-api-key
```

Cela stocke votre clé Fireworks dans la configuration OpenClaw et définit le modèle de démarrage Fire Pass comme modèle par défaut.

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice fireworks-api-key \
  --fireworks-api-key "$FIREWORKS_API_KEY" \
  --skip-health \
  --accept-risk
```

## Note sur l'environnement

Si la passerelle s'exécute en dehors de votre shell interactif, assurez-vous que `FIREWORKS_API_KEY`
est également disponible pour ce processus. Une clé se trouvant uniquement dans `~/.profile` ne sera pas utile à un daemon launchd/systemd à moins que cet environnement ne soit également importé là-bas.

## Catalogue intégré

| Référence du modèle                                    | Nom                         | Entrée     | Contexte | Sortie max | Notes                                      |
| ------------------------------------------------------ | --------------------------- | ---------- | -------- | ---------- | ------------------------------------------ |
| `fireworks/accounts/fireworks/routers/kimi-k2p5-turbo` | Kimi K2.5 Turbo (Fire Pass) | text,image | 256,000  | 256,000    | Modèle de démarrage par défaut intégré sur Fireworks |

## IDs de modèles Fireworks personnalisés

OpenClaw accepte également les IDs de modèles Fireworks dynamiques. Utilisez l'ID exact du modèle ou du routeur affiché par Fireworks et préfixez-le avec `fireworks/`.

Exemple :

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "fireworks/accounts/fireworks/routers/kimi-k2p5-turbo",
      },
    },
  },
}
```

Si Fireworks publie un modèle plus récent, comme une nouvelle version de Qwen ou Gemma, vous pouvez basculer directement vers celui-ci en utilisant son ID de modèle Fireworks sans attendre une mise à jour du catalogue intégré.
