---
summary: "Résumé visuel et preuves techniques pour la performance de mai 2026, le nettoyage de la taille des paquets, des dépendances et du shrinkwrap"
read_when:
  - You are validating the May 2026 performance and package-size cleanup
  - You need the numbers behind the OpenClaw performance and dependency blog post
  - You are changing release gates, package shrinkwrap, or plugin dependency boundaries
title: "Release performance sweep"
---

Cette page capture les preuves derrière la performance OpenClaw de mai 2026,
la taille des paquets, les dépendances et le nettoyage du shrinkwrap. C'est le
compagnon technique du billet de blog public.

Deux audits sont combinés ici :

- **Release performance sweep :** GitHub Releases de `v2026.5.27` jusqu'à
  `v2026.4.23` stable, en utilisant le workflow `OpenClaw Performance`,
  `profile=smoke`, `repeat=1`, mock-provider lane.
- **Contexte d'avril antérieur :** baselines mock-provider publiées de
  `clawgrit-reports` de `v2026.4.1` à `v2026.5.2`, utilisées uniquement pour
  éviter de traiter les versions cassées de fin avril comme la baseline de
  performance publique.
- **Install footprint sweep :** installations fraîches `npm install --ignore-scripts`
  dans des paquets temporaires, avec `du -sk node_modules` pour la taille et une
  marche `node_modules` pour les comptages d'instances de paquets.
- **npm package size sweep :** `npm pack openclaw@<version> --dry-run --json`
  pour les versions publiées, enregistrant la taille de la tarball compressée,
  la taille dépliée et le nombre de fichiers.

<Warning>
Le sweep de performance principal utilise un exemple smoke par tag. Le contexte
d'avril antérieur utilise les médianes repeat-3 publiées de `clawgrit-reports`.
Traitez les nombres comme des preuves de tendance et des signaux de chasse aux
régressions, pas comme des statistiques de release-gate.
</Warning>

## Snapshot

Couverture de performance : **76 versions demandées**, **73 points soutenus par
des artefacts**, et **3 exécutions CI indisponibles**. Dernier point stable
mesuré : `v2026.5.27`.

<CardGroup cols={2}>
  <Card title="Stable agent turn" icon="gauge">
    **2.9x faster cold turn**

    - `v2026.4.14`: 9.8s
    - `v2026.5.27`: 3.4s

  </Card>
  <Card title="Published package" icon="package">
    **17.8MB tarball**

    Dernier paquet stable, en baisse par rapport au pic de taille de paquet de
    43.3MB en mars.

  </Card>
  <Card title="Latest stable install" icon="hard-drive">
    **786.9MB fresh install**

    `v2026.5.27` contient toujours l'arborescence de dépendances OpenClaw
    imbriquée. L'état de la prochaine version sur `main` est 407.4MB.

  </Card>
  <Card title="Dependency graph" icon="boxes">
    **371 installed packages**

    Dernière version stable. Le `main` actuel est réduit à 314 après le
    nettoyage des dépendances de suivi.

  </Card>
</CardGroup>

## Install Footprint Timeline

<CardGroup cols={2}>
  <Card title="Monthly high" icon="triangle-alert">
    **645 dependencies**

    `2026.2.26` était le maximum de comptage de dépendances mensuelles dans cet
    exemple.

  </Card>
  <Card title="Shrinkwrap introduced" icon="lock">
    **1,020.6MB install**

    `2026.5.22` a ajouté le shrinkwrap racine et exposé un problème de forme
    de paquet : 911.8MB ont atterri sous `openclaw/node_modules` imbriqué.

  </Card>
  <Card title="Latest stable" icon="tag">
    **786.9MB install**

    `2026.5.27` a réduit le pic mais a toujours installé une arborescence
    OpenClaw imbriquée de 675.9MB.

  </Card>
  <Card title="Next-release state" icon="scissors">
    **407.4MB install**

    Le `main` actuel conserve le shrinkwrap, supprime l'arborescence imbriquée
    et installe 314 paquets.

  </Card>
</CardGroup>

<Tip>
Le shrinkwrap n'était pas le problème en soi. La mauvaise forme de paquet
l'était. Le `main` actuel expédie toujours le shrinkwrap, mais npm ne
matérialise plus une deuxième arborescence de dépendances OpenClaw pendant
l'installation.
</Tip>

