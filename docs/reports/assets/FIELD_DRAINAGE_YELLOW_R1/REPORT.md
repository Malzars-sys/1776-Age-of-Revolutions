# Drainage agricole — couleur des PM

Correction du 23 octobre 2026 : les onze méthodes de drainage utilisent désormais une icône jaune terne, dans la palette de l’irrigation standard, à la place du pictogramme violet `unused/maintained_sewers.dds`.

Le pictogramme de conduite et d’eau a été recoloré avec l’outil **image_gen intégré**, à partir de l’icône native et d’une référence de couleur native. Le prompt final exact est conservé dans [PROMPT.txt](PROMPT.txt). La sortie a été examinée, puis exportée au format de PM standard : 208 × 208, BGRA8, huit mipmaps, transparence conservée. La conversion de format et de taille n’effectue aucune recoloration supplémentaire.

Fichiers livrés dans le dépôt :

- PNG maître : `workshop_assets/source/1776_field_drainage_yellow.png`.
- Texture du jeu : `gfx/interface/icons/production_method_icons/1776_field_drainage_yellow.dds`.
- Aperçu à taille native : `docs/reports/assets/FIELD_DRAINAGE_YELLOW_R1/drainage_yellow_preview.png`.

Les onze références de `common/production_methods/22_field_drainage_plantations.txt` sont mises à jour. La correspondance du vérificateur `tools/audit_runtime_icon_bindings.py` vise également cette nouvelle texture pour conserver le choix lors des prochains audits. Aucun nom, technologie, emploi, intrant ou rendement n’est modifié ; l’illustration de technologie et les icônes des autres PM restent intactes.

**21/21 contrôles statiques réussis** : références, format, transparence, absence de violet visible, conservation des paramètres et **2 424 fichiers protégés** inchangés. L’installation vanilla, HEAD, branche et index Git sont préservés. L’aperçu a été contrôlé visuellement ; le rendu dans le jeu reste à vérifier après redémarrage.
