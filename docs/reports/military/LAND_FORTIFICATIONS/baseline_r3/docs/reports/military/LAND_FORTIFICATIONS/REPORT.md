# Fortifications terrestres

19 octobre 2026 — révision R2 — **LAND_FORTIFICATIONS_READY_FOR_RUNTIME_VALIDATION**

Ajout d’un bâtiment public de **Fortifications terrestres**, constructible uniquement dans les États **sans littoral**, avec un **plafond natif de cinq niveaux par État**. Les fortifications navales existantes sont inchangées. L’icône fournie par l’utilisateur est intégrée après retrait du fond blanc extérieur ; les trois méthodes conservent les icônes navales demandées.

**924/924 contrôles statiques réussis.** Les 1 953 fichiers existants protégés sont identiques à leur état au début de cette passe. La correction R2 protège aussi 1 965 fichiers, dont les méthodes, les déblocages, le plafond et l’icône. Le vanilla canonique, HEAD et l’index Git sont inchangés. [Résultats et scénarios](VALIDATION.json). **Essai en jeu : non effectué.** Les calculs de scénario évaluent les scripts écrits, sans exécuter Victoria 3.

La [passe préalable](AUDIT.md) relève les statistiques navales, les effets à retirer, les sources vanilla et le calibrage initial. Sur instruction de l’utilisateur, R2 applique les valeurs annoncées à **un niveau**, avec une réduction territoriale des fortifications plafonnée à **85 %**. Les résultats antérieurs sont conservés dans `history/R1/` et les fichiers précédant cette correction dans `baseline_r2/`.

## Bâtiment et méthodes

| Élément | Fortifications terrestres |
|---|---|
| Construction | Technologie **Fortification et poliorcétique**, comme le fort naval du mod |
| Limite | 5 niveaux par État, via `has_max_level` et le modificateur natif de plafond |
| Localisation autorisée | `is_coastal = no`, inverse de la condition navale |
| Groupe | Armée ; financement public ; pas de recrutement gratuit de bataillons |
| Construction / infrastructure | Même coût très faible que le fort naval ; 0,2 infrastructure par niveau ; pas d’économie d’échelle |
| Méthodes | Simples, renforcées, avancées ; mêmes icônes, emplois et biens consommés que les correspondantes navales |

| Méthode | Technologie supplémentaire | Emplois par niveau | Biens par niveau à effectif complet |
|---|---|---|---|
| Simples | Aucune au-delà du bâtiment | 900 soldats + 100 officiers | 5 armes légères, 5 fer |
| Renforcées | **Forts casematés** | 850 soldats + 150 officiers | 5 armes légères, 3 artillerie, 5 acier |
| Avancées | **Fortifications en béton** | 800 soldats + 200 officiers | 5 armes légères, 5 artillerie, 5 munitions, 10 acier |

Les emplois représentent la garnison du bâtiment, comme pour les forts navals. Ils ne créent ni unités de combat, ni commandants, ni conscrits supplémentaires. Aucun bâtiment initial n’a été ajouté à l’historique : le joueur et l’IA peuvent construire le nouveau type après déblocage.

Le plafond de cinq est ajouté à la **même technologie qui débloque déjà le bâtiment naval**. Cette addition fournit le plafond dynamique du nouveau type sans modifier les prérequis, les ères, les coûts ou les autres technologies, et sans introduire une initialisation récurrente par événement. Les USA, leurs lois, unités et technologies de départ ne sont pas modifiés.

## Effets terrestres

Les cinq effets maritimes sont exclus : protection contre les débarquements, soutien au combat naval, résistance au bombardement, résistance au blocus et contrôle des détroits.

À **un niveau et garnison complète**, la protection est :

| Méthode | Provinces perdues après défaite défensive | Pertes subies | Défense terrestre |
|---|---:|---:|---:|
| Simples | −10 % | −5 % | +5 % |
| Renforcées | −20 % | −10 % | +10 % |
| Avancées | −30 % | −15 % | +15 % |

