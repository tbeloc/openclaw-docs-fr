---
title: "Liste de contrôle de publication"
summary: "Liste de contrôle étape par étape pour la publication npm + application macOS"
read_when:
  - Cutting a new npm release
  - Cutting a new macOS app release
  - Verifying metadata before publishing
---

# Liste de contrôle de publication (npm + macOS)

Utilisez `pnpm` à partir de la racine du dépôt avec Node 24 par défaut. Node 22 LTS, actuellement `22.16+`, reste supporté pour la compatibilité. Gardez l'arborescence de travail propre avant le balisage/la publication.

## Déclenchement par l'opérateur

Quand l'opérateur dit « release », faites immédiatement cette vérification préalable (sans questions supplémentaires sauf si bloqué) :

- Lisez ce document et `docs/platforms/mac/release.md`.
- Chargez l'env depuis `~/.profile` et confirmez que `SPARKLE_PRIVATE_KEY_FILE` + les variables App Store Connect sont définis (SPARKLE_PRIVATE_KEY_FILE doit se trouver dans `~/.profile`).
- Utilisez les clés Sparkle depuis `~/Library/CloudStorage/Dropbox/Backup/Sparkle` si nécessaire.

## Versioning

Les versions actuelles d'OpenClaw utilisent le versioning basé sur la date.

- Version de publication stable : `YYYY.M.D`
  - Balise Git : `vYYYY.M.D`
  - Exemples de l'historique du dépôt : `v2026.2.26`, `v2026.3.8`
- Version de préversion bêta : `YYYY.M.D-beta.N`
  - Balise Git : `vYYYY.M.D-beta.N`
  - Exemples de l'historique du dépôt : `v2026.2.15-beta.1`, `v2026.3.8-beta.1`
- Balise de correction de secours : `vYYYY.M.D-N`
  - À utiliser uniquement comme balise de récupération en dernier recours quand une version stable publiée immuable a brûlé la balise d'origine et que vous ne pouvez pas la réutiliser.
  - La version du package npm reste `YYYY.M.D` ; le suffixe `-N` est uniquement pour la balise git et la version GitHub.
  - Préférez les bêtas pour l'itération de préversion normale, puis coupez une balise stable propre une fois prêt.
- Utilisez la même chaîne de version partout, moins le `v` initial où les balises Git ne sont pas utilisées :
  - `package.json`: `2026.3.8`
  - Balise Git : `v2026.3.8`
  - Titre de la version GitHub : `openclaw 2026.3.8`
- Ne remplissez pas avec des zéros le mois ou le jour. Utilisez `2026.3.8`, pas `2026.03.08`.
- Stable et bêta sont des dist-tags npm, pas des lignes de publication séparées :
  - `latest` = stable
  - `beta` = préversion/test
- Dev est la tête mobile de `main`, pas une version normale balisée par git.
- L'exécution d'aperçu déclenchée par balise accepte les balises stables, bêta et de correction de secours, et rejette les versions dont la date CalVer est à plus de 2 jours calendaires UTC de la date de publication.

Note historique :

- Les anciennes balises telles que `v2026.1.11-1`, `v2026.2.6-3` et `v2.0.0-beta2` existent dans l'historique du dépôt.
- Traitez les balises de correction comme une échappatoire de secours uniquement. Les nouvelles versions doivent toujours utiliser `vYYYY.M.D` pour stable et `vYYYY.M.D-beta.N` pour bêta.

1. **Version et métadonnées**

