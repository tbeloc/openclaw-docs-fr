---
summary: "Référence CLI pour `openclaw secrets` (reload, audit, configure, apply)"
read_when:
  - Re-resolving secret refs at runtime
  - Auditing plaintext residues and unresolved refs
  - Configuring SecretRefs and applying one-way scrub changes
title: "secrets"
---

# `openclaw secrets`

Utilisez `openclaw secrets` pour gérer les SecretRefs et maintenir l'intégrité de l'instantané d'exécution actif.

Rôles des commandes :

- `reload`: passerelle RPC (`secrets.reload`) qui re-résout les refs et échange l'instantané d'exécution uniquement en cas de succès complet (pas d'écritures de configuration).
- `audit`: analyse en lecture seule des magasins de configuration/authentification/modèles générés et des résidus hérités pour le texte brut, les refs non résolues et la dérive de précédence.
- `configure`: planificateur interactif pour la configuration des fournisseurs, le mappage des cibles et les vérifications préalables (TTY requis).
- `apply`: exécute un plan enregistré (`--dry-run` pour validation uniquement), puis nettoie les résidus de texte brut ciblés.

Boucle d'opérateur recommandée :

```bash
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets audit --check
openclaw secrets reload
```

Note sur le code de sortie pour CI/gates :

- `audit --check` retourne `1` en cas de résultats.
- les refs non résolues retournent `2`.

Liens connexes :

- Guide des secrets : [Secrets Management](/fr/gateway/secrets)
- Surface des credentials : [SecretRef Credential Surface](/fr/reference/secretref-credential-surface)
- Guide de sécurité : [Security](/fr/gateway/security)

## Recharger l'instantané d'exécution

Re-résout les refs de secrets et échange atomiquement l'instantané d'exécution.

```bash
openclaw secrets reload
openclaw secrets reload --json
```

Notes :

- Utilise la méthode RPC de passerelle `secrets.reload`.
- Si la résolution échoue, la passerelle conserve le dernier instantané connu bon et retourne une erreur (pas d'activation partielle).
- La réponse JSON inclut `warningCount`.

## Audit

Analyse l'état d'OpenClaw pour :

- stockage de secrets en texte brut
- refs non résolues
- dérive de précédence (credentials `auth-profiles.json` masquant les refs `openclaw.json`)
- résidus générés `agents/*/agent/models.json` (valeurs `apiKey` du fournisseur et en-têtes de fournisseur sensibles)
- résidus hérités (entrées du magasin d'authentification hérité, rappels OAuth)

Note sur les résidus d'en-têtes :

- La détection d'en-têtes de fournisseur sensibles est basée sur l'heuristique de nom (noms d'en-têtes d'authentification/credentials courants et fragments tels que `authorization`, `x-api-key`, `token`, `secret`, `password` et `credential`).

```bash
openclaw secrets audit
openclaw secrets audit --check
openclaw secrets audit --json
```

Comportement de sortie :

- `--check` sort avec un code non-zéro en cas de résultats.
- les refs non résolues sortent avec un code non-zéro de priorité plus élevée.

Points clés de la forme du rapport :

- `status`: `clean | findings | unresolved`
- `summary`: `plaintextCount`, `unresolvedRefCount`, `shadowedRefCount`, `legacyResidueCount`
- codes de résultats :
  - `PLAINTEXT_FOUND`
  - `REF_UNRESOLVED`
  - `REF_SHADOWED`
  - `LEGACY_RESIDUE`

## Configure (assistant interactif)

Construisez les modifications de fournisseur et SecretRef de manière interactive, exécutez les vérifications préalables et appliquez optionnellement :

```bash
openclaw secrets configure
openclaw secrets configure --plan-out /tmp/openclaw-secrets-plan.json
openclaw secrets configure --apply --yes
openclaw secrets configure --providers-only
openclaw secrets configure --skip-provider-setup
openclaw secrets configure --agent ops
openclaw secrets configure --json
```

Flux :

- Configuration du fournisseur en premier (`add/edit/remove` pour les alias `secrets.providers`).
- Mappage des credentials en deuxième (sélectionnez les champs et assignez les refs `{source, provider, id}`).
- Vérifications préalables et application optionnelle en dernier.

Drapeaux :

- `--providers-only`: configure `secrets.providers` uniquement, ignore le mappage des credentials.
- `--skip-provider-setup`: ignore la configuration du fournisseur et mappe les credentials aux fournisseurs existants.
- `--agent <id>`: limite la découverte et les écritures de cibles `auth-profiles.json` à un magasin d'agent.

Notes :

- Nécessite un TTY interactif.
- Vous ne pouvez pas combiner `--providers-only` avec `--skip-provider-setup`.
- `configure` cible les champs porteurs de secrets dans `openclaw.json` plus `auth-profiles.json` pour la portée d'agent sélectionnée.
- `configure` supporte la création de nouveaux mappages `auth-profiles.json` directement dans le flux du sélecteur.
- Surface supportée canonique : [SecretRef Credential Surface](/fr/reference/secretref-credential-surface).
- Il effectue une résolution préalable avant l'application.
- Les plans générés utilisent par défaut les options de nettoyage (`scrubEnv`, `scrubAuthProfilesForProviderTargets`, `scrubLegacyAuthJson` tous activés).
- Le chemin d'application est unidirectionnel pour les valeurs de texte brut nettoyées.
- Sans `--apply`, la CLI invite toujours `Apply this plan now?` après les vérifications préalables.
- Avec `--apply` (et sans `--yes`), la CLI invite une confirmation supplémentaire irréversible.

Note de sécurité du fournisseur Exec :

- Les installations Homebrew exposent souvent des binaires liés symboliquement sous `/opt/homebrew/bin/*`.
- Définissez `allowSymlinkCommand: true` uniquement si nécessaire pour les chemins de gestionnaire de paquets de confiance, et associez-le à `trustedDirs` (par exemple `["/opt/homebrew"]`).
- Sur Windows, si la vérification ACL n'est pas disponible pour un chemin de fournisseur, OpenClaw échoue de manière sécurisée. Pour les chemins de confiance uniquement, définissez `allowInsecurePath: true` sur ce fournisseur pour contourner les vérifications de sécurité du chemin.

## Appliquer un plan enregistré

Appliquez ou préflight un plan généré précédemment :

```bash
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --json
```

Détails du contrat du plan (chemins de cibles autorisés, règles de validation et sémantique d'échec) :

- [Secrets Apply Plan Contract](/fr/gateway/secrets-plan-contract)

Ce que `apply` peut mettre à jour :

- `openclaw.json` (cibles SecretRef + upserts/suppressions de fournisseurs)
- `auth-profiles.json` (nettoyage des cibles de fournisseur)
- résidus hérités `auth.json`
- `~/.openclaw/.env` clés de secrets connues dont les valeurs ont été migrées

## Pourquoi pas de sauvegardes de restauration

`secrets apply` n'écrit intentionnellement pas de sauvegardes de restauration contenant d'anciennes valeurs de texte brut.

La sécurité provient de vérifications préalables strictes + application atomique avec restauration en mémoire au meilleur effort en cas d'échec.

## Exemple

```bash
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets audit --check
```

Si `audit --check` signale toujours des résultats de texte brut, mettez à jour les chemins de cibles signalés restants et réexécutez l'audit.
