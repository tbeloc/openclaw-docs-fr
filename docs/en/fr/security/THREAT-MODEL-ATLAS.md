# Modèle de menace OpenClaw v1.0

## Framework MITRE ATLAS

**Version:** 1.0-draft
**Dernière mise à jour:** 2026-02-04
**Méthodologie:** MITRE ATLAS + Diagrammes de flux de données
**Framework:** [MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for AI Systems)

### Attribution du framework

Ce modèle de menace est basé sur [MITRE ATLAS](https://atlas.mitre.org/), le framework standard de l'industrie pour documenter les menaces adversariales aux systèmes IA/ML. ATLAS est maintenu par [MITRE](https://www.mitre.org/) en collaboration avec la communauté de la sécurité IA.

**Ressources clés d'ATLAS:**

- [Techniques ATLAS](https://atlas.mitre.org/techniques/)
- [Tactiques ATLAS](https://atlas.mitre.org/tactics/)
- [Études de cas ATLAS](https://atlas.mitre.org/studies/)
- [GitHub ATLAS](https://github.com/mitre-atlas/atlas-data)
- [Contribuer à ATLAS](https://atlas.mitre.org/resources/contribute)

### Contribuer à ce modèle de menace

Ceci est un document vivant maintenu par la communauté OpenClaw. Consultez [CONTRIBUTING-THREAT-MODEL.md](/security/CONTRIBUTING-THREAT-MODEL) pour les directives de contribution:

- Signaler de nouvelles menaces
- Mettre à jour les menaces existantes
- Proposer des chaînes d'attaque
- Suggérer des atténuations

---

## 1. Introduction

### 1.1 Objectif

Ce modèle de menace documente les menaces adversariales à la plateforme d'agent IA OpenClaw et à la marketplace de compétences ClawHub, en utilisant le framework MITRE ATLAS conçu spécifiquement pour les systèmes IA/ML.

### 1.2 Portée

| Composant              | Inclus | Notes                                            |
| ---------------------- | ------ | ------------------------------------------------ |
| Runtime de l'agent OpenClaw | Oui    | Exécution d'agent principal, appels d'outils, sessions       |
| Gateway                | Oui    | Authentification, routage, intégration de canaux     |
| Intégrations de canaux   | Oui    | WhatsApp, Telegram, Discord, Signal, Slack, etc. |
| Marketplace ClawHub    | Oui    | Publication de compétences, modération, distribution       |
| Serveurs MCP            | Oui    | Fournisseurs d'outils externes                          |
| Appareils utilisateur           | Partiel  | Applications mobiles, clients de bureau                     |

### 1.3 Hors de portée

Rien n'est explicitement hors de portée pour ce modèle de menace.

---

## 2. Architecture du système

### 2.1 Limites de confiance

```
┌─────────────────────────────────────────────────────────────────┐
│                    ZONE NON FIABLE                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  WhatsApp   │  │  Telegram   │  │   Discord   │  ...         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
└─────────┼────────────────┼────────────────┼──────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 1: Accès aux canaux                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      GATEWAY                              │   │
│  │  • Appairage d'appareil (période de grâce de 30s)                      │   │
│  │  • Validation AllowFrom / AllowList                       │   │
│  │  • Authentification Token/Mot de passe/Tailscale                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 2: Isolation des sessions              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   SESSIONS D'AGENT                          │   │
│  │  • Clé de session = agent:canal:pair                       │   │
│  │  • Politiques d'outils par agent                                │   │
│  │  • Journalisation des transcriptions                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 3: Exécution d'outils                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  SANDBOX D'EXÉCUTION                        │   │
│  │  • Sandbox Docker OU Hôte (exec-approvals)                │   │
│  │  • Exécution distante de nœud                                  │   │
│  │  • Protection SSRF (épinglage DNS + blocage IP)            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 4: Contenu externe               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              URLs RÉCUPÉRÉES / EMAILS / WEBHOOKS             │   │
│  │  • Enveloppe de contenu externe (balises XML)                   │   │
│  │  • Injection d'avis de sécurité                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 5: Chaîne d'approvisionnement                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      CLAWHUB                              │   │
│  │  • Publication de compétences (semver, SKILL.md requis)           │   │
│  │  • Drapeaux de modération basés sur des motifs                         │   │
│  │  • Analyse VirusTotal (à venir)                      │   │
│  │  • Vérification de l'âge du compte GitHub                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Flux de données

| Flux | Source  | Destination | Données               | Protection           |
| ---- | ------- | ----------- | -------------------- | -------------------- |
| F1   | Canal | Gateway     | Messages utilisateur      | TLS, AllowFrom       |
| F2   | Gateway | Agent       | Messages routés    | Isolation des sessions    |
| F3   | Agent   | Outils       | Invocations d'outils   | Application des politiques   |
| F4   | Agent   | Externe    | Requêtes web_fetch | Blocage SSRF        |
| F5   | ClawHub | Agent       | Code de compétence         | Modération, analyse |
| F6   | Agent   | Canal     | Réponses          | Filtrage de sortie     |

---

## 3. Analyse des menaces par tactique ATLAS

### 3.1 Reconnaissance (AML.TA0002)

#### T-RECON-001: Découverte du point de terminaison de l'agent

| Attribut               | Valeur                                                                |
| ----------------------- | -------------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0006 - Analyse active                                          |
| **Description**         | L'attaquant analyse les points de terminaison de la passerelle OpenClaw exposés                |
| **Vecteur d'attaque**       | Analyse réseau, requêtes shodan, énumération DNS                    |
| **Composants affectés** | Gateway, points de terminaison API exposés                                       |
| **Atténuations actuelles** | Option d'authentification Tailscale, liaison à la boucle locale par défaut                   |
| **Risque résiduel**       | Moyen - Les passerelles publiques sont découvrables                                |
| **Recommandations**     | Documenter le déploiement sécurisé, ajouter la limitation de débit sur les points de terminaison de découverte |

#### T-RECON-002: Sondage d'intégration de canal

| Attribut               | Valeur                                                              |
| ----------------------- | ------------------------------------------------------------------ |
| **ID ATLAS**            | AML.T0006 - Analyse active                                        |
| **Description**         | L'attaquant sonde les canaux de messagerie pour identifier les comptes gérés par l'IA |
| **Vecteur d'attaque**       | Envoi de messages de test, observation des modèles de réponse                 |
| **Composants affectés** | Toutes les intégrations de canaux                                           |
| **Atténuations actuelles** | Aucune spécifique                                                      |
| **Risque résiduel**       | Faible - Valeur limitée de la découverte seule                           |
| **Recommandations**     | Envisager la randomisation du délai de réponse                             |

---

### 3.2 Accès initial (AML.TA0004)

#### T-ACCESS-001: Interception du code d'appairage

| Attribut               | Valeur                                                    |
| ----------------------- | -------------------------------------------------------- |
| **ID ATLAS**            | AML.T0040 - Accès à l'API d'inférence du modèle IA                |
| **Description**         | L'attaquant intercepte le code d'appairage pendant la période de grâce de 30s |
| **Vecteur d'attaque**       | Observation par-dessus l'épaule, reniflage réseau, ingénierie sociale   |
| **Composants affectés** | Système d'appairage d'appareil                                    |
| **Atténuations actuelles** | Expiration de 30s, codes envoyés via le canal existant              |
| **Risque résiduel**       | Moyen - La période de grâce est exploitable                       |
| **Recommandations**     | Réduire la période de grâce, ajouter une étape de confirmation               |

#### T-ACCESS-002: Usurpation d'AllowFrom

| Attribut               | Valeur                                                                          |
| ----------------------- | ------------------------------------------------------------------------------ |
| **ID ATLAS**            | AML.T0040 - Accès à l'API d'inférence du modèle IA                                      |
| **Description**         | L'attaquant usurpe l'identité de l'expéditeur autorisé dans le canal                             |
| **Vecteur d'attaque**       | Dépend du canal - usurpation de numéro de téléphone, usurpation de nom d'utilisateur             |
| **Composants affectés** | Validation AllowFrom par canal                                               |
| **Atténuations actuelles** | Vérification d'identité spécifique au canal                                         |
| **Risque résiduel**       | Moyen - Certains canaux vulnérables à l'usurpation                                  |
| **Recommandations**     | Documenter les risques spécifiques au canal, ajouter la vérification cryptographique si possible |

#### T-ACCESS-003: Vol de jeton

| Attribut               | Valeur                                                       |
| ----------------------- | ----------------------------------------------------------- |
| **ID ATLAS**            | AML.T0040 - Accès à l'API d'inférence du modèle IA                   |
| **Description**         | L'attaquant vole les jetons d'authentification des fichiers de configuration     |
| **Vecteur d'attaque**       | Malware, accès non autorisé à l'appareil, exposition de sauvegarde de configuration |
| **Composants affectés** | ~/.openclaw/credentials/, stockage de configuration                    |
| **Atténuations actuelles** | Permissions de fichier                                            |
| **Risque résiduel**       | Élevé - Les jetons sont stockés en texte brut                           |
| **Recommandations**     | Implémenter le chiffrement des jetons au repos, ajouter la rotation des jetons      |

---

### 3.3 Exécution (AML.TA0005)

#### T-EXEC-001: Injection de prompt directe

| Attribut               | Valeur                                                                                     |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0051.000 - Injection de prompt LLM: Directe                                              |
| **Description**         | L'attaquant envoie des prompts élaborés pour manipuler le comportement de l'agent                               |
| **Vecteur d'attaque**       | Messages de canal contenant des instructions adversariales                                      |
| **Composants affectés** | LLM de l'agent, toutes les surfaces d'entrée                                                             |
| **Atténuations actuelles** | Détection de motifs, enveloppe de contenu externe                                              |
| **Risque résiduel**       | Critique - Détection uniquement, pas de blocage; les attaques sophistiquées contournent                      |
| **Recommandations**     | Implémenter une défense multicouche, validation de sortie, confirmation utilisateur pour les actions sensibles |

#### T-EXEC-002: Injection de prompt indirecte

| Attribut               | Valeur                                                       |
| ----------------------- | ----------------------------------------------------------- |
| **ID ATLAS**            | AML.T0051.001 - Injection de prompt LLM: Indirecte              |
| **Description**         | L'attaquant intègre des instructions malveillantes dans le contenu
