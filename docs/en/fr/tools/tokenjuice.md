---
title: "Tokenjuice"
summary: "Compacter les résultats des outils exec et bash bruyants avec un plugin fourni optionnel"
read_when:
  - Vous voulez des résultats `exec` ou `bash` plus courts dans OpenClaw
  - Vous voulez activer le plugin tokenjuice fourni
  - Vous devez comprendre ce que tokenjuice change et ce qu'il laisse brut
---

# Tokenjuice

`tokenjuice` est un plugin fourni optionnel qui compacte les résultats bruyants des outils `exec` et `bash` après l'exécution de la commande.

Il modifie le `tool_result` retourné, pas la commande elle-même. Tokenjuice ne réécrit pas l'entrée shell, ne réexécute pas les commandes et ne change pas les codes de sortie.

Aujourd'hui, cela s'applique aux exécutions Pi intégrées, où tokenjuice intercepte le chemin `tool_result` intégré et réduit la sortie qui revient dans la session.

## Activer le plugin

Chemin rapide :

```bash
openclaw config set plugins.entries.tokenjuice.enabled true
```

Équivalent :

```bash
openclaw plugins enable tokenjuice
```

OpenClaw livre déjà le plugin. Il n'y a pas d'étape `plugins install` ou `tokenjuice install openclaw` séparée.

Si vous préférez éditer la configuration directement :

```json5
{
  plugins: {
    entries: {
      tokenjuice: {
        enabled: true,
      },
    },
  },
}
```

## Ce que tokenjuice change

- Compacte les résultats bruyants de `exec` et `bash` avant qu'ils ne soient réinjectés dans la session.
- Garde l'exécution de la commande originale intacte.
- Préserve les lectures exactes du contenu des fichiers et autres commandes que tokenjuice doit laisser brutes.
- Reste optionnel : désactivez le plugin si vous voulez une sortie verbatim partout.

## Vérifier qu'il fonctionne

1. Activez le plugin.
2. Démarrez une session qui peut appeler `exec`.
3. Exécutez une commande bruyante comme `git status`.
4. Vérifiez que le résultat de l'outil retourné est plus court et plus structuré que la sortie shell brute.

## Désactiver le plugin

```bash
openclaw config set plugins.entries.tokenjuice.enabled false
```

Ou :

```bash
openclaw plugins disable tokenjuice
```
