---
title: "WhatsApp - Inbound DM Access and Privacy Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Inbound DM Access and Privacy Maturity Note

## Résumé

L'accès aux messages directs entrants WhatsApp et la confidentialité sont en version Bêta. La politique DM,
l'appairage, la liste d'autorisation, l'identité de l'expéditeur, la confirmation de lecture, l'auto-chat, la réception durable,
l'enveloppe entrante, le contexte cité et le comportement du hook de plugin sont documentés et
implémentés avec des paramètres par défaut de fermeture en cas d'échec. Cela reste en dessous de Stable car la preuve en direct actuelle ne valide pas profondément les limites de confirmation de lecture, d'historique et de confidentialité,
et l'historique des archives montre une agitation récente de l'auto-chat/confirmation de lecture.

## Portée de la catégorie

- `dmPolicy` de message direct, `allowFrom`, défi d'appairage, admission du
  magasin d'appairage et accès à l'expéditeur conscient du compte.
- Extraction d'identité de l'expéditeur, confirmations de lecture, protections d'auto-chat, contexte de contact et
  contexte cité, réception durable et construction d'enveloppe entrante.
- Contrôles de confidentialité pour les hooks de plugin et le contexte non approuvé.
- Hors de portée : routage de groupe, notation de charge utile multimédia, envois sortants et
  approbations natives.

## Fonctionnalités

