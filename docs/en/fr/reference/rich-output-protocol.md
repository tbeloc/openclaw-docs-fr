# Protocole de sortie enrichie

La sortie de l'assistant peut contenir un petit ensemble de directives de livraison/rendu :

- `MEDIA:` pour la livraison de pièces jointes
- `[[audio_as_voice]]` pour les indices de présentation audio
- `[[reply_to_current]]` / `[[reply_to:<id>]]` pour les métadonnées de réponse
- `[embed ...]` pour le rendu riche de l'interface de contrôle

Ces directives sont distinctes. `MEDIA:` et les balises de voix/réponse restent des métadonnées de livraison ; `[embed ...]` est le seul chemin de rendu riche pour le web.

## `[embed ...]`

`[embed ...]` est la seule syntaxe de rendu riche orientée agent pour l'interface de contrôle.

Exemple auto-fermant :

```text
[embed ref="cv_123" title="Status" /]
```

Règles :

- `[view ...]` n'est plus valide pour les nouvelles sorties.
- Les shortcodes d'intégration se rendent uniquement sur la surface du message de l'assistant.
- Seules les intégrations soutenues par une URL sont rendues. Utilisez `ref="..."` ou `url="..."`.
- Les shortcodes d'intégration HTML en ligne sous forme de bloc ne sont pas rendus.
- L'interface web supprime le shortcode du texte visible et rend l'intégration en ligne.
- `MEDIA:` n'est pas un alias d'intégration et ne doit pas être utilisé pour le rendu d'intégration riche.

## Forme de rendu stockée

Le bloc de contenu de l'assistant normalisé/stocké est un élément `canvas` structuré :

```json
{
  "type": "canvas",
  "preview": {
    "kind": "canvas",
    "surface": "assistant_message",
    "render": "url",
    "viewId": "cv_123",
    "url": "/__openclaw__/canvas/documents/cv_123/index.html",
    "title": "Status",
    "preferredHeight": 320
  }
}
```

Les blocs riches stockés/rendus utilisent cette forme `canvas` directement. `present_view` n'est pas reconnu.
