# Sources d'images et exports

## Ce qui reste dans le dépôt

- Les DDS effectivement utilisés par le jeu, dans `gfx/`.
- Les masters finaux approuvés, sans dégradation ni modification artistique.
- Les prompts, approbations, paramètres d'export et rapports utiles à la provenance.
- Le [registre des 111 exports reconstructibles](source_registry.json) et les outils nécessaires.

Les sources gardent leurs chemins historiques pour préserver les liens des manifestes d'export. Le dossier `previews/` peut contenir un **master final approuvé** : son nom ne signifie pas qu'il est jetable. Le registre désigne les sources exactes de chaque DDS.

## Ce qui ne doit plus être versionné

Miniatures 1/2/4/8 px, déclinaisons de taille, planches de comparaison, décodages DDS de contrôle, copies de références vanilla, DDS candidats ou sauvegardes temporaires et snapshots complets de fichiers avant intégration. Les mipmaps utiles au rendu restent dans le DDS ; elles ne nécessitent pas de PNG séparés.

Les sorties temporaires sont placées dans `.asset-cache/`, ignoré par Git. Les règles d'exclusion couvrent aussi les anciens répertoires de dérivés pour éviter leur réintroduction. Les références originales importantes pour un nouveau projet peuvent être conservées explicitement dans un dossier de sources, pas avec les copies natives de contrôle.

## Reconstruction et vérification

Le nouvel outil commun remplace la dépendance aux centaines de dérivés des anciens lots :

```powershell
node tools/rebuild_asset_icons.cjs --verify
node tools/rebuild_asset_icons.cjs --export-cache
node tools/rebuild_asset_icons.cjs --export-cache --asset=1776_precision_machinery
```

Il vérifie les empreintes des masters, reproduit les exports natifs BGRA8 et leurs mipmaps en mémoire, puis exige une identité **octet pour octet** avec les DDS approuvés. Les exports de reconstruction vont uniquement dans `.asset-cache/regenerated/`, sans modifier `gfx/`, les définitions ou le gameplay. Aucun PNG miniature n'est produit. La découverte initiale du registre est une opération de maintenance, pas une étape nécessaire pour reconstruire.

L'audit des biens (`tools/audit_remaining_goods_artwork.py`) écrit aussi dans le cache par défaut. Les anciens scripts par lot et rapports restent des archives de travail ; leurs contrôles avant intégration ne sont pas à relancer sur la version actuelle. Les liens historiques vers des dérivés supprimés ne constituent pas des fichiers source manquants : utiliser le registre et l'outil commun pour la version approuvée.

La reconstruction déterministe part des masters conservés. Relancer une génération IA à partir des prompts donne une nouvelle proposition, pas une garantie de reproduire la même peinture.
