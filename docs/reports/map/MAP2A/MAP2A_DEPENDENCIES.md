# MAP-2A — Dépendances et hypothèses de migration

## Population : conservation et limites

| State Region / propriétaire | Avant | Après |
|---|---:|---:|
| Lombardie AUS | 1 449 921 | 1 449 921 |
| Lombardie VEN | 483 307 | 478 307 |
| Lombardie SWI | 0 | 5 000 |
| Moravie AUS | 1 379 483 | 1 570 622 |
| Haute-Silésie AUS | 326 892 | 0 |
| Haute-Silésie PRU | 300 385 | 300 385 |
| Galicie occidentale GAL | 1 277 876 | 1 277 876 |
| Galicie occidentale AUS / Teschen | 0 | 135 753 |
| **Total des quatre régions** | **5 217 864** | **5 217 864** |

### Bormio

L'allocation de 5 000 habitants utilise comme repère d'ordre de grandeur le regroupement communal de Bormio de **4 832 habitants en 1807**, comprenant notamment les vallées proches et Livigno. Ce chiffre postérieur ne prouve pas une population précise de 1776 et ne prouve pas que son périmètre égale le RGB. Le territoire du jeu et les 5 000 sont une approximation prudente, non un nouveau recensement inventé.

Transfert : 4 999 `north_italian` à religion implicite catholique et 1 `north_italian` juif, prélevés sur les deux groupes VEN existants. Les 80 Juifs restants et 478 227 catholiques restent VEN. La population autrichienne lombarde n'est pas modifiée. Le total, les cultures et religions sont strictement conservés.

### Silésie autrichienne

Les sept groupes du pool AUS de 326 892 personnes sont partagés avec les proportions **vers Teschen** suivantes : Allemands du Nord 20 %, Polonais 80 %, Tchèques 30 %, Ashkénazes 50 %. Chaque calcul est arrondi par défaut ; le reste exact rejoint Moravie/Opava. Les religions explicites ou implicites restent identiques à chaque groupe d'origine.

Il s'agit d'une ventilation de gameplay orientée par les aires linguistiques, **pas de pourcentages historiques mesurés**. Elle évite une division automatique par nombre de provinces et préserve exactement chaque couple culture/religion. Les cultures existantes, y compris l'emploi initial de `north_german` par le mod, ne sont pas réécrites.

## Bâtiments et propriétaires

`common/history/buildings/02_east_europe.txt` : les déclarations AUS invalides de Haute-Silésie sont déplacées dans un nouveau sélecteur AUS de Galicie occidentale :

- Infrastructure régionale (`building_railway`) : 1 niveau détenu par un quartier d'affaires AUS, référence économique déplacée vers Teschen ; réseau routier traditionnel, pas de canaux, pas de réseau ferroviaire, pas de trains de voyageurs.
- Manufacture textile : 2 niveaux, propriété locale du bâtiment AUS, mêmes PM de vêtements cousus à la main, sans vêtements de luxe et métiers traditionnels.
- Réserves inchangées.

`98_build_start_1776_world_redistribution.txt` : la déclaration textile AUS correspondante (2 niveaux) suit Teschen, évitant qu'elle réinitialise un ancien État AUS inexistant. Elle n'est ni supprimée ni additionnée comme un nouvel investissement.

Aucun propriétaire économique étranger n'est nationalisé. Les autres bâtiments AUS, VEN, GAL, GEN et PRU, les ports, ressources, PM, canaux et potentiels régionaux sont conservés. Il n'existe pas de déclaration initiale de bâtiment VEN ou recrutement VEN en Lombardie à déplacer pour ce petit transfert ; les bâtiments autrichiens de Lombardie restent là où ils étaient. Aucun bâtiment artificiel n'est créé pour Bormio.

Le validateur compare tous les niveaux de propriété écrits par type de bâtiment mondialement, le nombre de déclarations et leur transformation exacte. Il ne simule pas l'agrégation base/overlay du moteur. Les possibilités d'emploi et l'accès au marché des nouveaux petits États doivent être testés en jeu.

## Armées, États et diplomatie

