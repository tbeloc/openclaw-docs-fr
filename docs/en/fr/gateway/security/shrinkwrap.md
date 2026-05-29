---
summary: "Explication en langage clair et technique de npm shrinkwrap dans les versions OpenClaw"
read_when:
  - Vous voulez savoir ce que npm shrinkwrap signifie dans une version OpenClaw
  - Vous examinez les fichiers de verrouillage de paquets, les changements de dépendances ou les risques de chaîne d'approvisionnement
  - Vous validez les paquets npm racine ou plugin avant publication
title: "npm shrinkwrap"
---

Les checkouts de source OpenClaw utilisent `pnpm-lock.yaml`. Les paquets npm OpenClaw publiés utilisent `npm-shrinkwrap.json`, le fichier de verrouillage de dépendances publiable d'npm, afin que les installations de paquets utilisent le graphe de dépendances examiné lors de la version.

## La version simple

Shrinkwrap est un reçu pour l'arborescence de dépendances qui est fournie avec un paquet npm. Il indique à npm exactement quelles versions de paquets transitifs installer.

Pour les versions OpenClaw, cela signifie :

- le paquet publié ne demande pas à npm d'inventer un nouveau graphe de dépendances au moment de l'installation ;
- les changements de dépendances deviennent plus faciles à examiner car ils apparaissent dans un fichier de verrouillage ;
- la validation de version peut tester le même graphe que les utilisateurs installeront ;
- les surprises de taille de paquet ou de dépendance native sont plus faciles à détecter avant la publication.

Shrinkwrap n'est pas un bac à sable. Il ne rend pas une dépendance sûre par lui-même, et il ne remplace pas l'isolation d'hôte, `openclaw security audit`, la provenance du paquet ou les tests de fumée d'installation.

Le modèle mental court :

| Fichier               | Où cela compte           | Ce que cela signifie                      |
| --------------------- | ------------------------ | ----------------------------------------- |
| `pnpm-lock.yaml`      | Checkout de source OpenClaw | Graphe de dépendances du mainteneur       |
| `npm-shrinkwrap.json` | Paquet npm publié        | Graphe d'installation npm pour les utilisateurs |
| `package-lock.json`   | Applications npm locales | Pas le contrat de publication OpenClaw   |

## Pourquoi OpenClaw l'utilise

OpenClaw est une passerelle, un hôte de plugin, un routeur de modèle et un runtime d'agent. Une installation par défaut peut affecter le temps de démarrage, l'utilisation du disque, les téléchargements de paquets natifs et l'exposition de la chaîne d'approvisionnement.

Shrinkwrap donne à l'examen de version une limite stable :

- les examinateurs peuvent voir le mouvement des dépendances transitives ;
- les validateurs de paquets peuvent rejeter la dérive inattendue du fichier de verrouillage ;
- l'acceptation de paquet peut tester les installations avec le graphe qui sera fourni ;
- les paquets de plugin peuvent porter leur propre graphe de dépendances verrouillé au lieu de dépendre du paquet racine pour posséder les dépendances spécifiques au plugin.

L'objectif n'est pas « plus de fichiers de verrouillage ». L'objectif est des installations de version reproductibles avec une propriété claire.

## Détails techniques

Le paquet npm racine `openclaw` et les paquets npm de plugin appartenant à OpenClaw incluent `npm-shrinkwrap.json` lors de la publication. Les paquets de plugin appartenant à OpenClaw appropriés peuvent également publier avec des `bundledDependencies` explicites, afin que leurs fichiers de dépendances runtime soient portés dans la tarball du plugin au lieu de dépendre uniquement de la résolution au moment de l'installation.

Maintenez la limite comme ceci :

```bash
pnpm deps:shrinkwrap:generate
pnpm deps:shrinkwrap:check
```

Le générateur résout le format de verrouillage publiable d'npm mais rejette les versions de paquets générées qui ne sont pas déjà présentes dans `pnpm-lock.yaml`. Cela maintient intact la limite d'âge de dépendance pnpm, de remplacement et d'examen de correctif.

Utilisez les commandes racine uniquement lors de l'actualisation intentionnelle du paquet racine sans toucher aux paquets de plugin :

```bash
pnpm deps:shrinkwrap:root:generate
pnpm deps:shrinkwrap:root:check
```

Examinez ces fichiers comme sensibles à la sécurité :

- `pnpm-lock.yaml`
- `npm-shrinkwrap.json`
- charges utiles de dépendances de plugin groupées
- tout diff `package-lock.json`

Les validateurs de paquets OpenClaw exigent shrinkwrap dans les nouvelles tarballs de paquets racine. Le chemin de publication npm du plugin vérifie le shrinkwrap local du plugin, installe les dépendances groupées locales au paquet, puis empaquète ou publie. Les validateurs de paquets rejettent `package-lock.json` pour les paquets OpenClaw publiés.

Pour inspecter un paquet racine publié :

```bash
npm pack openclaw@<version> --json --pack-destination /tmp/openclaw-pack
tar -tf /tmp/openclaw-pack/openclaw-<version>.tgz | grep '^package/npm-shrinkwrap.json$'
```

Pour inspecter un paquet de plugin appartenant à OpenClaw :

```bash
npm pack @openclaw/discord@<version> --json --pack-destination /tmp/openclaw-plugin-pack
tar -tf /tmp/openclaw-plugin-pack/openclaw-discord-<version>.tgz | grep '^package/npm-shrinkwrap.json$'
tar -tf /tmp/openclaw-plugin-pack/openclaw-discord-<version>.tgz | grep '^package/node_modules/'
```

Contexte : [npm-shrinkwrap.json](https://docs.npmjs.com/cli/v11/configuring-npm/npm-shrinkwrap-json).
