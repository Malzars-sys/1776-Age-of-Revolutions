# HOTFIX-5C2E-AUDIT - Uneasy Raj / Sepoy Mutiny regions

## 1. Resume executif

Cet audit couvre exclusivement `common/journal_entries/04_sepoy_mutiny.txt` et `events/india_events/sepoy_mutiny_events.txt`. Il recense exactement 142 references actives aux cinq anciens IDs indiens : 10 dans la journal entry et 132 dans les events. Le total historique approximatif de HOTFIX-5C1 etait donc exact.

Le hotfix et la vanilla 1.13 sont byte-identiques pour les deux fichiers et ne contiennent plus aucune de ces 142 references. Leur migration n'est toutefois pas un remplacement global :

- 135 occurrences relèvent de selections strategiques ou de capitales, majoritairement converties vers `region_north_india` et `region_south_india` ;
- 2 occurrences de l'event 4 deviennent la subdivision historique `geographic_region_bombay_old` ;
- 5 scopes de strategic regions sauvegardes par `je_uneasy_raj` sont simplement supprimes par la vanilla, car ils ne sont jamais relus ;
- les exceptions `region_himalayas`, `STATE_PASHTUNISTAN` et `STATE_QUETTA` doivent rester explicites ;
- le portage regional ne doit pas activer la chaine en 1776.

Avec un total runtime global initial de 273, la correction des 142 occurrences de cette chaine conduirait a 131 occurrences invalides restantes dans le reste du mod.

## 2. Etat Git

Etat initial verifie avant toute creation :

- branche : `hotfix-dlc-audit` ;
- working tree : propre ;
- HEAD : `f89273d Fix historical famine region selectors` ;
- HOTFIX-5C2D3 est donc present ;
- stash : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- stash non applique, non modifie et non inspecte comme contenu du fork courant.

## 3. Comptage initial

Le comptage exclut les commentaires et recherche les tokens exacts, afin de ne pas compter les cibles valides telles que `geographic_region_bengal_old`.

| Fichier | Bengal | Bombay | Central India | Madras | Punjab | Total |
|---|---:|---:|---:|---:|---:|---:|
| `common/journal_entries/04_sepoy_mutiny.txt` | 2 | 2 | 2 | 2 | 2 | 10 |
| `events/india_events/sepoy_mutiny_events.txt` | 23 | 25 | 30 | 24 | 30 | 132 |
| **Total** | **25** | **27** | **32** | **26** | **32** | **142** |

Il n'y a aucun ecart avec l'estimation HOTFIX-5C1 de 142. Cette estimation se decomposait deja correctement en 10 + 132 ; le present audit ajoute la ventilation exacte par ID, event, option et sous-bloc.

## 4. Definitions vanilla

Les anciens IDs `region_bengal`, `region_bombay`, `region_central_india`, `region_madras` et `region_punjab` ne sont plus definis comme strategic regions dans la vanilla locale.

| Region ou state region | Type | Membres ou localisation | Usage potentiel |
|---|---|---|---|
| `region_north_india` | strategic region | Gujarat, Sindh, Central Provinces, Awadh, Malwa, Agra, Bundelkhand, Bihar, East/West Bengal, Assam, Orissa, Punjab, Hill Punjab, Delhi, Rajputana | Controles larges du nord, capitales et breakup |
| `region_south_india` | strategic region | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool, Bombay | Controles larges du sud, capitales et breakup |
| `geographic_region_india` | geographic region | north India + south India + Quetta + Pashtunistan + Kashmir + Baluchistan | Visibilite ou controle panindien incluant les frontieres |
| `geographic_region_bengal_old` | geographic region historique | Bihar, East/West Bengal, Assam, Orissa | Presidency historique du Bengale |
| `geographic_region_bombay_old` | geographic region historique | Bombay, Gujarat, Sindh, Baluchistan | Presidency historique de Bombay |
| `geographic_region_central_india_old` | geographic region historique | Central Provinces, Awadh, Malwa, Agra, Bundelkhand | Centre historique |
| `geographic_region_madras_old` | geographic region historique | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool | Presidency historique de Madras |
| `geographic_region_punjab_old` | geographic region historique | Punjab, Hill Punjab, Delhi, Rajputana | Punjab historique |
| `region_himalayas` | strategic region | Himalayas et plateau tibetain, dont Kashmir | Exception peripherique conservee dans les selections de breakup |
| `STATE_PASHTUNISTAN` | state region explicite | frontiere nord-ouest, hors des deux strategic regions indiennes | Exception frontaliere explicite dans l'event 2 |
| `STATE_QUETTA` | state region explicite | frontiere baloutche, hors des deux strategic regions indiennes | Exception frontaliere explicite dans l'event 2 |

