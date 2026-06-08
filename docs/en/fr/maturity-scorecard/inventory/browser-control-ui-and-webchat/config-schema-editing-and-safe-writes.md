---
title: "Gateway Web App - Note de Maturité de Configuration"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Gateway Web App - Note de Maturité de Configuration

## Résumé

L'éditeur de configuration Control UI est une surface d'opérateur mature : il lit les instantanés expurgés, charge le schéma et les indices d'interface utilisateur, prend en charge l'édition de formulaire et brute, valide via la passerelle, utilise des gardes de hachage de base, restaure soigneusement les valeurs expurgées, applique les plans de configuration/redémarrage et gère la vérification préalable de SecretRef. La couverture est Stable car les flux d'écriture du serveur et les contrôleurs du navigateur disposent tous deux de tests ciblés. La qualité est Beta car l'implémentation est robuste, mais les preuves d'archive incluent des régressions en mode brut, des demandes d'UX de renforcement de configuration et des surprises de configuration de fournisseur/modèle.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Instantanés de configuration : Couvre les instantanés de configuration dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Édition de formulaire de schéma : Couvre l'édition de formulaire de schéma dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Édition JSON brute : Couvre l'édition JSON brute dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Écritures gardées par hachage de base : Couvre les écritures gardées par hachage de base dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Appliquer et redémarrer : Couvre l'application et le redémarrage dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.

## Fonctionnalités

- Instantanés de configuration : Couvre les instantanés de configuration dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Édition de formulaire de schéma : Couvre l'édition de formulaire de schéma dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Édition JSON brute : Couvre l'édition JSON brute dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Écritures gardées par hachage de base : Couvre les écritures gardées par hachage de base dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.
- Appliquer et redémarrer : Couvre l'application et le redémarrage dans `config.get`, `config.set`, `config.apply`, `config.patch` et le comportement d'édition de schéma de configuration et d'écritures sûres associés.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs : Les tests du serveur couvrent les méthodes de configuration, les modifications d'authentification partagée, la validation, les résultats d'écriture de redémarrage, le hachage de base et les assistants d'écriture de configuration ; les tests d'interface utilisateur couvrent les contrôleurs de configuration, le rendu de formulaire, la recherche, le comportement de formulaire du navigateur, les présets, la configuration rapide et le style.
- Signaux négatifs : L'édition de configuration complète s'étend sur les schémas de plugin/canal, les SecretRefs, le JSON5 brut, la politique de redémarrage/rechargement et les sessions de navigateur distant. La preuve d'interface utilisateur de bout en bout pour chaque branche de schéma et champ appartenant au plugin est nécessairement partielle.
- Lacunes d'intégration : Ajouter une preuve de scénario de navigateur pour l'aller-retour brut, les modifications en mode formulaire avec secrets expurgés, le rejet de SecretRef, les champs de schéma de plugin/canal, l'inadéquation du hachage de base d'édition simultanée et le suivi du redémarrage de config.apply.

## Score de Qualité

