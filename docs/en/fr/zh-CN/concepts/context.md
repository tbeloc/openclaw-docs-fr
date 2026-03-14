---
read_when:
  - Vous voulez comprendre ce que signifie "contexte" dans OpenClaw
  - Vous déboguez pourquoi le modèle "sait" certaines choses (ou les a oubliées)
  - Vous voulez réduire les frais généraux de contexte (/context, /status, /compact)
summary: Contexte : ce que le modèle voit, comment il est construit et comment le vérifier
title: Contexte
x-i18n:
  generated_at: "2026-02-03T07:46:15Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b32867b9b93254fdd1077d0d97c203cabfdba3330bb941693c83feba8e5db0cc
  source_path: concepts/context.md
  workflow: 15
---

# Contexte

Le "contexte" est **tout ce qu'OpenClaw envoie au modèle lors d'une exécution**. Il est limité par la **fenêtre de contexte** du modèle (limite de tokens).

Modèle mental pour les débutants :

- **Invite système** (construite par OpenClaw) : règles, outils, liste des Skills, heure/runtime, et fichiers d'espace de travail injectés.
- **Historique de conversation** : vos messages + messages de l'assistant dans cette session.
- **Appels d'outils/résultats + pièces jointes** : sorties de commandes, lectures de fichiers, images/audio, etc.

Le contexte n'est _pas la même chose_ que la "mémoire" : la mémoire peut être stockée sur disque et rechargée plus tard ; le contexte est ce qui se trouve actuellement dans la fenêtre du modèle.

## Démarrage rapide (vérifier le contexte)

- `/status` → Aperçu rapide "À quel point ma fenêtre est-elle pleine ?" + paramètres de session.
- `/context list` → Ce qui a été injecté + taille approximative (par fichier + total).
- `/context detail` → Ventilation plus approfondie : chaque fichier, taille de chaque schéma d'outil, taille de chaque entrée Skills et taille de l'invite système.
- `/usage tokens` → Ajoute un pied de page d'utilisation après les réponses normales montrant l'utilisation par réponse.
- `/compact` → Résume l'historique plus ancien en entrées compactes pour libérer de l'espace dans la fenêtre.

Voir aussi : [Commandes slash](/tools/slash-commands), [Utilisation des tokens et coûts](/reference/token-use), [Compaction](/concepts/compaction).

## Exemple de sortie

Les chiffres varient selon le modèle, le fournisseur, la stratégie d'outils et le contenu de l'espace de travail.

### `/context list`

```
🧠 Context breakdown
Workspace: <workspaceDir>
Bootstrap max/file: 20,000 chars
Sandbox: mode=non-main sandboxed=false
System prompt (run): 38,412 chars (~9,603 tok) (Project Context 23,901 chars (~5,976 tok))

Injected workspace files:
- AGENTS.md: OK | raw 1,742 chars (~436 tok) | injected 1,742 chars (~436 tok)
- SOUL.md: OK | raw 912 chars (~228 tok) | injected 912 chars (~228 tok)
- TOOLS.md: TRUNCATED | raw 54,210 chars (~13,553 tok) | injected 20,962 chars (~5,241 tok)
- IDENTITY.md: OK | raw 211 chars (~53 tok) | injected 211 chars (~53 tok)
- USER.md: OK | raw 388 chars (~97 tok) | injected 388 chars (~97 tok)
- HEARTBEAT.md: MISSING | raw 0 | injected 0
- BOOTSTRAP.md: OK | raw 0 chars (~0 tok) | injected 0 chars (~0 tok)

Skills list (system prompt text): 2,184 chars (~546 tok) (12 skills)
Tools: read, edit, write, exec, process, browser, message, sessions_send, …
Tool list (system prompt text): 1,032 chars (~258 tok)
Tool schemas (JSON): 31,988 chars (~7,997 tok) (counts toward context; not shown as text)
Tools: (same as above)

Session tokens (cached): 14,250 total / ctx=32,000
```

### `/context detail`

```
🧠 Context breakdown (detailed)
…
Top skills (prompt entry size):
- frontend-design: 412 chars (~103 tok)
- oracle: 401 chars (~101 tok)
… (+10 more skills)

Top tools (schema size):
- browser: 9,812 chars (~2,453 tok)
- exec: 6,240 chars (~1,560 tok)
… (+N more tools)
```

## Ce qui compte dans la fenêtre de contexte

