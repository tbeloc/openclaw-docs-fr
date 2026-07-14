---
summary: "Référence CLI et modèle de sécurité pour l'installation et la réparation d'OpenClaw avec inférence"
read_when:
  - You finished inference setup and want OpenClaw to configure the rest
  - You need to inspect or repair OpenClaw with the local setup agent
  - You are designing or enabling message-channel rescue mode
title: "Agent de configuration OpenClaw"
---

# `openclaw setup`

OpenClaw est livré avec un agent système intégré — il se présente comme « OpenClaw » — pour
la configuration locale, la réparation et la configuration (anciennement appelé Crestodian). Il démarre uniquement après que le modèle par défaut effectif complète un vrai tour.
Les installations récentes établissent d'abord l'inférence ; une configuration malformée reste sur le
chemin du docteur classique.

## Quand il démarre

L'exécution de `openclaw` sans sous-commande route en fonction de l'état de la configuration :

- Configuration manquante, ou existe sans paramètres créés (vide, ou seulement les clés `$schema`/`meta`) : démarre l'intégration guidée avec vérification IA en direct.
- Configuration existe mais échoue la validation : démarre l'intégration classique, qui signale les problèmes et vous dirige vers `openclaw doctor`.
- Configuration existe et est valide : ouvre l'interface utilisateur TUI de l'agent normal. Une passerelle configurée accessible dont l'agent par défaut a un modèle va directement à cette interface utilisateur
  sans intégration ni OpenClaw. Utilisez `/openclaw` dans l'interface utilisateur TUI, ou exécutez
  `openclaw setup` directement, pour accéder à OpenClaw plus tard.

L'exécution de `openclaw setup` teste d'abord en direct le modèle par défaut configuré. Un tour réussi démarre OpenClaw. Un échec interactif ouvre la configuration d'inférence guidée et bascule vers OpenClaw après qu'un candidat réussisse. Les demandes non interactives, JSON et autres échouent avec des instructions pour exécuter `openclaw onboard` quand l'inférence n'est pas disponible. `openclaw --help` et `openclaw --version` conservent leurs chemins rapides normaux.

Le `openclaw` nu non interactif (pas de TTY) se termine par un court message au lieu d'imprimer l'aide racine : il pointe vers l'intégration non interactive sur une installation récente ou invalide, ou vers `openclaw agent --local ...` quand la configuration est valide.

`openclaw onboard --modern` reste un alias de compatibilité pour OpenClaw, mais utilise la même porte d'inférence : l'inférence fonctionnelle ouvre le chat, les échecs interactifs démarrent la configuration d'inférence guidée, et les échecs non interactifs se terminent par des conseils d'intégration. `openclaw onboard --classic` ouvre l'assistant complet étape par étape.

## Ce qu'OpenClaw affiche

L'OpenClaw interactif ouvre le même shell TUI que `openclaw tui`, avec un backend de chat OpenClaw. Le message d'accueil au démarrage couvre :

- la validité de la configuration et l'agent par défaut
- le modèle vérifié qu'OpenClaw utilise
- l'accessibilité de la passerelle à partir de la première sonde de démarrage
- l'action de débogage suivante recommandée

Il ne vide pas les secrets ni ne charge les commandes CLI du plugin juste pour démarrer.

Utilisez `status` pour l'inventaire détaillé : chemin de configuration, chemins docs/source, sondes CLI locales, présence de clé/jeton, agents, modèle et détails de la passerelle.

OpenClaw utilise la même découverte de référence que les agents réguliers : dans un checkout Git, il pointe vers le `docs/` local et l'arborescence source ; dans une installation npm, il utilise les docs groupées et les liens vers [https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw), avec des conseils pour vérifier la source quand les docs ne suffisent pas.

## Exemples

```bash
openclaw
openclaw setup
openclaw setup --json
openclaw setup --message "models"
openclaw setup --message "validate config"
openclaw setup --message "setup workspace ~/Projects/work" --yes
openclaw setup --message "set default model openai/gpt-5.6" --yes
openclaw onboard --modern
```

À l'intérieur de l'interface utilisateur TUI OpenClaw :

```text
status
health
doctor
validate config
setup
setup workspace ~/Projects/work
config set gateway.port 19001
config set-ref gateway.auth.token env OPENCLAW_GATEWAY_TOKEN
gateway status
restart gateway
agents
create agent work workspace ~/Projects/work
models
configure model provider
set default model openai/gpt-5.6
channels
channel info slack
connect slack
open channel wizard for slack
plugins list
plugins search slack
plugin install clawhub:openclaw-codex-app-server
talk to work agent
talk to agent for ~/Projects/work
audit
quit
```

