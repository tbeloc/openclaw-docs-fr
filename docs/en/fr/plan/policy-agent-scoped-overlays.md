---
summary: "Les overlays de politique par agent sont superposés aux règles de politique globale."
read_when:
  - You are designing per-agent policy requirements
  - You need to distinguish tool posture policy from workspace policy
  - You are configuring stricter policy for one named agent
title: "Overlays de politique à portée d'agent"
---

# Overlays de politique à portée d'agent

La politique OpenClaw supporte les exigences globales et les exigences plus strictes pour
les identifiants d'agent d'exécution explicites. Certains déploiements nécessitent qu'un agent utilise un
espace de travail et une posture d'outil plus serrés que d'autres agents, mais les règles à l'échelle du déploiement ne doivent pas
forcer chaque agent à utiliser la même posture.

Cette page décrit le modèle d'overlay à portée d'agent. La référence des champs reste
[`openclaw policy`](/fr/cli/policy).

## Objectifs de conception

- Maintenir la politique globale comme ligne de base du déploiement.
- Permettre à un agent nommé d'ajouter des exigences plus strictes sans affaiblir les règles globales.
- Réutiliser les formes de section de politique existantes où la preuve peut être attribuée à
  un agent.
- Éviter de faire de `agents.workspace` un second système de permissions d'outils.
- Laisser les vérifications globales uniquement globales jusqu'à ce que leur preuve puisse être mappée à un
  agent.

## Forme

Utilisez `scopes.<scopeName>` pour les portées de politique d'agent nommées à des fins spécifiques. Chaque
portée liste les `agentIds` d'exécution auxquels elle s'applique, puis réutilise la grammaire de section de politique de haut niveau normale où la preuve de la section peut être attribuée à
ces agents. Les sections à portée initiales expédiées sont `tools` et
`agents.workspace` ; sandbox et ingress restent en dehors de cette PR et peuvent rejoindre
le même conteneur une fois que ces PR de politique arrivent et que leur preuve porte l'identité de l'agent. L'inventaire des champs à portée est soutenu par les métadonnées de règle de politique qui
enregistrent la sémantique de rigueur de chaque champ pour la conformité ultérieure du fichier de politique.

```jsonc
{
  "tools": {
    "denyTools": ["process"],
  },
  "agents": {
    "workspace": {
      "allowedAccess": ["none", "ro"],
    },
  },
  "scopes": {
    "release-agent-lockdown": {
      "agentIds": ["release-agent"],
      "agents": {
        "workspace": {
          "allowedAccess": ["none", "ro"],
        },
      },
      "tools": {
        "profiles": { "allow": ["minimal", "messaging"] },
        "fs": { "requireWorkspaceOnly": true },
        "exec": {
          "allowSecurity": ["deny", "allowlist"],
          "requireAsk": ["always"],
          "allowHosts": ["sandbox"],
        },
        "elevated": { "allow": false },
        "alsoAllow": { "expected": ["message", "read"] },
        "denyTools": ["exec", "process", "write", "edit", "apply_patch"],
      },
    },
  },
}
```

`agents.workspace` reste la ligne de base d'espace de travail existante pour tous les agents.
`scopes.<scopeName>` est un overlay à portée, pas un remplacement de la politique globale. Le nom de la portée est descriptif uniquement ; la correspondance utilise `agentIds`, pas
les noms d'affichage. Il contient délibérément des noms de section normaux au lieu d'une
mini-grammaire par agent personnalisée.
Chaque portée présente dans `policy.jsonc` doit être valide et applicable. Dans cette
PR, le seul sélecteur supporté est `agentIds`, et il supporte uniquement `tools.*`
et `agents.workspace.*`.

## Sémantique de superposition

L'évaluation de la politique est additive :

1. La politique de haut niveau s'applique à toutes les preuves correspondantes.
2. Le `agents.workspace` existant s'applique aux valeurs par défaut et à chaque agent listé.
3. `scopes.<scopeName>` s'applique aux preuves pour chaque identifiant d'exécution normalisé
   dans `agentIds`.
4. Plusieurs blocs de portée peuvent cibler le même agent lorsqu'ils gouvernent
   des champs différents, ou lorsqu'une valeur ultérieure pour le même champ est également ou
   plus restrictive selon les métadonnées de politique.
5. Un overlay d'agent nommé peut renforcer la politique, mais il ne peut pas rendre acceptable une
   violation globale.

Si les règles globales et à portée d'agent échouent toutes les deux, les résultats doivent pointer vers la règle
qui a été violée :

```text
oc://policy.jsonc/tools/denyTools
oc://policy.jsonc/scopes/release-agent-lockdown/tools/denyTools
oc://policy.jsonc/scopes/release-agent-lockdown/agents/workspace/allowedAccess
```

Cela maintient la posture d'outil large, la posture d'outil d'agent nommé et la posture d'espace de travail
auditables comme des exigences séparées même lorsqu'elles observent les mêmes champs de configuration.

Les affirmations de liste exacte telles que `tools.alsoAllow.expected` comparent la liste configurée
à la liste attendue et signalent à la fois les entrées attendues manquantes et les entrées supplémentaires inattendues. Ceci est destiné à la posture additive telle que `alsoAllow`, où
une entrée supplémentaire peut élargir un agent au-delà de son rôle examiné.

## Superposition de politique et de configuration

Le modèle d'overlay sépare l'endroit où la politique est créée de l'endroit où la configuration OpenClaw
est observée :

