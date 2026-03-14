# Plan de supervision PTY et processus

## 1. Problème et objectif

Nous avons besoin d'un cycle de vie fiable pour l'exécution de commandes longue durée sur :

- exécutions `exec` au premier plan
- exécutions `exec` en arrière-plan
- actions de suivi `process` (`poll`, `log`, `send-keys`, `paste`, `submit`, `kill`, `remove`)
- sous-processus du runner agent CLI

L'objectif n'est pas seulement de supporter PTY. L'objectif est une propriété prévisible, une annulation, un délai d'expiration et un nettoyage sans heuristiques dangereuses de correspondance de processus.

## 2. Portée et limites

- Garder l'implémentation interne dans `src/process/supervisor`.
- Ne pas créer un nouveau package pour cela.
- Garder la compatibilité du comportement actuel où pratique.
- Ne pas élargir la portée à la relecture de terminal ou à la persistance de session de style tmux.

## 3. Implémenté dans cette branche

### Ligne de base du superviseur déjà présente

- Le module superviseur est en place sous `src/process/supervisor/*`.
- L'exécution et le runner CLI sont déjà routés via le spawn et l'attente du superviseur.
- La finalisation du registre est idempotente.

### Cette passe complétée

1. Contrat de commande PTY explicite

- `SpawnInput` est maintenant une union discriminée dans `src/process/supervisor/types.ts`.
- Les exécutions PTY nécessitent `ptyCommand` au lieu de réutiliser `argv` générique.
- Le superviseur ne reconstruit plus les chaînes de commande PTY à partir de jointures argv dans `src/process/supervisor/supervisor.ts`.
- L'exécution runtime passe maintenant `ptyCommand` directement dans `src/agents/bash-tools.exec-runtime.ts`.

2. Découplage de type de couche processus

- Les types superviseur n'importent plus `SessionStdin` des agents.
- Le contrat stdin local du processus vit dans `src/process/supervisor/types.ts` (`ManagedRunStdin`).
- Les adaptateurs dépendent maintenant uniquement des types au niveau du processus :
  - `src/process/supervisor/adapters/child.ts`
  - `src/process/supervisor/adapters/pty.ts`

3. Amélioration de la propriété du cycle de vie de l'outil processus

- `src/agents/bash-tools.process.ts` demande maintenant l'annulation via le superviseur en premier.
- `process kill/remove` utilise maintenant la terminaison de secours process-tree en cas d'absence de recherche du superviseur.
- `remove` conserve le comportement de suppression déterministe en supprimant immédiatement les entrées de session en cours d'exécution après la demande de terminaison.

4. Défauts de surveillance de source unique

- Ajout de défauts partagés dans `src/agents/cli-watchdog-defaults.ts`.
- `src/agents/cli-backends.ts` consomme les défauts partagés.
- `src/agents/cli-runner/reliability.ts` consomme les mêmes défauts partagés.

5. Nettoyage des aides mortes

- Suppression du chemin d'aide `killSession` inutilisé de `src/agents/bash-tools.shared.ts`.

6. Tests de chemin superviseur direct ajoutés

- Ajout de `src/agents/bash-tools.process.supervisor.test.ts` pour couvrir le routage kill et remove via l'annulation du superviseur.

7. Corrections des lacunes de fiabilité complétées

- `src/agents/bash-tools.process.ts` revient maintenant à la terminaison réelle du processus au niveau du système d'exploitation en cas d'absence de recherche du superviseur.
- `src/process/supervisor/adapters/child.ts` utilise maintenant la sémantique de terminaison process-tree pour les chemins kill par défaut d'annulation/délai d'expiration.
- Ajout d'utilitaire process-tree partagé dans `src/process/kill-tree.ts`.

8. Couverture des cas limites du contrat PTY ajoutée

- Ajout de `src/process/supervisor/supervisor.pty-command.test.ts` pour le transfert verbatim de commande PTY et le rejet de commande vide.
- Ajout de `src/process/supervisor/adapters/child.test.ts` pour le comportement de kill process-tree dans l'annulation de l'adaptateur enfant.

## 4. Lacunes restantes et décisions

### Statut de fiabilité

Les deux lacunes de fiabilité requises pour cette passe sont maintenant fermées :

- `process kill/remove` a maintenant un secours de terminaison réelle du système d'exploitation en cas d'absence de recherche du superviseur.
- l'annulation/délai d'expiration enfant utilise maintenant la sémantique de kill process-tree pour le chemin kill par défaut.
- Des tests de régression ont été ajoutés pour les deux comportements.

### Durabilité et réconciliation au démarrage

Le comportement de redémarrage est maintenant explicitement défini comme un cycle de vie en mémoire uniquement.

