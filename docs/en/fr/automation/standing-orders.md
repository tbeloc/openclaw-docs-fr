---
summary: "Définir une autorité opérationnelle permanente pour les programmes d'agents autonomes"
read_when:
  - Setting up autonomous agent workflows that run without per-task prompting
  - Defining what the agent can do independently vs. what needs human approval
  - Structuring multi-program agents with clear boundaries and escalation rules
title: "Standing Orders"
---

# Standing Orders

Les standing orders accordent à votre agent une **autorité opérationnelle permanente** pour des programmes définis. Au lieu de donner des instructions individuelles à chaque fois, vous définissez des programmes avec un périmètre clair, des déclencheurs et des règles d'escalade — et l'agent s'exécute de manière autonome dans ces limites.

C'est la différence entre dire à votre assistant « envoie le rapport hebdomadaire » chaque vendredi et accorder une autorité permanente : « Tu gères le rapport hebdomadaire. Compile-le chaque vendredi, envoie-le, et escalade uniquement si quelque chose semble anormal. »

## Pourquoi les Standing Orders ?

**Sans standing orders :**

- Vous devez inviter l'agent pour chaque tâche
- L'agent reste inactif entre les demandes
- Le travail de routine est oublié ou retardé
- Vous devenez le goulot d'étranglement

**Avec les standing orders :**

- L'agent s'exécute de manière autonome dans les limites définies
- Le travail de routine se fait selon le calendrier sans invitation
- Vous n'êtes impliqué que pour les exceptions et les approbations
- L'agent remplit le temps d'inactivité de manière productive

## Comment ça marche

Les standing orders sont définis dans vos fichiers [agent workspace](/fr/concepts/agent-workspace). L'approche recommandée est de les inclure directement dans `AGENTS.md` (qui est auto-injecté à chaque session) afin que l'agent les ait toujours en contexte. Pour les configurations plus grandes, vous pouvez également les placer dans un fichier dédié comme `standing-orders.md` et le référencer depuis `AGENTS.md`.

Chaque programme spécifie :

1. **Périmètre** — ce que l'agent est autorisé à faire
2. **Déclencheurs** — quand exécuter (calendrier, événement ou condition)
3. **Portes d'approbation** — ce qui nécessite une approbation humaine avant d'agir
4. **Règles d'escalade** — quand arrêter et demander de l'aide

L'agent charge ces instructions à chaque session via les fichiers bootstrap de l'espace de travail (voir [Agent Workspace](/fr/concepts/agent-workspace) pour la liste complète des fichiers auto-injectés) et s'exécute contre eux, combinés avec les [cron jobs](/fr/automation/cron-jobs) pour l'application basée sur le temps.

<Tip>
Mettez les standing orders dans `AGENTS.md` pour garantir qu'ils sont chargés à chaque session. Le bootstrap de l'espace de travail injecte automatiquement `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md` et `MEMORY.md` — mais pas les fichiers arbitraires dans les sous-répertoires.
</Tip>

## Anatomie d'un Standing Order

```markdown
## Program: Weekly Status Report

**Authority:** Compile data, generate report, deliver to stakeholders
**Trigger:** Every Friday at 4 PM (enforced via cron job)
**Approval gate:** None for standard reports. Flag anomalies for human review.
**Escalation:** If data source is unavailable or metrics look unusual (>2σ from norm)

### Execution Steps

1. Pull metrics from configured sources
2. Compare to prior week and targets
3. Generate report in Reports/weekly/YYYY-MM-DD.md
4. Deliver summary via configured channel
5. Log completion to Agent/Logs/

### What NOT to Do

- Do not send reports to external parties
- Do not modify source data
- Do not skip delivery if metrics look bad — report accurately
```

## Standing Orders + Cron Jobs

Les standing orders définissent **ce que** l'agent est autorisé à faire. Les [cron jobs](/fr/automation/cron-jobs) définissent **quand** cela se produit. Ils fonctionnent ensemble :

```
Standing Order: "You own the daily inbox triage"
    ↓
Cron Job (8 AM daily): "Execute inbox triage per standing orders"
    ↓
Agent: Reads standing orders → executes steps → reports results
```

Le message du cron job doit référencer le standing order plutôt que de le dupliquer :

```bash
openclaw cron create \
  --name daily-inbox-triage \
  --cron "0 8 * * 1-5" \
  --tz America/New_York \
  --timeout-seconds 300 \
  --announce \
  --channel bluebubbles \
  --to "+1XXXXXXXXXX" \
  --message "Execute daily inbox triage per standing orders. Check mail for new alerts. Parse, categorize, and persist each item. Report summary to owner. Escalate unknowns."
```

## Exemples

### Exemple 1 : Contenu et Médias Sociaux (Cycle Hebdomadaire)

