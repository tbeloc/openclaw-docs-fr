---
title: "Native Windows - CLI Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Native Windows - CLI Maturity Note

## Résumé

L'installation PowerShell native et les points d'entrée CLI sont implémentés et documentés,
avec un vrai chemin `install.ps1`, des modes d'installation npm et git, des solutions de secours
Node/Git portables, la réparation PATH, la gestion du wrapper `openclaw.cmd`, et un lanceur
`openclaw` empaqueté. Les preuves sont les plus solides au niveau du code source et de la
définition de vérification de version. Les signaux actuels des opérateurs Windows natifs montrent
toujours une confusion autour de PowerShell par rapport à WSL2, la visibilité PATH, le comportement
des tâches planifiées, et les frictions de démarrage/mise à jour spécifiques à Windows.

## Portée de la catégorie

Inclus dans cette catégorie :

- Installateur PowerShell : chemin d'installateur hébergé install.ps1 natif Windows et drapeaux.
- Bootstrap du gestionnaire de nœuds et de paquets : bootstrap Node, Git, pnpm, npm et PATH pour Windows natif.
- Installation globale npm : installation globale npm, installation de checkout git, et openclaw.cmd généré.
- Lanceur CLI empaqueté : lanceur CLI openclaw empaqueté, version, et points d'entrée doctor.
- Shims de commande Windows : lanceur .cmd Windows, PATHEXT, et compatibilité shim du gestionnaire de paquets.
- openclaw onboard : openclaw onboard et openclaw onboard --non-interactive sur Windows natif
- Configuration de la passerelle locale : configuration de la passerelle locale, choix d'authentification, gestion SecretRef du jeton/mot de passe de la passerelle, et valeurs par défaut du point de terminaison local.
- Drapeaux d'installation du démon : drapeaux d'installation du démon pour l'intégration Windows natif.
- Limite de configuration native-vs-WSL : limite de configuration entre la passerelle Windows natif et le chemin WSL2 recommandé.

## Fonctionnalités

- Installateur PowerShell : chemin d'installateur hébergé install.ps1 natif Windows et drapeaux.
- Bootstrap du gestionnaire de nœuds et de paquets : bootstrap Node, Git, pnpm, npm et PATH pour Windows natif.
- Installation globale npm : installation globale npm, installation de checkout git, et openclaw.cmd généré.
- Lanceur CLI empaqueté : lanceur CLI openclaw empaqueté, version, et points d'entrée doctor.
- Shims de commande Windows : lanceur .cmd Windows, PATHEXT, et compatibilité shim du gestionnaire de paquets.
- openclaw onboard : openclaw onboard et openclaw onboard --non-interactive sur Windows natif
- Configuration de la passerelle locale : configuration de la passerelle locale, choix d'authentification, gestion SecretRef du jeton/mot de passe de la passerelle, et valeurs par défaut du point de terminaison local.
- Drapeaux d'installation du démon : drapeaux d'installation du démon pour l'intégration Windows natif.
- Limite de configuration native-vs-WSL : limite de configuration entre la passerelle Windows natif et le chemin WSL2 recommandé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (74%)`
- Signaux positifs : le code de vérification de version définit une voie d'installateur
  Windows natif qui utilise l'URL `install.ps1` publiée, résout le shim
  `openclaw.cmd` frais à partir d'une nouvelle session PowerShell, exécute l'intégration,
  exerce les vérifications du cycle de vie de la passerelle gérée, puis bascule vers une
  passerelle manuelle pour des vérifications d'exécution moins instables.
- Signaux négatifs : cet audit a trouvé des définitions de test et des rapports d'archive
  antérieurs, mais n'a pas trouvé ou exécuté une preuve hébergée native Windows
  end-to-end fraîche à partir d'une machine propre via `install.ps1`, `openclaw --version`,
  `openclaw doctor`, et la santé de la passerelle gérée.
- Lacunes d'intégration : la voie d'installateur ignore intentionnellement la santé du
  démon lors de l'intégration installée sur Windows natif et utilise une solution de
  secours de passerelle manuelle pour les vérifications d'exécution ultérieures, ce qui
  maintient la couverture en deçà d'une preuve Windows natif entièrement gérée.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : les requêtes directes `install.ps1` et PowerShell PATH n'ont
  retourné aucun résultat exact de problème ; les requêtes de point d'entrée Windows
  natif plus larges ont retourné des problèmes ouverts autour de l'intégration lente,
  des sondes de passerelle, des blocages de démarrage/statut, des solutions de contournement
  PATH, et des solutions de secours de dossier de démarrage obsolètes.
- Rapports Discrawl : les threads d'installateur Windows montrent des utilisateurs mélangeant
  l'installateur Linux/WSL avec PowerShell natif, ayant besoin de `%AppData%\npm` sur PATH,
  rencontrant une confusion Git/Node, et recevant des conseils répétés selon lesquels WSL2
  reste le chemin Windows plus fluide.
- Bonnes qualités : les docs et le code source s'accordent sur `install.ps1` ; l'installateur
  a une gestion explicite des défaillances PowerShell, un fallback Node et MinGit portable,
  des modes d'installation npm/git, une exécution sûre de shim de commande Windows, une
  réparation PATH utilisateur, et un transfert post-installation version/doctor/onboarding.
- Mauvaises qualités : le chemin Windows natif est toujours plus difficile à exploiter que
  WSL2, l'installateur n'a pas de drapeau verbose dédié, et les cas limites PATH, shell,
  NTFS et tâche planifiée Windows restent visibles dans les archives de support et de problèmes.
- Exclu de la qualité : la largeur de validation est enregistrée sous Couverture et
  Preuves uniquement.

## Score de complétude

- Score : `Beta (74%)`
- Instructions de surface : évaluées par rapport à `references/completeness/native-windows-cli-and-gateway.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent
  la portée de la taxonomie pour l'installateur PowerShell, le bootstrap du gestionnaire de
  nœuds et de paquets, l'installation globale npm, le lanceur CLI empaqueté, les shims de
  commande Windows, openclaw onboard, la configuration de la passerelle locale, les drapeaux
  d'installation du démon, la limite de configuration native-vs-WSL.
