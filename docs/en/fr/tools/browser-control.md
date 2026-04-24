---
summary: "API de contrôle du navigateur OpenClaw, référence CLI et actions de scripting"
read_when:
  - Scripting ou débogage du navigateur de l'agent via l'API de contrôle locale
  - Recherche de la référence CLI `openclaw browser`
  - Ajout d'automatisation de navigateur personnalisée avec snapshots et refs
title: "API de contrôle du navigateur"
---

Pour la configuration, la mise en place et le dépannage, voir [Browser](/fr/tools/browser).
Cette page est la référence pour l'API HTTP de contrôle locale, la CLI `openclaw browser`,
et les modèles de scripting (snapshots, refs, waits, debug flows).

## API de contrôle (optionnelle)

Pour les intégrations locales uniquement, la Gateway expose une petite API HTTP de loopback :

- Statut/démarrage/arrêt : `GET /`, `POST /start`, `POST /stop`
- Onglets : `GET /tabs`, `POST /tabs/open`, `POST /tabs/focus`, `DELETE /tabs/:targetId`
- Snapshot/capture d'écran : `GET /snapshot`, `POST /screenshot`
- Actions : `POST /navigate`, `POST /act`
- Hooks : `POST /hooks/file-chooser`, `POST /hooks/dialog`
- Téléchargements : `POST /download`, `POST /wait/download`
- Débogage : `GET /console`, `POST /pdf`
- Débogage : `GET /errors`, `GET /requests`, `POST /trace/start`, `POST /trace/stop`, `POST /highlight`
- Réseau : `POST /response/body`
- État : `GET /cookies`, `POST /cookies/set`, `POST /cookies/clear`
- État : `GET /storage/:kind`, `POST /storage/:kind/set`, `POST /storage/:kind/clear`
- Paramètres : `POST /set/offline`, `POST /set/headers`, `POST /set/credentials`, `POST /set/geolocation`, `POST /set/media`, `POST /set/timezone`, `POST /set/locale`, `POST /set/device`

Tous les endpoints acceptent `?profile=<name>`.

Si l'authentification de la gateway par secret partagé est configurée, les routes HTTP du navigateur nécessitent également une authentification :

- `Authorization: Bearer <gateway token>`
- `x-openclaw-password: <gateway password>` ou authentification HTTP Basic avec ce mot de passe

Notes :

- Cette API de navigateur loopback autonome **ne consomme pas** les en-têtes d'identité de proxy de confiance ou Tailscale Serve.
- Si `gateway.auth.mode` est `none` ou `trusted-proxy`, ces routes de navigateur loopback n'héritent pas de ces modes porteurs d'identité ; gardez-les loopback uniquement.

### Contrat d'erreur `/act`

`POST /act` utilise une réponse d'erreur structurée pour les validations au niveau des routes et les défaillances de politique :

```json
{ "error": "<message>", "code": "ACT_*" }
```

Valeurs `code` actuelles :

- `ACT_KIND_REQUIRED` (HTTP 400) : `kind` est manquant ou non reconnu.
- `ACT_INVALID_REQUEST` (HTTP 400) : la charge utile d'action a échoué la normalisation ou la validation.
- `ACT_SELECTOR_UNSUPPORTED` (HTTP 400) : `selector` a été utilisé avec un type d'action non supporté.
- `ACT_EVALUATE_DISABLED` (HTTP 403) : `evaluate` (ou `wait --fn`) est désactivé par la configuration.
- `ACT_TARGET_ID_MISMATCH` (HTTP 403) : `targetId` au niveau supérieur ou par lot entre en conflit avec la cible de la requête.
- `ACT_EXISTING_SESSION_UNSUPPORTED` (HTTP 501) : l'action n'est pas supportée pour les profils de session existante.

Les autres défaillances d'exécution peuvent toujours retourner `{ "error": "<message>" }` sans champ `code`.

### Exigence Playwright

Certaines fonctionnalités (navigate/act/snapshot IA/snapshot de rôle, captures d'écran d'éléments, PDF) nécessitent Playwright. Si Playwright n'est pas installé, ces endpoints retournent une erreur 501 claire.

