---
summary: "Comment OpenClaw examine les modifications de dépendances et les dépendances d'exécution du plugin de package"
read_when:
  - Vous examinez les modifications de dépendances ou le risque de la chaîne d'approvisionnement
  - Vous validez les packages npm racine ou plugin avant la publication
  - Vous souhaitez comprendre les dépendances du plugin regroupées
title: "Verrouillage des dépendances"
---

OpenClaw utilise `pnpm-lock.yaml` comme limite de révision de dépendance de produit engagée. Il enregistre le graphique de dépendance résolu utilisé par les extraits de source et l'IC, de sorte que les modifications transitives restent visibles dans la révision du code.

OpenClaw ne valide pas les verrous au format npm pour les packages de produit et ne les publie pas dans les archives de package. [npm 12 a supprimé le support de shrinkwrap](https://github.com/npm/cli/releases/tag/v12.0.0), y compris la commande `npm shrinkwrap` et le chargement de `npm-shrinkwrap.json` à partir des racines de package ou des archives de dépendance.

La chaîne d'outils de publication ClawHub de confiance est une exception distincte : `.github/release/clawhub-cli/package-lock.json` est un verrou de projet npm 12 engagé utilisé par l'automatisation de publication. Il n'est pas livré dans un package OpenClaw.

## Comportement du package publié

Les packages de plugin OpenClaw publiés regroupent leurs fichiers de dépendance d'exécution dans l'archive par défaut. Ces octets sont livrés avec le plugin et fonctionnent de la même manière que l'opérateur utilise npm, pnpm ou Bun.

Les plugins lourds en natif refusent le regroupement des dépendances d'exécution car leurs arbres de dépendance contiennent des artefacts natifs spécifiques à la plateforme ou volumineux. Ces plugins résolvent les dépendances au moment de l'installation à partir de dépendances directes exactement épinglées. Le package racine `openclaw` résout également les dépendances au moment de l'installation et ne regroupe pas son arbre de dépendance complet.

Aucun chemin ne publie un verrou :

- les archives racine et plugin ne contiennent ni `npm-shrinkwrap.json` ni `package-lock.json` ;
- `pnpm-lock.yaml` reste le graphique de dépendance source examiné ;
- les verrous de package npm n'existent que temporairement tandis qu'OpenClaw valide les graphiques de package ou exécute `npm ci` pour assembler un plugin regroupé.

## Valider les graphiques de dépendance npm

Le vérificateur de verrou npm génère `package-lock.json` dans un répertoire temporaire, applique les remplacements d'espace de travail et rejette toute version de registre générée absente de `pnpm-lock.yaml`. Il n'écrit pas de verrou dans l'extraction.

```bash
# Root and every publishable package
pnpm deps:npm-lock:check

# Only packages affected by the current changeset
pnpm deps:npm-lock:check:changed
```

## Inspecter une archive de plugin

```bash
npm pack @openclaw/discord@<version> --json --pack-destination /tmp/openclaw-plugin-pack
tar -tf /tmp/openclaw-plugin-pack/openclaw-discord-<version>.tgz | grep '^package/node_modules/'
tar -tf /tmp/openclaw-plugin-pack/openclaw-discord-<version>.tgz | grep -E '^package/(npm-shrinkwrap|package-lock)\.json$' && exit 1 || true
```

Les entrées `node_modules` prouvent que le plugin porte sa charge utile d'exécution regroupée. La vérification finale prouve qu'aucun format de verrou npm n'est livré dans l'archive.
