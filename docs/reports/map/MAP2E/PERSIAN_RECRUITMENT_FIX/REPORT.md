# MAP-2E — Redistribution finale du recrutement perse

## Résultat

20 unités déplacées de Tabriz (9 hussards, 11 infanteries irrégulières) vers dix autres États déjà possédés par PER. Tabriz conserve 2 artilleries, 1 hussard et 2 infanteries irrégulières. Les sept infanteries déjà présentes en Irak-Ajemi restent en place.

La Perse conserve exactement **32 unités permanentes et 38 unités de conscription**, leurs types, la même formation et son commandant Moḥammad Ṣādeq Khan Zand. Les six conscriptions de Tabriz, dont celle transférée lors de MAP-2E, sont inchangées. Aucun recrutement n’est recréé dans les khanats indépendants.

Seul fichier de gameplay modifié : `common/history/military_formations/04_military_formations_middle_east.txt`. Aucun bâtiment explicite de casernes ajouté : les unités créent leur recrutement automatiquement. Aucun niveau de route, bâtiment civil, population, frontière, PM ou accord diplomatique modifié. Aucun commit, merge ou push ; aucune nouvelle archive complète.

## Infrastructure : calcul statique, pas observation en jeu

Les unités sont comptées à 0,2 infrastructure et 1 000 emplois chacune. La capacité modélisée inclut les routes à plein emploi, la base de 3 et les traits régionaux ; elle exclut les bonus démographiques et de bloc. La demande civile inclut un proxy des bâtiments de propriété générés. Les historiques superposés sont estimés avec la dernière déclaration par type : ce calcul ne remplace pas le chargement natif.

« Cons. » indique la capacité inchangée de conscription. La dernière colonne ajoute par prudence la demande de toutes ces unités : ce scénario de stress n’est pas une mesure de la consommation des centres inactifs.

| État | Permanentes avant → après | Cons. | Demande totale avant → après | Capacité nominale | Réserve après | Réserve avec toutes les conscriptions |
|---|---:|---:|---:|---:|---:|---:|
| Fars / Shiraz | 0 → 1 | 3 | 15.5 → 15.7 | 16.2 | 0.5 | -0.1 |
| Irak-Ajemi | 7 → 8 | 9 | 17.4 → 17.6 | 18 | 0.4 | -1.4 |
| Ispahan | 0 → 4 | 3 | 13.1 → 13.9 | 15 | 1.1 | 0.5 |
| Kerman | 0 → 3 | 1 | 6.2 → 6.8 | 9 | 2.2 | 2 |
| Khorasan | 0 → 1 | 4 | 6.2 → 6.4 | 9 | 2.6 | 1.8 |
| Laristan | 0 → 0 | 0 | 1.1 → 1.1 | 6 | 4.9 | 4.9 |
| Luristan | 0 → 1 | 2 | 3.6 → 3.8 | 5.4 | 1.6 | 1.2 |
| Mazandéran | 0 → 3 | 6 | 6.4 → 7 | 12 | 5 | 3.8 |
| Kurdistan perse | 0 → 1 | 2 | 3.6 → 3.8 | 5.4 | 1.6 | 1.2 |
| Semnan | 0 → 1 | 0 | 1.1 → 1.3 | 6 | 4.7 | 4.7 |
| Tabriz | 25 → 5 | 6 | 21 → 17 | 18 | 1 | -0.2 |
| Ourmia | 0 → 4 | 2 | 4.7 → 5.5 | 8.1 | 2.6 | 2.2 |

À Tabriz, la demande militaire nominale passe de 5 à 1 : la réserve de paix modélisée passe de −3 à +1. La mobilisation intégrale reste tendue à Tabriz (−0,2), Fars (−0,1) et Irak-Ajemi (−1,4). Les deux derniers sont déjà des centres civils ou militaires chargés : un seul hussard leur est attribué. Aucun accroissement automatique des routes pour masquer ces limites.

## Population et personnel

Le modèle de main-d’œuvre est **25 % de la population libre**, non une mesure du chômage ni une garantie de qualification ou de recrutement. Les emplois civils explicites sont calculés à pleine capacité ; ils n’incluent pas tous les emplois générés des propriétaires ni la subsistance. Les surplus ci-dessous ne sont donc pas des salariés réellement disponibles.

