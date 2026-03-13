---
read_when:
  - 发布新的 npm 版本
  - 发布新的 macOS 应用版本
  - 发布前验证元数据
summary: npm + macOS 应用的逐步发布清单
x-i18n:
  generated_at: "2026-02-03T10:09:28Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1a684bc26665966eb3c9c816d58d18eead008fd710041181ece38c21c5ff1c62
  source_path: reference/RELEASING.md
  workflow: 15
---

# Liste de contrôle de publication (npm + macOS)

Utilisez `pnpm` (Node 22+) à partir de la racine du dépôt. Maintenez l'arborescence de travail propre avant de créer des étiquettes/publications.

## Déclenchement par l'opérateur

Lorsque l'opérateur dit « release », exécutez immédiatement cette vérification préalable (ne posez pas de questions supplémentaires sauf en cas de blocage) :

- Lisez ce document et `docs/platforms/mac/release.md`.
- Chargez les variables d'environnement depuis `~/.profile` et confirmez que `SPARKLE_PRIVATE_KEY_FILE` + les variables App Store Connect sont définis (SPARKLE_PRIVATE_KEY_FILE doit être dans `~/.profile`).
- Si nécessaire, utilisez la clé Sparkle depuis `~/Library/CloudStorage/Dropbox/Backup/Sparkle`.

1. **Version et métadonnées**

