---
summary: "Une conversation continue sur tous vos canaux : l'agent personnel par défaut"
read_when:
  - You want to understand where your agent "lives"
  - You expect the same context whether you write on Telegram, WhatsApp, or the web
  - You want your agent to know what happens in groups and side threads
title: "La session principale"
---

OpenClaw est d'abord un agent personnel. Par défaut, chaque message direct que
vous lui envoyez — depuis Telegram, WhatsApp, iMessage, Slack DMs, l'application
web, n'importe où — arrive dans **une conversation continue** : la session
principale. Posez une question sur votre téléphone, continuez depuis votre
ordinateur portable, et l'agent a le même contexte dans les deux endroits. Il y
a un seul cerveau, et c'est là qu'il pense.

Sous le capot, la session principale est une session ordinaire avec la clé
`agent:<agentId>:main` (par exemple `agent:main:main`). Ce qui la rend spéciale,
c'est que la portée DM par défaut réduit tous les messages directs en une seule,
et que le reste du système la traite comme la racine de l'agent : les battements
de cœur la réveillent, les travaux de fond lui rendent compte, et l'activité
ailleurs remonte vers elle.

## Accueil

Dans l'application web, la session principale est la page **Accueil** — la
première entrée dans la barre latérale. La ligne d'identité en haut est votre
agent (cliquez dessus pour le menu de l'agent) ; Accueil est l'endroit où vous
lui parlez. Les sessions qui se ramifient de la conversation principale
apparaissent sous **Threads**, les chats de groupe sous **Groupes**, et les
sessions de codage/CLI sous **Codage**.

## Ce qui s'écoule dans la session principale

La session principale n'est pas seulement un journal de chat ; c'est l'endroit où
le monde de votre agent converge :

- **Activité de groupe.** Les sessions de groupe et de salle restent isolées
  (voir ci-dessous), mais sous la portée DM par défaut, la session principale
  les surveille automatiquement. L'activité s'accumule sous forme d'avis compacts
  — fusionnés par conversation, jamais un réveil par message — et l'agent les
  voit la prochaine fois qu'il s'exécute : à votre prochain message ou à un
  battement de cœur programmé. L'agent peut également lire les sessions qu'il
  surveille, donc « qu'ai-je manqué dans le groupe familial ? » fonctionne.
- **Travail de fond.** Les sous-agents et les sessions générées annoncent leurs
  résultats à la session qui les a lancés, donc le travail que l'agent a lancé
  depuis Accueil rend compte à Accueil.
- **Battements de cœur.** Les battements de cœur programmés ciblent la session
  principale, ce qui transforme les avis en attente en conscience même quand vous
  n'avez rien écrit.

## Mémoire à travers les réinitialisations et les conversations

La conversation continue est limitée par la fenêtre de contexte du modèle, donc
la continuité provient de couches autour d'elle :

- `MEMORY.md`, la mémoire à long terme organisée de l'agent, est chargée dans
  chaque nouvelle session. Les notes quotidiennes (`memory/YYYY-MM-DD.md`) sont
  consultables à la demande et les récentes sont réamorçées après un `/new` ou
  `/reset`. Avant la compaction, l'agent vide les faits durables dans les notes
  quotidiennes afin que les longues conversations ne les perdent pas
  silencieusement.
- **Rappel de mémoire entre conversations** permet à l'agent de rappeler du
  contenu de ses autres sessions privées. Sur les configurations personnelles —
  `session.dmScope` global se résolvant en `main` sans surcharges DM par liaison
  — c'est activé par défaut ; tout isolement DM configuré le désactive sauf si
  vous acceptez explicitement. Voir [Configuration de la mémoire](/fr/reference/memory-config).

## Une session continue, pas une session immortelle

La session principale avance à travers les réinitialisations et la compaction
plutôt que de croître indéfiniment :

- Par défaut, la session se réinitialise quotidiennement à 04:00 heure locale
  (configurable, ou basée sur l'inactivité ; voir [Gestion des sessions](/fr/concepts/session)).
  Sur `/new` et `/reset`, la fin de la conversation qui se termine est enregistrée
  dans les notes de mémoire quotidiennes, et la session suivante réamorce les
  notes récentes.
- Quand la conversation approche de la fenêtre de contexte, la compaction résume
  et continue sur place — l'historique des transcriptions reste dans le magasin
  de sessions.
- Le magasin de sessions par agent conserve les transcriptions archivées jusqu'à
  ce qu'un budget disque (10 Go par défaut) évince les plus anciennes.

## Quand vous voulez l'isolement à la place

La session principale partagée est le bon défaut pour un agent que seul vous
contactez. Si plusieurs personnes peuvent envoyer des messages à votre agent,
isolez les DMs :

```json5
{
  session: {
    dmScope: "per-channel-peer",
  },
}
```

Avec une portée isolante, chaque expéditeur obtient sa propre session, la
surveillance de groupe depuis la session principale est désactivée, et le rappel
de mémoire entre conversations est désactivé par défaut. `openclaw security audit`
recommande l'isolement quand il détecte plusieurs expéditeurs DM. La matrice de
portée complète, la liaison d'identité, et les surcharges par route sont
couvertes dans [Gestion des sessions](/fr/concepts/session) et [Routage des
canaux](/fr/channels/channel-routing).

## Connexes

- [Gestion des sessions](/fr/concepts/session) — routage, portées, réinitialisations
- [Routage des canaux](/fr/channels/channel-routing) — comment les agents et les sessions sont sélectionnés
- [Mémoire](/fr/concepts/memory) — couches de mémoire durable
- [Multi-agent](/fr/concepts/multi-agent) — exécution de plusieurs agents isolés
