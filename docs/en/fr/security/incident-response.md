---
summary: "Comment OpenClaw trie, répond et assure le suivi des incidents de sécurité"
title: "Réponse aux incidents"
read_when:
  - Responding to a security report or suspected security incident
  - Preparing a coordinated disclosure or patched security release
  - Reviewing post-incident follow-up expectations
---

## 1. Détection et triage

Nous surveillons les signaux de sécurité provenant de :

- GitHub Security Advisories (GHSA) et rapports de vulnérabilités privés.
- Problèmes/discussions publics GitHub lorsque les rapports ne sont pas sensibles.
- Signaux automatisés (par exemple Dependabot, CodeQL, avis npm et analyse des secrets).

Triage initial :

1. Confirmer le composant affecté, la version et l'impact de la limite de confiance.
2. Classer comme problème de sécurité ou renforcement/pas d'action en utilisant les règles de portée et hors portée du fichier `SECURITY.md` du référentiel.
3. Un propriétaire d'incident répond en conséquence.

## 2. Évaluation

Guide de sévérité :

- **Critique :** Compromission de paquet/version/référentiel, exploitation active ou contournement de limite de confiance non authentifié avec contrôle ou exposition de données à fort impact.
- **Élevé :** Contournement de limite de confiance vérifié nécessitant des conditions préalables limitées (par exemple authentifié mais action non autorisée à fort impact), ou exposition des identifiants sensibles appartenant à OpenClaw.
- **Moyen :** Faiblesse de sécurité significative avec impact pratique mais exploitabilité limitée ou prérequis substantiels.
- **Faible :** Résultats de défense en profondeur, déni de service étroitement limité ou lacunes de renforcement/parité sans contournement de limite de confiance démontré.

## 3. Réponse

1. Accuser réception au rapporteur (en privé si sensible).
2. Reproduire sur les versions supportées et le dernier `main`, puis implémenter et valider un correctif avec couverture de régression.
3. Pour les incidents critiques/élevés, préparer les versions corrigées aussi rapidement que possible.
4. Pour les incidents moyen/faible, appliquer le correctif dans le flux de version normal et documenter les conseils d'atténuation.

## 4. Communication

Nous communiquons via :

- GitHub Security Advisories dans le référentiel affecté.
- Entrées de notes de version/changelog pour les versions corrigées.
- Suivi direct du rapporteur sur le statut et la résolution.

Politique de divulgation :

- Les incidents critiques/élevés doivent recevoir une divulgation coordonnée, avec émission de CVE le cas échéant.
- Les résultats de renforcement à faible risque peuvent être documentés dans les notes de version ou les avis sans CVE, selon l'impact et l'exposition des utilisateurs.

## 5. Récupération et suivi

Après la livraison du correctif :

1. Vérifier les remédiation dans les artefacts CI et de version.
2. Effectuer un court examen post-incident (chronologie, cause première, lacune de détection, plan de prévention).
3. Ajouter des tâches de suivi de renforcement/tests/docs et les suivre jusqu'à leur achèvement.
