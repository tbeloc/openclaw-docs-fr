---
title: "Hébergement Docker / Podman - Note de maturité du planificateur et de la version E2E Docker"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hébergement Docker / Podman - Note de maturité du planificateur et de la version E2E Docker

## Résumé

L'infrastructure Docker E2E est vaste : elle planifie des voies de version, des voies en direct, des voies soutenues par des paquets, des voies d'installation/mise à jour, des balayages de plugins, la migration de mise à jour, la survie de mise à niveau, Open WebUI, les identifiants, les images partagées, les limites du planificateur, le nettoyage des conteneurs obsolètes et les artefacts de paquets Docker. La couverture est stable pour Docker car de nombreux flux d'exécution majeurs ont des voies nommées. La qualité est bêta car l'ampleur est complexe, principalement spécifique à Docker, et la discussion d'archive confirme que certaines matrices de version-smoke sont des combinaisons implicites plutôt qu'une liste de contrôle canonique nommée.

## Portée des catégories

- Scripts de plan/planificateur Docker E2E, métadonnées de voie, regroupement ciblé, génération d'artefacts de paquets et action d'hydratation GitHub.
- Planification de scénarios d'installation de voie de version, mise à jour, survie de mise à niveau, fournisseur en direct, plugin, Open WebUI et nettoyage.
- Exclut la version smoke du runtime Podman, qui est notée dans le composant Podman.

## Fonctionnalités

- Scripts de plan/planificateur Docker E2E : scripts de plan/planificateur Docker E2E, métadonnées de voie, regroupement ciblé, génération d'artefacts de paquets et action d'hydratation GitHub
- Installation de voie de version : installation de voie de version, mise à jour, survie de mise à niveau, fournisseur en direct, plugin, Open WebUI et planification de scénarios de nettoyage

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (84%)`
- Signaux positifs : la planification des voies Docker couvre la voie de version, la voie de version bêta, Open WebUI, les besoins en images de paquets/en direct, les identifiants de fournisseur, install-e2e, update-channel, survie de mise à niveau, migration de mise à jour, balayages de plugins groupés et scénarios d'état (`/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:98-180`, `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:560-959`). Les tests du planificateur couvrent l'analyse CLI, les limites de ressources/poids, la sérialisation OpenAI en direct, le nettoyage des conteneurs obsolètes, la sortie bornée et le texte de limite d'opérateur (`/Users/kevinlin/code/openclaw/test/scripts/docker-all-scheduler.test.ts:39-294`).
- Signaux négatifs : cette machinerie est uniquement Docker et ne prouve pas automatiquement Podman ; certaines voies importantes sont une preuve de planificateur sauf si les artefacts CI/voie sont inspectés séparément.
- Lacunes d'intégration : aucun rapport agrégé ne lie les résultats récents des voies Docker de version aux scores de maturité Docker/Podman et aux régressions d'archive.

## Score de qualité

- Score : `Bêta (78%)`
- Rapports Gitcrawl : les preuves de requête incluent la PR #87508 pour le filtrage de matrice de flux de travail de version et les problèmes d'archive qui mettent en évidence le comportement de version Docker, y compris la balise `main` GHCR obsolète et les rapports de vérification de santé faux malsains.
- Rapports Discrawl : les preuves de requête incluent une discussion du 2026-05-02 clarifiant que la machinerie de version/mise à niveau smoke existe mais qu'une "matrice" nommée était une abstraction, pas une liste de contrôle canonique ; cela réduit la clarté de l'opérateur plutôt que la profondeur du test.
- Bonnes qualités : la planification des voies est explicite, les exigences d'identifiants sont dérivées, les scénarios d'état sont surfacés, la concurrence du planificateur est bornée par les classes de ressources/poids et les conteneurs obsolètes sont nettoyés avant les exécutions.
- Mauvaises qualités : le système est assez complexe pour que la confiance de l'opérateur nécessite la lecture des sorties du planificateur et du flux de travail ; Podman n'est pas inclus en tant que runtime pair dans ce planificateur.
- Exclu de la qualité : preuves de test unitaire, intégration, e2e, en direct et flux d'exécution.

## Score de complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/docker-podman-hosting.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les scripts de plan/planificateur Docker E2E, installation de voie de version.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Produire un artefact de résumé d'exécution de version qui répertorie les noms de voies Docker, l'état, les références d'image, l'artefact de paquet, les lignes de base et les scénarios de mise à niveau.
- Ajouter des voies smoke Podman ou marquer explicitement Podman comme couvert par les docs/source mais non couvert par la version-smoke.
- Transformer le regroupement implicite de version/mise à niveau smoke en une liste de contrôle nommée pour utilisation dans la fiche d'évaluation.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/docker.md:458-462` pointe les déploiements VM vers les étapes de mise à jour du runtime partagé.
- `/Users/kevinlin/code/openclaw/docs/install/docker-vm-runtime.md:140-148` documente les commandes de build/redémarrage de mise à jour que la version smoke devrait exercer.
- `/Users/kevinlin/code/openclaw/docs/reference/full-release-validation.md` est référencé dans la discussion d'archive comme le parapluie de version incluant la version smoke d'installation et les voies fraîches/mise à niveau multi-OS.

