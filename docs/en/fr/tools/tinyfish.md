---
summary: "Plugin TinyFish : automatisation de navigateur hébergée pour les workflows publics multi-étapes"
read_when:
  - You want hosted browser automation from OpenClaw
  - You are configuring or developing the TinyFish plugin
title: "TinyFish"
---

# TinyFish

TinyFish ajoute un outil d'automatisation de navigateur hébergé à OpenClaw pour les workflows web publics complexes : navigation multi-étapes, formulaires, pages gourmandes en JS, routage de proxy géo-conscient et extraction structurée.

Modèle mental rapide :

- Activez le plugin fourni
- Configurez `plugins.entries.tinyfish.config`
- Utilisez l'outil `tinyfish_automation` pour les workflows de navigateur publics
- Récupérez `run_id`, `status`, `result` et une `streaming_url` en direct quand TinyFish en fournit une

## Où il s'exécute

Le plugin TinyFish s'exécute à l'intérieur du processus Gateway, mais l'automatisation de navigateur qu'il déclenche s'exécute sur l'infrastructure hébergée de TinyFish.

Si vous utilisez une Gateway distante, activez et configurez le plugin sur la machine exécutant la Gateway.

## Activation

TinyFish est fourni en tant que plugin fourni et est désactivé par défaut.

```json5
{
  plugins: {
    entries: {
      tinyfish: {
        enabled: true,
      },
    },
  },
}
```

Redémarrez la Gateway après l'avoir activée.

## Configuration

Définissez la configuration sous `plugins.entries.tinyfish.config` :

```json5
{
  plugins: {
    entries: {
      tinyfish: {
        enabled: true,
        config: {
          apiKey: "tf_live_...",
          // Optionnel ; par défaut https://agent.tinyfish.ai
          baseUrl: "https://agent.tinyfish.ai",
        },
      },
    },
  },
}
```

Vous pouvez également fournir la clé API via `TINYFISH_API_KEY`.

## Outil

Le plugin enregistre un outil :

### tinyfish_automation

Exécutez l'automatisation de navigateur hébergée sur un site web public.

| Paramètre         | Requis | Description                                                       |
| ----------------- | ------ | ----------------------------------------------------------------- |
| `url`             | Oui    | URL du site web public cible                                      |
| `goal`            | Oui    | Description en langage naturel de ce qu'il faut accomplir         |
| `browser_profile` | Non    | `lite` (par défaut) ou `stealth` (mode anti-bot)                  |
| `proxy_config`    | Non    | Objet avec `enabled` (booléen) et `country_code` (ISO à 2 lettres)|

Forme de retour :

| Champ           | Description                                           |
| --------------- | ----------------------------------------------------- |
| `run_id`        | Identifiant d'exécution TinyFish                      |
| `status`        | `COMPLETED`, `FAILED` ou autre statut terminal        |
| `result`        | Résultat d'extraction structurée (en cas de succès)   |
| `error`         | Détails de l'erreur (en cas d'échec)                  |
| `streaming_url` | URL de session de navigateur en direct (si fournie)   |
| `help_url`      | Lien vers la documentation TinyFish pertinente        |
| `help_message`  | Conseil d'aide lisible par l'homme (en cas d'erreur)  |

## Bons cas d'usage

Utilisez TinyFish quand le navigateur intégré n'est pas la meilleure surface :

- Formulaires publics complexes avec plusieurs étapes
- Pages gourmandes en JS qui nécessitent un rendu de navigateur réel
- Workflows multi-étapes avec de nombreux clics et navigations
- Navigation sensible aux régions qui bénéficie du routage par proxy
- Extraction structurée à partir de sessions de navigateur en direct

Préférez d'autres outils quand :

- Une simple récupération HTTP ou recherche suffit (`web_fetch`, `web_search`)
- Vous voulez un contrôle CDP local ou distant direct avec le [Browser](/fr/tools/browser) intégré
- Vous avez besoin de sessions de navigateur authentifiées persistantes

## Limitations

- TinyFish cible les workflows web publics ; les sessions authentifiées persistantes sont hors de portée
- La résolution de CAPTCHA n'est pas supportée
- L'état de la session du navigateur ne persiste pas entre les exécutions
- Les exécutions par lot et parallèles sont hors de portée pour le plugin fourni initial

## Exemples de prompts

- "Ouvrez example.com/pricing et extrayez chaque nom de plan et prix en JSON."
- "Allez sur example.com/contact, remplissez le formulaire de demande publique et résumez ce qui s'est passé."
- "Visitez example.com/search, changez la région en Canada et extrayez les cinq premiers annonces publiques."
