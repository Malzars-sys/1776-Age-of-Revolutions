# Machines de précision — intégration finalisée

Le joueur a approuvé la révision 2, fondée sur ses quatre photos d'une machine à tailler les engrenages. Elle est liée au bien `precision_machinery` via `gfx/interface/icons/goods_icons/1776_precision_machinery.dds`.

## Fichiers utiles conservés

- [Master original approuvé](revision_v2/previews/precision_machinery_source.png).
- [Prompt exact et provenance](revision_v2/PROMPTS.md).
- [Inventaire des 71 biens après intégration](revision_v2/integration/goods_audit.json).
- [Résultat des contrôles d'intégration](revision_v2/integration/integration_validation.json).
- [Registre commun des sources et paramètres d'export](../source_registry.json).

Le dernier inventaire compte 53 images vanilla, 17 images locales et un seul placeholder : Cuivre, volontairement exclu. Aucune texture de bien n'est manquante ou illisible. Cela ne constitue pas un audit des PM ni une certification des droits des images tierces déjà présentes.

La source PNG est conservée sans retouche. Pour retrouver exactement le DDS intégré, l'outil commun ajoute 151 px de marge transparente par côté, réduit à 256 × 256 et encode neuf mipmaps en BGRA8 natif. L'empreinte de l'export doit être identique au fichier runtime approuvé.

```powershell
node tools/rebuild_asset_icons.cjs --verify --asset=1776_precision_machinery
node tools/rebuild_asset_icons.cjs --export-cache --asset=1776_precision_machinery
```

## Nettoyage

Les premières propositions, miniatures, PNG réduits, planches de comparaison, références vanilla dupliquées, DDS candidats et snapshots avant intégration ont été retirés. La reconstruction utilise le master et le registre, pas ces dérivés. Les exports temporaires vont dans `.asset-cache/`, ignoré par Git.

Le contrôle d'intégration conservé est un résultat historique avant nettoyage. Les fichiers de diagnostic qu'il mentionne ne sont plus requis. Aucun test du rendu moteur, changement du Steam Build, commit ou push n'est revendiqué pour l'intégration ni pour le nettoyage.
