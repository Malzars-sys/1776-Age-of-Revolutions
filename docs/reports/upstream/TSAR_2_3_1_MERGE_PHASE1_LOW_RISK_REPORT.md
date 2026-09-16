# Fusion Tsar 2.3.1 — phase 1 à faible risque

Date : 2026-09-16  
Portée : affinement de l'audit et intégration des seuls éléments immédiatement sûrs.

## Résultat de la phase

La phase 1 a intégré uniquement deux ADN de dirigeants déjà présents dans le fork :

| Dirigeant | Fiche historique conservée | ADN repris | Statut |
|---|---|---|---|
| Frédéric II de Prusse | fiche du fork `Frederick_II von_Hohenzollern` | `dna_frederick_great_pru` | intégré |
| Abdülhamid Ier | fiche du fork `Abdulhamid_I Osmanoglu` | `dna_abdul_hamid_otto` | intégré |

Les dates, cultures, religions, idéologies, groupes d'intérêt et traits Tsar n'ont pas été importés. Les deux fichiers ADN du fork sont identiques à la source Tsar une fois les espaces neutralisés.

Fichiers ajoutés :

- `common/dna_data/00_frederick_great_pru.txt`
- `common/dna_data/00_abdul_hamid_otto.txt`

Fichier raccordé :

- `common/history/characters/cleanup2b1 - major rulers 1776.txt`

## Arbitrage personnages

Les recherches historiques du fork restent autoritaires. Les personnages Tsar ne doivent pas remplacer nos dirigeants, commandants ou responsables politiques.

Règle permanente pour les prochaines phases :

1. identifier la même personne historique des deux côtés ;
2. conserver intégralement la fiche du fork ;
3. reprendre éventuellement l'ADN Tsar si le fork n'en possède pas ;
4. ne jamais importer automatiquement date, idéologie, traits, fonction ou appartenance politique avec l'ADN ;
5. refuser les personnages `TEMPORARY`, sans DNA ou moins documentés lorsqu'une reconstruction du fork existe.

L'audit des nouveautés `common/dna_data` ne trouve que les deux ADN intégrés pendant cette phase.

## Arbitrage Inde

Décision : **ne pas fusionner maintenant ; reporter au chantier de refonte de carte**.

Éléments intéressants :

- éviter de représenter en 1776 un royaume sikh unifié comparable à l'empire de Ranjit Singh, encore postérieur ;
- renforcer la présence marathe et réexaminer Agra, Malwa, Gwalior et les possessions européennes ;
- compléter bâtiments, armées, comptoirs et relations de sujet avec la future carte.

Problèmes empêchant une reprise directe :

- Tsar attribue l'ensemble du Pendjab aux Durrani et rend la région non incorporée ; cette représentation est trop nette, car l'Empire durrani avait perdu Lahore en 1765 face à la montée de la puissance sikh ;
- Gwalior conserve des définitions, personnages et références alors que son contrôle territorial est commenté au profit d'un ensemble marathe plus large ;
- le lot mélange corrections historiques, simplifications de gameplay et références résiduelles ;
- l'importation exigerait simultanément États, pays, pops, bâtiments, armées, diplomatie, personnages, événements, drapeaux et localisations.

Conclusion : la version Tsar est une **source de propositions**, pas une carte directement admissible.

Références historiques utilisées pour l'arbitrage :

