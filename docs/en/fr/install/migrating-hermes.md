---
summary: "Migrer de Hermes vers OpenClaw avec un import prévisualisé et réversible"
read_when:
  - You are coming from Hermes and want to keep your model config, prompts, memory, and skills
  - You want to know what OpenClaw imports automatically and what stays archive-only
  - You need a clean, scripted migration path (CI, fresh laptop, automation)
title: "Migration depuis Hermes"
---

OpenClaw importe l'état de Hermes via un fournisseur de migration intégré. Le fournisseur prévisualise tout avant de modifier l'état, masque les secrets dans les plans et rapports, et crée une sauvegarde vérifiée avant l'application.

<Note>
Les imports nécessitent une installation OpenClaw vierge. Si vous avez déjà un état OpenClaw local, réinitialisez d'abord la configuration, les identifiants, les sessions et l'espace de travail, ou utilisez `openclaw migrate` directement avec `--overwrite` après avoir examiné le plan.
</Note>

## Deux façons d'importer

<Tabs>
  <Tab title="Assistant d'intégration">
    Le chemin le plus rapide. L'assistant détecte Hermes à `~/.hermes` et affiche un aperçu avant l'application.

    ```bash
    openclaw onboard --flow import
    ```

    Ou pointez vers une source spécifique :

    ```bash
    openclaw onboard --import-from hermes --import-source ~/.hermes
    ```

  </Tab>
  <Tab title="CLI">
    Utilisez `openclaw migrate` pour les exécutions scriptées ou répétables. Consultez [`openclaw migrate`](/fr/cli/migrate) pour la référence complète.

    ```bash
    openclaw migrate hermes --dry-run    # aperçu uniquement
    openclaw migrate apply hermes --yes  # appliquer sans confirmation
    ```

    Ajoutez `--from <path>` quand Hermes se trouve en dehors de `~/.hermes`.

  </Tab>
</Tabs>

## Ce qui est importé

<AccordionGroup>
  <Accordion title="Configuration du modèle">
    - Sélection du modèle par défaut depuis `config.yaml` de Hermes.
    - Fournisseurs de modèles configurés et points de terminaison OpenAI compatibles personnalisés depuis `providers` et `custom_providers`.
  </Accordion>
  <Accordion title="Serveurs MCP">
    Définitions des serveurs MCP depuis `mcp_servers` ou `mcp.servers`.
  </Accordion>
  <Accordion title="Fichiers de l'espace de travail">
    - `SOUL.md` et `AGENTS.md` sont copiés dans l'espace de travail des agents OpenClaw.
    - `memories/MEMORY.md` et `memories/USER.md` sont **ajoutés** aux fichiers de mémoire OpenClaw correspondants au lieu de les remplacer.
  </Accordion>
  <Accordion title="Configuration de la mémoire">
    Paramètres par défaut de la configuration de mémoire pour la mémoire fichier OpenClaw. Les fournisseurs de mémoire externes tels que Honcho sont enregistrés comme éléments d'archive ou d'examen manuel afin que vous puissiez les déplacer délibérément.
  </Accordion>
  <Accordion title="Compétences">
    Les compétences avec un fichier `SKILL.md` sous `skills/<name>/` sont copiées, ainsi que les valeurs de configuration par compétence depuis `skills.config`.
  </Accordion>
  <Accordion title="Clés API (opt-in)">
    Définissez `--include-secrets` pour importer les clés `.env` supportées : `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`, `XAI_API_KEY`, `MISTRAL_API_KEY`, `DEEPSEEK_API_KEY`. Sans ce drapeau, les secrets ne sont jamais copiés.
  </Accordion>
</AccordionGroup>

## Ce qui reste en archive uniquement

Le fournisseur copie ces éléments dans le répertoire du rapport de migration pour examen manuel, mais ne les charge **pas** dans la configuration ou les identifiants OpenClaw actifs :

- `plugins/`
- `sessions/`
- `logs/`
- `cron/`
- `mcp-tokens/`
- `auth.json`
- `state.db`

OpenClaw refuse d'exécuter ou de faire confiance à cet état automatiquement car les formats et les hypothèses de confiance peuvent diverger entre les systèmes. Déplacez ce dont vous avez besoin manuellement après avoir examiné l'archive.

## Flux recommandé

