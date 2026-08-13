---
title: "Portails"
summary: "Exposer les serveurs de développement exécutés par l'agent à l'opérateur via la Gateway"
read_when:
  - Showing a development server in the Control UI
  - Declaring workspace development servers for an agent
  - Troubleshooting portal access or live reload
---

Les portails exposent un serveur de développement s'exécutant sur l'hôte Gateway au navigateur de l'opérateur. Ils mandatent HTTP et WebSockets pour le rechargement en direct et apparaissent dans **Control UI → Portails**.

## Démarrage rapide

Demandez à l'agent d'ouvrir un portail :

- « Montre-moi dans un portail. »
- « Démarre l'application dans un portail. »

L'agent ouvre un portail pour le port de l'application, puis démarre le serveur de développement avec un appel `exec` en arrière-plan. L'ouverture d'un portail crée uniquement l'écouteur proxy ; elle n'injecte pas de variables d'environnement dans votre serveur. L'agent définit `PORT` (le port qu'il a ouvert) et `PUBLIC_URL` (l'URL de base publique du portail) dans l'environnement de la commande `exec` elle-même, afin que l'application se lie au port attendu et génère les bonnes URL absolues.

## Déclarer les serveurs de développement

Validez optionnellement `.openclaw/portals.json` dans le référentiel de l'espace de travail afin que l'agent puisse découvrir les serveurs de développement disponibles :

```json
{
  "portals": [
    {
      "name": "web",
      "command": "pnpm dev",
      "cwd": ".",
      "port": 3000,
      "title": "App",
      "description": "Use the seeded test account."
    }
  ]
}
```

La Gateway n'exécute jamais ces commandes automatiquement. L'agent lit le fichier et décide quand exécuter un serveur déclaré.

| Champ         | Requis | Description                                                    |
| ------------- | ------ | -------------------------------------------------------------- |
| `name`        | oui    | Nom stable que l'agent utilise pour identifier le serveur.     |
| `command`     | oui    | Commande que l'agent démarre avec `exec` en arrière-plan.      |
| `port`        | oui    | Port TCP local sur lequel l'application écoute.                |
| `cwd`         | non    | Répertoire de travail relatif à la racine de l'espace de travail. |
| `title`       | non    | Titre d'affichage montré sur la page Portails.                 |
| `description` | non    | Conseils pour l'opérateur affichés à côté du portail.          |
| `path`        | non    | Chemin d'URL initial. Il doit commencer par `/`.               |

## Contrat d'application

L'application doit respecter `PORT`. Utilisez `PUBLIC_URL` quand elle doit générer des URL absolues.

Le proxy réécrit `Host` vers la cible locale, donc les serveurs de développement typiques comme Vite et Next.js n'ont besoin d'aucune configuration supplémentaire. Les WebSockets et le remplacement de module à chaud sont mandatés via le même portail.

## Disponibilité et configuration

Les portails n'ajoutent aucune clé de configuration dédiée. L'outil `portal` suit la politique ordinaire des outils, décrite dans [Configuration des outils](/fr/gateway/config-tools).

Par défaut :

- `portal` appartient à `group:ui` et au profil `coding`, donc les agents de codage l'ont tandis que les agents `messaging` et `minimal` ne l'ont pas.
- Les sessions en bac à sable ne le reçoivent jamais, car l'ouverture d'un portail démarre un écouteur sur l'hôte Gateway.
- Il est bloqué pour HTTP `POST /tools/invoke` et limité au propriétaire de la session, le même traitement que `terminal`.

Pour désactiver les portails partout, refusez l'outil dans la politique globale :

```json5
{
  tools: { deny: ["portal"] },
}
```

Pour les désactiver pour un seul agent, en laissant les autres inchangés :

```json5
{
  agents: { entries: { "<agentId>": { tools: { deny: ["portal"] } } } },
}
```

`tools.profile`, `tools.allow`, `byProvider` et `toolsBySender` s'appliquent à `portal` comme à tout autre outil, donc les portails peuvent également être limités à des fournisseurs, modèles ou expéditeurs spécifiques sans paramètre spécifique au portail.

Une conséquence à planifier : les écouteurs de portail se lient aux mêmes interfaces que la Gateway. Une Gateway liée à une adresse LAN ou tailnet publie également ses ports d'écouteur de portail sur ce réseau. L'accès à l'un d'eux nécessite toujours le jeton dans l'URL du portail, mais refusez l'outil quand l'hôte Gateway ne doit pas offrir de ports d'application accessibles à l'opérateur du tout.

## Modèle de sécurité

Chaque portail utilise une origine séparée sur son propre port et se lie aux mêmes interfaces que la Gateway. L'accès nécessite le jeton dans l'URL du portail. À la première requête, le proxy stocke ce jeton dans un cookie HttpOnly et le supprime des requêtes en amont suivantes. Le proxy valide ce cookie lui-même et ne le transmet jamais à l'application.

Les cookies du navigateur sont limités au nom d'hôte plutôt qu'au port, donc le proxy isole le pot de cookies de chaque application avec un préfixe de nom `oc_portal_<targetPort>_`. Les requêtes ne transmettent que les cookies avec le préfixe de ce portail et le suppriment avant d'atteindre l'application ; les cookies Gateway, les cookies sans préfixe et les cookies pour d'autres portails sont supprimés. Les réponses `Set-Cookie` de l'application reçoivent le préfixe, et tout attribut `Domain` est supprimé afin que le cookie reste limité à l'hôte.

Les portails mandatent uniquement le serveur de développement local sélectionné. Ils ne servent jamais les données Gateway, et chaque portail se termine quand la Gateway redémarre.

## Limitations

- Le serveur de développement doit s'exécuter sur l'hôte Gateway. Le support des workers distants est prévu.
- Un proxy ou tunnel devant la Gateway n'expose pas automatiquement les ports d'écouteur de portail. L'interface Control UI détecte cela et affiche une URL accessible avec des conseils de nouvelle tentative au lieu de monter une iframe morte.
- Le code côté navigateur voit les noms avec préfixe dans `document.cookie`. Les applications qui gèrent les cookies dans le code du navigateur doivent tenir compte du préfixe ; les cookies sans préfixe écrits directement par le code du navigateur ne sont pas transmis à la cible.

## Dépannage

### Le portail affiche une page d'attente 502

Le proxy est prêt, mais l'application n'écoute pas sur le port sélectionné. La page réessaie automatiquement. Vérifiez le processus en arrière-plan et confirmez que le serveur respecte `PORT`.

### Le portail n'est pas accessible depuis ce navigateur

L'interface Control UI a pu atteindre la Gateway mais n'a pas pu atteindre le port d'écouteur séparé du portail. Cela se produit couramment quand un proxy ou tunnel n'expose que le port Gateway principal. Ouvrez l'URL du portail affichée depuis un navigateur sur l'hôte Gateway, ou exposez ce port d'écouteur de portail via le même chemin réseau, puis sélectionnez **Réessayer**.

### Fermer un portail

Demandez à l'agent de « fermer le portail », ou utilisez le bouton de fermeture sur la page **Control UI → Portails**.
