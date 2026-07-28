---
summary: "Publier des sessions de codage locales rédigées dans un catalogue OpenClaw partagé en lecture seule"
read_when:
  - Sharing a Claude Code or Codex session with trusted Gateway operators
  - Configuring an authenticated session-ingest endpoint without connecting a node
  - Auditing what Beam stores and exposes
title: "Plugin Beam"
---

Le plugin `beam` fourni reçoit un instantané de session de codage désinfecté via HTTP authentifié et le présente dans le catalogue de sessions externes existant de l'interface utilisateur de contrôle. L'ordinateur source envoie du texte ; OpenClaw ne se reconnecte jamais à cet ordinateur et ne reçoit aucune capacité de système de fichiers, terminal, outil ou nœud.

Beam est fourni avec OpenClaw mais est désactivé par défaut. Lorsqu'il est activé, il enregistre :

- `POST /api/v1/beam/sessions`
- le catalogue de sessions **Beam** en lecture seule dans la barre latérale de l'interface utilisateur de contrôle

## Activer

```bash
openclaw plugins enable beam
openclaw gateway restart
```

Configuration équivalente :

```json5
{
  plugins: {
    entries: {
      beam: { enabled: true },
    },
  },
}
```

Désactivez le plugin lorsque la route d'ingestion n'est pas nécessaire :

```bash
openclaw plugins disable beam
openclaw gateway restart
```

## Authentification

Le récepteur utilise l'authentification HTTP Gateway normale. Ce n'est pas un point de terminaison de téléchargement anonyme.

- Avec `gateway.auth.mode: "trusted-proxy"`, envoyez les demandes via le proxy d'identité configuré. Beam s'appuie sur l'authentification Gateway mais ne persiste pas les en-têtes d'identité du proxy en tant qu'attribution du téléchargeur.
- Avec l'authentification par jeton ou mot de passe, envoyez `Authorization: Bearer <gateway-token-or-password>`.
- N'activez pas Beam avec `gateway.auth.mode: "none"` sauf si une autre entrée privée authentifie complètement chaque demande.

Un déploiement protégé par Cloudflare Access peut authentifier une CLI locale sans exposer un jeton GitHub :

```bash
cloudflared access login https://gateway.example.com
cloudflared access curl https://gateway.example.com/api/v1/beam/sessions \
  -H 'Content-Type: application/json' \
  --data-binary @sanitized-beam.json
```

