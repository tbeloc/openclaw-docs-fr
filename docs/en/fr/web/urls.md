---
summary: "Contrôlez les routes d'URL de l'interface utilisateur, la grammaire stable des liens de session et les paramètres de transfert de connexion"
read_when:
  - You need to bookmark or share a Control UI session
  - You are adding or changing a Control UI route
  - You need a terminal, approval, onboarding, or remote Gateway URL
title: "URLs de l'interface utilisateur de contrôle"
---

L'interface utilisateur de contrôle utilise des chemins lisibles pour les pages et les liens de session. Un `gateway.controlUi.basePath` configuré préfixe chaque chemin ci-dessous. Par exemple, `/chat/main` devient `/openclaw/chat/main` lorsque le chemin de base est `/openclaw`.

## URLs de session et de tableau de bord

Les vues de chat et de tableau de bord sont des espaces de noms de routes parallèles :

```text
/chat/main/deploy-monitor-6db92d48
/dashboard/main/deploy-monitor-6db92d48
/chat/main/telegram/12345
/chat/main/cron/nightly/run/8821
/chat/main
```

La grammaire du chemin est :

```text
/<namespace>/<agentId>
/<namespace>/<agentId>/<sessionRef>
/<namespace>/<agentId>/<restSegment>/<restSegment>...
```

`<namespace>` est soit `/chat` soit `/dashboard`. La première forme ouvre la session principale de cet agent. Les autres formes codent une clé de session immuable de l'une des deux façons.

La forme d'ID court s'applique lorsque le reste de la clé de session, tout ce qui suit `agent:<agentId>:`, se termine par un UUID. `<sessionRef>` est un slug de nom d'affichage optionnel plus un ID court, comme `deploy-monitor-6db92d48`. L'ID court est la partie faisant autorité : au moins huit caractères hexadécimaux minuscules du début de l'UUID final de la clé, avec les tirets UUID omis. Les préfixes plus longs jusqu'à tous les 32 caractères hexadécimaux sont acceptés. Le `sessionId` rotatif de la ligne ne fait pas partie de l'identité de l'URL.

Chaque autre clé utilise la forme de clé littérale. Chaque segment délimité par deux points après `agent:<agentId>:` devient un segment de chemin codé en URL. Par exemple, `agent:main:telegram:12345` devient `/chat/main/telegram/12345`, et `agent:main:cron:nightly:run:8821` devient `/chat/main/cron/nightly/run/8821`.

Les segments de repos littéraux exactement égaux à `.` ou `..` utilisent `~dot` et `~dotdot` afin que les navigateurs ne puissent pas les réduire en tant que segments de chemin relatif. Un segment littéral qui commence par `~` double ce caractère initial pour garder l'encodage réversible. Lorsqu'un repos littéral d'un seul segment pourrait être confondu avec un ID court, le générateur insère `~key` avant lui, par exemple `agent:main:release-deadbeef` devient `/chat/main/~key/release-deadbeef`. Le marqueur force l'interprétation littérale et n'apparaît que lorsque la forme non échappée serait ambiguë.

Les noms de repos littéraux réservés d'un seul segment sont `main`, `global`, `boot` et `sessions`. Le `session.mainKey` configuré rejoint cet ensemble au moment de l'exécution. Exactement un segment après l'ID d'agent est littéral lorsqu'il est réservé ou ne contient pas un ID court valide ; sinon c'est une référence courte. Deux segments ou plus après l'ID d'agent sont toujours littéraux.

Seul le `session.mainKey` configuré s'effondre au chemin de session principale agent uniquement. Avec `session.mainKey: "workspace"`, `agent:research:workspace` devient `/chat/research`, tandis que la clé distincte `agent:research:main` reste le chemin littéral `/chat/research/main`.

### Contrat de stabilité

Les parties suivantes sont des contrats d'URL stables :

- Les mots d'espace de noms `/chat` et `/dashboard`.
- L'ID court UUID de la clé dans les URLs de forme d'ID court.
- L'arité et les règles d'analyse court-versus-littéral ci-dessus.

Sous forme d'ID court, le segment d'agent et le slug sont explicitement décorateurs. Ils peuvent changer sans préavis et ne sont pas utilisés pour identifier ou valider la session. Après résolution, l'interface utilisateur de contrôle remplace la barre d'adresse par l'ID d'agent actuel et le slug de nom d'affichage actuel sans ajouter d'entrée à l'historique du navigateur.

