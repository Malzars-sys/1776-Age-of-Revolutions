# Profil natif des scripts — PROFC1, 19 novembre 2026

La session dédiée PROFC1 a réellement exécuté `ScriptProfiling.Enable`, simulé le monde initial de 1776, puis exécuté `ScriptProfiling.Dump`. Le moteur confirme « Enabled » et produit un export de **5 003 entrées**. Il ne s'agit pas d'un benchmark de débit, ni d'un profil CPU complet du moteur.

## Périmètre vérifié

Même source initiale, runtime normal figé et exécutable Steam 1.15.1 ; aucun retrait d'objectif ni de callback. La sauvegarde automatique native du 1er avril confirme **646 contrôleurs actifs, aucun pays ajouté ou manquant, objectifs et payloads attendus conservés**. La source préparée a aussi sa copie protégée ; aucune sauvegarde normale n'est remplacée.

Activation native : 02:15:06.066 UTC ; reprise de la simulation : 02:15:34.705 ; ouverture du menu après l'observation du 1er avril : 02:18:02.781 ; clic d'export : 02:18:49.693. Ces heures proviennent du journal d'actions ; les lignes natives de commandes confirment leur exécution. Le dernier DAY complet est celui du **7 avril 1776 à 03:18:02 heure locale**. La collecte inclut les périodes en pause avant/après la simulation, l'interface et la sauvegarde trimestrielle. Elle n'est pas limitée aux mêmes 56 jours que les benchmarks.

Seul le profil de cette session a été passé de 100 à 70 % d'échelle d'interface pour atteindre les boutons de collecte. Le bouton du profileur Jomini restait hors du cadre ; aucune table Start/Stop Jomini n'est revendiquée ici. La collecte obtenue est l'export Legacy natif. Les restrictions Windows de profilage n'ont pas été contournées.

## Appels des priorités effectivement observés

Le fichier natif annonce explicitement `time (seconds), call count`. Les emplacements sont rapprochés des douze blocs originaux vérifiés par empreinte dans le runtime figé. **Huit emplacements sur douze apparaissent dans l'export.**

| Priorité de bâtiment | Appels | Temps rapporté, secondes |
|---|---:|---:|
| Outils | 5 095 | 0,019332 |
| Acier | 554 | 0,001005 |
| Charbon | 1 668 | 0,009089 |
| Fer | 1 829 | 0,007917 |
| Exploitation forestière | 4 414 | 0,015351 |
| Calcaire | 2 976 | 0,008991 |
| Chemins de fer | 5 998 | 0,054465 |
| Alliages | 1 179 | 0,003240 |

Les emplacements moteurs, centrales, ciment et raffineries ne sont pas présents dans cet export. Cela ne prouve ni un coût nul, ni leur absence dans toutes les conditions de jeu. Les temps ne doivent pas être additionnés à des sous-appels imbriqués, convertis en parts exclusives du CPU ou soustraits aux 94–96 secondes d'un autre processus.

Cette trace confirme que plusieurs définitions testées sont réellement appelées ; elle apporte un appui supplémentaire au résultat négatif des répétitions C. Elle ne mesure pas le coût natif de parcourir les candidats, d'estimer leur rentabilité ou de choisir un PM autour de ces callbacks.

## Autres entrées observées

| Emplacement | Appels | Secondes rapportées | Sens vérifié dans le script |
|---|---:|---:|---|
| `common/treaty_articles/20_law_commitment.txt:108` | 8 786 | 1,730577 | Validation du type de loi d'un engagement de traité |
| `common/ai_strategies/00_default_strategy.txt:4526` | 76 704 | 0,617669 | Score d'intérêt pour une région stratégique |
| `common/ai_strategies/00_default_strategy.txt:3991` | 28 879 | 0,242173 | Objectif de capacité de construction |
| `common/diplomatic_actions/1776_deferred_debt.txt:46` | 260 103 | 0,163887 | Trigger d'une action diplomatique moddé |

Le score de **région stratégique** n'est pas le contrôleur mensuel d'infrastructure régionale. Un grand nombre d'appels ne suffit pas à désigner un goulet : l'action de dette ci-dessus compte beaucoup d'appels mais peu de temps rapporté. La première ligne du classement ne constitue pas à elle seule une explication du contraste global IA normale/inactive.

Les hypothèses de rentabilité native, construction publique, investissement privé et PM restent ouvertes. La prochaine expérience utile doit disposer d'un arrêt persistant d'une seule catégorie et d'une preuve d'activité réelle ; supprimer une instance d'objectif qui se recrée ne suffit pas. À défaut, une trace native de tâches ou une instrumentation moteur officiellement prise en charge a plus de valeur qu'une suppression supplémentaire de scripts sans validation.

## Preuves conservées hors dépôt

Laboratoire : `C:/Users/simeo/AppData/Local/Temp/aor56_ai_20261117`.

- `evidence/PROFC1_SCRIPT_PROFILING_NATIVE.txt` : export natif intégral préservé, avec empreinte vérifiée.
- `PROFC1_SCRIPT_PROFILE_RESULTS.json` : rapprochement des douze emplacements, unités, classement et limites.
- `PROFC1_POST_GOAL_PROOF.json` et `autosave_witnesses/PROFC1` : état natif du monde et contrôleurs.
- `actions/PROFC1.jsonl` et le dossier `runs/PROFC1_*` : commandes, journaux et fermeture du seul processus possédé.

Aucune optimisation préservant le gameplay n'est validée par cette collecte.
