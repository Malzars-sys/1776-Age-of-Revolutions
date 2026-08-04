# HOTFIX-6A.18F2 — Alignement 1.13 de l'implication dans la crise égyptienne

## 1. Phase, date et résultat

- phase : `HOTFIX_6A18F2_EGYPTIAN_CRISIS_ADD_INVOLVEMENT_1_13_ALIGNMENT`;
- date : 4 août 2026;
- branche : `hotfix-dlc-audit`;
- HEAD initial et final :
  `8878988216c04d1b509e77f39cc8d8e12006123a`;
- message du HEAD : `Retire obsolete declared interest history`;
- gameplay : un seul hunk dans un seul fichier;
- runtime : différé, aucun lancement humain ou automatique;
- commit automatique : aucun.

L'unique effet legacy de `egyptian_crisis_events.4` est remplacé par le bloc
`add_involvement` utilisé par Victoria 3 1.13 dans le même événement, la même
option et le même scope pays. L'Indochine reste byte-identique et l'ancien
historique fixe n'est pas restauré.

## 2. Préflight et état Git initial

Le préflight obligatoire a confirmé :

| Contrôle | Résultat |
| --- | --- |
| racine | fork exact |
| branche | `hotfix-dlc-audit` |
| HEAD | `8878988216c04d1b509e77f39cc8d8e12006123a` |
| message | exact |
| rapport F1 dans le HEAD | présent, douze verdicts présents |
| arbre suivi | propre |
| index staged | vide |
| non suivis | seulement `bject` et sept recherches technologiques protégées |
| `00_interests.txt` dans le HEAD | absent, `git cat-file -e` retourne 128 |
| `git diff --check` | PASS |
| processus Victoria 3 / Dowser / launcher Paradox | aucun |

Stash protégé :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

## 3. Sources lues

Les trois fichiers `events/egyptian_crisis_events.txt` ont été lus
intégralement en lecture seule avant l'écriture :

- fork : `1776_Age_of_Revolutions_fork`;
- source : `1776_Age_of_Revolutions_hotfix_source`;
- vanilla 1.13 : `C:\Games\Victoria 3 The Great Wave\game`.

Le fichier protégé `events/indochina.txt`, le rapport F1, les index autorisés
et les journaux existants ont également été lus. La source, le vanilla et les
journaux n'ont reçu aucune écriture.

## 4. Baseline gameplay et formats

| Arbre/fichier | Octets | Lignes | SHA-256 | Format |
| --- | ---: | ---: | --- | --- |
| fork égyptien initial | 4259 | 193 | `EE2A0881C43A14118E0347001FAA423FABA40080C106883BAD0CC6E5715A3168` | BOM UTF-8, LF, saut final |
| source égyptienne | 4273 | 198 | `FC3C83094B0FFBF873C9DED935F047ACEF4A19F5C8CD7C56C384A47E4C3A36F3` | BOM UTF-8, LF, saut final |
| vanilla 1.13 égyptien | 4296 | 195 | `0D2CBBC708F8BC22EE13ADD4E4BD567EFFF083FFAD9D5C86A568D5E65B455F32` | BOM UTF-8, LF, saut final |
| fork Indochine | 9626 | 516 | `177A6446668E9274260FCA90B0F7B0802280CA7E086CC1290E15C862E845B2BB` | BOM UTF-8, LF, saut final |

Avant correction, le fork contenait exactement deux occurrences actives de
`add_declared_interest` :

1. `events/egyptian_crisis_events.txt:187`;
2. `events/indochina.txt:346`.

## 5. Comparaison trois voies de l'objet `.4`

L'extraction par équilibre des accolades donne :

| Arbre | Objet | Lignes fichier | Lignes objet |
| --- | --- | ---: | ---: |
| fork initial | `egyptian_crisis_events.4` | 155–193 | 39 |
| source | `egyptian_crisis_events.4` | 158–198 | 41 |
| vanilla 1.13 | `egyptian_crisis_events.4` | 155–195 | 41 |

