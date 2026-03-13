---
read_when:
  - Vous souhaitez utiliser le modèle MiniMax dans OpenClaw
  - Vous avez besoin d'un guide de configuration MiniMax
summary: Utiliser MiniMax M2.1 dans OpenClaw
title: MiniMax
x-i18n:
  generated_at: "2026-02-03T10:08:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 861e1ddc3c24be88f716bfb72d6015d62875a9087f8e89ea4ba3a35f548c7fae
  source_path: providers/minimax.md
  workflow: 15
---

# MiniMax

MiniMax est une entreprise d'IA qui construit la famille de modèles **M2/M2.1**. La version actuelle orientée vers la programmation est **MiniMax M2.1** (23 décembre 2025), conçue pour les tâches complexes du monde réel.

Source : [Notes de version MiniMax M2.1](https://www.minimax.io/news/minimax-m21)

## Aperçu du modèle (M2.1)

MiniMax met l'accent sur les améliorations suivantes de M2.1 :

- Capacités de **programmation multilingue** plus fortes (Rust, Java, Go, C++, Kotlin, Objective-C, TS/JS).
- Meilleure **développement Web/applications** et qualité de sortie esthétique (y compris mobile natif).
- Traitement amélioré des **instructions composées**, adapté aux flux de travail de style bureautique, basé sur la pensée entrelacée et l'exécution de contraintes intégrées.
- **Réponses plus concises**, utilisation de tokens inférieure et cycles d'itération plus rapides.
- Compatibilité plus forte avec les **frameworks d'outils/agents** et gestion du contexte (Claude Code, Droid/Factory AI, Cline, Kilo Code, Roo Code, BlackBox).
- Sortie de **conversation et rédaction technique** de meilleure qualité.

## MiniMax M2.1 vs MiniMax M2.1 Lightning

- **Vitesse :** Lightning est la variante « rapide » dans le document de tarification de MiniMax.
- **Coût :** La tarification affiche le même coût d'entrée, mais Lightning a un coût de sortie plus élevé.
- **Routage du plan de programmation :** Le backend Lightning ne peut pas être utilisé directement dans le plan de programmation MiniMax. MiniMax achemine automatiquement la plupart des demandes vers Lightning, mais revient au backend M2.1 régulier pendant les pics de trafic.

## Choisir votre méthode de configuration

### MiniMax OAuth (Plan de programmation) — Recommandé

**Pour :** Configuration rapide du plan de programmation MiniMax via OAuth sans clé API.

Activez le plugin OAuth intégré et authentifiez-vous :

```bash
openclaw plugins enable minimax-portal-auth  # Ignorer si déjà chargé
openclaw gateway restart  # Redémarrer si Gateway est déjà en cours d'exécution
openclaw onboard --auth-choice minimax-portal
```

Vous serez invité à choisir un endpoint :

- **Global** - Utilisateurs internationaux (`api.minimax.io`)
- **CN** - Utilisateurs en Chine (`api.minimaxi.com`)

Voir [README du plugin MiniMax OAuth](https://github.com/openclaw/openclaw/tree/main/extensions/minimax-portal-auth) pour plus de détails.

### MiniMax M2.1 (Clé API)

**Pour :** MiniMax hébergé utilisant une API compatible Anthropic.

Configurez via CLI :

- Exécutez `openclaw configure`
- Sélectionnez **Model/auth**
- Sélectionnez **MiniMax M2.1**

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "minimax/MiniMax-M2.1" } } },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

### MiniMax M2.1 comme secours (Opus comme principal)

**Pour :** Garder Opus 4.5 comme modèle principal, basculer vers MiniMax M2.1 en cas de défaillance.

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-5": { alias: "opus" },
        "minimax/MiniMax-M2.1": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-5",
        fallbacks: ["minimax/MiniMax-M2.1"],
      },
    },
  },
}
```

### Optionnel : Exécution locale via LM Studio (Manuel)

**Pour :** Inférence locale avec LM Studio.
Nous avons observé d'excellents résultats lors de l'exécution de MiniMax M2.1 avec le serveur local de LM Studio sur du matériel puissant (par exemple, ordinateur de bureau/serveur).

Configurez manuellement via `openclaw.json` :

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: { "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Configuration via `openclaw configure`

Utilisez l'assistant de configuration interactif pour configurer MiniMax sans éditer JSON :

1. Exécutez `openclaw configure`.
2. Sélectionnez **Model/auth**.
3. Sélectionnez **MiniMax M2.1**.
4. Sélectionnez votre modèle par défaut lorsque vous y êtes invité.

## Options de configuration

- `models.providers.minimax.baseUrl` : Recommandé `https://api.minimax.io/anthropic` (compatible Anthropic) ; `https://api.minimax.io/v1` optionnel pour les charges compatibles OpenAI.
- `models.providers.minimax.api` : Recommandé `anthropic-messages` ; `openai-completions` optionnel pour les charges compatibles OpenAI.
- `models.providers.minimax.apiKey` : Clé API MiniMax (`MINIMAX_API_KEY`).
- `models.providers.minimax.models` : Définissez `id`, `name`, `reasoning`, `contextWindow`, `maxTokens`, `cost`.
- `agents.defaults.models` : Définissez des alias pour les modèles que vous souhaitez dans la liste blanche.
- `models.mode` : Gardez `merge` si vous souhaitez ajouter MiniMax avec les modèles intégrés.

## Remarques

- Le format de référence du modèle est `minimax/<model>`.
- API d'utilisation du plan de programmation : `https://api.minimaxi.com/v1/api/openplatform/coding_plan/remains` (nécessite une clé de plan de programmation).
- Pour un suivi précis des coûts, mettez à jour les valeurs de tarification dans `models.json`.
- Lien de recommandation du plan de programmation MiniMax (10 % de réduction) : https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link
- Voir [/concepts/model-providers](/concepts/model-providers) pour les règles des fournisseurs.
- Utilisez `openclaw models list` et `openclaw models set minimax/MiniMax-M2.1` pour basculer les modèles.

## Dépannage

### "Unknown model: minimax/MiniMax-M2.1"

Cela signifie généralement que le **fournisseur MiniMax n'est pas configuré** (pas d'entrée de fournisseur et aucun fichier de configuration d'authentification MiniMax/clé d'environnement trouvé). Le correctif pour cette détection est dans **2026.1.12** (non encore publié au moment de la rédaction). Solutions :

- Mettez à niveau vers **2026.1.12** (ou exécutez depuis la branche `main` du code source), puis redémarrez Gateway.
- Exécutez `openclaw configure` et sélectionnez **MiniMax M2.1**, ou
- Ajoutez manuellement le bloc `models.providers.minimax`, ou
- Définissez `MINIMAX_API_KEY` (ou le fichier de configuration d'authentification MiniMax) pour injecter le fournisseur.

Assurez-vous que l'id du modèle est **sensible à la casse** :

- `minimax/MiniMax-M2.1`
- `minimax/MiniMax-M2.1-lightning`

Puis revérifiez :

```bash
openclaw models list
```
