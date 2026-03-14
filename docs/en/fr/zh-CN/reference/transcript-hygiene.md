---
read_when:
  - Vous déboguez des problèmes de rejet de requêtes de fournisseur liés à la structure des enregistrements de conversation
  - Vous modifiez la logique de nettoyage des enregistrements de conversation ou de correction des appels d'outils
  - Vous enquêtez sur des problèmes de non-concordance des identifiants d'appels d'outils entre fournisseurs
summary: Référence : Règles de nettoyage et de correction des enregistrements de conversation spécifiques aux fournisseurs
title: Nettoyage des enregistrements de conversation
x-i18n:
  generated_at: "2026-02-01T21:38:16Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 6ce62fad0b07c4d8575c9cdb1c8c2663695ef2d4221cf4a0964fce03461523af
  source_path: reference/transcript-hygiene.md
  workflow: 15
---

# Nettoyage des enregistrements de conversation (Corrections spécifiques aux fournisseurs)

Ce document décrit les **corrections spécifiques aux fournisseurs** appliquées aux enregistrements de conversation avant l'exécution (lors de la construction du contexte du modèle). Il s'agit d'ajustements **en mémoire** pour satisfaire les exigences strictes des fournisseurs. Ils **ne réécrivent pas** les enregistrements de conversation JSONL stockés sur le disque.

La couverture inclut :

- Nettoyage des identifiants d'appels d'outils
- Correction de l'appairage des résultats d'outils
- Validation / tri des tours
- Nettoyage des signatures de réflexion
- Nettoyage des charges utiles d'images

Pour plus de détails sur le stockage des enregistrements de conversation, consultez :

- [/reference/session-management-compaction](/reference/session-management-compaction)

---

## Localisation de l'exécution

Toute la logique de nettoyage des enregistrements de conversation est centralisée dans le moteur intégré :

- Sélection de la politique : `src/agents/transcript-policy.ts`
- Application du nettoyage/correction : `sanitizeSessionHistory` dans `src/agents/pi-embedded-runner/google.ts`

La politique décide quelles règles appliquer en fonction de `provider`, `modelApi` et `modelId`.

---

## Règle globale : Nettoyage des images

Les charges utiles d'images sont toujours nettoyées pour éviter les rejets côté fournisseur dus aux limites de taille (mise à l'échelle/récompression des grandes images base64).

Implémentation :

- `sanitizeSessionMessagesImages` dans `src/agents/pi-embedded-helpers/images.ts`
- `sanitizeContentBlocksImages` dans `src/agents/tool-images.ts`

---

## Matrice des fournisseurs (Comportement actuel)

**OpenAI / OpenAI Codex**

- Nettoyage des images uniquement.
- Lors du basculement vers les modèles OpenAI Responses/Codex, suppression des signatures de réflexion orphelines (éléments de réflexion autonomes sans bloc de contenu suivant).
- Pas de nettoyage des identifiants d'appels d'outils.
- Pas de correction de l'appairage des résultats d'outils.
- Pas de validation ou de réorganisation des tours.
- Pas de génération de résultats d'outils synthétiques.
- Pas de suppression des signatures de réflexion.

**Google (Generative AI / Gemini CLI / Antigravity)**

- Nettoyage des identifiants d'appels d'outils : alphanumérique strict.
- Correction de l'appairage des résultats d'outils et résultats d'outils synthétiques.
- Validation des tours (alternance des tours au style Gemini).
- Correction du tri des tours Google (ajout d'un petit message d'amorce utilisateur en avant si l'historique commence par un assistant).
- Antigravity Claude : normalisation des signatures de réflexion ; suppression des blocs de réflexion non signés.

**Anthropic / Minimax (Compatible Anthropic)**

- Correction de l'appairage des résultats d'outils et résultats d'outils synthétiques.
- Validation des tours (fusion des tours utilisateur consécutives pour satisfaire les exigences d'alternance stricte).

**Mistral (Incluant la détection basée sur model-id)**

- Nettoyage des identifiants d'appels d'outils : strict9 (alphanumérique, longueur 9).

**OpenRouter Gemini**

- Nettoyage des signatures de réflexion : suppression des valeurs `thought_signature` non base64 (conservation des base64).

**Tous les autres fournisseurs**

- Nettoyage des images uniquement.

---

## Comportement historique (Avant 2026.1.22)

Avant la version 2026.1.22, OpenClaw appliquait un nettoyage multi-couches des enregistrements de conversation :

- Une **extension de nettoyage des enregistrements de conversation** s'exécutait à chaque construction de contexte, pouvant :
  - Corriger l'appairage utilisation d'outils/résultats.
  - Nettoyer les identifiants d'appels d'outils (incluant un mode non strict conservant `_`/`-`).
- Le moteur exécutait également le nettoyage spécifique aux fournisseurs, causant une duplication du travail.
- Des modifications supplémentaires existaient en dehors de la politique des fournisseurs, incluant :
  - Suppression des balises `<final>` du texte assistant avant la persistance.
  - Suppression des tours d'erreur assistant vides.
  - Troncature du contenu assistant après les appels d'outils.

Cette complexité a causé des problèmes de régression entre fournisseurs (notamment l'appairage `call_id|fc_id` pour `openai-responses`). Le nettoyage de 2026.1.22 a supprimé l'extension, centralisé la logique dans le moteur, et rendu OpenAI **sans modification** au-delà du nettoyage des images.
