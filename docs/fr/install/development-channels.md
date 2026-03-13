---
summary: "Canaux stable, beta et dev : sémantique, commutation et étiquetage"
read_when:
  - You want to switch between stable/beta/dev
  - You are tagging or publishing prereleases
title: "Canaux de développement"
---

# Canaux de développement

Dernière mise à jour : 2026-01-21

OpenClaw propose trois canaux de mise à jour :

- **stable** : npm dist-tag `latest`.
- **beta** : npm dist-tag `beta` (builds en test).
- **dev** : tête mobile de `main` (git). npm dist-tag : `dev` (lors de la publication).

Nous livrons des builds à **beta**, les testons, puis **promouvons un build validé vers `latest`**
sans changer le numéro de version — les dist-tags sont la source de vérité pour les installations npm.

## Commutation entre canaux

Checkout Git :

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

- `stable`/`beta` extraient la dernière balise correspondante (souvent la même balise).
- `dev` bascule vers `main` et rebase sur l'upstream.

Installation globale npm/pnpm :

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

Cela met à jour via le dist-tag npm correspondant (`latest`, `beta`, `dev`).

Lorsque vous **explicitement** basculez les canaux avec `--channel`, OpenClaw aligne également
la méthode d'installation :

- `dev` assure un checkout git (par défaut `~/openclaw`, à remplacer avec `OPENCLAW_GIT_DIR`),
  le met à jour et installe le CLI global à partir de ce checkout.
- `stable`/`beta` installe depuis npm en utilisant le dist-tag correspondant.

Conseil : si vous voulez stable + dev en parallèle, conservez deux clones et pointez votre passerelle vers celui qui est stable.

## Plugins et canaux

Lorsque vous basculez les canaux avec `openclaw update`, OpenClaw synchronise également les sources de plugins :

- `dev` préfère les plugins groupés du checkout git.
- `stable` et `beta` restaurent les packages de plugins installés via npm.

## Bonnes pratiques d'étiquetage

- Étiquetez les versions que vous voulez que les checkouts git atteignent (`vYYYY.M.D` pour stable, `vYYYY.M.D-beta.N` pour beta).
- `vYYYY.M.D.beta.N` est également reconnu pour la compatibilité, mais préférez `-beta.N`.
- Les anciennes balises `vYYYY.M.D-<patch>` sont toujours reconnues comme stable (non-beta).
- Gardez les balises immuables : ne déplacez jamais ou ne réutilisez jamais une balise.
- Les dist-tags npm restent la source de vérité pour les installations npm :
  - `latest` → stable
  - `beta` → build candidat
  - `dev` → snapshot main (optionnel)

## Disponibilité de l'application macOS

Les builds beta et dev peuvent **ne pas** inclure de version d'application macOS. C'est normal :

- La balise git et le dist-tag npm peuvent toujours être publiés.
- Signalez « pas de build macOS pour cette beta » dans les notes de version ou le changelog.