Ce qui fonctionne toujours sans Playwright :

- Snapshots ARIA
- Captures d'écran de page pour le navigateur `openclaw` géré quand un WebSocket CDP par onglet est disponible
- Captures d'écran de page pour les profils `existing-session` / Chrome MCP
- Captures d'écran basées sur ref `existing-session` (`--ref`) à partir de la sortie snapshot

Ce qui nécessite toujours Playwright :

- `navigate`
- `act`
- Snapshots IA / snapshots de rôle
- Captures d'écran d'éléments avec sélecteur CSS (`--element`)
- export PDF complet du navigateur

Les captures d'écran d'éléments rejettent également `--full-page` ; la route retourne `fullPage is not supported for element screenshots`.

Si vous voyez `Playwright is not available in this gateway build`, réparez les dépendances d'exécution du plugin de navigateur fourni pour que `playwright-core` soit installé, puis redémarrez la gateway. Pour les installations packagées, exécutez `openclaw doctor --fix`. Pour Docker, installez également les binaires du navigateur Chromium comme indiqué ci-dessous.

#### Installation Docker Playwright

Si votre Gateway s'exécute dans Docker, évitez `npx playwright` (conflits de remplacement npm).
Utilisez plutôt la CLI fournie :

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

Pour persister les téléchargements de navigateur, définissez `PLAYWRIGHT_BROWSERS_PATH` (par exemple,
`/home/node/.cache/ms-playwright`) et assurez-vous que `/home/node` est persisté via
`OPENCLAW_HOME_VOLUME` ou un bind mount. Voir [Docker](/fr/install/docker).

## Comment ça marche (interne)

Un petit serveur de contrôle loopback accepte les requêtes HTTP et se connecte aux navigateurs basés sur Chromium via CDP. Les actions avancées (click/type/snapshot/PDF) passent par Playwright au-dessus de CDP ; quand Playwright est manquant, seules les opérations non-Playwright sont disponibles. L'agent voit une interface stable tandis que les navigateurs locaux/distants et les profils se permutent librement en dessous.

## Référence rapide CLI

Toutes les commandes acceptent `--browser-profile <name>` pour cibler un profil spécifique, et `--json` pour une sortie lisible par machine.

<AccordionGroup>

<Accordion title="Bases : statut, onglets, ouvrir/focus/fermer">

```bash
openclaw browser status
openclaw browser start
openclaw browser stop            # efface aussi l'émulation sur attach-only/remote CDP
openclaw browser tabs
openclaw browser tab             # raccourci pour l'onglet actuel
openclaw browser tab new
openclaw browser tab select 2
openclaw browser tab close 2
openclaw browser open https://example.com
openclaw browser focus abcd1234
openclaw browser close abcd1234
```

</Accordion>

<Accordion title="Inspection : capture d'écran, snapshot, console, erreurs, requêtes">

```bash
openclaw browser screenshot
openclaw browser screenshot --full-page
openclaw browser screenshot --ref 12        # ou --ref e12
openclaw browser snapshot
openclaw browser snapshot --format aria --limit 200
openclaw browser snapshot --interactive --compact --depth 6
openclaw browser snapshot --efficient
openclaw browser snapshot --labels
openclaw browser snapshot --selector "#main" --interactive
openclaw browser snapshot --frame "iframe#main" --interactive
openclaw browser console --level error
openclaw browser errors --clear
openclaw browser requests --filter api --clear
openclaw browser pdf
openclaw browser responsebody "**/api" --max-chars 5000
```

</Accordion>

<Accordion title="Actions : navigate, click, type, drag, wait, evaluate">

