# WORLD RULERS 1776 R1 — livraison

Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.
31 pays reçoivent un dirigeant historique, représentant 30 personnes distinctes. Cayor et Baol partagent le même titulaire dans deux représentations techniques, sans modifier leur relation diplomatique.
645 pays actifs ont une décision traçable. Les personnages déjà marqués historiques sont préservés, sans nouvelle certification de leur biographie. Les souverains d’unions personnelles et les responsables historiques de compagnies sont distingués des lacunes.

| Décision | Pays |
| --- | ---: |
| COVERED_COMPANY_EXECUTIVE | 3 |
| COVERED_PERSONAL_UNION | 6 |
| DEFER_APPOINTMENT | 3 |
| DEFER_AUTHORITY | 1 |
| DEFER_CHRONOLOGY | 1 |
| DEFER_COLLECTIVE | 7 |
| DEFER_CONFLICT | 6 |
| DEFER_EXACT_OFFICEHOLDER | 1 |
| DEFER_NO_VERIFIED_REPRESENTATIVE | 236 |
| DEFER_SOURCE_GAP | 85 |
| DEFER_TRANSITION | 6 |
| HISTORICAL_RULER_INSTALLED_R1 | 31 |
| PRESERVE_EXISTING_SCRIPTED_HISTORICAL_RULER | 259 |

Contrôles statiques : 490/490. Chargement moteur, rendu, chronologie après simulation : NON TESTÉS. Aucun reçu humain créé.
Population mondiale : 837328654 → 837328654. Aucune cellule/RGB, frontière, ressource, bâtiment, recette, technologie ou loi modifiée. Quatre fichiers fonctionnels nouveaux, aucune réécriture de fichier partagé.
Préservation vérifiée par empreintes : fichiers fonctionnels préexistants, suivi SERG, références vanilla consultées, HEAD/branche/index Git. Les travaux Durrani, TECH, ECON, Amériques et autres ajouts présents à la capture d’installation sont conservés. Les évolutions antérieures à cette capture sont distinguées dans la comparaison des inventaires.

Fichiers : `FICHES_DIRIGEANTS.md`, `SOURCES.md`, `DECISIONS.md`, `COUNTRY_DECISIONS.json`, `STATIC_CHECKS.json`, `APPLY_BASELINE.json`, `INSTALLED.json`.

Protocole de contrôle en jeu : nouvelle partie au 1er janvier 1776, inspecter notamment Boina (Ravahiny), Shewa, Choughnan, Chaki, Cayor/Baol et les quatre Waldburg ; vérifier noms, traits, IG et absence de second dirigeant dans les unions/compagnies. Les personnages de Tonga et des Cherokees gardent un pays de type décentralisé : vérifier aussi leur disponibilité dans les vues de personnages, sans conclure de la seule syntaxe à un affichage natif garanti. Sauvegarder/recharger et vérifier la persistance. Aucun test intermédiaire d’une région territoriale n’est requis par cette livraison.

Lieux de naissance : un seul lieu probable recoupé ici (Chota pour Oconostota), explicitement non certain ; les autres restent inconnus. Les sources retenues ne donnent aucune nouvelle date de naissance complète assez sûre ; aucune date fictive n’a été introduite pour remplir les fiches.

Prochaine action : vérification des personnages livrés dans une nouvelle partie ; les dossiers différés restent documentés, sans création d’identité de remplacement. Aucune autre région territoriale n’est lancée.

Le premier contrôle des traits a produit 27 faux écarts, car il comparait aussi des positions de texte. La comparaison corrigée porte sur les définitions analysées, strictement identiques au vanilla. L’exécution initiale est conservée dans STATIC_CHECKS_INITIAL_FAILED.json ; aucun trait n’a été modifié pour satisfaire le test.
L’inventaire VFS détecte aussi 25 références héritées à des modèles vanilla supprimés (notamment personnages de1836). Elles étaient présentes avant cette installation et ne sont pas réintroduites. Voir APPLY_BASELINE.json, inventory.unresolved_templates : dette antérieure distinguée des nouveaux personnages.
