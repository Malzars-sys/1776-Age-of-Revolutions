# Équipements des navires primitifs — intégration du 8 octobre 2026

Statut : **définitions, descriptions, fonctions et déblocages intégrés ; les 36 choix principaux et les cinq fonctions utilisent leurs dessins approuvés. Aucun visuel restant pour ces 41 modules. Aucun essai en jeu.**

La validation du joueur remplace les anciens intitulés génériques par des techniques, gréements et systèmes d’armes identifiables. Les nombres de pièces sont des configurations de jeu, pas des inventaires attestés de navires nommés.

## Quatre catégories et trois choix

### Caravelle

| Catégorie | Bronze | Argent | Or |
| --- | --- | --- | --- |
| Coque / charpente | Bordage à franc-bord sur membrures | Couples doubles et serre-bauquières | Charpente à renforts diagonaux |
| Armement | 8 fauconneaux pivotants de 2 livres | 12 canons longs de 6 livres sur affûts à roulettes | 8 carronades de 12 livres sur glissières |
| Propulsion | Grand-voile carrée | Grand-voile et hunier | Grand-voile, hunier et perroquet |
| Aménagements / réserves | Tonneaux de vivres en cale | Gaillard arrière et cambuse séparée | Faux-pont de campagne et soutes à eau |

### Galère

| Catégorie | Bronze | Argent | Or |
| --- | --- | --- | --- |
| Coque / charpente | Bordage léger à franc-bord | Serres longitudinales et traverses de nage | Quille doublée et carlingue continue |
| Armement | 1 pièce de proue de 6 livres et 2 pierriers | 1 canon de chasse de 12 livres et 2 canons de 3 livres | 1 canon axial de 24 livres et 2 canons de 6 livres |
| Propulsion | Nage alla sensile : avirons séparés | Nage a scaloccio : aviron collectif | Nage a scaloccio et deux voiles latines |
| Aménagements / réserves | Coffres de banc et outres d’eau | Tonneaux sous coursie | Cambuse de poupe et avirons de rechange |

### Cogue

| Catégorie | Bronze | Argent | Or |
| --- | --- | --- | --- |
| Coque / charpente | Bordage à clins riveté | Varangues liées à une carlingue | Serres de cale et baux traversants |
| Armement | 4 pierriers pivotants de 1 livre | 4 canons longs de 3 livres | 4 carronades de 6 livres |
| Propulsion | Mât unique et voile carrée | Voile carrée à bandes de ris | Grand-voile carrée et hunier |
| Aménagements / réserves | Cale libre et logements sur le pont | Faux-pont de couchettes et râteliers | Pont de troupes et panneaux de chargement |

## Fonctions choisies et cumul

- Cogue : chaloupes de débarquement ; efficacité d’invasion +10 % et capacité de débarquement +0,1.
- Caravelle : organisation de blocus (+35 % de force de blocus) **et** chaloupes/détachement de débarquement (+10 % d’efficacité, +0,1 de capacité, −2 de réserve). Deux emplacements compatibles, actifs par défaut.
- Galère : batterie de combat côtier (+15 % de dégâts de coque, +1 de précision) **et** éperon d’étrave pour l’abordage (+20 % de dégâts d’équipage, +0,05 de capacité de débarquement, −0,1 de vitesse). Deux emplacements compatibles, actifs par défaut.
- L’éperon est une saillie d’étrave au-dessus de l’eau destinée à l’approche et à l’abordage, pas un bélier sous-marin moderne.

La portée de la galère reste **1**, avec **−80 % de dégâts de coque et d’équipage hors de portée**, comme le mécanisme de défense côtière natif. Aucun équipement ne supprime cette contrainte.

## Coûts et équipement par défaut

Les quatre catégories commencent explicitement au niveau bronze ; leurs suppléments de caractéristiques et de biens sont nuls à ce niveau. Les coûts de construction, les équipages et le ravitaillement de base des coques sont conservés. Les fonctions sélectionnées ajoutent de faibles coûts de bois, tissu, outils ou fer à la construction/réfection. Le coût de chantier ajoute 0,5 par niveau de modification. Les niveaux supérieurs ajoutent des biens et des caractéristiques modestes ; aucun moteur, charbon, acier moderne ni obus n’est exigé, et aucun nouvel entretien matériel n’est caché dans les modules.

