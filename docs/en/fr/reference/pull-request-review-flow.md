---
summary: "Comment les retours de Barnacle et ClawSweeper aident à faire avancer les pull requests OpenClaw dans la révision."
read_when:
  - Following up after Barnacle or ClawSweeper feedback
  - Asking ClawSweeper for review
  - Debugging Barnacle, ClawSweeper, stale labels, or auto-closures
title: "Flux de révision des pull requests"
sidebarTitle: "Flux de révision des PR"
---

Cette page explique le flux de révision après l'ouverture ou la mise à jour d'une pull request OpenClaw : ce que font Barnacle et ClawSweeper, comment améliorer la PR à partir de leurs retours, et ce qu'il faut vérifier quand l'automatisation reste silencieuse.

Barnacle et ClawSweeper aident les mainteneurs à maintenir la file d'attente de révision utilisable. Ils ne remplacent pas le jugement des mainteneurs.

## Barnacle

Barnacle est un triage GitHub déterministe. Il recherche les cas connus de gestion de file d'attente et répond avec des labels, des commentaires ou des fermetures.

Barnacle peut agir quand :

- le corps d'une PR est principalement vide ou manque de contexte sur le problème ;
- une PR n'a pas de preuve utile ;
- une modification docs uniquement, tests uniquement, refactorisation uniquement, CI uniquement ou infra manque de contexte de mainteneur lié ;
- une modification semble appartenir à ClawHub ou à un plugin plutôt qu'au cœur ;
- une branche porte du travail non lié ;
- un auteur a plus de 20 PR ouvertes.

Barnacle s'exécute à partir du code de flux de travail du référentiel de confiance. Il ne vérifie pas ou n'exécute pas le code du contributeur.

La plupart des labels de routage sont des signaux de mainteneur ou d'automatisation, donc les contributeurs n'ont pas besoin d'ajouter eux-mêmes les labels.

## ClawSweeper

ClawSweeper est le bot d'examen et de maintenance assisté par IA pour les référentiels OpenClaw. Il peut réviser les PR, évaluer les preuves, laisser des commentaires de révision durables et aider les mainteneurs avec des flux de réparation gardés ou d'autofusion.

Un résultat positif de ClawSweeper est une preuve de soutien, pas une approbation de mainteneur. Les mainteneurs décident toujours si et quand une PR est prête à être fusionnée.

ClawSweeper est basé sur une file d'attente. Ne vous attendez pas à une réponse immédiate après l'ouverture d'une PR, l'envoi d'un commit ou l'ajout d'une demande de révision. Les mises à jour de labels après une exécution de ClawSweeper peuvent également prendre du temps.

Les nouvelles PR entrent dans la file d'attente de révision de ClawSweeper. Les mainteneurs peuvent également mettre en file d'attente la révision, la réparation ou les flux d'autofusion avec des labels ou des commandes. Pour les mises à jour ordinaires des contributeurs, demandez à ClawSweeper une autre révision uniquement après avoir mis à jour la branche, la description de la PR, la preuve ou le code. Ensuite, demandez une révision nouvelle avec un nouveau commentaire de PR :

```text
@clawsweeper re-review
```

Les auteurs de PR peuvent également utiliser `@clawsweeper re-run` ; les utilisateurs ayant accès en écriture au référentiel peuvent utiliser l'une ou l'autre commande sur n'importe quel élément ouvert. La commande simple `@clawsweeper review` est réservée aux mainteneurs. Soyez patient : demander à nouveau avant que les modifications demandées ne soient présentes ajoute simplement du bruit à la file d'attente.

Quand ClawSweeper laisse des conversations de révision, traitez-les comme des retours de révision normaux et utilisez la liste de contrôle de suivi ci-dessous.

Si un contributeur humain ou un mainteneur a repris la PR et y travaille activement, ne convoquezpas ClawSweeper ou ne travaillez pas autrement sur la PR en même temps. Laissez la révision ou la réparation humaine se terminer en premier. Si l'activité s'arrête, vérifiez si l'auteur a été invité à fournir une preuve ou à effectuer d'autres mises à jour.

## Améliorer une PR pendant la révision

Une fois que Barnacle, ClawSweeper ou un mainteneur répond, utilisez ce retour comme liste de contrôle des prochaines étapes pour la PR.

