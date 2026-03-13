---
read_when:
  - Debugging model authentication or OAuth expiration
  - Logging authentication or credential storage
summary: Model authentication: OAuth, API keys and setup-token
title: Authentication
x-i18n:
  generated_at: "2026-02-03T07:47:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 66fa2c64ff374c9cfcdb4e7a951b0d164d512295e65513eb682f12191b75e557
  source_path: gateway/authentication.md
  workflow: 15
---

# Authentification

OpenClaw prend en charge OAuth et les clés API pour les fournisseurs de modèles. Pour les comptes Anthropic, nous recommandons d'utiliser des **clés API**. Pour l'accès aux abonnements Claude, utilisez les jetons de longue durée créés avec `claude setup-token`.

Consultez [/concepts/oauth](/concepts/oauth) pour connaître le flux OAuth complet et la disposition du stockage.

## Configuration Anthropic recommandée (clé API)

Si vous utilisez directement Anthropic, utilisez une clé API.

1. Créez une clé API dans la console Anthropic.
2. Placez-la sur l'**hôte Gateway** (la machine exécutant `openclaw gateway`).

```bash
export ANTHROPIC_API_KEY="..."
openclaw models status
```

3. Si Gateway s'exécute sous systemd/launchd, il est préférable de placer la clé dans `~/.openclaw/.env` pour que le démon puisse la lire :

```bash
cat >> ~/.openclaw/.env <<'EOF'
ANTHROPIC_API_KEY=...
EOF
```

Ensuite, redémarrez le démon (ou redémarrez votre processus Gateway) et revérifiez :

```bash
openclaw models status
openclaw doctor
```

Si vous ne souhaitez pas gérer vous-même les variables d'environnement, l'assistant d'intégration peut stocker la clé API pour le démon : `openclaw onboard`.

Consultez [l'aide](/help) pour plus de détails sur l'héritage des variables d'environnement (`env.shellEnv`, `~/.openclaw/.env`, systemd/launchd).

## Anthropic : setup-token (authentification par abonnement)

Pour Anthropic, le chemin recommandé est la **clé API**. Si vous utilisez un abonnement Claude, le flux setup-token est également pris en charge. Exécutez sur l'**hôte Gateway** :

```bash
claude setup-token
```

Puis collez-le dans OpenClaw :

```bash
openclaw models auth setup-token --provider anthropic
```

Si le jeton a été créé sur une autre machine, collez-le manuellement :

```bash
openclaw models auth paste-token --provider anthropic
```

Si vous voyez une erreur Anthropic comme celle-ci :

```
This credential is only authorized for use with Claude Code and cannot be used for other API requests.
```

…utilisez plutôt une clé API Anthropic.

Saisie manuelle de jetons (tout fournisseur ; écrit dans `auth-profiles.json` + met à jour la configuration) :

```bash
openclaw models auth paste-token --provider anthropic
openclaw models auth paste-token --provider openrouter
```

Vérification conviviale pour l'automatisation (quitte avec `1` si expiré/manquant, `2` si proche de l'expiration) :

```bash
openclaw models status --check
```

Scripts d'exploitation optionnels (systemd/Termux) documentés ici : [/automation/auth-monitoring](/automation/auth-monitoring)

> `claude setup-token` nécessite un TTY interactif.

## Vérifier l'état de l'authentification du modèle

```bash
openclaw models status
openclaw doctor
```

## Contrôler les identifiants utilisés

### Par session (commande de chat)

Utilisez `/model <alias-or-id>@<profileId>` pour épingler les identifiants d'un fournisseur spécifique pour la session actuelle (exemples d'ID de profil : `anthropic:default`, `anthropic:work`).

Utilisez `/model` (ou `/model list`) pour un sélecteur compact ; utilisez `/model status` pour une vue complète (candidats + profil d'authentification suivant, avec détails du point de terminaison du fournisseur lors de la configuration).

### Par agent (remplacement CLI)

Définissez un remplacement d'ordre de profil d'authentification explicite pour un agent (stocké dans `auth-profiles.json` de cet agent) :

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Utilisez `--agent <id>` pour spécifier un agent particulier ; omettez-le pour utiliser l'agent par défaut configuré.

## Dépannage

### "No credentials found"

Si le profil de jeton Anthropic est manquant, exécutez `claude setup-token` sur l'**hôte Gateway**, puis revérifiez :

```bash
openclaw models status
```

### Jeton proche de l'expiration/expiré

Exécutez `openclaw models status` pour confirmer quel profil est proche de l'expiration. Si le profil est manquant, réexécutez `claude setup-token` et collez à nouveau le jeton.

## Exigences

- Abonnement Claude Max ou Pro (pour `claude setup-token`)
- Claude Code CLI installé (commande `claude` disponible)