Ces valeurs ne garantissent pas un budget national précis : coûts de chantier, prix, salaires et consommation doivent encore être observés dans le moteur.

## Technologies et départ

| Technologie | Ère | Prérequis |
| --- | ---: | --- |
| Construction maritime à clins | 1 | Début de branche |
| Construction de galères | 1 | Début de branche |
| Gréements océaniques | 1 | Construction maritime à clins |
| Construction de frégates | 2 | Gréements océaniques, scientific_naval_architecture |
| Construction de vaisseaux de ligne | 3 | Construction de frégates, ship_classification_surveying |
| Carronades sur glissières | 4 | Construction de frégates, armament_standardization_inspection |
| Charpente navale diagonale | 5 | Construction de vaisseaux de ligne |

Frégates et vaisseaux de ligne disposent désormais de portes technologiques dédiées. Seules France, Grande-Bretagne, Espagne, Russie, Portugal, Pays-Bas, Danemark-Norvège et Suède en disposent au départ, avec prise en charge des tags Danemark/Norvège séparés lorsqu’ils existent. Les autres nations pourront les rechercher. Les sciences navales partagées ne sont pas retirées.

Les deux technologies de carronades et de charpente diagonale ne sont accordées à **aucun** pays au départ. Elles distinguent les adaptations tardives des systèmes anciens au lieu de changer seulement les mots ou la couleur du bouton.

Les flottes du Brésil, des Indes néerlandaises, de Sardaigne, des Deux-Siciles, de l’Empire ottoman et de Venise avaient encore des classes avancées : elles passent à des coques primitives autorisées. Le nombre de navires de chaque flotte est strictement conservé. Les flottes des puissances autorisées ne sont pas retouchées.

Les pays possédant une flotte initiale ou la technologie des arsenaux navals reçoivent les connaissances de construction primitive. Les prérequis manquants des classes avancées sont ajoutés uniquement aux pays autorisés. Armées, populations, administrations, bâtiments et propriété coloniale sont protégés contre tout changement dans cette passe.

## Rééquipement et succession

Le rééquipement permet d’améliorer les modules d’une même coque. Les successions caravelle → vaisseau de ligne, galère → défenseur côtier et cogue → transport moderne ne constituent **pas** une conversion native confirmée entre types ; elles nécessitent pour l’instant la construction de la coque successeure. Aucun faux champ de conversion n’a été ajouté.

## Visuels : les quatre catégories de caravelle intégrées

Les quatre catégories des trois navires utilisent désormais les dessins approuvés : trente-six icônes. Quatre autres images approuvées couvrent les cinq fonctions, avec une chaloupe partagée entre cogue et caravelle. Les quarante et une définitions ont donc leur visuel dédié, sans pictogramme générique restant pour ces modules.

Trois propositions de l’armement de caravelle ont été créées avec la compétence imagegen et le générateur intégré, en utilisant une planche des icônes navales natives comme référence de style : fauconneau bronze, canon long argent, carronade or. Leurs masters bruts approuvés sont conservés dans `docs/reports/assets/naval_equipment_armament_sources_2026-10-08/`. Le recadrage des marges transparentes, le redimensionnement et les mipmaps servent à l’export natif ; couleurs et alpha ne sont pas retouchés.

Le joueur a approuvé le premier lot avec « le premier lot est aprouve tu peut passé au lot de la coque ». Les originaux approuvés, y compris le léger halo argent, ont été conservés sans retouche ; les deux variantes argent écartées ne sont pas utilisées. Les [masters, prompts et recettes d’export](../assets/naval_equipment_armament_sources_2026-10-08/manifest.json) sont verrouillés par SHA-256. Trois textures DDS natives BGRA8 de 120 × 120 pixels avec sept mipmaps ont été ajoutées ; seuls trois champs `icon` ont changé, aucune caractéristique ni recette. Le registre comporte 154 exports, les 151 précédents sont inchangés. Validation exacte : `tools/integrate_naval_equipment_art.py check` et `tools/rebuild_asset_icons.cjs --verify`. Les coques seront proposées avant intégration.

## Coques de caravelle : lot validé et intégré