| État | Population inchangée | Modèle travailleurs libres | Emplois civils explicites | Militaires avant → après | Marge modélisée après |
|---|---:|---:|---:|---:|---:|
| Fars / Shiraz | 418 119 | 102 161 | 48 600 | 0 → 1 000 | 52 561 |
| Irak-Ajemi | 1 172 348 | 290 873 | 38 000 | 7 000 → 8 000 | 244 873 |
| Ispahan | 387 795 | 94 152 | 41 500 | 0 → 4 000 | 48 652 |
| Kerman | 176 812 | 42 183 | 22 000 | 0 → 3 000 | 17 183 |
| Khorasan | 555 868 | 137 724 | 23 000 | 0 → 1 000 | 113 724 |
| Laristan | 30 693 | 7 051 | 6 000 | 0 → 0 | 1 051 |
| Luristan | 252 538 | 60 726 | 16 000 | 0 → 1 000 | 43 726 |
| Mazandéran | 797 458 | 198 160 | 44 000 | 0 → 3 000 | 151 160 |
| Kurdistan perse | 311 684 | 76 872 | 16 000 | 0 → 1 000 | 59 872 |
| Semnan | 46 061 | 11 456 | 6 000 | 0 → 1 000 | 4 456 |
| Tabriz | 709 827 | 175 864 | 44 000 | 25 000 → 5 000 | 126 864 |
| Ourmia | 280 291 | 69 257 | 22 000 | 0 → 4 000 | 43 257 |

Laristan n’accueille aucune unité supplémentaire : sa population et sa marge de personnel sont faibles. Semnan ne reçoit qu’une infanterie ; Ispahan, Ourmia, Kerman et Mazandéran prennent l’essentiel du complément au transfert initial de dix unités. Aucun habitant libre ou esclave n’est ajouté, retiré ou déplacé.

## Justification et limites historiques

Répartition administrative de gameplay, pas reconstitution des garnisons : Shiraz est la capitale zand ; Ispahan, Tabriz et Kerman font partie des principaux centres du pouvoir et des alliances provinciales. Le recrutement cavalier est réparti entre ces centres et les régions occidentales plutôt que concentré artificiellement dans l’ancien espace caucasien.

Sources : [Zand Dynasty — Encyclopædia Iranica](https://www.iranicaonline.org/articles/zand-dynasty/), [Karim Khan Zand — Encyclopædia Iranica](https://www.iranicaonline.org/articles/karim-khan-zand/).

Le Khorasan relève d’une autonomie afsharide historiquement distincte du pouvoir zand. Il reste une région PER dans la carte existante, avec son recrutement de conscription préexistant. L’unique infanterie permanente supplémentaire est une abstraction du pays PER actuel, non l’affirmation d’une garnison zand historiquement démontrée. Ce point territorial reste hors du présent correctif : aucune frontière ni dépendance n’est modifiée.

## Validations et protections

Résultat : **PASS_STATIC**, 32 contrôles. Conservation mondiale : 835 804 980 habitants. Comparaison avec l’état réellement présent après MAP-2E : tous les propriétaires RGB, populations détaillées, groupes culturels/religieux, statuts libres/esclaves, bâtiments et niveaux, PM, propriétaires économiques, États et pays restent identiques. Seul le recrutement permanent PER prévu diffère. Commandants, formation et quartiers généraux restent identiques. Aucun nouveau doublon ou recrutement orphelin.

Empreintes de tous les fichiers de gameplay et des rapports MAP-2A/B/C/D/E contrôlées : seul l’historique militaire ciblé change. Les tests existants des journaux ottomans et des infrastructures IA passent. HEAD, références et index Git inchangés. La baseline légère `BASELINE.json`, le modèle `CANDIDATES.json` et le résultat `VALIDATION.json` rendent le correctif reproductible.

Le rapport original MAP2E_VALIDATION.json est conservé comme résultat de l’étape précédente. Son ancien contrôle exigeant toutes les unités transférées à Tabriz est désormais remplacé, pour ce suivi, par la comparaison exacte avec la redistribution autorisée dans `tools/persian_recruitment_map2e.py validate` ; il ne faut pas réécrire la baseline ou présenter cet ancien contrôle comme encore applicable.

## Vérifications dans une nouvelle partie

Le test natif post-correctif n’a pas été exécuté. L’ancienne autosauvegarde est binaire et n’a pas fourni de chiffres de personnel/infrastructure exploitables ; aucune sauvegarde n’a été altérée.

1. Nouvelle partie 1776 : Tabriz doit avoir 5 permanentes et 6 conscriptions ; la Perse entière 32 permanentes et 38 conscriptions.
2. Contrôler Tabriz, puis Fars et Irak-Ajemi : infrastructure utilisée/disponible, emplois des routes, pénuries et accès au marché ; vérifier aussi les autres destinataires après un mois.
3. Confirmer les 4 permanentes d’Ispahan, les 4 d’Ourmia et les 3 de Kerman/Mazandéran ; vérifier la même formation et le même commandant.
4. Confirmer les pays caucasiens, enclaves russes et corrections MAP-2A/B/C/D/E. Un éventuel déficit résiduel devra être distingué d’un défaut de recrutement ou d’une mobilisation ; aucun résultat d’accès au marché à 100 % n’est promis.
