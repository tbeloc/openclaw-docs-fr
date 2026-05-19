---
summary: "Testez les remplacements de plugins empaquetés avec les flux d'installation au moment de la configuration"
read_when:
  - Testing onboarding or setup flows against a locally packed plugin
  - Verifying a plugin package before publishing it
  - Replacing an automatic plugin install with a test artifact
title: "Remplacements d'installation de plugins"
sidebarTitle: "Remplacements d'installation"
---

Les remplacements d'installation de plugins permettent aux responsables de tester les installations de plugins au moment de la configuration par rapport à un package npm spécifique ou à une archive tarball npm-pack locale. Ils sont réservés aux tests E2E et à la validation des packages uniquement. Les utilisateurs normaux doivent installer les plugins avec
[`openclaw plugins install`](/fr/cli/plugins).

<Warning>
Les remplacements exécutent le code du plugin à partir de la source que vous fournissez. Utilisez-les uniquement dans un répertoire d'état isolé ou sur une machine de test jetable.
</Warning>

## Environnement

Les remplacements sont désactivés sauf si les deux variables sont définies :

```bash
export OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES=1
export OPENCLAW_PLUGIN_INSTALL_OVERRIDES='{
  "codex": "npm-pack:/tmp/openclaw-codex-2026.5.8.tgz",
  "openclaw-web-search": "npm:@openclaw/web-search@2026.5.8"
}'
```

La carte de remplacement est du JSON indexé par l'id du plugin. Les valeurs supportent :

- `npm:<registry-spec>` pour les packages de registre et les versions exactes ou les tags
- `npm-pack:<path.tgz>` pour les archives locales produites par `npm pack`

Les chemins relatifs `npm-pack:` sont résolus à partir du répertoire de travail actuel.

## Comportement

Lorsqu'un flux au moment de la configuration demande d'installer un plugin dont l'id apparaît dans la carte, OpenClaw utilise la source de remplacement au lieu du catalogue, du bundle ou de la source npm par défaut. Cela s'applique à l'intégration et aux autres flux qui utilisent le programme d'installation de plugins partagé au moment de la configuration.

Les remplacements appliquent toujours l'id de plugin attendu. Une archive mappée à `codex` doit installer un plugin dont l'id du manifeste est `codex`.

Les remplacements n'héritent pas du statut de source de confiance officielle. Même lorsque l'entrée du catalogue représente normalement un package appartenant à OpenClaw, un remplacement est traité comme une entrée de test fournie par l'opérateur.

Les fichiers `.env` de l'espace de travail ne peuvent pas activer les remplacements d'installation. Définissez ces variables dans le shell de confiance, la tâche CI ou la commande de test distant qui lance OpenClaw.

## E2E du package

Utilisez un répertoire d'état isolé afin que les installations de packages et les enregistrements d'installation ne touchent pas votre état OpenClaw normal :

```bash
npm pack extensions/codex --pack-destination /tmp

OPENCLAW_STATE_DIR="$(mktemp -d)" \
OPENCLAW_ALLOW_PLUGIN_INSTALL_OVERRIDES=1 \
OPENCLAW_PLUGIN_INSTALL_OVERRIDES='{"codex":"npm-pack:/tmp/openclaw-codex-2026.5.8.tgz"}' \
pnpm openclaw onboard --mode local
```

Vérifiez le package installé dans le répertoire d'état :

```bash
find "$OPENCLAW_STATE_DIR/npm/node_modules" -maxdepth 3 -name package.json -print
grep -R '"@openclaw/codex"' "$OPENCLAW_STATE_DIR/npm/package-lock.json"
```

Pour les E2E de fournisseur en direct, sourcez la clé API réelle à partir d'un shell de confiance ou d'un secret CI avant de lancer la commande de test. N'imprimez pas les clés ; signalez uniquement la source et si la clé était présente.
