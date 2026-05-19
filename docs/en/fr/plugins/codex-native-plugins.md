---
summary: "Configurez les plugins Codex natifs migrés pour les agents OpenClaw en mode Codex"
title: "Plugins Codex natifs"
read_when:
  - You want Codex-mode OpenClaw agents to use native Codex plugins
  - You are migrating source-installed openai-curated Codex plugins
  - You are troubleshooting codexPlugins, app inventory, destructive actions, or plugin app diagnostics
---

La prise en charge des plugins Codex natifs permet à un agent OpenClaw en mode Codex d'utiliser les capacités d'application et de plugin du serveur d'application Codex dans le même thread Codex qui gère le tour OpenClaw.

OpenClaw ne traduit pas les plugins Codex en outils dynamiques OpenClaw synthétiques `codex_plugin_*`. Les appels de plugin restent dans la transcription Codex native, et le serveur d'application Codex possède l'exécution MCP soutenue par l'application.

Utilisez cette page après que le [harnais Codex](/fr/plugins/codex-harness) de base fonctionne.

## Exigences

- Le runtime d'agent OpenClaw sélectionné doit être le harnais Codex natif.
- `plugins.entries.codex.enabled` doit être true.
- `plugins.entries.codex.config.codexPlugins.enabled` doit être true.
- V1 ne supporte que les plugins `openai-curated` que la migration a observés comme installés à partir de la source dans le répertoire Codex source.
- Le serveur d'application Codex cible doit pouvoir voir l'inventaire attendu du marketplace, du plugin et de l'application.

`codexPlugins` n'a aucun effet sur les exécutions PI, les exécutions normales du fournisseur OpenAI, les liaisons de conversation ACP ou d'autres harnais car ces chemins ne créent pas de threads de serveur d'application Codex avec la configuration native `apps`.

## Démarrage rapide

Prévisualisez la migration à partir du répertoire Codex source :

```bash
openclaw migrate codex --dry-run
```

Utilisez la vérification stricte de l'application source lorsque vous souhaitez que la migration vérifie l'accessibilité de l'application source avant de planifier l'activation du plugin natif :

```bash
openclaw migrate codex --dry-run --verify-plugin-apps
```

Appliquez la migration lorsque le plan semble correct :

```bash
openclaw migrate apply codex --yes
```

