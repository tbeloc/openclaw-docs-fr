---
title: "ClawHub - External Plugin Trust, Integrity, and Install Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - External Plugin Trust, Integrity, and Install Approvals Maturity Note

## Résumé

La confiance envers les plugins externes est explicite et comparativement robuste : la documentation avertit que l'installation d'un plugin équivaut à exécuter du code, la vérification d'installation de ClawHub valide les hachages d'artefacts, npm install vérifie la dérive d'intégrité, et les analyses au moment de l'installation peuvent bloquer le code dangereux. La couverture est Beta car il existe une couverture unitaire/runtime forte mais moins de preuve de registre en direct. La qualité est Stable car l'implémentation est fail-closed aux endroits importants et la limite de confiance est clairement documentée.

## Portée de la catégorie

- Modèle de confiance de l'opérateur pour installer et activer du code externe.
- Vérification du digest de l'archive ClawHub et ClawPack.
- Dérive d'intégrité npm et vérifications d'installation gérées.
- Scanner de code dangereux intégré et sémantique de remplacement d'urgence.
- Comportement de révision de publication/version cachée de ClawHub en tant que signal de confiance en amont.

## Fonctionnalités

- Modèle de confiance de l'opérateur pour l'installation : Modèle de confiance de l'opérateur pour installer et activer du code externe
- Archive ClawHub : Vérification du digest de l'archive ClawHub et ClawPack
- Dérive d'intégrité npm : Dérive d'intégrité npm et vérifications d'installation gérées
- Scanner de code dangereux intégré : Scanner de code dangereux intégré et sémantique de remplacement d'urgence
- Comportement de révision de publication/version cachée de ClawHub en tant qu'amont : Comportement de révision de publication/version cachée de ClawHub en tant que signal de confiance en amont

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : la documentation, le code source et les tests couvrent les avertissements de confiance, les hooks du scanner d'installation, la vérification des artefacts ClawHub, la vérification des fichiers de secours, la dérive d'intégrité npm et la dissimulation de révision de publication.
- Signaux négatifs : aucune preuve de plugin malveillant en direct, de blocage de scan ClawHub ou de version cachée de registre de production n'a été trouvée dans le dépôt OpenClaw.
- Lacunes d'intégration : les approbations d'installation externes sont des décisions de politique CLI/locale, et non un flux complet d'attestation de marché.

## Score de qualité

- Score : `Stable (80%)`
- Bonnes qualités : les vérifications d'intégrité échouent fermées, les remplacements d'installation non sécurisés ne contournent pas les blocs de politique de plugin ou les échecs du scanner, la gestion officielle des sources de confiance est explicite, et la documentation de sécurité place les plugins à l'intérieur du TCB de la passerelle.
- Mauvaises qualités : l'opérateur doit toujours choisir s'il fait confiance au code tiers, et les options locales de remplacement d'urgence peuvent contourner les conclusions critiques du scan sur la machine de l'utilisateur.
- Exclus de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux runtime ne sont comptabilisées que sous Couverture, pas Qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs : les preuves archivées de documentation, code source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le modèle de confiance de l'opérateur pour l'installation, l'archive ClawHub, la dérive d'intégrité npm, le scanner de code dangereux intégré, le comportement de révision de publication/version cachée de ClawHub en tant qu'amont.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les mises en garde visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve en direct pour une version de ClawHub cachée par le scan du registre puis révélée après vérification.
- Ajouter un résumé d'installation visible par l'opérateur qui affiche la confiance source, le niveau de vérification, les faits d'intégrité et les décisions de politique avant d'activer le code runtime.

## Preuves

### Documentation

- `docs/tools/plugin.md:66` : la documentation indique aux utilisateurs de traiter les installations de plugins comme l'exécution de code.
- `docs/cli/plugins.md:159` : `--dangerously-force-unsafe-install` contourne uniquement les blocs du scanner intégré et non les blocs de politique de plugin ou les échecs de scan.
- `docs/cli/plugins.md:228` : les installations ClawHub vérifient les en-têtes de digest, les digests d'artefacts, l'intégrité npm et les métadonnées shasum.
- `docs/clawhub/publishing.md:56` : le flux de version démarre les vérifications de sécurité et cache les versions jusqu'à ce que la révision et la vérification se terminent.
- `SECURITY.md:145` : les plugins/extensions font partie de la base de calcul de confiance de la passerelle.

### Code source

- `src/plugins/install-security-scan.ts:48` : analyse les sources d'installation du bundle.
- `src/plugins/install-security-scan.ts:63` : analyse les sources d'installation du package.
- `src/plugins/install-security-scan.ts:82` : analyse les arbres de dépendances des packages installés.
- `src/plugins/clawhub.ts:1164` : vérifie le digest ClawPack, l'intégrité npm et les champs shasum.
- `src/plugins/clawhub.ts:1204` : revient à la vérification stricte de `files[]` si nécessaire.

### Tests d'intégration

- Aucun test d'intégration de blocage de scan ClawHub ou de plugin malveillant en direct n'a été trouvé.
- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:41` : exerce la mécanique réelle d'installation/mise à jour de package utilisée après l'acceptation de la confiance source.

### Tests unitaires

- `src/plugins/clawhub.test.ts:678` : rejette les artefacts ClawPack lorsque le digest de téléchargement ne correspond pas aux métadonnées.
- `src/plugins/clawhub.test.ts:1102` : échoue fermé lorsque les métadonnées de hachage ne sont pas reconnues.
- `src/plugins/clawhub.test.ts:1322` : rejette les archives téléchargées dont le hachage dérive des métadonnées.
- `src/plugins/update.test.ts:1792` : abandonne les mises à jour npm exactement épinglées en cas de dérive d'intégrité par défaut.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "plugin install security scan integrity approval untrusted malicious plugin" --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "unsafe plugin install security scan trusted source" --limit 5 --json`

Résultats :

- Les deux requêtes n'ont retourné aucun résultat, donc les preuves d'archive GitHub n'ont pas ajouté de signal de bogue/régression en direct pour ce chemin de confiance.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "plugin install security scan trust approval"`

Résultats :

- N'a retourné aucun résultat, donc les preuves d'archive Discord n'ont pas ajouté de preuve d'opérateur en direct pour les approbations d'installation.
