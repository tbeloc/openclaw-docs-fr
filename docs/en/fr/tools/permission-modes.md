---
summary: "Modes de permission pour l'exécution sur l'hôte, les approbations Codex Guardian et les sessions du harnais ACPX"
read_when:
  - Choosing auto, ask, allowlist, full, or deny for command permissions
  - Configuring Codex Guardian-reviewed approvals through tools.exec.mode
  - Comparing OpenClaw exec approvals with ACPX harness permissions
title: "Modes de permission"
---

Les modes de permission décident du niveau d'autorité qu'un agent possède avant de pouvoir exécuter des commandes sur l'hôte, écrire des fichiers ou demander un accès supplémentaire à un harnais backend. Commencez par `tools.exec.mode: "auto"` quand vous voulez qu'OpenClaw utilise d'abord les listes blanches, puis l'auto-examen natif Codex ou une route d'approbation humaine pour les cas non couverts.

<Note>
  Le mode de permission est distinct de `tools.exec.host=auto`. `tools.exec.host`
  choisit où une commande s'exécute. `tools.exec.mode` choisit comment l'exécution
  sur l'hôte est approuvée.
</Note>

## Défaut recommandé

Utilisez `auto` pour les agents de codage qui ont besoin d'un accès utile à l'hôte sans transformer chaque cas non couvert en invite humaine :

```bash
openclaw config set tools.exec.mode auto
openclaw approvals get
openclaw gateway restart
```

Ensuite, vérifiez la politique effective :

```bash
openclaw exec-policy show
```

En mode `auto`, OpenClaw exécute directement les correspondances de liste blanche déterministes. Les cas non couverts passent d'abord par l'auto-examinateur natif d'OpenClaw, puis reviennent à la route d'approbation humaine configurée si nécessaire.

## Modes d'exécution sur l'hôte OpenClaw

`tools.exec.mode` est la surface de politique normalisée pour l'`exec` sur l'hôte.

| Mode        | Comportement                                     | À utiliser quand                                    |
| ----------- | ------------------------------------------------ | --------------------------------------------------- |
| `deny`      | Bloquer l'exécution sur l'hôte.                  | Aucune commande d'hôte n'est autorisée.             |
| `allowlist` | Exécuter uniquement les commandes en liste blanche. | Vous avez un ensemble de commandes sûres connu.     |
| `ask`       | Exécuter les correspondances de liste blanche et demander pour les cas non couverts. | Un humain doit examiner les nouvelles commandes.    |
| `auto`      | Exécuter les correspondances de liste blanche, puis utiliser l'auto-examen. | Les sessions de codage ont besoin d'un accès gardé pratique. |
| `full`      | Exécuter l'exécution sur l'hôte sans invites.    | Cet hôte/session de confiance doit ignorer les portes d'approbation. |

Pour la politique complète d'exécution sur l'hôte, le fichier d'approbations local, le schéma de liste blanche, les bacs sûrs et le comportement de transfert, voir [Approbations d'exécution](/fr/tools/exec-approvals).

## Mappage Codex Guardian

Pour les sessions natives d'application-serveur Codex, `tools.exec.mode: "auto"` correspond aux approbations examinées par Codex Guardian quand les exigences Codex locales le permettent. OpenClaw envoie généralement :

| Champ Codex         | Valeur typique    |
| ------------------- | ----------------- |
| `approvalPolicy`    | `on-request`      |
| `approvalsReviewer` | `auto_review`     |
| `sandbox`           | `workspace-write` |

En mode `auto`, OpenClaw ne préserve pas les remplacements Codex non sûrs hérités tels que `approvalPolicy: "never"` ou `sandbox: "danger-full-access"`. Utilisez `tools.exec.mode: "full"` uniquement quand vous voulez intentionnellement la posture sans approbation.

Pour la configuration du serveur d'application, l'ordre d'authentification et les détails du runtime Codex natif, voir [Harnais Codex](/fr/plugins/codex-harness).

## Permissions du harnais ACPX

Les sessions ACPX sont non-interactives, elles ne peuvent donc pas cliquer sur une invite de permission TTY. ACPX utilise des paramètres séparés au niveau du harnais sous `plugins.entries.acpx.config` :

| Paramètre                   | Valeur commune  | Signification                                       |
| --------------------------- | --------------- | --------------------------------------------------- |
| `permissionMode`            | `approve-reads` | Approuver automatiquement les lectures uniquement.   |
| `permissionMode`            | `approve-all`   | Approuver automatiquement les écritures et commandes shell. |
| `permissionMode`            | `deny-all`      | Refuser toutes les invites de permission.           |
| `nonInteractivePermissions` | `fail`          | Abandonner quand une invite serait requise.         |
| `nonInteractivePermissions` | `deny`          | Refuser l'invite et continuer si possible.          |

Définissez les permissions ACPX séparément des approbations d'exécution OpenClaw :

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw config set plugins.entries.acpx.config.nonInteractivePermissions fail
openclaw gateway restart
```

Utilisez `approve-all` comme équivalent de soupape de secours ACPX pour une session de harnais sans invite. Pour les détails de configuration et les modes d'échec, voir [Configuration des agents ACP](/fr/tools/acp-agents-setup#permission-configuration).

## Choisir un mode

| Objectif                                      | Configurer                                                  |
| --------------------------------------------- | ----------------------------------------------------------- |
| Bloquer complètement les commandes d'hôte     | `tools.exec.mode: "deny"`                                   |
| Laisser exécuter uniquement les commandes sûres connues | `tools.exec.mode: "allowlist"`                              |
| Demander à un humain pour chaque nouvelle forme de commande | `tools.exec.mode: "ask"`                                    |
| Utiliser l'auto-examen Codex/OpenClaw avant les humains | `tools.exec.mode: "auto"`                                   |
| Ignorer complètement les approbations d'exécution sur l'hôte | `tools.exec.mode: "full"` plus fichier d'approbations d'hôte correspondant |
| Permettre aux sessions ACPX non-interactives d'écrire/exécuter | `plugins.entries.acpx.config.permissionMode: "approve-all"` |

Si une commande invite ou échoue toujours après le changement de mode, inspectez les deux couches :

```bash
openclaw approvals get
openclaw exec-policy show
```

L'exécution sur l'hôte utilise le résultat le plus strict de la configuration OpenClaw et du fichier d'approbations local de l'hôte. Les permissions du harnais ACPX ne relâchent pas les approbations d'exécution sur l'hôte, et les approbations d'exécution sur l'hôte ne relâchent pas les invites du harnais ACPX.

## Connexes

- [Approbations d'exécution](/fr/tools/exec-approvals)
- [Approbations d'exécution - avancé](/fr/tools/exec-approvals-advanced)
- [Harnais Codex](/fr/plugins/codex-harness)
- [Configuration des agents ACP](/fr/tools/acp-agents-setup#permission-configuration)