```markdown
## Program: Content & Social Media

**Authority:** Draft content, schedule posts, compile engagement reports
**Approval gate:** All posts require owner review for first 30 days, then standing approval
**Trigger:** Weekly cycle (Monday review → mid-week drafts → Friday brief)

### Weekly Cycle

- **Monday:** Review platform metrics and audience engagement
- **Tuesday–Thursday:** Draft social posts, create blog content
- **Friday:** Compile weekly marketing brief → deliver to owner

### Content Rules

- Voice must match the brand (see SOUL.md or brand voice guide)
- Never identify as AI in public-facing content
- Include metrics when available
- Focus on value to audience, not self-promotion
```

### Exemple 2 : Opérations Financières (Déclenchement par Événement)

```markdown
## Program: Financial Processing

**Authority:** Process transaction data, generate reports, send summaries
**Approval gate:** None for analysis. Recommendations require owner approval.
**Trigger:** New data file detected OR scheduled monthly cycle

### When New Data Arrives

1. Detect new file in designated input directory
2. Parse and categorize all transactions
3. Compare against budget targets
4. Flag: unusual items, threshold breaches, new recurring charges
5. Generate report in designated output directory
6. Deliver summary to owner via configured channel

### Escalation Rules

- Single item > $500: immediate alert
- Category > budget by 20%: flag in report
- Unrecognizable transaction: ask owner for categorization
- Failed processing after 2 retries: report failure, do not guess
```

### Exemple 3 : Surveillance et Alertes (Continu)

```markdown
## Program: System Monitoring

**Authority:** Check system health, restart services, send alerts
**Approval gate:** Restart services automatically. Escalate if restart fails twice.
**Trigger:** Every heartbeat cycle

### Checks

- Service health endpoints responding
- Disk space above threshold
- Pending tasks not stale (>24 hours)
- Delivery channels operational

### Response Matrix

| Condition        | Action                   | Escalate?                |
| ---------------- | ------------------------ | ------------------------ |
| Service down     | Restart automatically    | Only if restart fails 2x |
| Disk space < 10% | Alert owner              | Yes                      |
| Stale task > 24h | Remind owner             | No                       |
| Channel offline  | Log and retry next cycle | If offline > 2 hours     |
```

## Le Modèle Execute-Verify-Report

Les standing orders fonctionnent mieux lorsqu'ils sont combinés avec une discipline d'exécution stricte. Chaque tâche dans un standing order doit suivre cette boucle :

1. **Execute** — Faire le travail réel (ne pas simplement reconnaître l'instruction)
2. **Verify** — Confirmer que le résultat est correct (fichier existe, message livré, données analysées)
3. **Report** — Dire au propriétaire ce qui a été fait et ce qui a été vérifié

```markdown
### Execution Rules

- Every task follows Execute-Verify-Report. No exceptions.
- "I'll do that" is not execution. Do it, then report.
- "Done" without verification is not acceptable. Prove it.
- If execution fails: retry once with adjusted approach.
- If still fails: report failure with diagnosis. Never silently fail.
- Never retry indefinitely — 3 attempts max, then escalate.
```

Ce modèle prévient le mode de défaillance d'agent le plus courant : reconnaître une tâche sans la compléter.

## Architecture Multi-Programme

Pour les agents gérant plusieurs domaines, organisez les standing orders comme des programmes séparés avec des limites claires :

```markdown
# Standing Orders

## Program 1: [Domain A] (Weekly)

...

## Program 2: [Domain B] (Monthly + On-Demand)

...

## Program 3: [Domain C] (As-Needed)

...

## Escalation Rules (All Programs)

- [Common escalation criteria]
- [Approval gates that apply across programs]
```

Chaque programme doit avoir :

- Son propre **cadence de déclenchement** (hebdomadaire, mensuel, événementiel, continu)
- Ses propres **portes d'approbation** (certains programmes nécessitent plus de surveillance que d'autres)
- Des **limites claires** (l'agent doit savoir où un programme se termine et où un autre commence)

## Bonnes Pratiques

### À Faire

- Commencer avec une autorité étroite et l'élargir à mesure que la confiance se construit
- Définir des portes d'approbation explicites pour les actions à haut risque
- Inclure des sections « Ce qu'il NE FAUT PAS faire » — les limites sont aussi importantes que les permissions
- Combiner avec les cron jobs pour une exécution fiable basée sur le temps
- Examiner les journaux de l'agent chaque semaine pour vérifier que les standing orders sont respectés
- Mettre à jour les standing orders à mesure que vos besoins évoluent — ce sont des documents vivants

### À Ne Pas Faire

- Accorder une autorité large dès le premier jour (« fais ce que tu penses être le mieux »)
- Ignorer les règles d'escalade — chaque programme a besoin d'une clause « quand arrêter et demander »
- Supposer que l'agent se souviendra des instructions verbales — mettez tout dans le fichier
- Mélanger les domaines dans un seul programme — séparez les programmes pour les domaines séparés
- Oublier d'appliquer avec les cron jobs — les standing orders sans déclencheurs deviennent des suggestions

## Connexes

- [Cron Jobs](/fr/automation/cron-jobs) — Planifier l'application des standing orders
- [Agent Workspace](/fr/concepts/agent-workspace) — Où vivent les standing orders, y compris la liste complète des fichiers bootstrap auto-injectés (AGENTS.md, SOUL.md, etc.)
