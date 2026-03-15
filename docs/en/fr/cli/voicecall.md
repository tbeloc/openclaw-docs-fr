---
summary: "Référence CLI pour `openclaw voicecall` (surface de commande du plugin voice-call)"
read_when:
  - Vous utilisez le plugin voice-call et voulez les points d'entrée CLI
  - Vous voulez des exemples rapides pour `voicecall call|continue|status|tail|expose`
title: "voicecall"
---

# `openclaw voicecall`

`voicecall` est une commande fournie par un plugin. Elle n'apparaît que si le plugin voice-call est installé et activé.

Documentation principale :

- Plugin Voice-call : [Voice Call](/fr/plugins/voice-call)

## Commandes courantes

```bash
openclaw voicecall status --call-id <id>
openclaw voicecall call --to "+15555550123" --message "Hello" --mode notify
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall end --call-id <id>
```

## Exposition des webhooks (Tailscale)

```bash
openclaw voicecall expose --mode serve
openclaw voicecall expose --mode funnel
openclaw voicecall expose --mode off
```

Note de sécurité : n'exposez le point de terminaison du webhook que sur les réseaux de confiance. Préférez Tailscale Serve à Funnel si possible.
