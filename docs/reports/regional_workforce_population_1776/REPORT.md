# Recrutement des infrastructures régionales — correctif de population

Date : 10 octobre 2026. Source observée : `observateur_3`, au 1er février 1776.

## Résultat livré

Ajout de **882 400 habitants libres dans dix régions**, exclusivement dans cinq fichiers d'historique des populations. Aucun habitant existant n'est supprimé ou converti. Aucun esclave n'est ajouté. Les frontières MAP-2A/MAP-2B, bâtiments, méthodes de production, technologies, lois, relations diplomatiques et nombres d'unités sont conservés.

Il s'agit d'un **calibrage de gameplay pour les emplois existants**, pas d'un recensement historique. Les augmentations sont parfois importantes et modifient les proportions culturelles locales : notamment davantage d'Espagnols aux Antilles espagnoles, de Britanniques dans les territoires britanniques et de Mandchous dans les régions chinoises concernées. Les populations locales préexistantes sont intégralement conservées.

## Répartition appliquée

| Région / propriétaire | Population initiale avant | Habitants ajoutés | Population initiale après | Population ajoutée |
| --- | ---: | ---: | ---: | --- |
| Floride / GBR | 30 957 | 89 100 | 120 057 | Britanniques protestants |
| Géorgie / USA | 42 993 | 109 200 | 152 193 | Dixie protestants |
| District de Columbia / USA | 5 000 | 192 600 | 197 600 | Yankee et Dixie protestants, selon leurs proportions libres antérieures |
| Nouveau-Brunswick / NVS | 20 000 | 60 400 | 80 400 | Anglo-canadiens protestants |
| Bermudes / GBR | 19 584 | 59 700 | 79 284 | Britanniques protestants |
| Antilles / SPA | 14 000 | 159 600 | 173 600 | Espagnols catholiques |
| Jamaïque / GBR | 520 000 | 16 200 | 536 200 | Employés britanniques protestants uniquement |
| Alxa / CHI | 44 788 | 61 600 | 106 388 | Mandchous confucianistes |
| Åland / SWE | 14 347 | 100 500 | 114 847 | Suédois protestants |
| Amour / CHI | 82 613 | 33 500 | 116 113 | Mandchous confucianistes |
| **Total** | | **882 400** | | |

Le total mondial statique passe de **835 804 980 à 836 687 380 habitants**. Cette hausse est distincte des transferts MAP-2B, qui avaient conservé le total mondial. Les anciens rapports MAP restent inchangés et décrivent leur étape précédente.

## Diagnostic et dimensionnement

Les effectifs libres et dépendants sont lus dans les populations de la sauvegarde, et non assimilés aux seuls compteurs d'emploi agrégés. Les emplois civils potentiels sont calculés à partir des PM réellement actifs, hors subsistance. Les effectifs militaires permanents prévus dans les historiques sont ajoutés comme concurrence pour les mêmes travailleurs, à partir de `max_manpower` ; les conscrits ne sont pas comptés.

L'estimation prend le plus faible des effectifs libres observés après un mois et des effectifs initiaux estimés, puis vise une marge de 5 % au-dessus de la capacité totale d'emploi. Le ratio de travailleurs utilisé est de 30 %, et de 35 % à Åland, cohérent avec les observations. La main-d'œuvre esclave existante n'est créditée que dans la limite des emplois agricoles de manœuvres ; elle n'est jamais considérée comme disponible pour les routes ou les postes administratifs qualifiés.

Des groupes d'employés et, lorsque nécessaire, de bureaucrates accompagnent les manœuvres. Les ajouts appartiennent aux cultures principales de leur pays afin de limiter les blocages de recrutement administratif. Les clés utilisées sont celles déjà présentes dans les historiques du jeu : culture, religion, type de population et taille. Aucun effet instantané d'embauche ni champ artificiel de qualifications n'est ajouté.

Washington est le cas le plus disproportionné : environ 1 476 travailleurs libres observés face à une capacité civile de 56 350 emplois, dont dix-neuf niveaux d'administration et sept niveaux d'infrastructures. Puisque la consigne autorise les ajouts de population et préserve les bâtiments, le correctif comble ce déséquilibre démographique sans supprimer d'administrations.

