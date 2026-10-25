# Implantation A1

## Fichiers fonctionnels ajoutés

1. `common/on_actions/1776_historical_forts_start.txt` : deux branchements enfants sur `on_game_started` et `on_game_started_after_lobby`. L'action enfant n'agit que lorsque `1776.1.1 <= current_date < 1776.1.2`.
2. `common/scripted_effects/1776_historical_forts_start.txt` : cinq effets nationaux, douze sélecteurs d'États et deux effets d'ajout protégés.

Ces fichiers n'écrasent aucun effet des actions natives. Aucun historique de bâtiments, de pays, de population ou de formations militaires n'est réécrit. Aucun fichier vanilla n'est modifié. Aucun changement Git d'écriture n'est effectué.

## Sélection et propriété

Le parcours commence dans `c:TAG`, puis utilise `every_scope_state` avec `state_region = s:STATE_…`. Il sélectionne donc la subdivision réellement détenue par ce pays. À Gibraltar, c'est la seule province britannique `xBC6ED3`, pas la portion espagnole de Haute-Andalousie.

La côte a été calculée depuis les couleurs de mer du `default.map` vanilla et les adjacences à quatre voisins du `map_data/provinces.png` actuel. Les provinces côtières sont ensuite croisées avec les provinces **possédées par le pays**, pas seulement avec le port de la State Region. Résultats : [INITIAL_STATE_AUDIT.json](INITIAL_STATE_AUDIT.json). Les États ciblés et leurs propriétaires sont revérifiés par le validateur.

La construction au démarrage utilise l'effet natif `create_building`, en portée État, avec `level = 1`, `reserves = 1` et activation du PM simple. La documentation locale de cet effet est conservée dans `docs/reports/military/LAND_FORTIFICATIONS/CONSTRUCTION_R1/sources/effects.log`, entrée `create_building`. Les bâtiments publics de ce groupe ne créent pas d'unité de campagne.

## Protections

- Technologie `scientific_fortification_siegecraft` déjà présente, jamais accordée par ce lot.
- Condition `is_coastal` conforme au bâtiment choisi.
- Aucun ajout si l'un des deux types de forts est déjà présent. Un fort déjà renforcé garde son PM, son niveau et ses réserves ; un ancien placement du mauvais type est signalable en jeu mais n'est pas doublé.
- Marqueur d'État posé seulement après la présence effective du bâtiment. En cas d'échec de création, le second branchement peut encore essayer au démarrage.
- Un État marqué ne reçoit pas de fort supplémentaire lors d'un nouvel appel. Une démolition ne provoque pas de réapparition.
- Aucun déclenchement mensuel, aucune implantation de rattrapage dans une ancienne campagne après le premier jour de 1776.
- Les cinq forts terrestres appellent les fonctions existantes de mise à jour du ralentissement de construction. Leurs mécanismes ne sont pas copiés ni réimplémentés.

## Système observé et préservé

| Objet | Définition effective |
| --- | --- |
| Fort intérieur | `building_aor1776_land_fortification` ; potentiel sans côte ; plafond de 5 fourni par la technologie |
| Fort côtier | `building_naval_fortification` ; potentiel côtier ; plafond natif de 5 |
| Déblocage commun | `scientific_fortification_siegecraft` |
| PM2 / PM3 | `casemated_fortifications` / `concrete_fortifications` |
| Coût de construction intérieur | 900 affichés ; ralentissement existant visant 900 / 1 100 / 1 300 / 1 500 / 1 700 effectifs avant autres bonus |
| Coût de construction côtier | 100 points, valeur `construction_cost_very_low` existante ; pas d'alignement sur 900 dans ce lot |
| Génie | `combat_unit_type_aor1776_engineer_corps` ; groupe spécialisé indépendant ; 1 000 hommes ; déblocage `permanent_engineer_services` |
| Entretien du génie | Par unité : 1 arme légère, 1 outil, 0,5 bois ; capacité de ravitaillement 30 |
| Combat ordinaire du génie | Pas de bonus d'attaque/défense/moral/naval ajouté ; les trois indications de réduction des protections des forts restent présentes |

Les forts installés représentent un capital historique déjà construit : ils ne consomment pas 900 points de la file de construction au démarrage. Les nouveaux niveaux construits ensuite utilisent les coûts existants.

## Reproduction des vérifications

Depuis la racine du dépôt, exécuter avec le Python fourni par l'app :

```text
python tools/validate_historical_forts_1776.py
```

L'outil lit les scripts et sources actuels et écrit uniquement dans ce dossier de rapport. Il compare le classeur, deux résolutions des technologies initiales, les propriétaires, les PM et les projections des scripts. Il ne lance ni le jeu ni les outils de modification cartographique. Les anciens tests n'ont pas été modifiés.

Les empreintes initiales protègent les fichiers préexistants. Les dérives concurrentes relevées sont conservées à part avec leurs anciennes et nouvelles empreintes. Les fichiers explicitement reconnus comme appartenant au chantier parallèle peuvent continuer d'évoluer ; leurs empreintes actuelles sont rapportées. Un changement sur un autre chemin non revu fait échouer le contrôle. Le rapport ne présente donc pas le workspace entier comme inchangé lorsque d'autres agents y travaillent.
