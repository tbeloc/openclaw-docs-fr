---
title: "Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité sur la sécurité réseau et les contrôles d'invite"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs de modèles locaux : Ollama, vLLM, SGLang, LM Studio - Note de maturité sur la sécurité réseau et les contrôles d'invite

## Résumé

La surface des fournisseurs locaux dispose de garde-fous solides autour de la confiance réseau auto-hébergée, de l'accès exact aux points de terminaison locaux, de la suppression des jetons spéciaux et des invites qui réduisent la pression sur les modèles locaux plus petits. L'implémentation refuse l'ajout à la liste blanche des hôtes de métadonnées dangereuses, limite la confiance du réseau privé aux origines configurées et documente les limites de la force du modèle. Le risque restant provient de la variabilité inhérente de la qualité des modèles locaux et de l'exposition du réseau privé contrôlée par l'opérateur.

## Portée de la catégorie

Inclus dans cette catégorie :

- Sécurité réseau : couvre la sécurité réseau sur le réseau privé et la confiance d'origine exacte pour les URL de base des fournisseurs locaux, les protections SSRF pour la configuration auto-hébergée, l'assainissement des jetons spéciaux, le comportement d'invite allégé du modèle local et les comportements connexes de contrôle de la sécurité réseau et de la pression d'invite.
- Contrôles de pression d'invite : couvre les contrôles de pression d'invite sur le réseau privé et la confiance d'origine exacte pour les URL de base des fournisseurs locaux, les protections SSRF pour la configuration auto-hébergée, l'assainissement des jetons spéciaux, le comportement d'invite allégé du modèle local et les comportements connexes de contrôle de la sécurité réseau et de la pression d'invite.

## Fonctionnalités

- Sécurité réseau : couvre la sécurité réseau sur le réseau privé et la confiance d'origine exacte pour les URL de base des fournisseurs locaux, les protections SSRF pour la configuration auto-hébergée, l'assainissement des jetons spéciaux, le comportement d'invite allégé du modèle local et les comportements connexes de contrôle de la sécurité réseau et de la pression d'invite.
- Contrôles de pression d'invite : couvre les contrôles de pression d'invite sur le réseau privé et la confiance d'origine exacte pour les URL de base des fournisseurs locaux, les protections SSRF pour la configuration auto-hébergée, l'assainissement des jetons spéciaux, le comportement d'invite allégé du modèle local et les comportements connexes de contrôle de la sécurité réseau et de la pression d'invite.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs :
  - `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md:632`
    jusqu'à la ligne 642 documentent l'assainissement des jetons spéciaux du contenu externe.
  - `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md:691`
    jusqu'à la ligne 704 documentent l'exposition du backend LLM auto-hébergé et les compromis de confiance.
  - `/Users/kevinlin/code/openclaw/src/plugins/provider-self-hosted-setup.ts:60`
    jusqu'à la ligne 76 implémentent la politique SSRF auto-hébergée.
  - `/Users/kevinlin/code/openclaw/src/agents/provider-transport-fetch.ts:560`
    jusqu'à la ligne 570 font confiance aux URL de base personnalisées ou locales exactement configurées.
  - `/Users/kevinlin/code/openclaw/src/agents/local-model-lean.ts:6` jusqu'à
    la ligne 50 fournissent les contrôles de pression d'invite du modèle local.
- Signaux négatifs :
  - Ces contrôles réduisent le risque, mais la force du modèle local, l'adhérence à l'invite et l'exposition du réseau privé dépendent toujours de l'opérateur et du modèle.
  - La documentation destinée aux utilisateurs explique le risque mais ne fournit pas une seule évaluation de disponibilité pour une « configuration de fournisseur local suffisamment sûre ».
- Lacunes d'intégration :
  - Ajouter un test de sécurité du fournisseur local qui tente l'ajout à la liste blanche de l'hôte de métadonnées, l'inadéquation d'origine exacte du réseau privé, l'injection de jetons spéciaux et un chemin de pression d'invite de modèle plus petit.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl :
  - La requête `self-hosted local model special tokens allowPrivateNetwork` a retourné la PR #73817, pertinente pour les contrôles de jetons spéciaux et de réseau privé pour le trafic de modèle local auto-hébergé.
