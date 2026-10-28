# CENTRAL-01 — délégation locale

27 octobre 2026. Une exécution réussie de ColGrep en mode agent, plus une tentative arrêtée avant recherche par refus d'accès au verrou de l'index.

```powershell
& 'C:/Users/simeo/.cargo/bin/colgrep.exe' --agent 'Read-only search. Locate existing preliminary regional research and current territorial implementation for Central America (Guatemala, Yucatan, Belize, Mosquito Coast, Costa Rica, Panama, New Granada) and Caribbean colonies in January 1776. Prioritize docs research reports and relevant state/country histories, return at most eight precise files and line ranges. Do not edit or run apply scripts.' .
```

- Tentative initiale : verrou de l'index dans AppData inaccessible ; 0,194 seconde mesurée, aucune exécution du modèle attestée pour cette tentative. Relance avec accès au verrou existant, sans changement d'intégration ni de modèle.
- Exécution achevée : **163,5389312 secondes**, code de sortie **0**. Configuration locale ColGrep-Agent-2B prévue par les instructions installées ; pas de télémétrie GPU ou de temps d'inférence séparé collectée.
- Résultats vérifiés : recherche militaire `CLEANUP2D5A_NORTH_AMERICA_CARIBBEAN_HISTORICAL_GENERALS.md:24–34` (réel, peu pertinent pour les frontières), recherche économique `BUILD_START_1776_AMERICAS_CARIBBEAN_RESEARCH.md:31–34` (réel, contexte utile), `common/history/pops/06_central_america.txt:1–424` (réel, données directement utiles).
- L'agent n'a pas retrouvé le dossier territorial R8 attendu. Localisation par nom exact et lecture CSV ciblée effectuées par Codex ; aucun résultat local n'a été accepté comme décision historique.
- Aucun index reconstruit, aucun modèle installé ou reconfiguré. Les formats binaires PNG/PDF ont été examinés séparément ; aucun résultat sémantique n'atteste leur couverture par cet index.
- Nombre exact de recherches `rg` et tokens Codex non instrumenté. Une localisation utile des POPs, mais absence de comparaison témoin : **aucune économie chiffrable de quota démontrée**. Le temps total de l'appel n'est pas une économie de temps démontrée non plus.
