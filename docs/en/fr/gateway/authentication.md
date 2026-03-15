---
summary: "Authentification du modèle : OAuth, clés API et setup-token"
read_when:
  - Debugging model auth or OAuth expiry
  - Documenting authentication or credential storage
title: "Authentification"
---

# Authentification

OpenClaw supporte OAuth et les clés API pour les fournisseurs de modèles. Pour les hôtes de passerelle toujours actifs, les clés API sont généralement l'option la plus prévisible. Les flux d'abonnement/OAuth sont également supportés lorsqu'ils correspondent à votre modèle de compte fournisseur.

Voir [/concepts/oauth](/concepts/oauth) pour le flux OAuth complet et la disposition du stockage.
Pour l'authentification basée sur SecretRef (`env`/`file`/`exec` providers), voir [Gestion des secrets](/gateway/secrets).
Pour les règles de codes de raison/d'éligibilité des credentials utilisées par `models status --probe`, voir [Sémantique des credentials d'authentification](/auth-credential-semantics).

## Configuration recommandée (clé API, n'importe quel fournisseur)

Si vous exécutez une passerelle de longue durée, commencez par une clé API pour votre fournisseur choisi.
Pour Anthropic spécifiquement, l'authentification par clé API est le chemin sûr et est recommandée par rapport à l'authentification par setup-token d'abonnement.

1. Créez une clé API dans la console de votre fournisseur.
2. Placez-la sur l'**hôte de passerelle** (la machine exécutant `openclaw gateway`).

```bash
export <PROVIDER>_API_KEY="..."
openclaw models status
```

3. Si la passerelle s'exécute sous systemd/launchd, préférez placer la clé dans
   `~/.openclaw/.env` pour que le daemon puisse la lire :

```bash
cat >> ~/.openclaw/.env <<'EOF'
<PROVIDER>_API_KEY=...
EOF
```

Puis redémarrez le daemon (ou redémarrez votre processus de passerelle) et revérifiez :

```bash
openclaw models status
openclaw doctor
```

Si vous préférez ne pas gérer les variables d'environnement vous-même, l'assistant d'intégration peut stocker les clés API pour l'utilisation du daemon : `openclaw onboard`.

Voir [Aide](/help) pour les détails sur l'héritage d'env (`env.shellEnv`,
`~/.openclaw/.env`, systemd/launchd).

## Anthropic : setup-token (authentification par abonnement)

Si vous utilisez un abonnement Claude, le flux setup-token est supporté. Exécutez-le sur l'**hôte de passerelle** :

```bash
claude setup-token
```

Puis collez-le dans OpenClaw :

```bash
openclaw models auth setup-token --provider anthropic
```

Si le token a été créé sur une autre machine, collez-le manuellement :

```bash
openclaw models auth paste-token --provider anthropic
```

Si vous voyez une erreur Anthropic comme :

```
This credential is only authorized for use with Claude Code and cannot be used for other API requests.
```

…utilisez plutôt une clé API Anthropic.

<Warning>
Le support du setup-token Anthropic est une compatibilité technique uniquement. Anthropic a bloqué certains usages d'abonnement en dehors de Claude Code par le passé. Utilisez-le uniquement si vous décidez que le risque politique est acceptable, et vérifiez vous-même les conditions actuelles d'Anthropic.
</Warning>

Entrée manuelle de token (n'importe quel fournisseur ; écrit `auth-profiles.json` + met à jour la config) :

```bash
openclaw models auth paste-token --provider anthropic
openclaw models auth paste-token --provider openrouter
```

Les références de profil d'authentification sont également supportées pour les credentials statiques :

- Les credentials `api_key` peuvent utiliser `keyRef: { source, provider, id }`
- Les credentials `token` peuvent utiliser `tokenRef: { source, provider, id }`

Vérification conviviale pour l'automatisation (sortie `1` en cas d'expiration/absence, `2` en cas d'expiration imminente) :

```bash
openclaw models status --check
```

Les scripts ops optionnels (systemd/Termux) sont documentés ici :
[/automation/auth-monitoring](/automation/auth-monitoring)

> `claude setup-token` nécessite un TTY interactif.

## Vérification du statut d'authentification du modèle

```bash
openclaw models status
openclaw doctor
```

## Comportement de rotation des clés API (passerelle)

Certains fournisseurs supportent la réessai d'une requête avec des clés alternatives lorsqu'un appel API atteint une limite de débit du fournisseur.

- Ordre de priorité :
  - `OPENCLAW_LIVE_<PROVIDER>_KEY` (remplacement unique)
  - `<PROVIDER>_API_KEYS`
  - `<PROVIDER>_API_KEY`
  - `<PROVIDER>_API_KEY_*`
- Les fournisseurs Google incluent également `GOOGLE_API_KEY` comme secours supplémentaire.
- La même liste de clés est dédupliquée avant utilisation.
- OpenClaw réessaie avec la clé suivante uniquement pour les erreurs de limite de débit (par exemple
  `429`, `rate_limit`, `quota`, `resource exhausted`).
- Les erreurs non liées à la limite de débit ne sont pas réessayées avec des clés alternatives.
- Si toutes les clés échouent, l'erreur finale de la dernière tentative est retournée.

## Contrôle du credential utilisé

### Par session (commande de chat)

Utilisez `/model <alias-or-id>@<profileId>` pour épingler un credential de fournisseur spécifique pour la session actuelle (exemples d'IDs de profil : `anthropic:default`, `anthropic:work`).

Utilisez `/model` (ou `/model list`) pour un sélecteur compact ; utilisez `/model status` pour la vue complète (candidats + profil d'authentification suivant, plus les détails du point de terminaison du fournisseur si configurés).

### Par agent (remplacement CLI)

Définissez un remplacement d'ordre de profil d'authentification explicite pour un agent (stocké dans le `auth-profiles.json` de cet agent) :

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Utilisez `--agent <id>` pour cibler un agent spécifique ; omettez-le pour utiliser l'agent par défaut configuré.

## Dépannage

### "No credentials found"

Si le profil de token Anthropic est manquant, exécutez `claude setup-token` sur l'
**hôte de passerelle**, puis revérifiez :

```bash
openclaw models status
```

### Token expirant/expiré

Exécutez `openclaw models status` pour confirmer quel profil expire. Si le profil
est manquant, réexécutez `claude setup-token` et collez le token à nouveau.

## Exigences

- Compte d'abonnement Anthropic (pour `claude setup-token`)
- Claude Code CLI installé (commande `claude` disponible)