Les listes de states explicitement manipulees par l'event 2 incluent notamment Madras, Mandalay, Pegu, Gujarat, Tenasserim, Travancore, Circars, Kurnool, Delhi, Agra, Awadh, Central Provinces et Bombay. Elles implementent les reprises prioritaires avant la redistribution par voisinage et ne doivent pas etre remplacees par un filtre regional large.

## 5. Inventaire de la journal entry

Le fichier contient deux objets : `je_uneasy_raj` et `je_sepoy_mutiny`.

### `je_uneasy_raj`

- `should_be_involved` : BIC ;
- `possible` dans le fork : `always = no`, avec ancien garde date/technologie commente ;
- `should_show_when_not_involved` : deja correctement fonde sur `geographic_region_india` ;
- progress bars : Bengal, Bombay et Madras uniquement ;
- `immediate` : initialise les trois variables globales de progression et le timer ;
- cinq blocs invalides sauvegardent des scopes strategiques jamais relus ;
- `complete` : regle coloniale consolidee, niveau de vie et radicals ;
- `fail` : timer ou expiration ;
- pulses hebdomadaire et mensuel : mettent a jour les variables de progression et peuvent declencher des events ;
- aucune ancienne region n'apparait dans `possible`, `complete`, `fail` ou dans les progress bars elles-memes.

### `je_sepoy_mutiny`

- ajoutee par l'echec de `je_uneasy_raj` ;
- suit MUG, BGL, SAT et PAN comme revoltes possibles ;
- `complete` exige la disparition des revoltes, une faible secession et la paix ;
- `fail` verifie les revoltes territoriales par state regions explicites ;
- le `hidden_trigger` contient les cinq anciennes regions pour verifier la capitale de la cible d'un `dp_sepoy_mutiny` ;
- `on_fail` declenche `sepoy_mutiny_events.2`.

| Objet | Sous-bloc | Scope | Nombre | Role | Cible probable | Confiance |
|---|---|---|---:|---|---|---|
| `je_uneasy_raj` | `immediate` scopes sauvegardes | strategic region | 5 | Scopes de presidencies, sans lecteur | suppression, comme vanilla | haute |
| `je_sepoy_mutiny` | `fail/hidden_trigger` | capitale de la cible du play | 5 | Detecter un play encore actif en Inde | north India OR south India | haute |

Les dix references ne sont donc pas toutes dans un hidden trigger : cinq sont dans l'`immediate` de `je_uneasy_raj`, cinq dans le `hidden_trigger` de `je_sepoy_mutiny`.

## 6. Inventaire des events

Seuls `sepoy_mutiny_events.2` et `sepoy_mutiny_events.4` contiennent les anciens IDs.

### `sepoy_mutiny_events.2` - 122 occurrences

Cet event est lance par `je_sepoy_mutiny.on_fail`. Ses quatre options territoriales sont :

- option `2.a` : independance des princes et breakup general, 35 occurrences ;
- option `2.b` : retraite vers le Bengale, 29 occurrences ;
- option `2.c` : retraite vers Madras, 29 occurrences ;
- option `2.e` : retraite vers Bombay, 29 occurrences.

| Event / option | Bloc fonctionnel | Occurrences | Fonction | Cible vanilla | Risque |
|---|---|---:|---|---|---|
| `.2.a` | detection de sujets | 5 | savoir si des princes doivent etre liberes | north + south, frontieres preservees | moyen |
| `.2.a` | filtre de liberation | 5 | rendre les sujets independants | north + south, frontieres preservees | eleve |
| `.2.a` | garde de breakup | 5 | autoriser les reprises prioritaires | north + south, Himalaya/frontieres preserves | eleve |
| `.2.a` | source de propagation | 5 | trouver un state BIC adjacent | north + south, Himalaya/frontieres preserves | eleve |
| `.2.a` | capitale du voisin | 5 | valider le prince adjacent | north + south, frontieres preservees | eleve |
| `.2.a` | selection du prince | 5 | choisir les pays receveurs | north + south, frontieres preservees | eleve |
| `.2.a` | state aleatoire transfere | 5 | transferer un state adjacent | north + south, Himalaya/frontieres preserves | eleve |
| `.2.b` | memes sept fonctions | 28 | retraite et breakup autour du Bengale | north + south avec exceptions | eleve |
| `.2.b` | radicals finaux | 1 | radicals dans la zone de retraite | north India | moyen |
| `.2.c` | memes sept fonctions | 28 | retraite et breakup autour de Madras | north + south avec exceptions | eleve |
| `.2.c` | radicals finaux | 1 | radicals dans la zone de retraite | south India | moyen |
| `.2.e` | memes sept fonctions | 28 | retraite et breakup autour de Bombay | north + south avec exceptions | eleve |
| `.2.e` | radicals finaux | 1 | radicals dans la zone de retraite | south India | moyen |