## What Changed After 5.27

Le nettoyage entre `v2026.5.27` et le `main` actuel a supprimé le graphique
d'installation par défaut dupliqué au lieu de supprimer les capacités elles-mêmes.

<CardGroup cols={2}>
  <Card title="Root default graph" icon="git-branch">
    Les chemins de paquets du shrinkwrap racine sont passés de **372** à
    **331**. Les noms de paquets uniques sont passés de **357** à **318**.
  </Card>
  <Card title="Direct root dependencies" icon="unplug">
    `@earendil-works/pi-agent-core`, `@earendil-works/pi-ai`,
    `@earendil-works/pi-coding-agent` et `pdfjs-dist` ont quitté le chemin de
    dépendance racine par défaut.
  </Card>
  <Card title="Native optional cones" icon="cpu">
    Les cônes de paquets natifs multi-plateformes `@napi-rs/canvas` et
    `@mariozechner/clipboard` ont cessé d'atterrir dans l'installation par
    défaut.
  </Card>
  <Card title="Supply-chain surface" icon="shield">
    Moins de paquets par défaut signifie moins de tarballs, de mainteneurs, de
    binaires natifs, de comportements au moment de l'installation et de chemins
    de mise à jour transitifs à faire confiance par défaut.
  </Card>
</CardGroup>

## Headline Numbers

N'utilisez pas les lignes cassées de fin avril comme baselines de performance
publiques. `v2026.4.23` et `v2026.4.29` sont des preuves de régression utiles,
mais les deltas de style `14x` décrivent principalement la récupération d'une
mauvaise ligne de version.

Pour la narration du blog, utilisez la baseline publiée d'avril antérieur comme
échelle :

| Metric          | Earlier April baseline | `v2026.5.27` |                    Delta |
| --------------- | ---------------------: | -----------: | -----------------------: |
| Cold agent turn |                9,819ms |      3,378ms | 65.6% lower, 2.9x faster |
| Warm agent turn |                7,458ms |      2,973ms | 60.1% lower, 2.5x faster |
| Agent peak RSS  |                686.2MB |      635.5MB |               7.4% lower |

La baseline d'avril antérieur est `v2026.4.14` de l'exécution mock-provider
`clawgrit-reports` publiée. Cette exécution a utilisé repeat 3 et a échoué
uniquement parce que la chronologie de diagnostic n'a pas été émise ; les
médianes froides, chaudes et RSS sont toujours utiles comme échelle approximative.
Traitez ceci comme un contexte narratif, pas une statistique de release-gate.

Dans le sweep stable de mai à un seul exemple, la ligne s'est déplacée plus
modestement :

| Metric          | `v2026.5.2` | `v2026.5.27` |       Delta |
| --------------- | ----------: | -----------: | ----------: |
| Cold agent turn |     3,897ms |      3,378ms | 13.3% lower |
| Warm agent turn |     3,610ms |      2,973ms | 17.6% lower |
| Agent peak RSS  |     613.7MB |      635.5MB | 3.6% higher |

Meilleur point de préversion dans le sweep à un seul exemple :

| Metric          | `v2026.5.27` | `v2026.5.27-beta.1` |       Delta |
| --------------- | -----------: | ------------------: | ----------: |
| Cold agent turn |      3,378ms |             2,575ms | 23.8% lower |
| Warm agent turn |      2,973ms |             2,217ms | 25.4% lower |
| Agent peak RSS  |      635.5MB |             635.3MB |        flat |

### Install footprint

| Metric                                          |  Baseline | Current main |       Delta |
| ----------------------------------------------- | --------: | -----------: | ----------: |
| Install size from `2026.5.22` peak              | 1,020.6MB |      407.4MB | 60.1% lower |
| Install size from latest release `2026.5.27`    |   786.9MB |      407.4MB | 48.2% lower |
| Dependencies from monthly high `2026.2.26`      |       645 |          314 | 51.3% lower |
| Dependencies from latest release `2026.5.27`    |       371 |          314 | 15.4% lower |
| Nested `openclaw/node_modules` from `2026.5.22` |   911.8MB |          0MB |     removed |
| Nested `openclaw/node_modules` from `2026.5.27` |   675.9MB |          0MB |     removed |

