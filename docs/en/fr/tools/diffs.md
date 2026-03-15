---
title: "Diffs"
summary: "Visionneuse de diff en lecture seule et moteur de rendu de fichiers pour les agents (outil de plugin optionnel)"
description: "Utilisez le plugin Diffs optionnel pour afficher les modifications de texte ou les correctifs unifiés avant et après sous forme de vue de diff hébergée par la passerelle, un fichier (PNG ou PDF), ou les deux."
read_when:
  - You want agents to show code or markdown edits as diffs
  - You want a canvas-ready viewer URL or a rendered diff file
  - You need controlled, temporary diff artifacts with secure defaults
---

# Diffs

`diffs` est un outil de plugin optionnel avec des conseils système intégrés concis et une compétence complémentaire qui transforme le contenu des modifications en un artefact de diff en lecture seule pour les agents.

Il accepte soit :

- du texte `before` et `after`
- un `patch` unifié

Il peut retourner :

- une URL de visionneuse de passerelle pour la présentation sur canvas
- un chemin de fichier rendu (PNG ou PDF) pour la livraison de messages
- les deux résultats en un seul appel

Lorsqu'il est activé, le plugin ajoute des conseils d'utilisation concis dans l'espace de l'invite système et expose également une compétence détaillée pour les cas où l'agent a besoin d'instructions plus complètes.

## Démarrage rapide

1. Activez le plugin.
2. Appelez `diffs` avec `mode: "view"` pour les flux canvas-first.
3. Appelez `diffs` avec `mode: "file"` pour les flux de livraison de fichiers de chat.
4. Appelez `diffs` avec `mode: "both"` quand vous avez besoin des deux artefacts.

## Activer le plugin

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
      },
    },
  },
}
```

## Désactiver les conseils système intégrés

Si vous souhaitez garder l'outil `diffs` activé mais désactiver ses conseils intégrés dans l'invite système, définissez `plugins.entries.diffs.hooks.allowPromptInjection` sur `false` :

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        hooks: {
          allowPromptInjection: false,
        },
      },
    },
  },
}
```

Cela bloque le hook `before_prompt_build` du plugin diffs tout en gardant le plugin, l'outil et la compétence complémentaire disponibles.

Si vous souhaitez désactiver à la fois les conseils et l'outil, désactivez le plugin à la place.

## Flux de travail typique de l'agent

1. L'agent appelle `diffs`.
2. L'agent lit les champs `details`.
3. L'agent soit :
   - ouvre `details.viewerUrl` avec `canvas present`
   - envoie `details.filePath` avec `message` en utilisant `path` ou `filePath`
   - fait les deux

## Exemples d'entrée

Avant et après :

```json
{
  "before": "# Hello\n\nOne",
  "after": "# Hello\n\nTwo",
  "path": "docs/example.md",
  "mode": "view"
}
```

Patch :

```json
{
  "patch": "diff --git a/src/example.ts b/src/example.ts\n--- a/src/example.ts\n+++ b/src/example.ts\n@@ -1 +1 @@\n-const x = 1;\n+const x = 2;\n",
  "mode": "both"
}
```

## Référence d'entrée de l'outil

Tous les champs sont optionnels sauf indication contraire :

- `before` (`string`) : texte original. Requis avec `after` quand `patch` est omis.
- `after` (`string`) : texte mis à jour. Requis avec `before` quand `patch` est omis.
- `patch` (`string`) : texte de diff unifié. Mutuellement exclusif avec `before` et `after`.
- `path` (`string`) : nom de fichier d'affichage pour le mode avant et après.
- `lang` (`string`) : indice de remplacement de langue pour le mode avant et après.
- `title` (`string`) : remplacement du titre de la visionneuse.
- `mode` (`"view" | "file" | "both"`) : mode de sortie. Par défaut `defaults.mode` du plugin.
- `theme` (`"light" | "dark"`) : thème de la visionneuse. Par défaut `defaults.theme` du plugin.
- `layout` (`"unified" | "split"`) : disposition du diff. Par défaut `defaults.layout` du plugin.
- `expandUnchanged` (`boolean`) : développer les sections inchangées quand le contexte complet est disponible. Option par appel uniquement (pas une clé de défaut du plugin).
- `fileFormat` (`"png" | "pdf"`) : format de fichier rendu. Par défaut `defaults.fileFormat` du plugin.
- `fileQuality` (`"standard" | "hq" | "print"`) : préréglage de qualité pour le rendu PNG ou PDF.
- `fileScale` (`number`) : remplacement de l'échelle de l'appareil (`1`-`4`).
- `fileMaxWidth` (`number`) : largeur de rendu maximale en pixels CSS (`640`-`2400`).
- `ttlSeconds` (`number`) : TTL de l'artefact de visionneuse en secondes. Par défaut 1800, max 21600.
- `baseUrl` (`string`) : remplacement de l'origine de l'URL de la visionneuse. Doit être `http` ou `https`, pas de query/hash.

