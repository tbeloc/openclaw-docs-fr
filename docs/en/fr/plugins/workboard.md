---
summary: "Tableau de bord facultatif pour les cartes détenues par des agents et le transfert de session"
read_when:
  - You want a Kanban-style workboard in the Control UI
  - You are enabling or disabling the bundled Workboard plugin
  - You want to track planned agent work without an external project manager
title: "Plugin Workboard"
---

Le plugin Workboard ajoute un tableau de style Kanban facultatif à l'
[interface de contrôle](/fr/web/control-ui). Utilisez-le pour collecter des cartes de travail à l'échelle des agents, les assigner à des agents et accéder à la session de tableau de bord liée à partir d'une carte.

Workboard est intentionnellement minimaliste. Il suit le travail opérationnel local pour une passerelle OpenClaw ; ce n'est pas un remplacement pour GitHub Issues, Linear, Jira ou d'autres systèmes de gestion de projet d'équipe.

## État par défaut

Workboard est un plugin fourni et est désactivé par défaut sauf si vous l'activez dans la configuration des plugins.

Activez-le avec :

```bash
openclaw plugins enable workboard
openclaw gateway restart
```

Ouvrez ensuite le tableau de bord :

```bash
openclaw dashboard
```

L'onglet Workboard apparaît dans la navigation du tableau de bord. Si l'onglet est visible mais que le plugin est désactivé ou bloqué par `plugins.allow` / `plugins.deny`, la vue affiche un état de plugin indisponible au lieu des données de cartes locales.

## Contenu des cartes

Chaque carte stocke :

- titre et notes
- statut : `backlog`, `todo`, `running`, `review`, `blocked` ou `done`
- priorité : `low`, `normal`, `high` ou `urgent`
- étiquettes
- identifiant d'agent facultatif
- session, exécution, tâche ou URL source liée facultative
- métadonnées d'exécution facultatives pour une session Codex ou Claude démarrée à partir de la carte
- métadonnées compactes pour les tentatives, commentaires, liens, preuves, modèles, état d'archivage et détection de session obsolète
- événements récents de la carte tels que créé, déplacé, lié, tentative, preuve, archivage, obsolète ou modifications mises à jour par l'agent

Les cartes sont stockées dans l'état de la passerelle du plugin. Elles sont locales au répertoire d'état de la passerelle et se déplacent avec le reste de l'état OpenClaw de cette passerelle.

Workboard conserve des métadonnées compactes par carte afin que les opérateurs puissent voir comment une carte s'est déplacée sur le tableau sans ouvrir la session liée. Les événements, résumés de tentatives, extraits de preuves, liens connexes, commentaires, marqueurs d'archivage et marqueurs de session obsolète sont intentionnellement des métadonnées locales ; ils ne remplacent pas les transcriptions de session ou l'historique des problèmes GitHub.

## Exécutions de cartes

Les cartes non liées peuvent démarrer le travail à partir de la carte. Le démarrage utilise l'agent par défaut configuré et le modèle de la passerelle. Les actions Codex et Claude sont des choix de modèle explicites facultatifs :

- Exécuter Codex ou Exécuter Claude crée une session de tableau de bord, envoie l'invite de la carte et marque la carte `running`.
- Ouvrir Codex ou Ouvrir Claude crée une session de tableau de bord liée sans envoyer l'invite de la carte ni déplacer la carte, afin que vous puissiez travailler manuellement tandis qu'elle reste attachée au tableau.

Les métadonnées d'exécution stockent le moteur sélectionné, le mode, la référence du modèle, la clé de session, l'identifiant d'exécution et l'état du cycle de vie sur la carte. Les exécutions Codex utilisent `openai/gpt-5.5` ; les exécutions Claude utilisent `anthropic/claude-sonnet-4-6`.

Chaque exécution liée enregistre également un résumé de tentative sur le même enregistrement de carte. Le résumé de tentative conserve le moteur, le mode, le modèle, l'identifiant d'exécution, les horodatages, l'état et le nombre d'échecs cumulatif afin que les échecs répétés restent visibles sur le tableau.

## Synchronisation du cycle de vie de la session

Les cartes peuvent être liées à des sessions de tableau de bord existantes ou à la session créée lorsque vous démarrez le travail à partir d'une carte. Les cartes liées affichent le cycle de vie de la session en ligne : en cours d'exécution, obsolète, inactif lié, terminé, échoué ou manquant.

