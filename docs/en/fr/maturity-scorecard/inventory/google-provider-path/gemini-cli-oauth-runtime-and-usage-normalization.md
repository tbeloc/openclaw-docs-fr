---
title: "Chemin du fournisseur Google - Note de maturité OAuth Gemini CLI"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin du fournisseur Google - Note de maturité OAuth Gemini CLI

## Résumé

Le chemin OAuth Gemini CLI existe en tant qu'exécution de fournisseur Google de première classe, avec
l'enregistrement du fournisseur, l'invocation du backend CLI, la connexion/actualisation OAuth, la migration des références héritées,
et la normalisation de l'utilisation. La couverture est Beta car la configuration, la documentation,
la source et les preuves unitaires sont présentes, mais la preuve en direct est limitée et le chemin est
sensible aux politiques. La qualité est Alpha car les archives montrent une confusion active concernant la précédence d'authentification,
le proxy, la session, la sécurité et la configuration, et la documentation avertit explicitement
que l'itinéraire est non officiel.

## Portée de la catégorie

Cette catégorie couvre le fournisseur `google-gemini-cli`, les références de modèle canoniques `google/*`
utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`,
l'invocation de commande Gemini CLI, la connexion/actualisation OAuth,
le formatage des jetons, les identifiants OAuth conscients du projet, et la normalisation de l'utilisation CLI.
Elle exclut le transport direct de clé API Gemini, Vertex, le cache de prompt, et Gemini Live.

## Fonctionnalités

- Sélection du runtime CLI : Couvre la sélection du runtime CLI sur le fournisseur `google-gemini-cli`, les références de modèle canoniques `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth gemini cli associé.
- Connexion et actualisation OAuth : Couvre la connexion et l'actualisation OAuth sur le fournisseur `google-gemini-cli`, les références de modèle canoniques `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth gemini cli associé.
- Références de modèle Google canoniques : Couvre les références de modèle Google canoniques sur le fournisseur `google-gemini-cli`, les références de modèle canoniques `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth gemini cli associé.
- Normalisation de l'utilisation CLI : Couvre la normalisation de l'utilisation CLI sur le fournisseur `google-gemini-cli`, les références de modèle canoniques `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth gemini cli associé.
- Diagnostics OAuth : Couvre les diagnostics OAuth sur le fournisseur `google-gemini-cli`, les références de modèle canoniques `google/*` utilisant `agentRuntime.id: "google-gemini-cli"`, les références héritées `google-gemini-cli/*`, l'invocation de commande Gemini CLI, et le comportement OAuth gemini cli associé.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (72%)`
- Signaux positifs : La documentation couvre la configuration et les avertissements ; la source implémente l'enregistrement du fournisseur,
  la politique de runtime, l'invocation du backend CLI, la connexion/actualisation OAuth, et la récupération de l'utilisation ; les tests unitaires couvrent la compatibilité directe des modèles, les métadonnées de configuration,
  et le comportement de connexion OAuth locale.
- Signaux négatifs : La preuve en direct/e2e pour la connexion OAuth réelle, l'actualisation des jetons, et
  l'exécution des commandes CLI est clairsemée et dépend de l'état de l'hôte local.
- Lacunes d'intégration : Aucun flux en direct toujours actif n'a été trouvé qui prouve la sélection du profil OAuth,
  le routage canonique `google/*`, l'invocation CLI, et la génération de rapports d'utilisation ensemble.

## Score de qualité

- Score : `Alpha (60%)`
- Rapports Gitcrawl : #79585 signale que le profil OAuth Gemini CLI est ignoré pour
  les modèles canoniques `google/*` lorsque `GEMINI_API_KEY` est présent ; #46184 signale
  l'échec d'OAuth derrière un proxy HTTP sur macOS ; #53578 signale des tours lents après
  la mise à niveau ; #54289 soulève des préoccupations de sécurité concernant l'extraction non autorisée d'identifiants OAuth ; #67609 a été fermé après correction des demandes OAuth routées vers le mauvais
  hôte Google.
- Rapports Discrawl : Les archives montrent une confusion doctor/configuration autour de la sélection du runtime actuel, des métadonnées de transport Cloud Code corrigées, et une configuration OAuth Gemini CLI précédemment orpheline/cassée.
- Bonnes qualités : La source maintient le formatage des jetons OAuth, le comportement d'actualisation,
  la sérialisation du backend CLI, et la sélection du runtime du fournisseur dans le code du plugin Google explicite.
- Mauvaises qualités : Le chemin dépend de l'installation CLI locale de l'hôte, de l'état OAuth local,
  de la politique de compte Google, et de la précédence du profil de runtime, qui sont tous des sources visibles de fragilité opérationnelle.
