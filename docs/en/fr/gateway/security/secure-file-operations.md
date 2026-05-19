---
summary: "Comment OpenClaw gère l'accès aux fichiers locaux de manière sécurisée, et pourquoi l'assistant Python fs-safe optionnel est désactivé par défaut"
read_when:
  - Changing file access, archive extraction, workspace storage, or plugin filesystem helpers
title: "Opérations de fichiers sécurisées"
---

OpenClaw utilise [`@openclaw/fs-safe`](https://github.com/openclaw/fs-safe) pour les opérations de fichiers locaux sensibles à la sécurité : lectures/écritures limitées à la racine, remplacement atomique, extraction d'archives, espaces de travail temporaires, état JSON et gestion des fichiers secrets.

L'objectif est une **barrière de sécurité cohérente** pour le code OpenClaw de confiance qui reçoit des noms de chemins non fiables. Ce n'est pas un bac à sable. Les permissions du système de fichiers hôte, les utilisateurs du système d'exploitation, les conteneurs et la politique de l'agent/outil définissent toujours le véritable rayon d'impact.

## Par défaut : pas d'assistant Python

OpenClaw désactive par défaut l'assistant Python POSIX fs-safe.

Pourquoi :

- la passerelle ne doit pas lancer un processus Python persistant à moins qu'un opérateur n'ait explicitement choisi de le faire ;
- de nombreuses installations n'ont pas besoin du renforcement supplémentaire de mutation du répertoire parent ;
- désactiver Python rend le comportement du package/runtime plus prévisible sur les environnements de bureau, Docker, CI et les applications groupées.

OpenClaw change uniquement la valeur par défaut. Si vous définissez explicitement un mode, fs-safe le respecte :

```bash
# Comportement OpenClaw par défaut : replis fs-safe Node uniquement.
OPENCLAW_FS_SAFE_PYTHON_MODE=off

# Accepter l'assistant quand disponible, avec repli si indisponible.
OPENCLAW_FS_SAFE_PYTHON_MODE=auto

# Échouer de manière sécurisée si l'assistant ne peut pas démarrer.
OPENCLAW_FS_SAFE_PYTHON_MODE=require

# Interpréteur explicite optionnel.
OPENCLAW_FS_SAFE_PYTHON=/usr/bin/python3
```

Les noms fs-safe génériques fonctionnent aussi : `FS_SAFE_PYTHON_MODE` et `FS_SAFE_PYTHON`.

## Ce qui reste protégé sans Python

Avec l'assistant désactivé, OpenClaw utilise toujours les chemins Node de fs-safe pour :

- rejeter les échappements de chemins relatifs tels que `..`, les chemins absolus et les séparateurs de chemins où seuls les noms sont autorisés ;
- résoudre les opérations via un handle racine de confiance au lieu de vérifications ad-hoc `path.resolve(...).startsWith(...)` ;
- refuser les modèles de lien symbolique et de lien physique sur les API qui l'exigent ;
- ouvrir les fichiers avec des vérifications d'identité où l'API retourne ou consomme le contenu des fichiers ;
- écritures atomiques de fichiers temporaires frères pour les fichiers d'état/configuration ;
- limites d'octets pour les lectures et l'extraction d'archives ;
- modes privés pour les secrets et les fichiers d'état où l'API l'exige.

Ces protections couvrent le modèle de menace OpenClaw normal : code de passerelle de confiance gérant une entrée de chemin de modèle/plugin/canal non fiable dans une limite d'opérateur unique de confiance.

## Ce que Python ajoute

Sur POSIX, l'assistant optionnel de fs-safe maintient un processus Python persistant et utilise des opérations de système de fichiers relatives aux descripteurs de fichiers pour les mutations de répertoire parent telles que renommer, supprimer, mkdir, stat/list et certains chemins d'écriture.

Cela réduit les fenêtres de course de même UID où un autre processus peut échanger un répertoire parent entre la validation et la mutation. C'est une défense en profondeur pour les hôtes où des processus locaux non fiables peuvent modifier les mêmes répertoires sur lesquels OpenClaw opère.

Si votre déploiement présente ce risque et que Python est garanti d'exister, utilisez :

```bash
OPENCLAW_FS_SAFE_PYTHON_MODE=require
```

Utilisez `require` plutôt que `auto` quand l'assistant fait partie de votre posture de sécurité ; `auto` revient intentionnellement au comportement Node uniquement si l'assistant est indisponible.

## Conseils pour les plugins et le cœur

- L'accès aux fichiers destiné aux plugins doit passer par les assistants `openclaw/plugin-sdk/*`, pas par `fs` brut, quand un chemin provient d'un message, d'une sortie de modèle, d'une configuration ou d'une entrée de plugin.
- Le code principal doit utiliser les wrappers fs-safe locaux sous `src/infra/*` pour que la politique de processus d'OpenClaw soit appliquée de manière cohérente.
- L'extraction d'archives doit utiliser les assistants d'archive fs-safe avec des limites explicites de taille, de nombre d'entrées, de lien et de destination.
- Les secrets doivent utiliser les assistants de secrets OpenClaw ou les assistants de secrets/état privé fs-safe ; ne pas implémenter manuellement les vérifications de mode autour de `fs.writeFile`.
- Si vous avez besoin d'une isolation d'utilisateur local hostile, ne vous fiez pas à fs-safe seul. Exécutez des passerelles séparées sous des utilisateurs/hôtes du système d'exploitation séparés ou utilisez un bac à sable.

Connexe : [Sécurité](/fr/gateway/security), [Bac à sable](/fr/gateway/sandboxing), [Approbations d'exécution](/fr/tools/exec-approvals), [Secrets](/fr/gateway/secrets).
