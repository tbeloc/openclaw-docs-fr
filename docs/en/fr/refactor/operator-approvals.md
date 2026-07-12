---
summary: "Concevoir des approbations durables et profondément liables sur Control UI, les applications natives, les canaux et les sessions parentes"
read_when:
  - Changing exec or plugin approval lifecycle, storage, protocol, or authorization
  - Adding approval links or native approval controls to a channel
  - Projecting child-session approvals into parent or orchestrator views
title: "Approbations d'opérateur multi-surface"
---

# Approbations d'opérateur multi-surface

Cette conception suit [#103505](https://github.com/openclaw/openclaw/issues/103505). Elle remplace l'autorité d'approbation locale au processus par un cycle de vie détenu par la Gateway et sauvegardé par SQLite. Chaque approbation d'exec ou de plugin/outil détenue par la Gateway obtient un ID stable, une route Control UI authentifiée, une résolution atomique du premier-répondant-gagne, et des projections réservées aux opérateurs vers ses flux de session source et ancêtres.

Les actions en ligne et les liens profonds coexistent. Il n'y a pas de basculement de mode d'approbation.

## Objectifs

- Un objet d'approbation durable pour les portes exec et plugin/outil.
- Route stable `${controlUiBasePath}/approve/{approvalId}`.
- Résolution depuis n'importe quelle surface Control UI, application native ou canal autorisée.
- Comportement atomique du premier-répondant-gagne sur les surfaces concurrentes.
- Tentatives identiques idempotentes ; les réponses tardives conflictuelles ne peuvent pas écraser le gagnant.
- Délai d'expiration, verdicts de confiance malformés, routes manquantes, annulation et redémarrage échouent fermés.
- Les événements demandés et terminaux atteignent la session source et tous les propriétaires parents/orchestrateurs pertinents.
- Les canaux reçoivent des actions d'approbation et de navigation typées ; les données de rappel de transport restent privées au canal.
- Les méthodes Gateway exec/plugin existantes restent compatibles tandis que leur implémentation converge vers un seul service.

## Non-objectifs

- Persister ou reprendre l'exécution de l'outil bloqué lui-même sur le redémarrage de la Gateway.
- Faire d'un ID d'approbation ou d'une URL une credential de porteur.
- Ajouter des invites d'approbation aux transcriptions visibles par le modèle ou réveiller les agents parents.
- Déplacer la politique d'approbation, les commandes de produit ou l'autorisation du réviseur dans les plugins de canal.
- Cloner l'état d'approbation par canal, appareil ou ancêtre.
- Redessiner les listes blanches exec, la composition de la politique de plugin ou la persistance `allow-always` sauf si nécessaire pour rendre les résultats terminaux sans ambiguïté.
- Rendre une TUI intégrée sans gateway à distance accessible dans le premier incrément. Elle reste locale uniquement et doit échouer fermée quand aucun réviseur n'existe.

## Système existant et carte des preuves

| Surface           | Point d'entrée et propriétaire actuels                                                                                                                        | Comportement et lacune actuels                                                                                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent exec        | `src/agents/bash-tools.exec-approval-request.ts`, `src/agents/bash-tools.exec-host-shared.ts`                                                                   | L'enregistrement en deux phases `exec.approval.*` empêche une course `/approve` précoce, mais le délai d'expiration peut toujours devenir allow via `askFallback`.                            |
| Porte outil plugin  | `src/agents/agent-tools.before-tool-call.ts`                                                                                                                    | Demande `plugin.approval.*` ; `timeoutBehavior: "allow"` peut approuver une porte expirée. Le mode intégré a une autorité locale au processus séparée dans `src/infra/embedded-plugin-approval-broker.ts`. |
| Porte nœud plugin  | `src/gateway/node-invoke-plugin-policy.ts`                                                                                                                      | Crée et diffuse directement via le gestionnaire de plugin, dupliquant une partie du cycle de vie de la méthode serveur.                                                                     |
| Autorité Gateway | `src/gateway/server-aux-handlers.ts`, `src/gateway/exec-approval-manager.ts`, `src/gateway/server-methods/approval-shared.ts`                                   | Les gestionnaires exec et plugin séparés utilisent des cartes locales au processus. Les entrées terminales survivent pendant 15 secondes. Le premier-répondant-gagne ne tient que dans un seul processus.                                          |
| Protocole Gateway  | `packages/gateway-protocol/src/schema/exec-approvals.ts`, `packages/gateway-protocol/src/schema/plugin-approvals.ts`, `src/gateway/methods/core-descriptors.ts` | Exec a `get` en attente uniquement ; plugin n'a pas de `get` ; aucune recherche terminale agnostique au type n'existe pour un lien profond.                                                  |
| Livraison          | `src/infra/exec-approval-channel-runtime.ts`, `src/infra/approval-native-runtime.ts`, `src/infra/approval-handler-runtime.ts`                                   | Supporte le routage d'origine, les DM approbateurs, la relecture en attente, les gestionnaires natifs et le nettoyage terminal en processus. PR 5 ajoute la réconciliation terminale durable.  |
| Actions portables  | `src/interactive/payload.ts`, `src/plugin-sdk/interactive-runtime.ts`, `src/plugin-sdk/approval-reply-runtime.ts`                                               | Les boutons d'approbation sont des actions de commande contenant `/approve ...` ; les cibles URL et Web App sont des champs de bouton non typés.                                              |
| Telegram          | `extensions/telegram/src/approval-handler.runtime.ts`, `extensions/telegram/src/button-types.ts`                                                                | Le moteur de rendu analyse le texte de commande pour reconnaître la sémantique d'approbation avant de produire des données de rappel privées.                                                |
| Control UI        | `ui/src/app/exec-approval.ts`, `ui/src/app/overlays.ts`, `ui/src/components/exec-approval.ts`                                                                   | L'interface d'approbation est une modale globale. `ui/src/app-route-paths.ts` et `ui/src/app-routes.ts` utilisent des routes exactes et réécrivent les chemins inconnus en Chat.              |
| Propriété de session | `src/agents/subagent-registry.types.ts`, `src/agents/subagent-registry-read.ts`, `src/config/sessions/types.ts`                                                 | Le contrôleur, le demandeur, le parent explicite et la propriété de génération héritée existent, mais les événements d'approbation ne sont pas projetés sur ces flux de session.            |
| État partagé      | `src/state/openclaw-state-schema.sql`, `src/state/openclaw-state-db.ts`                                                                                         | Les transactions immédiates existantes et les mises à jour conditionnelles Kysely supportent la comparaison-et-ensemble durable dans `state/openclaw.sqlite`.                                |

Les tests actuels représentatifs incluent `src/gateway/exec-approval-manager.test.ts`, `src/gateway/server-methods/approval-shared.test.ts`, `src/agents/bash-tools.exec-gateway-approval.e2e.test.ts`, `extensions/telegram/src/approval-handler.runtime.test.ts`, et `ui/src/e2e/approval-flow.e2e.test.ts`.

Le SDK de plugin reste la seule limite canal/plugin. Les modifications du runtime d'approbation et de présentation doivent être exportées via les sous-chemins existants `src/plugin-sdk/approval-*.ts` et `src/plugin-sdk/interactive-runtime.ts` ; le code de production du plugin ne doit pas importer les internes de Gateway.

## Art antérieur

Omnigent fournit une UX et une sémantique d'échec utiles :

- [`approval.py`](https://github.com/omnigent-ai/omnigent/blob/46e3cd9754c3b8567f7b09f4d19b6249dabe0e80/omnigent/runtime/policies/approval.py) gare ASK, applique des délais d'expiration par politique, et traite uniquement une acceptation exacte comme approbation.
- [`sessions.py`](https://github.com/omnigent-ai/omnigent/blob/46e3cd9754c3b8567f7b09f4d19b6249dabe0e80/omnigent/server/routes/sessions.py) contient la porte du harnais natif côté serveur et la projection de demande/résolution d'ancêtre.
- [`ApprovePage.tsx`](https://github.com/omnigent-ai/omnigent/blob/46e3cd9754c3b8567f7b09f4d19b6249dabe0e80/web/src/pages/ApprovePage.tsx) fournit la page d'approbation mobile autonome.

Ne copiez pas sa réclamation de stockage sans critique. L'état en attente actif actuel est local au processus dans [`_elicitation_registry.py`](https://github.com/omnigent-ai/omnigent/blob/46e3cd9754c3b8567f7b09f4d19b6249dabe0e80/omnigent/server/_elicitation_registry.py), et la table en attente inutilisée est supprimée par [`e3b1f2a4c9d7_drop_pending_tool_calls_table.py`](https://github.com/omnigent-ai/omnigent/blob/46e3cd9754c3b8567f7b09f4d19b6249dabe0e80/omnigent/db/migrations/versions/e3b1f2a4c9d7_drop_pending_tool_calls_table.py). OpenClaw va délibérément plus loin : SQLite est autoritaire et chaque transition terminale est une comparaison-et-ensemble de base de données.

## Architecture et propriété

La Gateway possède le cycle de vie :

1. Un agent, un hook de plugin ou une politique de nœud fournit une demande spécifique au type et une liaison d'exécution locale au processus.
2. La Gateway la valide et construit une projection de réviseur assainie.
3. Le service d'approbation calcule une audience source/propriétaire, insère la ligne canonique, puis enregistre l'attente en processus.
4. Après insertion durable, la Gateway publie les événements d'approbation existants, les projections de session, les notifications de canal et la notification native.
5. Chaque surface se résout via le même service.
6. Le service valide une transition terminale, réveille l'attente du runtime et publie les projections terminales.
7. Un échec de livraison d'événement ne revient jamais sur la décision validée ; les clients se rétablissent via `approval.get` ou la relecture de liste.

Limites de propriété :

- `src/gateway/` : service d'approbation, autorisation, adaptateurs RPC, construction d'URL, cycle de vie d'attente et publication d'événements.
- `src/state/` : schéma partagé et types Kysely générés.
- `src/infra/` : modèles de vue d'approbation assainis et construction de présentation portable.
- `src/agents/` : demande, attente et application du verdict retourné ; pas de persistance.
- `src/channels/` et `extensions/*` : rendre les actions typées, autoriser les utilisateurs de canal, encoder les rappels privés et mettre à jour les contrôles livrés.
- `src/plugin-sdk/` : contrats d'approbation et de présentation publics uniquement.
- `ui/` : page autonome et clients de file d'attente/modale existants.

L'attente en processus est un mécanisme de notification, pas une autorité. L'enregistrement insère la ligne et installe l'attente de manière synchrone avant de publier la demande, donc un résolveur ne peut pas s'entrelacer entre ces étapes. Chaque résolveur ultérieur valide via SQLite avant de régler cette attente.

## Enregistrement persistant

Ajoutez une table `operator_approvals` à la base de données d'état partagée.

| Colonne                                    | Objectif                                                                                                                                       |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `approval_id`                              | ID canonique globalement unique. Conservez les ID exec existants et les ID `plugin:` pour la compatibilité du protocole, mais ne déduisez jamais le type du préfixe. |
| `resolution_ref`                           | Localisateur base64url SHA-256 complet unique pour les rappels de transport qui ne peuvent pas porter l'ID canonique. Ce n'est pas une autorisation ou un ID d'URL public. |
| `kind`                                     | Discriminateur fermé `exec \| plugin`.                                                                                                        |
| `status`                                   | État fermé `pending \| allowed \| denied \| expired \| cancelled`.                                                                          |
| `presentation_json`                        | Projection du relecteur validée et marquée par type. Les demandes d'exécution brutes, les liaisons de commande et les charges utiles de rappel restent locales au processus. |
| `source_agent_id`, `source_session_key`    | Ancrage de projection d'identité source et de session. La clé de session est durable ; l'UUID de session rotatif ne l'est pas.                |
| `audience_session_keys_json`                | Tableau JSON ordonné et dédupliqué produit par la marche de propriété en largeur d'abord bornée. Les événements demandés et terminaux utilisent le même instantané. |
| `requested_by_device_id`, `requested_by_client_id` | Métadonnées durables du demandeur/audit. L'ID de connexion reste en mémoire et n'est pas un principal inter-surfaces. |
| `reviewer_device_ids_json`                 | Appareils relecteurs explicitement ciblés fournis uniquement par l'exécution d'approbation de confiance. |
| `runtime_epoch`                            | Époque de processus qui possède l'exécution garée ; utilisée pour annuler les lignes orphelines après redémarrage. |
| `created_at_ms`, `expires_at_ms`, `updated_at_ms` | Minutage faisant autorité.                                                                                                                   |
| `decision`                                 | Décision utilisateur explicite quand elle existe.                                                                                            |
| `terminal_reason`                          | Raison fermée telle que `user`, `timeout`, `malformed-verdict`, `no-route`, `run-aborted` ou `gateway-restart`. |
| `resolved_at_ms`, `resolver_kind`, `resolver_id` | Gagnant et identité d'audit conservés côté serveur. Les projections du relecteur omettent les identifiants bruts du résolveur. |
| `consumed_at_ms`, `consumed_by`            | Garde de relecture séparée pour `allow-once` ; la consommation ne doit pas effacer la décision enregistrée. |

Index requis :

- `(resolution_ref)` unique ; les insertions rejettent également l'ambiguïté entre colonnes `approval_id`/`resolution_ref`
- `(status, expires_at_ms)`
- `(source_session_key, created_at_ms DESC)`
- `(resolved_at_ms)` pour l'élagage de rétention

Les tableaux d'audience sont petits et bornés. La relecture filtrée par session sélectionne d'abord les lignes en attente visibles via Kysely, puis décode et filtre les tableaux d'audience bornés dans le code d'application ; elle n'utilise pas la correspondance de chaîne ou les requêtes JSON SQL brutes.

Conservez les lignes terminales pendant 30 jours, alignées avec la rétention des métadonnées d'audit dans `src/audit/audit-event-store.ts`. L'élagage est une politique de maintenance fixe, pas une nouvelle surface de configuration. La base de données est un état du plan de contrôle local privé, mais les API du relecteur ne doivent jamais exposer la demande stockée complète ou la liaison d'exécution.

## Machine d'état et compare-and-set

Seules ces transitions sont valides :

- `pending -> allowed` : `allow-once` ou `allow-always` explicite.
- `pending -> denied` : refus explicite, verdict terminal malformé de confiance ou aucune route de livraison.
- `pending -> expired` : délai faisant autorité atteint.
- `pending -> cancelled` : abandon d'exécution, arrêt gracieux ou récupération d'orphelin de redémarrage.

Chaque état terminal non autorisé a un verdict de refus effectif.

La résolution utilise une transaction SQLite immédiate et une mise à jour conditionnelle Kysely équivalente à :

```sql
UPDATE operator_approvals
SET status = ?, decision = ?, terminal_reason = ?, resolved_at_ms = ?
WHERE approval_id = ?
  AND status = 'pending'
  AND expires_at_ms > ?;
```

Si la mise à jour n'affecte aucune ligne, la même transaction lit l'enregistrement :

- Manquant ou non autorisé : retourner non trouvé ; ne révélez pas l'existence.
- Toujours en attente mais délai atteint : comparez-le et définissez-le sur `expired`, puis retournez cette ligne terminale.
- Même décision enregistrée : retourner le succès idempotent avec le gagnant enregistré.
- Décision différente : l'API unifiée retourne `applied: false` avec le gagnant enregistré ; les adaptateurs hérités conservent `APPROVAL_ALREADY_RESOLVED` où requis par leur contrat expédié.
- Tout état terminal : ne le mutez jamais.

`now == expires_at_ms` est expiré. L'heure de la passerelle fait autorité.

L'exécution `allow-once` utilise un deuxième CAS sur `consumed_at_ms IS NULL`, lié au contexte exact de commande/exécution système existant. La ligne d'approbation reste un enregistrement d'audit après consommation.

L'entrée HTTP/RPC malformée qui ne peut pas être authentifiée ou identifier une approbation est rejetée sans mutation et ne peut jamais approuver. Un verdict terminal malformé reçu d'un harnais/attente de confiance pour une approbation connue passe à `denied`.

## API de passerelle

Ajoutez des méthodes de relecteur indépendantes du type :

| Méthode                                   | Contrat                                                                                                                                                                                                            |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `approval.get { id }`                     | Retourne une projection en attente visible ou terminale conservée.                                                                                                                                                 |
| `approval.resolve { id, kind, decision }` | Accepte l'ID canonique ou la référence de transport de taille fixe, puis exécute l'autorisation, la validation du type et de la décision autorisée, la réconciliation des délais et le CAS terminal. La réponse porte toujours l'ID canonique. |

La validation de demande spécifique au type reste dans `exec.approval.request` et `plugin.approval.request`. Les méthodes existantes `exec.approval.get/list/waitDecision/resolve` et `plugin.approval.list/waitDecision/resolve` deviennent des adaptateurs de limite de protocole au service canonique car elles sont une API de passerelle expédiée. Les appelants internes migrent vers le service dans le même changement.

Une projection du relecteur est une union marquée :

```ts
type OperatorApproval = {
  id: string;
  status: OperatorApprovalStatus;
  presentation:
    | { kind: "exec"; commandText: string /* safe exec preview */ }
    | { kind: "plugin"; title: string; description: string /* safe plugin preview */ };
  // common lifecycle fields
};
```

Le chemin stable est dérivé, non persisté. `approval.get` retourne `urlPath` ; les surfaces qui connaissent une origine publique approuvée peuvent également recevoir une `url` absolue. Les instantanés du relecteur omettent les clés de session source et d'audience. La passerelle conserve ces clés de routage côté serveur pour la projection `session.approval` séparée.

## Événements et actions portables

PR 1 préserve les noms d'événements expédiés, les charges utiles et les filtres de destinataires au niveau des enregistrements existants :

- `exec.approval.requested`
- `exec.approval.resolved`
- `plugin.approval.requested`
- `plugin.approval.resolved`

Ces événements hérités peuvent contenir la demande d'exécution complète, ils ne doivent donc pas être distribués à chaque client dans le champ d'approbation. PR 5 ajoute des champs de cycle de vie marqués (`status`, `sourceSessionKey`, `urlPath`, métadonnées terminales et un `kind` au niveau de la présentation) via la projection de cycle de vie assainie au lieu d'élargir la livraison d'événements hérités.

Ajoutez un événement de projection `session.approval` dans le champ d'approbation. Publiez l'événement canonique une fois avec les clés d'audience persistées ; les abonnés de session exacte reçoivent le même événement pour chaque clé correspondante :

- `sessionKey` : flux recevant la projection.
- `sourceSessionKey` : enfant/source qui a levé la barrière.
- `phase` : `requested \| terminal`.
- une projection `OperatorApproval` sûre.

Enregistrez l'événement sous `operator.approvals` dans `src/gateway/server-broadcast.ts`. L'abonnement à la session seul ne confère jamais la visibilité d'approbation.

Étendez `MessagePresentationAction` dans `src/interactive/payload.ts` :

```ts
type MessagePresentationAction =
  | { type: "command"; command: string }
  | { type: "callback"; value: string }
  | {
      type: "approval";
      approvalId: string;
      approvalKind: "exec" | "plugin";
      decision: ExecApprovalDecision;
    }
  | { type: "url"; url: string }
  | { type: "web-app"; url: string };
```

Core construit des actions de décision typées et un lien Review séparé quand une origine Control UI absolue approuvée est disponible. Les canaux codent une action d'approbation dans leur propre format de rappel et envoient la résolution au service canonique. Un rappel utilise l'ID canonique exact quand il s'adapte ; sinon il utilise le `resolution_ref` de résumé complet unique de la ligne. La référence est seulement une clé de recherche compacte : l'authentification normale de la passerelle, l'autorisation des enregistrements, le type explicite, la validation de la décision autorisée, la réconciliation des délais et le CAS de première réponse s'appliquent toujours. Les canaux ne doivent pas tronquer les ID, résoudre les préfixes de hachage, analyser le texte `/approve` ou déduire le type d'un préfixe d'ID.

Conservez `button.url`, `button.webApp` et les contrôles d'approbation soutenus par des commandes comme entrées de compatibilité SDK de plugin dépréciées. Normalisez-les à la limite du SDK ; migrez chaque appelant interne fourni dans le même PR. `/approve {id} {decision}` reste un repli textuel et une commande CLI/chat, pas le contrat sémantique du bouton.

## Interface utilisateur de contrôle

L'itinéraire est `${basePath}/approve/{approvalId}`. L'ID est le seul paramètre de chemin ; l'identité de session source provient de l'enregistrement.

Parce que le routeur actuel a des itinéraires statiques exacts et réécrit les chemins inconnus en Chat, détectez ce lien profond dans `ui/src/app/bootstrap.ts` avant la normalisation d'itinéraire normale. Réutilisez la configuration normale de la passerelle/authentification, mais rendez une page d'approbation autonome en dehors de la coque de barre latérale et de la modale globale.

États de la page :

- chargement
- authentification requise
- en attente
- résolution
- approuvé ou refusé ici
- résolu ailleurs
- expiré
- annulé
- interdit/non trouvé
- erreur de connexion avec nouvelle tentative

La page appelle Gateway RPC, pas une deuxième API REST non authentifiée. Une actualisation du navigateur relit l'état durable. Elle ne place jamais les identifiants de passerelle dans l'URL, la requête ou le fragment.

## Autorisation et confidentialité

L'URL est un localisateur, non une autorité. La résolution nécessite :

1. une connexion Gateway authentifiée ;
2. `operator.approvals` ou `operator.admin` ;
3. une autorisation d'examinateur au niveau de l'enregistrement.

Règles au niveau de l'enregistrement :

- `operator.admin` peut examiner.
- `reviewer_device_ids` fait autorité quand présent. Seul un appareil `operator.approvals` appairé listé peut examiner ; l'appareil demandeur n'a pas d'accès implicite à moins d'être également listé.
- Sans liste d'examinateurs explicite, l'appareil `operator.approvals` appairé demandeur peut examiner son propre enregistrement.
- Les véritables enregistrements hérités sans demandeur ni liaison d'examinateur conservent une large visibilité d'appareil appairé afin que les mises à niveau ne bloquent pas les travaux déjà en attente.
- Les runtimes internes sans appareil peuvent résoudre, mais non lire, via la connexion runtime d'approbation délimitée. Cette autorité provient uniquement du jeton runtime authentifié par le serveur ; les champs publics `approval.resolve` ne peuvent pas le générer.
- La propriété de la connexion du demandeur en direct reste valide pour les adaptateurs hérités ; elle n'est jamais déduite d'un nom de client correspondant.
- L'adhésion à l'audience ne modifie que la présentation. Elle n'élargit jamais l'autorisation.

`approval.get` expose uniquement la projection d'examinateur assainie et omet les clés de routage source/audience internes. L'événement `session.approval` de la PR 5 porte sa seule destination `sessionKey` plus `sourceSessionKey` après que la Gateway applique l'instantané d'audience persisté côté serveur. Les événements exec/plugin existants conservent leur charge utile historique et les destinataires restreints jusqu'à ce que les consommateurs migrent. La demande exécutable, la liaison de commande et la continuation restent uniquement dans l'attente locale du processus. La ligne durable contient la présentation sûre plus les métadonnées de cycle de vie, de routage et d'audit ; elle ne stocke jamais les valeurs d'environnement brutes, les identifiants, les en-têtes d'authentification ou les données de rappel de canal.

## Projection d'audience

Calculez l'audience une fois avant l'insertion et persistez l'instantané ordonné. La propriété est un graphe, pas toujours une seule chaîne parente : un enfant peut avoir à la fois un contrôleur actuel et un demandeur original, et ces propriétaires peuvent mener à des racines différentes.

Utilisez une marche en largeur d'abord déterministe :

1. Initialisez la file d'attente avec la clé de session source.
2. Pour chaque clé retirée de la file, lisez la dernière ligne du registre de sous-agent et mettez en file d'attente les deux arêtes de propriété distinctes dans un ordre fixe : `controllerSessionKey`, puis `requesterSessionKey`.
3. Quand une ligne de registre utilisable existe, ne suivez pas aussi la lignée d'entrée de session qui peut être obsolète après la direction. Sinon, mettez en file d'attente la seule arête de secours actuelle `parentSessionKey ?? spawnedBy`.
4. Normalisez et dédupliquéz à la mise en file d'attente afin que le premier chemin le plus court gagne.
5. Arrêtez à 64 clés uniques ; ce plafond de taille d'audience limite également la profondeur de traversée.

La source du registre est `src/agents/subagent-registry-read.ts` ; les champs de propriété sont définis dans `src/agents/subagent-registry.types.ts`. Les champs de secours de session sont définis dans `src/config/sessions/types.ts`.

Les projections demandées et terminales utilisent la même audience persistée même si la propriété de focus/contrôleur change pendant que l'approbation est en attente. Cela garantit que chaque surface qui a affiché la demande reçoit le nettoyage terminal. La résolution cible toujours l'ID d'approbation source ; les sessions d'audience ne reçoivent jamais d'état d'approbation cloné.

N'écrivez pas de messages de transcription, n'injectez pas d'invites système, ne commencez pas les tours du propriétaire ou n'émettez pas `sessions.changed` uniquement pour une approbation.

## Convergence de surface livrée

Les gestionnaires d'approbation natifs conservent déjà leurs entrées de message livrées assez longtemps pour remplacer ou retirer les contrôles actifs. Les messages d'approbation transférés génériques rejettent actuellement `MessageReceipt`, donc une décision sur une autre surface peut laisser leurs anciens contrôles en attente. La PR 5 comble cette lacune avec une table enfant `operator_approval_deliveries` dans la base de données d'état partagée.

Chaque ligne stocke l'ID d'approbation, un ID de livraison unique, le canal/compte/route exacte, un localisateur de message validé JSON limité privé au canal, les horodatages de livraison et l'état de terminaison. Elle ne stocke jamais les données de rappel, les jetons de décision ou les demandes d'approbation brutes. Le canal possède l'encodage du localisateur et la mutation de message ; le cœur possède le statut canonique, la sélection de cible, la politique de nouvelle tentative et le texte terminal de secours.

L'enregistrement de livraison et la résolution terminale font la course en toute sécurité :

1. Après qu'un envoi en attente retourne son reçu, insérez le localisateur de livraison et lisez le statut d'approbation parent dans une seule transaction.
2. Si le parent est déjà terminal, planifiez la terminaison immédiate au lieu de laisser la livraison tardive en attente.
3. Chaque transition terminale validée planifie séparément toutes les lignes de livraison non finalisées ; les diffusions supprimables ne sont pas le déclencheur.
4. Un terminaliseur de canal signale `replaced`, `retired` ou `unsupported`. Remplacé supprime un message terminal en double ; retiré envoie le suivi terminal existant ; non pris en charge ou échec revient en arrière sans annuler l'approbation CAS.
5. Au démarrage, les approbations terminales avec livraisons inachevées sont relancées, rendant le nettoyage résilient au redémarrage de la Gateway.

Ce cycle de vie de transport est un crochet d'adaptateur de livraison optionnel, pas une action de message orientée rendu ou modèle. Les messages QQ C2C/groupe n'ont actuellement pas d'API d'édition, de suppression ou d'effacement de clavier ; cet adaptateur reste non pris en charge et ne peut afficher que la vérité canonique après un clic ultérieur jusqu'à ce que le transport gagne une API de mutation.

## Redémarrage, délai d'expiration et sémantique de route

La persistance SQLite n'implique pas la reprise d'exécution. Les liaisons de commande/outil restent en mémoire car elles peuvent contenir des faits runtime sensibles à la sécurité et ne sont pas un contrat de travail reprise.

Au démarrage de la Gateway :

- générez une nouvelle époque runtime ;
- transitionner atomiquement les lignes en attente des anciennes époques vers `cancelled` avec la raison `gateway-restart` ;
- conserver les lignes afin que leurs URL expliquent ce qui s'est passé ;
- ne jamais exécuter une approbation ultérieure contre une liaison runtime manquante.

Les minuteurs sont des optimisations de réveil. L'autorité de délai est stockée `expires_at_ms` ; les lectures, les attentes et les résolutions exécutent toutes la réconciliation d'expiration.

Comportement final strict :

- délai d'expiration -> `expired`, refuser ;
- pas de route -> `denied`, refuser ;
- abandon d'exécution -> `cancelled`, refuser ;
- verdict de confiance mal formé -> `denied`, refuser ;
- uniquement une décision d'autorisation explicite autorisée -> `allowed`.

Le comportement actuellement expédié entre en conflit avec ce contrat :

- `src/agents/bash-tools.exec-host-shared.ts` peut appliquer `askFallback`.
- `src/agents/agent-tools.before-tool-call.ts` peut honorer `timeoutBehavior: "allow"`.
- `docs/tools/exec-approvals.md`, `docs/cli/approvals.md` et `docs/plugins/plugin-permission-requests.md` documentent ces surfaces.

Ne les changez pas silencieusement dans la PR de stockage. La PR de sémantique stricte doit mettre à jour le code, les types, les docs, les tests et le changelog ensemble, avec un examen explicite du propriétaire/sécurité. `askFallback` peut continuer à décrire la sélection de politique pré-gate pendant la migration, mais elle ne doit pas transformer le délai d'expiration d'un enregistrement en attente créé en approbation.

## Plan de compatibilité

- Protocole Gateway additif ; pas de changement de version de protocole.
- Préserver les méthodes et événements exec/plugin existants à la limite externe.
- Conserver les ID existants, y compris les préfixes `plugin:`, mais arrêter d'utiliser les préfixes comme information de type.
- Conserver le comportement de la commande texte `/approve`.
- Conserver les champs URL/Web App de bouton hérité et les actions de commande comme entrée de compatibilité SDK de plugin ; la nouvelle sortie de cœur est typée.
- Migrer tous les canaux groupés et les appelants internes dans le même changement d'action typée.
- Ajouter une entrée de changelog pour la nouvelle URL/page et pour le changement de comportement de délai d'expiration ultérieur.
- N'ajoutez pas de paramètre de mode d'élicitation.

## Déploiement

### PR 1 : cycle de vie durable

- Cette note de conception.
- Schéma SQLite partagé, génération Kysely, magasin et élagage de 30 jours.
- Service d'approbation Gateway, pont d'attente runtime et gestion des orphelins de redémarrage.
- `approval.get/resolve` unifié.
- Adaptateurs de méthode Exec/plugin.
- Première réponse gagnante, idempotence, expiration, autorisation et tests de consommation.
- Aucun changement d'interface utilisateur ou de comportement de canal pour le moment.

### PR 2 : actions typées et rappels de canal

- Actions d'approbation, d'URL et d'application Web typées.
- Constructeurs de présentation de cœur et exportations SDK de plugin.
- Encodage de rappel privé au transport avec type de propriétaire explicite.
- Références de rappel de taille fixe durable pour les ID canoniques au-delà des limites de transport.
- Migration de canal groupé loin de l'inférence de texte de commande et d'ID d'approbation.
- Vérité terminale canonique de première réponse sur la surface cliquée et mises à jour terminales natives actives au mieux ; la réconciliation durable reste dans la PR 5.
- Tests SDK et canal groupé.

### PR 3 : lien profond de l'interface utilisateur de contrôle

- Page d'approbation authentifiée autonome et routage de démarrage conscient du chemin de base.
- Charge utile d'URL créée par Gateway et interrogation d'état en attente jusqu'à ce que les événements de cycle de vie soient expédiés.
- Preuve de largeur mobile, reconnexion, réponse concurrente, rechargement et chemin monté.

### PR 4 : clients natifs

- Les surfaces d'examen iOS, watchOS et Android utilisent `approval.get/resolve` conscient du type.
- La vérité terminale canonique de première réponse remplace l'état de décision tenté local.
- Preuve unitaire native, de construction et de plateforme.

### PR 5 : propagation et comportement de fermeture défaillante

- Livraison de demande/terminal `session.approval` à partir de l'instantané d'audience persisté dans la PR 1.
- Localisateurs de livraison transférée durable et nettoyage terminal canonique sur chaque surface livrée, y compris la relecture de redémarrage.
- Migrer `node-invoke-plugin-policy.ts` et le courtier de plugin intégré loin de l'autorité en double.
- Sémantique stricte de délai d'expiration/mal formée/pas de route et docs de compatibilité.
- Preuve de bout en bout multi-surface et sous-agent imbriqué.

## Tests

Couverture ciblée requise :

- La réouverture SQLite préserve les projections en attente et terminales.
- Deux résolveurs concurrents produisent exactement un gagnant CAS.
- La nouvelle tentative de même décision réussit de manière idempotente ; la nouvelle tentative conflictuelle retourne le gagnant enregistré.
- La résolution à ou après la date limite ne peut pas approuver.
- `allow-once` est consommable exactement une fois sans effacer l'état d'audit terminal.
- Le démarrage annule les anciennes époques runtime.
- La recherche et la résolution non autorisées ne révèlent pas l'existence de l'enregistrement.
- Liste d'examinateurs explicite et comportement général `operator.approvals` appairé.
- Les méthodes héritées Exec et plugin partagent le même magasin.
- Schémas de demande/liste/obtention/résolution de Gateway et charges utiles d'événement additives.
- Normalisation d'action typée, rendu de secours, exportations SDK et commutateurs de canal groupé.
- L'encodage de rappel Telegram contient des données privées au transport et aucune inférence de chaîne de commande.
- Enfant direct, propriétaires de contrôleur/demandeur ramifiés, propriétaires imbriqués, réaffectation, secours de champ de session, cycle et plafond de taille d'audience.
- Les tableaux d'audience demandés et terminaux sont identiques.
- Les projections de propriétaire ne causent aucune mutation de transcription ou réveil d'agent.
- L'itinéraire de l'interface utilisateur de contrôle fonctionne à `/` et un chemin de base configuré ; l'actualisation affiche la vérité en attente ou terminale.
- Les réponses simultanées de l'interface utilisateur de contrôle et de Telegram affichent un gagnant et « résolu ailleurs » sur le perdant.
- Preuve de chemin utilisateur via Testbox/Crabbox, y compris une page d'approbation de largeur mobile et nettoyage d'action Telegram.

## Observabilité

Émettez des journaux de transition structurés et sans contenu avec ID d'approbation, type, clé de session source, statut, raison et latence. Ne journalisez jamais l'aperçu ou la liaison brute.

Suivre :

- nombre demandé par type ;
- nombre terminal par type/statut/raison ;
- jauge en attente ;
- latence demande-à-terminal ;
- résultats de course de résolution : gagnant, nouvelle tentative idempotente, conflit, expiré ;
- nombre de routes de livraison et refus sans route ;
- annulations d'orphelin de démarrage ;
- taille de l'audience.

Une transition validée est un succès même si la livraison d'événement ultérieure échoue. L'échec de livraison est journalisé séparément ; la PR 5 répare l'état distant via la relecture de livraison durable et la recherche canonique.

## Décisions ouvertes

1. **Origine de l'interface utilisateur de contrôle accessible de l'extérieur.** Chaque snapshot porte le `urlPath` relatif stable. Une URL absolue ne peut être annoncée que depuis un emplacement Tailscale Serve/Funnel mis en cache après la réussite de l'exposition de la passerelle ; `allowedOrigins`, les en-têtes Host de la requête, `gateway.remote.url`, et les candidats loopback/LAN affichés uniquement ne sont pas des origines canoniques. Telegram peut utiliser son wrapper Mini App authentifié pour conserver le chemin d'approbation via bootstrap. Les proxies inverses arbitraires restent relatifs uniquement jusqu'à ce qu'un contrat d'URL publique explicite examiné séparément existe. Ne laissez jamais un canal deviner l'origine.
2. **Basculement strict de compatibilité des délais d'expiration.** La cible est fermée en cas d'échec, mais `askFallback` et le contrat d'expédition du plugin `timeoutBehavior: "allow"` sont des contrats expédiés. Recommandé : effectuer le changement de comportement dans la PR 5 avec approbation explicite du propriétaire/sécurité, journal des modifications, documentation et une décision de migration/dépréciation plutôt que de la masquer dans la PR 1.
3. **Mode intégré sans passerelle.** Recommandé : le garder local uniquement initialement, puis en faire un client du service canonique quand une passerelle existe. N'annoncez pas un lien profond qu'aucun serveur ne peut résoudre.
