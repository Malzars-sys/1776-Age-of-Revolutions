# Fortifications terrestres — coût de base et extensions

19 octobre 2026 — **LAND_FORT_CONSTRUCTION_READY_FOR_RUNTIME_VALIDATION**.

Le coût affiché du bâtiment passe de **100 à 900 points par niveau**. La valeur précédente était la constante `construction_cost_very_low = 100`, et non 400. Le nouveau coût utilise une constante propre au fort ; les autres bâtiments conservent leurs coûts.

L’efficacité locale de construction vise le barème choisi par l’utilisateur : **900, 1 100, 1 300, 1 500 et 1 700 points effectifs**, avant les autres bonus ou malus. La valeur requise affichée reste 900 ; le supplément vient d’une progression hebdomadaire plus lente.

| Niveau à construire | Niveaux déjà construits | Modificateur d’efficacité propre aux forts | Équivalent visé sans autre modificateur |
|---|---:|---:|---:|
| 1 | 0 | 0 % | 900 |
| 2 | 1 | −18,1818 % | ≈ 1 100 |
| 3 | 2 | −30,7692 % | ≈ 1 300 |
| 4 | 3 | −40 % | 1 500 |
| 5 | 4 | −47,0588 % | ≈ 1 700 |

Le calcul de calibrage est `900 / (1 + modificateur)`. Les constantes sont arrondies à six décimales. L’outil calcule un écart inférieur à 0,01 point par rapport aux cibles en arithmétique décimale ; la précision fixe du moteur n’est pas reproduite par cet outil. Les modificateurs nationaux, les autres effets locaux et le plancher natif d’efficacité conservent leurs règles. Le total théorique visé pour cinq extensions successives est d’environ **6 500 points effectifs**, pour 4 500 points de progression affichée.

## Portée et recalcul

Le groupe du seul bâtiment terrestre active le paramètre natif `construction_efficiency_modifier = yes`. Les quatre modificateurs s’appliquent à l’État et ciblent exclusivement `building_group_bg_aor1776_land_fortification_construction_efficiency_add`. Ils ne changent ni les forts navals, ni les casernes, ni les autres chantiers.

Le niveau effectivement construit sélectionne le modificateur. La file d’attente n’augmente pas ce niveau dans le calcul. Les PM et les effectifs de garnison ne sont pas consultés ; un fort vide conserve donc le coût de ses extensions.

Les actions natives de construction et d’agrandissement déclenchent un recalcul immédiat. Le début d’une extension rafraîchit aussi la valeur. Les transferts de propriétaire, créations d’États et impulsions mensuelles réparent l’état du système. Les effets des actions natives et des autres chantiers sont conservés par ajout d’actions filles.

Une seule chaîne quotidienne est entretenue par pays possédant un fort ou un ancien modificateur à retirer. Elle actualise les seuls États concernés et traite les réductions de niveau ou démolitions, pour lesquelles aucun callback spécifique n’a été trouvé. Les anciens paliers sont retirés, un seul palier peut subsister, et la chaîne s’arrête quand il n’y a plus de fort ni de modificateur résiduel. Le marqueur de chaîne expire après deux jours pour permettre une réparation si un callback manque.

Un fort au plafond de cinq niveaux garde le dernier palier, sans autorisation de sixième niveau. Les statistiques défensives, le plafond, les technologies, les emplois, les biens consommés et le contre du corps du génie sont inchangés.

## Vérifications

- **168 contrôles ciblés réussis** : syntaxe, coûts, paliers, PM et garnisons, nettoyage, démolition, propriétaires, initialisation répétée, chaînes uniques, arrêt et réparation du suivi, actions natives, localisation et préservation des sources.
- **2 073 contrôles des forts et du génie réussis** après adaptation du seul coût attendu et de la référence de préservation autorisée.
- **1 992 fichiers protégés inchangés**, dont les cartes, unités, combats, technologies et illustrations. HEAD, index Git et vanilla canonique sont conservés.
- Textes FR/EN avec BOM UTF-8, clés uniques et descriptions visibles des modificateurs.

Les scénarios interprètent les conditions et effets réellement écrits avec des faits synthétiques. Ils n’exécutent pas Victoria 3. [Résultats ciblés](VALIDATION.json), [résultats de régression](../../ENGINEER_CORPS/VALIDATION.json), [manifeste](MANIFEST.json).

## Essais moteur restant à réaliser

1. Dans un État intérieur sans fort, vérifier 900 points affichés, construire le premier niveau, puis contrôler la pénalité du deuxième. Refaire les cinq extensions sans autres modificateurs et relever les points alloués et les progrès reçus.
2. Tester une commande groupée de cinq niveaux, plusieurs projets simultanés, réorganisation de la file, annulation et reprise. Le rythme réel des callbacks et la consommation dans une même semaine ne sont pas prouvés par les projections. Un modificateur d’État est partagé par les chantiers simultanés de ce type ; il n’attache pas un coût individuel à chaque élément de file.
3. Tester démolition et réduction de niveau : retrait ou changement au plus tard au prochain contrôle quotidien. Vérifier un changement de propriétaire et un État partagé.
4. Vérifier les trois PM, une garnison vide et le plafond de cinq. Les bonus défensifs et les seuils du génie doivent rester identiques.
5. Sauvegarder/recharger, y compris une ancienne sauvegarde antérieure au système : le début d’une extension ou la réparation mensuelle doit initialiser le suivi si aucune chaîne n’existait. Contrôler plusieurs pays et la disparition de la chaîne après le dernier fort.
6. Vérifier le coût réellement supporté avec des bonus nationaux ou locaux et le plancher d’efficacité. Tester aussi l’IA, l’affichage des décimales et le coût du suivi quotidien.

**Statut moteur : NOT_RUN.** Le barème est une cible d’efficacité, pas cinq valeurs natives distinctes de points requis.

## Sources

Vanilla canonique local : `common/building_groups/00_building_groups.txt` pour le paramètre d’efficacité, `common/modifier_type_definitions/01_building_modifier_types.txt` pour la famille de modificateurs, `common/production_methods/12_subsistence.txt` pour un effet de cette famille porté par un État, `common/on_actions/00_code_on_actions.txt` pour les callbacks et `common/defines/00_defines.txt` pour le plancher d’efficacité de 0,05.

Le suivi différé reprend le schéma déjà présent dans le dépôt pour les laboratoires : `common/on_actions/11_tech8c_laboratory_operation.txt` et `common/scripted_effects/13_tech8c_laboratory_operation.txt`. La documentation générée du moteur 1.13 confirme les portées d’ajout et de retrait des modificateurs ; copie conservée dans `sources/effects.log`, [source](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/blob/main/1.13.0/docs/effects.log).
