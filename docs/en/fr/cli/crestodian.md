---
summary: "Référence CLI et modèle de sécurité pour Crestodian, l'assistant de configuration et de réparation sans configuration"
read_when:
  - You run openclaw with no command and want to understand Crestodian
  - You need a configless-safe way to inspect or repair OpenClaw
  - You are designing or enabling message-channel rescue mode
title: "Crestodian"
---

# `openclaw crestodian`

Crestodian est l'assistant local de configuration, de réparation et de gestion des paramètres d'OpenClaw. Il est
conçu pour rester accessible quand le chemin normal de l'agent est cassé.

L'exécution d'`openclaw` sans commande démarre Crestodian dans un terminal interactif.
L'exécution d'`openclaw crestodian` démarre le même assistant explicitement.

## Ce que Crestodian affiche

Au démarrage, Crestodian interactif ouvre le même shell TUI utilisé par
`openclaw tui`, avec un backend de chat Crestodian. Le journal de chat commence par un court
message d'accueil :

- quand démarrer Crestodian
- le chemin du modèle ou du planificateur déterministe que Crestodian utilise réellement
- la validité de la configuration et l'agent par défaut
- l'accessibilité de la passerelle à partir de la première sonde de démarrage
- la prochaine action de débogage que Crestodian peut entreprendre

Il ne vide pas les secrets ni ne charge les commandes CLI des plugins juste pour démarrer. Le TUI
fournit toujours l'en-tête normal, le journal de chat, la ligne d'état, le pied de page, l'autocomplétion,
et les contrôles de l'éditeur.

Utilisez `status` pour l'inventaire détaillé avec le chemin de configuration, les chemins docs/source,
les sondes CLI locales, la présence de clé API, les agents, le modèle, et les détails de la passerelle.

Crestodian utilise la même découverte de référence OpenClaw que les agents normaux. Dans un checkout Git,
il se pointe lui-même sur `docs/` local et l'arborescence source locale. Dans une installation de package npm, il
utilise les docs du package groupé et les liens vers
[https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw), avec des
conseils explicites pour examiner la source chaque fois que la documentation n'est pas suffisante.

## Exemples

```bash
openclaw
openclaw crestodian
openclaw crestodian --json
openclaw crestodian --message "models"
openclaw crestodian --message "validate config"
openclaw crestodian --message "setup workspace ~/Projects/work model openai/gpt-5.5" --yes
openclaw crestodian --message "set default model openai/gpt-5.5" --yes
openclaw onboard --modern
```

À l'intérieur du TUI Crestodian :

```text
status
health
doctor
doctor fix
validate config
setup
setup workspace ~/Projects/work model openai/gpt-5.5
config set gateway.port 19001
config set-ref gateway.auth.token env OPENCLAW_GATEWAY_TOKEN
gateway status
restart gateway
agents
create agent work workspace ~/Projects/work
models
set default model openai/gpt-5.5
talk to work agent
talk to agent for ~/Projects/work
audit
quit
```

## Démarrage sécurisé

Le chemin de démarrage de Crestodian est délibérément petit. Il peut s'exécuter quand :

- `openclaw.json` est manquant
- `openclaw.json` est invalide
- la passerelle est arrêtée
- l'enregistrement des commandes des plugins n'est pas disponible
- aucun agent n'a été configuré encore

`openclaw --help` et `openclaw --version` utilisent toujours les chemins rapides normaux.
`openclaw` non interactif se termine par un court message au lieu d'imprimer l'aide racine,
car le produit sans commande est Crestodian.

## Opérations et approbation

Crestodian utilise des opérations typées au lieu de modifier la configuration ad hoc.

Les opérations en lecture seule peuvent s'exécuter immédiatement :

- afficher l'aperçu
- lister les agents
- afficher l'état du modèle/backend
- exécuter les vérifications de statut ou de santé
- vérifier l'accessibilité de la passerelle
- exécuter le docteur sans corrections interactives
- valider la configuration
- afficher le chemin du journal d'audit

Les opérations persistantes nécessitent une approbation conversationnelle en mode interactif sauf si
vous passez `--yes` pour une commande directe :

