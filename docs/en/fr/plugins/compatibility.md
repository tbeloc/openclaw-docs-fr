---
summary: "Contrats de compatibilité des plugins, métadonnées de dépréciation et attentes de migration"
title: "Compatibilité des plugins"
read_when:
  - You maintain an OpenClaw plugin
  - You see a plugin compatibility warning
  - You are planning a plugin SDK or manifest migration
---

OpenClaw maintient les anciens contrats de plugins câblés via des adaptateurs de compatibilité nommés avant de les supprimer. Cela protège les plugins groupés et externes existants tandis que les contrats du SDK, du manifeste, de la configuration, de la configuration et du runtime de l'agent évoluent.

## Registre de compatibilité

Les contrats de compatibilité des plugins sont suivis dans le registre principal à `src/plugins/compat/registry.ts`.

Chaque enregistrement contient :

- un code de compatibilité stable
- statut : `active`, `deprecated`, `removal-pending`, ou `removed`
- propriétaire : SDK, config, setup, channel, provider, exécution de plugin, runtime de l'agent, ou core
- dates d'introduction et de dépréciation le cas échéant
- conseils de remplacement
- docs, diagnostics et tests couvrant l'ancien et le nouveau comportement

Le registre est la source pour la planification des mainteneurs et les futurs contrôles de l'inspecteur de plugins. Si un comportement visible par les plugins change, ajoutez ou mettez à jour l'enregistrement de compatibilité dans le même changement qui ajoute l'adaptateur.

## Package d'inspecteur de plugins

L'inspecteur de plugins doit résider en dehors du référentiel principal d'OpenClaw en tant que package/référentiel séparé soutenu par les contrats de compatibilité et de manifeste versionnés.

La CLI du jour un devrait être :

```sh
openclaw-plugin-inspector ./my-plugin
```

Elle devrait émettre :

- validation du manifeste/schéma
- la version de compatibilité du contrat en cours de vérification
- vérifications des métadonnées d'installation/source
- vérifications d'importation du chemin froid
- avertissements de dépréciation et de compatibilité

Utilisez `--json` pour une sortie stable lisible par machine dans les annotations CI. Le cœur d'OpenClaw doit exposer les contrats et les fixtures que l'inspecteur peut consommer, mais ne doit pas publier le binaire de l'inspecteur à partir du package principal `openclaw`.

## Politique de dépréciation

OpenClaw ne doit pas supprimer un contrat de plugin documenté dans la même version que celle qui introduit son remplacement.

La séquence de migration est :

1. Ajouter le nouveau contrat.
2. Garder l'ancien comportement câblé via un adaptateur de compatibilité nommé.
3. Émettre des diagnostics ou des avertissements quand les auteurs de plugins peuvent agir.
4. Documenter le remplacement et le calendrier.
5. Tester les deux chemins, ancien et nouveau.
6. Attendre la fenêtre de migration annoncée.
7. Supprimer uniquement avec approbation explicite de version de rupture.

Les enregistrements dépréciés doivent inclure une date de début d'avertissement, un remplacement, un lien de documentation et une date de suppression cible si connue.

## Domaines de compatibilité actuels

Les enregistrements de compatibilité actuels incluent :

- les importations SDK larges héritées telles que `openclaw/plugin-sdk/compat`
- les formes de plugins héritées basées sur les hooks uniquement et `before_agent_start`
- le comportement de liste blanche et d'activation des plugins groupés
- les métadonnées du manifeste des variables d'environnement du fournisseur/canal héritées
- les indices d'activation qui sont remplacés par la propriété de contribution du manifeste
- les alias de nommage `embeddedHarness` et `agent-harness` tandis que le nommage public se déplace vers `agentRuntime`
- le repli des métadonnées de configuration de canal groupé générées tandis que les métadonnées `channelConfigs` basées sur le registre arrivent

Le nouveau code de plugin doit préférer le remplacement listé dans le registre et dans le guide de migration spécifique. Les plugins existants peuvent continuer à utiliser un chemin de compatibilité jusqu'à ce que la documentation, les diagnostics et les notes de version annoncent une fenêtre de suppression.

## Notes de version

Les notes de version doivent inclure les dépréciations de plugins à venir avec les dates cibles et les liens vers la documentation de migration. Cet avertissement doit se produire avant qu'un chemin de compatibilité ne passe à `removal-pending` ou `removed`.