- Exclu de la qualité : La présence ou l'absence de tests unitaires, d'intégration, e2e, en direct, et de flux de runtime réel ;
  ceux-ci sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Beta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/google-provider-path.md`.
- Signaux positifs : les archives de documentation, source, test, Gitcrawl, et preuves Discrawl couvrent la portée de la taxonomie pour la sélection du runtime CLI, la connexion et l'actualisation OAuth, les références de modèle Google canoniques, la normalisation de l'utilisation CLI, les diagnostics OAuth.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'itinéraire OAuth est non officiel et sensible aux restrictions de compte.
- L'installation et l'état de connexion locaux de Gemini CLI sont en dehors du contrôle direct d'OpenClaw.
- Les preuves archivées montrent que la précédence d'authentification et la sélection du profil du fournisseur restent
  confuses pour les utilisateurs.
- La normalisation de l'utilisation est implémentée, mais la preuve en direct avec la sortie CLI réelle n'est
  pas large.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/providers/google.md:70` avertit que le
  fournisseur `google-gemini-cli` est une intégration non officielle.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:89` documente
  la connexion OAuth Gemini CLI et `--set-default`.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:102` documente la
  forme de la politique de runtime pour les références de modèle canoniques `google/*`.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:124` documente les références de modèle héritées
  `google-gemini-cli/*`.
- `/Users/kevinlin/code/openclaw/docs/providers/google.md:439` documente la normalisation
  de l'utilisation JSON Gemini CLI.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:217`
  documente `google-gemini-cli`, la connexion, le modèle par défaut, et l'analyse de l'utilisation.

### Source

- `/Users/kevinlin/code/openclaw/extensions/google/gemini-cli-provider.ts:13`
  déclare l'ID du fournisseur `google-gemini-cli`.
- `/Users/kevinlin/code/openclaw/extensions/google/gemini-cli-provider.ts:27`
  enregistre la documentation du fournisseur, l'avertissement d'authentification, le correctif de configuration, la résolution dynamique des modèles,
  les hooks OAuth, et la récupération de l'instantané d'utilisation.
- `/Users/kevinlin/code/openclaw/extensions/google/cli-backend.ts:14` enregistre
  la commande du backend Gemini CLI et les arguments de session.
- `/Users/kevinlin/code/openclaw/extensions/google/gemini-auth.ts:3` analyse
  les identifiants de jetons JSON OAuth dans les en-têtes Google.
- `/Users/kevinlin/code/openclaw/extensions/google/oauth.ts:17` implémente
  la connexion OAuth Gemini CLI avec PKCE, rappel localhost, et secours manuel.
- `/Users/kevinlin/code/openclaw/extensions/google/oauth.ts:96` actualise
  les jetons OAuth Gemini CLI.
- `/Users/kevinlin/code/openclaw/extensions/google/oauth-token-shared.ts:9`
  analyse le JSON de jetons OAuth conscient du projet.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/gateway-models.profiles.live.test.ts:2019`
  inclut la gestion des références de fournisseur en direct pour `google-gemini-cli`.
- `/Users/kevinlin/code/openclaw/src/agents/models.profiles.live.test.ts:1323`
  exécute les chemins de profil de modèle en direct avec la gestion spéciale Google/Gemini CLI.
- Aucun test OAuth en direct toujours actif dédié et d'exécution de commande CLI n'a été
  trouvé pour cet audit.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/google/provider-models.test.ts:41`
  couvre la résolution de modèle Gemini CLI compatible en avant.
- `/Users/kevinlin/code/openclaw/extensions/google/setup-api.test.ts:21` couvre
  les métadonnées de configuration du backend Gemini CLI.
- `/Users/kevinlin/code/openclaw/extensions/google/oauth.local-login.test.ts:3`
  couvre le comportement du rappel de connexion OAuth locale.
- `/Users/kevinlin/code/openclaw/src/utils/provider-utils.test.ts:36` couvre
  la classification du fournisseur Gemini CLI.

### Requêtes Gitcrawl

Requête : `gitcrawl search issues "Gemini CLI OAuth google-gemini-cli" -R openclaw/openclaw --state all`

Résultats :

- #79585 `le profil OAuth google-gemini-cli est ignoré pour les modèles canoniques google/* lorsque GEMINI_API_KEY est présent`.
- #46184 OAuth échoue derrière un proxy HTTP sur macOS.
- #53578 comportement lent par tour après la mise à niveau.
- #84527 ajoute Antigravity CLI comme direction de remplacement.
- #68216 Le fournisseur Gemini CLI ne parvient pas à écrire les fichiers d'identité de l'espace de travail.
- #66093 Régression du secours de réinitialisation de session CLI.
- #54289 préoccupation concernant l'extraction non autorisée d'identifiants OAuth.

Requête : `gitcrawl search issues "google-gemini-cli provider routes OAuth requests" -R openclaw/openclaw --state all`

Résultats :

- #67609 fermé après correction des demandes OAuth routées vers `generativelanguage.googleapis.com` au lieu de `cloudcode-pa.googleapis.com`.

### Requêtes Discrawl

Requête : `discrawl search --limit 5 "Gemini CLI OAuth google-gemini-cli"`

Résultats :

- Retourné une confusion setup/doctor où l'utilisateur avait un runtime actuel de
  `google-gemini-cli` tandis que son chemin de modèle principal était différent.
- Retourné les notes de fermeture #67609 indiquant que le main actuel utilise les métadonnées de transport Cloud Code
  pour OAuth Gemini CLI.
- Retourné les notes de fermeture #65318 concernant la configuration OAuth Gemini CLI précédemment orpheline/cassée
  dans v2026.4.10.