- Signaux négatifs : la note archivée a précédé la notation de complétude process-version-3,
  donc ce score est initialisé à partir de la même largeur de preuves et du registre de
  lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les
  branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin d'un artefact de preuve Windows natif propre et actuel pour l'hébergement `install.ps1`
  via `openclaw --version`, `openclaw doctor`, l'intégration, l'installation de la passerelle
  gérée, et `openclaw gateway status`.
- Besoin de diagnostics d'opérateur plus clairs pour la réparation PATH et npm-prefix quand
  `openclaw` s'installe mais n'est pas découvrable dans une nouvelle session PowerShell.
- Besoin d'un commutateur d'installateur verbose de première classe au lieu de s'appuyer sur
  le traçage PowerShell.
- Les docs Windows natif doivent toujours réduire la confusion entre `install.ps1`,
  WSL2 `install.sh`, l'utilisation CLI uniquement, et l'utilisation du service de passerelle gérée.

# Preuve

## Docs

- Commande : `nl -ba /Users/kevinlin/code/openclaw/docs/install/index.md | sed -n '1,190p'`
- Résultats : `docs/install/index.md:10` documente Node 24 recommandé ou Node
  22.19+ et indique que Windows natif et WSL2 sont supportés avec WSL2 plus stable ;
  `docs/install/index.md:26` documente `iwr -useb https://openclaw.ai/install.ps1 | iex` ;
  `docs/install/index.md:68` documente les options d'installation globale npm, pnpm et bun ;
  `docs/install/index.md:151` documente `openclaw --version`,
  `openclaw doctor`, et `openclaw gateway status`.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/docs/install/installer.md | sed -n '279,435p'`
- Résultats : `docs/install/installer.md:279` décrit le flux `install.ps1` :
  PowerShell 5+, installation de Node via winget/Chocolatey/Scoop/Node portable,
  modes d'installation npm/git, mises à jour PATH, actualisation du service Gateway, vérification
  doctor au mieux, gestion des échecs de scriptblock, drapeaux, variables d'environnement et
  dépannage Windows.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/docs/platforms/windows.md | sed -n '1,190p'`
