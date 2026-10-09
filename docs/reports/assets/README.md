# Sources d'images et exports

## Ce qui reste dans le dépôt

- Les DDS effectivement utilisés par le jeu, dans `gfx/`.
- Les masters finaux approuvés, sans dégradation ni modification artistique.
- Les prompts, approbations, paramètres d'export et rapports utiles à la provenance.
- Le [registre des 191 exports reconstructibles](source_registry.json) et les outils nécessaires.

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

Les entrées carrées gardent leur champ `size`. Pour les profils de navires rectangulaires, l'exporteur accepte `width` et `height`, conserve les proportions du master et construit la chaîne complète jusqu'à 1 × 1. Le stockage BGRA8 et l'alpha restent identiques. L'extension a été vérifiée sans changer les 143 DDS antérieurs. Les trois profils approuvés ont leurs [masters et provenance d'origine](early_ship_sources_2026-10-08/manifest.json), conservés sans miniatures ni copies de contrôle. La [révision capitale](early_ship_sources_2026-10-08/capital_colour_revision.json) remplace ensuite la caravelle orange par le jaune natif des navires capitaux, sans redessin ; galère et cogue restent bleues. Le registre pointe vers le nouveau master jaune, sans supprimer l'original historique. Les corrections de classe et la [proposition d'équipements et de technologies](../naval/early_ship_design_proposal_2026-10-08.md) sont distinguées : seuls les rôles, la contrainte côtière et la recoloration sont intégrés à cette étape.

L'[étape navale suivante](../naval/early_ship_equipment_integration_2026-10-08.md), autorisée ensuite par le joueur, intègre 36 choix d'équipement et cinq fonctions, dont deux cumulables pour caravelle et galère, ainsi que les déblocages. Elle conserve les pictogrammes navals natifs actifs. Les [trois premiers nouveaux dessins proposés](../naval/early_ship_equipment_art_proposals_2026-10-08.json), armements bronze/argent/or de la caravelle, restent dans le cache de preview en attente d'approbation ; aucun DDS ni entrée supplémentaire du registre n'est installé pour ces propositions.

Pour installer ou réinstaller un export déjà enregistré et approuvé, l'option explicite `--install-approved --asset=nom_exact` écrit uniquement ce DDS dans `gfx/`. Elle refuse l'absence de sélecteur, une correspondance multiple ou une empreinte différente du master/export approuvé. Elle ne génère pas d'image IA et ne modifie aucune définition. Exemple pour le lot de ciment validé :

```powershell
node tools/rebuild_asset_icons.cjs --install-approved --asset=1776_natural_cement_process
```

L'audit des biens (`tools/audit_remaining_goods_artwork.py`) écrit aussi dans le cache par défaut. Les anciens scripts par lot et rapports restent des archives de travail ; leurs contrôles avant intégration ne sont pas à relancer sur la version actuelle. Les liens historiques vers des dérivés supprimés ne constituent pas des fichiers source manquants : utiliser le registre et l'outil commun pour la version approuvée.

La reconstruction déterministe part des masters conservés. Relancer une génération IA à partir des prompts donne une nouvelle proposition, pas une garantie de reproduire la même peinture.

## Double flèche commune aux groupes

La double flèche est universelle à la demande du joueur : réutiliser ses variantes existantes selon le code couleur, sans génération IA ni redessin par groupe. Le [lot 13 approuvé](pm_group_arrow_sources_2026-10-08/manifest.json) introduit la flèche jaune partagée. La [clôture autorisée de tous les groupes](pm_group_arrow_sources_2026-10-08/completion.json) intègre le lot 14 et les autres raccordements, cuivre compris : 122 groupes locaux contrôlés, 76 corrections de texture. Jaune production, vert automatisation/locomotives, violet préparation/secondaire/scientifique, rouge militaire/canaux, vert bleuté santé, blanc imprimerie/distillation et bleu personnel. Deux masters finaux seulement sont conservés pour les variantes jaune et médicale ; les cinq autres couleurs réutilisent les fichiers existants sans copies. La variante médicale est un décalage de teinte de la flèche native, avec alpha, proportions et valeur HSV inchangés. Les miniatures et snapshots restent ignorés. La dernière autorisation supprime les lots de trois pour cette intégration de groupes ; les dessins individuels de PM restent soumis à validation préalable.

La [correction suivante des familles](pm_group_arrow_sources_2026-10-08/family_corrections.json) conserve explicitement le **bleu des données** et utilise la flèche bleue existante pour leurs six groupes. La cuisine fine épicée est classée en production secondaire : sa flèche devient violette, ses trois dessins violets restant inchangés. Sept raccordements, aucun nouveau fichier image. Les cinq PM individuels du cuivre attendent les icônes de la mise à jour 1.15 ; aucune génération anticipée.

La couverture des groupes peut être revérifiée avec `tools/preview_pm_group_bindings.py docs/reports/assets/pm_group_arrow_sources_2026-10-08/completion.json --check-coverage`, sans dépendre des snapshots du cache. Le contrôle inclut les groupes locaux inutilisés et les références actives natives ; `pmg_dummy`, auxiliaire natif non visuel des hubs urbains, reste volontairement sans image.

## Couleurs des PM

La dernière consigne ferroviaire vise les locomotives uniquement : vert, dessins existants conservés. Les wagons gardent leurs palettes et raccordements actuels. Les [quatre recolorations](pm_locomotive_colour_sources_2026-10-07/manifest.json) enregistrent les empreintes natives et les décalages de teinte ; aucun redessin ni génération IA. Les dimensions natives sont conservées (208/8 pour la primitive, 104/7 pour les trois autres).

Le [lot 15 validé](pm_secondary_colour_sources_2026-10-08/manifest.json) conserve les dessins de désactivation des machines de précision, distillation fractionnée et craquage thermo-catalytique, harmonisés en violet. Ses trois masters finaux sont enregistrés ; les sources d'origine utiles à la provenance restent conservées. Les deux DDS de raffinerie gardent leurs chemins ; la désactivation dispose d'un nouveau DDS dédié pour ne pas modifier une texture vanilla partagée. Alpha, dimensions, valeur HSV et recettes sont inchangés. `tools/recolour_pm_icons.py` permet les previews dans le cache et le contrôle d'intégration sur le snapshot correspondant ; ne pas relancer ce contrôle historique après d'autres changements légitimes de groupes. La vérification du registre reste valable sur l'état actuel.

La [fin d'harmonisation autorisée](pm_final_colour_sources_2026-10-08/manifest.json) conserve les dessins natif/TKR des avions tout métal et articles ménagers aluminium, teintés du jaune de production. Les deux derniers cas forment exceptionnellement un lot de deux, à la demande de terminer. Les paramètres incluent une saturation minimale et une teinte pour les pixels achromatiques des articles ménagers ; leur alpha et valeur HSV restent identiques, comme leur relief et leurs proportions. L'original TKR demeure dans `gfx/` comme source de la recoloration et conserve ses références d'attribution/droits ; cette variante ne crée aucune nouvelle autorisation de redistribution. L'avion natif installé n'est pas modifié. Deux masters finaux et deux exports dédiés sont enregistrés, toutes les comparaisons restant dans le cache ignoré. Aucun bâtiment, technologie, recette ou départ économique n'est changé.

Le [contrat de palette par famille et par groupe](pm_palette_rules.json) conserve les décisions du joueur du 7 octobre et la clôture des flèches du 8 octobre. Les couleurs se choisissent selon le PMG réel, pas selon le mot « électrique » ou « machine ». L'audit `tools/audit_pm_group_palette.py --report` relève les palettes inconnues, les placeholders de groupe et les écarts potentiels dans `.asset-cache/pm_palette_2026-10-07/`. Il est en lecture seule ; son tri par pixels ne remplace pas une inspection artistique. Les corrections des **dessins individuels** suivent toujours le cycle lot de trois, preview, approbation, puis intégration. Ne jamais recolorer un fichier vanilla partagé en place ; les icônes `unused/` retenues, les PM individuels du cuivre et les sept anciens PM de laboratoire restent protégés.

## Équipements navals : lot d’armement approuvé le 8 octobre 2026

Les trois armements de caravelle (bronze/argent/or) sont intégrés tels qu’approuvés, sans retouche. [Masters, prompts et recette d’export](naval_equipment_armament_sources_2026-10-08/manifest.json). DDS natifs de 120 × 120 avec sept mipmaps, alpha conservé ; trois liens d’icône seulement, aucun changement de coût/statistique. Ce lot a porté le registre à 154 exports exacts. Pas d’essai en jeu dans cette passe.

## Équipements navals : lot de coque approuvé le 8 octobre 2026

Les trois coques de caravelle sont intégrées telles que validées : franc-bord bronze, couples doubles argent et renforts diagonaux or. [Masters, prompts et export](naval_equipment_hull_sources_2026-10-08/manifest.json), originaux et halo conservés sans retouche. Trois DDS natifs 120 × 120 avec sept mipmaps, seuls trois champs `icon` sont modifiés. Les 154 exports antérieurs restent inchangés, registre total : 157. Contrôle de cette passe : `tools/integrate_naval_equipment_art.py check --lot hull` ; les contrôles historiques exacts de lots précédents ne doivent pas être relancés après les nouveaux lots. `tools/build_early_ship_equipment.py --check` et la reconstruction du registre valident l’état global courant. Le [lot propulsion v2](../naval/caravel_propulsion_art_proposals_v2_2026-10-08.json) a été intégré lors de la passe suivante : un mât commun, une à trois rangées de voiles superposées. La progression horizontale précédente a été refusée et reste archivée. Aucun essai en jeu.


## Équipements navals : gréement vertical approuvé le 8 octobre 2026

Trois icônes verticales et leurs intitulés français/anglais sont intégrés après validation du joueur. [Masters exacts, prompts et recettes](naval_equipment_propulsion_sources_2026-10-08/manifest.json) conservés sans retouche ; trois DDS natifs 120 × 120 et sept mipmaps. Statistiques, coûts et technologies inchangés. Les 157 exports précédents sont protégés, registre total à cette étape : 160. Contrôles `tools/integrate_naval_equipment_art.py check --lot propulsion`, `tools/build_early_ship_equipment.py --check` et `tools/rebuild_asset_icons.cjs --verify` réussis. Le lot pont a ensuite été approuvé et intégré comme indiqué ci-dessous. Aucun essai en jeu.

## Équipements navals : pont approuvé le 8 octobre 2026

Trois [masters exacts et recettes](naval_equipment_deck_sources_2026-10-08/manifest.json) : bronze original, argent v5 et or original. Les anciennes révisions argent refusées ne sont pas exportées. Trois DDS natifs 120 × 120 avec sept mipmaps, alpha généré conservé sans retouche ; trois liens d’icône seulement. Les 160 exports antérieurs restent exacts, registre total à cette étape : 163, douze icônes de caravelle intégrées. Contrôle étroit `tools/integrate_naval_equipment_art.py check --lot deck` réussi, sans changement de gameplay et sans essai en jeu. Les armements de galère v2 ont ensuite été approuvés et intégrés.

## Équipements navals : armements de galère v2 approuvés le 8 octobre 2026

Le joueur a refusé le premier lot, trop similaire, puis approuvé les trois silhouettes v2 : pivots, affûts à grandes roues et longue glissière axiale. [Masters, prompts et recettes](naval_equipment_galley_armament_sources_2026-10-08/manifest.json) : exacts sans retouche, halo argent et alpha originaux conservés. Trois DDS natifs 120 × 120 / sept mipmaps, trois liens `aor_galley_guns_*` uniquement. Les 163 exports antérieurs sont préservés, registre total à cette étape : 166. Contrôles étroit et global des équipements réussis, quinze icônes approuvées actives ; aucun essai en jeu. Les coques de galère ont ensuite été approuvées et intégrées.

## Équipements navals : coques de galère approuvées le 8 octobre 2026

Trois [masters exacts, prompts et exports](naval_equipment_galley_hull_sources_2026-10-08/manifest.json) : bordage bronze, traverses argent, quille doublée or. Originaux et alpha conservés sans retouche, halo or compris. Trois DDS 120 × 120 / sept mipmaps et trois liens `aor_galley_armor_*` seulement. Les statistiques et coûts d’amélioration existent déjà et restent inchangés. Les 166 exports antérieurs sont préservés ; registre total à cette étape : 169, dix-huit équipements approuvés actifs. La propulsion de galère a ensuite été approuvée et intégrée.

## Équipements navals : propulsion de galère approuvée le 8 octobre 2026

Trois [masters exacts, prompts et recettes](naval_equipment_galley_propulsion_sources_2026-10-08/manifest.json) : avirons séparés bronze, aviron collectif argent, deux voiles latines et aviron collectif or. Originaux et alpha préservés sans retouche, halo bronze et argent compris. Trois DDS 120 × 120 / sept mipmaps et trois liens `aor_galley_propulsion_*` seulement. Les 169 exports antérieurs restent exacts ; registre total à cette étape : 172, vingt et une icônes d’équipement approuvées actives. Statistiques, recettes, technologies et flottes inchangées ; aucun essai en jeu. L’approvisionnement de galère a ensuite été approuvé et intégré.

## Équipements navals : approvisionnement de galère approuvé le 8 octobre 2026

Trois [masters exacts, prompts et recettes](naval_equipment_galley_supply_sources_2026-10-08/manifest.json) : coffres et outres bronze, tonneaux sous coursie argent, cambuse et avirons de rechange or. Originaux et alpha préservés sans retouche, halo bronze et argent compris. Trois DDS 120 × 120 / sept mipmaps et trois liens `aor_galley_range_*` seulement. Les 172 exports antérieurs restent exacts ; registre total à cette étape : 175, vingt-quatre icônes approuvées actives. Statistiques, recettes, technologies, portée côtière et flottes inchangées ; aucun essai en jeu. Les coques de cogue ont ensuite été approuvées et intégrées.

## Équipements navals : coques de cogue approuvées le 8 octobre 2026

Trois [masters exacts, prompts et recettes](naval_equipment_cog_hull_sources_2026-10-08/manifest.json) : bordage à clins bronze, varangues et carlingue argent, serres et baux or. Originaux et alpha préservés sans retouche, halo argent compris. Trois DDS 120 × 120 / sept mipmaps et trois liens `aor_cog_armor_*` seulement. Les 175 exports antérieurs restent exacts ; registre total à cette étape : 178, vingt-sept icônes approuvées actives. Statistiques, recettes, technologies et flottes inchangées ; aucun essai en jeu. Les armements de cogue ont ensuite été approuvés et intégrés.

## Équipements navals : armements de cogue approuvés le 8 octobre 2026

Trois [masters exacts, prompts et recettes](naval_equipment_cog_armament_sources_2026-10-08/manifest.json) : pierrier sur pivot bronze v2, canon long à roues argent inchangé, carronade sur glissière or v3. Originaux et alpha conservés sans retouche, halo doré inclus. Trois DDS 120 × 120 / sept mipmaps et trois liens `aor_cog_guns_*` seulement. Registre total à cette étape : 181, trente icônes approuvées actives. Statistiques, recettes, technologies et flottes inchangées ; contrôle étroit réussi, aucun essai en jeu. La propulsion de cogue a ensuite été approuvée et intégrée.

## Équipements navals : propulsion de cogue approuvée le 8 octobre 2026

Trois [masters exacts, prompts et recettes](naval_equipment_cog_propulsion_sources_2026-10-08/manifest.json) : voile carrée bronze, bandes de ris argent, hunier superposé or. Originaux et alpha préservés sans retouche. Trois DDS 120 × 120 / sept mipmaps et trois liens `aor_cog_propulsion_*` seulement. Registre total à cette étape : 184, trente-trois icônes approuvées actives. Vitesse, recettes, technologies et flottes inchangées ; contrôle étroit réussi, aucun essai en jeu. Les aménagements de cogue ont ensuite été approuvés et intégrés.

## Équipements navals : aménagements de cogue approuvés le 8 octobre 2026

Trois [masters exacts, prompts et recettes](naval_equipment_cog_supply_sources_2026-10-08/manifest.json) : cale libre et couchage bronze, couchettes et râtelier argent, pont de troupes et panneau de chargement or. Originaux et alpha préservés sans retouche. Trois DDS 120 × 120 / sept mipmaps et trois liens `aor_cog_range_*` seulement. Registre total à cette étape : 187, trente-six icônes principales approuvées actives. Statistiques, recettes, technologies et flottes inchangées ; contrôles étroit et global réussis, reconstruction exacte des 187 exports, aucun essai en jeu. Les fonctions navales ont ensuite été corrigées, approuvées et intégrées.

## Fonctions navales : lot corrigé approuvé le 9 octobre 2026

Trois [masters exacts, prompts et recettes](naval_equipment_naval_functions_sources_2026-10-09/manifest.json) : chaloupe bleue, cordon de trois voiliers bronze v2, batterie côtière rouge. L’ancien blocus à chaîne métallique est exclu de l’export. Trois DDS 120 × 120 / sept mipmaps et quatre liens seulement : les deux fonctions de débarquement partagent la chaloupe sans fusion de leurs statistiques. Les palettes des fonctions natives, originaux et alpha sont conservés sans retouche. Registre total à cette étape : 190, trente-neuf dessins navals uniques couvrant quarante modules. Contrôles étroit, global et reconstruction exacte réussis, aucun essai en jeu. L’éperon d’étrave a ensuite été approuvé et intégré.

## Fonctions navales : éperon d’étrave et clôture le 9 octobre 2026

Un [master exact, prompt et recette](naval_equipment_galley_boarding_spur_sources_2026-10-09/manifest.json) : éperon d’étrave bleu, original et alpha conservés sans retouche. Un DDS natif 120 × 120 avec sept mipmaps, un seul lien `aor_galley_boarding_spur`. Statistiques, coûts, technologies et flottes inchangés ; contrôles étroit et global réussis. Registre total : 191 exports reconstructibles à l’identique. Les 36 choix principaux et cinq fonctions des coques primitives disposent de leurs 40 dessins uniques approuvés, la chaloupe étant partagée entre deux fonctions. Aucun visuel restant pour ces modules. Aucun essai en jeu ou redémarrage par l’agent ; vérification du rendu confiée au joueur.
