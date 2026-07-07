---
summary: "Référence CLI pour `openclaw promos` (lister et réclamer les offres de modèles promotionnels)"
read_when:
  - You want to try a free promotional model offer from ClawHub
  - You are configuring a provider through a promotion instead of onboarding
title: "Promos"
---

# `openclaw promos`

Découvrez et réclamez les offres de modèles promotionnels publiées sur ClawHub. Réclamer une
promotion configure le fournisseur (authentification et plugin, si nécessaire) et enregistre
les modèles de la promotion — sans relancer l'intégration et sans modifier
votre modèle par défaut sauf si vous le demandez.

Connexes :

- Modèle par défaut et secours : [Models](/fr/cli/models)
- Configuration de l'authentification du fournisseur : [Getting started](/fr/start/getting-started)

## Commandes

```bash
openclaw promos list
openclaw promos claim <slug>
openclaw promos claim <slug> --api-key <key> --set-default
```

## `openclaw promos list`

Liste les promotions actuellement actives, avec leurs modèles, le modèle suggéré
par défaut, le temps restant, et la commande de réclamation exacte. `--json` affiche la
charge utile brute.

## `openclaw promos claim <slug>`

Réclame une promotion active :

1. Récupère la promotion depuis ClawHub et vérifie qu'elle se trouve dans sa fenêtre de validité.
2. Valide le fournisseur de la promotion, le choix d'authentification et les packages de plugins déclarés
   par rapport à votre version OpenClaw installée. Les identifiants inconnus ou les incompatibilités de packages sont
   refusés — une promotion ne peut jamais faire exécuter au CLI quelque chose qu'il ne sait pas déjà
   comment faire.
3. Réutilise vos identifiants de fournisseur existants si vous les avez. Sinon, il
   suit le flux d'authentification normal du fournisseur (en affichant d'abord l'URL d'inscription de la promotion
   pour une clé gratuite). `--api-key <key>` complète l'authentification par clé API sans
   invites ; pour garder la clé hors de la ligne de commande, exportez la variable d'environnement du fournisseur
   à la place (par exemple `OPENROUTER_API_KEY`) — les identifiants d'environnement existants sont
   détectés automatiquement et aucun drapeau n'est nécessaire.
4. Enregistre les modèles de la promotion avec leurs alias. Les alias existants ne sont
   jamais écrasés.
5. Propose de définir le modèle suggéré de la promotion comme votre modèle par défaut —
   `--set-default` ignore la question ; sinon rien concernant vos paramètres par défaut ne
   change.

Lorsque la fenêtre de la promotion se termine, le fournisseur cesse de servir les modèles gratuits ;
votre configuration et vos identifiants restent inchangés. Revenez à tout moment avec
`openclaw models set <model>`.

## Découverte passive dans `models list`

`openclaw models list` met également en avant les promotions sans que vous demandiez ClawHub
directement :

- Les offres actives dont vous n'avez pas configuré les modèles apparaissent dans un
  groupe "Available via promotion" sous le tableau, chacune avec sa commande de
  réclamation.
- Les modèles que vous avez enregistrés via `promos claim` portent une étiquette `promo`, qui
  devient `promo ended` une fois que la fenêtre de l'offre se termine.
- La première fois qu'une nouvelle offre est vue, un avis unique pointe vers
  `openclaw promos list`. Les offres que vous avez déjà listées ou réclamées ne sont
  jamais annoncées à nouveau.

Cela lit une copie en cache local du flux de promotions hébergé par ClawHub
(normalement actualisé une fois par jour avec une demande conditionnelle, ou plus tôt lorsque l'instantané
en cache expire ; les échecs d'actualisation sont silencieusement ignorés). Une actualisation obsolète
attend au maximum 2,5 secondes et ne casse jamais le listage. Les sorties `--json` et
`--plain` restent propres pour les machines : pas de sections de promotion ou d'avis.
La réclamation revalide toujours par rapport à l'API ClawHub en direct, donc une offre retirée
tôt est refusée même si une copie en cache la montre toujours.