- Résultats : `docs/platforms/windows.md:10` indique que WSL2 est le chemin plus stable ;
  `docs/platforms/windows.md:23` dit que les flux CLI Windows natifs s'améliorent ;
  `docs/platforms/windows.md:29` liste l'installateur du site web via `install.ps1` et
  l'utilisation CLI locale telle que `openclaw --version` et `openclaw doctor` ;
  `docs/platforms/windows.md:40` documente d'abord la tâche planifiée avec repli du dossier de démarrage.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/docs/start/getting-started.md | sed -n '1,70p'`
- Résultats : `docs/start/getting-started.md:20` répète WSL2 comme recommandé pour
  l'expérience Windows complète et `docs/start/getting-started.md:40` affiche la
  commande d'installation PowerShell Windows natif.

## Source

- Commande : `nl -ba /Users/kevinlin/code/openclaw/scripts/install.ps1 | sed -n '1,1540p'`
- Résultats : `scripts/install.ps1:5` expose `-Tag`, `-InstallMethod npm|git`,
  `-GitDir`, `-NoOnboard`, `-NoGitUpdate`, et `-DryRun` ;
  `scripts/install.ps1:151` nécessite Node 22.19+ ;
  `scripts/install.ps1:183` place Node portable sous
  `%LOCALAPPDATA%\OpenClaw\deps\portable-node` ;
  `scripts/install.ps1:337` essaie winget, Chocolatey, Scoop, puis Node portable ;
  `scripts/install.ps1:458` utilise `%LOCALAPPDATA%\OpenClaw\deps\portable-git` ;
  `scripts/install.ps1:619` résout `openclaw.cmd` avant `openclaw` ;
  `scripts/install.ps1:704` exécute les shims de commande Windows à partir d'un répertoire local sûr ;
  `scripts/install.ps1:757` répare le PATH global npm ;
  `scripts/install.ps1:1060` installe `openclaw` globalement avec npm ;
  `scripts/install.ps1:1137` installe à partir de git, construit et
  écrit `%USERPROFILE%\.local\bin\openclaw.cmd` ;
  `scripts/install.ps1:1262` exécute `openclaw doctor --non-interactive` ;
  `scripts/install.ps1:1418` lit `openclaw --version` avant d'imprimer le succès ;
  `scripts/install.ps1:1500` démarre l'intégration sauf si `-NoOnboard` est défini.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/openclaw.mjs | sed -n '1,560p'`
- Résultats : `openclaw.mjs:1` est le lanceur Node empaqueté ;
  `openclaw.mjs:11` définit le plancher Node 22.19 ;
  `openclaw.mjs:87` inclut la gestion des signaux Windows ;
  `openclaw.mjs:332` imprime la récupération pour les installations source non construites et
  recommande `npm install -g openclaw@latest` ;
  `openclaw.mjs:448` supporte l'aide racine précalculée avant d'importer le runtime complet.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/package.json | sed -n '1,36p;1684,1696p;1778,1790p'`
- Résultats : `package.json:16` mappe le bin `openclaw` à `openclaw.mjs` ;
  `package.json:1786` définit `test:windows:ci` avec commande axée sur Windows,
  importation de runtime, processus, racine d'installation et vérifications de runner.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/src/daemon/schtasks.ts | sed -n '1,280p'`
- Résultats : `src/daemon/schtasks.ts:45` définit les conditions de repli Windows natif
  pour les échecs de tâche planifiée ;
  `src/daemon/schtasks.ts:121` construit le XML du planificateur de tâches ;
  `src/daemon/schtasks.ts:236` relit la commande de tâche générée.

## Tests d'intégration