- écrire la configuration
- exécuter `config set`
- définir les valeurs SecretRef supportées via `config set-ref`
- exécuter l'amorçage de configuration/intégration
- changer le modèle par défaut
- démarrer, arrêter ou redémarrer la passerelle
- créer des agents
- exécuter les réparations du docteur qui réécrivent la configuration ou l'état

Les écritures appliquées sont enregistrées dans :

```text
~/.openclaw/audit/crestodian.jsonl
```

La découverte n'est pas auditée. Seules les opérations appliquées et les écritures sont enregistrées.

`openclaw onboard --modern` démarre Crestodian comme l'aperçu d'intégration moderne.
`openclaw onboard` simple exécute toujours l'intégration classique.

## Amorçage de configuration

`setup` est l'amorçage d'intégration en premier lieu de chat. Il écrit uniquement via des opérations de
configuration typées et demande d'abord l'approbation.

```text
setup
setup workspace ~/Projects/work
setup workspace ~/Projects/work model openai/gpt-5.5
```

Quand aucun modèle n'est configuré, setup sélectionne le premier backend utilisable dans cet
ordre et vous dit ce qu'il a choisi :

- modèle explicite existant, s'il est déjà configuré
- `OPENAI_API_KEY` -> `openai/gpt-5.5`
- `ANTHROPIC_API_KEY` -> `anthropic/claude-opus-4-7`
- Claude Code CLI -> `claude-cli/claude-opus-4-7`
- Codex CLI -> `codex-cli/gpt-5.5`

Si aucun n'est disponible, setup écrit toujours l'espace de travail par défaut et laisse le
modèle non défini. Installez ou connectez-vous à Codex/Claude Code, ou exposez
`OPENAI_API_KEY`/`ANTHROPIC_API_KEY`, puis exécutez setup à nouveau.

## Planificateur assisté par modèle

Crestodian démarre toujours en mode déterministe. Pour les commandes floues que l'analyseur
déterministe ne comprend pas, Crestodian local peut faire un tour de planificateur borné via les chemins
d'exécution normaux d'OpenClaw. Il utilise d'abord le modèle OpenClaw configuré. Si aucun modèle configuré
n'est utilisable pour le moment, il peut revenir aux runtimes locaux déjà présents sur la machine :

- Claude Code CLI : `claude-cli/claude-opus-4-7`
- Harnais app-server Codex : `openai/gpt-5.5` avec `embeddedHarness.runtime: "codex"`
- Codex CLI : `codex-cli/gpt-5.5`

Le planificateur assisté par modèle ne peut pas muter la configuration directement. Il doit traduire la
demande en l'une des commandes typées de Crestodian, puis les règles d'approbation et d'audit normales
s'appliquent. Crestodian imprime le modèle qu'il a utilisé et la commande interprétée avant d'exécuter
quoi que ce soit. Les tours du planificateur de secours sans configuration sont temporaires, les outils
désactivés où le runtime le supporte, et utilisent un espace de travail/session temporaire.

Le mode de sauvetage par canal de message n'utilise pas le planificateur assisté par modèle. Le sauvetage
à distance reste déterministe afin qu'un chemin d'agent normal cassé ou compromis ne puisse pas être
utilisé comme éditeur de configuration.

## Basculer vers un agent

Utilisez un sélecteur en langage naturel pour quitter Crestodian et ouvrir le TUI normal :

```text
talk to agent
talk to work agent
switch to main agent
```

`openclaw tui`, `openclaw chat`, et `openclaw terminal` ouvrent toujours le TUI normal
de l'agent directement. Ils ne démarrent pas Crestodian.

Après basculement dans le TUI normal, utilisez `/crestodian` pour revenir à Crestodian.
Vous pouvez inclure une demande de suivi :

```text
/crestodian
/crestodian restart gateway
```

Les basculements d'agents à l'intérieur du TUI laissent une trace que `/crestodian` est disponible.

## Mode de sauvetage par message

Le mode de sauvetage par message est le point d'entrée du canal de message pour Crestodian. C'est pour
le cas où votre agent normal est mort, mais un canal de confiance tel que WhatsApp
reçoit toujours les commandes.

Commande texte supportée :

- `/crestodian <request>`

Flux opérateur :

