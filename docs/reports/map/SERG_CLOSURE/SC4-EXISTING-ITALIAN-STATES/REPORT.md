# SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %

Passe du 19 octobre 2026. Une seule nouvelle tâche exécutée : **SC4-EXISTING-ITALIAN-STATES**, P0 admissible, sélectionnée après l'enregistrement du reçu d'Autriche antérieure et contrôle du suivi. [Autorisation](AUTHORIZATION.md), [sources historiques et limites de consultation](SOURCES.md), [audit régional](SECTOR_AUDIT.md).

## Attestation précédente et progression

Le joueur confirme intégralement le protocole AN-I-W/AN-I-A/AN-P-A. [Attestation humaine](../SC2-ANTERIOR-AUSTRIA/RUNTIME_USER_ATTESTATION_2026_10_19.json), [acceptation additive](../SC2-ANTERIOR-AUSTRIA/ACCEPTANCE_2026_10_19.md), mission originale conservée dans le même dossier. Les deux administrations AUS et la correction du propriétaire public du port sont **PASS_RUNTIME_USER_VALIDATED pour les seuls sous-lots installés**. Aucune observation, capture, date effective de test ou langue supplémentaire n'est inventée.

L'Autriche antérieure reste **BLOCKED**, Hohenberg/Fricktal et propriété du chantier naval ouverts. Le reçu ne vaut ni clôture territoriale ni certification cadastrale. Un nouveau garde du suivi refuse explicitement d'utiliser ce reçu limité pour attribuer un PASS global. Contrôle d'acceptation : 12/12, validateur PASS.

Progression avant/après : **82/235 = 34,89 % → 82/235 = 34,89 %**, 24 tâches qualifiées, périmètre 1.0.0 et barème inchangés. SERG-RM-0016 consigne le reçu partiel sans point; SERG-RM-0017 consigne cette nouvelle passe sans point. Aucune nouvelle installation italienne n'est validée humainement.

## Modifications réellement installées

| Sous-lot indépendant | Installation | Fichier nouveau |
| --- | --- | --- |
| IT-I-MOD | Un niveau administratif public MOD, auparavant absent | `common/history/buildings/1776_sc4_mod_administration.txt` |
| IT-I-PAR | Un niveau administratif public PAR, auparavant absent | `common/history/buildings/1776_sc4_par_administration.txt` |
| IT-I-LUC | Un niveau administratif public LUC, auparavant absent | `common/history/buildings/1776_sc4_luc_administration.txt` |

Les offices ducaux de Modène et de Parme et les magistratures républicaines lucquoises préexistent à 1776. Les trois niveaux sont des abstractions administratives B, sans effectif ou budget historique prétendu exact. Les quatre méthodes sont compatibles avec les lois et technologies initiales vérifiées, y compris les substitutions république/oligarchie de Lucques. La méthode bureaucratique n'institue pas de monarchie. Les deux niveaux administratifs toscans déjà présents restent inchangés.

**Aucun fichier fonctionnel préexistant n'a été réécrit.** Aucun changement de propriété territoriale, frontière, population, titulaire, loi, pacte, unité ou registre. [Implémentation](IMPLEMENTATION.json), [fichiers et empreintes](FILES_MODIFIED.json), [politiques initiales effectives](INITIAL_POLICIES.json).

Le suivi et ses vues sont actualisés. Son outil `tools/serg_closure_roadmap.py` distingue désormais les reçus partiels de la clôture globale et affiche les corrections validées sous blocage. Trois outils nouveaux portent l'enregistrement du reçu, la passe italienne et ses tests : `serg_closure_accept_anterior_austria.py`, `serg_sc4_italian_states.py`, `test_serg_sc4_italian_states.py`. Les anciens tests restent intacts. Le manifeste de livraison final énumère les documents, outils et fichiers fonctionnels concernés.

## Périmètre inspecté et conservé

| Pays existant | RGB / cellules | Population initiale conservée |
| --- | --- | --- |
| Modène | 2 / 452 | 505 752 |
| Parme | 2 / 463 | 368 163 |
| Lucques | 1 / 174 | 84 558 |
| Toscane | 6 / 1 321 | 1 273 269 |

Total : **11 RGB / 2 410 cellules, 2 231 742 habitants écrits**. Les trois pays corrigés regroupent 958 473 habitants initiaux. Population mondiale conservée : 834 926 252. Ces valeurs décrivent l'installation et ne certifient pas un recensement de 1776. [Chaque RGB avant/après](RGB_BEFORE_AFTER.csv), [inventaire complet et voisins](NATIVE_INVENTORY.json), [carte native](NATIVE_READING.png).