Les quatre options ne doivent pas etre fusionnees : elles conservent des states de repli et des reprises prioritaires differents. Le CSV detaille les 31 sous-blocs de l'event 2 separement.

### `sepoy_mutiny_events.4` - 10 occurrences

| Event / option | Bloc | Occurrences | Fonction | Cible vanilla | Risque |
|---|---|---:|---|---|---|
| `.4.a` | alignement SAT | 2 | rejoindre le play SAT depuis la sphere de Bombay | `geographic_region_bombay_old` | moyen |
| `.4.a` | alignement MUG | 3 | rejoindre le play MUG depuis le nord | `region_north_india` | moyen |
| `.4.b` | poids IA MUG | 3 | favoriser l'option moghole au nord | `region_north_india` | faible |
| `.4.c` | poids IA SAT | 2 | favoriser l'option marathe au sud | `region_south_india` | faible |

La vanilla ajoute aussi une branche KNO fondee sur `geographic_region_madras_old`. Cette addition ne remplace aucune des 142 occurrences et ne doit donc pas etre importee implicitement sans validation du hunk complet.

## 7. Classification semantique

Chaque bloc du CSV appartient a une seule categorie principale.

| Classification | Blocs | Occurrences | Priorite |
|---|---:|---:|---|
| `CAPITAL_OR_REVOLT_SELECTION` | 20 | 81 | critique avant test de breakup |
| `PAN_INDIA_STRATEGIC` | 15 | 54 | haute |
| `HISTORICAL_PRESIDENCY` | 1 | 2 | haute, hunk event 4 isole |
| `REMOVE_OR_REDUNDANT` | 1 | 5 | haute, suppression vanilla exacte |
| `PAN_INDIA_GEOGRAPHIC` | 0 | 0 | aucune ancienne reference de cette chaine |
| `EXPLICIT_STATE_REGIONS` | 0 | 0 | listes existantes a preserver |
| `FRONTIER_STATE_REGIONS` | 0 | 0 | exceptions existantes a preserver |
| `MANUAL_RESEARCH_REQUIRED` | 0 | 0 | aucune cible non resolue par hotfix/vanilla |
| **Total** | **37** | **142** | |

Les frontieres explicites sont des siblings valides des anciennes references, pas des occurrences invalides. Elles figurent donc dans les notes du CSV sans gonfler le total.

## 8. Analyse des presidencies

| Presidency | Initialisation | Progression | Propagation | Resolution | Cible recommandee |
|---|---|---|---|---|---|
| Bengal | barre et variable globale, pas une zone | scripted progress bar et events | option `2.b`, breakup et voisinage | radicals vanilla sur north India | supprimer le scope obsolete ; north India pour l'effet final |
| Bombay | barre et variable globale, pas une zone | scripted progress bar et events | option `2.e`, breakup et voisinage | radicals vanilla sur south India ; event 4 historique sur Bombay old | supprimer le scope obsolete ; choisir la cible selon le bloc |
| Madras | barre et variable globale, pas une zone | scripted progress bar et events | option `2.c`, breakup et voisinage | radicals vanilla sur south India | supprimer le scope obsolete ; south India pour l'effet final |
| Punjab | aucune barre propre | aucune initialisation propre | seulement inclus dans les selections larges | pas de resolution de barre | north India dans les controles strategiques |
| Central India | aucune barre propre | aucune initialisation propre | seulement inclus dans les selections larges | pas de resolution de barre | north India dans les controles strategiques |

Les noms des variables de progression ne definissent pas une zone. Les trois barres lisent leurs variables globales et les effets/scripts associes ; aucun des cinq scopes sauvegardes aux lignes 44-56 n'est reference ailleurs. Leur suppression ne modifie donc pas l'initialisation des barres.

