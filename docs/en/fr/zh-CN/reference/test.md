---
read_when:
  - 运行或修复测试
summary: 如何在本地运行测试（vitest）以及何时使用 force/coverage 模式
title: 测试
x-i18n:
  generated_at: "2026-02-03T10:09:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: be7b751fb81c8c94b1293624bdca6582e60a26084960d1df9558061969502e6f
  source_path: reference/test.md
  workflow: 15
---

# Tests

- Suite de tests complète (ensembles de tests, tests en direct, Docker) : [Tests](/help/testing)

- `pnpm test:force` : Termine tout processus Gateway hérité occupant le port de contrôle par défaut, puis exécute la suite Vitest complète avec un port Gateway isolé, de sorte que les tests serveur ne conflictent pas avec l'instance en cours d'exécution. Utilisez cette commande lorsqu'une exécution Gateway précédente occupait le port 18789.
- `pnpm test:coverage` : Exécute Vitest avec la couverture V8. Le seuil global est de 70 % de couverture des lignes/branches/fonctions/déclarations. La couverture exclut les points d'entrée intensifs en intégration (connexion CLI, passerelles gateway/telegram, serveur statique webchat) pour maintenir l'accent sur la logique testable par unité.
- `pnpm test:e2e` : Exécute les tests de fumée de bout en bout Gateway (appairage multi-instances WS/HTTP/nœud).
- `pnpm test:live` : Exécute les tests en direct des fournisseurs (minimax/zai). Nécessite des clés API et `LIVE=1` (ou `*_LIVE_TEST=1` spécifique au fournisseur) pour désactiver le saut.

## Benchmark de latence du modèle (clés locales)

Script : [`scripts/bench-model.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-model.ts)

Utilisation :

- `source ~/.profile && pnpm tsx scripts/bench-model.ts --runs 10`
- Variables d'environnement optionnelles : `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `ANTHROPIC_API_KEY`
- Invite par défaut : "Reply with a single word: ok. No punctuation or extra text."

Dernière exécution (2025-12-31, 20 fois) :

- minimax médiane 1279ms (min 1114, max 2431)
- opus médiane 2454ms (min 1224, max 3170)

## Onboarding E2E (Docker)

Docker est optionnel ; ceci est uniquement pour les tests de fumée d'onboarding conteneurisés.

Processus de démarrage à froid complet dans un conteneur Linux propre :

```bash
scripts/e2e/onboard-docker.sh
```

Ce script pilote l'assistant interactif via un pseudo-terminal, valide les fichiers de configuration/espace de travail/session, puis lance Gateway et exécute `openclaw health`.

## Test de fumée d'importation QR (Docker)

Assurez-vous que `qrcode-terminal` se charge dans Docker sous Node 22+ :

```bash
pnpm test:docker:qr
```