La migration écrit des entrées `codexPlugins` explicites pour les plugins éligibles et appelle `plugin/install` du serveur d'application Codex pour les plugins sélectionnés. Une configuration migrée typique ressemble à ceci :

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          codexPlugins: {
            enabled: true,
            allow_destructive_actions: true,
            plugins: {
              "google-calendar": {
                enabled: true,
                marketplaceName: "openai-curated",
                pluginName: "google-calendar",
              },
            },
          },
        },
      },
    },
  },
}
```

Après avoir modifié `codexPlugins`, utilisez `/new`, `/reset` ou redémarrez la passerelle pour que les futures sessions du harnais Codex commencent avec l'ensemble d'applications mis à jour.

## Comment fonctionne la configuration du plugin natif

L'intégration a trois états distincts :

- Installé : Codex a le bundle de plugin local dans le runtime du serveur d'application cible.
- Activé : la configuration OpenClaw est disposée à mettre le plugin à disposition des tours du harnais Codex.
- Accessible : le serveur d'application Codex confirme que les entrées d'application du plugin sont disponibles pour le compte actif et peuvent être mappées à l'identité du plugin migré.

La migration est l'étape d'installation/d'éligibilité durable. Pendant la planification, OpenClaw lit les détails `plugin/read` du Codex source et vérifie que la réponse du compte du serveur d'application Codex source est un compte d'abonnement ChatGPT. Les réponses de compte non-ChatGPT ou manquantes ignorent les plugins soutenus par l'application avec `codex_subscription_required`. Par défaut, la migration n'appelle pas `app/list` source ; les plugins source soutenus par l'application qui passent la porte du compte sont planifiés sans vérification d'accessibilité de l'application source, et les défaillances de transport de recherche de compte ignorent avec `codex_account_unavailable`. Avec `--verify-plugin-apps`, la migration prend un snapshot `app/list` source frais et exige que chaque application possédée soit présente, activée et accessible avant de planifier l'activation native. Dans ce mode, les défaillances de transport de recherche de compte passent par la porte d'inventaire d'application source. L'inventaire d'application runtime est la vérification d'accessibilité de session cible après la migration. La configuration de l'application du thread du harnais Codex calcule ensuite une configuration d'application de thread restrictive pour les applications de plugin activées et accessibles.

La configuration de l'application du thread est calculée lorsque OpenClaw établit une session du harnais Codex ou remplace une liaison de thread Codex obsolète. Elle n'est pas recalculée à chaque tour.

## Limite de support V1

V1 est intentionnellement étroite :

- Seuls les plugins `openai-curated` qui étaient déjà installés dans l'inventaire du serveur d'application Codex source sont éligibles à la migration.
- Les plugins source soutenus par l'application doivent passer la porte d'abonnement au moment de la migration. `--verify-plugin-apps` ajoute la porte d'inventaire d'application source. Les comptes à porte d'abonnement plus, en mode de vérification, les applications source inaccessibles, désactivées, manquantes ou les défaillances d'actualisation d'inventaire d'application source sont signalés comme éléments manuels ignorés au lieu d'entrées de configuration activées. Les détails de plugin illisibles sont ignorés avant la porte d'inventaire d'application source.
- La migration écrit des identités de plugin explicites avec `marketplaceName` et `pluginName` ; elle n'écrit pas les chemins de cache `marketplacePath` locaux.
- `codexPlugins.enabled` est le commutateur d'activation global.
- Il n'y a pas de caractère générique `plugins["*"]` et aucune clé de configuration qui accorde une autorité d'installation arbitraire.
- Les marketplaces non supportées, les bundles de plugin en cache, les hooks et les fichiers de configuration Codex sont préservés dans le rapport de migration pour examen manuel.

## Inventaire d'application et propriété

OpenClaw lit l'inventaire d'application Codex via `app/list` du serveur d'application, le met en cache pendant une heure et actualise les entrées obsolètes ou manquantes de manière asynchrone. Le cache est en mémoire uniquement ; redémarrer l'interface de ligne de commande ou la passerelle le supprime, et OpenClaw le reconstruit à partir de la prochaine lecture `app/list`.

La migration et le runtime utilisent des clés de cache distinctes :

- La vérification de migration source utilise le répertoire Codex source et les options de démarrage du serveur d'application source. Cela s'exécute uniquement lorsque `--verify-plugin-apps` est défini, et il force une traversée `app/list` source fraîche pour cette exécution de planification.
- La configuration du runtime cible utilise l'identité du serveur d'application Codex de l'agent cible lorsqu'elle construit la configuration de l'application du thread Codex. L'activation du plugin invalide cette clé de cache cible, puis la force-actualise après `plugin/install`.

Une application de plugin n'est exposée que lorsque OpenClaw peut la mapper au plugin migré via la propriété stable :

- ID d'application exact à partir du détail du plugin
- Nom du serveur MCP connu
- Métadonnées stables uniques

La propriété par nom d'affichage uniquement ou ambiguë est exclue jusqu'à ce que la prochaine actualisation d'inventaire prouve la propriété.

## Configuration de l'application du thread

OpenClaw injecte un patch `config.apps` restrictif pour le thread Codex : `_default` est désactivé et seules les applications possédées par les plugins migrés activés sont activées.

OpenClaw définit `destructive_enabled` au niveau de l'application à partir de la politique `allow_destructive_actions` globale ou par plugin effective et laisse Codex appliquer les métadonnées d'outil destructif à partir de ses annotations d'outil d'application natives. La configuration de l'application `_default` est désactivée avec `open_world_enabled: false`. Les applications de plugin activées sont émises avec `open_world_enabled: true` ; OpenClaw n'expose pas un bouton de politique open-world distinct par plugin et ne maintient pas de listes de refus de noms d'outils destructifs par plugin.

Le mode d'approbation d'outil est automatique par défaut pour les applications de plugin afin que les outils de lecture non destructifs puissent s'exécuter sans une interface utilisateur d'approbation du même thread. Les outils destructifs restent contrôlés par la politique `destructive_enabled` de chaque application.

## Politique d'action destructive

Les élicitations de plugin destructif sont autorisées par défaut pour les plugins Codex migrés, tandis que les schémas non sécurisés et la propriété ambiguë échouent toujours fermés :

- `allow_destructive_actions` global par défaut à `true`.
- `allow_destructive_actions` par plugin remplace la politique globale pour ce plugin.
- Lorsque la politique est `false`, OpenClaw retourne un refus déterministe.
- Lorsque la politique est `true`, OpenClaw accepte automatiquement uniquement les schémas sûrs qu'il peut mapper à une réponse d'approbation, comme un champ d'approbation booléen.
- L'identité de plugin manquante, la propriété ambiguë, un ID de tour manquant, un ID de tour incorrect ou un schéma d'élicitation non sécurisé refuse au lieu de demander.

## Dépannage

**`auth_required` :** la migration a installé le plugin, mais l'une de ses applications a toujours besoin d'authentification. L'entrée de plugin explicite est écrite désactivée jusqu'à ce que vous réautorisiez et l'activiez.

**`app_inaccessible`, `app_disabled` ou `app_missing` :**
la migration n'a pas installé le plugin car l'inventaire d'application Codex source n'a pas montré toutes les applications possédées comme présentes, activées et accessibles tandis que `--verify-plugin-apps` était défini. Réautorisez ou activez l'application dans Codex, puis réexécutez la migration avec `--verify-plugin-apps`.

**`app_inventory_unavailable` :** la migration n'a pas installé le plugin car la vérification stricte de l'application source a été demandée et l'actualisation de l'inventaire d'application Codex source a échoué. Corrigez l'accès au serveur d'application Codex source ou réessayez sans `--verify-plugin-apps` si vous acceptez le plan plus rapide à porte de compte.

**`codex_subscription_required` :** la migration n'a pas installé le plugin soutenu par l'application car le compte du serveur d'application Codex source n'était pas connecté avec un compte d'abonnement ChatGPT. Connectez-vous à l'application Codex avec l'authentification d'abonnement, puis réexécutez la migration.

**`codex_account_unavailable` :** la migration n'a pas installé le plugin soutenu par l'application car le compte du serveur d'application Codex source n'a pas pu être lu. Corrigez l'authentification du serveur d'application Codex source ou réexécutez avec `--verify-plugin-apps` si vous souhaitez que l'inventaire d'application source décide de l'éligibilité lorsque la recherche de compte échoue.

**`marketplace_missing` ou `plugin_missing` :** le serveur d'application Codex cible ne peut pas voir le marketplace `openai-curated` ou le plugin attendu. Réexécutez la migration par rapport au runtime cible ou inspectez l'état du plugin du serveur d'application Codex.

**`app_inventory_missing` ou `app_inventory_stale` :** la disponibilité de l'application provenait d'un cache vide ou obsolète. OpenClaw planifie une actualisation asynchrone et exclut les applications de plugin jusqu'à ce que la propriété et la disponibilité soient connues.

**`app_ownership_ambiguous` :** l'inventaire d'application ne correspondait que par nom d'affichage, donc l'application n'est pas exposée au thread Codex.

**La configuration a changé mais l'agent ne peut pas voir le plugin :** utilisez `/new`, `/reset` ou redémarrez la passerelle. Les liaisons de thread Codex existantes conservent la configuration d'application avec laquelle elles ont commencé jusqu'à ce qu'OpenClaw établisse une nouvelle session de harnais ou remplace une liaison obsolète.

**L'action destructive est refusée :** vérifiez les valeurs `allow_destructive_actions` globales et par plugin. Même lorsque la politique est true, les schémas d'élicitation non sécurisés et l'identité de plugin ambiguë échouent toujours fermés.

## Connexes

- [Harnais Codex](/fr/plugins/codex-harness)
- [Référence du harnais Codex](/fr/plugins/codex-harness-reference)
- [Runtime du harnais Codex](/fr/plugins/codex-harness-runtime)
- [Référence de configuration](/fr/gateway/configuration-reference#codex-harness-plugin-config)
- [CLI Migrate](/fr/cli/migrate)