### npm package size

| Version     | Compressed tarball | Unpacked package |  Files | Notes                             |
| ----------- | -----------------: | ---------------: | -----: | --------------------------------- |
| `2026.1.30` |             12.8MB |           33.5MB |  4,607 | early rebranded package           |
| `2026.2.26` |             23.6MB |           82.9MB | 10,125 | feature growth                    |
| `2026.3.31` |             43.3MB |          182.6MB | 21,037 | package-size high point           |
| `2026.4.29` |             22.9MB |           74.6MB |  9,309 | package pruning visible           |
| `2026.5.12` |             23.4MB |           80.1MB | 12,035 | major external-plugin split       |
| `2026.5.22` |             17.2MB |           76.9MB | 12,386 | docs/assets excluded from package |
| `2026.5.27` |             17.8MB |           79.0MB | 12,509 | latest stable package             |

`2026.5.12` est le jalon visible d'extraction de plugin dans le changelog :
Amazon Bedrock, Bedrock Mantle, Slack, OpenShell sandbox, Anthropic Vertex,
Matrix et WhatsApp ont quitté le chemin de dépendance principal afin que leurs
cônes de dépendances s'installent avec ces plugins au lieu de chaque
installation principale.

## Kova agent turn summary

La ligne stable d'avril contient deux histoires différentes. L'avril antérieur
était lent mais reconnaissable. La fin avril est devenue une falaise de
régression. `v2026.5.2` est où la mock-provider lane descend d'abord dans la
plage 3-5s et commence à passer régulièrement dans le sweep fourni.

Contexte publié antérieur :

| Release      | Kova | Cold turn | Warm turn | Agent peak RSS |
| ------------ | ---- | --------: | --------: | -------------: |
| `v2026.4.10` | FAIL |  11,031ms |   7,962ms |        679.0MB |
| `v2026.4.12` | FAIL |  11,965ms |   8,289ms |        713.5MB |
| `v2026.4.14` | FAIL |   9,819ms |   7,458ms |        686.2MB |
| `v2026.4.20` | FAIL |  22,314ms |  18,811ms |        810.8MB |
| `v2026.4.22` | FAIL |   9,630ms |   7,459ms |        743.0MB |

Sweep à un seul exemple fourni :

| Release             | Kova | Cold turn | Warm turn | Agent peak RSS |
| ------------------- | ---- | --------: | --------: | -------------: |
| `v2026.4.23`        | FAIL |  47,847ms |   8,010ms |      1,082.7MB |
| `v2026.4.24`        | FAIL |  48,264ms |  25,483ms |        996.0MB |
| `v2026.4.25`        | FAIL |  81,080ms |  59,172ms |      1,113.9MB |
| `v2026.4.26`        | FAIL |  76,771ms |  54,941ms |      1,140.8MB |
| `v2026.4.27`        | FAIL |  60,902ms |  33,699ms |      1,156.0MB |
| `v2026.4.29`        | FAIL |  94,031ms |  57,334ms |      3,613.7MB |
| `v2026.5.2`         | PASS |   3,897ms |   3,610ms |        613.7MB |
| `v2026.5.7`         | PASS |   3,923ms |   3,693ms |        654.1MB |
| `v2026.5.12`        | PASS |   7,248ms |   6,629ms |        834.8MB |
| `v2026.5.18`        | PASS |   3,301ms |   2,913ms |        630.3MB |
| `v2026.5.20`        | PASS |   3,413ms |   2,952ms |        643.2MB |
| `v2026.5.22`        | PASS |   4,494ms |   4,093ms |        654.3MB |
| `v2026.5.26`        | PASS |   2,626ms |   2,282ms |        660.4MB |
| `v2026.5.27-beta.1` | PASS |   2,575ms |   2,217ms |        635.3MB |
| `v2026.5.27`        | PASS |   3,378ms |   2,973ms |        635.5MB |

## Sondes source

Les sondes source ont été ignorées pour 17 références plus anciennes réussies car ces arbres source n'avaient pas encore les points d'entrée de sonde requis. Les métriques de tour d'agent existent toujours pour ces références.