La source et le vanilla ont un objet `.4` identique. Le fork initial n'en
diffère que par un hunk dans l'option `egyptian_crisis_events.4.a` : une ligne
blanche locale et l'effet legacy sont remplacés, côté source/vanilla, par le
bloc de quatre lignes.

### 5.1 Fork vers source

- fichier complet : quatre hunks;
- objet `.4` : un hunk;
- les trois hunks voisins appartiennent uniquement à
  `egyptian_crisis_events.1` : trigger de coup diplomatique, manœuvres et
  probabilités IA, clés de région et ordre tooltip/effet;
- aucun de ces hunks voisins n'est absorbé.

### 5.2 Fork vers vanilla

- fichier complet : trois hunks;
- objet `.4` : un hunk;
- les deux hunks voisins appartiennent uniquement à `.1` et concernent
  `region_arabic` vers `sr:region_arabia` ainsi que l'ordre du tooltip et du
  déclenchement caché;
- ces deux hunks restent inchangés.

### 5.3 Source vers vanilla

- fichier complet : quatre hunks, tous dans `.1`;
- objet `.4` : zéro hunk, identité exacte;
- les différences portent sur le trigger diplomatique, les manœuvres, le
  `default_option` et les probabilités IA.

## 6. Scope, option et effets voisins

Le bloc se trouve dans `egyptian_crisis_events.4`, déclaré comme
`country_event`, dans l'option `egyptian_crisis_events.4.a`. Il n'est entouré
d'aucun changement de scope : l'effet s'exécute donc directement sur le pays
root qui reçoit l'événement, exactement comme dans la source et le vanilla.

L'option conserve avant le bloc :

```text
name = egyptian_crisis_events.4.a
default_option = yes
```

Elle ne contient aucun effet suivant avant sa fermeture. L'option `.4.b`,
également sans effet, suit immédiatement. Le remplacement conserve ainsi la
même option et le même scope pays, avec :

```text
région legacy = region_arabic
région 1.13 = sr:region_near_east
valeur vanilla = 2500
```

## 7. Correction atomique appliquée

Ancien hunk :

```txt
        add_declared_interest = region_arabic
```

Nouveau hunk :

```txt
		add_involvement = {
			strategic_region = sr:region_near_east
			value = 2500
		}
```

Diff gameplay exact :

```diff
@@ -184,7 +184,10 @@ egyptian_crisis_events.4 = {
 		name = egyptian_crisis_events.4.a
         default_option = yes
 
-        add_declared_interest = region_arabic
+		add_involvement = {
+			strategic_region = sr:region_near_east
+			value = 2500
+		}
 	}
```

Il s'agit d'un seul hunk, quatre ajouts et une suppression. Conformément à la
substitution autorisée, la ligne blanche locale préexistante est conservée;
aucune autre ligne du fichier n'est modifiée.

## 8. Fichier final et contrôle syntaxique

```text
path = events/egyptian_crisis_events.txt
size = 4297 octets
lines = 196
SHA-256 = E637C1F8EF27BBEBCB43C516EB5F0E6C943ECC7A51FC1A06FCD73999547489F7
encoding = UTF-8 avec BOM
line endings = 196 LF, 0 CRLF
final newline = présent
```

Le fichier contient 55 accolades ouvrantes et 55 fermantes. L'objet `.4`
s'étend désormais des lignes 155 à 196, revient à une profondeur finale nulle
et reste équilibré. L'indentation du nouveau bloc reproduit la source et le
vanilla.

Les deux usages de `region_arabic` dans les triggers de `.1`, lignes 82 et 104,
restent inchangés. Le remplacement n'a donc touché aucune autre occurrence.

## 9. Validation statique

Après correction :

- zéro `add_declared_interest` dans le fichier égyptien;
- exactement un `add_involvement` dans `.4.a`;
- exactement un `strategic_region = sr:region_near_east`;
- exactement un `value = 2500` associé au bloc;
- une seule occurrence active de `add_declared_interest` dans tout le fork;
- cette occurrence est uniquement `events/indochina.txt:346`;
- `common/history/interests/00_interests.txt` reste absent;
- le diff gameplay comporte exactement un fichier et un hunk;
- `git diff --check` passe et l'index staged reste vide.

