---
summary: "Résolvez les secrets Gateway avec la CLI 1Password et laissez les agents utiliser la compétence 1password intégrée"
read_when:
  - You want API keys out of openclaw.json and inside 1Password
  - You run the Gateway headless and need service account auth for op
  - You want agents to read or inject secrets with the op CLI
title: "1Password"
---

OpenClaw s'associe à **1Password** de deux manières indépendantes :

- **Secrets de configuration :** tout champ [SecretRef](/fr/gateway/secrets) dans `openclaw.json` peut être résolu via la CLI `op` à l'exécution, de sorte que les clés API ne vivent jamais dans le fichier de configuration.
- **Workflows d'agents :** la compétence `1password` intégrée enseigne aux agents à se connecter et à lire ou injecter des secrets avec `op` pour leurs propres tâches.

## Prérequis

- La [CLI 1Password](https://developer.1password.com/docs/cli/get-started/) (`op`) installée sur l'hôte Gateway (`brew install 1password-cli` sur macOS).
- Un mode d'authentification pour `op` :
  - **Compte de service** (recommandé pour les Gateways sans interface) : exportez `OP_SERVICE_ACCOUNT_TOKEN` dans l'environnement du service Gateway. Pas d'application de bureau, pas de connexion interactive.
  - **Intégration d'application de bureau** : l'application 1Password s'exécute sur la même machine avec l'intégration CLI activée. Les premiers appels peuvent déclencher Touch ID ou une authentification système.
  - **Connexion autonome** : `op signin` demande une invite par session. Possible pour les agents via la compétence, mais non adapté à la résolution des secrets de configuration sur un Gateway sans interface.

## Résoudre les secrets de configuration avec op

Déclarez un fournisseur de secrets exec qui exécute `op read` avec une référence `op://vault/item/field`, puis pointez tout champ compatible SecretRef vers celui-ci :

```json5
{
  secrets: {
    providers: {
      onepassword_openai: {
        source: "exec",
        command: "/opt/homebrew/bin/op",
        allowSymlinkCommand: true, // required for Homebrew symlinked binaries
        trustedDirs: ["/opt/homebrew"],
        args: ["read", "op://Personal/OpenClaw QA API Key/password"],
        passEnv: ["HOME"],
        jsonOnly: false,
      },
    },
  },
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        models: [{ id: "gpt-5", name: "gpt-5" }],
        apiKey: { source: "exec", provider: "onepassword_openai", id: "value" },
      },
    },
  },
}
```

Comment les pièces s'assemblent :

- `command` doit être un chemin absolu ; `trustedDirs` marque son répertoire comme approuvé, et `allowSymlinkCommand` est nécessaire car Homebrew installe `op` comme un lien symbolique.
- `args` porte la référence `op://vault/item/field` textuellement. OpenClaw n'analyse pas le schéma `op://` lui-même ; le binaire `op` le résout.
- `passEnv` transfère les variables listées depuis l'environnement Gateway. L'intégration d'application de bureau a besoin de `HOME` ; les comptes de service ont également besoin que `OP_SERVICE_ACCOUNT_TOKEN` soit présent dans l'environnement du service Gateway (ajoutez-le à `passEnv`, ou définissez-le via `env` uniquement si vous acceptez que le token soit lisible dans le fichier de configuration).
- Pour une sortie à valeur unique, conservez `id: "value"`. Avec `jsonOnly: true` et une charge utile JSON, adressez les champs avec un id de pointeur JSON à la place.
- Une entrée de fournisseur par secret garde les références auditables ; nommez les fournisseurs d'après leur consommateur (`onepassword_openai`, `onepassword_telegram`).

Voir [Gateway secrets](/fr/gateway/secrets) pour l'ordre de résolution, la mise en cache et la sémantique des défaillances, et [SecretRef Credential Surface](/fr/reference/secretref-credential-surface) pour chaque champ qui accepte les SecretRefs.

## Configuration du compte de service pour les Gateways sans interface

1. Créez un compte de service dans votre compte 1Password et accordez-lui un accès en lecture uniquement aux éléments de coffre dont le Gateway a besoin.
2. Fournissez `OP_SERVICE_ACCOUNT_TOKEN` au service Gateway (plist launchd, unité systemd, ou env de conteneur).
3. Ajoutez `"OP_SERVICE_ACCOUNT_TOKEN"` à la liste `passEnv` du fournisseur.
4. Vérifiez depuis l'environnement hôte Gateway : `op whoami` doit imprimer le compte de service sans demander d'invite.

Les lectures de compte de service nécessitent que le coffre soit nommé explicitement dans la référence `op://`. Limitez le compte étroitement ; c'est une credential de porteur.

## La compétence 1password pour les agents

OpenClaw intègre une compétence `1password` qui transforme les agents en opérateurs `op` compétents : elle détecte le mode d'authentification disponible (compte de service, intégration d'application de bureau, ou connexion autonome), vérifie l'accès avec `op whoami` avant de lire quoi que ce soit, et préfère `op run` / `op inject` à l'écriture de valeurs secrètes sur le disque. La compétence nécessite le binaire `op` et propose une installation Homebrew quand il est manquant.

Les agents l'utilisent pour leurs propres workflows, par exemple lire un token de déploiement au milieu d'une tâche ou injecter des variables d'environnement dans une commande. Elle est indépendante de la résolution des secrets de configuration ; le Gateway résout les SecretRefs sans aucune compétence impliquée.

## Notes de sécurité

- Les valeurs secrètes résolues via les fournisseurs exec restent en mémoire Gateway ; les snapshots de configuration et les réponses `config.get` masquent les champs SecretRef.
- Ne placez jamais les valeurs secrètes dans `openclaw.json`, les journaux ou le chat. Gardez les noms d'éléments en configuration, les valeurs dans 1Password.
- La piste d'audit 1Password montre chaque lecture de compte de service, ce qui rend la rotation des clés et l'examen des incidents pratiques.

## Dépannage

- `command not found` ou erreurs de spawn : utilisez le chemin absolu `op` et incluez son répertoire dans `trustedDirs`.
- `op` se résout mais les lectures échouent avec des erreurs de lien symbolique : définissez `allowSymlinkCommand: true` pour les installations Homebrew.
- `account is not signed in` : pour les comptes de service, confirmez que `OP_SERVICE_ACCOUNT_TOKEN` atteint le service Gateway et est listé dans `passEnv` ; pour l'intégration de bureau, confirmez que l'application s'exécute et est déverrouillée.
- Lectures lentes au premier appel : augmentez `timeoutMs` sur le fournisseur ; les démarrages à froid `op` peuvent dépasser les délais d'attente stricts sur les hôtes occupés.
