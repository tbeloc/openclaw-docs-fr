---
title: "Automatisation des navigateurs et outils exec/sandbox - Note de maturité Sandboxed Browser et Codex Dynamic Tools"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automatisation des navigateurs et outils exec/sandbox - Note de maturité Sandboxed Browser et Codex Dynamic Tools

## Résumé

Sandboxed browser et Codex dynamic tools est en Beta. Le chemin du navigateur sandbox Docker a une implémentation réelle et des tests : authentification du relais CDP, jetons noVNC, hachages de configuration du navigateur, publication en loopback, réutilisation de pont et démarrage automatique. Codex dynamic tools a également une conception claire de fermeture en cas d'échec qui expose `sandbox_exec` et `sandbox_process` lorsque le sandboxing OpenClaw désactive le Code Mode natif de l'hôte. Le score reste Beta car le sandboxing des navigateurs non-Docker n'est pas supporté, le serveur exec-sandbox Codex est en aperçu/local uniquement, et plusieurs rapports actifs mentionnent la disponibilité du sandbox du navigateur et les frictions CDP/noVNC.

## Portée de la catégorie

Cette note couvre la configuration du sandbox du navigateur, la création du conteneur du navigateur Docker, l'authentification du relais CDP, le flux de mot de passe/jeton noVNC, le serveur de pont du navigateur, les plages sources CDP, la récréation du hachage de configuration, `allowHostControl`, les backends non supportés, la désactivation de l'exécution native Codex sous sandboxing OpenClaw actif, `sandbox_exec`, `sandbox_process`, et le serveur exec-sandbox Codex en aperçu.

## Fonctionnalités

- Sandboxed Browser : Couvre Sandboxed Browser sur la configuration du sandbox du navigateur, la création du conteneur du navigateur Docker, l'authentification du relais CDP, le flux de mot de passe/jeton noVNC, et le comportement associé du navigateur sandbox et des outils dynamiques codex.
- Codex Dynamic Tools : Couvre Codex Dynamic Tools sur la configuration du sandbox du navigateur, la création du conteneur du navigateur Docker, l'authentification du relais CDP, le flux de mot de passe/jeton noVNC, et le comportement associé du navigateur sandbox et des outils dynamiques codex.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - La documentation décrit explicitement le démarrage automatique du navigateur sandbox, le réseau Docker dédié, la plage source CDP, les URL de jeton observateur noVNC, allowHostControl et les listes blanches de contrôle personnalisées.
  - La source implémente les vérifications du contrat d'image du navigateur Docker, l'authentification CDP, la gestion des mots de passe/jetons noVNC, la récréation du hachage de configuration, la publication des ports en loopback et la réutilisation du pont.
  - La documentation et la source Codex implémentent l'exécution native en fermeture en cas d'échec et les outils dynamiques distincts soutenus par sandbox.
  - Les tests couvrent les arguments de création du sandbox du navigateur, l'authentification noVNC, l'authentification du relais CDP, les changements de politique de pont, l'exposition des outils dynamiques et le serveur exec-sandbox Codex.
- Signaux négatifs :
  - La documentation indique que le support du sandbox du navigateur est Docker uniquement ; SSH/OpenShell ne le supportent pas.
  - Le serveur exec-sandbox Codex est un chemin en aperçu nécessitant un support app-server plus récent et un app-server loopback local.
  - L'archive inclut des rapports target=sandbox browser indisponible et des demandes de support de sandbox de navigateur non-Docker.
- Lacunes d'intégration :
  - Ajouter une E2E de sandbox du navigateur de release-gate qui ouvre le flux de jeton noVNC, prouve l'authentification CDP et exécute l'instantané/l'action du navigateur via la cible sandbox.
  - Ajouter une vérification de compatibilité du serveur exec-sandbox app-server pour les versions app-server Codex supportées et une vérification de fermeture en cas d'échec pour les versions non supportées.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl :
  - `sandbox browser` a retourné le problème #84942 concernant le rapport de politique sandbox indiquant sandboxed alors que target=sandbox browser est indisponible, le problème #52662 pour les backends de sandbox de navigateur non-Docker, le problème #49609 pour l'encodage du presse-papiers noVNC, la PR #85572 ajoutant des vérifications de posture sandbox et le problème #64383 concernant la simplification du chemin CDP du sandbox du navigateur.
  - `sandbox browser sandbox_exec sandbox_process Codex app-server` n'a retourné aucun résultat ciblé, donc des preuves d'archive sandbox/navigateur plus larges ont été utilisées.
