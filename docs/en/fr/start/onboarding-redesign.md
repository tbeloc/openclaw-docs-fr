---
summary: "Plan de mise en œuvre pour la refonte de l'intégration des dépositaires (document vivant)"
read_when:
  - You are implementing or reviewing a phase of the onboarding redesign
title: "Refonte de l'intégration"
---

# Refonte de l'intégration — plan de mise en œuvre

> **Document vivant.** Cette page suit la refonte de l'intégration des dépositaires au niveau de la mise en œuvre et est mise à jour à chaque phase fusionnée. Lorsque la dernière phase est fusionnée, cette page est réécrite en tant que guide d'intégration destiné aux utilisateurs et rejoint la navigation de la documentation. Elle n'est intentionnellement pas dans `docs.json` jusqu'à ce moment.

## Étoile polaire

Un utilisateur non technique tape `openclaw onboard` (ou ouvre l'application) et est accueilli par une présence conversationnelle unique — OpenClaw, le dépositaire du système (« dépositaire » est le nom interne uniquement ; l'utilisateur voit toujours « OpenClaw ») — qui trouve son IA, configure tout avec des valeurs par défaut annoncées au lieu de questions, fait éclore son agent comme un moment d'identité visible, et reste accessible à jamais après en tant que gardien du système. Magie par défaut, une limite de consentement, pas d'impasses.

Principes de conception (décidés, ne pas remettre en question légèrement) :

- **Les valeurs par défaut annoncées avec annulation facile** remplacent les questions bloquantes. La seule exigence stricte est l'inférence fonctionnelle ; tout le reste est une offre.
- **La question zéro est la limite du consentement** : « Accès complet » (recommandé) signifie que la découverte est silencieuse et automatique ; « Demander d'abord » place chaque découverte — balayage de l'IA et balayage des sources de mémoire — derrière un seul oui explicite, avec un chemin entièrement manuel qui ne balaye jamais.
- **La conversation comme interface utilisateur avec intelligence progressive** : la surface du dépositaire existe avant que toute IA ne fonctionne (dialogue scriptée), devient soutenue par le modèle dès qu'une route se vérifie, et le dit visiblement.
- **L'éclosion est une cérémonie** : même fil, échange d'avatar, l'agent se nomme lui-même et choisit son propre visage. Le dépositaire enseigne la hiérarchie une fois : « demandez-moi à propos du système, ou demandez simplement à votre agent — il relaye. »
- **Les installations configurées sont sacrées** : réexécuter l'intégration est une passe de vérification. Elle ne réapplique jamais la configuration et ne redémarre jamais le service Gateway.
- **Les modèles faibles obtiennent une surface réduite** (auto `localModelLean`), expliquée en termes simples — jamais en termes d'outils, de mode code ou de fenêtres de contexte.

## Phases

