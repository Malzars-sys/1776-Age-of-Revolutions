# MAP-1C — Décisions préparées, aucune intégration

Date : 10 octobre 2026. Cible historique : 1er janvier 1776.

**Résultat : une réparation syntaxique prête à être approuvée, une approximation politique concrète proposée pour LUX et deux réparations de scopes silésiens séparées de l'arbitrage territorial. Aucun transfert provincial n'est suffisamment démontré.** Ce résultat ne remplit donc pas encore l'objectif de premières corrections de frontières historiquement vérifiées. Il ne faut pas lancer l'intégration territoriale ni étendre automatiquement ce calage aux 410 dossiers.

## Les décisions utiles maintenant

| Décision | Proposition | État de préparation |
|---|---|---|
| TECH-BESS-01 | Retirer les cinq mots parasites `git status git fetch origin` de la commande Bessarabie du **candidat du collaborateur seulement** | Patch non appliqué; égalité du contenu syntaxique utile vérifiée en mémoire |
| APP-LUX-01 | Conserver LUX, ses habitants, ses bâtiments et ses unités, mais établir une union personnelle AUS → LUX | **DOCUMENTED_GAMEPLAY_APPROXIMATION**, accord explicite requis; contrôle du dirigeant et des effets de sujet avant application |
| TECH-SIL-01 | Ranger la référence autrichienne de `x9061E0` sous WEST_GALICIA, conformément à la définition actuelle | Ne change pas AUS; préparation conditionnelle, car ce split autrichien n'existe pas actuellement dans l'historique de cette région |
| TECH-SIL-02 | Séparer les mauvaises références de région des doubles propriétaires de `x71E080` / `xF0E080` | Pas prêt à appliquer : déplacer les références ne tranche pas AUS/PRU |

La Bessarabie du dossier principal est déjà dépourvue de ces commandes parasites. Le patch ne doit pas être appliqué indistinctement au principal, ni servir à importer l'ensemble du candidat.

L'option LUX ne certifie **ni les 47 pixels de `xD001A0` comme duché complet, ni les contours des voisins**. C'est une représentation jouable du lien habsbourgeois qui conserve le pays existant. Elle conserve les **137 881 habitants écrits** des quatre enregistrements LUX; aucune population n'est distribuée selon la surface d'un RGB. Les commandes de bâtiments, leurs propriétaires et leurs méthodes restent intactes. Le journal des dépendances indique leurs fichiers, sans prétendre simuler leurs niveaux effectifs dans le moteur.

## Pourquoi les trois régions ne donnent pas encore de transfert sûr

**Luxembourg.** Les provinces du jeu regroupent des zones du duché, de Liège, de Bouillon ou d'autres juridictions. Les sources documentent ces autorités, mais les scans précis des limites et les listes de villages manquent. La relecture du scan Janvier montre de surcroît que certaines observations MAP-1B visent des positions voisines des noms plutôt que les symboles exacts des villes. Les anciennes observations restent conservées; leurs calculs ne sont pas promus en preuves.

**Lombardie.** L'autorité vénitienne sur Bergame/Brescia/Crema et l'autorité autrichienne sur Milan/Mantoue ne suffisent pas à attribuer les formes entières. Une piste nouvelle, distincte d'un simple maintien, concerne **Bormio/Valtellina/Chiavenna sous les Trois Ligues** en 1776 : `x9AC196` mérite une enquête nord-alpine avant un éventuel retrait à VEN. La correspondance du RGB entier n'est cependant pas démontrée. Lui donner SWI confondrait en outre les Trois Ligues avec la représentation du pays suisse et exigerait un compromis politique distinct. Aucun de ces transferts n'est proposé à l'application.

**Silésie.** Les deux RGB méridionaux ont à la fois un mauvais scope et des propriétaires AUS/PRU concurrents. `x9061E0` a un seul propriétaire écrit, AUS, mais appartient à WEST_GALICIA dans la définition géographique. Une réparation technique ne constitue pas une preuve de la frontière austro-prussienne. Les annexes villageoises de la démarcation restent à obtenir.

## Calage : ce qui a été testé et ce qui ne l'a pas été

