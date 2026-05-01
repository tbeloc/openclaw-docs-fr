---
summary: "Comment OpenClaw planifie, prépare et répare les dépendances d'exécution des plugins groupés"
read_when:
  - You are debugging bundled plugin runtime dependency repair
  - You are changing plugin startup, doctor, or package-manager install behavior
  - You are maintaining packaged OpenClaw installs or bundled plugin manifests
title: "Résolution des dépendances des plugins"
sidebarTitle: "Dépendances"
---

OpenClaw n'installe pas chaque arborescence de dépendances de plugin groupé au moment de l'installation du paquet. Il dérive d'abord un plan de plugin effectif à partir de la configuration et des métadonnées du plugin, puis prépare les dépendances d'exécution uniquement pour les plugins appartenant à OpenClaw que le plan peut réellement charger.

Cette page couvre les dépendances d'exécution empaquetées pour les plugins groupés OpenClaw. Les plugins tiers et les chemins de plugins personnalisés utilisent toujours des commandes d'installation de plugins explicites telles que `openclaw plugins install` et `openclaw plugins update`.

## Répartition des responsabilités

OpenClaw possède le plan et la politique :

- quels plugins sont actifs pour cette configuration
- quelles racines de dépendances sont accessibles en écriture ou en lecture seule
- quand la réparation est autorisée
- quels identifiants de plugin sont préparés pour le démarrage
- vérifications finales avant l'importation des modules d'exécution du plugin

Le gestionnaire de paquets possède la convergence des dépendances :

- résolution du graphe de paquets
- gestion des dépendances de production, optionnelles et pairs
- disposition de `node_modules`
- intégrité des paquets
- métadonnées de verrouillage et d'installation

En pratique, OpenClaw doit décider ce qui doit exister. `pnpm` ou `npm` doit faire correspondre le système de fichiers à cette décision.

OpenClaw possède également le verrou de coordination par racine d'installation. Les gestionnaires de paquets protègent leur propre transaction d'installation, mais ils ne sérialisent pas les écritures de manifeste d'OpenClaw, la copie/renommage de l'étape isolée, la validation finale ou l'importation du plugin par rapport à une autre passerelle, un docteur ou un processus CLI touchant la même racine de dépendance d'exécution.

## Plan de plugin effectif

Le plan de plugin effectif est dérivé de la configuration plus les métadonnées de plugin découvertes. Ces entrées peuvent activer les dépendances d'exécution des plugins groupés :

- `plugins.entries.<id>.enabled`
- `plugins.allow`, `plugins.deny`, et `plugins.enabled`
- configuration de canal hérité telle que `channels.telegram.enabled`
- fournisseurs configurés, modèles ou références de backend CLI qui nécessitent un plugin
- valeurs par défaut du manifeste groupé telles que `enabledByDefault`
- l'index des plugins installés et les métadonnées du manifeste groupé

La désactivation explicite l'emporte. Un plugin désactivé, un identifiant de plugin refusé, un système de plugin désactivé ou un canal désactivé ne déclenche pas la réparation des dépendances d'exécution. L'état d'authentification persistant seul n'active pas non plus un canal ou un fournisseur groupé.

Le plan de plugin est l'entrée stable. La matérialisation des dépendances générées est une sortie de ce plan.

## Flux de démarrage

Le démarrage de la passerelle analyse la configuration et construit la table de recherche des plugins de démarrage avant le chargement des modules d'exécution du plugin. Le démarrage prépare ensuite les dépendances d'exécution uniquement pour les `startupPluginIds` sélectionnés par ce plan.

Pour les installations empaquetées, la préparation des dépendances est autorisée avant l'importation du plugin. Après la préparation, le chargeur d'exécution importe les plugins de démarrage avec la réparation d'installation désactivée ; à ce stade, la matérialisation des dépendances manquantes est traitée comme une défaillance de chargement, et non comme une autre boucle de réparation.

Lorsque la préparation des dépendances de démarrage est différée derrière la liaison HTTP, la disponibilité de la passerelle reste bloquée sur la raison `plugin-runtime-deps` jusqu'à ce que les dépendances de plugin de démarrage sélectionnées soient matérialisées et que l'exécution du plugin de démarrage soit chargée.

## Quand la réparation s'exécute

La réparation des dépendances d'exécution doit s'exécuter quand l'une de ces conditions est vraie :

- le plan de plugin effectif a changé et ajoute des plugins groupés qui ont besoin de dépendances d'exécution
- le manifeste de dépendances généré ne correspond plus au plan effectif
- les sentinelles de paquets installés attendues sont manquantes ou incomplètes
- `openclaw doctor --fix` ou `openclaw plugins deps --repair` a été demandé

La réparation des dépendances d'exécution ne doit pas s'exécuter simplement parce qu'OpenClaw a démarré. Un démarrage normal avec un plan inchangé et une matérialisation complète des dépendances doit ignorer le travail du gestionnaire de paquets.

Les commandes qui modifient la configuration, activent les plugins ou réparent les résultats du docteur peuvent entrer en mode plan de plugin une fois, matérialiser les dépendances de plugin groupées nouvellement requises, puis revenir au flux de commande normal. Les `openclaw onboard` et `openclaw configure` locaux le font automatiquement après avoir écrit avec succès la configuration, de sorte que la prochaine exécution de la passerelle ne découvre pas les paquets de plugins groupés manquants après que le démarrage ait déjà commencé. L'intégration/configuration à distance reste en lecture seule pour les dépendances d'exécution locales.

## Règle de rechargement à chaud

