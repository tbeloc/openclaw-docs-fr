---
title: "WhatsApp - Note de Maturité Accès et Identité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Note de Maturité Accès et Identité

## Résumé

L'appairage WhatsApp, la connexion et l'authentification de session sont en Beta. La connexion QR principale,
l'authentification par compte, la récupération des identifiants corrompus, la déconnexion/reliaison et les chemins du magasin d'appairage DM
sont documentés et soutenus par la source, mais la preuve en direct commence principalement après
que les identifiants existent déjà et les preuves d'archive montrent toujours le churn QR/session et
les limites de profil.

## Normalisation

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Access and Identity`
- Fusionnée depuis : `Access Control`
- Report de score : minimum conservateur des scores de catégorie source fusionnés.

## Portée de la catégorie

Inclus dans cette catégorie :

- Connexion QR : flux de connexion QR et flux QR de connexion d'agent
- Persistance d'authentification multi-fichiers Baileys : persistance d'authentification multi-fichiers Baileys, écritures d'identifiants en file d'attente, restauration de sauvegarde et récupération de connexion.
- Défi d'appairage DM : défi d'appairage DM et persistance du magasin d'autorisation où elle croise WhatsApp
- Résolution multi-compte/compte par défaut : résolution multi-compte/compte par défaut et récupération Baileys 515/401
- dmPolicy de message direct : dmPolicy de message direct, allowFrom, défi d'appairage, magasin d'appairage
- Extraction d'identité de l'expéditeur : extraction d'identité de l'expéditeur, accusés de réception, protections de chat personnel et correspondance de contacts.
- Contrôles de confidentialité pour les crochets de plugin : contrôles de confidentialité pour les crochets de plugin et contexte non fiable
- `dmPolicy` de message direct : couvre le comportement `dmPolicy` de message direct, `allowFrom`, défi d'appairage, magasin d'appairage.
- Extraction d'identité de l'expéditeur : couvre l'extraction d'identité de l'expéditeur, les accusés de réception, les protections de chat personnel, le contact et le comportement.
- Contrôles de confidentialité pour les crochets de plugin et : couvre les contrôles de confidentialité pour les crochets de plugin et le comportement de contexte non fiable.

## Fonctionnalités

- Connexion QR : flux de connexion QR et flux QR de connexion d'agent
- Persistance d'authentification multi-fichiers Baileys : persistance d'authentification multi-fichiers Baileys, écritures d'identifiants en file d'attente, restauration de sauvegarde et récupération de connexion.
- Défi d'appairage DM : défi d'appairage DM et persistance du magasin d'autorisation où elle croise WhatsApp
- Résolution multi-compte/compte par défaut : résolution multi-compte/compte par défaut et récupération Baileys 515/401
- dmPolicy de message direct : dmPolicy de message direct, allowFrom, défi d'appairage, magasin d'appairage
- Extraction d'identité de l'expéditeur : extraction d'identité de l'expéditeur, accusés de réception, protections de chat personnel et correspondance de contacts.
- Contrôles de confidentialité pour les crochets de plugin : contrôles de confidentialité pour les crochets de plugin et contexte non fiable

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : la documentation couvre la connexion QR, la connexion spécifique au compte, l'approbation d'appairage,
  les chemins d'authentification, la reconnexion, la déconnexion et les comptes par défaut multi-comptes ; la source
  couvre l'authentification Baileys, les écritures en file d'attente, la restauration de sauvegarde, les barrières d'état d'authentification, la gestion du redémarrage 515
  et le nettoyage de déconnexion 401.
- Signaux négatifs : l'assurance qualité en direct standard utilise des archives d'authentification pré-louées et ne
  prouve pas régulièrement la première analyse QR, la reliaison ou l'isolation large des identifiants multi-comptes.
- Lacunes d'intégration : aucun scénario en direct situé n'exerce la première analyse QR,
  la reliaison de compte, le démarrage du compte secondaire et l'isolation d'authentification des limites de profil dans
  une matrice de régression.

## Score de qualité

- Score : `Beta (72%)`
- Rapports Gitcrawl : `WhatsApp QR login authDir pairing multi-account Baileys session restart` a surfacé l'ouverture #77066 crash de démarrage de compte secondaire ; `WhatsApp credentials leak across profile boundaries` a surfacé l'ouverture #64555 fuite d'identifiants entre les limites de profil.
- Rapports Discrawl : les recherches QR/login ont surfacé #51111 déconnexions device-removed, un fil où QR réussit mais l'écouteur ne démarre jamais avec récupération 515/logout répétée, problème de liaison QR Railway et discussions autour des correctifs de spam de code d'appairage.
- Bonnes qualités : les écritures d'identifiants sont en file d'attente et atomiques, les identifiants corrompus peuvent
  se restaurer à partir de la sauvegarde, le nettoyage des symlinks/répertoires personnalisés est gardé, les ID de compte sont
  normalisés et la documentation s'aligne avec les avertissements de source.
- Mauvaises qualités : Baileys est épinglé à la version candidate de sortie `7.0.0-rc13`, la connexion QR uniquement est fragile sur les hôtes distants/sans tête et les preuves d'archive récentes montrent des défauts multi-comptes/limites de profil.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas augmenté ni diminué ce score de qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la connexion QR, la persistance d'authentification multi-fichiers Baileys, le défi d'appairage DM, la résolution multi-compte/compte par défaut, la dmPolicy de message direct, l'extraction d'identité de l'expéditeur, les contrôles de confidentialité pour les crochets de plugin.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des scénarios récurrents en direct de première connexion QR et reliaison.
- Ajouter une preuve d'isolation d'authentification/profil multi-compte en direct large.
- Garder visible le travail de remise QR à distance/sans tête et la solution de secours par code téléphone jusqu'à ce que la friction opérationnelle QR soit réduite.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:8` indique que le canal est prêt pour la production via WhatsApp Web/Baileys et que Gateway possède les sessions liées.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:63` documente la connexion QR, la connexion spécifique au compte, le `authDir` personnalisé, l'approbation d'appairage et les avertissements QR uniquement.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:165` documente les sockets possédés par Gateway, les boucles de reconnexion, les écouteurs actifs et les règles de session DM/groupe.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:557` documente la sélection de compte, les chemins d'identifiants et la sémantique de déconnexion.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:134` documente la configuration multi-compte, le compte par défaut, la migration d'authentification héritée et les remplacements par compte.
- `/Users/kevinlin/code/openclaw/docs/concepts/qa-e2e-automation.md:694` documente les scénarios d'assurance qualité WhatsApp et le comportement du pool d'identifiants.

### Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/session.ts:129` crée le socket Baileys avec authentification multi-fichiers, sauvegarde d'identifiants en file d'attente, rappel QR et avertissement 401.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/login.ts:13` résout le répertoire de compte/authentification, restaure la sauvegarde, attend la connexion et gère les erreurs de reliaison.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/login-qr.ts:58` maintient la TTL de connexion QR active et l'état de connexion active par compte.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auth-store.ts:69` restaure les sauvegardes et signale les états d'authentification liés, non liés ou instables.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auth-store.ts:204` efface les fichiers d'authentification Baileys et gère le nettoyage de déconnexion.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/accounts.ts:21` résout la configuration de compte, la sélection du répertoire d'authentification et la gestion de l'authentification héritée.
- `/Users/kevinlin/code/openclaw/src/pairing/pairing-store.ts:35` définit les demandes en attente d'une heure, la portée par compte et la persistance du magasin d'autorisation.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:222` définit le `whatsapp-pairing-block` en direct.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.test.ts:154` vérifie l'enregistrement du scénario standard canary, pairing-block et mention-gating.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.web-auto-reply.connection-and-logging.e2e.test.ts:402` couvre le nettoyage de l'authentification/écouteur obsolète après les statuts terminaux.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/login.coverage.test.ts:119` couvre le redémarrage 515, la sortie QR, le nettoyage de déconnexion et les erreurs de connexion génériques.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/login-qr.test.ts:104` couvre le redémarrage QR, la déconnexion, l'authentification instable, les sessions récupérées et la rotation QR.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auth-store.test.ts:78` couvre la restauration de sauvegarde, les identifiants volumineux, la sécurité des symlinks et l'authentification instable.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/access-control.test.ts:85` couvre la grâce d'appairage, le `dmPolicy` au niveau du compte et le comportement d'appairage persistant.
- `/Users/kevinlin/code/openclaw/src/pairing/pairing-store.test.ts:301` couvre le cycle de vie, les limites, le magasin d'autorisation à portée de compte et les demandes en attente.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp qr login pairing session auth" --json`

Résultats :

- A surfacé le travail de connexion par code téléphone #85866, le besoin de solution de secours #85867 QR-unavailable/headless, #85868 appairage bloqué à Logging in jusqu'à ce que le redémarrage de Gateway finalise la récupération 515 et #75153 demande de contrôle de redémarrage de canal.

Requête :

`gitcrawl search openclaw/openclaw --query "WhatsApp credentials leak across profile boundaries" --json`

Résultats :

- A surfacé l'ouverture #64555 fuite d'identifiants entre les limites de profil.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp qr login pairing session auth" --limit 5`

Résultats :

- A retourné #51111 connexion QR liée brièvement puis déconnectée avec 401/device_removed, un fil où QR réussit mais l'écouteur ne démarre jamais avec identifiants corrompus restaurés et 515/logout répétée, problème de liaison QR de déploiement Railway et ancien bavardage de configuration.

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "WhatsApp pairing code auth" --limit 5`

Résultats :

- A retourné la discussion de correction `dmPolicy` de compte, la discussion de correction de spam de code d'appairage et les conseils de support d'appairage multi-compte.