- [Encyclopaedia Iranica — Afghanistan, political history](https://www.iranicaonline.org/articles/afghanistan-x-political-history/), notamment la perte de Lahore en 1765 et la montée de la puissance sikh ;
- [Cambridge — Malwa: Land of Many Empires](https://www.cambridge.org/core/books/negotiating-mughal-law/malwa-land-of-many-empires/43C7D1A9E9CD4EE41CA477E68F8D511C), sur les dominations marathes de Malwa, dont les Sindhia de Gwalior.

## Arbitrage Vietnam

Décision : **bonne base conceptuelle, mais reporter au chantier de carte et corriger avant intégration**.

Points cohérents :

- présence d'un acteur Tây Sơn dès 1776 ;
- séparation entre le Nord Lê/Trịnh, la révolte du centre et les restes Nguyễn au Sud ;
- capitale Tây Sơn en Annam et guerre contre les Nguyễn conformes à la dynamique de la période.

Points à corriger :

- l'attribution stable de tout l'Annam à Tây Sơn et du Mékong à `NG1` simplifie une guerre très mobile en 1776–1777 ;
- `NGU` possède une histoire de pays mais aucune définition ni possession correspondante : c'est une référence orpheline ;
- les personnages Tây Sơn et Nguyễn sont encore marqués `TEMPORARY` ;
- la loi de république paysanne, la guerre initiale, les revendications et la diplomatie doivent être adaptées ensemble.

Références historiques utilisées :

- [Vietnam Law Magazine — The state and law under the Tay Son dynasty](https://vietnamlawmagazine.vn/the-state-and-law-under-the-tay-son-dynasty-1776-1802-4509.html), sur la proclamation de Nguyễn Nhạc et les conquêtes de 1776 ;
- [Library of Congress Country Studies — The Tay Son Rebellion](https://countrystudies.us/vietnam/13.htm), sur la chute des Nguyễn et la conquête ultérieure du Nord en 1786.

## Arbitrage unités militaires

Tsar ajoute exactement deux types d'unité au fichier terrestre :

| Unité | Position statistique | Décision | Raccord recommandé |
|---|---|---|---|
| `combat_unit_type_musket_infantry` | 15 attaque / 20 défense, entre irréguliers 10/10 et infanterie de ligne 20/25 | retenir | déblocage par `regulated_small_arms`, puis amélioration vers l'infanterie de ligne de `light_infantry_tactics` |
| `combat_unit_type_improved_cannon_artillery` | 25 attaque, entre canon de base proposé à 20 et artillerie mobile ultérieure | retenir sous réserve de rééquilibrage | déblocage par `standardized_field_artillery` ; déplacer le canon de base vers un nœud militaire antérieur |

Ces unités conviennent à la période et peuvent donner un contenu réel à deux nœuds du nouvel arbre. Elles ne sont toutefois pas à faible risque : leur intégration exige de modifier les chaînes d'amélioration, les déblocages et de nombreuses formations militaires initiales.

Elles sont donc validées **conceptuellement**, mais reportées à une phase militaire dédiée. Le fichier Tsar complet `00_land_combat_unit_types.txt` ne devra pas être copié.

## Arbitrage bâtiments et méthodes de production

Décision : **aucune importation directe**.

| Contenu Tsar | Décision | Motif |
|---|---|---|
| bâtiment de routes | refuser | doublonne le bâtiment unifié routes/canaux/rail de TECH7A |
| PM de routes | refuser | modèle et valeurs incompatibles avec TECH7A |
| ports remplacés | refuser | ajout d'infrastructure contraire à l'équilibre cumulé du réseau terrestre |
| mine d'or remplacée | refuser | override global et gate `shaft_mining` non justifié |
| rotations du blé | refuser | système trop étroit et production directe d'engrais sémantiquement incorrecte |
| outils agricoles | refuser | concurrence les PM et technologies agricoles déjà restructurés |
| élevage | refuser | progression trop sommaire, sans avantage sur le système du fork |
| exploitation forestière renforcée | refuser | redondante avec le rework du bois et potentiellement surproductive |
| construction navale `pm_interesting_shipbuilding` | refuser | PM minimal, nom provisoire et équilibre non démontré |

Les idées pourront être relues plus tard, mais aucun de ces éléments ne vaut le coût d'un conflit avec les systèmes déjà développés.

## Validation

- ADN Frédéric II : données identiques à Tsar après neutralisation des espaces ;
- ADN Abdülhamid Ier : données identiques à Tsar après neutralisation des espaces ;
- chaque ADN est référencé une fois par le dirigeant correspondant ;
- `git diff --check` ciblé : réussi, hors avertissement de conversion LF/CRLF ;
- aucune donnée de personnage autre que les deux références ADN n'a été modifiée ;
- aucune carte, unité, formation, technologie, bâtiment ou méthode de production Tsar n'a été fusionnée pendant cette phase.

## Prochaine phase recommandée

**Phase 2 militaire ciblée** : intégrer les deux unités comme définitions isolées, définir leurs déblocages dans notre arbre, auditer les formations de 1776 puis migrer seulement les pays historiquement concernés.

La refonte Inde/Vietnam doit rester une phase séparée ultérieure, synchronisée avec le chantier de carte.
