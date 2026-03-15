---
title: "Outil PDF"
summary: "Analysez un ou plusieurs documents PDF avec support natif du fournisseur et secours d'extraction"
read_when:
  - You want to analyze PDFs from agents
  - You need exact pdf tool parameters and limits
  - You are debugging native PDF mode vs extraction fallback
---

# Outil PDF

`pdf` analyse un ou plusieurs documents PDF et retourne du texte.

Comportement rapide :

- Mode fournisseur natif pour les fournisseurs de modèles Anthropic et Google.
- Mode secours d'extraction pour les autres fournisseurs (extraire d'abord le texte, puis les images de page si nécessaire).
- Supporte une entrée unique (`pdf`) ou multiple (`pdfs`), max 10 PDF par appel.

## Disponibilité

L'outil n'est enregistré que lorsqu'OpenClaw peut résoudre une configuration de modèle capable de traiter les PDF pour l'agent :

1. `agents.defaults.pdfModel`
2. secours à `agents.defaults.imageModel`
3. secours aux valeurs par défaut du fournisseur basées sur l'authentification disponible

Si aucun modèle utilisable ne peut être résolu, l'outil `pdf` n'est pas exposé.

## Référence d'entrée

- `pdf` (`string`): un chemin PDF ou une URL
- `pdfs` (`string[]`): plusieurs chemins PDF ou URLs, jusqu'à 10 au total
- `prompt` (`string`): invite d'analyse, par défaut `Analyze this PDF document.`
- `pages` (`string`): filtre de page comme `1-5` ou `1,3,7-9`
- `model` (`string`): remplacement de modèle optionnel (`provider/model`)
- `maxBytesMb` (`number`): limite de taille par PDF en MB

Notes d'entrée :

- `pdf` et `pdfs` sont fusionnés et dédupliqués avant le chargement.
- Si aucune entrée PDF n'est fournie, l'outil génère une erreur.
- `pages` est analysé comme des numéros de page basés sur 1, dédupliqués, triés et limités au nombre maximum de pages configuré.
- `maxBytesMb` par défaut à `agents.defaults.pdfMaxBytesMb` ou `10`.

## Références PDF supportées

- chemin de fichier local (y compris l'expansion `~`)
- URL `file://`
- URL `http://` et `https://`

Notes de référence :

- Les autres schémas URI (par exemple `ftp://`) sont rejetés avec `unsupported_pdf_reference`.
- En mode sandbox, les URLs distantes `http(s)` sont rejetées.
- Avec la politique de fichiers réservés à l'espace de travail activée, les chemins de fichiers locaux en dehors des racines autorisées sont rejetés.

## Modes d'exécution

### Mode fournisseur natif

Le mode natif est utilisé pour les fournisseurs `anthropic` et `google`.
L'outil envoie les octets PDF bruts directement aux API du fournisseur.

Limites du mode natif :

- `pages` n'est pas supporté. S'il est défini, l'outil retourne une erreur.

### Mode secours d'extraction

Le mode secours est utilisé pour les fournisseurs non-natifs.

Flux :

1. Extraire le texte des pages sélectionnées (jusqu'à `agents.defaults.pdfMaxPages`, par défaut `20`).
2. Si la longueur du texte extrait est inférieure à `200` caractères, rendre les pages sélectionnées en images PNG et les inclure.
3. Envoyer le contenu extrait plus l'invite au modèle sélectionné.

Détails du secours :

- L'extraction d'images de page utilise un budget de pixels de `4,000,000`.
- Si le modèle cible ne supporte pas l'entrée d'image et qu'il n'y a pas de texte extractible, l'outil génère une erreur.
- Le secours d'extraction nécessite `pdfjs-dist` (et `@napi-rs/canvas` pour le rendu d'images).

## Configuration

```json5
{
  agents: {
    defaults: {
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5-mini"],
      },
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
    },
  },
}
```

Voir [Référence de configuration](/fr/gateway/configuration-reference) pour les détails complets des champs.

## Détails de sortie

L'outil retourne du texte dans `content[0].text` et des métadonnées structurées dans `details`.

Champs `details` courants :

- `model`: référence de modèle résolue (`provider/model`)
- `native`: `true` pour le mode fournisseur natif, `false` pour le secours
- `attempts`: tentatives de secours qui ont échoué avant le succès

Champs de chemin :

- entrée PDF unique : `details.pdf`
- entrées PDF multiples : `details.pdfs[]` avec entrées `pdf`
- métadonnées de réécriture de chemin sandbox (le cas échéant) : `rewrittenFrom`

## Comportement d'erreur

- Entrée PDF manquante : lance `pdf required: provide a path or URL to a PDF document`
- Trop de PDF : retourne une erreur structurée dans `details.error = "too_many_pdfs"`
- Schéma de référence non supporté : retourne `details.error = "unsupported_pdf_reference"`
- Mode natif avec `pages` : lance une erreur claire `pages is not supported with native PDF providers`

## Exemples

PDF unique :

```json
{
  "pdf": "/tmp/report.pdf",
  "prompt": "Summarize this report in 5 bullets"
}
```

PDF multiples :

```json
{
  "pdfs": ["/tmp/q1.pdf", "/tmp/q2.pdf"],
  "prompt": "Compare risks and timeline changes across both documents"
}
```

Modèle de secours filtré par page :

```json
{
  "pdf": "https://example.com/report.pdf",
  "pages": "1-3,7",
  "model": "openai/gpt-5-mini",
  "prompt": "Extract only customer-impacting incidents"
}
```
