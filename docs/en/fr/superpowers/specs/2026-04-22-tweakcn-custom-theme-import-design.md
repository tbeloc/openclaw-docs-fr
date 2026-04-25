# Conception de l'importation de thème personnalisé Tweakcn

Statut : approuvé en terminal le 2026-04-22

## Résumé

Ajouter exactement un emplacement de thème Control UI personnalisé local au navigateur qui peut être importé à partir d'un lien de partage tweakcn. Les familles de thèmes intégrées existantes restent `claw`, `knot` et `dash`. La nouvelle famille `custom` se comporte comme une famille de thème OpenClaw normale et supporte les modes `light`, `dark` et `system` lorsque la charge utile tweakcn importée inclut les deux ensembles de jetons clairs et sombres.

Le thème importé est stocké uniquement dans le profil de navigateur actuel avec le reste des paramètres Control UI. Il n'est pas écrit dans la configuration de la passerelle et ne se synchronise pas entre les appareils ou les navigateurs.

## Problème

Le système de thème Control UI est actuellement fermé sur trois familles de thèmes codées en dur :

- `ui/src/ui/theme.ts`
- `ui/src/ui/views/config.ts`
- `ui/src/styles/base.css`

Les utilisateurs peuvent basculer entre les familles intégrées et les variantes de mode, mais ils ne peuvent pas importer un thème de tweakcn sans modifier le CSS du référentiel. Le résultat demandé est plus petit qu'un système de thématisation général : conserver les trois thèmes intégrés et ajouter un emplacement importé contrôlé par l'utilisateur qui peut être remplacé à partir d'un lien tweakcn.

## Objectifs

- Conserver les familles de thèmes intégrées existantes inchangées.
- Ajouter exactement un emplacement personnalisé importé, pas une bibliothèque de thèmes.
- Accepter un lien de partage tweakcn ou une URL directe `https://tweakcn.com/r/themes/{id}`.
- Persister le thème importé dans le stockage local du navigateur uniquement.
- Faire fonctionner l'emplacement importé avec les contrôles de mode `light`, `dark` et `system` existants.
- Maintenir un comportement d'échec sûr : une mauvaise importation ne casse jamais le thème UI actif.

## Non-objectifs

- Pas de bibliothèque multi-thème ou liste d'importations locale au navigateur.
- Pas de persistance côté passerelle ou synchronisation entre appareils.
- Pas d'éditeur CSS arbitraire ou d'éditeur JSON de thème brut.
- Pas de chargement automatique des ressources de polices distantes depuis tweakcn.
- Pas de tentative de support des charges utiles tweakcn qui n'exposent qu'un seul mode.
- Pas de refactorisation de thématisation à l'échelle du référentiel au-delà des coutures requises pour Control UI.

## Décisions utilisateur déjà prises

- Conserver les trois thèmes intégrés.
- Ajouter un emplacement d'importation alimenté par tweakcn.
- Stocker le thème importé dans le navigateur, pas dans la configuration de la passerelle.
- Supporter `light`, `dark` et `system` pour l'emplacement importé.
- Remplacer l'emplacement personnalisé par l'importation suivante est le comportement prévu.

## Approche recommandée

Ajouter un quatrième identifiant de famille de thème, `custom`, au modèle de thème Control UI. La famille `custom` devient sélectionnable uniquement lorsqu'une importation tweakcn valide est présente. La charge utile importée est normalisée dans un enregistrement de thème personnalisé spécifique à OpenClaw et stockée dans le stockage local du navigateur avec le reste des paramètres UI.

À l'exécution, OpenClaw rend une balise `<style>` gérée qui définit les blocs de variables CSS personnalisées résolus :

```css
:root[data-theme="custom"] { ... }
:root[data-theme="custom-light"] { ... }
```

Cela maintient les variables de thème personnalisé limitées à la famille `custom` et évite de fuir les variables CSS en ligne dans les familles intégrées.

## Architecture

### Modèle de thème

Mettre à jour `ui/src/ui/theme.ts` :

- Étendre `ThemeName` pour inclure `custom`.
- Étendre `ResolvedTheme` pour inclure `custom` et `custom-light`.
- Étendre `VALID_THEME_NAMES`.
- Mettre à jour `resolveTheme()` pour que `custom` reflète le comportement de famille existant :
  - `custom + dark` -> `custom`
  - `custom + light` -> `custom-light`
  - `custom + system` -> `custom` ou `custom-light` selon la préférence du système d'exploitation

Aucun alias hérité n'est ajouté pour `custom`.

### Modèle de persistance

Étendre la persistance `UiSettings` dans `ui/src/ui/storage.ts` avec une charge utile de thème personnalisé optionnel :

- `customTheme?: ImportedCustomTheme`

Forme stockée recommandée :

```ts
type ImportedCustomTheme = {
  sourceUrl: string;
  themeId: string;
  label: string;
  importedAt: string;
  light: Record<string, string>;
  dark: Record<string, string>;
};
```

