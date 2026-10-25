# Équilibrage — A1

## Échelle retenue

Un seul niveau simple par réseau régional retenu, sans compter séparément chaque bastion, fort ou batterie. Strasbourg et Neuf-Brisach partagent ainsi un niveau. La valeur est une convention prudente pour le premier test, pas une estimation des dépenses historiques.

Aucun petit État ne reçoit cinq niveaux gratuits ; aucun PM renforcé ou avancé n'est installé. Les colonies américaines et les formations de la guerre d'indépendance ne sont pas modifiées. Les deux nouveaux forts britanniques peuvent néanmoins influencer cette guerre indirectement en mobilisant davantage de budget et de main-d'œuvre : cela demande un test en partie.

## Protection terrestre existante

À effectif complet, chaque niveau du PM simple apporte au combat défensif local admissible : **−5 % de provinces perdues, −5 % de pertes subies, +5 % de défense**. PM2 : 10 % ; PM3 : 15 % par niveau. Les totaux à cinq niveaux restent 25 / 50 / 75 %.

Les cinq forts terrestres A1 sont répartis dans cinq États distincts : leurs protections ne s'additionnent pas en un bonus national de 25 %. La province doit appartenir au défenseur et rester sous son contrôle ; l'État doit aussi lui appartenir et être intérieur. L'emploi effectif module les valeurs. Le script existant arrondit la puissance par paliers : aucune garnison complète n'est fabriquée par l'initialisation.

Le génie attaquant engagé en bataille retire **un point de pourcentage par 1 000 hommes présents**, jusqu'à annulation des protections supplémentaires. Cinq niveaux simples nécessitent donc 25 bataillons complets, PM2 50 et PM3 75. Un seul niveau simple A1 est annulé par 5 bataillons complets. Les ingénieurs du défenseur ne réduisent pas ses propres forts. L'artillerie ordinaire ne reçoit pas gratuitement cette capacité.

La projection statique relit les expressions réellement installées : bataillons partiels, cumul, dépassement, défense, absence de fort et province occupée. Les conditions ordinaires de combat/retraite restent celles du système précédent. La bataille réelle reste à tester.

## Limite côtière explicite

Les sept bâtiments côtiers conservent leurs effets natifs : protection des invasions, défense navale, résistance aux bombardements/blocus et contrôle des détroits selon les conditions du moteur. Le PM simple contient notamment les valeurs brutes 100 / 0,05 / 250 / 25 et le booléen de contrôle du détroit ; **100 n'est pas présenté comme 100 %**.

Le mécanisme de contre-mesure du génie vise actuellement les **forts terrestres intérieurs**, pas les forts navals. Remplacer une implantation côtière par le bâtiment naval ne lui ajoute donc ni protection terrestre ni contre-mesure du génie. Cette limite est conservée conformément à la demande d'utiliser les bâtiments existants sans réimplémenter les systèmes. Une unification éventuelle exige un chantier séparé et des essais moteur.

## Entretien maximal théorique des nouvelles implantations

Les deux PM simples utilisent chacun 5 armes légères et 5 fers par niveau à plein emploi, avec 900 militaires et 100 officiers. Les besoins suivants sont des plafonds nominaux, pas des mesures de budget :

| Pays | Niveaux ajoutés | Armes légères | Fer | Emplois |
| --- | ---: | ---: | ---: | ---: |
| France | 4 | 20 | 20 | 4 000 |
| Grande-Bretagne | 2 | 10 | 10 | 2 000 |
| Espagne | 3 | 15 | 15 | 3 000 |
| Portugal | 2 | 10 | 10 | 2 000 |
| Provinces-Unies | 1 | 5 | 5 | 1 000 |
| Total | 12 | 60 | 60 | 12 000 |

Les prix, salaires, recrutements et disponibilités locaux déterminent le coût réel. Gibraltar mérite une attention particulière sur l'emploi, le marché et l'absence de recrutement de campagne ajouté par erreur. Réserves initiales à 100 % ne signifie pas emploi initial à 100 %.

## Points à décider après le test

- Soutenabilité des dépenses nationales après un mois ; aucune compensation fiscale automatique.
- Lisibilité de la distinction des forts côtiers et intérieurs, particulièrement en Alentejo et Beira.
- Défense britannique supplémentaire et rythme de l'intervention française dans une partie américaine.
- Aucune augmentation des niveaux ou distribution de bataillons du génie avant observation de ces effets.
