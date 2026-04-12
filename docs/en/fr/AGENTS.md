# Guide de la documentation

Ce répertoire gère la création de documentation, les règles de liens Mintlify et la politique i18n de la documentation.

## Règles Mintlify

- La documentation est hébergée sur Mintlify (`https://docs.openclaw.ai`).
- Les liens de documentation interne dans `docs/**/*.md` doivent rester relatifs à la racine sans suffixe `.md` ou `.mdx` (exemple : `[Config](/fr/configuration)`).
- Les références croisées de sections doivent utiliser des ancres sur des chemins relatifs à la racine (exemple : `[Hooks](/fr/configuration#hooks)`).
- Les titres de la documentation doivent éviter les tirets cadratins et les apostrophes car la génération d'ancres Mintlify est fragile à ce niveau.
- Le README et les autres documents rendus par GitHub doivent conserver les URLs absolues de la documentation pour que les liens fonctionnent en dehors de Mintlify.
- Le contenu de la documentation doit rester générique : pas de noms de périphériques personnels, de noms d'hôtes ou de chemins locaux ; utilisez des espaces réservés comme `user@gateway-host`.

## Règles de contenu de la documentation

- Pour la documentation, la copie d'interface utilisateur et les listes de sélecteurs, classez les services/fournisseurs par ordre alphabétique sauf si la section décrit explicitement l'ordre d'exécution ou l'ordre de détection automatique.
- Maintenez la cohérence de la dénomination des plugins groupés avec les règles de terminologie des plugins à l'échelle du repo dans le fichier `AGENTS.md` racine.

## i18n de la documentation

- Les documents en langue étrangère ne sont pas maintenus dans ce repo. La sortie de publication générée se trouve dans le repo séparé `openclaw/docs` (souvent cloné localement sous `../openclaw-docs`).
- N'ajoutez pas ou ne modifiez pas les documents localisés sous `docs/<locale>/**` ici.
- Traitez la documentation en anglais dans ce repo plus les fichiers de glossaire comme la source de vérité.
- Pipeline : mettez à jour la documentation en anglais ici, mettez à jour `docs/.i18n/glossary.<locale>.json` selon les besoins, puis laissez le repo de publication se synchroniser et `scripts/docs-i18n` s'exécuter dans `openclaw/docs`.
- Avant de réexécuter `scripts/docs-i18n`, ajoutez des entrées de glossaire pour tout nouveau terme technique, titre de page ou étiquette de navigation courte qui doit rester en anglais ou utiliser une traduction fixe.
- `pnpm docs:check-i18n-glossary` est la garde pour les titres de documents en anglais modifiés et les étiquettes de documents internes courtes.
- La mémoire de traduction se trouve dans les fichiers `docs/.i18n/*.tm.jsonl` générés dans le repo de publication.
- Voir `docs/.i18n/README.md`.
