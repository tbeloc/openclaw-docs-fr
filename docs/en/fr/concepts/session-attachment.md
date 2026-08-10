---
doc-schema-version: 1
summary: "Comment les sessions détenues par Gateway continuent sur l'interface Control UI, le terminal, la CLI, les clients mobiles et les harnais de codage"
read_when:
  - You want to continue a Control UI session in the terminal
  - You want to attach a coding harness to an existing session
  - You are troubleshooting session links, remote pairing, or attachment failures
title: "Synchronisation des sessions et attachement"
---

OpenClaw conserve l'état de session partagée sur la Gateway. L'interface Control UI, les clients mobiles, ACP, `openclaw tui <target>` et `openclaw attach <target>` projettent cet état détenu par la Gateway au lieu de conserver des copies de session indépendantes. Cela vous permet d'ouvrir une session dans plusieurs clients sans exporter ou copier sa transcription.

Utilisez `openclaw tui` quand vous voulez continuer la conversation dans un terminal. Utilisez `openclaw attach` quand vous voulez un harnais de codage à côté de la session avec une subvention MCP temporaire et limitée à la session.

Le mode local intégré est séparé : `openclaw tui --local`, `openclaw chat` et `openclaw terminal` utilisent le runtime d'agent local et ne peuvent pas accepter une cible de session. Consultez la [référence CLI TUI](/fr/cli/tui#notes) pour le comportement en mode local.

## Une Gateway, plusieurs clients

La Gateway détient les lignes de session, l'historique des transcriptions, les métadonnées de routage et les exécutions actives. Les clients sélectionnent une clé de session et lisent ou mettent à jour cet état via le protocole Gateway. Un nœud mobile reste un périphérique connecté à la Gateway ; il ne devient pas un deuxième propriétaire de session.

La plupart des clés de session d'agent utilisent cette forme :

```text
agent:<agentId>:<rest>
```

La portion `<rest>` peut être un nom simple, plusieurs segments délimités par des deux-points, ou une valeur se terminant par un UUID. Une Gateway configurée avec une portée de session globale utilise la session canonique `global` à la place. Quand une URL réservée à l'agent est ouverte sur une Gateway à portée globale, la CLI demande à la Gateway sa portée de session et résout l'URL à cette session globale canonique.

Consultez [Gestion des sessions](/fr/concepts/session) pour les détails de routage, d'isolation, de cycle de vie et de stockage.

## URLs de session et liens courts

Les liens de chat et de tableau de bord de l'interface Control UI partagent cette grammaire de route :

```text
/{chat|dashboard}/<agentId>
/{chat|dashboard}/<agentId>/<slug>-<shortId>
/{chat|dashboard}/<agentId>/<literal-rest-segments...>
```

Un chemin de base Control UI configuré préfixe ces routes. La forme réservée à l'agent ouvre la projection principale de cet agent. Les formes littérales encodent la clé de session délimitée par des deux-points après `agent:<agentId>:` comme segments de chemin.

Pour une clé dont le reste se termine par un UUID, la forme courte partageable utilise 8 à 32 caractères hexadécimaux minuscules du début de cet UUID, avec les tirets UUID supprimés. L'ID court est autoritaire. Le slug du nom d'affichage est décoratif sauf si deux sessions partagent le même préfixe, auquel cas une correspondance de slug exacte résout l'ambiguïté. Pour les cibles de lien court CLI, le segment d'agent est également décoratif : la Gateway résout l'ID court sans le contraindre à cet agent d'URL.

La méthode Gateway `sessions.resolve` est responsable de la résolution pour les clés exactes, les ID de session bruts, les étiquettes et les ID courts. Les sélecteurs de découverte sont filtrés par la visibilité de session du client appelant. L'ambiguïté d'ID court contient au maximum dix candidats récents, afin que les clients puissent vous demander un préfixe plus long sans deviner. Consultez [URLs Control UI](/fr/web/urls) pour l'encodage littéral complet et le contrat de stabilité.

### Gateways actuelles et anciennes

