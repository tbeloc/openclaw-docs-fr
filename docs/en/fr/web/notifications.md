---
summary: "Activez et testez les notifications du navigateur ou de macOS à partir de l'interface de contrôle"
title: "Notifications"
read_when:
  - Enabling notifications from Settings
  - Troubleshooting browser or macOS notification permission
  - Comparing Control UI notifications with mobile push
---

OpenClaw peut vous signaler quand quelque chose nécessite votre attention — dans le navigateur qui exécute l'interface de contrôle, ou via les notifications natives de macOS lorsque vous utilisez l'application macOS OpenClaw. Tout se trouve sous **Paramètres → Notifications** : activez l'appareil actuel, vérifiez son statut et envoyez-vous un test.

Cette page couvre ces deux surfaces. Elle ne contrôle pas les notifications de réaction de canal, le transfert de notifications Android ou les notifications push en arrière-plan iOS — les applications mobiles s'enregistrent pour les notifications push via leurs propres chemins de nœud ; voir [iOS](/fr/platforms/ios) et [Nœuds](/fr/nodes).

## Quelle surface vous obtenez

Ce que la page Notifications contrôle dépend de l'endroit où vous l'avez ouverte :

| Où les paramètres sont ouverts                    | Transport                                          | Ce que vous pouvez faire                                                      |
| ------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------- |
| Navigateur web pris en charge ou PWA Control UI installée | API Push du navigateur via le service worker de l'interface de contrôle | Accorder la permission, vous abonner ou vous désabonner de ce navigateur, envoyer un test |
| Application macOS OpenClaw                        | Notifications natives de macOS                     | Accorder la permission à l'application, accéder aux Paramètres système en cas de blocage, envoyer un test local |
| Navigateur sans support de l'API Push             | Aucun                                              | Statut uniquement ; l'activation et le test restent indisponibles             |

L'application macOS utilise intentionnellement le flux de permission natif au lieu des notifications push du navigateur — c'est le système de notification que votre Mac respecte déjà.

## Activer les notifications du navigateur

1. Ouvrez l'interface de contrôle dans un navigateur qui prend en charge les service workers, `PushManager` et les notifications.
2. Assurez-vous que l'interface de contrôle est connectée à la passerelle.
3. Ouvrez **Paramètres → Notifications** et sélectionnez **Activer les notifications**.
4. Autorisez les notifications lorsque le navigateur vous le demande.
5. Sélectionnez **Envoyer un test** — une notification de test devrait arriver dans quelques secondes.

En coulisse, l'activation crée un abonnement push dans ce navigateur et enregistre son point de terminaison et ses clés auprès de la passerelle. La passerelle conserve les abonnements au navigateur et sa clé de signature VAPID dans `state/openclaw.sqlite` — il n'y a pas de clé `openclaw.json` à modifier. Lorsque l'interface de contrôle se reconnecte, les abonnements existants sont automatiquement réconciliés avec la passerelle.

**Envoyer un test** demande à la passerelle de pousser un message de test vers chaque abonnement au navigateur enregistré. **Se désabonner** supprime le point de terminaison du navigateur actuel de la passerelle, puis se désabonne localement.

## Activer les notifications dans l'application macOS

1. Ouvrez **Paramètres → Notifications** dans l'application macOS OpenClaw.
2. Sélectionnez **Activer les notifications** tandis que la permission affiche **Non demandée**.
3. Approuvez l'invite de permission de macOS.
4. Sélectionnez **Envoyer un test** pour publier une notification OpenClaw locale.

Si la permission affiche **Refusée**, macOS ne vous redemandera pas : sélectionnez **Ouvrir les Paramètres système**, autorisez les notifications pour OpenClaw là-bas, et revenez — la page revérifie la permission lorsque l'application reprend le focus. Cette permission appartient à macOS, pas à la configuration de la passerelle.

## Dépannage

### L'activation n'est pas disponible

Soit le navigateur manque des API Web Push requises, soit l'interface de contrôle n'est pas connectée à la passerelle. Essayez un navigateur actuel, confirmez la connexion à la passerelle et rechargez la page.

### La permission du navigateur est bloquée

Une permission de navigateur refusée ne peut pas être rouverte à partir de la page. Autorisez les notifications pour l'origine de l'interface de contrôle dans les paramètres du site du navigateur, puis rechargez les paramètres.

### Le service worker n'est pas prêt

L'interface de contrôle attend jusqu'à 10 secondes son service worker. Si cela expire juste après une mise à jour, actualisez la page en dur. Si un ancien worker persiste, effacez les données du site pour l'origine du tableau de bord et reconnectez-vous.

### Web Push demande une migration Doctor

Exécutez `openclaw doctor --fix` avec la passerelle arrêtée. Web Push refuse d'utiliser les magasins JSON retirés jusqu'à ce que Doctor les importe dans SQLite.

## Connexes

- [PWA de l'interface de contrôle et Web Push](/fr/web/control-ui#pwa-install-and-web-push)
- [Livraison des notifications push iOS](/fr/platforms/ios)
- [Commandes de notification de nœud](/fr/nodes)
