---
summary: "Manifeste de plugin + exigences du schéma JSON (validation stricte de la configuration)"
read_when:
  - You are building a OpenClaw plugin
  - You need to ship a plugin config schema or debug plugin validation errors
title: "Plugin Manifest"
---

# Manifeste de plugin (openclaw.plugin.json)

Chaque plugin **doit** inclure un fichier `openclaw.plugin.json` à la **racine du plugin**.
OpenClaw utilise ce manifeste pour valider la configuration **sans exécuter le code du plugin**.
Les manifestes manquants ou invalides sont traités comme des erreurs de plugin et bloquent la validation de la configuration.

Consultez le guide complet du système de plugins : [Plugins](/tools/plugin).

## Champs obligatoires

```json
{
  "id": "voice-call",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

Clés obligatoires :

- `id` (string) : identifiant canonique du plugin.
- `configSchema` (object) : schéma JSON pour la configuration du plugin (en ligne).

Clés optionnelles :

- `kind` (string) : type de plugin (exemples : `"memory"`, `"context-engine"`).
- `channels` (array) : identifiants de canal enregistrés par ce plugin (exemple : `["matrix"]`).
- `providers` (array) : identifiants de fournisseur enregistrés par ce plugin.
- `skills` (array) : répertoires de compétences à charger (relatifs à la racine du plugin).
- `name` (string) : nom d'affichage du plugin.
- `description` (string) : résumé court du plugin.
- `uiHints` (object) : étiquettes de champ de configuration/espaces réservés/drapeaux sensibles pour le rendu de l'interface utilisateur.
- `version` (string) : version du plugin (informatif).

## Exigences du schéma JSON

- **Chaque plugin doit inclure un schéma JSON**, même s'il n'accepte aucune configuration.
- Un schéma vide est acceptable (par exemple, `{ "type": "object", "additionalProperties": false }`).
- Les schémas sont validés à la lecture/écriture de la configuration, pas à l'exécution.

## Comportement de validation

- Les clés `channels.*` inconnues sont des **erreurs**, sauf si l'identifiant de canal est déclaré par un manifeste de plugin.
- `plugins.entries.<id>`, `plugins.allow`, `plugins.deny` et `plugins.slots.*` doivent référencer des identifiants de plugin **découvrables**. Les identifiants inconnus sont des **erreurs**.
- Si un plugin est installé mais a un manifeste ou un schéma cassé ou manquant, la validation échoue et Doctor signale l'erreur du plugin.
- Si la configuration du plugin existe mais que le plugin est **désactivé**, la configuration est conservée et un **avertissement** est affiché dans Doctor + les journaux.

## Notes

- Le manifeste est **obligatoire pour tous les plugins**, y compris les chargements du système de fichiers local.
- L'exécution charge toujours le module du plugin séparément ; le manifeste est uniquement pour la découverte + validation.
- Les types de plugin exclusifs sont sélectionnés via `plugins.slots.*`.
  - `kind: "memory"` est sélectionné par `plugins.slots.memory`.
  - `kind: "context-engine"` est sélectionné par `plugins.slots.contextEngine` (par défaut : `legacy` intégré).
- Si votre plugin dépend de modules natifs, documentez les étapes de construction et toute exigence de liste d'autorisation du gestionnaire de paquets (par exemple, pnpm `allow-build-scripts` - `pnpm rebuild <package>`).
