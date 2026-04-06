---
title: "Alibaba Model Studio"
summary: "Génération vidéo Alibaba Wan dans OpenClaw"
read_when:
  - You want to use Alibaba Wan video generation in OpenClaw
  - You need Model Studio or DashScope API key setup for video generation
---

# Alibaba Model Studio

OpenClaw est livré avec un fournisseur de génération vidéo `alibaba` intégré pour les modèles Wan sur
Alibaba Model Studio / DashScope.

- Fournisseur : `alibaba`
- Authentification préférée : `MODELSTUDIO_API_KEY`
- Également accepté : `DASHSCOPE_API_KEY`, `QWEN_API_KEY`
- API : Génération vidéo asynchrone DashScope / Model Studio

## Démarrage rapide

1. Définissez une clé API :

```bash
openclaw onboard --auth-choice qwen-standard-api-key
```

2. Définissez un modèle vidéo par défaut :

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: {
        primary: "alibaba/wan2.6-t2v",
      },
    },
  },
}
```

## Modèles Wan intégrés

Le fournisseur `alibaba` intégré enregistre actuellement :

- `alibaba/wan2.6-t2v`
- `alibaba/wan2.6-i2v`
- `alibaba/wan2.6-r2v`
- `alibaba/wan2.6-r2v-flash`
- `alibaba/wan2.7-r2v`

## Limites actuelles

- Jusqu'à **1** vidéo de sortie par requête
- Jusqu'à **1** image d'entrée
- Jusqu'à **4** vidéos d'entrée
- Jusqu'à **10 secondes** de durée
- Supporte `size`, `aspectRatio`, `resolution`, `audio` et `watermark`
- Le mode image/vidéo de référence nécessite actuellement des **URL http(s) distantes**

## Relation avec Qwen

Le fournisseur `qwen` intégré utilise également les points de terminaison DashScope hébergés par Alibaba pour
la génération vidéo Wan. Utilisez :

- `qwen/...` lorsque vous voulez la surface du fournisseur Qwen canonique
- `alibaba/...` lorsque vous voulez la surface vidéo Wan directe du fournisseur

## Connexes

- [Video Generation](/fr/tools/video-generation)
- [Qwen](/fr/providers/qwen)
- [Configuration Reference](/fr/gateway/configuration-reference#agent-defaults)
