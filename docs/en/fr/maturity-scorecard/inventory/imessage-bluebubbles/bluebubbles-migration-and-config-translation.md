---
title: "iMessage / BlueBubbles - Note de maturité de la migration et de la traduction de configuration BlueBubbles"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# iMessage / BlueBubbles - Note de maturité de la migration et de la traduction de configuration BlueBubbles

## Résumé

La migration BlueBubbles et la traduction de configuration sont en Alpha pour la couverture et en Beta pour la qualité. La documentation indique explicitement que le support BlueBubbles a été supprimé et que les anciens opérateurs doivent migrer vers `channels.imessage`. Le guide de migration couvre les principales traductions de clés et les pièges de basculement. Le score de couverture inférieur reflète qu'il s'agit principalement de documentation/preuves de source : aucune ancienne voie de migration BlueBubbles vers imsg n'a été trouvée.

## Portée de la catégorie

Cette note couvre l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions, et la liste de contrôle de basculement de l'opérateur.

## Fonctionnalités

- Traduire la configuration héritée : couvre la traduction de la configuration héritée dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions, et la liste de contrôle de basculement de l'opérateur.
- Basculer en toute sécurité : couvre le basculement sécurisé dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions, et la liste de contrôle de basculement de l'opérateur.
- Gérer les avertissements de migration : couvre la gestion des avertissements de migration dans l'annonce de suppression, le guide de migration, la référence de configuration, la traduction de l'ancienne clé `channels.bluebubbles`, le piège du registre de groupe, les avertissements de session, les notes de parité des pièces jointes/actions, et la liste de contrôle de basculement de l'opérateur.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (62%)`
- Signaux positifs :
  - Il y a une annonce de suppression dédiée et un guide de migration complet.
  - La documentation de configuration indique clairement que `channels.bluebubbles` n'est plus supporté.
  - Le guide couvre la suppression de clés de transport, la copie de clés de comportement, les avertissements du registre de groupe, la vérification des actions d'API privée, et les avertissements de session.
  - Les tests de migration de configuration héritée couvrent une route adjacente d'anciens paramètres de chat de groupe vers `channels.imessage.groups`.
- Signaux négatifs :
  - Aucun démarrage de test de fumée de migration automatisée ne commence avec l'ancienne configuration `channels.bluebubbles` et ne vérifie un runtime `channels.imessage` fonctionnel.
  - Aucune preuve de démantèlement/basculement du serveur BlueBubbles en direct n'a été trouvée.
  - Les preuves d'archive montrent que les anciennes orientations utilisateur pointaient les gens vers BlueBubbles, ce qui crée une charge de dérive de documentation pour la migration.
- Lacunes d'intégration :
  - Ajouter une fixture qui traduit les configurations `channels.bluebubbles` représentatives en `channels.imessage`, y compris les caractères génériques de groupe, les pièces jointes, les limites de médias, les actions, et les avertissements de session.
  - Ajouter un linter docs/config qui empêche la documentation actuelle de créer des liens vers une page de runtime BlueBubbles supportée.

## Score de qualité

- Score : `Beta (72%)`
- Rapports de Gitcrawl :
  - `BlueBubbles removed imessage` a retourné #83160, notant que BlueBubbles a été intentionnellement exclu car il a été supprimé en amont dans `07bf572` le 2026-05-07.
  - `iMessage BlueBubbles migration channels.bluebubbles channels.imessage` a retourné des résultats adjacents de configuration/sécurité tels que #73822, #87023, #62387, et #64322.
- Rapports de Discrawl :
  - `BlueBubbles removed imessage` a retourné des extraits d'archive Discord/GitHub plus anciens sur le comportement de BlueBubbles et les orientations utilisateur, y compris une réponse d'assistance de 2026-03 qui décrivait toujours BlueBubbles comme le chemin futur à ce moment-là.
  - `iMessage BlueBubbles migration channels.bluebubbles channels.imessage` n'a retourné aucun extrait lors du dernier passage.
- Bonnes qualités :
  - La documentation ne laisse pas l'opérateur deviner : il n'y a pas de serveur BlueBubbles, de mot de passe, de webhook, ou de runtime dans le chemin supporté.
  - Le tableau de traduction appelle les clés de comportement qui se reportent et les clés de transport qui doivent être supprimées.
  - Le guide appelle les pièges à haut risque : `includeAttachments` est désactivé par défaut, les entrées du registre de groupe sont porteuses de charge, les anciennes clés de session ne se reportent pas, et les deux canaux ne doivent pas s'exécuter involontairement pendant le basculement.
- Mauvaises qualités :
  - La migration repose sur la discipline de copie/édition de l'opérateur plutôt que sur une commande de migration guidée.
  - Les anciennes orientations d'archive et la documentation précédente peuvent entrer en conflit avec le nouvel état de suppression.
  - La continuité de session n'est pas préservée pour les anciennes clés de session BlueBubbles.
- Exclu de la qualité :
  - Les preuves de test unitaire, d'intégration, e2e, en direct, et de flux de runtime sont enregistrées sous Couverture uniquement.

## Score de complétude

