# Artefacts de documentation générée

Ces artefacts de base sont générés à partir du schéma de configuration OpenClaw appartenant au référentiel et des métadonnées de canal/plugin groupées.

- Ne modifiez pas `config-baseline.json` à la main.
- Ne modifiez pas `config-baseline.jsonl` à la main.
- Régénérez-le avec `pnpm config:docs:gen`.
- Validez-le dans CI ou localement avec `pnpm config:docs:check`.