MOD/PAR/TUS sont déjà membres du système impérial et bénéficiaires de dix lignes du registre; LUC est présent territorialement mais absent de ces listes. Ce constat technique ne tranche pas les droits historiques. François III, Ferdinand et Pierre-Léopold sont déjà installés; Lucques reste une république oligarchique sans souverain nommé artificiellement par cette passe.

Le contexte historique distingue Modène/Reggio de Ferrare pontificale, le gouvernement bourbonien de Parme des possessions directement autrichiennes, et la Toscane dynastique d'une annexion par AUS. Les voisins vénitiens et pontificaux ne deviennent pas impériaux par proximité. Piombino, Massa-Carrare, Présides/Elbe, fiefs ligures, Savoie/Nice et franges milanaises restent des dossiers distincts; leur examen d'interface ne les commence pas. Aucune frontière napoléonienne ou de 1815 projetée sur 1776.

## Contrôles exécutés

- [Statique](VALIDATION.json) : **91/91** réussis. Inventaire mondial et toutes les données antérieures conservés, contrats des trois ajouts, méthodes compatibles, république de Lucques, gardes du registre courant, reçu partiel non transformable en clôture globale, preuves précédentes et Git contrôlés.
- [Suite cumulative](TESTS.json) : **381 tests, 377 réussis, 3 échecs hérités, 1 exclusion**. Les trois échecs concernent des assertions anciennes supposant une précédente couche finale du registre. La couche actuelle Salzbourg et les 574 lignes conservées passent leurs gardes.
- [Suite ciblée](SCOPED_TESTS.json) : **121 tests, 120 réussis, 1 exclusion**, aucun échec. Quinze nouveaux tests couvrent les limites des installations et du reçu partiel. Aucun ancien test réécrit, aucun nouvel échec inexpliqué. [Classement](TEST_REVIEW.json).
- L'exclusion vise seulement le contrôle de non-modification propre à l'initialisation d'origine. Les 44 doublons RGB et 12 références invalides hérités restent strictement identiques à l'instantané; aucune nouvelle erreur de ces catégories.
- [Validateur du suivi](TRACKER_VALIDATION.json); contrôles finaux après actualisation dans `FINAL_CHECKS.json` et `FINAL_TESTS.json`. Aucun moteur de jeu lancé par l'agent.

## Protections et concurrence

Les 2 406 fichiers fonctionnels préexistants sont conservés octet pour octet; seuls trois fichiers sont ajoutés. Cela protège les administrations et corrections validées de l'Autriche intérieure/antérieure, Ljubljana, Bohême/Moravie, Silésie/MAP2A, Salzbourg/Passau/Freising/Ratisbonne, tous les autres noyaux approuvés et leurs institutions. Les 574 droits impériaux et neuf titres électoraux ne sont pas modifiés.

Les fortifications, Corps du génie, unités militaires, États-Unis, Minutemen, accords franco-américains, Saint-Gobain, Anzin et autres modifications françaises restent identiques à l'instantané courant. Aucune restauration depuis une baseline ancienne. HEAD, branche et index conservés; aucune écriture Git, aucun fichier vanilla modifié. Les anciens rapports d'installation restent intacts : les reçus et commentaires d'acceptation sont additifs.

## Blocages, test joueur et suite

La tâche régionale reste **BLOCKED**. Il faut encore établir la traduction des droits juridiques de Lucques en obligations dans le système constitutionnel du mod, ainsi que la portée des droits impériaux de PAR/Guastalla et du protectorat espagnol. Ni le titre impérial seul ni l'influence d'une dynastie ne justifient une soumission uniforme. Le registre et le pacte sont maintenus provisoirement, sans approbation définitive. Ces lacunes demeurent P0; elles ne sont pas reclassées P2.

Les trois sous-lots sont **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. [Protocole joueur](PLAYER_TEST_PROTOCOL.md) : nouvelle partie 1776, vérification séparée des trois administrations et des conservations ciblées, un mois complet puis sauvegarde/rechargement. Une réussite de ces bâtiments ne résoudra pas les questions juridiques et ne suffira pas à fermer la tâche régionale.

Prochaine action du joueur : ce protocole. Prochaine candidate P0 indépendante calculée : **SC4-SAVOY-NICE**, laissée NOT_STARTED, sans recherche ni installation commencée. Hohenberg/Fricktal et chantier naval restent ouverts; SC2-AUSTRIA demeure BLOCKED pour l'Innviertel; SC2-TESCHEN reste indépendant. La mission s'arrête après cette seule nouvelle tâche.
