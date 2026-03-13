---
read_when:
  - ゼロからの初回セットアップ
  - 動作するチャットへの最短ルートを知りたい
summary: OpenClawをインストールし、数分で最初のチャットを実行しましょう。
title: はじめに
x-i18n:
  generated_at: "2026-02-08T17:15:16Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 27aeeb3d18c495380e94e6b011b0df3def518535c9f1eee504f04871d8a32269
  source_path: start/getting-started.md
  workflow: 15
---

# Démarrage

Objectif : réaliser votre premier chat fonctionnel à partir de zéro avec une configuration minimale.

<Info>
Méthode de chat la plus rapide : ouvrez l'interface de contrôle (aucune configuration de canal requise). Exécutez `openclaw dashboard` pour discuter dans votre navigateur, ou ouvrez `http://127.0.0.1:18789/` sur le <Tooltip headline="Hôte Gateway" tip="Machine exécutant le service OpenClaw Gateway.">hôte Gateway</Tooltip>.
Documentation : [Dashboard](/web/dashboard) et [Interface de contrôle](/web/control-ui).
</Info>

## Prérequis

- Node 22 ou ultérieur

<Tip>
Si vous n'êtes pas sûr, vérifiez votre version de Node avec `node --version`.
</Tip>

## Configuration rapide (CLI)

<Steps>
  <Step title="Installer OpenClaw (recommandé)">
    <Tabs>
      <Tab title="macOS/Linux">
        ```bash
        curl -fsSL https://openclaw.ai/install.sh | bash
        ```
      </Tab>
      <Tab title="Windows (PowerShell)">
        ```powershell
        iwr -useb https://openclaw.ai/install.ps1 | iex
        ```
      </Tab>
    </Tabs>

    <Note>
    Autres méthodes d'installation et exigences : [Installation](/install).
    </Note>

  </Step>
  <Step title="Exécuter l'assistant d'intégration">
    ```bash
    openclaw onboard --install-daemon
    ```

    L'assistant configurera l'authentification, les paramètres de Gateway et les canaux optionnels.
    Voir [Assistant d'intégration](/start/wizard) pour plus de détails.

  </Step>
  <Step title="Vérifier Gateway">
    Si vous avez installé le service, il devrait déjà être en cours d'exécution :

    ```bash
    openclaw gateway status
    ```

  </Step>
  <Step title="Ouvrir l'interface de contrôle">
    ```bash
    openclaw dashboard
    ```
  </Step>
</Steps>

<Check>
Si l'interface de contrôle se charge, Gateway est prêt à être utilisé.
</Check>

## Vérification optionnelle et fonctionnalités supplémentaires

<AccordionGroup>
  <Accordion title="Exécuter Gateway au premier plan">
    Utile pour les tests rapides ou le dépannage.

    ```bash
    openclaw gateway --port 18789
    ```

  </Accordion>
  <Accordion title="Envoyer un message de test">
    Nécessite un canal configuré.

    ```bash
    openclaw message send --target +15555550123 --message "Hello from OpenClaw"
    ```

  </Accordion>
</AccordionGroup>

## En savoir plus

<Columns>
  <Card title="Assistant d'intégration (détails)" href="/start/wizard">
    Référence complète de l'assistant CLI et options avancées.
  </Card>
  <Card title="Intégration de l'application macOS" href="/start/onboarding">
    Flux de première exécution de l'application macOS.
  </Card>
</Columns>

## État après la fin

- Gateway en cours d'exécution
- Authentification configurée
- Accès à l'interface de contrôle ou canaux connectés

## Prochaines étapes

- Sécurité et approbation des messages directs : [Appairage](/channels/pairing)
- Connecter plus de canaux : [Canaux](/channels)
- Workflows avancés et construction à partir de la source : [Configuration](/start/setup)