- [ ] Mettez à jour la version `package.json` (par exemple, `2026.1.29`).
- [ ] Exécutez `pnpm plugins:sync` pour aligner les versions des packages d'extension + les journaux des modifications.
- [ ] Mettez à jour les chaînes CLI/version dans [`src/version.ts`](https://github.com/openclaw/openclaw/blob/main/src/version.ts) et l'agent utilisateur Baileys dans [`src/web/session.ts`](https://github.com/openclaw/openclaw/blob/main/src/web/session.ts).
- [ ] Confirmez les métadonnées du package (nom, description, dépôt, mots-clés, licence) et que la carte `bin` pointe vers [`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs) pour `openclaw`.
- [ ] Si les dépendances ont changé, exécutez `pnpm install` pour que `pnpm-lock.yaml` soit à jour.

2. **Build et artefacts**

- [ ] Si les entrées A2UI ont changé, exécutez `pnpm canvas:a2ui:bundle` et validez tout [`src/canvas-host/a2ui/a2ui.bundle.js`](https://github.com/openclaw/openclaw/blob/main/src/canvas-host/a2ui/a2ui.bundle.js) mis à jour.
- [ ] `pnpm run build` (régénère `dist/`).
- [ ] Vérifiez que le package npm `files` inclut tous les dossiers `dist/*` requis (notamment `dist/node-host/**` et `dist/acp/**` pour node headless + CLI ACP).
- [ ] Confirmez que `dist/build-info.json` existe et inclut le hash `commit` attendu (la bannière CLI l'utilise pour les installations npm).
- [ ] Optionnel : `npm pack --pack-destination /tmp` après le build ; inspectez le contenu de la tarball et gardez-la à portée de main pour la version GitHub (ne la **validez pas**).

3. **Changelog et docs**

- [ ] Mettez à jour `CHANGELOG.md` avec les points forts visibles par l'utilisateur (créez le fichier s'il manque) ; gardez les entrées strictement décroissantes par version.
- [ ] Assurez-vous que les exemples/drapeaux README correspondent au comportement CLI actuel (notamment les nouvelles commandes ou options).

4. **Validation**

- [ ] `pnpm build`
- [ ] `pnpm check`
- [ ] `pnpm test` (ou `pnpm test:coverage` si vous avez besoin de la sortie de couverture)
- [ ] `pnpm release:check` (vérifie le contenu du pack npm)
- [ ] Si `pnpm config:docs:check` échoue dans le cadre de la validation de publication et que le changement de surface de configuration est intentionnel, exécutez `pnpm config:docs:gen`, examinez `docs/.generated/config-baseline.json` et `docs/.generated/config-baseline.jsonl`, validez les baselines mises à jour, puis réexécutez `pnpm release:check`.
- [ ] `OPENCLAW_INSTALL_SMOKE_SKIP_NONROOT=1 pnpm test:install:smoke` (test de fumée d'installation Docker, chemin rapide ; requis avant la publication)
  - Si la version npm immédiatement précédente est connue comme cassée, définissez `OPENCLAW_INSTALL_SMOKE_PREVIOUS=<last-good-version>` ou `OPENCLAW_INSTALL_SMOKE_SKIP_PREVIOUS=1` pour l'étape de préinstallation.
- [ ] (Optionnel) Test de fumée d'installation complet (ajoute la couverture non-root + CLI) : `pnpm test:install:smoke`
- [ ] (Optionnel) Installation E2E (Docker, exécute `curl -fsSL https://openclaw.ai/install.sh | bash`, intègre, puis exécute les appels d'outils réels) :
  - `pnpm test:install:e2e:openai` (nécessite `OPENAI_API_KEY`)
  - `pnpm test:install:e2e:anthropic` (nécessite `ANTHROPIC_API_KEY`)
  - `pnpm test:install:e2e` (nécessite les deux clés ; exécute les deux fournisseurs)
- [ ] (Optionnel) Vérification rapide de la passerelle web si vos modifications affectent les chemins d'envoi/réception.

5. **Application macOS (Sparkle)**

- [ ] Construisez + signez l'application macOS, puis compressez-la pour la distribution.
- [ ] Générez l'appcast Sparkle (notes HTML via [`scripts/make_appcast.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/make_appcast.sh)) et mettez à jour `appcast.xml`.
- [ ] Gardez le zip de l'application (et le zip dSYM optionnel) prêt à joindre à la version GitHub.
- [ ] Suivez [macOS release](/fr/platforms/mac/release) pour les commandes exactes et les variables env requises.
  - `APP_BUILD` doit être numérique + monotone (pas de `-beta`) pour que Sparkle compare correctement les versions.
  - Si vous notarisez, utilisez le profil de chaîne de clés `openclaw-notary` créé à partir des variables env de l'API App Store Connect (voir [macOS release](/fr/platforms/mac/release)).

6. **Publier (npm)**

- [ ] Confirmez que le statut git est propre ; validez et poussez si nécessaire.
- [ ] Confirmez que la publication de confiance npm est configurée pour le package `openclaw`.
- [ ] Ne vous fiez pas à un secret `NPM_TOKEN` pour ce flux de travail ; le travail de publication utilise la publication de confiance GitHub OIDC.
- [ ] Poussez la balise git correspondante pour déclencher l'exécution d'aperçu dans `.github/workflows/openclaw-npm-release.yml`.
- [ ] Exécutez `OpenClaw NPM Release` manuellement avec la même balise pour publier après l'approbation de l'environnement `npm-release`.
  - Les balises stables publient sur npm `latest`.
  - Les balises bêta publient sur npm `beta`.
  - Les balises de correction de secours comme `v2026.3.13-1` correspondent à la version npm `2026.3.13`.
  - L'exécution d'aperçu et l'exécution de publication manuelle rejettent les balises qui ne correspondent pas à `package.json`, ne sont pas sur `main`, ou dont la date CalVer est à plus de 2 jours calendaires UTC de la date de publication.
  - Si `openclaw@YYYY.M.D` est déjà publié, une balise de correction de secours est toujours utile pour la version GitHub et la récupération Docker, mais npm publish ne republiera pas cette version.
- [ ] Vérifiez le registre : `npm view openclaw version`, `npm view openclaw dist-tags`, et `npx -y openclaw@X.Y.Z --version` (ou `--help`).

### Dépannage (notes de la version 2.0.0-beta2)

- **npm pack/publish se bloque ou produit une énorme tarball** : le bundle d'application macOS dans `dist/OpenClaw.app` (et les zips de publication) sont balayés dans le package. Corrigez en mettant en liste blanche le contenu de publication via `package.json` `files` (incluez les sous-répertoires dist, docs, skills ; excluez les bundles d'application). Confirmez avec `npm pack --dry-run` que `dist/OpenClaw.app` n'est pas listé.
- **boucle web d'authentification npm pour dist-tags** : utilisez l'authentification héritée pour obtenir une invite OTP :
  - `NPM_CONFIG_AUTH_TYPE=legacy npm dist-tag add openclaw@X.Y.Z latest`
- **`npx` la vérification échoue avec `ECOMPROMISED: Lock compromised`** : réessayez avec un cache frais :
  - `NPM_CONFIG_CACHE=/tmp/npm-cache-$(date +%s) npx -y openclaw@X.Y.Z --version`
- **La balise a besoin d'une récupération après un correctif tardif** : si la balise stable d'origine est liée à une version GitHub immuable, créez une balise de correction de secours comme `vX.Y.Z-1` au lieu d'essayer de forcer la mise à jour de `vX.Y.Z`.
  - Gardez la version du package npm à `X.Y.Z` ; le suffixe de correction est uniquement pour la balise git et la version GitHub.
  - Utilisez ceci uniquement en dernier recours. Pour l'itération normale, préférez les balises bêta, puis coupez une version stable propre.

7. **Version GitHub + appcast**

- [ ] Balise et poussée : `git tag vX.Y.Z && git push origin vX.Y.Z` (ou `git push --tags`).
  - Pousser la balise déclenche également le flux de travail de publication npm.
- [ ] Créez/actualisez la version GitHub pour `vX.Y.Z` avec le **titre `openclaw X.Y.Z`** (pas seulement la balise) ; le corps doit inclure la section **complète** du changelog pour cette version (Points forts + Modifications + Correctifs), en ligne (pas de liens nus), et **ne doit pas répéter le titre dans le corps**.
- [ ] Joignez les artefacts : tarball `npm pack` (optionnel), `OpenClaw-X.Y.Z.zip`, et `OpenClaw-X.Y.Z.dSYM.zip` (si généré).
- [ ] Validez le `appcast.xml` mis à jour et poussez-le (Sparkle se nourrit de main).
- [ ] À partir d'un répertoire temporaire propre (pas de `package.json`), exécutez `npx -y openclaw@X.Y.Z send --help` pour confirmer que les points d'entrée d'installation/CLI fonctionnent.
- [ ] Annoncez/partagez les notes de publication.

## Portée de publication des plugins (npm)

Nous publions uniquement les **plugins npm existants** sous la portée `@openclaw/*`. Les plugins groupés qui ne sont pas sur npm restent **disk-tree uniquement** (toujours expédiés dans `extensions/**`).

Processus pour dériver la liste :

1. `npm search @openclaw --json` et capturez les noms de packages.
2. Comparez avec les noms `extensions/*/package.json`.
3. Publiez uniquement l'**intersection** (déjà sur npm).

Liste actuelle des plugins npm (mettez à jour selon les besoins) :

- @openclaw/bluebubbles
- @openclaw/diagnostics-otel
- @openclaw/discord
- @openclaw/feishu
- @openclaw/lobster
- @openclaw/matrix
- @openclaw/msteams
- @openclaw/nextcloud-talk
- @openclaw/nostr
- @openclaw/voice-call
- @openclaw/zalo
- @openclaw/zalouser

Les notes de publication doivent également appeler les **nouveaux plugins groupés optionnels** qui ne sont **pas activés par défaut** (exemple : `tlon`).
