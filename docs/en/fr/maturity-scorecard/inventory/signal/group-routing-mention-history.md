---
title: "Signal - Conversation Routing and Delivery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Signal - Conversation Routing and Delivery Maturity Note

## Résumé

Cette note migre les preuves de maturité archivées pour `Signal` / `Group Routing, Mentions, and Pending History` dans l'inventaire actuel de la fiche d'évaluation process-version-3.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Conversation Routing and Delivery`
- Fusionnée à partir de : `Conversation Access and Routing`, `Message Delivery and Actions`
- Report du score : minimum conservateur des scores des catégories sources fusionnées.

## Portée de la catégorie

Inclus dans cette catégorie :

- Appairage DM : Définit la configuration de l'appairage DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le contrôle d'accès et l'appairage DM.
- Listes blanches DM : Définit la configuration des listes blanches DM, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le contrôle d'accès et l'appairage DM.
- Normalisation de l'identité de l'expéditeur : Définit la configuration de la normalisation de l'identité de l'expéditeur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le contrôle d'accès et l'appairage DM.
- Listes blanches de groupe : Définit l'autorisation des listes blanches de groupe, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le routage de groupe, les mentions et l'historique en attente.
- Portes de mention : Définit l'autorisation des portes de mention, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le routage de groupe, les mentions et l'historique en attente.
- Historique de groupe en attente : Définit l'autorisation de l'historique de groupe en attente, les limites de confiance et de sécurité, et les contrôles de l'opérateur pour le routage de groupe, les mentions et l'historique en attente.
- Cibles de livraison de texte : Couvre le routage des cibles de livraison de texte, la liaison de session, l'historique et le contexte de conversation pour la livraison sortante, les médias, les reçus et la saisie.
- Livraison de médias et limites : Couvre le routage de la livraison de médias et des limites, la liaison de session, l'historique et le contexte de conversation pour la livraison sortante, les médias, les reçus et la saisie.
- Saisie et reçus de lecture : Couvre le routage de la saisie et des reçus de lecture, la liaison de session, l'historique et le contexte de conversation pour la livraison sortante, les médias, les reçus et la saisie.
- Sortie stylisée/fragmentée : Couvre le routage de la sortie stylisée/fragmentée, la liaison de session, l'historique et le contexte de conversation pour la livraison sortante, les médias, les reçus et la saisie.
- Découverte d'action de réaction : Couvre le routage de la découverte d'action de réaction, la liaison de session, l'historique et le contexte de conversation pour l'outil de message de réactions.
- Ajouter/supprimer des réactions : Couvre le routage de l'ajout/suppression de réactions, la liaison de session, l'historique et le contexte de conversation pour l'outil de message de réactions.
- Ciblage de réaction de groupe : Couvre le routage du ciblage de réaction de groupe, la liaison de session, l'historique et le contexte de conversation pour l'outil de message de réactions.

## Fonctionnalités

- Conversation Routing and Delivery : Portée des preuves pour Conversation Routing and Delivery.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (70%)`

La couverture est Beta car la documentation, la source, les tests de contrat et les tests unitaires couvrent les portes de groupe, les mentions et l'historique en attente, mais aucune transcription de routage de groupe en direct n'a été trouvée.

## Score de qualité

- Score : `Alpha (66%)`

La qualité est Alpha car le modèle de groupe est configurable mais l'historique de l'opérateur montre que les valeurs par défaut et la correspondance de l'expéditeur sont difficiles à raisonner dans les vrais groupes. Exclus de la qualité : les preuves de test unitaire, d'intégration, e2e, en direct et de flux d'exécution ; celles-ci affectent uniquement la couverture.

## Score de complétude

- Score : `Beta (70%)`
- Instructions de surface : évaluées par rapport à `references/completeness/signal.md`.
- Signaux positifs : la documentation archivée, la source, le test, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Conversation Routing and Delivery.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Voir les signaux négatifs spécifiques au score et les preuves archivées ci-dessous.

## Preuves

### Documentation

- `docs/channels/signal.md` lignes 254-261 documentent `groupPolicy`, `groupAllowFrom`, les remplacements par groupe, `groupMentionAliases` et `requireMention`.
- `docs/channels/signal.md` lignes 263-268 expliquent les enveloppes entrantes normalisées et le comportement de route-back.
- `docs/channels/signal.md` lignes 270-278 documentent les limites de médias, d'historique et de capture pertinentes au contexte de groupe.

### Source

- `extensions/signal/src/monitor/access-policy.ts` applique les listes blanches de groupe, les ID de groupe, le comportement de secours et les calculs de liste blanche de groupe effectifs.
- `extensions/signal/src/monitor/event-handler.ts` résout les ID de groupe, gère les blocs d'accès de groupe, évalue la politique de mention, stocke l'historique en attente pour les messages ignorés et ingère le contexte de hook interne lorsqu'il est configuré.
- `extensions/signal/src/identity.ts` distingue les ID de groupe des expéditeurs directs afin que les ID de groupe ne satisfassent pas les listes blanches directes.
- `extensions/signal/src/types.ts` porte les types de groupe Signal et d'enveloppe de message utilisés par le chemin du moniteur.

### Tests d'intégration

- `extensions/signal/src/inbound-context.contract.test.ts` valide les clés de session de groupe et les champs de contexte Signal.
- Aucun routage de groupe en direct, mention de groupe ou exécution d'historique de groupe n'a été trouvé dans `qa/`, `test/` ou `tests`.

### Tests unitaires

- `extensions/signal/src/monitor/access-policy.test.ts` couvre les formes de liste blanche de groupe, le blocage de non-correspondance, le secours `allowFrom`, les ID de groupe ne satisfaisant pas les listes blanches directes, les groupes d'accès et les listes blanches de groupe effectifs.
- `extensions/signal/src/monitor/event-handler.mention-gating.test.ts` couvre les décisions de suppression/autorisation autour des mentions, les groupes sans mention requise, les ID de groupe configurés, l'historique en attente et le contournement de commande de contrôle.
- `extensions/signal/src/monitor/event-handler.inbound-context.test.ts` couvre l'historique de groupe en attente structuré par rapport au texte actuel.

### Requêtes Gitcrawl

- Requête : `Signal groupAllowFrom requireMention`
  - Résultats : la recherche d'archive a retourné les problèmes de politique de groupe et de portage de mention, y compris le problème `#53308`.
- Requête : `Signal groupAllowFrom sender mismatch requireMention default`
  - Résultats : le problème `#53308` signale la non-correspondance de l'expéditeur de la liste blanche de groupe et le comportement par défaut de `requireMention` rendant l'intégration de groupe non fonctionnelle.

### Requêtes Discrawl

- Requête : `Signal groupAllowFrom requireMention`
  - Résultats : les messages d'assistance des 20 et 21 avril 2026 expliquent `groupPolicy`, `groupAllowFrom`, `groups.<id>.requireMention`, les alias et le comportement de mention par défaut.
- Requête : `Signal groupAllowFrom sender mismatch requireMention default`
  - Résultats : le contenu du miroir GitHub Discord pour le problème `#53308` a répété le rapport de non-correspondance de l'expéditeur et de mention par défaut.
