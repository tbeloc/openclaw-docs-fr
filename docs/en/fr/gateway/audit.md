---
summary: "Historique d'audit métadonnées uniquement pour les exécutions d'agent, les actions d'outils et les cycles de vie des messages opt-in"
read_when:
  - You need a durable record of what the Gateway did without storing content
  - You are deciding whether to enable message lifecycle auditing
  - You need to explain what audit records do and do not prove
title: "Historique d'audit"
---

# Historique d'audit

La Gateway conserve un registre d'audit limité et contenant uniquement des métadonnées dans la base de données d'état OpenClaw partagée. Il répond à des questions opérationnelles telles que « quel agent a été exécuté, quand et comment s'est-il terminé », « quelles actions d'outils une exécution a-t-elle effectuées » et, lorsque l'audit du cycle de vie des messages est activé, « un message entrant accepté a-t-il atteint la distribution » et « un message sortant a-t-il atteint un état de livraison terminal ».

Le registre stocke l'identité, l'ordre, la provenance, l'action, le statut et les codes de résultat normalisés. Il ne stocke jamais les invites, les corps de messages, les arguments d'outils, les résultats d'outils, les pièces jointes, les noms de fichiers, les URL, la sortie de commande ou le texte d'erreur brut.

## Familles d'enregistrements

Les événements d'exécution et d'outils sont enregistrés chaque fois que l'audit est activé (par défaut). Les événements du cycle de vie des messages sont opt-in et désactivés par défaut.

| Famille      | Actions                                                  | Par défaut |
| ------------ | -------------------------------------------------------- | ---------- |
| Exécutions d'agent   | `agent.run.started`, `agent.run.finished`                | activé      |
| Actions d'outils | `tool.action.started`, `tool.action.finished`            | activé      |
| Messages     | `message.inbound.processed`, `message.outbound.finished` | désactivé     |

Chaque enregistrement porte un identifiant d'événement stable, une séquence de registre monotone, un horodatage du cycle de vie, un acteur, une action, un statut, `schemaVersion: 1` et `redaction: "metadata_only"`. Voir [Enregistrements d'audit](/fr/cli/audit) pour la référence complète des champs et les filtres de requête.

## Événements du cycle de vie des messages

