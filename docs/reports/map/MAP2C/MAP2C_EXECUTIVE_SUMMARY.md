# MAP-2C — Vénétie et Provence / Avignon

11 octobre 2026. Retouche appliquée au dossier de travail, sans commit, merge ni push.

## Résultat

Deux contours locaux ont été repris dans le bitmap natif des provinces. Les identifiants RGB et leurs rattachements aux State Regions restent les mêmes : aucun nouvel État, pays ou sujet n'est créé. Les populations, bâtiments et unités des subdivisions politiques existantes sont conservés intégralement.

### Provence / Avignon

- La subdivision pontificale `xB0C0E0` est réduite de **257 à 173 pixels**. La grande pointe vers le sud-est rejoint les subdivisions françaises voisines ; le contour est recentré vers Avignon et le Comtat.
- **112 pixels** précédemment pontificaux deviennent français et **28 pixels** de la subdivision française septentrionale rejoignent le contour pontifical. Cela représente 140 pixels retouchés, et non un transfert de provinces entières.
- Les RGB français `x31C0DF`, `xB040E0` et `xC03918` restent chacun d'un seul tenant. Le RGB pontifical, auparavant constitué d'un corps de 256 pixels et d'un pixel isolé, forme désormais un seul ensemble.
- La portion PAP reçoit le nom **Avignon et Comtat Venaissin**, avec traduction anglaise. Le nom général **Provence**, la Provence française et Nice sarde sont conservés.
- La State Region partagée est maintenue. Aucun port ni locator n'est déplacé. Le locator physique d'Avignon reste dans la portion PAP.

Les **99 500 habitants** pontificaux restent exactement les mêmes : 96 000 Occitans, 2 000 Français et 1 500 Séfarades. Les groupes français et sardes ne changent pas non plus. Les six niveaux de soie et quatre de coton français, ainsi que tous les autres bâtiments, restent dans leurs historiques précédents.

### Complément demandé : droits de transit franco-pontificaux

Un traité actif dès le **1er janvier 1776** accorde aux États pontificaux les **droits de transit commerciaux à travers la France**, avec un seul article `transit_rights`, `source_country = c:FRA` et `target_country = c:PAP`. Il ne contient ni accès militaire, ni union douanière, ni transfert de souveraineté. Son nom est localisé en français et en anglais. L'arrangement est explicitement un réglage demandé pour le jeu, sans inventer une convention historique signée à une date précise.

Le verrou de retrait est de cinq ans ; ce n'est pas une expiration automatique du traité. L'entretien standard de l'article est de **50 points d'influence**, payé par PAP. Les valeurs natives de l'article ne sont pas changées.

**Attention à la distinction entre les deux marchés** : la définition native `common/treaty_articles/24_transit_rights.txt` et la localisation anglaise `transit_rights_effects_desc` portent sur l'accès aux **plaques tournantes du marché mondial** français. Elles ne garantissent pas un raccordement interne Avignon–Latium. Le traité demandé est bien installé, mais une connexion au marché intérieur pontifical ne sera pas annoncée comme résolue sans observation en jeu. Aucun port artificiel ni autre accord n'est ajouté pour masquer cette limite.

### Venise / Frioul

- Le RGB autrichien `x56C78A` englobait les locators d'**Udine** et de **Gorizia**, alors que ces villes relevaient de souverainetés différentes en 1776.
- **102 pixels occidentaux** rejoignent le RGB vénitien voisin `x108021`. Le contour de ce dernier passe de 166 à 268 pixels. Les 84 pixels restants de `x56C78A` gardent Gorizia côté autrichien.
- La définition du hub minier d'Udine passe de `x56C78A` à `x108021`, sans modifier sa position graphique. Le hub forestier de Gorizia conserve `x56C78A`. Trieste et les autres attributions MAP-2B ne changent pas.
- La partie vénitienne de la région partagée est nommée **Frioul et Istrie vénitiens**. Sa partie autrichienne reçoit le nom descriptif **Littoral habsbourgeois** : cela ne crée pas le territoire administratif formalisé au XIXe siècle.
- **Vénétie** est explicitement conservé comme nom de l'État principal vénitien. Pour le pays, le remplacement du nom par celui de la capitale est désactivé. La règle républicaine déjà existante affiche **Sérénissime République de Venise**, avec traduction anglaise. Les lois et la logique du nom dynamique ne sont pas changées.

Les anciennes répartitions démographiques sont conservées : 340 246 habitants dans la portion vénitienne de `STATE_ISTRIA`, 339 850 dans sa portion autrichienne. Une retouche de pixels ne constitue pas un nouveau recensement ni une migration de ces groupes. La Lombardie, le Trentin et les dépendances politiques ne sont pas réouverts.

## Preuves historiques et limites

