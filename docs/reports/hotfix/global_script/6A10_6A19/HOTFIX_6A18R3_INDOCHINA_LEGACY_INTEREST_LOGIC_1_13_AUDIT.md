# HOTFIX-6A.18R3/F3 — Audit puis retrait de la logique legacy d'intérêt en Indochine

## 1. Phase, date et résultat

- phases : `HOTFIX_6A18R3_INDOCHINA_LEGACY_INTEREST_LOGIC_1_13_AUDIT`, puis
  `HOTFIX_6A18F3_INDOCHINA_REMOVE_LEGACY_INTEREST_LOGIC_1_13_ALIGNMENT`;
- date : 4 août 2026;
- branche : `hotfix-dlc-audit`;
- HEAD initial et final :
  `e6c06c3cfdd90ab91a411d81aa7a4d8acae35613`;
- message du HEAD : `Align Egyptian crisis involvement with 1.13`;
- nature : audit documentaire et statique, suivi de la correction bornée
  autorisée par l'opérateur humain;
- gameplay : un seul bloc legacy supprimé dans `events/indochina.txt`;
- runtime : aucun;
- commit automatique : aucun.

L'audit prouve que le garde de slots et l'effet d'intérêt de `indochina.3.a`
appartiennent à l'ancien système binaire, sont rejetés ou absents en 1.13 et ne
soutiennent aucune conséquence voisine. Source hotfix et vanilla 1.13
suppriment exactement ce bloc sans `add_involvement`. Aucune intention 1776
spécifique ne justifie sa conservation. Après lecture de ces preuves,
l'opérateur humain a choisi explicitement de supprimer le bloc. F3 applique
donc cette décision sans ajouter d'implication de remplacement.

## 2. Préflight et état Git initial

| Contrôle | Résultat |
| --- | --- |
| racine | fork exact |
| branche | `hotfix-dlc-audit` |
| HEAD | `e6c06c3cfdd90ab91a411d81aa7a4d8acae35613` |
| message | exact |
| rapport F2 dans le HEAD | présent, onze verdicts présents |
| arbre suivi | propre |
| index staged | vide |
| non suivis | seulement `bject` et sept recherches technologiques protégées |
| `00_interests.txt` dans le HEAD | absent, `git cat-file -e` retourne 128 |
| `git diff --check` | PASS |
| Victoria 3 / Dowser / launcher Paradox | aucun processus |

Stash protégé :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

## 3. Sources lues

Les sources obligatoires ont été lues intégralement avant conclusion :

- les trois versions d'`events/indochina.txt`;
- `indochina.1`, `indochina.3`, `indochina.4` et
  `common/journal_entries/01_indochina.txt`;
- les localisations anglaises vanilla de la chaîne événementielle;
- rapports 6A.18F2, 6A.18R2 et 6A.18Q;
- roadmap, matrice des blocs et index des rapports;
- les trois inventaires CSV canoniques, chargés avec `Import-Csv`;
- changelogs complets du fork et de la source;
- audit amont cité par l'inventaire;
- journaux courants et 60 rotations/fichiers pertinents;
- historique Git et blame du fichier cible;
- texte script, métadonnées et chaînes ASCII de `victoria3.exe` nécessaires à
  l'audit des trois identifiants.

La source hotfix, le vanilla, les logs, les localisations et tous les périmètres
protégés sont restés strictement en lecture seule.

## 4. Baselines et formats trois voies

| Arbre/fichier | Octets | Lignes | SHA-256 | Format |
| --- | ---: | ---: | --- | --- |
| fork Indochine | 9626 | 516 | `177A6446668E9274260FCA90B0F7B0802280CA7E086CC1290E15C862E845B2BB` | BOM UTF-8, LF, saut final |
| source hotfix Indochine | 9575 | 508 | `17C22704A0E650EAEEEFFE7B9DA68CD1BAAD88D0F82C1D2594955CC737CEF8B4` | BOM UTF-8, LF, saut final |
| vanilla 1.13 Indochine | 9575 | 508 | `17C22704A0E650EAEEEFFE7B9DA68CD1BAAD88D0F82C1D2594955CC737CEF8B4` | BOM UTF-8, LF, saut final |
| fork crise égyptienne F2 | 4297 | 196 | `E637C1F8EF27BBEBCB43C516EB5F0E6C943ECC7A51FC1A06FCD73999547489F7` | BOM UTF-8, LF, saut final |

