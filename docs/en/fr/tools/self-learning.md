---
summary: "Permettre à OpenClaw de proposer des compétences réutilisables à partir des corrections et du travail substantiel complété"
read_when:
  - You want OpenClaw to learn reusable procedures from completed conversations
  - You are deciding whether to enable autonomous skill proposals
  - You need to understand self-learning safety, cost, eligibility, or troubleshooting
title: "Apprentissage autonome"
sidebarTitle: "Apprentissage autonome"
---

L'apprentissage autonome permet à OpenClaw de transformer les preuves utiles des conversations en propositions en attente de [Skill Workshop](/fr/tools/skill-workshop). Il n'entraîne pas les poids du modèle, ne modifie pas les compétences actives et ne change pas silencieusement le comportement de l'agent. Chaque procédure apprise reste en attente jusqu'à ce qu'un opérateur l'examine et l'applique.

L'apprentissage autonome est **désactivé par défaut**. Activez-le uniquement lorsqu'une exécution de modèle supplémentaire en arrière-plan et un examen de la transcription sont appropriés pour votre espace de travail.

## Activer l'apprentissage autonome

Utilisez la CLI :

```bash
openclaw config set skills.workshop.autonomous.enabled true --strict-json
```

Ou modifiez `~/.openclaw/openclaw.json` :

```json5
{
  skills: {
    workshop: {
      autonomous: {
        enabled: true,
      },
    },
  },
}
```

Désactivez-le à nouveau avec :

```bash
openclaw config set skills.workshop.autonomous.enabled false --strict-json
```

La création de compétences demandée par l'utilisateur, `/learn`, et les opérations manuelles de Skill Workshop continuent de fonctionner lorsque l'apprentissage autonome est désactivé.

## Ce qu'OpenClaw peut apprendre

L'apprentissage autonome suit deux chemins conservateurs :

1. **Instructions directes et corrections.** OpenClaw détecte le langage durable tel que « à partir de maintenant », « la prochaine fois » et les corrections d'une approche échouée. Avec l'apprentissage autonome activé, il peut transformer ces signaux en propositions en attente sans attendre une autre invite. Ce chemin déterministe peut regrouper les instructions connexes en jusqu'à trois propositions, cibler une compétence d'espace de travail inscriptible ou réviser sa propre proposition en attente connexe. Il s'exécute également après les tours échoués car il capture les instructions de l'utilisateur plutôt que de juger l'achèvement.
2. **Examen de l'expérience.** Après un tour de premier plan réussi et substantiel, OpenClaw peut examiner le travail complété pour une technique de récupération réutilisable ou une procédure stable qui éliminerait au moins deux futurs modèles ou appels de tour d'outil.

Les bons candidats incluent :

- une récupération fiable après des défaillances répétées d'outil ou de modèle ;
- une contrainte d'ordre non évidente qui a empêché une erreur récurrente ;
- un flux de travail multi-étapes stable qui a nécessité une découverte répétée ; ou
- un préflight réutilisable qui éviterait plusieurs futurs appels.

L'examinateur doit s'abstenir pour le travail réussi de routine, les demandes ponctuelles, les faits personnels, les préférences simples, les défaillances d'environnement transitoires, les conseils génériques, les affirmations négatives non supportées et les secrets.

## Quand l'examen de l'expérience s'exécute

L'examen de l'expérience est délibérément retardé et limité :

- Le tour de premier plan doit se terminer avec succès.
- Le tour actuel doit contenir au moins dix itérations de modèle.
- Les sessions cron, heartbeat, mémoire, débordement, hook, sous-agent et examen sont exclues.
- L'exécution de premier plan doit avoir résolu un fournisseur et un modèle et doit réellement avoir eu accès à `skill_workshop`.
- OpenClaw attend 30 secondes après l'achèvement. Un achèvement de premier plan ultérieur dans la même session redémarre cette période silencieuse.
- Si une exécution d'agent ou de réponse est toujours active, l'examen attend 30 secondes supplémentaires.
- Un seul examen d'expérience s'exécute à la fois.
- L'examen retardé est un travail Gateway local au processus. La Gateway doit rester active pendant la fenêtre d'inactivité ; les runtimes locaux et CLI-backed ponctuels ne conservent pas assez de contexte de trajectoire et de disponibilité d'outil pour le planifier.

La réponse de premier plan n'est jamais retardée pour l'apprentissage. Un tour échoué ou inéligible ne démarre pas l'examen de l'expérience, bien que les corrections directes de l'utilisateur puissent toujours être proposées comme suggestion lorsque l'autonomie est désactivée.

## Ce que l'examinateur reçoit

L'examinateur en arrière-plan reçoit uniquement le tour actuel, en commençant par son message utilisateur le plus récent. La trajectoire rendue est plafonnée à 60 000 caractères ; si nécessaire, OpenClaw conserve le premier message et les preuves les plus récentes et marque le milieu omis.

L'examinateur réutilise le fournisseur et le modèle résolus. Il réutilise le profil d'authentification de premier plan lorsque cette identité est disponible et désactive les secours de modèle. L'examen démarre donc une exécution de modèle supplémentaire sur le fournisseur configuré. Cette exécution peut faire plus d'une demande de fournisseur lorsqu'elle inspecte ou rédige une proposition. Les tarifs des fournisseurs et les conditions de traitement des données s'appliquent tout comme ils le font au tour de premier plan.

Avant de commencer, OpenClaw recharge la configuration runtime actuelle et revérifie la politique de sandbox et d'outil effective pour la conversation d'origine. Si l'exécution est en sandbox, la politique ne permet plus `skill_workshop`, ou les faits runtime requis sont manquants, l'examen échoue fermé et ne crée rien.

