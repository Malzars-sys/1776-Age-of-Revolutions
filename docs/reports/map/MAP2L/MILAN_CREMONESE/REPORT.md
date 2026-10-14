# MAP-2L — Continuité du Milanais et du Crémonais

Correction appliquée le 13 octobre 2026, cible : 1er janvier 1776. Aucun lancement du jeu, commit ou changement de playset.

## Résultat

Les possessions autrichiennes de `STATE_LOMBARDY` formaient deux composantes terrestres. Elles forment désormais une seule composante connectée par les côtés des pixels, et non par leurs coins. La correction porte sur le Crémonais et les possessions mantouanes adjacentes absorbés par l'ancienne province vénitienne mixte `x4713EE`. Ce n'est ni une annexion de tout Brescia, ni la création d'un nouveau pays Milan indépendant de l'Autriche.

La province de 325 pixels est scindée en trois : `x4713EE` (228 pixels, VEN, conserve le hub forestier), `xEDA700` (33 pixels, VEN, fragment occidental conservé), `xEDA701` (64 pixels, AUS, liaison méridionale). Deux nouveaux RGB ; 97 pixels recolorés, dont seulement 64 changent de propriétaire. Chaque RGB est connecté et déclaré une fois en Lombardie, région numérique 76, sans confondre ces trois types d'identifiants.

Les provinces `x867A90` et `x9AC196`, ainsi que toutes les provinces hors `x4713EE`, gardent leur tracé et leur propriétaire. Le Tyrol du Sud n'est pas modifié : le premier message avait été interprété à tort comme concernant Trente, avant la précision de l'utilisateur sur Milan.

## Fondement et limites historiques

Réutilisation des dossiers R1-0008/0009, MAP1B/LOMBARDY_READING.md, MAP1C/METHOD_AND_EVIDENCE.md et de leurs scans conservés. Le diagnostic MAP2B indiquait déjà que l'attribution intégrale de `x4713EE` à Venise absorbait une frange crémonaise. Les refus des anciens modèles de calage restent conservés ; cette correction limitée ne les transforme pas en frontières validées.

