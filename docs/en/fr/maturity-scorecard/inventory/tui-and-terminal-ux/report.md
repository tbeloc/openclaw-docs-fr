---
title: "Rapport de Maturité TUI"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité TUI

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (76%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (76%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `tui-and-terminal-ux` de `/Users/kevinlin/tmp/maturity/tui-and-terminal-ux` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de Couverture et Qualité proviennent des lignes de score archivées soutenues par des preuves. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                     | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Modes d'exécution](launch-modes-and-cli-entrypoints.md)                     | ❌  | `Beta (78%)`   | `Beta (72%)`  | `Beta (78%)`   | Lancement TUI de passerelle, Lancement de chat local, Lancement d'alias terminal, Lancement de message initial, Validation des options de lancement, Connexion de passerelle, Authentification de passerelle, Chargement de l'historique à l'attachement, Visibilité de reconnexion, RPC de commande de passerelle, Chat local intégré, Flux d'authentification local, Boucle de réparation de configuration, Récupération sans passerelle |
| [Entrée et Commandes](composer-keybindings-and-input-editing.md)              | ❌  | `Beta (76%)`   | `Beta (70%)`  | `Beta (76%)`   | Composition de message, Historique d'entrée, Raccourcis clavier, Gestion du collage et de la soumission occupée, Gestion IME et AltGr, Commandes slash, Sélecteurs, Paramètres                                                                                                                                     |
| [Gestion de Session](session-lifecycle-history-and-resume.md)                | ❌  | `Stable (80%)` | `Alpha (68%)` | `Stable (80%)` | Cycle de vie de session, Historique, Reprise                                                                                                                                                                                                                                                                    |
| [Exécution de Shell Local](local-shell-execution-and-approval-boundary.md)   | ❌  | `Beta (70%)`   | `Beta (76%)`  | `Beta (70%)`   | Routage de commande bang, Invite d'approbation, Affichage de la sortie de commande, Marqueur d'environnement d'exécution                                                                                                                                                                                        |
| [Rendu et Sécurité de Sortie](streaming-message-rendering-and-tool-cards.md) | ❌  | `Beta (76%)`   | `Beta (70%)`  | `Beta (76%)`   | Rendu de message en continu, Cartes d'outils, Primitives de rendu terminal, Sécurité de sortie                                                                                                                                                                                                                  |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Modes d'exécution

Ancres de recherche : Lancement TUI Gateway, Lancement chat local, Lancement alias terminal, Lancement message initial, Validation option de lancement, raccourcis clavier, mode gateway, mode local, Connexion Gateway, Authentification Gateway, Chargement historique à l'attachement, Visibilité reconnexion, RPC commandes Gateway, Chat local intégré, Flux auth local, Boucle réparation config, Récupération sans Gateway, sélecteurs + superpositions.

Note de catégorie : [Modes d'exécution](launch-modes-and-cli-entrypoints.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Lancement TUI Gateway : Couvre le lancement TUI Gateway sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation option local-vs-Gateway, relancement de lancement depuis les chemins setup/hatch, drapeaux message initial et timeout, et docs de lancement.
- Lancement chat local : Couvre le lancement chat local sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation option local-vs-Gateway, relancement de lancement depuis les chemins setup/hatch, drapeaux message initial et timeout, et docs de lancement.
- Lancement alias terminal : Couvre le lancement alias terminal sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation option local-vs-Gateway, relancement de lancement depuis les chemins setup/hatch, drapeaux message initial et timeout, et docs de lancement.
- Lancement message initial : Couvre le lancement message initial sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation option local-vs-Gateway, relancement de lancement depuis les chemins setup/hatch, drapeaux message initial et timeout, et docs de lancement.
- Validation option de lancement : Couvre la validation option de lancement sur `openclaw tui`, `openclaw chat`, `openclaw terminal`, validation option local-vs-Gateway, relancement de lancement depuis les chemins setup/hatch, drapeaux message initial et timeout, et docs de lancement.
- Connexion Gateway : Couvre la connexion Gateway sur résolution connexion Gateway, auth token/password/SecretRef pour TUI, exigences auth `--url`, enregistrement mode/capacité client, et transport gateway, auth, et comportement historique associés.
- Authentification Gateway : Couvre l'authentification Gateway sur résolution connexion Gateway, auth token/password/SecretRef pour TUI, exigences auth `--url`, enregistrement mode/capacité client, et transport gateway, auth, et comportement historique associés.
- Chargement historique à l'attachement : Couvre le chargement historique à l'attachement sur résolution connexion Gateway, auth token/password/SecretRef pour TUI, exigences auth `--url`, enregistrement mode/capacité client, et transport gateway, auth, et comportement historique associés.
- Visibilité reconnexion : Couvre la visibilité reconnexion sur résolution connexion Gateway, auth token/password/SecretRef pour TUI, exigences auth `--url`, enregistrement mode/capacité client, et transport gateway, auth, et comportement historique associés.
- RPC commandes Gateway : Couvre les RPC commandes Gateway sur résolution connexion Gateway, auth token/password/SecretRef pour TUI, exigences auth `--url`, enregistrement mode/capacité client, et transport gateway, auth, et comportement historique associés.
- Chat local intégré : Couvre le chat local intégré sur cycle de vie backend intégré, chargement catalogue modèle local, projection événement `chat.send` local, exécutions locales en file d'attente, historique session local, `/auth` local, docs réparation config local, et scénarios récupération sans Gateway.
- Flux auth local : Couvre le flux auth local sur cycle de vie backend intégré, chargement catalogue modèle local, projection événement `chat.send` local, exécutions locales en file d'attente, historique session local, `/auth` local, docs réparation config local, et scénarios récupération sans Gateway.
- Boucle réparation config : Couvre la boucle réparation config sur cycle de vie backend intégré, chargement catalogue modèle local, projection événement `chat.send` local, exécutions locales en file d'attente, historique session local, `/auth` local, docs réparation config local, et scénarios récupération sans Gateway.
- Récupération sans Gateway : Couvre la récupération sans Gateway sur cycle de vie backend intégré, chargement catalogue modèle local, projection événement `chat.send` local, exécutions locales en file d'attente, historique session local, `/auth` local, docs réparation config local, et scénarios récupération sans Gateway.

Docs principales :

- `docs/cli/tui.md`
- `docs/web/tui.md`
- `docs/cli/index.md`

### 2. Entrée et Commandes

Ancres de recherche : Composition message, Historique entrée, Raccourcis clavier, Gestion collage et busy-submit, Gestion IME et AltGr, mode gateway, mode local, Commandes slash, Sélecteurs, Paramètres, commandes slash tui et terminal ux, sélecteurs, et paramètres, commandes slash, sélecteurs, et paramètres.

Note de catégorie : [Entrée et Commandes](composer-keybindings-and-input-editing.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Composition message : Couvre la composition message sur éditeur, gestionnaire submit, historique entrée, routage slash/shell local, comportement busy-submit, fallback collage, dedupe backspace, raccourcis Ctrl/Esc, gestion AltGr, et raccourcis clavier documentés.
- Historique entrée : Couvre l'historique entrée sur éditeur, gestionnaire submit, historique entrée, routage slash/shell local, comportement busy-submit, fallback collage, dedupe backspace, raccourcis Ctrl/Esc, gestion AltGr, et raccourcis clavier documentés.
- Raccourcis clavier : Couvre les raccourcis clavier sur éditeur, gestionnaire submit, historique entrée, routage slash/shell local, comportement busy-submit, fallback collage, dedupe backspace, raccourcis Ctrl/Esc, gestion AltGr, et raccourcis clavier documentés.
- Gestion collage et busy-submit : Couvre la gestion collage et busy-submit sur éditeur, gestionnaire submit, historique entrée, routage slash/shell local, comportement busy-submit, fallback collage, dedupe backspace, raccourcis Ctrl/Esc, gestion AltGr, et raccourcis clavier documentés.
- Gestion IME et AltGr : Couvre la gestion IME et AltGr sur éditeur, gestionnaire submit, historique entrée, routage slash/shell local, comportement busy-submit, fallback collage, dedupe backspace, raccourcis Ctrl/Esc, gestion AltGr, et raccourcis clavier documentés.
- Commandes slash : Couvre les commandes slash sur analyse commande slash, transfert commande, commandes local-only, sélecteurs modèle/agent/session, superposition paramètres, sélecteur mode contexte, liste commande Gateway dynamique, commandes patch session, et docs commande.
- Sélecteurs : Couvre les sélecteurs sur analyse commande slash, transfert commande, commandes local-only, sélecteurs modèle/agent/session, superposition paramètres, sélecteur mode contexte, liste commande Gateway dynamique, commandes patch session, et docs commande.
- Paramètres : Couvre les paramètres sur analyse commande slash, transfert commande, commandes local-only, sélecteurs modèle/agent/session, superposition paramètres, sélecteur mode contexte, liste commande Gateway dynamique, commandes patch session, et docs commande.

Docs principales :

- `docs/web/tui.md`

### 3. Gestion de Session

Ancres de recherche : Cycle de vie session, Historique, Reprise, cycle de vie session tui et terminal ux, historique, et reprise, cycle de vie session, historique, et reprise.

Note de catégorie : [Gestion de Session](session-lifecycle-history-and-resume.md)

Décisions de score :

- Couverture : `Stable (80%)`
- Qualité : `Alpha (68%)`
- Complétude : `Stable (80%)`
- LTS : ❌

Fonctionnalités :

- Cycle de vie session : Couvre le cycle de vie session sur résolution clé session, persistance session dernière sélection, politique sélecteur session, chargement historique, et comportement cycle de vie session, historique, et reprise associé.
- Historique : Couvre l'historique sur résolution clé session, persistance session dernière sélection, politique sélecteur session, chargement historique, et comportement cycle de vie session, historique, et reprise associé.
- Reprise : Couvre la reprise sur résolution clé session, persistance session dernière sélection, politique sélecteur session, chargement historique, et comportement cycle de vie session, historique, et reprise associé.

Docs principales :

- `docs/web/tui.md`
- `docs/cli/sessions.md`

### 4. Exécution Shell Local

Ancres de recherche : Routage commande bang, Invite approbation, Affichage sortie commande, Marqueur environnement exécution, raccourcis clavier, mode gateway, mode local, sélecteurs + superpositions.

Note de catégorie : [Exécution Shell Local](local-shell-execution-and-approval-boundary.md)

Décisions de score :

- Couverture : `Beta (70%)`
- Qualité : `Beta (76%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Routage commande bang : Couvre le routage commande bang sur routage `!`, invite approbation exec local, superposition Oui/Non, exécution commande, capture et limitation sortie, rendu sortie/erreur, marqueur environnement, gestion cwd, et docs qui distinguent exécution hôte local d'exécution Gateway.
- Invite approbation : Couvre l'invite approbation sur routage `!`, invite approbation exec local, superposition Oui/Non, exécution commande, capture et limitation sortie, rendu sortie/erreur, marqueur environnement, gestion cwd, et docs qui distinguent exécution hôte local d'exécution Gateway.
- Affichage sortie commande : Couvre l'affichage sortie commande sur routage `!`, invite approbation exec local, superposition Oui/Non, exécution commande, capture et limitation sortie, rendu sortie/erreur, marqueur environnement, gestion cwd, et docs qui distinguent exécution hôte local d'exécution Gateway.
- Marqueur environnement exécution : Couvre le marqueur environnement exécution sur routage `!`, invite approbation exec local, superposition Oui/Non, exécution commande, capture et limitation sortie, rendu sortie/erreur, marqueur environnement, gestion cwd, et docs qui distinguent exécution hôte local d'exécution Gateway.

Docs principales :

- `docs/web/tui.md`
- `docs/cli/tui.md`

### 5. Rendu et Sécurité Sortie

Ancres de recherche : Rendu message streaming, Cartes outils, rendu message streaming tui et terminal ux et cartes outils, rendu message streaming et cartes outils, Primitives rendu terminal, Sécurité sortie, primitives rendu terminal tui et terminal ux et sécurité sortie, primitives rendu terminal et sécurité sortie.

Note de catégorie : [Rendu et Sécurité Sortie](streaming-message-rendering-and-tool-cards.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Rendu message streaming : Couvre le rendu message streaming sur rendu journal chat, assemblage flux assistant, résolution final/erreur, visibilité réflexion, et comportement rendu message streaming et cartes outils associé.
- Cartes outils : Couvre les cartes outils sur rendu journal chat, assemblage flux assistant, résolution final/erreur, visibilité réflexion, et comportement rendu message streaming et cartes outils associé.
- Primitives rendu terminal : Couvre les primitives rendu terminal sur aides sortie terminal partagées utilisées par surfaces CLI/TUI : écriture flux sécurisée, assainissement texte, gestion ANSI/OSC, enveloppe tableau, et comportement primitives rendu terminal et sécurité sortie associé.
- Sécurité sortie : Couvre la sécurité sortie sur aides sortie terminal partagées utilisées par surfaces CLI/TUI : écriture flux sécurisée, assainissement texte, gestion ANSI/OSC, enveloppe tableau, et comportement primitives rendu terminal et sécurité sortie associé.

Docs principales :

- `docs/web/tui.md`
- `docs/cli/qr.md`
- `docs/cli/logs.md`
- `docs/cli/completion.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche agent catégorie en direct avant de traiter un score élevé comme porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, les docs, et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/tui-and-terminal-ux/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuve archivée :
  `/Users/kevinlin/tmp/maturity/tui-and-terminal-ux`.