```bash
openclaw browser navigate https://example.com
openclaw browser resize 1280 720
openclaw browser click 12 --double           # ou e12 pour les refs de rôle
openclaw browser type 23 "hello" --submit
openclaw browser press Enter
openclaw browser hover 44
openclaw browser scrollintoview e12
openclaw browser drag 10 11
openclaw browser select 9 OptionA OptionB
openclaw browser download e12 report.pdf
openclaw browser waitfordownload report.pdf
openclaw browser upload /tmp/openclaw/uploads/file.pdf
openclaw browser fill --fields '[{"ref":"1","type":"text","value":"Ada"}]'
openclaw browser dialog --accept
openclaw browser wait --text "Done"
openclaw browser wait "#main" --url "**/dash" --load networkidle --fn "window.ready===true"
openclaw browser evaluate --fn '(el) => el.textContent' --ref 7
openclaw browser highlight e12
openclaw browser trace start
openclaw browser trace stop
```

</Accordion>

<Accordion title="État : cookies, stockage, hors ligne, en-têtes, géo, appareil">

```bash
openclaw browser cookies
openclaw browser cookies set session abc123 --url "https://example.com"
openclaw browser cookies clear
openclaw browser storage local get
openclaw browser storage local set theme dark
openclaw browser storage session clear
openclaw browser set offline on
openclaw browser set headers --headers-json '{"X-Debug":"1"}'
openclaw browser set credentials user pass            # --clear pour supprimer
openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"
openclaw browser set media dark
openclaw browser set timezone America/New_York
openclaw browser set locale en-US
openclaw browser set device "iPhone 14"
```

</Accordion>

</AccordionGroup>

Notes :

- `upload` et `dialog` sont des appels **d'armement** ; exécutez-les avant le click/press qui déclenche le chooser/dialog.
- `click`/`type`/etc nécessitent une `ref` de `snapshot` (ref numérique `12` ou ref de rôle `e12`). Les sélecteurs CSS ne sont intentionnellement pas supportés pour les actions.
- Les chemins de téléchargement, trace et upload sont limités aux racines temporaires OpenClaw : `/tmp/openclaw{,/downloads,/uploads}` (fallback : `${os.tmpdir()}/openclaw/...`).
- `upload` peut aussi définir directement les entrées de fichier via `--input-ref` ou `--element`.

Drapeaux Snapshot en un coup d'œil :

