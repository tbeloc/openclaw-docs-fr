---
summary: Utilisation informatique par défaut via une couture à deux fournisseurs (CUA + Peekaboo) derrière un contrat computer.act v2 typé, TCC propriétaire de l'application, prêt pour cloud-gateway/multi-nœud.
title: Plan d'utilisation informatique
read_when:
  - Implémentation ou révision de computer.act v2, la couture du fournisseur de nœud, ou les adaptateurs CUA/Peekaboo
  - Modification du spawning du pilote embarqué macOS, de la sélection du fournisseur UX, ou des artefacts de pilote gérés
  - Extension des surfaces d'intégration Peekaboo ou CUA
---

## Statut

Campagne active, démarrée le 2026-08-13. Dirigée par le propriétaire (steipete) : construire de manière autonome de bout en bout, tester en direct tout, livrer complètement. Le tableau de suivi ci-dessous est la source de vérité et est mis à jour au fur et à mesure que le travail arrive. Dérivé de la RFC 0025 (openclaw/rfcs `rfcs/0025-default-pluggable-computer-use.md`, RomneyDa) avec les décisions du propriétaire enregistrées sous Décisions. Coordonnez avec l'auteur de la RFC avant chaque vague (vérifiez les PR en direct pour éviter les collisions avec le travail du mainteneur en cours).

## Problème