1. Lisez les `Rank-up moves:` et `Proof guidance:` de ClawSweeper comme la liste d'actions pour cette PR. Les évaluations et les labels sont des signaux de révision, pas des cibles de fusion fixes.
2. Envoyez la modification de code ou de docs demandée, et mettez à jour la description de la PR quand le problème, la solution, l'impact utilisateur ou la preuve a changé.
3. Ajoutez la preuve demandée, en utilisant une preuve qui correspond à la modification.
4. Résolvez vous-même les conversations de révision traitées. Répondez et laissez une conversation ouverte uniquement quand vous avez besoin du jugement du mainteneur ou du relecteur.
5. Demandez une re-révision uniquement après que la branche, la description de la PR, la preuve et les résultats CI pertinents soient à jour. Plusieurs cycles de mise à jour et de révision entre l'auteur, le mainteneur et ClawSweeper sont normaux.
6. Gardez la discussion sur la PR quand c'est possible. Passez à `#clawtributors` sur Discord uniquement quand la PR a besoin de coordination de mainteneur, l'automatisation semble bloquée, ou la prochaine décision est difficile à régler dans les commentaires GitHub. Incluez le lien de la PR, le statut actuel et la question spécifique ou la preuve restante.

Gardez le corps de la PR à jour. Les commentaires aident à la discussion, mais la description de la PR est le résumé durable que les mainteneurs et l'automatisation revisitent.

`status: ⏳ waiting on author` signifie que la prochaine action est avec l'auteur de la PR : mettez à jour la branche, la description de la PR, la preuve ou répondez avec le contexte manquant avant de demander une autre révision.

Les preuves utiles incluent la sortie de test ciblée, les résultats CI, les captures d'écran, les enregistrements, la sortie du terminal, les observations en direct, les journaux expurgés ou les liens d'artefacts. Pour les modifications visuelles, incluez les captures d'écran avant et après quand c'est pratique. Pour les fichiers de preuve, préférez lier les artefacts CI, les captures d'écran ou enregistrements téléchargés sur GitHub, ou un court extrait de journal expurgé. Ne validez pas les fichiers de preuve générés à moins qu'ils ne fassent partie de la modification réelle des docs, tests ou produit.

L'expurgation des données sensibles est la responsabilité du contributeur. Supprimez les secrets, les jetons, les URL privées, les données utilisateur et les journaux non liés avant de publier la preuve.

OpenClaw utilise également une automatisation d'obsolescence séparée. Les problèmes et PR non assignés peuvent être marqués obsolètes après 14 jours d'inactivité, puis fermés après 7 jours d'inactivité supplémentaires. Les PR assignées sont marquées obsolètes 27 jours après l'ouverture, indépendamment des mises à jour ultérieures, puis fermées après 7 jours d'inactivité sans activité. Si une PR assignée est toujours active, coordonnez-vous avec le mainteneur qui y travaille.

## Quand l'automatisation reste silencieuse

L'automatisation peut rester silencieuse quand un mainteneur gère déjà l'élément, une demande de révision ou de réparation est toujours en file d'attente, l'événement est routinier, ou la voie ClawSweeper n'est pas configurée pour l'action demandée.

Elle peut également éviter d'agir quand un flux de travail de confiance aurait besoin d'exécuter du code contributeur non fiable. Dans ce cas, les mainteneurs utilisent plutôt une révision normale ou un flux de travail plus sûr.

## Dépannage

Si ClawSweeper ne répond pas immédiatement, attendez avant de réessayer. Le service est basé sur une file d'attente, et les commentaires ou modifications de labels répétés peuvent rendre le fil plus difficile à réviser sans rendre la file d'attente plus rapide.

Avant de demander de l'aide, vérifiez :

- la description de la PR est à jour ;
- le dernier commit contient la modification demandée ;
- CI a terminé, ou le corps de la PR explique pourquoi tout échec restant est sans rapport avec la PR ;
- la dernière demande de révision a été faite comme un commentaire de PR :
  `@clawsweeper re-review` ;
- un mainteneur ou contributeur ne travaille pas déjà activement sur la PR ;
- la dernière demande n'est pas encore dans le délai normal de la file d'attente ClawSweeper.

S'il n'y a toujours pas de réponse de ClawSweeper plusieurs heures après que la PR soit à jour, ou si la PR semble bloquée par l'automatisation, demandez sur `#clawtributors` sur Discord. Incluez le lien de la PR, ce que vous attendiez, quand vous avez demandé et ce qui a changé depuis le dernier commentaire du bot.

## Forking l'automatisation

Les projets qui veulent une automatisation de révision similaire peuvent étudier ou forker ClawSweeper :

- [openclaw/clawsweeper](https://github.com/openclaw/clawsweeper)
- [Documentation ClawSweeper](https://clawsweeper.bot/)

## Connexes

- [Contributing](https://github.com/openclaw/openclaw/blob/main/CONTRIBUTING.md)
- [Pipeline CI](/fr/ci)
