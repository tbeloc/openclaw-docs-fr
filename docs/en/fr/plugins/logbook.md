---
summary: "Journal de travail automatique optionnel construit à partir d'instantanés d'écran périodiques"
read_when:
  - You want a Dayflow-style timeline of your day in the Control UI
  - You are enabling or configuring the bundled Logbook plugin
  - You want standup summaries or day recall grounded in screen activity
title: "Plugin Logbook"
---

Le plugin Logbook transforme l'activité d'écran en un journal de travail automatique. Il
capture des instantanés d'écran périodiques à partir d'un nœud appairé (par exemple l'application
Mac OpenClaw), les résume avec un modèle de vision en observations horodatées,
et les synthétise en cartes de chronologie que vous pouvez parcourir dans l'
[Interface de contrôle](/fr/web/control-ui). En plus de la chronologie, il génère des notes
de standup quotidiennes et répond à des questions sur votre journée.

Tout reste local : les instantanés et la base de données de chronologie se trouvent sous
le répertoire d'état de la passerelle. Seuls les lots d'analyse sont envoyés au modèle que vous
configurez, alors choisissez un modèle local si les instantanés ne doivent jamais quitter la machine.

## État par défaut

Logbook est un plugin fourni et est désactivé par défaut. La capture d'écran est
optionnelle.

Activez-le avec :

```bash
openclaw plugins enable logbook
openclaw gateway restart
```

Puis ouvrez le tableau de bord et sélectionnez l'onglet Logbook :

```bash
openclaw dashboard
```

L'onglet Logbook est fourni via la surface d'onglet de l'interface de contrôle du plugin
(`registerControlUiDescriptor` avec `surface: "tab"`), il apparaît donc dans la
barre latérale uniquement lorsque le plugin est activé sur la passerelle connectée.

## Exigences

- Un nœud connecté capable de capturer l'écran. Le nœud de l'application macOS annonce
  `screen.snapshot` par défaut (voir [Nœuds](/fr/nodes)) ; les hôtes de nœud macOS sans interface
  (`openclaw node host run`) obtiennent une commande `logbook.snapshot` fournie par le plugin
  soutenue par l'outil système `screencapture` lorsque Logbook est activé.
- Un modèle de vision dont le fournisseur de compréhension des médias supporte l'extraction
  structurée (le plugin Codex fourni le fait, par exemple `codex/gpt-5.5`).
  Logbook résout le modèle dans cet ordre :
  1. `plugins.entries.logbook.config.visionModel` (référence `"provider/model"`)
  2. la première entrée Codex capable de traiter les images sous `tools.media.image.models` ou
     `tools.media.models` (les autres fournisseurs de médias n'exposent pas actuellement le
     contrat d'extraction structurée que Logbook nécessite)
- La synthèse des cartes de chronologie, les notes de standup et les réponses « interrogez votre journée »
  utilisent le modèle d'agent par défaut via le runtime LLM du plugin.

## Fonctionnement

1. **Capture** : tous les `captureIntervalSeconds` (30s par défaut) Logbook invoque
   `screen.snapshot` sur le nœud de capture et stocke une image JPEG mise à l'échelle.
   Les images consécutives identiques sont marquées comme inactives et exclues de l'analyse.
2. **Observation** : une fois qu'une fenêtre d'analyse (15 minutes par défaut) s'écoule, les
   images sont envoyées au modèle de vision, qui retourne des observations d'activité horodatées
   (« VS Code : édition de store.ts, correction d'une erreur de type »).
3. **Synthèse** : les observations plus les 45 dernières minutes de cartes existantes sont
   révisées en cartes de chronologie (10-60 minutes chacune) avec un titre, un résumé,
   une catégorie, l'application principale et toute brève distraction.
4. **Élagage** : les images plus anciennes que `retentionDays` (14 par défaut) sont supprimées.
   Les cartes, observations et standups sont conservés.

Les images et la base de données de chronologie se trouvent sous `<state-dir>/logbook/`.

## Configuration

```json
{
  "plugins": {
    "entries": {
      "logbook": {
        "enabled": true,
        "config": {
          "captureIntervalSeconds": 30,
          "analysisIntervalMinutes": 15,
          "screenIndex": 0,
          "maxWidth": 1440,
          "nodeId": "my-mac",
          "visionModel": "codex/gpt-5.5",
          "retentionDays": 14,
          "captureEnabled": true
        }
      }
    }
  }
}
```

Toutes les clés sont optionnelles. Laissez `nodeId` non défini pour utiliser le premier nœud connecté
qui supporte `screen.snapshot`. Définissez `captureEnabled: false` pour garder l'interface
de chronologie disponible sans capture ; le tableau de bord a aussi un bouton de pause pour la session.

## Onglet du tableau de bord

- **Chronologie** : cartes extensibles par activité avec couleurs de catégorie, l'application
  principale, des puces de distraction et une image clé d'instantané.
- **Aperçu de la journée** : ratio de concentration, répartition des catégories, applications principales.
- **Standup quotidien** : transforme hier et aujourd'hui en une mise à jour prête à coller.
- **Interrogez votre journée** : questions en langage naturel répondues à partir de la
  chronologie suivie (« quand ai-je examiné la PR de la passerelle ? »).
- **Analyser maintenant** : ferme la fenêtre de capture actuelle immédiatement au lieu
  d'attendre l'intervalle d'analyse.

## Méthodes de passerelle

Logbook enregistre les méthodes RPC de passerelle pour le tableau de bord. `logbook.status`,
`logbook.days` et `logbook.timeline` retournent du texte dérivé et sont lisibles
avec `operator.read`. Tout ce qui retourne des pixels d'écran bruts
(`logbook.frames`, `logbook.frame`), dépense des jetons de modèle (`logbook.standup`,
`logbook.ask`), ou mute l'état du runtime (`logbook.capture.set`,
`logbook.analyze.now`) nécessite `operator.write`. L'onglet Interface de contrôle nécessite
`operator.write` car la vue fournie expose ces actions et les aperçus d'images brutes ;
les clients en lecture seule peuvent appeler directement les méthodes de texte dérivé.

## Notes de confidentialité

- Les instantanés peuvent contenir n'importe quoi à l'écran, y compris des secrets. Les images ne
  quittent jamais la machine sauf comme entrée de modèle pour les lots d'analyse.
- Utilisez un fournisseur d'extraction structurée qui s'exécute localement, lorsqu'il est disponible et
  explicitement configuré, pour un pipeline entièrement sur l'appareil.
- Les images, la base de données de chronologie et les captures temporaires sont écrites avec
  des permissions de fichier réservées au propriétaire.
- Ajouter `screen.snapshot` à `gateway.nodes.denyCommands` est le
  bouton d'arrêt de capture d'écran : il bloque la capture d'application-nœud et la propre
  commande `logbook.snapshot` de Logbook.
- Définir `tools.media.image.enabled: false` arrête également Logbook d'emprunter
  les modèles d'image de médias pour l'analyse ; seul un `visionModel` explicite dans la
  configuration du plugin est utilisé alors.
