# MIL-CAVALRY-AUDIT — préparation de MIL-CAVALRY-1776

Statut : **AUDIT_AND_PROPOSAL_ONLY**. Les définitions mondiales d'unités, technologies, méthodes de production et arbres d'amélioration ne sont pas modifiées.

## Données actuelles du mod

Source : `common/combat_unit_types/00_land_combat_unit_types.txt`. Les quatre types appartiennent au groupe de cavalerie et ont 1 000 hommes au maximum. Données extraites dans STATS.json ; exposition par contingent dans EXPOSURE.csv.

| Statistique | Lanciers | Dragons | Hussards | Cuirassiers |
|---|---:|---:|---:|---:|
| Attaque ajoutée | 16 | 20 | 24 | 32 |
| Défense ajoutée | 10 | 24 | 18 | 28 |
| Perte de moral ajoutée, moins est préférable | 12 | 9 | 8 | 6 |
| Taux de mortalité additionnel | +0,03 | 0 | 0 | +0,05 |
| Dégâts de moral multipliés | 0 | 0 | 0 | +0,05 |
| Occupation multipliée | +0,15 | +0,25 | +0,30 | +0,30 |
| Efficacité d'invasion navale | −0,25 | −0,25 | −0,25 | −0,25 |
| Vitesse de mobilisation de formation | +0,10 | +0,10 | +0,25 | +0,05 |
| Vitesse de déplacement de formation | +0,10 | +0,10 | +0,25 | +0,05 |
| Capacité de ravitaillement | 25 | 35 | 40 | 55 |
| Grain, entretien de base | 1 | 1 | 1,5 | 2 |
| Armes légères, entretien de base | 0 | 1 | 1 | 1,5 |
| Fer, entretien de base | 0 | 0 | 0 | 0,5 |
| Valorisation des biens au prix de base | 20 £ | 80 £ | 90 £ | 150 £ |
| Déblocage | aucun | regulated_small_arms | horse_artillery | military_veterinary_services |

Les prix de base sont grain 20, armes légères 60, fer 40. La valorisation multiplie les quantités scriptées par ces prix ; **elle n'est pas le budget réel d'un bataillon**. Les salaires, prix du marché, état de mobilisation, approvisionnement et modificateurs ne sont pas inclus. Aucun bien cheval distinct ne figure dans ces quatre entretiens ; ne pas prétendre que le coût du fourrage ou des remontes est intégralement simulé par les grains.

Aucun maximum de moral, maximum d'organisation, délai spécifique de recrutement ou bonus de renfort propre à ces quatre types n'est défini dans leurs blocs. Le moral et l'organisation effectifs proviennent aussi des lois, des commandants, du ravitaillement et des règles de formation ; absence de valeur locale ne signifie pas zéro dans le moteur. Les bonus de vitesse sont des modificateurs de formation, pas une preuve qu'une unité isolée parcourt exactement 25 % de distance supplémentaire dans toute composition.

Recrutement : bâtiment militaire recruteur et capacité par loi ; pas de méthode de production propre à chacun de ces quatre types. Les méthodes de formation déterminent emplois et instruction, tandis que le type porte ici son entretien. Leur ordre de déblocage ne suffit pas à démontrer qu'un pays possède les qualifications ou les biens pour les entretenir. Aucun contingent de cavalerie conscrit n'a été trouvé dans l'inventaire initial ; cela ne démontre pas une interdiction universelle du moteur.

Arbre actuel : lanciers → dragons/hussards/cuirassiers ; dragons → hussards/cuirassiers ; hussards → cuirassiers ; cuirassiers → chars légers. C'est une progression vers le lourd qui peut encourager une amélioration purement verticale, en dépit des fonctions différentes.

## Lecture historique et ludique

