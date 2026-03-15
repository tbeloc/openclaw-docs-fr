---
summary: "Déployer OpenClaw Gateway sur un cluster Kubernetes avec Kustomize"
read_when:
  - You want to run OpenClaw on a Kubernetes cluster
  - You want to test OpenClaw in a Kubernetes environment
title: "Kubernetes"
---

# OpenClaw sur Kubernetes

Un point de départ minimal pour exécuter OpenClaw sur Kubernetes — pas un déploiement prêt pour la production. Il couvre les ressources essentielles et est destiné à être adapté à votre environnement.

## Pourquoi pas Helm ?

OpenClaw est un conteneur unique avec quelques fichiers de configuration. La personnalisation intéressante se trouve dans le contenu des agents (fichiers markdown, compétences, surcharges de configuration), pas dans la création de modèles d'infrastructure. Kustomize gère les superpositions sans la surcharge d'un graphique Helm. Si votre déploiement devient plus complexe, un graphique Helm peut être ajouté en couche au-dessus de ces manifestes.

## Ce dont vous avez besoin

- Un cluster Kubernetes en cours d'exécution (AKS, EKS, GKE, k3s, kind, OpenShift, etc.)
- `kubectl` connecté à votre cluster
- Une clé API pour au moins un fournisseur de modèle

## Démarrage rapide

```bash
# Remplacez par votre fournisseur : ANTHROPIC, GEMINI, OPENAI, ou OPENROUTER
export <PROVIDER>_API_KEY="..."
./scripts/k8s/deploy.sh

kubectl port-forward svc/openclaw 18789:18789 -n openclaw
open http://localhost:18789
```

Récupérez le jeton de passerelle et collez-le dans l'interface utilisateur de contrôle :

```bash
kubectl get secret openclaw-secrets -n openclaw -o jsonpath='{.data.OPENCLAW_GATEWAY_TOKEN}' | base64 -d
```

Pour le débogage local, `./scripts/k8s/deploy.sh --show-token` affiche le jeton après le déploiement.

## Test local avec Kind

Si vous n'avez pas de cluster, créez-en un localement avec [Kind](https://kind.sigs.k8s.io/) :

```bash
./scripts/k8s/create-kind.sh           # détection automatique de docker ou podman
./scripts/k8s/create-kind.sh --delete  # démonter
```

Puis déployez comme d'habitude avec `./scripts/k8s/deploy.sh`.

## Étape par étape

### 1) Déployer

**Option A** — Clé API dans l'environnement (une étape) :

```bash
# Remplacez par votre fournisseur : ANTHROPIC, GEMINI, OPENAI, ou OPENROUTER
export <PROVIDER>_API_KEY="..."
./scripts/k8s/deploy.sh
```

Le script crée un Secret Kubernetes avec la clé API et un jeton de passerelle généré automatiquement, puis déploie. Si le Secret existe déjà, il préserve le jeton de passerelle actuel et toutes les clés de fournisseur qui ne sont pas modifiées.

**Option B** — créer le secret séparément :

```bash
export <PROVIDER>_API_KEY="..."
./scripts/k8s/deploy.sh --create-secret
./scripts/k8s/deploy.sh
```

Utilisez `--show-token` avec l'une ou l'autre commande si vous souhaitez que le jeton soit imprimé sur stdout pour les tests locaux.

### 2) Accéder à la passerelle

```bash
kubectl port-forward svc/openclaw 18789:18789 -n openclaw
open http://localhost:18789
```

## Ce qui est déployé

```
Namespace: openclaw (configurable via OPENCLAW_NAMESPACE)
├── Deployment/openclaw        # Pod unique, conteneur init + passerelle
├── Service/openclaw           # ClusterIP sur le port 18789
├── PersistentVolumeClaim      # 10Gi pour l'état et la configuration de l'agent
├── ConfigMap/openclaw-config  # openclaw.json + AGENTS.md
└── Secret/openclaw-secrets    # Jeton de passerelle + clés API
```

## Personnalisation

### Instructions des agents

