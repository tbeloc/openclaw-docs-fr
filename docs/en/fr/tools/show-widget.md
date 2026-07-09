---
summary: "Afficher des widgets SVG ou HTML autonomes en ligne dans le chat web"
title: "Afficher un widget"
sidebarTitle: "Afficher un widget"
read_when:
  - You want an agent to render an interactive result inside web chat
  - You need the show_widget input, security, or retention contract
---

`show_widget` affiche un fragment SVG ou HTML autonome en ligne dans la transcription de chat de l'interface de contrôle. Le plugin Canvas fourni possède l'outil et héberge chaque résultat en tant que document Canvas de même origine.

L'outil n'est disponible que lorsque le client Gateway d'origine déclare la capacité `inline-widgets`. L'interface de contrôle déclare cette capacité automatiquement. Les exécutions de canal telles que Telegram et WhatsApp ne reçoivent pas `show_widget`.

Le transport de capacité couvre les backends de modèles intégrés, Codex app-server et CLI. Les appelants MCP authentifiés par subvention et les appelants d'invocation d'outil HTTP directs restent fermés en cas d'échec car ils ne déclarent pas les capacités du client.

## Utiliser l'outil

L'agent fournit deux chaînes de caractères obligatoires :

<ParamField path="title" type="string" required>
  Titre court affiché avec l'aperçu en ligne et dans le titre du document hébergé.
</ParamField>

<ParamField path="widget_code" type="string" required>
  Fragment SVG ou HTML autonome. L'entrée commençant par `<svg` après suppression des espaces est rendue en mode SVG ; toutes les autres entrées sont traitées comme un fragment HTML. Longueur maximale : 262 144 caractères.
</ParamField>

Le résultat de l'outil inclut un handle d'aperçu Canvas, de sorte que le chat web affiche le widget directement à partir de l'appel d'outil et le restaure après le rechargement de l'historique. Les transcriptions qui ne rendent pas les aperçus affichent toujours le chemin Canvas hébergé.

## Sécurité et stockage

Les documents de widget utilisent une politique de sécurité du contenu restrictive : les styles et scripts en ligne sont autorisés, les images peuvent utiliser des URL `data:`, et les récupérations externes et les chargements de ressources sont bloqués. Conservez tous les balises, styles, scripts et données d'image dans `widget_code`.

L'iframe omet toujours `allow-same-origin`, même lorsque le mode d'intégration global de l'interface de contrôle est `trusted`, de sorte que les scripts de widget ne peuvent pas lire l'origine de l'application parente. L'hôte Canvas sert également les documents de widget avec un en-tête de réponse `Content-Security-Policy: sandbox allow-scripts`, de sorte que l'ouverture directe de l'URL hébergée exécute toujours le widget dans une origine opaque au lieu de l'origine de l'interface de contrôle. Le sandboxing du navigateur n'empêche pas un script de naviguer dans sa propre iframe ; ne rendez que le code de widget que vous êtes disposé à exécuter dans ce cadre isolé.

L'iframe suit également [`gateway.controlUi.embedSandbox`](/fr/web/control-ui#hosted-embeds). Le niveau `scripts` par défaut prend en charge les widgets interactifs tout en préservant l'isolement des origines.

Canvas conserve au maximum 32 widgets par session (ou par agent lorsqu'aucune session n'est disponible). La création d'un autre widget supprime le document le plus ancien dans cette portée.

## Connexes

- [Intégrations hébergées de l'interface de contrôle](/fr/web/control-ui#hosted-embeds)
- [Plugin Canvas](/fr/plugins/reference/canvas)
- [Capacités du client du protocole Gateway](/fr/gateway/protocol#client-capabilities)
