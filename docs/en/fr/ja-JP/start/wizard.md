---
read_when:
  - オンボーディングウィザードの実行または設定時
  - 新しいマシンのセットアップ時
sidebarTitle: Wizard (CLI)
summary: CLIオンボーディングウィザード：Gateway、ワークスペース、チャンネル、Skillsの対話式セットアップ
title: オンボーディングウィザード（CLI）
x-i18n:
  generated_at: "2026-02-08T17:15:18Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 9a650d46044a930aa4aaec30b35f1273ca3969bf676ab67bf4e1575b5c46db4c
  source_path: start/wizard.md
  workflow: 15
---

# Assistant d'intégration (CLI)

L'assistant d'intégration CLI est le chemin recommandé pour configurer OpenClaw sur macOS, Linux et Windows (via WSL2). En plus d'une connexion Gateway locale ou distante, il configure les paramètres par défaut de l'espace de travail, les canaux et les Skills.

```bash
openclaw onboard
```

<Info>
Le moyen le plus rapide de commencer votre premier chat : ouvrez l'interface de contrôle (aucune configuration de canal requise). Exécutez `openclaw dashboard` pour discuter dans votre navigateur. Documentation : [Dashboard](/web/dashboard).
</Info>

## Démarrage rapide vs Configuration avancée

L'assistant vous permet de choisir entre **Démarrage rapide** (paramètres par défaut) et **Configuration avancée** (contrôle complet).

<Tabs>
  <Tab title="Démarrage rapide (paramètres par défaut)">
    - Gateway local sur loopback
    - Espace de travail existant ou espace de travail par défaut
    - Port Gateway `18789`
    - Jeton d'authentification Gateway généré automatiquement (généré même sur loopback)
    - Publication Tailscale désactivée
    - Messages directs Telegram et WhatsApp autorisés par défaut (vous pourrez être invité à entrer des numéros de téléphone)
  </Tab>
  <Tab title="Configuration avancée (contrôle complet)">
    - Affiche le flux de questions complet pour le mode, l'espace de travail, la Gateway, les canaux, le démon et les Skills
  </Tab>
</Tabs>

## Détails de l'intégration CLI

<Columns>
  <Card title="Référence CLI" href="/start/wizard-cli-reference">
    Description complète des flux locaux et distants, authentification et matrice de modèles, sortie de configuration, RPC de l'assistant, comportement de signal-cli.
  </Card>
  <Card title="Automatisation et scripts" href="/start/wizard-cli-automation">
    Recettes pour l'intégration non-interactive et exemples d'`agents add` automatisé.
  </Card>
</Columns>

## Commandes de suivi courantes

```bash
openclaw configure
openclaw agents add <name>
```

<Note>
`--json` ne signifie pas le mode non-interactif. Utilisez `--non-interactive` dans les scripts.
</Note>

<Tip>
Recommandé : configurez une clé API Brave Search pour que vos agents puissent utiliser `web_search` (`web_fetch` fonctionne sans clé). Le moyen le plus simple : exécutez `openclaw configure --section web` pour enregistrer `tools.web.search.apiKey`. Documentation : [Outils Web](/tools/web).
</Tip>

## Documentation connexe

- Référence des commandes CLI : [`openclaw onboard`](/cli/onboard)
- Intégration de l'application macOS : [Intégration](/start/onboarding)
- Procédure de premier lancement d'agent : [Amorçage d'agent](/start/bootstrapping)