| Portée de politique                     | Configuration observée                                 | S'applique à                      | Résultat exemple                                                                                                      |
| --------------------------------------- | ------------------------------------------------------ | --------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `tools.*` de haut niveau                | `tools.*` global et posture d'outil d'agent hérité     | Tous les agents utilisant la posture correspondante | Refuser l'hôte exec `gateway` pour chaque agent sauf si la politique globale le permet.                               |
| `tools.*` de haut niveau                | Remplacements `agents.list[].tools.*`                 | Tout agent avec un remplacement   | Signaler un agent qui remplace `tools.exec.host` par une valeur non approuvée.                                       |
| `scopes.<scopeName>.tools.*`            | Entrée `agents.list[]` correspondante et posture héritée | Uniquement cet agent nommé        | Permettre à la plupart des agents d'utiliser l'hôte exec `node` tandis qu'un agent doit utiliser uniquement `sandbox`. |
| `agents.workspace`                      | Posture d'espace de travail par défaut et de chaque agent listé | Valeurs par défaut et tous les agents listés | Exiger que chaque accès à l'espace de travail de l'agent soit `none` ou `ro`.                                         |
| `scopes.<scopeName>.agents.workspace.*` | Posture d'espace de travail `agents.list[]` correspondante | Uniquement cet agent nommé        | Exiger qu'un agent soit en lecture seule sans exiger la même chose pour `main`.                                       |

Les overlays par agent sont additifs. Une règle d'agent nommé peut être plus stricte que la
règle de haut niveau, mais elle ne peut pas rendre acceptable une violation globale. Pour les règles de liste d'autorisation, l'ensemble autorisé effectif est l'intersection de la règle globale et de l'
overlay d'agent nommé lorsque les deux sont présents.

Par exemple, si `tools.exec.allowHosts` de haut niveau permet `["sandbox", "node"]`
et `scopes.release-agent-lockdown.tools.exec.allowHosts` permet uniquement
`["sandbox"]`, `release-agent` échoue lorsque son hôte exec effectif est `node` ;
un autre agent peut toujours réussir
avec `node`.

## Posture d'outil par rapport à posture d'espace de travail

La posture d'outil appartient sous `tools` car elle décrit quel comportement d'outil une
configuration peut exposer. La politique `tools.*` existante observe à la fois la configuration
`tools.*` globale et les remplacements `agents.list[].tools.*` par agent.

La posture d'espace de travail appartient sous `workspace` car elle décrit le mode sandbox
et l'accès à l'espace de travail. La section d'espace de travail ne doit pas se transformer en espace de noms de politique d'outil général. Si un agent a besoin de restrictions d'outil plus strictes pour rendre sa
posture d'espace de travail significative, mettez ces restrictions dans le même overlay d'agent
sous `scopes.<scopeName>.tools`.

Pour un agent de version restreint, la division prévue est :

```jsonc
{
  "scopes": {
    "release-agent-lockdown": {
      "agentIds": ["release-agent"],
      "agents": {
        "workspace": { "allowedAccess": ["none", "ro"] },
      },
      "tools": {
        "denyTools": ["exec", "process", "write", "edit", "apply_patch"],
      },
    },
  },
}
```

## Admissibilité de la section

Une section à portée d'agent ne doit être ajoutée que lorsque la preuve de politique porte un
identifiant d'agent ou peut être attribuée à un sans deviner.

| Section     | Statut initial à portée d'agent | Raison                                                                                    |
| ----------- | ------------------------------- | ----------------------------------------------------------------------------------------- |
| `workspace` | Inclure                         | La preuve d'espace de travail/sandbox d'agent a déjà l'identité de l'agent.               |
| `tools`     | Inclure                         | La preuve de posture d'outil inclut la configuration d'outil globale et par agent.        |
| `sandbox`   | Suivi du pipeline               | Garder en dehors jusqu'à ce que la PR de posture sandbox arrive et que la preuve soit scoped. |
| `ingress`   | Suivi du pipeline               | Garder en dehors jusqu'à ce que la posture ingress/channel arrive avec l'attribution d'agent. |
| `models`    | Inclure lorsque mappé           | Les références de modèle sélectionnées peuvent être spécifiques à l'agent.                |
| `mcp`       | Inclure lorsque mappé           | Utiliser uniquement lorsque la preuve du serveur MCP est attribuable à un agent.         |
| `auth`      | Différer                        | Les métadonnées du profil d'authentification sont un catalogue de configuration sauf si la liaison d'agent est claire. |
| `channels`  | Différer                        | La posture du fournisseur de canal est au niveau du déploiement jusqu'à ce que le routage soit scoped. |
| `gateway`   | Garder global                   | La posture d'exposition/auth/http de la passerelle est au niveau du processus.            |
| `network`   | Garder global                   | La posture SSRF du réseau privé est au niveau du runtime.                                |
| `secrets`   | Garder global d'abord           | La posture du fournisseur de secret est partagée sauf si les références sont attribuées à l'agent. |

## Compatibilité

L'implémentation est additive :

- garder tous les champs de politique de haut niveau existants valides ;
- garder la sémantique `agents.workspace` inchangée ;
- valider `scopes` avant d'évaluer les règles à portée ;
- rejeter clairement les sections à portée non supportées jusqu'à ce que leur preuve et leur contrat de politique soient implémentés ;
- ne pas réinterpréter `tools.requireMetadata` de haut niveau comme à portée d'agent, car les métadonnées d'outil décrivent le catalogue d'outils d'espace de travail déclaré ;
- inclure la preuve à portée d'agent dans le hash d'attestation lorsqu'une règle à portée est présente.

Cela permet à la posture d'outil large de rester un contrat de politique de haut niveau tandis que les agents nommés ajoutent des affirmations observables plus strictes sans affaiblir la ligne de base globale.
