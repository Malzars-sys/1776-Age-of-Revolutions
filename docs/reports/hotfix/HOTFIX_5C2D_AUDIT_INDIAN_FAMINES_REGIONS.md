# HOTFIX-5C2D-AUDIT - Indian Famines regions

## 1. Resume executif

L'audit confirme exactement **100 references invalides** dans la chaine Indian Famines: 60 dans la journal entry et 40 dans les events. Le hotfix upstream et la vanilla 1.13 sont bit-a-bit identiques pour les deux fichiers compares.

La migration est claire pour 95 references:

- 45 controles larges doivent utiliser `geographic_region_india`;
- 45 controles fondes sur les strategic regions doivent utiliser `region_north_india` et `region_south_india`;
- 5 conditions de fin regionales doivent utiliser les subdivisions historiques `*_old`.

Les cinq selecteurs qui definissent `bengal_famine_var`, `punjab_famine_var`, `bombay_famine_var`, `madras_famine_var` et `central_india_famine_var` restent ambigus. La migration vanilla/hotfix vers nord/sud rend certaines branches `else_if` inaccessibles et peut faire diverger le nom de la famine de sa zone de completion. Ils doivent rester isoles dans une troisieme sous-phase.

## 2. Etat Git

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `d159379 Fix India Railway region references` |
| HOTFIX-5C2C | Commit present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. Comptage initial

Le comptage utilise les cinq tokens exacts dans les deux fichiers, sans compter les noms `geographic_region_*`.

| Fichier | Bengal | Bombay | Central India | Madras | Punjab | Total |
|---|---:|---:|---:|---:|---:|---:|
| `common/journal_entries/04_indian_famines.txt` | 12 | 12 | 12 | 12 | 12 | **60** |
| `events/india_events/indian_famines.txt` | 8 | 8 | 8 | 8 | 8 | **40** |
| **Total** | **20** | **20** | **20** | **20** | **20** | **100** |

Le total runtime global avant implementation reste **373** references invalides dans `common/` et `events/`, commentaires exclus.

## 4. Definitions vanilla

References vanilla:

- `common/strategic_regions/west_south_asia_strategic_regions.txt`;
- `common/geographic_regions/04_geographic_regions_asia.txt`;
- `common/geographic_regions/06_old_strategic_regions.txt`.

| Region | Type | Membres principaux | Usage adapte |
|---|---|---|---|
| `region_north_india` | Strategic | Gujarat, Sindh, Central Provinces, Awadh, Malwa, Agra, Bundelkhand, Bihar, East/West Bengal, Assam, Orissa, Punjab, Hill Punjab, Delhi, Rajputana | Listes de states fondees sur les deux grandes strategic regions |
| `region_south_india` | Strategic | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool, Bombay | Complement sud des controles strategic-region |
| `geographic_region_india` | Geographic | Nord + sud + Quetta, Pashtunistan, Kashmir, Baluchistan | Controle panindien large dans un state scope |
| `geographic_region_bengal_old` | Geographic historique | Bihar, East/West Bengal, Assam, Orissa | Branche Bengal precise |
| `geographic_region_bombay_old` | Geographic historique | Bombay, Gujarat, Sindh, Baluchistan | Branche Bombay precise |
| `geographic_region_central_india_old` | Geographic historique | Central Provinces, Awadh, Malwa, Agra, Bundelkhand | Branche Central India precise |
| `geographic_region_madras_old` | Geographic historique | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool | Branche Madras precise |
| `geographic_region_punjab_old` | Geographic historique | Punjab, Hill Punjab, Delhi, Rajputana | Branche Punjab precise |

Les cinq anciennes strategic regions `region_bengal`, `region_bombay`, `region_central_india`, `region_madras` et `region_punjab` ne sont pas definies par la vanilla locale.

## 5. Inventaire de la journal entry

Objet unique: `je_indian_famines`.

