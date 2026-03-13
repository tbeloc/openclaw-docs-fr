---
last_updated: "2026-01-19"
owner: openclaw
status: draft
summary: Plan : ajouter le point de terminaison OpenResponses /v1/responses et déprécier proprement les complétions de chat
title: Plan de la passerelle OpenResponses
x-i18n:
  generated_at: "2026-02-03T07:47:33Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 71a22c48397507d1648b40766a3153e420c54f2a2d5186d07e51eb3d12e4636a
  source_path: experiments/plans/openresponses-gateway.md
  workflow: 15
---

# Plan d'intégration de la passerelle OpenResponses

## Contexte

La passerelle OpenClaw expose actuellement un point de terminaison Chat Completions minimal compatible avec OpenAI sur `/v1/chat/completions` (voir [OpenAI Chat Completions](/gateway/openai-http-api)).

Open Responses est une norme de raisonnement ouvert basée sur l'API Responses d'OpenAI. Elle est conçue pour les flux de travail d'agents, utilisant des entrées basées sur des éléments et des événements de flux sémantique. La spécification OpenResponses définit `/v1/responses`, et non `/v1/chat/completions`.

## Objectifs

- Ajouter un point de terminaison `/v1/responses` qui respecte la sémantique d'OpenResponses.
- Conserver Chat Completions comme couche de compatibilité, facile à désactiver et à supprimer à terme.
- Utiliser des schémas isolés et réutilisables pour normaliser la validation et l'analyse.

## Non-objectifs

- Implémenter complètement les fonctionnalités d'OpenResponses au cours de la première phase (images, fichiers, outils hébergés).
- Remplacer la logique d'exécution d'agents interne ou l'orchestration d'outils.
- Modifier le comportement existant de `/v1/chat/completions` au cours de la première phase.

## Résumé de la recherche

Sources : OpenAPI OpenResponses, site de spécification OpenResponses et article de blog Hugging Face.

Points clés extraits :

- `POST /v1/responses` accepte les champs `CreateResponseBody` tels que `model`, `input` (chaîne ou `ItemParam[]`), `instructions`, `tools`, `tool_choice`, `stream`, `max_output_tokens` et `max_tool_calls`.
- `ItemParam` est une union discriminée des types suivants :
  - Éléments `message` avec rôles `system`, `developer`, `user`, `assistant`
  - `function_call` et `function_call_output`
  - `reasoning`
  - `item_reference`
- Une réponse réussie retourne une `ResponseResource` avec `object: "response"`, `status` et éléments `output`.
- La diffusion en continu utilise des événements sémantiques tels que :
  - `response.created`, `response.in_progress`, `response.completed`, `response.failed`
  - `response.output_item.added`, `response.output_item.done`
  - `response.content_part.added`, `response.content_part.done`
  - `response.output_text.delta`, `response.output_text.done`
- Les exigences de spécification :
  - `Content-Type: text/event-stream`
  - `event:` doit correspondre au champ JSON `type`
  - L'événement de terminaison doit être le littéral `[DONE]`
- Les éléments de raisonnement peuvent exposer `content`, `encrypted_content` et `summary`.
- L'exemple HF inclut `OpenResponses-Version: latest` dans la requête (en-tête optionnel).

## Architecture proposée

- Ajouter `src/gateway/open-responses.schema.ts`, contenant uniquement les schémas Zod (pas d'importations de passerelle).
- Ajouter `src/gateway/openresponses-http.ts` (ou `open-responses-http.ts`) pour `/v1/responses`.
- Conserver `src/gateway/openai-http.ts` inchangé, comme adaptateur de compatibilité hérité.
- Ajouter la configuration `gateway.http.endpoints.responses.enabled` (par défaut `false`).
- Garder `gateway.http.endpoints.chatCompletions.enabled` indépendant ; permettre à chaque point de terminaison d'être basculé séparément.
- Émettre un avertissement au démarrage lorsque Chat Completions est activé pour indiquer son statut hérité.

## Chemin de dépréciation de Chat Completions

- Maintenir des limites de module strictes : pas de partage de types de schéma entre responses et chat completions.
- Rendre Chat Completions optionnel via la configuration, de sorte qu'il puisse être désactivé sans modification du code.
- Une fois que `/v1/responses` est stable, mettre à jour la documentation pour marquer Chat Completions comme hérité.
- Étape future optionnelle : mapper les requêtes Chat Completions au processeur Responses pour une suppression plus simple.

## Sous-ensemble pris en charge en première phase

- Accepter `input` comme chaîne ou `ItemParam[]` avec rôles de message et `function_call_output`.
- Extraire les messages système et développeur dans `extraSystemPrompt`.
- Utiliser le dernier message `user` ou `function_call_output` comme message actuel pour l'exécution de l'agent.
- Rejeter avec `invalid_request_error` pour les parties de contenu non prises en charge (images/fichiers).
- Retourner un seul message d'assistant avec contenu `output_text`.
- Retourner `usage` avec des valeurs nulles jusqu'à l'intégration du comptage de tokens.

## Stratégie de validation (sans SDK)

- Implémenter les schémas Zod pour le sous-ensemble pris en charge :
  - `CreateResponseBody`
  - `ItemParam` + union de parties de contenu de message
  - `ResponseResource`
  - Formes d'événements de diffusion en continu utilisées par la passerelle
- Conserver les schémas dans un module isolé unique pour éviter la dérive et permettre la génération de code future.

## Implémentation de la diffusion en continu (première phase)

- Lignes SSE avec `event:` et `data:`.
- Séquence requise (minimum viable) :
  - `response.created`
  - `response.output_item.added`
  - `response.content_part.added`
  - `response.output_text.delta` (répété selon les besoins)
  - `response.output_text.done`
  - `response.content_part.done`
  - `response.completed`
  - `[DONE]`

## Plan de test et de validation

- Ajouter une couverture de bout en bout pour `/v1/responses` :
  - Authentification requise
  - Forme de réponse non diffusée
  - Ordre des événements de diffusion en continu et `[DONE]`
  - Routage de session avec en-têtes et `user`
- Conserver `src/gateway/openai-http.e2e.test.ts` inchangé.
- Manuel : curl `/v1/responses` avec `stream: true` et vérifier l'ordre des événements et le `[DONE]` de terminaison.

## Mises à jour de la documentation (ultérieures)

- Ajouter une nouvelle page de documentation pour l'utilisation et les exemples de `/v1/responses`.
- Mettre à jour `/gateway/openai-http-api` avec une note de statut hérité et un pointeur vers `/v1/responses`.
