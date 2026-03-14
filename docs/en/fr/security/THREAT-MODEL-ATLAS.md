# Modèle de menace OpenClaw v1.0

## Framework MITRE ATLAS

**Version :** 1.0-draft
**Dernière mise à jour :** 2026-02-04
**Méthodologie :** MITRE ATLAS + Diagrammes de flux de données
**Framework :** [MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for AI Systems)

### Attribution du framework

Ce modèle de menace est construit sur [MITRE ATLAS](https://atlas.mitre.org/), le framework standard de l'industrie pour documenter les menaces adversariales aux systèmes IA/ML. ATLAS est maintenu par [MITRE](https://www.mitre.org/) en collaboration avec la communauté de la sécurité IA.

**Ressources clés d'ATLAS :**

- [Techniques ATLAS](https://atlas.mitre.org/techniques/)
- [Tactiques ATLAS](https://atlas.mitre.org/tactics/)
- [Études de cas ATLAS](https://atlas.mitre.org/studies/)
- [GitHub ATLAS](https://github.com/mitre-atlas/atlas-data)
- [Contribuer à ATLAS](https://atlas.mitre.org/resources/contribute)

### Contribuer à ce modèle de menace

Ceci est un document vivant maintenu par la communauté OpenClaw. Consultez [CONTRIBUTING-THREAT-MODEL.md](/security/CONTRIBUTING-THREAT-MODEL) pour les directives de contribution :

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
| Runtime de l'agent OpenClaw | Oui      | Exécution d'agent principal, appels d'outils, sessions       |
| Passerelle                | Oui      | Authentification, routage, intégration de canaux     |
| Intégrations de canaux   | Oui      | WhatsApp, Telegram, Discord, Signal, Slack, etc. |
| Marketplace ClawHub    | Oui      | Publication de compétences, modération, distribution       |
| Serveurs MCP            | Oui      | Fournisseurs d'outils externes                          |
| Appareils utilisateur           | Partielle  | Applications mobiles, clients de bureau                     |

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
│                 LIMITE DE CONFIANCE 1 : Accès aux canaux                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      PASSERELLE                              │   │
│  │  • Appairage d'appareil (période de grâce de 30s)                      │   │
│  │  • Validation AllowFrom / AllowList                       │   │
│  │  • Authentification par jeton/mot de passe/Tailscale                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 2 : Isolation des sessions              │
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
│                 LIMITE DE CONFIANCE 3 : Exécution d'outils                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  SANDBOX D'EXÉCUTION                        │   │
│  │  • Sandbox Docker OU Hôte (exec-approvals)                │   │
│  │  • Exécution à distance de nœud                                  │   │
│  │  • Protection SSRF (épinglage DNS + blocage IP)            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 4 : Contenu externe               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              URLs / EMAILS / WEBHOOKS RÉCUPÉRÉS             │   │
│  │  • Encapsulation de contenu externe (balises XML)                   │   │
│  │  • Injection d'avis de sécurité                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 LIMITE DE CONFIANCE 5 : Chaîne d'approvisionnement                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      CLAWHUB                              │   │
│  │  • Publication de compétences (semver, SKILL.md requis)           │   │
│  │  • Drapeaux de modération basés sur des motifs                         │   │
│  │  • Analyse VirusTotal (à venir)                      │   │
│  │  • Vérification de l'ancienneté du compte GitHub                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Flux de données

| Flux | Source  | Destination | Données               | Protection           |
| ---- | ------- | ----------- | ------------------ | -------------------- |
| F1   | Canal | Passerelle     | Messages utilisateur      | TLS, AllowFrom       |
| F2   | Passerelle | Agent       | Messages routés    | Isolation de session    |
| F3   | Agent   | Outils       | Invocations d'outils   | Application de politique   |
| F4   | Agent   | Externe    | Requêtes web_fetch | Blocage SSRF        |
| F5   | ClawHub | Agent       | Code de compétence         | Modération, analyse |
| F6   | Agent   | Canal     | Réponses          | Filtrage de sortie     |

## 3. Analyse des menaces par tactique ATLAS

### 3.1 Reconnaissance (AML.TA0002)

#### T-RECON-001: Découverte de point de terminaison d'agent

| Attribut                | Valeur                                                                |
| ----------------------- | -------------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0006 - Active Scanning                                          |
| **Description**         | L'attaquant analyse les points de terminaison de passerelle OpenClaw exposés |
| **Vecteur d'attaque**   | Analyse réseau, requêtes shodan, énumération DNS                     |
| **Composants affectés** | Passerelle, points de terminaison API exposés                        |
| **Atténuations actuelles** | Option d'authentification Tailscale, liaison à loopback par défaut   |
| **Risque résiduel**     | Moyen - Les passerelles publiques sont découvrables                  |
| **Recommandations**     | Documenter le déploiement sécurisé, ajouter la limitation de débit sur les points de terminaison de découverte |

#### T-RECON-002: Sondage d'intégration de canal

| Attribut                | Valeur                                                              |
| ----------------------- | ------------------------------------------------------------------ |
| **ID ATLAS**            | AML.T0006 - Active Scanning                                        |
| **Description**         | L'attaquant sonde les canaux de messagerie pour identifier les comptes gérés par l'IA |
| **Vecteur d'attaque**   | Envoi de messages de test, observation des modèles de réponse      |
| **Composants affectés** | Toutes les intégrations de canal                                   |
| **Atténuations actuelles** | Aucune spécifique                                                  |
| **Risque résiduel**     | Faible - Valeur limitée de la découverte seule                     |
| **Recommandations**     | Envisager la randomisation du délai de réponse                     |

---

### 3.2 Accès initial (AML.TA0004)

#### T-ACCESS-001: Interception de code d'appairage

| Attribut                | Valeur                                                    |
| ----------------------- | -------------------------------------------------------- |
| **ID ATLAS**            | AML.T0040 - AI Model Inference API Access                |
| **Description**         | L'attaquant intercepte le code d'appairage pendant la période de grâce de 30s |
| **Vecteur d'attaque**   | Observation par-dessus l'épaule, reniflage réseau, ingénierie sociale |
| **Composants affectés** | Système d'appairage d'appareil                           |
| **Atténuations actuelles** | Expiration de 30s, codes envoyés via canal existant      |
| **Risque résiduel**     | Moyen - Période de grâce exploitable                     |
| **Recommandations**     | Réduire la période de grâce, ajouter une étape de confirmation |

#### T-ACCESS-002: Usurpation d'AllowFrom

| Attribut                | Valeur                                                                          |
| ----------------------- | ------------------------------------------------------------------------------ |
| **ID ATLAS**            | AML.T0040 - AI Model Inference API Access                                      |
| **Description**         | L'attaquant usurpe l'identité de l'expéditeur autorisé dans le canal           |
| **Vecteur d'attaque**   | Dépend du canal - usurpation de numéro de téléphone, usurpation de nom d'utilisateur |
| **Composants affectés** | Validation AllowFrom par canal                                                 |
| **Atténuations actuelles** | Vérification d'identité spécifique au canal                                    |
| **Risque résiduel**     | Moyen - Certains canaux vulnérables à l'usurpation                             |
| **Recommandations**     | Documenter les risques spécifiques au canal, ajouter la vérification cryptographique où possible |

#### T-ACCESS-003: Vol de jeton

| Attribut                | Valeur                                                       |
| ----------------------- | ----------------------------------------------------------- |
| **ID ATLAS**            | AML.T0040 - AI Model Inference API Access                   |
| **Description**         | L'attaquant vole les jetons d'authentification des fichiers de configuration |
| **Vecteur d'attaque**   | Malware, accès non autorisé à l'appareil, exposition de sauvegarde de configuration |
| **Composants affectés** | ~/.openclaw/credentials/, stockage de configuration         |
| **Atténuations actuelles** | Permissions de fichier                                      |
| **Risque résiduel**     | Élevé - Les jetons sont stockés en texte brut              |
| **Recommandations**     | Implémenter le chiffrement des jetons au repos, ajouter la rotation des jetons |

---

### 3.3 Exécution (AML.TA0005)

#### T-EXEC-001: Injection de prompt directe

| Attribut                | Valeur                                                                                     |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0051.000 - LLM Prompt Injection: Direct                                              |
| **Description**         | L'attaquant envoie des prompts élaborés pour manipuler le comportement de l'agent         |
| **Vecteur d'attaque**   | Messages de canal contenant des instructions adversariales                                |
| **Composants affectés** | LLM d'agent, toutes les surfaces d'entrée                                                 |
| **Atténuations actuelles** | Détection de motif, encapsulation de contenu externe                                      |
| **Risque résiduel**     | Critique - Détection uniquement, pas de blocage ; les attaques sophistiquées contournent |
| **Recommandations**     | Implémenter une défense multicouche, validation de sortie, confirmation utilisateur pour les actions sensibles |

#### T-EXEC-002: Injection de prompt indirecte

| Attribut                | Valeur                                                       |
| ----------------------- | ----------------------------------------------------------- |
| **ID ATLAS**            | AML.T0051.001 - LLM Prompt Injection: Indirect              |
| **Description**         | L'attaquant intègre des instructions malveillantes dans le contenu récupéré |
| **Vecteur d'attaque**   | URLs malveillantes, emails empoisonnés, webhooks compromis  |
| **Composants affectés** | web_fetch, ingestion d'email, sources de données externes   |
| **Atténuations actuelles** | Encapsulation de contenu avec balises XML et avis de sécurité |
| **Risque résiduel**     | Élevé - Le LLM peut ignorer les instructions d'encapsulation |
| **Recommandations**     | Implémenter l'assainissement du contenu, contextes d'exécution séparés |

#### T-EXEC-003: Injection d'argument d'outil

| Attribut                | Valeur                                                        |
| ----------------------- | ------------------------------------------------------------ |
| **ID ATLAS**            | AML.T0051.000 - LLM Prompt Injection: Direct                 |
| **Description**         | L'attaquant manipule les arguments d'outil par injection de prompt |
| **Vecteur d'attaque**   | Prompts élaborés qui influencent les valeurs de paramètre d'outil |
| **Composants affectés** | Tous les appels d'outil                                      |
| **Atténuations actuelles** | Approbations exec pour les commandes dangereuses            |
| **Risque résiduel**     | Élevé - Repose sur le jugement de l'utilisateur             |
| **Recommandations**     | Implémenter la validation d'argument, appels d'outil paramétrés |

#### T-EXEC-004: Contournement d'approbation Exec

| Attribut                | Valeur                                                      |
| ----------------------- | ---------------------------------------------------------- |
| **ID ATLAS**            | AML.T0043 - Craft Adversarial Data                         |
| **Description**         | L'attaquant élabore des commandes qui contournent la liste d'autorisation d'approbation |
| **Vecteur d'attaque**   | Obfuscation de commande, exploitation d'alias, manipulation de chemin |
| **Composants affectés** | exec-approvals.ts, liste d'autorisation de commande        |
| **Atténuations actuelles** | Mode liste d'autorisation + demande                        |
| **Risque résiduel**     | Élevé - Pas d'assainissement de commande                    |
| **Recommandations**     | Implémenter la normalisation de commande, élargir la liste de blocage |

---

### 3.4 Persistance (AML.TA0006)

#### T-PERSIST-001: Installation de compétence malveillante

| Attribut                | Valeur                                                                    |
| ----------------------- | ------------------------------------------------------------------------ |
| **ID ATLAS**            | AML.T0010.001 - Supply Chain Compromise: AI Software                     |
| **Description**         | L'attaquant publie une compétence malveillante sur ClawHub               |
| **Vecteur d'attaque**   | Créer un compte, publier une compétence avec code malveillant caché      |
| **Composants affectés** | ClawHub, chargement de compétence, exécution d'agent                     |
| **Atténuations actuelles** | Vérification de l'âge du compte GitHub, drapeaux de modération basés sur des motifs |
| **Risque résiduel**     | Critique - Pas d'isolation, examen limité                                |
| **Recommandations**     | Intégration VirusTotal (en cours), isolation de compétence, examen communautaire |

#### T-PERSIST-002: Empoisonnement de mise à jour de compétence

| Attribut                | Valeur                                                          |
| ----------------------- | -------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0010.001 - Supply Chain Compromise: AI Software           |
| **Description**         | L'attaquant compromet une compétence populaire et pousse une mise à jour malveillante |
| **Vecteur d'attaque**   | Compromission de compte, ingénierie sociale du propriétaire de compétence |
| **Composants affectés** | Versioning ClawHub, flux de mise à jour automatique            |
| **Atténuations actuelles** | Empreinte digitale de version                                  |
| **Risque résiduel**     | Élevé - Les mises à jour automatiques peuvent extraire des versions malveillantes |
| **Recommandations**     | Implémenter la signature de mise à jour, capacité de restauration, épinglage de version |

#### T-PERSIST-003: Falsification de configuration d'agent

| Attribut                | Valeur                                                           |
| ----------------------- | --------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0010.002 - Supply Chain Compromise: Data                   |
| **Description**         | L'attaquant modifie la configuration de l'agent pour persister l'accès |
| **Vecteur d'attaque**   | Modification de fichier de configuration, injection de paramètres |
| **Composants affectés** | Configuration d'agent, politiques d'outil                       |
| **Atténuations actuelles** | Permissions de fichier                                          |
| **Risque résiduel**     | Moyen - Nécessite un accès local                                |
| **Recommandations**     | Vérification d'intégrité de configuration, journalisation d'audit pour les modifications de configuration |

---

### 3.5 Évasion de défense (AML.TA0007)

#### T-EVADE-001: Contournement de motif de modération

| Attribut                | Valeur                                                                  |
| ----------------------- | ---------------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0043 - Craft Adversarial Data                                     |
| **Description**         | L'attaquant élabore du contenu de compétence pour contourner les motifs de modération |
| **Vecteur d'attaque**   | Homoglyphes Unicode, astuces d'encodage, chargement dynamique          |
| **Composants affectés** | ClawHub moderation.ts                                                  |
| **Atténuations actuelles** | FLAG_RULES basés sur des motifs                                        |
| **Risque résiduel**     | Élevé - Les regex simples sont facilement contournées                  |
| **Recommandations**     | Ajouter l'analyse comportementale (VirusTotal Code Insight), détection basée sur AST |

#### T-EVADE-002: Échappement d'encapsulation de contenu

| Attribut                | Valeur                                                     |
| ----------------------- | --------------------------------------------------------- |
| **ID ATLAS**            | AML.T0043 - Craft Adversarial Data                        |
| **Description**         | L'attaquant élabore du contenu qui s'échappe du contexte d'encapsulation XML |
| **Vecteur d'attaque**   | Manipulation de balise, confusion de contexte, remplacement d'instruction |
| **Composants affectés** | Encapsulation de contenu externe                          |
| **Atténuations actuelles** | Balises XML + avis de sécurité                            |
| **Risque résiduel**     | Moyen - Les échappements nouveaux sont découverts régulièrement |
| **Recommandations**     | Couches d'encapsulation multiples, validation côté sortie  |

---

### 3.6 Découverte (AML.TA0008)

#### T-DISC-001: Énumération d'outil

| Attribut                | Valeur                                                 |
| ----------------------- | ----------------------------------------------------- |
| **ID ATLAS**            | AML.T0040 - AI Model Inference API Access             |
| **Description**         | L'attaquant énumère les outils disponibles par interrogation |
| **Vecteur d'attaque**   | Requêtes de style « Quels outils avez-vous ? »        |
| **Composants affectés** | Registre d'outil d'agent                              |
| **Atténuations actuelles** | Aucune spécifique                                     |
| **Risque résiduel**     | Faible - Les outils sont généralement documentés       |
| **Recommandations**     | Envisager les contrôles de visibilité d'outil          |

#### T-DISC-002: Extraction de données de session

| Attribut                | Valeur                                                 |
| ----------------------- | ----------------------------------------------------- |
| **ID ATLAS**            | AML.T0040 - AI Model Inference API Access             |
| **Description**         | L'attaquant extrait les données sensibles du contexte de session |
| **Vecteur d'attaque**   | Requêtes « De quoi avons-nous discuté ? », sondage de contexte |
| **Composants affectés** | Transcriptions de session, fenêtre de contexte         |
| **Atténuations actuelles** | Isolation de session par expéditeur                    |
| **Risque résiduel**     | Moyen - Les données intra-session sont accessibles     |
| **Recommandations**     | Implémenter la rédaction de données sensibles dans le contexte |

---

### 3.7 Collecte et exfiltration (AML.TA0009, AML.TA0010)

#### T-EXFIL-001: Vol de données via web_fetch

| Attribut                | Valeur                                                                  |
| ----------------------- | ---------------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0009 - Collection                                                 |
| **Description**         | L'attaquant exfiltre les données en instruisant l'agent d'envoyer vers une URL externe |
| **Vecteur d'attaque**   | Injection de prompt causant l'envoi de données par l'agent vers le serveur de l'attaquant |
| **Composants affectés** | Outil web_fetch                                                        |
| **Atténuations actuelles** | Blocage SSRF pour les réseaux internes                                 |
| **Risque résiduel**     | Élevé - Les URLs externes sont autorisées                              |
| **Recommandations**     | Implémenter la liste blanche d'URL, sensibilisation à la classification des données |

#### T-EXFIL-002: Envoi de message non autorisé

| Attribut                | Valeur                                                            |
| ----------------------- | ---------------------------------------------------------------- |
| **ID ATLAS**            | AML.T0009 - Collection                                           |
| **Description**         | L'attaquant cause l'envoi de messages contenant des données sensibles par l'agent |
| **Vecteur d'attaque**   | Injection de prompt causant l'envoi de messages par l'agent à l'attaquant |
| **Composants affectés** | Outil de message, intégrations de canal                          |
| **Atténuations actuelles** | Contrôle de messagerie sortante                                  |
| **Risque résiduel**     | Moyen - Le contrôle peut être contourné                          |
| **Recommandations**     | Exiger une confirmation explicite pour les nouveaux destinataires |

#### T-EXFIL-003: Récolte d'identifiants

| Attribut                | Valeur                                                   |
| ----------------------- | ------------------------------------------------------- |
| **ID ATLAS**            | AML.T0009 - Collection                                  |
| **Description**         | Une compétence malveillante récolte les identifiants du contexte d'agent |
| **Vecteur d'attaque**   | Le code de compétence lit les variables d'environnement, fichiers de configuration |
| **Composants affectés** | Environnement d'exécution de compétence                 |
| **Atténuations actuelles** | Aucune spécifique aux compétences                       |
| **Risque résiduel**     | Critique - Les compétences s'exécutent avec les privilèges d'agent |
| **Recommandations**     | Isolation de compétence, isolation d'identifiants       |

---

### 3.8 Impact (AML.TA0011)

#### T-IMPACT-001: Exécution de commande non autorisée

| Attribut                | Valeur                                               |
| ----------------------- | --------------------------------------------------- |
| **ID ATLAS**            | AML.T0031 - Erode AI Model Integrity                |
| **Description**         | L'attaquant exécute des commandes arbitraires sur le système utilisateur |
| **Vecteur d'attaque**   | Injection de prompt combinée avec contournement d'approbation exec |
| **Composants affectés** | Outil Bash, exécution de commande                   |
| **Atténuations actuelles** | Approbations exec, option sandbox Docker             |
| **Risque résiduel**     | Critique - Exécution d'hôte sans sandbox             |
| **Recommandations**     | Sandbox par défaut, améliorer l'UX d'approbation    |

#### T-IMPACT-002: Épuisement de ressources (DoS)

| Attribut                | Valeur                                              |
| ----------------------- | -------------------------------------------------- |
| **ID ATLAS**            | AML.T0031 - Erode AI Model Integrity               |
| **Description**         | L'attaquant épuise les crédits API ou les ressources de calcul |
| **Vecteur d'attaque**   | Inondation de messages automatisée, appels d'outil coûteux |
| **Composants affectés** | Passerelle, sessions d'agent, fournisseur API       |
| **Atténuations actuelles** | Aucune                                              |
| **Risque résiduel**     | Élevé - Pas de limitation de débit                  |
| **Recommandations**     | Implémenter les limites de débit par expéditeur, budgets de coût |

#### T-IMPACT-003: Dommages à la réputation

| Attribut                | Valeur                                                   |
| ----------------------- | ------------------------------------------------------- |
| **ID ATLAS**            | AML.T0031 - Erode AI Model Integrity                    |
| **Description**         | L'attaquant cause l'envoi de contenu nuisible/offensant par l'agent |
| **Vecteur d'attaque**   | Injection de prompt causant des réponses inappropriées  |
| **Composants affectés** | Génération de sortie, messagerie de canal              |
| **Atténuations actuelles** | Politiques de contenu du fournisseur LLM              |
| **Risque résiduel**     | Moyen - Les filtres du fournisseur sont imparfaits     |
| **Recommandations**     | Couche de filtrage de sortie, contrôles utilisateur    |

---

## 4. Analyse de la chaîne d'approvisionnement ClawHub

### 4.1 Contrôles de sécurité actuels

| Contrôle             | Implémentation              | Efficacité                                           |
| -------------------- | --------------------------- | ---------------------------------------------------- |
| Âge du compte GitHub | `requireGitHubAccountAge()` | Moyen - Élève la barre pour les nouveaux attaquants |
| Assainissement des chemins | `sanitizePath()`            | Élevé - Prévient la traversée de répertoires        |
| Validation du type de fichier | `isTextFile()`              | Moyen - Fichiers texte uniquement, mais peut être malveillant |
| Limites de taille    | 50 Mo de bundle total       | Élevé - Prévient l'épuisement des ressources        |
| SKILL.md obligatoire | Readme obligatoire          | Faible valeur de sécurité - Informatif uniquement   |
| Modération des motifs | FLAG_RULES dans moderation.ts | Faible - Facilement contournable                    |
| Statut de modération | Champ `moderationStatus`    | Moyen - Examen manuel possible                      |

### 4.2 Motifs de signalisation de modération

Motifs actuels dans `moderation.ts` :

```javascript
// Known-bad identifiers
/(keepcold131\/ClawdAuthenticatorTool|ClawdAuthenticatorTool)/i

// Suspicious keywords
/(malware|stealer|phish|phishing|keylogger)/i
/(api[-_ ]?key|token|password|private key|secret)/i
/(wallet|seed phrase|mnemonic|crypto)/i
/(discord\.gg|webhook|hooks\.slack)/i
/(curl[^\n]+\|\s*(sh|bash))/i
/(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd)/i
```

**Limitations :**

- Vérifie uniquement le slug, displayName, summary, frontmatter, metadata, chemins de fichiers
- N'analyse pas le contenu réel du code de compétence
- Les expressions régulières simples sont facilement contournables par obfuscation
- Pas d'analyse comportementale

### 4.3 Améliorations prévues

| Amélioration         | Statut                                | Impact                                                                |
| -------------------- | ------------------------------------- | --------------------------------------------------------------------- |
| Intégration VirusTotal | En cours                              | Élevé - Analyse comportementale Code Insight                          |
| Signalisation communautaire | Partielle (table `skillReports` existe) | Moyen                                                                 |
| Journalisation d'audit | Partielle (table `auditLogs` existe)  | Moyen                                                                 |
| Système de badges    | Implémenté                            | Moyen - `highlighted`, `official`, `deprecated`, `redactionApproved` |

---

## 5. Matrice des risques

### 5.1 Probabilité vs Impact

| ID de menace  | Probabilité | Impact   | Niveau de risque | Priorité |
| ------------- | ----------- | -------- | ---------------- | -------- |
| T-EXEC-001    | Élevée      | Critique | **Critique**     | P0       |
| T-PERSIST-001 | Élevée      | Critique | **Critique**     | P0       |
| T-EXFIL-003   | Moyen       | Critique | **Critique**     | P0       |
| T-IMPACT-001  | Moyen       | Critique | **Élevé**        | P1       |
| T-EXEC-002    | Élevée      | Élevé    | **Élevé**        | P1       |
| T-EXEC-004    | Moyen       | Élevé    | **Élevé**        | P1       |
| T-ACCESS-003  | Moyen       | Élevé    | **Élevé**        | P1       |
| T-EXFIL-001   | Moyen       | Élevé    | **Élevé**        | P1       |
| T-IMPACT-002  | Élevée      | Moyen    | **Élevé**        | P1       |
| T-EVADE-001   | Élevée      | Moyen    | **Moyen**        | P2       |
| T-ACCESS-001  | Faible      | Élevé    | **Moyen**        | P2       |
| T-ACCESS-002  | Faible      | Élevé    | **Moyen**        | P2       |
| T-PERSIST-002 | Faible      | Élevé    | **Moyen**        | P2       |

### 5.2 Chaînes d'attaque du chemin critique

**Chaîne d'attaque 1 : Vol de données basé sur les compétences**

```
T-PERSIST-001 → T-EVADE-001 → T-EXFIL-003
(Publier une compétence malveillante) → (Contourner la modération) → (Récolter les identifiants)
```

**Chaîne d'attaque 2 : Injection de prompt vers RCE**

```
T-EXEC-001 → T-EXEC-004 → T-IMPACT-001
(Injecter un prompt) → (Contourner l'approbation exec) → (Exécuter des commandes)
```

**Chaîne d'attaque 3 : Injection indirecte via contenu récupéré**

```
T-EXEC-002 → T-EXFIL-001 → Exfiltration externe
(Empoisonner le contenu URL) → (L'agent récupère et suit les instructions) → (Données envoyées à l'attaquant)
```

---

## 6. Résumé des recommandations

### 6.1 Immédiat (P0)

| ID    | Recommandation                              | Adresse                    |
| ----- | ------------------------------------------- | -------------------------- |
| R-001 | Compléter l'intégration VirusTotal          | T-PERSIST-001, T-EVADE-001 |
| R-002 | Implémenter le sandboxing des compétences   | T-PERSIST-001, T-EXFIL-003 |
| R-003 | Ajouter la validation de sortie pour les actions sensibles | T-EXEC-001, T-EXEC-002     |

### 6.2 Court terme (P1)

| ID    | Recommandation                           | Adresse      |
| ----- | ---------------------------------------- | ------------ |
| R-004 | Implémenter la limitation de débit       | T-IMPACT-002 |
| R-005 | Ajouter le chiffrement des tokens au repos | T-ACCESS-003 |
| R-006 | Améliorer l'UX et la validation de l'approbation exec | T-EXEC-004   |
| R-007 | Implémenter la liste blanche d'URL pour web_fetch | T-EXFIL-001  |

### 6.3 Moyen terme (P2)

| ID    | Recommandation                                        | Adresse       |
| ----- | ----------------------------------------------------- | ------------- |
| R-008 | Ajouter la vérification de canal cryptographique où possible | T-ACCESS-002  |
| R-009 | Implémenter la vérification de l'intégrité de la configuration | T-PERSIST-003 |
| R-010 | Ajouter la signature des mises à jour et l'épinglage de version | T-PERSIST-002 |

---

## 7. Appendices

### 7.1 Mappage des techniques ATLAS

| ID ATLAS      | Nom de la technique            | Menaces OpenClaw                                                 |
| ------------- | ------------------------------ | ---------------------------------------------------------------- |
| AML.T0006     | Analyse active                 | T-RECON-001, T-RECON-002                                         |
| AML.T0009     | Collecte                       | T-EXFIL-001, T-EXFIL-002, T-EXFIL-003                            |
| AML.T0010.001 | Chaîne d'approvisionnement : Logiciel IA | T-PERSIST-001, T-PERSIST-002                                     |
| AML.T0010.002 | Chaîne d'approvisionnement : Données | T-PERSIST-003                                                    |
| AML.T0031     | Éroder l'intégrité du modèle IA | T-IMPACT-001, T-IMPACT-002, T-IMPACT-003                         |
| AML.T0040     | Accès à l'API d'inférence du modèle IA | T-ACCESS-001, T-ACCESS-002, T-ACCESS-003, T-DISC-001, T-DISC-002 |
| AML.T0043     | Créer des données adversariales | T-EXEC-004, T-EVADE-001, T-EVADE-002                             |
| AML.T0051.000 | Injection de prompt LLM : Directe | T-EXEC-001, T-EXEC-003                                           |
| AML.T0051.001 | Injection de prompt LLM : Indirecte | T-EXEC-002                                                       |

### 7.2 Fichiers de sécurité clés

| Chemin                                | Objectif                    | Niveau de risque |
| ----------------------------------- | --------------------------- | ------------ |
| `src/infra/exec-approvals.ts`       | Logique d'approbation des commandes | **Critique** |
| `src/gateway/auth.ts`               | Authentification de la passerelle | **Critique** |
| `src/web/inbound/access-control.ts` | Contrôle d'accès aux canaux | **Critique** |
| `src/infra/net/ssrf.ts`             | Protection SSRF             | **Critique** |
| `src/security/external-content.ts`  | Atténuation de l'injection de prompt | **Critique** |
| `src/agents/sandbox/tool-policy.ts` | Application de la politique d'outils | **Critique** |
| `convex/lib/moderation.ts`          | Modération ClawHub          | **Élevé**    |
| `convex/lib/skillPublish.ts`        | Flux de publication de compétence | **Élevé**    |
| `src/routing/resolve-route.ts`      | Isolation de session        | **Moyen**    |

### 7.3 Glossaire

| Terme                | Définition                                                |
| -------------------- | --------------------------------------------------------- |
| **ATLAS**            | Paysage des menaces adversariales de MITRE pour les systèmes IA |
| **ClawHub**          | Marché des compétences d'OpenClaw                         |
| **Passerelle**       | Couche d'authentification et de routage des messages d'OpenClaw |
| **MCP**              | Model Context Protocol - interface du fournisseur d'outils |
| **Injection de prompt** | Attaque où des instructions malveillantes sont intégrées dans l'entrée |
| **Compétence**       | Extension téléchargeable pour les agents OpenClaw         |
| **SSRF**             | Server-Side Request Forgery (Falsification de requête côté serveur) |

---

_Ce modèle de menace est un document vivant. Signalez les problèmes de sécurité à security@openclaw.ai_
