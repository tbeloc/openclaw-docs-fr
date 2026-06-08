---
title: "Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Zalo Personal / Zalouser Channel Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Feishu, QQ Bot, WeChat, Yuanbao, Zalo, Zalo Personal, regional channels - Zalo Personal / Zalouser Channel Maturity Note

## Résumé

Zalo Personal est un type de compte distinct du canal bot Zalo. Il utilise `zca-js` pour automatiser un compte personnel normal et la documentation avertit que l'automatisation non officielle peut entraîner la suspension ou le bannissement du compte. Les sources et les tests couvrent les profils QR/connexion, la portée du compte, les portes de groupe, les pairs de répertoire, les envois, les réactions, les outils, le statut, les vérifications du médecin et les adaptateurs de client Zalo. Le plafond de maturité est plus bas car l'intégration en amont est non officielle, la preuve de compte en direct n'est pas capturée dans cet audit, et les archives montrent des problèmes récents visibles par l'utilisateur autour du démarrage, des médias, des métadonnées de citation, de l'analyse de l'expéditeur et de la documentation des profils.

## Portée de la catégorie

- Plugin de canal `zalouser` pour l'automatisation du compte personnel Zalo via `zca-js` natif.
- Connexion QR, profils enregistrés, sélection multi-compte/profil et runtime local de passerelle.
- Appairage DM, politique de groupe, portage de groupe, pairs de répertoire et routage de l'expéditeur/session.
- Envoi de message, médias image/lien/document, réactions, statut, outils amis/groupes/moi et normalisation du style de texte.
- Vérifications du médecin/statut pour la disponibilité du runtime et la santé du profil/session.
- Risque explicite de compte non officiel et protections de l'opérateur.

## Fonctionnalités

- Plugin de canal zalouser : plugin de canal zalouser pour l'automatisation du compte personnel Zalo via zca-js natif
- Connexion QR : connexion QR, profils enregistrés, sélection multi-compte/profil et runtime local de passerelle
- Appairage DM : appairage DM, politique de groupe, portage de groupe, pairs de répertoire et routage de l'expéditeur/session
- Envoi de message : envoi de message, médias image/lien/document, réactions, statut, outils amis/groupes/moi et normalisation du style de texte
- Vérifications du médecin/statut pour la disponibilité du runtime : vérifications du médecin/statut pour la disponibilité du runtime et la santé du profil/session
- Risque explicite de compte non officiel : risque explicite de compte non officiel et protections de l'opérateur

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (58%)`
- Signaux positifs : les tests d'extension couvrent la configuration, la gestion QR/profil, la portée du compte, le comportement du moniteur, les portes de groupe, les pairs de répertoire, les envois, les réactions, le statut, les vérifications du médecin, le comportement des outils, la gestion du SID de message et les adaptateurs de client ZCA.
- Signaux négatifs : aucun scénario de compte personnel Zalo en direct actuel n'a été trouvé qui prouve la connexion QR, la persistance de session, la commutation de compte/profil, le routage de groupe, les médias, les réactions, les outils et la reconnexion par rapport au client/service Zalo réel.
- Lacunes d'intégration : la preuve de runtime répétable manque pour les limites de suspension/bannissement de compte, la reconnexion QR, la récupération de profil, les médias de document, les métadonnées de citation, les liens d'invitation de groupe et le comportement du moniteur à long terme.

Étiquettes de couverture :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct ou les preuves de flux de runtime réel dans le composant. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de qualité

- Score : `Alpha (52%)`
- Rapports Gitcrawl : une large recherche `zalouser` a retourné des rapports ouverts pour le blocage du compte de démarrage après reconnexion, les pièces jointes photo entrantes, la livraison en double de médias de document, le rendu markdown, les métadonnées de citation et les actions de lien d'invitation de groupe.
- Rapports Discrawl : les recherches `zalouser` et `Zalo Personal` ont retourné des notes de timing d'installation, un contexte de révision de nettoyage de délai d'attente, des corrections de routage de politique de mention et la PR `#69643` documentant les variables d'environnement de profil Zalo.
- Bonnes qualités : la documentation étiquette clairement le risque d'automatisation non officielle et sépare `zalouser` de `zalo` ; la source expose le médecin/statut, le compte/profil, la politique de groupe, le répertoire, les réactions, les outils et la normalisation du texte plutôt que de cacher la complexité de ZCA.
- Mauvaises qualités : l'automatisation en amont non officielle crée un risque de sécurité du compte ; les archives montrent que la documentation des profils est en retard, le risque d'analyse des étiquettes d'expéditeur, les blocages de démarrage, la duplication des médias, la perte de métadonnées de citation et les lacunes de rendu du client réel.
- Exclu de la qualité : présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux de runtime réel ; ce sont uniquement des entrées de couverture.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct ou de flux de runtime réel comme entrée de notation.

## Score de complétude

