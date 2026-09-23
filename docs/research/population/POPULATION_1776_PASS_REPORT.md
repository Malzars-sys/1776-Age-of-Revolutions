# Population 1776 — passe mondiale conservatrice

## Résultat

La passe modifie uniquement les valeurs `size` dans les blocs de population historiques déjà existants. Aucun État, groupe de population, type de population, culture ou religion n'a été ajouté ou supprimé. La [matrice État–propriétaire](POPULATION_1776_STATE_TARGETS.csv) donne pour chaque entrée le total initial, la cible appliquée, la méthode et la référence. Le [snapshot avant passe](POPULATION_1776_BASELINE.csv) et les [points d'ancrage Clio Infra](CLIO_INFRA_ANCHORS_1700_1840.csv) sont conservés.

| Indicateur | Avant | Après |
|---|---:|---:|
| Population de l'ensemble des fichiers historiques | 921 501 776 | 835 423 101 |
| Groupes de population | 4 385 | 4 385 |
| Entrées État–propriétaire modifiées | — | 941 |
| Entrées protégées ou différées | — | 105 |

Exemples de cibles : États-Unis **9 711 257 → 2 487 774** (calcul par État/colonie, pas par réduction uniforme) ; Grande-Bretagne métropolitaine **16 551 366 → 8 000 000** ; Irlande **8 024 356 → 4 170 000** ; Russie **36 264 375 → 27 000 000** ; Prusse **12 493 753 → 5 100 000**. Le sous-continent dans le fichier `10_india.txt` passe de **166 219 721 à 190 000 000** ; sa ventilation provinciale reste provisoire, car une série comparable pour chaque État du mod n'est pas disponible.

## Exceptions et méthode

- **Chine (`CHI`), Gênes (`GEN`) et Venise (`VEN`) : aucune population changée.** Les deux Sérénissimes restent des cas réservés à une intervention humaine.
- **Vietnam en attente de redécoupage :** les blocs des États Tonkin, Annam, Mékong et Laos sont laissés intacts, quel que soit leur propriétaire actuel.
- **Australasie :** fichier intégralement différé, sa carte et les populations autochtones nécessitant une passe cartographique distincte.
- Les treize colonies américaines utilisent les estimations 1770 et 1780 de l'[Historical Statistics of the United States du Census Bureau](https://www2.census.gov/prod2/statcomp/documents/CT1970p2-13.pdf), interpolées à 1776. Les groupes de l'actuel District of Columbia et de Virginie-Occidentale sont séparés avec une allocation prudente des totaux coloniaux de Maryland et Virginie. Le [Census Bureau](https://www.census.gov/library/stories/2023/12/boston-tea-party.html) situe l'ensemble colonial vers 2,5 millions d'habitants.
- Pour les territoires non américains, les cibles nationales utilisent surtout les séries de [Clio Infra — Total Population](https://clio-infra.eu/Indicators/TotalPopulation.html), interpolées entre les points pré-1800 ou utilisées comme borne basse. Ces séries reposent sur les frontières des pays modernes : la correspondance avec les tags de 1776 est une **estimation**, non un recensement contemporain précis. Le tableau d'ancrage local conserve les valeurs d'origine, avec attribution à Clio Infra (données CC BY 3.0).
- Les cibles canadiennes s'appuient aussi sur les [séries historiques de Statistique Canada](https://www150.statcan.gc.ca/n1/pub/98-187-x/4064810-eng.htm) et, pour le Haut-Canada, sur l'[Annuaire du Canada](https://www65.statcan.ca/acyb02/1867/acyb02_1867001803-eng.htm).
- Les 538 entrées sans série territoriale suffisamment précise reçoivent une **borne basse régionale provisoire**, identifiée `PROVISIONAL_REGIONAL_LOW` dans la matrice. La même proportion peut être appliquée à plusieurs États d'une région ; elle ne doit pas être interprétée comme une estimation historique précise État par État. C'est la principale dette de recherche de cette passe.

## Contrôles

Le validateur `tools/population_1776_apply.py` (sans argument) confronte chaque total État–propriétaire à la matrice, compte les groupes, rejette les tailles nulles et vérifie les accolades. Résultat : **1 046 cibles, 4 385 groupes, 0 écart**, y compris **105 entrées protégées/différées**. `git diff --check` passe pour les fichiers de population. Aucune validation en jeu n'a encore été effectuée : les conséquences sur emploi, fiscalité et prix demandent un lancement sur une nouvelle partie.

La passe n'a touché ni les bâtiments, ni les frontières, ni les effectifs militaires/navals, ni les fichiers de pays. Aucun commit ni push.