Validation et limites :

- `before` et `after` chacun max 512 KiB.
- `patch` max 2 MiB.
- `path` max 2048 bytes.
- `lang` max 128 bytes.
- `title` max 1024 bytes.
- Limite de complexité du patch : max 128 fichiers et 120000 lignes au total.
- `patch` et `before` ou `after` ensemble sont rejetés.
- Limites de sécurité des fichiers rendus (s'appliquent à PNG et PDF) :
  - `fileQuality: "standard"` : max 8 MP (8 000 000 pixels rendus).
  - `fileQuality: "hq"` : max 14 MP (14 000 000 pixels rendus).
  - `fileQuality: "print"` : max 24 MP (24 000 000 pixels rendus).
  - PDF a également un maximum de 50 pages.

## Contrat des détails de sortie

L'outil retourne des métadonnées structurées sous `details`.

Champs partagés pour les modes qui créent une visionneuse :

- `artifactId`
- `viewerUrl`
- `viewerPath`
- `title`
- `expiresAt`
- `inputKind`
- `fileCount`
- `mode`

Champs de fichier quand PNG ou PDF est rendu :

- `filePath`
- `path` (même valeur que `filePath`, pour la compatibilité de l'outil de message)
- `fileBytes`
- `fileFormat`
- `fileQuality`
- `fileScale`
- `fileMaxWidth`

Résumé du comportement du mode :

- `mode: "view"` : champs de visionneuse uniquement.
- `mode: "file"` : champs de fichier uniquement, pas d'artefact de visionneuse.
- `mode: "both"` : champs de visionneuse plus champs de fichier. Si le rendu du fichier échoue, la visionneuse retourne toujours avec `fileError`.

## Sections inchangées réduites

- La visionneuse peut afficher des lignes comme `N unmodified lines`.
- Les contrôles d'expansion sur ces lignes sont conditionnels et non garantis pour chaque type d'entrée.
- Les contrôles d'expansion apparaissent quand le diff rendu a des données de contexte extensibles, ce qui est typique pour l'entrée avant et après.
- Pour de nombreuses entrées de patch unifié, les corps de contexte omis ne sont pas disponibles dans les hunks de patch analysés, donc la ligne peut apparaître sans contrôles d'expansion. C'est le comportement attendu.
- `expandUnchanged` s'applique uniquement quand le contexte extensible existe.

## Valeurs par défaut du plugin

Définissez les valeurs par défaut au niveau du plugin dans `~/.openclaw/openclaw.json` :

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        config: {
          defaults: {
            fontFamily: "Fira Code",
            fontSize: 15,
            lineSpacing: 1.6,
            layout: "unified",
            showLineNumbers: true,
            diffIndicators: "bars",
            wordWrap: true,
            background: true,
            theme: "dark",
            fileFormat: "png",
            fileQuality: "standard",
            fileScale: 2,
            fileMaxWidth: 960,
            mode: "both",
          },
        },
      },
    },
  },
}
```

Valeurs par défaut supportées :

- `fontFamily`
- `fontSize`
- `lineSpacing`
- `layout`
- `showLineNumbers`
- `diffIndicators`
- `wordWrap`
- `background`
- `theme`
- `fileFormat`
- `fileQuality`
- `fileScale`
- `fileMaxWidth`
- `mode`

Les paramètres explicites de l'outil remplacent ces valeurs par défaut.

## Configuration de sécurité

- `security.allowRemoteViewer` (`boolean`, par défaut `false`)
  - `false` : les requêtes non-loopback aux routes de visionneuse sont refusées.
  - `true` : les visionneuses distantes sont autorisées si le chemin tokenisé est valide.

Exemple :

```json5
{
  plugins: {
    entries: {
      diffs: {
        enabled: true,
        config: {
          security: {
            allowRemoteViewer: false,
          },
        },
      },
    },
  },
}
```

## Cycle de vie et stockage des artefacts

- Les artefacts sont stockés sous le sous-dossier temp : `$TMPDIR/openclaw-diffs`.
- Les métadonnées de l'artefact de visionneuse contiennent :
  - ID d'artefact aléatoire (20 caractères hex)
  - token aléatoire (48 caractères hex)
  - `createdAt` et `expiresAt`
  - chemin `viewer.html` stocké
- Le TTL de visionneuse par défaut est de 30 minutes quand non spécifié.
- Le TTL de visionneuse maximum accepté est de 6 heures.
- Le nettoyage s'exécute opportunément après la création de l'artefact.
- Les artefacts expirés sont supprimés.
- Le nettoyage de secours supprime les dossiers obsolètes plus anciens que 24 heures quand les métadonnées manquent.

## URL de visionneuse et comportement réseau

Route de visionneuse :

- `/plugins/diffs/view/{artifactId}/{token}`

Ressources de visionneuse :

- `/plugins/diffs/assets/viewer.js`
- `/plugins/diffs/assets/viewer-runtime.js`

Comportement de construction d'URL :

- Si `baseUrl` est fourni, il est utilisé après validation stricte.
- Sans `baseUrl`, l'URL de visionneuse par défaut est loopback `127.0.0.1`.
- Si le mode de liaison de la passerelle est `custom` et `gateway.customBindHost` est défini, cet hôte est utilisé.

Règles `baseUrl` :

- Doit être `http://` ou `https://`.
- Query et hash sont rejetés.
- L'origine plus le chemin de base optionnel est autorisé.

