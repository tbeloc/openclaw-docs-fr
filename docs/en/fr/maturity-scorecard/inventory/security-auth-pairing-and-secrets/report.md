---
title: "Rapport de maturité Sécurité, authentification, appairage et secrets"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité Sécurité, authentification, appairage et secrets

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Stable (80%)`
- Qualité : `Alpha (67%)`
- Complétude : `Stable (80%)`
- Fonctionnalités LTS : `5/6`

## Résumé

Ce rapport promeut les preuves archivées `security-auth-pairing-and-secrets` de `/Users/kevinlin/tmp/maturity/security-auth-pairing-and-secrets` dans le contrat d'inventaire actuel process-version-3.

Les scores de Couverture et Qualité de la catégorie proviennent des lignes de score soutenues par les preuves archivées. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                                | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                             |
| --------------------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Politique d'approbation et protections des outils dangereux](approval-policy-and-dangerous-tool-safeguards.md) | ✅  | `Stable (86%)` | `Beta (72%)`  | `Stable (86%)` | Politique d'approbation, Protections des outils dangereux                                                                                                                                                                                             |
| [Authentification de passerelle et accès à distance](gateway-auth-and-network-exposure.md)                  | ✅  | `Stable (82%)` | `Alpha (68%)` | `Stable (82%)` | Authentification par jeton/mot de passe de passerelle partagée, Mode d'authentification de passerelle, Identité de proxy de confiance, Tailscale Serve/Funnel, Restrictions de liaison et d'origine, Authentification de poignée de main WebSocket, Documentation destinée aux opérateurs, Interface utilisateur de contrôle de navigateur, Confiance du client distant                          |
| [Contrôle d'accès aux canaux](channel-identity-allowlists-and-sender-pairing.md)             | ✅  | `Beta (78%)`   | `Alpha (66%)` | `Beta (78%)`   | Identité de canal, Listes blanches, Appairage d'expéditeur                                                                                                                                                                                            |
| [Appairage d'appareil et de nœud](device-identity-and-operator-pairing.md)                      | ✅  | `Stable (83%)` | `Alpha (66%)` | `Stable (83%)` | Codes de configuration, Création d'identité d'appareil, Émission de jeton d'appareil, Approbations d'appairage d'appareil pour l'opérateur, Portées d'opérateur qui contrôlent l'appairage, Interface utilisateur de contrôle local, Migration d'authentification, Documentation destinée aux opérateurs, Appairage de nœud, Confiance de capacité, Approbations d'exécution à distance |
| [Confiance des plugins](plugin-installation-trust-and-security-boundaries.md)                    | ❌  | `Beta (76%)`   | `Beta (70%)`  | `Beta (76%)`   | Confiance d'installation de plugin, Limites de sécurité                                                                                                                                                                                               |
| [Hygiène des identifiants et secrets](secrets-storage-redaction-and-configuration-hygiene.md) | ✅  | `Beta (78%)`   | `Alpha (62%)` | `Beta (78%)`   | Profils d'authentification de fournisseur, Santé des clés API, Stockage des secrets, Rédaction, Hygiène de configuration                                                                                                                             |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de Couverture uniquement ; elles
  ne relèvent ni n'abaissent la Qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface prévues. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Politique d'approbation et protections des outils

Ancres de recherche : politique d'approbation, protections des outils dangereux, approbations exec.

Note de catégorie : [Politique d'approbation et protections des outils dangereux](approval-policy-and-dangerous-tool-safeguards.md)

Décisions de score :

- Couverture : `Stable (86%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (86%)`
- LTS : ✅

Fonctionnalités :

- Politique d'approbation : Couvre la politique d'approbation dans la politique d'approbation exec, les magasins d'approbation locaux à l'hôte, les modes liste blanche et demande, les protections des outils dangereux, le routage d'approbation natif/chat, le routage d'approbation des plugins, les décisions d'approbation, la liaison d'approbation et la gestion CLI côté opérateur.
- Protections des outils dangereux : Couvre les protections des outils dangereux dans la politique d'approbation exec, les magasins d'approbation locaux à l'hôte, les modes liste blanche et demande, les protections des outils dangereux, le routage d'approbation natif/chat, le routage d'approbation des plugins, les décisions d'approbation, la liaison d'approbation et la gestion CLI côté opérateur.

Docs principaux :

- `docs/tools/exec-approvals.md`
- `docs/cli/approvals.md`
- `docs/plugins/plugin-permission-requests.md`
- `docs/gateway/security/audit-checks.md`

### 2. Authentification de la passerelle et accès à distance

Ancres de recherche : gateway.auth.mode, authentification proxy de confiance, Tailscale Serve/Funnel, authentification de la poignée de main WebSocket, authentification de l'interface de contrôle, confiance du client distant, origines autorisées.

Note de catégorie : [Authentification de la passerelle et exposition réseau](gateway-auth-and-network-exposure.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Alpha (68%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Authentification par jeton/mot de passe partagé de la passerelle : Authentification par jeton et mot de passe pour les clients HTTP et WebSocket de la passerelle, y compris la résolution d'authentification à l'exécution, la validation au démarrage, la comparaison de secret partagé et les conseils aux opérateurs.
- Mode d'authentification de la passerelle : Sélection du mode d'authentification de la passerelle, y compris le comportement d'ingestion privée et les avertissements des opérateurs pour l'exposition non sécurisée.
- Identité proxy de confiance : Identité proxy de confiance, gateway.trustedProxies, trustedProxy.userHeader, requiredHeaders, allowUsers, allowLoopback, validation de la source du proxy inverse et comportement de portée
- Tailscale Serve/Funnel : Tailscale Serve/Funnel et règles d'exposition du proxy inverse, y compris les en-têtes d'identité Tailscale, tailscale whois, exigences de mot de passe Funnel et séparation entre l'identité de l'interface de contrôle/WS et l'authentification de l'API HTTP
- Restrictions de liaison et d'origine : modes de liaison loopback/LAN/tailnet/personnalisé, vérifications d'exposition non-loopback, vérifications d'origine du navigateur, controlUi.allowedOrigins, risque de secours d'en-tête Host et gestion des en-têtes transférés
- Authentification de la poignée de main WebSocket : Authentification de la poignée de main WebSocket, y compris l'ordre challenge/connect, l'authentification d'appareil liée à nonce, l'authentification partagée, les vérifications d'origine du navigateur, les limites de pré-authentification, le délai d'expiration du socket non authentifié et la rotation d'authentification partagée obsolète
- Docs côté opérateur : Docs et runbooks côté opérateur pour l'audit de sécurité, l'accès à distance, la restauration d'exposition, Tailscale, proxy de confiance, rotation des identifiants et sondage explicite des identifiants
- Interface de contrôle du navigateur : Couvre l'interface de contrôle du navigateur dans la confiance du navigateur de l'interface de contrôle/WebChat, l'appairage d'appareil pour les clients du navigateur, les origines autorisées, le comportement de Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface de contrôle du navigateur et de la confiance du client distant.
- Confiance du client distant : Couvre la confiance du client distant dans la confiance du navigateur de l'interface de contrôle/WebChat, l'appairage d'appareil pour les clients du navigateur, les origines autorisées, le comportement de Tailscale/proxy de confiance pour les sessions du navigateur et le comportement connexe de l'interface de contrôle du navigateur et de la confiance du client distant.

Docs principaux :

- `docs/gateway/security/index.md`
- `docs/gateway/security/exposure-runbook.md`
- `docs/gateway/trusted-proxy-auth.md`
- `docs/gateway/tailscale.md`
- `docs/gateway/remote.md`
- `docs/gateway/configuration-reference.md`
- `docs/cli/gateway.md`
- `docs/cli/doctor.md`
- `docs/web/control-ui.md`
- `docs/tools/browser-control.md`
- `docs/gateway/security/audit-checks.md`

### 3. Contrôle d'accès aux canaux

Ancres de recherche : appairage DM, allowFrom, listes blanches d'expéditeurs.

Note de catégorie : [Contrôle d'accès aux canaux](channel-identity-allowlists-and-sender-pairing.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Identité du canal : Couvre l'identité du canal dans qui peut parler à OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et comportement connexe d'identité du canal, listes blanches et appairage d'expéditeur.
- Listes blanches : Couvre les listes blanches dans qui peut parler à OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et comportement connexe d'identité du canal, listes blanches et appairage d'expéditeur.
- Appairage d'expéditeur : Couvre l'appairage d'expéditeur dans qui peut parler à OpenClaw via les canaux de messages : codes d'appairage DM, magasins d'appairage, `dmPolicy`, `allowFrom` et comportement connexe d'identité du canal, listes blanches et appairage d'expéditeur.

Docs principaux :

- `docs/channels/pairing.md`
- `docs/channels/telegram.md`
- `docs/channels/access-groups.md`
- `docs/gateway/security/audit-checks.md`

### 4. Appairage d'appareil et de nœud

Ancres de recherche : codes de configuration, signature de défi d'appareil, portées d'opérateur, appairage de nœud, capacités déclarées par nœud, approbations exec à distance.

Note de catégorie : [Identité d'appareil et appairage d'opérateur](device-identity-and-operator-pairing.md)

Décisions de score :

- Couverture : `Stable (83%)`
- Qualité : `Alpha (66%)`
- Complétude : `Stable (83%)`
- LTS : ✅

Fonctionnalités :

- Codes de configuration : Codes de configuration et UX d'appairage QR pour l'intégration mobile/nœud via le plugin device-pair
- Création d'identité d'appareil : Création d'identité d'appareil, stockage, IDs d'appareil dérivés de clé publique, signature de défi et vérification du serveur
- Émission de jeton d'appareil : Émission de jeton d'appareil, réutilisation de reconnexion, récupération de non-concordance de jeton, rotation de jeton, révocation de jeton et nettoyage de jeton obsolète
- Approbations d'appairage d'appareil pour l'opérateur : Approbations d'appairage d'appareil pour les rôles d'opérateur et de nœud, y compris les demandes en attente, les mises à niveau de rôle/portée et les demandes de réparation
- Portées d'opérateur qui contrôlent l'appairage : Portées d'opérateur qui contrôlent l'appairage, la gestion des jetons d'appareil, l'appairage de nœud et les approbations de rôle/portée à risque plus élevé
- Interface de contrôle locale : Interface de contrôle locale, WebChat, proxy de confiance et comportement d'appairage automatique du backend ou d'exception sans appareil où cela affecte l'appairage d'opérateur
- Migration d'authentification : Migration d'authentification et erreurs de récupération pour la signature d'appareil pré-défi, la dérive de jeton, la non-concordance de portée et la configuration d'authentification de passerelle mixte
- Docs côté opérateur : Docs côté opérateur pour les appareils, l'appairage, WebChat, l'interface de contrôle, l'authentification du protocole et le dépannage
- Appairage de nœud : Couvre l'appairage de nœud dans l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par nœud et le comportement connexe d'appairage de nœud, de confiance de capacité et d'approbations exec à distance.
- Confiance de capacité : Couvre la confiance de capacité dans l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par nœud et le comportement connexe d'appairage de nœud, de confiance de capacité et d'approbations exec à distance.
- Approbations exec à distance : Couvre les approbations exec à distance dans l'appairage de nœud/appareil pour les hôtes de capacité, l'état de nœud en attente et approuvé, l'approbation automatique CIDR de confiance, les limites de confiance de commande/capacité déclarées par nœud et le comportement connexe d'appairage de nœud, de confiance de capacité et d'approbations exec à distance.

Docs principaux :

- `docs/gateway/protocol.md`
- `docs/cli/devices.md`
- `docs/channels/pairing.md`
- `docs/gateway/pairing.md`
- `docs/gateway/operator-scopes.md`
- `docs/web/control-ui.md`
- `docs/web/webchat.md`
- `docs/cli/approvals.md`

### 5. Confiance des plugins

Ancres de recherche : confiance du manifeste du plugin, analyses de sécurité d'installation de plugin, listes blanches de plugins.

Note de catégorie : [Confiance des plugins](plugin-installation-trust-and-security-boundaries.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Confiance d'installation de plugin : Couvre la confiance d'installation de plugin dans la confiance du manifeste du plugin, les analyses de sécurité d'installation/mise à jour de plugin, les listes blanches de plugins, les métadonnées d'authentification/secret détenues par le manifeste et le comportement connexe de confiance d'installation de plugin et de limites de sécurité.
- Limites de sécurité : Couvre les limites de sécurité dans la confiance du manifeste du plugin, les analyses de sécurité d'installation/mise à jour de plugin, les listes blanches de plugins, les métadonnées d'authentification/secret détenues par le manifeste et le comportement connexe de confiance d'installation de plugin et de limites de sécurité.

Docs principaux :

- `docs/plugins/manifest.md`
- `docs/plugins/plugin-permission-requests.md`
- `docs/plugins/manage-plugins.md`
- `docs/gateway/security/audit-checks.md`

### 6. Hygiène des identifiants et des secrets

Ancres de recherche : auth-profiles.json, clés API du fournisseur, profils OAuth, SecretRef, snapshots de secrets à l'exécution, modèles de rédaction.

Note de catégorie : [Stockage des secrets, rédaction et hygiène de configuration](secrets-storage-redaction-and-configuration-hygiene.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (62%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Profils d'authentification du fournisseur : Couvre les profils d'authentification du fournisseur dans les identifiants du fournisseur et la santé d'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportement connexe des profils d'authentification du fournisseur et de la santé des clés API.
- Santé des clés API : Couvre la santé des clés API dans les identifiants du fournisseur et la santé d'authentification en tant que surface de sécurité/secrets : clés API, profils OAuth, `auth-profiles.json`, ordre d'authentification et comportement connexe des profils d'authentification du fournisseur et de la santé des clés API.
- Stockage des secrets : Couvre le stockage des secrets dans le contrat SecretRef et les fournisseurs, les snapshots de secrets à l'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré et le comportement connexe de stockage des secrets, de rédaction et d'hygiène de configuration.
- Rédaction : Couvre la rédaction dans le contrat SecretRef et les fournisseurs, les snapshots de secrets à l'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré et le comportement connexe de stockage des secrets, de rédaction et d'hygiène de configuration.
- Hygiène de configuration : Couvre l'hygiène de configuration dans le contrat SecretRef et les fournisseurs, les snapshots de secrets à l'exécution, les SecretRefs d'authentification de passerelle, les résidus de profil d'authentification et de modèle généré et le comportement connexe de stockage des secrets, de rédaction et d'hygiène de configuration.

Docs principaux :

- `docs/gateway/authentication.md`
- `docs/cli/models.md`
- `docs/providers/openai.md`
- `docs/concepts/oauth.md`
- `docs/gateway/secrets.md`
- `docs/cli/secrets.md`
- `docs/reference/secretref-credential-surface.md`
- `docs/gateway/security/audit-checks.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, les docs et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/security-auth-pairing-and-secrets/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/security-auth-pairing-and-secrets`.