Points de sonde source représentatifs :

| Version             | `readyz` par défaut p50 | `readyz` 50 plugins p50 | Santé CLI p50 | RSS max du plugin |
| ------------------- | ----------------------: | ----------------------: | ------------: | ----------------: |
| `v2026.4.29`        |                2,819ms |                 2,618ms |       1,679ms |          389.0MB |
| `v2026.5.2`         |                2,324ms |                 2,013ms |       1,384ms |          377.2MB |
| `v2026.5.7`         |                1,649ms |                 1,540ms |       1,175ms |          387.6MB |
| `v2026.5.18`        |                1,942ms |                 1,927ms |         607ms |          426.5MB |
| `v2026.5.20`        |                1,966ms |                 1,987ms |         621ms |          455.0MB |
| `v2026.5.22`        |                2,081ms |                 1,884ms |       5,095ms |          444.2MB |
| `v2026.5.26`        |                1,546ms |                 1,634ms |         656ms |          400.4MB |
| `v2026.5.27-beta.1` |                1,462ms |                 1,548ms |         548ms |          394.0MB |
| `v2026.5.27`        |                1,874ms |                 1,925ms |         660ms |          398.0MB |

Le pic de santé CLI `v2026.5.22` est visible dans ce tableau même si la voie de tour d'agent a toujours réussi. Conservez les sondes source lors de l'investigation des régressions CLI ou passerelle ciblées.

## Audit d'empreinte d'installation

Les exemples de dépendances utilisent une version stable par mois, plus l'événement d'introduction de shrinkwrap `2026.5.22`, la dernière version `2026.5.27` et le `main` actuel.

| Point              | Dépendances installées | Installation fraîche | Package OpenClaw | `openclaw/node_modules` imbriqué | Shrinkwrap racine | Comportement d'installation Canvas                |
| ------------------ | ---------------------: | -------------------: | ---------------: | --------------------------------: | ----------------- | ------------------------------------------------- |
| Jan `2026.1.30`    |                    605 |            438.4MB |           45.8MB |                            2.4MB | non               | wrapper de niveau supérieur + `darwin-arm64`     |
| Feb `2026.2.26`    |                    645 |            575.7MB |          110.1MB |                            3.5MB | non               | wrapper de niveau supérieur + `darwin-arm64`     |
| Mar `2026.3.31`    |                    438 |            584.1MB |          234.8MB |                              0MB | non               | wrapper de niveau supérieur + `darwin-arm64`     |
| Apr `2026.4.29`    |                    392 |            335.0MB |           97.4MB |                              0MB | non               | aucun installé                                    |
| `2026.5.22`        |                    401 |          1,020.6MB |        1,020.4MB |                          911.8MB | oui               | imbriqué : les 12 packages `@napi-rs/canvas`     |
| May `2026.5.26`    |                    371 |            767.5MB |          767.4MB |                          656.4MB | oui               | imbriqué : les 12 packages `@napi-rs/canvas`     |
| Latest `2026.5.27` |                    371 |            786.9MB |          786.7MB |                          675.9MB | oui               | imbriqué : les 12 packages `@napi-rs/canvas`     |
| Current `main`     |                    314 |            407.4MB |          101.0MB |                              0MB | oui               | wrapper de niveau supérieur + `darwin-arm64`     |

### Limite de shrinkwrap

<CardGroup cols={2}>
  <Card title="Avant shrinkwrap" icon="unlock">
    `2026.5.20` n'a pas de shrinkwrap racine et pas d'arborescence de dépendances OpenClaw imbriquée volumineuse.
  </Card>
  <Card title="Introduit" icon="lock">
    `2026.5.22` ajoute un shrinkwrap racine et installe 911.8MB sous `openclaw/node_modules` imbriqué.
  </Card>
  <Card title="Dernière version stable" icon="tag">
    `2026.5.27` conserve le shrinkwrap et installe toujours 675.9MB sous `openclaw/node_modules` imbriqué.
  </Card>
  <Card title="Main actuel" icon="check">
    `main` conserve le shrinkwrap et supprime l'arborescence de dépendances OpenClaw imbriquée.
  </Card>
</CardGroup>

L'inspection de l'archive publiée vérifie la limite :

