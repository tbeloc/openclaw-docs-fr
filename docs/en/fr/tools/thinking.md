---
summary: "Syntaxe des directives pour /think, /fast, /verbose et visibilité du raisonnement"
read_when:
  - Adjusting thinking, fast-mode, or verbose directive parsing or defaults
title: "Niveaux de réflexion"
---

# Niveaux de réflexion (directives /think)

## Fonctionnement

- Directive en ligne dans n'importe quel corps entrant : `/t <level>`, `/think:<level>`, ou `/thinking <level>`.
- Niveaux (alias) : `off | minimal | low | medium | high | xhigh | adaptive`
  - minimal → "think"
  - low → "think hard"
  - medium → "think harder"
  - high → "ultrathink" (budget maximal)
  - xhigh → "ultrathink+" (modèles GPT-5.2 + Codex uniquement)
  - adaptive → budget de raisonnement adaptatif géré par le fournisseur (pris en charge pour la famille de modèles Anthropic Claude 4.6)
  - `x-high`, `x_high`, `extra-high`, `extra high`, et `extra_high` correspondent à `xhigh`.
  - `highest`, `max` correspondent à `high`.
- Notes des fournisseurs :
  - Les modèles Anthropic Claude 4.6 utilisent par défaut `adaptive` quand aucun niveau de réflexion explicite n'est défini.
  - Z.AI (`zai/*`) ne supporte que la réflexion binaire (`on`/`off`). Tout niveau autre que `off` est traité comme `on` (mappé à `low`).
  - Moonshot (`moonshot/*`) mappe `/think off` à `thinking: { type: "disabled" }` et tout niveau autre que `off` à `thinking: { type: "enabled" }`. Quand la réflexion est activée, Moonshot n'accepte que `tool_choice` `auto|none` ; OpenClaw normalise les valeurs incompatibles à `auto`.

## Ordre de résolution

1. Directive en ligne sur le message (s'applique uniquement à ce message).
2. Remplacement de session (défini en envoyant un message contenant uniquement la directive).
3. Défaut global (`agents.defaults.thinkingDefault` dans la config).
4. Secours : `adaptive` pour les modèles Anthropic Claude 4.6, `low` pour les autres modèles capables de raisonnement, `off` sinon.

## Définir un défaut de session

- Envoyez un message qui est **uniquement** la directive (espaces autorisés), par ex. `/think:medium` ou `/t high`.
- Cela persiste pour la session actuelle (par défaut par expéditeur) ; effacé par `/think:off` ou réinitialisation d'inactivité de session.
- Une réponse de confirmation est envoyée (`Thinking level set to high.` / `Thinking disabled.`). Si le niveau est invalide (par ex. `/thinking big`), la commande est rejetée avec un indice et l'état de session reste inchangé.
- Envoyez `/think` (ou `/think:`) sans argument pour voir le niveau de réflexion actuel.

## Application par agent

- **Embedded Pi** : le niveau résolu est transmis au runtime de l'agent Pi en processus.

## Mode rapide (/fast)

- Niveaux : `on|off`.
- Un message contenant uniquement la directive bascule un remplacement de mode rapide de session et répond `Fast mode enabled.` / `Fast mode disabled.`.
- Envoyez `/fast` (ou `/fast status`) sans mode pour voir l'état du mode rapide effectif actuel.
- OpenClaw résout le mode rapide dans cet ordre :
  1. Directive en ligne/contenant uniquement `/fast on|off`
  2. Remplacement de session
  3. Config par modèle : `agents.defaults.models["<provider>/<model>"].params.fastMode`
  4. Secours : `off`
- Pour `openai/*`, le mode rapide applique le profil rapide OpenAI : `service_tier=priority` quand supporté, plus effort de raisonnement faible et verbosité de texte faible.
- Pour `openai-codex/*`, le mode rapide applique le même profil à faible latence sur les réponses Codex. OpenClaw maintient un seul bouton `/fast` partagé entre les deux chemins d'authentification.
- Pour les demandes directes d'API-key `anthropic/*`, le mode rapide mappe aux niveaux de service Anthropic : `/fast on` définit `service_tier=auto`, `/fast off` définit `service_tier=standard_only`.
- Le mode rapide Anthropic est API-key uniquement. OpenClaw ignore l'injection de niveau de service Anthropic pour l'authentification par jeton de configuration Claude / OAuth et pour les URL de base proxy non-Anthropic.

## Directives verbeux (/verbose ou /v)

- Niveaux : `on` (minimal) | `full` | `off` (défaut).
- Un message contenant uniquement la directive bascule la session verbeux et répond `Verbose logging enabled.` / `Verbose logging disabled.` ; les niveaux invalides retournent un indice sans changer l'état.
- `/verbose off` stocke un remplacement de session explicite ; effacez-le via l'interface utilisateur Sessions en choisissant `inherit`.
- La directive en ligne affecte uniquement ce message ; les défauts de session/globaux s'appliquent sinon.
- Envoyez `/verbose` (ou `/verbose:`) sans argument pour voir le niveau verbeux actuel.
- Quand le mode verbeux est activé, les agents qui émettent des résultats d'outils structurés (Pi, autres agents JSON) renvoient chaque appel d'outil comme son propre message contenant uniquement des métadonnées, préfixé avec `<emoji> <tool-name>: <arg>` quand disponible (chemin/commande). Ces résumés d'outils sont envoyés dès que chaque outil démarre (bulles séparées), pas comme des deltas de streaming.
- Les résumés d'échec d'outil restent visibles en mode normal, mais les suffixes de détail d'erreur bruts sont masqués sauf si le mode verbeux est `on` ou `full`.
- Quand le mode verbeux est `full`, les sorties d'outils sont également transmises après la fin (bulle séparée, tronquée à une longueur sûre). Si vous basculez `/verbose on|full|off` pendant qu'une exécution est en cours, les bulles d'outils suivantes respectent le nouveau paramètre.

## Visibilité du raisonnement (/reasoning)

- Niveaux : `on|off|stream`.
- Un message contenant uniquement la directive bascule si les blocs de réflexion sont affichés dans les réponses.
- Quand activé, le raisonnement est envoyé comme un **message séparé** préfixé avec `Reasoning:`.
- `stream` (Telegram uniquement) : diffuse le raisonnement dans la bulle de brouillon Telegram pendant que la réponse est générée, puis envoie la réponse finale sans raisonnement.
- Alias : `/reason`.
- Envoyez `/reasoning` (ou `/reasoning:`) sans argument pour voir le niveau de raisonnement actuel.

## Connexes

- La documentation du mode élevé se trouve dans [Mode élevé](/fr/tools/elevated).

## Battements de cœur

- Le corps de la sonde de battement de cœur est l'invite de battement de cœur configurée (défaut : `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`). Les directives en ligne dans un message de battement de cœur s'appliquent comme d'habitude (mais évitez de changer les défauts de session à partir des battements de cœur).
- La livraison du battement de cœur utilise par défaut la charge utile finale uniquement. Pour envoyer également le message `Reasoning:` séparé (quand disponible), définissez `agents.defaults.heartbeat.includeReasoning: true` ou par agent `agents.list[].heartbeat.includeReasoning: true`.

## Interface utilisateur de chat web

- Le sélecteur de réflexion du chat web reflète le niveau stocké de la session à partir du magasin/config de session entrant quand la page se charge.
- Choisir un autre niveau s'applique uniquement au message suivant (`thinkingOnce`) ; après l'envoi, le sélecteur revient au niveau de session stocké.
- Pour changer le défaut de session, envoyez une directive `/think:<level>` (comme avant) ; le sélecteur la reflètera après le prochain rechargement.
