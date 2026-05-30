---
summary: "Utilisez l'ID de fournisseur Qwen Portal avec OpenClaw"
read_when:
  - You want to configure the qwen-oauth provider id
  - You previously used Qwen Portal OAuth credentials
  - You need the Qwen Portal endpoint or migration guidance
title: "Qwen OAuth / Portal"
---

`qwen-oauth` est l'ID de fournisseur Qwen Portal. Il cible le point de terminaison Qwen Portal
et maintient les anciennes configurations Qwen OAuth / portal adressables via un
ID de fournisseur distinct.

Utilisez ce fournisseur lorsque vous avez spécifiquement un jeton Qwen Portal actuel pour
`https://portal.qwen.ai/v1`, ou lorsque vous migrez une ancienne configuration Qwen Portal /
Qwen CLI et souhaitez conserver ces identifiants séparés du fournisseur
Qwen Cloud canonique. Ce n'est pas le premier choix recommandé pour les nouveaux utilisateurs Qwen.

Pour les nouvelles configurations Qwen Cloud, préférez [Qwen](/fr/providers/qwen) avec le point de terminaison
ModelStudio Standard sauf si vous avez spécifiquement un jeton Qwen Portal actuel.

## Configuration

Fournissez votre jeton portal lors de l'intégration :

```bash
openclaw onboard --auth-choice qwen-oauth
```

Ou définissez :

```bash
export QWEN_API_KEY="<your-qwen-portal-token>" # pragma: allowlist secret
```

## Valeurs par défaut

- Fournisseur : `qwen-oauth`
- Alias : `qwen-portal`, `qwen-cli`
- URL de base : `https://portal.qwen.ai/v1`
- Variable d'environnement : `QWEN_API_KEY`
- Style API : Compatible OpenAI
- Modèle par défaut : `qwen-oauth/qwen3.5-plus`

## Différences avec Qwen

OpenClaw dispose de deux ID de fournisseur orientés Qwen :

| Fournisseur  | Famille de points de terminaison                         | Idéal pour                                                                                      |
| ------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `qwen`       | Points de terminaison Qwen Cloud / Alibaba DashScope et Coding Plan | Nouvelles configurations de clé API, Standard à l'usage, Coding Plan, fonctionnalités multimodales DashScope |
| `qwen-oauth` | Point de terminaison Qwen Portal à `portal.qwen.ai/v1`   | Jetons Qwen Portal existants et configurations héritées Qwen OAuth / CLI                        |

Les deux fournisseurs utilisent des formes de requête compatibles OpenAI, mais ce sont des
surfaces d'authentification distinctes. Un jeton stocké pour `qwen-oauth` ne doit pas être traité comme une
clé DashScope ou ModelStudio, et une nouvelle clé DashScope doit utiliser le fournisseur
`qwen` canonique à la place.

## Quand choisir Qwen OAuth / Portal

- Vous avez déjà un jeton Qwen Portal fonctionnel.
- Vous préservez un flux de travail Qwen OAuth ou Qwen CLI hérité tout en passant au
  modèle de fournisseur d'OpenClaw.
- Vous devez tester la compatibilité avec le point de terminaison Qwen Portal spécifiquement.

Choisissez [Qwen](/fr/providers/qwen) pour une nouvelle configuration, des choix de points de terminaison plus larges, ModelStudio
Standard, Coding Plan et le catalogue Qwen complet fourni.

## Modèles

Le catalogue fourni initialise la valeur par défaut de Qwen Portal :

- `qwen-oauth/qwen3.5-plus`

La disponibilité dépend du compte Qwen Portal actuel et du jeton. Si votre
compte utilise des clés API ModelStudio / DashScope à la place, configurez le fournisseur
`qwen` canonique :

```bash
openclaw onboard --auth-choice qwen-standard-api-key
openclaw models set qwen/qwen3-coder-plus
```

## Migration

Les anciens profils OAuth Qwen Portal peuvent ne pas être actualisables. Si un profil portal
cesse de fonctionner, réauthentifiez-vous avec un jeton actuel ou basculez vers le fournisseur Qwen Standard :

```bash
openclaw onboard --auth-choice qwen-standard-api-key
```

ModelStudio global Standard utilise :

```text
https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

## Dépannage

- Échecs d'actualisation OAuth Portal : les anciens profils OAuth Qwen Portal peuvent ne pas être
  actualisables. Réexécutez l'intégration avec un jeton actuel.
- Erreurs de point de terminaison incorrect : confirmez que la référence du modèle commence par `qwen-oauth/` lors de
  l'utilisation d'un jeton portal. Utilisez les références `qwen/` uniquement pour le fournisseur Qwen canonique.
- Confusion `QWEN_API_KEY` : les deux pages Qwen mentionnent cette variable d'environnement, mais l'intégration
  stocke les identifiants sous l'ID de fournisseur sélectionné. Préférez l'intégration lorsque vous
  gardez à la fois `qwen` et `qwen-oauth` disponibles sur la même machine.

## Connexes

- [Qwen](/fr/providers/qwen)
- [Alibaba Model Studio](/fr/providers/alibaba)
- [Fournisseurs de modèles](/fr/concepts/model-providers)
- [Tous les fournisseurs](/fr/providers/index)
