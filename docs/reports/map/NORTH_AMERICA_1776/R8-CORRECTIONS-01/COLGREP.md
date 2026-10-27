# Mesure ColGrep — constat limité

Un appel à l'agent local, exécuté et terminé avec code 0 :

```powershell
& 'C:\Users\simeo\.cargo\bin\colgrep.exe' --agent "Locate already researched 1776 Comanche erroneous Alabama Mississippi Arkansas ownership, native Muscogee Choctaw Chickasaw Caddo Quapaw Osage Wichita territorial recommendations, Texas Spanish post mapping, Apache northern Mexico and British Florida 1765 treaty work. Find existing implementation helpers and regional georeferencing. Return concise exact source file locations; do not edit." .
```

Résultat : `tools/build_start_1776_implementation.py:1–16` seulement. Chemin et lignes relus : il s'agit d'une enveloppe de validation mondiale, pas d'un outil de découpage régional. Elle importe `build_start_1776_final_validate.main` et mentionne un autre script d'application globale ; **aucun de ces applicateurs mondiaux n'a été lancé**.

Ce retour est trop peu pertinent pour guider les transferts. Les identifiants, dossiers MAP1 déjà connus et scripts HBC ont donc été vérifiés par lecture ciblée et `rg`, conformément au repli prévu par AGENTS.md. Aucun second appel redondant, changement de modèle ou reconstruction de l'index.

| Mesure | Résultat réellement disponible |
|---|---|
| Appels `--agent` | 1 |
| Terminaison | code 0 ; résultat local obtenu |
| Temps total d'inférence locale | Non instrumenté/conservé ; aucune durée inventée |
| Modèle/GPU | Configuration locale 2B demandée, non modifiée ; pas de compteur d'utilisation GPU indépendant conservé |
| Tokens Codex | Aucun compteur fiable de la mission disponible |
| Recherches classiques | Repli effectif vers `rg`/lectures ciblées ; compteur exhaustif non instrumenté, aucune fausse mesure précise |
| Recherches évitées | Aucune démontrée par ce résultat |
| Économie de quota | Non mesurable sans comparaison contrôlée ; cette recherche large n'a pas démontré de gain |

L'intérêt potentiel reste celui d'un outil de localisation pour des questions mieux ciblées. Ici le retour n'a ni remplacé la vérification historique ni réduit de façon démontrable le travail de contrôle.

## Suite FLORIDA-01 : deuxième appel mesuré

```powershell
$r8Timer=[System.Diagnostics.Stopwatch]::StartNew()
& 'C:/Users/simeo/.cargo/bin/colgrep.exe' --agent 'Locate existing tools that split Victoria 3 State Regions and update their dependent strategic regions, geographic regions, generated hub locators and history references. Focus on reusable examples in tools and MAP2 reports; return at most five file paths with line ranges. Search and read only; do not modify files, run apply tools, or change configuration.' .
$r8Timer.Stop()
```

Code 0 ; **284,97 secondes mesurées de commande complète**, pas une mesure isolée de l'inférence GPU. Le résultat local comprenait notamment `tools/audit_naval_admin_revision.py:35–136` et `tools/serg_sc4_italian_states.py:34–59`. Les portions visibles ont été relues et leurs fonctions confirmées : démographie navale et inventaire italien, **pas des implémentations de division de State Regions**. Sortie longue partiellement tronquée dans l'outil ; les pistes non relues ne sont ni citées comme preuves ni utilisées.

Total du chantier R8 + Floride : **2 appels `--agent`**. Temps total non disponible puisque le premier n'avait pas été chronométré ; deuxième appel seul : 284,97 s. Aucun gain de quota mesurable, aucune recherche classique évitée démontrée. Aucun de ces scripts suggérés n'a été exécuté pour modifier les POPs ou la carte. Le résultat n'a pas justifié une troisième tentative, un nouveau modèle ou une reconstruction complète de l'index.
