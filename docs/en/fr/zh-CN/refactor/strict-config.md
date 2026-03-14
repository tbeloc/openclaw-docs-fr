---
read_when:
  - Concevoir ou implémenter un comportement de validation de configuration
  - Gérer les migrations de configuration ou les flux de travail doctor
  - Gérer le schéma de configuration des plugins ou les contrôles de chargement des plugins
summary: Validation stricte de la configuration + migration uniquement via doctor
title: Validation stricte de la configuration
x-i18n:
  generated_at: "2026-02-03T10:08:51Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 5bc7174a67d2234e763f21330d8fe3afebc23b2e5c728a04abcc648b453a91cc
  source_path: refactor/strict-config.md
  workflow: 15
---

# Validation stricte de la configuration (migration uniquement via doctor)

## Objectifs

- **Rejeter les clés de configuration inconnues partout** (racine + imbriquées).
- **Rejeter la configuration des plugins sans schéma** ; ne pas charger le plugin.
- **Supprimer les migrations automatiques héritées au chargement** ; les migrations se font uniquement via doctor.
- **Exécuter automatiquement doctor (dry-run) au démarrage** ; bloquer les commandes non diagnostiques si invalide.

## Non-objectifs

- Compatibilité rétroactive au chargement (les anciennes clés ne seront pas migrées automatiquement).
- Suppression silencieuse des clés non reconnues.

## Règles de validation stricte

- La configuration doit correspondre exactement au schéma à chaque niveau.
- Les clés inconnues sont des erreurs de validation (aucun pass-through autorisé à la racine ou imbriquées).
- `plugins.entries.<id>.config` doit être validé par le schéma du plugin.
  - Si le plugin n'a pas de schéma, **rejeter le chargement du plugin** avec une erreur claire.
- Les clés `channels.<id>` inconnues sont une erreur, sauf si le manifeste du plugin déclare cet id de canal.
- Tous les plugins nécessitent un manifeste de plugin (`openclaw.plugin.json`).

## Application du schéma des plugins

- Chaque plugin fournit un schéma JSON strict pour sa configuration (intégré dans le manifeste).
- Flux de chargement des plugins :
  1. Analyser le manifeste du plugin + schéma (`openclaw.plugin.json`).
  2. Valider la configuration par rapport au schéma.
  3. Si le schéma est manquant ou la configuration invalide : bloquer le chargement du plugin, enregistrer l'erreur.
- Les messages d'erreur incluent :
  - L'id du plugin
  - La raison (schéma manquant / configuration invalide)
  - Le chemin où la validation a échoué
- Les plugins désactivés conservent leur configuration, mais Doctor + les journaux affichent un avertissement.

## Flux Doctor

- Doctor s'exécute à chaque chargement de configuration (dry-run par défaut).
- Si la configuration est invalide :
  - Afficher un résumé + des erreurs exploitables.
  - Indiquer : `openclaw doctor --fix`.
- `openclaw doctor --fix` :
  - Appliquer les migrations.
  - Supprimer les clés inconnues.
  - Écrire la configuration mise à jour.

## Contrôle des commandes (quand la configuration est invalide)

Commandes autorisées (diagnostiques uniquement) :

- `openclaw doctor`
- `openclaw logs`
- `openclaw health`
- `openclaw help`
- `openclaw status`
- `openclaw gateway status`

Toutes les autres commandes doivent échouer avec le message : « Config invalid. Run `openclaw doctor --fix`. »

## Format d'expérience utilisateur des erreurs

- Un titre de résumé unique.
- Sections groupées :
  - Clés inconnues (chemin complet)
  - Clés héritées / nécessitant une migration
  - Échecs de chargement des plugins (id du plugin + raison + chemin)

## Points de contact d'implémentation

- `src/config/zod-schema.ts` : supprimer le pass-through au niveau racine ; utiliser des objets stricts partout.
- `src/config/zod-schema.providers.ts` : assurer un schéma de canaux strict.
- `src/config/validation.ts` : échouer sur les clés inconnues ; ne pas appliquer les migrations héritées.
- `src/config/io.ts` : supprimer les migrations automatiques héritées ; toujours exécuter doctor dry-run.
- `src/config/legacy*.ts` : déplacer l'utilisation vers doctor uniquement.
- `src/plugins/*` : ajouter un registre de schéma + contrôle.
- Contrôle des commandes CLI dans `src/cli`.

## Tests

- Rejet des clés inconnues (racine + imbriquées).
- Plugin sans schéma → chargement du plugin bloqué avec erreur claire.
- Configuration invalide → démarrage de la passerelle bloqué, sauf pour les commandes diagnostiques.
- Doctor dry-run s'exécute automatiquement ; `doctor --fix` écrit la configuration corrigée.