- Score : `Alpha (62%)`
- Instructions de surface : évaluées par rapport à `references/completeness/imessage-bluebubbles.md`.
- Signaux positifs : les preuves de docs archivées, de source, de test, de Gitcrawl, et de Discrawl couvrent la portée de la taxonomie pour Traduire la configuration héritée, Basculer en toute sécurité, Gérer les avertissements de migration.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune commande de migration ou preuve de traduction automatisée n'a été trouvée.
- Les anciennes sessions BlueBubbles restent un avertissement manuel.
- Les anciennes docs/réponses d'assistance peuvent induire les utilisateurs en erreur à moins que la documentation actuelle ne soit suivie.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/announcements/bluebubbles-imessage.md:12` : OpenClaw n'expédie plus BlueBubbles ; iMessage s'exécute maintenant via `imessage` et `imsg` fournis.
- `/Users/kevinlin/code/openclaw/docs/announcements/bluebubbles-imessage.md:14` : les configurations `channels.bluebubbles` doivent migrer vers `channels.imessage`.
- `/Users/kevinlin/code/openclaw/docs/announcements/bluebubbles-imessage.md:18` : aucun serveur HTTP BlueBubbles, route webhook, mot de passe REST, ou runtime de plugin ne reste dans le chemin supporté.
- `/Users/kevinlin/code/openclaw/docs/announcements/bluebubbles-imessage.md:69` : les anciennes clés de comportement ont des équivalents iMessage.
- `/Users/kevinlin/code/openclaw/docs/announcements/bluebubbles-imessage.md:73` : les anciennes clés de session BlueBubbles ne deviennent pas des clés de session iMessage.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:10` : iMessage fourni atteint la même surface d'API privée via `imsg`.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:20` : la liste de contrôle de migration vérifie `imsg`, copie les clés de comportement, supprime les clés de transport, sonde, teste les DM/groupes/pièces jointes/actions, puis supprime BlueBubbles.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:95` : le tableau de traduction de configuration commence.
- `/Users/kevinlin/code/openclaw/docs/channels/imessage-from-bluebubbles.md:109` : les entrées de caractères génériques de groupe doivent être copiées car elles font partie de la porte du registre.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:596` : `channels.bluebubbles` n'est pas une surface de configuration de runtime supportée.

### Source

- `/Users/kevinlin/code/openclaw/extensions/imessage/openclaw.plugin.json:6` : le plugin fourni déclare l'id de canal `imessage`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:52` : l'adaptateur de configuration du plugin pointe la politique de groupe vers `channels.imessage.groupPolicy`.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/shared.ts:53` : l'adaptateur de configuration du plugin pointe la liste d'autorisation de groupe vers `channels.imessage.groupAllowFrom`.
- `/Users/kevinlin/code/openclaw/src/config/types.imessage.ts:77` : la configuration iMessage possède le comportement include-attachments.
- `/Users/kevinlin/code/openclaw/src/config/types.imessage.ts:83` : la configuration iMessage possède les limites de taille de médias.
- `/Users/kevinlin/code/openclaw/src/config/types.imessage.ts:122` : la configuration iMessage possède la forme de politique de caractères génériques de groupe.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/legacy-config-migrate.test.ts:896` : les anciens paramètres de mention de chat de groupe sont déplacés vers `channels.imessage.groups`.
- `/Users/kevinlin/code/openclaw/src/commands/doctor/shared/legacy-config-migrate.test.ts:907` : le message de migration nomme le chemin de destination `channels.imessage.groups."*".requireMention`.
- Aucune ancienne voie de basculement BlueBubbles-vers-iMessage en direct n'a été trouvée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/imessage/src/config-schema.test.ts:119` : accepte `remoteHost` sûr lors de la validation de nouvelle configuration.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/config-schema.test.ts:138` : accepte les modèles de racine de pièce jointe que la documentation de migration dit aux utilisateurs de copier.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor.gating.test.ts:433` : bloque les messages de groupe lorsque `imessage.groups` est défini sans caractère générique.
- `/Users/kevinlin/code/openclaw/extensions/imessage/src/monitor/group-allowlist-warnings.test.ts:13` : l'avertissement se déclenche lorsque `groupPolicy=allowlist` et `groups` est indéfini.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "BlueBubbles removed imessage" --json --limit 6`

Résultats :

- L'extrait de la PR ouverte #83160 dit que BlueBubbles a été intentionnellement exclu car il a été supprimé en amont dans `07bf572` le 2026-05-07.

Requête :

`gitcrawl search openclaw/openclaw --query "iMessage BlueBubbles migration channels.bluebubbles channels.imessage" --json --limit 6`

Résultats :

- Les résultats adjacents incluaient #73822, #87023, #62387, #39065, #83160, et #64322, reflétant le travail de configuration/sécurité/session qui mentionne iMessage ou BlueBubbles mais pas une preuve de migration directe.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search "BlueBubbles removed imessage" --limit 6`

Résultats :

- Les extraits d'archive incluaient les anciens commentaires de PR BlueBubbles et une réponse d'assistance de 2026-03 qui recommandait toujours BlueBubbles comme le chemin futur, ce qui est maintenant obsolète par rapport à la documentation de suppression actuelle.

Requête :

`/Users/kevinlin/.local/bin/discrawl search "iMessage BlueBubbles migration channels.bluebubbles channels.imessage" --limit 6`

Résultats :

- Aucun extrait retourné lors du dernier passage.
