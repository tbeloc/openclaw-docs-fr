---
title: "Application compagne Linux - Note de maturité Chat et Sessions"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Linux - Note de maturité Chat et Sessions

## Résumé

OpenClaw dispose de contrats WebChat matures pour navigateur et macOS/iOS, et les PR d'application Linux ouvertes revendiquent des fenêtres de chat natives et des contrôles de session/modèle. La surface d'application compagne Linux prise en charge n'est toujours pas intégrée, donc les utilisateurs sur Linux doivent utiliser l'interface utilisateur de contrôle du navigateur ou les canaux pour le chat pris en charge.

## Portée de la catégorie

Inclus dans cette catégorie :

- Fenêtre de chat Linux native : comportement de la fenêtre de chat Linux native, statut et vérification visible par l'opérateur.
- Transcription : transcription, compositeur, sélecteur de session, sélecteur de modèle, contrôles d'envoi/abandon/suivi
- Transport de chat de passerelle : transport de chat WebSocket de passerelle à partir d'un client de bureau Linux.

## Fonctionnalités

- Fenêtre de chat Linux native : comportement de la fenêtre de chat Linux native, statut et vérification visible par l'opérateur.
- Transcription : transcription, compositeur, sélecteur de session, sélecteur de modèle, contrôles d'envoi/abandon/suivi
- Transport de chat de passerelle : transport de chat WebSocket de passerelle à partir d'un client de bureau Linux.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (10%)`
- Signaux positifs : les contrats de chat de passerelle et la documentation WebChat pour navigateur/macOS/iOS constituent une preuve adjacente solide ; les PR Linux ouvertes revendiquent des implémentations de client de chat.
- Signaux négatifs : aucun client de chat Linux natif enregistré ou test d'application Linux pris en charge n'existe.
- Lacunes d'intégration : aucune preuve de chat e2e Linux natif pris en charge, reconnexion WebSocket, transcription, session, modèle ou compositeur n'a été trouvée.

## Score de qualité

- Score : `Expérimental (36%)`
- Rapports Gitcrawl : la requête spécifique au chat Linux a révélé une PR de suivi large et des PR d'application Linux ouvertes avec une fonctionnalité de chat revendiquée.
- Rapports Discrawl : les commentaires du problème #75 signalent une étape importante du chat de l'application Linux avec fenêtre de chat native, transcription, compositeur, sélection de session, sélection de modèle et diagnostics.
- Bonnes qualités : les modèles sous-jacents de passerelle `chat.history`, `chat.send` et d'interface utilisateur de contrôle fournissent un contrat cohérent pour un futur client Linux.
- Mauvaises qualités : aucune expérience utilisateur Linux prise en charge n'existe pour l'état du chat, la persistance locale, la reconnexion, l'accessibilité, le rendu markdown/outils ou la sélection de session ; la preuve d'archive est une preuve de branche contributeur plutôt qu'une preuve expédiée.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Expérimental (10%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la fenêtre de chat Linux native, la transcription et le transport de chat de passerelle.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Intégrer ou reporter explicitement le chat Linux natif.
- Définir la parité avec l'interface utilisateur de contrôle du navigateur et WebChat macOS/iOS.
- Documenter l'authentification du chat Linux, la persistance de session, la reconnexion, la relecture de transcription et les paramètres locaux.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/web/webchat.md:8` : l'interface utilisateur de chat SwiftUI macOS/iOS communique directement avec la passerelle WebSocket.
- `/Users/kevinlin/code/openclaw/docs/web/webchat.md:12` : WebChat est une interface utilisateur de chat native pour la passerelle sur les clients natifs pris en charge.
- `/Users/kevinlin/code/openclaw/docs/web/webchat.md:25` : WebChat utilise `chat.history`, `chat.send` et `chat.inject`.
- `/Users/kevinlin/code/openclaw/docs/web/control-ui.md:98` : l'interface utilisateur de contrôle du navigateur fournit le chat et Talk aujourd'hui.
- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:13` : les applications compagnes Linux sont prévues, donc le chat natif Linux n'est actuellement pas promis comme pris en charge.

### Source

- Aucune source de client de chat natif `apps/linux` ou `apps/linux-gtk` enregistrée n'existe.
- `/Users/kevinlin/code/openclaw/apps/shared/OpenClawKit/Sources/OpenClawChatUI` : une interface utilisateur de chat native partagée existe pour les clients Apple/mobiles actuels, mais n'est pas une implémentation d'application Linux.
- La source de l'interface utilisateur de contrôle du navigateur existe sous la surface web de la passerelle, pas comme une application Linux native.

### Tests d'intégration

- Aucun test d'intégration de chat d'application Linux native n'a été trouvé.
- Les tests de chat existants spécifiques à l'application et au navigateur/passerelle sont adjacents, pas une preuve d'application Linux native.

### Tests unitaires

- Aucun test unitaire de chat Linux natif n'a été trouvé.
- Les tests de chat OpenClawKit partagés existants couvrent le comportement d'interface utilisateur Swift partagé pour les clients d'application actuels, pas Linux.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Linux companion chat window session model diagnostics" --mode keyword --limit 8 --json`
- `gitcrawl gh pr view 59859 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`
- `gitcrawl gh pr view 61576 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`

Résultats :

- La requête de chat Linux a retourné la PR de suivi large #74163, incluant une référence aux téléchargements de compagnon officiels.
- La PR #59859 revendique des surfaces de gestion natives et un tableau de bord/général/diagnostics, mais elle reste ouverte.
- La PR #61576 revendique une vue de chat GTK4 avec envoi/réception en direct, rendu Markdown, sélecteur de modèle de session, indicateur de saisie, basculements de réflexion/appel d'outil et `chat.history`, mais elle reste ouverte et précoce.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux companion chat window session model diagnostics"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux companion app native Linux app"`

Résultats :

- La requête de chat/session a retourné un commentaire du problème #75 du 19 avril indiquant que l'application Linux prend en charge le chat en tant que surface de produit réelle dans une piste contributeur, avec fenêtre de chat native, transcription, compositeur, sélection de session, sélection de modèle, comportement singleton et diagnostics.
- La requête d'application Linux native a également retourné des conseils de support indiquant que les utilisateurs Linux doivent utiliser l'interface utilisateur OpenClaw/web ou d'autres ponts car aucune application compagne Linux native prise en charge n'existe encore.
