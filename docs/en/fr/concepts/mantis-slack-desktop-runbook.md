---
summary: "Runbook opérateur pour Mantis Slack desktop QA : dispatch GitHub, CLI local, baux VNC chauds, modes d'hydratation, interprétation des timings, artefacts et gestion des défaillances."
read_when:
  - Running Mantis Slack desktop QA from GitHub or locally
  - Debugging slow Mantis Slack desktop runs
  - Choosing source, prehydrated, or warm-lease mode
  - Posting screenshot and video evidence to a PR
title: "Mantis Slack desktop runbook"
---

Mantis Slack desktop QA est la voie d'assurance qualité pour interface réelle destinée aux bugs de classe Slack qui nécessitent un bureau Linux, un sauvetage VNC, Slack Web, une véritable passerelle OpenClaw, des captures d'écran, des vidéos et un commentaire de preuve sur une PR.

Utilisez-le quand les tests unitaires ou la voie Slack live sans interface graphique ne peuvent pas prouver le bug.

## Modèle de stockage

Mantis utilise trois couches de stockage différentes :

- Image du fournisseur : appartient à Crabbox et est stockée dans le compte du fournisseur cloud.
  Elle contient les capacités de la machine telles que Chrome/Chromium, ffmpeg, scrot,
  Node/corepack/pnpm, outils de compilation natifs et répertoires de cache vides.
- État du bail chaud : appartient à la session opérateur actuelle. Il peut contenir un
  profil de navigateur connecté, `/var/cache/crabbox/pnpm` et une extraction de source préparée
  tant que le bail est actif.
- Artefacts Mantis : appartiennent à l'exécution OpenClaw. Ils se trouvent sous
  `.artifacts/qa-e2e/mantis/...`, puis GitHub Actions les télécharge et
  l'application GitHub Mantis commente les preuves en ligne sur la PR.

Ne mettez jamais de secrets, de cookies de navigateur, d'état de connexion Slack, d'extractions de référentiel,
`node_modules` ou `dist/` dans une image de fournisseur précuite.

## Dispatch GitHub

Exécutez le workflow depuis `main` :

```bash
gh workflow run mantis-slack-desktop-smoke.yml \
  --ref main \
  -f candidate_ref=<trusted-ref-or-sha> \
  -f pr_number=<pr-number> \
  -f scenario_id=slack-canary \
  -f crabbox_provider=aws \
  -f keep_vm=false \
  -f hydrate_mode=source
```

Les valeurs `candidate_ref` autorisées sont intentionnellement étroites car le workflow
utilise des identifiants en direct : ascendance `main` actuelle, balises de version ou une tête PR ouverte
depuis `openclaw/openclaw`.

Le workflow écrit :

- artefact téléchargé : `mantis-slack-desktop-smoke-<run-id>-<attempt>`;
- commentaire PR en ligne de l'application GitHub Mantis;
- `slack-desktop-smoke.png`;
- `slack-desktop-smoke.mp4`;
- `slack-desktop-smoke-preview.gif`;
- `slack-desktop-smoke-change.mp4`;
- `mantis-slack-desktop-smoke-summary.json`;
- `mantis-slack-desktop-smoke-report.md`;
- journaux distants tels que `slack-desktop-command.log`, `openclaw-gateway.log`,
  `chrome.log` et `ffmpeg.log`.

Le commentaire PR est mis à jour sur place par le marqueur caché
`<!-- mantis-slack-desktop-smoke -->`.

## CLI local

Preuve de source froide :

```bash
pnpm openclaw qa mantis slack-desktop-smoke \
  --provider aws \
  --class standard \
  --gateway-setup \
  --credential-source convex \
  --credential-role maintainer \
  --provider-mode live-frontier \
  --model openai/gpt-5.4 \
  --alt-model openai/gpt-5.4 \
  --scenario slack-canary \
  --hydrate-mode source
```

Conservez la VM pour le sauvetage VNC :

```bash
pnpm openclaw qa mantis slack-desktop-smoke \
  --provider aws \
  --class standard \
  --gateway-setup \
  --scenario slack-canary \
  --keep-lease
```

Ouvrez VNC :

```bash
crabbox vnc --provider aws --id <cbx_id> --open
```

Réutilisez un bail chaud :

```bash
pnpm openclaw qa mantis slack-desktop-smoke \
  --provider aws \
  --lease-id <cbx_id-or-slug> \
  --gateway-setup \
  --scenario slack-canary \
  --hydrate-mode source
```

