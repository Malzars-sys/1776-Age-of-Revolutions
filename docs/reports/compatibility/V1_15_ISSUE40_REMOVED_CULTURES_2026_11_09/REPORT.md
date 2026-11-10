# Mission 40 — cultures héritées et population de 1776

9 novembre 2026 — Hawk. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**.

Installation locale sur HEAD `0396b1133168c1721b61cee5ae5334f1a4f5e4e1`, jeu canonique vérifié **1.15.0**. Aucun lancement moteur ni résultat joueur nouveau n'est attesté. La mission GitHub reste ouverte.

## Correction installée

Les identifiants `north_caucasian` et `siberian` ont chacun un fournisseur additionnel unique. Ils conservent les noms FR/EN, couleurs, religions par défaut, 54 éléments de listes de noms, graphismes et poids d'ethnicités retrouvés dans les anciennes données versionnées. Les noms et les fournisseurs graphiques/ethniques actuels sont vérifiés. Aucun fichier vanilla n'est masqué.

Le système de traits a été adapté au contrat 1.15 : héritages natifs régionaux actuels, tradition caucasienne pour la première culture et langues agrégées dédiées, avec groupes distincts. Ces ensembles géographiques servent à conserver des catégories héritées ; ils ne certifient pas une langue unique ou une famille commune, et n'attribuent pas tous les habitants à une ethnie native particulière. Aucune autre culture ne partage ces nouveaux traits. Voir `STRATEGY.md`, écrit avant installation, pour les conséquences d'acceptation et les limites.

Seuls cinq fichiers de jeu sont ajoutés :

- `common/cultures/zz_1776_legacy_cultures.txt` : deux définitions.
- `common/discrimination_traits/zz_1776_legacy_languages.txt` : deux traits linguistiques.
- `common/discrimination_trait_groups/zz_1776_legacy_languages.txt` : deux groupes.
- `localization/french/1776_legacy_cultures_l_french.yml` et `localization/english/1776_legacy_cultures_l_english.yml` : six clés par langue, UTF-8 avec BOM.

Les empreintes figurent dans `CANDIDATE_MANIFEST.json`, `INSTALLATION_PLAN.json` et `INSTALLATION_RECEIPT.json`. Aucun fichier de population, pays, événement, loi, technologie, frontière, ressource ou bâtiment n'est modifié par ce lot.

## Inventaire et démographie

L'inventaire élargi retrouve **109 consommateurs typés dans 16 fichiers effectifs** : 72 groupes de population, 11 références de cultures principales, 11 foyers, trois personnages, un ajout de culture principale en histoire tchétchène, un effet initial russe, huit usages événementiels du Caucase et deux branches natives de localisation personnalisée russe. Les occurrences du même mot dans les définitions d'ethnicités sont distinguées des références à une culture.

Onze définitions nationales emploient ces identifiants : DAG, SIB, SKH, ULT, TNS, FER, NCA, KMC, CKC, ABK et CAUC. Cinq apparaissent dans les instructions initiales de propriété d'État : SKH, ULT, CKC, ABK et CAUC. Les autres ne sont pas créées ou activées par la correction. L'ensemble des 646 TAG présents dans ces instructions possède une liste de cultures définies et non vide ; cette vérification statique ne prouve pas leur instanciation moteur.

| Périmètre scripté | Avant | Après | Écart |
| --- | ---: | ---: | ---: |
| 54 groupes nord-caucasiens | 591 979 | 591 979 | 0 |
| 18 groupes sibériens | 150 297 | 150 297 | 0 |
| Total concerné | 742 276 | 742 276 | 0 |
| Total de tous les enregistrements de population effectifs | 837 328 654 | 837 328 654 | 0 |

Les **6 815 enregistrements**, les empreintes des **18 fichiers** de population, les totaux des **677 États** et **644 propriétaires** sont conservés. La comparaison des 72 blocs concernés conserve aussi religions, types, États, propriétaires et tous leurs autres champs par empreinte. Aucun changement de classification d'un enregistrement ni transfert numérique n'est effectué. Ces sommes portent sur les valeurs inscrites dans les scripts effectifs, y compris leurs branches ; elles ne sont pas une population observée en jeu ni une mesure de pertes causées par l'ancien défaut.

`POPULATION_RECORDS.csv`, `STATE_TOTALS.csv`, `COUNTRY_TOTALS.csv` et `CONSUMERS.csv` rendent les vérifications consultables. Les fichiers JSON conservent les empreintes et détails reproductibles.

## Sources et limites

