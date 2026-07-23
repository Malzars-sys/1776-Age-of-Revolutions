# Phase HOTFIX-6A.2F — Correction ciblée Autriche–Croatie–Slavonie–Suisse

FORK :
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE :
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE :
`C:\Games\Victoria 3 The Great Wave\game`

MODÈLE RECOMMANDÉ : GPT-5.6 Thinking avec raisonnement élevé.

## Verdict d’entrée

- `READY_FOR_AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX`
- `HOTFIX_6A2R_TARGET_HUNK_RESOLUTION_COMPLETE`
- `SWISS_POP_HUNK_SHOULD_BE_OMITTED`
- `SHIPYARD_CROATIA_REQUIRED_COMPATIBLE`
- `AUS_FLEET_REQUIRED_RECONSTRUCTED`
- `AGRAM_MIGRATION_REQUIRED_MINIMAL`

## Objectif unique

Appliquer uniquement les hunks fermés ci-dessous, exécuter tous les tests statiques, puis préparer et effectuer un seul lancement Victoria 3 pour le runtime consolidé. Ne jamais importer un fichier ou bloc hotfix complet. Ne pas committer automatiquement.

## Contrôles initiaux obligatoires

Exécuter `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`, `git diff --check`, `git diff --cached --name-only` et `git stash list`.

Exiger : racine exacte, branche `hotfix-dlc-audit`, rapport `HOTFIX_6A2R_TARGET_HUNK_RESOLUTION.md` présent dans HEAD, arbre propre sauf `docs/research/technology/`, staging vide, Russie identique au commit `991f6a1`, stash MARATH intact. Ne pas inspecter/appliquer/pop/drop le stash. Au départ, Victoria 3 et le launcher doivent être fermés.

Si l’arbre est sale : `BLOCKED_DIRTY_TREE`. Si une autre session écrit dans le dépôt : `BLOCKED_CONCURRENT_WORK_COLLISION`.

## Sources canoniques

Lire avant toute modification :

- `docs/reports/hotfix/_index/HOTFIX_6A2R_TARGET_HUNK_RESOLUTION.md`;
- `docs/reports/hotfix/_index/HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_AUDIT.md`;
- `docs/reports/hotfix/_index/HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_DELTA_MAP.csv`;
- les rapports suivis sous `docs/reports/navy/` nécessaires aux contrôles de non-régression.

## Liste exacte et fermée des fichiers gameplay modifiables

1. `common/history/states/00_states.txt`
2. `common/history/pops/01_south_europe.txt`
3. `common/history/buildings/01_south_europe.txt`
4. `common/history/diplomacy/00_subject_relationships.txt`
5. `common/history/military_formations/00_military_formations_europe.txt`

Interdiction explicite de modifier `common/history/pops/00_west_europe.txt` : le hunk AUS de 30 000 est omis.

Documents autorisés après correction : créer un rapport `HOTFIX_6A2F_AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX.md`, mettre à jour la delta map 6A.2, `docs/reports/hotfix/INDEX.md`, `HOTFIX_REPORT_INDEX.csv`, `HOTFIX_MERGE_BLOCK_STATUS.csv`, `HOTFIX_MERGE_COMPLETION_ROADMAP.md` et `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`. Aucun autre fichier.

## Hunk 1 — STATE_CROATIA

Dans `00_states.txt`, sous `s:STATE_CROATIA/create_state`, remplacer seulement `country = c:CRO` par `country = c:AUS`. Conserver exactement les huit provinces : `x71A041 x70DF00 x6D8BC6 xF021C0 x71A0C0 xB39050 xB339EC x458E4C`.

Rollback : AUS→CRO sur cette seule ligne.

## Hunk 2 — STATE_SLAVONIA

Sous `s:STATE_SLAVONIA/create_state`, remplacer seulement `country = c:CRO` par `country = c:AUS`. Conserver exactement les sept provinces : `x51A021 x106020 x13318D x906121 x80CF00 x902161 x1A4DF9`.

Rollback : AUS→CRO sur cette seule ligne.

## Hunk 3 — portion suisse

Sous `s:STATE_EAST_SWITZERLAND`, retirer seulement `x90C0E0` de `region_state:SWI/create_state/owned_provinces`, puis ajouter un `create_state` AUS dans le même state avec `owned_provinces = { x90C0E0 }`. Ne modifier aucune autre province.

Rollback : supprimer le `create_state` AUS et remettre `x90C0E0` dans la liste SWI à sa position d’origine.

## Hunk 4 — pops Croatia et Slavonia

Dans `01_south_europe.txt`, remplacer uniquement :

- `s:STATE_CROATIA/region_state:CRO` par `region_state:AUS`;
- `s:STATE_SLAVONIA/region_state:CRO` par `region_state:AUS`.

Ne modifier aucune culture, religion, profession ni taille. Rollback : les deux scopes AUS→CRO.

## Hunk 5 — buildings Croatia

Dans le bloc `s:STATE_CROATIA` de `01_south_europe.txt` :

- remplacer `region_state:CRO` par `region_state:AUS`;
- remplacer exactement les huit références `country="c:CRO"` du bloc par `country="c:AUS"` : administration, paper mill, university, wheat-farm manor house, livestock-ranch manor house, logging financial district, fishing wharf et port;
- préserver l’ownership HUN, tous les niveaux, réserves et PM existants;
- entre le fishing wharf et le port, insérer uniquement :

