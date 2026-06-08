---
title: "Windows via WSL2 - Chaîne de démarrage Windows et note de maturité de la persistance de connexion"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Windows via WSL2 - Chaîne de démarrage Windows et note de maturité de la persistance de connexion

## Résumé

L'histoire de la chaîne de démarrage Windows est documentée mais peu implémentée par OpenClaw lui-même. Le runbook explique correctement qu'un service utilisateur systemd WSL2 persiste après le démarrage de WSL, tandis que le démarrage Windows avant la connexion nécessite `loginctl enable-linger` plus une tâche planifiée Windows qui démarre la distribution. Cela rend ce composant Alpha pour la couverture et la qualité : le chemin est viable, mais c'est plutôt une recette d'opérateur qu'un cycle de vie géré par le produit.

## Portée des catégories

- Linger du service utilisateur WSL.
- Disponibilité de systemd WSL après le démarrage de la distribution.
- Tâche planifiée Windows qui lance WSL.
- Vérification avant la connexion Windows.
- Attentes claires concernant l'alimentation du PC, la mise en veille, le démarrage de Windows, le démarrage de WSL et la disponibilité de la passerelle.
- Exclut le comportement natif de la tâche planifiée Windows Gateway.

## Fonctionnalités

- Linger du service utilisateur WSL : comportement, statut et vérification visible par l'opérateur du linger du service utilisateur WSL.
- Disponibilité de Systemd après le démarrage de Windows : disponibilité de Systemd après le démarrage de Windows et le démarrage de la distribution WSL.
- Tâche de démarrage Windows pour WSL : comportement de la tâche de démarrage Windows pour lancer WSL avant la connexion.
- Vérification avant la connexion Windows : comportement de vérification avant la connexion Windows, statut et vérification visible par l'opérateur.
- Attentes claires concernant l'alimentation du PC : attentes claires concernant l'alimentation du PC, la mise en veille, le démarrage de Windows, le démarrage de WSL et la disponibilité de la passerelle

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (64%)`
- Signaux positifs : la documentation de la plateforme Windows décrit chaque étape de la chaîne de démarrage et inclut des commandes concrètes pour linger, l'installation de Gateway, `schtasks` Windows, la recherche de noms de distribution et la vérification post-redémarrage.
- Signaux négatifs : la tâche planifiée de démarrage Windows est une recette PowerShell manuelle ; OpenClaw n'installe ni ne vérifie cette tâche côté Windows pour le chemin WSL2.
- Lacunes d'intégration : aucune e2e de démarrage avant connexion WSL2 ou preuve en direct n'a été trouvée ; les tests actuels couvrent le comportement de systemd Linux et les sondes de disponibilité WSL Windows, pas la persistance complète du démarrage Windows.

## Score de qualité

- Score : `Alpha (66%)`
- Rapports Gitcrawl : `WSL2 Windows boot loginctl linger schtasks` a retourné 0 résultats. La recherche plus large `Windows WSL2 gateway systemd` a retourné des problèmes actifs de cycle de vie de service mais pas un problème d'implémentation de chaîne de démarrage propre.
- Discrawl rapporte : les recherches de support/démarrage WSL2 incluent des conseils de support selon lesquels la passerelle systemd WSL2 démarre quand Ubuntu/WSL démarre, mais le démarrage de Windows seul peut ne pas démarrer WSL sans configuration supplémentaire.
- Bonnes qualités : la documentation appelle explicitement la chaîne de démarrage sans tête au lieu d'impliquer qu'un service utilisateur Linux résout automatiquement le démarrage de Windows.
- Mauvaises qualités : la chaîne traverse le produit, WSL, le planificateur de tâches Windows et les paramètres d'alimentation de Windows, donc le succès opérationnel dépend fortement du fait que les utilisateurs suivent et maintiennent une tâche Windows manuelle côté.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont exclues de ce score de qualité.

## Score de complétude

- Score : `Alpha (64%)`
- Instructions de surface : évaluées par rapport à `references/completeness/windows-via-wsl2.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le linger du service utilisateur WSL, la disponibilité de Systemd après le démarrage de Windows, la tâche de démarrage Windows pour WSL, la vérification avant la connexion Windows, les attentes claires concernant l'alimentation du PC.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin d'une tâche de démarrage WSL gérée par OpenClaw ou vérifiée par doctor.
- Besoin de preuve en direct que la passerelle est accessible après le redémarrage de Windows avant la connexion.
- Besoin d'un message `status` ou `doctor` plus clair quand le service WSL2 est sain mais que le démarrage de Windows n'a pas démarré WSL.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:94` : la documentation introduit le démarrage automatique de Gateway avant la connexion Windows.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:99` : la première étape de la chaîne de démarrage est `sudo loginctl enable-linger "$(whoami)"`.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:107` : la deuxième étape installe le service utilisateur OpenClaw Gateway à l'intérieur de WSL.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:115` : la troisième étape démarre WSL automatiquement au démarrage de Windows à l'aide de PowerShell.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:120` : la commande de tâche planifiée appelle `wsl.exe -d Ubuntu --exec /bin/true` au démarrage en tant que SYSTEM.
- `/Users/kevinlin/code/openclaw/docs/platforms/windows.md:129` : la vérification vérifie `systemctl --user is-enabled` et `systemctl --user status`.

