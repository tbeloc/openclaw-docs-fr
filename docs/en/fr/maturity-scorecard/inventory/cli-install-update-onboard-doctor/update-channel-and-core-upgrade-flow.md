---
title: CLI - Updates and Upgrades Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# CLI - Updates and Upgrades Maturity Note

## Summary

OpenClaw dispose d'un grand système de mise à jour dédié qui couvre les canaux stable, bêta et dev,
le changement de type d'installation, le redémarrage de passerelle géré et la convergence des plugins après mise à jour. La couverture est forte car le système de mise à jour est largement implémenté et documenté. La qualité est plus faible car le chemin de mise à jour possède toujours certains des modes de défaillance de service et de propriété les plus risqués.

## Scope de la catégorie

Cette catégorie couvre `openclaw update`, l'état de la mise à jour, le changement de canal,
le redémarrage géré après mise à jour et la convergence des plugins principaux. Elle ne couvre pas l'installation initiale ou la réparation autonome du docteur en dehors du flux de mise à jour.

## Fonctionnalités

- Canaux de mise à jour : openclaw update supporte la sélection des canaux stable, bêta et dev.
- Changement de type d'installation : Les flux de mise à jour peuvent basculer entre les installations de paquets et les installations git/source lorsqu'elles sont supportées.
- Redémarrage de passerelle géré : Les flux de mise à jour documentent quand la passerelle gérée est arrêtée, redémarrée ou intentionnellement laissée seule.
- État de mise à jour et RPC : Les opérateurs peuvent inspecter l'état de la mise à jour et l'état du plan de contrôle de la passerelle associé.
- Convergence des plugins : Les mises à jour principales documentent comment les versions des plugins et les avertissements de réparation des plugins sont gérés par la suite.

## Fraîcheur de l'archive

- gitcrawl: `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`, `api_supported=false`, `github_token_present=false`.
- discrawl: `generated_at=2026-05-30T01:10:41Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - `docs/install/updating.md` et `docs/cli/update.md` décrivent les mises à jour de paquets et git, le changement de canal, le comportement de redémarrage et les étapes de récupération manuelle.
  - L'implémentation du système de mise à jour est substantielle dans `src/cli/update-cli/update-command.ts`, `src/cli/update-cli/status.ts`, `src/cli/update-cli/progress.ts` et `src/cli/update-cli/shared.ts`.
  - La logique d'affichage de l'état de mise à jour et du canal est implémentée séparément de la mutation.
  - Le dépôt contient des tests ciblés pour le progrès, les assistants de redémarrage, les exécuteurs de commandes partagées et le comportement de la commande de mise à jour.
- Signaux négatifs :
  - Le système de mise à jour s'étend sur les installations de paquets, les checkouts git, la synchronisation des plugins, le docteur et le redémarrage du service dans un seul flux.
  - Les résultats de redémarrage et de propriété varient toujours selon le type d'installation et la plateforme.
- Lacunes d'intégration :
  - Aucune fumée de mise à jour multi-plateforme en direct n'a été trouvée qui prouve la séquence complète d'échange de paquets plus redémarrage plus convergence des plugins de bout en bout.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports de Gitcrawl :
  - La requête `gitcrawl search issues "openclaw update beta dev restart" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné des problèmes ouverts incluant `#76150 Gateway did not become healthy after restart` et `#86612 Docker gateway container restart loop when OPENCLAW_SANDBOX=1 and OPENCLAW_HOME=/mnt/...`.
- Rapports de Discrawl :
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw update beta dev restart"` a mis en évidence les conseils des opérateurs où les mises à jour n'ont pas pu être appliquées, les conseils de récupération du canal dev manuel et la résolution des problèmes répétés de redémarrage après mise à jour.
- Bonnes qualités :
  - Le système de mise à jour comprend explicitement la sémantique des canaux stable, bêta et dev.
  - Les modes de simulation et d'état permettent aux opérateurs d'inspecter l'intention sans muter l'état.
  - La convergence des plugins principaux est traitée comme une partie de première classe du flux de mise à jour.
- Mauvaises qualités :
  - Les défaillances de mise à jour s'écoulent souvent dans le redémarrage de la passerelle et le travail de réparation du docteur.
  - Les interactions du gestionnaire de services restent l'une des parties les plus risquées du flux.
  - La dérive de propriété et les installations sensibles à l'environnement apparaissent toujours dans l'historique des problèmes adjacents.
- Exclu de la qualité :
  - Les tests de commande de mise à jour et de progrès ne comptent que pour la couverture.

## Lacunes connues

- Aucune matrice de mise à jour de bout en bout en direct sur les types d'installation et les plateformes n'a été trouvée.
- La santé du redémarrage et la convergence après mise à jour produisent toujours des défaillances actives.

## Preuves

### Docs

- `docs/install/updating.md`
- `docs/cli/update.md`
- `docs/gateway/troubleshooting.md`

### Source

- `src/cli/update-cli/update-command.ts`
- `src/cli/update-cli/status.ts`
- `src/cli/update-cli/progress.ts`
- `src/cli/update-cli/shared.ts`

### Tests d'intégration

- Aucun trouvé pour un flux complet de mise à jour et redémarrage multi-plateforme.

### Tests unitaires

- `src/cli/update-cli/update-command.test.ts`
- `src/cli/update-cli/progress.test.ts`
- `src/cli/update-cli/restart-helper.test.ts`
- `src/cli/update-cli/shared.command-runner.test.ts`
- `src/cli/update-cli/post-core-plugin-convergence.test.ts`

### Commandes de validation de surface

- `none declared in taxonomy`: `pass` - La surface CLI ne déclare pas de commandes de validation supplémentaires pour la notation.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "openclaw update beta dev restart" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`

Résultats :

- `[{"number":76150,"state":"open","title":"[Bug]: Gateway did not become healthy after restart.","url":"https://github.com/openclaw/openclaw/issues/76150"},{"number":83981,"state":"open","title":"[Bug]: sessions_yield tool available even when removed from tool policy allowlist","url":"https://github.com/openclaw/openclaw/issues/83981"},{"number":86612,"state":"open","title":"Docker gateway container restart loop when OPENCLAW_SANDBOX=1 and OPENCLAW_HOME=/mnt/...","url":"https://github.com/openclaw/openclaw/issues/86612"}]`

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw update beta dev restart"`

Résultats :

- Les résultats de l'archive incluent plusieurs fils de récupération d'opérateurs où `openclaw update --channel dev|beta`, `openclaw doctor` et `openclaw gateway restart` étaient les étapes prescrites après des mises à niveau échouées ou incomplètes.