| Lignes fork | Bloc | Scope | References | Role | Cible principale |
|---|---|---|---:|---|---|
| 10-20 | `is_shown_when_inactive` | `any_scope_state` | 5 | Afficher la JE si le pays possede un state en Inde | `PAN_INDIA_GEOGRAPHIC` |
| 23-49 | `possible`, cinq branches regionales | `any_scope_state` | 5 | Atteindre un seuil de 4 ou 5 states en famine | `PAN_INDIA_STRATEGIC` |
| 50-60 | `possible`, grande famine | `any_scope_state` | 5 | Atteindre 15 states en famine dans toute l'Inde | `PAN_INDIA_GEOGRAPHIC` |
| 75-90 | `immediate`, grande famine | `any_scope_state` | 5 | Definir `great_indian_famine_var` | `PAN_INDIA_GEOGRAPHIC` |
| 91-113 | `immediate`, selecteur Bengal | `any_scope_state` | 1 | Definir `bengal_famine_var` | `MANUAL_RESEARCH_REQUIRED` |
| 98-110 | `immediate`, exclusion grande famine de Bengal | `NOT/any_scope_state` | 5 | Eviter une branche regionale si 15 famines sont presentes | `PAN_INDIA_GEOGRAPHIC` |
| 114-136 | `immediate`, selecteur Punjab | `any_scope_state` | 1 | Definir `punjab_famine_var` | `MANUAL_RESEARCH_REQUIRED` |
| 121-133 | `immediate`, exclusion grande famine de Punjab | `NOT/any_scope_state` | 5 | Meme garde panindienne | `PAN_INDIA_GEOGRAPHIC` |
| 137-159 | `immediate`, selecteur Bombay | `any_scope_state` | 1 | Definir `bombay_famine_var` | `MANUAL_RESEARCH_REQUIRED` |
| 144-156 | `immediate`, exclusion grande famine de Bombay | `NOT/any_scope_state` | 5 | Meme garde panindienne | `PAN_INDIA_GEOGRAPHIC` |
| 160-182 | `immediate`, selecteur Madras | `any_scope_state` | 1 | Definir `madras_famine_var` | `MANUAL_RESEARCH_REQUIRED` |
| 167-179 | `immediate`, exclusion grande famine de Madras | `NOT/any_scope_state` | 5 | Meme garde panindienne | `PAN_INDIA_GEOGRAPHIC` |
| 183-205 | `immediate`, selecteur Central India | `any_scope_state` | 1 | Definir `central_india_famine_var` | `MANUAL_RESEARCH_REQUIRED` |
| 190-202 | `immediate`, exclusion grande famine de Central India | `NOT/any_scope_state` | 5 | Meme garde panindienne | `PAN_INDIA_GEOGRAPHIC` |
| 208-263 | `complete`, cinq `trigger_if` regionaux | `NOT/any_scope_state` | 5 | Finir la JE quand la subdivision nommee n'a plus de famine | `HISTORICAL_PRESIDENCY` |
| 264-280 | `complete`, grande famine | `NOT/any_scope_state` | 5 | Finir quand aucune famine ne reste dans l'Inde large | `PAN_INDIA_GEOGRAPHIC` |

La JE ne contient aucune progress bar locale. Elle affecte des progress bars externes pendant son activite, mais ces fichiers sont hors perimetre et ne doivent pas etre modifies.

## 6. Inventaire des events

`indian_famines.3` ne contient aucune reference regionale. Les 40 occurrences se trouvent dans les trois autres events.

| Lignes fork | Objet | Bloc | Scope | References | Role |
|---|---|---|---|---:|---|
| 22-39 | `indian_famines.1` | `trigger` | `any_scope_state` | 5 | Verifier une famine dans les possessions indiennes |
| 41-55 | `indian_famines.1` | `immediate` | `random_scope_state.limit` | 5 | Sauvegarder un state en famine |
| 126-154 | `indian_famines.2` | `trigger` | `any_scope_state` | 5 | Verifier famine et plantations dans un state indien |
| 156-177 | `indian_famines.2` | `immediate` | `random_scope_state.limit` | 5 | Sauvegarder le state cible |
| 190-224 | `indian_famines.2` | option A, tooltip | `ordered_scope_state.limit` | 5 | Montrer le state qui recevra l'aide |
| 225-252 | `indian_famines.2` | option A, effet cache | `every_scope_state.limit` | 5 | Appliquer l'aide a tous les states eligibles |
| 387-404 | `indian_famines.4` | `trigger` | `any_scope_state` | 5 | Verifier une famine dans les possessions indiennes |
| 406-420 | `indian_famines.4` | `immediate` | `random_scope_state.limit` | 5 | Sauvegarder un state en famine |