- Commande : `nl -ba /Users/kevinlin/code/openclaw/scripts/openclaw-cross-os-release-checks.ts | sed -n '1122,1185p;1891,1925p;1990,2022p;3824,3833p'`
- Résultats : `scripts/openclaw-cross-os-release-checks.ts:1122` exécute un test de fumée d'importation de navigateur Windows installé ;
  `scripts/openclaw-cross-os-release-checks.ts:1132` exécute l'intégration installée ;
  `scripts/openclaw-cross-os-release-checks.ts:1142` exerce le cycle de vie du Gateway géré après l'installation ;
  `scripts/openclaw-cross-os-release-checks.ts:1161` documente le repli Gateway manuel Windows après validation de l'enregistrement de la tâche planifiée ;
  `scripts/openclaw-cross-os-release-checks.ts:1891` vérifie le chemin `openclaw --version` du shell Windows frais ;
  `scripts/openclaw-cross-os-release-checks.ts:2016` ajoute `--install-daemon` quand la voie demande l'installation du Gateway géré ;
  `scripts/openclaw-cross-os-release-checks.ts:3828` résout l'URL de l'installateur Windows natif publié à `https://openclaw.ai/install.ps1`.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/test/openclaw-launcher.e2e.test.ts | sed -n '100,180p;520,570p'`
- Résultats : `test/openclaw-launcher.e2e.test.ts:136` aligne le lanceur, la garde runtime et le plancher Node du paquet ;
  `test/openclaw-launcher.e2e.test.ts:539` vérifie la messagerie de récupération d'installation source ;
  `test/openclaw-launcher.e2e.test.ts:556` vérifie le comportement du cache de compilation de source-checkout.

## Tests unitaires

- Commande : `nl -ba /Users/kevinlin/code/openclaw/test/scripts/install-ps1.test.ts | sed -n '1,560p'`
- Résultats : `test/scripts/install-ps1.test.ts:63` couvre la gestion des échecs install.ps1 ;
  `test/scripts/install-ps1.test.ts:91` couvre les valeurs par défaut d'installation npm ;
  `test/scripts/install-ps1.test.ts:116` couvre l'exécution du shim de commande Windows ;
  `test/scripts/install-ps1.test.ts:192` couvre le repli Node portable ;
  `test/scripts/install-ps1.test.ts:232` couvre la persistance Git portable ;
  `test/scripts/install-ps1.test.ts:251` couvre l'activation pnpm épinglée au repo et le comportement d'installation git ;
  `test/scripts/install-ps1.test.ts:349` couvre le lancement d'intégration interactive.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/test/scripts/openclaw-cross-os-release-checks.test.ts | sed -n '612,770p;790,905p'`