Le [National Army Museum, Cavalry Roles](https://www.nam.ac.uk/explore/cavalry-roles) distingue reconnaissance des hussards, dragons légers et dragons de choc selon les traditions nationales. Les Britanniques ne rebaptisent certains dragons légers en hussards qu'à partir de 1806 : ne pas transférer cette chronologie à toutes les armées de 1776. La fonction originelle de dragons démontés ne signifie pas que tous les dragons combattent constamment comme infanterie au XVIIIe siècle.

Le [Musée de l'Armée sur la cuirasse Fauveau](https://www.musee-armee.fr/collections/tresors-du-musee/la-cuirasse-du-carabinier-fauveau.html) montre l'équipement protecteur de cavalerie lourde, dans un contexte de 1815. Cette source illustre la fonction de la cuirasse ; ses équipements et performances ne sont pas projetés sans réserve sur chaque armée de 1776. Protection relative et action de choc justifient une défense supérieure à une cavalerie légère, sans faire du cuirassier une infanterie défensive universellement supérieure.

Constats : les hussards actuels ne dominent pas les dragons dans toutes les dimensions : attaque +20 %, défense −25 %, entretien nominal +12,5 %, mobilité meilleure. Le cuirassier, en revanche, cumule attaque, défense, résistance au moral, mortalité, ravitaillement et occupation élevés. Sa défense de 28 n'est que 16,7 % au-dessus des dragons à 24, mais le cumul de ces avantages mérite un essai. Son entretien est aussi 87,5 % plus cher que celui des dragons : supprimer tous ses avantages rendrait ce coût peu défendable.

## Proposition chiffrée P1, non installée

Les valeurs sont une hypothèse de gameplay à comparer au témoin. Garder les quantités de biens et les technologies inchangées dans ce premier essai pour isoler les effets des statistiques.

| Champ proposé | Lanciers | Dragons | Hussards | Cuirassiers |
|---|---:|---:|---:|---:|
| Attaque | 16, inchangé | 22, ancien 20 | 18, ancien 24 | 28, ancien 32 |
| Défense | 10, inchangé | 18, ancien 24 | 12, ancien 18 | 20, ancien 28 |
| Perte de moral | 12, inchangé | 10, ancien 9 | 9, ancien 8 | 8, ancien 6 |
| Taux de mortalité additionnel | +0,03 | 0 | +0,04, ancien 0 | +0,05 |
| Dégâts de moral | 0 | 0 | 0 | +0,05 |
| Occupation | +0,15 | +0,20, ancien +0,25 | +0,35, ancien +0,30 | +0,10, ancien +0,30 |
| Mobilisation / déplacement | +0,10 / +0,10 | +0,10 / +0,10 | +0,25 / +0,25 | +0,05 / +0,05 |
| Capacité de ravitaillement | 25 | 35 | 40 | 30, ancien 55 |
| Entretien nominal de biens | 20 £ | 80 £ | 90 £ | 150 £ |

Rôles visés : lanciers accessibles et bon marché ; dragons polyvalents ; hussards rapides pour exploitation et poursuite, avec une faible défense en engagement frontal ; cuirassiers chers et solides pour le choc, à faible aptitude d'occupation. Occupation n'est pas reconnaissance : aucun prétendu bonus de renseignement n'est introduit. L'ajout de mortalité des hussards représente ici une poursuite abstraite, pas un capteur réel de reconnaissance ou de retraite ; son efficacité en bataille doit être vérifiée.

La capacité de ravitaillement de 55 des cuirassiers paraît mal orientée pour une troupe lourde, mais la réduire peut modifier l'organisation de formations mixtes. Tester ce champ séparément si le premier essai combat produit trop de variations. Les cuirassiers gardent une défense 20 supérieure aux hussards 12 et aux lanciers 10 ; ils ne deviennent pas une unité sans protection.

P2 distincte, après essais : remplacer la progression automatique vers les cuirassiers par des branches de spécialisation. Ne pas intervertir les identifiants des dragons et hussards : les historiques, sauvegardes, images et améliorations les référencent. Les liens horse_artillery/hussards et military_veterinary_services/cuirassiers sont des abstractions discutables à revoir avec tout l'arbre militaire ; ne pas changer ces technologies pour résoudre seulement ce tableau. Une cavalerie coloniale de dragons antérieure à regulated_small_arms nécessite un autre lot de déblocages, sans abaisser mondialement un prérequis en douce.

## Exposition et régressions à tester

Après MIL-START, les quatre types représentent **505 réguliers, 0 conscrit déclaré, 165 contingents, 156 formations nommées dans 117 pays** : 182 lanciers, 179 dragons, 117 hussards, 27 cuirassiers. L'inventaire tient compte des fichiers mod/vanilla effectifs par nom ; il décrit les déclarations, pas les effectifs conservés après initialisation. Deux formations partageant le même nom dans un pays pourraient être regroupées par le compteur de noms : les 165 contingents restent la donnée de détail.

Si P1 était appliquée à cet inventaire, somme théorique des attaques ajoutées : 10 164 → 9 712 (−452) ; défenses : 8 978 → 6 986 (−1 992). Ce cumul n'est pas un score de puissance : il ignore infanterie, artillerie, terrain, effectifs, commandants et batailles. La valorisation d'entretien nominal resterait 32 540 £ pour les mêmes contingents. Les pertes différentes modifieraient néanmoins le coût réel des renforts.

Séparer le lot MIL-CAVALRY-1776 dans un manifeste de quatre blocs exactement, avec une référence avant/après des technologies, coûts et arbres. Aucune modification mondiale n'est nécessaire pour terminer l'audit présent.

Tests P1 : pays disposant de chaque type (liste exacte dans EXPOSURE.csv), notamment PRU/AUS/FRA/GBR/POR et une armée à lanciers ; composition à 10 bataillons de même taille, expérience et chefs comparables ; terrain plat puis accidenté, attaque et défense, prix normaux puis pénurie de grain/armes, pure cavalerie puis formation mixte. Comparer moral, pertes, vitesse, ravitaillement et organisation. Définir avant essai le rôle attendu ; ne pas sélectionner seulement les batailles gagnées. Faire ensuite campagne mondiale sur 12 mois et comparer 117 pays, budgets et effectifs. Tester mises à niveau et chargement de sauvegarde séparément.

## Validation de l'audit

Extraction statique, références de types/technologies/biens et décompte des contingents vérifiables. Les quatre définitions sont identiques à la base Git. Les CSV/JSON ne sont pas lus par le jeu. Aucun résultat d'équilibrage moteur n'est acquis ; les valeurs P1 restent une proposition.
