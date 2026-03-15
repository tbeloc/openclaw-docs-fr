---
summary: "Flux d'intégration au premier lancement pour OpenClaw (application macOS)"
read_when:
  - Designing the macOS onboarding assistant
  - Implementing auth or identity setup
title: "Intégration (Application macOS)"
sidebarTitle: "Intégration : Application macOS"
---

# Intégration (Application macOS)

Ce document décrit le flux d'intégration au premier lancement **actuel**. L'objectif est une expérience fluide au « jour 0 » : choisir où la Gateway s'exécute, connecter l'authentification, exécuter l'assistant et laisser l'agent s'initialiser.
Pour un aperçu général des chemins d'intégration, voir [Aperçu de l'intégration](/fr/start/onboarding-overview).

<Steps>
<Step title="Approuver l'avertissement macOS">
<Frame>
<img src="/assets/macos-onboarding/01-macos-warning.jpeg" alt="" />
</Frame>
</Step>
<Step title="Approuver la recherche de réseaux locaux">
<Frame>
<img src="/assets/macos-onboarding/02-local-networks.jpeg" alt="" />
</Frame>
</Step>
<Step title="Bienvenue et avis de sécurité">
<Frame caption="Lisez l'avis de sécurité affiché et décidez en conséquence">
<img src="/assets/macos-onboarding/03-security-notice.png" alt="" />
</Frame>

Modèle de confiance en matière de sécurité :

- Par défaut, OpenClaw est un agent personnel : une limite d'opérateur de confiance unique.
- Les configurations partagées/multi-utilisateurs nécessitent un verrouillage (limites de confiance divisées, accès aux outils minimal, et suivre [Sécurité](/fr/gateway/security)).
- L'intégration locale définit maintenant par défaut les nouvelles configurations sur `tools.profile: "coding"` afin que les nouvelles configurations locales conservent les outils de système de fichiers/runtime sans forcer le profil `full` sans restriction.
- Si les hooks/webhooks ou d'autres flux de contenu non fiable sont activés, utilisez un niveau de modèle moderne fort et maintenez une politique d'outils/sandboxing stricte.

</Step>
<Step title="Local ou distant">
<Frame>
<img src="/assets/macos-onboarding/04-choose-gateway.png" alt="" />
</Frame>

Où la **Gateway** s'exécute-t-elle ?

- **Ce Mac (Local uniquement) :** l'intégration peut configurer l'authentification et écrire les identifiants localement.
- **Distant (via SSH/Tailnet) :** l'intégration ne configure **pas** l'authentification locale ; les identifiants doivent exister sur l'hôte de la gateway.
- **Configurer plus tard :** ignorer la configuration et laisser l'application non configurée.

<Tip>
**Conseil d'authentification Gateway :**

- L'assistant génère maintenant un **token** même pour la boucle locale, donc les clients WS locaux doivent s'authentifier.
- Si vous désactivez l'authentification, tout processus local peut se connecter ; utilisez cela uniquement sur des machines entièrement fiables.
- Utilisez un **token** pour l'accès multi-machines ou les liaisons non-boucle.

</Tip>
</Step>
<Step title="Permissions">
<Frame caption="Choisissez les permissions que vous souhaitez accorder à OpenClaw">
<img src="/assets/macos-onboarding/05-permissions.png" alt="" />
</Frame>

L'intégration demande les permissions TCC nécessaires pour :

- Automatisation (AppleScript)
- Notifications
- Accessibilité
- Enregistrement d'écran
- Microphone
- Reconnaissance vocale
- Caméra
- Localisation

</Step>
<Step title="CLI">
  <Info>Cette étape est optionnelle</Info>
  L'application peut installer la CLI globale `openclaw` via npm/pnpm afin que les flux de terminal et les tâches launchd fonctionnent immédiatement.
</Step>
<Step title="Chat d'intégration (session dédiée)">
  Après la configuration, l'application ouvre une session de chat d'intégration dédiée afin que l'agent puisse se présenter et guider les étapes suivantes. Cela maintient les conseils au premier lancement séparés de votre conversation normale. Voir [Initialisation](/fr/start/bootstrapping) pour ce qui se passe sur l'hôte de la gateway lors de la première exécution de l'agent.
</Step>
</Steps>