Notes :

- `sourceUrl` stocke l'entrée utilisateur d'origine après normalisation.
- `themeId` est l'identifiant de thème tweakcn extrait de l'URL.
- `label` est le champ tweakcn `name` s'il est présent, sinon `Custom`.
- `light` et `dark` sont déjà des cartes de jetons OpenClaw normalisées, pas des charges utiles tweakcn brutes.
- La charge utile importée vit à côté d'autres paramètres locaux au navigateur et est sérialisée dans le même document de stockage local.
- Si les données de thème personnalisé stockées sont manquantes ou invalides au chargement, ignorez la charge utile et revenez à `theme: "claw"` lorsque la famille persistée était `custom`.

### Application à l'exécution

Ajouter un gestionnaire de feuille de style de thème personnalisé étroit dans le runtime Control UI, détenu près de `ui/src/ui/app-settings.ts` et `ui/src/ui/theme.ts`.

Responsabilités :

- Créer ou mettre à jour une balise `<style id="openclaw-custom-theme">` stable dans `document.head`.
- Émettre du CSS uniquement lorsqu'une charge utile de thème personnalisé valide existe.
- Supprimer le contenu de la balise de style lorsque la charge utile est effacée.
- Conserver le CSS de famille intégrée dans `ui/src/styles/base.css` ; ne pas fusionner les jetons importés dans la feuille de style vérifiée.

Ce gestionnaire s'exécute chaque fois que les paramètres sont chargés, enregistrés, importés ou effacés.

### Sélecteurs en mode clair

L'implémentation devrait préférer `data-theme-mode="light"` pour le style clair inter-familles plutôt que de traiter spécialement `custom-light`. Si un sélecteur existant est épinglé à `data-theme="light"` et doit s'appliquer à chaque famille claire, élargissez-le dans le cadre de ce travail.

## UX d'importation

Mettre à jour `ui/src/ui/views/config.ts` dans la section `Appearance` :

- Ajouter une carte `Custom` à côté de `Claw`, `Knot` et `Dash`.
- Afficher la carte comme désactivée lorsqu'aucun thème personnalisé importé n'existe.
- Ajouter un panneau d'importation sous la grille de thèmes avec :
  - une entrée de texte pour un lien de partage tweakcn ou une URL `/r/themes/{id}`
  - un bouton `Import`
  - un chemin `Replace` lorsqu'une charge utile personnalisée existe déjà
  - une action `Clear` lorsqu'une charge utile personnalisée existe déjà
- Afficher l'étiquette de thème importée et l'hôte source lorsqu'une charge utile existe.
- Si le thème actif est `custom`, l'importation d'un remplacement s'applique immédiatement.
- Si le thème actif n'est pas `custom`, l'importation stocke uniquement la nouvelle charge utile jusqu'à ce que l'utilisateur sélectionne la carte `Custom`.

Le sélecteur de thème des paramètres rapides dans `ui/src/ui/views/config-quick.ts` devrait également afficher `Custom` uniquement lorsqu'une charge utile existe.

## Analyse d'URL et récupération distante

Le chemin d'importation du navigateur accepte :

- `https://tweakcn.com/themes/{id}`
- `https://tweakcn.com/r/themes/{id}`

L'implémentation devrait normaliser les deux formes en :

- `https://tweakcn.com/r/themes/{id}`

Le navigateur récupère ensuite le point de terminaison `/r/themes/{id}` normalisé directement.

Utilisez un validateur de schéma étroit pour la charge utile externe. Un schéma zod est préféré car c'est une limite externe non fiable.

Champs distants requis :

- `name` au niveau supérieur comme chaîne optionnelle
- `cssVars.theme` comme objet optionnel
- `cssVars.light` comme objet
- `cssVars.dark` comme objet

Si `cssVars.light` ou `cssVars.dark` est manquant, rejetez l'importation. C'est délibéré : le comportement du produit approuvé est le support complet du mode, pas la synthèse au mieux de l'effort d'un côté manquant.

## Mappage de jetons

Ne pas refléter les variables tweakcn aveuglément. Normaliser un sous-ensemble limité en jetons OpenClaw et dériver le reste dans un assistant.

### Jetons importés directement

De chaque bloc de mode tweakcn :

- `background`
- `foreground`
- `card`
- `card-foreground`
- `popover`
- `popover-foreground`
- `primary`
- `primary-foreground`
- `secondary`
- `secondary-foreground`
- `muted`
- `muted-foreground`
- `accent`
- `accent-foreground`
- `destructive`
- `destructive-foreground`
- `border`
- `input`
- `ring`
- `radius`

De `cssVars.theme` partagé lorsqu'il est présent :

- `font-sans`
- `font-mono`

Si un bloc de mode remplace `font-sans`, `font-mono` ou `radius`, la valeur locale du mode gagne.