- Rapports Discrawl :
  - La requête `LM Studio local provider` a retourné une discussion du responsable sur la PR de brouillon #80751 pour la confiance d'origine exacte SSRF et les appels de modèle local à LM Studio, Ollama, vLLM et llama-server.
- Bonnes qualités :
  - La règle d'origine exacte est un signal de qualité fort : les points de terminaison locaux/privés configurés peuvent fonctionner sans faire confiance largement à des URL de réseau privé arbitraires.
  - La configuration auto-hébergée refuse l'ajout à la liste blanche de l'hôte du service de métadonnées, et les jetons spéciaux sont supprimés du contenu externe avant les invites du modèle.
  - Le code dispose d'une couche allégée de modèle local spécifique au lieu de s'appuyer uniquement sur des invites génériques pour les backends locaux plus petits.
- Mauvaises qualités :
  - La sécurité du modèle local reste inégale car le modèle lui-même peut ignorer les instructions, halluciner des outils ou être déployé derrière un point de terminaison local non sécurisé.
  - Certains contrôles de risque ne sont découvrables qu'après la lecture des pages de sécurité et de configuration plutôt que par des avertissements au moment de la configuration.
- Exclus de la qualité :
  - La couverture des tests et la présence de tests de sécurité n'ont pas été utilisées comme entrées de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/local-model-providers-ollama-vllm-sglang-lm-studio.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour la sécurité réseau et les contrôles de pression d'invite.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- La configuration ne semble pas produire un avertissement consolidé qui résume la confiance du point de terminaison, la force du modèle, la pression d'invite et la gestion des jetons spéciaux pour le fournisseur local sélectionné.
- L'exposition du réseau privé contrôlée par l'opérateur reste un risque résiduel même avec la confiance d'origine exacte.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md:632`
  documente l'assainissement des jetons spéciaux pour le contenu externe.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md:691`
  documente les risques du backend LLM auto-hébergé.
- `/Users/kevinlin/code/openclaw/docs/gateway/security/index.md:706`
  documente les attentes de force du modèle.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:450` documente
  la confiance d'origine exacte.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-tools.md:527` documente
  `allowPrivateNetwork`.
- `/Users/kevinlin/code/openclaw/docs/gateway/local-models.md:324` documente
  le dépannage et les conseils de sécurité des modèles locaux.

### Source

- `/Users/kevinlin/code/openclaw/src/plugins/provider-self-hosted-setup.ts:60`
  implémente la politique SSRF pour la configuration auto-hébergée.
- `/Users/kevinlin/code/openclaw/src/agents/provider-transport-fetch.ts:560`
  limite la confiance du réseau privé aux origines exactement configurées.
- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-utils.ts:18`
  exporte les utilitaires de suppression des jetons spéciaux.
- `/Users/kevinlin/code/openclaw/src/agents/local-model-lean.ts:6` implémente
  le comportement d'invite allégé du modèle local.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/plugins/provider-self-hosted-setup.test.ts:373`
  vérifie que les hôtes du service de métadonnées ne sont pas autorisés pour la configuration auto-hébergée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/agents/embedded-agent-utils.strip-model-special-tokens.test.ts:7`
  couvre la suppression des jetons spéciaux du modèle.
- `/Users/kevinlin/code/openclaw/src/agents/local-model-lean.test.ts:10`
  couvre le comportement allégé du modèle local.
- `/Users/kevinlin/code/openclaw/src/agents/local-model-lean.test.ts:165`
  couvre le comportement d'invite allégé supplémentaire.

### Requêtes Gitcrawl

Requête : `gitcrawl search openclaw/openclaw --query "self-hosted local model special tokens allowPrivateNetwork" --json --limit 5`

Résultats :

- A retourné la PR #73817, pertinente pour le comportement des jetons spéciaux et du réseau privé du modèle local auto-hébergé.

### Requêtes Discrawl

Requête : `discrawl search --mode hybrid --limit 5 "LM Studio local provider"`

Résultats :

- A retourné une discussion du responsable sur la PR de brouillon #80751 pour la confiance d'origine exacte SSRF et les appels de modèle local à LM Studio, Ollama, vLLM et llama-server.