- `--format ai` (par défaut avec Playwright) : snapshot IA avec refs numériques (`aria-ref="<n>"`).
- `--format aria` : arbre d'accessibilité, pas de refs ; inspection uniquement.
- `--efficient` (ou `--mode efficient`) : preset de snapshot de rôle compact. Définissez `browser.snapshotDefaults.mode: "efficient"` pour en faire la valeur par défaut (voir [Configuration de la Gateway](/fr/gateway/configuration-reference#browser)).
- `--interactive`, `--compact`, `--depth`, `--selector` forcent un snapshot de rôle avec refs `ref=e12`. `--frame "<iframe>"` limite les snapshots de rôle à une iframe.
- `--labels` ajoute une capture d'écran viewport uniquement avec des étiquettes ref superposées (imprime `MEDIA:<path>`).

## Snapshots et refs

OpenClaw supporte deux styles de "snapshot" :

- **Snapshot IA (refs numériques)** : `openclaw browser snapshot` (par défaut ; `--format ai`)
  - Sortie : un snapshot texte qui inclut des refs numériques.
  - Actions : `openclaw browser click 12`, `openclaw browser type 23 "hello"`.
  - En interne, la ref est résolue via `aria-ref` de Playwright.

- **Snapshot de rôle (refs de rôle comme `e12`)** : `openclaw browser snapshot --interactive` (ou `--compact`, `--depth`, `--selector`, `--frame`)
  - Sortie : une liste/arbre basée sur les rôles avec `[ref=e12]` (et optionnel `[nth=1]`).
  - Actions : `openclaw browser click e12`, `openclaw browser highlight e12`.
  - En interne, la ref est résolue via `getByRole(...)` (plus `nth()` pour les doublons).
  - Ajoutez `--labels` pour inclure une capture d'écran viewport avec des étiquettes `e12` superposées.

Comportement des refs :

- Les refs **ne sont pas stables à travers les navigations** ; si quelque chose échoue, réexécutez `snapshot` et utilisez une ref fraîche.
- Si le snapshot de rôle a été pris avec `--frame`, les refs de rôle sont limitées à cette iframe jusqu'au prochain snapshot de rôle.

## Améliorations Wait

Vous pouvez attendre plus que juste le temps/texte :

- Attendre une URL (globs supportés par Playwright) :
  - `openclaw browser wait --url "**/dash"`
- Attendre un état de chargement :
  - `openclaw browser wait --load networkidle`
- Attendre un prédicat JS :
  - `openclaw browser wait --fn "window.ready===true"`
- Attendre qu'un sélecteur devienne visible :
  - `openclaw browser wait "#main"`

Ceux-ci peuvent être combinés :

```bash
openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --fn "window.ready===true" \
  --timeout-ms 15000
```

## Workflows de débogage

Quand une action échoue (par ex. "not visible", "strict mode violation", "covered") :

1. `openclaw browser snapshot --interactive`
2. Utilisez `click <ref>` / `type <ref>` (préférez les refs de rôle en mode interactif)
3. Si ça échoue toujours : `openclaw browser highlight <ref>` pour voir ce que Playwright cible
4. Si la page se comporte bizarrement :
   - `openclaw browser errors --clear`
   - `openclaw browser requests --filter api --clear`
5. Pour un débogage approfondi : enregistrez une trace :
   - `openclaw browser trace start`
   - reproduisez le problème
   - `openclaw browser trace stop` (imprime `TRACE:<path>`)

## Sortie JSON

`--json` est pour le scripting et les outils structurés.

Exemples :

```bash
openclaw browser status --json
openclaw browser snapshot --interactive --json
openclaw browser requests --filter api --json
openclaw browser cookies --json
```

Les snapshots de rôle en JSON incluent `refs` plus un petit bloc `stats` (lines/chars/refs/interactive) pour que les outils puissent raisonner sur la taille et la densité de la charge utile.

## Boutons d'état et d'environnement

Ceux-ci sont utiles pour les workflows "faire se comporter le site comme X" :

- Cookies : `cookies`, `cookies set`, `cookies clear`
- Stockage : `storage local|session get|set|clear`
- Hors ligne : `set offline on|off`
- En-têtes : `set headers --headers-json '{"X-Debug":"1"}'` (l'ancien `set headers --json '{"X-Debug":"1"}'` reste supporté)
- Authentification HTTP basique : `set credentials user pass` (ou `--clear`)
- Géolocalisation : `set geo <lat> <lon> --origin "https://example.com"` (ou `--clear`)
- Média : `set media dark|light|no-preference|none`
- Fuseau horaire / locale : `set timezone ...`, `set locale ...`
- Appareil / viewport :
  - `set device "iPhone 14"` (présets d'appareils Playwright)
  - `set viewport 1280 720`

## Sécurité et confidentialité

- Le profil de navigateur openclaw peut contenir des sessions connectées ; traitez-le comme sensible.
- `browser act kind=evaluate` / `openclaw browser evaluate` et `wait --fn`
  exécutent du JavaScript arbitraire dans le contexte de la page. L'injection de prompt peut le diriger.
  Désactivez-le avec `browser.evaluateEnabled=false` si vous n'en avez pas besoin.
- Pour les connexions et les notes anti-bot (X/Twitter, etc.), voir [Connexion au navigateur + publication X/Twitter](/fr/tools/browser-login).
- Gardez l'hôte Gateway/node privé (loopback ou tailnet uniquement).
- Les points de terminaison CDP distants sont puissants ; tunnelisez et protégez-les.

Exemple en mode strict (bloquer les destinations privées/internes par défaut) :

```json5
{
  browser: {
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false,
      hostnameAllowlist: ["*.example.com", "example.com"],
      allowedHostnames: ["localhost"], // optional exact allow
    },
  },
}
```

## Connexes

- [Navigateur](/fr/tools/browser) — aperçu, configuration, profils, sécurité
- [Connexion au navigateur](/fr/tools/browser-login) — se connecter aux sites
- [Dépannage du navigateur Linux](/fr/tools/browser-linux-troubleshooting)
- [Dépannage du navigateur WSL2](/fr/tools/browser-wsl2-windows-remote-cdp-troubleshooting)
