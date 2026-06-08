---
title: "Signal - Note de Maturité Accès et Identité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Note de Maturité Accès et Identité

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Contrôle d'Accès et Appairage DM` dans l'inventaire de scorecard actuel de la version-3 du processus.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Accès et Identité`
- Fusionnée depuis : `Accès aux Conversations et Routage`
- Report de score : minimum conservateur des scores de la catégorie source fusionnée.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Appairage DM : Définit la configuration d'appairage DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM.
- Listes blanches DM : Définit la configuration des listes blanches DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM.
- Normalisation de l'identité de l'expéditeur : Définit la configuration de normalisation de l'identité de l'expéditeur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM.
- Listes blanches de groupe : Définit l'autorisation des listes blanches de groupe, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.
- Portes de mention : Définit l'autorisation des portes de mention, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.
- Historique de groupe en attente : Définit l'autorisation de l'historique de groupe en attente, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.
- Appairage DM : Définit la configuration d'appairage DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM
- Listes blanches DM : Définit la configuration des listes blanches DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM
- Normalisation de l'identité de l'expéditeur : Définit la configuration de normalisation de l'identité de l'expéditeur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM
- Listes blanches de groupe : Définit l'autorisation des listes blanches de groupe, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente
- Portes de mention : Définit l'autorisation des portes de mention, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente
- Historique de groupe en attente : Définit l'autorisation de l'historique de groupe en attente, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente
- Cibles de livraison de texte : Couvre le routage des cibles de livraison de texte, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Accusés de Réception et la Saisie.
- Livraison de médias et limites : Couvre le routage de livraison de médias et limites, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Accusés de Réception et la Saisie.
- Saisie et accusés de lecture : Couvre le routage de saisie et accusés de lecture, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Accusés de Réception et la Saisie.
- Sortie stylisée/fragmentée : Couvre le routage de sortie stylisée/fragmentée, la liaison de session, l'historique et le contexte de conversation pour la Livraison Sortante, les Médias, les Accusés de Réception et la Saisie.
- Découverte d'action de réaction : Couvre le routage de découverte d'action de réaction, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.
- Ajouter/supprimer des réactions : Couvre le routage d'ajout/suppression de réactions, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.
- Ciblage de réaction de groupe : Couvre le routage de ciblage de réaction de groupe, la liaison de session, l'historique et le contexte de conversation pour l'Outil de Message de Réactions.

## Fonctionnalités

- Appairage DM : Définit la configuration d'appairage DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM.
- Listes blanches DM : Définit la configuration des listes blanches DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM.
- Normalisation de l'identité de l'expéditeur : Définit la configuration de normalisation de l'identité de l'expéditeur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Contrôle d'Accès et Appairage DM.
- Listes blanches de groupe : Définit l'autorisation des listes blanches de groupe, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.
- Portes de mention : Définit l'autorisation des portes de mention, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.
- Historique de groupe en attente : Définit l'autorisation de l'historique de groupe en attente, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le Routage de Groupe, les Mentions et l'Historique en Attente.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Bêta (72%)`

La couverture est Bêta car la documentation, la source et les tests unitaires couvrent l'appairage, les listes blanches et les formes d'identité sur les expéditeurs téléphone et UUID, mais la preuve d'appairage en direct est absente.

## Score de Qualité

- Score : `Bêta (70%)`

La qualité est Bêta car le modèle d'accès est explicite et soutenu par la source, mais l'historique de l'opérateur montre une confusion sur les listes blanches et un suivi ouvert sur la correspondance d'alias. Exclus de la qualité : les preuves de test unitaire, intégration, e2e, en direct et flux d'exécution ; celles-ci affectent uniquement la Couverture.

## Score de Complétude

- Score : `Bêta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs : la documentation archivée, la source, le test, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'appairage DM, les listes blanches DM, la normalisation de l'identité de l'expéditeur, les listes blanches de groupe, les portes de mention, l'historique de groupe en attente.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude de la version-3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `docs/channels/signal.md` lignes 30-54 documentent `dmPolicy`, `allowFrom` et la configuration d'appairage par défaut.
- `docs/channels/signal.md` lignes 74-79 documentent la normalisation des numéros et la protection contre les boucles automatiques.
- `docs/channels/signal.md` lignes 246-253 documentent le comportement d'appairage DM et d'accès.
- `docs/channels/signal.md` lignes 367-372 documentent les notes de sécurité pour les listes blanches et l'isolation des comptes.

### Source

- `extensions/signal/src/setup-core.ts` demande `allowFrom`, définit par défaut `dmPolicy` à l'appairage et stocke la politique de message direct par compte.
- `extensions/signal/src/identity.ts` résout les expéditeurs téléphone et UUID, formate les ID de pairs, analyse les entrées de liste blanche, supporte les valeurs de caractères génériques et normalise les alias UUID/téléphone.
- `extensions/signal/src/monitor/access-policy.ts` calcule l'état d'accès, applique les vérifications du magasin d'appairage, gère les réponses de défi d'appairage de message direct et construit des alias d'identité stables.
- `extensions/signal/src/monitor/event-handler.ts` filtre les messages de boucle automatique/synchronisation, résout l'accès au message direct, gère les réponses d'appairage et supprime les commandes de message direct non autorisées.

### Tests d'intégration

- `extensions/signal/src/inbound-context.contract.test.ts` vérifie les clés de contexte entrant Signal et les champs de fournisseur/surface.
- Aucune preuve d'appairage de message direct en direct n'a été trouvée dans `qa/`, `test/` ou `tests`.

### Tests unitaires

- `extensions/signal/src/monitor/access-policy.test.ts` couvre les groupes d'accès, les expéditeurs directs du magasin d'appairage, le blocage de non-correspondance de groupe du magasin d'appairage, le flux de code de défi d'appairage de message direct et les portes de commande de contrôle.
- `extensions/signal/src/monitor.tool-result.pairs-uuid-only-senders-uuid-allowlist-entry.test.ts` couvre l'appairage d'expéditeur UUID uniquement et la gestion des entrées de liste blanche UUID.
- `extensions/signal/src/core.test.ts` couvre l'analyse de configuration pour les entrées de liste blanche UUID et caractères génériques.
- `extensions/signal/src/monitor/event-handler.inbound-context.test.ts` couvre les messages directs autorisés, les accusés de lecture et la suppression des commandes de message direct en mode ouvert sans listes blanches.

### Requêtes Gitcrawl

- Requête : `Signal allowlist uuid e164 alias`
  - Résultats : la PR ouverte `#78022` propose la correspondance des listes blanches sur les alias UUID ou E.164.
- Requête : `Signal dmPolicy pairing allowFrom uuid`
  - Résultats : les résultats plus larges montrent les discussions d'appairage et de liste blanche mais aucun enregistrement de réussite de bout en bout en direct.

### Requêtes Discrawl

- Requête : `Signal dmPolicy pairing allowFrom uuid`
  - Résultats : la discussion d'assistance du 2026-02-25 et 2026-02-26 a conseillé de rester sur `dmPolicy: "pairing"` et a montré une confusion de l'opérateur autour de `allowFrom` et des expéditeurs UUID uniquement.
- Requête : `Signal allowlist uuid e164 alias`
  - Résultats : aucun résultat affiché n'a prouvé que le suivi de correspondance d'alias avait été déployé et exercé en direct.
