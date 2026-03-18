---
summary: "Utiliser les modèles xAI Grok dans OpenClaw"
read_when:
  - Vous souhaitez utiliser les modèles Grok dans OpenClaw
  - Vous configurez l'authentification xAI ou les identifiants de modèle
title: "xAI"
---

# xAI

OpenClaw est livré avec un plugin de fournisseur `xai` intégré pour les modèles Grok.

## Configuration

1. Créez une clé API dans la console xAI.
2. Définissez `XAI_API_KEY`, ou exécutez :

```bash
openclaw onboard --auth-choice xai-api-key
```

3. Choisissez un modèle tel que :

```json5
{
  agents: { defaults: { model: { primary: "xai/grok-4" } } },
}
```

## Catalogue de modèles intégrés actuel

OpenClaw inclut maintenant ces familles de modèles xAI prêtes à l'emploi :

- `grok-4`, `grok-4-0709`
- `grok-4-fast-reasoning`, `grok-4-fast-non-reasoning`
- `grok-4-1-fast-reasoning`, `grok-4-1-fast-non-reasoning`
- `grok-4.20-experimental-beta-0304-reasoning`
- `grok-4.20-experimental-beta-0304-non-reasoning`
- `grok-code-fast-1`

Le plugin résout également en avant les identifiants `grok-4*` et `grok-code-fast*` plus récents lorsqu'ils suivent la même forme d'API.

## Recherche web

Le fournisseur de recherche web `grok` intégré utilise également `XAI_API_KEY` :

```bash
openclaw config set tools.web.search.provider grok
```

## Limites connues

- L'authentification est actuellement par clé API uniquement. Il n'y a pas encore de flux OAuth/code-appareil xAI dans OpenClaw.
- `grok-4.20-multi-agent-experimental-beta-0304` n'est pas supporté sur le chemin du fournisseur xAI normal car il nécessite une surface API en amont différente du transport xAI standard d'OpenClaw.
- Les outils côté serveur xAI natifs tels que `x_search` et `code_execution` ne sont pas encore des fonctionnalités de fournisseur de modèle de première classe dans le plugin intégré.

## Notes

- OpenClaw applique automatiquement les correctifs de compatibilité de schéma d'outil et d'appel d'outil spécifiques à xAI sur le chemin du runner partagé.
- Pour un aperçu plus large des fournisseurs, voir [Fournisseurs de modèles](/fr/providers/index).