Ces huit listes ont toutes la meme cible principale: `PAN_INDIA_STRATEGIC`. Le hotfix et la vanilla remplacent chaque liste de cinq par `region_south_india` et `region_north_india` en conservant `region = sr:*`.

## 7. Classification semantique

| Classification | Blocs | Occurrences |
|---|---|---:|
| `PAN_INDIA_GEOGRAPHIC` | JE: affichage, controles grande famine, cinq gardes d'exclusion, completion grande famine | **45** |
| `PAN_INDIA_STRATEGIC` | JE: seuils regionaux de `possible` (5); events: huit listes panindiennes (40) | **45** |
| `HISTORICAL_PRESIDENCY` | JE: cinq conditions de completion liees aux variables regionales | **5** |
| `MANUAL_RESEARCH_REQUIRED` | JE: cinq selecteurs `else_if` qui definissent les variables regionales | **5** |
| `EXPLICIT_STATE_REGIONS` | Aucun bloc exige cette cible d'apres les preuves actuelles | **0** |
| `REMOVE_OR_REDUNDANT` | Aucun | **0** |
| **Total** | | **100** |

## 8. Comparaison fork/hotfix/vanilla

Les SHA-256 montrent que les deux fichiers hotfix sont strictement identiques a leurs homologues vanilla. Il n'existe donc aucune divergence hotfix/vanilla a arbitrer, mais le fork 1776 reste l'autorite pour le comportement historique souhaite.

| Objet | Fork | Hotfix et vanilla | Cible recommandee | Confiance |
|---|---|---|---|---|
| JE `is_shown_when_inactive` | OR de cinq IDs invalides | `geographic_region_india` | Geographic India | Haute |
| JE `possible`, seuils regionaux | Cinq branches historiques, seuils 4/5 | Deux branches north/south, seuil 4 | North/south, hunk vanilla exact | Moyenne-haute: aggregation modifiee |
| JE controles de grande famine | OR de cinq IDs invalides | `geographic_region_india` | Geographic India | Haute |
| JE cinq gardes anti-grande-famine | Cinq OR de cinq IDs | Un test Geographic India par garde | Geographic India | Haute |
| JE selecteurs de variables regionales | Une ancienne region precise par variable | Bengal/Punjab/Central -> north; Bombay/Madras -> south | Decision separee, ne pas importer encore | Faible |
| JE completion regionale | Une ancienne region precise par variable | Cinq geographic regions `*_old` | Subdivision historique correspondante | Haute |
| Events `.1`, `.2`, `.4` | Huit OR de cinq IDs | Huit OR north/south | North/south | Haute |

### Ambiguite des selecteurs regionaux

Dans le hunk vanilla/hotfix, les branches restent ordonnees en `else_if`:

1. Bengal teste north avec `count >= 5`;
2. Punjab teste north avec `count >= 4`;
3. Bombay teste south avec `count >= 4`;
4. Madras teste south avec `count >= 5`;
5. Central India teste north avec `count >= 5`.

Cette structure implique qu'une famine north de cinq states prend toujours le nom Bengal, que Central India ne peut pas atteindre sa branche, et qu'une famine south de cinq states est deja capturee par Bombay avant Madras. Les conditions de completion restent pourtant limitees a Bengal/Bombay/Madras/Punjab/Central India via `*_old`. Le custom loc vanilla affiche directement ces variables dans le nom de la JE. Copier ce hunk sans decision peut donc produire un nom et une condition de fin incoherents.

## 9. Syntaxes par scope

Les syntaxes suivantes sont confirmees dans les deux fichiers vanilla correspondants:

```txt
# State scope, Inde large
is_in_geographic_region = geographic_region_india

# State scope, subdivision historique
is_in_geographic_region = geographic_region_bengal_old

# State scope, appartenance a une strategic region
region = sr:region_north_india

# Country vers ses states
any_scope_state = {
	region = sr:region_north_india
	has_famine = yes
}

# Iterator avec filtre state
random_scope_state = {
	limit = {
		is_in_geographic_region = geographic_region_india
		has_famine = yes
	}
}
```

La forme actuelle de la JE, `region = region_punjab` sans `sr:`, n'est ni une strategic region valide ni la syntaxe geographic-region 1.13.

## 10. Analyse du risque 1776

| Chaine | Garde | Possible en 1776 ? | Risque actuel | Risque apres correction |
|---|---|---|---|---|
| Affichage/activation JE | `has_dlc_feature = ip2_content`; aucun verrou date/technologie | Oui, si les seuils de famine sont atteints | IDs invalides pouvant rendre l'affichage ou `possible` faux et polluer les logs | Activation reelle possible des 1776; verifier les seuils sans ajouter de date ici |
| `on_yearly_pulse` de la JE | JE active; poids `20=0`, trois events a `5` | Oui | Events probablement bloques indirectement par la JE invalide | Events annuels peuvent fonctionner des la premiere famine eligible |
| `indian_famines.1` et `.4` | BIC ou heritage sud-asiatique + famine; aucune date/tech interne | Oui | Trigger et choix de state peuvent echouer | Comportement fonctionnel, mais potentiellement frequent en debut de partie |
| `indian_famines.2` | BIC, pas de `hunger_strike_var`, famine, plantations niveau 5, agitateur | Oui si le setup satisfait ces conditions | Trigger/selection invalides | Event et effets agricoles deviennent accessibles |
| `indian_famines.3` | Declenche par `.2` apres 30 jours | Oui | Aucun risque regional direct | Inchange |
| Completion regionale | Variable regionale deja definie | Oui | JE peut ne jamais finir correctement | Haute confiance avec `*_old`, sauf si la variable a ete choisie par un scope north/south incoherent |

Aucune garde chronologique ne doit etre ajoutee dans HOTFIX-5C2D. Une adaptation historique de date ou de frequence serait une phase distincte.

## 11. References a haute confiance

**95 references** disposent d'une cible confirmee sans ambiguite de syntaxe:

- 45 vers `geographic_region_india`;
- 45 vers north/south, dont 40 dans les events et 5 dans le `possible` de la JE;
- 5 vers les subdivisions historiques `*_old` dans `complete`.

Ces changements doivent etre appliques hunk par hunk. Aucun fichier entier hotfix/vanilla ne doit etre copie, car les versions contiennent d'autres differences hors regions.

## 12. References ambigues

Les cinq references des selecteurs de variables regionales sont ambigues malgre la presence d'un hunk vanilla/hotfix:

| Variable | Cible vanilla/hotfix | Cible semantique alternative | Probleme |
|---|---|---|---|
| `bengal_famine_var` | north | `geographic_region_bengal_old` | North inclut beaucoup plus que Bengal |
| `punjab_famine_var` | north | `geographic_region_punjab_old` | Branche masquee pour `count >= 5` par Bengal |
| `bombay_famine_var` | south | `geographic_region_bombay_old` | South ne couvre pas Gujarat/Sindh/Baluchistan de l'ancienne Bombay |
| `madras_famine_var` | south | `geographic_region_madras_old` | Branche masquee par Bombay des `count >= 4` |
| `central_india_famine_var` | north | `geographic_region_central_india_old` | Branche masquee par Bengal des `count >= 5` |

Recommandation: privilegier une recherche/tests cibles avant implementation. La solution semantiquement la plus coherente parait etre `*_old` pour chaque selecteur, mais elle ne doit pas etre appliquee sans une phase HOTFIX-5C2D3 explicite.

## 13. Plan ferme d'implementation

### HOTFIX-5C2D1 - Controles panindiens a haute confiance