- Résultats : `test/scripts/openclaw-cross-os-release-checks.test.ts:621` couvre la recherche CLI Windows frais sous le préfixe npm ;
  `test/scripts/openclaw-cross-os-release-checks.test.ts:680` sert `scripts/install.ps1` en tant que texte UTF-8 ;
  `test/scripts/openclaw-cross-os-release-checks.test.ts:756` mappe win32 à `install.ps1` ;
  `test/scripts/openclaw-cross-os-release-checks.test.ts:796` maintient le runtime de l'installateur Windows sur le Gateway manuel après les vérifications du cycle de vie géré ;
  `test/scripts/openclaw-cross-os-release-checks.test.ts:838` normalise les chemins CLI Windows installés à `.cmd` ;
  `test/scripts/openclaw-cross-os-release-checks.test.ts:886` enveloppe les replis `.cmd` CLI Windows installés en toute sécurité.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/src/infra/windows-install-roots.test.ts | sed -n '1,260p'`
- Résultats : `src/infra/windows-install-roots.test.ts:14` rejette les racines d'installation Windows invalides ;
  `src/infra/windows-install-roots.test.ts:27` préfère les racines du registre HKLM aux valeurs d'environnement ;
  `src/infra/windows-install-roots.test.ts:136` revient en toute sécurité quand les racines du registre et de l'environnement sont invalides.
- Commande : `nl -ba /Users/kevinlin/code/openclaw/test/openclaw-npm-postpublish-verify.test.ts | sed -n '220,278p'`
- Résultats : `test/openclaw-npm-postpublish-verify.test.ts:241` s'attend à ce que le chemin du shim npm Windows soit `<prefix>\openclaw.cmd` ;
  `test/openclaw-npm-postpublish-verify.test.ts:260` enveloppe le shim npm installé Windows via `cmd.exe` sans mode shell.

## Requêtes Gitcrawl

Requête :

```bash
gitcrawl doctor --json
gitcrawl search issues "install.ps1 Windows PowerShell openclaw version doctor npm global PATH" -R openclaw/openclaw --state open --json number,title,url,state --limit 8
gitcrawl search issues "install.ps1 Windows PowerShell openclaw version doctor npm global PATH" -R openclaw/openclaw --state closed --json number,title,url,state --limit 8
gitcrawl search issues "native Windows installer openclaw command not found PATH Node portable Git" -R openclaw/openclaw --state open --json number,title,url,state --limit 8
gitcrawl search issues "windows openclaw command not found" -R openclaw/openclaw --state open --json number,title,url,state --limit 8
gitcrawl search issues "windows openclaw command not found" -R openclaw/openclaw --state closed --json number,title,url,state --limit 8
gitcrawl search issues "windows gateway schtasks" -R openclaw/openclaw --state open --json number,title,url,state --limit 8
```

Résultats :

- La commande de fraîcheur a retourné l'état de l'archive gitcrawl enregistré ci-dessus.
- La recherche exacte `install.ps1 Windows PowerShell openclaw version doctor npm global PATH`
  a retourné `[]` pour les problèmes ouverts et fermés.
- La recherche exacte `native Windows installer openclaw command not found PATH Node portable Git`
  a retourné `[]` pour les problèmes ouverts.
- `windows openclaw command not found` a retourné 8 résultats ouverts, incluant
  #18985 support MSYS/Fish, #82594 intégration Windows lente, #79099 sonde gateway inaccessible alors que la santé est OK, #82735 codes d'erreur runtime/spawn stables, #73814 problème stdin du programme d'installation shell, #76563 échec de réparation doctor,
  #87353 rapport d'opération destructive non lié, et #86752 privation de gateway WSL2/Docker.
- `windows openclaw command not found` a retourné `[]` pour les problèmes fermés.
- `windows gateway schtasks` a retourné 7 résultats ouverts : #44559 fermeture de fenêtre PowerShell déconnecte Gateway, #70788 flash de fenêtre cmd du dossier de démarrage, #84600 fenêtre cmd visible du battement cardiaque, #84001 blocage du statut Windows, #76553 contournement PATH plus boucle de redémarrage Gateway, #87156 la mise à jour doctor laisse un repli du dossier de démarrage obsolète, et #78571 rapport de connexion Telegram.

## Requêtes Discrawl

Requête :

```bash
/Users/kevinlin/.local/bin/discrawl status --json
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "install.ps1 Windows PowerShell openclaw version doctor npm global PATH"
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "native Windows installer openclaw command not found PATH Node portable Git"
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "windows openclaw command not found"
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "windows install.ps1 WSL2 PowerShell"
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 6 "windows gateway schtasks"
```

Résultats :

- La commande de fraîcheur a retourné l'état de l'archive discrawl enregistré ci-dessus.
- Les requêtes exactes install.ps1/PowerShell/PATH et installateur natif/Git portable
  n'ont retourné aucun résultat stdout.
- `windows openclaw command not found` a retourné des fils de support sur le démarrage Telegram Windows,
  mauvaise expérience Windows natif, vérification de `openclaw --version`
  plus versions Node/npm, ajout de `%AppData%\npm` à PATH, récupération Git-for-Windows, et éviter `openclaw reset` pour les problèmes PATH/service/config.
- `windows install.ps1 WSL2 PowerShell` a retourné des fils où les utilisateurs avaient exécuté
  l'installateur Linux/WSL à partir de PowerShell natif, ont été invités à utiliser
  `install.ps1` dans PowerShell ou `install.sh` à l'intérieur de WSL2, et ont reçu
  des commandes directes `openclaw.cmd --version` et d'intégration quand PATH était suspect.
- `windows gateway schtasks` a retourné des résumés Windows natifs pour l'installateur,
  l'intégration, le démarrage de la tâche planifiée, le polissage de la fenêtre de console, le travail de mise à jour, et
  des discussions concrètes de repli/débogage de tâche planifiée.