## 9. Analyse des progress bars

Les progress bars sont definies en vanilla dans `common/scripted_progress_bars/00_sepoy_mutiny_progress_bars.txt`. Elles couvrent Bengal, Bombay et Madras, utilisent les variables globales correspondantes et sont modifiees par des scripted effects et events.

Constats :

- aucune barre Punjab ou Central India n'existe ;
- aucune barre ne lit `bengal_sr_scope`, `bombay_sr_scope`, `madras_sr_scope`, `punjab_sr_scope` ou `central_india_sr_scope` ;
- les cinq scopes ne servent donc ni au calcul, ni a l'affichage, ni a la resolution ;
- les effets territoriaux de l'event 2 emploient volontairement les nouvelles strategic regions larges dans la vanilla ;
- il ne faut pas convertir automatiquement toutes les variables nommees Bengal/Bombay/Madras vers les subdivisions `*_old`.

## 10. Creation et propagation de la revolte

La creation des pays revoltes et du `dp_sepoy_mutiny` est principalement deleguee aux scripted effects hors des deux fichiers audites. Dans les deux fichiers autorises :

- `je_uneasy_raj` determine quand les effets de mutinerie doivent etre lances ;
- `je_sepoy_mutiny` suit les revoltes et declenche l'event 2 en cas d'echec ;
- l'event 2 libere des princes, recree certains tags, transfere des states, puis redistribue des states BIC a des voisins eligibles ;
- l'event 4 permet aux princely states de rejoindre les plays SAT, KNO ou MUG selon leur capitale et leurs affinites.

Le remplacement trop large par `geographic_region_india` dans l'event 2 inclurait Kashmir et Baluchistan en plus de Pashtunistan/Quetta, alors que la vanilla choisit north/south puis ajoute seulement certaines exceptions. Il pourrait donc liberer ou transferer des states non prevus.

## 11. Selections de states et capitales

Les blocs a fort impact sont :

- les filtres de capitales des sujets rendus independants ;
- les listes de pays eligibles a recevoir un state ;
- les `while` de propagation par voisinage ;
- les `random_scope_state` qui transferent effectivement la propriete ;
- le filtre de capitale de `je_sepoy_mutiny.fail` ;
- les choix d'alignement et poids IA de l'event 4.

Risques d'une cible trop large :

- inclusion de Baluchistan ou Kashmir par un filtre geographic India ;
- inclusion non controlee de Pashtunistan, Quetta ou Himalaya si les exceptions sont absorbees ;
- liberation de sujets dont la capitale n'etait pas visee ;
- transfert d'un state frontalier hors du breakup prevu ;
- choix d'une faction de revolte incoherente avec la presidency historique ;
- boucle de propagation plus longue ou sans candidat valide.

La vanilla fournit une solution fermee : paire north/south pour l'event 2, exceptions explicites conservees, subdivision Bombay old pour le premier hunk de l'event 4.

## 12. Comparaison fork / hotfix / vanilla

Les hashes SHA-256 confirment que les deux fichiers hotfix sont identiques a leurs homologues vanilla. Le fork diverge par les anciennes regions et par quelques adaptations/differences qui ne doivent pas etre importees globalement.

| Objet | Fork | Hotfix | Vanilla | Cible recommandee | Confiance |
|---|---|---|---|---|---|
| `je_uneasy_raj.immediate` | cinq scopes invalides sauvegardes | scopes absents | scopes absents | supprimer les cinq blocs | haute |
| `je_sepoy_mutiny.fail.hidden_trigger` | cinq anciennes regions | north + south | north + south | north + south | haute |
| event 2, options a/b/c/e | anciennes presidencies + exceptions | north/south + memes exceptions | identique hotfix | hunks vanilla locaux | haute technique, moyenne gameplay 1776 |
| event 2, radicals Bengal | ancienne Bengal | north India | north India | north India | haute |
| event 2, radicals Madras/Bombay | anciennes Madras/Bombay | south India | south India | south India | haute |
| event 4, SAT | Bombay OR Madras anciennes | Bombay old | Bombay old | Bombay old | haute |
| event 4, KNO | branche absente du fork | Madras old | Madras old | audit/import explicite dans le hunk E2 | moyenne pour le fork 1776 |
| event 4, MUG | Bengal/Punjab/Central anciennes | north India | north India | north India | haute |
| event 4, poids SAT | Bombay/Madras anciennes | south India | south India | south India | haute |