En Jamaïque, les 152 109 travailleurs libres observés sont déjà suffisants en nombre. Le correctif vise uniquement les employés : seulement 61 travailleurs de ce métier sont pleinement acceptés dans la sauvegarde, contre 4 665 emplois potentiels correspondants. Les 16 200 habitants ajoutés sont donc exclusivement de type `clerks`, soit environ 4 860 travailleurs selon le modèle, et non une augmentation massive de manœuvres.

**Aucun ajout en Guyenne** : environ 415 307 travailleurs libres pour 37 850 emplois civils potentiels. Le petit déficit observé ne démontre pas une insuffisance de population. Les autres déficits de capacité, comme Minsk, ou les différences de niveaux chargés, comme en Prusse orientale, ne sont pas traités par des ajouts démographiques arbitraires.

## Avant / après : distinguer observation et projection

| Région | Infrastructure observée le 1er février | Utilisation observée | Travailleurs libres retenus pour le calcul | Travailleurs libres après ajout, estimation |
| --- | ---: | ---: | ---: | ---: |
| Floride | 6,91 | 7,10 | 2 552 | 29 282 |
| Géorgie | 4,89 | 9,90 | 7 378 | 40 138 |
| District de Columbia | 3,17 | 19,70 | 1 403 | 59 183 |
| Nouveau-Brunswick | 5,78 | 6,30 | 6 000 | 24 120 |
| Bermudes | 2,31 | 5,90 | 5 875 | 23 785 |
| Antilles espagnoles | 2,40 | 7,70 | 3 888 | 51 768 |
| Jamaïque | 15,89 | 18,50 | 152 109 | 156 969 |
| Alxa | 1,50 | 3,40 | 13 413 | 31 893 |
| Åland | 4,09 | 6,80 | 5 021 | 40 196 |
| Amour | 2,25 | 6,00 | 24 784 | 34 834 |

La dernière colonne est une estimation de main-d'œuvre, **pas une mesure d'infrastructure effective après correction**. Les populations supplémentaires peuvent aussi accroître la demande de biens et entraîner la croissance des centres urbains. Les qualifications, salaires, disponibilités de biens et priorités d'embauche restent déterminés par le moteur.

## Vérifications réalisées

- Instantané immuable de l'état local après MAP-2B, avant cet ajout démographique.
- Validation syntaxique et comparaison exacte de chaque historique avec la transformation prévue : cinq fichiers de populations modifiés, et seulement les groupes supplémentaires documentés.
- Conservation exacte de tous les groupes de population antérieurs, y compris les esclaves et les minorités.
- Vérification du supplément mondial et de chaque supplément par région, culture et religion, sans perte ni duplication.
- Inventaire comparatif : mêmes provinces, propriétaires, géométries, statuts des États, bâtiments, propriétaires économiques et unités ; aucune nouvelle référence orpheline ou duplication territoriale.
- **2 583 fichiers protégés inchangés**, dont les historiques non démographiques et les rapports MAP-1C/MAP-2A/MAP-2B.
- Dix scénarios du correctif de pénurie des infrastructures : réussis dans le modèle de scripts.
- Régressions des journaux ottomans : 1 024 combinaisons administratives, 192 combinaisons politiques, introduction par événements et indépendance des résolutions : réussies dans le modèle de scripts.
- Contrôle des espaces en fin de ligne : réussi pour les fichiers concernés.
- Aucun commit, merge ou push. Sauvegarde `observateur_3` laissée intacte.

Le résultat de validation est **PASS_STATIC**. Ces tests ne constituent pas une exécution native de Victoria 3 après les ajouts.

## Vérification restante en jeu

Lancer une **nouvelle partie**, puis sauvegarder après un mois. Une sauvegarde déjà existante n'intègre pas les nouveaux historiques de population. Comparer les dix régions : niveaux et PM des infrastructures, effectifs par profession, pénuries, infrastructure disponible/utilisée et accès au marché.

Vérifier également les finances nationales : mieux remplir les administrations et les unités déjà présentes peut augmenter les dépenses de salaires et d'entretien, sans changer leur nombre. L'accès au marché ou un excédent budgétaire ne sont donc pas garantis par le seul test statique.

Fichiers de preuve associés : `DIAGNOSIS.json`, `BASELINE.json`, `PLAN.json`, `VALIDATION.json`. Le script `tools/regional_workforce_population.py` produit les propositions et validations ; les historiques ont été modifiés par correctifs explicites, pas par écrasement de la sauvegarde.
