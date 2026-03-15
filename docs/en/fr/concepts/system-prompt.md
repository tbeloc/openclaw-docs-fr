---
summary: "Ce que contient l'invite système OpenClaw et comment elle est assemblée"
read_when:
  - Editing system prompt text, tools list, or time/heartbeat sections
  - Changing workspace bootstrap or skills injection behavior
title: "Invite système"
---

# Invite système

OpenClaw construit une invite système personnalisée pour chaque exécution d'agent. L'invite est **propriété d'OpenClaw** et n'utilise pas l'invite par défaut de pi-coding-agent.

L'invite est assemblée par OpenClaw et injectée dans chaque exécution d'agent.

## Structure

L'invite est intentionnellement compacte et utilise des sections fixes :

- **Outils** : liste d'outils actuelle + descriptions courtes.
- **Sécurité** : rappel court des garde-fous pour éviter les comportements de recherche de pouvoir ou le contournement de la surveillance.
- **Compétences** (si disponibles) : indique au modèle comment charger les instructions de compétences à la demande.
- **Mise à jour automatique OpenClaw** : comment exécuter `config.apply` et `update.run`.
- **Espace de travail** : répertoire de travail (`agents.defaults.workspace`).
- **Documentation** : chemin local vers la documentation OpenClaw (dépôt ou paquet npm) et quand la consulter.
- **Fichiers d'espace de travail (injectés)** : indique que les fichiers d'amorçage sont inclus ci-dessous.
- **Sandbox** (si activée) : indique l'exécution en environnement isolé, les chemins sandbox et si l'exécution élevée est disponible.
- **Date et heure actuelles** : heure locale de l'utilisateur, fuseau horaire et format d'heure.
- **Balises de réponse** : syntaxe de balise de réponse optionnelle pour les fournisseurs pris en charge.
- **Pulsations** : invite de pulsation et comportement d'accusé de réception.
- **Exécution** : hôte, système d'exploitation, node, modèle, racine du dépôt (si détectée), niveau de réflexion (une ligne).
- **Raisonnement** : niveau de visibilité actuel + conseil de basculement /reasoning.

Les garde-fous de sécurité dans l'invite système sont consultatifs. Ils guident le comportement du modèle mais n'appliquent pas la politique. Utilisez la politique d'outils, les approbations d'exécution, l'isolation et les listes blanches de canaux pour une application stricte ; les opérateurs peuvent les désactiver par conception.

## Modes d'invite

OpenClaw peut afficher des invites système plus petites pour les sous-agents. L'exécution définit un
`promptMode` pour chaque exécution (pas une configuration accessible à l'utilisateur) :

- `full` (par défaut) : inclut toutes les sections ci-dessus.
- `minimal` : utilisé pour les sous-agents ; omet **Compétences**, **Rappel de mémoire**, **Mise à jour automatique OpenClaw**, **Alias de modèle**, **Identité utilisateur**, **Balises de réponse**,
  **Messagerie**, **Réponses silencieuses** et **Pulsations**. Les outils, **Sécurité**,
  l'espace de travail, la sandbox, la date et heure actuelles (si connues), l'exécution et le contexte injecté
  restent disponibles.
- `none` : retourne uniquement la ligne d'identité de base.

Quand `promptMode=minimal`, les invites injectées supplémentaires sont étiquetées **Contexte de sous-agent**
au lieu de **Contexte de groupe de discussion**.

## Injection d'amorçage d'espace de travail

Les fichiers d'amorçage sont réduits et ajoutés sous **Contexte du projet** afin que le modèle voie le contexte d'identité et de profil sans avoir besoin de lectures explicites :

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (uniquement sur les nouveaux espaces de travail)
- `MEMORY.md` si présent, sinon `memory.md` comme alternative en minuscules

Tous ces fichiers sont **injectés dans la fenêtre de contexte** à chaque tour, ce qui
signifie qu'ils consomment des jetons. Gardez-les concis — en particulier `MEMORY.md`, qui peut
croître au fil du temps et entraîner une utilisation de contexte inopinément élevée et une compaction plus fréquente.

> **Remarque :** les fichiers quotidiens `memory/*.md` ne sont **pas** injectés automatiquement. Ils
> sont accessibles à la demande via les outils `memory_search` et `memory_get`, donc ils
> ne comptent pas dans la fenêtre de contexte à moins que le modèle ne les lise explicitement.

Les fichiers volumineux sont tronqués avec un marqueur. La taille maximale par fichier est contrôlée par
`agents.defaults.bootstrapMaxChars` (par défaut : 20000). Le contenu d'amorçage injecté total
est limité par `agents.defaults.bootstrapTotalMaxChars`
(par défaut : 150000). Les fichiers manquants injectent un marqueur de fichier manquant court. Quand la troncature
se produit, OpenClaw peut injecter un bloc d'avertissement dans le contexte du projet ; contrôlez cela avec
`agents.defaults.bootstrapPromptTruncationWarning` (`off`, `once`, `always`;
par défaut : `once`).

Les sessions de sous-agent injectent uniquement `AGENTS.md` et `TOOLS.md` (les autres fichiers d'amorçage
sont filtrés pour garder le contexte du sous-agent petit).

Les crochets internes peuvent intercepter cette étape via `agent:bootstrap` pour muter ou remplacer
les fichiers d'amorçage injectés (par exemple en remplaçant `SOUL.md` par une persona alternative).

Pour inspecter la contribution de chaque fichier injecté (brut vs injecté, troncature, plus surcharge de schéma d'outil), utilisez `/context list` ou `/context detail`. Voir [Contexte](/fr/concepts/context).

## Gestion du temps

L'invite système inclut une section **Date et heure actuelles** dédiée quand le
fuseau horaire de l'utilisateur est connu. Pour maintenir la stabilité du cache d'invite, elle inclut maintenant
uniquement le **fuseau horaire** (pas d'horloge dynamique ni de format d'heure).

Utilisez `session_status` quand l'agent a besoin de l'heure actuelle ; la carte d'état
inclut une ligne d'horodatage.

Configurez avec :

- `agents.defaults.userTimezone`
- `agents.defaults.timeFormat` (`auto` | `12` | `24`)

Voir [Date et heure](/fr/date-time) pour les détails complets du comportement.

## Compétences

Quand des compétences éligibles existent, OpenClaw injecte une **liste de compétences disponibles** compacte
(`formatSkillsForPrompt`) qui inclut le **chemin de fichier** pour chaque compétence. L'invite
indique au modèle d'utiliser `read` pour charger le SKILL.md à l'emplacement indiqué (espace de travail, géré ou fourni). Si aucune compétence n'est éligible, la
section Compétences est omise.

```
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
  </skill>
</available_skills>
```

Cela garde l'invite de base petite tout en permettant l'utilisation ciblée de compétences.

## Documentation

Quand disponible, l'invite système inclut une section **Documentation** qui pointe vers le
répertoire de documentation OpenClaw local (soit `docs/` dans l'espace de travail du dépôt soit la
documentation du paquet npm fourni) et note également le miroir public, le dépôt source, le Discord communautaire et
ClawHub ([https://clawhub.com](https://clawhub.com)) pour la découverte de compétences. L'invite indique au modèle de consulter d'abord la documentation locale
pour le comportement, les commandes, la configuration ou l'architecture d'OpenClaw, et d'exécuter
`openclaw status` lui-même quand possible (ne demandant à l'utilisateur que quand il n'y a pas accès).
