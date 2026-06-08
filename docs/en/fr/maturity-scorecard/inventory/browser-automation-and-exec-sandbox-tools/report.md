---
title: "Rapport de maturité des outils d'automatisation de navigateur et d'exécution/sandbox"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité des outils d'automatisation de navigateur et d'exécution/sandbox

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (79%)`
- Qualité : `Beta (75%)`
- Complétude : `Beta (79%)`
- Fonctionnalités LTS : `2/3`

## Résumé

Ce rapport promeut les preuves de maturité archivées `browser-automation-and-exec-sandbox-tools` de `/Users/kevinlin/tmp/maturity/browser-automation-and-exec-sandbox-tools` dans le contrat d'inventaire actuel process-version-3.

Les scores de Couverture et Qualité de la catégorie proviennent des lignes de score soutenues par les preuves archivées. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                               | LTS | Couverture     | Qualité      | Complétude     | Fonctionnalités à évaluer                                                                                            |
| ---------------------------------------------------------------------- | --- | -------------- | ------------ | -------------- | --------------------------------------------------------------------------------------------------------------- |
| [Automatisation de navigateur](browser-actions-snapshots-and-artifacts.md)       | ❌  | `Beta (78%)`   | `Beta (74%)` | `Beta (78%)`   | Actions de navigateur, Snapshots, Artefacts, Service de plugin de navigateur, Profils, Sécurité du navigateur, SSRF, Contrôle à distance |
| [Invocation et exécution d'outils](exec-routing-and-process-lifecycle.md) | ✅  | `Stable (82%)` | `Beta (79%)` | `Stable (82%)` | Routage Exec, Cycle de vie des processus, API d'invocation d'outils directs, Node System.run, Approbations Exec d'hôte, Mode élevé    |
| [Politique de sandbox et d'outils](sandbox-backends-and-workspace-isolation.md) | ✅  | `Beta (76%)`   | `Beta (72%)` | `Beta (76%)`   | Backends Sandbox, Isolation de l'espace de travail, Navigateur en sandbox, Outils dynamiques Codex, Politique d'outils, Portes d'outils Sandbox  |

## Rubrique de notation

- Couverture :
  notation maturity-label pour l'intégration, e2e, live, ou les preuves de flux
  serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation maturity-label pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et du flux runtime réel sont des entrées de Couverture
  uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation maturity-label pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Automatisation de navigateur

Ancres de recherche : Actions de navigateur, Snapshots, Artefacts, automatisation de navigateur et outils d'exécution/sandbox actions de navigateur, snapshots et artefacts, actions de navigateur, snapshots et artefacts, Service de plugin de navigateur, Profils, automatisation de navigateur et outils d'exécution/sandbox service de plugin de navigateur et profils, service de plugin de navigateur et profils, Sécurité du navigateur, SSRF, Contrôle à distance, automatisation de navigateur et outils d'exécution/sandbox sécurité du navigateur, ssrf et contrôle à distance, sécurité du navigateur, ssrf et contrôle à distance.

Note de catégorie : [Automatisation de navigateur](browser-actions-snapshots-and-artifacts.md)

Décisions de notation :

- Couverture : `Beta (78%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Actions de navigateur : Couvre les actions de navigateur dans les schémas d'action d'outil de navigateur, les opérations navigate/act/snapshot/screenshot, les formats de snapshot AI/role/ARIA, le stockage de références d'action et le comportement connexe des actions de navigateur, snapshots et artefacts.
- Snapshots : Couvre les snapshots dans les schémas d'action d'outil de navigateur, les opérations navigate/act/snapshot/screenshot, les formats de snapshot AI/role/ARIA, le stockage de références d'action et le comportement connexe des actions de navigateur, snapshots et artefacts.
- Artefacts : Couvre les artefacts dans les schémas d'action d'outil de navigateur, les opérations navigate/act/snapshot/screenshot, les formats de snapshot AI/role/ARIA, le stockage de références d'action et le comportement connexe des actions de navigateur, snapshots et artefacts.
- Service de plugin de navigateur : Couvre le service de plugin de navigateur dans l'activation du plugin de navigateur fourni, l'enregistrement CLI du navigateur, le routage de la passerelle `browser.request`, le démarrage du service de contrôle et le comportement connexe du service de plugin de navigateur et des profils.
- Profils : Couvre les profils dans l'activation du plugin de navigateur fourni, l'enregistrement CLI du navigateur, le routage de la passerelle `browser.request`, le démarrage du service de contrôle et le comportement connexe du service de plugin de navigateur et des profils.
- Sécurité du navigateur : Couvre la sécurité du navigateur dans l'authentification du contrôle du navigateur, la validation de l'URL de navigation, les gardes de navigation retardée, la politique SSRF stricte du réseau privé et le comportement connexe de la sécurité du navigateur, ssrf et du contrôle à distance.
- SSRF : Couvre SSRF dans l'authentification du contrôle du navigateur, la validation de l'URL de navigation, les gardes de navigation retardée, la politique SSRF stricte du réseau privé et le comportement connexe de la sécurité du navigateur, ssrf et du contrôle à distance.
- Contrôle à distance : Couvre le contrôle à distance dans l'authentification du contrôle du navigateur, la validation de l'URL de navigation, les gardes de navigation retardée, la politique SSRF stricte du réseau privé et le comportement connexe de la sécurité du navigateur, ssrf et du contrôle à distance.

Documentation principale :

- `docs/tools/browser-control.md`
- `docs/help/testing.md`
- `docs/tools/browser.md`
- `docs/gateway/security/index.md`
- `docs/gateway/security/audit-checks.md`

### 2. Invocation et exécution d'outils

Ancres de recherche : Routage Exec, Cycle de vie des processus, automatisation de navigateur et outils d'exécution/sandbox routage exec et cycle de vie des processus, routage exec et cycle de vie des processus, API d'invocation d'outils directs, Node System.run, automatisation de navigateur et outils d'exécution/sandbox api d'invocation d'outils directs et node system.run, api d'invocation d'outils directs et node system.run, Approbations Exec d'hôte, Mode élevé, automatisation de navigateur et outils d'exécution/sandbox approbations exec d'hôte et mode élevé, approbations exec d'hôte et mode élevé.

Note de catégorie : [Invocation et exécution d'outils](exec-routing-and-process-lifecycle.md)

Décisions de notation :

- Couverture : `Stable (82%)`
- Qualité : `Beta (79%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Routage Exec : Couvre le routage Exec dans l'exécution au premier plan et en arrière-plan `exec`, `yieldMs`, les délais d'expiration, PTY et le comportement connexe du routage exec et du cycle de vie des processus.
- Cycle de vie des processus : Couvre le cycle de vie des processus dans l'exécution au premier plan et en arrière-plan `exec`, `yieldMs`, les délais d'expiration, PTY et le comportement connexe du routage exec et du cycle de vie des processus.
- API d'invocation d'outils directs : Couvre l'API d'invocation d'outils directs dans HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, la sémantique du corps de la requête et de l'authentification, la restauration de l'étendue de l'opérateur à secret partagé et le comportement connexe de l'api d'invocation d'outils directs et de node system.run.
- Node System.run : Couvre Node System.run dans HTTP `POST /tools/invoke`, Gateway RPC `tools.invoke`, la sémantique du corps de la requête et de l'authentification, la restauration de l'étendue de l'opérateur à secret partagé et le comportement connexe de l'api d'invocation d'outils directs et de node system.run.
- Approbations Exec d'hôte : Couvre les approbations Exec d'hôte dans la politique d'approbation exec, l'état des approbations locales, l'enregistrement et l'attente des demandes d'approbation, la consommation allow-once et le comportement connexe des approbations exec d'hôte et du mode élevé.
- Mode élevé : Couvre le mode élevé dans la politique d'approbation exec, l'état des approbations locales, l'enregistrement et l'attente des demandes d'approbation, la consommation allow-once et le comportement connexe des approbations exec d'hôte et du mode élevé.

Documentation principale :

- `docs/tools/exec.md`
- `docs/gateway/background-process.md`
- `docs/gateway/tools-invoke-http-api.md`
- `docs/gateway/operator-scopes.md`
- `docs/gateway/protocol.md`
- `docs/tools/exec-approvals.md`
- `docs/tools/exec-approvals-advanced.md`
- `docs/tools/elevated.md`

### 3. Politique de sandbox et d'outils

Ancres de recherche : Backends Sandbox, Isolation de l'espace de travail, automatisation de navigateur et outils d'exécution/sandbox backends sandbox et isolation de l'espace de travail, backends sandbox et isolation de l'espace de travail, Navigateur en sandbox, Outils dynamiques Codex, automatisation de navigateur et outils d'exécution/sandbox navigateur en sandbox et outils dynamiques codex, navigateur en sandbox et outils dynamiques codex, Politique d'outils, Portes d'outils Sandbox, automatisation de navigateur et outils d'exécution/sandbox politique d'outils et portes d'outils sandbox, politique d'outils et portes d'outils sandbox.

Note de catégorie : [Politique de sandbox et d'outils](sandbox-backends-and-workspace-isolation.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (76%)`
- LTS : ✅

Fonctionnalités :

- Backends Sandbox : Couvre les backends Sandbox dans les modes sandbox, les étendues, les racines de l'espace de travail, workspaceAccess et le comportement connexe des backends sandbox et de l'isolation de l'espace de travail.
- Isolation de l'espace de travail : Couvre l'isolation de l'espace de travail dans les modes sandbox, les étendues, les racines de l'espace de travail, workspaceAccess et le comportement connexe des backends sandbox et de l'isolation de l'espace de travail.
- Navigateur en sandbox : Couvre le navigateur en sandbox dans la configuration du navigateur sandbox, la création du conteneur de navigateur Docker, l'authentification du relais CDP, le flux de jeton/mot de passe noVNC et le comportement connexe du navigateur en sandbox et des outils dynamiques codex.
- Outils dynamiques Codex : Couvre les outils dynamiques Codex dans la configuration du navigateur sandbox, la création du conteneur de navigateur Docker, l'authentification du relais CDP, le flux de jeton/mot de passe noVNC et le comportement connexe du navigateur en sandbox et des outils dynamiques codex.
- Politique d'outils : Couvre la politique d'outils dans les profils d'outils, les groupes d'outils, la politique allow/deny, la politique du fournisseur et le comportement connexe de la politique d'outils et des portes d'outils sandbox.
- Portes d'outils Sandbox : Couvre les portes d'outils Sandbox dans les profils d'outils, les groupes d'outils, la politique allow/deny, la politique du fournisseur et le comportement connexe de la politique d'outils et des portes d'outils sandbox.

Documentation principale :

- `docs/gateway/sandboxing.md`
- `docs/gateway/sandbox-vs-tool-policy-vs-elevated.md`
- `docs/tools/multi-agent-sandbox-tools.md`
- `docs/plugins/codex-harness-reference.md`
- `docs/gateway/config-tools.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les documents et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/browser-automation-and-exec-sandbox-tools/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/browser-automation-and-exec-sandbox-tools`.