La compétence `beam` dans [openclaw/agent-skills](https://github.com/openclaw/agent-skills) gère la découverte de transcriptions locales, la rédaction, la connexion Cloudflare Access et le téléchargement pour Claude Code et Codex.

## Demande

```http
POST /api/v1/beam/sessions
Content-Type: application/json
```

```json
{
  "version": 1,
  "beamId": "0123456789abcdef0123456789abcdef",
  "source": "claude",
  "title": "Fix the upload flow",
  "updatedAt": "2026-07-20T12:00:00.000Z",
  "completed": false,
  "items": [
    { "type": "userMessage", "text": "Fix the upload flow." },
    { "type": "agentMessage", "text": "Implemented and tested." },
    { "type": "other", "text": "3 read, 2 write, 1 execute; raw tool outputs dropped: 4" }
  ]
}
```

Le schéma est fermé. Beam rejette les champs inconnus, les types d'éléments invalides, le texte vide, plus de 200 éléments, le texte d'élément supérieur à 6 000 caractères, les demandes non-JSON et les corps supérieurs à 56 KiB.

Un téléchargement réussi retourne l'identifiant Beam stable et une URL relative de l'interface utilisateur de contrôle :

```json
{
  "ok": true,
  "beamId": "0123456789abcdef0123456789abcdef",
  "url": "/chat?session=catalog%3Abeam%3Agateway%3A0123456789abcdef0123456789abcdef"
}
```

Le téléchargement du même `beamId` met à jour la ligne de catalogue existante. Un téléchargement terminé définit l'état de la ligne sur `completed` ; les mises à jour antérieures s'affichent comme `live`.

## Stockage et visibilité

Beam stocke les charges utiles désinfectées dans l'état du plugin soutenu par SQLite partagé d'OpenClaw :

- au maximum 500 sessions
- rétention de sept jours actualisée par chaque mise à jour
- expulsion de l'entrée la plus ancienne lorsque le catalogue atteint sa limite
- l'heure de réception du serveur contrôle l'ordre du catalogue ; les clients ne peuvent pas se placer devant eux-mêmes avec un horodatage falsifié

Le catalogue est intentionnellement partagé dans le domaine de l'opérateur Gateway. Chaque client avec `operator.read` peut voir chaque session beamée, tandis que les téléchargements nécessitent `operator.write` ou `operator.admin`. L'identité du téléchargeur n'est pas conservée, et tout opérateur autorisé en écriture qui connaît un identifiant Beam peut mettre à jour cette ligne. Les portées d'opérateur OpenClaw ne sont pas l'isolation des locataires ; utilisez une Gateway séparée lorsque les sessions doivent être isolées entre les équipes ou les machines.

## Limite de sécurité

Beam est une publication de session passive, pas un contrôle à distance.

- Il n'a pas de capacité `continueSession`, archive, terminal, outil ou nœud.
- Il accepte uniquement les éléments de transcription normalisés en texte brut, pas HTML, scripts, archives, pièces jointes ou URL récupérées par le serveur.
- La compétence officielle supprime les résultats d'outils bruts, le raisonnement, les invites, les chemins locaux, les identifiants, les cookies et le matériel d'authentification avant le téléchargement.
- Le récepteur traite toujours chaque transcription comme du texte non fiable. Copier une transcription beamée dans une nouvelle session d'agent est une action d'opérateur distincte.
- Les demandes sont limitées en débit et en concurrence avant la lecture du corps.

## Mise en miroir

Beam peut également agir en tant qu'expéditeur : un miroir opt-in qui publie continuellement les sessions de codage locales actives de cette machine (Claude Code, Codex et autres catalogues de sessions enregistrés) vers un récepteur Beam distant, tel qu'une Gateway d'équipe partagée. Les coéquipiers regardent ensuite les transcriptions de session quasi-en direct dans l'interface utilisateur de contrôle distante sans aucun accès à la machine source.

```json5
{
  plugins: {
    entries: {
      beam: {
        enabled: true,
        config: {
          mirror: {
            endpoint: "https://team.example.com/api/v1/beam/sessions",
            token: { source: "env", provider: "default", id: "BEAM_TEAM_TOKEN" },
            catalogs: ["claude", "codex"],
          },
        },
      },
    },
  },
}
```

- `endpoint` (obligatoire) : l'URL du récepteur distant. HTTPS est appliqué pour les hôtes non-loopback ; le texte brut `http://` n'est accepté que pour le développement `localhost`/`127.0.0.1`/`::1`.
- `token` : identifiant Gateway pour le récepteur distant, envoyé en tant que `Authorization: Bearer`. Accepte une chaîne simple ou une référence secrète ; un jeton configuré mais non résolu met en pause la mise en miroir au lieu d'envoyer des demandes non authentifiées. Les déploiements précédés d'un proxy conscient de l'identité ont besoin d'une entrée qui accepte cette identité de porteur.
- `catalogs` (obligatoire) : les identifiants de catalogue de sessions à mettre en miroir, en tant que consentement explicite par catalogue — une liste omise ou vide ne met rien en miroir. Le catalogue du récepteur `beam` local est toujours exclu afin que deux Gateways mises en miroir ne puissent pas se re-mettre en miroir les lignes respectives.
- `pollSeconds` (par défaut 30, minimum 10) : la fréquence à laquelle le miroir analyse les catalogues locaux.
- `activeWindowMinutes` (par défaut 180) : les sessions avec une activité plus récente que cette fenêtre comptent comme actives et restent mises en miroir ; lorsqu'une session devient inactive au-delà de la fenêtre, le miroir envoie une mise à jour `completed` finale.

Le miroir applique le même contrat de rédaction que la compétence beam avant que quoi que ce soit ne quitte la machine : seul le texte des messages utilisateur et agent est téléchargé, tandis que le raisonnement, les appels d'outils, les résultats d'outils et les charges utiles brutes sont remplacés par des comptages compacts. Les instantanés sont limités aux limites du récepteur (200 éléments, 56 KiB), en supprimant d'abord les entrées les plus anciennes et en marquant le téléchargement comme `truncated`. Les sessions sur les nœuds appairés ne sont pas mises en miroir ; le miroir partage uniquement les sessions de la machine Gateway de ce Gateway, les 32 plus récentes en premier.

## Dépannage

`404 Not Found`

: Le plugin Beam est désactivé, la Gateway n'a pas redémarré depuis l'activation, ou la demande atteint une autre Gateway.

`401 Unauthorized`

: La demande n'a pas satisfait l'authentification HTTP Gateway. Vérifiez l'identifiant de porteur ou la session de proxy de confiance/Access.

`405 Method Not Allowed`

: Le récepteur n'accepte que `POST`.

`413 Payload Too Large`

: La demande sérialisée a dépassé 56 KiB. La compétence officielle supprime les messages désinfectés plus anciens jusqu'à ce que l'instantané s'adapte.

`429 Too Many Requests`

: Le client authentifié a dépassé la limite de demande ou de concurrence délimitée. Réessayez après la fenêtre de minute actuelle.

## Connexes

- [Interface utilisateur de contrôle](/fr/web/control-ui)
- [Portées d'opérateur](/fr/gateway/operator-scopes)
- [Authentification par proxy de confiance](/fr/gateway/trusted-proxy-auth)
- [Gestion des plugins](/fr/plugins/manage-plugins)