Sous forme de clé littérale, le segment d'agent fait autorité car il fait partie de la clé de session reconstruite. Les segments littéraux restants font également autorité. Un slug, lorsqu'il est présent, est toujours décorateur ; les formes de clé littérale n'en synthétisent pas.

Si un ID court correspond à plus d'une session, l'interface utilisateur ne devine pas. Elle affiche une petite vue de désambiguïsation avec les noms d'affichage correspondants, les agents et les préfixes d'ID plus longs. Utilisez un préfixe plus long pour rendre l'URL unique. La résolution examine au maximum cinq pages de résultats de recherche ; s'il en reste plus, la vue indique que la recherche était incomplète au lieu de deviner.

Les liens canoniques n'utilisent pas `?session=` ou `?face=`. Les liens publiés tels que `/chat?session=<sessionKey>` sont acceptés uniquement à la limite de l'application comme aide à la migration et sont immédiatement réécrits, sans ajouter d'historique du navigateur, au chemin canonique. Le compagnon `?face=dashboard` publié sélectionne l'espace de noms `/dashboard` lors de cette réécriture. Les chargeurs et le code de page ne lisent jamais l'identité du formulaire de requête, et les nouveaux liens ne doivent pas l'émettre. La liste des sessions conserve son propre paramètre `?session=` car ce paramètre développe une ligne ; ce n'est pas un lien profond de session. La valeur du compositeur unique `?draft=` reste prise en charge sur les chemins de session de chat et de tableau de bord.

## Tableau des routes

Ce tableau répertorie chaque route d'application de l'interface utilisateur de contrôle. Un tiret signifie que la route n'a pas de paramètres d'URL spécifiques à la route.

| Page                | Chemin canonique            | Alias                     | Paramètres ou formes dynamiques                  |
| ------------------- | --------------------------- | ------------------------- | ------------------------------------------------ |
| Chat                | `/chat`                     | -                         | Formes de session sauvegardées par clé ci-dessus ; `?draft=<text>`  |
| Tableau de bord      | `/dashboard`                | -                         | Formes de session sauvegardées par clé ci-dessus ; `?draft=<text>`  |
| Demander à OpenClaw | `/custodian`                | -                         | `?intent=new-agent`, `?onboarding=1`             |
| Nouvelle session    | `/new`                      | -                         | `?agent=<agentId>`, `?catalog=<catalogId>`       |
| Activité            | `/activity`                 | -                         | -                                                |
| Applications        | `/apps`                     | -                         | -                                                |
| Agents              | `/settings/agents`          | `/agents`                 | `?agent=<agentId>`                               |
| Canaux              | `/settings/channels`        | `/channels`               | Paramètres de paramètres partagés ci-dessous    |
| Connexion           | `/settings/connection`      | -                         | Paramètres de paramètres partagés ci-dessous    |
| Paramètres généraux | `/settings/general`         | `/config`                 | Paramètres de paramètres partagés ci-dessous    |
| Profil              | `/settings/profile`         | `/profile`                | Paramètres de paramètres partagés ci-dessous    |
| Communications      | `/settings/communications`  | `/communications`         | Paramètres de paramètres partagés ci-dessous    |
| Apparence           | `/settings/appearance`      | `/appearance`             | Paramètres de paramètres partagés ci-dessous    |
| Notifications       | `/settings/notifications`   | -                         | Paramètres de paramètres partagés ci-dessous    |
| Sécurité            | `/settings/security`        | -                         | Paramètres de paramètres partagés ci-dessous    |
| Avancé              | `/settings/advanced`        | -                         | Paramètres de paramètres partagés ci-dessous    |
| Approbations        | `/settings/approvals`       | -                         | Paramètres de paramètres partagés ci-dessous    |
| Paramètres d'automatisation | `/settings/automation`      | `/automation`             | Paramètres de paramètres partagés ci-dessous    |
| MCP                 | `/settings/mcp`             | `/mcp`                    | Paramètres de paramètres partagés ci-dessous    |
| Infrastructure      | `/settings/infrastructure`  | `/infrastructure`         | Paramètres de paramètres partagés ci-dessous    |
| Laboratoires        | `/settings/labs`            | -                         | Paramètres de paramètres partagés ci-dessous    |
| À propos            | `/settings/about`           | -                         | Paramètres de paramètres partagés ci-dessous    |
| IA et agents        | `/settings/ai-agents`       | `/ai-agents`              | Paramètres de paramètres partagés ci-dessous    |
| Configuration du modèle | `/settings/model-setup`     | `/model-setup`            | `?firstRun=1`                                    |
| Fournisseurs de modèles | `/settings/model-providers` | `/model-providers`        | Paramètres de paramètres partagés ci-dessous    |
| Importer la mémoire  | `/memory-import`            | `/settings/memory-import` | -                                                |
| Tableau de travail   | `/workboard`                | -                         | `/workboard/<boardId>`                           |
| Arbres de travail    | `/worktrees`                | `/settings/worktrees`     | -                                                |
| Sessions            | `/sessions`                 | `/settings/sessions`      | `?session=<sessionKey>`, `?status=archived\|all` |
| Utilisation         | `/usage`                    | -                         | -                                                |
| Débogage            | `/debug`                    | -                         | -                                                |
| Journaux            | `/logs`                     | -                         | -                                                |
| Atelier de compétences | `/skills/workshop`          | -                         | -                                                |
| Compétences         | `/skills`                   | -                         | -                                                |
| Plugins             | `/settings/plugins`         | -                         | `?tab=discover\|installed`                       |
| Automatisations     | `/cron`                     | -                         | -                                                |
| Tâches              | `/tasks`                    | -                         | -                                                |
| Appareils           | `/settings/devices`         | `/nodes`                  | Paramètres de paramètres partagés ci-dessous    |
| Hôte d'onglet de plugin | `/plugin`                   | -                         | `?plugin=<pluginId>&id=<tabId>`                  |

