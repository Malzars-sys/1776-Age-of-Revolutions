# MIL-CAVALRY-1776 — diagnostic et patch P1 isolé

Statut : **DESIGN_ONLY — proposition testable, NON INSTALLÉE**. La mission autorise explicitement cet arrêt du sous-lot mondial après diagnostic et patch isolé. Les autres fonctionnalités R2 sont installées indépendamment.

Audit réexécuté sur les définitions chargées et les formations actuelles : **117 pays, 505 bataillons réguliers**. Répartition : 182 lanciers, 179 dragons, 117 hussards, 27 cuirassiers. `CAVALRY_VALIDATION.json` contient les contingents, pays, formations, valeurs et contrôles. Les définitions de cavalerie restent identiques à l'audit R1 ; la correction du type naval américain ne change pas cette exposition.

## Valeurs et essai proposé

| Type | Attaque / défense actuelle → P1 | Perte de moral actuelle → P1 | Autres modifications P1 | Entretien nominal, inchangé | Technologie, inchangée |
|---|---|---|---|---:|---|
| Lanciers | 16 / 10 → inchangé | 12 → inchangé | aucun changement | 20 £ | aucune |
| Dragons | 20 / 24 → 22 / 18 | 9 → 10 | occupation +25 % → +20 % | 80 £ | regulated_small_arms |
| Hussards | 24 / 18 → 18 / 12 | 8 → 9 | occupation +30 % → +35 % ; mortalité additionnelle +0 → +0,04 | 90 £ | horse_artillery |
| Cuirassiers | 32 / 28 → 28 / 20 | 6 → 8 | occupation +30 % → +10 % ; capacité de ravitaillement 55 →30 | 150 £ | military_veterinary_services |

Coûts calculés aux prix de base des biens, hors salaires, lois et prix locaux : lanciers 1 grain ; dragons 1 grain +1 arme ; hussards 1,5 grain +1 arme ; cuirassiers 2 grains +1,5 arme +0,5 fer. Les quatre recettes, maximums d'effectif et coûts de recrutement restent inchangés. Mobilisation/déplacement restent respectivement +10 %, +10 %, +25 %, +5 %. Les améliorations possibles et les identifiants restent identiques, ce qui évite d'intervertir des unités déjà référencées par les sauvegardes et historiques.

Les hussards gardent donc un rôle de cavalerie légère rapide, à occupation et poursuite abstraites renforcées ; ils ne sont pas les moins efficaces dans toutes les dimensions. L'occupation n'est **pas** une statistique de reconnaissance. Le taux de mortalité additionnel est une approximation de l'exploitation, pas un nouveau système observant les retraites. Les dragons restent polyvalents ; les cuirassiers conservent la meilleure attaque et une défense supérieure aux autres types proposés, ainsi que +0,05 de mortalité et +5 % de dégâts de moral, avec un coût et une mobilité défavorables. La cuirasse n'est pas traitée comme une absence de protection.

Le [National Army Museum, Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles), distingue les emplois et leurs évolutions. Ses exemples couvrent plusieurs époques et armées : ne pas donner rétroactivement à tous les Britanniques de 1776 la désignation hussard de régiments convertis plus tard. Le [Musée de l'Armée, cuirasse Fauveau](https://www.musee-armee.fr/collections/tresors-du-musee/la-cuirasse-du-carabinier-fauveau.html), documente la protection de la cavalerie lourde en 1815 ; il illustre une fonction, sans imposer ce matériel précis à chaque cuirassier de 1776. Les chiffres P1 sont des hypothèses de gameplay, pas des données historiques mesurées.

## Impact mesuré, limites et fichiers livrés

Les sommes pondérées sur les bataillons initiaux passent arithmétiquement de 10 164 à 9 712 en attaque (−452) et de 8 978 à 6 986 en défense (−1 992). L'entretien nominal reste 32 540 £. Ces agrégats ne sont ni des résultats de bataille, ni une estimation de pertes, de victoire ou de budget réel. Le coût inchangé peut défavoriser les cuirassiers et les hussards si leurs avantages de rôle ne compensent pas les réductions frontales ; aucune conclusion de campagne n'est inventée.

Le changement de capacité des cuirassiers peut affecter le ravitaillement de formations mixtes. Le conserver dans ce candidat rend le test global plus exigeant : comparer aussi une variante sans cette seule réduction pour distinguer combat et logistique. Les déblocages horse_artillery et military_veterinary_services restent des abstractions discutables ; les réorganiser demanderait un lot complet de progression militaire, en dehors de ce patch de statistiques.

Livrables :

- `CAVALRY_P1_ISOLATED.patch` : différence applicable à **un seul fichier**, sans application dans le mod actif.
- `proposal/00_land_combat_unit_types.txt` : version candidate complète, rangée dans les rapports pour lecture ; le moteur ne la charge pas.
- `CAVALRY_VALIDATION.json` : inventaire et non-régression, empreinte du fichier actif, vérification du candidat et applicabilité du patch sans l'appliquer.
- `tools/audit_cavalry_r2.py` : audit reproductible en lecture seule.

Les contrôles vérifient que seules les statistiques indiquées changent dans le candidat, que les lanciers et toutes les unités non montées sont identiques, que les coûts/technologies/mobilités sont conservés et que le patch s'applique à la version actuelle. Aucune formation historique, population ou carte n'est modifiée pour ce lot.

## Protocole avant installation mondiale

Dans une copie de test du mod, appliquer le patch après contrôle de sa base. Comparer un témoin et P1, mêmes effectifs, commandants, terrain, mobilisation et approvisionnement. Tester dragons/hussards/cuirassiers contre infanterie, puis formations mixtes ; mesurer durée, pertes, moral, progression, coût et ravitaillement. Répéter sur plusieurs graines ou batailles, sans déduire l'équilibre d'un seul résultat.

Choisir ensuite des pays exposés dans l'inventaire : France, Prusse, Autriche, Grande-Bretagne et puissances coloniales disposant réellement des types concernés ; vérifier aussi les pays dont l'historique utilise une unité sans sa technologie. Contrôler recrutement, améliorations, IA et sauvegarde/rechargement. Les corrections R1 du Portugal, Brésil, Nouvelle-Grenade et Río de la Plata doivent rester présentes ; les États-Unis conservent zéro cavalerie initiale. Sans ces essais moteur, aucune installation mondiale ni déclaration de cavalerie implémentée.