L'utilisation informatique d'OpenClaw est au premier plan partout : le fulfiller macOS pilote le curseur partagé via Peekaboo embarqué + primitives CGEvent, et le plugin `cua-computer` utilise uniquement la portée de bureau global de CUA (`scope:"desktop"`, pas de `delivery_mode`). CUA et Peekaboo ont maintenant une véritable entrée scoped à la fenêtre en arrière-plan (pas de déplacement de curseur, pas de vol de focus, pas de changement d'espace), observation sémantique (arbre AX + capture d'écran + références d'éléments), et vérification structurée. Rien de tout cela n'atteint le modèle. L'adaptateur CUA actuel mappe 8 des 49 outils du pilote ; la surface MCP de Peekaboo (25 outils, clics par défaut en arrière-plan, liaison de cadre `see`, `verify_state`) n'est pas du tout accessible via `computer.act`.

## Objectifs

- Un contrat `computer.act` v2 typé (actions portables : cibles window/element/browser, `deliveryMode: background|foreground`, enveloppe de vérification) porté sur le protocole de nœud existant. Cloud gateway + plusieurs nœuds de bureau appairés fonctionne sans changement — les processus du fournisseur vivent sur le nœud.
- Deux fournisseurs macOS de première classe derrière une couture d'adaptateur dans le worker de nœud TypeScript propriétaire de l'application : CUA (`cua-driver serve --embedded`, spawné par l'application, TCC via chaîne de responsabilité) et Peekaboo (`peekaboo mcp` ou PeekabooAutomationKit en processus). Sélecteur de paramètres ; annonce de capacité exacte par fournisseur ; pas de fallback par appel entre eux.
- Windows/Linux via le même plugin groupé : démon CUA + proxy MCP supervisé par l'hôte de nœud ; PR compagnon Windows dans `openclaw/openclaw-windows-node`.
- Guidance du modèle (profil de compétence) enseignant l'échelle prioritaire en arrière-plan : observer la fenêtre -> action d'élément en arrière-plan -> pixel en arrière-plan -> premier plan -> bureau, piloté par les résultats structurés `effect`/refusal.
- Testé en direct à chaque étape ; les changements d'interface utilisateur sont livrés avec des captures d'écran/vidéo.

## Non-objectifs

- Passthrough MCP du fournisseur brut au modèle (rejeté dans la RFC 0025 ; casse la mise en cache multi-nœud, l'armement et les compétences).
- Réimplémentation des internes du pilote en TS/Swift.
- Parité d'enregistrement/relecture + isolation du navigateur pour Peekaboo (familles de capacités optionnelles ; CUA uniquement au départ).
- Wayland-au-delà-upstream, cibles Windows élevées/UIAccess en v1.

## Décisions (décisions du propriétaire, 2026-08-13)

1. **Pas de compatibilité rétroactive.** v2 remplace la charge utile `computer.act` v1 sur place sous les mêmes noms de commande. Ancien nœud + nouvelle gateway (ou inverse) reçoit un rejet `COMPUTER_CONTRACT_MISMATCH` typé — un résultat visible, pas une dégradation silencieuse. Pas de contrat de fil double, pas de voie de préservation v1. (Remplace la règle de livraison RFC « le contrat de fil v1 expédié reste vert ».)
2. **La LOC de production est une contrainte stricte.** La couture du fournisseur remplace l'enregistrement de commande dupliqué par plugin ; la refonte du plugin CUA supprime les branches de portée de bureau uniquement qu'elle rend obsolètes ; l'adaptateur Peekaboo réutilise le même noyau de mappage (liaison de cadre, codes de refusal, mise en file d'attente) plutôt que de le forker. Cible : LOC de production nette-nouvelle bornée par les suppressions ailleurs ; chaque vague rapporte son delta.
3. **Peekaboo est le nôtre à modifier.** Les lacunes se ferment en amont dans Peekaboo (clic moyen/triple, hold/mouse-down/up, `get_cursor_position` ; la forme de l'outil de navigateur peut s'aligner vers la famille de navigateur v2) au lieu de défauts d'adaptateur.
4. **Regrouper CUA sur macOS** (binaire universel de 38 Mo, re-signé avec notre ID de développeur à l'intérieur des ressources OpenClaw.app — la forme d'intégration recommandée en amont ; évite les frictions Gatekeeper). Windows/Linux utilisent le téléchargement géré épinglé par digest selon la RFC OC-10A.
5. **Les deux fournisseurs sont livrés ensemble sur macOS** avec un sélecteur de paramètres (CUA recommandé / Peekaboo). La sélection du fournisseur est locale au nœud ; le changement termine l'exécution active et fait tourner la génération du fournisseur.
6. **`invoke_menu` rejoint l'union d'action v2** (les deux fournisseurs le supportent ; la RFC l'a omis). L'enregistrement + les familles de navigateur sont des familles de capacités optionnelles — un fournisseur sans elles est de première classe, pas dégradé.

## Architecture

```text
Modèle ── un outil informatique (actions v2 typées, filtrées par capacité)
  Gateway (cloud OK) ── node.invoke("computer.act") sur protocole de nœud
    Nœud de bureau
      couture du fournisseur node-host (une enregistrement pour screen.snapshot + computer.act)
        ├─ Adaptateur CUA ── cua-driver mcp ──socket── cua-driver serve --embedded
        │    (macOS : spawné par l'application, chaîne de responsabilité TCC ; Win/Linux : supervisé par node-host,
        │     session interactive requise)
        └─ Adaptateur Peekaboo ── peekaboo mcp / PeekabooAutomationKit (macOS uniquement)
```

Invariants clés (tous existants, préservés) : liaison de cadre/observation (`displayFrameId` -> v2 `observationId`+`elementRef`, scoped à la génération), armement de commande dangereuse, approbation d'appairage, actions sérialisées, captures d'écran modèle uniquement, l'annulation libère l'entrée maintenue. TCC : OpenClaw.app sonde et maintient Accessibilité + Enregistrement d'écran au démarrage ; les enfants du pilote spawné par l'application héritent via la chaîne de responsabilité macOS — pas de nouvelle UX de permission.

Vérité de capacité du fournisseur (vérifiée en source, 2026-08-13) :

- CUA 0.19.3 : 49 outils MCP ; livraison en arrière-plan par appel avec refusals typés (`background_unavailable`, `background_occluded`, `background_uipi_blocked`, `off_space_or_ax_unresolved`) ; affichage SkyLight par pid sur macOS, injection de pointeur synthétique sur Windows, XTest/libei sur Linux (Wayland ne peut pas cibler les fenêtres en arrière-plan — capacité-gated). Le mode hôte embarqué, l'IPC hérité (#2410, PR 2545) et l'adaptateur de consentement protégé (#2411, PR 2578) sont tous contenus dans v0.13.1+ (vérifiés via containment de tag) — le 0.19.3 épinglé n'a besoin d'aucun bump.
- Peekaboo v4 : 25 outils MCP ; clics par défaut en arrière-plan (action AX-first, événements routés par pid, pointeur routé par fenêtre) ; `see` = capture d'écran + carte d'éléments + `reference_id` (mappe à la liaison d'observation) ; `verify_state` prédicats structurés sans focus ; gestion d'application/fenêtre/menu/dialogue/espace ; outil de navigateur CDP dans Chrome utilisateur avec consentement de connexion explicite. Manquant vs v2 : clic moyen/triple, entrée maintenue, position du curseur, enregistrement.

## Flux de travail et suivi

Les vagues suivent le plan de mise en œuvre de la RFC 0025, compressé par la règle sans compatibilité.
Statut : `todo | in-progress | pr | landed | blocked`.

| ID         | Travail                                                                                                                                            | Dépôt                 | Statut | Notes                                                                                                                                                            |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W0-FIX     | Matrice de parité + fixtures épinglées : 49 outils CUA + 25 outils Peekaboo classifiés par rapport à l'union v2 ; outils enregistrés/liste + fixtures de résultats           | openclaw              | landed | landed #123469 (d9646ad): 58 outils CUA + 26 Peekaboo, +1059 LOC test-only                                                                                        |
| W0-PIN     | Sélectionner + épingler la version CUA avec support IPC embarqué/hérité ; bump de dépendance (nécessite l'approbation de Dependency Guard)                                      | openclaw              | landed | résolu : 0.19.3 contient déjà #2410+#2411                                                                                                                    |
| W1-PROTO   | Types v2 : union d'action (+`invoke_menu`), union de cible, descripteur de capacité, enveloppe de résultat, codes d'erreur fermés ; **remplace** les paramètres v1 sur place | openclaw              | landed | landed #123544 (d19c755)                                                                                                                                         |
| W1-TOOL    | Outil informatique intégré v2 : schéma filtré par capacité, références d'observation, projection de résultat, pas de retry automatique                                          | openclaw              | landed | landed #123544: v1 651 / v2 742 tokens                                                                                                                           |
| W1-SEAM    | Couture fournisseur nœud-hôte : une inscription, sélection de fournisseur, génération, chemin de fermeture du cycle de vie ; absorbe l'inscription directe de cua-computer        | openclaw              | landed | landed #123509 (848a7e3): couture+contrat, prod +348/-217                                                                                                          |
| W2-CUA     | Refactorisation du plugin CUA sur la couture : mappage v2 complet (fenêtre/élément/arrière-plan), session par exécution, supprime l'adaptateur scope-desktop-only              | openclaw              | landed | landed #123604 (2af5eca): adaptateur v2 complet, prod +1129/-41                                                                                                        |
| W2-MAC     | Application macOS : bundle + re-signer le driver, spawn direct `serve --embedded`, remise de socket privée au worker, gestion du redémarrage TCC                        | openclaw              | landed | landed #123635 (19ace68): daemon propriétaire de l'app + picker + orphan reaping, live-proven                                                                                |
| W2-PKB     | Adaptateur Peekaboo sur la même couture (macOS) : mappage see/click/type/press/set_value/verify_state/app/window/menu                                     | openclaw              | todo   | nouveau vs RFC (était v1-only)                                                                                                                                         |
| W2-PKB-UP  | Peekaboo upstream : middle/triple click, hold_key + mouse down/up dans BackgroundInputDriver, get_cursor_position ; alignement de forme de navigateur optionnel   | Peekaboo              | todo   | approbation du propriétaire                                                                                                                                                   |
| W2-UX      | Paramètres -> Sélecteur de fournisseur Computer Use + liste de contrôle de disponibilité (les deux apps : macOS maintenant, Tauri Linux plus tard)                           | openclaw              | todo   | tranche RFC OC-10B ; possède les captures d'écran du picker (W2-MAC expédié sans elles ; verrou d'instance d'app à `/tmp/openclaw-UID-app-instances` peut bloquer un lancement de profil frais) |
| W3-GATE    | Porte d'intégration : verticale en direct sur macOS (les deux fournisseurs) + Linux X11 (CUA) : observer la fenêtre -> clic sur élément d'arrière-plan -> vérifier                  | openclaw              | todo   | RFC OC-8                                                                                                                                                         |
| W3-SKILL   | Profil de compétence épinglé en version : échelle d'arrière-plan en premier, précédence des résultats, pas d'instructions CLI/daemon                                               | openclaw              | todo   | RFC OC-9D                                                                                                                                                        |
| W4-BROWSER | Famille de navigateurs CUA (profil isolé en premier ; profil existant conditionné au consentement de l'adaptateur)                                                             | openclaw              | todo   | RFC OC-9B ; famille optionnelle                                                                                                                                       |
| W4-REC     | Famille d'enregistrement/ressources CUA avec racines propriétaires du nœud                                                                                               | openclaw              | todo   | RFC OC-9C ; famille optionnelle                                                                                                                                       |
| W4-WIN     | RP hôte CUA compagnon Windows                                                                                                                      | openclaw-windows-node | todo   | RFC WIN-1 ; après W1-SEAM/W2-CUA                                                                                                                                  |
| W4-ART     | Artefacts gérés : téléchargement épinglé par digest Win/Linux, mise à jour atomique + rollback                                                      | openclaw              | todo   | RFC OC-10A                                                                                                                                                       |
| W5-SEC     | Fermeture de sécurité : classification des actions à haut risque, audit de propriété de socket, tests d'arguments hostiles                                                       | openclaw              | todo   | RFC OC-10C                                                                                                                                                       |
| W5-ACC     | Acceptation multiplateforme packagée + déploiement du fournisseur par défaut                                                                                      | openclaw              | todo   | RFC OC-11/12                                                                                                                                                     |

Registre LOC de production (mis à jour par RP landed) : cible nette ≤ +1500 pour toute la
campagne excluant les tests/fixtures, financée par la suppression des branches v1-only, du
chemin d'inscription en double et de l'adaptateur à huit outils.

## Matrice de test en direct

Chaque vague porte une preuve en direct ; les fixtures unitaires seules n'avancent jamais le suivi.

- **macOS les deux fournisseurs** : passerelle de développement (répertoire `OPENCLAW_STATE_DIR` isolé, port propre)
  - build OpenClaw.app local signé sur l'un des Mac du propriétaire. Scénario :
    clic d'arrière-plan + saisie dans une fenêtre TextEdit non-frontmost tandis que l'app frontmost
    conserve le focus ; affirmer que l'app frontmost est inchangée, la position du curseur est inchangée,
    `verify_state`/`effect` confirme la modification. Vidéo via enregistrement d'écran pour
    les changements visibles dans l'UX.
- **Linux CUA** : hôte Crabbox Xvfb (recette prouvée dans la RP #117205) : le nœud enregistre
  la paire de commandes, capture d'écran réelle + id de frame, action de fenêtre d'arrière-plan contre
  l'app test xterm/gtk ; smoke Wayland sur Sway uniquement.
- **Windows** : compagnon openclaw-windows-node sur une boîte/VM Windows
  (labo Parallels) ; sonde de rejet de Session 0 sur SSH.
- **Multi-nœud** : deux Mac appairés + passerelle cloud ; sélection explicite de `node`,
  les tokens de frame ne traversent pas les nœuds, la génération du fournisseur tourne au redémarrage de l'app.
- **Sonde de décalage** (règle sans compatibilité) : ancienne app + nouvelle passerelle doit produire l'erreur de
  contrat typée dans le résultat de l'outil, pas le silence.

## Risques

- Churn de préversion CUA : tout épingle à une version acceptée + fixtures ;
  le décalage de version refuse fermé.
- Coût du token d'union v2 : mesuré dans W1-TOOL ; divisé en famille d'outils uniquement si un
  fournisseur ne peut pas consommer une union discriminée de manière fiable.
- Embedding de socket privée : répertoire propriétaire uniquement, 0600, propriété validée, chemin pré-existant
  rejeté ; mise à niveau vers IPC hérité quand la version épinglée le supporte.
- Les approbations de Dependency Guard (bump CUA, nouvelle surface de dépendance Peekaboo) interrompent
  l'autonomie ; les regrouper par vague.
- Collision avec le travail en cours de l'auteur de la RFC : vérifier les RP en direct avant chaque vague.