Trois charpentes validées par « Hop, je valide le lot, tu peux passer au suivant. À savoir la propulsion. » : franc-bord sur membrures simples en bronze, couples doubles et serre-bauquières en argent, renforts diagonaux en or. Dessins en coupe simplifiée, sans coque métallique. Les [masters, prompts et recettes](../assets/naval_equipment_hull_sources_2026-10-08/manifest.json) sont conservés ; trois DDS natifs 120 × 120 avec sept mipmaps sont liés exclusivement aux `aor_caravel_armor_*`. Le halo des originaux validés est conservé ; les tentatives de détourage écartées ne sont pas consommées. Statistiques, coûts, technologies, armées et départs inchangés dans cette passe. Le registre totalise 157 exports reconstructibles, les 154 précédents sont préservés. Contrôle : `tools/integrate_naval_equipment_art.py check --lot hull`. Le validateur global protège les six changements d’icône autorisés et toutes les définitions de jeu.

## Gréement vertical de caravelle : lot validé et intégré

Le premier lot horizontal a été refusé : il ajoutait des mâts plutôt que des étages de voiles. La [révision verticale v2](caravel_propulsion_art_proposals_v2_2026-10-08.json) a été approuvée par « Hop, tu peux intégrer et passer au jeu suivant, le pont. ». Les trois originaux sont conservés sans retouche dans le [pack source avec prompts et recettes d’export](../assets/naval_equipment_propulsion_sources_2026-10-08/manifest.json). Un seul mât central : grand-voile en bronze, grand-voile et hunier en argent, grand-voile, hunier et perroquet en or. Trois DDS natifs 120 × 120 avec sept mipmaps remplacent exclusivement les icônes `aor_caravel_propulsion_*`. Les trois noms et descriptions sont adaptés en français et en anglais avec BOM préservé. Statistiques, coûts et technologies inchangés. Les 157 exports antérieurs restent exacts ; registre total : 160. Contrôle de passe : `tools/integrate_naval_equipment_art.py check --lot propulsion`. Les formes sont des symboles, pas des plans historiques complets de gréement. Un halo extérieur reste présent dans les originaux approuvés.

## Pont et approvisionnement de caravelle : lot validé et intégré

Lot approuvé par « Tu peux intégrer et passer au lot suivant. » : bronze et or originaux, argent v5 avec caisse et tonneau refaits sur la structure validée. Les [masters exacts, prompts et recettes](../assets/naval_equipment_deck_sources_2026-10-08/manifest.json) sont conservés sans retouche. Trois DDS 120 × 120 avec sept mipmaps remplacent exclusivement `aor_caravel_range_low/mid/high`. Coûts, statistiques, technologies et départs inchangés ; les 160 exports antérieurs sont préservés, registre total : 163. La [proposition v5](caravel_deck_art_proposals_v5_2026-10-08.json) conserve l’historique d’approbation. Contrôle de passe : `tools/integrate_naval_equipment_art.py check --lot deck` ; contrôle global : douze raccordements approuvés.

## Armements de galère : lot v2 validé et intégré

Trois pièces centrales de proue, avec deux armes latérales plus petites : pièce de 6 livres et pierriers en bronze ; canon de chasse de 12 livres et pièces de 3 livres en argent ; canon axial de 24 livres sur glissière et pièces de 6 livres en or. La première proposition est refusée : silhouettes trop proches, progression perçue comme un simple grossissement du tube. La [proposition v2](galley_armament_art_proposals_v2_2026-10-08.json), pivots hauts / grandes roues / longue glissière, a été approuvée par « que tu peux intégrer et passer au suivant. ». Les [masters exacts, prompts et recettes](../assets/naval_equipment_galley_armament_sources_2026-10-08/manifest.json) sont conservés sans retouche, y compris le halo argent. Trois DDS 120 × 120 avec sept mipmaps remplacent uniquement `aor_galley_guns_low/mid/high`. Les 163 exports antérieurs restent exacts ; registre total : 166. Contrôle étroit `tools/integrate_naval_equipment_art.py check --lot galley_armament` réussi, sans changement de gameplay ni essai en jeu. Les calibres et nombres de pièces correspondent aux choix de jeu existants, pas à l’inventaire certifié d’une galère historique.

## Coques de galère : lot validé et intégré