Source hotfix et vanilla sont byte-identiques pour l'Indochine. Le fork ne
contient plus qu'une occurrence active d'`add_declared_interest`, à la ligne
346 de ce fichier.

## 5. Identification exacte de l'objet

```text
event = indochina.3
type = country_event
fork lines = 299–405
source/vanilla lines = 298–397
option = indochina.3.a
default_option = yes
```

L'objet a été extrait par équilibre des accolades : 107 lignes dans le fork,
100 dans source/vanilla.

### 5.1 Appel entrant et pays receveur

`indochina.1` est un `country_event` dont le root est le pays indochinois
persécutant les catholiques. Son trigger exige notamment :

- capitale dans `sr:region_indochina`;
- loi de religion d'État;
- population catholique;
- existence d'une grande puissance catholique dont la capitale est hors
  d'Indochine.

L'option `indochina.1.a` fixe `indochina_campaign_target` sur ce pays root,
sélectionne `scope:potential_imperial_power`, puis exécute :

```txt
scope:potential_imperial_power = {
    trigger_event = { id = indochina.3 days = 30 }
}
```

Le root recevant `indochina.3` est donc la grande puissance catholique. Le pays
indochinois persécuteur est retrouvé en `immediate` par sa variable puis sauvé
comme `scope:indochina_target`. Le scope root ne change pas dans l'option `.3.a`.

### 5.2 Scopes, variables et relations

- `scope:indochina_target` : pays indochinois cible;
- `scope:potential_imperialism_initiator` : root de `.3`, grande puissance;
- `indochina_campaign_target` : variable posée sur le pays cible;
- `je_indochina` : journal entry ajouté au root;
- objectif secret `conquer` du root envers la cible;
- incident de valeur 20 contre la cible;
- notifications selon la pertinence diplomatique.

L'option `.3.b` améliore les relations avec la cible, pénalise certains groupes
d'intérêt et retire la variable. Elle n'est pas touchée.

### 5.3 Appels sortants

`.3.a` n'appelle aucun autre événement. Le journal entry ajouté sauvegarde la
cible, fixe `indochina_intervention_happened`, vérifie conquêtes, sujets et
contrôle d'États dans `sr:region_indochina`, puis appelle `indochina.4` à sa
complétion. Aucun de ces triggers ne dépend d'un intérêt déclaré ou d'une
valeur d'implication.

## 6. Bloc legacy et effets voisins

Bloc fork :

```txt
		if = {
			limit = {
				num_declared_interests < max_num_declared_interests
			}
			add_declared_interest = region_indochina
		}
```

Effet précédent :

```txt
add_journal_entry = {
    type = je_indochina
}
```

Effets suivants : objectif secret `conquer`, incident 20 et notifications.
Le bloc legacy ne produit aucun scope, aucune variable et aucun résultat lu par
ces effets.

L'ancienne région `region_indochina` désignait la région binaire dans laquelle
la grande puissance devait recevoir un intérêt déclaré. Elle servait à ouvrir
des interactions diplomatiques ultérieures, pas à faire fonctionner le journal
entry ou les conséquences immédiates.

## 7. Comparaison trois voies

### 7.1 Fork vers source hotfix

Le fichier complet présente cinq hunks :

1. garde global d'`indochina.1` absent du fork;
2. clé legacy de `has_interest_marker_in_region` dans `indochina.2`;
3. ancienne forme de `set_variable`;
4. ancienne forme de retrait de variable;
5. bloc d'intérêt legacy de `indochina.3`.

L'objet `.3` ne présente qu'un seul hunk : la suppression des six lignes du
bloc et de sa ligne blanche terminale. Aucun hunk voisin n'est absorbé.

### 7.2 Fork vers vanilla 1.13

Le résultat est identique : cinq hunks au fichier, un seul dans `.3`. Vanilla
supprime le garde et l'effet sans ajouter `add_involvement`, traité, pacte,
revendication, présence militaire ou autre compensation.

### 7.3 Source hotfix vers vanilla 1.13

Zéro hunk au fichier et zéro hunk dans l'objet. La source hotfix a déjà adopté
exactement le comportement vanilla.

