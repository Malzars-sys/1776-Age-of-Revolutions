# SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %

Passe du **23 octobre 2026**. Une seule nouvelle étape exécutée : **SC4-SAVOY-NICE**, P0 sans dépendance, confirmée par le suivi après enregistrement du reçu italien. [Autorisation](AUTHORIZATION.md), [audit et décisions](SECTOR_AUDIT.md), [sources et limites réelles de consultation](SOURCES.md).

## Validation précédente et progression

**IT-I-MOD, IT-I-PAR, IT-I-LUC : PASS_RUNTIME_USER_VALIDATED** pour les trois seules administrations. Confirmation intégrale du protocole par le joueur : nouvelle partie au 1er janvier 1776, administrations présentes et fonctionnelles, république de Lucques et administrations TUS conservées, vérifications de conservation réussies, mois complet, sauvegarde/rechargement sans anomalie. [Attestation bornée](../SC4-EXISTING-ITALIAN-STATES/RUNTIME_USER_ATTESTATION_2026_10_23.json), [acceptation additive](../SC4-EXISTING-ITALIAN-STATES/ACCEPTANCE_2026_10_23.md), mission intégrale conservée à côté. Aucune capture, mesure ou date effective de test inventée.

Le contrôle préalable passe **12/12**, le validateur canonique PASS. L'installation italienne et son manifeste original sont intacts; aucun changement fonctionnel intervenu depuis cette livraison n'a été trouvé. **SC4-EXISTING-ITALIAN-STATES reste BLOCKED** : droits de Lucques, Parme/Guastalla, liens Habsbourg/Bourbons/Espagne et traduction constitutionnelle ouverts. Aucun crédit régional tiré des trois reçus.

Progression vérifiée avant/après : **82/235 = 34,89 % → 82/235 = 34,89 %**. Périmètre **1.0.0**, 81 tâches, 24 qualifiées, barème inchangé. SERG-RM-0018 consigne la validation italienne limitée; SERG-RM-0019 consigne la passe Savoie–Nice, sans point supplémentaire.

## Recherche et corrections installées

Les traités de 1754, 1713/1718 et 1760 sont distingués des annexions révolutionnaires et de 1860. La carte de 1750 déjà conservée a été relue comme contexte; elle ne vaut pas limite postérieure à 1760. Les notices de l'édition Borgonio/Stagnon de 1772 fournissent une piste précise pour reprendre la cartographie, sans image distante prétendue lue. Chambéry conserve ses administrations sous le roi de Sardaigne; Nice dispose de son Sénat et de ses offices avant 1776. Ces institutions justifient les deux corrections.

| Sous-lot indépendant | Avant → après | Fichier fonctionnel nouveau |
| --- | --- | --- |
| **SN-I-SAV** | Administration publique SAR en Savoie : **0 → 1 niveau** | `common/history/buildings/1776_sc4_savoy_administration.txt` |
| **SN-I-NIC** | Administration publique dans la seule subdivision SAR de Provence/Nice : **0 → 1 niveau** | `common/history/buildings/1776_sc4_nice_administration.txt` |

Capacité institutionnelle de catégorie **B**, sans effectif ou budget historique inventé. Propriété publique SAR, réserve 1; organisation simple, bureaucratie héréditaire, bureaucrates religieux et absence de collecte organisée des données. Les définitions effectives, groupes de PM et conditions initiales de SAR sont vérifiés. Aucun nouveau pays, vassal, monarque ou régime créé. [Implémentation](IMPLEMENTATION.json), [politiques effectives](INITIAL_POLICIES.json), [fichiers et empreintes](FILES_MODIFIED.json).

## Territoires, population et bâtiments conservés

| Portion | RGB / cellules avant = après | Population initiale avant = après |
| --- | --- | --- |
| Savoie SAR | 4 / 802 | 365 664 |
| Nice, portion SAR de Provence | 1 / 177 | 134 316 |
| **Périmètre principal** | **5 / 979** | **499 980** |

Savoie : `x56B04B` 299 cellules, `x6B4BA4` 264, `xD000E0` 152, `xDDDD3B` 87; Nice : `x5080E0` 177. Tous demeurent SAR. [RGB avant/après](RGB_BEFORE_AFTER.csv), [inventaire avec voisins, populations, bâtiments et unités](NATIVE_INVENTORY.json), [lecture de la carte native](NATIVE_READING.png).

Contexte protégé : Piémont SAR 9 RGB/2 227 cellules et 1 921 911 habitants, quatre niveaux administratifs conservés; île de Sardaigne 8 RGB/1 621 cellules et 408 786 habitants. Population mondiale : **834 926 252**, inchangée. Les chiffres décrivent le mod et ne certifient pas un recensement de 1776.