Trois fragments de charpente pour `aor_galley_armor_*` : bordage léger à franc-bord en bronze ; serres longitudinales et traverses de nage en argent ; quille doublée et carlingue continue en or. Le [lot proposé](galley_hull_art_proposals_2026-10-08.json) a été approuvé avec la demande d’intégrer et de poursuivre. Les [masters exacts, prompts et recettes](../assets/naval_equipment_galley_hull_sources_2026-10-08/manifest.json) sont conservés sans retouche, halo or inclus. Trois DDS 120 × 120 avec sept mipmaps remplacent seulement `aor_galley_armor_low/mid/high`. Les 166 exports antérieurs sont exacts ; registre total : 169. Contrôle étroit `tools/integrate_naval_equipment_art.py check --lot galley_hull` réussi ; aucune statistique, recette, technologie ni flotte modifiée.

## Statistiques des équipements de galère déjà configurées

Les intégrations de dessins ne changent pas ces effets. Le bronze représente l’équipement de base, avec bonus additifs nuls ; les statistiques initiales restent celles de la coque du navire. Argent et or sont des choix alternatifs d’amélioration, pas des bonus à cumuler entre niveaux d’une même catégorie.

| Catégorie | Argent : bonus par rapport à la base | Or : bonus par rapport à la base |
| --- | --- | --- |
| Coque | +100 points de coque, +1 blindage | +220 points de coque, +3 blindage |
| Armement | +5 dégâts de coque, +2 dégâts d’équipage | +8 dégâts de coque, +4 dégâts d’équipage |
| Propulsion | +0,2 vitesse, +10 capacité d’équipage | +0,4 vitesse, +20 capacité d’équipage |
| Réserves | +4 capacité d’approvisionnement | +8 capacité d’approvisionnement |

Source : `common/ship_modifications/10_1776_early_equipment.txt`, modules raccordés au type de galère dans `common/ship_types/10_1776_early_ships.txt`. Les niveaux avancés ont aussi des coûts de construction supplémentaires et des technologies requises. Effets configurés et vérifiés dans les fichiers ; pas encore observés en jeu.

## Propulsion de galère : lot validé et intégré

Le joueur a approuvé les trois dessins par « Ok, tu peux tout incorporer et passer au lot suivant. » : avirons séparés bronze ; aviron collectif argent ; aviron collectif et deux voiles latines or. [Proposition et validation](galley_propulsion_art_proposals_2026-10-08.json), [masters exacts, prompts et recettes](../assets/naval_equipment_galley_propulsion_sources_2026-10-08/manifest.json). Aucun moteur, aucune retouche des originaux ou de leur alpha ; le halo bronze et argent est conservé. Trois DDS natifs 120 × 120 / sept mipmaps remplacent seulement `aor_galley_propulsion_low/mid/high`. Statistiques, coûts, technologies et flottes inchangés. Les 169 exports antérieurs sont préservés ; registre total : 172. Contrôles étroit et global réussis, vingt et une icônes approuvées actives ; aucun essai en jeu.

## Approvisionnement de galère : lot validé et intégré

Lot approuvé par « Ok, tu peux intégrer et passer au suivant. » : coffres de banc et outres d’eau bronze ; tonneaux sous coursie argent ; cambuse de poupe et avirons de rechange or. [Proposition et validation](galley_supply_art_proposals_2026-10-08.json), [masters exacts, prompts et recettes](../assets/naval_equipment_galley_supply_sources_2026-10-08/manifest.json). Originaux et alpha conservés sans retouche, halo bronze et argent inclus. Trois DDS natifs 120 × 120 / sept mipmaps remplacent seulement `aor_galley_range_low/mid/high`. Les 172 exports antérieurs restent exacts ; registre total : 175, vingt-quatre icônes d’équipement approuvées actives. Statistiques, coûts, technologies et flottes inchangés ; bonus d’approvisionnement +0 / +4 / +8 et contrainte côtière conservés. Contrôles étroit et global réussis ; aucun essai en jeu.

## Coques de cogue : lot validé et intégré