## Opérations et approbation

OpenClaw utilise des opérations typées au lieu de modifier la configuration de manière ad hoc.

Les opérations en lecture seule s'exécutent immédiatement : afficher l'aperçu, lister les agents, lister les plugins installés, rechercher les plugins ClawHub, afficher l'état du modèle/backend, exécuter les vérifications de statut/santé, vérifier l'accessibilité de la passerelle, exécuter le docteur sans corrections interactives, valider la configuration, afficher le chemin du journal d'audit.

Le démarrage de la configuration de canal guidée (`connect telegram`) s'exécute également immédiatement. Son assistant collecte les réponses explicites et possède les écritures résultantes.

Les opérations persistantes nécessitent une approbation conversationnelle (ou `--yes` pour une commande directe) : écrire la configuration, `config set`, `config set-ref`, bootstrap d'installation/intégration, modifier le modèle par défaut, démarrer/arrêter/redémarrer la passerelle, créer des agents et installer des plugins.

Les réparations du docteur ne sont pas disponibles dans OpenClaw car elles peuvent réécrire le fournisseur, l'authentification ou la route d'inférence de l'agent par défaut alimentant la session. Quittez OpenClaw et exécutez `openclaw doctor --fix` dans un terminal. Le `doctor` en lecture seule reste disponible dans OpenClaw.

Les nouveaux agents héritent de la route d'inférence par défaut vérifiée en direct. Les identifiants d'agent `openclaw` et `crestodian` sont réservés à l'agent système et ne peuvent pas être créés en tant qu'agents normaux. L'identifiant retiré reste bloqué pour qu'une ancienne configuration ne puisse pas le réclamer.

`config set` et `config set-ref` ne peuvent pas modifier l'état de la route d'inférence,
y compris les identifiants de fournisseur d'inférence, le niveau supérieur `auth.*`, les catalogues de modèles,
les backends CLI, les routes de modèle par défaut/par agent, les paramètres/outils d'agent, ou la racine
`tools.*`. Les écritures brutes sous `env.*`, `secrets.*`, `plugins.*`, et `$include`
sont également refusées car elles peuvent remplacer la résolution des identifiants ou l'activation du fournisseur. L'authentification de la passerelle et du canal restent des surfaces de configuration normales. Utilisez les flux de plugin/canal typés et
`set default model <provider/model>` pour une route déjà
configurée ; elle teste en direct la route avant de la sauvegarder. Pour configurer ou
réparer l'accès au fournisseur/authentification, quittez OpenClaw et exécutez `openclaw onboard`.

La désinstallation du plugin est refusée dans OpenClaw car la suppression d'un plugin de fournisseur
pourrait désactiver la route d'inférence alimentant la session. Quittez OpenClaw
et exécutez `openclaw plugins uninstall <id>` à partir d'un terminal.

L'approbation est donnée avec vos propres mots : les réponses sans ambiguïté (« yes », « sure », « go ahead », « not now ») se résolvent à partir d'une liste déterministe fermée. Quand la route configurée supporte un appel d'achèvement séparé, d'autres réponses peuvent être classées à partir de seulement votre message et de la proposition en attente — jamais par le modèle de conversation lui-même, qui ne peut pas s'auto-approuver. Les réponses non classifiées ou ambiguës gardent la proposition en attente et la conversation demande à nouveau.

Les écritures appliquées sont enregistrées dans `~/.openclaw/audit/system-agent.jsonl`. La découverte n'est pas auditée ; seules les opérations et écritures appliquées le sont.

La configuration du canal peut s'exécuter en tant que conversation hébergée jusqu'à ce qu'elle atteigne un secret. L'interface utilisateur TUI OpenClaw locale n'accepte pas les réponses d'assistant sensibles car l'entrée de chat terminal est visible. Elle offre `open channel wizard` immédiatement, portant le canal sélectionné dans l'assistant terminal masqué ; vous pouvez également exécuter
`openclaw channels add --channel <channel>` plus tard.

### Passage à la configuration de canal masquée

Le chat local peut transférer le contrôle à l'assistant de canal masqué :

```text
open channel wizard for slack
channel info slack
```

`open channel wizard for <channel>` ouvre la configuration de canal masquée après la fermeture du chat
TUI. Utilisez d'abord `channel info <channel>` pour l'étiquette du canal, l'état de configuration,
le résumé des prérequis et le lien de documentation.

