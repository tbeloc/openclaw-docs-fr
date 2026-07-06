---
summary: "Référence CLI pour les enregistrements d'audit des exécutions d'agent et des actions d'outil en métadonnées uniquement"
read_when:
  - You need to answer who ran an agent or tool, when it ran, and how it ended
  - You need a bounded, redaction-safe activity export
title: "Enregistrements d'audit"
---

# `openclaw audit`

Interrogez le registre d'audit en métadonnées uniquement de la Gateway pour les exécutions d'agent et les actions d'outil.

L'enregistrement est activé par défaut ; définissez [`audit.enabled: false`](/fr/gateway/configuration-reference#audit)
pour arrêter les nouvelles écritures. Les enregistrements existants restent interrogeables jusqu'à leur expiration (30 jours).
Le registre est séparé des transcriptions de conversation : il enregistre l'identité,
l'ordre, la provenance, l'action, le statut et les codes d'erreur normalisés, mais ne stocke jamais
les invites, les messages, les arguments d'outil, les résultats d'outil, la sortie de commande ou le texte d'erreur brut.

La Gateway écrit les enregistrements dans la base de données d'état OpenClaw partagée via un
writer d'arrière-plan limité. Les requêtes ne retournent jamais d'enregistrements antérieurs à 30 jours,
et le registre est limité à 100 000 lignes. Les lignes expirées sont supprimées lors du
démarrage de la Gateway, de la maintenance horaire et des écritures ultérieures.

```bash
openclaw audit
openclaw audit --agent main --status failed
openclaw audit --session "agent:main:main" --after 2026-07-01T00:00:00Z
openclaw audit --run 8c69f72e-8b11-4c54-98d5-1a3dd67450c3
openclaw audit --kind tool_action --limit 50 --json
```

## Filtres

- `--agent <id>`: identifiant d'agent exact
- `--session <key>`: clé de session exacte
- `--run <id>`: identifiant d'exécution exact
- `--kind <kind>`: `agent_run` ou `tool_action`
- `--status <status>`: `started`, `succeeded`, `failed`, `cancelled`,
  `timed_out`, `blocked`, ou `unknown`
- `--after <timestamp>` / `--before <timestamp>`: horodatage ISO inclusif ou
  millisecondes Unix
- `--limit <count>`: taille de page de 1 à 500 ; par défaut `100`
- `--cursor <sequence>`: continuer une requête précédente du plus récent au plus ancien
- `--json`: imprimer la page limitée en JSON

La sortie texte affiche l'heure, le type, le statut, l'agent, l'exécution et l'action. Les actions d'outil affichent également
le nom de l'outil. La sortie JSON est une exportation limitée et sûre des mêmes métadonnées
et inclut `nextCursor` quand une autre page existe. Passez cette valeur à
`--cursor` pour continuer sans réorganiser les enregistrements qui arrivent lors de la pagination.

## Événements enregistrés

La Gateway projette les flux d'événements d'agent existants en quatre actions :

- `agent.run.started`
- `agent.run.finished`
- `tool.action.started`
- `tool.action.finished`

Chaque enregistrement a un identifiant d'événement stable, une séquence de registre monotone croissante,
la séquence d'événement d'exécution d'origine, l'horodatage du cycle de vie quand le runtime le fournit
(sinon l'heure d'observation), la provenance de l'agent/exécution, l'acteur, et un
marqueur `redaction: "metadata_only"`. Les enregistrements terminaux distinguent le succès,
l'échec, l'annulation, le délai d'expiration et les blocages de politique avec un statut fermé et des codes d'erreur. `unknown` est un résultat explicite de non-succès quand un runtime en amont
n'expose pas un résultat terminal faisant autorité. Les identifiants d'appel d'outil sont exportés
uniquement comme empreintes digitales stables unidirectionnelles. Les noms d'outil doivent correspondre au contrat de nom compact
orienté modèle ; les autres valeurs deviennent `unknown`. Les identifiants de session, les clés de session,
les identifiants d'exécution et les noms d'outil conservés sont des métadonnées d'opérateur ; protégez les exportations
comme des enregistrements opérationnels.

Le registre d'audit ne remplace pas les transcriptions, l'historique des tâches, l'historique des exécutions cron,
ou les journaux. Il fournit un petit index inter-exécution pour les questions d'opérateur sans
copier le contenu de la conversation dans un autre magasin.

## RPC Gateway

`audit.list` nécessite `operator.read` et accepte les mêmes filtres. Exemple :

```bash
openclaw gateway call audit.list --params '{"agentId":"main","status":"failed","limit":50}'
```

Le résultat est `{ "events": AuditEvent[], "nextCursor"?: string }`. Les résultats sont
du plus récent au plus ancien et limités à 500 enregistrements par requête.

## Connexes

- [Protocole Gateway](/fr/gateway/protocol#audit-ledger-rpc)
- [Sessions](/fr/cli/sessions)
- [Tâches](/fr/cli/tasks)
- [Tâches Cron](/fr/automation/cron-jobs)
