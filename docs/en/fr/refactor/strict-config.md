---
summary: "Validation stricte de la config + migrations réservées au doctor"
read_when:
  - Concevoir ou implémenter le comportement de validation de la config
  - Travailler sur les migrations de config ou les workflows doctor
  - Gérer les schémas de config de plugin ou le gating de chargement de plugin
title: "Validation stricte de la config"
---

# Validation stricte de la config (migrations réservées au doctor)

## Objectifs

- **Rejeter les clés de config inconnues partout** (racine + imbriquées), sauf les métadonnées `$schema` à la racine.
- **Rejeter la config de plugin sans schéma** ; ne pas charger ce plugin.
- **Supprimer la migration automatique héritée au chargement** ; les migrations s'exécutent via doctor uniquement.
- **Exécuter automatiquement doctor (dry-run) au démarrage** ; si invalide, bloquer les commandes non-diagnostiques.

## Non-objectifs

- Compatibilité rétroactive au chargement (les clés héritées ne migrent pas automatiquement).
- Suppression silencieuse des clés non reconnues.

## Règles de validation stricte

- La config doit correspondre exactement au schéma à chaque niveau.
- Les clés inconnues sont des erreurs de validation (pas de passthrough à la racine ou imbriquées), sauf `$schema` à la racine quand c'est une chaîne.
- `plugins.entries.<id>.config` doit être validée par le schéma du plugin.
  - Si un plugin n'a pas de schéma, **rejeter le chargement du plugin** et afficher une erreur claire.
- Les clés `channels.<id>` inconnues sont des erreurs sauf si un manifeste de plugin déclare l'id du canal.
- Les manifestes de plugin (`openclaw.plugin.json`) sont obligatoires pour tous les plugins.

## Application du schéma de plugin

- Chaque plugin fournit un schéma JSON strict pour sa config (intégré dans le manifeste).
- Flux de chargement du plugin :
  1. Résoudre le manifeste + schéma du plugin (`openclaw.plugin.json`).
  2. Valider la config par rapport au schéma.
  3. Si schéma manquant ou config invalide : bloquer le chargement du plugin, enregistrer l'erreur.
- Le message d'erreur inclut :
  - L'id du plugin
  - La raison (schéma manquant / config invalide)
  - Le(s) chemin(s) qui ont échoué la validation
- Les plugins désactivés conservent leur config, mais Doctor + les logs affichent un avertissement.

## Flux Doctor

- Doctor s'exécute **à chaque fois** que la config est chargée (dry-run par défaut).
- Si config invalide :
  - Afficher un résumé + erreurs exploitables.
  - Instruire : `openclaw doctor --fix`.
- `openclaw doctor --fix` :
  - Applique les migrations.
  - Supprime les clés inconnues.
  - Écrit la config mise à jour.

## Gating de commande (quand la config est invalide)

Autorisé (diagnostique uniquement) :

- `openclaw doctor`
- `openclaw logs`
- `openclaw health`
- `openclaw help`
- `openclaw status`
- `openclaw gateway status`

Tout le reste doit échouer avec : "Config invalide. Exécutez `openclaw doctor --fix`."

## Format UX d'erreur

- En-tête de résumé unique.
- Sections groupées :
  - Clés inconnues (chemins complets)
  - Clés héritées / migrations nécessaires
  - Échecs de chargement de plugin (id du plugin + raison + chemin)

## Points de contact d'implémentation

- `src/config/zod-schema.ts` : supprimer le passthrough à la racine ; objets stricts partout.
- `src/config/zod-schema.providers.ts` : assurer des schémas de canal stricts.
- `src/config/validation.ts` : échouer sur les clés inconnues ; ne pas appliquer les migrations héritées.
- `src/config/io.ts` : supprimer les migrations automatiques héritées ; toujours exécuter doctor dry-run.
- `src/config/legacy*.ts` : déplacer l'utilisation vers doctor uniquement.
- `src/plugins/*` : ajouter le registre de schéma + gating.
- Gating de commande CLI dans `src/cli`.

## Tests

- Rejet de clé inconnue (racine + imbriquée).
- Plugin sans schéma → chargement du plugin bloqué avec erreur claire.
- Config invalide → démarrage de la gateway bloqué sauf commandes diagnostiques.
- Doctor dry-run automatique ; `doctor --fix` écrit la config corrigée.