## Modèle de sécurité

Durcissement de la visionneuse :

- Loopback uniquement par défaut.
- Chemins de visionneuse tokenisés avec validation stricte de l'ID et du token.
- CSP de réponse de visionneuse :
  - `default-src 'none'`
  - scripts et ressources uniquement depuis self
  - pas de `connect-src` sortant
- Limitation des tentatives distantes quand l'accès distant est activé :
  - 40 échecs par 60 secondes
  - Verrouillage de 60 secondes (`429 Too Many Requests`)

Durcissement du rendu de fichier :

- Le routage des requêtes du navigateur de capture d'écran est refusé par défaut.
- Seules les ressources de visionneuse locales depuis `http://127.0.0.1/plugins/diffs/assets/*` sont autorisées.
- Les requêtes réseau externes sont bloquées.

## Exigences du navigateur pour le mode fichier

`mode: "file"` et `mode: "both"` nécessitent un navigateur compatible Chromium.

Ordre de résolution :

1. `browser.executablePath` dans la configuration OpenClaw.
2. Variables d'environnement :
   - `OPENCLAW_BROWSER_EXECUTABLE_PATH`
   - `BROWSER_EXECUTABLE_PATH`
   - `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`
3. Découverte de commande/chemin de plateforme de secours.

Texte d'erreur courant :

- `Diff PNG/PDF rendering requires a Chromium-compatible browser...`

Corrigez en installant Chrome, Chromium, Edge ou Brave, ou en définissant l'une des options de chemin exécutable ci-dessus.

## Dépannage

Erreurs de validation d'entrée :

- `Provide patch or both before and after text.`
  - Incluez à la fois `before` et `after`, ou fournissez `patch`.
- `Provide either patch or before/after input, not both.`
  - Ne mélangez pas les modes d'entrée.
- `Invalid baseUrl: ...`
  - Utilisez l'origine `http(s)` avec chemin optionnel, pas de query/hash.
- `{field} exceeds maximum size (...)`
  - Réduisez la taille de la charge utile.
- Rejet de patch volumineux
  - Réduisez le nombre de fichiers de patch ou les lignes totales.

Problèmes d'accessibilité de la visionneuse :

- L'URL de visionneuse se résout en `127.0.0.1` par défaut.
- Pour les scénarios d'accès distant, soit :
  - passez `baseUrl` par appel d'outil, soit
  - utilisez `gateway.bind=custom` et `gateway.customBindHost`
- Activez `security.allowRemoteViewer` uniquement quand vous avez l'intention d'un accès à la visionneuse externe.

La ligne de lignes inchangées n'a pas de bouton d'expansion :

- Cela peut se produire pour l'entrée de patch quand le patch ne porte pas de contexte extensible.
- C'est le comportement attendu et n'indique pas un échec de la visionneuse.

Artefact non trouvé :

- L'artefact a expiré en raison du TTL.
- Le token ou le chemin a changé.
- Le nettoyage a supprimé les données obsolètes.

## Conseils opérationnels

- Préférez `mode: "view"` pour les révisions interactives locales sur canvas.
- Préférez `mode: "file"` pour les canaux de chat sortants qui ont besoin d'une pièce jointe.
- Gardez `allowRemoteViewer` désactivé sauf si votre déploiement nécessite des URL de visionneuse distantes.
- Définissez un `ttlSeconds` court explicite pour les diffs sensibles.
- Évitez d'envoyer des secrets dans l'entrée de diff quand ce n'est pas nécessaire.
- Si votre canal compresse les images de manière agressive (par exemple Telegram ou WhatsApp), préférez la sortie PDF (`fileFormat: "pdf"`).

Moteur de rendu de diff :

- Alimenté par [Diffs](https://diffs.com).

## Docs connexes

- [Tools overview](/fr/tools)
- [Plugins](/fr/tools/plugin)
- [Browser](/fr/tools/browser)