Les observations distinguent désormais trois coordonnées : symboles relevés sur les scans historiques, coordonnées **WGS84 contemporaines de GeoNames**, et locators du jeu. Douze modèles locaux ont été calculés : affine et similitude, pour chacun des trois dossiers, vers le scan et vers les locators. Les témoins réservés et les résidus de validation croisée restent tous enregistrés, y compris Bergame/Brescia et Olomouc. La relecture invalide l'emploi des observations héritées comme contrôle historique définitif.

Les couches physiques `rivers.png`, les provinces exactes et les données modernes Natural Earth ont également été examinées. **Aucun ajustement physique indépendant au bitmap n'est validé** : les cours d'eau du jeu sont schématisés, certaines identités de branches demeurent ambiguës et les lacs ne fournissent pas ici une correspondance bitmap suffisamment certaine. Aucun point physique supposé n'est présenté comme confirmé, aucun zéro résiduel d'interpolation n'est invoqué comme preuve.

Les erreurs défavorables MAP-1B restent la référence de prudence, pas une borne statistique garantie : Luxembourg 10,122 pixels, Lombardie 4,786, Silésie 27,864. Pour `xD001A0` (9 × 8 pixels), la première dépasse la petite dimension; pour `x71E080` (19 × 13), l'erreur silésienne la dépasse deux fois. Même une erreur plus petite que la boîte d'une grande province ne prouve pas l'absence de territoire mixte ou de passages étroits.

## Méthode alternative avant la poursuite mondiale

1. **Reprendre les points sur des symboles identifiables**, avec extraits agrandis, intervalle de lecture et double contrôle. Conserver les points anciens dans une couche d'audit, sans les supprimer ni confondre correction d'identification et exclusion d'un témoin défavorable.
2. Établir un calage physique local indépendant, sur au moins quatre points non colinéaires réellement identifiés et trois témoins réservés : confluences/estuaires/accidents de côte. Rejeter les correspondances ambiguës; publier aussi ce rejet. Comparer affine et similitude avant d'envisager une déformation locale, dont chaque point de contrôle devra être conservé.
3. Obtenir les **feuilles Ferraris et pièces ANLux CP-A-45/46 avec leur datation**, les listes de juridictions lombardes après 1757 et les annexes de démarcation silésienne de 1743 corroborées en 1763. Un document du 2 mai 1776 ne prouve pas à lui seul l'état du 1er janvier.
4. Croiser chaque contour RGB exact avec ces juridictions; documenter les éventuelles portions mixtes et les populations réellement affectables. Pour un territoire mixte, soumettre un compromis explicite plutôt que classer artificiellement le RGB comme vérifié.

Le prochain travail ciblé devrait donc porter sur **la frontière luxembourgeoise et Bormio**, pas sur un nouvel inventaire mondial. Si les sources fines demeurent inaccessibles, présenter un découpage de gameplay explicite avec choix d'autorité, plutôt qu'un transfert prétendument historique.

## Livrables et validations

- `MAP1C_MAPPING_DECISIONS.csv` : 13 provinces/choix prioritaires, géométrie, propriétaires, limites des preuves, impacts et replis.
- `MAP1C_APPROXIMATIONS_FOR_APPROVAL.csv` : une proposition politique LUX, **non approuvée**.
- `MAP1C_TECHNICAL_FIXES.csv` : trois problèmes distincts, dont un seul immédiatement préparé.
- `MAP1C_IMPLEMENTATION_CANDIDATES.csv` : trois candidats avec préconditions et tests futurs; aucun transfert de souveraineté provincial autorisé.
- `MAP1C_GEOGRAPHIC_EVIDENCE/` : observations, modèles, extraits, sources brutes et empreintes, impacts des dépendances, patch Bessarabie non appliqué et validation.

**Contrôles réussis :** les 1 900 fichiers de gameplay protégés restent identiques; les 66 fichiers MAP-1B et les 1 220 entrées du manifeste MAP-1 restent identiques. Les cinq modifications suivies préexistantes restent en place. HEAD principal inchangé. Aucune frontière, aucun historique, aucun bâtiment, aucune population ni relation diplomatique modifiés. Aucun commit, merge ou push. Aucune validation en jeu effectuée, puisqu'aucun candidat n'a été appliqué.

Méthode, passages consultés et limites : [dossier de preuves](MAP1C_GEOGRAPHIC_EVIDENCE/METHOD_AND_EVIDENCE.md). Résultats machine : `MAP1C_GEOGRAPHIC_EVIDENCE/VALIDATION.json`.