Modifiez le `AGENTS.md` dans `scripts/k8s/manifests/configmap.yaml` et redéployez :

```bash
./scripts/k8s/deploy.sh
```

### Configuration de la passerelle

Modifiez `openclaw.json` dans `scripts/k8s/manifests/configmap.yaml`. Voir [Configuration de la passerelle](/gateway/configuration) pour la référence complète.

### Ajouter des fournisseurs

Réexécutez avec des clés supplémentaires exportées :

```bash
export ANTHROPIC_API_KEY="..."
export OPENAI_API_KEY="..."
./scripts/k8s/deploy.sh --create-secret
./scripts/k8s/deploy.sh
```

Les clés de fournisseur existantes restent dans le Secret sauf si vous les remplacez.

Ou corrigez le Secret directement :

```bash
kubectl patch secret openclaw-secrets -n openclaw \
  -p '{"stringData":{"<PROVIDER>_API_KEY":"..."}}'
kubectl rollout restart deployment/openclaw -n openclaw
```

### Espace de noms personnalisé

```bash
OPENCLAW_NAMESPACE=my-namespace ./scripts/k8s/deploy.sh
```

### Image personnalisée

Modifiez le champ `image` dans `scripts/k8s/manifests/deployment.yaml` :

```yaml
image: ghcr.io/openclaw/openclaw:2026.3.1
```

### Exposer au-delà de port-forward

Les manifestes par défaut lient la passerelle à la boucle locale à l'intérieur du pod. Cela fonctionne avec `kubectl port-forward`, mais ne fonctionne pas avec un `Service` Kubernetes ou un chemin Ingress qui doit atteindre l'IP du pod.

Si vous souhaitez exposer la passerelle via un Ingress ou un équilibreur de charge :

- Modifiez la liaison de la passerelle dans `scripts/k8s/manifests/configmap.yaml` de `loopback` à une liaison non-loopback qui correspond à votre modèle de déploiement
- Gardez l'authentification de la passerelle activée et utilisez un point d'entrée approprié avec terminaison TLS
- Configurez l'interface utilisateur de contrôle pour l'accès à distance en utilisant le modèle de sécurité Web pris en charge (par exemple HTTPS/Tailscale Serve et origines autorisées explicites si nécessaire)

## Redéployer

```bash
./scripts/k8s/deploy.sh
```

Cela applique tous les manifestes et redémarre le pod pour récupérer les modifications de configuration ou de secret.

## Démantèlement

```bash
./scripts/k8s/deploy.sh --delete
```

Cela supprime l'espace de noms et toutes les ressources qu'il contient, y compris le PVC.

## Notes d'architecture

- La passerelle se lie à la boucle locale à l'intérieur du pod par défaut, donc la configuration incluse est pour `kubectl port-forward`
- Aucune ressource au niveau du cluster — tout se trouve dans un seul espace de noms
- Sécurité : `readOnlyRootFilesystem`, capacités `drop: ALL`, utilisateur non-root (UID 1000)
- La configuration par défaut garde l'interface utilisateur de contrôle sur le chemin d'accès local plus sûr : liaison loopback plus `kubectl port-forward` vers `http://127.0.0.1:18789`
- Si vous allez au-delà de l'accès localhost, utilisez le modèle distant pris en charge : HTTPS/Tailscale plus la liaison de passerelle appropriée et les paramètres d'origine de l'interface utilisateur de contrôle
- Les secrets sont générés dans un répertoire temporaire et appliqués directement au cluster — aucun matériel secret n'est écrit dans le checkout du référentiel

## Structure des fichiers

```
scripts/k8s/
├── deploy.sh                   # Crée l'espace de noms + secret, déploie via kustomize
├── create-kind.sh              # Cluster Kind local (détection automatique de docker/podman)
└── manifests/
    ├── kustomization.yaml      # Base Kustomize
    ├── configmap.yaml          # openclaw.json + AGENTS.md
    ├── deployment.yaml         # Spécification de pod avec renforcement de la sécurité
    ├── pvc.yaml                # Stockage persistant 10Gi
    └── service.yaml            # ClusterIP sur 18789
```