| Version     | Stable publié ? | `npm-shrinkwrap.json` racine | Notes                                          |
| ----------- | --------------- | ---------------------------- | ---------------------------------------------- |
| `2026.5.20` | oui             | non                          | dernière version stable avant shrinkwrap       |
| `2026.5.21` | non             | n/a                          | pas de version npm stable                      |
| `2026.5.22` | oui             | oui                          | shrinkwrap introduit                           |
| `2026.5.23` | non             | n/a                          | pas de version npm stable                      |
| `2026.5.24` | non             | n/a                          | pas de version npm stable                      |
| `2026.5.25` | non             | n/a                          | pas de version npm stable                      |
| `2026.5.26` | oui             | oui                          | arborescence de dépendances imbriquée toujours présente |
| `2026.5.27` | oui             | oui                          | arborescence de dépendances imbriquée toujours présente |
| `main`      | n/a             | oui                          | arborescence de dépendances imbriquée supprimée |

La distinction importante : **le shrinkwrap lui-même n'est pas le problème**. Le `main` actuel expédie toujours le shrinkwrap racine. Le problème était la forme du package qui a fait que npm matérialise une grande arborescence de dépendances OpenClaw imbriquée et les 12 packages de plateforme `@napi-rs/canvas`.

Pour une explication en langage clair du shrinkwrap et des vérifications de package au niveau du mainteneur, voir [npm shrinkwrap](/fr/gateway/security/shrinkwrap).

## Interprétation de la chaîne d'approvisionnement

Le nombre de dépendances est une métrique de sécurité opérationnelle, pas seulement une métrique de taille d'installation. Chaque package élargit l'ensemble des mainteneurs, des archives, des mises à jour transitives, des binaires natifs optionnels et des comportements au moment de l'installation que les opérateurs doivent approuver.

La direction du nettoyage est :

- garder les capacités lourdes et optionnelles en dehors de l'installation principale par défaut
- faire que les packages de plugin possèdent leur graphe de dépendances d'exécution
- éviter la réparation du gestionnaire de packages d'exécution lors du démarrage de la passerelle
- préserver les installations déterministes sans causer la matérialisation de packages natifs sur toutes les plateformes
- garder les scripts d'installation désactivés dans les chemins d'acceptation et de mesure des packages
- détecter les arbres de dépendances imbriqués et les explosions de dépendances optionnelles natives avant la publication

Docs connexes :

- [Résolution des dépendances des plugins](/fr/plugins/dependency-resolution)
- [Inventaire des plugins](/fr/plugins/plugin-inventory)
- [Validation complète de la version](/fr/reference/full-release-validation)

## Exécutions de performance indisponibles

| Version             | Exécution                                                                    | Résultat  | Raison                                                                                                                                |
| ------------------- | ---------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `v2026.5.3-1`       | [26561664645](https://github.com/openclaw/openclaw/actions/runs/26561664645) | échec     | tâche mock-provider échouée : démarrage CLI expiré en attente de qa-channel prêt ; aucun compte qa-channel signalé                   |
| `v2026.5.3`         | [26561666722](https://github.com/openclaw/openclaw/actions/runs/26561666722) | échec     | tâche mock-provider échouée : démarrage CLI expiré en attente de qa-channel prêt ; aucun compte qa-channel signalé                   |
| `v2026.4.29-beta.2` | [26561683635](https://github.com/openclaw/openclaw/actions/runs/26561683635) | annulée   | la récupération de base optionnelle s'est suspendue avant le téléchargement d'artefact                                                |

## Portes de suivi

Vérifications de version recommandées à partir de ce balayage :

1. Exécutez le test de fumée de performance mock-provider pour les candidats à la version et conservez les artefacts.
2. Suivez le tour froid, le tour chaud, le RSS de l'agent, la `readyz` de la passerelle et la santé CLI.
3. Installation fraîche de l'archive compressée avec scripts désactivés.
4. Enregistrez le nombre de dépendances installées, la taille d'installation, la taille du package, la taille de `openclaw/node_modules` imbriqué et la forme du package natif optionnel.
5. Échouez ou maintenez l'examen de la version lorsque des arbres de dépendances imbriqués ou des packages natifs sur toutes les plateformes apparaissent de manière inattendue.
