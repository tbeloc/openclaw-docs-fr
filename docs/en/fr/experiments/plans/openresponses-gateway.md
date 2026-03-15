---
summary: "Plan: Add OpenResponses /v1/responses endpoint and deprecate chat completions cleanly"
read_when:
  - Designing or implementing `/v1/responses` gateway support
  - Planning migration from Chat Completions compatibility
owner: "openclaw"
status: "draft"
last_updated: "2026-01-19"
title: "OpenResponses Gateway Plan"
---

# Plan d'intégration de la passerelle OpenResponses

## Contexte

La passerelle OpenClaw expose actuellement un point de terminaison Chat Completions minimal compatible avec OpenAI à
`/v1/chat/completions` (voir [OpenAI Chat Completions](/gateway/openai-http-api)).

Open Responses est une norme d'inférence ouverte basée sur l'API OpenAI Responses. Elle est conçue
pour les flux de travail d'agent et utilise des entrées basées sur des éléments ainsi que des événements de streaming sémantique. La spécification OpenResponses définit `/v1/responses`, et non `/v1/chat/completions`.

## Objectifs

- Ajouter un point de terminaison `/v1/responses` qui adhère à la sémantique OpenResponses.
- Conserver Chat Completions comme couche de compatibilité facile à désactiver et à supprimer éventuellement.
- Standardiser la validation et l'analyse avec des schémas isolés et réutilisables.

## Non-objectifs

- Parité complète des fonctionnalités OpenResponses au premier passage (images, fichiers, outils hébergés).
- Remplacer la logique d'exécution d'agent interne ou l'orchestration d'outils.
- Modifier le comportement existant de `/v1/chat/completions` pendant la première phase.

## Résumé de la recherche

Sources : OpenResponses OpenAPI, site de spécification OpenResponses et article de blog Hugging Face.

Points clés extraits :

- `POST /v1/responses` accepte les champs `CreateResponseBody` tels que `model`, `input` (chaîne ou
  `ItemParam[]`), `instructions`, `tools`, `tool_choice`, `stream`, `max_output_tokens` et
  `max_tool_calls`.
- `ItemParam` est une union discriminée de :
  - éléments `message` avec les rôles `system`, `developer`, `user`, `assistant`
  - `function_call` et `function_call_output`
  - `reasoning`
  - `item_reference`
- Les réponses réussies retournent une `ResponseResource` avec `object: "response"`, `status` et
  éléments `output`.
- Le streaming utilise des événements sémantiques tels que :
  - `response.created`, `response.in_progress`, `response.completed`, `response.failed`
  - `response.output_item.added`, `response.output_item.done`
  - `response.content_part.added`, `response.content_part.done`
  - `response.output_text.delta`, `response.output_text.done`
- La spécification exige :
  - `Content-Type: text/event-stream`
  - `event:` doit correspondre au champ JSON `type`
  - l'événement terminal doit être littéralement `[DONE]`
- Les éléments de raisonnement peuvent exposer `content`, `encrypted_content` et `summary`.
- Les exemples HF incluent `OpenResponses-Version: latest` dans les requêtes (en-tête optionnel).

## Architecture proposée

- Ajouter `src/gateway/open-responses.schema.ts` contenant uniquement les schémas Zod (pas d'importations de passerelle).
- Ajouter `src/gateway/openresponses-http.ts` (ou `open-responses-http.ts`) pour `/v1/responses`.
- Conserver `src/gateway/openai-http.ts` intact comme adaptateur de compatibilité hérité.
- Ajouter la configuration `gateway.http.endpoints.responses.enabled` (par défaut `false`).
- Conserver `gateway.http.endpoints.chatCompletions.enabled` indépendant ; permettre aux deux points de terminaison d'être
  basculés séparément.
- Émettre un avertissement au démarrage lorsque Chat Completions est activé pour signaler le statut hérité.

## Chemin de dépréciation pour Chat Completions

- Maintenir des limites de module strictes : aucun type de schéma partagé entre les réponses et les complétions de chat.
- Rendre Chat Completions optionnel par configuration afin qu'il puisse être désactivé sans modifications de code.
- Mettre à jour la documentation pour étiqueter Chat Completions comme hérité une fois que `/v1/responses` est stable.
- Étape future optionnelle : mapper les requêtes Chat Completions au gestionnaire Responses pour un chemin de suppression plus simple.

## Sous-ensemble de support de la phase 1

- Accepter `input` comme chaîne ou `ItemParam[]` avec les rôles de message et `function_call_output`.
- Extraire les messages système et développeur dans `extraSystemPrompt`.
- Utiliser le message `user` ou `function_call_output` le plus récent comme message actuel pour les exécutions d'agent.
- Rejeter les parties de contenu non prises en charge (image/fichier) avec `invalid_request_error`.
- Retourner un seul message d'assistant avec le contenu `output_text`.
- Retourner `usage` avec des valeurs mises à zéro jusqu'à ce que la comptabilité des jetons soit câblée.

## Stratégie de validation (pas de SDK)

- Implémenter les schémas Zod pour le sous-ensemble pris en charge de :
  - `CreateResponseBody`
  - `ItemParam` + unions de parties de contenu de message
  - `ResponseResource`
  - Formes d'événements de streaming utilisées par la passerelle
- Conserver les schémas dans un module unique et isolé pour éviter la dérive et permettre la future génération de code.

## Implémentation du streaming (phase 1)

- Lignes SSE avec à la fois `event:` et `data:`.
- Séquence requise (minimum viable) :
  - `response.created`
  - `response.output_item.added`
  - `response.content_part.added`
  - `response.output_text.delta` (répéter au besoin)
  - `response.output_text.done`
  - `response.content_part.done`
  - `response.completed`
  - `[DONE]`

## Plan de tests et de vérification

- Ajouter une couverture e2e pour `/v1/responses` :
  - Authentification requise
  - Forme de réponse sans streaming
  - Ordre des événements de streaming et `[DONE]`
  - Routage de session avec en-têtes et `user`
- Conserver `src/gateway/openai-http.test.ts` inchangé.
- Manuel : curl vers `/v1/responses` avec `stream: true` et vérifier l'ordre des événements et le terminal
  `[DONE]`.

## Mises à jour de la documentation (suivi)

- Ajouter une nouvelle page de documentation pour l'utilisation et les exemples de `/v1/responses`.
- Mettre à jour `/gateway/openai-http-api` avec une note hérité et un pointeur vers `/v1/responses`.
