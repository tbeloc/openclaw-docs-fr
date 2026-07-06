---
summary: "Configuration de l'API LongCat pour LongCat-2.0"
title: "LongCat"
read_when:
  - You want to use LongCat-2.0 with OpenClaw
  - You need the LongCat API key or model limits
---

[LongCat](https://longcat.ai) fournit une API hébergée pour LongCat-2.0, un
modèle de raisonnement conçu pour les charges de travail de codage et d'agents. OpenClaw fournit le
plugin officiel `longcat` pour le point de terminaison compatible OpenAI de LongCat.

| Propriété  | Valeur                             |
| ---------- | ---------------------------------- |
| Fournisseur| `longcat`                          |
| Auth       | `LONGCAT_API_KEY`                  |
| API        | Chat Completions compatible OpenAI |
| URL de base| `https://api.longcat.chat/openai`  |
| Modèle     | `longcat/LongCat-2.0`              |
| Contexte   | 1 048 576 tokens                   |
| Sortie max | 131 072 tokens                     |
| Entrée     | Texte                              |

## Installer le plugin

Installez le package officiel, puis redémarrez Gateway :

```bash
openclaw plugins install @openclaw/longcat-provider
openclaw gateway restart
```

## Commencer

<Steps>
  <Step title="Créer une clé API">
    Connectez-vous à la [Plateforme API LongCat](https://longcat.chat/platform/) et
    créez une clé sur la page [Clés API](https://longcat.chat/platform/api_keys).
  </Step>
  <Step title="Exécuter l'intégration">
    ```bash
    openclaw onboard --auth-choice longcat-api-key
    ```
  </Step>
  <Step title="Vérifier le modèle">
    ```bash
    openclaw models list --provider longcat
    ```
  </Step>
</Steps>

L'intégration ajoute le catalogue hébergé et sélectionne `longcat/LongCat-2.0` quand
aucun modèle principal n'est déjà configuré.

### Configuration non-interactive

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice longcat-api-key \
  --longcat-api-key "$LONGCAT_API_KEY"
```

## Comportement du raisonnement

LongCat expose un contrôle binaire de la réflexion. OpenClaw mappe les niveaux de réflexion activés
à `thinking: { type: "enabled" }` et `/think off` à
`thinking: { type: "disabled" }`. LongCat ne documente pas actuellement
`reasoning_effort`, donc OpenClaw ne l'envoie pas.

LongCat retourne le raisonnement dans `reasoning_content`. OpenClaw préserve ce champ
lors de la relecture des tours d'appels d'outils de l'assistant afin que les sessions d'agents multi-tours conservent
la forme de message attendue du fournisseur.

## Tarification

Le catalogue intégré utilise les tarifs de liste à l'usage de LongCat en USD par million
de tokens : 0,75 $ pour l'entrée non mise en cache, 0,015 $ pour l'entrée mise en cache, et 2,95 $ pour la sortie. LongCat peut
offrir des réductions temporaires ; la [page de tarification](https://longcat.chat/platform/docs/Pricing/LongCat-2.0.html)
et vos relevés de facturation font autorité.

## LongCat-2.0 auto-hébergé

Le fournisseur `longcat` cible l'API hébergée de LongCat. Pour les poids ouverts sur
[Hugging Face](https://huggingface.co/meituan-longcat/LongCat-2.0), servez le
modèle via un runtime compatible OpenAI et utilisez plutôt le
[vLLM](/fr/providers/vllm) ou le fournisseur [SGLang](/fr/providers/sglang) existant d'OpenClaw.

Conservez l'identifiant exact du modèle du runtime dans le catalogue du fournisseur auto-hébergé ;
ne routez pas un déploiement local via `longcat/LongCat-2.0`.

## Dépannage

<AccordionGroup>
  <Accordion title="La clé fonctionne dans un shell mais pas dans Gateway">
    Les processus Gateway gérés par daemon n'héritent pas de toutes les variables de shell interactif.
    Mettez `LONGCAT_API_KEY` dans `~/.openclaw/.env`, configurez-le via
    l'intégration, ou utilisez une référence de secret approuvée.
  </Accordion>

  <Accordion title="Les requêtes échouent avec 402 ou 429">
    `402` signifie que le compte a un quota de tokens insuffisant. `429` signifie que la
    clé API a atteint une limite de débit. Vérifiez [l'utilisation de LongCat](https://longcat.chat/platform/usage)
    et réessayez les requêtes limitées après la fenêtre de backoff du fournisseur.
  </Accordion>

  <Accordion title="Le modèle n'apparaît pas">
    Exécutez `openclaw plugins list` et confirmez que le plugin `longcat` est
    activé, puis exécutez `openclaw models list --provider longcat`.
  </Accordion>
</AccordionGroup>

## Connexes

<CardGroup cols={2}>
  <Card title="Fournisseurs de modèles" href="/fr/concepts/model-providers" icon="layers">
    Configuration du fournisseur, références de modèles et comportement de basculement.
  </Card>
  <Card title="Documentation de l'API LongCat" href="https://longcat.chat/platform/docs/" icon="arrow-up-right-from-square">
    Points de terminaison API hébergés, authentification, limites et exemples.
  </Card>
  <Card title="Fiche du modèle LongCat-2.0" href="https://huggingface.co/meituan-longcat/LongCat-2.0" icon="arrow-up-right-from-square">
    Architecture, conseils de déploiement et détails du modèle.
  </Card>
  <Card title="Secrets" href="/fr/gateway/secrets" icon="key">
    Stockez les identifiants du fournisseur sans intégrer du texte brut dans la configuration.
  </Card>
</CardGroup>
