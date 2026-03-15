---
summary: "Contexte : ce que le modèle voit, comment il est construit et comment l'inspecter"
read_when:
  - You want to understand what "context" means in OpenClaw
  - You are debugging why the model "knows" something (or forgot it)
  - You want to reduce context overhead (/context, /status, /compact)
title: "Contexte"
---

# Contexte

Le « contexte » est **tout ce qu'OpenClaw envoie au modèle pour une exécution**. Il est limité par la **fenêtre de contexte** du modèle (limite de tokens).

Modèle mental pour débutants :

- **Invite système** (construite par OpenClaw) : règles, outils, liste des compétences, heure/runtime et fichiers d'espace de travail injectés.
- **Historique de conversation** : vos messages + les messages de l'assistant pour cette session.
- **Appels d'outils/résultats + pièces jointes** : sortie de commande, lectures de fichiers, images/audio, etc.

Le contexte _n'est pas la même chose_ que la « mémoire » : la mémoire peut être stockée sur disque et rechargée ultérieurement ; le contexte est ce qui se trouve dans la fenêtre actuelle du modèle.

## Démarrage rapide (inspecter le contexte)

- `/status` → vue rapide « à quel point ma fenêtre est-elle pleine ? » + paramètres de session.
- `/context list` → ce qui est injecté + tailles approximatives (par fichier + totaux).
- `/context detail` → ventilation plus approfondie : par fichier, tailles de schémas d'outils, tailles d'entrées de compétences et taille de l'invite système.
- `/usage tokens` → ajouter un pied de page d'utilisation par réponse aux réponses normales.
- `/compact` → résumer l'historique plus ancien en une entrée compacte pour libérer de l'espace dans la fenêtre.

Voir aussi : [Commandes slash](/tools/slash-commands), [Utilisation des tokens et coûts](/reference/token-use), [Compaction](/concepts/compaction).

## Exemple de sortie

Les valeurs varient selon le modèle, le fournisseur, la politique d'outils et ce qui se trouve dans votre espace de travail.

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

- Invite système (toutes les sections).
- Historique de conversation.
- Appels d'outils + résultats d'outils.
- Pièces jointes/transcriptions (images/audio/fichiers).
- Résumés de compaction et artefacts d'élagage.
- « Wrappers » de fournisseur ou en-têtes cachés (non visibles, toujours comptabilisés).

## Comment OpenClaw construit l'invite système

L'invite système est **propriété d'OpenClaw** et reconstruite à chaque exécution. Elle comprend :

- Liste des outils + descriptions courtes.
- Liste des compétences (métadonnées uniquement ; voir ci-dessous).
- Emplacement de l'espace de travail.
- Heure (UTC + heure utilisateur convertie si configurée).
- Métadonnées de runtime (hôte/OS/modèle/réflexion).
- Fichiers d'amorçage d'espace de travail injectés sous **Contexte du projet**.

Ventilation complète : [Invite système](/concepts/system-prompt).

## Fichiers d'espace de travail injectés (Contexte du projet)

Par défaut, OpenClaw injecte un ensemble fixe de fichiers d'espace de travail (s'ils sont présents) :

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (première exécution uniquement)

Les fichiers volumineux sont tronqués par fichier en utilisant `agents.defaults.bootstrapMaxChars` (par défaut `20000` caractères). OpenClaw applique également un plafond d'injection d'amorçage total sur les fichiers avec `agents.defaults.bootstrapTotalMaxChars` (par défaut `150000` caractères). `/context` affiche les tailles **brutes vs injectées** et indique si une troncature s'est produite.

Lorsqu'une troncature se produit, le runtime peut injecter un bloc d'avertissement dans l'invite sous Contexte du projet. Configurez ceci avec `agents.defaults.bootstrapPromptTruncationWarning` (`off`, `once`, `always` ; par défaut `once`).

## Compétences : ce qui est injecté vs chargé à la demande

L'invite système inclut une **liste de compétences** compacte (nom + description + emplacement). Cette liste a un vrai surcoût.

Les instructions de compétence ne sont _pas_ incluses par défaut. Le modèle est censé `read` le `SKILL.md` de la compétence **uniquement si nécessaire**.

## Outils : il y a deux coûts

Les outils affectent le contexte de deux façons :

1. **Texte de la liste des outils** dans l'invite système (ce que vous voyez comme « Tooling »).
2. **Schémas d'outils** (JSON). Ceux-ci sont envoyés au modèle pour qu'il puisse appeler des outils. Ils comptent dans le contexte même si vous ne les voyez pas en texte brut.

`/context detail` ventile les plus grands schémas d'outils pour que vous puissiez voir ce qui domine.

## Commandes, directives et « raccourcis en ligne »

Les commandes slash sont gérées par la passerelle. Il y a quelques comportements différents :

- **Commandes autonomes** : un message qui est uniquement `/...` s'exécute en tant que commande.
- **Directives** : `/think`, `/verbose`, `/reasoning`, `/elevated`, `/model`, `/queue` sont supprimées avant que le modèle ne voie le message.
  - Les messages contenant uniquement des directives conservent les paramètres de session.
  - Les directives en ligne dans un message normal agissent comme des indices par message.
- **Raccourcis en ligne** (expéditeurs autorisés uniquement) : certains tokens `/...` à l'intérieur d'un message normal peuvent s'exécuter immédiatement (exemple : « hey /status »), et sont supprimés avant que le modèle ne voie le texte restant.

Détails : [Commandes slash](/tools/slash-commands).

## Sessions, compaction et élagage (ce qui persiste)

Ce qui persiste entre les messages dépend du mécanisme :

- **Historique normal** persiste dans la transcription de session jusqu'à ce qu'il soit compacté/élagué par la politique.
- **Compaction** persiste un résumé dans la transcription et conserve les messages récents intacts.
- **Élagage** supprime les anciens résultats d'outils de l'invite _en mémoire_ pour une exécution, mais ne réécrit pas la transcription.

Docs : [Session](/concepts/session), [Compaction](/concepts/compaction), [Élagage de session](/concepts/session-pruning).

Par défaut, OpenClaw utilise le moteur de contexte `legacy` intégré pour l'assemblage et la compaction. Si vous installez un plugin qui fournit `kind: "context-engine"` et le sélectionnez avec `plugins.slots.contextEngine`, OpenClaw délègue l'assemblage du contexte, `/compact` et les crochets de cycle de vie du contexte des sous-agents associés à ce moteur à la place.

## Ce que `/context` rapporte réellement

`/context` préfère le dernier rapport d'invite système **construit à l'exécution** lorsqu'il est disponible :

- `System prompt (run)` = capturé à partir de la dernière exécution intégrée (capable d'outils) et persisté dans le magasin de session.
- `System prompt (estimate)` = calculé à la volée lorsqu'aucun rapport d'exécution n'existe (ou lors de l'exécution via un backend CLI qui ne génère pas le rapport).

De toute façon, il rapporte les tailles et les principaux contributeurs ; il ne **dump pas** l'invite système complète ou les schémas d'outils.