Si la session liée est manquante, la carte reste liée pour le contexte et offre toujours des contrôles de démarrage afin que vous puissiez redémarrer le travail dans une nouvelle session de tableau de bord. Si une session liée active cesse de signaler une activité récente, Workboard marque la carte comme obsolète et stocke le marqueur en tant que métadonnées de carte jusqu'à ce que le cycle de vie l'efface.

Vous pouvez également capturer une session de tableau de bord existante à partir de l'onglet Sessions avec Ajouter à Workboard. La carte est liée à cette session, utilise l'étiquette de session ou l'invite utilisateur récente comme titre et amorce les notes à partir de l'invite utilisateur récente plus la dernière réponse de l'assistant lorsque l'historique de chat est disponible.

Workboard suit la session liée tandis que la carte est toujours dans un état de travail actif :

- session liée active -> `running`
- session liée complétée -> `review`
- session liée échouée, tuée, expirée ou abandonnée -> `blocked`

Les états d'examen manuel gagnent. Si vous déplacez une carte vers `review`, `blocked` ou `done`, Workboard arrête de déplacer automatiquement cette carte jusqu'à ce que vous la remettiez à `todo` ou `running`.

## Flux de travail du tableau de bord

1. Ouvrez l'onglet Workboard dans l'interface de contrôle.
2. Créez une carte avec un titre, des notes, une priorité, des étiquettes, un agent facultatif et une session liée facultative.
3. Ou ouvrez Sessions et choisissez Ajouter à Workboard pour une session existante.
4. Faites glisser la carte entre les colonnes ou utilisez les contrôles de colonne.
5. Démarrez le travail à partir de la carte pour créer ou réutiliser une session de tableau de bord.
6. Ouvrez la session liée à partir de la carte pendant que l'agent travaille.
7. Laissez la synchronisation du cycle de vie déplacer le travail en cours vers l'examen ou le blocage, puis déplacez manuellement la carte vers terminé lorsqu'elle est acceptée.

Le démarrage d'une carte utilise les sessions normales de la passerelle. Le plugin Workboard stocke uniquement les métadonnées et les liens de carte ; la transcription de conversation, la sélection du modèle et le cycle de vie d'exécution restent la propriété du système de session régulier.

Utilisez Arrêter sur une carte liée active pour abandonner l'exécution de session active. Workboard marque cette carte `blocked` afin qu'elle reste visible pour le suivi.

Les nouvelles cartes peuvent démarrer à partir de modèles Workboard pour les corrections de bogues, la documentation, les versions, les révisions de PR ou le travail sur les plugins. Les modèles préremplissent le titre, les notes, les étiquettes et la priorité, et l'identifiant de modèle sélectionné est stocké en tant que métadonnées de carte.

## Permissions

Le plugin enregistre les méthodes RPC de la passerelle sous l'espace de noms `workboard.*` :

- `workboard.cards.list` nécessite `operator.read`
- `workboard.cards.export` nécessite `operator.read`
- les méthodes de création, mise à jour, déplacement, suppression, commentaire, liaison, preuve et archivage nécessitent `operator.write`

Les navigateurs connectés avec un accès opérateur en lecture seule peuvent inspecter le tableau mais ne peuvent pas modifier les cartes.

## Configuration

Workboard n'a pas de configuration spécifique au plugin aujourd'hui. Activez ou désactivez-le avec l'entrée de plugin standard :

```json5
{
  plugins: {
    entries: {
      workboard: {
        enabled: true,
        config: {},
      },
    },
  },
}
```

Désactivez-le à nouveau avec :

```bash
openclaw plugins disable workboard
openclaw gateway restart
```

## Dépannage

### L'onglet indique que Workboard est indisponible

Vérifiez la politique des plugins :

```bash
openclaw plugins inspect workboard --runtime --json
```

Si `plugins.allow` est configuré, ajoutez `workboard` à cette liste d'autorisation. Si `plugins.deny` contient `workboard`, supprimez-le avant d'activer le plugin.

### Les cartes ne s'enregistrent pas

Confirmez que la connexion du navigateur a un accès `operator.write`. Les sessions d'opérateur en lecture seule peuvent lister les cartes mais ne peuvent pas les créer, les modifier, les déplacer ou les supprimer.

### Le démarrage d'une carte n'ouvre pas la session attendue

Workboard crée des liens vers des sessions de tableau de bord normales. Vérifiez l'identifiant d'agent et la session liée de la carte, puis ouvrez la vue Sessions ou Chat pour inspecter l'état d'exécution réel.

## Connexes

- [Interface de contrôle](/fr/web/control-ui)
- [Plugins](/fr/tools/plugin)
- [Gérer les plugins](/fr/plugins/manage-plugins)
- [Sessions](/fr/concepts/session)
