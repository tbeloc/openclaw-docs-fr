---
title: "Application compagne Linux - Note de maturité des notifications Tray, Status et natives"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne Linux - Note de maturité des notifications Tray, Status et natives

## Résumé

Les affordances Tray, status et notification sont centrales dans l'application compagne macOS et sont visibles dans les PR ouvertes de l'application Linux, mais aucune n'est intégrée dans la source Linux actuelle. Le chemin Linux actuellement supporté expose le statut Gateway via des flux CLI/navigateur plutôt qu'une surface de statut Linux native ou de notification.

## Portée de la catégorie

- Élément tray/status Linux.
- Ligne de statut runtime et notifications natives.
- Intégration de l'environnement de bureau pour le comportement tray GNOME/KDE/Wayland/X11.
- Surfaces adjacentes hors portée : statut de l'interface utilisateur de contrôle du navigateur, CLI `openclaw status`, statut de la barre de menu macOS.

## Fonctionnalités

- Élément tray/status Linux : comportement, statut et vérification visible par l'opérateur de l'élément tray/status Linux.
- Ligne de statut runtime : ligne de statut runtime et notifications natives
- Intégration de l'environnement de bureau : intégration de l'environnement de bureau pour le comportement tray GNOME/KDE/Wayland/X11

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Experimental (5%)`
- Signaux positifs : la PR ouverte #59859 rapporte une vérification manuelle tray/status sur Ubuntu GNOME, et la documentation actuelle montre le comportement attendu de la barre de menu macOS.
- Signaux négatifs : la source enregistrée ne contient aucun helper tray Linux, code d'élément de statut, code de notification, fichier de bureau ou runtime d'application Linux.
- Lacunes d'intégration : aucun chemin tray ou notification Linux supporté ne peut être exercé à partir du checkout source actuel.

## Score de qualité

- Score : `Experimental (25%)`
- Rapports Gitcrawl : `Linux tray notifications companion` a retourné la PR #59859, dont le corps indique que l'intégration tray/status Ubuntu GNOME existe dans cette PR ouverte.
- Rapports Discrawl : la même requête a retourné une discussion sur le compagnon Windows mais aucune preuve de version Linux supportée ; les commentaires du problème #75 mentionnent le travail shell/status Linux dans les branches des contributeurs.
- Bonnes qualités : les PR ouvertes identifient le risque tray Linux et isolent les limites des helpers AppIndicator/GTK.
- Mauvaises qualités : la documentation actuelle n'explique pas les limitations tray Linux, les environnements de bureau supportés, les permissions de notification ou le comportement de secours car il n'y a pas encore d'application supportée.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, live et de flux runtime réel sont exclues de ce score de qualité.

## Score de complétude

- Score : `Experimental (5%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-companion-app.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'élément tray/status Linux, la ligne de statut runtime, l'intégration de l'environnement de bureau.
- Signaux négatifs : la note archivée a précédé le scoring de complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Intégrer ou rejeter une architecture tray spécifique pour le comportement GNOME/KDE/StatusNotifier/AppIndicator.
- Définir le comportement des permissions de notification et les modes d'échec sur le bureau Linux.
- Ajouter la documentation pour les états des icônes de statut, le routage des notifications et le secours lorsqu'un hôte tray n'est pas disponible.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md:15` : l'application compagne macOS affiche les notifications natives et le statut dans la barre de menu.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/menu-bar.md` : macOS a une page de statut dédiée à la barre de menu ; aucune page équivalente Linux n'existe.
- `/Users/kevinlin/code/openclaw/docs/platforms/linux.md:13` : les applications compagnes Linux sont prévues.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/MenuContentView.swift` : macOS a une source de contenu de menu enregistrée ; aucune source menu/tray `apps/linux` n'existe dans le checkout actuel.
- `find apps -maxdepth 2 -type d` n'a retourné aucun répertoire d'application compagne Linux.
- `rg --files apps | rg -i "(tray|status|notification|appindicator|gtk|libadwaita|linux)"` n'a trouvé aucune source d'application Linux actuelle.

### Tests d'intégration

- Aucun test d'intégration tray/status/notification Linux enregistré n'a été trouvé.
- Les tests de fumée Linux adjacents sont des tests d'installation CLI uniquement, pas des tests d'interface utilisateur de statut de bureau.

### Tests unitaires

- Aucune cible de test unitaire tray/status/notification Linux n'a été trouvée.
- Le comportement menu/status macOS a une couverture de test et de source spécifique à l'application en dehors de cette surface Linux.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "Linux tray notifications companion" --mode keyword --limit 8 --json`
- `gitcrawl gh pr view 59859 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`
- `gitcrawl gh pr view 61576 --repo openclaw/openclaw --json number,title,state,author,updatedAt,body,headRefName,baseRefName,url`

Résultats :

- La requête de fonctionnalité a retourné la PR ouverte #59859 avec des extraits sur l'exercice des surfaces tray/status, diagnostics, onboarding/readiness et dashboard.
- La PR #59859 indique qu'elle ajoute un helper tray GTK3 Ayatana/AppIndicator privé pour l'intégration tray/status Ubuntu GNOME.
- La PR #61576 énumère « Pas de barre d'état système sur les WM en mosaïque (StatusNotifierWatcher absent) » comme une lacune connue.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux tray notifications companion"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "Linux Windows Clawdbot Apps issue 75"`

Résultats :

- La requête tray/notifications a retourné des commentaires sur le compagnon natif Windows et aucune preuve de version compagne Linux supportée.
- La requête du problème #75 a retourné des commentaires sur le jalon de l'application Linux concernant la parité shell et le travail de statut, mais ces commentaires pointent vers l'activité des problèmes/PR des contributeurs plutôt que vers la source actuelle enregistrée.