Fichiers autorises:

- `common/journal_entries/04_indian_famines.txt`;
- `events/india_events/indian_famines.txt`;
- rapport D1 dedie.

Objets exacts:

- JE: `is_shown_when_inactive`, controles larges de `possible`, grande famine dans `immediate`, cinq gardes d'exclusion, grande famine dans `complete`;
- JE: cinq branches de seuil de `possible`, remplacees par le hunk north/south vanilla;
- events: les huit listes regionales de `.1`, `.2` et `.4`.

Retrait attendu: **90** anciennes references. Cibles: 45 Geographic India et 45 north/south. Interdits: les cinq selecteurs de variables, les cinq completions regionales, dates, seuils hors hunk, variables, events/options/effects non regionaux. Total global attendu: **283**.

Tests: demarrage avec IP2, apparition de la JE, seuils 4/15, selection de state dans `.1/.2/.4`, `error.log`.

### HOTFIX-5C2D2 - Completions historiques

Fichier autorise:

- `common/journal_entries/04_indian_famines.txt`;
- rapport D2 dedie.

Objet exact: les cinq `trigger_if` de `complete` lies aux variables Bengal, Bombay, Madras, Punjab et Central India.

Retrait attendu: **5** anciennes references. Cibles: les cinq geographic regions `*_old`. Interdits: `possible`, `immediate`, variables, on-actions, events et boutons. Total global attendu apres D2: **278**.

Tests: forcer ou observer chaque variable, supprimer la famine dans la subdivision correspondante, verifier la completion et les tooltips.

### HOTFIX-5C2D3 - Selecteurs regionaux ambigus

Fichier autorise:

- `common/journal_entries/04_indian_famines.txt`;
- rapport D3 dedie.

Objet exact: les cinq tests directs des branches `else_if` qui definissent les variables regionales. Avant modification, choisir explicitement entre le hunk north/south vanilla/hotfix et les cinq subdivisions `*_old` qui preservent les noms historiques.

Retrait attendu si la phase est autorisee: **5** anciennes references. Total global final attendu: **273**. Aucun autre bloc ne doit etre touche.

Tests obligatoires: chacun des cinq scenarios regionaux, ordre des `else_if`, nom dynamique de la JE, variable posee, zone de completion, cas de quatre/cinq/quinze states.

## 14. Totaux attendus par sous-phase

| Etat | Retrait de la sous-phase | Total runtime attendu |
|---|---:|---:|
| Avant HOTFIX-5C2D | 0 | **373** |
| Apres HOTFIX-5C2D1 | 90 | **283** |
| Apres HOTFIX-5C2D2 | 5 | **278** |
| Apres HOTFIX-5C2D3, si decidee | 5 | **273** |

## 15. Tests recommandes

1. Tester avec IP2 actif et uniquement le mod charge.
2. Verifier l'activation en 1776 pour BIC et au moins un pays sud-asiatique non BIC.
3. Tester les seuils de 4, 5 et 15 states en famine.
4. Verifier les trois events du pulse annuel et le state sauvegarde.
5. Tester l'option agricole de `.2` sur les plantations eligibles.
6. Tester le nom dynamique et la completion des cinq famines regionales.
7. Surveiller `error.log` pour les cinq anciens IDs, `Invalid right side`, `Invalid strategic region`, erreurs de scope et PostValidate.

## 16. Fichier cree

- `docs/reports/hotfix/HOTFIX_5C2D_AUDIT_INDIAN_FAMINES_REGIONS.md`

## 17. Gameplay inchange

Aucun fichier gameplay n'a ete modifie. Aucun fichier du hotfix ou de la vanilla n'a ete copie.

## 18. Domaines proteges

Sepoy, Durrani, BIC, NAVY, ADMIN et MARATH n'ont pas ete modifies. Aucune date, technologie, loi, formation, localisation, carte, state, pop, building, bouton ou event n'a ete change.

## 19. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present et intact. Il n'a ete ni applique, ni inspecte comme contenu courant, ni restaure, ni supprime.
