---
summary: "Supervisez la passerelle OpenClaw en tant que processus enfant à partir d'Electron ou d'une autre application hôte"
read_when:
  - Embedding OpenClaw in a desktop or server application
  - Supervising the Gateway as a child process
  - Handling Gateway readiness, restart, shutdown, or invalid config without scraping logs
title: "Intégration d'OpenClaw"
---

Une application hôte d'intégration doit superviser l'exécutable `openclaw` installé, utiliser le protocole WebSocket de la passerelle comme plan de contrôle, et traiter le processus enfant comme un runtime remplaçable. Cela rend explicites la propriété du processus, la disponibilité, la récupération des défaillances et les mises à jour sans dépendre de la disposition d'état privé d'OpenClaw.

Pour l'authentification du client et l'état de reconnexion, consultez
[Créer un client de passerelle](https://docs.openclaw.ai/gateway/clients).

## Démarrer l'enfant avec un préréglage d'intégration

Utilisez une installation réelle de `node_modules` et lancez l'exécutable du package. Une base utile pour un hôte qui possède la découverte, le redémarrage et le cycle de vie des canaux est :

```ts
import { spawn } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Supply an absolute path to a real Node runtime managed by the host application.
declare const hostNodeExecutable: string;

const packageEntry = fileURLToPath(import.meta.resolve("openclaw"));
const openclawEntry = resolve(dirname(packageEntry), "..", "openclaw.mjs");
const gateway = spawn(hostNodeExecutable, [openclawEntry, "gateway", "--allow-unconfigured"], {
  env: {
    ...process.env,
    OPENCLAW_DISABLE_BONJOUR: "1",
    OPENCLAW_EXEC_SHELL_SNAPSHOT: "0",
    OPENCLAW_NO_RESPAWN: "1",
    OPENCLAW_SKIP_CHANNELS: "1",
  },
  stdio: ["ignore", "inherit", "inherit"],
});
```

Résolvez OpenClaw via le package installé comme indiqué ; ne supposez pas qu'un binaire `openclaw` local au projet se trouve sur le `PATH` du processus hôte. L'exemple hérite de la sortie afin que l'enfant ne puisse pas se bloquer sur des pipes stdout ou stderr pleins. Si l'hôte capture plutôt ces flux, attachez les consommateurs immédiatement après le lancement.

| Paramètre                        | Effet d'intégration                                                                                                                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OPENCLAW_DISABLE_BONJOUR=1`     | Désactive la publicité multidiffusion LAN détenue par la passerelle lorsque l'hôte possède la découverte.                                                                                |
| `OPENCLAW_NO_RESPAWN=1`          | Dans un enfant d'intégration non géré, empêche OpenClaw de confier un redémarrage de mise à jour à un enfant détaché. Les redémarrages de routine restent en processus, l'hôte conserve la propriété du PID suivi. |
| `OPENCLAW_EXEC_SHELL_SNAPSHOT=0` | Désactive la capture d'instantané de shell de connexion pour les commandes exec d'hôte.                                                                                                   |
| `OPENCLAW_SKIP_CHANNELS=1`       | Ignore le démarrage et le rechargement des canaux. Définissez-le uniquement lorsque l'application d'intégration souhaite une passerelle de plan de contrôle ou WebChat uniquement.        |

`--allow-unconfigured` contourne uniquement la garde de démarrage `gateway.mode=local`. Il n'écrit pas de configuration ni ne répare un fichier invalide. Omettez-le lorsque l'application d'intégration provisionne une configuration locale normale via l'intégration, l'interface CLI de configuration ou Gateway RPC.

### Avertissement concernant l'instantané du shell Electron

La capture d'instantané du shell exécute `process.execPath -e <script>` à partir d'un shell de connexion. Dans un processus Node normal, `process.execPath` est l'exécutable Node. Sous Electron, c'est le binaire Electron, qui peut interpréter l'invocation comme un lancement d'application et afficher une fenêtre contextuelle « Impossible de trouver l'application Electron ». Définissez `OPENCLAW_EXEC_SHELL_SNAPSHOT=0` dans l'environnement de l'enfant de la passerelle, pas seulement dans le processus de rendu. Pour la même raison, `hostNodeExecutable` doit pointer vers un runtime Node réel plutôt que vers `process.execPath` d'Electron.

## Gérer la configuration invalide par code de sortie

Le démarrage de la passerelle utilise le code de sortie `78` (`EX_CONFIG`) pour les défaillances de démarrage de classe configuration, y compris une configuration invalide. Branchez sur le code de sortie au lieu de scraper stderr lisible :

1. Exécutez `openclaw doctor --fix --yes --non-interactive` contre le même environnement de configuration et d'état que l'enfant de la passerelle.
2. Réessayez le démarrage de la passerelle une fois après la sortie réussie du docteur.
3. Si l'enfant quitte `78` à nouveau, arrêtez la boucle de réparation et signalez l'échec de configuration à l'utilisateur.

Conservez stderr pour les diagnostics, mais ne prenez pas de décisions de cycle de vie en fonction de sa formulation.

Après un démarrage réussi, une édition de configuration en direct invalide est moins destructrice. Le moniteur de configuration enregistre que le rechargement a été ignoré et continue à servir la dernière configuration en mémoire acceptée. Réparez le fichier, puis laissez le moniteur accepter le prochain instantané valide.

## Attendre la disponibilité du protocole

Utilisez les signaux WebSocket au lieu d'une sous-chaîne de journal :

1. Ouvrez le WebSocket de la passerelle.
2. Attendez l'événement `connect.challenge`. Il prouve que l'écouteur a accepté le WebSocket et que la poignée de main de défi peut commencer.
3. Envoyez `connect` avec la signature d'appareil liée au défi.
4. Traitez `hello-ok` comme la disponibilité de l'application pour RPC authentifié.

Le défi est délibérément antérieur à l'initialisation complète. Si les sidecars de démarrage sont toujours en attente, `connect` retourne une erreur `UNAVAILABLE` réessayable avec `details.reason: "startup-sidecars"`, un `retryAfterMs` borné, puis se ferme avec le code `1013` et la raison `gateway starting`. Utilisez `resolveGatewayStartupRetryAfterMs` de `@openclaw/gateway-protocol/startup-unavailable` ou la politique intégrée du client de référence, puis reconnectez-vous.

## Interpréter le redémarrage et l'arrêt

Avant une fermeture ordonnée, la passerelle diffuse un événement `shutdown` avec `reason` et `restartExpectedMs`. Un `restartExpectedMs` non nul signifie qu'un redémarrage en processus ou supervisé est attendu ; `null` signifie un arrêt terminal.

Le code de fermeture WebSocket suivant est `1012` dans les deux cas. La raison de fermeture du client ordinaire est également `service restart` dans les deux cas, donc ni le code de fermeture ni la raison ne distinguent le redémarrage de l'arrêt. Préservez la charge utile `shutdown` précédente lorsqu'elle arrive, et combinez-la avec l'intention d'arrêt propre de l'hôte et l'état de sortie de l'enfant. Si la connexion disparaît sans l'événement, utilisez la politique de reconnexion et de supervision d'enfant normalement bornée.

## Utiliser RPC au lieu de fichiers d'état

Gardez la passerelle comme seul propriétaire de l'état OpenClaw. Les opérations d'intégration courantes ont déjà des méthodes RPC :

| Tâche                             | Méthodes RPC                                         |
| --------------------------------- | ---------------------------------------------------- |
| Catalogue et cycle de vie de session | `sessions.list`, `sessions.patch`, `sessions.delete` |
| Affichage de la transcription      | `chat.history`                                       |
| Rapports de coût et d'utilisation  | `usage.cost`, `sessions.usage`                       |
| État des identifiants de modèle    | `models.authStatus`                                  |
| Configuration                      | `config.get`, `config.patch`                         |

`config.get` rédige les valeurs sensibles et les identifiants SecretRef avant de retourner l'instantané. Les méthodes d'écriture retournent également la configuration réduite. Un client doit traiter la sentinelle de rédaction comme opaque et utiliser le contrat d'écriture de configuration documenté ; il ne doit jamais s'attendre à ce que la passerelle retourne des secrets en texte brut.

Ne lisez pas ou ne mutez pas les fichiers, les tables SQLite, les fichiers de transcription ou les répertoires de cache sous `~/.openclaw` pour implémenter les fonctionnalités de l'application. Ces dispositions sont des détails d'implémentation de runtime privés et peuvent se déplacer ou changer sans compatibilité de protocole.

## Installer ; ne pas aplatir

Le package racine `openclaw` n'est pas une cible de vendoring de fichier unique. Les fichiers runtime groupés sous `dist/extensions` conservent les auto-imports nus tels que `openclaw/plugin-sdk/*`, tandis que le package npm exclut intentionnellement les arbres `node_modules` par extension.

Installez OpenClaw via npm, pnpm ou une autre installation de package Node normale afin que Node puisse résoudre les exports de package et l'arborescence des dépendances racine. Lancez l'exécutable `openclaw` installé. Ne copiez que `dist`, n'aplatissez pas le package dans un bundle d'application ou ne vendez les fichiers d'extension sélectionnés.

## Connexes

- [Créer un client de passerelle](https://docs.openclaw.ai/gateway/clients)
- [Protocole de passerelle](https://docs.openclaw.ai/gateway/protocol)
- [Interface CLI de passerelle](https://docs.openclaw.ai/cli/gateway)
- [Intégrations de passerelle pour les applications externes](https://docs.openclaw.ai/gateway/external-apps)