- [ ] Mettez à jour la version dans `package.json` (par exemple `2026.1.29`).
- [ ] Exécutez `pnpm plugins:sync` pour aligner les versions des paquets d'extension et les journaux des modifications.
- [ ] Mettez à jour les chaînes CLI/version : agent utilisateur Baileys dans [`src/cli/program.ts`](https://github.com/openclaw/openclaw/blob/main/src/cli/program.ts) et [`src/provider-web.ts`](https://github.com/openclaw/openclaw/blob/main/src/provider-web.ts).
- [ ] Confirmez les métadonnées du paquet (name, description, repository, keywords, license) et que le mappage `bin` pointe vers [`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs) en tant que `openclaw`.
- [ ] Si les dépendances ont changé, exécutez `pnpm install` pour vous assurer que `pnpm-lock.yaml` est à jour.

2. **Construction et artefacts**

- [ ] Si les entrées A2UI ont changé, exécutez `pnpm canvas:a2ui:bundle` et validez le [`src/canvas-host/a2ui/a2ui.bundle.js`](https://github.com/openclaw/openclaw/blob/main/src/canvas-host/a2ui/a2ui.bundle.js) mis à jour.
- [ ] `pnpm run build` (régénère `dist/`).
- [ ] Vérifiez que les `files` du paquet npm contiennent tous les dossiers `dist/*` nécessaires (en particulier `dist/node-host/**` et `dist/acp/**` pour le node headless + CLI ACP).
- [ ] Confirmez que `dist/build-info.json` existe et contient le hash `commit` attendu (la bannière CLI utilise ces informations lors de l'installation npm).
- [ ] Optionnel : après la construction, exécutez `npm pack --pack-destination /tmp` ; inspectez le contenu de la tarball et conservez-la pour la publication GitHub (**ne la validez pas**).

3. **Journal des modifications et documentation**

- [ ] Mettez à jour `CHANGELOG.md`, en ajoutant les points forts destinés aux utilisateurs (créez le fichier s'il n'existe pas) ; classez les entrées en ordre strictement décroissant par version.
- [ ] Assurez-vous que les exemples/drapeaux README correspondent au comportement CLI actuel (en particulier les nouvelles commandes ou options).

4. **Vérification**

- [ ] `pnpm build`
- [ ] `pnpm check`
- [ ] `pnpm test` (utilisez `pnpm test:coverage` si vous avez besoin d'une sortie de couverture)
- [ ] `pnpm release:check` (vérifiez le contenu de npm pack)
- [ ] `OPENCLAW_INSTALL_SMOKE_SKIP_NONROOT=1 pnpm test:install:smoke` (test de fumée d'installation Docker, chemin rapide ; obligatoire avant la publication)
  - Si une version npm publiée précédente est connue pour avoir des problèmes, définissez `OPENCLAW_INSTALL_SMOKE_PREVIOUS=<last-good-version>` ou `OPENCLAW_INSTALL_SMOKE_SKIP_PREVIOUS=1` pour l'étape de pré-installation.
- [ ] (Optionnel) Test de fumée complet du programme d'installation (ajoutez non-root + couverture CLI) : `pnpm test:install:smoke`
- [ ] (Optionnel) E2E du programme d'installation (Docker, exécutez `curl -fsSL https://openclaw.ai/install.sh | bash`, onboarding, puis exécutez des appels d'outils réels) :
  - `pnpm test:install:e2e:openai` (nécessite `OPENAI_API_KEY`)
  - `pnpm test:install:e2e:anthropic` (nécessite `ANTHROPIC_API_KEY`)
  - `pnpm test:install:e2e` (nécessite les deux clés ; exécute les deux fournisseurs)
- [ ] (Optionnel) Si vos modifications affectent les chemins d'envoi/réception, vérifiez la passerelle Web Gateway.

5. **Application macOS (Sparkle)**

- [ ] Construisez et signez l'application macOS, puis compressez-la pour la distribution.
- [ ] Générez l'appcast Sparkle (générez des commentaires HTML via [`scripts/make_appcast.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/make_appcast.sh)) et mettez à jour `appcast.xml`.
- [ ] Conservez le zip de l'application (et optionnellement le zip dSYM) pour l'attacher à la publication GitHub.
- [ ] Suivez [Publication macOS](/platforms/mac/release) pour les commandes exactes et les variables d'environnement requises.
  - `APP_BUILD` doit être numérique et strictement croissant (sans `-beta`) pour que Sparkle compare correctement les versions.
  - Si vous effectuez une notarisation, utilisez la configuration du profil de chaîne de clés `openclaw-notary` créée à partir des variables d'environnement de l'API App Store Connect (voir [Publication macOS](/platforms/mac/release)).

6. **Publication (npm)**

- [ ] Confirmez que l'état git est propre ; validez et poussez selon les besoins.
- [ ] Si nécessaire, `npm login` (vérifiez 2FA).
- [ ] `npm publish --access public` (utilisez `--tag beta` pour les versions de pré-publication).
- [ ] Vérifiez le registre : `npm view openclaw version`, `npm view openclaw dist-tags` et `npx -y openclaw@X.Y.Z --version` (ou `--help`).

### Dépannage (notes de la publication 2.0.0-beta2)

- **npm pack/publish se bloque ou produit une tarball énorme** : le paquet d'application macOS dans `dist/OpenClaw.app` (et le zip de publication) est aspiré dans le paquet. Corrigez en publiant le contenu via la liste blanche `files` de `package.json` (incluez les sous-répertoires dist, docs, skills ; excluez le paquet d'application). Confirmez avec `npm pack --dry-run` que `dist/OpenClaw.app` n'est pas listé.
- **Boucle Web d'authentification npm dist-tags** : utilisez l'authentification héritée pour obtenir l'invite OTP :
  - `NPM_CONFIG_AUTH_TYPE=legacy npm dist-tag add openclaw@X.Y.Z latest`
- **La vérification `npx` échoue avec `ECOMPROMISED: Lock compromised`** : réessayez avec un nouveau cache :
  - `NPM_CONFIG_CACHE=/tmp/npm-cache-$(date +%s) npx -y openclaw@X.Y.Z --version`
- **Besoin de rediriger les étiquettes après un correctif retardé** : forcez la mise à jour et poussez les étiquettes, puis assurez-vous que les ressources de publication GitHub correspondent toujours :
  - `git tag -f vX.Y.Z && git push -f origin vX.Y.Z`

7. **Publication GitHub + appcast**

- [ ] Créez une étiquette et poussez : `git tag vX.Y.Z && git push origin vX.Y.Z` (ou `git push --tags`).
- [ ] Créez/actualisez la publication GitHub pour `vX.Y.Z`, **avec le titre `openclaw X.Y.Z`** (pas seulement l'étiquette) ; le corps doit contenir la section **complète** du journal des modifications pour cette version (points forts + modifications + corrections), affichée en ligne (sans liens nus), et **ne doit pas répéter le titre dans le corps**.
- [ ] Attachez les artefacts : tarball `npm pack` (optionnel), `OpenClaw-X.Y.Z.zip` et `OpenClaw-X.Y.Z.dSYM.zip` (si généré).
- [ ] Validez le `appcast.xml` mis à jour et poussez (Sparkle récupère la source depuis main).
- [ ] À partir d'un répertoire temporaire propre (sans `package.json`), exécutez `npx -y openclaw@X.Y.Z send --help` pour confirmer que l'installation/le point d'entrée CLI fonctionne correctement.
- [ ] Annoncez/partagez les notes de publication.

## Portée de publication des plugins (npm)

Nous publions uniquement les **plugins npm existants** sous la portée `@openclaw/*`. Les plugins intégrés non sur npm restent **arborescence disque uniquement** (toujours publiés dans `extensions/**`).

Processus pour obtenir la liste :

1. `npm search @openclaw --json` et capturez les noms de paquets.
2. Comparez avec les noms dans `extensions/*/package.json`.
3. Publiez uniquement l'**intersection** (déjà sur npm).

Liste actuelle des plugins npm (mettez à jour selon les besoins) :

- @openclaw/bluebubbles
- @openclaw/diagnostics-otel
- @openclaw/discord
- @openclaw/lobster
- @openclaw/matrix
- @openclaw/msteams
- @openclaw/nextcloud-talk
- @openclaw/nostr
- @openclaw/voice-call
- @openclaw/zalo
- @openclaw/zalouser

Les notes de publication doivent également appeler les **nouveaux plugins intégrés optionnels** qui sont **désactivés par défaut** (par exemple : `tlon`).
