---
summary: "Récupérer après l'échec des mises à jour OpenClaw dans l'interface de contrôle ou la CLI"
read_when:
  - Une mise à jour OpenClaw a échoué
  - La passerelle n'a pas signalé de résultat de mise à jour final
title: "Dépannage des mises à jour"
---

Commencez par **Control UI → Settings → Updates**. La page lit la dernière tentative de mise à jour enregistrée depuis la passerelle connectée et affiche son heure, sa cible, son code de raison, l'étape défaillante et les détails de diagnostic limités.

La correction dans l'interface de contrôle utilise uniquement les actions de produit typées. Elle commence par une action de passerelle authentifiée ou native lorsque l'interface utilisateur connectée dispose de la capacité et de la portée requises, préserve les confirmations pour les opérations perturbantes et conserve les commandes de terminal comme solutions de secours secondaires côté hôte. Elle n'analyse jamais les conseils localisés ni n'exécute une chaîne de commande arbitraire.

## Récupérer dans l'interface de contrôle

1. Sélectionnez **Check status** lorsque la passerelle a redémarré, s'est déconnectée ou n'a pas signalé de résultat final. Cela lit `update.status` ; cela ne démarre pas une autre mise à jour. Les contrôles de récupération restent désactivés pendant que la vérification est en attente, et une demande rejetée apparaît comme une erreur sur la page.
2. Ouvrez **View details** et traitez l'étape défaillante enregistrée. Le texte de diagnostic est limité et masqué pour l'affichage ; utilisez les journaux de la passerelle lorsque plus de contexte est requis.
3. Sélectionnez **Retry update** uniquement après que la cause soit résolue. L'interface de contrôle utilise le flux de mise à jour confirmé normal et indique que les sessions en cours sont interrompues lors du redémarrage de la passerelle.

Les contrôles nécessitent une passerelle connectée, la prise en charge de la méthode de passerelle typée correspondante et une portée administrateur. Lorsque ces conditions ne sont pas remplies, utilisez la solution de secours CLI sur l'hôte de la passerelle.

## Codes de raison

- `dirty`, `no-upstream` : réparez l'extraction source avant de réessayer.
- `deps-install-failed`, `build-failed`, `ui-build-failed` : inspectez l'étape défaillante, corrigez l'erreur de dépendance ou de compilation, puis réessayez.
- `global-install-failed` : réessayez après avoir vérifié la propriété et les permissions du gestionnaire de paquets. Réexécutez l'installateur si l'installation du paquet est incomplète.
- `doctor-failed` : exécutez Doctor sur l'hôte de la passerelle, résolvez ses conclusions, puis réessayez.
- `restart-disabled`, `restart-unavailable` : restaurez un superviseur pris en charge ou activez les redémarrages de la passerelle avant de réessayer.
- `restart-unhealthy`, `restart-revision-mismatch`, `restart-revision-unavailable` : inspectez la santé du service de la passerelle et sa racine d'installation avant de réessayer.
- `managed-service-handoff-*` : vérifiez d'abord le statut. Si la transmission s'est arrêtée, utilisez la CLI sur l'hôte de la passerelle pour préserver la sortie de diagnostic complète.

Les codes de raison inconnus restent visibles. Vérifiez les journaux de la passerelle avant de réessayer.

## Solution de secours CLI

Exécutez ces commandes sur l'hôte de la passerelle, et non sur l'ordinateur qui a simplement l'interface de contrôle ouverte :

```bash
openclaw update status --json
openclaw doctor --non-interactive
openclaw update
```

Utilisez `openclaw update --dry-run` pour prévisualiser une nouvelle tentative. Si une mise à jour de paquet a échoué après le début de l'installation, suivez les étapes de récupération de l'installateur dans [Updating](/fr/install/updating#alternative-re-run-the-installer).

## Limite de restauration

Ne restaurez pas l'état comme première réponse à un échec de mise à jour. Réinstallez d'abord le code connu comme bon tout en préservant l'état actuel. Restaurez un snapshot d'état pré-mise à jour vérifié uniquement lorsque le code plus ancien ne peut pas lire la configuration ou la base de données actuelle. Voir [Rollback](/fr/install/updating#rollback).

## Diagnostics de support

Collectez les éléments suivants sans publier les identifiants, la configuration brute ou la sortie de processus non masquée :

- Version et type d'installation d'OpenClaw ;
- horodatage de mise à jour, cible, phase et code de raison de Settings → Updates ;
- le détail d'échec limité affiché par **View details** ;
- `openclaw update status --json` ;
- `openclaw gateway status --deep --json` ;
- lignes de journal de passerelle pertinentes et masquées.