| #   | Phase                                                                                                                                                                     | Surface                  | Statut                                                                     |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | -------------------------------------------------------------------------- |
| 1   | Recommandations de plugins d'applications installées (balayage, candidats, correspondance IA, étape de l'assistant, commande de nœud `device.apps`)                       | service + assistant classique | PR [#109668](https://github.com/openclaw/openclaw/pull/109668) — en révision |
| 2   | Épine dorsale du dépositaire CLI (question zéro, théâtre de découverte, application automatique + éclosion)                                                              | CLI guidée               | PR [#109841](https://github.com/openclaw/openclaw/pull/109841) — en révision |
| 3   | Remise en main navigateur en premier (détection de session GUI, attendre la connexion du tableau de bord, TUI comme solution de secours)                                 | CLI → web                | planifié                                                                    |
| 4   | Surface du dépositaire web (rendu de carte d'option partagé avec l'outil de question, états pré-IA scriptés sur `openclaw.chat`, remise de chat post-assistant)         | Interface de contrôle    | planifié                                                                    |
| 5   | Éclosion et amorçage (création d'agent vierge, auto-nommage, avatar auto-dessiné via génération d'image si disponible, recommandations comme dernière étape d'amorçage, opt-in d'auto-apprentissage) | amorçage d'agent         | planifié                                                                    |
| 6   | Présence du dépositaire (entrée de barre latérale épinglée, dock Paramètres avec commentaire réactif aux événements, invocation de canal et récupération d'agent arrêté, script de modèle faible) | web + canaux             | planifié                                                                    |
| 7   | Résilience (dépositaire accessible sur configuration cassée, récupération de surface partielle, auto-docteur)                                                           | passerelle              | suivi                                                                      |

## Notes de mise en œuvre par phase

### Phase 1 — recommandations d'applications (PR #109668)

- Scanneur : `src/infra/installed-apps.ts` (énumération macOS sans TCC).
- Candidats : catalogues officiels + recherche ClawHub, budget de 20 s, dégradation gracieuse hors ligne.
- Correspondance IA : une complétion sur la route vérifiée
  (`src/system-agent/setup-app-recommendations.ts`) ; pas de carte bundle-id curée —
  le modèle rejette les chevauchements de noms accidentels.
- Commande de nœud `device.apps` (hôte de nœud TS, parité d'enveloppe Android), partage désactivé par défaut ; commutateur de suppression de passerelle `wizard.appRecommendations`.
- La livraison vit actuellement dans l'assistant classique
  (`src/wizard/setup.app-recommendations.ts`) ; elle se réoriente vers la queue d'amorçage en phase 5 (le service prend déjà une source d'inventaire injectable).
- Également corrigé : les invites `completeSetupInference` personnalisées n'héritent plus du plafond de sortie de sonde de vérification de 32 jetons.

### Phase 2 — épine dorsale du dépositaire CLI (PR #109841)

- Refonte du flux dans `src/commands/onboard-guided.ts` ; l'intégration de la passerelle distante
  conserve sa remise de chat héritée via `handoffMode: "chat"`.
- La question zéro persiste `wizard.accessMode` (« full » | « guarded ») ; les réexécutions
  utilisent par défaut le choix enregistré. Guarded + manuel utilise
  `listManualSetupInferenceOptions` (config/manifestes uniquement, pas de sondage) et
  ignore le balayage des sources de mémoire.
- Découverte : collecte d'échecs silencieux (ligne de résumé unique ; détails derrière
  « Voir d'autres options »), boutade d'agent de codage, route par défaut annoncée.
- Installations fraîches : `applySystemAgentSetup` (le « oui » conversationnel déterministe), puis éclosion via `launchTuiCli` ensemencée avec le message d'amorçage.
  Installations configurées (modèle ou configuration de passerelle préexistants) : vérification
  uniquement — pas d'application, pas de redémarrage du service Gateway. L'échec de l'application revient au
  chat conversationnel.

### Phase 3 — remise en main navigateur en premier (planifiée)

- Détecter une session graphique (Aqua macOS vs `SSH_CONNECTION`) ; GUI ouvre l'URL du tableau de bord tokenisé, headless l'imprime en grand et attend.
- Le signal de disponibilité est un client de l'interface de contrôle se connectant à la passerelle — pas le code de sortie `open`. Pas de connexion dans la fenêtre → le même flux s'affiche dans le terminal. Le TUI cesse d'être une question et devient le plan C.

### Phase 4 — surface du dépositaire web (planifiée)

- Un composant de carte d'option (en-tête, question, 2–4 cartes, une recommandée,
  toujours ignorable) partagé par l'intégration scriptée et l'outil de question d'agent
  (les formes `src/agents/harness/user-input-bridge.ts`).
- Dialogue pré-IA scriptée comme une petite machine d'état consommée par CLI et web ;
  la page web s'exécute sur le RPC `openclaw.chat` existant en mode d'intégration masquant le chrome. Les pages de l'assistant de configuration du modèle restent comme solution de secours « Plus d'options », intégrées en tant que cartes.
- Le dépositaire scriptée ne doit jamais feindre l'intelligence : l'entrée de texte libre avant
  qu'une route se vérifie obtient un « laisse-moi d'abord faire fonctionner mon cerveau » gracieux.

### Phase 5 — éclosion et amorçage (planifiée)

- Le dépositaire crée un agent sans nom (appel d'outil) ; l'amorçage de l'agent s'ouvre
  avec auto-nommage et un avatar auto-dessiné (échelle de génération d'image : candidats générés par modèle → marques prédéfinies → garder le logo). Même fil, échange d'avatar ; la marque de griffe reste réservée au dépositaire.
- Les recommandations (service de phase 1, balayage stocké) arrivent comme dernière
  étape d'amorçage avant la suppression du fichier d'amorçage : « ensemble minimal ou commodité maximale ? » Les boutons de connexion de canal portent des livrets de configuration par canal ; l'agent collecte les identifiants de manière conversationnelle et relaye les écritures de configuration au dépositaire (« demander à OpenClaw… » est l'idiome canonique).
- L'auto-apprentissage est demandé, non annoncé, et double le consentement de l'atelier de compétences ; ClawHub est décrit comme « balayé, signé et vérifié avant installation » —
  rien de plus fort.
- Auto-éclosion : après vérification de l'IA, l'éclosion procède avec une annonce
  (« Vous pouvez toujours me trouver dans Paramètres… éclosion maintenant ») ; le bouton ignore seulement le battement. Zéro agent à la première exécution auto-éclot ; zéro agent après suppression offre à la place.

### Phase 6 — présence du dépositaire (planifiée)

- Entrée de barre latérale épinglée (session permanente — c'est la piste d'audit de configuration) et volet d'atterrissage Paramètres ancré avec la même session ; les réponses créent des liens profonds vers les sections des paramètres.
- Commentaire réactif aux événements avec garde-fous anti-Clippy : changements conséquents ou échoués uniquement, au maximum une fois par visite des paramètres sauf demande.
- Canaux : jour après jour invisibles (l'agent relaye) ; accessibles par invocation explicite et sur les événements d'agent arrêté dans le même fil, avec son propre nom et avatar où la plateforme le permet.
- Modèle faible détecté à la configuration : auto-définir `localModelLean`, et le dépositaire le dit en termes simples avec une offre de mise à niveau.

### Phase 7 — résilience (suivi)

- Le dépositaire doit être accessible peu importe la cassure de la configuration : récupérer
  les surfaces fonctionnelles (selon les règles SecretRef de démarrage dégradé de la passerelle), dire clairement ce qui est cassé, et exécuter `openclaw doctor` automatiquement.

## Journal des décisions

- Balayage magique avec commutateur de suppression, pas de consentement en premier (phase 1 ; la divulgation vit
  dans la ligne de progression du balayage et la note des résultats).
- Verticale complète incluant la commande de nœud `device.apps` (phase 1).
- Deux cartes d'accès, pas trois ; consentement en amont du choix (phase 2).
- Auto-éclosion avec annonce, pas un bouton bloquant (phases 2/5).
- Le dépositaire obtient la présence du canal (invocation + récupération), pas web/CLI uniquement
  (phase 6).
- L'éclosion se produit dans le même fil avec un échange d'avatar ; après achèvement l'application
  passe à l'interface utilisateur régulière (phase 5).
- La surface des paramètres garde le nom « Paramètres » ; le dépositaire y vit
  (et dans la barre latérale) plutôt que de la remplacer (phase 6).
- La copie destinée à l'utilisateur ne dit jamais « mode code », « outils » ou « fenêtre de contexte » lors de l'explication du rognage de modèle faible (phase 6).