OpenClaw ne change jamais l'accès au fournisseur/authentification de l'intérieur de sa propre session : la
session dépend déjà de cette route d'inférence. Pour la configuration ou la réparation du fournisseur de modèle, `configure model provider` retourne des conseils de sortie/intégration sans
démarrer un assistant ou écrire la configuration. Quittez OpenClaw et exécutez `openclaw
onboard` ; l'intégration prépare les identifiants et sauvegarde uniquement une route qui
complète un vrai tour en direct. Démarrez OpenClaw à nouveau après que l'intégration réussisse.

## Bootstrap de configuration

`setup` configure l'état de l'espace de travail et de la passerelle restant après que l'intégration guidée a déjà établi l'inférence. Il écrit uniquement via des opérations de configuration typées et demande d'abord l'approbation.

```text
setup
setup workspace ~/Projects/work
```

`setup` préserve le modèle effectif vérifié. Il ne configure ni ne remplace l'inférence.

Si l'inférence est manquante ou sa vérification en direct échoue, quittez OpenClaw et exécutez `openclaw onboard`. L'intégration guidée détecte les modèles configurés, les clés API et les CLIs locales authentifiées, demande à chaque candidat une réponse réelle, et persiste uniquement une route réussie. OpenClaw démarre immédiatement après cette limite et peut alors configurer l'espace de travail, la passerelle, les canaux, les agents, les plugins et d'autres fonctionnalités optionnelles.

L'application macOS ignore complètement cette échelle quand elle atteint une passerelle configurée
dont l'agent par défaut a déjà un modèle configuré ; elle ouvre l'interface utilisateur de l'agent normal.
Pour une passerelle récente ou incomplète, l'application conduit l'échelle d'inférence via
les méthodes de passerelle `openclaw.setup.detect` et `openclaw.setup.activate` :
detect liste chaque candidat backend qu'il trouve, activate teste en direct un
candidat (une vraie complétion « reply with OK »), et persiste uniquement le modèle,
l'identifiant et l'état du fournisseur/runtime nécessaires pour cette route après que le test réussisse. Les valeurs par défaut de l'espace de travail et de la passerelle restent pour OpenClaw. Un candidat défaillant
ne change jamais la configuration ; l'application marche automatiquement vers le bas de l'échelle et finalement
offre une étape manuelle de clé/jeton remplie à partir des plugins de fournisseur d'inférence textuelle actifs de la passerelle. Le fournisseur sélectionné possède son modèle de démarrage
et sa configuration, et l'identifiant est vérifié de la même manière avant d'être sauvegardé.

La supervision Codex et d'autres fonctionnalités de plugin optionnelles restent en dehors de cette
transaction d'activation d'inférence. Configurez-les uniquement après que l'inférence fonctionne et qu'OpenClaw a démarré ; la politique de plugin existante et les refus de supervision explicites restent intacts pendant la configuration d'inférence.

## Conversation IA

La conversation libre interactive d'OpenClaw s'exécute à travers la même boucle d'agent que les agents OpenClaw ordinaires, limitée à un outil d'autorité OpenClaw ring-zéro, `openclaw`, qui encapsule les opérations typées. Les actions de lecture s'exécutent librement, les mutations nécessitent votre approbation conversationnelle pour cette opération exacte (voir Opérations et approbation), et chaque écriture appliquée est auditée et revalidée. La session d'agent persiste, donc OpenClaw dispose d'une véritable mémoire multi-tours. Si la route d'inférence vérifiée cesse de fonctionner ultérieurement, retournez à `openclaw onboard` et réparez-la avant de continuer.

L'hôte n'analyse pas les demandes en langage naturel en opérations. Les messages libres — y compris le texte ressemblant à des commandes et les questions telles que « pourquoi ma passerelle s'est-elle arrêtée ? » — vont à l'IA, qui peut mapper la demande à une opération typée via l'outil `openclaw`.

Quand une mutation est en attente, seules les phrases d'approbation ou de refus non ambiguës d'une liste fermée sont résolues sans inférence. Le consentement ambigu va à un appel d'achèvement configuré séparé et échoue autrement de manière fermée. Les champs d'assistant structurés et la navigation d'hôte exacte sont des contrôles d'interface utilisateur, pas l'analyse d'opération en langage naturel. Une exception d'hygiène secrète est particulièrement importante : un `config set` exact sur un chemin sensible (jetons, clés, mots de passe) n'atteint jamais un modèle. L'hôte crée une proposition expurgée, et la valeur est masquée dans l'historique visible par l'IA. Préférez `config set-ref <path> env <ENV_VAR>` pour les secrets.

