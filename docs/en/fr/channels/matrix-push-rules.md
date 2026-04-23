---
summary: "Règles de notification Matrix par destinataire pour les modifications d'aperçu finalisées en mode silencieux"
read_when:
  - Setting up Matrix quiet streaming for self-hosted Synapse or Tuwunel
  - Users want notifications only on finished blocks, not on every preview edit
title: "Règles de notification Matrix pour les aperçus silencieux"
---

# Règles de notification Matrix pour les aperçus silencieux

Quand `channels.matrix.streaming` est `"quiet"`, OpenClaw modifie un seul événement d'aperçu sur place et marque la modification finalisée avec un drapeau de contenu personnalisé. Les clients Matrix envoient une notification sur la modification finale uniquement si une règle de notification par utilisateur correspond à ce drapeau. Cette page est destinée aux opérateurs qui auto-hébergent Matrix et souhaitent installer cette règle pour chaque compte destinataire.

Si vous ne voulez que le comportement de notification Matrix standard, utilisez `streaming: "partial"` ou laissez le streaming désactivé. Voir [Configuration du canal Matrix](/fr/channels/matrix#streaming-previews).

## Prérequis

- utilisateur destinataire = la personne qui doit recevoir la notification
- utilisateur bot = le compte Matrix OpenClaw qui envoie la réponse
- utilisez le jeton d'accès de l'utilisateur destinataire pour les appels API ci-dessous
- faites correspondre `sender` dans la règle de notification avec le MXID complet de l'utilisateur bot
- le compte destinataire doit déjà avoir des pushers fonctionnels — les règles d'aperçu silencieux ne fonctionnent que lorsque la livraison de notification Matrix normale est saine

## Étapes

<Steps>
  <Step title="Configurer les aperçus silencieux">

```json5
{
  channels: {
    matrix: {
      streaming: "quiet",
    },
  },
}
```

  </Step>

  <Step title="Obtenir le jeton d'accès du destinataire">
    Réutilisez un jeton de session client existant si possible. Pour en créer un nouveau :

```bash
curl -sS -X POST \
  "https://matrix.example.org/_matrix/client/v3/login" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "m.login.password",
    "identifier": { "type": "m.id.user", "user": "@alice:example.org" },
    "password": "REDACTED"
  }'
```

  </Step>

  <Step title="Vérifier que les pushers existent">

```bash
curl -sS \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" \
  "https://matrix.example.org/_matrix/client/v3/pushers"
```

Si aucun pusher n'est retourné, corrigez la livraison de notification Matrix normale pour ce compte avant de continuer.

  </Step>

  <Step title="Installer la règle de notification de remplacement">
    OpenClaw marque les modifications d'aperçu finalisées en texte uniquement avec `content["com.openclaw.finalized_preview"] = true`. Installez une règle qui correspond à ce marqueur plus le MXID du bot en tant qu'expéditeur :

```bash
curl -sS -X PUT \
  "https://matrix.example.org/_matrix/client/v3/pushrules/global/override/openclaw-finalized-preview-botname" \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "conditions": [
      { "kind": "event_match", "key": "type", "pattern": "m.room.message" },
      {
        "kind": "event_property_is",
        "key": "content.m\\.relates_to.rel_type",
        "value": "m.replace"
      },
      {
        "kind": "event_property_is",
        "key": "content.com\\.openclaw\\.finalized_preview",
        "value": true
      },
      { "kind": "event_match", "key": "sender", "pattern": "@bot:example.org" }
    ],
    "actions": [
      "notify",
      { "set_tweak": "sound", "value": "default" },
      { "set_tweak": "highlight", "value": false }
    ]
  }'
```

    Remplacez avant d'exécuter :

    - `https://matrix.example.org` : l'URL de base de votre serveur d'accueil
    - `$USER_ACCESS_TOKEN` : le jeton d'accès de l'utilisateur destinataire
    - `openclaw-finalized-preview-botname` : un ID de règle unique par bot par destinataire (modèle : `openclaw-finalized-preview-<botname>`)
    - `@bot:example.org` : votre MXID de bot OpenClaw, pas celui du destinataire

  </Step>

  <Step title="Vérifier">

```bash
curl -sS \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" \
  "https://matrix.example.org/_matrix/client/v3/pushrules/global/override/openclaw-finalized-preview-botname"
```

Ensuite, testez une réponse en streaming. En mode silencieux, la salle affiche un aperçu de brouillon silencieux et envoie une notification une fois que le bloc ou le tour est terminé.

  </Step>
</Steps>

Pour supprimer la règle ultérieurement, `DELETE` la même URL de règle avec le jeton du destinataire.

## Notes sur les bots multiples

Les règles de notification sont indexées par `ruleId` : réexécuter `PUT` contre le même ID met à jour une seule règle. Pour plusieurs bots OpenClaw notifiant le même destinataire, créez une règle par bot avec une correspondance d'expéditeur distincte.

Les nouvelles règles `override` définies par l'utilisateur sont insérées avant les règles de suppression par défaut, donc aucun paramètre de classement supplémentaire n'est nécessaire. La règle n'affecte que les modifications d'aperçu en texte uniquement qui peuvent être finalisées sur place ; les solutions de secours pour les médias et les solutions de secours pour les aperçus obsolètes utilisent la livraison Matrix normale.

## Notes sur le serveur d'accueil

<AccordionGroup>
  <Accordion title="Synapse">
    Aucune modification spéciale de `homeserver.yaml` n'est requise. Si les notifications Matrix normales atteignent déjà cet utilisateur, le jeton destinataire + l'appel `pushrules` ci-dessus est l'étape de configuration principale.

    Si vous exécutez Synapse derrière un proxy inverse ou des workers, assurez-vous que `/_matrix/client/.../pushrules/` atteint correctement Synapse. La livraison des notifications est gérée par le processus principal ou `synapse.app.pusher` / les workers pushers configurés — assurez-vous que ceux-ci sont sains.

  </Accordion>

  <Accordion title="Tuwunel">
    Même flux que Synapse ; aucune configuration spécifique à Tuwunel n'est nécessaire pour le marqueur d'aperçu finalisé.

    Si les notifications disparaissent alors que l'utilisateur est actif sur un autre appareil, vérifiez si `suppress_push_when_active` est activé. Tuwunel a ajouté cette option dans la version 1.4.2 (septembre 2025) et elle peut intentionnellement supprimer les notifications vers d'autres appareils tandis qu'un appareil est actif.

  </Accordion>
</AccordionGroup>

## Connexes

- [Configuration du canal Matrix](/fr/channels/matrix)
- [Concepts de streaming](/fr/concepts/streaming)