Utilisez `--hydrate-mode prehydrated` uniquement quand l'espace de travail distant réutilisé a déjà
`node_modules` et un `dist/` construit. Mantis échoue fermé si ceux-ci sont
manquants.

## Modes d'hydratation

| Mode          | À utiliser quand                                  | Comportement distant                                                                       | Compromis                                                 |
| ------------- | ----------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `source`      | Preuve PR normale, machines froides, CI        | Exécute `pnpm install --frozen-lockfile --prefer-offline` et `pnpm build` à l'intérieur de la VM | Plus lent, preuve d'extraction de source la plus forte                 |
| `prehydrated` | Vous avez intentionnellement préparé un bail réutilisé | Nécessite `node_modules` et `dist/` existants; ignore install/build                     | Rapide, mais valide uniquement pour les baux chauds contrôlés par l'opérateur |

GitHub Actions prépare toujours l'extraction candidate avant l'exécution de la VM. Son
magasin pnpm est mis en cache par OS, version Node et lockfile. L'exécution source de la VM utilise également
`/var/cache/crabbox/pnpm` quand présent.

## Interprétation des timings

`mantis-slack-desktop-smoke-report.md` inclut les timings des phases :

- `crabbox.warmup`: démarrage du fournisseur cloud, disponibilité du bureau/navigateur et SSH.
- `crabbox.inspect`: recherche de métadonnées de bail.
- `credentials.prepare`: acquisition du bail de credential Convex.
- `crabbox.remote_run`: synchronisation, lancement du navigateur, installation/construction OpenClaw ou
  validation d'hydratation, démarrage de la passerelle, capture d'écran et capture vidéo.
- `artifacts.copy`: rsync retour depuis la VM.

`crabbox.remote_run` peut être marqué `accepted` quand Crabbox retourne un statut
distant non-zéro après que Mantis ait copié les métadonnées prouvant que la passerelle OpenClaw
est active et la configuration terminée. Traitez `accepted` comme succès-avec-explication,
pas un scénario échoué.

Si l'exécution est lente :

- warmup domine : précuisez ou promouvez une meilleure image de fournisseur Crabbox;
- remote_run domine en `source` : utilisez un bail chaud, améliorez la réutilisation du magasin pnpm,
  ou déplacez les prérequis de la machine dans l'image du fournisseur;
- remote_run domine en `prehydrated` : l'espace de travail distant n'était pas réellement
  prêt, ou la configuration de la passerelle/navigateur/Slack est lente;
- la copie d'artefacts domine : inspectez la taille vidéo et le contenu du répertoire d'artefacts.

## Liste de contrôle des preuves

Un bon commentaire PR devrait montrer :

- id du scénario et SHA candidate;
- URL d'exécution GitHub Actions;
- URL de l'artefact;
- capture d'écran en ligne;
- aperçu animé en ligne quand disponible;
- liens MP4 complet et MP4 réduit;
- statut de succès/échec;
- résumé des timings dans le rapport joint.

Ne validez pas les captures d'écran ou les vidéos dans le référentiel. Conservez-les dans les artefacts
GitHub Actions ou le commentaire PR.

## Gestion des défaillances

Si le workflow échoue avant l'exécution de la VM, inspectez d'abord le job Actions. Les causes typiques
sont `candidate_ref` non fiable, secrets d'environnement manquants ou échec d'installation/construction candidate.

Si l'exécution de la VM échoue mais que les captures d'écran ont été copiées, inspectez :

```bash
cat mantis-slack-desktop-smoke-report.md
cat mantis-slack-desktop-smoke-summary.json
cat slack-desktop-command.log
cat openclaw-gateway.log
cat chrome.log
cat ffmpeg.log
```

Si l'exécution a conservé le bail, ouvrez VNC avec la commande `crabbox vnc ...` du rapport.
Arrêtez le bail quand vous avez terminé :

```bash
crabbox stop --provider aws <cbx_id-or-slug>
```

Si la connexion Slack a expiré, réparez-la en VNC sur un bail conservé et réexécutez avec
`--lease-id`. Ne précuisez pas ce profil de navigateur dans une image de fournisseur.

## Connexes

- [QA overview](/fr/concepts/qa-e2e-automation)
- [Slack channel](/fr/channels/slack)
- [Testing](/fr/help/testing)
