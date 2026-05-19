---
summary: "Plan de migration pour rendre explicite la propriété des sessions ACP et des processus ACPX"
read_when:
  - Refactorisation du cycle de vie des sessions ACP ou nettoyage des processus ACPX
  - Débogage des processus orphelins ACPX, réutilisation de PID ou sécurité du nettoyage multi-passerelle
  - Modification de la visibilité sessions_list pour les sessions ACP ou subagent générées
  - Conception de métadonnées de propriété pour les tâches de fond, les sessions ACP ou les baux de processus
title: "Refactorisation du cycle de vie ACP"
sidebarTitle: "Refactorisation du cycle de vie ACP"
---

Le cycle de vie ACP fonctionne actuellement, mais trop de celui-ci est déduit après coup.
Le nettoyage des processus reconstruit la propriété à partir des PID, des chaînes de commande, des
chemins d'enveloppe et de la table des processus actifs. La visibilité des sessions reconstruit la propriété
à partir des chaînes de clé de session plus les recherches secondaires `sessions.list({ spawnedBy })`.
Cela rend les corrections étroites possibles, mais cela rend aussi les cas limites faciles à manquer :
la réutilisation de PID, les commandes entre guillemets, les petits-enfants d'adaptateur, les racines d'état multi-passerelle,
`cancel` versus `close`, et la visibilité `tree` versus `all` deviennent tous des endroits séparés pour redécouvrir les mêmes règles de propriété.

Cette refactorisation rend la propriété de première classe. L'objectif n'est pas une nouvelle surface de produit ACP ;
c'est un contrat interne plus sûr pour le comportement ACP et ACPX existant.

## Objectifs

- Le nettoyage ne signale jamais un processus à moins que la preuve actuelle en direct ne corresponde à un
  bail détenu par OpenClaw.
- `cancel`, `close` et le nettoyage au démarrage ont des intentions de cycle de vie distinctes.
- `sessions_list`, `sessions_history`, `sessions_send` et les vérifications d'état utilisent
  le même modèle de session détenue par le demandeur.
- Les installations multi-passerelle ne peuvent pas nettoyer les enveloppes ACPX les unes des autres.
- Les anciens enregistrements de session ACPX continuent de fonctionner pendant la migration.
- Le runtime reste détenu par le plugin ; le noyau n'apprend pas les détails du package ACPX.

## Non-objectifs

- Remplacer ACPX ou modifier la surface de commande publique `/acp`.
- Déplacer le comportement de l'adaptateur ACP spécifique au fournisseur dans le noyau.
- Exiger que les utilisateurs nettoient manuellement l'état avant la mise à niveau.
- Faire en sorte que `cancel` ferme les sessions ACP réutilisables.

## Modèle cible

### Identité de l'instance de passerelle

Chaque processus Gateway devrait avoir un identifiant d'instance runtime stable :

```ts
type GatewayInstanceId = string;
```

Il peut être généré au démarrage de Gateway et conservé dans l'état pour la durée de vie de
cette installation. Ce n'est pas un secret de sécurité ; c'est un discriminateur de propriété utilisé
pour éviter de confondre les processus ACP d'une Gateway avec les processus d'une autre Gateway.

### Propriété de la session ACP

Chaque session ACP générée devrait avoir des métadonnées de propriété normalisées :

```ts
type AcpSessionOwner = {
  sessionKey: string;
  spawnedBy?: string;
  parentSessionKey?: string;
  ownerSessionKey: string;
  agentId: string;
  backend: "acpx";
  gatewayInstanceId: GatewayInstanceId;
  createdAt: number;
};
```

La Gateway devrait retourner ces champs sur les lignes de session où ils sont connus.
Le filtrage de visibilité devrait être une vérification pure sur les métadonnées de ligne :

```ts
canSeeSessionRow({
  row,
  requesterSessionKey,
  visibility,
  a2aPolicy,
});
```

Cela supprime les appels secondaires `sessions.list({ spawnedBy })` cachés des
vérifications de visibilité. Un enfant ACP cross-agent généré est détenu par le demandeur parce que
la ligne le dit, pas parce qu'une deuxième requête le trouve par hasard.

### Baux de processus ACPX

Chaque lancement d'enveloppe généré devrait créer un enregistrement de bail :

