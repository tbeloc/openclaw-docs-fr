---
summary: "Comment la propriété de session et la présence fonctionnent lorsque plusieurs personnes exploitent un agent"
read_when:
  - Vous partagez un agent OpenClaw avec d'autres opérateurs
  - Vous devez comprendre le propriétaire de session et les indicateurs de présence
  - Vous décidez si un agent partagé fournit suffisamment d'isolation
title: "Mode multi-utilisateur"
---

Le mode multi-utilisateur permet à plusieurs personnes de confiance d'exploiter le même agent OpenClaw. Il ajoute la propriété de session, la présence en direct et le filtrage par créateur afin qu'une équipe puisse savoir qui a commencé le travail et qui le regarde actuellement.

## Limite de confiance

Tous ceux qui peuvent exploiter un agent peuvent le faire faire n'importe quoi que cet agent peut faire. La propriété de session, la visibilité dans la barre latérale et les indicateurs de présence sont des fonctionnalités d'utilisabilité, pas des limites de sécurité.

Si les gens ne doivent pas accéder aux sessions, outils, identifiants ou fichiers les uns des autres, donnez-leur des agents séparés ou des limites de confiance de passerelle/hôte séparées. Ne vous fiez pas aux avatars de propriétaire ou aux filtres pour l'isolation.

## Propriété et présence

Les nouvelles sessions enregistrent leur créateur lorsque la passerelle dispose d'une identité de confiance disponible. L'identité de proxy de confiance a la priorité ; sinon OpenClaw utilise l'étiquette d'opérateur ou le nom d'affichage de l'appareil appairé. Les sessions plus anciennes et les sessions créées sans l'une ou l'autre identité n'ont pas de marque de propriétaire.

L'application web maintient la propriété et la présence visuellement distinctes :

- Un avatar de propriétaire solide est permanent pour la durée de vie de cette session.
- Les avatars de présence en anneau ou translucides montrent les personnes actuellement connectées ou qui regardent.
- Le filtre de personne de la barre latérale affiche les sessions créées par une identité tout en préservant les groupes personnalisés existants.

Lorsque moins de deux créateurs distincts apparaissent dans la liste de sessions chargée, OpenClaw masque tous les éléments de propriété et de filtre de personne. Une passerelle mono-utilisateur ressemble donc à l'inchangée.

## Attribution de tour

L'attribution de l'expéditeur du tour est au mieux un effort. La direction peut fusionner l'entrée dans un tour actif, donc la transcription ne peut pas toujours représenter la contribution de chaque personne comme un tour séparé.

## Connexes

- [La session principale](/fr/concepts/main-session)
- [Gestion de session](/fr/concepts/session)
- [Présence](/fr/concepts/presence)
- [Sécurité de la passerelle](/fr/gateway/security)
