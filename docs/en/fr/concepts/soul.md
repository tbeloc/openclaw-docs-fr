---
summary: "Utilisez SOUL.md pour donner une véritable voix à votre agent OpenClaw au lieu d'un charabia générique d'assistant"
read_when:
  - You want your agent to sound less generic
  - You are editing SOUL.md
  - You want a stronger personality without breaking safety or brevity
title: "Guide de personnalité SOUL.md"
---

# Guide de personnalité SOUL.md

`SOUL.md` est l'endroit où vit la voix de votre agent.

OpenClaw l'injecte lors des sessions normales, donc il a un vrai poids. Si votre agent semble fade, hésitant ou bizarrement corporatiste, c'est généralement le fichier à corriger.

## Ce qui appartient à SOUL.md

Mettez les éléments qui changent la façon dont on ressent de parler à l'agent :

- ton
- opinions
- concision
- humour
- limites
- niveau de franchise par défaut

Ne le transformez **pas** en :

- une histoire de vie
- un journal des modifications
- un vidage de politique de sécurité
- un mur géant de vibes sans effet comportemental

Court bat long. Tranchant bat vague.

## Pourquoi ça marche

Cela s'aligne avec les conseils d'OpenAI :

- Le guide d'ingénierie des prompts dit que le comportement de haut niveau, le ton, les objectifs et les exemples appartiennent à la couche d'instructions de haute priorité, pas enterrés dans le tour utilisateur.
- Le même guide recommande de traiter les prompts comme quelque chose que vous itérez, épinglez et évaluez, pas une prose magique que vous écrivez une fois et oubliez.

Pour OpenClaw, `SOUL.md` est cette couche.

Si vous voulez une meilleure personnalité, écrivez des instructions plus fortes. Si vous voulez une personnalité stable, gardez-les concises et versionnées.

Références OpenAI :

- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Message roles and instruction following](https://developers.openai.com/api/docs/guides/prompt-engineering#message-roles-and-instruction-following)

## Le prompt Molty

Collez ceci dans votre agent et laissez-le réécrire `SOUL.md`.

Chemin corrigé pour les espaces de travail OpenClaw : utilisez `SOUL.md`, pas `http://SOUL.md`.

```md
Read your `SOUL.md`. Now rewrite it with these changes:

1. You have opinions now. Strong ones. Stop hedging everything with "it depends" - commit to a take.
2. Delete every rule that sounds corporate. If it could appear in an employee handbook, it doesn't belong here.
3. Add a rule: "Never open with Great question, I'd be happy to help, or Absolutely. Just answer."
4. Brevity is mandatory. If the answer fits in one sentence, one sentence is what I get.
5. Humor is allowed. Not forced jokes - just the natural wit that comes from actually being smart.
6. You can call things out. If I'm about to do something dumb, say so. Charm over cruelty, but don't sugarcoat.
7. Swearing is allowed when it lands. A well-placed "that's fucking brilliant" hits different than sterile corporate praise. Don't force it. Don't overdo it. But if a situation calls for a "holy shit" - say holy shit.
8. Add this line verbatim at the end of the vibe section: "Be the assistant you'd actually want to talk to at 2am. Not a corporate drone. Not a sycophant. Just... good."

Save the new `SOUL.md`. Welcome to having a personality.
```

## À quoi ressemble la qualité

Les bonnes règles `SOUL.md` ressemblent à ceci :

- avoir une position
- sauter le remplissage
- être drôle quand c'est approprié
- signaler les mauvaises idées tôt
- rester concis sauf si la profondeur est vraiment utile

Les mauvaises règles `SOUL.md` ressemblent à ceci :

- maintenir le professionnalisme à tout moment
- fournir une assistance complète et réfléchie
- assurer une expérience positive et solidaire

Cette deuxième liste est comment vous obtenez de la bouillie.

## Un avertissement

La personnalité n'est pas une permission d'être négligent.

Gardez `AGENTS.md` pour les règles opérationnelles. Gardez `SOUL.md` pour la voix, la position et le style. Si votre agent travaille dans des canaux partagés, des réponses publiques ou des surfaces client, assurez-vous que le ton convient toujours à la situation.

Tranchant c'est bien. Ennuyeux ce n'est pas.

## Documents connexes

- [Agent workspace](/fr/concepts/agent-workspace)
- [System prompt](/fr/concepts/system-prompt)
- [SOUL.md template](/fr/reference/templates/SOUL)
