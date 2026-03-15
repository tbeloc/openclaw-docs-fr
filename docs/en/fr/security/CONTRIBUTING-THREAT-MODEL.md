# Contribuer au modèle de menace OpenClaw

Merci d'aider à sécuriser OpenClaw. Ce modèle de menace est un document vivant et nous accueillons les contributions de tous - vous n'avez pas besoin d'être un expert en sécurité.

## Façons de contribuer

### Ajouter une menace

Vous avez repéré un vecteur d'attaque ou un risque que nous n'avons pas couverts ? Ouvrez un problème sur [openclaw/trust](https://github.com/openclaw/trust/issues) et décrivez-le avec vos propres mots. Vous n'avez pas besoin de connaître des cadres ou de remplir chaque champ - décrivez simplement le scénario.

**Utile à inclure (mais non obligatoire) :**

- Le scénario d'attaque et comment il pourrait être exploité
- Quelles parties d'OpenClaw sont affectées (CLI, passerelle, canaux, ClawHub, serveurs MCP, etc.)
- Le niveau de gravité que vous pensez (faible / moyen / élevé / critique)
- Tous les liens vers des recherches connexes, des CVE ou des exemples du monde réel

Nous gérerons le mappage ATLAS, les ID de menace et l'évaluation des risques lors de l'examen. Si vous souhaitez inclure ces détails, c'est très bien - mais ce n'est pas attendu.

> **Ceci est pour ajouter au modèle de menace, pas pour signaler les vulnérabilités actives.** Si vous avez trouvé une vulnérabilité exploitable, consultez notre [page Trust](https://trust.openclaw.ai) pour les instructions de divulgation responsable.

### Suggérer une atténuation

Vous avez une idée sur comment résoudre une menace existante ? Ouvrez un problème ou une PR en référençant la menace. Les atténuations utiles sont spécifiques et exploitables - par exemple, « limitation de débit par expéditeur de 10 messages/minute à la passerelle » est mieux que « implémenter une limitation de débit ».

### Proposer une chaîne d'attaque

Les chaînes d'attaque montrent comment plusieurs menaces se combinent en un scénario d'attaque réaliste. Si vous voyez une combinaison dangereuse, décrivez les étapes et comment un attaquant les enchaînerait. Un court récit de la façon dont l'attaque se déroule en pratique est plus précieux qu'un modèle formel.

### Corriger ou améliorer le contenu existant

Fautes de frappe, clarifications, informations obsolètes, meilleurs exemples - les PR sont bienvenues, aucun problème n'est nécessaire.

## Ce que nous utilisons

### MITRE ATLAS

Ce modèle de menace est construit sur [MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for AI Systems), un cadre conçu spécifiquement pour les menaces IA/ML comme l'injection de prompt, l'abus d'outils et l'exploitation d'agents. Vous n'avez pas besoin de connaître ATLAS pour contribuer - nous mappons les soumissions au cadre lors de l'examen.

### ID de menace

Chaque menace reçoit un ID comme `T-EXEC-003`. Les catégories sont :

| Code    | Catégorie                                      |
| ------- | ---------------------------------------------- |
| RECON   | Reconnaissance - collecte d'informations       |
| ACCESS  | Accès initial - obtenir l'entrée               |
| EXEC    | Exécution - exécuter des actions malveillantes |
| PERSIST | Persistance - maintenir l'accès                |
| EVADE   | Évasion de défense - éviter la détection       |
| DISC    | Découverte - apprendre l'environnement         |
| EXFIL   | Exfiltration - voler des données               |
| IMPACT  | Impact - dommages ou perturbations             |

Les ID sont attribués par les responsables lors de l'examen. Vous n'avez pas besoin d'en choisir un.

### Niveaux de risque

| Niveau       | Signification                                                                    |
| ------------ | -------------------------------------------------------------------------------- |
| **Critique** | Compromission complète du système, ou probabilité élevée + impact critique       |
| **Élevé**    | Dommages importants probables, ou probabilité moyenne + impact critique          |
| **Moyen**    | Risque modéré, ou probabilité faible + impact élevé                             |
| **Faible**   | Peu probable et impact limité                                                   |

Si vous n'êtes pas sûr du niveau de risque, décrivez simplement l'impact et nous l'évaluerons.

## Processus d'examen

1. **Triage** - Nous examinons les nouvelles soumissions dans les 48 heures
2. **Évaluation** - Nous vérifions la faisabilité, attribuons le mappage ATLAS et l'ID de menace, validons le niveau de risque
3. **Documentation** - Nous nous assurons que tout est formaté et complet
4. **Fusion** - Ajouté au modèle de menace et à la visualisation

## Ressources

- [Site Web ATLAS](https://atlas.mitre.org/)
- [Techniques ATLAS](https://atlas.mitre.org/techniques/)
- [Études de cas ATLAS](https://atlas.mitre.org/studies/)
- [Modèle de menace OpenClaw](/fr/security/THREAT-MODEL-ATLAS)

## Contact

- **Vulnérabilités de sécurité :** Consultez notre [page Trust](https://trust.openclaw.ai) pour les instructions de signalement
- **Questions sur le modèle de menace :** Ouvrez un problème sur [openclaw/trust](https://github.com/openclaw/trust/issues)
- **Chat général :** Canal Discord #security

## Reconnaissance

Les contributeurs au modèle de menace sont reconnus dans les remerciements du modèle de menace, les notes de version et le hall of fame de la sécurité OpenClaw pour les contributions significatives.