Le mode de secours du canal de message n'utilise jamais le planificateur assisté par modèle. Le secours à distance reste déterministe afin qu'un chemin d'agent normal cassé ou compromis ne puisse pas être utilisé comme éditeur de configuration.

### Modèle de confiance du harnais CLI

Les runtimes intégrés et le harnais du serveur d'application Codex appliquent la restriction ring-zéro directement : l'exécution porte une liste d'autorisation d'outil OpenClaw avec uniquement l'outil `openclaw`. Pour Codex, OpenClaw désactive également les environnements, l'exécution native, multi-agent, l'objectif, l'application/plugin, la compétence/MCP, la recherche web et les surfaces `request_user_input` pour cette exécution. Codex injecte toujours son utilitaire natif inerte `update_plan` ; il peut mettre à jour la liste de contrôle temporaire du modèle mais ne peut pas écrire de fichiers ou de configuration OpenClaw. Les harnais CLI ne consomment pas la liste d'autorisation d'OpenClaw, donc OpenClaw n'admet que les backends dont le propre contrat de sélection d'outil peut prouver la même restriction :

- Les backends sélectionnables, y compris Claude Code, se lancent avec une sélection d'outil natif vide et un outil MCP, `openclaw`. La configuration MCP générée par Claude est appliquée avec `--strict-mcp-config`, donc aucun autre serveur MCP n'est chargé.
- Les backends qui ne déclarent aucun outil natif reçoivent le même serveur MCP OpenClaw dédié.
- Les backends d'outil natif toujours actifs ou inconnus échouent de manière fermée avant l'inférence ; ils ne peuvent pas héberger une session OpenClaw.

Seules les sessions OpenClaw obtiennent le serveur MCP openclaw ; les exécutions d'agent normal ne voient jamais cet outil. Les backends CLI sélectionnables/sans outil natif et les modèles de clé API appliquent donc la boucle littérale à outil unique. Les modèles du serveur d'application Codex appliquent un outil d'autorité OpenClaw unique plus l'utilitaire de planification natif inerte. Dans les trois cas, les écritures de configuration restent confinées au contrat d'approbation audité d'OpenClaw.

Gemini CLI reste disponible pour les agents normaux, mais il ne peut pas appliquer la sonde sans outil requise par la porte d'inférence, donc il ne peut pas héberger OpenClaw.

## Basculer vers un agent

Utilisez un sélecteur en langage naturel pour quitter OpenClaw et ouvrir l'interface utilisateur TUI normale :

```text
talk to agent
talk to work agent
switch to main agent
```

`openclaw tui`, `openclaw chat` et `openclaw terminal` ouvrent directement l'interface utilisateur TUI d'agent normal ; ils ne démarrent pas OpenClaw. Après basculement dans l'interface utilisateur TUI normale, `/openclaw` revient à OpenClaw, éventuellement avec une demande de suivi :

```text
/openclaw
/openclaw restart gateway
```

## Mode de secours du message

Le mode de secours du message est le point d'entrée du canal de message pour OpenClaw : utilisez-le quand votre agent normal est mort mais qu'un canal de confiance (par exemple WhatsApp) reçoit toujours des commandes.

C'est un gestionnaire de commandes d'urgence déterministe, pas l'agent OpenClaw conversationnel. Il n'amorce pas une nouvelle configuration ni ne relâche la porte d'inférence pour le chat OpenClaw.

Commande prise en charge : `/openclaw <request>`. Le secours accepte uniquement la grammaire de commande typée exacte — le langage naturel est rejeté avec un indice, jamais deviné en une opération, et aucun modèle n'est jamais consulté.

```text
Vous, dans un DM du propriétaire de confiance : /openclaw status
OpenClaw: OpenClaw rescue mode. Gateway reachable: no. Config valid: no.
Vous: /openclaw restart gateway
OpenClaw: Plan: restart the Gateway. Reply /openclaw yes to apply.
Vous: /openclaw yes
OpenClaw: Applied. Audit entry written.
```

La création d'agent peut également être mise en file d'attente localement ou via secours :

```text
create agent work workspace ~/Projects/work model openai/gpt-5.6-sol
/openclaw create agent work workspace ~/Projects/work
```

La création d'agent ne peut nommer que le modèle par défaut en direct actuellement vérifié. Omettez le modèle pour hériter de cette route.

Le secours à distance est une surface d'administration et doit être traité comme une réparation de configuration à distance, pas un chat normal.