### 7.4 Conditions et probabilités IA

`.3.a` reste l'option par défaut dans les trois arbres et ne possède pas
d'`ai_chance` propre. `.3.b` réutilise la localisation de `.2.b`. Les
localisations anglaises décrivent une représaille, l'ouverture de l'Indochine,
un casus belli et une future intervention; aucune ne promet ni ne nomme un
intérêt déclaré.

## 8. Audit séparé des trois identifiants

| Identifiant | Ancien type attendu | Usage fork actif | Source | Vanilla 1.13 | Diagnostic | Registre 1.13 | Remplacement exact | Classification |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| `num_declared_interests` | valeur/trigger numérique du nombre de slots utilisés | 1 | 0 | 0 | `Unknown trigger type` | absent | aucun | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| `max_num_declared_interests` | valeur numérique de capacité maximale | 1, opérande droite | 0 | 0 | aucun diagnostic séparé, car le trigger externe échoue d'abord | absent | aucun | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| `add_declared_interest` | effet ajoutant un intérêt binaire | 1 | absent de ce fichier | 0 | `Unknown effect` | absent | aucun dans ce contexte | `VANILLA_1_13_ALIGNMENT_REQUIRED` |

Les recherches ASCII dans `victoria3.exe` donnent zéro occurrence pour les
trois identifiants legacy et quatre pour `add_involvement`. Ce dernier est un
effet enregistré, mais il ne constitue pas le remplacement du bloc indochinois
: il ajoute une valeur courante temporaire, alors que vanilla ne l'utilise pas
ici.

À l'échelle de la source hotfix complète, `add_declared_interest` subsiste dans
son ancien historique fixe et dans d'autres événements legacy; cela ne change
pas la comparaison ciblée : sa version d'`events/indochina.txt` en contient
zéro et est byte-identique au vanilla. Les deux identifiants de capacité sont
absents de toute la source.

## 9. Diagnostics actuels et historiques

Le `debug.log` courant contient :

```text
[14:58:18] Unknown trigger type: num_declared_interests ... events/indochina.txt:344
[14:58:18] Unknown effect add_declared_interest at events/indochina.txt:346
```

`debug.2.log` contient les mêmes deux causes à `13:23:05`. Sur toutes les
rotations pertinentes :

- `num_declared_interests` : 2 lignes, deux fichiers, deux timestamps;
- `max_num_declared_interests` : 0 ligne explicite;
- `add_declared_interest` : 95 lignes, dont 93 dans l'ancienne session avec
  l'historique fixe et deux dans le log courant antérieur à F2.

Les logs courants n'ont pas été renouvelés après F2; le diagnostic égyptien
qu'ils contiennent est donc historique par rapport au HEAD. Le diagnostic
indochinois demeure pertinent jusqu'à F3.

## 10. Intention fonctionnelle — réponses

1. Le garde empêchait de dépasser la capacité d'intérêts binaires déclarés.
2. Oui, l'ancien système limitait leur nombre par slots.
3. Non, cette limitation n'existe plus sous cette forme en 1.13.
4. Non, le système d'implication graduée n'expose pas une capacité équivalente.
5. Non, la conséquence principale ne dépend pas de l'intérêt.
6. Oui, l'intérêt facilitait seulement les interactions diplomatiques futures.
7. Oui, l'événement reste cohérent : JE, objectif, incident et notifications
   restent complets.
8. Oui, vanilla supprime les deux identifiants et leur enveloppe sans
   compensation.
9. Non, la source hotfix ne conserve pas l'ancien comportement; elle est
   byte-identique au vanilla.
10. Non, aucune modification ou documentation 1776 ne l'exige.
11. Oui, `add_involvement` inventerait une impulsion temporaire non justifiée.
12. Oui, une cible durable devrait provenir d'un territoire, d'une
    revendication, d'une présence, d'un traité, d'un pacte ou d'un sujet.
13. Oui, créer une telle source modifierait l'équilibrage et le gameplay.
14. Oui, la suppression bornée préserve tous les autres effets de l'option.

## 11. Intention 1776 et provenance