```text
Vous, dans un DM propriétaire de confiance : /crestodian status
OpenClaw: Crestodian rescue mode. Gateway reachable: no. Config valid: no.
Vous : /crestodian restart gateway
OpenClaw: Plan: restart the Gateway. Reply /crestodian yes to apply.
Vous : /crestodian yes
OpenClaw: Applied. Audit entry written.
```

La création d'agent peut également être mise en file d'attente à partir de l'invite locale ou du mode de sauvetage :

```text
create agent work workspace ~/Projects/work model openai/gpt-5.5
/crestodian create agent work workspace ~/Projects/work
```

Le mode de sauvetage à distance est une surface d'administration. Il doit être traité comme une
réparation de configuration à distance, pas comme un chat normal.

Contrat de sécurité pour le sauvetage à distance :

- Désactivé quand le sandboxing est actif. Si un agent/session est en sandbox,
  Crestodian doit refuser le sauvetage à distance et expliquer que la réparation CLI locale est
  requise.
- L'état effectif par défaut est `auto` : autoriser le sauvetage à distance uniquement en opération YOLO de confiance,
  où le runtime a déjà une autorité locale non sandboxée.
- Exiger une identité de propriétaire explicite. Le sauvetage ne doit pas accepter les règles d'expéditeur
  générique, la politique de groupe ouverte, les webhooks non authentifiés, ou les canaux anonymes.
- DMs propriétaire uniquement par défaut. Le sauvetage de groupe/canal nécessite un opt-in explicite et
  devrait toujours acheminer les invites d'approbation vers le DM propriétaire.
- Le sauvetage à distance ne peut pas ouvrir le TUI local ou basculer dans une session d'agent interactif.
  Utilisez `openclaw` local pour la remise d'agent.
- Les écritures persistantes nécessitent toujours une approbation, même en mode de sauvetage.
- Auditer chaque opération de sauvetage appliquée, y compris le canal, le compte, l'expéditeur,
  la clé de session, l'opération, le hash de configuration avant, et le hash de configuration après.
- Ne jamais afficher les secrets. L'inspection SecretRef doit signaler la disponibilité, pas
  les valeurs.
- Si la passerelle est vivante, préférer les opérations typées de la passerelle. Si la passerelle est
  morte, utiliser uniquement la surface de réparation locale minimale qui ne dépend pas de la
  boucle d'agent normale.

Forme de configuration :

```jsonc
{
  "crestodian": {
    "rescue": {
      "enabled": "auto",
      "ownerDmOnly": true,
    },
  },
}
```

`enabled` devrait accepter :

- `"auto"` : par défaut. Autoriser uniquement quand le runtime effectif est YOLO et
  le sandboxing est désactivé.
- `false` : ne jamais autoriser le sauvetage par canal de message.
- `true` : autoriser explicitement le sauvetage quand les vérifications de propriétaire/canal passent. Cela
  ne doit toujours pas contourner le refus de sandboxing.

La posture YOLO `"auto"` par défaut est :

- le mode sandbox se résout à `off`
- `tools.exec.security` se résout à `full`
- `tools.exec.ask` se résout à `off`

Le sauvetage à distance est couvert par la voie Docker :

```bash
pnpm test:docker:crestodian-rescue
```

Le repli du planificateur local sans configuration est couvert par :

```bash
pnpm test:docker:crestodian-planner
```

Des vérifications de fumée de surface de commande de canal en direct opt-in `/crestodian status` plus un
tour d'approbation persistant via le gestionnaire de sauvetage :

```bash
pnpm test:live:crestodian-rescue-channel
```

La configuration sans configuration fraîche via Crestodian est couverte par :

```bash
pnpm test:docker:crestodian-first-run
```

Cette voie commence avec un répertoire d'état vide, achemine `openclaw` nu vers Crestodian,
définit le modèle par défaut, crée un agent supplémentaire, configure Discord via
une SecretRef de jeton, valide la configuration, et vérifie le journal d'audit.

## Connexes

- [Référence CLI](/fr/cli)
- [Docteur](/fr/cli/doctor)
- [TUI](/fr/cli/tui)
- [Sandbox](/fr/cli/sandbox)
- [Sécurité](/fr/cli/security)
