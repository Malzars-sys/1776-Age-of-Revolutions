# Chine — système des cantons et bâtiments de départ

Statut : **PASS_STATIC_PENDING_RUNTIME**. Nouvelle partie requise ; aucun test moteur effectué.

## Changements appliqués

| État chinois | Centres de commerce avant | Après |
|---|---:|---:|
| Guangdong occidental (`STATE_GUANGDONG`) | 5 | 5 |
| Fujian | 4 | 0 |
| Zhejiang | 4 | 0 |
| Nanjing | 4 | 0 |
| Zhili | 2 | 0 |
| Hubei oriental | 4 | 0 |
| Suzhou | 6 | 0 |

Suppression de 24 niveaux dans douze déclarations, dont six dans le fichier de redistribution mondial. Le port chinois du Guangdong occidental passe de **2 à 5 niveaux au total**, en conservant sa propriété publique et `pm_basic_port`. Les possessions portugaises de Macao et leurs bâtiments restent inchangés.

## Loi commerciale

`chi - china.txt` active déjà `law_traditionalism` puis `law_canton_system`. La définition de cette dernière existe dans les données effectives et conserve la restriction du commerce hors du Guangdong occidental. Aucun script d'écrasement certain n'a été identifié : la cause précise du comportement constaté en jeu n'est donc pas démontrée.

Ajout d'une réactivation de sécurité dans un enfant de `on_game_started_after_lobby`, qui intervient une fois lors de la création de campagne. Elle ne concerne que CHI, sous traditionalisme, possédant la partie majoritaire du Guangdong occidental, et seulement si la loi des cantons manque. Aucun changement forcé de loi économique, aucun déclenchement mensuel/journalier, aucun verrouillage des futures réformes et aucune réparation automatique des sauvegardes existantes.

## Fichiers de jeu modifiés

- `common/history/buildings/11_east_asia.txt`
- `common/history/buildings/98_build_start_1776_world_redistribution.txt`
- `common/on_actions/14_1776_china_canton_start.txt` (nouveau)

Contrôle reproductible : `tools/china_canton_2026_10_15.py validate`. Le dossier conserve une référence avant modification et le détail des changements dans `BASELINE.json`, ainsi que les résultats dans `VALIDATION.json`. Ne pas relancer `prepare` pour remplacer cette référence.

## Vérifications et limites

- Comparaison exacte de toutes les déclarations de bâtiments effectives : seules les suppressions demandées et le port sont modifiés, propriétés économiques et méthodes comprises.
- Contrôle par empreintes de tous les autres fichiers de jeu du dépôt : frontières, populations, unités, lois existantes, interface et ajouts économiques précédents inchangés.
- Syntaxe des historiques et du nouveau déclencheur contrôlée ; nombre de ports et de centres de commerce vérifié en cumulant tous les historiques.
- HEAD et index Git inchangés. Aucun commit, changement de branche ou push.
- Les anomalies cartographiques préexistantes ne sont ni modifiées ni requalifiées par cette passe.
- ColGrep : un appel tenté ; accès refusé à la résolution du dépôt, donc aucun lancement réussi du modèle local confirmé. Repli sur recherche exacte et lecture des données effectives, sans changement d'intégration.

À vérifier dans une **nouvelle partie** : loi des cantons active après entrée en jeu ; seuls les cinq niveaux chinois de Canton présents ; port chinois niveau cinq ; absence de recréation des centres ailleurs après un mois. La restriction future est celle du moteur via la loi existante, pas un script de destruction périodique. Ne pas considérer ces points comme déjà validés en jeu.
