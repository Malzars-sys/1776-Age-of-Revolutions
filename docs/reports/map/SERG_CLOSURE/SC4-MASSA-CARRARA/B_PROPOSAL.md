# Décision opérationnelle B : noyau de résidence massais

## Comparaison avant installation

Inventaire réel : MOD possède `xEF0021` (336 cellules) et `xF08021` (116), avec **505 752 habitants** dans une seule déclaration nord-italienne sans religion ni métier explicites. LUC possède `xF080A0` (174 cellules, 84 558 habitants) ; GEN et TUS sont distincts. La pointe côtière de `xF08021` touche la mer et Lucques, à l'est du promontoire génois. La carte Robert 1750 a été effectivement lue : Massa/Carrare se trouvent dans cette interface littorale, distincte de la haute Lunigiana, de la Garfagnana et du domaine lucquois. Aucun ancien recalage R4 n'est utilisé.

| Option | Cellules / propriétaire avant → après | Population touchée | Risque / difficulté | Décision |
| --- | --- | --- | --- | --- |
| Centre ponctuel | `[4328,1031]`, `[4328,1032]`, MOD → MCA | Groupe MOD de 505 752 concerné ; 10 000 à transférer si retenu | Deux cellules confondent résidence et territoire ; proportion urbaine forcée, très faible accès à la mer | Rejetée au profit du petit noyau côtier connecté |
| Province existante entière | 116 cellules de `xF08021`, MOD → MCA | Même groupe MOD ; habitants propres à cette province non identifiés, aucun transfert calculé par ratio de surface | Emporte Lunigiana/Garfagnana et conserve implicitement des droits non démontrés ; disproportion avec le duché littoral | Rejetée, pas de transfert de bloc |
| **Découpe RGB localisée** | **8 cellules listées ci-dessous, MOD → MCA**, nouveau `xEDBC00` ; parent MOD 116 → 108 | **10 000 transférés**, MOD 505 752 → 495 752 ; MCA 0 → 10 000 | Approximation de résidence de catégorie B ; contours extérieurs et population complète de Carrare non certifiés. Parent MOD demeure connecté, aucun hub ou voisin déplacé | **Retenue et installée**, souveraineté réelle avec noyau limité |
| Région économique nouvelle pour les mêmes 8 cellules | Même transfert MOD → MCA | Même transfert possible de 10 000 | Exige nouveau State_ID, redistribution des ressources/arables et cinq locators ; changements plus larges sans gain de preuve historique | Non retenue dans cette passe. Portion MCA de STATE_EMILIA utilisée, comme les autres noyaux politiques du chantier |
| Personnalité juridique sans territoire | 0 cellule, MOD demeure propriétaire | 0 transféré ; 505 752 inchangés | TAG sans État vivant, aucune restitution de souveraineté jouable | Rejetée : ne résout pas l'omission |

Cellules retenues, coordonnées natives zéro-indexées :
`[4325,1029] [4326,1029] [4326,1030] [4327,1030] [4327,1031] [4328,1030] [4328,1031] [4328,1032]`.

Ce contour suit une pointe côtière existante, en escalier, entre la côte génoise et le premier bord lucquois ; il ne s'agit ni d'un rectangle tracé sur les coordonnées modernes ni du transfert de toute la province. Il donne un noyau de résidence représentatif au couple de titres Massa/Carrare ; aucune enclave intérieure Malaspina n'est absorbée. Cette correspondance **B politique**, appréciée par voisinage et topologie littorale, n'est pas une superposition géodésique ou une localisation cadastrale des deux villes.

## Conséquences bornées

- TAG **MCA** libre dans les définitions et sans réemploi des drapeaux MAC/Macédonie. `MAS` et `MCR` sont déjà présents et ne sont pas réutilisés.
- Capitale technique : portion incorporée **MCA de STATE_EMILIA**, contenant ce seul noyau littoral. Masse politique de résidence : **Massa** ; aucun locator de Parme, Modène ou Lucques déplacé. Le libellé et le placement automatiques de la capitale de cet État partagé restent à contrôler en jeu ; ne pas prétendre qu'un nouveau hub urbain Massa a été créé.
- **10 000** est une estimation prudente pour le noyau de résidence massais, basée sur l'ordre de grandeur de sa communauté en 1765/1801. La population totale du duché, de Carrare et des fiefs n'est pas reconstruite. Le noyau ne gagne pas artificiellement des habitants : transfert exact depuis le MOD actuellement chargé.
- Cultures, religions et métiers : mêmes champs que le donneur ; nord-italien, catholicisme par défaut, aucune profession inventée. Groupes minoritaires TUS et tous autres pays inchangés.
- Un niveau d'administration publique propre à la chambre ducale est ajouté. L'administration MOD validée reste en place ; aucun bâtiment antérieur confisqué. Ressources, plafonds, arables et unités inchangés ; le marbre relève du potentiel pierre partagé, sans nouvelle mine/port industriel ni concessionnaire inventé.
- Prime-land : l'enfant RGB reçoit le même classement que son parent, sans extension de surface fertile. Même terrain ; aucun changement du trait régional, de la mer ou de la taille du bitmap.
- Registre impérial : 574 → **575 RGB** ; titre MOD résiduel conservé, titre MCA ajouté. Emprise physique impériale identique, neuf électeurs inchangés. Pays impérial distinct, aucune prétention aux fiefs voisins.

## Limites et suite précise

Le protocole joueur porte sur **MC-I-CORE**, huit cellules et 10 000 habitants. L'exhaustivité de Carrare et la population des périphéries ne sont pas validées. Une extension ultérieure doit partir du même détail historique, distinguer Sarzana/Lerici, Montignoso lucquois, Pietrasanta/Seravezza toscanes et Garfagnana modénaise, proposer une liste de cellules et un transfert démographique propre ; pas de nouvelle recherche physique d'Elbe. Si le moteur place la capitale partagée hors du noyau, corriger ce problème précis avant toute acceptation, avec un hub/région séparé si nécessaire.