- Score : `Beta (78%)`
- Rapports Gitcrawl : La requête de configuration a retourné #39780 pour appliquer les suggestions de renforcement de configuration via l'interface utilisateur, #59330 pour le mode brut désactivé par régression d'aller-retour, et les PR #59336 et #76034 pour la réparation du mode brut et l'UX de champ/lien de documentation basique/avancé.
- Rapports Discrawl : La requête de configuration exacte n'a retourné aucune ligne, mais le trafic d'archive du panneau d'opérateur inclut la confusion des utilisateurs autour de la forme de configuration exec élevée et des effets de redémarrage.
- Bonnes qualités : La conception utilise des instantanés source, la restauration d'expurgation, la coercition pilotée par schéma, les gardes de hachage de base, le mode brut de secours sûr, les sentinelles de redémarrage et les RPC délimitées.
- Mauvaises qualités : La configuration est une surface d'administrateur à fort impact ; les petits bugs de schéma, d'expurgation ou de plan de rechargement peuvent casser l'authentification de la passerelle ou les permissions d'opérateur de manière que les utilisateurs expérimentent via WebChat.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel affectent uniquement la couverture.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-control-ui-and-webchat.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les instantanés de configuration, l'édition de formulaire de schéma, l'édition JSON brute, les écritures gardées par hachage de base, l'application et le redémarrage.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Les suggestions de renforcement de configuration demandent toujours une meilleure UX d'application avec diff.
- Le mode brut et le mode formulaire ont besoin de preuves récurrentes par rapport à la dérive des schémas de plugin et des valeurs par défaut d'exécution.
- Les résultats de redémarrage et de rechargement à chaud ont besoin d'un statut plus clair face à l'utilisateur dans le même flux qui a enregistré la configuration.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md` documente config get/set/apply, validation, rendu de schéma/formulaire, contraintes d'éditeur JSON brut, garde de hachage de base, vérification préalable de SecretRef et comportement de réinitialisation brute.
- `/Users/kevinlin/code/openclaw/docs/gateway/configuration.md` et `/Users/kevinlin/code/openclaw/docs/gateway/configuration-reference.md` documentent le modèle de configuration sous-jacent.

### Source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/config.ts` implémente les RPC de configuration, le chargement de schéma, l'analyse/validation brute, les vérifications de hachage de base, la restauration d'expurgation et les commandes d'ouverture de configuration.
- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/config-write-flow.ts` valide les écritures de configuration, planifie les redémarrages, gère les modifications d'authentification partagée et écrit les sentinelles de redémarrage.
- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/config.ts` charge les instantanés/schémas, sérialise les éditions de formulaire/brutes, coerce les valeurs de schéma, supprime les anciens espaces réservés expurgés et soumet les hachages de base.
- `/Users/kevinlin/code/openclaw/ui/src/ui/views/config-form.render.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/config-form.node.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/views/config.ts` rendent l'éditeur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/config.test.ts`, `/Users/kevinlin/code/openclaw/src/gateway/server-methods/config.shared-auth.test.ts` et `/Users/kevinlin/code/openclaw/src/gateway/runtime-plugin-config.test.ts` couvrent le comportement de configuration de la passerelle.
- `/Users/kevinlin/code/openclaw/src/secrets/runtime.gateway-auth.integration.test.ts` couvre le comportement du secret d'exécution lié à l'authentification.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/ui/src/ui/controllers/config.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/config-form.search.node.test.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/config-form.node.ts`, `/Users/kevinlin/code/openclaw/ui/src/ui/views/config.browser.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/ui/config-form.browser.test.ts` couvrent le comportement de l'éditeur de configuration du navigateur.
- `/Users/kevinlin/code/openclaw/ui/src/styles/config.test.ts` et `/Users/kevinlin/code/openclaw/ui/src/styles/config-quick.test.ts` couvrent les contrats de style d'interface utilisateur de configuration.

### Requêtes Gitcrawl

Requête : `gitcrawl --json search issues -R openclaw/openclaw "config form Control UI"`

Résultats :

- A retourné l'ouverture #39780, `Control UI: Config upgrade/hardening suggestions should apply changes automatically with before/after diff and user acceptance, not direct users to edit files manually`.
- A retourné l'ouverture #59330, `Control UI Raw mode permanently disabled since 2026.3.31`.
- A retourné les problèmes de configuration/fournisseur adjacents #81961, #74310, #74395 et #65345.

Requête : `gitcrawl --json search prs -R openclaw/openclaw "config form Control UI"`

Résultats :

- A retourné la PR ouverte #59336, `fix: Config Raw mode permanently disabled due to round-trip check regression`.
- A retourné la PR ouverte #76034, `feat(config-ui): add basic/advanced field split and doc-link affordance`.
- A retourné les PR de localisation et de configuration adjacente #81743, #82514 et #58333.

### Requêtes Discrawl

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI config schema config apply secret ref raw json form"`

Résultats :

- N'a retourné aucune ligne.

Requête : `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Control UI channels sessions cron skills nodes exec approvals"`

Résultats :

- A trouvé une transcription WebChat utilisateur où la mauvaise forme de configuration pour exec élevé a dû être corrigée et le redémarrage n'a toujours pas immédiatement accordé la capacité de session actuelle.
