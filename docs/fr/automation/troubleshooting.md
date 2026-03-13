---
summary: "Dépanner la planification et la livraison des tâches cron et heartbeat"
read_when:
  - Cron ne s'est pas exécuté
  - Cron s'est exécuté mais aucun message n'a été livré
  - Heartbeat semble silencieux ou ignoré
title: "Dépannage de l'automatisation"
---

# Dépannage de l'automatisation

Utilisez cette page pour les problèmes de planificateur et de livraison (`cron` + `heartbeat`).

## Échelle de commandes

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Ensuite, exécutez les vérifications d'automatisation :

```bash
openclaw cron status
openclaw cron list
openclaw system heartbeat last
```

## Cron ne s'exécute pas

```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw logs --follow
```

Une bonne sortie ressemble à :

- `cron status` signale activé et un `nextWakeAtMs` futur.
- La tâche est activée et a un calendrier/fuseau horaire valide.
- `cron runs` affiche `ok` ou une raison d'ignorance explicite.

Signatures courantes :

- `cron: scheduler disabled; jobs will not run automatically` → cron désactivé dans la config/env.
- `cron: timer tick failed` → le tick du planificateur a échoué ; inspectez le contexte de pile/log environnant.
- `reason: not-due` dans la sortie d'exécution → exécution manuelle appelée sans `--force` et tâche pas encore due.

## Cron s'est exécuté mais pas de livraison

```bash
openclaw cron runs --id <jobId> --limit 20
openclaw cron list
openclaw channels status --probe
openclaw logs --follow
```

Une bonne sortie ressemble à :

- Le statut d'exécution est `ok`.
- Le mode/cible de livraison sont définis pour les tâches isolées.
- La sonde de canal signale le canal cible connecté.

Signatures courantes :

- L'exécution a réussi mais le mode de livraison est `none` → aucun message externe n'est attendu.
- Cible de livraison manquante/invalide (`channel`/`to`) → l'exécution peut réussir en interne mais ignorer le sortant.
- Erreurs d'authentification de canal (`unauthorized`, `missing_scope`, `Forbidden`) → livraison bloquée par les credentials/permissions du canal.

## Heartbeat supprimé ou ignoré

```bash
openclaw system heartbeat last
openclaw logs --follow
openclaw config get agents.defaults.heartbeat
openclaw channels status --probe
```

Une bonne sortie ressemble à :

- Heartbeat activé avec un intervalle non nul.
- Le dernier résultat de heartbeat est `ran` (ou la raison d'ignorance est comprise).

Signatures courantes :

- `heartbeat skipped` avec `reason=quiet-hours` → en dehors de `activeHours`.
- `requests-in-flight` → voie principale occupée ; heartbeat différé.
- `empty-heartbeat-file` → heartbeat d'intervalle ignoré car `HEARTBEAT.md` n'a pas de contenu actionnable et aucun événement cron balisé n'est en attente.
- `alerts-disabled` → les paramètres de visibilité suppriment les messages heartbeat sortants.

## Pièges du fuseau horaire et activeHours

```bash
openclaw config get agents.defaults.heartbeat.activeHours
openclaw config get agents.defaults.heartbeat.activeHours.timezone
openclaw config get agents.defaults.userTimezone || echo "agents.defaults.userTimezone not set"
openclaw cron list
openclaw logs --follow
```

Règles rapides :

- `Config path not found: agents.defaults.userTimezone` signifie que la clé n'est pas définie ; heartbeat revient au fuseau horaire de l'hôte (ou `activeHours.timezone` s'il est défini).
- Cron sans `--tz` utilise le fuseau horaire de l'hôte gateway.
- Heartbeat `activeHours` utilise la résolution de fuseau horaire configurée (`user`, `local`, ou IANA tz explicite).
- Les timestamps ISO sans fuseau horaire sont traités comme UTC pour les calendriers cron `at`.

Signatures courantes :

- Les tâches s'exécutent à la mauvaise heure après les changements de fuseau horaire de l'hôte.
- Heartbeat toujours ignoré pendant votre journée car `activeHours.timezone` est incorrect.

Connexes :

- [/automation/cron-jobs](/automation/cron-jobs)
- [/gateway/heartbeat](/gateway/heartbeat)
- [/automation/cron-vs-heartbeat](/automation/cron-vs-heartbeat)
- [/concepts/timezone](/concepts/timezone)
