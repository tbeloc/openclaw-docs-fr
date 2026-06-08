---
title: "Voix et conversation en temps réel - Note de maturité des contrôles Agent Consult, Steering et Talkback"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Voix et conversation en temps réel - Note de maturité des contrôles Agent Consult, Steering et Talkback

## Résumé

La surface de consultation/contrôle de l'agent est un différenciateur clé de Talk : les fournisseurs en temps réel appellent `openclaw_agent_consult`, et les utilisateurs/opérateurs peuvent diriger ou annuler l'exécution de l'agent intégré. La couverture est au niveau bêta. La qualité est au niveau bêta mais reste exposée aux problèmes de latence signalés dans les archives, de politique d'outils et de divergence de sortie vocale.

## Portée de la catégorie

- Gestion des appels d'outils `openclaw_agent_consult`.
- Statut actif de l'exécution de l'agent Talk, contrôles d'annulation, de direction et de suivi.
- Comportement du runtime Talkback et coordination de la parole de l'assistant.
- Planification forcée de la consultation et propagation des événements de contrôle.

## Fonctionnalités

- Transfert de consultation d'agent : Comportement de transfert de consultation entre les sessions Talk actives et les exécutions d'agent.
- Statut actif de l'exécution de l'agent Talk : Statut actif de l'exécution de l'agent Talk, contrôles d'annulation, de direction et de suivi
- Comportement du runtime Talkback : Comportement du runtime Talkback et coordination de la parole de l'assistant
- Planification forcée de la consultation : Planification forcée de la consultation et propagation des événements de contrôle

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`

Le composant dispose de documentation pour la consultation et la direction, du code source Gateway, des adaptateurs UI, des types du SDK de plugin, des hooks du runtime de relais et des tests dans les modules de consultation/contrôle. La couverture n'est pas stable car le comportement réel s'étend sur les appels LLM, la sortie vocale et le timing du pont du fournisseur.

## Score de qualité

- Score : `Bêta (72%)`

La qualité bénéficie d'une résolution explicite des exécutions actives, de l'annulation, de la direction, de la mise en file d'attente des suivis, de l'idempotence, de l'activité de diagnostic et des hooks de contrôle côté fournisseur. Le risque de qualité persiste là où la consultation en temps réel est lente, où les outils sont annoncés mais indisponibles, et où la sortie vocale peut diverger de la livraison de l'interface utilisateur de contrôle.

Exclus de la qualité : Présence ou absence de tests unitaires, d'intégration, e2e, en direct et de flux runtime réel.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/voice-and-realtime-talk.md`.
- Signaux positifs : les archives de documentation, le code source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour le transfert de consultation d'agent, le statut actif de l'exécution de l'agent Talk, le comportement du runtime Talkback, la planification forcée de la consultation.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La latence et la fragilité de la consultation en temps réel ont été signalées dans les preuves d'archive.
- Les incompatibilités de politique d'outils peuvent confondre les instructions du fournisseur.
- Le comportement du miroir de livraison peut faire que Talk prononce une réponse différente de celle affichée par l'interface utilisateur de contrôle.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:23` décrit la consultation en temps réel du navigateur via `talk.client.toolCall`.
- `/Users/kevinlin/code/openclaw/docs/nodes/talk.md:24` documente `talk.client.steer` et `talk.session.steer`.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:101` documente la consultation et la direction dans le chemin Talk du navigateur.

### Code source

- `/Users/kevinlin/code/openclaw/src/gateway/server-methods/talk-client.ts:160` implémente `talk.client.toolCall` et valide `openclaw_agent_consult`.
- `/Users/kevinlin/code/openclaw/src/gateway/talk-agent-consult.ts:14` construit et envoie des demandes de chat de consultation avec des options de runtime spécifiques à Talk.
- `/Users/kevinlin/code/openclaw/src/talk/agent-run-control.ts:58` contrôle les exécutions d'agent Talk intégrées actives pour le statut, l'annulation, la direction et le suivi.
- `/Users/kevinlin/code/openclaw/src/talk/agent-consult-runtime.ts:193` démarre les sessions de runtime de consultation et gère le contexte de livraison.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/realtime-voice.ts:1` exporte les types de fournisseur de voix en temps réel, les hooks de contrôle, les types de consultation et les hooks de diagnostic.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/talk-realtime-relay.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-consult.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-gateway-relay.test.ts`
- `/Users/kevinlin/code/openclaw/ui/src/ui/realtime-talk-webrtc.test.ts`

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/talk/agent-consult-runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/agent-consult-tool.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/agent-run-control.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/agent-talkback-runtime.test.ts`
- `/Users/kevinlin/code/openclaw/src/talk/forced-consult-coordinator.test.ts`

### Requêtes Gitcrawl

- `gitcrawl search issues "openclaw_agent_consult realtime voice" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #85275 pour incompatibilité de sortie vocale, #86425 pour support de cadre de caméra et #80840 pour outils en temps réel annoncés sans liaison de gestionnaire.
- `gitcrawl search issues "talk.session gateway relay" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10` a retourné #84664 et #84639, tous deux pertinents pour un contexte en temps réel plus riche et l'injection de parole.

### Requêtes Discrawl

- `/Users/kevinlin/.local/bin/discrawl search "openclaw_agent_consult realtime" --limit 5` a retourné la preuve d'archive #71849 que la consultation vocale en temps réel peut être trop lente ou fragile pour les appels en direct.
- `/Users/kevinlin/.local/bin/discrawl search "gateway relay talk" --limit 5` a retourné la preuve #71262 corrigée sur main pour exposer les outils d'agent Gateway via l'outil de consultation en temps réel partagé et un commentaire d'examen de PR #71272 sur les instructions `toolPolicy: none`.
