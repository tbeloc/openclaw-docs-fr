---
title: "Tencent Cloud (TokenHub)"
summary: "Configuration de Tencent Cloud TokenHub"
read_when:
  - You want to use Tencent Hy models with OpenClaw
  - You need the TokenHub API key setup
---

# Tencent Cloud (TokenHub)

Le fournisseur Tencent Cloud donne accès aux modèles Tencent Hy via le point de terminaison TokenHub (`tencent-tokenhub`).

Le fournisseur utilise une API compatible avec OpenAI.

## Démarrage rapide

```bash
openclaw onboard --auth-choice tokenhub-api-key
```

## Exemple non-interactif

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice tokenhub-api-key \
  --tokenhub-api-key "$TOKENHUB_API_KEY" \
  --skip-health \
  --accept-risk
```

## Fournisseurs et points de terminaison

| Fournisseur        | Point de terminaison          | Cas d'usage                 |
| ------------------ | ----------------------------- | --------------------------- |
| `tencent-tokenhub` | `tokenhub.tencentmaas.com/v1` | Hy via Tencent TokenHub     |

## Modèles disponibles

### tencent-tokenhub

- **hy3-preview** — Aperçu Hy3 (contexte 256K, raisonnement, par défaut)

## Remarques

- Les références de modèles TokenHub utilisent `tencent-tokenhub/<modelId>`.
- Remplacez les métadonnées de tarification et de contexte dans `models.providers` si nécessaire.

## Note sur l'environnement

Si la passerelle s'exécute en tant que démon (launchd/systemd), assurez-vous que `TOKENHUB_API_KEY`
est disponible pour ce processus (par exemple, dans `~/.openclaw/.env` ou via
`env.shellEnv`).

## Documentation connexe

- [Configuration OpenClaw](/fr/configuration)
- [Fournisseurs de modèles](/fr/concepts/model-providers)
- [Tencent TokenHub](https://cloud.tencent.com/document/product/1823/130050)