### Source

- `/Users/kevinlin/code/openclaw/src/daemon/systemd-hints.ts:17` : les conseils du serveur sans tête incluent `loginctl enable-linger`.
- `/Users/kevinlin/code/openclaw/src/flows/doctor-health-contributions.ts:623` : la santé systemd-linger du doctor importe l'assistant linger pour les services utilisateur Linux.
- `/Users/kevinlin/code/openclaw/src/flows/doctor-health-contributions.ts:642` : la santé linger explique que systemd arrête la session utilisateur à la déconnexion/inactivité sans lingering.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd-linger.ts` : l'assistant systemd linger possède le statut et l'activation du linger utilisateur.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/.github/workflows/windows-testbox-probe.yml:76` : le workflow sonde la disponibilité de WSL2 sur les exécuteurs Windows.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/doctor-install-switch/scenario.sh:12` : Docker e2e stub `loginctl` et systemd pour les flux de service.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/response.test.ts:26` : les tests de réponse daemon classifient les conseils systemd linger sans tête.
- `/Users/kevinlin/code/openclaw/src/cli/daemon-cli/response.test.ts:34` : les tests de réponse daemon classifient les conseils systemd WSL.
- `/Users/kevinlin/code/openclaw/src/daemon/systemd.test.ts` : les tests systemd couvrent la disponibilité du service utilisateur et le comportement du bus utilisateur.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "WSL2 Windows boot loginctl linger schtasks" --mode keyword --limit 8 --json`
- `gitcrawl search openclaw/openclaw --query "Windows WSL2 gateway systemd" --mode keyword --limit 10 --json`

Résultats :

- La requête exacte boot/loginctl/schtasks a retourné 0 résultats.
- La requête WSL2 systemd plus large a retourné 10 résultats actifs de cycle de vie de service, incluant le PR de diagnostics WSL #58853, le PR du bus utilisateur WSL #68400, les problèmes de cycle de vie de Gateway WSL2 et les problèmes de redémarrage/verrouillage de systemd.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "WSL2 Windows boot loginctl linger schtasks"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 8 "Windows WSL2 gateway systemd"`

Résultats :

- La requête exacte boot/loginctl/schtasks n'a retourné aucun résultat affiché.
- La requête WSL2 systemd a retourné des conseils de support selon lesquels le service Gateway devrait démarrer automatiquement quand Ubuntu/WSL démarre, mais que le démarrage de Windows seul ne signifie pas toujours que WSL a démarré.
