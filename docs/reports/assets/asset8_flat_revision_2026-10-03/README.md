# Révision des PM et du pavage — 3 octobre 2026

**Décision du joueur le 4 octobre : les dix PM hors laboratoire sont validés et intégrés dans la [révision avec grain fin et dégradé vertical](../asset8_pm_grain_revision_2026-10-03/README.md).** Les sept PM du laboratoire gardent leurs anciennes icônes en jeu : ni les propositions plates ici ni leurs variantes granuleuses ne sont sélectionnées. Les fichiers de comparaison restent conservés. La technologie de pavage et le bâtiment vanilla restent inchangés.

## Ce qui est déjà intégré

Les **Infrastructures régionales** réutilisent maintenant directement l’image vanilla des chemins de fer. Seul le champ `icon` du bâtiment a changé. L’illustration personnalisée rejetée est conservée dans le précédent dossier ; elle ne doit pas être intégrée.

## Ce qui attend la validation visuelle

**17 icônes de méthodes de production et 1 icône de technologie** ont été refaites avec imagegen. Aucun de ces nouveaux PNG n’est encore exporté en DDS ni intégré au jeu.

- [Routes, pavage et bâtiment vanilla](ROUTES_TECH_APERCU_REVISE.png)
- [PM des laboratoires](PM_LABORATOIRE_PLATS.png)
- [PM d’industrie et d’extraction](PM_INDUSTRIE_PLATS.png)
- [Comparaison à 64 px : page 1](PM_COMPARAISON_VANILLA_1.png), [page 2](PM_COMPARAISON_VANILLA_2.png), [page 3](PM_COMPARAISON_VANILLA_3.png)
- [Technologie et photographie de référence](TECH_PAVAGE_REFERENCE.png)
- [Transparence sur damier](TRANSPARENCE_DAMIER.png)

Les PM sont désormais des symboles 2D simplifiés beige/ocre, sans éclairage en volume, ombre portée, biseau ni texture réaliste. Les contours restent plus francs que ceux des trois références vanilla : la proximité visuelle doit donc être approuvée sur les comparaisons, et n’est pas déclarée parfaite automatiquement.

La technologie **Génie routier** reprend les pavés gris disposés en éventail de la photographie fournie, vus du dessus. Elle ne comporte plus de coupe de fondation ni d’outil ajouté. Elle n’utilise pas le style schématique réservé aux PM.

## Vérifications

Les 18 images ont un véritable canal alpha et des coins entièrement transparents. Les ouvertures ont également été regardées sur damier : fioles, roues, tamis, fenêtres et espace autour du feu. Les aperçus montrent les formats 32, 48 et 64 pixels sur fond clair et sombre.

La comparaison avec l’état du dépôt avant cette demande protège **1 213 fichiers** de `common` et `gfx`. Le seul changement est le champ d’image du bâtiment mentionné plus haut. Les 13 anciennes textures DDS des PM déjà intégrés sont inchangées ; les cinq autres propositions n’ont pas été exportées. Aucun effet économique ni condition de technologie n’a été modifié. Aucun test en jeu n’a été effectué pour ces nouvelles propositions.

## Fichiers et traçabilité

- `previews/` : masters PNG générés, copiés sans retouche artistique ; les originaux restent conservés.
- `target_size_png/` : simples réductions aux formats natifs, PM 208 px et technologie 256 px ; pas des fichiers installés dans le jeu.
- `references/` : copies exactes des quatre références fournies et décodage de l’image vanilla du bâtiment.
- [Requêtes de génération intégrales](generation_requests.json) : instructions exactes et références utilisées.
- [Résultats de génération](generation_results.json) : chemins des originaux et copies.
- [Contrôles techniques](preview_validation.json) et [contrôle du bâtiment vanilla](native_building_validation.json).
- `baseline.json` : empreintes avant modification, conservées sans réécriture.

Le précédent lot reste archivé dans `../asset8_preview_2026-10-03/` avec un avis de retrait. L’intégration des nouvelles images générées doit attendre l’accord de l’utilisateur, puis inclure les contrôles de couleur RGBA/BGRA et des mipmaps pour éviter la dérive bleue déjà rencontrée.
