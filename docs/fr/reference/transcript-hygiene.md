---
summary: "Référence : règles de désinfection et de réparation de transcription spécifiques au fournisseur"
read_when:
  - You are debugging provider request rejections tied to transcript shape
  - You are changing transcript sanitization or tool-call repair logic
  - You are investigating tool-call id mismatches across providers
title: "Transcript Hygiene"
---

# Transcript Hygiene (Provider Fixups)

Ce document décrit les **correctifs spécifiques au fournisseur** appliqués aux transcriptions avant une exécution
(construction du contexte du modèle). Il s'agit d'ajustements **en mémoire** utilisés pour satisfaire les exigences strictes
du fournisseur. Ces étapes d'hygiène **ne réécrivent pas** la transcription JSONL stockée
sur disque ; cependant, une passe de réparation de fichier de session séparé peut réécrire les fichiers JSONL malformés
en supprimant les lignes invalides avant le chargement de la session. Lorsqu'une réparation se produit, le fichier original
est sauvegardé à côté du fichier de session.

La portée comprend :

- Désinfection des identifiants d'appel d'outil
- Validation des entrées d'appel d'outil
- Réparation de l'appairage des résultats d'outil
- Validation / réorganisation des tours
- Nettoyage de la signature de pensée
- Désinfection de la charge utile d'image
- Marquage de la provenance des entrées utilisateur (pour les invites acheminées entre sessions)

Si vous avez besoin de détails sur le stockage des transcriptions, consultez :

- [/reference/session-management-compaction](/reference/session-management-compaction)

---

## Où cela s'exécute

Toute l'hygiène des transcriptions est centralisée dans le runner intégré :

- Sélection de la politique : `src/agents/transcript-policy.ts`
- Application de la désinfection/réparation : `sanitizeSessionHistory` dans `src/agents/pi-embedded-runner/google.ts`

La politique utilise `provider`, `modelApi` et `modelId` pour décider ce qu'il faut appliquer.

Indépendamment de l'hygiène des transcriptions, les fichiers de session sont réparés (si nécessaire) avant le chargement :

- `repairSessionFileIfNeeded` dans `src/agents/session-file-repair.ts`
- Appelé depuis `run/attempt.ts` et `compact.ts` (runner intégré)

---

## Règle globale : désinfection des images

Les charges utiles d'image sont toujours désinfectées pour éviter le rejet côté fournisseur en raison des limites de taille
(réduction d'échelle/recompression des images base64 surdimensionnées).

Cela aide également à contrôler la pression des jetons liée aux images pour les modèles compatibles avec la vision.
Les dimensions maximales plus basses réduisent généralement l'utilisation des jetons ; les dimensions plus élevées préservent les détails.

Implémentation :

- `sanitizeSessionMessagesImages` dans `src/agents/pi-embedded-helpers/images.ts`
- `sanitizeContentBlocksImages` dans `src/agents/tool-images.ts`
- Le côté image max est configurable via `agents.defaults.imageMaxDimensionPx` (par défaut : `1200`).

---

## Règle globale : appels d'outil malformés

Les blocs d'appel d'outil assistant qui manquent à la fois `input` et `arguments` sont supprimés
avant la construction du contexte du modèle. Cela évite les rejets du fournisseur provenant d'appels d'outil partiellement
persistés (par exemple, après un échec de limite de débit).

Implémentation :

- `sanitizeToolCallInputs` dans `src/agents/session-transcript-repair.ts`
- Appliqué dans `sanitizeSessionHistory` dans `src/agents/pi-embedded-runner/google.ts`

---

## Règle globale : provenance des entrées entre sessions

Lorsqu'un agent envoie une invite dans une autre session via `sessions_send` (y compris
les étapes de réponse/annonce agent-à-agent), OpenClaw persiste le tour utilisateur créé avec :

- `message.provenance.kind = "inter_session"`

Ces métadonnées sont écrites au moment de l'ajout de la transcription et ne changent pas le rôle
(`role: "user"` reste pour la compatibilité du fournisseur). Les lecteurs de transcription peuvent utiliser
ceci pour éviter de traiter les invites internes acheminées comme des instructions créées par l'utilisateur final.

Lors de la reconstruction du contexte, OpenClaw ajoute également un court marqueur `[Inter-session message]`
à ces tours utilisateur en mémoire afin que le modèle puisse les distinguer des
instructions de l'utilisateur final externe.

---

## Matrice des fournisseurs (comportement actuel)

**OpenAI / OpenAI Codex**

- Désinfection des images uniquement.
- Suppression des signatures de raisonnement orphelines (éléments de raisonnement autonomes sans bloc de contenu suivant) pour les transcriptions OpenAI Responses/Codex.
- Pas de désinfection des identifiants d'appel d'outil.
- Pas de réparation d'appairage des résultats d'outil.
- Pas de validation ou de réorganisation des tours.
- Pas de résultats d'outil synthétiques.
- Pas de suppression de signature de pensée.

**Google (Generative AI / Gemini CLI / Antigravity)**

- Désinfection des identifiants d'appel d'outil : alphanumérique strict.
- Réparation d'appairage des résultats d'outil et résultats d'outil synthétiques.
- Validation des tours (alternance de style Gemini).
- Correctif de réorganisation des tours Google (ajouter un petit amorçage utilisateur si l'historique commence par un assistant).
- Antigravity Claude : normaliser les signatures de pensée ; supprimer les blocs de pensée non signés.

**Anthropic / Minimax (compatible Anthropic)**

- Réparation d'appairage des résultats d'outil et résultats d'outil synthétiques.
- Validation des tours (fusionner les tours utilisateur consécutifs pour satisfaire l'alternance stricte).

**Mistral (y compris la détection basée sur l'identifiant de modèle)**

- Désinfection des identifiants d'appel d'outil : strict9 (alphanumérique longueur 9).

**OpenRouter Gemini**

- Nettoyage de la signature de pensée : supprimer les valeurs `thought_signature` non-base64 (conserver base64).

**Tout le reste**

- Désinfection des images uniquement.

---

## Comportement historique (pré-2026.1.22)

Avant la version 2026.1.22, OpenClaw appliquait plusieurs couches d'hygiène des transcriptions :

- Une **extension de désinfection de transcription** s'exécutait à chaque construction de contexte et pouvait :
  - Réparer l'appairage utilisation d'outil/résultat.
  - Désinfectez les identifiants d'appel d'outil (y compris un mode non strict qui préservait `_`/`-`).
- Le runner effectuait également une désinfection spécifique au fournisseur, ce qui dupliquait le travail.
- Des mutations supplémentaires se sont produites en dehors de la politique du fournisseur, notamment :
  - Suppression des balises `<final>` du texte assistant avant la persistance.
  - Suppression des tours d'erreur assistant vides.
  - Rognage du contenu assistant après les appels d'outil.

Cette complexité a causé des régressions entre fournisseurs (notamment `openai-responses`
appairage `call_id|fc_id`). Le nettoyage 2026.1.22 a supprimé l'extension, centralisé
la logique dans le runner, et rendu OpenAI **sans modification** au-delà de la désinfection des images.