<Steps>
  <Step title="Prévisualiser le plan">
    ```bash
    openclaw migrate hermes --dry-run
    ```

    Le plan énumère tout ce qui va changer, y compris les conflits, les éléments ignorés et tous les éléments sensibles. La sortie du plan masque les clés ressemblant à des secrets imbriquées.

  </Step>
  <Step title="Appliquer avec sauvegarde">
    ```bash
    openclaw migrate apply hermes --yes
    ```

    OpenClaw crée et vérifie une sauvegarde avant l'application. Si vous avez besoin d'importer des clés API, ajoutez `--include-secrets`.

  </Step>
  <Step title="Exécuter doctor">
    ```bash
    openclaw doctor
    ```

    [Doctor](/fr/gateway/doctor) réapplique toutes les migrations de configuration en attente et vérifie les problèmes introduits lors de l'import.

  </Step>
  <Step title="Redémarrer et vérifier">
    ```bash
    openclaw gateway restart
    openclaw status
    ```

    Confirmez que la passerelle est saine et que votre modèle importé, la mémoire et les compétences sont chargés.

  </Step>
</Steps>

## Gestion des conflits

L'application refuse de continuer quand le plan signale des conflits (un fichier ou une valeur de configuration existe déjà à la cible).

<Warning>
Réexécutez avec `--overwrite` uniquement quand le remplacement de la cible existante est intentionnel. Les fournisseurs peuvent toujours écrire des sauvegardes au niveau des éléments pour les fichiers remplacés dans le répertoire du rapport de migration.
</Warning>

Pour une installation OpenClaw vierge, les conflits sont inhabituels. Ils apparaissent généralement quand vous réexécutez l'import sur une configuration qui a déjà des modifications utilisateur.

Si un conflit apparaît au milieu de l'application (par exemple, une course inattendue sur un fichier de configuration), Hermes marque les éléments de configuration dépendants restants comme `skipped` avec la raison `blocked by earlier apply conflict` au lieu de les écrire partiellement. Le rapport de migration enregistre chaque élément bloqué afin que vous puissiez résoudre le conflit d'origine et réexécuter l'import.

## Secrets

Les secrets ne sont jamais importés par défaut.

- Exécutez d'abord `openclaw migrate apply hermes --yes` pour importer l'état non-secret.
- Si vous voulez aussi que les clés `.env` supportées soient copiées, réexécutez avec `--include-secrets`.
- Pour les identifiants gérés par SecretRef, configurez la source SecretRef après la fin de l'import.

## Sortie JSON pour l'automatisation

```bash
openclaw migrate hermes --dry-run --json
openclaw migrate apply hermes --json --yes
```

Avec `--json` et sans `--yes`, apply affiche le plan et ne modifie pas l'état. C'est le mode le plus sûr pour CI et les scripts partagés.

## Dépannage

<AccordionGroup>
  <Accordion title="L'application refuse avec des conflits">
    Inspectez la sortie du plan. Chaque conflit identifie le chemin source et la cible existante. Décidez par élément s'il faut ignorer, modifier la cible ou réexécuter avec `--overwrite`.
  </Accordion>
  <Accordion title="Hermes se trouve en dehors de ~/.hermes">
    Passez `--from /actual/path` (CLI) ou `--import-source /actual/path` (onboarding).
  </Accordion>
  <Accordion title="L'onboarding refuse d'importer sur une configuration existante">
    Les imports d'onboarding nécessitent une configuration vierge. Soit réinitialisez l'état et réintégrez, soit utilisez `openclaw migrate apply hermes` directement, qui supporte `--overwrite` et le contrôle explicite des sauvegardes.
  </Accordion>
  <Accordion title="Les clés API n'ont pas été importées">
    `--include-secrets` est requis, et seules les clés énumérées ci-dessus sont reconnues. Les autres variables dans `.env` sont ignorées.
  </Accordion>
</AccordionGroup>

## Connexes

- [`openclaw migrate`](/fr/cli/migrate): référence CLI complète, contrat de plugin et formes JSON.
- [Onboarding](/fr/cli/onboard): flux de l'assistant et drapeaux non-interactifs.
- [Migration](/fr/install/migrating): déplacer une installation OpenClaw entre machines.
- [Doctor](/fr/gateway/doctor): vérification de santé post-migration.
- [Espace de travail des agents](/fr/concepts/agent-workspace): où vivent `SOUL.md`, `AGENTS.md` et les fichiers de mémoire.
