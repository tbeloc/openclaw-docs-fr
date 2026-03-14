---
summary: "Rituel d'amorçage d'agent qui initialise les fichiers d'espace de travail et d'identité"
read_when:
  - Understanding what happens on the first agent run
  - Explaining where bootstrapping files live
  - Debugging onboarding identity setup
title: "Amorçage d'agent"
sidebarTitle: "Amorçage"
---

# Amorçage d'agent

L'amorçage est le rituel de **première exécution** qui prépare un espace de travail d'agent et
collecte les détails d'identité. Il se produit après l'intégration, au premier démarrage de l'agent.

## Ce que fait l'amorçage

À la première exécution de l'agent, OpenClaw amorce l'espace de travail (par défaut
`~/.openclaw/workspace`) :

- Initialise `AGENTS.md`, `BOOTSTRAP.md`, `IDENTITY.md`, `USER.md`.
- Exécute un court rituel de questions-réponses (une question à la fois).
- Écrit l'identité + les préférences dans `IDENTITY.md`, `USER.md`, `SOUL.md`.
- Supprime `BOOTSTRAP.md` une fois terminé pour qu'il ne s'exécute qu'une seule fois.

## Où il s'exécute

L'amorçage s'exécute toujours sur l'**hôte de passerelle**. Si l'application macOS se connecte à
une passerelle distante, l'espace de travail et les fichiers d'amorçage se trouvent sur cette machine distante.

<Note>
Lorsque la passerelle s'exécute sur une autre machine, modifiez les fichiers d'espace de travail sur l'hôte de passerelle
(par exemple, `user@gateway-host:~/.openclaw/workspace`).
</Note>

## Documentation connexe

- Intégration de l'application macOS : [Intégration](/start/onboarding)
- Disposition de l'espace de travail : [Espace de travail d'agent](/concepts/agent-workspace)
