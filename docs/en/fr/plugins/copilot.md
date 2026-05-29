---
summary: "Exécutez les tours d'agent OpenClaw intégrés via le harnais du SDK GitHub Copilot fourni"
title: "Harnais du SDK Copilot"
read_when:
  - You want to use the bundled GitHub Copilot SDK harness for an agent
  - You need configuration examples for the `copilot` runtime
  - You are wiring an agent to subscription Copilot (github / openclaw / copilot) and want it to run through the Copilot CLI
---

L'extension `copilot` fournie permet à OpenClaw d'exécuter les tours d'agent Copilot d'abonnement intégrés via la CLI GitHub Copilot (`@github/copilot-sdk`) au lieu du harnais PI intégré.

Utilisez le harnais du SDK Copilot lorsque vous souhaitez que la session CLI Copilot soit propriétaire de la boucle d'agent de bas niveau : exécution native des outils, compaction native (`infiniteSessions`) et état de thread géré par la CLI sous `copilotHome`. OpenClaw reste propriétaire des canaux de chat, des fichiers de session, de la sélection du modèle, des outils dynamiques OpenClaw (pontés), des approbations, de la livraison des médias, du miroir de transcription visible, des questions latérales `/btw` (gérées par le repli PI dans l'arborescence — voir [Questions latérales (`/btw`)](#side-questions-btw)) et `openclaw doctor`.

Pour la répartition plus large modèle/fournisseur/runtime, commencez par [Agent runtimes](/fr/concepts/agent-runtimes).

## Exigences

- OpenClaw avec l'extension `copilot` fournie disponible.
- Si votre config utilise `plugins.allow`, incluez `copilot` (l'id du manifeste dans `extensions/copilot/openclaw.plugin.json`). Une liste d'autorisation restrictive qui utilise le nom de package de style npm `@openclaw/copilot` laissera le plugin fourni bloqué et le runtime ne se chargera pas même avec `agentRuntime.id: "copilot"`.
- Un abonnement GitHub Copilot qui peut piloter la CLI Copilot (ou une entrée `gitHubToken` env / auth-profile pour les exécutions sans interface / cron).
- Un répertoire `copilotHome` accessible en écriture. Le harnais utilise par défaut `~/.openclaw/agents/<agentId>/copilot` pour une isolation complète par agent. La valeur par défaut de la plateforme (`%APPDATA%\copilot` sur Windows, `$XDG_CONFIG_HOME/copilot` ou `~/.config/copilot` ailleurs) est utilisée comme repli de sonde doctor lorsqu'aucune home explicite n'est définie.

`openclaw doctor` exécute le [contrat doctor](#doctor-and-probes) fourni pour l'extension ; les défaillances là-bas sont le moyen canonique de confirmer que l'environnement est prêt avant d'opter un agent.

## Installation SDK à la demande

Le runtime d'agent Copilot expédie son petit code TypeScript fourni à l'intérieur de la tarball openclaw, mais le package `@github/copilot-sdk` sous-jacent (et son binaire CLI `@github/copilot-<platform>-<arch>` spécifique à la plateforme) n'est **pas** installé par défaut — ensemble, ils ajoutent ~260 MB à votre empreinte d'installation openclaw, et la plupart des utilisateurs openclaw ne sélectionnent pas un modèle Copilot.

L'assistant propose d'installer le SDK la première fois que vous sélectionnez un modèle `github-copilot/*` **et** que votre config opte le modèle (ou son fournisseur) dans le runtime d'agent Copilot via `agentRuntime: { id: "copilot" }` (voir [Quickstart](#quickstart) ci-dessous). Sans l'opt-in, openclaw utilise son fournisseur GitHub Copilot intégré et ne demande jamais l'installation du SDK :

```
The Copilot agent runtime needs @github/copilot-sdk (~260 MB on first
install, downloads the @github/copilot CLI binary for your platform).
Install now? [Y/n]
```

Si vous acceptez, le SDK est installé dans `~/.openclaw/npm-runtime/copilot/` et détecté lors des exécutions suivantes. L'installation exécute `npm ci` contre un `package-lock.json` enregistré expédié avec openclaw à `src/commands/copilot-sdk-install-manifest/package-lock.json`, donc le graphe transitif exact examiné pour cette version se retrouve sur le disque sur chaque machine utilisateur.

Si vous refusez, le runtime échouera à la première invocation avec un message d'installation exploitable ; réexécutez `openclaw setup` pour réessayer l'installation (ou copiez le manifeste épinglé dans `~/.openclaw/npm-runtime/copilot/` et exécutez `npm ci` vous-même si vous devez installer hors ligne).

Le runtime résout le SDK dans cet ordre :

1. `import("@github/copilot-sdk")` contre l'installation openclaw hôte (couvre les checkouts source/dev et tout environnement qui pré-installe le SDK aux côtés d'openclaw).
2. Le répertoire de repli bien connu `~/.openclaw/npm-runtime/copilot/` (la cible d'installation de l'assistant).

Un SDK manquant affiche une seule erreur avec le code `COPILOT_SDK_MISSING` et la commande d'installation manuelle ci-dessus.

## Démarrage rapide

Épinglez un modèle (ou un fournisseur) au harnais :

```json5
{
  agents: {
    defaults: {
      model: "github-copilot/gpt-5.5",
      models: {
        "github-copilot/gpt-5.5": {
          agentRuntime: { id: "copilot" },
        },
      },
    },
  },
}
```

Les deux routes sont équivalentes. Utilisez `agentRuntime.id` sur une seule entrée de modèle lorsque seul ce modèle doit être acheminé via le harnais ; définissez `agentRuntime.id` sur un fournisseur lorsque chaque modèle sous ce fournisseur doit l'utiliser.

## Fournisseurs pris en charge

Le harnais annonce le support du fournisseur canonique `github-copilot` (le même id détenu par `extensions/github-copilot`) :

- `github-copilot`

Tout ce qui se trouve en dehors de cet ensemble retombe dans la branche `auto_pi` de `selection.ts` vers PI.

## Authentification

Précédence par agent, appliquée lors de `runCopilotAttempt` :

1. **`useLoggedInUser: true` explicite** sur l'entrée de tentative. Utilise l'utilisateur connecté de la CLI Copilot résolu sous le `copilotHome` de l'agent.
2. **`gitHubToken` explicite** sur l'entrée de tentative (avec `profileId` + `profileVersion`). Utile pour les invocations CLI directes et les tests où l'appelant souhaite contourner la résolution du profil d'authentification.
3. **`resolvedApiKey` + `authProfileId` résolus par contrat** à partir de la forme `EmbeddedRunAttemptParams`. C'est le **chemin principal de production** : core résout le profil d'authentification `github-copilot` configuré de l'agent (via `src/infra/provider-usage.auth.ts:resolveProviderAuths`) avant d'invoquer le harnais, et le harnais consomme les deux champs directement. Cela rend un profil d'authentification `github-copilot:<profile>` fonctionnel de bout en bout pour les configurations sans interface / cron / multi-profil sans variables d'environnement.
4. **Repli de variable d'environnement** pour les exécutions CLI directes / dogfood où aucun profil d'authentification n'est configuré. Le runtime vérifie les variables suivantes dans l'ordre de précédence, reflétant le fournisseur `github-copilot` expédié (`extensions/github-copilot/auth.ts`) et la configuration documentée du SDK Copilot :
   1. `OPENCLAW_GITHUB_TOKEN` -- remplacement spécifique au harnais ; définissez ceci pour épingler un token pour le harnais OpenClaw sans perturber la config `gh` / CLI Copilot à l'échelle du système.
   2. `COPILOT_GITHUB_TOKEN` -- variable d'environnement standard du SDK / CLI Copilot.
   3. `GH_TOKEN` -- variable d'environnement standard de la CLI `gh` (correspond à la précédence du fournisseur `github-copilot` existant).
   4. `GITHUB_TOKEN` -- repli générique de token GitHub.

   La première valeur non vide gagne ; les chaînes vides sont traitées comme absentes. L'id du profil du pool synthétisé est `env:<NAME>` et la profileVersion est une empreinte sha256 non réversible du token, donc faire tourner la valeur env nettoie proprement le pool client.

5. **`useLoggedInUser` par défaut** lorsqu'aucun signal de token n'est disponible.

Chaque agent obtient un `copilotHome` dédié afin que les tokens, sessions et config de la CLI Copilot ne fuient pas entre les agents sur la même machine. La valeur par défaut est `<agentDir>/copilot` lorsque l'hôte remet un répertoire d'agent au harnais (isolant l'état du SDK du `models.json` / `auth-profiles.json` d'OpenClaw dans le même répertoire), ou `~/.openclaw/agents/<agentId>/copilot` sinon. Remplacez par `copilotHome: <path>` sur l'entrée de tentative lorsque vous avez besoin d'un emplacement personnalisé (par exemple, un montage partagé pour la migration).

`probeCopilotAuthShape` (voir [Doctor and probes](#doctor-and-probes)) est la vérification de forme pure qui valide lequel des modes ci-dessus sera utilisé. Elle n'effectue pas une poignée de main SDK en direct.

## Surface de configuration

Le harnais lit sa config à partir de l'entrée par tentative (`runCopilotAttempt({...})`) plus un petit ensemble de valeurs par défaut env à l'intérieur de `extensions/copilot/src/` :

- `copilotHome` — répertoire d'état CLI par agent (valeurs par défaut documentées ci-dessus).
- `model` — chaîne ou `{ provider, id, api? }`. Lorsqu'omis, OpenClaw utilise la sélection de modèle normale de l'agent et le harnais vérifie que le fournisseur résolu se trouve dans l'ensemble pris en charge.
- `reasoningEffort` — `"low" | "medium" | "high" | "xhigh"`. Mappe à partir de la résolution `ThinkLevel` / `ReasoningLevel` d'OpenClaw dans `auto-reply/thinking.ts`.
- `infiniteSessionConfig` — remplacement optionnel pour le bloc `infiniteSessions` du SDK piloté par `harness.compact`. Les valeurs par défaut sont sûres à laisser telles quelles.
- `hooksConfig` — config de pont optionnel exposant les hooks before/after-message-write d'OpenClaw à la boucle du SDK.
- `permissionPolicy` — remplacement optionnel pour le gestionnaire `onPermissionRequest` du SDK utilisé pour les types d'outils SDK intégrés (`shell`, `write`, `read`, `url`, `mcp`, `memory`, `hook`). La valeur par défaut est `rejectAllPolicy` comme filet de sécurité ; en pratique, le SDK n'invoque jamais aucun de ces types car chaque outil OpenClaw ponté est enregistré avec `overridesBuiltInTool: true` et `skipPermission: true` donc 100% des appels d'outils circulent via le `execute()` enrobé d'OpenClaw. Voir [Permissions and ask_user](#permissions-and-ask_user).
- `enableSessionTelemetry` — routage OpenTelemetry opt-in via `telemetry-bridge.ts`.

Rien dans le reste d'OpenClaw n'a besoin de connaître ces champs. Les autres plugins, canaux et code core ne voient que la forme standard `AgentHarnessAttemptParams` / `AgentHarnessAttemptResult`.

## Compaction

Lorsque `harness.compact` s'exécute, le harnais du SDK Copilot :

1. Active `infiniteSessions` sur la session du SDK.
2. Laisse le SDK effectuer sa compaction native.
3. Écrit un marqueur de forme OpenClaw à `workspacePath/files/openclaw-compaction-<ts>.json` afin que les lecteurs de transcription OpenClaw existants voient toujours un artefact familier.

Le miroir de transcription côté OpenClaw (voir ci-dessous) continue de recevoir les messages post-compaction, donc l'historique de chat visible par l'utilisateur reste cohérent.

## Mirroring de transcription

`runCopilotAttempt` écrit en double chaque message mirrorable du tour dans la transcription d'audit OpenClaw via `extensions/copilot/src/dual-write-transcripts.ts`. Le miroir est limité par session (`copilot:${sessionId}`) et utilise une identité par message (`${role}:${sha256_16(role,content)}`) afin que les réémissions d'entrées de tour antérieur entrent en collision avec les clés existantes sur le disque et ne se dupliquent pas.

Le miroir est enrobé dans deux couches de confinement d'échec afin qu'une défaillance d'écriture de transcription ne puisse pas échouer la tentative : un wrapper best-effort interne et une défense en profondeur `.catch(...)` au niveau de la tentative. Les défaillances sont enregistrées mais non affichées.

## Questions latérales (`/btw`)

`/btw` n'est **pas** natif sur ce harnais. `createCopilotAgentHarness()` laisse délibérément `harness.runSideQuestion` indéfini, donc le dispatcher `/btw` d'OpenClaw (`src/agents/btw.ts`) retombe dans le même chemin de repli PI dans l'arborescence qu'il utilise pour chaque runtime non-Codex : le fournisseur de modèle configuré est appelé directement avec un court prompt de question latérale et diffusé en retour via `streamSimple` (pas de session CLI, pas de slot de pool supplémentaire).

Cela garde les sessions CLI Copilot réservées à la boucle de tour principal de l'agent, et garde le comportement `/btw` identique aux autres runtimes soutenus par PI. Le contrat est affirmé dans [`extensions/copilot/harness.test.ts`](https://github.com/openclaw/openclaw/blob/main/extensions/copilot/harness.test.ts) sous `describe("runSideQuestion")`.

## Docteur et sondes

`extensions/copilot/doctor-contract-api.ts` est chargé automatiquement par
`src/plugins/doctor-contract-registry.ts`. Il contribue :

- Un `legacyConfigRules` vide (aucun champ retiré au MVP).
- Un `normalizeCompatibilityConfig` sans opération (conservé pour que les
  retraits de champs futurs aient un foyer stable dans l'arborescence).
- Une entrée `sessionRouteStateOwners` revendiquant le fournisseur
  `github-copilot` ; l'exécution `copilot` ; la clé de session CLI
  `copilot` ; le préfixe du profil d'authentification `github-copilot:`.

`extensions/copilot/src/doctor-probes.ts` exporte trois sondes impératives
que les hôtes (y compris `openclaw doctor`) peuvent appeler pour vérifier
l'environnement :

| Sonde                      | Ce qu'elle vérifie                                                                | Raisons pour lesquelles elle peut échouer                                        |
| -------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `probeCopilotCliVersion`   | `copilot --version` se termine avec le code 0 et une chaîne de version non vide   | `non-zero-exit`, `empty-version`, `spawn-failed`, `spawn-error`, `probe-timeout` |
| `probeCopilotHomeWritable` | `mkdir -p copilotHome` + écriture + suppression d'un fichier marqueur             | `copilothome-not-writable` (avec l'erreur fs sous-jacente dans `details.rawError`) |
| `probeCopilotAuthShape`    | Au moins l'un de `useLoggedInUser`, `gitHubToken`, ou `profileId`+`profileVersion` | `no-auth-source`                                                                 |

Chaque sonde accepte une couche d'injection de dépendances (`spawnFn`,
`fsApi`) pour que les tests ne lancent pas le vrai CLI Copilot ni ne
touchent le système de fichiers de l'hôte.

## Limitations

- Le harnais ne revendique que le fournisseur canonique `github-copilot` au
  MVP. Les fournisseurs supplémentaires (BYOK ou autres) doivent arriver
  dans les PR de suivi qui livrent l'adaptateur avec le câblage.
- Le harnais ne fournit pas d'interface TUI ; l'interface TUI de PI n'est
  pas affectée et reste le recours pour tous les runtimes qui n'ont pas de
  surface homologue.
- L'état de session PI n'est pas migré quand un agent bascule vers
  `copilot`. La sélection se fait par tentative ; les sessions PI existantes
  restent valides.
- **L'`ask_user` interactif n'est pas encore câblé.** Le gestionnaire
  `onUserInputRequest` du SDK n'est intentionnellement pas enregistré, ce qui
  selon le contrat du SDK masque complètement l'outil `ask_user` au modèle.
  Les agents s'exécutant sous ce harnais prennent des décisions au mieux de
  leur jugement à partir de l'invite initiale plutôt que de poser des
  questions de clarification en cours de tour. Un suivi portera le motif
  codex à `extensions/codex/src/app-server/user-input-bridge.ts` pour
  acheminer les `UserInputRequest`s du SDK via le chemin du canal OpenClaw
  ou de l'invite TUI ; l'échafaudage dormant dans
  `extensions/copilot/src/user-input-bridge.ts` est la surface que le suivi
  câblera.

## Permissions et ask_user

L'application des permissions pour les outils OpenClaw pontés se fait
**à l'intérieur du wrapper d'outil**, pas via le rappel
`onPermissionRequest` du SDK. Le même `wrapToolWithBeforeToolCallHook` que
PI utilise (`src/agents/pi-tools.before-tool-call.ts`) est appliqué par
`createOpenClawCodingTools` à chaque outil de codage : détection de boucles,
politiques de plugins de confiance, hooks avant appel d'outil, et approbations
de plugins en deux phases via la passerelle (`plugin.approval.request`) s'exécutent
tous avec le même chemin de code que les tentatives PI natives.

Pour laisser ce wrapper prendre la décision, l'outil SDK retourné par
`convertOpenClawToolToSdkTool` est marqué avec :

- `overridesBuiltInTool: true` — remplace l'outil intégré du CLI Copilot du
  même nom (edit, read, write, bash, …) pour que chaque invocation d'outil
  soit redirigée vers OpenClaw.
- `skipPermission: true` — indique au SDK de ne pas déclencher
  `onPermissionRequest({kind: "custom-tool"})` avant d'invoquer l'outil.
  L'`execute()` enveloppé effectue la vérification de politique OpenClaw plus
  riche en interne ; une invite au niveau du SDK court-circuiterait soit
  l'application d'OpenClaw (si nous autorisons tout) soit bloquerait chaque
  appel d'outil (si nous rejetons tout) — ni l'un ni l'autre ne correspond à
  la parité PI.

Le harnais codex dans l'arborescence utilise la même séparation : les outils
OpenClaw pontés sont enveloppés (`extensions/codex/src/app-server/dynamic-tools.ts`)
et les types d'approbation natifs propres au serveur d'application codex
(`item/commandExecution/requestApproval`,
`item/fileChange/requestApproval`,
`item/permissions/requestApproval`) sont acheminés via
`plugin.approval.request`
(`extensions/codex/src/app-server/approval-bridge.ts`). L'équivalent du SDK
Copilot — `rejectAllPolicy` fermé à l'échec pour tout type non-`custom-tool`
qui atteint jamais `onPermissionRequest` — est le même filet de sécurité, et
il ne se déclenche pas en pratique car `overridesBuiltInTool: true` remplace
chaque outil intégré.

Pour que la couche d'outil enveloppé prenne des décisions de politique
équivalentes à PI, le harnais transmet le contexte complet de tentative
d'outil PI à `createOpenClawCodingTools` — identité (`senderIsOwner`,
`memberRoleIds`, `ownerOnlyToolAllowlist`, …), canal/routage
(`groupId`, `currentChannelId`, `replyToMode`, bascules d'outil de message),
authentification (`authProfileStore`), identité d'exécution
(`sessionKey`/`runSessionKey` dérivés de `sandboxSessionKey`,
`runId`), contexte du modèle (`modelApi`, `modelContextWindowTokens`,
`modelCompat`, `modelHasVision`), et hooks d'exécution (`onToolOutcome`,
`onYield`). Sans ces champs, les listes blanches réservées au propriétaire
se comportent silencieusement comme un refus par défaut, les politiques de
confiance des plugins ne peuvent pas se résoudre au bon périmètre, et
`session_status: "current"` se résout en une clé sandbox obsolète. Le
constructeur de pont est dans `extensions/copilot/src/tool-bridge.ts` et
reflète l'appel faisant autorité PI à
`src/agents/pi-embedded-runner/run/attempt.ts:1029-1117`. Deux champs PI
ne sont intentionnellement **pas** transmis au MVP et sont suivis comme
des suites : `sandbox` (le harnais ne route pas encore via
`resolveSandboxContext`) et la machinerie de recherche d'outils/mode code
PI (`toolSearchCatalogRef`, `includeCoreTools`,
`includeToolSearchControls`, `toolSearchCatalogExecutor`,
`toolConstructionPlan`), qui n'a pas d'analogue à la limite du SDK.

### Jeton GitHub au niveau de la session

Le contrat du SDK Copilot distingue le jeton GitHub au **niveau client**
(`CopilotClientOptions.gitHubToken`, utilisé pour authentifier le processus
CLI lui-même) du jeton au **niveau session**
(`SessionConfig.gitHubToken`, qui détermine l'exclusion de contenu,
l'acheminement du modèle et le quota pour cette session et est honoré sur
`createSession` et `resumeSession`). Le harnais résout l'authentification une
fois via `resolveCopilotAuth` et définit les deux champs quand le mode
d'authentification est `gitHubToken` (un `auth.gitHubToken` explicite ou une
`resolvedApiKey` résolue par contrat à partir d'un profil d'authentification
`github-copilot` configuré). Quand le mode résolu est `useLoggedInUser`, le
champ au niveau session est omis pour que le SDK continue de dériver
l'identité de l'identité connectée.

`ask_user` est intentionnellement masqué — voir Limitations ci-dessus.

## Connexes

- [Runtimes d'agent](/fr/concepts/agent-runtimes)
- [Harnais Codex](/fr/plugins/codex-harness)
- [Plugins de harnais d'agent (référence SDK)](/fr/plugins/sdk-agent-harness)
