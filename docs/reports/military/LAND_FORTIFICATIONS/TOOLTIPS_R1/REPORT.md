# Fortifications terrestres et génie — fiches chiffrées

Statut : contrôles statiques réussis ; rendu et comportement moteur non testés.

## Demande appliquée

Les valeurs occupent désormais trois lignes de modificateurs dans les infobulles natives. Le marqueur unique « Puissance des fortifications terrestres » disparaît. Les descriptions françaises et anglaises expliquent la portée locale des effets sans porter leur liste principale.

| Méthode du fort | Provinces perdues | Pertes subies | Défense |
| --- | ---: | ---: | ---: |
| Simple, par niveau à garnison complète | −5 % | −5 % | +5 % |
| Renforcée, par niveau à garnison complète | −10 % | −10 % | +10 % |
| Avancée, par niveau à garnison complète | −15 % | −15 % | +15 % |

Chaque bataillon du génie affiche trois réductions de −1 % : protection du terrain des forts adverses, protection contre les pertes des forts adverses et bonus de défense des forts adverses. Il s’agit d’un point de pourcentage par millier d’hommes effectivement engagé, explicité au survol de chaque statistique. Les trois lignes sont bénéfiques, donc vertes. Les coûts d’entretien restent rouges dans la présentation native.

À la demande complémentaire du joueur, le génie perd ses quatre statistiques ordinaires : attaque +15, défense +20, perte de moral +10 et efficacité d’invasion navale −25 %. Son bloc de statistiques de bataille ne contient plus que les trois lignes de neutralisation des forts. Entretien, effectif maximal, groupe indépendant, technologie et sept variantes d’illustrations sont conservés. Aucun malus de déplacement n’est ajouté.

## Réalisation et limites

- Les six nouvelles grandeurs utilisent des types `script_only`, avec `percent = yes` et une couleur adaptée au signe. Le jeu peut donc les lister via ses descriptions natives de modificateurs, sans surcharge de fenêtre GUI.
- Les trois sorties du fort sont locales et proportionnelles à la garnison. Les statistiques natives de combat restent appliquées uniquement par la condition défensive admissible : propriétaire et contrôleur de la province, propriétaire du fort, État intérieur. Les marqueurs ne doublent pas ces bonus.
- La protection territoriale affichée remplace l’ancienne force interne comme entrée du calcul. La conversion par −20 conserve l’arrondi historique à un point de force, puis la multiplication par cinq. Les deux autres sorties rendent lisibles les deux autres effets, identiques en amplitude et vérifiés contre les conditions générées.
- Les lignes du génie décrivent le compteur existant ; elles ne sont pas un malus global aux forts ennemis. Le compteur continue de lire les effectifs et le type des unités réellement engagées. Les 301 conditions de fort et les 21 conditions vanilla conservent les mêmes valeurs et fichiers qu’avant cette passe.
- L’affichage présente les valeurs avant le contre adverse. À garnison partielle, les sorties proportionnelles peuvent différer de la protection effective arrondie par pas de cinq points. Cette précision figure au survol. Les coefficients ne peuvent devenir une pénalité quand le fort est entièrement neutralisé.

## Vérifications

- `tools/validate_land_fortifications.py` : **2 096 / 2 096** contrôles réussis, dont valeurs affichées comparées aux effets de bataille, signes/couleurs, suppression des statistiques ordinaires, seuils 25/50/75, effectifs partiels, camps alliés/adverses, retraites natives et illustrations.
- `tools/validate_land_fortification_construction.py` : **168 / 168** contrôles réussis. Base de 900 points, efficacité progressive et événements de suivi conservés.
- **2 023 fichiers protégés** inchangés contre le relevé de début de passe, notamment carte, institutions impériales, données navales, illustrations et sources de construction.
- Localisations FR/EN : clés résolues et uniques, UTF-8 BOM et retours de ligne conservés.
- Git HEAD et index inchangés ; vanilla consulté en lecture seule.

Ces contrôles projettent les scripts ; ils n’exécutent pas le moteur. Il reste à observer en jeu les fiches du génie et les aperçus de construction/PM du fort, puis une bataille avec des sapeurs. Après rechargement des scripts, les trois lignes doivent apparaître directement parmi les valeurs, les dépenses restant dans leur section native. Vérifier aussi la réévaluation des sorties de PM lors du chargement d’une ancienne sauvegarde.

## Références locales analysées

- `C:/Games/Victoria 3/game/common/modifier_type_definitions/modifier_types.md` : portée par préfixe, pourcentages, décimales et couleurs.
- `C:/Games/Victoria 3/game/common/modifier_type_definitions/03_modifier_types_script_only.txt` : modificateurs natifs de conditions de bataille déclarés `script_only`.
- `C:/Games/Victoria 3/game/localization/french/customized_tooltips_l_french.yml`, `DATA_COMBAT_UNIT_TYPE_NAME_TOOLTIP` : lecture de `CombatUnitType.GetBattleModifier.GetDesc` avant l’entretien et la description.
- `C:/Games/Victoria 3/game/gui/custom_tooltip.gui`, `FancyTooltip_CombatUnitTypeWithoutCulture` et `FancyTooltip_CombatUnitTypeWithCulture` : même contenu natif de statistiques.

Le relevé initial et les rapports de validation précédents restent dans ce dossier. `MANIFEST.json` donne les fichiers créés/modifiés et les empreintes avant/après ; `VALIDATION.json` récapitule les deux validations de cette passe.
