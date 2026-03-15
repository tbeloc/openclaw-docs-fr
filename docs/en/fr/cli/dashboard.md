---
summary: "Référence CLI pour `openclaw dashboard` (ouvrir l'interface de contrôle)"
read_when:
  - Vous souhaitez ouvrir l'interface de contrôle avec votre jeton actuel
  - Vous souhaitez imprimer l'URL sans lancer un navigateur
title: "dashboard"
---

# `openclaw dashboard`

Ouvrez l'interface de contrôle en utilisant votre authentification actuelle.

```bash
openclaw dashboard
openclaw dashboard --no-open
```

Remarques :

- `dashboard` résout les SecretRefs configurés `gateway.auth.token` si possible.
- Pour les jetons gérés par SecretRef (résolus ou non résolus), `dashboard` imprime/copie/ouvre une URL sans jeton pour éviter d'exposer les secrets externes dans la sortie du terminal, l'historique du presse-papiers ou les arguments de lancement du navigateur.
- Si `gateway.auth.token` est géré par SecretRef mais non résolu dans ce chemin de commande, la commande imprime une URL sans jeton et des conseils de correction explicites au lieu d'intégrer un espace réservé de jeton invalide.
