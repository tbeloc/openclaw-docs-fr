---
title: "Application compagne Windows native - Note de maturité de connexion Gateway"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Windows native - Note de maturité de connexion Gateway

## Résumé

OpenClaw dispose d'un véritable service Gateway Windows et d'une infrastructure d'appairage de nœuds, mais pas d'une application compagne Windows native prise en charge qui gère le mode de connexion local/distant, l'appairage d'appareils ou l'attachement/démarrage de Gateway médié par l'application. Les preuves archivées indiquent que l'appairage est un point faible connu dans l'effort de l'application compagne Windows.

## Portée de la catégorie

Inclus dans cette catégorie :

- Attachement/démarrage local de Gateway géré par l'application : Attachement/démarrage local de Gateway géré par l'application et statut
- Modes de connexion Gateway distante : Modes de connexion Gateway distante, gestion des jetons/TLS et reconnexion
- Appairage d'appareil/nœud : Appairage d'appareil/nœud, UX d'approbation en attente et récupération d'appairage

## Fonctionnalités

- Attachement/démarrage local de Gateway géré par l'application : Attachement/démarrage local de Gateway géré par l'application et statut
- Modes de connexion Gateway distante : Modes de connexion Gateway distante, gestion des jetons/TLS et reconnexion
- Appairage d'appareil/nœud : Appairage d'appareil/nœud, UX d'approbation en attente et récupération d'appairage

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (8%)`
- Signaux positifs : la branche principale actuelle dispose de connexion Gateway, de service Windows et de primitives d'appairage de nœuds qu'une future application peut réutiliser.
- Signaux négatifs : aucun coordinateur de mode local/distant d'application Windows, interface utilisateur d'appairage, magasin d'identité d'appareil d'application, gestionnaire de tunnel distant ou UX de reconnexion n'existe dans la source prise en charge.
- Lacunes d'intégration : aucun appairage d'application de bout en bout, attachement/démarrage local, connexion Gateway distante, réparation TLS/jeton ou scénario de reconnexion n'est disponible.

Étiquettes de couverture :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Bêta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, les preuves de bout en bout, en direct ou de flux d'exécution réel sur le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Expérimental (35%)`
- Rapports Gitcrawl : `#73315` propose une application compagne de bureau multiplateforme ; la requête spécifique aux fonctionnalités pour l'appairage/installation n'a retourné aucun résultat Gitcrawl.
- Rapports Discrawl : le message du responsable du `2026-05-06` indique que l'appairage n'est pas aussi robuste que souhaité pour l'application compagne de code natif Windows.
- Bonnes qualités : les limites Gateway et d'appairage de nœuds sont établies dans le référentiel, et la documentation Windows oriente les utilisateurs vers les chemins CLI/Gateway/WSL2 pris en charge.
- Mauvaises qualités : le contrat de connexion au niveau de l'application est absent et la discussion de prototype connue souligne la fragilité de l'appairage.
- Exclu de la qualité : les preuves unitaires, d'intégration, de bout en bout, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer la qualité.

Étiquettes de qualité :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Bêta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, de bout en bout, en direct ou d'exécution réelle comme entrée de notation.

## Score de complétude

- Score : `Expérimental (8%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'attachement/démarrage local de Gateway géré par l'application, les modes de connexion Gateway distante, l'appairage d'appareil/nœud.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune interface utilisateur d'appairage d'application Windows ou cycle de vie d'identité d'appareil d'application n'existe dans la branche principale actuelle.
- Aucun paramètre de mode local/distant d'application native ou gestionnaire de tunnel n'existe.
- La documentation n'explique pas comment une application Windows externe/prototype devrait s'appairer avec les versions Gateway actuelles.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:10-15` sépare le support CLI/Gateway natif du support d'application compagne planifié.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:52-59` documente le démarrage géré de Gateway Windows natif, pas le démarrage géré par l'application compagne.
- `/Users/kevinlin/code/openclaw/docs/gateway/index.md` documente le fonctionnement de Gateway et le comportement du service Tâche planifiée Windows.

### Source

- `/Users/kevinlin/code/openclaw/src/daemon/service.ts:288-300` mappe la gestion du service Gateway `win32` aux Tâches planifiées.
- `/Users/kevinlin/code/openclaw/src/infra/node-pairing.ts` et `/Users/kevinlin/code/openclaw/src/infra/node-pairing-authz.ts` fournissent des primitives d'appairage adjacentes.
- Aucune source de mode de connexion d'application Windows, d'invite d'appairage ou de tunnel distant n'a été trouvée.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/parallels/windows-smoke.ts` valide les flux CLI/Gateway Windows natifs, y compris le démarrage de Gateway et les tours d'agent.
- Aucun test d'intégration d'appairage d'application Windows ou de mode local/distant n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/infra/node-pairing.test.ts`
- `/Users/kevinlin/code/openclaw/src/infra/node-pairing-authz.test.ts`
- `/Users/kevinlin/code/openclaw/src/gateway/server.node-pairing-authz.test.ts`
- Aucun test unitaire d'appairage d'application Windows n'a été trouvé.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Windows companion pairing install x64 arm WSL" --json`
- `gitcrawl search openclaw/openclaw --query "Tauri desktop companion Windows Linux" --json`

Résultats :

- La requête appairage/installation n'a retourné aucun résultat.
- `#73315` PR ouvert propose un MVP d'application compagne Tauri pour Linux/Windows.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --limit 6 "Windows companion pairing install x64 arm WSL"`

Résultats :

- Le message du responsable du `2026-05-06` indique que l'effort d'application compagne Windows native vise la parité avec l'application compagne Mac, mais l'appairage et l'installation ne sont pas aussi robustes que souhaité et les combinaisons x64/ARM/Windows/WSL restent.