Les Gateways actuelles résolvent les références courtes au propriétaire du magasin de sessions. L'interface Control UI et la CLI utilisent ensuite la clé canonique retournée.

Une ancienne Gateway peut rejeter le sélecteur `shortId` additif. L'interface Control UI peut revenir à sa recherche de liste bornée plus ancienne, en scannant au maximum cinq pages. La CLI ne recrée pas cette politique de pagination : elle vous dit de copier la clé de session complète de la Gateway de cette Gateway ou de mettre à niveau la Gateway.

## Choisir comment continuer

La CLI accepte trois syntaxes de cible :

- Une URL Control UI complète, telle que
  `https://claw.example.com/dashboard/main/deploy-monitor-6db92d48`.
- Raccourci Gateway, tel que
  `claw.example.com/main/deploy-monitor-6db92d48`.
- Une référence courte nue ou une clé complète, telle que `deploy-monitor-6db92d48` ou
  `agent:main:telegram:12345`. Les références nues utilisent la Gateway configurée ou par défaut.

Les URLs de session ne doivent pas contenir de credentials. Passez `--token` ou `--password` séparément lors du premier appairage avec une origine Gateway.

### Continuer dans le terminal

Pour la continuation soutenue par Gateway, passez l'URL ou la référence à `openclaw tui` :

```bash
openclaw tui https://claw.example.com/dashboard/main/deploy-monitor-6db92d48
openclaw tui deploy-monitor-6db92d48
```

Vous pouvez également coller une URL de session complète directement à la racine CLI :

```bash
openclaw https://claw.example.com/dashboard/main/deploy-monitor-6db92d48
```

Cela ouvre le TUI sur la clé de session canonique retournée par la Gateway. Il ne clone pas la transcription ni ne crée une nouvelle session. Consultez [TUI](/fr/cli/tui) pour les conflits de cible, les options d'URL nue supportées et les exemples.

### Attacher un harnais de codage

Passez la même URL ou référence à `openclaw attach` :

```bash
openclaw attach https://claw.example.com/dashboard/main/deploy-monitor-6db92d48
openclaw attach deploy-monitor-6db92d48
```

La Gateway résout d'abord la session, puis émet une subvention temporaire limitée à cette session et lance le harnais de codage avec une configuration MCP stricte. Le jeton porteur se déplace dans l'environnement enfant au lieu de argv. Un lancement normal révoque la subvention quand le harnais se termine ; `--print-config` la laisse active jusqu'à l'expiration de son TTL. Consultez [Attach CLI](/fr/cli/attach) pour la durée de vie de la subvention et les options de lancement.

## Appairer une fois par origine Gateway

Une URL ou un raccourci gateway sélectionne de manière autoritaire une origine Gateway normalisée. OpenClaw ne réutilise jamais les credentials configurés ou un jeton d'appareil stocké d'une autre origine pour cette cible.

Au premier contact :

1. Exécutez la commande TUI ou attach avec `--token` ou `--password` une fois.
2. Ouvrez **Paramètres > Appareils** dans l'interface Control UI de cette Gateway et approuvez la demande en attente. Sur l'hôte Gateway, vous pouvez plutôt prévisualiser la demande la plus récente avec `openclaw devices approve --latest`, la vérifier et exécuter la commande `openclaw devices approve <requestId>` imprimée.
3. Réessayez la commande originale. OpenClaw stocke le jeton d'appareil opérateur émis dans SQLite sous cette origine Gateway normalisée exacte.
4. Les connexions ultérieures à la même origine peuvent utiliser le jeton d'appareil stocké. Un `--token` ou `--password` explicite gagne toujours pour la connexion entière.

Révoquez ou supprimez l'appareil de la même page **Appareils** de la Gateway quand ce client ne doit plus se connecter. Les jetons ne traversent pas les origines. Les sondes en lecture seule via un tunnel SSH suppriment également l'authentification d'appareil stockée car le transport de boucle locale n'identifie pas l'origine distante ; les credentials explicites fonctionnent toujours.

