---
read_when:
  - Vous voyez une erreur et voulez corriger le chemin
  - L'installateur affiche « Succès » mais l'interface CLI ne fonctionne pas
summary: Centre de dépannage : Symptôme → Vérification → Correction
title: Dépannage
x-i18n:
  generated_at: "2026-02-03T07:49:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 00ba2a20732fa22ccf9bcba264ab06ea940e9d6e96b31290811ff21a670eaad2
  source_path: help/troubleshooting.md
  workflow: 15
---

# Dépannage

## Les soixante premières secondes

Exécutez ces commandes dans l'ordre :

```bash
openclaw status
openclaw status --all
openclaw gateway probe
openclaw logs --follow
openclaw doctor
```

Si la passerelle Gateway est accessible, effectuez une sonde approfondie :

```bash
openclaw status --deep
```

## Situations courantes « c'est cassé »

### `openclaw: command not found`

C'est presque toujours un problème de PATH Node/npm. Commencez ici :

- [Installation (Vérification d'intégrité du PATH Node/npm)](/install#nodejs--npm-path-sanity)

### L'installateur a échoué (ou vous avez besoin du journal complet)

Réexécutez l'installateur en mode verbeux pour voir la trace complète et la sortie npm :

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --verbose
```

Pour une installation bêta :

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --beta --verbose
```

Vous pouvez également définir `OPENCLAW_VERBOSE=1` à la place du drapeau.

### La passerelle Gateway « unauthorized », impossible de se connecter ou reconnexion persistante

- [Dépannage de la passerelle Gateway](/gateway/troubleshooting)
- [Authentification de la passerelle Gateway](/gateway/authentication)

### L'interface de contrôle échoue sur HTTP (identité d'appareil requise)

- [Dépannage de la passerelle Gateway](/gateway/troubleshooting)
- [Interface de contrôle](/web/control-ui#insecure-http)

### `docs.openclaw.ai` affiche une erreur SSL (Comcast/Xfinity)

Certaines connexions Comcast/Xfinity bloquent `docs.openclaw.ai` via Xfinity Advanced Security.
Désactivez Advanced Security ou ajoutez `docs.openclaw.ai` à la liste d'autorisation, puis réessayez.

- Aide Xfinity Advanced Security : https://www.xfinity.com/support/articles/using-xfinity-xfi-advanced-security
- Vérification rapide : essayez un point d'accès mobile ou un VPN pour confirmer qu'il s'agit d'un filtrage au niveau du FAI

### Le service affiche qu'il s'exécute, mais la sonde RPC échoue

- [Dépannage de la passerelle Gateway](/gateway/troubleshooting)
- [Processus/service en arrière-plan](/gateway/background-process)

### Échec du modèle/authentification (limite de débit, facturation, « all models failed »)

- [Modèle](/cli/models)
- [Concepts OAuth / Authentification](/concepts/oauth)

### `/model` affiche `model not allowed`

Cela signifie généralement que `agents.defaults.models` est configuré comme liste d'autorisation. Quand elle n'est pas vide, seules les clés de fournisseur/modèle de cette liste peuvent être sélectionnées.

- Vérifiez la liste d'autorisation : `openclaw config get agents.defaults.models`
- Ajoutez le modèle que vous souhaitez (ou videz la liste d'autorisation) puis réessayez `/model`
- Utilisez `/models` pour parcourir les fournisseurs/modèles autorisés

### Lors de la soumission d'un problème

Collez un rapport de sécurité :

```bash
openclaw status --all
```

Si possible, incluez la fin des journaux pertinents de `openclaw logs --follow`.
