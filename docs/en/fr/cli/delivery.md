---
summary: "Inspectez, compactez, purgez et renvoyez en toute sécurité les échecs de livraison retenus"
read_when:
  - A session or outbound delivery is dead-lettered
  - You need to remove sensitive failed-delivery detail without breaking idempotency
title: "Échecs de livraison"
---

# `openclaw delivery failures`

OpenClaw conserve les livraisons sortantes et de session ayant échoué séparément de la file d'attente de nouvelle tentative active. L'enregistrement d'échec peut conserver les détails de diagnostic ou de récupération pendant une durée limitée tandis que sa pierre tombale compacte continue de posséder un ID de livraison stable.

## Lister les métadonnées d'échec

```bash
openclaw delivery failures list
openclaw delivery failures list --queue outbound-prepared-v1 --limit 50
openclaw delivery failures list --json
openclaw delivery failures list --exact-ids
```

La limite par défaut est 100 et le maximum absolu est 500. La sortie inclut la file d'attente, l'âge, l'état des détails, la classification de relecture, la politique de clôture, le code de raison et le nombre de tentatives. Elle n'inclut jamais le message ou la charge utile, l'itinéraire, la cible, le compte, la clé de session, le chemin média ou l'erreur brute du fournisseur.

Les identifiants stables peuvent contenir l'identité de routage, donc la sortie humaine et JSON utilisent une empreinte SHA-256 répétable par défaut. Passez `--exact-ids` uniquement lorsqu'un identifiant exact est nécessaire pour une commande de suivi. Les clôtures limitées par producteur affichent également une `idPrefixFingerprint` par défaut ; `--exact-ids` révèle également leur préfixe de producteur exact.

## Prévisualiser ou appliquer le nettoyage de rétention

```bash
openclaw delivery failures purge
openclaw delivery failures purge --queue session
openclaw delivery failures purge --apply --yes
```

`purge` est un essai à blanc par défaut. Le mode application supprime uniquement les lignes de diagnostic expirées dont la politique n'a pas de clôture, plus les clôtures limitées par producteur après l'expiration de leur âge créé ou de leur limite de comptage local du producteur. Les enregistrements non expirés limités par producteur, permanents et gérés par le propriétaire conservent leur pierre tombale de propriété tandis que les détails sensibles sont compactés. L'essai à blanc et l'application utilisent le même ensemble de lignes limité ; `--queue` et `--limit` délimitent les deux modes de manière identique.

Il n'y a pas d'option pour forcer la rupture d'une clôture. Sans `--yes`, le mode application demande une confirmation dans un terminal interactif et refuse en JSON ou autre utilisation non interactive.

La compaction logique efface le JSON porteur de charge utile, les erreurs brutes et les métadonnées dénormalisées de session/canal/cible/compte. SQLite peut continuer à réserver les pages libérées à l'intérieur du fichier de base de données. Pour retourner les pages libres au système de fichiers, arrêtez la Gateway et exécutez [`openclaw doctor --state-sqlite compact`](/fr/cli/doctor#shared-state-sqlite-compaction).

## Renvoyer en toute sécurité un échec

```bash
openclaw delivery failures resubmit <id>
openclaw delivery failures resubmit <id> --queue session
openclaw delivery failures resubmit <id> --queue outbound-prepared-v1
openclaw delivery failures resubmit <id> --url ws://127.0.0.1:18789 --token <token>
```

`resubmit` nécessite une Gateway en cours d'exécution et accessible, et accepte les options client Gateway standard : `--url`, `--token`, `--password` et `--timeout`. La Gateway effectue la transition d'échec à en attente et planifie immédiatement une ligne de session éligible dans son runtime de livraison actif. Si le runtime démarre toujours ou si la planification immédiate échoue après cette transition durable, la commande signale que la ligne reste en file d'attente pour la récupération au démarrage. Une défaillance de connexion ou d'authentification se produit avant que la ligne ne change.

Les files d'attente de session et sortante ont des espaces de noms d'ID indépendants. Si les deux possèdent le même ID, un renvoi non qualifié est refusé ; réexécutez avec l'espace de noms `--queue` exact affiché par `openclaw delivery failures list --exact-ids`.

Le succès signifie **en file d'attente pour récupération**, pas livré. Les lignes sortantes sont récupérées par l'intervalle de récupération sortante limité de la Gateway ; la commande ne prétend pas à la livraison du destinataire ni ne démarre une deuxième boucle de récupération.

Le renvoi générique est intentionnellement étroit. Les lignes sortantes nécessitent une classification explicite pré-effet secondaire, une charge utile préparée canonique complète, aucun propriétaire durable ou clôture stable, et chaque fichier média appartenant à la file d'attente. Les lignes de session nécessitent les détails complets, aucun propriétaire, aucun marqueur de début de livraison ou de règlement, et aucune ambiguïté. La transition d'échec à en attente de la Gateway est atomique, donc une deuxième invocation ne soumet pas la même ligne à nouveau.

Les ID sortants stables et les producteurs de session revendiqués conservent la propriété d'échec même lorsque les envois réussis ne conserveraient pas un reçu d'achèvement.

OpenClaw refuse l'ambiguïté entre files d'attente, compactée, ambiguë, gérée par le propriétaire, inconnue héritée, espace de noms de migration, média manquant et lignes de propriétaire obsolète. Les échecs d'achèvement du sous-agent restent sous leurs commandes de propriétaire :

```bash
openclaw tasks retry <task-id>
openclaw tasks dismiss <task-id>
```

## Sauvegardes et octets retenus

Les snapshots SQLite globaux suppriment chaque ligne de file d'attente de livraison avant de publier le snapshot, y compris le travail en attente, les clôtures échouées et les reçus d'achèvement ou d'idempotence. La restauration d'une n'est pas une continuation de livraison exactement une fois ; l'artefact assaini choisit délibérément la confidentialité et la portabilité sans relecture plutôt que la continuité de la file d'attente. Une sauvegarde d'état normale peut contenir la base de données active, donc protégez-la comme tout autre état OpenClaw sensible. La rétention logique et la réclamation de taille de fichier SQLite sont des opérations distinctes ; utilisez le flux de compaction du docteur explicite lorsque la réclamation physique est requise.

## Connexes

- [`openclaw health`](/fr/cli/health)
- [`openclaw doctor`](/fr/cli/doctor)
- [Récupération au redémarrage](/fr/gateway/restart-recovery)
