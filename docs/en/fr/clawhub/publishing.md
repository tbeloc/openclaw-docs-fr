---
summary: "Comment fonctionne la publication sur ClawHub pour les skills, plugins, propriétaires, scopes, versions et révisions."
read_when:
  - Publishing a skill or plugin
  - Debugging owner or package scope errors
  - Adding publish UI, CLI, or backend behavior
---

# Publication sur ClawHub

La publication sur ClawHub est limitée au propriétaire : chaque publication cible un éditeur, et le serveur décide si l'utilisateur connecté est autorisé à publier là.

## Propriétaires

Un propriétaire est un identifiant d'éditeur ClawHub, tel que `@alice` ou `@openclaw`.
Les propriétaires personnels sont créés pour les utilisateurs. Les propriétaires d'organisation peuvent avoir plusieurs membres.

Lorsque vous publiez, vous utilisez soit votre propriétaire personnel, soit vous choisissez un propriétaire d'organisation où vous avez accès à la publication.

## Skills

Les skills sont publiés à partir d'un dossier de skill. La page publique est :

```text
https://clawhub.ai/<owner>/<slug>
```

Exemple :

```text
https://clawhub.ai/alice/review-helper
```

La demande de publication inclut le propriétaire sélectionné, le slug, la version, le journal des modifications et les fichiers. Le serveur vérifie que l'acteur peut publier en tant que ce propriétaire avant de créer la version.

## Plugins

Les plugins utilisent des noms de packages de style npm. Les noms de packages avec scope incluent le propriétaire dans la première partie du nom :

```text
@owner/package-name
```

Le scope doit correspondre au propriétaire de publication sélectionné. Si votre package s'appelle `@openclaw/dronzer`, il ne peut être publié que sous `@openclaw`. Si vous publiez sous `@vintageayu`, renommez le package en `@vintageayu/dronzer`.

Cela empêche un package de revendiquer un namespace d'organisation que l'éditeur ne contrôle pas.

## Flux de publication

1. L'interface utilisateur, la CLI ou le workflow GitHub rassemble les métadonnées et les fichiers du package.
2. La demande de publication est envoyée à ClawHub avec le propriétaire sélectionné.
3. Le serveur valide les permissions du propriétaire, le scope du package, le nom du package, la version, les limites de fichiers et les métadonnées source.
4. ClawHub stocke la version et démarre les vérifications de sécurité automatisées.
5. Les nouvelles versions sont masquées des surfaces d'installation/téléchargement normales jusqu'à ce que la révision et la vérification soient terminées.

Si la validation échoue, la version n'est pas créée.

## FAQ

### Le scope du package doit correspondre au propriétaire sélectionné

Si le scope du package et le propriétaire sélectionné ne correspondent pas, ClawHub rejette la publication :

```text
Package scope "@openclaw" must match selected owner "@vintageayu".
Publish as "@openclaw" or rename this package to "@vintageayu/dronzer".
```

Pour corriger cela, choisissez soit le propriétaire nommé par le scope du package, soit renommez le package pour que le scope corresponde au propriétaire sous lequel vous pouvez publier.

Si le nom du package a déjà le bon scope mais que le package est détenu par le mauvais éditeur, transférez plutôt la propriété :

```sh
clawhub package transfer @opik/opik-openclaw --to opik
```

Utilisez le transfert de package uniquement lorsque vous avez un accès administrateur au propriétaire du package actuel et à l'éditeur de destination. Cela ne vous permet pas de publier dans un scope que vous ne pouvez pas gérer.

Cela protège les namespaces d'organisation. Un package nommé `@openclaw/dronzer` revendique le namespace `@openclaw`, donc seuls les éditeurs ayant accès au propriétaire `@openclaw` peuvent le publier.