- Rapports Discrawl :
  - La recherche hybride `browser sandbox` a retourné un message de responsable du 2026-05-21 concernant l'utilisation de l'automatisation du navigateur à partir d'une devbox/session hébergée aux États-Unis et l'évitement des flux de travail du navigateur nécessitant un VPN.
  - La même recherche a retourné les notes de version du 2026-05-14 indiquant que l'appairage de l'interface utilisateur du navigateur/contrôle est devenu plus strict et la rédaction des résultats de transcription/outil est devenue plus cohérente.
  - `sandbox_exec sandbox_process browser sandbox` n'a retourné aucun résultat FTS de haut signal.
- Bonnes qualités :
  - L'image et la configuration du conteneur du sandbox du navigateur ont des vérifications de contrat/hachage explicites et des chemins de récréation de conteneur obsolète.
  - CDP et noVNC sont publiés sur loopback et protégés par des mécanismes d'authentification/jeton.
  - Le sandboxing OpenClaw actif désactive les surfaces d'exécution native Codex côté hôte au lieu de traiter silencieusement le sandbox hôte Codex comme équivalent.
  - L'exposition des outils dynamiques utilise des noms distincts `sandbox_exec`/`sandbox_process` et des conseils de suivi.
- Mauvaises qualités :
  - Le sandbox du navigateur est couplé à Docker aujourd'hui.
  - Le chemin CDP/noVNC/conteneur est sensible à la sécurité et opérationnellement compliqué.
  - Le serveur exec-sandbox Codex reste en aperçu et local uniquement, ce qui maintient le chemin stable intentionnellement en fermeture en cas d'échec.
- Exclu de la qualité :
  - Les preuves de test unitaire, intégration, e2e, live et flux d'exécution n'ont affecté que la couverture.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/browser-automation-and-exec-sandbox-tools.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Sandboxed Browser, Codex Dynamic Tools.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le support du sandbox de navigateur non-Docker a besoin d'une histoire de première partie ou d'un point d'extension clairement documenté.
- Le serveur exec-sandbox Codex doit rester Beta jusqu'à ce que le contrat d'environnement soit stable et couvert par l'intégration de release-gate.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:21`: le document de détails du navigateur en sandbox décrit le démarrage automatique, le réseau, la plage source CDP, l'URL du jeton noVNC, allowHostControl et les listes blanches de cibles personnalisées.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:78`: la matrice backend indique que le sandbox du navigateur est supporté sur Docker et non supporté sur SSH/OpenShell.
- `/Users/kevinlin/code/openclaw/docs/gateway/sandboxing.md:101`: le sandboxing OpenClaw actif désactive le Code Mode natif de Codex, l'MCP utilisateur et les plugins soutenus par l'application tout en exposant les outils soutenus par le sandbox.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness-reference.md:151`: la documentation Codex explique que le sandboxing OpenClaw actif désactive les surfaces d'exécution natives côté hôte.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness-reference.md:170`: l'exécution native en sandbox est en aperçu et échoue fermé par défaut.
- `/Users/kevinlin/code/openclaw/docs/plugins/codex-harness-reference.md:197`: le chemin d'aperçu démarre un serveur exec loopback soutenu par le sandbox actif et l'enregistre auprès du serveur d'application Codex.

### Source

- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.ts:77`: le navigateur sandbox attend la disponibilité CDP avec authentification.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.ts:162`: le contrat d'image du navigateur sandbox est vérifié avant utilisation.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.ts:210`: `ensureSandboxBrowser` crée ou réutilise un contexte de navigateur sandbox.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.ts:222`: le sandbox du navigateur est ignoré lorsque la politique d'outil sandbox ne permet pas le navigateur.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.ts:325`: les nouveaux conteneurs génèrent un mot de passe noVNC et un jeton d'authentification CDP.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.ts:364`: les ports CDP et noVNC sont publiés sur loopback.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.ts:478`: le serveur de pont du navigateur démarre avec la configuration résolue, l'authentification, le démarrage automatique et le résolveur de jeton noVNC.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/novnc-auth.ts:58`: les jetons observateurs noVNC sont des jetons à usage unique de courte durée.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/dynamic-tool-build.ts:508`: les outils dynamiques du shell sandbox sont ajoutés lorsque le sandboxing OpenClaw désactive l'exécution native.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/dynamic-tool-build.ts:526`: `sandbox_exec` enveloppe exec et réécrit les conseils de suivi en `sandbox_process`.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/native-execution-policy.ts:63`: la politique d'exécution native mappe auto vers sandbox/gateway et bloque les surfaces natives ciblées par node.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/sandbox-exec-server.ts:60`: l'environnement du serveur exec sandbox Codex est enregistré uniquement lorsqu'un backend sandbox actif existe.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/browser-cdp-snapshot-docker.sh:84`: Docker browser E2E valide l'interaction du navigateur soutenue par CDP.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/sandbox-exec-server.test.ts:116`: le serveur exec sandbox Codex achemine l'exécution du processus via un environnement soutenu par sandbox.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/sandbox-exec-server.http.test.ts:29`: le serveur exec sandbox Codex achemine les requêtes HTTP via le backend sandbox.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.create.test.ts:258`: vérifie que les images de navigateur sandbox obsolètes sont rejetées.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.create.test.ts:292`: vérifie la publication loopback noVNC et l'env de mot de passe.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.create.test.ts:431`: vérifie que la politique SSRF du navigateur est transmise au pont sandbox.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.create.test.ts:647`: vérifie que le relais CDP sandbox nécessite une authentification.
- `/Users/kevinlin/code/openclaw/src/agents/sandbox/browser.novnc-url.test.ts:26`: vérifie les jetons observateurs noVNC à usage unique.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/dynamic-tool-build.test.ts:219`: vérifie que les outils shell sandbox sont exposés pour les backends sandbox non-Docker.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/dynamic-tool-build.test.ts:689`: vérifie que les surfaces natives Codex sont désactivées lorsque le sandbox OpenClaw est actif.
- `/Users/kevinlin/code/openclaw/extensions/codex/src/app-server/dynamic-tool-build.test.ts:739`: vérifie que les surfaces natives du serveur exec sandbox restent derrière la politique d'outil sandbox.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "sandbox browser" --json`

Résultats :

- Problème ouvert #84942 : runtime en sandbox signalé alors que target=sandbox browser n'est pas disponible.
- Problème ouvert #52662 : le sandbox du navigateur devrait supporter les backends non-Docker.
- PR ouvert #85572 : ajouter les vérifications de conformité de posture sandbox.
- Problème ouvert #49609 : noVNC du navigateur sandbox brouille les caractères non-Latin-1.
- Problème ouvert #64383 : simplifier le chemin CDP du navigateur sandbox.

Requête :

`gitcrawl search openclaw/openclaw --query "sandbox browser sandbox_exec sandbox_process Codex app-server" --json`

Résultats :

- Aucun résultat ciblé retourné ; les résultats `sandbox browser` plus larges fournissent les preuves d'archive actuelles.

### Requêtes Discrawl

Requête :

`discrawl search --mode hybrid --limit 5 "browser sandbox"`

Résultats :

- 2026-05-21 l'archive des mainteneurs discute de l'automatisation du navigateur à partir d'une devbox/session hébergée et des alternatives Playwright/Chrome locales.
- 2026-05-14 l'archive de version note un appairage setup/browser/control UI plus strict et une rédaction de transcript/tool-result plus cohérente.

Requête :

`discrawl search --mode fts --limit 5 "sandbox_exec sandbox_process browser sandbox"`

Résultats :

- Aucun résultat FTS à haut signal.
