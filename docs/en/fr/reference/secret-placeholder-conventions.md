---
summary: "Conventions de placeholder sécurisé pour les docs et exemples"
read_when:
  - Rédaction de docs incluant des tokens, clés API ou extraits d'identifiants
  - Mise à jour d'exemples qui peuvent être analysés par des outils de détection de secrets
title: "Conventions de placeholder de secret"
---

# Conventions de placeholder de secret

Utilisez des placeholders lisibles par l'homme mais qui ne ressemblent pas à de vrais secrets.

## Style recommandé

- Préférez les valeurs descriptives comme `example-openai-key-not-real` ou `example-discord-bot-token`.
- Pour les extraits shell, préférez `${OPENAI_API_KEY}` aux chaînes ressemblant à des tokens en ligne.
- Gardez les exemples manifestement faux et limités à leur objectif (fournisseur, canal, type d'authentification).

## Évitez ces modèles dans les docs

- Texte d'en-tête ou de pied de page de clé privée PEM littéral.
- Préfixes qui ressemblent à des identifiants actifs, par exemple `sk-...`, `xoxb-...`, `AKIA...`.
- Tokens bearer ressemblant à des données réelles copiés à partir des journaux d'exécution.

## Exemple

```bash
# Bon
export OPENAI_API_KEY="example-openai-key-not-real"

# Meilleur (quand la doc porte sur le câblage des variables d'environnement)
export OPENAI_API_KEY="${OPENAI_API_KEY}"
```
