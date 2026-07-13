---
summary: "Activer et invoquer des résumés HealthKit protégés par la confidentialité à partir d'un nœud iPhone"
read_when:
  - Enabling HealthKit summaries on an iPhone node
  - Invoking health.summary or troubleshooting missing health metrics
  - Reviewing what health data can leave an iPhone
title: "Résumés HealthKit"
---

# Résumés HealthKit

OpenClaw peut demander un résumé en lecture seule du jour calendaire actuel à partir d'un nœud iPhone connecté. L'iPhone calcule l'agrégat sur l'appareil et retourne uniquement les pas, la durée du sommeil, la fréquence cardiaque au repos moyenne et le nombre/la durée des entraînements. Les échantillons HealthKit individuels, les sources, les métadonnées, les dossiers cliniques, l'ingestion en arrière-plan et les écritures ne sont pas pris en charge.

Cette fonctionnalité est désactivée par défaut. Elle nécessite un consentement distinct sur l'iPhone et une autorisation sur la Gateway.

## Conditions requises

- Un iPhone exécutant l'application OpenClaw iOS où HealthKit signale les données de santé comme disponibles.
- Un nœud iPhone connecté et approuvé. Voir [Configuration de l'application iOS](/fr/platforms/ios).
- Une Gateway actuelle qui peut atteindre le nœud iPhone.
- Données de santé lisibles pour toutes les métriques que vous vous attendez à voir. Une Apple Watch peut contribuer des données au magasin Health de l'iPhone, mais l'application OpenClaw watchOS n'est pas requise pour les résumés HealthKit.

## Activer l'accès

### 1. Autoriser la commande Gateway

Ajoutez `health.summary` au tableau `gateway.nodes.allowCommands` existant dans `openclaw.json`. Conservez toutes les commandes déjà présentes :

```json5
{
  gateway: {
    nodes: {
      allowCommands: ["health.summary"],
    },
  },
}
```

`health.summary` est classée comme lourde en matière de confidentialité et n'est jamais autorisée par défaut par la plateforme iOS. Une entrée dans `gateway.nodes.denyCommands` remplace l'entrée d'autorisation. Voir [Politique de commande de nœud](/fr/nodes#command-policy).

### 2. Activer le partage sur l'iPhone

Dans l'application iOS :

1. Ouvrez **Paramètres -> Autorisations -> Confidentialité et accès -> Résumés de santé**.
2. Appuyez sur **Activer et partager les résumés**.
3. Lisez la divulgation, puis choisissez les catégories de santé qu'OpenClaw peut lire dans la feuille d'autorisation d'Apple.

Le commutateur enregistre votre choix de partage OpenClaw explicite. Il ne prétend pas qu'Apple a accordé chaque catégorie demandée.

L'activation des résumés de santé ajoute `health.summary` à la surface de commande déclarée du nœud. Approuvez la mise à jour d'appairage de nœud résultante :

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

Vérifiez ensuite que l'iPhone connecté expose une commande `health.summary` effective :

```bash
openclaw nodes describe --node "<iPhone name>"
```

## Demander le résumé d'aujourd'hui

Seul `today` est pris en charge. Il couvre minuit local jusqu'à l'heure de la demande, en utilisant le calendrier et le fuseau horaire actuels de l'iPhone.

```bash
openclaw nodes invoke \
  --node "<iPhone name>" \
  --command health.summary \
  --params '{"period":"today"}' \
  --json
```

Les agents peuvent appeler la même commande avec l'outil `nodes` :

```json
{
  "action": "invoke",
  "node": "<iPhone name>",
  "invokeCommand": "health.summary",
  "invokeParamsJson": "{\"period\":\"today\"}"
}
```

La charge utile du résumé contient :

| Champ                    | Signification                                       |
| ------------------------ | ----------------------------------------------------- |
| `period`                 | Toujours `today`                                |
| `startISO`               | Début local du jour, codé comme un instant ISO |
| `endISO`                 | Heure de la demande, codée comme un instant ISO       |
| `timeZoneIdentifier`     | Identifiant de fuseau horaire iPhone                   |
| `stepCount`              | Pas cumulatifs arrondis                      |
| `sleepDurationMinutes`   | Temps de sommeil dédupliqué, limité à aujourd'hui    |
| `restingHeartRateBpm`    | Fréquence cardiaque au repos moyenne                    |
| `workoutCount`           | Entraînements qui ont commencé aujourd'hui                   |
| `workoutDurationMinutes` | Durée totale de ces entraînements              |

Les champs de métrique sont facultatifs et sont omis lorsque HealthKit ne retourne aucune valeur lisible. Les étapes de sommeil et les sources qui se chevauchent sont fusionnées avant le calcul de la durée, de sorte que la même minute n'est pas comptée deux fois.

## Comportement de confidentialité

- L'agrégation se fait sur l'iPhone. Les échantillons bruts ne quittent pas l'appareil.
- L'agrégat demandé quitte l'iPhone via votre Gateway. Lorsqu'un agent le demande, l'agrégat atteint le fournisseur d'IA configuré et peut rester dans l'historique de chat. Une invocation CLI directe le retourne à l'opérateur CLI.
- OpenClaw demande un accès en lecture uniquement. Il ne peut pas ajouter ou modifier les données de santé.
- OpenClaw lit HealthKit uniquement lorsque `health.summary` est invoqué. Il n'y a pas d'ingestion de santé en arrière-plan.
- HealthKit ne révèle délibérément pas si l'accès en lecture a été refusé. Une métrique manquante peut signifier un accès refusé, aucun échantillon correspondant ou un type de données indisponible. OpenClaw ne peut pas distinguer ces cas.
- Le résumé est destiné au contexte personnel de santé et de remise en forme, non au diagnostic ou aux conseils médicaux.

Pour arrêter le partage, retournez à **Résumés de santé** et appuyez sur **Désactiver**. L'iPhone supprime alors la capacité de santé et la commande `health.summary` de sa surface de nœud. Vous pouvez également supprimer `health.summary` de `gateway.nodes.allowCommands` pour fermer le côté Gateway de la porte.

## Dépannage

### La commande n'est pas déclarée par le nœud

Confirmez que les résumés de santé sont activés dans l'application iOS et que l'iPhone est connecté. Exécutez `openclaw nodes pending` et approuvez toute mise à jour de capacité, puis inspectez à nouveau `openclaw nodes describe --node "<iPhone name>"`.

### La commande nécessite un consentement explicite

Ajoutez `health.summary` à `gateway.nodes.allowCommands`. Vérifiez également que `gateway.nodes.denyCommands` ne le contient pas ; la liste de refus l'emporte.

### `HEALTH_ACCESS_DISABLED`

Le commutateur de partage côté application est désactivé. Activez **Résumés de santé** sous **Confidentialité et accès** sur l'iPhone.

### Le résumé réussit mais les métriques manquent

Ouvrez l'application Santé d'Apple et confirmez que les données existent pour aujourd'hui. Vérifiez l'accès d'OpenClaw dans les paramètres de santé d'Apple, mais ne traitez pas un résultat vide comme une preuve que l'accès a été refusé : HealthKit cache intentionnellement cette distinction.

### Les anciennes plages échouent

La commande accepte uniquement `{"period":"today"}`. Les résumés multi-jours et historiques ne sont pas pris en charge.

## Connexes

- [Application iOS](/fr/platforms/ios)
- [Nœuds](/fr/nodes)
- [Référence de configuration Gateway](/fr/gateway/configuration-reference#gateway)
- [Audit de sécurité](/fr/gateway/security)
