---
summary: "Aperçu des options et flux d'intégration OpenClaw"
read_when:
  - Choosing an onboarding path
  - Setting up a new environment
title: "Aperçu de l'intégration"
sidebarTitle: "Aperçu de l'intégration"
---

# Aperçu de l'intégration

OpenClaw prend en charge plusieurs chemins d'intégration selon l'endroit où la Gateway s'exécute et la façon dont vous préférez configurer les fournisseurs.

## Choisissez votre chemin d'intégration

- **Assistant CLI** pour macOS, Linux et Windows (via WSL2).
- **Application macOS** pour une première exécution guidée sur Apple silicon ou Intel Macs.

## Assistant d'intégration CLI

Exécutez l'assistant dans un terminal :

```bash
openclaw onboard
```

Utilisez l'assistant CLI lorsque vous souhaitez un contrôle total de la Gateway, de l'espace de travail, des canaux et des compétences. Documentation :

- [Assistant d'intégration (CLI)](/start/wizard)
- [Commande `openclaw onboard`](/cli/onboard)

## Intégration de l'application macOS

Utilisez l'application OpenClaw lorsque vous souhaitez une configuration entièrement guidée sur macOS. Documentation :

- [Intégration (Application macOS)](/start/onboarding)

## Fournisseur personnalisé

Si vous avez besoin d'un endpoint qui n'est pas répertorié, y compris les fournisseurs hébergés qui exposent des API OpenAI ou Anthropic standard, choisissez **Fournisseur personnalisé** dans l'assistant CLI. Il vous sera demandé de :

- Choisir compatible OpenAI, compatible Anthropic, ou **Inconnu** (détection automatique).
- Entrer une URL de base et une clé API (si requise par le fournisseur).
- Fournir un ID de modèle et un alias optionnel.
- Choisir un ID d'endpoint pour que plusieurs endpoints personnalisés puissent coexister.

Pour les étapes détaillées, consultez la documentation d'intégration CLI ci-dessus.
