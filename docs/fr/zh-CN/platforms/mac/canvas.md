---
read_when:
  - 实现 macOS Canvas 面板
  - 为可视化工作区添加智能体控制
  - 调试 WKWebView canvas 加载
summary: 通过 WKWebView + 自定义 URL 方案嵌入的智能体控制 Canvas 面板
title: Canvas
x-i18n:
  generated_at: "2026-02-03T07:52:39Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e39caa21542e839d9f59ad0bf7ecefb379225ed7e8f00cd59131d188f193bec6
  source_path: platforms/mac/canvas.md
  workflow: 15
---

# Canvas (application macOS)

L'application macOS utilise `WKWebView` pour intégrer un **panneau Canvas** contrôlé par un agent. Il s'agit d'un espace de travail de visualisation léger pour HTML/CSS/JS, A2UI et les petites interfaces interactives.

## Emplacement de stockage de Canvas

L'état de Canvas est stocké dans Application Support :

- `~/Library/Application Support/OpenClaw/canvas/<session>/...`

Le panneau Canvas fournit ces fichiers via un **schéma d'URL personnalisé** :

- `openclaw-canvas://<session>/<path>`

Exemples :

- `openclaw-canvas://main/` → `<canvasRoot>/main/index.html`
- `openclaw-canvas://main/assets/app.css` → `<canvasRoot>/main/assets/app.css`
- `openclaw-canvas://main/widgets/todo/` → `<canvasRoot>/main/widgets/todo/index.html`

S'il n'y a pas de `index.html` à la racine, l'application affiche une **page d'échafaudage intégrée**.

## Comportement du panneau

- Panneau sans bordure, redimensionnable, ancré près de la barre de menus (ou du curseur de la souris).
- Mémorise la taille/position pour chaque session.
- Recharge automatiquement lorsque les fichiers canvas locaux changent.
- Un seul panneau Canvas affiché à la fois (basculez entre les sessions selon les besoins).

Canvas peut être désactivé depuis Paramètres → **Autoriser Canvas**. Lorsqu'il est désactivé, les commandes de nœud canvas retournent `CANVAS_DISABLED`.

## Interface API de l'agent

Canvas est exposé via la **passerelle WebSocket Gateway**, permettant aux agents de :

- Afficher/masquer le panneau
- Naviguer vers un chemin ou une URL
- Exécuter du JavaScript
- Capturer des images d'instantané

Exemples CLI :

```bash
openclaw nodes canvas present --node <id>
openclaw nodes canvas navigate --node <id> --url "/"
openclaw nodes canvas eval --node <id> --js "document.title"
openclaw nodes canvas snapshot --node <id>
```

Remarques :

- `canvas.navigate` accepte les **chemins canvas locaux**, les URL `http(s)` et les URL `file://`.
- Si vous passez `"/"`, Canvas affiche l'échafaudage local ou `index.html`.

## A2UI dans Canvas

A2UI est hébergé par l'hôte canvas Gateway et rendu dans le panneau Canvas.
Lorsque Gateway diffuse l'hôte Canvas, l'application macOS navigue automatiquement vers la page d'hôte A2UI à la première ouverture.

URL d'hôte A2UI par défaut :

```
http://<gateway-host>:18793/__openclaw__/a2ui/
```

### Commandes A2UI (v0.8)

Canvas accepte actuellement les messages serveur→client **A2UI v0.8** :

- `beginRendering`
- `surfaceUpdate`
- `dataModelUpdate`
- `deleteSurface`

`createSurface` (v0.9) n'est pas pris en charge.

Exemple CLI :

```bash
cat > /tmp/a2ui-v0.8.jsonl <<'EOFA2'
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":{"explicitList":["title","content"]}}}},{"id":"title","component":{"Text":{"text":{"literalString":"Canvas (A2UI v0.8)"},"usageHint":"h1"}}},{"id":"content","component":{"Text":{"text":{"literalString":"If you can read this, A2UI push works."},"usageHint":"body"}}}]}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
EOFA2

openclaw nodes canvas a2ui push --jsonl /tmp/a2ui-v0.8.jsonl --node <id>
```

Test rapide :

```bash
openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"
```

## Déclencher des exécutions d'agent à partir de Canvas

Canvas peut déclencher de nouvelles exécutions d'agent via des liens profonds :

- `openclaw://agent?...`

Exemple (en JS) :

```js
window.location.href = "openclaw://agent?message=Review%20this%20design";
```

L'application demande une confirmation à moins qu'une clé valide ne soit fournie.

## Considérations de sécurité

- Le schéma Canvas bloque la traversée de répertoires ; les fichiers doivent se trouver sous la racine de la session.
- Le contenu Canvas local utilise un schéma personnalisé (pas besoin de serveur loopback).
- Les URL externes `http(s)` ne sont autorisées que lors d'une navigation explicite.
