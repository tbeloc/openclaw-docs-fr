---
summary: "Maintenir un plan durable et une carte de statut pour une session"
title: "Carte de progression"
sidebarTitle: "Carte de progression"
read_when:
  - You want an agent to publish durable at-a-glance progress for its current session
  - You need the progress_card input, limits, rendering, or clearing contract
---

`progress_card` est l'outil de statut d'agent unique pour une session. Il stocke un plan d'étapes ordonné, une note Markdown compacte, ou les deux. Chaque appel remplace la carte entière, de sorte que la dernière écriture est la source de vérité pour quelqu'un qui suit le travail sans lire la transcription.

La carte est un état de session durable. Une reconnexion ou un rechargement de page lit la dernière carte depuis la Gateway au lieu de la reconstruire à partir des événements d'outils ou de l'historique de transcription. La transcription ne conserve qu'un court reçu de mise à jour, pas une autre copie complète de la carte.

## Mettre à jour une carte

Les deux champs d'entrée sont optionnels :

- `plan` : jusqu'à 50 étapes ordonnées. Chaque étape a un texte `step` non vide et un `status` de `pending`, `in_progress`, ou `completed`. Au maximum une étape peut être `in_progress`.
- `markdown` : un récit compacte sur ce qui s'est passé, ce qui est bloqué, ou ce qui vient ensuite. Utilisez-le quand une note lisible en un coup d'œil en dit plus que la liste d'étapes ; ne répétez pas le plan en Markdown.

Par exemple :

```json
{
  "plan": [
    { "step": "Inspect the failing route", "status": "completed" },
    { "step": "Repair the session owner", "status": "in_progress" },
    { "step": "Run focused verification", "status": "pending" }
  ],
  "markdown": "The failure is isolated to session ownership. No blocker."
}
```

Chaque appel est un remplacement, pas un correctif. Omettre `markdown` supprime la note précédente ; omettre `plan` supprime la liste de contrôle précédente.

L'outil retourne un court reçu tel que `Progress card updated (rev 4, 1/3 done)` ou `Progress card updated (rev 4)` quand il n'y a pas de plan. Son résultat structuré contient la révision et soit les comptages d'étapes complétées/totales, soit `null` quand aucun plan n'est présent. OpenClaw émet également des événements de plan pour les applications natives et les rendeurs de canal pendant leur migration, mais la carte durable reste l'état faisant autorité.

## Formater la note

Markdown accepte le formatage ordinaire, les petits tableaux, les liens, et les barres de progression optionnelles :

```md
Tests are running.

<progress value="3" max="7"></progress>

| check      | state   |
| ---------- | ------- |
| unit tests | passed  |
| live flow  | running |
```

L'interface Control rend les éléments `progress` avec les attributs `value` et `max`. Les autres HTML bruts sont supprimés par le désinfectant Markdown.

## Limites

- Markdown : au maximum 8 192 octets UTF-8.
- Plan : au maximum 50 étapes.
- Texte d'étape : non vide et au maximum 512 octets UTF-8 par étape.
- Travail actif : au maximum une étape `in_progress`.

La Gateway supprime les caractères Unicode invisibles et les caractères de contrôle bidirectionnels de Markdown et du texte d'étape avant de stocker la carte.

## Effacer une carte

Appelez `progress_card` avec les deux parties absentes ou vides pour supprimer la carte actuelle :

```json
{}
```

Un plan vide plus un Markdown vide ou contenant uniquement des espaces l'efface également. Un effacement réussi retourne `Progress card cleared`.

## Où la carte apparaît

Le chat actuel affiche exactement une carte en direct :

- Quand le rail de session est visible, la carte apparaît dans le rail.
- Aux largeurs étroites où le rail est masqué, la carte apparaît dans la surface repliable à côté du compositeur.

Les deux placements s'excluent mutuellement. Les autres sessions peuvent afficher leur dernière carte dans la carte de survol de la barre latérale. Tous les placements lisent le même état soutenu par Gateway et se rafraîchissent après les notifications `progressCard.changed`.
