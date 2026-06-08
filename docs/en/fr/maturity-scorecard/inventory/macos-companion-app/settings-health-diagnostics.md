---
title: "Application compagnon macOS - Note de Maturité du Statut et des Paramètres"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon macOS - Note de Maturité du Statut et des Paramètres

## Résumé

La surface des paramètres et des diagnostics est large : Général/Connexion, Autorisations, Activation Vocale, Canaux, Compétences, Cron, Approbations Exec, Sessions, Instances, Config, Débogage, À propos, sondage de santé, cartes d'état des canaux, journaux de diagnostics continus et actions de débogage. La couverture est Bêta car les flux de paramètres et de santé sont larges avec des preuves de fumée/assistance, mais aucun scénario de diagnostic d'opérateur complet n'a été trouvé. La qualité est Bêta car l'implémentation et la documentation sont claires, tandis que les preuves d'archive montrent que les diagnostics et la santé des canaux restent des points de pression courants pour les opérateurs.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Statut de la barre de menu : Statut de la barre de menu, menu d'action, état de l'icône de statut, menu du dock, raccourcis tableau de bord/chat/canvas/talk
- Ingestion d'état d'activité : Ingestion d'état d'activité et comportement de la ligne de statut
- Navigation des paramètres : Navigation des paramètres et onglets
- Sondage de santé : Sondage de santé, statut des canaux, journaux, actions de débogage, visibilité config/session/instance
- Paramètres des canaux : Paramètres des canaux et statut QR/connexion/sonde surfacés via l'application

## Fonctionnalités

- Statut de la barre de menu : Statut de la barre de menu, menu d'action, état de l'icône de statut, menu du dock, raccourcis tableau de bord/chat/canvas/talk
- Ingestion d'état d'activité : Ingestion d'état d'activité et comportement de la ligne de statut
- Navigation des paramètres : Navigation des paramètres et onglets
- Sondage de santé : Sondage de santé, statut des canaux, journaux, actions de débogage, visibilité config/session/instance
- Paramètres des canaux : Paramètres des canaux et statut QR/connexion/sonde surfacés via l'application

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Bêta (72%)`
- Signaux positifs : La source couvre les groupes de paramètres, les onglets en cache lazy, la surveillance des autorisations, l'instantané du chemin config/état, le sondage de santé, le statut des canaux, le menu de débogage, la journalisation des fichiers continus et les magasins de paramètres des canaux. Les tests de fumée construisent les onglets de paramètres majeurs, les paramètres des canaux, les instances, les sessions, la config, le débogage et les assistants d'état de santé.
- Signaux négatifs : Aucun scénario d'opérateur complet ne prouve le diagnostic d'un canal cassé, la révélation des journaux, l'exécution d'une vérification de santé, la mise à jour de la config et la récupération d'une Gateway/canal depuis l'application macOS.
- Lacunes d'intégration : Besoin d'un flux de diagnostic d'application empaquetée pour la santé dégradée, la connexion/sonde du canal, la capture de journaux, l'édition de config et le basculement du mode distant/local.

## Score de Qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl : Les résultats incluent des problèmes de santé des diagnostics/journaux tels que #84787 le statut passe 40-50s dans la résolution du résumé/runtime du modèle, #84012 le statut se bloque avant la connexion Gateway, #53684 la récupération/notification d'échec de gateway, et #87402 le conflit d'écouteur géré. Les résultats de la requête de paramètres des canaux incluent les PR de paramètres d'application et les rapports liés aux canaux.
- Rapports Discrawl : Les rapports des responsables mettent en évidence le travail de qualité/diagnostics, les fumées d'observabilité, les correctifs d'horodatage/suivi des journaux, la gestion des plist macOS et les listes de contrôle de test de version qui incluent `openclaw status`, `openclaw doctor`, les journaux, le canal/fournisseur et la version exacte.
- Bonnes qualités : Les paramètres sont groupés par tâche d'opérateur, le magasin de santé met en cache le dernier succès/erreur pour éviter le scintillement, la journalisation de débogage est explicitement sensible/désactivée par défaut, et les paramètres peuvent rouvrir l'intégration pour la récupération des autorisations.
- Mauvaises qualités : L'opérateur doit toujours raisonner sur la santé de l'application, le statut CLI/doctor, l'état du canal, les journaux Gateway, les tunnels distants et les autorisations natives. Les preuves d'archive montrent que le statut/diagnostics peut se bloquer ou sous-expliquer la récupération.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux de runtime réel n'a pas été utilisée pour augmenter ou diminuer la Qualité.

## Score de Complétude

- Score : `Bêta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : Les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le Statut de la barre de menu, l'Ingestion d'état d'activité, la Navigation des paramètres, le Sondage de santé, les Paramètres des canaux.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Besoin d'une route de diagnostic native « quoi inspecter en premier » pour Gateway hors ligne, canal non lié, nœud déconnecté et tunnel distant dégradé.
- Besoin de preuves en direct que les actions QR/connexion/sonde du canal récupèrent les états de canal courants.
- Besoin d'un flux de partage/révision sécurisé plus facile pour les journaux de diagnostics.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/health.md` documente l'état de santé du menu/paramètres, le comportement de la sonde, l'instantané en cache et les vérifications CLI associées.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/logging.md` documente la journalisation des fichiers de diagnostics continus, la confidentialité de la journalisation unifiée et la gestion des journaux sensibles.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` documente la CLI de débogage de la connectivité gateway et les docs associées.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/remote.md` inclut le dépannage pour WebChat bloqué, nœud/capacité hors ligne et Activation Vocale.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/SettingsRootView.swift` définit les groupes d'onglets de paramètres et les routes des vues de détail pour Général, Connexion, Autorisations, Activation Vocale, Canaux, Compétences, Cron, Approbations Exec, Sessions, Instances, Config, Débogage et À propos.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/HealthStore.swift` sonde la santé, met en cache les instantanés/erreurs et dérive les états résumé/dégradé.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ChannelsSettings.swift` et `ChannelsStore*.swift` surfacent la config/statut/cycle de vie du canal.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/DiagnosticsFileLog.swift` implémente la journalisation des fichiers de diagnostics continus.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/DebugActions.swift` implémente les actions de débogage santé/journal/config.

