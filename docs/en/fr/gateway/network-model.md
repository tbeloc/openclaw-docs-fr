---
summary: "Comment la Gateway, les nœuds et l'hôte canvas se connectent."
read_when:
  - Vous voulez une vue concise du modèle de réseau Gateway
title: "Modèle de réseau"
---

La plupart des opérations transitent par la Gateway (`openclaw gateway`), un processus unique et long terme qui possède les connexions de canal et le plan de contrôle WebSocket.

## Règles fondamentales

- Une Gateway par hôte est recommandée. C'est le seul processus autorisé à posséder la session WhatsApp Web. Pour les bots de secours ou l'isolation stricte, exécutez plusieurs gateways avec des profils et des ports isolés. Voir [Plusieurs gateways](/fr/gateway/multiple-gateways).
- Loopback en premier : la WS Gateway par défaut est `ws://127.0.0.1:18789`. L'assistant génère un jeton de gateway par défaut, même pour loopback. Pour l'accès tailnet, exécutez `openclaw gateway --bind tailnet --token ...` car les jetons sont requis pour les liaisons non-loopback.
- Les nœuds se connectent à la WS Gateway via LAN, tailnet ou SSH selon les besoins. Le pont TCP hérité est obsolète.
- L'hôte canvas est servi par le serveur HTTP Gateway sur le **même port** que la Gateway (par défaut `18789`) :
  - `/__openclaw__/canvas/`
  - `/__openclaw__/a2ui/`
    Quand `gateway.auth` est configuré et que la Gateway se lie au-delà de loopback, ces routes sont protégées par l'authentification Gateway. Les clients nœuds utilisent des URL de capacité limitées au nœud liées à leur session WS active. Voir [Configuration Gateway](/fr/gateway/configuration) (`canvasHost`, `gateway`).
- L'utilisation à distance se fait généralement via tunnel SSH ou VPN tailnet. Voir [Accès distant](/fr/gateway/remote) et [Découverte](/fr/gateway/discovery).
