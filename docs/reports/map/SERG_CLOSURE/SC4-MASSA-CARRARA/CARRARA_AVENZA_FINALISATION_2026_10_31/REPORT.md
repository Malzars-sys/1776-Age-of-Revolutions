# SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %

**SC4-MASSA-CARRARA — finalisation ciblée Carrare/Avenza, 31 octobre 2026.**

**Réponse : pas encore de contour historiquement assez étayé pour installer l'extension.** La donnée de 1775 est désormais confirmée sur le fac-similé : 3 700 habitants pour la ville et 8 010 pour la commune. Les quatorze localités de la principauté sont confirmées par la notice d'archives. Mais la couverture du total communal et la correspondance des grandes localités avec les cellules restent à établir ; aucun transfert arbitraire de pixels ou de POPs n'a été réalisé.

## Acquis préservés et décision

- MC-I-CORE reste reçu dans son périmètre exact : MCA, Marie-Thérèse, huit cellules xEDBC00, 10 000 habitants, administration et droits impériaux. Le reçu du 23 octobre n'est ni modifié ni étendu.
- Le bitmap courant confirme 108 cellules résiduelles MOD pour xF08021. A/B/C conservent la connexité ; l'ancienne variante de trois cellules créerait le résidu MOD 104 + 1 et reste rejetée.
- L'hypothèse B de cinq cellules est préparée comme proposition de travail, sans prétendre que la géométrie démontre sa frontière historique. Ni A, ni B, ni C n'est installé.
- Aucun changement des voisins GEN/LUC/TUS/PAR, des bâtiments, PM, ressources, unités, propriétaires, pays ou droits impériaux. Toujours 581 titres et neuf électeurs.

La preuve manquante est précisément localisée : **AS Massa, Archivio storico del Comune di Carrara, I Serie, cartes Avenza 1775 b.84–86 et Carrare 1775 b.87–88**. Leurs cotes sont lues dans l'inventaire téléchargé ; les images des cartes originales n'y figurent pas et ne sont pas prétendues consultées. Le relevé des maisons de 1775 b.65 et les actes du cadastre b.250 peuvent aider à vérifier le ressort statistique, sans confondre maisons, biens et habitants.

## Livrables

1. [Rapport historique et cartographique](HISTORICAL_AND_MAP_REPORT.md), [matrice des localités](JURISDICTION_REVIEW.csv) et [source exacte des lectures](SOURCES.md).
2. [Cellules et topologie actuelles](CURRENT_GEOMETRY_AND_OPTIONS.json), [continuité MOD et voisinages](CANDIDATE_COUNTRY_TOPOLOGY.json), illustration des trois candidats.
3. [Démographie et couvertures](DEMOGRAPHIC_REPORT.md) : transfert éventuel de 8 010, jamais 3 700 + 8 010 ; aucune application actuelle.
4. [Proposition B et incertitudes](B_PROPOSAL_AND_UNCERTAINTIES.md), [décision structurée](RESEARCH_DECISION.json).
5. [Tests et conservation](TECHNICAL_VERIFICATION.md), journaux bruts et manifeste exact des fichiers.
6. [Protocole joueur conditionnel](PLAYER_TEST_PROTOCOL.md) : nouvelle partie 1776, nouvelle extension seulement si livrée, inspection MCA/MOD/voisins/droits, un mois et sauvegarde/rechargement. Aucun nouveau test demandé pour les seuls documents ; aucun moteur exécuté.

## Avant / après réellement acquis

| Mesure | Avant | Après |
| --- | ---: | ---: |
| Cellules MCA | 8 | **8** |
| Parent MOD xF08021 | 108 | **108** |
| Population MCA/Émilie | 10 000 | **10 000** |
| Groupe MOD/Émilie | 495 752 | **495 752** |
| Population mondiale | 837 328 654 | **837 328 654** |
| Jalons qualifiés | 32/81 | **32/81** |
| Points | 93/235 | **93/235** |
| Pourcentage canonique | 39,57 % | **39,57 %** |
| SC4-MASSA-CARRARA | BLOCKED P0 | **BLOCKED P0** |

Si territoire et couverture statistique sont ultérieurement établis, le transfert conservatif proposé conduirait à MCA 18 010 et MOD/Émilie 487 742. Ces valeurs sont **conditionnelles**, pas installées, et ne donnent aucun des trois points régionaux.

## Contrôles et suite

**44/44 contrôles ciblés PASS.** Tests anciens Massa : **10/11 PASS**, une assertion obsolète de dernière couche classée et conservée. Suivi canonique : **27 PASS, un SKIP prévu** ; validateur PASS. Les anciens 134/134 et 411/416 ne sont pas revendiqués comme nouveaux tests.

Prochaine action unique : obtenir ou retrouver les reproductions des cartes contemporaines identifiées et établir la concordance des grandes localités et du total communal. Aucun nouveau territoire ; Teschen reste suspendu de recherche active. Le dossier est préparé sur la branche dédiée, avec conservation des travaux diplomatiques du répertoire principal. Aucune PR fonctionnelle créée puisqu'aucune installation n'est justifiée. Les fichiers canoniques sont actualisés seulement pour cette recherche et son blocage, sans nouvelle validation humaine.


## Vérification du répertoire principal du mod

Après les tests de la copie isolée, **15/15 contrôles de conservation** passent également dans le répertoire principal : propriétaires, POPs, bâtiments et unités des six pays ciblés, total mondial et dix dépendances fonctionnelles correspondent à la version vérifiée. Les fins de ligne du checkout sont normalisées uniquement pour cette comparaison de texte ; le bitmap est comparé octet par octet. Les modifications diplomatiques locales inventoriées au départ restent inchangées. Seuls ce nouveau dossier et les cinq vues/fichiers de suivi SERG ont été publiés dans le répertoire principal ; aucun fichier de gameplay. Le validateur canonique y donne PASS, 93/235 et 39,57 %. Preuves : `PRIMARY_WORKSPACE_CHECK.json`, `PRIMARY_PUBLICATION_CHECK.json`, `WORKSPACE_CONTEXT.json`.