### Source

- `/Users/kevinlin/code/openclaw/scripts/lib/docker-e2e-plan.mjs` possède les définitions de voies Docker E2E et la planification de voie de version.
- `/Users/kevinlin/code/openclaw/scripts/test-docker-all.mjs` possède la planification des voies Docker, les limites de ressources, la vérification préalable et le JSON du plan.
- `/Users/kevinlin/code/openclaw/scripts/package-openclaw-for-docker.mjs:1-14` possède la séquence de build/inventaire/pack d'artefact de paquet Docker E2E.
- `/Users/kevinlin/code/openclaw/.github/actions/docker-e2e-plan/action.yml:58-133` crée des plans, émet des sorties, télécharge les artefacts de paquets et extrait les images Docker partagées.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:98-180` vérifie la planification des voies de version et de version bêta.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:560-658` vérifie l'expansion de scénario/ligne de base de survie de mise à niveau et de migration de mise à jour.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-e2e-plan.test.ts:696-959` vérifie les voies Docker en direct/soutenues par des paquets, Open WebUI, les scénarios d'état, le mappage install-e2e, le mappage de balayage de plugin et les erreurs de voie inconnue.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-all-scheduler.test.ts:123-294` vérifie les limites du planificateur, la sérialisation OpenAI en direct, le nettoyage des conteneurs obsolètes, la sortie bornée et les limites lisibles par l'opérateur.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/test/scripts/targeted-docker-lane-groups.test.ts:4-68` couvre le regroupement de voies ciblées et le partitionnement de survie de mise à niveau.
- `/Users/kevinlin/code/openclaw/test/scripts/package-acceptance-workflow.test.ts` couvre le câblage du flux de travail de paquet/version pour Docker E2E.
- `/Users/kevinlin/code/openclaw/test/scripts/docker-build-helper.test.ts` couvre le comportement du helper de build Docker utilisé par les voies.

### Requêtes Gitcrawl

Requête : `Docker E2E lane release path`

Résultats :

- Atteint la PR #87508, `ci: filter release workflow matrices`, décrivant la planification de matrice de flux de travail de version pour les chunks Docker E2E gérés par profil.

Requête : `Docker release ghcr image main latest`

Résultats :

- Atteint le problème #75827 pour la balise Docker `main` obsolète et le problème #75701 pour le comportement actuel de vérification de santé d'image.

### Requêtes Discrawl

Requête : `Docker E2E release upgrade survivor`

Résultats :

- Trouvé une discussion du 2026-05-02 indiquant que la machinerie explicite de version/mise à niveau smoke existe, y compris la version smoke d'installation, les voies fraîches/mise à niveau multi-OS et `scripts/e2e/upgrade-survivor-docker.sh` ; elle a également clarifié qu'une formulation de "matrice" nommée était une abstraction plutôt qu'une liste de contrôle canonique.

Requête : `Docker VPS`

Résultats :

- Trouvé une discussion de mainteneur sur les cas favorables aux conteneurs de test dans Docker ou VPS avant de prendre le travail de problème, renforçant l'utilisation pratique des voies Docker pour la repro.
