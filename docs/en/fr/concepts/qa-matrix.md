---
summary: "Référence de maintenance pour la lane Matrix QA avec Docker : CLI, profils, variables d'environnement, scénarios et artefacts de sortie."
read_when:
  - Running pnpm openclaw qa matrix locally
  - Adding or selecting Matrix QA scenarios
  - Triaging Matrix QA failures, timeouts, or stuck cleanup
title: "Matrix QA"
---

La lane Matrix QA exécute le plugin `@openclaw/matrix` fourni contre un serveur d'accueil Tuwunel jetable dans Docker, avec des comptes de pilote, SUT et observateur temporaires ainsi que des salons pré-remplis. C'est la couverture de transport réel en direct pour Matrix.

Ceci est un outil réservé aux mainteneurs. Les versions OpenClaw empaquetées omettent intentionnellement `qa-lab`, donc `openclaw qa` n'est disponible que depuis une extraction de source. Les extractions de source chargent le runner fourni directement — aucune étape d'installation de plugin n'est nécessaire.

Pour un contexte plus large du framework QA, voir [Aperçu QA](/fr/concepts/qa-e2e-automation).

## Démarrage rapide

```bash
pnpm openclaw qa matrix --profile fast --fail-fast
```

Le simple `pnpm openclaw qa matrix` exécute `--profile all` et ne s'arrête pas à la première défaillance. Utilisez `--profile fast --fail-fast` pour une porte de version ; fragmentez le catalogue avec `--profile transport|media|e2ee-smoke|e2ee-deep|e2ee-cli` lors de l'exécution de l'inventaire complet en parallèle.

## Ce que fait la lane