Le hotfix sert ici d'indication d'intention forte, car il est identique a la vanilla. Le setup territorial et chronologique du fork 1776 reste cependant l'autorite pour les tests de comportement.

## 13. Syntaxes par scope

Toutes les syntaxes suivantes sont attestees dans la vanilla locale :

```txt
# State scope, Inde geographique large
is_in_geographic_region = geographic_region_india

# State scope, presidency historique
is_in_geographic_region = geographic_region_bombay_old

# State scope, strategic region
region = sr:region_north_india
region = sr:region_south_india

# Strategic-region scope direct
sr:region_north_india = {
	root_owns_state_in_region = yes
}

# State region explicite
state_region = s:STATE_PASHTUNISTAN
```

Le `sr:` est requis pour les comparaisons `region = ...` et les scopes directs de strategic regions. `is_in_geographic_region` attend un identifiant de geographic region sans prefixe `sr:`.

## 14. Risque de declenchement en 1776

| Chaine | Garde actuelle | Accessible en 1776 ? | Risque actuel | Risque apres correction regionale |
|---|---|---|---|---|
| `je_uneasy_raj` | `possible = { always = no }` | non organiquement | faible ; definition chargee mais inactive | inchange si le garde reste intact |
| ajout global | ligne `add_contextless_journal_entry` commentee | non | faible | inchange |
| ancien garde date/tech | `year > 1830`, nationalism et secession, entierement commente | non applique | aucun effet runtime | ne pas restaurer dans cette migration |
| `je_sepoy_mutiny` | ajoutee seulement par l'echec d'Uneasy Raj | non organiquement | faible | inchange |
| event 2 | appele par `je_sepoy_mutiny.on_fail` | non organiquement | faible, sauf console/appel force | comportement territorial corrigé si appele |
| event 4 | appele par les scripted effects de la chaine | non organiquement | faible, sauf console/appel force | alignements corriges si appele |
| garde DLC | aucune dans les deux fichiers | sans objet tant que la JE est desactivee | faible | inchange |

BIC existe dans le setup 1776, mais cela ne suffit pas a activer la chaine. Aucune date, technologie, loi BIC, valeur de radicals ou variable historique ne doit etre modifiee dans le portage regional. Une future activation chronologique est un chantier separe.

## 15. References a haute confiance

Les 142 occurrences disposent d'une cible vanilla/hotfix exacte :

- 5 scopes redondants a supprimer ;
- 5 tests du hidden trigger JE a convertir en paire north/south ;
- 122 usages de l'event 2 a convertir selon les hunks north/south vanilla ;
- 2 usages de l'event 4 a convertir en Bombay old ;
- 8 usages de l'event 4 a convertir en north ou south India.

La confiance syntaxique est haute. Le risque reside dans les effets de territoire, pas dans l'identification des cibles.

## 16. References ambigues

Aucune des 142 anciennes references n'est sans cible. Deux points exigent toutefois une validation comportementale :

1. La paire north/south est parfois plus large que la liste ancienne d'une option qui omettait sa zone de repli. C'est le comportement vanilla actuel, mais il faut verifier qu'il ne redistribue pas le state de repli dans le setup 1776.
2. Le hunk SAT de l'event 4 retire Madras de la branche SAT et ajoute une branche KNO/Madras. La cible region est certaine ; l'import de la branche KNO, qui n'ajoute aucune ancienne-reference retiree, doit rester explicite et trace.

Les listes explicites de state regions et les exceptions frontalieres ne sont pas ambigues et doivent rester inchangees.

## 17. Plan ferme d'implementation

### HOTFIX-5C2E1 - Controles panindiens et hidden trigger

- fichiers autorises : les deux fichiers audites ;
- objets : `je_sepoy_mutiny.fail.hidden_trigger`, event 4 options a/b/c ;
- anciennes references retirees : 13 ;
- cibles : north/south selon les hunks vanilla ;
- interdits : activation de la JE, date/technologie, Persia, localisations, scripted effects ;
- total runtime global attendu : 273 -> 260 ;
- tests : chargement sans invalid region, filtre de play et poids IA via console/save de test.

### HOTFIX-5C2E2 - Presidencies, initialisation et effets regionaux