```text
EGYPTIAN_CRISIS_ADD_INVOLVEMENT_1_13_STATIC_PASS
EGYPTIAN_CRISIS_LEGACY_EFFECT_REMOVED
EGYPTIAN_CRISIS_VANILLA_1_13_EVENT_SEMANTICS_ALIGNED
INDOCHINA_LEGACY_INTEREST_LOGIC_UNCHANGED
```

## 10. Indochine protégée

Le hash d'`events/indochina.txt` reste :

```text
177A6446668E9274260FCA90B0F7B0802280CA7E086CC1290E15C862E845B2BB
```

Son garde et son effet restent inchangés :

```txt
num_declared_interests < max_num_declared_interests
add_declared_interest = region_indochina
```

Vanilla 1.13 supprime les deux sans ajouter `add_involvement`. Cette divergence
1776 exige donc un audit séparé et n'est pas résolue dans F2.

## 11. Runtime différé

Aucun runtime n'est exécuté ou demandé dans F2. Les journaux existants restent
strictement en lecture seule. Avant écriture, les 60 fichiers du dossier de
journaux formaient le manifeste SHA-256 :

```text
2B111126A04FF174C9FAB754E50B814DCC1F0AAEA6C5DCD367622BD1BA643089
```

Le runtime sera regroupé avec la future résolution de l'Indochine afin de
vérifier en une seule ouverture que les deux diagnostics événementiels passent
ensemble de deux à zéro.

```text
RUNTIME_DEFERRED_TO_COMBINED_DECLARED_INTEREST_EVENT_QA
```

## 12. Prochaine phase

La seule phase suivante sélectionnée est :

```text
NEXT_EXECUTION_PHASE = HOTFIX_6A18R3_INDOCHINA_LEGACY_INTEREST_LOGIC_1_13_AUDIT
```

R3 et le runtime combiné ne sont pas commencés dans F2.

## 13. Documents créés ou modifiés

- création du présent rapport;
- mise à jour de `docs/reports/hotfix/INDEX.md`;
- mise à jour de `HOTFIX_REPORT_INDEX.csv`;
- mise à jour de `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- ajout de F2 à `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- sélection de R3 dans `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun autre document n'est créé ou modifié.

## 14. État Git final et protections

Les contrôles finaux ont confirmé :

- branche et HEAD inchangés;
- seul `events/egyptian_crisis_events.txt` modifié côté gameplay;
- seulement les cinq documents autorisés modifiés et le présent rapport créé;
- staged vide et `git diff --check` PASS;
- huit non-suivis protégés plus le rapport autorisé;
- `00_interests.txt` toujours absent;
- Indochine, BIC, NAVY, ADMIN, localisations et descripteurs inchangés;
- aucun diff contenant `law_colonial_exploitation`;
- loi BIC `law_frontier_colonization` conservée;
- manifeste des journaux inchangé;
- stash exact et aucun processus du jeu;
- aucun runtime, commit, push ou changement de stash automatique.

```text
branch = hotfix-dlc-audit
HEAD = 8878988216c04d1b509e77f39cc8d8e12006123a
gameplay deltas = 1 file, 1 hunk, +4/-1
tracked documentation deltas = 5
new authorized report = 1
staged files = 0
git diff --check = PASS
runtime = 0
game processes = 0
```

## 15. Verdicts finaux

```text
HOTFIX_6A18F2_EGYPTIAN_CRISIS_ADD_INVOLVEMENT_1_13_ALIGNMENT_COMPLETE
EGYPTIAN_CRISIS_ADD_INVOLVEMENT_1_13_STATIC_PASS
EGYPTIAN_CRISIS_LEGACY_EFFECT_REMOVED
EGYPTIAN_CRISIS_VANILLA_1_13_EVENT_SEMANTICS_ALIGNED
INDOCHINA_LEGACY_INTEREST_LOGIC_UNCHANGED
RUNTIME_DEFERRED_TO_COMBINED_DECLARED_INTEREST_EVENT_QA
NO_ADDITIONAL_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A18R3_INDOCHINA_LEGACY_INTEREST_LOGIC_1_13_AUDIT
```