La [révision fc8143b du miroir Victoria-3-files](https://github.com/tjysdsg/Victoria-3-files/blob/fc8143b83f54f8abed97fc556b556e4085b6e691/game/common/cultures/00_cultures.txt) a été consultée directement, ainsi que ses localisations FR/EN. Son commit du 18 juin 2025 annonce une mise à jour vers 1.9.0. `LEGACY_PROVENANCE.json` conserve les deux blocs et les noms vérifiés. Cette copie versionnée établit une définition antérieure réelle, sans prétendre être une provenance officielle ou le bloc exact de 1.13/1.14.

La syntaxe et les dépendances sont confrontées aux données canoniques installées : cultures actuelles, `common/discrimination_traits/discrimination_traits.md`, héritages, langues, traditions, groupes, graphismes, ethnicités, lois de citoyenneté et constantes d'assimilation. Aucun fichier canonique n'est modifié.

La précision ethnolinguistique des anciens groupes reste une limite héritée. Le classement nord-caucasien utilise maintenant l'héritage européen régional natif plutôt que le vieux trait moyen-oriental ; les nouvelles langues agrégées n'accordent pas de proximité linguistique arbitraire envers d'autres cultures. Les résultats d'acceptation et d'assimilation en partie doivent donc être testés ; il n'est pas promis de reproduire exactement l'ancien moteur. Les lois, seuils, taux et foyers ne sont pas changés.

## Contrôles exécutés

1. `issue40_culture_compatibility_audit.py --baseline` : fournisseurs absents confirmés, 109 consommateurs, 72 groupes et leurs effectifs reproduits ; aucune erreur de lecture.
2. Premier candidat : **1 791/1 793**, deux échecs du contrôleur graphique, qui consultait un mauvais dossier d'ethnicités. Les fournisseurs existent dans `common/ethnicities`. Le résultat est conservé ; aucun fichier du jeu n'a été modifié pour le faire passer.
3. Candidat corrigé R2 : **1 793/1 793**, et **15/15** contrôles négatifs détectés.
4. Précontrôle d'installation : les **2 509 fichiers runtime préexistants** de la baseline sont encore identiques ; les cinq destinations sont absentes et les cinq candidats conformes aux empreintes.
5. Audit de l'installation réelle : **1 794/1 794**, **15/15** contrôles négatifs, zéro fichier préexistant modifié. Les contrôles négatifs injectent des défauts dans les données analysées : fournisseur absent/doublonné, ancien champ, mauvais héritage/groupe/type, localisations/noms manquants, graphisme invalide, population/religion/total altérés, consommateur supprimé et BOM absent.
6. Outil existant `issue24_map_dlc_audit.py --skip-pixels` : **324 cultures**, aucune référence culturelle manquante, aucun groupe de population de culture absente, aucune erreur de lecture. Son statut global reste `FINDINGS_STATIC_ONLY` pour **14 allocations multiples** et **quatre anciens TAG natifs absents**, déjà hors périmètre de 40. Aucun de ces problèmes n'est masqué ou déclaré résolu.
7. Ancien lecteur `population_1776_baseline.rows()` : échec **avant et après**, car son lecteur de champs ne reconnaît pas 108 blocs existants écrits sur une seule ligne. Exemple : population allemande de PAS dans STATE_AUSTRIA, taille 1 400. Les preuves d'échec sont conservées ; l'outil et sa baseline historique ne sont pas réécrits. Les comparaisons structurelles de tous les enregistrements et leurs totaux sont réalisées par le nouveau contrôleur, sans affirmer que l'ancien outil a réussi.

Les contrôles statiques ne démontrent ni chargement moteur, ni rendu, ni assimilation en simulation. Le protocole groupé est dans `RUNTIME_PROTOCOL.md`.

## Concurrence et protections

Les journaux 39, les fichiers des portages 21/27, les frontières et suivis WORLD/SERG, les populations, technologies et recettes communes sont préservés. Deux fichiers ajoutés pendant le travail par un autre chantier sont conservés et exclus de la livraison 40 : `common/production_method_groups/09_misc_resource.txt` et `common/production_methods/12_subsistence.txt`.

Les preuves d'installation recensent seulement les cinq nouvelles sources appartenant à 40. HEAD et index Git sont inchangés aux contrôles effectués ; aucune opération Git d'écriture ou publication du code n'a été lancée. La mise à jour du suivi GitHub ne vaut pas publication des fichiers locaux.

## Prochaine action

Effectuer les tests moteur de `RUNTIME_PROTOCOL.md`, puis consigner uniquement les observations réellement confirmées. La livraison technique est prête à relire ; aucune acceptation joueur n'est créée et la mission reste ouverte.
