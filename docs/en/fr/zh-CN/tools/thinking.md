---
read_when:
  - 调整思考或详细模式指令解析或默认值时
summary: "`/think` + `/verbose` 的指令语法及其对模型推理的影响"
title: 思考级别
x-i18n:
  generated_at: "2026-02-01T21:43:37Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 1a611474c2781c9a8e9dac0e084e7ee4ef58aebece181fdc877392fc27442746
  source_path: tools/thinking.md
  workflow: 15
---

# Niveaux de réflexion (directive `/think`)

## Description des fonctionnalités

- Utilisez des directives en ligne dans le corps de tout message entrant : `/t <level>`, `/think:<level>` ou `/thinking <level>`.
- Niveaux (alias) : `off | minimal | low | medium | high | xhigh` (modèles GPT-5.2 + Codex uniquement)
  - minimal → "think"
  - low → "think hard"
  - medium → "think harder"
  - high → "ultrathink" (budget maximal)
  - xhigh → "ultrathink+" (modèles GPT-5.2 + Codex uniquement)
  - `highest`, `max` sont mappés à `high`.
- Notes du fournisseur :
  - Z.AI (`zai/*`) ne supporte que la réflexion binaire (`on`/`off`). Tout niveau autre que `off` est traité comme `on` (mappé à `low`).

## Ordre de priorité d'analyse

1. Directives en ligne sur le message (s'appliquent uniquement à ce message).
2. Remplacement de session (défini en envoyant un message contenant uniquement la directive).
3. Valeurs par défaut globales (`agents.defaults.thinkingDefault` dans la configuration).
4. Secours : `low` pour les modèles dotés de capacités de raisonnement ; sinon `off`.

## Définir les valeurs par défaut de la session

- Envoyez un message contenant **uniquement** la directive (les espaces blancs sont autorisés), par exemple `/think:medium` ou `/t high`.
- Ce paramètre reste actif dans la session actuelle (par défaut par expéditeur) ; effacez-le avec `/think:off` ou lors de la réinitialisation de la session inactive.
- Une réponse de confirmation est envoyée (`Thinking level set to high.` / `Thinking disabled.`). Si le niveau est invalide (par exemple `/thinking big`), la commande est rejetée avec un message d'aide et l'état de la session reste inchangé.
- Envoyez `/think` (ou `/think:`) sans paramètre pour afficher le niveau de réflexion actuel.

## Application par agent

- **Pi intégré** : le niveau analysé est transmis au runtime de l'agent Pi en processus.

## Directive de mode détaillé (`/verbose` ou `/v`)

- Niveaux : `on` (minimal) | `full` | `off` (par défaut).
- Un message contenant uniquement la directive bascule le mode détaillé de la session et répond `Verbose logging enabled.` / `Verbose logging disabled.` ; un niveau invalide retourne un message d'aide sans modifier l'état.
- `/verbose off` stocke un remplacement de session explicite ; effacez-le en sélectionnant `inherit` via l'interface de session.
- Les directives en ligne affectent uniquement ce message ; sinon, les valeurs par défaut de session/globales s'appliquent.
- Envoyez `/verbose` (ou `/verbose:`) sans paramètre pour afficher le niveau de mode détaillé actuel.
- Lorsque le mode détaillé est activé, les agents émettant des résultats d'outils structurés (Pi et autres agents JSON) renvoient chaque appel d'outil en tant que message de métadonnées distinct, préfixé par `<emoji> <tool-name>: <arg>` le cas échéant (chemin/commande). Ces résumés d'outils sont envoyés immédiatement au démarrage de chaque outil (bulle indépendante), et non comme des incréments en continu.
- Lorsque le mode détaillé est `full`, la sortie de l'outil est également transmise après son achèvement (bulle indépendante, tronquée à une longueur sûre). Si vous basculez `/verbose on|full|off` pendant l'exécution, les bulles d'outils suivantes respecteront le nouveau paramètre.

## Visibilité du raisonnement (`/reasoning`)

- Niveaux : `on|off|stream`.
- Un message contenant uniquement la directive bascule l'affichage des blocs de réflexion dans la réponse.
- Lorsqu'il est activé, le contenu du raisonnement est envoyé en tant que **message distinct**, préfixé par `Reasoning:`.
- `stream` (Telegram uniquement) : diffuse le contenu du raisonnement en continu dans la bulle de brouillon Telegram pendant la génération de la réponse, puis envoie la réponse finale sans le raisonnement.
- Alias : `/reason`.
- Envoyez `/reasoning` (ou `/reasoning:`) sans paramètre pour afficher le niveau de raisonnement actuel.

## Contenu connexe

- La documentation du mode élevé se trouve à [Mode élevé](/tools/elevated).

## Pulsation

- Le corps de la sonde de pulsation est l'invite de pulsation configurée (par défaut : `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`). Les directives en ligne dans les messages de pulsation fonctionnent normalement (mais évitez de modifier les valeurs par défaut de session à partir de la pulsation).
- La livraison de pulsation inclut par défaut uniquement la charge utile finale. Pour envoyer également un message `Reasoning:` distinct (s'il est disponible), définissez `agents.defaults.heartbeat.includeReasoning: true` ou par agent `agents.list[].heartbeat.includeReasoning: true`.

## Interface de chat Web

- Le sélecteur de réflexion du chat Web lit le niveau stocké de la session à partir du stockage de session entrant/configuration au chargement de la page et reflète le niveau stocké de la session.
- La sélection d'un autre niveau s'applique uniquement au message suivant (`thinkingOnce`) ; après l'envoi, le sélecteur revient au niveau de session stocké.
- Pour modifier la valeur par défaut de la session, envoyez la directive `/think:<level>` (comme avant) ; le sélecteur reflètera ce paramètre lors du prochain rafraîchissement.