À **cinq niveaux et garnison complète**, le cumul devient :

| Méthode | Provinces perdues après défaite défensive | Pertes subies | Défense terrestre |
|---|---:|---:|---:|
| Simples | −50 % | −25 % | +25 % |
| Renforcées | −85 % | −50 % | +50 % |
| Avancées | −85 % | −75 % | +75 % |

Un niveau complet apporte respectivement 1, 2 ou 3 points de puissance. Chaque point donne −10 % de provinces perdues, −5 % de pertes et +5 % de défense. La contribution territoriale des fortifications est plafonnée à −85 % dans toutes les positions, y compris les variantes de poursuite et de retraite. Les pertes humaines et la défense conservent leur cumul jusqu’aux quinze points permis par cinq niveaux avancés. Les coûts et emplois sont inchangés.

La puissance est proportionnelle à l’effectif employé selon le mécanisme natif `workforce_scaled`, puis arrondie au point le plus proche pour sélectionner une condition de bataille, jusqu’à 15 points. Moins de 0,5 point ne fournit aucune protection. Une garnison presque pleine ne perd ainsi pas un palier entier pour quelques postes vacants. L’écart maximal d’arrondi, avant application du plafond, est de 5 points de pourcentage sur les provinces et de 2,5 sur les pertes ou la défense.

Les champs de combat sont **natifs** : `unit_provinces_lost_mult`, `battle_casualties_mult` et `unit_army_defense_mult`. Les valeurs R2 suivent le calibrage fort demandé par l’utilisateur, et non des valeurs attribuées à un bâtiment terrestre vanilla préexistant. Les réductions sont relatives aux calculs du moteur : elles ne garantissent pas un nombre fixe de provinces, de morts ou de blessés. Le plafond de 85 % porte sur le bonus des fortifications ; les autres modificateurs applicables, comme Liberty Or Death, conservent leurs règles de cumul natives.

## Portée locale et déroulement du combat

La protection est portée par une **condition du côté de bataille**, avec les gardes suivantes :

- côté défendant ;
- province possédée **et contrôlée** par le pays de ce côté ;
- État de cette province appartenant au même pays et sans littoral ;
- bâtiment de fortification terrestre présent et puissance suffisante.

Un attaquant, un occupant ennemi, une garnison vide, un fort démoli ou un combat ailleurs ne reçoit donc pas ce soutien. La règle de propriété est stricte : un pays allié qui représente lui-même le côté de bataille dans le territoire d’un autre propriétaire ne reçoit pas le bonus. Ce point doit être observé dans les batailles à plusieurs pays lors de la validation.

Dans un combat éligible, le côté défendant utilise la condition **Position fortifiée**. Elle prend la place du tirage ordinaire de manœuvre de ce côté : ce n’est pas un bonus permanent national ajouté à toutes les conditions tactiques. Les conditions natives **poursuite**, **déroute** et **retraite contrôlée** disposent toutefois de variantes fortifiées qui conservent intégralement leurs statistiques et leurs poids tout en ajoutant la protection locale. Les pénalités d’une déroute et les mécanismes de repli ne sont pas effacés par le fort.

Les références à ces trois états tactiques reconnaissent leurs équivalents fortifiés, y compris lorsque l’ennemi est concerné. Un changement de palier remappe la condition. Une disparition de la protection remappe une retraite vers son équivalent natif, ou retire le bonus de la position fortifiée au prochain contrôle natif. Aucun modificateur temporaire n’est attaché au pays ou au commandant, aucun drapeau de combat n’est enregistré, aucune impulsion quotidienne n’est ajoutée.