1. Provisionne un serveur d'accueil Tuwunel jetable dans Docker (image par défaut `ghcr.io/matrix-construct/tuwunel:v1.5.1`, nom du serveur `matrix-qa.test`, port `28008`).
2. Enregistre trois utilisateurs temporaires — `driver` (envoie le trafic entrant), `sut` (le compte OpenClaw Matrix en test), `observer` (capture de trafic tiers).
3. Pré-remplit les salons requis par les scénarios sélectionnés (principal, threading, média, redémarrage, secondaire, liste d'autorisation, E2EE, vérification DM, etc.).
4. Démarre une passerelle OpenClaw enfant avec le plugin Matrix réel limité au compte SUT ; `qa-channel` n'est pas chargé dans l'enfant.
5. Exécute les scénarios en séquence, en observant les événements via les clients Matrix du pilote/observateur.
6. Démantèle le serveur d'accueil, écrit les artefacts de rapport et de résumé, puis se termine.

## CLI

```text
pnpm openclaw qa matrix [options]
```

### Drapeaux courants

| Drapeau               | Par défaut                                    | Description                                                                                                            |
| --------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `--profile <profile>` | `all`                                         | Profil de scénario. Voir [Profils](#profils).                                                                         |
| `--fail-fast`         | désactivé                                     | S'arrête après la première vérification ou le premier scénario échoué.                                                 |
| `--scenario <id>`     | —                                             | Exécute uniquement ce scénario. Répétable. Voir [Scénarios](#scénarios).                                              |
| `--output-dir <path>` | `<repo>/.artifacts/qa-e2e/matrix-<timestamp>` | Où les rapports, résumé, événements observés et le journal de sortie sont écrits. Les chemins relatifs se résolvent par rapport à `--repo-root`. |
| `--repo-root <path>`  | `process.cwd()`                               | Racine du référentiel lors de l'invocation depuis un répertoire de travail neutre.                                    |
| `--sut-account <id>`  | `sut`                                         | ID de compte Matrix à l'intérieur de la configuration de la passerelle QA.                                            |

### Drapeaux du fournisseur

La lane utilise un transport Matrix réel mais le fournisseur de modèle est configurable :

| Drapeau                  | Par défaut       | Description                                                                                                                               |
| ------------------------ | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `--provider-mode <mode>` | `live-frontier`  | `mock-openai` pour une distribution de simulation déterministe ou `live-frontier` pour les fournisseurs frontier en direct. L'alias hérité `live-openai` fonctionne toujours. |
| `--model <ref>`          | défaut du fournisseur | Référence `provider/model` primaire.                                                                                                             |
| `--alt-model <ref>`      | défaut du fournisseur | Référence `provider/model` alternative où les scénarios changent en cours d'exécution.                                                            |
| `--fast`                 | désactivé        | Activez le mode rapide du fournisseur où pris en charge.                                                                                                |

Matrix QA n'accepte pas `--credential-source` ou `--credential-role`. La lane provisionne des utilisateurs jetables localement ; il n'y a pas de pool de credentials partagé à louer.

## Profils

Le profil sélectionné décide quels scénarios s'exécutent.

| Profil          | Utilisez-le pour                                                                                                                                                                                      |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `all` (par défaut) | Catalogue complet. Lent mais exhaustif.                                                                                                                                                              |
| `fast`          | Sous-ensemble de porte de version qui exerce le contrat de transport en direct : canary, gating de mention, blocage de liste d'autorisation, forme de réponse, reprise de redémarrage, suivi de thread, isolation de thread, observation de réaction. |
| `transport`     | Threading au niveau du transport, DM, salle, autojoin, scénarios de mention/liste d'autorisation.                                                                                                                     |
| `media`         | Couverture des pièces jointes image, audio, vidéo, PDF, EPUB.                                                                                                                                             |
| `e2ee-smoke`    | Couverture E2EE minimale — réponse chiffrée de base, suivi de thread, succès du bootstrap.                                                                                                             |
| `e2ee-deep`     | Scénarios exhaustifs de perte d'état E2EE, sauvegarde, clé et récupération.                                                                                                                                |
| `e2ee-cli`      | Scénarios CLI `openclaw matrix encryption setup` et `verify *` pilotés via le harnais QA.                                                                                                                  |

Le mappage exact se trouve dans `extensions/qa-matrix/src/runners/contract/scenario-catalog.ts`.

## Scénarios

La liste complète des ID de scénario est l'union `MatrixQaScenarioId` dans `extensions/qa-matrix/src/runners/contract/scenario-catalog.ts:15`. Les catégories incluent :

- threading — `matrix-thread-*`, `matrix-subagent-thread-spawn`
- top-level / DM / salle — `matrix-top-level-reply-shape`, `matrix-room-*`, `matrix-dm-*`
- média — `matrix-media-type-coverage`, `matrix-room-image-understanding-attachment`, `matrix-attachment-only-ignored`, `matrix-unsupported-media-safe`
- routage — `matrix-room-autojoin-invite`, `matrix-secondary-room-*`
- réactions — `matrix-reaction-*`
- redémarrage et relecture — `matrix-restart-*`, `matrix-stale-sync-replay-dedupe`, `matrix-room-membership-loss`, `matrix-homeserver-restart-resume`, `matrix-initial-catchup-then-incremental`
- gating de mention et listes d'autorisation — `matrix-mention-*`, `matrix-allowlist-*`, `matrix-multi-actor-ordering`, `matrix-inbound-edit-*`, `matrix-mxid-prefixed-command-block`, `matrix-observer-allowlist-override`
- E2EE — `matrix-e2ee-*` (réponse de base, suivi de thread, bootstrap, cycle de vie de clé de récupération, variantes de perte d'état, comportement de sauvegarde serveur, hygiène des appareils, vérification SAS / QR / DM, redémarrage, rédaction d'artefacts)
- CLI E2EE — `matrix-e2ee-cli-*` (configuration du chiffrement, configuration idempotente, échec du bootstrap, cycle de vie de clé de récupération, multi-compte, aller-retour de réponse de passerelle, auto-vérification)

Passez `--scenario <id>` (répétable) pour exécuter un ensemble sélectionné à la main ; combinez avec `--profile all` pour ignorer le gating de profil.

## Variables d'environnement

| Variable                                | Par défaut                                | Effet                                                                                                                                                                                         |
| --------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OPENCLAW_QA_MATRIX_TIMEOUT_MS`         | `1800000` (30 min)                        | Limite supérieure stricte sur l'exécution entière.                                                                                                                                            |
| `OPENCLAW_QA_MATRIX_NO_REPLY_WINDOW_MS` | `8000`                                    | Fenêtre silencieuse pour les assertions sans réponse négatives. Limité à `≤` le délai d'exécution.                                                                                                                 |
| `OPENCLAW_QA_MATRIX_CLEANUP_TIMEOUT_MS` | `90000`                                   | Limite pour le démantèlement Docker. Les surfaces d'échec incluent la commande de récupération `docker compose ... down --remove-orphans`.                                                                           |
| `OPENCLAW_QA_MATRIX_TUWUNEL_IMAGE`      | `ghcr.io/matrix-construct/tuwunel:v1.5.1` | Remplacez l'image du serveur d'accueil lors de la validation par rapport à une version Tuwunel différente.                                                                                                             |
| `OPENCLAW_QA_MATRIX_PROGRESS`           | activé                                    | `0` réduit au silence les lignes de progression `[matrix-qa] ...` sur stderr. `1` les force activées.                                                                                                                   |
| `OPENCLAW_QA_MATRIX_CAPTURE_CONTENT`    | rédacté                                   | `1` conserve le corps du message et `formatted_body` dans `matrix-qa-observed-events.json`. Par défaut, rédige pour garder les artefacts CI sûrs.                                                                    |
| `OPENCLAW_QA_MATRIX_DISABLE_FORCE_EXIT` | désactivé                                 | `1` ignore le `process.exit` déterministe après l'écriture d'artefact. La valeur par défaut force la sortie car les handles de crypto natifs de matrix-js-sdk peuvent garder la boucle d'événements active au-delà de l'achèvement des artefacts. |
| `OPENCLAW_RUN_NODE_OUTPUT_LOG`          | non défini                                | Lorsqu'il est défini par un lanceur externe (par exemple `scripts/run-node.mjs`), Matrix QA réutilise ce chemin de journal au lieu de démarrer son propre tee.                                                                   |

## Artefacts de sortie

Écrits dans `--output-dir` :

- `matrix-qa-report.md` — Rapport de protocole Markdown (ce qui a réussi, échoué, a été ignoré et pourquoi).
- `matrix-qa-summary.json` — Résumé structuré adapté à l'analyse CI et aux tableaux de bord.
- `matrix-qa-observed-events.json` — Événements Matrix observés à partir des clients du pilote et de l'observateur. Les corps sont masqués sauf si `OPENCLAW_QA_MATRIX_CAPTURE_CONTENT=1`.
- `matrix-qa-output.log` — Sortie combinée stdout/stderr de l'exécution. Si `OPENCLAW_RUN_NODE_OUTPUT_LOG` est défini, le journal du lanceur externe est réutilisé à la place.

Le répertoire de sortie par défaut est `<repo>/.artifacts/qa-e2e/matrix-<timestamp>` afin que les exécutions successives ne s'écrasent pas mutuellement.

## Conseils de triage

- **L'exécution se bloque près de la fin :** les poignées de chiffrement natif `matrix-js-sdk` peuvent survivre au harnais. Par défaut, force une sortie propre `process.exit` après l'écriture des artefacts ; si vous avez défini `OPENCLAW_QA_MATRIX_DISABLE_FORCE_EXIT=1`, attendez-vous à ce que le processus traîne.
- **Erreur de nettoyage :** recherchez la commande de récupération imprimée (une invocation `docker compose ... down --remove-orphans`) et exécutez-la manuellement pour libérer le port du serveur d'accueil.
- **Fenêtres d'assertion négative instables en CI :** réduisez `OPENCLAW_QA_MATRIX_NO_REPLY_WINDOW_MS` (par défaut 8 s) quand CI est rapide ; augmentez-le sur les exécuteurs partagés lents.
- **Besoin de corps masqués pour un rapport de bogue :** réexécutez avec `OPENCLAW_QA_MATRIX_CAPTURE_CONTENT=1` et joignez `matrix-qa-observed-events.json`. Traitez l'artefact résultant comme sensible.
- **Version Tuwunel différente :** pointez `OPENCLAW_QA_MATRIX_TUWUNEL_IMAGE` vers la version en cours de test. La vérification de la voie ne concerne que l'image par défaut épinglée.

## Contrat de transport en direct

Matrix est l'une des trois voies de transport en direct (Matrix, Telegram, Discord) qui partagent une liste de contrôle de contrat unique définie dans [Aperçu QA → Couverture du transport en direct](/fr/concepts/qa-e2e-automation#live-transport-coverage). `qa-channel` reste la suite synthétique large et ne fait intentionnellement pas partie de cette matrice.

## Connexes

- [Aperçu QA](/fr/concepts/qa-e2e-automation) — pile QA globale et contrat de transport en direct
- [Canal QA](/fr/channels/qa-channel) — adaptateur de canal synthétique pour les scénarios sauvegardés par le référentiel
- [Tests](/fr/help/testing) — exécution des tests et ajout de couverture QA
- [Matrix](/fr/channels/matrix) — le plugin de canal en cours de test