Les changelogs complets ne mentionnent aucune adaptation indochinoise ni aucun
besoin d'intérêt régional. Ils ne documentent que des réarrangements globaux
d'intérêts, notamment l'Australie, sans lien avec cet événement.

`git log --follow` ne contient qu'un commit pour le fichier :

```text
b602804 Initial import of 1776 Age of Revolutions fork
```

Le blame attribue le bloc entier à cet import; son blob initial possède déjà le
hash actuel. Aucun commit fonctionnel ultérieur ne fournit une intention.

Les inventaires canoniques marquent le fichier `INTENTIONAL_FORK_DIVERGENCE`,
mais leur preuve est uniquement topologique : fork différent, source égale au
vanilla, `last_fork_commit=b602804`. L'audit amont cité ne mentionne pas
l'Indochine. Cette étiquette ne prouve donc pas une intention sémantique 1776 et
est dépassée pour ce hunk précis par les preuves R3.

Classification de l'éventuelle création future d'une implication indochinoise :
`POST_MERGE_DESIGN_BACKLOG`.

## 12. Classifications et matrice de décision

| Groupe | Classification | Gravité gameplay | Merge | Atomicité | Runtime futur |
| --- | --- | --- | --- | --- | --- |
| garde slots complet | `VANILLA_1_13_ALIGNMENT_REQUIRED` | compatibilité P1, comportement actuel mort | correction requise | un hunk avec l'effet | oui, combiné |
| effet Indochine | `VANILLA_1_13_ALIGNMENT_REQUIRED` | diagnostic P1, aucune exécution actuelle | correction requise | même hunk | oui, combiné |
| ancien intérêt 1776 allégué | `OBSOLETE_HOTFIX_CONTENT` | aucun comportement actuel | à retirer | atomique avec garde | oui, combiné |
| nouvelle implication explicite | `POST_MERGE_DESIGN_BACKLOG` | équilibrage majeur | hors hotfix | non atomique | runtime dédié futur |
| quatre hunks voisins | `UNKNOWN_REQUIRES_REVIEW` | variable selon hunk | hors R3/F3 | non absorbés | séparé |

Les quatorze conditions de sélection passent : objet, hunk, invalidité,
suppression vanilla, indépendance des autres effets, absence de remplacement,
absence d'intention documentée, scopes inchangés, aucune région remappée,
aucune source naturelle créée, hash/diff/rollback calculables et runtime combiné
possible.

## 13. Correction F3 appliquée sur décision de l'opérateur humain

La correction retire les lignes physiques 342 à 348 de la version initiale : les six lignes du
bloc et sa ligne blanche terminale. Elle conserve la ligne blanche précédente,
donc l'espacement entre `add_journal_entry` et `hidden_effect` devient
exactement celui de source/vanilla.

Cette suppression est un choix explicite de l'opérateur humain, pris après
l'audit R3. Elle ne résulte pas d'une équivalence automatique entre l'ancien
intérêt déclaré et une nouvelle source d'implication 1.13.

```text
size = 9494 octets
lines = 509
SHA-256 = 70965044236460BFD2ADE5EDE18A0BEF6DC2E1EEAFB496423E027E80091B28A9
encoding = UTF-8 avec BOM
line endings = LF
final newline = présent
accolades = 137 ouvrantes / 137 fermantes
object indochina.3 = 100 lignes, identique au vanilla
hunks = 1
remaining legacy occurrences = 0
```

Ces métadonnées ont été vérifiées sur le fichier effectivement modifié dans le
worktree.

### Diff appliqué

```diff
@@ -338,14 +338,7 @@ indochina.3 = {
 		add_journal_entry = {
 			type = je_indochina
 		}
-
-		if = {
-			limit = {
-				num_declared_interests < max_num_declared_interests
-			}
-			add_declared_interest = region_indochina
-		}
 
 		hidden_effect = {
 			set_secret_goal = {
```

### Rollback exact documenté

```diff
@@ -338,7 +338,14 @@ indochina.3 = {
 		add_journal_entry = {
 			type = je_indochina
 		}
+
+		if = {
+			limit = {
+				num_declared_interests < max_num_declared_interests
+			}
+			add_declared_interest = region_indochina
+		}
 
 		hidden_effect = {
 			set_secret_goal = {
```

## 14. Runtime futur combiné

