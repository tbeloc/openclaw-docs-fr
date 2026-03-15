---
summary: "Comment exécuter les tests localement (vitest) et quand utiliser les modes force/coverage"
read_when:
  - Running or fixing tests
title: "Tests"
---

# Tests

- Kit de test complet (suites, live, Docker) : [Testing](/help/testing)

- `pnpm test:force` : Tue tout processus de passerelle en attente occupant le port de contrôle par défaut, puis exécute la suite Vitest complète avec un port de passerelle isolé pour que les tests serveur ne entrent pas en collision avec une instance en cours d'exécution. À utiliser quand une exécution de passerelle antérieure a laissé le port 18789 occupé.
- `pnpm test:coverage` : Exécute la suite unitaire avec la couverture V8 (via `vitest.unit.config.ts`). Les seuils globaux sont 70% pour les lignes/branches/fonctions/déclarations. La couverture exclut les points d'entrée lourds en intégration (câblage CLI, passerelles gateway/telegram, serveur statique webchat) pour garder l'objectif concentré sur la logique testable en unité.
- `pnpm test` sur Node 22, 23 et 24 utilise `vmForks` de Vitest par défaut pour un démarrage plus rapide. Node 25+ revient à `forks` jusqu'à revalidation. Vous pouvez forcer le comportement avec `OPENCLAW_TEST_VM_FORKS=0|1`.
- `pnpm test` : exécute la voie unitaire principale rapide par défaut pour un retour local rapide.
- `pnpm test:channels` : exécute les suites lourdes en canaux.
- `pnpm test:extensions` : exécute les suites d'extension/plugin.
- Intégration de la passerelle : opt-in via `OPENCLAW_TEST_INCLUDE_GATEWAY=1 pnpm test` ou `pnpm test:gateway`.
- `pnpm test:e2e` : Exécute les tests de fumée de bout en bout de la passerelle (appairage multi-instance WS/HTTP/node). Par défaut `vmForks` + workers adaptatifs dans `vitest.e2e.config.ts` ; ajustez avec `OPENCLAW_E2E_WORKERS=<n>` et définissez `OPENCLAW_E2E_VERBOSE=1` pour les journaux détaillés.
- `pnpm test:live` : Exécute les tests live du fournisseur (minimax/zai). Nécessite des clés API et `LIVE=1` (ou `*_LIVE_TEST=1` spécifique au fournisseur) pour dépasser.

## Portail local PR

Pour les vérifications locales de fusion/portail PR, exécutez :

- `pnpm check`
- `pnpm build`
- `pnpm test`
- `pnpm check:docs`

Si `pnpm test` vacille sur un hôte chargé, réexécutez une fois avant de le traiter comme une régression, puis isolez avec `pnpm vitest run <path/to/test>`. Pour les hôtes à mémoire limitée, utilisez :

- `OPENCLAW_TEST_PROFILE=low OPENCLAW_TEST_SERIAL_GATEWAY=1 pnpm test`

## Banc de latence du modèle (clés locales)

Script : [`scripts/bench-model.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-model.ts)

Utilisation :

- `source ~/.profile && pnpm tsx scripts/bench-model.ts --runs 10`
- Env optionnel : `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `ANTHROPIC_API_KEY`
- Invite par défaut : "Reply with a single word: ok. No punctuation or extra text."

Dernière exécution (2025-12-31, 20 exécutions) :

- minimax médiane 1279ms (min 1114, max 2431)
- opus médiane 2454ms (min 1224, max 3170)

## Banc de démarrage CLI

Script : [`scripts/bench-cli-startup.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-cli-startup.ts)

Utilisation :

- `pnpm tsx scripts/bench-cli-startup.ts`
- `pnpm tsx scripts/bench-cli-startup.ts --runs 12`
- `pnpm tsx scripts/bench-cli-startup.ts --entry dist/entry.js --timeout-ms 45000`

Ceci évalue ces commandes :

- `--version`
- `--help`
- `health --json`
- `status --json`
- `status`

La sortie inclut la moyenne, p50, p95, min/max et la distribution des codes de sortie/signaux pour chaque commande.

## Onboarding E2E (Docker)

Docker est optionnel ; ceci n'est nécessaire que pour les tests de fumée d'onboarding conteneurisés.

Flux de démarrage à froid complet dans un conteneur Linux propre :

```bash
scripts/e2e/onboard-docker.sh
```

Ce script pilote l'assistant interactif via un pseudo-tty, vérifie les fichiers de configuration/espace de travail/session, puis démarre la passerelle et exécute `openclaw health`.

## Test de fumée d'importation QR (Docker)

Assure que `qrcode-terminal` se charge sous les runtimes Docker Node pris en charge (Node 24 par défaut, Node 22 compatible) :

```bash
pnpm test:docker:qr
```
