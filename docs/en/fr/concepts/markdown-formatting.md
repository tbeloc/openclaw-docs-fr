---
summary: "Pipeline de formatage Markdown pour les canaux sortants"
read_when:
  - You are changing markdown formatting or chunking for outbound channels
  - You are adding a new channel formatter or style mapping
  - You are debugging formatting regressions across channels
title: "Formatage Markdown"
---

# Formatage Markdown

OpenClaw formate le Markdown sortant en le convertissant en une représentation intermédiaire partagée (IR) avant de générer la sortie spécifique à chaque canal. L'IR conserve le texte source intact tout en portant des spans de style/lien afin que le chunking et le rendu restent cohérents entre les canaux.

## Objectifs

- **Cohérence :** une étape d'analyse, plusieurs rendus.
- **Chunking sûr :** diviser le texte avant le rendu afin que le formatage en ligne ne se casse jamais entre les chunks.
- **Adaptation au canal :** mapper le même IR à Slack mrkdwn, Telegram HTML et Signal style ranges sans réanalyser le Markdown.

## Pipeline

1. **Analyser Markdown -> IR**
   - L'IR est du texte brut plus des spans de style (gras/italique/barré/code/spoiler) et des spans de lien.
   - Les décalages sont en unités de code UTF-16 afin que les plages de style Signal s'alignent avec son API.
   - Les tableaux ne sont analysés que lorsqu'un canal opte pour la conversion de tableau.
2. **Chunker l'IR (format en premier)**
   - Le chunking se fait sur le texte IR avant le rendu.
   - Le formatage en ligne ne se divise pas entre les chunks ; les spans sont découpés par chunk.
3. **Rendu par canal**
   - **Slack :** jetons mrkdwn (gras/italique/barré/code), liens comme `<url|label>`.
   - **Telegram :** balises HTML (`<b>`, `<i>`, `<s>`, `<code>`, `<pre><code>`, `<a href>`).
   - **Signal :** texte brut + plages `text-style` ; les liens deviennent `label (url)` quand le label diffère.

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

## Où c'est utilisé

- Les adaptateurs sortants Slack, Telegram et Signal se rendent à partir de l'IR.
- Les autres canaux (WhatsApp, iMessage, MS Teams, Discord) utilisent toujours du texte brut ou leurs propres règles de formatage, avec la conversion de tableau Markdown appliquée avant le chunking si activée.

## Gestion des tableaux

Les tableaux Markdown ne sont pas uniformément supportés sur tous les clients de chat. Utilisez `markdown.tables` pour contrôler la conversion par canal (et par compte).

- `code` : rendre les tableaux sous forme de blocs de code (par défaut pour la plupart des canaux).
- `bullets` : convertir chaque ligne en points de liste (par défaut pour Signal + WhatsApp).
- `off` : désactiver l'analyse des tableaux et la conversion ; le texte brut du tableau passe tel quel.

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

- Les limites de chunk proviennent des adaptateurs/config de canal et sont appliquées au texte IR.
- Les clôtures de code sont préservées comme un bloc unique avec une nouvelle ligne de fin afin que les canaux les rendent correctement.
- Les préfixes de liste et les préfixes de blockquote font partie du texte IR, donc le chunking ne divise pas au milieu d'un préfixe.
- Les styles en ligne (gras/italique/barré/code-en-ligne/spoiler) ne sont jamais divisés entre les chunks ; le rendu réouvre les styles à l'intérieur de chaque chunk.

Si vous avez besoin de plus d'informations sur le comportement du chunking entre les canaux, consultez [Streaming + chunking](/concepts/streaming).

## Politique de lien

- **Slack :** `[label](url)` -> `<url|label>` ; les URLs nues restent nues. L'autolink est désactivé lors de l'analyse pour éviter la double liaison.
- **Telegram :** `[label](url)` -> `<a href="url">label</a>` (mode d'analyse HTML).
- **Signal :** `[label](url)` -> `label (url)` sauf si le label correspond à l'URL.

## Spoilers

Les marqueurs de spoiler (`||spoiler||`) ne sont analysés que pour Signal, où ils correspondent à des plages de style SPOILER. Les autres canaux les traitent comme du texte brut.

## Comment ajouter ou mettre à jour un formateur de canal

1. **Analyser une fois :** utilisez l'assistant partagé `markdownToIR(...)` avec les options appropriées au canal (autolink, style de titre, préfixe blockquote).
2. **Rendu :** implémentez un rendu avec `renderMarkdownWithMarkers(...)` et une carte de marqueurs de style (ou des plages de style Signal).
3. **Chunk :** appelez `chunkMarkdownIR(...)` avant le rendu ; rendez chaque chunk.
4. **Adapter le câblage :** mettez à jour l'adaptateur sortant du canal pour utiliser le nouveau chunker et le rendu.
5. **Test :** ajoutez ou mettez à jour les tests de format et un test de livraison sortante si le canal utilise le chunking.

## Pièges courants

- Les jetons entre crochets Slack (`<@U123>`, `<#C123>`, `<https://...>`) doivent être préservés ; échappez le HTML brut en toute sécurité.
- Telegram HTML nécessite d'échapper le texte en dehors des balises pour éviter un balisage cassé.
- Les plages de style Signal dépendent des décalages UTF-16 ; n'utilisez pas les décalages de point de code.
- Préservez les nouvelles lignes de fin pour les blocs de code clôturés afin que les marqueurs de fermeture se trouvent sur leur propre ligne.