- Score : `Alpha (58%)`
- Instructions de surface : évaluées par rapport à `references/completeness/feishu-qq-bot-wechat-yuanbao-zalo-zalo-personal-regional-channels.md`.
- Signaux positifs : les preuves archivées, sources, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le plugin de canal zalouser, la connexion QR, l'appairage DM, l'envoi de message, les vérifications du médecin/statut pour la disponibilité du runtime, le risque explicite de compte non officiel.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un scénario Zalo Personal en direct pour la connexion QR, la sélection de profil, l'appairage DM, le routage de groupe, les envois, les médias, les réactions, les outils, la reconnexion et la récupération de reconnexion.
- Documenter les limites de sécurité du compte, les variables d'environnement de profil, la sélection de profil multi-compte et les étapes de récupération dans un runbook d'opérateur.
- Fermer ou documenter les problèmes récents de compte de démarrage, de médias de document, de métadonnées de citation, d'étiquette d'expéditeur et de rendu.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/zalouser.md` documente Zalo Personal via `zca-js`, avertit du risque d'automatisation non officielle et de suspension/bannissement de compte, explique l'ID de canal `zalouser`, le runtime local de passerelle, les options d'installation, la configuration du canal, les commandes CLI et les actions des outils.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference/zalouser.md` identifie le package `@openclaw/zalouser`, la route d'installation `npm; ClawHub` et la surface `channels: zalouser; contracts: tools`.

### Source

- `/Users/kevinlin/code/openclaw/extensions/zalouser/src/channel.ts`, `channel.runtime.ts`, `channel.setup.ts`, `runtime.ts`, `monitor.ts`, `zca-client.ts`, `zalo-js.ts`, `zca-constants.ts` et `zca-js-exports.d.ts` implémentent le runtime du canal et l'intégration ZCA.
- `/Users/kevinlin/code/openclaw/extensions/zalouser/src/accounts.ts`, `accounts.runtime.ts`, `qr-temp-file.ts`, `setup-core.ts`, `setup-surface.ts`, `config-schema.ts`, `status-issues.ts`, `doctor.ts` et `doctor-contract.ts` implémentent les comptes, la configuration du profil/session, les fichiers QR, la configuration, le statut et les vérifications du médecin.
- `/Users/kevinlin/code/openclaw/extensions/zalouser/src/group-policy.ts`, `session-route.ts`, `send.ts`, `send-receipt.ts`, `reaction.ts`, `directory.ts`, `tool.ts`, `text-styles.ts` et `message-sid.ts` implémentent le routage, la politique de groupe, les envois, les réactions, le répertoire, les outils, le rendu et l'identité du message.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/zalouser/src/channel.setup.test.ts`, `channel.sendpayload.test.ts`, `channel.directory.test.ts`, `monitor.account-scope.test.ts`, `monitor.group-gating.test.ts`, `tool.test.ts`, `reaction.test.ts`, `doctor.test.ts` et `probe.test.ts` exercent le comportement du flux du plugin.
- Aucun scénario de compte personnel Zalo en direct actuel n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/zalouser/src/accounts.test.ts`, `zalo-js.credentials.test.ts`, `zca-client.test.ts`, `group-policy.test.ts`, `send.test.ts`, `message-sid.test.ts`, `text-styles.test.ts`, `status-issues.test.ts`, `security-audit.test.ts` et les aides de test de configuration couvrent le compte ciblé, les identifiants, le client, la politique, l'envoi, l'identité, le texte, le statut et le comportement de sécurité.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "zalouser QR login zca-js group auth dangerous name matching" --json --limit 6`
- `gitcrawl search openclaw/openclaw --query "zalouser" --json --limit 8`

Résultats :

- La requête spécifique à la fonctionnalité n'a retourné aucun résultat.
- La large requête zalouser a retourné des résultats ouverts incluant `#82543` blocage du compte de démarrage après reconnexion, `#84924` pièces jointes photo entrantes, `#84770` livraison en double de médias de document, `#85039` normalisation du rendu markdown, `#87237` et `#86854` transfert de métadonnées de citation, `#86851` problème de métadonnées de citation et `#86561` action de lien d'invitation de groupe.

### Requêtes Discrawl

Requête :

- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 6 "zalouser QR login zca-js group auth"`
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "zalouser"`
- `/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 8 "Zalo Personal"`

Résultats :

- La requête spécifique à la fonctionnalité n'a retourné aucun résultat.
- La requête `zalouser` a retourné des notes de timing d'installation, un contexte de révision de nettoyage de délai d'attente, des corrections de routage de politique de mention et la PR `#69643` documentant les variables d'environnement de profil Zalo.
- La requête `Zalo Personal` a retourné des commentaires de révision sur l'analyse du préfixe de canal cassant les étiquettes d'expéditeur Zalo Personal, la documentation des variables d'environnement de profil et la sortie de configuration utilisateur listant Zalo Personal comme canal sélectionnable.