### Tests d'intégration

- Aucun scénario de diagnostic d'opérateur natif complet n'a été trouvé.
- `/Users/kevinlin/code/openclaw/qa/scenarios/config/config-apply-restart-wakeup.md` et les scénarios QA associés couvrent le comportement Gateway/config, pas le chemin des paramètres natifs.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/SettingsViewSmokeTests.swift` rend de nombreuses vues de paramètres, y compris les autorisations, général, config, débogage, sessions, instances et activation vocale.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/ChannelsSettingsSmokeTests.swift` rend les paramètres des canaux.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/HealthStoreStateTests.swift`, `HealthDecodeTests.swift` et `LogLocatorTests.swift` couvrent les assistants santé/journal.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/ConfigStoreTests.swift`, `OpenClawConfigFileTests.swift` et `ConfigSchemaSupportTests.swift` couvrent le comportement de sauvegarde de config.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS diagnostics log health" --json`

Résultats :

- Problème #84787 `openclaw status passe 40-50s dans la résolution du résumé de session/runtime du modèle`.
- Problème #84012 `la commande CLI openclaw status se bloque avant de se connecter à la gateway`.
- Problème #53684 `Mécanisme de récupération et de notification d'échec de Gateway`.
- Problème #87402 `Le redémarrage de Gateway traite l'écouteur géré comme un conflit de port`.

Requête :

`gitcrawl search openclaw/openclaw --query "macOS app channel settings" --json`

Résultats :

- PR #59214 `Ajouter le sélecteur de couleur de bulle de chat utilisateur pour l'application macOS`.
- Problème #82709 `Avertissements Doctor/config pour les combinaisons de battement cardiaque et de délai d'expiration risquées`.
- Le problème #70253 inclut la méthode d'installation `mac app` et le comportement du canal/config.
- La PR #58333 référence une version d'application macOS empaquetée pour l'interface utilisateur de config.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS diagnostics"`

Résultats :

- Le rapport du responsable du 2026-05-26 énumère le travail de qualité et de diagnostics, les fumées d'observabilité, les correctifs d'horodatage/suivi des journaux, la gestion des plist macOS et les scripts sûrs pour Windows.
- Le rapport du responsable du 2026-05-22 énumère le travail de diagnostics et la détection d'ascendance de gateway macOS.
- Le test bêta du 2026-05-16 demande aux utilisateurs d'inclure `openclaw status --all`, `openclaw doctor`, le canal/fournisseur et ce qui a changé après la mise à jour.
