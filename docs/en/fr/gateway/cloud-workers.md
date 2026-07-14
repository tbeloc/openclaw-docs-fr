---
summary: "Dispatcher les sessions vers des machines cloud jetables : provisionnement, runtime worker, inférence proxifiée et streaming des résultats"
title: "Cloud Workers"
sidebarTitle: "Cloud Workers"
read_when: "Vous voulez que les sessions d'agent s'exécutent sur des machines cloud éphémères au lieu de l'hôte Gateway, ou vous configurez des profils cloudWorkers."
status: active
---

Les cloud workers permettent à une session d'exécuter sa boucle d'agent sur une machine cloud jetable tandis que tout ce qui concerne la session reste où il a toujours été : visible dans la barre latérale, en streaming en direct, avec la transcription détenue par la Gateway. La Gateway loue une machine, installe une copie épinglée d'OpenClaw dessus, synchronise l'espace de travail de la session, et confie la boucle de tour à un processus `openclaw worker` restreint. Les appels de modèle sont proxifiés à travers la Gateway, donc les identifiants du fournisseur ne quittent jamais votre machine, et la mise en cache des invites continue de fonctionner car le fournisseur voit un flux continu.

Quand le travail est terminé (ou que la machine s'arrête), la machine est supprimée. L'état durable — transcription, commits d'espace de travail, enregistrements de placement — vit avec la Gateway.

<Note>
Les cloud workers sont opt-in et invisibles jusqu'à ce que vous configuriez un profil. Les installations non configurées ne voient aucun nouvel RPC, configuration ou interface utilisateur.
</Note>

## Ce qui s'exécute où

| Préoccupation                                           | Localisation                                                                     |
| ------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Boucle d'agent + outils (`exec`, `read`, `write`, `edit`, …) | Machine cloud worker                                                             |
| Inférence de modèle et identifiants du fournisseur     | Gateway (proxifiée par référence `{provider, model}`)                            |
| Transcription (durable, magasin de session)            | Gateway                                                                          |
| Streaming en direct dans la barre latérale             | Fanout Gateway, alimenté par le flux d'événements rejouable du worker            |
| Historique git de l'espace de travail                  | Créé sur la machine sans identifiants ; la Gateway adopte les commits et possède push/PR |

La machine n'a besoin d'aucun port entrant sauf `sshd` et aucune sortie au-delà de ce que votre commande de configuration utilise : la Gateway se connecte via SSH et un tunnel inverse ramène le WebSocket du worker. Aucun Tailscale ou VPN requis.

## Exigences

- Un plugin de fournisseur worker. Le plugin `crabbox` fourni pilote la [CLI Crabbox](https://github.com/openclaw/crabbox), qui courtise les baux sur les backends cloud (AWS, Hetzner, et autres). Le binaire `crabbox` doit être sur `PATH` (ou définir `settings.binary`) avec les identifiants du fournisseur déjà configurés.
- Node.js sur la machine louée. Les images cloud nues en manquent généralement — installez-le dans la commande `setup` du profil.
- Une session avec un worktree géré détenu par la session (créez-en un avec `worktree: true`). La dispatch déplace le contenu de ce worktree ; les répertoires simples se synchronisent comme un miroir de manifeste.

## Configuration

Ajoutez un profil sous `cloudWorkers.profiles` dans `openclaw.json` :

```json
{
  "cloudWorkers": {
    "profiles": {
      "aws": {
        "provider": "crabbox",
        "install": "bundle",
        "settings": {
          "provider": "aws",
          "class": "standard",
          "ttl": "8h",
          "idleTimeout": "45m",
          "setup": "test -x /usr/bin/node || (curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs)"
        }
      }
    }
  }
}
```

Champs du profil :

| Clé        | Signification                                                                                                                                                                             |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `provider` | ID du fournisseur worker enregistré par un plugin (`crabbox` pour le plugin fourni).                                                                                                     |
| `install`  | `bundle` (par défaut) expédie la compilation de la Gateway en cours ; `npm` installe la version Gateway exacte publiée avec intégrité épinglée. `npm` nécessite que la Gateway s'exécute à partir d'une version packagée. |
| `settings` | JSON détenu par le fournisseur. Pour crabbox : `provider` (backend), `class` (classe de machine), `ttl`, `idleTimeout` (durées Go), `setup` optionnel et chemin `binary` absolu.        |
| `lifetime` | Politique stockée optionnelle (`idleTimeoutMinutes`, `maxLifetimeMinutes`).                                                                                                               |

### La commande de configuration

`settings.setup` s'exécute sur la machine louée après qu'elle soit prête pour SSH et avant l'installation d'OpenClaw. Elle s'exécute sur **chaque** tentative de provisionnement (y compris les rejeux après une dispatch interrompue), elle doit donc être idempotente — gardez les installations avec une vérification `command -v`/`test -x` comme dans l'exemple. Si la configuration échoue, le fournisseur arrête le bail et la dispatch échoue fermée ; aucune machine à moitié configurée n'est laissée en cours d'exécution.

### Canaux d'installation

- **`bundle`** empaquette la `dist` de la Gateway en cours d'exécution, un `package.json` élagué, et tous les packages d'espace de travail que la compilation référence, tous couverts par un hash de contenu. La machine vérifie le bundle pristine par rapport à ce hash, puis installe les dépendances npm de production (scripts désactivés). C'est ainsi que vous exécutez une compilation de développement sur un worker.
- **`npm`** prouve que la version existe sur le registre public, épingle son intégrité SHA-512, et installe `openclaw@<version>` correspondant exactement à la Gateway.

## Dispatcher une session

Créez une session avec un worktree géré, puis dispatcher-la (l'RPC nécessite `operator.admin` et n'existe que lorsque les profils sont configurés) :

```bash
openclaw gateway call sessions.create \
  --params '{"key":"agent:main:big-refactor","worktree":true,"cwd":"/path/to/repo","worktreeName":"big-refactor"}'

openclaw gateway call sessions.dispatch \
  --timeout 1500000 \
  --params '{"key":"agent:main:big-refactor","profileId":"aws"}'
```

`sessions.dispatch` ferme l'admission locale des tours, draine le travail actif, provisionne le bail, exécute la configuration, amorce OpenClaw, synchronise l'espace de travail, et retourne une fois que le placement atteint la propriété active du worker. Budgétisez plusieurs minutes pour la première dispatch ; les baux et les installations sont mis en cache où le fournisseur le supporte. Après cela, parlez à la session comme d'habitude — les tours sont acheminés vers le worker automatiquement.

Le placement se déplace à travers une machine d'état durable (`local → requested → provisioning → syncing → starting → active`), donc un redémarrage de Gateway en pleine dispatch se réconcilie au lieu de fuir des machines. La dispatch est unidirectionnelle en v1 : il n'y a pas encore d'RPC de retrait, et un tour worker échoué fail-stops le placement avec la queue stderr du worker préservée dans l'erreur de placement pour le diagnostic.

## Modèle de sécurité

- **Ingress worker fermé.** Les workers parlent un protocole dédié sur le socket tunnelisé avec une liste de méthodes fermée — un worker ne peut pas appeler les RPC d'opérateur.
- **Identifiants frappés, hachés au repos.** Chaque dispatch frappe un identifiant worker ; la Gateway stocke uniquement son hash. La rotation des identifiants et la clôture d'époque du propriétaire garantissent au maximum un propriétaire actif par session — un worker obsolète qui se reconnecte est clôturé, jamais fusionné.
- **Épinglage de clé d'hôte.** Le fournisseur doit exposer la clé d'hôte SSH de la machine au moment du provisionnement ; l'amorçage se connecte avec épinglage strict et échoue fermé sans elle.
- **Aucun secret sur la machine.** L'authentification du modèle reste sur la Gateway (l'inférence se déplace par référence `{provider, model}`), et les commits git de l'espace de travail sont créés sur la machine sans identifiants.
- **Transcriptions durables et exactement une fois.** Le worker valide les lots de transcription via un protocole compare-and-swap par rapport à la feuille de la session ; une base obsolète fail-stops la course au lieu de dupliquer ou rebaser la sortie payante.

## Dépannage

- **`sessions.dispatch` est une méthode inconnue** — aucun `cloudWorkers.profiles` n'est configuré, ou l'appelant manque de `operator.admin`.
- **"Worker bootstrap requires Node.js on the leased host"** — ajoutez une installation de Node à `settings.setup` (voir ci-dessus).
- **La dispatch échoue avec une erreur de fournisseur** — l'enregistrement de placement et `environments.list` conservent la dernière erreur, y compris la queue stderr de configuration/amorçage. Les machines sont détruites en cas d'échec, donc cette queue est le principal élément de preuve.
- **Délai d'expiration du client lors de la dispatch** — `openclaw gateway call` par défaut à un délai d'expiration de 10s ; passez `--timeout` généreusement (la dispatch continue de s'exécuter côté serveur de toute façon, et une nouvelle tentative pendant le provisionnement est rejetée avec `session cannot dispatch from placement provisioning`).
- **Entretien des baux** — `crabbox list --provider <backend>` affiche les baux actifs ; `crabbox stop --provider <backend> --id <lease>` en libère un manuellement. Les baux inactifs expirent sur le `idleTimeout` du profil.

## Connexes

- [Sandboxing](/fr/gateway/sandboxing) — réduire le rayon d'explosion pour l'exécution locale des outils
- [Sessions CLI](/fr/cli/sessions) — inspection des sessions stockées
- [Référence de configuration](/fr/gateway/configuration-reference)