- fichiers autorises : les deux fichiers audites ;
- objets : `je_uneasy_raj.immediate`, event 2 radicals Bengal/Madras/Bombay, event 4 option a SAT ;
- anciennes references retirees : 10 ;
- cibles : suppression des cinq scopes ; north India pour Bengal ; south India pour Madras/Bombay ; Bombay old pour SAT ;
- hunk KNO/Madras : n'ajoute aucun retrait au compteur, import uniquement s'il est explicitement inclus et teste ;
- interdits : progress bars, variables, valeurs de radicals, lois et technologie BIC ;
- total runtime global attendu : 260 -> 250 ;
- tests : valeurs des trois barres inchangees, effets radicals dans les states attendus, alignement SAT/KNO.

### HOTFIX-5C2E3 - Selections, capitales, propagation et breakup

- fichier autorise : `events/india_events/sepoy_mutiny_events.txt` ;
- objets : event 2 options a/b/c/e, hors trois lignes de radicals traitees en E2 ;
- anciennes references retirees : 119 ;
- cibles : paires north/south vanilla avec maintien de Himalayas, Pashtunistan et Quetta ;
- interdits : listes de reprises prioritaires, tags crees, lois appliquees, war goals, ownership hors hunks regionaux ;
- total runtime global attendu : 250 -> 131 ;
- tests : chaque option, liberation de sujets, pays recrees, boucle de voisinage, capitales, transferts, fin de BIC.

### HOTFIX-5C2E4 - Cas ambigus et listes explicites

- aucune ancienne reference a modifier sur la base de cet audit ;
- anciennes references retirees : 0 ;
- total runtime global attendu : 131 -> 131 ;
- ouvrir cette phase seulement si les tests E3 montrent une divergence du setup 1776 ;
- toute liste explicite devra etre justifiee state par state, sans remplacer les choix vanilla par supposition.

## 18. Totaux attendus par sous-phase

| Phase | References retirees | Total global attendu |
|---|---:|---:|
| Initial | 0 | 273 |
| HOTFIX-5C2E1 | 13 | 260 |
| HOTFIX-5C2E2 | 10 | 250 |
| HOTFIX-5C2E3 | 119 | 131 |
| HOTFIX-5C2E4 | 0 | 131 |
| **Total chaine** | **142** | **131** |

Le champ `occurrence_count` du CSV totalise exactement 142.

## 19. Tests en jeu recommandes

1. Demarrer en 1776 avec BIC et confirmer que `je_uneasy_raj` ne s'active pas spontanement.
2. Verifier `error.log` pour les cinq anciens IDs et pour `Invalid scope` / `Invalid right side`.
3. Sur une sauvegarde de test, forcer la chaine et verifier les trois progress bars sans modifier leurs valeurs de script.
4. Tester separement les options 2.a, 2.b, 2.c et 2.e.
5. Relever les sujets liberes et les states transferes avant/apres chaque option.
6. Verifier que Pashtunistan, Quetta et Himalaya ne sont inclus que par leurs exceptions existantes.
7. Verifier qu'aucune capitale de revolte n'est choisie hors du noyau attendu.
8. Verifier SAT, KNO et MUG dans l'event 4, y compris le poids IA et les war goals.
9. Laisser tourner au moins un mois apres le breakup et surveiller les boucles de transfert.
10. Recompter globalement : 260 apres E1, 250 apres E2, 131 apres E3.

## 20. Fichiers crees

- `docs/reports/hotfix/HOTFIX_5C2E_AUDIT_SEPOY_MUTINY_REGIONS.md`
- `docs/reports/hotfix/HOTFIX_5C2E_SEPOY_REGION_MAP.csv`

Le CSV est encode en UTF-8 avec BOM.

## 21. Confirmation gameplay

Aucun fichier gameplay n'a ete modifie. Aucun fichier du hotfix ou de la vanilla n'a ete copie. Les deux sources ont uniquement ete lues et comparees par hunks.

## 22. Domaines proteges

Sont inchanges :

- BIC, `law_frontier_colonization`, ses autres lois et sa technologie ;
- Bengal Army et toutes les formations militaires ;
- Durrani ;
- Indian Famines ;
- India Railway ;
- batiments, ports et shipyards ;
- localisations ;
- boutons coloniaux ;
- NAVY et ADMIN ;
- MARATH et Travancore.

## 23. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present, intact et non applique. Aucun `git stash pop` ni restauration de stash n'a ete execute.