Lot approuvé par « Ok, tu peux intégrer et passer au lot suivant. » : bordage à clins riveté bronze ; varangues liées à une carlingue argent ; serres de cale et baux traversants or. [Proposition et validation](cog_hull_art_proposals_2026-10-08.json), [masters exacts, prompts et recettes](../assets/naval_equipment_cog_hull_sources_2026-10-08/manifest.json). Originaux et alpha conservés sans retouche, halo argent inclus. Trois DDS natifs 120 × 120 / sept mipmaps remplacent seulement `aor_cog_armor_low/mid/high`. Les 175 exports antérieurs restent exacts ; registre total : 178, vingt-sept icônes d’équipement approuvées actives. Les statistiques configurées restent inchangées : bronze de base, argent +80 points de coque / +1 blindage, or +180 points de coque / +3 blindage. Coûts, déblocages et flottes inchangés ; contrôles étroit et global réussis, aucun essai en jeu.

## Armements de cogue : lot corrigé, validé et intégré

Lot approuvé par « Hop, tu peux intégrer et passer au le suivant. » : pierrier sur pivot bronze v2, canon long sur affût à roues argent inchangé, carronade sur glissière or v3. Chaque pictogramme montre une pièce représentative des batteries défensives de quatre pièces, pas quatre copies illisibles du même canon. [Proposition corrigée](cog_armament_art_proposals_2026-10-08.json), [masters exacts, prompts et recettes](../assets/naval_equipment_cog_armament_sources_2026-10-08/manifest.json). Trois DDS natifs 120 × 120 / sept mipmaps remplacent seulement `aor_cog_guns_low/mid/high`. Originaux et alpha conservés sans retouche, halo doré approuvé inclus. Registre total : 181, trente icônes approuvées actives. Modificateurs existants conservés : bronze +0 / +0, argent +1 dégât de coque / +1 dégât d’équipage, or +2 / +2. Recettes, technologies et flottes inchangées ; contrôle étroit réussi, aucun essai en jeu.

## Propulsion de cogue : lot validé et intégré

Lot approuvé par « Je vais, tu peux intégrer, passer au lot suivant. » : mât unique et voile carrée bronze ; voile carrée à deux bandes de ris argent ; grand-voile et hunier superposé or. Le mât reste unique, sans machine ni multiplication horizontale des mâts. [Proposition et validation](cog_propulsion_art_proposals_2026-10-08.json), [masters exacts, prompts et recettes](../assets/naval_equipment_cog_propulsion_sources_2026-10-08/manifest.json). Trois DDS natifs 120 × 120 / sept mipmaps remplacent seulement `aor_cog_propulsion_low/mid/high`. Originaux et alpha conservés sans retouche. Registre total : 184, trente-trois icônes approuvées actives. Bonus de vitesse existants conservés : +0 / +0,4 / +0,8 ; recettes, technologies, localisations et flottes inchangées. Contrôle étroit et contrôle global des définitions réussis ; aucun essai en jeu.

## Aménagements de cogue : lot validé et intégré

Lot approuvé par « OK, tu peux intégrer et passer au lot suivant. » : cale libre avec couverture roulée et coffre bronze ; faux-pont de couchettes et râtelier argent ; pont de troupes avec panneau de chargement ouvert et échelle or. [Proposition et validation](cog_supply_art_proposals_2026-10-08.json), [masters exacts, prompts et recettes](../assets/naval_equipment_cog_supply_sources_2026-10-08/manifest.json). Trois DDS 120 × 120 avec sept mipmaps remplacent seulement `aor_cog_range_low/mid/high`, originaux et alpha conservés sans retouche. Registre total : 187, trente-six icônes principales actives. Bonus existants conservés : capacité de transport +0 / +0,15 / +0,3 et approvisionnement +0 / +5 / +10. Statistiques, coûts, technologies et flottes inchangés ; contrôles étroit, global et reconstruction exacte réussis, aucun essai en jeu.

## Fonctions navales : lot corrigé, validé et intégré le 9 octobre

Lot approuvé par « Ok, tu peux intégrer et passer au lot suivant s'il y en a un. » : chaloupe bleue commune aux débarquements de cogue et de caravelle ; trois voiliers bronze en cordon de blocus diagonal sans chaîne métallique ; batterie de galère côtière rouge. [Proposition v2 et validation](naval_functions_art_proposals_v2_2026-10-09.json), [masters exacts, prompts et export](../assets/naval_equipment_naval_functions_sources_2026-10-09/manifest.json). Trois DDS 120 × 120 / sept mipmaps, quatre champs `icon` seulement. Palette des fonctions natives, alpha et originaux conservés sans retouche. Statistiques, recettes, déblocages et flottes inchangés. Registre total : 190 exports ; trente-neuf dessins uniques couvrent quarante définitions. Contrôles étroit, global et reconstruction exacte réussis ; aucun essai en jeu.