Cela nécessite une adaptation de `common/battle_conditions/00_battle_conditions.txt`, absente du mod au début de la passe. Les 21 conditions canoniques sont conservées. Leurs valeurs et poids sont inchangés ; leurs gardes permettent le parcours fortifié et les trois équivalences de retraite. Hors contexte fortifié, les projections retrouvent les conditions possibles et transitions natives. Les 61 nouvelles définitions comprennent 15 paliers de position, 45 variantes de transition et une condition de sortie sans bonus. Elles sont générées de façon reproductible depuis le vanilla canonique local, avec une empreinte de source contrôlée.

## Icône et localisation

L’icône du bâtiment utilise le dessin fourni, détouré avec **l’outil intégré image_gen**, puis converti sans nouvelle retouche en **DDS BGRA8, 256 × 256, neuf niveaux de mipmap**, comme l’icône navale canonique. Les quatre coins sont entièrement transparents. L’alpha retourné par l’outil est préservé, y compris son intérieur presque opaque.

- [Icône utilisée par le jeu](../../../../gfx/interface/icons/building_icons/building_aor1776_land_fortification.dds)
- [Aperçu du DDS décodé](ICON_PREVIEW.png)
- [Sources, outil et consigne exacte de détourage](ASSET.md)

Le bâtiment, le groupe, les méthodes, les types de modificateur et les conditions ont des textes FR/EN avec BOM UTF-8, clés uniques et références vérifiées. Les icônes de méthode restent celles des trois méthodes navales ; aucune localisation navale existante n’est renommée.

## Fichiers du lot

Créés :

- `common/buildings/1776_land_fortifications.txt`
- `common/building_groups/1776_land_fortifications.txt`
- `common/production_methods/1776_land_fortifications.txt`
- `common/production_method_groups/1776_land_fortifications.txt`
- `common/modifier_type_definitions/1776_land_fortifications.txt`
- `common/scripted_triggers/1776_land_fortifications.txt`
- `common/battle_conditions/00_battle_conditions.txt` — adaptation du fichier canonique, générée
- `common/battle_conditions/1776_land_fortifications.txt` — variantes locales générées
- `localization/french/1776_land_fortifications_l_french.yml`
- `localization/english/1776_land_fortifications_l_english.yml`
- l’icône DDS et les deux PNG conservés dans `workshop_assets/source/`
- les outils `build_land_fortification_battles.py`, `build_land_fortification_icon.py`, `validate_land_fortifications.py`.

Modification existante : `common/technology/technologies/20_tech3a_military.txt`, ajout du seul plafond de cinq à `scientific_fortification_siegecraft`. L’index des rapports reçoit un lien. [Manifeste et empreintes](MANIFEST.json).

## Vérification et points à éprouver en jeu

Les 924 vérifications couvrent syntaxe, références, ressources, emplois, technologies, plafond déclaré, absence d’effets navals, portée de propriété et contrôle, effectifs partiels, arrondis, plafonnement, 15 paliers, maintien des retraites, suppression du soutien perdu, équivalence des contextes non fortifiés, localisation, export de l’icône et préservation des autres fichiers. R2 vérifie également les valeurs réelles de chaque méthode aux niveaux 1 à 5, le plafond territorial de 85 % dans les 60 conditions fortifiées et la conservation des autres règles. Les scénarios évaluent l’AST réel des conditions avec des faits de bataille fournis. Ils ne simulent pas les combats.

Restent à confirmer dans Victoria 3 : le plafond dans l’interface et la file de construction, les effets des technologies déjà acquises dans une ancienne sauvegarde, la valeur de puissance issue d’une vraie garnison, le choix et le changement des conditions, le calcul effectif des pertes et provinces à la défaite, l’IA et le budget. Un changement d’un autre mod sur le même fichier canonique des conditions demande une fusion explicite ; la génération ne suppose pas qu’un ordre de chargement résolve ce conflit.

Le [protocole de validation](RUNTIME_VALIDATION.md) indique les essais à réaliser. Aucune clôture moteur n’est revendiquée. Les chantiers territoriaux et impériaux n’ont pas été ouverts ou modifiés par ce lot.