Tous les bâtiments antérieurs sont conservés, y compris les ports niçois hérités, routes, activités et unités. Victor-Amédée III, la monarchie et la capitale nationale à Turin/Piémont restent identiques. Les voisins FRA/SWI/GEN/AUS conservent leurs propriétaires; aucun transfert de cellule, aucun tracé moderne plaqué sur 1776.

## Registre et blocage régional

Les **574 lignes du registre** et les **neuf électeurs** sont inchangés. SAR est déjà membre national; ses neuf droits territoriaux restent limités au Piémont. La Savoie et Nice ne sont pas intégrées par le seul titre royal, et leur absence n'est pas approuvée définitivement.

Les notices de diplômes et dossiers d'investiture/vicariat attestent des droits continentaux distincts de l'île royale. La démarche électorale de 1773 n'autorise aucun électorat nouveau. Mais ces pièces ne suffisent pas à homologuer les limites de cinq gros RGB, ni à leur appliquer automatiquement tous les effets de restitution du système actuel. Les notices d'archives ne remplacent pas la lecture de chaque acte opératoire.

**SC4-SAVOY-NICE reste BLOCKED P0** pour la correspondance des frontières de 1754/1760 et la traduction des droits d'investiture/vicariat dans les mécanismes impériaux. Reprise concrète : cartes 1772 et plans de limitation genevois/franco-sardes, liste fermée de candidats B, confrontation des dossiers 1773–1774 référencés, ou arbitrage explicite exposant les effets. Aucun nouveau recalage improductif, aucune revendication sur toute la Provence, Genève, les diocèses du vicariat ou toute SAR. Les deux administrations sont indépendantes de ce blocage.

## Contrôles réellement exécutés

- [Statique](VALIDATION.json) : **101/101** réussis. Inventaire mondial, syntaxe des ajouts, propriétaires, RGB, populations, bâtiments, unités, PM, régime, registre, preuves antérieures et index Git contrôlés. Les 44 doublons RGB et 12 références invalides hérités restent strictement identiques; aucune nouvelle erreur de ces catégories.
- [Suite cumulative](TESTS.json) : **390 tests, 386 réussis, 3 échecs hérités, 1 exclusion**. Les trois assertions anciennes supposent une précédente couche finale du registre; la chaîne courante Salzbourg et les 574 droits passent leurs gardes. Aucun échec nouveau inexpliqué.
- [Suite ciblée](SCOPED_TESTS.json) : **130 tests, 129 réussis, 1 exclusion**, aucun échec. Neuf nouveaux tests vérifient les erreurs de périmètre, propriété, capacité, effets hors champ et l'impossibilité de clore une région avec un reçu partiel. Aucun ancien test réécrit. [Classement des résultats](TEST_REVIEW.json).
- L'exclusion concerne le contrôle de non-modification de l'initialisation originale. Tests finaux après suivi : **51/52 réussis, une exclusion, aucun échec**. Validateur canonique PASS; contrôles de conservation dans `FINAL_CHECKS.json`. Le contrôle de blancs du diff retrouve quatre lignes avec espaces finaux dans `common/history/pops/00_west_europe.txt`, fichier préexistant conservé octet pour octet; dette héritée classée dans `DIFF_CHECK.json`, sans réécriture. Aucun moteur de jeu exécuté par l'agent.

## Conservation, test joueur et prochaine action

Les **2 409 fichiers fonctionnels préexistants** sont intacts octet pour octet; seuls deux fichiers nouveaux sont ajoutés. Les noyaux approuvés, administrations italiennes et autrichiennes, corrections MAP2A, institutions et autres données antérieures sont conservés. Fortifications modernes, Corps du génie, implantation des forteresses, unités spécialisées, États-Unis/Minutemen, accords franco-américains, Saint-Gobain/Anzin et autres travaux français restent intacts. Aucune restauration depuis une ancienne baseline, aucune opération Git d'écriture et aucun fichier vanilla modifié.

**SN-I-SAV et SN-I-NIC attendent votre validation en jeu** : [protocole complet](PLAYER_TEST_PROTOCOL.md), nouvelle partie 1776, contrôle distinct des deux administrations et des conservations, un mois, sauvegarde/rechargement. Statut des installations **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**; aucun reçu anticipé. Ce test ne clôturera pas automatiquement la région.

Prochaine candidate P0 indépendante calculée : **SC4-LIGURIAN-FIEFS**, laissée **NOT_STARTED**, sans recherche ni installation commencée. Innviertel, Hohenberg/Fricktal, chantier naval, questions juridiques italiennes, Teschen et autres blocages demeurent séparés. La mission s'arrête après cette seule nouvelle étape.
