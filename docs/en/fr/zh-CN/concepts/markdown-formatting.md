---
read_when:
  - Vous modifiez la logique de formatage Markdown ou de chunking des canaux sortants
  - Vous ajoutez de nouveaux formateurs de canaux ou des mappages de styles
  - Vous déboguez des problèmes de régression de formatage entre canaux
summary: Pipeline de formatage Markdown pour les canaux sortants
title: Formatage Markdown
x-i18n:
  generated_at: "2026-02-01T20:22:42Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f9cbf9b744f9a218860730f29435bcad02d3db80b1847fed5f17c063c97d4820
  source_path: concepts/markdown-formatting.md
  workflow: 14
---

# Formatage Markdown

OpenClaw effectue le formatage en convertissant le Markdown sortant en une représentation intermédiaire (IR) partagée, puis en le rendant en sortie spécifique au canal. L'IR préserve le texte source inchangé tout en portant les informations d'étendue de style/lien, ce qui rend le chunking et le rendu cohérents entre les canaux.

## Objectifs

- **Cohérence :** une seule analyse, plusieurs rendus.
- **Chunking sécurisé :** diviser le texte avant le rendu, en s'assurant que le formatage en ligne ne se casse pas entre les chunks.
- **Adaptation au canal :** mapper le même IR à Slack mrkdwn, Telegram HTML et Signal style ranges, sans réanalyse Markdown.

## Pipeline

1. **Analyser Markdown -> IR**
   - L'IR est du texte pur plus des étendues de style (gras/italique/barré/code/spoiler) et des étendues de lien.
   - Les décalages utilisent des unités de code UTF-16 pour aligner les étendues de style Signal avec son API.
   - Les tableaux ne sont analysés que si la conversion de tableau est activée pour le canal.
2. **Chunker l'IR (format-first)**
   - Le chunking opère sur le texte IR avant le rendu.
   - Le formatage en ligne ne se casse pas entre les chunks ; les étendues sont découpées par chunk.
3. **Rendu par canal**
   - **Slack :** marquage mrkdwn (gras/italique/barré/code), liens au format `<url|label>`.
   - **Telegram :** balises HTML (`<b>`, `<i>`, `<s>`, `<code>`, `<pre><code>`, `<a href>`).
   - **Signal :** texte pur + étendues `text-style` ; les liens deviennent `label (url)` lorsque le label diffère de l'URL.

## Exemple d'IR

Markdown d'entrée :

```markdown
Hello **world** — see [docs](https://docs.openclaw.ai).
```

IR (schématique) :

```json
{
  "text": "Hello world — see docs.",
  "styles": [{ "start": 6, "end": 11, "style": "bold" }],
  "links": [{ "start": 19, "end": 23, "href": "https://docs.openclaw.ai" }]
}
```

## Cas d'usage

- Les adaptateurs sortants pour Slack, Telegram et Signal effectuent le rendu à partir de l'IR.
- Les autres canaux (WhatsApp, iMessage, Microsoft Teams, Discord) utilisent toujours du texte pur ou leurs propres règles de formatage, avec conversion de tableau Markdown appliquée avant le chunking lorsqu'activée.

## Traitement des tableaux

Le support des tableaux Markdown n'est pas cohérent entre les clients de chat. Utilisez `markdown.tables` pour contrôler la conversion par canal (et par compte).

- `code` : rendre les tableaux sous forme de bloc de code (par défaut pour la plupart des canaux).
- `bullets` : convertir chaque ligne en liste à puces (par défaut pour Signal + WhatsApp).
- `off` : désactiver l'analyse et la conversion des tableaux ; le texte du tableau brut passe directement.

Clés de configuration :

```yaml
channels:
  discord:
    markdown:
      tables: code
    accounts:
      work:
        markdown:
          tables: off
```

## Règles de chunking

- Les limites de chunking proviennent des adaptateurs/configurations de canal, appliquées au texte IR.
- Les clôtures de code sont conservées comme un seul chunk avec une nouvelle ligne de fin, pour assurer un rendu correct du canal.
- Les préfixes de liste et les préfixes de bloc de citation font partie du texte IR, donc le chunking ne se casse pas au milieu d'un préfixe.
- Le formatage en ligne (gras/italique/barré/code en ligne/spoiler) ne se casse pas entre les chunks ; les rendus rouvrent les styles dans chaque chunk.

Pour plus de détails sur le comportement du chunking entre canaux, voir [Streaming + Chunking](/concepts/streaming).

## Stratégie de lien

- **Slack :** `[label](url)` -> `<url|label>` ; les URL nues restent inchangées. Les autolinks sont désactivés lors de l'analyse pour éviter les doublons.
- **Telegram :** `[label](url)` -> `<a href="url">label</a>` (mode analyse HTML).
- **Signal :** `[label](url)` -> `label (url)`, sauf si le label correspond à l'URL.

## Spoilers

Les marqueurs de spoiler (`||spoiler||`) ne sont analysés que pour Signal, mappés à des étendues de style SPOILER. Les autres canaux les traitent comme du texte pur.

## Comment ajouter ou mettre à jour un formateur de canal

1. **Analyser une fois :** utilisez la fonction d'aide partagée `markdownToIR(...)`, en passant les options appropriées au canal (autolinks, style de titre, préfixe de bloc de citation).
2. **Rendu :** implémentez un rendu avec `renderMarkdownWithMarkers(...)` et un mappage de marqueurs de style (ou étendues de style Signal).
3. **Chunking :** appelez `chunkMarkdownIR(...)` avant le rendu ; rendez chunk par chunk.
4. **Intégration à l'adaptateur :** mettez à jour l'adaptateur sortant du canal pour utiliser le nouveau chunker et rendu.
5. **Tests :** ajoutez ou mettez à jour les tests de formatage, et les tests de livraison sortante si le canal utilise le chunking.

## Pièges courants

- Les marqueurs entre crochets pointus Slack (`<@U123>`, `<#C123>`, `<https://...>`) doivent être préservés ; échappez correctement le HTML brut.
- Telegram HTML nécessite d'échapper le texte en dehors des balises pour éviter la corruption du balisage.
- Les étendues de style Signal dépendent des décalages UTF-16 ; n'utilisez pas les décalages de point de code.
- Préservez la nouvelle ligne de fin des clôtures de code pour assurer que la balise de fermeture est sur sa propre ligne.