```ts
type AcpxProcessLease = {
  leaseId: string;
  gatewayInstanceId: GatewayInstanceId;
  sessionKey: string;
  wrapperRoot: string;
  wrapperPath: string;
  rootPid: number;
  processGroupId?: number;
  commandHash: string;
  startedAt: number;
  state: "open" | "closing" | "closed" | "lost";
};
```

Le processus d'enveloppe devrait recevoir l'identifiant de bail et l'identifiant d'instance de passerelle dans son
environnement :

```sh
OPENCLAW_ACPX_LEASE_ID=...
OPENCLAW_GATEWAY_INSTANCE_ID=...
```

Quand la plateforme le permet, la vérification devrait préférer les métadonnées de processus actifs
qui ne peuvent pas être confondues par les guillemets de commande :

- le PID racine existe toujours
- le chemin d'enveloppe actif est sous `wrapperRoot`
- le groupe de processus correspond au bail quand disponible
- l'environnement contient l'identifiant de bail attendu quand lisible
- le hash de commande ou le chemin exécutable correspond au bail

Si le processus actif ne peut pas être vérifié, le nettoyage échoue fermé.

## Contrôleur de cycle de vie

Introduire un contrôleur de cycle de vie ACPX qui possède les baux de processus et la politique de nettoyage :

```ts
interface AcpxLifecycleController {
  ensureSession(input: AcpRuntimeEnsureInput): Promise<AcpRuntimeHandle>;
  cancelTurn(handle: AcpRuntimeHandle): Promise<void>;
  closeSession(input: {
    handle: AcpRuntimeHandle;
    discardPersistentState?: boolean;
    reason?: string;
  }): Promise<void>;
  reapStartupOrphans(): Promise<void>;
  verifyOwnedTree(lease: AcpxProcessLease): Promise<OwnedProcessTree | null>;
}
```

`cancelTurn` demande uniquement l'annulation du tour. Il ne doit pas nettoyer les processus d'enveloppe
ou d'adaptateur réutilisables.

`closeSession` est autorisé à nettoyer, mais seulement après avoir chargé l'enregistrement de session,
chargé le bail et vérifié que l'arborescence des processus actifs appartient toujours à ce
bail.

`reapStartupOrphans` commence par les baux ouverts dans l'état. Il peut utiliser la table des processus
pour trouver les descendants, mais il ne devrait pas scanner d'abord les commandes ressemblant à ACP arbitraires
puis décider qu'elles sont probablement les nôtres.

## Contrat d'enveloppe

Les enveloppes générées doivent rester petites. Elles doivent :

- démarrer l'adaptateur dans un groupe de processus où supporté
- transférer les signaux de terminaison normaux au groupe de processus
- détecter la mort du parent
- à la mort du parent, envoyer SIGTERM, puis garder l'enveloppe vivante jusqu'à ce que le
  fallback SIGKILL s'exécute
- signaler le PID racine et l'identifiant du groupe de processus au contrôleur de cycle de vie quand
  c'est disponible

Les enveloppes ne doivent pas décider de la politique de session. Elles appliquent uniquement le nettoyage local des arbres de processus
pour leur propre groupe d'adaptateur.

## Contrat de visibilité de session

La visibilité devrait utiliser la propriété de ligne normalisée :

```ts
type SessionVisibilityInput = {
  requesterSessionKey: string;
  row: {
    key: string;
    agentId: string;
    ownerSessionKey?: string;
    spawnedBy?: string;
    parentSessionKey?: string;
  };
  visibility: "self" | "tree" | "agent" | "all";
  a2aPolicy: AgentToAgentPolicy;
};
```

Règles :

- `self` : uniquement la session du demandeur.
- `tree` : session du demandeur plus les lignes détenues par ou générées à partir du demandeur.
- `all` : toutes les lignes du même agent, les lignes cross-agent autorisées par a2a, et les lignes
  cross-agent générées détenues par le demandeur même quand a2a général est désactivé.
- `agent` : même agent uniquement, sauf si une relation de propriété explicite dit que la ligne
  appartient au demandeur.

Cela rend `tree` et `all` monotones : `all` ne doit pas masquer un enfant détenu que
`tree` montrerait.

## Plan de migration

### Phase 1 : Ajouter l'identité et les baux

- Ajouter `gatewayInstanceId` à l'état de Gateway.
- Ajouter un magasin de bail ACPX sous le répertoire d'état ACPX.
- Écrire un bail avant de générer une enveloppe.
- Stocker `leaseId` sur les nouveaux enregistrements de session ACPX.
- Conserver les champs PID et commande existants pour les anciens enregistrements.