- Politique dmPolicy de message direct : Politique dmPolicy de message direct, `allowFrom`, défi d'appairage, appairage
- Extraction d'identité de l'expéditeur : Extraction d'identité de l'expéditeur, confirmations de lecture, protections d'auto-chat et correspondance de contact.
- Contrôles de confidentialité pour les hooks de plugin : Contrôles de confidentialité pour les hooks de plugin et le contexte non approuvé

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`
- Signaux positifs : la documentation explique les modes d'accès DM, l'approbation d'appairage, les enveloppes entrantes, les confirmations de lecture, les protections d'auto-chat et l'opt-in de confidentialité ; les tests de flux d'exécution et de surveillance couvrent les décisions d'autorisation/refus, l'extraction de messages,
  la distribution et la gestion des auto-messages.
- Signaux négatifs : l'assurance qualité en direct standard couvre le canari DM, le bloc d'appairage et la limitation des mentions de groupe, mais ne valide pas profondément les limites de confirmation de lecture, la confidentialité des hooks de plugin ou la suppression d'historique.
- Lacunes d'intégration : aucune matrice en direct localisée ne prouve désactivé, refus de liste d'autorisation,
  défi d'appairage, approbation d'appairage, choix de confirmation de lecture, ignorance d'auto-chat, relecture de réception durable et suppression d'historique dans une exécution WhatsApp.

## Score de qualité

- Score : `Bêta (76%)`
- Rapports Gitcrawl : `whatsapp dm allowFrom pairing inbound privacy` a surfacé
  le problème ouvert #68214 pour un événement de hook non autorisé et un drapeau de configuration de suppression de réponse d'appairage ; `whatsapp read receipt` a surfacé #79996 autour des limites d'activité WhatsApp sortante pour un hook proposé.
- Rapports Discrawl : `whatsapp read receipt` a retourné des preuves d'examen/support
  pour la suppression de confirmation de lecture d'auto-chat, l'opt-out de confirmation de lecture du groupe de surveillance,
  les conseils d'assistance pour désactiver les confirmations de lecture et les preuves de note de version que
  WhatsApp respecte les limites de confirmation de lecture.
- Bonnes qualités : les politiques de message direct sont explicites, l'état d'appairage est partagé
  et limité au compte, les expéditeurs inconnus ne sont pas admis silencieusement, les confirmations de lecture
  sont retardées jusqu'à la fin du traitement, les boucles d'auto-chat sont protégées, la réception durable déduplique/rejoue les ID de message stables et la confidentialité des hooks de plugin est opt-in.
- Mauvaises qualités : la personnalisation des messages rejetés n'est pas encore de première classe, les réponses d'appairage peuvent toujours être bruyantes pour certains opérateurs, la journalisation entrante inclut des détails sensibles à la confidentialité du corps/chemin multimédia, et l'examen des archives montre que les limites d'auto-chat et de confirmation de lecture ont toujours besoin d'attention.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel
  n'a pas augmenté ou diminué ce score de qualité.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Politique dmPolicy de message direct, Extraction d'identité de l'expéditeur, Contrôles de confidentialité pour les hooks de plugin.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter des régressions de message direct en direct pour tous les modes de refus et d'admission.
- Ajouter des assertions en direct récurrentes pour pas de lecture d'expéditeur bloqué, pas de lecture d'auto-chat,
  confirmations de lecture désactivées, suppression d'historique et confidentialité des hooks de plugin.
- Décider si #68214 devrait devenir un chemin de hook/config pris en charge.
- Améliorer les diagnostics visibles par l'opérateur lorsqu'un expéditeur est bloqué par la
  politique de message direct plutôt que par une défaillance d'exécution.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:178` documente les invites d'appairage, l'indépendance d'approbation exec/plugin, les approbateurs `allowFrom` et le chemin d'authentification `/approve` manuel.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:210` documente les hooks de plugin et l'opt-in de confidentialité.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:250` documente la politique DM, l'appairage, les listes d'autorisation et l'accès aux messages directs.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:322` documente les protections d'auto-chat.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:330` documente l'enveloppe entrante, le contexte cité, les espaces réservés multimédia et les confirmations de lecture.
- `/Users/kevinlin/code/openclaw/src/config/types.whatsapp.ts:53` tape `dmPolicy`, `allowFrom`, `groupAllowFrom`, limites d'historique, `selfChatMode` et `sendReadReceipts`.
- `/Users/kevinlin/code/openclaw/docs/channels/pairing.md:10` documente l'appairage comme approbation d'accès explicite pour les expéditeurs DM inconnus.

### Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/access-control.ts:24` implémente le contrôle d'accès DM/groupe, le défi d'appairage, la politique de groupe et la prise de décision de confirmation de lecture.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/monitor.ts:543` normalise les messages entrants Baileys et supprime les événements non-utilisateur/statut/écho avant le routage.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/monitor.ts:660` gère les confirmations de lecture, y compris la suppression d'auto-chat.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/monitor.ts:716` persiste, déduplique et rejoue les messages entrants durables.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/extract.ts:209` extrait les JID mentionnés et le contexte de l'expéditeur.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/extract.ts:233` extrait le texte, les légendes et le contexte de contact.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound-policy.ts:136` mappe les identités d'expéditeur WhatsApp dans la politique d'entrée de canal stable partagée avec la sensibilité d'identité téléphonique.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/process-message.ts:75` limite les hooks de plugin derrière un opt-in explicite.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/process-message.ts:405` construit le contexte de réponse visible et le contexte d'invite direct/groupe.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:204` définit les scénarios en direct de canari WhatsApp, bloc d'appairage et limitation de mention.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:928` exécute les scénarios de message direct et de groupe par rapport aux messages du pilote en direct.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/monitor-inbox.allows-messages-from-senders-allowfrom-list.test-support.ts:101` couvre les DM autorisés et du même téléphone.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/monitor-inbox.blocks-messages-from-unauthorized-senders-not-allowfrom.test-support.ts:96` couvre le blocage d'expéditeur non autorisé, aucun appel de gestionnaire et aucune confirmation de lecture.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/monitor-inbox.streams-inbound-messages.test-support.ts:170` couvre la diffusion en continu des messages entrants, les confirmations de lecture retardées, la réserve durable, la reconnexion et le comportement du cache de métadonnées.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound-context.contract.test.ts:1` couvre le comportement du contrat de contexte entrant.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/access-control.test.ts:85` couvre la grâce d'appairage, `dmPolicy` au niveau du compte et le comportement d'appairage persistant.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/access-control.test.ts:356` couvre la portée d'auto-chat.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/inbound-context.test.ts:42` couvre le filtrage d'historique de groupe et la suppression de citation.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply/monitor/inbound-dispatch.test.ts:315` couvre la construction de contexte entrant finalisée.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/extract.test.ts:1` couvre le comportement d'extraction entrant.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/inbound/send-result.test.ts:1` couvre la gestion des résultats d'envoi utilisée par les flux entrants.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/monitor-inbox.blocks-messages-from-unauthorized-senders-not-allowfrom.test-support.ts:1` prend en charge le comportement du moniteur d'expéditeur non autorisé.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/monitor-inbox.allows-messages-from-senders-allowfrom-list.test-support.ts:1` prend en charge le comportement du moniteur allowFrom.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp dm allowFrom pairing inbound privacy" --json`

Résultats :

- A surfacé #68214 demandant un événement de hook non autorisé et un drapeau de configuration de suppression de réponse d'appairage.

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp read receipt" --json`

Résultats :

- A surfacé #79996, notant qu'aucune activité WhatsApp sortante telle que réponse, réaction d'accusé de réception, confirmation de lecture ou saisie n'est déclenchée par un hook proposé.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp dm allowFrom pairing inbound privacy" --limit 5`

Résultats :

- A retourné `null` ; aucun résultat d'archive Discrawl pertinent pour ce composant exact dans l'instantané actuel.

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp read receipt" --limit 5`

Résultats :

- A retourné des preuves d'examen/support pour la suppression de confirmation de lecture d'auto-chat, l'opt-out de confirmation de lecture du groupe de surveillance, les conseils d'assistance pour désactiver les confirmations de lecture et les preuves de note de version que WhatsApp respecte les limites de confirmation de lecture.
