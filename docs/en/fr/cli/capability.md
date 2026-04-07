---
summary: "CLI inférence en premier lieu pour les workflows de modèle, image, audio, TTS, vidéo, web et embedding soutenus par un fournisseur"
read_when:
  - Adding or modifying `openclaw infer` commands
  - Designing stable headless capability automation
title: "CLI d'inférence"
---

# CLI d'inférence

`openclaw infer` est la surface headless canonique pour les workflows d'inférence soutenus par un fournisseur.

`openclaw capability` reste supporté comme alias de secours pour la compatibilité.

Il expose intentionnellement les familles de capacités, et non les noms RPC de passerelle bruts ni les identifiants d'outils d'agent bruts.

## Arborescence des commandes

```text
 openclaw infer
  list
  inspect

  model
    run
    list
    inspect
    providers
    auth login
    auth logout
    auth status

  image
    generate
    edit
    describe
    describe-many
    providers

  audio
    transcribe
    providers

  tts
    convert
    voices
    providers
    status
    enable
    disable
    set-provider

  video
    generate
    describe
    providers

  web
    search
    fetch
    providers

  embedding
    create
    providers
```

## Transport

Drapeaux de transport supportés :

- `--local`
- `--gateway`

Le transport par défaut est implicitement automatique au niveau de la famille de commandes :

- Les commandes d'exécution sans état par défaut en local.
- Les commandes d'état gérées par la passerelle par défaut en passerelle.

Exemples :

```bash
openclaw infer model run --prompt "hello" --json
openclaw infer image generate --prompt "friendly lobster" --json
openclaw infer tts status --json
openclaw infer embedding create --text "hello world" --json
```

## Sortie JSON

Les commandes de capacité normalisent la sortie JSON sous une enveloppe partagée :

```json
{
  "ok": true,
  "capability": "image.generate",
  "transport": "local",
  "provider": "openai",
  "model": "gpt-image-1",
  "attempts": [],
  "outputs": []
}
```

Les champs de niveau supérieur sont stables :

- `ok`
- `capability`
- `transport`
- `provider`
- `model`
- `attempts`
- `outputs`
- `error`

## Notes

- `model run` réutilise le runtime d'agent afin que les remplacements de fournisseur/modèle se comportent comme l'exécution d'agent normale.
- `tts status` par défaut en passerelle car il reflète l'état TTS géré par la passerelle.