### Jetons dérivés pour OpenClaw

L'importateur dérive les variables OpenClaw uniquement à partir des couleurs de base importées :

- `--bg-accent`
- `--bg-elevated`
- `--bg-hover`
- `--panel`
- `--panel-strong`
- `--panel-hover`
- `--chrome`
- `--chrome-strong`
- `--text`
- `--text-strong`
- `--chat-text`
- `--muted`
- `--muted-strong`
- `--accent-hover`
- `--accent-muted`
- `--accent-subtle`
- `--accent-glow`
- `--focus`
- `--focus-ring`
- `--focus-glow`
- `--secondary`
- `--secondary-foreground`
- `--danger`
- `--danger-muted`
- `--danger-subtle`

Les règles de dérivation vivent dans un assistant pur pour pouvoir être testées indépendamment. Les formules exactes de mélange de couleurs sont un détail d'implémentation, mais l'assistant doit satisfaire deux contraintes :

- préserver le contraste lisible proche de l'intention du thème importé
- produire une sortie stable pour la même charge utile importée

### Jetons ignorés en v1

Ces jetons tweakcn sont intentionnellement ignorés dans la première version :

- `chart-*`
- `sidebar-*`
- `font-serif`
- `shadow-*`
- `tracking-*`
- `letter-spacing`
- `spacing`

Cela maintient la portée sur les jetons que Control UI actuel a réellement besoin.

### Polices

Les chaînes de pile de polices sont importées si présentes, mais OpenClaw ne charge pas les ressources de polices distantes en v1. Si la pile importée référence des polices indisponibles dans le navigateur, le comportement de secours normal s'applique.

## Comportement d'échec

Les mauvaises importations doivent échouer fermées.

- Format d'URL invalide : afficher l'erreur de validation en ligne, ne pas récupérer.
- Hôte ou forme de chemin non supportés : afficher l'erreur de validation en ligne, ne pas récupérer.
- Échec réseau, réponse non-OK ou JSON malformé : afficher l'erreur en ligne, conserver la charge utile stockée actuelle intacte.
- Échec de schéma ou blocs light/dark manquants : afficher l'erreur en ligne, conserver la charge utile stockée actuelle intacte.
- Action Clear :
  - supprime la charge utile personnalisée stockée
  - supprime le contenu de la balise de style personnalisée gérée
  - si `custom` est actif, bascule la famille de thème vers `claw`
- Charge utile personnalisée stockée invalide au premier chargement :
  - ignorer la charge utile stockée
  - ne pas émettre de CSS personnalisé
  - si la famille de thème persistée était `custom`, revenir à `claw`

À aucun moment une importation échouée ne devrait laisser le document actif avec des variables CSS personnalisées partielles appliquées.

## Fichiers attendus pour changer dans l'implémentation

Fichiers principaux :

- `ui/src/ui/theme.ts`
- `ui/src/ui/storage.ts`
- `ui/src/ui/app-settings.ts`
- `ui/src/ui/views/config.ts`
- `ui/src/ui/views/config-quick.ts`
- `ui/src/styles/base.css`

Assistants probablement nouveaux :

- `ui/src/ui/custom-theme.ts`
- `ui/src/ui/custom-theme-import.ts`

Tests :

- `ui/src/ui/app-settings.test.ts`
- `ui/src/ui/storage.node.test.ts`
- `ui/src/ui/views/config.browser.test.ts`
- nouveaux tests ciblés pour l'analyse d'URL et la normalisation de charge utile

## Tests

Couverture d'implémentation minimale :

- analyser l'URL du lien de partage dans l'identifiant de thème tweakcn
- normaliser `/themes/{id}` et `/r/themes/{id}` dans l'URL de récupération
- rejeter les hôtes non supportés et les identifiants malformés
- valider la forme de charge utile tweakcn
- mapper une charge utile tweakcn valide dans des cartes de jetons OpenClaw clairs et sombres normalisées
- charger et enregistrer la charge utile personnalisée dans les paramètres locaux du navigateur
- résoudre `custom` pour `light`, `dark` et `system`
- désactiver la sélection `Custom` lorsqu'aucune charge utile n'existe
- appliquer le thème importé immédiatement lorsque `custom` est déjà actif
- revenir à `claw` lorsque le thème personnalisé actif est effacé

Cible de vérification manuelle :

- importer un thème tweakcn connu depuis Paramètres
- basculer entre `light`, `dark` et `system`
- basculer entre `custom` et les familles intégrées
- recharger la page et confirmer que le thème personnalisé importé persiste localement

## Notes de déploiement

Cette fonctionnalité est intentionnellement petite. Si les utilisateurs demandent ultérieurement plusieurs thèmes importés, renommer, exporter ou synchroniser entre appareils, traitez cela comme une conception de suivi. Ne pré-construisez pas une abstraction de bibliothèque de thèmes dans cette implémentation.