- `reconcileOrphans()` reste une no-op dans `src/process/supervisor/supervisor.ts` par conception.
- Les exécutions actives ne sont pas récupérées après le redémarrage du processus.
- Cette limite est intentionnelle pour cette passe d'implémentation afin d'éviter les risques de persistance partielle.

### Suites de maintenabilité

1. `runExecProcess` dans `src/agents/bash-tools.exec-runtime.ts` gère toujours plusieurs responsabilités et peut être divisé en aides ciblées dans une suite.

## 5. Plan d'implémentation

La passe d'implémentation pour les éléments de fiabilité et de contrat requis est complète.

Complété :

- secours de terminaison réelle `process kill/remove`
- annulation process-tree pour le chemin kill par défaut de l'adaptateur enfant
- tests de régression pour le kill de secours et le chemin kill de l'adaptateur enfant
- tests de cas limites de commande PTY sous `ptyCommand` explicite
- limite de redémarrage en mémoire explicite avec `reconcileOrphans()` no-op par conception

Suite optionnelle :

- diviser `runExecProcess` en aides ciblées sans dérive de comportement

## 6. Carte des fichiers

### Superviseur de processus

- `src/process/supervisor/types.ts` mis à jour avec entrée spawn discriminée et contrat stdin local du processus.
- `src/process/supervisor/supervisor.ts` mis à jour pour utiliser `ptyCommand` explicite.
- `src/process/supervisor/adapters/child.ts` et `src/process/supervisor/adapters/pty.ts` découplés des types d'agent.
- `src/process/supervisor/registry.ts` finalisation idempotente inchangée et conservée.

### Intégration exec et processus

- `src/agents/bash-tools.exec-runtime.ts` mis à jour pour passer la commande PTY explicitement et conserver le chemin de secours.
- `src/agents/bash-tools.process.ts` mis à jour pour annuler via le superviseur avec terminaison de secours process-tree réelle.
- `src/agents/bash-tools.shared.ts` chemin d'aide kill direct supprimé.

### Fiabilité CLI

- `src/agents/cli-watchdog-defaults.ts` ajouté comme ligne de base partagée.
- `src/agents/cli-backends.ts` et `src/agents/cli-runner/reliability.ts` consomment maintenant les mêmes défauts.

## 7. Exécution de validation dans cette passe

Tests unitaires :

- `pnpm vitest src/process/supervisor/registry.test.ts`
- `pnpm vitest src/process/supervisor/supervisor.test.ts`
- `pnpm vitest src/process/supervisor/supervisor.pty-command.test.ts`
- `pnpm vitest src/process/supervisor/adapters/child.test.ts`
- `pnpm vitest src/agents/cli-backends.test.ts`
- `pnpm vitest src/agents/bash-tools.exec.pty-cleanup.test.ts`
- `pnpm vitest src/agents/bash-tools.process.poll-timeout.test.ts`
- `pnpm vitest src/agents/bash-tools.process.supervisor.test.ts`
- `pnpm vitest src/process/exec.test.ts`

Cibles E2E :

- `pnpm vitest src/agents/cli-runner.test.ts`
- `pnpm vitest run src/agents/bash-tools.exec.pty-fallback.test.ts src/agents/bash-tools.exec.background-abort.test.ts src/agents/bash-tools.process.send-keys.test.ts`

Note de vérification de type :

- Utilisez `pnpm build` (et `pnpm check` pour la porte complète lint/docs) dans ce repo. Les notes plus anciennes qui mentionnent `pnpm tsgo` sont obsolètes.

## 8. Garanties opérationnelles préservées

- Le comportement de durcissement de l'env Exec est inchangé.
- Le flux d'approbation et de liste d'autorisation est inchangé.
- L'assainissement de la sortie et les plafonds de sortie sont inchangés.
- L'adaptateur PTY garantit toujours le règlement d'attente sur kill forcé et la suppression du listener.

## 9. Définition de terminé

1. Le superviseur est propriétaire du cycle de vie pour les exécutions gérées.
2. Le spawn PTY utilise un contrat de commande explicite sans reconstruction argv.
3. La couche processus n'a aucune dépendance de type sur la couche agent pour les contrats stdin du superviseur.
4. Les défauts de surveillance sont une source unique.
5. Les tests unitaires et e2e ciblés restent verts.
6. La limite de durabilité de redémarrage est explicitement documentée ou entièrement implémentée.

## 10. Résumé

La branche a maintenant une forme de supervision cohérente et plus sûre :

- contrat PTY explicite
- couches de processus plus propres
- chemin d'annulation piloté par superviseur pour les opérations de processus
- terminaison de secours réelle en cas d'absence de recherche du superviseur
- annulation process-tree pour les chemins kill par défaut des exécutions enfants
- défauts de surveillance unifiés
- limite de redémarrage en mémoire explicite (pas de réconciliation orpheline entre redémarrage dans cette passe)