### Phase 2 : Nettoyage basé sur les baux

- Modifier le nettoyage de fermeture pour charger `leaseId` en premier.
- Vérifier la propriété du processus actif par rapport au bail avant de signaler.
- Conserver le PID racine actuel et le fallback wrapper-root uniquement pour les enregistrements hérités.
- Marquer les baux `closed` après nettoyage vérifié.
- Marquer les baux `lost` quand le processus est parti avant le nettoyage.

### Phase 3 : Nettoyage au démarrage basé sur les baux

- Le nettoyage au démarrage scanne les baux ouverts.
- Pour chaque bail, vérifier le processus racine et collecter les descendants.
- Nettoyer les arbres vérifiés enfants-d'abord.
- Expirer les anciens baux `closed` et `lost` avec une fenêtre de rétention limitée.
- Conserver le balayage de marqueur de commande uniquement comme fallback hérité temporaire, gardé par
  la racine d'enveloppe et l'instance de Gateway où possible.

### Phase 4 : Lignes de propriété de session

- Ajouter des métadonnées de propriété aux lignes de session Gateway.
- Enseigner aux rédacteurs ACPX, subagent, background-task et session-store de remplir
  `ownerSessionKey` ou `spawnedBy`.
- Convertir les vérifications de visibilité de session pour utiliser les métadonnées de ligne.
- Supprimer les recherches secondaires `sessions.list({ spawnedBy })` au moment de la visibilité.

### Phase 5 : Supprimer les heuristiques héritées

Après une fenêtre de version :

- arrêter de s'appuyer sur les chaînes de commande racine stockées pour le nettoyage ACPX non-hérité
- supprimer les balayages de marqueur de commande au démarrage
- supprimer les recherches de fallback de visibilité
- conserver le comportement défensif fail-closed pour les baux manquants ou non vérifiables

## Tests

Ajouter deux suites table-driven.

Simulateur de cycle de vie de processus :

- PID réutilisé par un processus non lié
- PID réutilisé par la racine d'enveloppe d'une autre Gateway
- la commande d'enveloppe stockée est shell-quoted, la commande `ps` actuelle ne l'est pas
- l'enfant d'adaptateur se termine, le petit-enfant reste dans le groupe de processus
- le fallback SIGTERM de mort du parent atteint SIGKILL
- la liste des processus indisponible
- bail obsolète avec processus manquant
- orphelin au démarrage avec enveloppe, enfant d'adaptateur et petit-enfant

Matrice de visibilité de session :

- `self`, `tree`, `agent`, `all`
- a2a activé et désactivé
- ligne du même agent
- ligne cross-agent
- ligne ACP cross-agent générée détenue par le demandeur
- demandeur en sandbox limité à `tree`
- actions list, history, send et status

L'invariant important : un enfant généré détenu par le demandeur est visible partout où
la visibilité configurée inclut l'arborescence de session du demandeur, et `all` n'est pas
moins capable que `tree`.

## Notes de compatibilité

Les anciens enregistrements de session peuvent ne pas avoir `leaseId`. Ils doivent utiliser le chemin de nettoyage hérité
fail-closed :

- exiger un processus racine actif
- exiger la propriété wrapper-root quand une enveloppe générée est attendue
- exiger l'accord de commande pour les racines non-enveloppe
- ne jamais signaler basé uniquement sur les métadonnées de PID stockées obsolètes

Si un enregistrement hérité ne peut pas être vérifié, le laisser tranquille. Le nettoyage de bail au démarrage et
la fenêtre de version suivante devraient éventuellement retirer le fallback.

## Critères de succès

- Fermer une session ACPX ancienne ou obsolète ne peut pas tuer le processus d'une autre Gateway.
- La mort du parent ne laisse pas les petits-enfants d'adaptateur obstinés en cours d'exécution.
- `cancel` abandonne le tour actif sans fermer les sessions réutilisables.
- `sessions_list` peut montrer les enfants ACP cross-agent détenus par le demandeur sous
  `tree` et `all`.
- Le nettoyage au démarrage est piloté par les baux, pas par les balayages de chaîne de commande larges.
- Les tests de matrice de processus et de visibilité ciblés couvrent tous les cas limites qui
  nécessitaient auparavant des corrections d'examen ponctuelles.
