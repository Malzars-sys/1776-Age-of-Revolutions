# Journaux ottomans — Séparation des conditions

Ce rapport remplace, pour la répartition des conditions, les indications des rapports précédents. Les événements d’introduction et les descriptions immersives sont conservés.

## Journal administratif : dix objectifs, pas onze

| Objectif | Condition exécutée |
|---|---|
| Offices | Ne plus appliquer les bureaucrates héréditaires, ni leurs variantes |
| Solde bureaucratique | Bureaucratie ≥ 0 |
| Réserve bureaucratique | Bureaucratie ≥ 0 et aucune pénurie imminente |
| Affaires intérieures | Institution ≥ 3 ; remplace entièrement l’objectif de pénurie de biens |
| Fiscalité foncière | Ne plus appliquer l’imposition foncière traditionnelle, ni ses variantes |
| Fiscalité de consommation | Ne plus appliquer cette loi fiscale, ni ses variantes |
| Forces de l’ordre | Institution ≥ 3 |
| Éducation | Institution ≥ 3 |
| Capacité de taxation | Besoins couverts dans au moins 75 % des États incorporés ; ensemble non vide |
| Recrutement administratif | Au moins 90 % des administrations ont ≥ 80 % de leurs emplois pourvus ; au moins une administration existe |

Chaque objectif donne toujours **−10 points de gaspillage fiscal supplémentaire et +1 point de compensation du malus bureaucratique**, via le même modificateur multiplié par le score de 0 à 10. Calcul hebdomadaire et absence de duplication conservés.

Les dix objectifs doivent être simultanément remplis pendant **12 mois consécutifs**. Leur régression remet la consolidation à zéro. Aucune recherche de Rainurage ou d’Abolitionnisme, ni condition relative au commerce d’esclaves, n’intervient dans l’activation, le score ou l’achèvement administratif.

## Journal politique : prérequis et alternatives

Prérequis communs supplémentaires, exclusivement politiques :

- `rifling` recherchée : définition du mod dans `common/technology/technologies/20_tech3a_military.txt`.
- `abolitionist_mobilization` recherchée : définition du mod dans `common/technology/technologies/30_tech3a_society.txt`.
- Absence de `law_slave_trade`, définie dans `common/laws/02_slavery.txt`, et de ses variantes : utilisation de `has_law_or_variant`.

La nouvelle obligation globale d’institutions au niveau 3 est retirée. Les trois voies politiques d’origine sont rétablies :

1. Centralisation : légitimité ≥ 60 et **police OU éducation ≥ 2**.
2. Compromis : légitimité ≥ 75 et tous les sujets sous 25 de désir de liberté.
3. Rétablissement de l’État : journal administratif déjà résolu et légitimité ≥ 50. Aucun maintien ultérieur des institutions au niveau 3 n’est ajouté.

Les autres conditions communes préexistantes restent inchangées, notamment territoire, sujets, absence de guerre/révolution/faillite et solde bureaucratique non négatif. Ce dernier prérequis existait dans les deux journaux et n’est pas supprimé par cette correction. L’indépendance des résolutions, les 36 points de stabilité, la progression accélérée après résolution administrative, l’échéance du **1er janvier 1836**, l’échec anticipé et la transition vers L’Homme malade de l’Europe sont conservés.

## Fichiers modifiés dans ce lot

- `common/scripted_triggers/1776_ottoman_reform_triggers.txt` : nouvel objectif Affaires intérieures, séparation des prérequis et rétablissement de l’alternative institutionnelle politique.
- `common/scripted_effects/1776_ottoman_reform_effects.txt` : seul le test du quatrième objectif change ; calcul, modificateurs, compteurs et protections conservés.
- `common/journal_entries/1776_ottoman_reforms.txt` : liste des dix objectifs et suppression du prérequis politique dans l’achèvement administratif.
- `localization/french/1776_diplomacy_ottoman_l_french.yml` et `localization/english/1776_diplomacy_ottoman_l_english.yml` : statuts et infobulles conformes aux règles exécutées.
- `tools/validate_diplomacy_ottoman_1776.py` : validations adaptées et renforcées pour empêcher le retour des conditions croisées.
- Le présent rapport.

## Vérifications

Validateur complet : **tous les contrôles passent**.

- 1 024 combinaisons des dix objectifs ; dix contributions individuelles au score ; score et amplitude des réductions ; stabilité du calcul hebdomadaire.
- Seuils des trois institutions administratives, recrutement et taxation ; consolidation sur 12 mois et remise à zéro lors d’une régression.
- Résolution administrative possible sans les deux technologies et avec le commerce d’esclaves ; ces mêmes conditions bloquent la résolution politique.
- 192 combinaisons des trois voies politiques ; seuils de légitimité et de désir de liberté ; compromis et rétablissement possibles sans institutions actives ; variante synthétique du commerce d’esclaves rejetée.
- Échéance ferme, échec anticipé, résolution indépendante, migration, non-réactivation et deux événements d’ouverture conservés.
- Syntaxe, identifiants réellement définis, localisation bilingue et compteurs vérifiés. `git diff --check` ne relève aucune erreur.
- Comparaison des empreintes de 1 528 fichiers de gameplay/localisation avant et après : seuls les cinq fichiers de données listés ci-dessus changent. Historiques des bâtiments, armées, diplomatie, événements, modificateurs et autres éléments de gameplay strictement conservés. Descriptions narratives et textes d’introduction FR/EN identiques.

Tests statiques et de simulation : **aucun nouveau test en jeu effectué**. Le prochain lancement permettra de confirmer le rendu des infobulles actualisées. Aucun push, merge ou commit effectué.
