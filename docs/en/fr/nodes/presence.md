---
summary: "Détectez le Mac que vous avez utilisé le plus récemment et acheminez les alertes de nœud vers celui-ci"
read_when:
  - You want OpenClaw to identify the active Mac
  - You are debugging last-input activity or active-node selection
  - You want to understand node connection notification routing
title: "Présence active de l'ordinateur"
---

La présence active de l'ordinateur indique à la Gateway quel nœud macOS connecté a reçu l'entrée physique la plus récente de la souris ou du clavier. OpenClaw utilise ce signal pour marquer un Mac comme `active`, donner à l'agent un indice de nœud actif stable, et acheminer les alertes de connexion de nœud vers l'ordinateur où vous êtes probablement présent.

Ceci est distinct de la [présence système](/fr/concepts/presence), qui est la liste active des clients Gateway, et des balises durables `node.presence.alive`, qui enregistrent quand un nœud mobile s'est réveillé pour la dernière fois sans le traiter comme connecté.

## Conditions requises

- L'application macOS OpenClaw est appairée et connectée en mode nœud.
- La permission **Accessibilité** est accordée à l'application OpenClaw signée.
- Pour les alertes de connexion, la permission **Notifications** est également accordée et le nœud Mac expose `system.notify`.

La génération de rapports d'activité est actuellement implémentée par le nœud natif macOS. iOS, Android, watchOS et les hôtes de nœud sans interface graphique peuvent signaler l'état de connexion ou de dernier accès en arrière-plan, mais ils ne concourent pas pour la désignation d'ordinateur actif.

## Vérifier l'ordinateur actif

1. Dans l'application macOS, ouvrez **Paramètres -> Autorisations** et accordez
   **Accessibilité** dans les Paramètres système macOS.
2. Confirmez que le nœud Mac est connecté :

   ```bash
   openclaw nodes status --connected
   ```

3. Déplacez la souris ou appuyez sur une touche sur ce Mac, puis exécutez :

   ```bash
   openclaw nodes status
   openclaw nodes describe --node <node-id-or-name>
   ```

Le Mac éligible le plus récent est marqué `active`. La sortie d'état affiche l'âge de sa dernière entrée ; `describe` expose `active`, `lastActiveAtMs` et `presenceUpdatedAtMs`. L'activité est intentionnellement regroupée, donc l'affichage peut prendre jusqu'à environ 15 secondes pour refléter une autre entrée après un rapport récent.

## Comment l'activité devient présence

Le rapporteur macOS échantillonne l'horloge d'inactivité HID toutes les deux secondes. Il rapporte une fois quand une connexion de nœud devient prête, puis rapporte une activité physique plus récente au maximum une fois toutes les 15 secondes. En cas d'inactivité, il envoie un keepalive toutes les trois minutes. La durée d'inactivité est plafonnée à 30 jours afin qu'un échantillon très ancien ne puisse pas dériver vers l'avant et devenir incorrectement l'ordinateur le plus récent.

La Gateway accepte l'activité uniquement lorsque tous les éléments suivants sont vrais :

- l'événement appartient à la connexion authentifiée actuelle pour cet identifiant de nœud ;
- le nœud a la permission effective `accessibility: true` ;
- la charge utile contient une valeur entière bornée `idleSeconds`.

La Gateway soustrait `idleSeconds` de son propre temps d'observation pour dériver `lastActiveAtMs`. Elle ne fait jamais confiance à un horodatage mural fourni par le nœud. Parmi les Macs éligibles connectés, le `lastActiveAtMs` le plus récent gagne ; une égalité utilise la mise à jour de présence la plus récente.

La présence est locale au processus et liée à la connexion. La déconnexion de la session actuelle, son remplacement par une autre session utilisant le même identifiant de nœud, ou la révocation d'Accessibilité efface l'état d'activité de ce nœud et recalcule le Mac actif.

## Confidentialité et contexte du modèle

OpenClaw envoie la durée d'inactivité, pas le contenu de l'entrée. Il n'envoie pas les valeurs de clés, les coordonnées de souris, les noms d'applications, les titres de fenêtres ou les événements d'entrée bruts. Le rapporteur macOS lit l'état HID du matériel, donc les événements de contrôle informatique synthétiques ne font pas apparaître un Mac automatisé comme l'ordinateur que vous avez physiquement utilisé.

L'activité continue ne crée pas d'événements système visibles par le modèle. La ligne de runtime dynamique contient uniquement l'identifiant de nœud authentifié :

```text
active_node=<node-id>
```

Les horodatages exacts et les noms d'affichage contrôlés par le nœud restent en dehors de l'invite pour éviter l'injection d'invite et l'usure du cache. Lorsque l'agent a besoin de détails actuels, l'outil `nodes` peut lire `node.list` ou `node.describe` à la place.

## Comment les alertes de connexion sont acheminées

Après qu'un nœud termine sa poignée de main Gateway, OpenClaw attend 750 millisecondes pour que le Mac de connexion puisse soumettre son premier échantillon d'activité. Il essaie ensuite le Mac connecté capable de notification avec l'activité la plus récente.

- Si la livraison principale réussit, aucun autre Mac ne reçoit l'alerte.
- Si aucun Mac actif n'est disponible ou si la livraison principale échoue, OpenClaw attend cinq secondes et essaie chaque Mac connecté restant qui expose `system.notify`.
- Une alerte de reconnexion pour le même nœud est supprimée pendant cinq minutes après une tentative de livraison réelle, empêchant le flottement de reconnexion de produire une tempête de notifications.

Les alertes sont liées à des connexions de nœud exactes. Une session source déconnectée ou remplacée ne peut pas terminer une ancienne alerte programmée, et une connexion de destination de remplacement peut toujours participer à la livraison de secours.

## Dépannage

| Symptôme                                   | Vérifier                                                                                                                                                                |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aucune ligne n'est marquée `active`                 | Confirmez qu'un nœud macOS natif est connecté et que `openclaw nodes describe --node <id>` affiche `permissions.accessibility: true`.                                          |
| Le mauvais Mac reste actif              | Utilisez ce Mac physiquement, attendez la fenêtre de regroupement, puis réexécutez `openclaw nodes status`. Les actions de contrôle informatique synthétiques ne comptent pas.                        |
| Les données de dernière entrée disparaissent                | Vérifiez si le Mac s'est déconnecté, sa session de nœud a été remplacée ou l'Accessibilité a été révoquée. Chaque condition efface intentionnellement l'activité.                       |
| L'alerte apparaît sur plusieurs Macs         | La livraison principale n'était pas disponible ou a échoué, donc le secours retardé s'est exécuté. Vérifiez que le Mac actif est connecté, autorise les notifications et expose `system.notify`. |
| L'agent ne mentionne pas le Mac actif | Commencez un nouveau tour après le changement d'activité. L'indice de runtime est stable et compact ; utilisez l'outil `nodes` pour les métadonnées actuelles exactes.                                    |

Pour la récupération TCC, voir [Autorisations macOS](/fr/platforms/mac/permissions). Pour les défaillances de connexion de nœud et de commande, voir [Dépannage des nœuds](/fr/nodes/troubleshooting).

## Connexes

- [Nœuds](/fr/nodes)
- [CLI Nœuds](/fr/cli/nodes)
- [Présence système](/fr/concepts/presence)
- [Protocole Gateway](/fr/gateway/protocol#presence)
- [Application macOS](/fr/platforms/macos)
