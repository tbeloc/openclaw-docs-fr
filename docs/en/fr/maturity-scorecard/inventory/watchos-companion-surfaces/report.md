---
title: "Rapport de maturité des surfaces compagnon watchOS"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité des surfaces compagnon watchOS

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Expérimental (45%)`
- Qualité : `Alpha (57%)`
- Complétude : `Expérimental (45%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `watchos-companion-surfaces` de `/Users/kevinlin/tmp/maturity/watchos-companion-surfaces` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuve archivée et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                          | LTS | Couverture           | Qualité              | Complétude           | Fonctionnalités à évaluer                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------- | --- | -------------------- | -------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Livraison et récupération](apns-background-recovery-and-stale-approval-cleanup.md)   | ❌  | `Expérimental (46%)` | `Alpha (60%)`        | `Expérimental (46%)` | Enregistrement relais/direct APNs tel qu'il affecte, Push silencieux, ID de récupération d'approbation en attente, Approbation d'exécution côté passerelle iOS, Transport WatchConnectivity côté iPhone, Activation du récepteur côté montre, Secours de livraison parmi les messages accessibles |
| [Approbations d'exécution](exec-approval-review-decisions-and-snapshots.md)                 | ❌  | `Alpha (54%)`        | `Alpha (64%)`        | `Alpha (54%)`        | Invite d'approbation d'exécution sur la montre, Interface utilisateur de liste/détail d'approbation sur la montre, Mise en cache d'invite côté iPhone                                                                                                                                                         |
| [Distribution et support](packaging-signing-and-distribution-boundary.md)        | ❌  | `Expérimental (38%)` | `Expérimental (48%)` | `Expérimental (38%)` | Application montre, Variables de signature/profil, Statut public/support, Journal des modifications, Métadonnées de version, Thèmes de bogues/régressions historiques pertinents pour la notation                                                                                                |
| [Notifications et réponses](watch-notify-command-payloads-and-prompt-defaults.md) | ❌  | `Expérimental (44%)` | `Alpha (57%)`        | `Expérimental (44%)` | watch.status, Normalisation de la charge utile, Secours de notification iOS en miroir quand montre, Boutons d'action de montre à partir d'invites génériques, Charges utiles de réponse montre-vers-iPhone, Dédoublonnage côté iPhone, Secours d'action de notification iOS en miroir                            |
| [Interface utilisateur de la montre](watch-inbox-ui-and-persistent-state.md)                            | ❌  | `Expérimental (42%)` | `Alpha (58%)`        | `Expérimental (42%)` | Point d'entrée de l'application montre, Boîte de réception générique, État persistant de la boîte de réception de la montre                                                                                                                                                            |

## Barème de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct, ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une
  fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; ils ne
  augmentent ni ne diminuent la qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifiques à la surface prévu. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `qualité > 80 et couverture > 90`, ou quand la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Adorable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité plus élevé.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Livraison et récupération

Ancres de recherche : surfaces compagnon watchos apns récupération en arrière-plan et nettoyage d'approbation obsolète, récupération en arrière-plan apns et nettoyage d'approbation obsolète, surfaces compagnon watchos statut de session watchconnectivity et livraison, statut de session watchconnectivity et livraison.

Note de catégorie : [Livraison et récupération](apns-background-recovery-and-stale-approval-cleanup.md)

Décisions de notation :

- Couverture : `Expérimental (46%)`
- Qualité : `Alpha (60%)`
- Complétude : `Expérimental (46%)`
- LTS : ❌

Fonctionnalités :

- Enregistrement relais/direct APNs tel qu'il affecte : Enregistrement relais/direct APNs tel qu'il affecte la récupération/réveil d'approbation de montre
- Push silencieux : Push silencieux, actualisation en arrière-plan, et chemins de réveil de localisation significative
- ID de récupération d'approbation en attente : ID de récupération d'approbation en attente, actualisation d'instantané, et nettoyage résolu/obsolète
- Approbation d'exécution côté passerelle iOS : Ciblage APNs d'approbation d'exécution côté passerelle iOS
- Transport WatchConnectivity côté iPhone : Transport WatchConnectivity côté iPhone et instantané de statut
- Activation du récepteur côté montre : Activation du récepteur côté montre et gestion de la charge utile entrante
- Secours de livraison parmi les messages accessibles : Secours de livraison parmi les messages accessibles, informations utilisateur en file d'attente, et instantanés de contexte d'application

Docs principaux :

- `docs/platforms/ios.md`

### 2. Approbations d'exécution

Ancres de recherche : surfaces compagnon watchos examen d'approbation d'exécution, décisions, et instantanés, examen d'approbation d'exécution, décisions, et instantanés.

Note de catégorie : [Approbations d'exécution](exec-approval-review-decisions-and-snapshots.md)

Décisions de notation :

- Couverture : `Alpha (54%)`
- Qualité : `Alpha (64%)`
- Complétude : `Alpha (54%)`
- LTS : ❌

Fonctionnalités :

- Invite d'approbation d'exécution sur la montre : Invite d'approbation d'exécution sur la montre, instantané, résoudre, résolu, et charges utiles expirées
- Interface utilisateur de liste/détail d'approbation sur la montre : Interface utilisateur de liste/détail d'approbation sur la montre et boutons de décision
- Mise en cache d'invite côté iPhone : Mise en cache d'invite côté iPhone, publication d'invite de montre, gestion d'instantané, et résolution

Docs principaux :

- `docs/tools/exec-approvals.md`
- `docs/platforms/ios.md`

### 3. Distribution et support

Ancres de recherche : surfaces compagnon watchos empaquetage, signature, et limite de distribution, empaquetage, signature, et limite de distribution, surfaces compagnon watchos historique source et preuve de version, historique source et preuve de version.

Note de catégorie : [Distribution et support](packaging-signing-and-distribution-boundary.md)

Décisions de notation :

- Couverture : `Expérimental (38%)`
- Qualité : `Expérimental (48%)`
- Complétude : `Expérimental (38%)`
- LTS : ❌

Fonctionnalités :

- Application montre : Application montre et cibles d'extension WatchKit
- Variables de signature/profil : Variables de signature/profil, identifiants de bundle, ressources d'icône, et flux de version bêta iOS
- Statut public/support : Statut public/support pour le compagnon watchOS tel que distribué via l'application iOS
- Journal des modifications : Journal des modifications et preuves d'historique de repo pour la maturité du compagnon watchOS
- Métadonnées de version : Métadonnées de version et preuves de préparation App Store/TestFlight
- Thèmes de bogues/régressions historiques pertinents pour la notation : Thèmes de bogues/régressions historiques pertinents pour la notation de la qualité source actuelle

Docs principaux :

- `docs/platforms/ios.md`

### 4. Notifications et réponses

Ancres de recherche : surfaces compagnon watchos commande watch notify, charges utiles, et valeurs par défaut d'invite, commande watch notify, charges utiles, et valeurs par défaut d'invite, surfaces compagnon watchos actions de réponse rapide et remise d'agent, actions de réponse rapide et remise d'agent.

Note de catégorie : [Notifications et réponses](watch-notify-command-payloads-and-prompt-defaults.md)

Décisions de notation :

- Couverture : `Expérimental (44%)`
- Qualité : `Alpha (57%)`
- Complétude : `Expérimental (44%)`
- LTS : ❌

Fonctionnalités :

- watch.status : Contrats de commande watch.status et watch.notify
- Normalisation de la charge utile : Normalisation de la charge utile pour titre/corps, métadonnées d'invite/session, priorité, risque, et boutons d'action
- Secours de notification iOS en miroir quand montre : Secours de notification iOS en miroir quand la livraison de montre est en file d'attente
- Boutons d'action de montre à partir d'invites génériques : Boutons d'action de montre à partir de notifications d'invite génériques
- Charges utiles de réponse montre-vers-iPhone : Comportement des charges utiles de réponse montre-vers-iPhone, statut, et vérification visible par l'opérateur.
- Dédoublonnage côté iPhone : Dédoublonnage côté iPhone, mise en file d'attente hors ligne, et transfert de demande d'agent
- Secours d'action de notification iOS en miroir : Secours d'action de notification iOS en miroir

Docs principaux :

- `docs/platforms/ios.md`

### 5. Interface utilisateur de la montre

Ancres de recherche : surfaces compagnon watchos interface utilisateur boîte de réception montre et état persistant, interface utilisateur boîte de réception montre et état persistant.

Note de catégorie : [Interface utilisateur de la montre](watch-inbox-ui-and-persistent-state.md)

Décisions de notation :

- Couverture : `Expérimental (42%)`
- Qualité : `Alpha (58%)`
- Complétude : `Expérimental (42%)`
- LTS : ❌

Fonctionnalités :

- Point d'entrée de l'application montre : Point d'entrée de l'application montre et navigation SwiftUI
- Boîte de réception générique : Boîte de réception générique, actions d'invite, vues de chargement/liste/détail d'approbation d'exécution
- État persistant de la boîte de réception de la montre : État persistant de la boîte de réception de la montre et suppression de livraison en double

Docs principaux :

- `docs/platforms/ios.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, les docs, et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/watchos-companion-surfaces/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuve archivée :
  `/Users/kevinlin/tmp/maturity/watchos-companion-surfaces`.
