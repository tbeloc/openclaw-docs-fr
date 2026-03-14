---
summary: "Utiliser MiniMax M2.5 dans OpenClaw"
read_when:
  - You want MiniMax models in OpenClaw
  - You need MiniMax setup guidance
title: "MiniMax"
---

# MiniMax

MiniMax est une entreprise d'IA qui développe la famille de modèles **M2/M2.5**. La version actuelle
axée sur le codage est **MiniMax M2.5** (23 décembre 2025), conçue pour
les tâches complexes du monde réel.

Source : [Note de version MiniMax M2.5](https://www.minimax.io/news/minimax-m25)

## Aperçu du modèle (M2.5)

MiniMax met en avant ces améliorations dans M2.5 :

- **Codage multilingue** plus robuste (Rust, Java, Go, C++, Kotlin, Objective-C, TS/JS).
- Meilleur **développement web/app** et qualité de sortie esthétique (y compris mobile natif).
- Gestion améliorée des **instructions composites** pour les flux de travail de style bureautique, s'appuyant
  sur la pensée entrelacée et l'exécution des contraintes intégrées.
- **Réponses plus concises** avec une utilisation de tokens réduite et des boucles d'itération plus rapides.
- Compatibilité plus robuste avec les **frameworks d'outils/agents** et gestion du contexte (Claude Code,
  Droid/Factory AI, Cline, Kilo Code, Roo Code, BlackBox).
- Sorties de **dialogue et d'écriture technique** de meilleure qualité.

## MiniMax M2.5 vs MiniMax M2.5 Highspeed

- **Vitesse :** `MiniMax-M2.5-highspeed` est le niveau rapide officiel dans la documentation MiniMax.
- **Coût :** La tarification MiniMax liste le même coût d'entrée et un coût de sortie plus élevé pour highspeed.
- **IDs de modèle actuels :** utilisez `MiniMax-M2.5` ou `MiniMax-M2.5-highspeed`.

## Choisir une configuration

### MiniMax OAuth (Plan Coding) — recommandé

**Idéal pour :** configuration rapide avec MiniMax Coding Plan via OAuth, aucune clé API requise.

Activez le plugin OAuth fourni et authentifiez-vous :

```bash
openclaw plugins enable minimax-portal-auth  # skip if already loaded.
openclaw gateway restart  # restart if gateway is already running
openclaw onboard --auth-choice minimax-portal
```

Vous serez invité à sélectionner un point de terminaison :

- **Global** - Utilisateurs internationaux (`api.minimax.io`)
- **CN** - Utilisateurs en Chine (`api.minimaxi.com`)

Voir [README du plugin MiniMax OAuth](https://github.com/openclaw/openclaw/tree/main/extensions/minimax-portal-auth) pour plus de détails.

### MiniMax M2.5 (clé API)

**Idéal pour :** MiniMax hébergé avec API compatible Anthropic.

Configurez via CLI :

- Exécutez `openclaw configure`
- Sélectionnez **Model/auth**
- Choisissez **MiniMax M2.5**

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "minimax/MiniMax-M2.5" } } },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: true,
            input: ["text"],
            cost: { input: 0.3, output: 1.2, cacheRead: 0.03, cacheWrite: 0.12 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
          {
            id: "MiniMax-M2.5-highspeed",
            name: "MiniMax M2.5 Highspeed",
            reasoning: true,
            input: ["text"],
            cost: { input: 0.3, output: 1.2, cacheRead: 0.03, cacheWrite: 0.12 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

### MiniMax M2.5 comme secours (exemple)

**Idéal pour :** garder votre modèle de dernière génération le plus puissant comme principal, basculer vers MiniMax M2.5.
L'exemple ci-dessous utilise Opus comme principal concret ; remplacez par votre modèle principal de dernière génération préféré.

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "primary" },
        "minimax/MiniMax-M2.5": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.5"],
      },
    },
  },
}
```

### Optionnel : Local via LM Studio (manuel)

**Idéal pour :** inférence locale avec LM Studio.
Nous avons observé d'excellents résultats avec MiniMax M2.5 sur du matériel puissant (par exemple un
ordinateur de bureau/serveur) en utilisant le serveur local de LM Studio.

Configurez manuellement via `openclaw.json` :

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.5-gs32" },
      models: { "lmstudio/minimax-m2.5-gs32": { alias: "Minimax" } },
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
            id: "minimax-m2.5-gs32",
            name: "MiniMax M2.5 GS32",
            reasoning: true,
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

## Configurer via `openclaw configure`

Utilisez l'assistant de configuration interactif pour configurer MiniMax sans éditer JSON :

1. Exécutez `openclaw configure`.
2. Sélectionnez **Model/auth**.
3. Choisissez **MiniMax M2.5**.
4. Sélectionnez votre modèle par défaut lorsque vous y êtes invité.

## Options de configuration

- `models.providers.minimax.baseUrl` : préférez `https://api.minimax.io/anthropic` (compatible Anthropic) ; `https://api.minimax.io/v1` est optionnel pour les charges utiles compatibles OpenAI.
- `models.providers.minimax.api` : préférez `anthropic-messages` ; `openai-completions` est optionnel pour les charges utiles compatibles OpenAI.
- `models.providers.minimax.apiKey` : clé API MiniMax (`MINIMAX_API_KEY`).
- `models.providers.minimax.models` : définissez `id`, `name`, `reasoning`, `contextWindow`, `maxTokens`, `cost`.
- `agents.defaults.models` : alias des modèles que vous souhaitez dans la liste d'autorisation.
- `models.mode` : gardez `merge` si vous souhaitez ajouter MiniMax aux modèles intégrés.

## Notes

- Les références de modèle sont `minimax/<model>`.
- IDs de modèle recommandés : `MiniMax-M2.5` et `MiniMax-M2.5-highspeed`.
- API d'utilisation du plan Coding : `https://api.minimaxi.com/v1/api/openplatform/coding_plan/remains` (nécessite une clé de plan coding).
- Mettez à jour les valeurs de tarification dans `models.json` si vous avez besoin d'un suivi des coûts exact.
- Lien de parrainage pour MiniMax Coding Plan (10% de réduction) : [https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link](https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link)
- Voir [/concepts/model-providers](/concepts/model-providers) pour les règles des fournisseurs.
- Utilisez `openclaw models list` et `openclaw models set minimax/MiniMax-M2.5` pour basculer.

## Dépannage

### "Unknown model: minimax/MiniMax-M2.5"

Cela signifie généralement que le **fournisseur MiniMax n'est pas configuré** (aucune entrée de fournisseur
et aucune clé d'authentification/env MiniMax trouvée). Un correctif pour cette détection est dans
**2026.1.12** (non publié au moment de la rédaction). Corrigez en :

- Mettant à niveau vers **2026.1.12** (ou en exécutant depuis la source `main`), puis en redémarrant la passerelle.
- Exécutant `openclaw configure` et en sélectionnant **MiniMax M2.5**, ou
- Ajoutant manuellement le bloc `models.providers.minimax`, ou
- Définissant `MINIMAX_API_KEY` (ou un profil d'authentification MiniMax) pour que le fournisseur puisse être injecté.

Assurez-vous que l'ID du modèle est **sensible à la casse** :

- `minimax/MiniMax-M2.5`
- `minimax/MiniMax-M2.5-highspeed`

Puis revérifiez avec :

```bash
openclaw models list
```
