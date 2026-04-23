---
title: "Export de diagnostics"
summary: "Créer des bundles de diagnostics Gateway partageables pour les rapports de bugs"
read_when:
  - Preparing a bug report or support request
  - Debugging Gateway crashes, restarts, memory pressure, or oversized payloads
  - Reviewing what diagnostics data is recorded or redacted
---

# Export de diagnostics

OpenClaw peut créer un fichier zip de diagnostics local qui est sûr à joindre aux rapports de bugs.
Il combine l'état Gateway sanitisé, la santé, les logs, la forme de la configuration, et les événements de stabilité récents sans charge utile.

## Démarrage rapide

```bash
openclaw gateway diagnostics export
```

La commande affiche le chemin du fichier zip écrit. Pour choisir un chemin :

```bash
openclaw gateway diagnostics export --output openclaw-diagnostics.zip
```

Pour l'automatisation :

```bash
openclaw gateway diagnostics export --json
```

## Contenu de l'export

Le fichier zip inclut :

- `summary.md` : aperçu lisible par l'homme pour le support.
- `diagnostics.json` : résumé lisible par machine de la configuration, des logs, de l'état, de la santé,
  et des données de stabilité.
- `manifest.json` : métadonnées d'export et liste des fichiers.
- Forme de configuration sanitisée et détails de configuration non-secrets.
- Résumés de logs sanitisés et lignes de logs récentes redactées.
- Snapshots d'état et de santé Gateway au meilleur effort.
- `stability/latest.json` : bundle de stabilité persisté le plus récent, quand disponible.

L'export est utile même quand la Gateway est en mauvais état. Si la Gateway ne peut pas
répondre aux demandes d'état ou de santé, les logs locaux, la forme de la configuration, et le
bundle de stabilité le plus récent sont toujours collectés quand disponibles.

## Modèle de confidentialité

Les diagnostics sont conçus pour être partageables. L'export conserve les données opérationnelles
qui aident au débogage, telles que :

- noms de sous-systèmes, ids de plugins, ids de fournisseurs, ids de canaux, et modes configurés
- codes de statut, durées, comptages d'octets, état de la file d'attente, et lectures de mémoire
- métadonnées de logs sanitisées et messages opérationnels redactés
- forme de configuration et paramètres de fonctionnalités non-secrets

L'export omet ou redacte :

- texte de chat, prompts, instructions, corps de webhooks, et sorties d'outils
- identifiants, clés API, tokens, cookies, et valeurs secrètes
- corps de requêtes ou réponses bruts
- ids de comptes, ids de messages, ids de sessions bruts, noms d'hôtes, et noms d'utilisateurs locaux

Quand un message de log ressemble à du texte utilisateur, chat, prompt, ou charge utile d'outil,
l'export conserve seulement qu'un message a été omis et le comptage d'octets.

## Enregistreur de stabilité

La Gateway enregistre un flux de stabilité borné et sans charge utile par défaut quand
les diagnostics sont activés. C'est pour les faits opérationnels, pas le contenu.

Inspectez l'enregistreur en direct :

```bash
openclaw gateway stability
openclaw gateway stability --type payload.large
openclaw gateway stability --json
```

Inspectez le bundle de stabilité persisté le plus récent après une sortie fatale, un délai d'expiration d'arrêt,
ou un échec de démarrage au redémarrage :

```bash
openclaw gateway stability --bundle latest
```

Créez un fichier zip de diagnostics à partir du bundle persisté le plus récent :

```bash
openclaw gateway stability --bundle latest --export
```

Les bundles persistés se trouvent sous `~/.openclaw/logs/stability/` quand des événements existent.

## Options utiles

```bash
openclaw gateway diagnostics export \
  --output openclaw-diagnostics.zip \
  --log-lines 5000 \
  --log-bytes 1000000
```

- `--output <path>` : écrire dans un chemin zip spécifique.
- `--log-lines <count>` : nombre maximum de lignes de logs sanitisées à inclure.
- `--log-bytes <bytes>` : nombre maximum d'octets de logs à inspecter.
- `--url <url>` : URL WebSocket Gateway pour les snapshots d'état et de santé.
- `--token <token>` : token Gateway pour les snapshots d'état et de santé.
- `--password <password>` : mot de passe Gateway pour les snapshots d'état et de santé.
- `--timeout <ms>` : délai d'expiration du snapshot d'état et de santé.
- `--no-stability-bundle` : ignorer la recherche de bundle de stabilité persisté.
- `--json` : afficher les métadonnées d'export lisibles par machine.

## Désactiver les diagnostics

Les diagnostics sont activés par défaut. Pour désactiver l'enregistreur de stabilité et
la collecte d'événements de diagnostic :

```json5
{
  diagnostics: {
    enabled: false,
  },
}
```

La désactivation des diagnostics réduit le détail du rapport de bug. Cela n'affecte pas
la journalisation normale de la Gateway.

## Documentation connexe

- [Health Checks](/fr/gateway/health)
- [Gateway CLI](/fr/cli/gateway#gateway-diagnostics-export)
- [Gateway Protocol](/fr/gateway/protocol#system-and-identity)
- [Logging](/fr/logging)