```txt
create_building={
	building="building_shipyard"
	add_ownership={
		building={
			type="building_financial_district"
			country="c:AUS"
			levels=2
			region="STATE_CROATIA"
		}
	}
	reserves=1
	activate_production_methods={ "pm_basic_shipbuilding"  }
}
```

Rollback : supprimer ce seul bloc, remettre les huit ownerships à CRO et le scope à CRO.

## Hunk 6 — buildings Slavonia

Dans `s:STATE_SLAVONIA`, remplacer `region_state:CRO` par `region_state:AUS` et l’unique manor-house ownership `country="c:CRO"` par `country="c:AUS"`. Préserver HUN et tous les PM.

Rollback : les deux valeurs AUS→CRO.

## Hunk 7 — pactes CRO

Dans `00_subject_relationships.txt`, supprimer uniquement les deux blocs AUS→CRO `create_diplomatic_pact` de types `crown_land` et `decrease_payments`. Ne toucher à aucun autre sujet ou pacte.

Rollback : restaurer les deux blocs à leurs ancres d’origine.

## Hunk 8 — flotte AUS reconstruite

Dans `00_military_formations_europe.txt`, immédiatement sous `c:AUS ?= {` et avant les armées, ajouter exactement :

```txt
create_military_formation = {
	type = fleet
	hq_region = sr:region_balkans
	name = K_K_Kriegsmarine

	ship = {
		type = ship_type:ship_type_ship_of_the_line
		state_region = s:STATE_CROATIA
		count = 1
	}

	ship = {
		type = ship_type:ship_type_frigate
		state_region = s:STATE_CROATIA
		count = 3
	}
}
```

Ne pas copier la flotte hotfix anonyme 3+6. Ne créer ni amiral, loi, technologie, administration navale ni localisation. Rollback : supprimer exactement cette formation.

## Hunk 9 — migration Agram

Déplacer byte-for-byte le `create_military_formation` `generalkommando_agram` actuellement sous `c:CRO ?= {` vers `c:AUS ?= {`, immédiatement après la flotte et avant `generalkommando_lemberg`. Conserver :

- `type = army`;
- `hq_region = sr:region_balkans`;
- les quatre groupes line infantry : Slavonia 2, Croatia 12, Croatia 4, Slavonia 6;
- total 24;
- tous commentaires, types et state regions.

Supprimer seulement le wrapper `c:CRO ?= {}` devenu vide. Ne reprendre aucune valeur hotfix 22+4+6. Rollback : retirer Agram d’AUS et restaurer exactement le wrapper/bloc CRO d’origine.

## Protections absolues

Préserver NAVY hors des deux hunks explicitement autorisés, ADMIN hors des re-clés d’ownership, MARATH, BIC, Travancore, Russie, Inde, Japon, Mamluk Iraq, localisations, descripteurs, sauvegardes, harnais et `docs/research/technology/`. Ne modifier aucune source hotfix/vanilla. Ne pas utiliser `git add .`.

## Tests statiques avant jeu

Avant tout lancement :

1. vérifier les trois owners/provinces states;
2. confirmer qu’aucun `region_state:AUS` de 30 000 n’a été ajouté dans `00_west_europe.txt` et que le fichier est inchangé;
3. confirmer les deux scopes pops AUS sans changement de groupes;
4. compter exactement huit ownerships Croatia et un Slavonia passés à AUS;
5. confirmer le shipyard unique niveau 2 et ses PMs;
6. confirmer l’absence des deux pactes CRO et la conservation de tous les autres;
7. confirmer une seule `K_K_Kriegsmarine`, 1 SOL + 3 frégates, HQ Balkans, chaque unité en Croatia;
8. confirmer un seul Agram sous AUS, zéro sous CRO, total 24 line infantry;
9. vérifier accolades, ancres, IDs et strategic regions;
10. exécuter `git diff --check`, `git status --short`, `git diff --name-only`, `git diff --name-status`, `git diff --stat`, `git diff --cached --name-only` et `git stash list`;
11. exiger exactement les cinq fichiers gameplay autorisés plus les documents autorisés, zéro staged, Russie et recherche technologique intactes, stash intact.

En cas d’échec statique, rollback du fichier concerné par hunk inverse ciblé; ne pas lancer le jeu.

## Runtime unique

Après réussite de tous les tests statiques, préparer puis effectuer un seul lancement Victoria 3. Charger le setup 1776 et vérifier :

- AUS possède Croatia, Slavonia et `x90C0E0`;
- SWI conserve le reste de East Switzerland et sa population totale n’est pas gonflée;
- la portion AUS vide ne produit pas d’erreur;
- CRO n’est plus sujet/owner initial mais reste un tag dormant/libérable;
- pops et buildings Croatia/Slavonia appartiennent au bon region_state;
- AUS dispose de l’accès côtier, du port et du shipyard Croatia;
- `K_K_Kriegsmarine` apparaît avec 1 vaisseau de ligne et 3 frégates;
- Agram apparaît sous AUS avec 24 line infantry;
- RUS reste non régressif;
- `error.log`, `game.log` et `debug.log` ne contiennent aucune nouvelle erreur pertinente de state, pop, building, ownership, pacte, formation, HQ, strategic region ou ship type.

Fermer ensuite Victoria 3 et le launcher.

## Verdict attendu

Si statique et runtime passent : `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_COMPLETE`. Sinon publier un verdict bloquant précis, conserver les preuves et ne pas élargir le périmètre.

Ajouter : `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`. Ne pas committer automatiquement.
