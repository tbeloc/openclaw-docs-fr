---
read_when:
  - 你正在构建一个 OpenClaw 插件
  - 你需要提供插件配置 Schema 或调试插件验证错误
summary: 插件清单及 JSON Schema 要求（严格配置验证）
title: 插件清单
x-i18n:
  generated_at: "2026-02-01T21:34:21Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 47b3e33c915f47bdd172ae0316af7ef16ca831c317e3f1a7fdfcd67e3bd43f56
  source_path: plugins/manifest.md
  workflow: 15
---

# Manifeste du plugin (openclaw.plugin.json)

Chaque plugin **doit** fournir un fichier `openclaw.plugin.json` dans la **racine du plugin**. OpenClaw utilise ce manifeste pour **valider la configuration sans exécuter le code du plugin**. Un manifeste manquant ou invalide sera considéré comme une erreur de plugin et bloquera la validation de la configuration.

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

- `id` (chaîne) : l'identifiant canonique du plugin.
- `configSchema` (objet) : JSON Schema pour la configuration du plugin (forme en ligne).

Clés optionnelles :

- `kind` (chaîne) : type de plugin (par exemple : `"memory"`).
- `channels` (tableau) : identifiants des canaux enregistrés par ce plugin (par exemple : `["matrix"]`).
- `providers` (tableau) : identifiants des fournisseurs enregistrés par ce plugin.
- `skills` (tableau) : répertoires de Skills à charger (relatifs à la racine du plugin).
- `name` (chaîne) : nom d'affichage du plugin.
- `description` (chaîne) : description courte du plugin.
- `uiHints` (objet) : étiquettes/espaces réservés/drapeaux sensibles des champs de configuration pour le rendu de l'interface utilisateur.
- `version` (chaîne) : version du plugin (à titre informatif uniquement).

## Exigences du schéma JSON

- **Chaque plugin doit fournir un schéma JSON**, même s'il n'accepte aucune configuration.
- Un schéma vide est acceptable (par exemple `{ "type": "object", "additionalProperties": false }`).
- Le schéma est validé lors de la lecture/écriture de la configuration, non à l'exécution.

## Comportement de validation

- Les clés `channels.*` inconnues sont considérées comme une **erreur**, sauf si l'identifiant du canal a été déclaré dans le manifeste du plugin.
- `plugins.entries.<id>`, `plugins.allow`, `plugins.deny` et `plugins.slots.*` doivent référencer des identifiants de plugin **découvrables**. Les identifiants inconnus sont considérés comme une **erreur**.
- Si un plugin est installé mais que son manifeste ou son schéma est corrompu ou manquant, la validation échouera et Doctor signalera une erreur de plugin.
- Si une configuration de plugin existe mais que le plugin est **désactivé**, la configuration est conservée et un **avertissement** s'affiche dans Doctor et les journaux.

## Remarques

- Le manifeste est **requis pour tous les plugins**, y compris ceux chargés à partir du système de fichiers local.
- Le module du plugin est toujours chargé séparément à l'exécution ; le manifeste est utilisé uniquement pour la découverte et la validation.
- Si votre plugin dépend de modules natifs, documentez les étapes de construction et toutes les exigences de liste d'autorisation du gestionnaire de paquets (par exemple `allow-build-scripts` de pnpm - `pnpm rebuild <package>`).