- Un conscrit AUS, infanterie de ligne, est recruté à Teschen (`STATE_WEST_GALICIA`) au lieu d'un sélecteur AUS de Haute-Silésie sans province physique valide. Son type et son nombre restent identiques ; formations, scopes sauvegardés, commandants et HQ sont conservés.
- Permanents, flottes et recrutement PRU inchangés.
- Nouvelle subdivision AUS de Galicie occidentale ; GAL conserve toutes ses provinces et sa dépendance autrichienne existante.
- Disparition de la subdivision AUS invalide de Haute-Silésie, pas d'un pays.
- Nouvelle subdivision SWI de Lombardie ; SWI conserve sa capitale et sa représentation confédérale existante. Le proxy des Trois Ligues ne crée pas un canton ou une nouvelle dépendance.
- Capitales, relations, sujets, traités, homelands et revendications existants inchangés. Les nouvelles subdivisions reprennent le statut incorporé par défaut, cohérent avec les districts européens auxquels elles se substituent ; aucune incorporation coloniale modifiée.
- Toutes les définitions de State Regions, hubs et potentiels restent identiques. Les allocations sont corrigées dans les historiques, pas dans la géométrie.

Les sept historiques MAP-2A modifiés sont énumérés dans `MAP2A_VALIDATION.json`. Les autres anciens fichiers sont protégés par leurs empreintes avant/après, y compris les références de pays, journaux, événements et décisions.

## Sources et portée de leur preuve

- **Trois Ligues** : [Dictionnaire historique de la Suisse](https://hls-dhs-dss.ch/it/articles/026840/2004-04-14/) : république et relations avec les cantons ; appuie le choix d'un proxy associé, pas d'un canton de 1803.
- **Valteline / Bormio** : [Lombardia, DHS](https://hls-dhs-dss.ch/it/articles/007079/2015-05-07/) et [Grigioni, DHS](https://hls-dhs-dss.ch/it/articles/007391/2023-08-29/) : contrôle des Trois Ligues avant 1797. Ce contrôle n'est ni vénitien ni autrichien en 1776.
- **Population-repère de Bormio** : [inventaire institutionnel de Sondrio, Lombardia Beni Culturali](https://www.lombardiabeniculturali.it/docs/istituzioni/Sondrio-s.pdf), notice du regroupement de 1807 ; pas une preuve d'effectif de 1776.
- **Répartition silésienne** : [Kuzio-Podrucki, Zaranie Śląskie, 2022](https://zaranieslaskie.bs.katowice.pl/en/article/download/44/18/36), passages sur les traités de 1742/1743/1745/1763, déjà référencés en MAP-1C. Appuie la conservation autrichienne de Teschen/Opava et la grande Silésie prussienne, sans résoudre les villages de frontière.
- **Trentin reporté** : [Archivio di Stato di Trento — Antichi regimi](https://archiviodistatotrento.cultura.gov.it/antichi-regimi/) et [Trentino Cultura — Il Settecento roveretano](https://www.cultura.trentino.it/La-storia-del-Trentino/Il-Settecento-roveretano). Distinguent principauté épiscopale et administrations tyroliennes ; le découpage VEN/AUS hérité n'est pas déclaré définitivement vérifié.

Les identifications géographiques viennent des travaux MAP-1B/MAP-1C conservés. Les résidus défavorables et réserves de ces travaux ne sont pas retirés. La décision MAP-2A applique maintenant la tolérance aux approximations autorisée par l'utilisateur, au lieu de prétendre que ces résidus ont disparu.

## Copie candidate du collaborateur

Chemin : `C:/Users/simeo/.codex/worktrees/map-0-collaborator-integration/1776_Age_of_Revolutions_fork/common/history/states/00_states.txt`.

Deux seules corrections de son texte de travail : supprimer les tokens `git status` / `git fetch origin` en Bessarabie, et retirer `x867A90` de AUS en Lombardie (VEN conserve la province). Diff vérifié : exactement ces deux zones. Pas de staging, commit ou finalisation de la fusion préexistante.

Cette copie candidate **reste distincte** du scénario modifié testé statiquement ici : son choix AUS sur `x9AC196`, ses anciennes divergences ottomanes et sa ventilation luxembourgeoise ne sont pas approuvés ni intégrés. Le lot n'ajoute aucun nouveau commit collaborateur à main.