Consultez [Appareils](/fr/cli/devices), [Accès distant](/fr/gateway/remote) et [Sécurité Gateway](/fr/gateway/security) pour l'approbation, la rotation, la révocation et les conseils réseau.

## Taxonomie des défaillances

Les défaillances de connexion Gateway utilisent un classificateur structuré en premier. Les anciennes Gateways fonctionnent toujours via un repli textuel borné, donc la santé, le statut et le TUI donnent la même catégorie et les mêmes conseils de récupération.

| Défaillance ou type                | Ce que cela signifie                                                                    | Que faire                                                                                                                                                      |
| ---------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rejet de lien court Gateway ancien  | La Gateway n'accepte pas `shortId` dans `sessions.resolve`.                             | Copiez la clé de session complète de l'interface Control UI de cette Gateway, ou mettez à niveau la Gateway.                                                   |
| Session manquante                  | La Gateway sélectionnée ne peut pas trouver cette clé ou cet ID court.                  | Pour la Gateway configurée, exécutez `openclaw sessions list`. Pour une cible d'URL, choisissez la session dans l'interface Control UI de cette Gateway.       |
| Référence de session ambiguë       | Plus d'une session visible partage le préfixe et le slug n'en a pas sélectionné une.   | Utilisez l'un des préfixes d'ID plus longs affichés par la CLI, ou copiez la clé complète.                                                                    |
| `pairing-required`                 | L'appareil est nouveau ou un appareil existant a besoin d'une approbation de rôle, portée ou métadonnées. | Approuvez la demande en attente dans **Paramètres > Appareils**, ou prévisualisez-la avec `openclaw devices approve --latest` et exécutez la commande d'ID exact imprimée, puis réessayez. |
| `device-identity-required`         | La Gateway nécessite une identité d'appareil signée pour cette connexion.               | Utilisez un client OpenClaw actuel, laissez-le créer son identité d'appareil et complétez l'appairage.                                                       |
| `scope-mismatch`                   | Le jeton d'appareil stocké est valide mais manque de la portée opérateur demandée.      | Consultez `openclaw devices list`, approuvez la mise à niveau de portée en attente et reconnectez-vous.                                                      |
| `auth-rejected`                    | Un credential partagé explicite est incorrect, ou un jeton d'appareil appairé a été révoqué ou pivoté. | Vérifiez l'authentification Gateway explicite. Pour un jeton d'appareil obsolète, pivotez-le avec `openclaw devices rotate --device <deviceId> --role operator` ou appairez à nouveau. |
| `rate-limited`                     | Trop de tentatives d'authentification échouées ont causé un verrouillage temporaire.    | Attendez l'expiration du verrouillage, puis réessayez. Ne pivotez pas les credentials simplement parce que la Gateway est limitée en débit.                    |
| `gateway-rejected`                 | La Gateway a retourné un autre rejet structuré, tel qu'une incompatibilité de protocole. | Suivez les détails de l'erreur. Pour l'asymétrie de version, mettez à jour le client ou la Gateway plus ancien avant de réessayer.                            |
| `unreachable`                      | L'origine sélectionnée ne peut pas être atteinte.                                       | Vérifiez le processus Gateway et la route. Pour un hôte `*.ts.net`, connectez Tailscale et confirmez la disponibilité du tailnet ; pour SSH, confirmez que le tunnel est en cours d'exécution. |
| Incompatibilité d'empreinte TLS    | Le certificat présenté ne correspond pas à l'épingle configurée ou explicite.           | Vérifiez le certificat et l'empreinte attendue. Modifiez l'épingle uniquement après avoir confirmé l'identité Gateway.                                        |

## Pages connexes

- [Gestion des sessions](/fr/concepts/session)
- [URLs Control UI](/fr/web/urls)
- [TUI](/fr/cli/tui)
- [Attach CLI](/fr/cli/attach)
- [Appareils](/fr/cli/devices)
- [Accès distant](/fr/gateway/remote)
- [Sécurité Gateway](/fr/gateway/security)
