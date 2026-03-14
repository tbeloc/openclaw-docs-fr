---
read_when:
  - 你想在 stable/beta/dev 之间切换
  - 你正在标记或发布预发布版本
summary: stable、beta 和 dev 渠道：语义、切换和标签
title: 开发渠道
x-i18n:
  generated_at: "2026-02-03T10:07:21Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2b01219b7e705044ce39838a0da7c7fa65c719809ab2f8a51e14529064af81bf
  source_path: install/development-channels.md
  workflow: 15
---

# Canaux de développement

Dernière mise à jour : 2026-01-21

OpenClaw propose trois canaux de mise à jour :

- **stable** : npm dist-tag `latest`.
- **beta** : npm dist-tag `beta` (constructions en test).
- **dev** : tête mobile de `main` (git). npm dist-tag : `dev` (lors de la publication).

Nous publions les constructions sur **beta**, les testons, puis **promouvons les constructions validées vers `latest`**,
le numéro de version reste inchangé — le dist-tag est la source de données pour l'installation npm.

## Basculer entre les canaux

Checkout Git :

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

- `stable`/`beta` extrait la dernière balise correspondante (généralement la même balise).
- `dev` bascule vers `main` et rebase sur l'amont.

Installation globale npm/pnpm :

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

Cela met à jour via le dist-tag npm correspondant (`latest`, `beta`, `dev`).

Lorsque vous basculez explicitement les canaux avec `--channel`, OpenClaw aligne également la méthode d'installation :

- `dev` garantit un checkout git (par défaut `~/openclaw`, peut être remplacé via `OPENCLAW_GIT_DIR`),
  le met à jour et installe le CLI global à partir de ce checkout.
- `stable`/`beta` installent depuis npm en utilisant le dist-tag correspondant.

Conseil : si vous souhaitez utiliser à la fois stable + dev, conservez deux clones et pointez la passerelle Gateway vers celui stable.

## Plugins et canaux

Lorsque vous basculez les canaux avec `openclaw update`, OpenClaw synchronise également les sources de plugins :

- `dev` privilégie les plugins intégrés du checkout git.
- `stable` et `beta` reviennent aux packages de plugins installés via npm.

## Meilleures pratiques pour les balises

- Balisez les versions de publication sur lesquelles vous souhaitez que le checkout git se trouve (`vYYYY.M.D` ou `vYYYY.M.D-<patch>`).
- Gardez les balises immuables : ne déplacez jamais ou ne réutilisez jamais une balise.
- Le dist-tag npm reste la source de données pour l'installation npm :
  - `latest` → stable
  - `beta` → construction candidate
  - `dev` → snapshot main (optionnel)

## Disponibilité de l'application macOS

Les constructions beta et dev peuvent **ne pas** inclure de publication d'application macOS. C'est normal :

- Les balises git et les dist-tag npm peuvent toujours être publiés.
- Notez dans les notes de publication ou le journal des modifications « Aucune construction macOS pour cette bêta ».