La frontière vénéto-habsbourgeoise comportait de nombreuses enclaves, et l'accord de 1756 n'en supprimait pas la complexité. Le contour retenu est une **approximation documentée à l'échelle du jeu**, séparant Udine vénitienne et Gorizia habsbourgeoise ; ce n'est pas le tracé exact de chaque village. Sources : [frontière de 1521 à 1797, Institut régional FVG](https://www.regionestoriafvg.eu/tematiche/tema/240/Confine-tra-Venezia-e-Austria), [chronologie de l'époque moderne](https://www.regionestoriafvg.eu/tematiche/tema/274/Moderna).

Pour Avignon et le Comtat, la carte conservée par les [Archives départementales de Vaucluse](https://memento.vaucluse.fr/toutes-les-ressources/revendication-de-propriete-sur-le-rhone) sert à vérifier l'organisation générale du territoire et son rapport au Rhône. La référence à l'[occupation française de 1768–1774](https://francearchives.gouv.fr/subject/30298779) est cohérente avec le maintien pontifical de 1776. [L'histoire municipale d'Orange](https://www.ville-orange.fr/article234.html) rappelle son rattachement antérieur à la France : Orange n'est pas ajouté au domaine pontifical.

Les scans historiques ne sont pas présentés comme des cadastres de 1776 géoréférencés au pixel près. Les positions techniques du jeu ont été distinguées des coordonnées réelles des villes. L'interprétation du contour est qualitative, confrontée aux localités et au réseau physique ; aucun résidu ou score de précision artificiel n'est annoncé. Valréas et les petites enclaves du Comtat, les enclaves frioulanes, Pazin et certains secteurs mixtes restent simplifiés. Ces limites sont répertoriées dans `MAP2C_UNRESOLVED.csv`.

## Validations réalisées

- **PASS statique** : comparaison avant/après de l'ensemble de l'inventaire des propriétaires, State Regions, groupes culturels/religieux, commandes de bâtiments, niveaux écrits et unités.
- Population mondiale écrite : **835 804 980 avant et après**, différence **0**. Aucun groupe démographique supprimé, dupliqué ou déplacé.
- Bitmap RGB natif : **8192 × 3616**, mêmes **40 875 couleurs**, mêmes identifiants de province, aucun pixel de mer ou de côte recoloré. **242 pixels terrestres** changés, exclusivement dans les deux zones visées. Les six RGB touchés sont contigus après retouche.
- Définitions d'États : seul le RGB du hub minier d'Udine change. Ressources, rattachements, capitales des autres pays et règles de la Lombardie et du Tyrol sont conservés.
- Localisations FR/EN présentes avec encodage UTF-8 BOM ; branches préexistantes du script de nommage conservées. Les hooks de démarrage et de changement de propriétaire déjà utilisés sont inchangés.
- Empreintes de **1 967 fichiers** de référence contrôlées : **1 962 inchangées** ; cinq fichiers existants modifiés intentionnellement et quatre nouveaux fichiers runtime. Les rapports MAP-1C / MAP-2A / MAP-2B et l'instantané de révision démographique sont intacts.
- Les 62 anciennes doubles attributions RGB et les 14 anciennes anomalies de références sont identiques au point de départ. Elles ne sont pas présentées comme résolues par cette retouche locale.
- Le locator forestier hérité de Provence comporte déjà une divergence entre sa position physique et sa définition. Il reste inchangé et est signalé dans le manifeste des limites.
- Les trois CSV sont vérifiés cellule par cellule, avec contrôle des différences démographiques et inspection de leurs aperçus.
- Traité vérifié : un seul article commercial FRA → PAP dans les historiques effectifs, pas de doublon, date initiale et localisations correctes. Tous les traités préexistants et les dépendances politiques restent inchangés.

### Vérification en jeu à faire

**Aucun chargement natif après MAP-2C n'a été réalisé.** Les aperçus du dossier sont des vues techniques du bitmap, pas des captures de Victoria 3. Relancer le jeu et ouvrir une **nouvelle partie en 1776** pour vérifier le chargement de la carte, les noms, les contours d'Avignon et du Frioul, les ports, le traité franco-pontifical, l'accès au marché mondial et l'accès au marché intérieur du Latium. Ces deux derniers indicateurs doivent être relevés séparément. Les observations positives de la version précédente ne constituent pas un test de cette nouvelle géométrie.

## Fichiers runtime modifiés

1. `map_data/provinces.png` — nouvelle surcharge locale du bitmap effectif vanilla, avec seulement les pixels documentés modifiés.
2. `map_data/state_regions/01_south_europe.txt` — RGB du hub minier d'Udine.
3. `common/country_definitions/00_countries.txt` — uniquement le drapeau de nom dérivé de la capitale pour VEN, en conservant les modifications locales antérieures du fichier.
4. `common/scripted_effects/1776_alpine_state_names.txt` — nommage ciblé de Vénétie et du Comtat, sans supprimer les règles antérieures.
5. `localization/french/1776_alpine_state_names_l_french.yml`.
6. `localization/english/1776_alpine_state_names_l_english.yml`.
7. `localization/french/replace/1776_map2c_l_french.yml`.
8. `localization/english/replace/1776_map2c_l_english.yml`.
9. `common/history/treaties/1776_avignon_transit_rights.txt` — seul complément diplomatique, expressément demandé après la retouche cartographique.

Les scripts de travail et les preuves sont distincts des fichiers chargés par le jeu. L'état antérieur est sauvegardé dans `MAP2C_BASELINE.json`, `MAP2C_PATCH_INPUTS.json` et le bitmap effectif byte-exact `MAP2C_GEOGRAPHIC_EVIDENCE/provinces_before.png`.

## Livrables

- `MAP2C_TERRITORIAL_CHANGES.csv` : pixels et noms modifiés, propriétaires, sources et limites.
- `MAP2C_POPULATION_VALIDATION.csv` : tous les groupes démographiques des cinq régions concernées ou immédiatement protégées, avant/après et différence.
- `MAP2C_UNRESOLVED.csv` : approximations maintenues, anomalies antérieures et test natif restant.
- `MAP2C_VALIDATION.json` : résultats reproductibles, empreintes du bitmap et contrôle des locators.
- `MAP2C_GEOGRAPHIC_EVIDENCE/` : comparatifs avant/après, scans de référence, grille physique et changements RGB détaillés.

**Aucun commit, merge ni push effectué. Aucun historique de population, bâtiment, armée, technologie, loi ou journal modifié dans cette phase. Les accords diplomatiques préexistants sont intacts ; seul le nouveau traité de transit demandé a été ajouté.**
