---
summary: "Rôles d'opérateur, portées et vérifications au moment de l'approbation pour les clients Gateway"
read_when:
  - Débogage des erreurs de portée d'opérateur manquantes
  - Examen des approbations d'appairage de périphérique ou de nœud
  - Ajout ou classification des méthodes RPC Gateway
title: "Portées d'opérateur"
---

Les portées d'opérateur définissent ce qu'un client Gateway peut faire après son authentification.
Il s'agit d'une barrière de sécurité du plan de contrôle au sein d'un domaine d'opérateur Gateway de confiance,
et non d'une isolation multi-locataire hostile. Si vous avez besoin d'une séparation forte entre
des personnes, des équipes ou des machines, exécutez des Gateways séparés sous des utilisateurs ou
des hôtes OS séparés.

Connexe : [Sécurité](/fr/gateway/security), [Protocole Gateway](/fr/gateway/protocol),
[Appairage Gateway](/fr/gateway/pairing), [CLI Périphériques](/fr/cli/devices).

## Rôles

Les clients WebSocket Gateway se connectent avec un rôle :

- `operator` : clients du plan de contrôle tels que CLI, Interface de contrôle, automatisation et
  processus d'assistance de confiance.
- `node` : hôtes de capacité tels que macOS, iOS, Android ou nœuds sans interface graphique qui
  exposent des commandes via `node.invoke`.

Les méthodes RPC d'opérateur nécessitent le rôle `operator`. Les méthodes d'origine de nœud
nécessitent le rôle `node`.

## Niveaux de portée

| Portée                  | Signification                                                                                                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `operator.read`         | Lectures de statut, listes, catalogue, journaux, lectures de session et autres appels du plan de contrôle non mutants.                                                               |
| `operator.write`        | Actions d'opérateur mutantes normales telles que l'envoi de messages, l'invocation d'outils, la mise à jour des paramètres de conversation/voix et le relais de commande de nœud. Satisfait également `operator.read`. |
| `operator.admin`        | Accès administratif au plan de contrôle. Satisfait chaque portée `operator.*`. Requis pour la mutation de configuration, les mises à jour, les hooks natifs, les espaces de noms réservés sensibles et les approbations à haut risque. |
| `operator.pairing`      | Gestion de l'appairage de périphérique et de nœud, y compris l'énumération, l'approbation, le rejet, la suppression, la rotation et la révocation des enregistrements d'appairage ou des jetons de périphérique. |
| `operator.approvals`    | API d'approbation d'exécution et de plugin.                                                                                                                                           |
| `operator.talk.secrets` | Lecture de la configuration Talk avec secrets inclus.                                                                                                                                 |

Les portées `operator.*` futures inconnues nécessitent une correspondance exacte sauf si l'appelant a
`operator.admin`.

## La portée de la méthode n'est que la première barrière

Chaque RPC Gateway a une portée de méthode de moindre privilège. Cette portée de méthode décide
si la demande peut atteindre le gestionnaire. Certains gestionnaires appliquent ensuite des vérifications
d'approbation plus strictes en fonction de la chose concrète en cours d'approbation ou de mutation.

Exemples :

- `device.pair.approve` est accessible avec `operator.pairing`, mais l'approbation d'un
  périphérique d'opérateur ne peut que créer ou préserver les portées que l'appelant détient déjà.
- `node.pair.approve` est accessible avec `operator.pairing`, puis dérive des portées d'approbation supplémentaires
  à partir de la liste de commandes de nœud en attente.
- `chat.send` est normalement une méthode à portée d'écriture, mais `/config set`
  et `/config unset` persistants nécessitent `operator.admin` au niveau de la commande.

Cela permet aux opérateurs de portée inférieure d'effectuer des actions d'appairage à faible risque sans rendre
toute approbation d'appairage réservée aux administrateurs.

## Approbations d'appairage de périphérique

Les enregistrements d'appairage de périphérique sont la source durable des rôles et portées approuvés.
Les périphériques déjà appairés n'obtiennent pas un accès plus large silencieusement : les reconnexions qui demandent
un rôle plus large ou des portées plus larges créent une nouvelle demande de mise à niveau en attente.

Lors de l'approbation d'une demande de périphérique :

- Une demande sans rôle d'opérateur n'a pas besoin d'approbation de portée de jeton d'opérateur.
- Une demande pour `operator.read`, `operator.write`, `operator.approvals`,
  `operator.pairing` ou `operator.talk.secrets` nécessite que l'appelant détienne
  ces portées, ou `operator.admin`.
- Une demande pour `operator.admin` nécessite `operator.admin`.
- Une demande de réparation sans portées explicites peut hériter des portées de jeton d'opérateur existantes. Si ce jeton existant a une portée d'administrateur, l'approbation nécessite toujours
  `operator.admin`.

Pour les sessions de jeton de périphérique appairé, la gestion est auto-limitée sauf si l'appelant
a également `operator.admin` : les appelants non-administrateurs ne voient que leurs propres entrées d'appairage,
peuvent approuver ou rejeter uniquement leur propre demande en attente, et peuvent faire pivoter, révoquer ou
supprimer uniquement leur propre entrée de périphérique.

## Approbations d'appairage de nœud

L'héritage `node.pair.*` utilise un magasin d'appairage de nœud séparé appartenant à Gateway. Les nœuds WS
utilisent l'appairage de périphérique avec `role: node`, mais le même vocabulaire de niveau d'approbation
s'applique.

`node.pair.approve` utilise la liste de commandes de demande en attente pour dériver des portées supplémentaires requises :

- Demande sans commande : `operator.pairing`
- Commandes de nœud non-exécution : `operator.pairing` + `operator.write`
- `system.run`, `system.run.prepare` ou `system.which` :
  `operator.pairing` + `operator.admin`

L'appairage de nœud établit l'identité et la confiance. Il ne remplace pas la
politique d'approbation d'exécution `system.run` propre du nœud.

## Authentification par secret partagé

L'authentification par jeton/mot de passe de gateway partagé est traitée comme un accès d'opérateur de confiance pour
ce Gateway. Les surfaces HTTP compatibles OpenAI et `/tools/invoke` restaurent l'ensemble de portée d'opérateur par défaut complet normal pour l'authentification du porteur de secret partagé, même si un
appelant envoie des portées déclarées plus étroites.

Les modes porteurs d'identité, tels que l'authentification de proxy de confiance ou l'ingress privé `none`,
peuvent toujours honorer les portées déclarées explicites. Utilisez des Gateways séparés pour la séparation réelle des limites de confiance.