Les chemins de rechargement à chaud qui peuvent modifier les plugins actifs doivent revenir en mode plan de plugin avant de charger l'exécution du plugin. Le rechargement doit comparer le nouveau plan de plugin effectif avec le précédent, préparer les dépendances manquantes pour les plugins groupés nouvellement actifs, puis charger ou redémarrer l'exécution affectée.

Si un rechargement de configuration ne change pas le plan de plugin effectif, il ne doit pas réparer les dépendances d'exécution des plugins groupés.

## Exécution du gestionnaire de paquets

OpenClaw écrit un manifeste d'installation généré pour les dépendances d'exécution des plugins groupés sélectionnés et exécute le gestionnaire de paquets dans la racine d'installation des dépendances d'exécution. Il préfère `pnpm` quand il est disponible et revient au coureur `npm` fourni avec Node.

Le chemin `pnpm` utilise les dépendances de production, désactive les scripts de cycle de vie, ignore l'espace de travail et garde le magasin à l'intérieur de la racine d'installation :

```bash
pnpm install \
  --prod \
  --ignore-scripts \
  --ignore-workspace \
  --config.frozen-lockfile=false \
  --config.minimum-release-age=0 \
  --config.store-dir=<install-root>/.openclaw-pnpm-store \
  --config.node-linker=hoisted \
  --config.virtual-store-dir=.pnpm
```

Le secours `npm` utilise le wrapper d'installation npm sécurisé avec les dépendances de production, les scripts de cycle de vie désactivés, le mode espace de travail désactivé, l'audit désactivé, la sortie de financement désactivée, le comportement de dépendance pair hérité et la sortie de verrouillage de paquet activée pour la racine d'installation générée.

Après l'installation, OpenClaw valide l'arborescence des dépendances préparées avant de la rendre visible à la racine des dépendances d'exécution. La préparation isolée est copiée dans la racine des dépendances d'exécution et validée à nouveau.

Toute la section de réparation/matérialisation est protégée par un verrou de racine d'installation. Les propriétaires de verrous actuels enregistrent le PID, l'heure de démarrage du processus quand elle est disponible et l'heure de création. Les verrous hérités sans preuve d'heure de démarrage du processus ou d'heure de création ne sont reclamés que par l'ancienneté du système de fichiers, de sorte que les verrous PID 1 Docker recyclés se récupèrent sans expirer les installations actuelles longues en cours simplement par l'ancienneté.

## Racines d'installation

Les installations empaquetées ne doivent pas muter les répertoires de paquets en lecture seule. OpenClaw peut lire les racines de dépendances à partir de couches empaquetées, mais écrit les dépendances d'exécution générées dans une étape accessible en écriture telle que :

- `OPENCLAW_PLUGIN_STAGE_DIR`
- `$STATE_DIRECTORY`
- `~/.openclaw/plugin-runtime-deps`
- `/var/lib/openclaw/plugin-runtime-deps` dans les installations de style conteneur

La racine accessible en écriture est la cible de matérialisation finale. Les racines en lecture seule plus anciennes sont conservées comme couches de compatibilité uniquement si nécessaire.

Quand une mise à jour empaquetée d'OpenClaw change la racine accessible en écriture versionnée mais que le plan de dépendances de plugin groupé sélectionné est toujours satisfait par une racine préparée précédente, la réparation réutilise cette arborescence `node_modules` précédente au lieu d'exécuter le gestionnaire de paquets à nouveau. La nouvelle racine versionnée obtient toujours son propre miroir d'exécution de paquet actuel, de sorte que le code du plugin provient du paquet OpenClaw actuel tandis que les arborescences de dépendances inchangées sont partagées entre les mises à jour. La réutilisation ignore les racines précédentes avec un verrou de dépendance d'exécution OpenClaw actif, de sorte qu'une nouvelle racine ne se lie pas à une arborescence de dépendances qu'une autre passerelle, un docteur ou un processus CLI répare actuellement.

## Commandes Docteur et CLI

Utilisez `plugins deps` pour inspecter ou réparer la matérialisation des dépendances d'exécution des plugins groupés :

```bash
openclaw plugins deps
openclaw plugins deps --json
openclaw plugins deps --repair
openclaw plugins deps --prune
```

Utilisez le docteur quand l'état des dépendances fait partie de la santé d'installation plus large :

```bash
openclaw doctor
openclaw doctor --fix
```

`plugins deps` et le docteur opèrent sur les dépendances d'exécution des plugins groupés appartenant à OpenClaw sélectionnés par le plan de plugin effectif. Ce ne sont pas des commandes d'installation ou de mise à jour de plugins tiers.

## Dépannage

Si une installation empaquetée signale des dépendances d'exécution de plugins groupés manquantes :

1. Exécutez `openclaw plugins deps --json` pour inspecter le plan sélectionné et les paquets manquants.
2. Exécutez `openclaw plugins deps --repair` ou `openclaw doctor --fix` pour réparer l'étape de dépendances accessible en écriture.
3. Si la racine d'installation est en lecture seule, définissez `OPENCLAW_PLUGIN_STAGE_DIR` sur un chemin accessible en écriture et réexécutez la réparation.
4. Redémarrez la passerelle après la réparation si la dépendance manquante a bloqué le chargement du plugin de démarrage.

Dans les extraits de source, l'installation de l'espace de travail fournit généralement les dépendances des plugins groupés. Exécutez `pnpm install` pour la réparation des dépendances de source au lieu d'utiliser la réparation des dépendances d'exécution empaquetées comme première étape.
