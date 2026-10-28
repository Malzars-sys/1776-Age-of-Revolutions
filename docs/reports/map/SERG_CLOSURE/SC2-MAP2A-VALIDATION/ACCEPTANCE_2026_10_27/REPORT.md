# Réception humaine de MAP2A — 27 octobre 2026

`SC2-MAP2A-VALIDATION` : `PASS_RUNTIME_USER_VALIDATED`, après attestation explicite intégrale du joueur.
Portée : x9AC196 SWI/Lombardie, x71E080 et xF0E080 AUS/Moravie, x9061E0 AUS/Galicie occidentale ; Bergame VEN ; populations, bâtiments, PM et recrutement associés. Deux niveaux textiles et un niveau de réseau routier à Teschen, sans addition artificielle des déclarations base/overlay. Formations, commandants et HQ AUS/PRU conservés.

Le joueur atteste nouvelle partie 1776, mois complet sans anomalie et sauvegarde/rechargement. Date effective du test, captures, statistiques économiques et mesures d’emploi non fournies ; aucune n’est inventée. Empreintes collectées par l’agent au moment de la réception, distinctes d’empreintes testées fournies par le joueur.

Conservation ciblée : voir [ACCEPTANCE_CHECKS.json](ACCEPTANCE_CHECKS.json). Ancien validateur global : échec `Unexpected territorial change.` conservé intégralement dans [LEGACY_MAP2A_READONLY_RAW.json](LEGACY_MAP2A_READONLY_RAW.json). Il exige encore toute la carte du 10 octobre, antérieure aux autres lots autorisés. Les quatre corrections sont présentes. Les pools lombards plus larges ont changé dans les redistributions ultérieures ; populations, bâtiments et unités des quatre régions identiques à l’audit du 26 octobre. Les transferts MAP2A SWI (5000), Moravie et Teschen (135753) restent exacts. Références : MAP2A_DEPENDENCIES.md ; MAP2L/MILAN_CREMONESE/REPORT.md et PLAN.json. Aucun ancien test, résultat brut ou baseline réécrit.

Progression calculée : 83/235 (35.32 %, 25/81) → 85/235 (36.17 %, 26/81). Deux points pour cette seule tâche. Les 23 tâches bloquées restent inchangées. SC2-TESCHEN et TE-R-CORE, limites cadastrales silésiennes, mine de Berchtesgaden, Milan et autres tâches ne sont pas validés par ce reçu. Le reçu Luxembourg est conservé.

Aucun fichier fonctionnel, vanilla ou Git écrit. Aucune installation ni nouveau test moteur par l’agent. Les résultats finaux et écarts concurrents sont consignés dans FINAL_CHECKS.json et CONCURRENT_CHANGES.json.

Suite recommandée : SC4-MILAN-VALIDATION, puis les cinq autres lignes du [protocole groupé actualisé](PLAYER_TEST_PROTOCOL_GROUPED.md), soit huit points conditionnels. Sous-lots TE-R-CORE et mine ordinaire maintenus séparément. Aucun nouveau territoire commencé.