Contrat de sécurité pour le secours à distance :

- Désactivé quand le sandboxing est actif pour l'agent/session ; OpenClaw refuse le secours à distance et pointe vers la réparation CLI locale.
- L'état effectif par défaut est `auto` : autoriser le secours à distance uniquement en opération YOLO de confiance, où le runtime a déjà une autorité locale non sandboxée (`tools.exec.security` se résout en `full` et `tools.exec.ask` se résout en `off`, avec le mode sandbox `off`).
- Nécessite une identité de propriétaire explicite ; pas de règles de sender générique, de politique de groupe ouverte, de webhooks non authentifiés ou de canaux anonymes.
- DM du propriétaire uniquement par défaut ; le secours de groupe/canal nécessite un opt-in explicite.
- La recherche et la liste de plugins sont en lecture seule. L'installation de plugin est toujours locale uniquement (bloquée en secours, même si elle est autrement activée) car elle télécharge du code exécutable. La désinstallation de plugin est refusée à la fois dans OpenClaw local et en secours ; exécutez `openclaw plugins uninstall <id>` à partir d'un terminal.
- Le secours à distance ne peut pas ouvrir l'interface utilisateur TUI locale ni basculer dans une session d'agent interactive ; utilisez `openclaw` local pour la remise d'agent.
- Les écritures persistantes nécessitent toujours une approbation, même en mode secours.
- Chaque opération de secours appliquée est auditée. Le secours du canal de message enregistre les métadonnées du canal, du compte, de l'expéditeur et de l'adresse source ; les opérations de mutation de configuration enregistrent également les hachages de configuration avant et après.
- Les secrets ne sont jamais répétés. L'inspection SecretRef rapporte la disponibilité, pas les valeurs.
- Si la passerelle est active, le secours préfère les opérations typées de la passerelle ; si elle est morte, le secours utilise uniquement la surface de réparation locale minimale qui ne dépend pas de la boucle d'agent normal.

Forme de configuration :

```jsonc
{
  "systemAgent": {
    "rescue": {
      "enabled": "auto",
      "ownerDmOnly": true,
      "pendingTtlMinutes": 15,
    },
  },
}
```

- `enabled` : `"auto"` (par défaut) autorise le secours uniquement quand le runtime effectif est YOLO et le sandboxing est désactivé ; `false` n'autorise jamais le secours du canal de message ; `true` autorise explicitement le secours quand les vérifications de propriétaire/canal passent (toujours soumis au refus de sandboxing).
- `ownerDmOnly` : restreindre le secours aux messages directs du propriétaire. Par défaut `true`.
- `pendingTtlMinutes` : combien de temps une écriture de secours en attente reste ouverte pour l'approbation `/openclaw yes` avant d'expirer. Par défaut `15`.

`openclaw doctor --fix` migre le bloc de configuration `crestodian` hérité vers
`systemAgent`. Le runtime lit uniquement le bloc canonique.

Le secours à distance est couvert par la voie Docker :

```bash
pnpm test:docker:system-agent-rescue
```

Une surface de commande de canal en direct opt-in effectue des vérifications de fumée `/openclaw status` plus un aller-retour d'approbation persistant via le gestionnaire de secours :

```bash
pnpm test:live:system-agent-rescue-channel
```

La configuration d'une première exécution packagée avec porte d'inférence est couverte par :

```bash
pnpm test:docker:system-agent-first-run
```

Cette voie CLI packagée commence avec un répertoire d'état vide et prouve qu'OpenClaw échoue de manière fermée sans inférence. Elle teste ensuite et active Claude faux via le module d'activation packagé. Ce n'est qu'après qu'une demande floue atteint le planificateur et se résout en configuration typée, suivie de commandes ponctuelles qui créent un agent supplémentaire, configurent Discord via un activation de plugin plus SecretRef de jeton, valident la configuration et vérifient le journal d'audit. Cette voie est une preuve de porte/opération de support ; elle n'exerce pas l'intégration interactive ou la conversation d'agent/outil/approbation OpenClaw. Le scénario du laboratoire d'assurance qualité ci-dessous redirige vers la même voie Docker :

```bash
pnpm openclaw qa suite --scenario system-agent-ring-zero-setup
```

## Connexes

- [Référence CLI](/fr/cli)
- [Doctor](/fr/cli/doctor)
- [TUI](/fr/cli/tui)
- [Sandbox](/fr/cli/sandbox)
- [Sécurité](/fr/cli/security)