Les routes de paramètres qui utilisent des liens profonds sauvegardés par schéma acceptent `?section=<section>`, `?advanced=1` et `#<setting-id>`. Ces valeurs sélectionnent le contenu dans la page ; elles ne modifient pas l'identité de la route.

## Documents spéciaux et modes de démarrage

Ces documents servis par Gateway se situent en dehors du tableau des routes d'application :

- `/?onboarding=1` ouvre la présentation d'intégration à la première exécution.
- `/?view=terminal` ouvre le document terminal uniquement en plein écran utilisé par les applications mobiles. La disponibilité nécessite toujours `gateway.terminal.enabled` et `operator.admin`.
- `/approve/<approvalId>` ouvre un document d'approbation autonome. Avec un chemin de base, utilisez `<basePath>/approve/<approvalId>`. L'ID identifie une approbation mais ne l'autorise jamais ; l'authentification Gateway normale s'applique toujours.

L'espace de noms d'approbation est réservé à l'avance pour les routes HTTP des plugins pour toutes les méthodes HTTP. Lorsque la fourniture de l'interface utilisateur de contrôle est désactivée, elle retourne `404` au lieu de passer à une route de plugin.

## Transfert de passerelle distante

L'interface de développement Vite peut se connecter à une passerelle différente :

```text
http://localhost:5173/?gatewayUrl=ws%3A%2F%2F<gateway-host>%3A18789
http://localhost:5173/?gatewayUrl=wss%3A%2F%2F<gateway-host>%3A18789#token=<gateway-token>
```

Encodez en URL une valeur `ws://` ou `wss://` complète. `gatewayUrl` n'est accepté que dans une fenêtre de niveau supérieur, stocké après le chargement et supprimé de la barre d'adresse. Préférez `#token=` car les fragments n'entrent pas dans les journaux de requêtes HTTP ni dans les en-têtes Referer. Le transfert `?token=` hérité reste une solution de secours pour les identifiants d'amorçage uniquement et est supprimé immédiatement. Les mots de passe restent en mémoire uniquement.

Lorsque `gatewayUrl` sélectionne une autre passerelle, l'interface utilisateur ne revient pas à la configuration locale ou aux identifiants d'environnement. Fournissez explicitement le jeton ou le mot de passe de la passerelle distante, et utilisez `wss://` derrière TLS.

## Connexes

- [Interface de contrôle](/fr/web/control-ui)
- [Tableau de bord](/fr/web/dashboard)
- [Tableaux de bord de session](/fr/web/dashboards)