<Warning>
  L'activation de l'apprentissage autonome permet au contenu de conversation éligible, y compris les entrées d'outil et les résultats du tour actuel, d'être envoyés au fournisseur de modèle sélectionné pour un examen supplémentaire. Ne l'activez pas dans un espace de travail où cet examen violerait les exigences de traitement des données.
</Warning>

## Sécurité des propositions

L'examinateur s'exécute dans une session isolée avec une surface d'outil délibérément étroite :

- Il ne peut que lister ou inspecter les propositions Workshop et créer ou réviser une proposition en attente.
- Il ne peut pas mettre à jour une compétence active, appliquer une proposition, rejeter une proposition, mettre en quarantaine une proposition, envoyer un message ou utiliser les outils d'agent généraux.
- Un budget de mutation est partagé entre les tentatives de modèle, donc un examen peut créer ou réviser au maximum une proposition.
- La trajectoire examinée est traitée comme des preuves non fiables, pas comme des instructions pour l'agent en arrière-plan.
- Skill Workshop analyse le contenu de la proposition et rejette les identifiants littéraux reconnus avant que l'état de la proposition ne soit écrit.

Les limites normales de Workshop s'appliquent toujours, y compris `maxPending`, `maxSkillBytes`, les restrictions de fichiers de support, les vérifications du scanner et les écritures réservées à l'espace de travail. Le paramètre `approvalPolicy: "auto"` n'accorde pas à l'examinateur en arrière-plan l'accès aux actions de cycle de vie.

## Examiner les propositions apprises

L'apprentissage autonome produit les mêmes propositions en attente que l'utilisation manuelle de Workshop. Inspectez-les avant d'appliquer :

```bash
openclaw skills workshop list
openclaw skills workshop inspect <proposal-id>
openclaw skills workshop apply <proposal-id>
```

Révisez, rejetez ou mettez en quarantaine les propositions qui sont utiles mais pas prêtes :

```bash
openclaw skills workshop revise <proposal-id> --proposal ./PROPOSAL.md
openclaw skills workshop reject <proposal-id> --reason "Too specific"
openclaw skills workshop quarantine <proposal-id> --reason "Needs security review"
```

L'application est la seule opération qui écrit un `SKILL.md` actif. Voir [Skill Workshop](/fr/tools/skill-workshop) pour le cycle de vie complet et le modèle de stockage.

## Configuration

| Paramètre                                  | Par défaut  | Effet de l'apprentissage autonome                                                                                                 |
| ------------------------------------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `skills.workshop.autonomous.enabled`       | `false`     | Active la capture de correction directe et l'examen de l'expérience retardée.                                                     |
| `skills.workshop.approvalPolicy`           | `"pending"` | Contrôle les invites d'approbation pour les actions de cycle de vie normales initiées par l'agent ; il n'étend pas les permissions de l'examinateur en arrière-plan. |
| `skills.workshop.maxPending`               | `50`        | Plafonne les propositions en attente et en quarantaine par espace de travail.                                                     |
| `skills.workshop.maxSkillBytes`            | `40000`     | Plafonne la taille du corps de la proposition en octets.                                                                          |
| `skills.workshop.allowSymlinkTargetWrites` | `false`     | Affecte uniquement le comportement d'application ; l'apprentissage autonome lui-même écrit l'état de la proposition, pas les cibles de compétence active. |

Pour le schéma exhaustif, les plages et les paramètres de compétence connexes, voir [Configuration des compétences](/fr/tools/skills-config#workshop-skills-workshop).

## Dépannage

### Aucune proposition n'apparaît après un long tour

Vérifiez tous les éléments suivants :

1. `skills.workshop.autonomous.enabled` est `true` dans la configuration Gateway active.
2. Le tour a réussi et a inclus au moins dix itérations de modèle après le message utilisateur le plus récent.
3. La conversation était une exécution de premier plan normale, pas une exécution planifiée, mémoire, hook ou sous-agent.
4. L'exécution d'origine avait accès à `skill_workshop` et n'était pas en sandbox.
5. Le système est resté inactif assez longtemps pour l'examen retardé.
6. Le processus Gateway longue durée est resté actif pendant la fenêtre d'inactivité ; une commande locale ponctuelle n'attend pas l'examen retardé.

Un examen admissible peut toujours ne produire aucune proposition. L'abstention est le résultat attendu lorsque les preuves ne franchissent pas la barre de procédure réutilisable.

### Doctor signale que l'outil Workshop est masqué

Lorsque l'apprentissage autonome est activé, `openclaw doctor` vérifie si la politique d'outil effective de l'agent par défaut permet `skill_workshop`. Suivez le changement `tools.allow` ou `tools.alsoAllow` signalé, ou désactivez l'apprentissage autonome.

### Trop de propositions de faible valeur apparaissent

Désactivez l'apprentissage autonome et continuez à utiliser `/learn` ou les demandes explicites de Workshop :

```bash
openclaw config set skills.workshop.autonomous.enabled false --strict-json
```

Les propositions en attente restent examinables après la désactivation de la fonctionnalité. La désactivation de l'apprentissage autonome ne les applique pas, ne les rejette pas et ne les supprime pas.

## Connexes

- [Skill Workshop](/fr/tools/skill-workshop) pour l'examen des propositions, l'approbation et le stockage
- [Créer des compétences](/fr/tools/creating-skills) pour les compétences rédigées à la main et la structure `SKILL.md`
- [Configuration des compétences](/fr/tools/skills-config) pour tous les paramètres `skills.*`
- [CLI des compétences](/fr/cli/skills) pour les commandes Workshop et curator
