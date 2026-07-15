---
summary: "Lancez des widgets HTML OpenClaw autonomes dans Discord Activities"
read_when:
  - Setting up or troubleshooting Discord Activity widgets
title: "Discord Activities"
---

Discord Activities permet à un agent de publier un widget HTML interactif et autonome dans le canal Discord actuel. Le message inclut un bouton **Ouvrir le widget** ; en cliquant dessus, le widget se lance dans Discord.

La fonctionnalité est désactivée par défaut. OpenClaw enregistre les routes HTTP Activity, l'outil agent `discord_widget` et le gestionnaire de bouton de lancement uniquement lorsque `channels.discord.activities` est présent et qu'un secret client se résout.

## Prérequis

- un [bot Discord OpenClaw](/fr/channels/discord) existant
- un nom d'hôte HTTPS public qui atteint la passerelle OpenClaw
- la permission de configurer Activities et OAuth2 pour l'application Discord du bot
- une liste d'autorisation d'utilisateurs Discord existante (`allowFrom` ou `dm.allowFrom`), sauf si le compte utilise intentionnellement des DM ouverts

N'importe quel proxy inverse HTTPS ou tunnel fonctionne. Un tunnel Cloudflare nommé fournit un nom d'hôte stable sans exposer directement le port de la passerelle.

```yaml
# ~/.cloudflared/config.yml
tunnel: openclaw-discord
credentials-file: /home/you/.cloudflared/TUNNEL-ID.json
ingress:
  - hostname: openclaw.example.com
    service: http://127.0.0.1:18789
  - service: http_status:404
```

```bash
cloudflared tunnel login
cloudflared tunnel create openclaw-discord
cloudflared tunnel route dns openclaw-discord openclaw.example.com
cloudflared tunnel run openclaw-discord
```

Gardez l'authentification normale de la passerelle activée. Seul le préfixe Activity est public, et le plugin valide lui-même OAuth, les listes d'autorisation, les sessions et les capacités de document à usage unique.

## Configuration

<Steps>
  <Step title="Exposer la passerelle via HTTPS">
    Démarrez votre tunnel ou proxy inverse et vérifiez que `https://openclaw.example.com/discord/activity/` atteint la passerelle après l'ajout de la configuration Activities. Remplacez le nom d'hôte d'exemple par le vôtre.
  </Step>

  <Step title="Activer Activities dans Discord">
    Ouvrez l'application bot existante dans le [Portail des développeurs Discord](https://discord.com/developers/applications). Ouvrez **Activities**, activez Activities et créez un mappage d'URL :

    - prefix: `ROOT` (`/`)
    - target: `openclaw.example.com/discord/activity`

    La cible est le nom d'hôte public plus `/discord/activity`, sans barre oblique finale.

  </Step>

  <Step title="Copier le secret client OAuth2">
    Ouvrez **OAuth2** dans le Portail des développeurs. Discord nécessite au moins un URI de redirection, donc ajoutez un espace réservé local tel que l'adresse de bouclage si l'application n'en a pas encore ; le SDK d'application intégré gère le flux de retour Activity. Copiez ou réinitialisez le secret client de l'application. Traitez-le comme une credential : ne le collez pas dans le chat, les journaux ou un fichier de configuration validé.
  </Step>

  <Step title="Configurer OpenClaw">
    Ajoutez un bloc au compte Discord qui devrait offrir des widgets :

    ```json5
    {
      channels: {
        discord: {
          token: "${DISCORD_BOT_TOKEN}",
          allowFrom: ["YOUR_DISCORD_USER_ID"],
          activities: {
            clientSecret: "${DISCORD_CLIENT_SECRET}",
            // Optionnel. Par défaut, l'ID d'application du bot appris au démarrage.
            applicationId: "YOUR_DISCORD_APPLICATION_ID",
          },
        },
      },
    }
    ```

    Vous pouvez omettre `clientSecret` du bloc lorsque `DISCORD_CLIENT_SECRET` est défini. Le bloc lui-même doit rester présent pour accepter.

  </Step>

  <Step title="Redémarrer et tester">
    Redémarrez la passerelle. Dans une conversation Discord, demandez à l'agent d'afficher un widget interactif. L'agent peut appeler `discord_widget` ; cliquez sur **Ouvrir le widget** sur le message publié.
  </Step>
</Steps>

## Modèle de sécurité

- OAuth identifie l'utilisateur Discord avant que les métadonnées du widget ne soient renvoyées.
- L'utilisateur doit correspondre à `allowFrom` ou `dm.allowFrom` du compte configuré. Un compte sans liste d'autorisation n'autorise tout le monde que lorsque sa politique DM est explicitement `open`.
- Les sessions OAuth expirent après 15 minutes. Les capacités de document du widget expirent après 60 secondes et fonctionnent une seule fois.
- Les widgets expirent après sept jours, avec au maximum 64 conservés par instance du plugin Discord.
- Le HTML du widget est créé par votre agent et doit être traité comme du contenu de confiance. N'intégrez pas de secrets que vous ne voudriez pas qu'un widget défectueux expose.
- Le widget peut naviguer dans sa propre frame imbriquée. L'iframe `sandbox="allow-scripts"` bloque la navigation de haut niveau, les popups et l'accès à la même origine, tandis que sa Content Security Policy bloque les connexions réseau et les ressources externes. Ces contrôles sont une défense en profondeur, pas une limite de sécurité contre l'agent qui a créé le widget.
- Lorsque Activities est désactivé, `/discord/activity` n'est pas enregistré du tout.

Le shell Activity public et la route d'échange de jetons deviennent accessibles via votre tunnel lorsqu'ils sont activés. Ils n'exposent pas le HTML du widget sans une session OAuth valide et une capacité de document à usage unique.

## Dépannage

### L'Activity dit « Gateway offline »

- confirmez que le tunnel est en cours d'exécution et achemine vers le port de liaison réel de la passerelle
- confirmez que la cible du Portail des développeurs inclut `/discord/activity`
- redémarrez la passerelle après avoir modifié la configuration Discord ou OpenClaw
- vérifiez les journaux de la passerelle pour l'avertissement d'une ligne sur un secret client Activities manquant

### Discord ouvre une page vierge ou signale `blocked:csp`

- vérifiez que le mappage d'URL utilise `ROOT` et n'ajoute pas un deuxième segment `/discord/activity`
- confirmez que le shell, `shell.js` et le module SDK reviennent tous via le proxy Discord
- inspectez les journaux de la passerelle pour les requêtes sous `/discord/activity/`

Les requêtes réseau du widget sont intentionnellement bloquées. Intégrez en ligne tout CSS, JavaScript, image et données nécessaires au widget.

### « Not authorized »

Ajoutez l'ID Discord stable de l'utilisateur à `allowFrom` ou `dm.allowFrom` sur le même compte Discord qui possède Activities. Redémarrez après avoir modifié la configuration.

### « Widget unavailable »

Lancez le bouton à partir du canal où l'agent l'a publié. Si Discord ne porte pas l'ID personnalisé du bouton dans l'Activity, OpenClaw revient uniquement lorsque ce canal a exactement un widget actif ; plusieurs widgets échouent fermés comme indisponibles.