- [Terre ferme vénitienne, Regione Lombardia](https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.03) : Bergame, Brescia et Crema restent vénitiens ; le Brescian jouxte le territoire milanais de Crémone et le duché de Mantoue. Asola n'est pas assimilée automatiquement au Mantouan moderne.
- [Lombardia austriaca](https://www.lombardiabeniculturali.it/istituzioni/schede/8000357/) et [institutions autrichiennes](https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.06) : les institutions et circonscriptions applicables avant les réformes de 1786 sont distinguées de ces réformes postérieures.
- Scan Robert de Vaugondy, *Partie occidentale de la Lombardie*, 1750, BnF, identifiant `btv1b530425827`. Source originale conservée en MAP1B, SHA-256 `d9b6a956bce7a292e9760a16e9d2655504b1da4555f6bd85fe6c7c3b3f835632`. Le dérivé existant de 1 600 pixels est relu, sans télécharger ou substituer une nouvelle carte générale.

Le polygone suit l'enveloppe souveraine méridionale de Brescia, en laissant Crema et Asola vénitiennes. Seul son recoupement avec le parent mixte est appliqué. L'affine est reproductible à partir de Milan, Parme et Vérone, trois repères urbains, jamais des hubs contestés Bergame/Brescia. Les écarts aux contrôles sont explicitement conservés : Plaisance (ferme) 2,219 pixels, Côme (mine) 3,312, Gênes (port, hors secteur local) 5,107. Les trois points d'ajustement ont un résidu nul par construction : ce n'est pas une preuve indépendante.

**Statut : approximation historique à la résolution du jeu, pas frontière cadastrale certifiée.** Les micro-juridictions et le tracé exact de la strada cremasca restent abstraits. Les franges de Bergame/Brescia et Côme/Chiavenna non traitées ne sont pas déclarées entièrement corrigées. Mantoue garde ses institutions historiques distinctes malgré la représentation politique AUS commune. Aucune frontière extérieure au parent autorisé n'est redessinée pour forcer une connexion.

## Conservation et dépendances

70 406 habitants sont réaffectés de VEN à AUS, sans création : 70 394 avec religion par défaut et 12 juifs, tous nord-italiens. Allocation entière de gameplay sur la subdivision source complète, documentée dans PLAN.json ; elle n'est pas un recensement de 1776 ni une population historique déduite des pixels. Les quatre enregistrements source sont traités exactement une fois, depuis l'instantané immuable.

Tous les bâtiments, niveaux, méthodes de production, réserves et propriétaires économiques sont inchangés : les niveaux indivisibles existants restent dans leurs subdivisions. Aucune unité, conscription, capitale, ressource ou localisation de hub n'est déplacée. La nouvelle province hérite du terrain de son parent.

Le registre impérial gagne uniquement `xEDA701` pour AUS : 394 RGB et 62 580 pixels, soit +64. `xEDA700` et le reliquat `x4713EE` vénitiens ne sont pas inscrits au Saint-Empire. Le registre, les scripts compilés de restitution, les listes localisées et les deux représentations cartographiques sont actualisés ensemble. Les migrations distinguent maintenant les propriétaires physiques des seuls droits impériaux ; les tests anciens vérifient les deltas de pixels exacts plutôt que de geler l'ancienne superficie malgré une rétrocession autorisée.

## Fichiers de jeu modifiés

- `map_data/provinces.png`, `map_data/province_terrains.txt`, `map_data/state_regions/01_south_europe.txt`.
- `common/history/states/00_states.txt`, `common/history/pops/01_south_europe.txt`.
- `common/scripted_triggers/1776_imperial_constitution.txt`, `common/scripted_effects/1776_imperial_constitution.txt`, `common/power_bloc_identities/1776_imperial_federation.txt`.
- Localisations anglaises et françaises `1776_imperial_feedback` et `1776_imperial_repairs`.
- Textures `gfx/interface/journal_entries/aor1776_hre_registered_map.dds`, `gfx/map/map_painting/aor1776_hre_mask.dds`. Le sentinel généré est vérifié mais n'est changé que si ses octets diffèrent.

Le registre MAP2L, les manifestes, aperçus et outils de cette passe sont des artefacts de contrôle supplémentaires. La liste exacte des fichiers de jeu dont les octets ont changé figure dans VALIDATION.json. Les sources et instantanés des anciens lots ne sont pas remplacés.

## Vérifications

Le contrôle propre au lot passe **381/381** assertions : avant/deux composantes et après/une composante, classification exacte des 325 pixels par le polygone source, terrains, profils démographiques et bâtiments, références, propriétaires, hubs, registre, scripts, périmètre et protection de HEAD/index Git. La carte native passe **16/16** tests hors moteur, dont round-trip DDS et compilation du helper shader.

Le total mondial écrit reste **835 804 980 habitants**. Les **44 doubles attributions RGB et 12 anomalies de référence préexistantes** restent inchangées et séparées du résultat du lot : aucune nouvelle dans ce périmètre. Le résultat des suites cumulatives est consigné dans NON_REGRESSION.json après leur exécution. Un test statique ne remplace pas le chargement dans Victoria 3 ; le lancement reste différé jusqu'à la fin des lots impériaux, conformément à la demande de l'utilisateur. Une nouvelle partie sera nécessaire pour évaluer les historiques modifiés.

Suites cumulatives : Belgique 315/315, Piémont 232/232, Franconie 561/561, Neckar 447/447, Mayence/Palatinat 573/573, possessions de Mayence 559/559, complément méridional de Mayence 434/434. Les nouveaux contrôles couvrent aussi les RGB vénitiens non impériaux : ils ne sont pas simplement retirés du périmètre testé.

`git diff --check` contre HEAD n'est pas globalement propre : une ligne blanche avec tabulations subsiste en Istrie, maintenant ligne 846 de `common/history/pops/01_south_europe.txt`. Elle est présente dans l'instantané antérieur au lot et reste inchangée hors du périmètre lombard. Les lignes ajoutées pour les populations du Crémonais sont nettoyées et indentées après application du patch préparatoire.

## ColGrep

Un appel local `colgrep --agent` a recherché les dépendances de Trente avant la clarification sur Milan. Il s'est terminé avec code 0 après **259,77 secondes**, renvoyant notamment MAP2B_EXECUTIVE_SUMMARY.md:24-26 et MAP1-P0-002.md:11. Les passages ont été relus ; la piste concernant Trente n'a pas été appliquée. Après la précision, les emplacements et dossiers lombards étaient déjà connus : aucune seconde recherche sémantique redondante n'a été lancée. Les identifiants exacts et dépendances ont été vérifiés par recherches ciblées classiques.

Commande locale : `C:\Users\simeo\.cargo\bin\colgrep.exe --agent "Locate the retained research, approved ownership decisions, RGB mappings and map correction dependencies for the secular prince-bishopric of Trent/Trient in 1776, specifically the allegedly incorrect detached southern fragment between Lombardy and Venice. Return verified repository paths and line numbers only; do not edit files or decide boundaries." ./docs/reports/map`.

Aucun compteur fiable de tokens Codex par recherche, ni comparaison contrôlée sans délégation, n'est accessible ici. Aucun gain de quota exact n'est revendiqué. Pour cette passe, l'appel local a eu une utilité faible et une latence élevée, du fait notamment de la mauvaise identification initiale de la cible. Aucun modèle ou paramètre d'intégration n'est changé.

Le nombre exhaustif de consultations classiques n'a pas été instrumenté pour cette reprise : il n'est pas reconstruit artificiellement après coup. Aucun index n'est effacé ou reconstruit ; aucune nouvelle recherche ColGrep ne nécessitait ici une actualisation manuelle après les éditions. Les scans et le bitmap sont inspectés par leurs pixels, pas considérés comme des frontières sémantiquement indexées.
