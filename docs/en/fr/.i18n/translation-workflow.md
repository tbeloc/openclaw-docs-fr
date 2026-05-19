# Flux de travail de traduction

Note interne pour le pipeline de publication des docs. Ce fichier se trouve sous `docs/.i18n`, qui est ignoré par la compilation du site de docs et n'est pas publié.

## Objectifs

- Les docs en anglais se déploient rapidement après chaque synchronisation des docs source.
- La traduction des paramètres régionaux ne s'exécute pas pour chaque commit `main` actif.
- Le travail de traduction est débité de sorte qu'une rafale de commits de docs devient une vague de traduction.
- Les tâches de paramètres régionaux traduisent uniquement les pages dont le hash source a changé depuis la dernière sortie de paramètres régionaux réussie.
- Les sorties de paramètres régionaux réussies sont validées ensemble, même si une ou plusieurs tâches de paramètres régionaux échouent.
- Une réconciliation hebdomadaire réexécute chaque chemin de paramètres régionaux/page pour réparer les traductions manquées ou instables.

## Flux d'événements

1. `openclaw/openclaw` synchronise les docs en anglais dans `openclaw/docs`.
2. GitHub Pages déploie immédiatement les modifications en anglais/source à partir du commit de synchronisation.
3. `Translate All` est déclenché par le commit de synchronisation, la distribution de version, la distribution manuelle ou le calendrier hebdomadaire.
4. Le coordinateur attend une fenêtre de refroidissement avant de commencer la traduction.
5. Après le refroidissement, le coordinateur lit les métadonnées source `origin/main` actuelles.
6. Si une synchronisation de docs plus récente est arrivée pendant le refroidissement, le coordinateur utilise l'état source plus récent.
7. Les tâches de traduction par paramètres régionaux s'exécutent en parallèle avec `fail-fast: false`.
8. Chaque tâche de paramètres régionaux télécharge un artefact pour le SHA source demandé.
9. Le finaliseur télécharge les artefacts disponibles, ignore les charges utiles obsolètes ou défaillantes, et pousse un commit i18n agrégé.
10. Après l'arrivée du commit agrégé, le finaliseur distribue le déploiement Pages une seule fois.
11. Le flux de travail Pages distribue le smoke en direct après le déploiement.

## Politique de débitage

Le coordinateur attend 1 heure après une synchronisation de docs ou une distribution de version, puis relit `origin/main`.

Le refroidissement par défaut est contrôlé par la variable de référentiel de publication `OPENCLAW_DOCS_TRANSLATION_COOLDOWN_SECONDS`, qui par défaut est `3600`. Les appelants de distribution de référentiel peuvent la remplacer par `client_payload.cooldown_seconds`, et les exécutions manuelles peuvent définir `cooldown_seconds`.

Si `.openclaw-sync/source.json` a changé pendant l'attente, il attend à nouveau à partir du nouvel état. Si `main` continue de se déplacer, l'attente est plafonnée par `OPENCLAW_DOCS_TRANSLATION_MAX_WAIT_SECONDS`, qui par défaut est la valeur de refroidissement. L'état le plus récent observé est traduit après le plafond.

Les exécutions manuelles et hebdomadaires n'attendent pas par défaut.

## Traduction incrémentale

Chaque page traduite stocke `x-i18n.source_hash`. Les tâches de paramètres régionaux comparent le hash de la page anglaise actuelle avec le hash de paramètres régionaux stocké.

Les exécutions normales traduisent uniquement :

- les pages de paramètres régionaux manquantes
- les pages de paramètres régionaux avec `x-i18n.source_hash` obsolète
- les pages affectées par la suppression/élagage de source

Les fichiers internes sous `docs/.i18n/**` ne sont pas des entrées de traduction. Les exécutions déclenchées par push qui ne modifient que les fichiers i18n internes sont ignorées avant la matrice de paramètres régionaux.

Si une tâche de paramètres régionaux échoue, son artefact est marqué comme défaillant et ne porte aucune charge utile. Le finaliseur valide toujours les paramètres régionaux réussis. Les paramètres régionaux défaillants restent obsolètes et sont repris par la prochaine exécution incrémentale car leurs hashes source ne correspondent toujours pas.

## Contrat d'artefact

Chaque tâche de paramètres régionaux télécharge un artefact nommé avec les paramètres régionaux et le SHA source :

```text
i18n-zh-cn-<source-sha>
```

Contenu de l'artefact :

```text
metadata.json
changed-files.txt
deleted-files.txt
payload/docs/<locale>/**
payload/docs/.i18n/<locale>.tm.jsonl
```

`metadata.json` inclut les paramètres régionaux, le slug de paramètres régionaux, le SHA source, le nombre en attente, le nombre de modifications et toute raison d'échec. Le finaliseur rejette les artefacts dont le `source_sha` ne correspond pas au `.openclaw-sync/source.json` actuel.

Le flux de travail de version du référentiel source distribue un événement `translate-all-release`. Le coordinateur accepte toujours les anciens événements de version par paramètres régionaux pour la compatibilité, mais ce ne sont qu'un recours.

## Commit agrégé

Le finaliseur possède le seul push de paramètres régionaux dans le chemin normal.

Message de commit :

```text
chore(i18n): refresh translations
```

Le commit peut contenir un ensemble de paramètres régionaux partiel. Le résumé du travail répertorie les paramètres régionaux appliqués, les paramètres régionaux sans modifications, les paramètres régionaux manquants ou défaillants, les artefacts obsolètes et les artefacts invalides.

## Réconciliation hebdomadaire

L'exécution hebdomadaire utilise le mode `full`. Elle force une réconciliation complète sur chaque paramètre régional et chaque page source au lieu de s'appuyer uniquement sur les hashes source modifiés.

Les modifications du glossaire forcent également une réconciliation complète car les conseils du glossaire peuvent affecter les pages dont les hashes source n'ont pas changé.

Comportement attendu :

- régénérer ou vérifier chaque page de paramètres régionaux
- élaguer les pages de paramètres régionaux obsolètes
- actualiser la mémoire de traduction selon les besoins
- utiliser toujours les tâches de paramètres régionaux parallèles
- valider toujours un résultat agrégé
- tolérer toujours les défaillances individuelles de paramètres régionaux

L'exécution hebdomadaire est le mécanisme de réparation pour l'instabilité LLM, les défaillances partielles et les mises à jour incrémentales manquées.

## Politique de déploiement

L'anglais se déploie à partir des commits de synchronisation source.

Les traductions se déploient après le commit i18n agrégé. Le finaliseur distribue GitHub Pages une seule fois car GitHub supprime les exécutions de flux de travail déclenchées normalement à partir des commits `GITHUB_TOKEN`. Le flux de travail Pages distribue le smoke en direct après le déploiement afin que le test de smoke vérifie le site déployé au lieu de faire la course au déploiement.

Une journée de docs active devrait produire de nombreux déploiements anglais rapides, mais seulement un petit nombre de déploiements de paramètres régionaux.

Si les fournisseurs de déploiement externes tels que Mintlify surveillent chaque push, le commit i18n agrégé est le réducteur de charge. Évitez de restaurer les pushes par paramètres régionaux vers `main`.
