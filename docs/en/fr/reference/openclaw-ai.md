---
summary: "Le package npm @openclaw/ai : transports de modèles réutilisables, runtimes isolés et ports de politique d'hôte"
title: "Package @openclaw/ai"
read_when:
  - You want to reuse OpenClaw's model transports in another application
  - You are changing packages/ai or the AI transport host ports
  - You are reviewing what the openclaw release publishes to npm besides the root package
---

`@openclaw/ai` est la forme de bibliothèque publiable de la couche d'exécution
de modèles d'OpenClaw : contrats de messages/outils/flux neutres par rapport au
fournisseur, validation, diagnostics, flux d'événements, un registre de runtime
isolé, et des adaptateurs lazy pour les huit familles d'API intégrées (Anthropic
Messages, OpenAI Completions, OpenAI Responses, Azure OpenAI Responses,
ChatGPT/Codex Responses, Google Generative AI, Google Vertex, Mistral
Conversations).

Il est publié aux côtés du package racine `openclaw` à chaque version, épinglé à
la même version, avec son propre `npm-shrinkwrap.json` pour que son arborescence
de dépendances transitives soit verrouillée au moment de l'installation.
L'installation de `openclaw` installe automatiquement le `@openclaw/ai`
correspondant ; les consommateurs de bibliothèques peuvent en dépendre
directement sans aucun code d'application OpenClaw.

## Démarrage rapide

```js
import { createLlmRuntime } from "@openclaw/ai";
import { registerBuiltInApiProviders } from "@openclaw/ai/providers";

const runtime = createLlmRuntime();
registerBuiltInApiProviders(runtime.registry);

const stream = runtime.streamSimple(model, { messages }, { apiKey });
for await (const event of stream) {
  if (event.type === "text_delta") process.stdout.write(event.delta);
}
const result = await stream.result();
```

Une version exécutable se trouve dans le référentiel à `examples/ai-chat`.

## Contrat de conception

- **Limité à l'instance par défaut.** L'importation du package n'enregistre rien
  globalement. `createApiRegistry()` / `createLlmRuntime()` retournent des
  instances isolées ; `registerBuiltInApiProviders(registry)` opte un registre
  pour les transports intégrés. Les modules SDK du fournisseur se chargent
  paresseusement à la première utilisation.
- **La politique d'hôte est injectée, non regroupée.** La protection de la
  récupération des requêtes (par exemple la politique SSRF), la rédaction des
  secrets du texte de relecture des résultats d'outils, les valeurs par défaut
  strictes des outils OpenAI, et la journalisation des diagnostics sont des
  ports `AiTransportHost` configurés avec `configureAiTransportHost`. Les
  valeurs par défaut de la bibliothèque sont inertes ; OpenClaw installe ses
  implémentations réelles dans sa façade de flux.
- **Une identité de flux d'événements.** `@openclaw/ai/event-stream` est le
  constructeur `EventStream` canonique partagé par le noyau OpenClaw, le
  noyau d'agent, et les consommateurs externes.
- **Les sous-chemins `internal/*` ne sont pas une API.** Ils existent pour
  l'application OpenClaw elle-même et ne portent aucune garantie semver.
- Les identifiants de fournisseur, les identifiants, les catalogues de modèles,
  les tentatives et le basculement restent des préoccupations d'application.
  OpenClaw les superpose autour de ce package ; un consommateur de bibliothèque
  fournit un objet `Model` et des options directement.

## Exports de sous-chemins

| Sous-chemin      | Contenu                                                                        |
| ---------------- | ------------------------------------------------------------------------------ |
| `.`              | Contrats, `createApiRegistry`, `createLlmRuntime`, `configureAiTransportHost` |
| `./providers`    | `registerBuiltInApiProviders`, `resetApiProviders`                             |
| `./types`        | Types de modèle/message/outil/flux                                             |
| `./validation`   | Validation des arguments d'outil                                               |
| `./diagnostics`  | Contrats de diagnostics                                                        |
| `./event-stream` | Implémentation `EventStream` partagée                                          |
| `./internal/*`   | Interne à OpenClaw, aucune garantie semver                                     |