Tout ce que le modèle reçoit compte, y compris :

- L'invite système (toutes les parties).
- L'historique de conversation.
- Les appels d'outils + résultats d'outils.
- Les pièces jointes/transcriptions (images/audio/fichiers).
- Les résumés compactés et les artefacts de pruning.
- Les "wrappers" du fournisseur ou en-têtes cachés (invisibles, mais toujours comptés).

## Comment OpenClaw construit l'invite système

L'invite système est **détenue par OpenClaw** et reconstruite à chaque exécution. Elle comprend :

- Liste des outils + brève description.
- Liste des Skills (métadonnées uniquement ; voir ci-dessous).
- Emplacement de l'espace de travail.
- Heure (UTC + conversion au fuseau horaire de l'utilisateur si configurée).
- Métadonnées de runtime (hôte/OS/modèle/réflexion).
- Fichiers d'amorçage de l'espace de travail injectés sous **Contexte du projet**.

Ventilation complète : [Invite système](/concepts/system-prompt).

## Fichiers d'espace de travail injectés (contexte du projet)

Par défaut, OpenClaw injecte un ensemble fixe de fichiers d'espace de travail (s'ils existent) :

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (première exécution uniquement)

Les fichiers volumineux sont tronqués par fichier en utilisant `agents.defaults.bootstrapMaxChars` (par défaut `20000` caractères). `/context` affiche les tailles **brutes vs injectées** et indique si une troncature s'est produite.

## Skills : contenu injecté vs chargement à la demande

L'invite système contient une **liste compacte de Skills** (nom + description + emplacement). Cette liste a un coût réel.

Les instructions Skill ne sont _pas_ incluses par défaut. Le modèle devrait **uniquement `read` le `SKILL.md` d'un Skill si nécessaire**.

## Outils : deux types de coûts

Les outils affectent le contexte de deux façons :

1. **Texte de la liste d'outils** dans l'invite système (le "Tooling" que vous voyez).
2. **Schémas d'outils** (JSON). Ceux-ci sont envoyés au modèle pour qu'il puisse appeler les outils. Ils comptent dans le contexte, même si vous ne les voyez pas en tant que texte brut.

`/context detail` ventile les plus grands schémas d'outils pour que vous puissiez voir ce qui domine.

## Commandes, directives et "raccourcis en ligne"

Les commandes slash sont traitées par la passerelle Gateway. Il existe plusieurs comportements différents :

- **Commandes autonomes** : les messages qui sont uniquement `/...` s'exécutent en tant que commandes.
- **Directives** : `/think`, `/verbose`, `/reasoning`, `/elevated`, `/model`, `/queue` sont supprimées avant que le modèle ne voie le message.
  - Seuls les messages de directive persistent les paramètres de session.
  - Les directives en ligne dans les messages normaux agissent comme des invites par message.
- **Raccourcis en ligne** (liste blanche d'expéditeurs uniquement) : certains tokens `/...` dans les messages normaux peuvent s'exécuter immédiatement (par exemple : "hey /status") et sont supprimés avant que le modèle ne voie le texte restant.

Détails : [Commandes slash](/tools/slash-commands).

## Sessions, compaction et pruning (ce qui persiste)

Ce qui persiste entre les messages dépend du mécanisme :

- **L'historique normal** persiste dans l'enregistrement de session jusqu'à ce qu'il soit compacté/prunné par la politique.
- **La compaction** persiste les résumés dans l'enregistrement et garde les messages récents inchangés.
- **Le pruning** supprime les anciens résultats d'outils de l'invite en mémoire de l'exécution, mais ne réécrit pas l'enregistrement.

Documentation : [Session](/concepts/session), [Compaction](/concepts/compaction), [Session pruning](/concepts/session-pruning).

## Ce que `/context` rapporte réellement

`/context` rapporte en priorité l'**invite système construite lors de la dernière exécution** lorsqu'elle est disponible :

- `System prompt (run)` = capturée à partir de la dernière exécution intégrée (avec capacités d'outils) et persistée dans le stockage de session.
- `System prompt (estimate)` = calculée à la volée quand aucun rapport d'exécution n'existe (ou lors d'exécutions via un backend CLI qui ne génère pas de rapports).

De toute façon, elle rapporte la taille et les contributeurs majeurs ; elle **ne** déverse pas l'invite système complète ou les schémas d'outils.