R3/F3 ne lance aucun runtime. Après la correction F3, une seule ouverture devra
vérifier ensemble :

- zéro diagnostic égyptien `add_declared_interest`;
- zéro diagnostic indochinois pour le trigger et l'effet;
- chargement du fork et d'une nouvelle partie;
- absence de régression des implications naturelles;
- absence de nouvelle erreur attribuable aux deux hunks.

Le manifeste initial des 60 fichiers de logs est :

```text
2B111126A04FF174C9FAB754E50B814DCC1F0AAEA6C5DCD367622BD1BA643089
```

```text
RUNTIME_DEFERRED_TO_COMBINED_DECLARED_INTEREST_EVENT_QA
```

## 15. Décision humaine et prochaine phase

L'opérateur humain a choisi la suppression exacte prouvée par R3. F3 est
appliquée; la seule phase suivante sélectionnée est le runtime événementiel
combiné :

```text
INDOCHINA_LEGACY_INTEREST_LOGIC_REMOVAL_PROVEN
HUMAN_OPERATOR_DECISION_REMOVE_INDOCHINA_LEGACY_INTEREST_LOGIC
HOTFIX_6A18F3_INDOCHINA_REMOVE_LEGACY_INTEREST_LOGIC_1_13_ALIGNMENT_COMPLETE
NEXT_EXECUTION_PHASE = HOTFIX_6A18Q2_COMBINED_DECLARED_INTEREST_EVENT_RUNTIME_QA
```

Le runtime combiné n'est pas commencé.

## 16. Documents créés ou modifiés

- création du présent rapport;
- mise à jour de `docs/reports/hotfix/INDEX.md`;
- mise à jour de `HOTFIX_REPORT_INDEX.csv`;
- mise à jour de `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- ajout de R3 à `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- enregistrement de F3 et sélection du runtime combiné dans
  `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Ces six fichiers Markdown/CSV constituent toute la mise à jour documentaire.
Le seul autre fichier modifié est la cible gameplay `events/indochina.txt`.

## 17. État Git final

Les contrôles finaux ont confirmé :

- branche, HEAD et message inchangés;
- `events/indochina.txt` au hash final
  `70965044236460BFD2ADE5EDE18A0BEF6DC2E1EEAFB496423E027E80091B28A9`;
- fichier égyptien au hash F2;
- `00_interests.txt` absent;
- un seul gameplay modifié, cinq documents suivis modifiés et le rapport R3
  créé;
- aucune localisation, aucun descripteur, log ou périmètre protégé modifié;
- index staged vide et `git diff --check` PASS;
- huit non-suivis protégés plus le rapport autorisé;
- stash exact et aucun processus du jeu;
- aucun runtime, commit, push ou changement de stash automatique.

```text
branch = hotfix-dlc-audit
HEAD = e6c06c3cfdd90ab91a411d81aa7a4d8acae35613
gameplay deltas = 1
tracked documentation deltas = 5
new authorized report = 1
staged files = 0
git diff --check = PASS
runtime = 0
game processes = 0
```

## 18. Verdicts finaux

```text
HOTFIX_6A18R3_INDOCHINA_LEGACY_INTEREST_LOGIC_1_13_AUDIT_COMPLETE
HOTFIX_6A18F3_INDOCHINA_REMOVE_LEGACY_INTEREST_LOGIC_1_13_ALIGNMENT_COMPLETE
INDOCHINA_LEGACY_GUARD_AND_EFFECT_THREE_WAY_AUDITED
INDOCHINA_1776_DESIGN_INTENT_AUDITED
HUMAN_OPERATOR_DECISION_REMOVE_INDOCHINA_LEGACY_INTEREST_LOGIC
INDOCHINA_LEGACY_INTEREST_LOGIC_REMOVAL_STATIC_PASS
INDOCHINA_LEGACY_GUARD_AND_EFFECT_REMOVED
EGYPTIAN_CRISIS_F2_REMAINS_UNCHANGED
RUNTIME_DEFERRED_TO_COMBINED_DECLARED_INTEREST_EVENT_QA
NO_ADDITIONAL_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
INDOCHINA_LEGACY_INTEREST_LOGIC_REMOVAL_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A18Q2_COMBINED_DECLARED_INTEREST_EVENT_RUNTIME_QA
```
