---
title: CLI - Note de maturité de l'intégration et de la configuration d'authentification
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# CLI - Note de maturité de l'intégration et de la configuration d'authentification

## Résumé

L'interface CLI dispose d'une large surface d'intégration et de reconfiguration couvrant la configuration de l'espace de travail, le mode passerelle, l'authentification des fournisseurs, le stockage soutenu par SecretRef, et les choix de passerelle distante par rapport à locale. La couverture est solide car les flux sont bien documentés et largement testés ; la qualité est inférieure à la couverture car l'authentification et les divisions passerelle distante/locale restent subtiles.

## Portée de la catégorie

Cette catégorie couvre `openclaw onboard`, `openclaw configure`, les choix d'authentification, la persistance de l'authentification de la passerelle, et le comportement d'intégration distante. Elle ne couvre pas les spécificités des plugins/canaux ou le cycle de vie du service de passerelle gérée.

## Fonctionnalités

- Intégration guidée : openclaw onboard guide à travers la configuration de l'espace de travail, de la passerelle, de l'authentification du modèle, des canaux, des compétences et de la santé.
- Reconfiguration ciblée : openclaw configure permet aux opérateurs de revisiter uniquement les sections qu'ils souhaitent modifier après la configuration initiale.
- Choix d'authentification : L'intégration et la configuration supportent les choix d'authentification par clé API, OAuth et autres spécifiques au fournisseur.
- Stockage de l'authentification de la passerelle : La configuration du jeton et du mot de passe de la passerelle sont documentées, y compris le comportement du stockage géré par SecretRef.
- Intégration distante : L'intégration de passerelle distante documente ce qui est configuré localement par rapport à ce qui doit déjà exister sur l'hôte distant.

## Fraîcheur de l'archive

- gitcrawl : `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `repository_count=2`, `api_supported=false`, `github_token_present=false`.
- discrawl : `generated_at=2026-05-30T01:10:41Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Score de couverture

- Score : `Stable (86%)`
- Signaux positifs :
  - `docs/cli/onboard.md`, `docs/cli/configure.md`, et `docs/start/onboarding-overview.md` documentent les flux interactifs, non-interactifs, locaux, distants, OAuth, clé API et SecretRef.
  - Les implémentations d'intégration et de configuration sont divisées en modules dédiés dans `src/commands/onboard.ts`, `src/commands/onboard-interactive.ts`, `src/commands/onboard-non-interactive.ts`, `src/commands/configure.ts`, et `src/commands/configure.gateway-auth.ts`.
  - La persistance du jeton de passerelle et les protections SecretRef existent dans `src/commands/gateway-install-token.ts`.
  - Le comportement d'intégration distante est directement exercé dans `src/commands/onboard-remote.test.ts`.
- Signaux négatifs :
  - Le comportement d'authentification, de fournisseur et de passerelle distante/locale s'étend sur de nombreux modules et branches de configuration.
  - La preuve en environnement réel est plus mince que la surface de test des commandes et de la configuration.
- Lacunes d'intégration :
  - Aucun e2e complet dédié pour l'intégration d'une véritable passerelle distante plus l'authentification du fournisseur n'a été trouvé dans le dépôt principal.

## Score de qualité

- Score : `Beta (78%)`
- Rapports de gitcrawl :
  - La requête `gitcrawl search issues "onboard configure auth remote gateway" -R openclaw/openclaw --state open --json number,title,url,state --limit 5` a retourné un résultat ouvert : `#59165 RFC: Credential Provider Plugin`.
- Rapports de discrawl :
  - La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw onboard auth remote gateway"` a mis en évidence des discussions autour de l'ancien mode d'échec d'alignement de jeton distant et la confusion des opérateurs lorsque les surfaces de jeton local et distant divergent.
- Bonnes qualités :
  - La documentation distingue explicitement l'intégration locale de l'intégration distante.
  - La gestion du jeton de passerelle gérée par SecretRef échoue fermée au lieu de cuire silencieusement du texte brut dans les métadonnées du service.
  - Le choix d'authentification et le comportement spécifique au fournisseur sont implémentés via des modules dédiés au lieu de demandes ad hoc dispersées.
- Mauvaises qualités :
  - La sémantique de l'authentification de la passerelle et du jeton distant est suffisamment subtile pour avoir produit une confusion antérieure des opérateurs.
  - L'ampleur des combinaisons de fournisseur et d'authentification supportées augmente la chance de dérive des cas limites.
- Exclu de la qualité :
  - Les fichiers de test d'intégration et d'authentification énumérés ci-dessous fournissent uniquement une corroboration de couverture.

## Lacunes connues

- Aucune preuve e2e locale au dépôt pour un parcours complet d'intégration de passerelle distante n'a été trouvée.
- L'ampleur du fournisseur augmente le fardeau de maintenance à long terme de cette surface.

## Preuves

### Docs

- `docs/cli/onboard.md`
- `docs/cli/configure.md`
- `docs/start/onboarding-overview.md`

### Source

- `src/commands/onboard.ts`
- `src/commands/onboard-interactive.ts`
- `src/commands/onboard-non-interactive.ts`
- `src/commands/configure.ts`
- `src/commands/configure.gateway-auth.ts`
- `src/commands/gateway-install-token.ts`

### Tests d'intégration

- Aucun trouvé pour un flux complet de passerelle distante plus authentification du fournisseur de bout en bout.

### Tests unitaires

- `src/commands/onboard-remote.test.ts`
- `src/commands/onboard-auth.config-shared.test.ts`
- `src/commands/onboard-search.test.ts`
- `src/commands/onboard-non-interactive.gateway.test.ts`
- `src/commands/configure.gateway.test.ts`
- `src/commands/auth-choice.test.ts`

### Commandes de validation de surface

- `none declared in taxonomy`: `pass` - La surface CLI ne déclare pas de commandes de validation supplémentaires pour la notation.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "onboard configure auth remote gateway" -R openclaw/openclaw --state open --json number,title,url,state --limit 5`

Résultats :

- `[{"number":59165,"state":"open","title":"RFC: Credential Provider Plugin","url":"https://github.com/openclaw/openclaw/issues/59165"}]`

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 5 "openclaw onboard auth remote gateway"`

Résultats :

- Les résultats d'archive discutent de la confusion historique de `gateway.remote.token` et montrent que ce domaine a nécessité une explication minutieuse même lorsque le bug immédiat a été considéré ultérieurement comme non reproductible sur `main` actuel.
