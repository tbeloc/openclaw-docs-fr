```markdown
---
summary: "Référence CLI pour `openclaw security` (audit et correction des failles de sécurité courantes)"
read_when:
  - Vous voulez exécuter un audit de sécurité rapide sur la config/l'état
  - Vous voulez appliquer des suggestions de correction sûres (chmod, renforcer les valeurs par défaut)
title: "security"
---

# `openclaw security`

Outils de sécurité (audit + corrections optionnelles).

Connexes :

- Guide de sécurité : [Security](/gateway/security)

## Audit

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
openclaw security audit --json
```

L'audit avertit lorsque plusieurs expéditeurs DM partagent la session principale et recommande le **mode DM sécurisé** : `session.dmScope="per-channel-peer"` (ou `per-account-channel-peer` pour les canaux multi-comptes) pour les boîtes de réception partagées.
Ceci est destiné au renforcement des boîtes de réception coopératives/partagées. Une Gateway unique partagée par des opérateurs mutuellement non fiables/adversaires n'est pas une configuration recommandée ; divisez les limites de confiance avec des gateways séparées (ou des utilisateurs/hôtes OS séparés).
Il émet également `security.trust_model.multi_user_heuristic` lorsque la config suggère une entrée utilisateur partagée probable (par exemple une politique DM/groupe ouverte, des cibles de groupe configurées, ou des règles d'expéditeur avec caractères génériques), et vous rappelle qu'OpenClaw est un modèle de confiance d'assistant personnel par défaut.
Pour les configurations multi-utilisateurs intentionnelles, les conseils d'audit sont de mettre en sandbox toutes les sessions, de garder l'accès au système de fichiers limité à l'espace de travail, et de garder les identités personnelles/privées ou les credentials hors de ce runtime.
Il avertit également lorsque de petits modèles (`<=300B`) sont utilisés sans sandboxing et avec des outils web/navigateur activés.
Pour l'entrée webhook, il avertit lorsque `hooks.defaultSessionKey` n'est pas défini, lorsque les remplacements de `sessionKey` de requête sont activés, et lorsque les remplacements sont activés sans `hooks.allowedSessionKeyPrefixes`.
Il avertit également lorsque les paramètres Docker de sandbox sont configurés alors que le mode sandbox est désactivé, lorsque `gateway.nodes.denyCommands` utilise des entrées inefficaces de type motif/inconnues (correspondance exacte du nom de commande de nœud uniquement, pas de filtrage de texte shell), lorsque `gateway.nodes.allowCommands` active explicitement des commandes de nœud dangereuses, lorsque le profil global `tools.profile="minimal"` est remplacé par des profils d'outils d'agent, lorsque les groupes ouverts exposent les outils runtime/système de fichiers sans protections sandbox/espace de travail, et lorsque les outils de plugin d'extension installés peuvent être accessibles selon une politique d'outils permissive.
Il signale également `gateway.allowRealIpFallback=true` (risque d'usurpation d'en-tête si les proxies sont mal configurés) et `discovery.mdns.mode="full"` (fuite de métadonnées via les enregistrements TXT mDNS).
Il avertit également lorsque le navigateur sandbox utilise le réseau Docker `bridge` sans `sandbox.browser.cdpSourceRange`.
Il signale également les modes réseau Docker sandbox dangereux (y compris les jointures d'espace de noms `host` et `container:*`).
Il avertit lorsque les conteneurs Docker du navigateur sandbox existants ont des étiquettes de hash manquantes/obsolètes (par exemple les conteneurs pré-migration manquant `openclaw.browserConfigEpoch`) et recommande `openclaw sandbox recreate --browser --all`.
Il avertit lorsque les enregistrements d'installation de plugin/hook basés sur npm ne sont pas épinglés, manquent de métadonnées d'intégrité, ou dérivent des versions de package actuellement installées.
Il avertit lorsque les listes blanches de canaux s'appuient sur des noms/e-mails/tags mutables au lieu d'ID stables (Discord, Slack, Google Chat, MS Teams, Mattermost, portées IRC le cas échéant).
Il avertit lorsque `gateway.auth.mode="none"` laisse les API HTTP Gateway accessibles sans secret partagé (`/tools/invoke` plus tout point de terminaison `/v1/*` activé).
Les paramètres préfixés par `dangerous`/`dangerously` sont des remplacements explicites de l'opérateur de secours ; en activer un n'est pas, en soi, un rapport de vulnérabilité de sécurité.
Pour l'inventaire complet des paramètres dangereux, consultez la section « Résumé des drapeaux non sécurisés ou dangereux » dans [Security](/gateway/security).

## Sortie JSON

Utilisez `--json` pour les vérifications CI/politique :

```bash
openclaw security audit --json | jq '.summary'
openclaw security audit --deep --json | jq '.findings[] | select(.severity=="critical") | .checkId'
```

Si `--fix` et `--json` sont combinés, la sortie inclut à la fois les actions de correction et le rapport final :

```bash
openclaw security audit --fix --json | jq '{fix: .fix.ok, summary: .report.summary}'
```

## Ce que `--fix` change

`--fix` applique des remédiation sûres et déterministes :

- bascule `groupPolicy="open"` courant à `groupPolicy="allowlist"` (y compris les variantes de compte dans les canaux pris en charge)
- définit `logging.redactSensitive` de `"off"` à `"tools"`
- renforce les permissions pour l'état/config et les fichiers sensibles courants (`credentials/*.json`, `auth-profiles.json`, `sessions.json`, session `*.jsonl`)

`--fix` ne :

- ne fait pas tourner les tokens/mots de passe/clés API
- ne désactive pas les outils (`gateway`, `cron`, `exec`, etc.)
- ne change pas les choix d'exposition bind/auth/réseau de la gateway
- ne supprime ni ne réécrit les plugins/compétences
```