## Dernier visuel : éperon d’étrave, validé et intégré le 9 octobre

Le joueur a approuvé [l’éperon d’étrave pour l’abordage](galley_boarding_spur_art_proposal_2026-10-09.json) avec « que tu peux intégrer. Je vais relancer le jeu de mon côté, ensuite. ». [Master exact, prompt et export](../assets/naval_equipment_galley_boarding_spur_sources_2026-10-09/manifest.json) : proue courte et éperon pointu renforcé, palette bleue de la fonction native de marine/abordage, alpha original conservé sans retouche. Un DDS natif 120 × 120 avec sept mipmaps et un seul champ `icon`, celui de `aor_galley_boarding_spur`. Ses caractéristiques existantes restent +20 % de dégâts à l’équipage, +0,05 de capacité de marine et −0,1 de vitesse. Statistiques, recettes, déblocages et flottes inchangés. Registre total : 191 exports ; quarante dessins uniques couvrent les quarante et un modules, liste des visuels restants vide. Contrôles étroit, global et reconstruction exacte réussis ; aucun essai en jeu, sauvegarde ou redémarrage effectué par l’agent.

## Références et limites historiques

- La [caravelle portugaise du National Maritime Museum](https://www.rmg.co.uk/collections/objects/rmgc-object-66267) illustre un gréement tardif à quatre mâts. Les configurations nommées du mod sont des adaptations de jeu, pas trois variantes certifiées d’un bâtiment historique unique.
- Les [canons de la Mary Rose](https://maryrose.org/discover/collections/the-weaponry-of-the-mary-rose/great-guns/) documentent la diversité des systèmes anciens, dont les chargements et affûts distincts. Ils ne justifient pas les nombres de pièces choisis pour nos trois coques.
- Le [plan de 1804 d’affût de carronade de 12 livres](https://www.rmg.co.uk/collections/objects/rmgc-object-86785) et la [carronade de 6 livres conservée à Gibraltar](https://www.ministryforheritage.gi/heritage-and-antiquities/6-pdr-carronade-military-heritage-centre-1315) étayent les calibres et la distinction entre canons longs et pièces courtes, sans représenter des équipements initiaux de 1776.
- Le [National Maritime Museum sur Seppings](https://www.rmg.co.uk/collections/objects/rmgc-object-14491) situe sa carrière et ses travaux de renforcement diagonal après le départ du mod. Cette charpente ne remplace pas une coque en fer.
- La [galère de guerre du Rijksmuseum](https://www.rijksmuseum.nl/en/collection/object/Model-of-a-War-Galley--dd5fdedc5f7f1bd12d46c16da1cdc5d4?tab=catalogue) présente une pièce de proue guidée dans l’axe ; nos trois compléments de batterie restent des choix d’équilibrage, pas son inventaire exact.

## Contrôles réalisés

- 41 modules définis : 36 choix principaux et 5 fonctions, descriptions françaises et anglaises présentes avec BOM.
- 7 technologies, références/prérequis/ères validés, absence de cycle dans leurs chemins de recherche.
- 41 flottes vérifiées, effectifs et flottes des pays autorisés préservés ; aucune coque initiale avec déblocage manquant.
- Définitions cohérentes avec les paramètres navals présents dans les fichiers natifs ; deux fonctions compatibles sur caravelle et galère.
- Fichiers runtime hors de la liste autorisée inchangés. Les 151 exports graphiques existants ne sont pas modifiés.
- QA détaillée : `.asset-cache/early_ship_equipment_2026-10-08/equipment_validation.json` ; réexécution : `tools/build_early_ship_equipment.py --check`.
- **Non vérifié en jeu** : écran du concepteur, cumul effectif des fonctions, coûts observés, rééquipement et emploi des modèles initiaux. Aucun démarrage de nouvelle partie ni redémarrage du jeu effectué.