Définissez [`audit.messages`](/fr/gateway/configuration-reference#audit) pour choisir ce qui est enregistré, puis redémarrez la Gateway :

- `off` (par défaut) : aucun enregistrement de message.
- `direct` : uniquement les messages dans les conversations directes.
- `all` : messages directs, de groupe et de canal.

Deux limites autoritaires produisent des enregistrements de messages :

- Les lignes **Inbound** sont écrites lorsqu'un message accepté atteint la distribution principale, y compris les résultats de traitement en double et terminal.
- Les lignes **Outbound** sont écrites lorsque la livraison durable partagée atteint un résultat terminal : envoyé, supprimé, échoué ou un `unknown` explicite pour les envois ambigus en cas de crash. La récupération de file d'attente et les résultats de lettre morte sont inclus. Chaque charge utile de réponse logique originale obtient une ligne terminale ; le chunking et le fan-out d'adaptateur s'agrègent en `resultCount`.

### Classification du type de conversation

Le mode `direct` est une limite de confidentialité, donc un message est classé comme une conversation directe uniquement lorsque les faits de destination le prouvent : le chemin d'envoi a déclaré le type de conversation de destination, ou l'itinéraire de la session de livraison nomme exactement le canal et le pair en cours de livraison. Les signaux plus faibles, tels que l'état de la politique ou la conversation d'origine, peuvent classer un message comme `group` (l'excluant de la collection `direct`) mais ne peuvent jamais prétendre à `direct`. Les messages qui ne peuvent pas être prouvés directs sont classés `unknown` et ne sont pas enregistrés en mode `direct`. Les canaux qui ne déclarent pas les types de chat peuvent donc enregistrer moins de lignes en mode `direct` qu'en mode `all`.

## Modèle de confidentialité

Les lignes de messages ne stockent jamais les identifiants de plateforme bruts. Les identifiants de compte, de conversation, de message et de cible, lorsque la corrélation est disponible, sont exportés uniquement sous forme de pseudonymes à clé locale d'installation (`hmac-sha256:v1:<keyId>:<digest>`) :

- La clé HMAC est générée à la première utilisation, est séparée par domaine par type d'identifiant et réside dans la même base de données d'état que le registre.
- Les pseudonymes sont stables au sein d'une installation, donc les lignes concernant la même conversation se corrèlent sans révéler l'identifiant de plateforme.
- Ceci est **corrélation, pas anonymisation** : quiconque ayant accès en lecture à la base de données d'état a également la clé et peut tester les identifiants bruts candidats par rapport aux pseudonymes. Les exportations RPC et CLI n'incluent jamais la clé.
- Si le matériel clé est manquant ou corrompu tandis que les lignes de messages sont conservées, la Gateway échoue fermée et supprime les nouveaux enregistrements de messages au lieu de tourner silencieusement vers une nouvelle clé, ce qui diviserait la corrélation.

Les enregistrements d'exécution et d'outils conservent `sessionKey` et `sessionId` pour la corrélation ; les clés de session canoniques peuvent elles-mêmes contenir des identifiants de compte de plateforme ou des identifiants de pair. Les enregistrements de messages omettent intentionnellement les deux.

Les exportations d'audit restent des métadonnées opérationnelles sensibles même sans contenu : le timing, les canaux, les résultats et les pseudonymes stables peuvent corréler l'activité. Protégez les exportations avec les mêmes contrôles d'accès et pratiques de rétention que les autres enregistrements d'opérateur.

## Limites de couverture et de preuve

Le registre est au mieux un effort et délibérément limité. Traitez-le comme une preuve de ce qui a été enregistré, pas comme une preuve de ce qui s'est passé :

- **L'absence d'une ligne ne prouve rien.** Les chutes pré-admission entrantes, les envois à partir de processus CLI sans enregistreur Gateway en cours d'exécution et les chemins locaux de plugin ou d'envoi direct qui contournent la livraison durable partagée ne laissent aucune trace.
- Les écritures passent par un worker d'arrière-plan limité ; l'échec du worker ou la saturation de la file d'attente supprime les enregistrements et enregistre un avertissement opérationnel.
- Les envois sortants ambigus en cas de crash sont enregistrés comme `unknown` plutôt que des résultats inventés.

Ce registre prend en charge le débogage et l'examen opérationnel. Ce n'est pas une archive de conformité sans perte ; si vous en avez besoin, utilisez un système externe alimenté par [OpenTelemetry](/fr/gateway/opentelemetry) ou des outils au niveau du canal.

## Stockage, rétention et migration

Les enregistrements résident dans la base de données d'état partagée (`state/openclaw.sqlite`) et sont écrits en dehors du chemin chaud de livraison. Les requêtes ne retournent jamais d'enregistrements antérieurs à 30 jours, et le registre est limité à 100 000 lignes ; les lignes expirées sont supprimées au démarrage, lors de la maintenance horaire et lors des écritures ultérieures. La maintenance de rétention continue de s'exécuter même lorsque la collection est désactivée.

La mise à niveau à partir d'une Gateway avec le registre antérieur réservé aux exécutions/outils migre le schéma automatiquement au démarrage (ou via `openclaw doctor --fix`) ; les lignes existantes et leurs séquences de registre sont conservées.

## Interrogation

- CLI : [`openclaw audit`](/fr/cli/audit) avec des filtres pour l'agent, la session, l'exécution, le type, le statut, la direction, le canal, les limites de temps et la pagination du curseur.
- Gateway RPC : `audit.activity.list` (nécessite `operator.read`) retourne l'union d'événement d'activité V1 versionnée ; le RPC `audit.list` expédié est inchangé pour les clients run/tool plus anciens. Voir [Protocole Gateway](/fr/gateway/protocol#audit-ledger-rpc).

## Connexes

- [CLI des enregistrements d'audit](/fr/cli/audit)
- [Référence de configuration](/fr/gateway/configuration-reference#audit)
- [Protocole Gateway](/fr/gateway/protocol#audit-ledger-rpc)
- [OpenTelemetry](/fr/gateway/opentelemetry)
