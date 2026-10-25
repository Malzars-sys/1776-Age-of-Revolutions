# SC4-PIOMBINO — audit et blocage territorial

**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

Avant/après : **82/235 → 82/235**, 24 tâches qualifiées, périmètre 1.0.0, 81 tâches, poids inchangés. La tâche est **BLOCKED P0**, aucune nouvelle installation, aucun point acquis.

## Reçu précédent

**LF-GEN-ADM-PM : PASS_RUNTIME_USER_VALIDATED**, selon votre confirmation intégrale du protocole. Reçu distinct dans `../SC4-LIGURIAN-FIEFS/RUNTIME_USER_ATTESTATION_2026_10_23.json`, mission originale conservée, **9/9 contrôles d'acceptation**. Événement additif **SERG-RM-0022** ; les 21 événements antérieurs sont inchangés. Aucune date effective du test, mesure, capture, langue ou observation supplémentaire inventée. **SC4-LIGURIAN-FIEFS reste BLOCKED P0**, sans crédit territorial.

Le validateur PASS confirme ensuite **SC4-PIOMBINO**, P0 sans dépendance, seule nouvelle tâche de la mission.

## Elbe existe-t-elle ?

**Oui : 54 cellules de terre dans la carte du mod**, et non une île à créer. Elles partagent toutefois le RGB **x6A7662** avec **165 cellules continentales**. Les **219 cellules sont TUS / STATE_TUSCANY**, sans séparation des souverainetés de 1776. ELBA_NATIVE_EVIDENCE.json contient le masque exact, ses limites et son contrôle de connexité ; ELBA_DETAIL.png le rend visible. Aucun lancement moteur ou capture du jeu n'est revendiqué par l'agent.

## Résultat historique et corrections

Les sources archivistiques distinguent la principauté, Gaetano Boncompagni Ludovisi en 1776, le ressort toscan de Portoferraio, les possessions princières et Longone napolitain. Elles imposent aussi de distinguer la dignité impériale et les droits supérieurs napolitains. Antonio ne succède qu'en 1777 ; les réorganisations de 1801/1805/1815 ne sont pas une carte de départ. Sources réellement lues et limites d'accès dans SOURCES.md ; huit ensembles examinés dans JURISDICTION_MATRIX.csv.

**Aucune correction fonctionnelle installée.** L'omission de Piombino et la représentation uniforme d'Elbe sont démontrées, mais une attribution de fragments, une population correspondante et la traduction des droits restent à établir. Donner tout le RGB partagé au prince entraînerait aussi un morceau de côte toscane ; lui donner toute l'île effacerait Portoferraio et Longone. Une simple administration TUS supplémentaire ne corrigerait pas cette erreur politique. Aucun changement artificiel créé.

**B_PROPOSAL.md** prépare deux solutions : ensemble princier continental/insulaire avec trois autorités sur Elbe, ou noyau continental B en conservant le blocage insulaire. Le masque physique de l'île est acquis ; la division politique manque. Les documents de reprise sont identifiés précisément. Aucun cadastre parfait exigé, aucun recalage forcé, aucune conservation définitive de l'erreur approuvée.

| Donnée contrôlée | Avant | Après |
|---|---|---|
| Elbe dans le bitmap | 54 cellules TUS, même RGB que le continent | identique |
| x6A7662 | 219 = 165 continentales + 54 insulaires | identique |
| Ensemble TUS | 6 RGB / 1321 cellules | identique |
| Population TUS | 1273269, deux groupes initiaux | identique |
| Bâtiments TUS | 10 déclarations, deux niveaux administratifs existants | identique |
| TAG PIO | absent | absent ; disponibilité du code seulement relevée |
| Régions, propriétaires, unités, capitales, gouvernements et pactes | état courant capturé | identique |
| Registre et électeurs | 574 droits / neuf électeurs | identique |
| Fichiers fonctionnels | 2411 | 2411, tous octets conservés |

## Contrôles et suite

Contrôles statiques : **33/33**. Suite cumulative : **401 réussites / 405**, trois anciennes assertions de fin de registre et une exclusion initiale. Suite ciblée : **144 réussites / 145**, même exclusion, aucun échec. Les six nouveaux tests de connexité, de portée et de reçu réussissent. Aucun nouvel échec ou échec inexpliqué ; aucun ancien test réécrit. Résultats dans VALIDATION.json, TESTS.json, SCOPED_TESTS.json et leurs journaux. Les 44 doublons et 12 références invalides de la dette cartographique restent inchangés.

Après actualisation du suivi : **66 réussites / 67**, même exclusion initiale, aucun échec. Validateur canonique **PASS**, 82/235 et SC4-MASSA-CARRARA confirmés. Le contrôle final est consigné dans FINAL_CHECKS.json et TRACKER_VALIDATION_FINAL.json. Les quatre signalements d'espaces hérités de `common/history/pops/00_west_europe.txt` (2983, 2999, 3015, 3031) sont conservés dans DIFF_CHECK.json, fichier non réécrit.

Toutes les corrections validées et tous les fichiers fonctionnels militaires, américains, diplomatiques et français sont conservés. Les contrôles d'empreinte couvrent aussi les preuves anciennes, HEAD, branche et index. Aucun Git ni vanilla écrit.

Pas de nouveau test moteur requis pour cette passe sans installation ; PLAYER_TEST_PROTOCOL.md décrit une reconnaissance facultative, sans pouvoir de clôture. Prochaine candidate indépendante **SC4-MASSA-CARRARA**, seulement identifiée après recalcul ; aucune deuxième tâche commencée. Les blocages Innviertel, Hohenberg/Fricktal/chantier naval, droits italiens, Savoie–Nice, fiefs ligures, Teschen et les autres dépendances canoniques restent ouverts.
