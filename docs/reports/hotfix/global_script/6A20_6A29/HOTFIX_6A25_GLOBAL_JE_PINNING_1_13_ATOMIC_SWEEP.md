# HOTFIX-6A.25 — Sweep atomique global des pinning de journal entries pour Victoria 3 1.13

Date : 9 août 2026
Branche : `hotfix-dlc-audit`
HEAD d'entrée : `e4c6583baf20ab9ef8062c26556814a04f96de59` — `Audit German unification journal entry pinning for 1.13`
Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé
Lancements Victoria 3 : **0**

## 1. Décision opérateur et périmètre

La correction fichier par fichier sélectionnée par 6A.24 est remplacée avant
toute exécution par une migration statique consolidée :

```text
OPERATOR_ARCHITECTURE_DECISION =
SUPERSEDE_UNEXECUTED_6A24F_WITH_GLOBAL_JE_PINNING_ATOMIC_SWEEP

SUPERSEDED_EXECUTION_PHASE =
HOTFIX_6A24F_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT

NEW_EXECUTION_PHASE =
HOTFIX_6A25_GLOBAL_JE_PINNING_1_13_ATOMIC_SWEEP
```

Le rapport 6A.24 reste une preuve historique inchangée. Ce sweep porte
exclusivement sur le nom exact `should_be_pinned_by_default` et sa forme 1.13
`should_be_pinned_by_default_uninvolved_or_context`. Aucune autre API, valeur,
structure, condition ou donnée de gameplay n'est modifiée.

## 2. Préflight

Le dépôt, la branche, le HEAD et le message attendus ont été confirmés. L'arbre
suivi et l'index étaient vides, `git diff --check` était propre, les huit
non-suivis protégés étaient seuls présents et aucun processus Victoria 3,
Dowser ou launcher Paradox n'était actif. Le stash supérieur est resté :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Les non-suivis de recherche technologique et `bject` n'ont été ni ouverts ni
touchés.

## 3. Inventaire global recalculé

Le scan porte sur les fichiers `.txt` suivis par Git, avec un parseur de blocs
qui ignore commentaires et chaînes. Chaque propriété a été rattachée à son
objet racine, à ses bornes et à sa profondeur structurelle. L'inventaire
exhaustif par occurrence se trouve dans
`HOTFIX_6A25_GLOBAL_JE_PINNING_INVENTORY.csv`.

| Mesure avant correction | Total |
|---|---:|
| anciennes propriétés exactes | 370 |
| fichiers portant une ancienne propriété | 137 |
| propriétés déjà modernes | 29 |
| fichiers déjà modernes | 17 |
| fichiers distincts dans la famille | 154 |
| lectures littérales de l'ancien nom hors déclarations | 0 |

Les cinq propriétés distinctes
`should_be_pinned_by_default_involved` restent hors périmètre et sont
byte-identiques.

## 4. Preuve globale de l'API vanilla 1.13

Le recalcul de `game/common/journal_entries` reproduit exactement la baseline
6A.24 :

```text
modern occurrences = 394
modern files = 157
modern yes = 378
modern no = 16
modern structural depth = 1
legacy exact occurrences = 0
```

La migration B est donc une migration d'API globale démontrée par la vanilla
1.13 ; elle ne constitue pas un import de gameplay vanilla.

## 5. Diagnostics historiques réconciliés

Les fichiers de logs actuellement présents ont été renouvelés après 6A.22Q et
ne sont pas utilisés comme nouvelle baseline. Les identités historiques ont
été reconstruites depuis la liste exhaustive engagée de 6A.10 : 378 identités,
moins les 9 pinning déjà corrigés dans Roumanie, colonialisme portugais, Coup,
Pologne et Afghanistan, soit 369 identités fraîches encore pertinentes avant
6A.25.

Le scan statique en trouve 370. L'unique différence est
`common/journal_entries/07_poland_lithuania_mod.txt:604`, objet
`je_plc_reform_great_power`. Cette propriété se situe après l'erreur de parsing
antérieure de la ligne 594 ; elle était donc masquée dans les diagnostics
runtime, sans être absente du fichier. Cette explication réconcilie exactement
les deux comptes.

## 6. Classification atomique et dry-run

| Classe | Définition | Occurrences | Traitement |
|---|---|---:|---|
| A | `DIRECT_THREE_WAY_ATOMIC` | 338 | corrigées |
| B | `GLOBAL_API_MIGRATION_ATOMIC_CUSTOM_OBJECT` | 18 | corrigées |
| C | `ALREADY_MODERN` | 29 | inchangées |
| D | `PINNING_ATOMICITY_EXCEPTION` | 14 | inchangées |

Les classes A et B totalisent 356 substitutions dans 129 fichiers et 344
objets. Le dry-run a calculé chaque sortie en mémoire, son SHA-256 théorique et
son numstat, puis a inversé les substitutions. Tous les fichiers ont restitué
exactement leurs octets d'entrée. Les 356 substitutions représentent 356
hunks d'une ligne et un diff global exact de `356+/356-`.

### PINNING_SWEEP_EXCEPTIONS

| Chemin:ligne | Objet | Valeur fork | R?f?rence moderne | Cat?gorie | Bloqueur exact | Statut merge |
|---|---|---:|---|---|---|---|
| `common/journal_entries/00_autocracy.txt:210` | `je_king_in_parliament` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/00_battle_for_india_mod.txt:80` | `je_battle_for_india_goal` | `yes` | source=absente; vanilla=absente | `PROTECTED_WORK` | PROTECTED_WORK_BIC: absolute operator protection forbids gameplay changes without an explicit human decision | `UNREGISTERED` |
| `common/journal_entries/00_canals.txt:52` | `je_suez_survey` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/00_canals.txt:146` | `je_panama_survey` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/00_corn_laws.txt:80` | `je_corn_laws` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/00_prohibition_laws.txt:120` | `je_prohibition` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/00_skyscraper.txt:62` | `je_skyscraper_site` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/00_skyscraper.txt:99` | `je_skyscraper_construction` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/01_paris_commune.txt:70` | `je_the_paris_commune_display` | `no` | source=yes; vanilla=yes | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `no` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/02_peru_bolivia.txt:355` | `je_peru_bolivia` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/03_korea.txt:186` | `je_korean_rebellion` | `yes` | source=no; vanilla=yes | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| `common/journal_entries/05_grunderzeit.txt:19` | `je_grunderzeit` | `yes` | source=no; vanilla=no | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `yes` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/05_montenegro_je.txt:662` | `je_mon_serb_unity` | `no` | source=yes; vanilla=yes | `UNKNOWN_SEMANTIC_REPLACEMENT` | bool?en fork `no` contradictoire avec la r?f?rence moderne | `INTENTIONAL_FORK_DIVERGENCE` |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt:50` | `je_hindustan_is_durrani` | `yes` | source=absente; vanilla=absente | `PROTECTED_WORK` | PROTECTED_WORK_BIC: protected concurrent Durrani/Battle-for-India work requires an explicit human decision | `PROTECTED_CONCURRENT_WORK` |

Douze exceptions sont `UNKNOWN_SEMANTIC_REPLACEMENT` : la valeur booléenne du
fork contredit au moins une référence moderne et les critères A/B interdisent
de décider automatiquement entre conservation et transformation de la
valeur. Deux exceptions sont `PROTECTED_WORK` dans la chaîne BIC/Battle for
India ; aucune modification n'y est autorisée sans décision humaine explicite.
Les 14 occurrences D occupent 12 fichiers, dont quatre portent aussi une
occurrence A corrigée. Aucune exception n'est motivée par la seule présence
d'une autre API invalide.

## 7. Application batch et preuve byte-level

Pour chaque occurrence A/B, seuls les octets du nom de propriété ont été
remplacés. Indentation, espaces, valeur, commentaire, BOM, fins de ligne,
position et tous les octets adjacents sont inchangés. Les hashes réels après
écriture correspondent aux 129 hashes théoriques ; l'inversion de chacun
restitue son hash d'entrée.

Le cas allemand est inclus dans ce batch et atteint exactement :

```text
SHA-256 = 30A3F3356AA43060C0E8D315DDF34D8D304680290134E0212AE6AEB852C8F239
legacy = 0
modern = 5
diff = 5+/5-
octets = 9527
lignes = 448 LF
BOM = preserved
```

Afghanistan et Pologne sont restés byte-identiques aux hashes fermés :

```text
Afghanistan = C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13
Pologne     = A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A
```

## 8. Résultat statique global

```text
LEGACY_PINNING_OCCURRENCES_BEFORE = 370
LEGACY_PINNING_OCCURRENCES_CORRECTED = 356
LEGACY_PINNING_OCCURRENCES_EXCEPTIONS = 14
LEGACY_PINNING_OCCURRENCES_AFTER = 14

TARGET_RUNTIME_PINNING_DIAGNOSTICS_BEFORE = 355
EXPECTED_TARGET_RUNTIME_PINNING_DIAGNOSTICS_AFTER = 0
```

Le total runtime ciblé est 355, et non 356, car la propriété statique PLC de
la ligne 604 était masquée dans les logs historiques. Les 14 diagnostics des
exceptions ne font pas partie de la cohorte corrigée et peuvent donc subsister.
Aucune disparition runtime n'est revendiquée pendant cette phase statique.

## 9. Matrice fichier par fichier

La colonne `runtime attendu` exprime le nombre de diagnostics historiques
susceptibles de rester dans le fichier à cause des seules exceptions D ; il ne
s'agit pas d'une mesure exécutée en 6A.25.

| Chemin | Objets corrig?s | ancien avant | moderne avant | A | B | D | frais historique | corrig? | ancien apr?s | runtime attendu | octets avant?apr?s | SHA-256 avant | SHA-256 apr?s th?orique/r?el | lignes | BOM | LF | numstat | inversion |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---|---:|---:|---|
| `common/journal_entries/00_acw_entries.txt` | `je_acw_countdown`, `je_acw_equality`, `je_acw_reconstruction`, `je_acw_reincorporate`, `je_acw_war`, `je_acw_wild_wild_west` | 6 | 0 | 6 | 0 | 0 | 6 | 6 | 0 | 0 | 7770?7902 | `AD7269B774B5AD6C952FCD7597E79D1CE91D6E0A7F016A117016CBF86ECCECDB` | `ABC6CB296275C1DC44A1AA7E82DD2F586D9C095C840E39C29EA36CDC2C33FA03` | 448 | oui | 448 | `6	6` | `PASS` |
| `common/journal_entries/00_alaska.txt` | `je_alaska`, `je_sale_of_alaska` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 3726?3770 | `4FF2D43DD4572DB4410C545A32D941AF15B81DCE3A12A8B8B15F1A40A55D86EC` | `D1CE30A655BC83F994B3065C4C723F92A64949699017276053538710F63343C2` | 211 | oui | 211 | `2	2` | `PASS` |
| `common/journal_entries/00_antarctica.txt` | `je_antarctica` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2582?2604 | `F92FF24A3CFC6BD2301FFFC47E9427563CF43B9890F12C4C69CE5BF030932D15` | `70B56EADAD987C768C02F61187A935F1D0DFAB84A03052A82FA53AB93AC3CD90` | 123 | oui | 123 | `1	1` | `PASS` |
| `common/journal_entries/00_autocracy.txt` | ? | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 3608?3608 | `20C988F78A1F687626582390471E8DA921C18070A2E9EA5E5E7CFAFA7DCEB403` | `20C988F78A1F687626582390471E8DA921C18070A2E9EA5E5E7CFAFA7DCEB403` | 213 | oui | 213 | `0	0` | `PASS` |
| `common/journal_entries/00_battle_for_india_mod.txt` | ? | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1964?1964 | `0ECAA092E7B2ACE0FAC8CE2BB0DE8BDE58DC6F72434A926AE5B59675396369B9` | `0ECAA092E7B2ACE0FAC8CE2BB0DE8BDE58DC6F72434A926AE5B59675396369B9` | 83 | oui | 82 | `0	0` | `PASS` |
| `common/journal_entries/00_boxer_rebellion.txt` | `je_boxer_rebellion` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1322?1344 | `DE1A14A85AF3AD20B8679A8D4B5BA43E15BB564C29E674832328B72ACDEB3790` | `D8653E4857E7C40CDC125655D7759CBAF4DE04242187D8EA023338E171BE2679` | 50 | oui | 50 | `1	1` | `PASS` |
| `common/journal_entries/00_canada_australia.txt` | `je_australia_aus`, `je_australia_gbr`, `je_canada_can`, `je_canada_gbr` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 5762?5850 | `9A7C977630272510223ADEB52DB32FDE8E32FEA2DDEC08256B726CA9995A67B9` | `523B1E01F3C90D18D67B6046015D300CEAC28CD4F6314D57F2BDFAB10425EFAE` | 260 | oui | 260 | `4	4` | `PASS` |
| `common/journal_entries/00_canals.txt` | `je_panama_canal`, `je_suez_canal` | 4 | 0 | 2 | 0 | 2 | 4 | 2 | 2 | 2 | 3351?3395 | `6D45A61952DE69EB48124A1598E5E752D1DB5DDADF78F02BCA21DF5691BC82F4` | `77E0AC11DFE9030CA5897317D9B29FC4AAE4783C8EB68B131F977E70FAF6D5AA` | 187 | oui | 187 | `2	2` | `PASS` |
| `common/journal_entries/00_central_africa.txt` | `je_central_africa_expedition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3694?3716 | `E2A9B8E6011BEC6B510165FBE46432DDD76F0B1AC7DE2ED61A6CF685B96DA489` | `9EB2F2022E7149FF18AEF52E6AC58B3434551149C1FDF674F2688716FEE23329` | 143 | oui | 143 | `1	1` | `PASS` |
| `common/journal_entries/00_central_and_south_america.txt` | `central_america_falls_apart`, `je_reunify_central_america`, `ragamuffin_war`, `ragamuffin_war_minors` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 3374?3462 | `AE679E6B8CCC04086AEB617FA75DECC4B6697C6243A84E5468C5A03C135A4DED` | `91A37EB50C16DEFF82CDFB75F4E83C13A3AD80B2317D5B5ADFE311992AEFF6D5` | 213 | oui | 213 | `4	4` | `PASS` |
| `common/journal_entries/00_communism.txt` | `je_communism_1` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 6233?6255 | `E65BE84E103FD2FC1C1435A84D39B8F94BE3E4EFAB25AC0FF16B277994DB89F1` | `0089230769D47D3AA2EF89394C408262F09861CEE499C8954804FE812824D640` | 326 | oui | 326 | `1	1` | `PASS` |
| `common/journal_entries/00_congo.txt` | `je_congo_expedition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 4013?4035 | `59373E154DEBF416AE61B6A9E115A3E87D29D5FC022D6E1223E3EA6BFFC8A3D6` | `0525DCFA5F710437E7D263D3786B7B004869C94E32E75577FBDB1C6BA041262F` | 151 | oui | 151 | `1	1` | `PASS` |
| `common/journal_entries/00_congo_free_state.txt` | `je_free_state` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3463?3485 | `B80AB687B2D349BBAA8A28A19C9EE8F2B8D6920A7838E69207D2CE5888203CD8` | `37CD79C35A2D637CB690E543B805C76FE8C4E0574292F4A04F90401DF4D60E98` | 174 | oui | 174 | `1	1` | `PASS` |
| `common/journal_entries/00_corn_laws.txt` | ? | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1474?1474 | `CD95FDEC7B13C30057B4EB1226CF07435D5971C242DE94F33DD77875962A077D` | `CD95FDEC7B13C30057B4EB1226CF07435D5971C242DE94F33DD77875962A077D` | 81 | oui | 81 | `0	0` | `PASS` |
| `common/journal_entries/00_east_indies.txt` | `je_consolidate_colonial_rule` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3853?3875 | `3E33450D38B078523B9F7718FBD6DF0B1896D4A12FB1A62DCA7E0AA936ACD8A6` | `5AE3089A731B5C956B7E6BB95C38853A12867DFF1E7854AB53C057497C9EE35F` | 203 | oui | 203 | `1	1` | `PASS` |
| `common/journal_entries/00_establish_colonial_administration.txt` | `je_colonial_administration` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2446?2468 | `73DFD48B924F9B723E9BA2B87724316BEB7666942113BA8016F94ABB595B06B7` | `417673AD11B4D3BCA4122DE198484B53BEDE2E9E632B1903F9247B09A610F3ED` | 86 | oui | 86 | `1	1` | `PASS` |
| `common/journal_entries/00_ethiopia.txt` | `je_age_of_princes` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 597?619 | `F2608E8A3A45BF4567E1407D1876FD4B2FEE700FEE9513A15EBBA50E5A2139A7` | `BFDC6CE879B3F36118B076AA88B99078B0C0913DD59E66DCBCF0589D0C9806E2` | 39 | oui | 39 | `1	1` | `PASS` |
| `common/journal_entries/00_fascism.txt` | `je_fascism_1`, `je_fascism_2`, `je_modernization_program` | 3 | 0 | 3 | 0 | 0 | 3 | 3 | 0 | 0 | 10914?10980 | `D8CDF76AC8F9FB43190BD8581B46DC04A5118D05F08585AE77F671C6A9870D79` | `615F87C4A0267D74275963F01EE71EB9DA7F9485AA5D18FAD1297816167DA754` | 561 | oui | 561 | `3	3` | `PASS` |
| `common/journal_entries/00_german_unification.txt` | `je_german_unification`, `je_german_unification_idea`, `je_north_german_unification`, `je_schleswig_holstein_question`, `je_south_german_unification` | 5 | 0 | 5 | 0 | 0 | 5 | 5 | 0 | 0 | 9417?9527 | `A52D4525DED1BE8F804CEEDD99329E03EAABB9E53376D04F4BBE9A8CDC32EC22` | `30A3F3356AA43060C0E8D315DDF34D8D304680290134E0212AE6AEB852C8F239` | 448 | oui | 448 | `5	5` | `PASS` |
| `common/journal_entries/00_grand_exhibition.txt` | `je_grand_exhibition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2884?2906 | `CCD6BB6039F7F87BB157BC14D4179AA84B5CB70AE818576846128C0076BA6D4D` | `270AD440AA9BED24AB928BCAD15C41B7025F546A8C12C29714EEB6268583A452` | 154 | oui | 154 | `1	1` | `PASS` |
| `common/journal_entries/00_greek_nationalism.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5956?5956 | `1938E6AB97C9F85424961BD35675D474CB7F65F0CFD74EB9879ADF66DCE80B50` | `1938E6AB97C9F85424961BD35675D474CB7F65F0CFD74EB9879ADF66DCE80B50` | 251 | oui | 251 | `0/0` | `N/A` |
| `common/journal_entries/00_hawaii.txt` | `je_hawaii`, `je_hawaiian_interest` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 2452?2496 | `C5D702F764BF3B92A959A43DCA96BB8140F1BFE0F0B75A401A34FBA05203CA18` | `8864B51247A3381677FEAC3B34BF87DD631A534B9FBC91A97AC7B6E86DB7D4BA` | 138 | oui | 138 | `2	2` | `PASS` |
| `common/journal_entries/00_ig_agendas.txt` | `je_government_petition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 8683?8705 | `F28DB01616ED28379678F48205684447CC0607CF116CB90A726A3C08D03FF11D` | `DD8D9563B68CF78B0B4FE895858A732FE7BA3F28D64DAE90ED405ECCEE135C71` | 287 | oui | 287 | `1	1` | `PASS` |
| `common/journal_entries/00_impose_law.txt` | `je_law_imposition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2482?2504 | `E59ED8C00D280DE7A81A952408A848F661ABDAF218F311F3AB21DFED556971B0` | `A5ADF8191149AA332CB65D818AADE2228349ED1B7D10D4E5D057FE748BD407F1` | 104 | oui | 104 | `1	1` | `PASS` |
| `common/journal_entries/00_indian_removal.txt` | `je_indian_removal` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1416?1438 | `30B19421B0D3ACBD1BACA956029D8E0A02929CF57DAD0335BDB5A01D89E35EB8` | `7721EC92A61552D9632728EBD34AD0D6D17894ECF603C762CDF22D74785C07A4` | 73 | oui | 73 | `1	1` | `PASS` |
| `common/journal_entries/00_italian_unification.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2448?2448 | `2FB4CE01C9529B89EFAB126D6912D15181720DB34322C4B7F1EC868426132D87` | `2FB4CE01C9529B89EFAB126D6912D15181720DB34322C4B7F1EC868426132D87` | 134 | oui | 134 | `0/0` | `N/A` |
| `common/journal_entries/00_krakatoa.txt` | `je_krakatoa` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1807?1829 | `230FD1223AC5CD6F266C6642160B6966047833C6CD2BE41F22D7BE35E55FA65E` | `053C5ED7BA6A5C44005F900749F8D72A78B420D8E4CF850224A04383A8A33550` | 106 | oui | 106 | `1	1` | `PASS` |
| `common/journal_entries/00_land_reclamation.txt` | `je_land_reclamation` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1397?1419 | `7AABE7E4D9B3844D360DDDEF05F5FCA4E377799307043AF925CDDBBA9FECEFFC` | `40B2BC46FD1A522F7D617995238B3A883750845F41292DB2BE06547A3B6C51BD` | 77 | oui | 77 | `1	1` | `PASS` |
| `common/journal_entries/00_manifest_destiny.txt` | `je_manifest_destiny_frontier_wars`, `je_manifest_destiny_mexico` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 1336?1380 | `F8B1DE5D57CD4AEAB140D09A30E356207262160EC4E81DC1DF8E6698FA4ED19A` | `44D882A983404270008832841A6381EB3E36E7E070C005DFEE6A68D7A238A9B6` | 55 | oui | 55 | `2	2` | `PASS` |
| `common/journal_entries/00_meiji_restoration.txt` | `je_meiji_army`, `je_meiji_diplomacy`, `je_meiji_economy`, `je_meiji_main`, `je_meiji_restoration`, `je_terakoya` | 6 | 0 | 5 | 1 | 0 | 6 | 6 | 0 | 0 | 6177?6309 | `354A5EDE127171278F6FFD6CC4D64A4E4665334883E35201666973C32CB66977` | `4066221939FFE27A222A0BCE6DADA9FA20E701028C8795FE88C3B40F6EE59EFE` | 348 | oui | 348 | `6	6` | `PASS` |
| `common/journal_entries/00_negotiation_quests_je.txt` | `je_government_petition_negotiation_version`, `je_government_petition_negotiation_version_b`, `je_negotiate_army_quest`, `je_negotiate_building_group`, `je_negotiate_buildings`, `je_negotiate_sol`, `je_negotiate_taxes` | 7 | 0 | 7 | 0 | 0 | 7 | 7 | 0 | 0 | 21264?21418 | `FABE7156A215D65AE8BBA1E06C922468508D644192C31FC07A67DFBEAA566A04` | `1F4190BC1AC0CEDDB23A8A877058CE3201086F357563DB89A2CD379ADCED3641` | 826 | oui | 826 | `7	7` | `PASS` |
| `common/journal_entries/00_niger_river.txt` | `je_niger_river_expedition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3696?3718 | `54A2C56CDC0F077D7825BFE05486EE6DA36BAB3C0C54C6CD784826D8D0303503` | `99583D938E13615C8A31BB4F1B6FBA31D62203F9D3A428B108D2109C9D3870DA` | 142 | oui | 142 | `1	1` | `PASS` |
| `common/journal_entries/00_opium_wars.txt` | `je_opium_obsession`, `je_opium_wars` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 3214?3258 | `6C1CFFB4D67619F2A8EDBE4EEB6B2440650566CD85E6FA9BAAB18EE3818960EC` | `167CD0056ABDAC54EB10EDE02C587DAC8CCDA6DC5EB716B54DD31B5EF00D2DC0` | 194 | oui | 194 | `2	2` | `PASS` |
| `common/journal_entries/00_patagonia.txt` | `je_patagonia` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1483?1505 | `93CFC705F94FEA24EF62A0A9946E3632EEDF2676E7418151C40DB6A9EE0913EF` | `1F5CB73B9DE8738BD58CD4E9C6B925F2CE3B53FC210466C3C999B75007A9CF24` | 83 | oui | 83 | `1	1` | `PASS` |
| `common/journal_entries/00_peoples_springtime_je.txt` | `je_red_summer`, `je_springtime_of_the_peoples` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 10550?10594 | `F4CDC7255EF7516AE76B3462100E7F5CC3841358D90985D8DFEB3E3DD40529A3` | `9B3B89C35D0455E46188C648A434D108B2223E0C5EC2BAC20974F4DBEBBC7656` | 482 | oui | 482 | `2	2` | `PASS` |
| `common/journal_entries/00_plague.txt` | `je_spanish_flu` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2228?2250 | `4073E17AFC1DE6CD56B8411C1685515B2D78028B5666E80A54FBE0231A1055DD` | `967C55E4AF3EAB7612391FDC556BF98293B6F49E5C0612540E0CC89A3C3DF488` | 133 | oui | 133 | `1	1` | `PASS` |
| `common/journal_entries/00_player_objectives_economic_dominance.txt` | `je_expanding_the_market`, `je_exporting_profits`, `je_lower_production_costs`, `je_objective_expand_goods_production`, `je_raise_exports_value`, `je_refining_goods`, `je_specialized_goods`, `je_specialized_inputs`, `je_strong_market`, `je_utilizing_our_strength` | 10 | 0 | 10 | 0 | 0 | 10 | 10 | 0 | 0 | 6014?6234 | `2FBEEDFC3FEA9864DED16879ECE33578B99E3B158E1BB8A52E0EB21EECD74976` | `75228F0BCBB72EABCB0A2BB13E3E623158D3254D62544AB120DE0A6A10449927` | 346 | oui | 346 | `10	10` | `PASS` |
| `common/journal_entries/00_player_objectives_egalitarian_society.txt` | `je_egalitarian_society`, `je_liberate_the_slaves`, `je_objective_encourage_liberal_ideas`, `je_pass_laws`, `je_public_services`, `je_women_and_children` | 6 | 0 | 6 | 0 | 0 | 6 | 6 | 0 | 0 | 4777?4909 | `6DD06E14C9C7035B9A71B6024E6C5A304728EEEFF6DEE9216C4B85EAC6659F5E` | `752C04043124F2FCEC37028D3520E1B2C8AEB140AF4889E613CD0CF4C4FE129A` | 207 | oui | 207 | `6	6` | `PASS` |
| `common/journal_entries/00_player_objectives_great_game.txt` | `je_achieve_sovereignty`, `je_acquire_korean_protectorate`, `je_chinese_concessions`, `je_codify_chinese_border`, `je_consolidate_afghanistan_objective`, `je_consolidate_british_india`, `je_consolidate_central_asia`, `je_consolidate_persia`, `je_counter_russian_pacific_influence`, `je_disrupt_russian_caucasus`, `je_great_game_control`, `je_maintain_afghan_protectorate`, `je_pacify_kazakh_steppes`, `je_pamir_expedition_objective`, `je_secure_influence_over_persia`, `je_secure_persian_border`, `je_unify_afghanistan_objective` | 17 | 0 | 17 | 0 | 0 | 17 | 17 | 0 | 0 | 35605?35979 | `0353354E1DC9925EA37BED22930738E2D6AF649EAAE8C47323ED3AB3ABE25677` | `72937E24C93FA2771B0843432B5F8894CC4E66A588AB134A99EDFD5F44853A89` | 1847 | oui | 1847 | `17	17` | `PASS` |
| `common/journal_entries/00_player_objectives_hegemon.txt` | `je_african_colonies`, `je_colonization_laws`, `je_expand_navy_and_army`, `je_form_alliance`, `je_great_power`, `je_greater_power`, `je_greatest_power`, `je_increase_technology`, `je_take_subject`, `je_the_hegemon`, `je_unrecognized_power` | 11 | 0 | 11 | 0 | 0 | 11 | 11 | 0 | 0 | 4441?4683 | `610DF305BFC1F76C654E024C11EDC4A7050A4D1F37394576DD13D71072530566` | `6531EE0667FF504184951B25B5E879669CDF6033173C76E7406F2ABDC3026B5B` | 266 | oui | 266 | `11	11` | `PASS` |
| `common/journal_entries/00_poland.txt` | ? | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3016?3016 | `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` | `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` | 132 | oui | 132 | `0/0` | `N/A` |
| `common/journal_entries/00_prohibition_laws.txt` | ? | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 2183?2183 | `42E51BEBA8A66C3CDAA46EC93EC55555152B1B2FD9B8A4CCF4DD6668CB3D9531` | `42E51BEBA8A66C3CDAA46EC93EC55555152B1B2FD9B8A4CCF4DD6668CB3D9531` | 121 | oui | 121 | `0	0` | `PASS` |
| `common/journal_entries/00_red_scare.txt` | `je_the_red_scare` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2362?2384 | `7531EDFB51621B5A9AF7DDAC312C329AF2DB0BF0F96BDA546B0C4B28B3DE3B1C` | `87EADC16E6FB6ECA0C2F954CE1DBDBAD07955A0727B56F5B078A75C01493F0CE` | 88 | oui | 88 | `1	1` | `PASS` |
| `common/journal_entries/00_request_recognition.txt` | `je_earn_recognition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1451?1473 | `4633C26CABD8774865837C67258E4E6466F9149E2EA7C42B55A6E23F36AC8BE8` | `7309FBC8315F20DDDBE804F58CF94AE91A63E9D62B9DDD45AD6910FA67E0045B` | 70 | oui | 70 | `1	1` | `PASS` |
| `common/journal_entries/00_reunify_china.txt` | `je_reunify_china` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2910?2932 | `573B2B156C6C277EA02E2F4D9E1D5B545F8EBEB095DFC9C846E4FAE069047D8B` | `CEE69EDBC8BD4FE9575D385B4393124AC6602F91C1F320050F237F0131FED377` | 133 | oui | 133 | `1	1` | `PASS` |
| `common/journal_entries/00_romania.txt` | ? | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3901?3901 | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` | 150 | oui | 150 | `0/0` | `N/A` |
| `common/journal_entries/00_scramble_for_africa.txt` | `je_scramble_for_africa` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3804?3826 | `4A2291026B00879225FE9332047E194504166C3E8BB2019B7162A61DD5979D5C` | `8C441B825BDEB11EC25D0814917CA3293599893B0BC84869F57DD18E5796951C` | 194 | oui | 194 | `1	1` | `PASS` |
| `common/journal_entries/00_seminole_wars.txt` | `je_seminole_wars` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1481?1503 | `E70B33E961CAB35CC9A4B49DA4BD44B6B748F3A230DF5B291FA509444C67B7F1` | `ABFEBCA9EABC4BFAE0BB6E76AA9452647BEBC3057D351910E9D31309E84B9C07` | 85 | oui | 85 | `1	1` | `PASS` |
| `common/journal_entries/00_sick_man.txt` | ? | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8879?8879 | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | 501 | oui | 501 | `0/0` | `N/A` |
| `common/journal_entries/00_skyscraper.txt` | ? | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 2 | 2 | 1633?1633 | `6448083CDCBD77C4AA9D2D8E0FE0E51E87730A277E930DBF08E41643D68289E5` | `6448083CDCBD77C4AA9D2D8E0FE0E51E87730A277E930DBF08E41643D68289E5` | 100 | oui | 100 | `0	0` | `PASS` |
| `common/journal_entries/00_standard_of_living.txt` | `je_sol_1` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1732?1754 | `37D2A06A5969D756551E38B7A8DB632221063063C248CB28B71D3C0513AEEFFB` | `76F931B1DF74300C9CC9703EAE609CAAF4F90AC30BCC81AB0D997578536C530B` | 97 | oui | 97 | `1	1` | `PASS` |
| `common/journal_entries/00_strike_je.txt` | `je_strike` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2738?2760 | `D204DF6C6E15CE86C4D9070870BE89A8BC03480F6F314C80B2F41369C590DB94` | `0E793CD4F05F739593AC56FD87DC19CBAE52915BC3A871E9683EBB8A79BDD3E4` | 157 | oui | 157 | `1	1` | `PASS` |
| `common/journal_entries/00_suffragists.txt` | `je_suffragists` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1775?1797 | `F355D80B61A2C83EA4ED0AD4D9ACEF53FEDC8E66E2A35558811B4047252ECF77` | `404E9376152F50C6C40D2F6886A1D69CF022FC851AB14FB3CF4053E807A0241E` | 75 | oui | 75 | `1	1` | `PASS` |
| `common/journal_entries/00_taiping.txt` | `je_chinese_missions`, `je_heavenly_kingdom_main`, `je_taiping`, `je_taiping_revolution` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 5862?5950 | `B9137C8C8DA1B6C74884E8B9F8770773E04F8E148448897F821E3ED2BFEF6522` | `2034BA0ABB93A7C4FDCCB4003CF30A4633738DA81170EDC3F266C6C4DFA50141` | 343 | oui | 343 | `4	4` | `PASS` |
| `common/journal_entries/00_trade_route_event_missions.txt` | `je_build_local_arms_industry`, `je_set_up_grain_import`, `je_set_up_paper_import`, `je_set_up_steel_import` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 3089?3177 | `29718D5E71F603192FF592AC83A33D2525372487CE7123A58D87088713904C6B` | `17FA2D0EC53B5D19F39341E7E98A8F506E4BFA27327CE5DDE04FC21A4436EC33` | 191 | oui | 191 | `4	4` | `PASS` |
| `common/journal_entries/00_turtle_island.txt` | `je_unite_the_nations` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1745?1767 | `DAE249E7CF51D9E3B57592192E32B153180648336E512C25F7CA661B3B7DD1EA` | `9B0B99611A32209DF3617C0A099F2FFEB52B7A2D16BFCC6996A989B6F7BBE15C` | 86 | oui | 86 | `1	1` | `PASS` |
| `common/journal_entries/00_tutorial.txt` | `je_subject_liberty`, `je_tutorial_capacity_deficit`, `je_tutorial_change_production_method`, `je_tutorial_colonize_state`, `je_tutorial_convoy_raiding`, `je_tutorial_create_formation`, `je_tutorial_declare_an_interest`, `je_tutorial_earn_obligation`, `je_tutorial_enact_institution_law`, `je_tutorial_establish_company`, `je_tutorial_expand_basic_building`, `je_tutorial_expand_military`, `je_tutorial_expand_productive_building`, `je_tutorial_fix_budget_deficit`, `je_tutorial_fix_unproductive_building`, `je_tutorial_foreign_investment`, `je_tutorial_form_power_bloc`, `je_tutorial_grow_gdp`, `je_tutorial_improve_consumer_goods_access`, `je_tutorial_improve_market_access_with_railways`, `je_tutorial_improve_rank`, `je_tutorial_improve_supply_network`, `je_tutorial_incorporate_state`, `je_tutorial_increase_immigration`, `je_tutorial_increase_market_access_by_decree`, `je_tutorial_increase_relations`, `je_tutorial_invest_into_an_institution`, `je_tutorial_is_play_target`, `je_tutorial_lobbies`, `je_tutorial_make_interest_group_happy`, `je_tutorial_make_peace`, `je_tutorial_mobilize_army`, `je_tutorial_prevent_revolution`, `je_tutorial_promote_movement`, `je_tutorial_recover_from_default`, `je_tutorial_recruit_promote_commander`, `je_tutorial_reform_government`, `je_tutorial_research_technology`, `je_tutorial_send_general_to_front`, `je_tutorial_start_diplomatic_play` | 52 | 0 | 52 | 0 | 0 | 52 | 52 | 0 | 0 | 31726?32870 | `06482E7300968DAEF778A80D48F9BA202E61C13D0D573545FB24FA3A4C4E2017` | `282FB8A24F404874FA905F5E9E9187627102114BF0F6F72D744E63A2407E6885` | 1740 | oui | 1740 | `52	52` | `PASS` |
| `common/journal_entries/00_veiled_protectorate.txt` | `je_veiled_protectorate` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1234?1256 | `F9396C040A81BCF7A0D2DF51CE40C9E3CB1457B927C286465EBFE1F99635AE81` | `4E5416113B5DBA8059D1F39B68D7DEAFCD52A7181C55FF1248EC9B1C2CF20524` | 74 | oui | 74 | `1	1` | `PASS` |
| `common/journal_entries/00_victoria.txt` | `je_victoria` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1432?1454 | `D75A815854C2EEA310A2CFEC68A61F663BE60C16783A51FA2006A65D069651FF` | `B55646BD41D0A8C0DD9DD0486A185F7E701222F15AA917B9ECD77B561625E6AB` | 101 | oui | 101 | `1	1` | `PASS` |
| `common/journal_entries/00_warlord_china.txt` | `je_warlord_china` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2288?2310 | `CCE8A4F3C979E77E41E3CC0795F30EC199C2145F15B9900284E2420EE66B28BA` | `B450CE6B18E39E15E317442E15F2E6DCF1FE8EC43672F77CBACADD91395F4021` | 107 | oui | 107 | `1	1` | `PASS` |
| `common/journal_entries/00_west_america.txt` | `je_west_america_expedition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3680?3702 | `DD55BE4BC4A21C0867071A899F1D9635B9B3125DF30B05087400E03C70BE47A0` | `ED15B734FDDE9CBD390EF943CB90F2BEEC11A60F51A2BE66F3ACAA4098FAC654` | 146 | oui | 146 | `1	1` | `PASS` |
| `common/journal_entries/00_zanzibar.txt` | `je_lion_of_the_zanj`, `je_splitting_oman` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 7191?7235 | `429A410BC9462613B4BD9475AD8B5011AD6B405BA1F80AE59EEAFD6BF1B5E4A2` | `03E4C7A3C2E8668B3AF351CCA8078D4313F545F453BB4C04FDB58525A6402B98` | 324 | oui | 324 | `2	2` | `PASS` |
| `common/journal_entries/01_algeria.txt` | `je_conquest_of_algeria`, `je_french_foreign_legion`, `je_reconquest_of_algeria`, `je_the_algerian_departements` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 6652?6740 | `8411EE72E8215C3320842499BDB61E187AE44A146307925C31E78251122FF075` | `229F2D1F0048F66C90E211608CD14E4FD63719219F4BA12CB39D31D81F9776A8` | 317 | oui | 317 | `4	4` | `PASS` |
| `common/journal_entries/01_coup.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2954?2954 | `37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602` | `37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602` | 145 | oui | 145 | `0/0` | `N/A` |
| `common/journal_entries/01_dreyfus_affair.txt` | `je_dreyfus_affair` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1511?1533 | `4867536D65CB980BFCDB8F1A525262791FAD631E6120E0804D1C1A7D24EA6A02` | `2C6119470940964721AE01E4B24D5F8A2DBFF0F54F9F60129EB5F4259DF98F0A` | 97 | oui | 97 | `1	1` | `PASS` |
| `common/journal_entries/01_french_monarchism.txt` | `je_cement_the_rightful_dynasty`, `je_divided_monarchists` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 14798?14842 | `56048B1FC48E5345E766F84CDBF3EB7433C3CCAA4AE60C400680C7903623C830` | `702D9BD9C303DC6656143879DE26F7C83C33D8FE0EFE2C50B8B2076CE6C4F0FF` | 513 | oui | 513 | `2	2` | `PASS` |
| `common/journal_entries/01_hispaniola.txt` | `je_haitian_debt` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2760?2782 | `53A7A54042D904AFDAB67CEFAFFE642CEB4860F9157FACCFD52A1B786F9DE447` | `5C4C240A28F2885786E3B03F7DCF79304CC02525289A19C310358BDB6A311248` | 92 | oui | 92 | `1	1` | `PASS` |
| `common/journal_entries/01_indochina.txt` | `je_indochina` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1635?1657 | `33133173D639698BF7B662F8D27669DBBDE8251F155C0CBE70F2B86904FFF4AA` | `2EA7CBC1757CAC7DE668D4594F9F7B6ADA22797D4FC2B4ABB999E9BB09DCF43E` | 83 | oui | 83 | `1	1` | `PASS` |
| `common/journal_entries/01_krakow.txt` | `je_the_krakow_uprising` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1503?1525 | `B3D9296312DC68628BAEF5C3F5C87FBBE9F46B4DC7783346E4693ECA334F57D3` | `098790CB02BE59406F0666B0BE31CEB95125BFF6646ACD12329A5588300CCF41` | 65 | oui | 65 | `1	1` | `PASS` |
| `common/journal_entries/01_natural_borders_of_france.txt` | `je_confederation_of_the_rhine`, `je_french_natural_borders` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 4681?4725 | `AFB646222CF708B953375F84496F72D58C50535A5144E12804EEB73FE8673BC9` | `33750CC263550A3A67CD8702ECEC0EF38894A2BF652A292ACB12E61632955C27` | 243 | oui | 243 | `2	2` | `PASS` |
| `common/journal_entries/01_nihilism.txt` | `je_nihilist_movement` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3922?3944 | `87E4C591520C2BB488571151E62E27641ACFC273B2882D48356639A76FB0D1FC` | `94ECC16CCD32B5C250D78A0F50DB7F902C2AB75E0FBB6E56E80987818B9AF4BD` | 206 | oui | 206 | `1	1` | `PASS` |
| `common/journal_entries/01_paris_commune.txt` | `je_the_paris_commune_communards`, `je_the_paris_commune_france` | 3 | 0 | 2 | 0 | 1 | 3 | 2 | 1 | 1 | 6972?7016 | `FAFA460F2F8C0474E5774A23D3FA3D6761B3E7EE60DF6F54A69C2D7B06CD1D38` | `69E24EC0FD0C2F07164AD6492CD9F4694879F1EA639B84900BCDEA20A5FF6199` | 340 | oui | 340 | `2	2` | `PASS` |
| `common/journal_entries/01_ryukyu_rivalry.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6178?6178 | `B50F63CF7AE1201216F153186040344E76ED4980702F63B8107D499F8D21BD7E` | `B50F63CF7AE1201216F153186040344E76ED4980702F63B8107D499F8D21BD7E` | 329 | oui | 329 | `0/0` | `N/A` |
| `common/journal_entries/01_silkworm_diseases.txt` | `je_silkworm_diseases` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2951?2973 | `22E2A266EF3DF56DCD96683D0161EDBA70058AFE828ED80F9B6FC88DC160D2C5` | `9E6D5C90C530998C915CEA127751CA0DE767C0B24AAFE556A656F94F4AC559AE` | 159 | oui | 159 | `1	1` | `PASS` |
| `common/journal_entries/02_acre_dispute.txt` | `je_acre_dispute` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 604?626 | `BB2CCE10F6EEE9627DC78CE4B4E8EEDD757C5313E35143F93079B7CA8519BCE5` | `CE80D7CCBB66C01122C148EF11797076EFC806C73195044E6B423B58839B2B8C` | 34 | oui | 34 | `1	1` | `PASS` |
| `common/journal_entries/02_amazonas.txt` | `je_amazonas` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1295?1317 | `22EA8DA4600AFDE67F9725E8FF790459F8A68EA96FE229673442CD37534E7431` | `D42D606838DE1DE1F998F57DCFD6D6121FC85AD4B16CB81334BFAA4E4E45EE04` | 62 | oui | 62 | `1	1` | `PASS` |
| `common/journal_entries/02_brazil_navy.txt` | `je_brazil_navy` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2281?2303 | `99D3A7B51C87EE1B93C61E64D23828A1FE56A982AD9F4E42B8CADB709C132689` | `91F3CAAA14E174CBD1A5AAE4A7B1BB4488A089539AB0132A2D7F70EA8FFDBBE9` | 136 | oui | 136 | `1	1` | `PASS` |
| `common/journal_entries/02_brazilian_nation_building.txt` | `je_brazilian_nation_building` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1880?1902 | `7ED542816D75BB1CE4146F07C6B0139A63B2D38E4547377CADDF17F79F172E01` | `F83841541DC8386C0831E4758AE900FD3AC20F230D2B59DE3DEA763EA3FBA58C` | 80 | oui | 80 | `1	1` | `PASS` |
| `common/journal_entries/02_brazilian_slavery.txt` | `je_aberdeen_act`, `je_matter_of_slavery` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 6996?7040 | `11535425942E9B046CE134E549FBB43BCFF4E462EABE3C64154345D8E30C5B3E` | `0A796C64D652E3939DE03F538BA2E14C863D099B04BE2937C4D506EFB84426DB` | 263 | oui | 263 | `2	2` | `PASS` |
| `common/journal_entries/02_caudillo.txt` | `je_caudillo` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1385?1407 | `421121DA0FA3CB88DE95FFCF45CB2D0773D2CABA397B25DC3DCAFF1D771DB571` | `56DD875FBD7AB2744233E522A175D094DD2DD9612FD1A808ABA9C8BCF5B21059` | 70 | oui | 70 | `1	1` | `PASS` |
| `common/journal_entries/02_coffee_and_milk.txt` | `je_agricultural_development`, `je_coffee_with_milk` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 5477?5521 | `4D5A06762EFBBDD38CBE7F25D84B13A683D0BD36404FAE2D748097DEA134FE32` | `66E0F7F02BD79F683FD4489E70B9CC1C5246BDEE997D49471E4BD6E0A3EDC307` | 284 | oui | 284 | `2	2` | `PASS` |
| `common/journal_entries/02_cristo_redentor.txt` | `je_cristo_redentor` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1847?1869 | `DF7AA978F54AEE03C131AF829A9E3AF35739553952762D8DBCF0BEEEBCFEB014` | `E226FE9178BAB0F5660670D4D3A5D40372552DDFDEE255E76A19E9F9AC0254EE` | 66 | oui | 66 | `1	1` | `PASS` |
| `common/journal_entries/02_gran_colombia.txt` | `je_andean_federation`, `je_gran_colombia`, `je_la_plata` | 3 | 0 | 3 | 0 | 0 | 3 | 3 | 0 | 0 | 6017?6083 | `0D7E32C64B3B4E5E2044BBA5B303DE9E949C9459AE8FC1D3CEFDA256AEC92585` | `A6F1925247136AB175A35E59A5084A7FB615CF96DC3D0056086998F923555A1D` | 230 | oui | 230 | `3	3` | `PASS` |
| `common/journal_entries/02_paraguay.txt` | `je_expanding_paraguay`, `je_francocracia`, `je_modernizing_paraguay`, `je_paraguayan_war` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 12235?12323 | `A3ECE915C0B089F661F866DFAE3A41120F50684139E82A6A49E1741292B17219` | `99CC52566A0963DAC7DB7873C53A120D933983303FA723CE32FB6C85D0D9AAC7` | 419 | oui | 419 | `4	4` | `PASS` |
| `common/journal_entries/02_pedro_brazil.txt` | `je_isabel`, `je_pedro_brazil`, `je_pedro_republic` | 3 | 0 | 3 | 0 | 0 | 3 | 3 | 0 | 0 | 6952?7018 | `6F2E01D208E80CF7327CADC9E6137149ED075E9C34B6408532988A6CDABDCF0C` | `81D4C81CD2DBE8B3F4094CFE5072B2A7729BBF591877EA5D9667A81D681576C7` | 397 | oui | 397 | `3	3` | `PASS` |
| `common/journal_entries/02_peru_bolivia.txt` | ? | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 6395?6395 | `AC3E6B2E8BAC504BE20EC86ACE1B5E55F08DD9FAEB9FED7D5AC390E23B67D52D` | `AC3E6B2E8BAC504BE20EC86ACE1B5E55F08DD9FAEB9FED7D5AC390E23B67D52D` | 356 | oui | 356 | `0	0` | `PASS` |
| `common/journal_entries/02_positivism.txt` | `je_positivist_movement` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3240?3262 | `AA131209893B970FA3E41FA4CA643E9939D3BC5B10BBC970204D9B40C7FD5968` | `C9C9963D09E2F04A7619AC456D47176AAAD6FAC023BC73DB775F4B345471425A` | 141 | oui | 141 | `1	1` | `PASS` |
| `common/journal_entries/02_south_america_migration.txt` | `je_american_west_migration`, `je_central_america_migration`, `je_south_america_migration` | 3 | 0 | 3 | 0 | 0 | 3 | 3 | 0 | 0 | 10097?10163 | `344B48806BF9CDB8732EBCD17B8B713FBC1CCB5CC266E390BAE79C940F012576` | `04CF77749684B72C460EBDAC05CD8CDB5AB273B342DBB3128CE6E9031F263702` | 472 | oui | 472 | `3	3` | `PASS` |
| `common/journal_entries/02_south_american_national_identity.txt` | `je_south_american_national_identity`, `je_south_american_national_identity_emergence` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 10810?10854 | `4C7F7F3513A49A02997C0CCD45FFEB3E2E12EC25B25D0E69A179FFED12DB16C3` | `3DA4A2A9185DFC8D1BB2731802D590A6EEFB708A0DCAB5EB2AB8C1140D4812AB` | 609 | oui | 609 | `2	2` | `PASS` |
| `common/journal_entries/02_vargas.txt` | `je_new_republic`, `je_populist_unrest` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 4492?4536 | `D74771B12EDB06836C45EB089A2F6D9037D20A5642D5AA20CFE6D915BA4B90CA` | `198049D9605F877E6AD41AAD3171E2BF444EF4A739910A35C870671681121539` | 227 | oui | 227 | `2	2` | `PASS` |
| `common/journal_entries/03_afghanistan.txt` | ? | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 36813?36813 | `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13` | `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13` | 1877 | oui | 1877 | `0/0` | `N/A` |
| `common/journal_entries/03_eastern_frontier.txt` | `je_eastern_frontier` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3009?3031 | `07964D763970E212A7E0EF699C5291A7C91555CC67555B0B00D8B3AA26391FAB` | `8068CD49C701306AAFBA2765A171920CBC713392D1D0789545FBD86D9647C377` | 99 | oui | 99 | `1	1` | `PASS` |
| `common/journal_entries/03_korea.txt` | `je_donghak_movement`, `je_gyojo_shinwon` | 3 | 0 | 2 | 0 | 1 | 3 | 2 | 1 | 1 | 6535?6579 | `821197371358ACEAAABBDD8A99EEF7D876D283F53D3575274B1D3CEF3D336455` | `8BD11B8E39FADCFE63F7270535D84B58C4F2ABB65805DDFB027906527E6C4F8E` | 353 | oui | 353 | `2	2` | `PASS` |
| `common/journal_entries/03_lobbies.txt` | `je_anti_lobby_demand`, `je_anti_lobby_opportunity`, `je_pro_lobby_demand`, `je_pro_lobby_opportunity` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 9882?9970 | `5F51917ED1DF7B22A077847C094B4D4A5E95C2C1B173351E01AE877526FCAABD` | `DFB70ACE268E0260308A9C091684072D093720E3256071E37B678C119F2EEB6D` | 526 | oui | 526 | `4	4` | `PASS` |
| `common/journal_entries/03_russia.txt` | `je_caucasian_war`, `je_caucasian_war_circassia`, `je_caucasian_war_imamate`, `je_circassian_expulsions`, `je_conquest_of_central_asia`, `je_great_reformer`, `je_great_reforms_bureaucratic`, `je_great_reforms_military`, `je_great_reforms_serfdom`, `je_pacify_the_steppes`, `je_the_eastern_border`, `je_the_last_kazakh_khan` | 12 | 0 | 12 | 0 | 0 | 12 | 12 | 0 | 0 | 36446?36710 | `CD43326BD2FE772C68D0E7EC35E24AB1382ADD9F61AD5382AFCC595EEAAA62C6` | `825FBB15BE1131BF67D62480F06D81713EED485FC4CFA8C7554272735637F052` | 1345 | oui | 1345 | `12	12` | `PASS` |
| `common/journal_entries/03_tibetan_expedition.txt` | `je_tibet_expedition` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 5975?5997 | `7DFAD141376CF303F6D0C050C7C844BC63DE6B93EA062AF5557346E32F68CAAB` | `06B009AAA31899FE4758FFCB37CC07FC1C9C7FEBDFBA17D88762ADE49467A770` | 259 | oui | 259 | `1	1` | `PASS` |
| `common/journal_entries/04_communal_divides.txt` | `je_communal_divides` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 6209?6231 | `512EDBADCB215BCF91E3B5E2BDD47DA9AEAF16572DA51253A60F591BF5948469` | `5D38C1EC405B3CDDDAC5A26E1710703A51CEEC0C4E2AB5BCCFDA488D58C4B724` | 201 | oui | 201 | `1	1` | `PASS` |
| `common/journal_entries/04_dravidian_movement.txt` | `je_dravidian_movement` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2475?2497 | `631035D1CB59B7C884F6DB421644D7E60F9AF6E4F769E950BBFC2C2DF166668A` | `384AD22D74D132B2E14F1E4C3FDC3CA6CD026A0E9A27381FC6AD5426B0F675F0` | 101 | oui | 101 | `1	1` | `PASS` |
| `common/journal_entries/04_imperialism_of_promise.txt` | `je_imperialism_of_promise` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2912?2934 | `80E38C181A5AEB547E8F98EBFD03844F3522CADC59426D9FC16588B908105C3B` | `EF5200E0B9E7A58AF904C73CDD82F3CC4009FFE0CA9364952F793AB4F3E2A682` | 142 | oui | 142 | `1	1` | `PASS` |
| `common/journal_entries/04_india_british_dictates.txt` | `je_british_dictate_law`, `je_british_dictate_military`, `je_british_dictate_plantations`, `je_british_dictate_universities` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 8685?8773 | `6075C5B204C7D184B1C2CE5AA244B3E1C5B3416B701AFF7E67674EE1B8DEF39C` | `BE9FC03619946E632A20AE15EE9B66249D7C9FE8E65B102963AB3E195C709ED7` | 419 | oui | 419 | `4	4` | `PASS` |
| `common/journal_entries/04_india_home_rule.txt` | `je_india_home_rule`, `je_india_nationalism_britain` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 5021?5065 | `C6877EAE59612D3943BA8210769C316B0C7DD163E8ECCDBB8BCD979ECC4B7734` | `4C35F800185A4661D0B092822DD8CA37F2BE706EF31F4414E9A59E46C7922B17` | 249 | oui | 249 | `2	2` | `PASS` |
| `common/journal_entries/04_india_nationalism.txt` | `je_india_nationalism` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2113?2135 | `AA28A05206EEA4553E065889F89A085B3AD3365AACA3B79F29C3E8ACC6055FEE` | `68D4944036755F6EA61CD9F4CCAA4BDB3D27D2B3975CE2FD354B3AB500C22931` | 111 | oui | 111 | `1	1` | `PASS` |
| `common/journal_entries/04_india_non_cooperation.txt` | `je_india_non_cooperation_movement` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 7411?7433 | `B38742122F9538A891C8F196D8BB0A8ECBA99CF6CCE4BC74D0C29F1EA46059A4` | `A697D95414E03ED3F7E010E771F11E19636D45CD8BAECD312FCE510AB432CA1F` | 294 | oui | 294 | `1	1` | `PASS` |
| `common/journal_entries/04_indian_famines.txt` | `je_indian_famines` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 4757?4779 | `4156E8248F99357F534647229F6A3AB5EC5CA4412050A76E5C8129F29F6948BF` | `F7BD76538FE9D9342B5522531F746752F696E6342276891C2F24F0FA5BD536A6` | 237 | oui | 237 | `1	1` | `PASS` |
| `common/journal_entries/04_indian_federation.txt` | `je_federation_of_india` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2702?2724 | `F33904A7BE9A6ECFE008A798A77267801FA62654F960932D96F8771F6E33641D` | `5FCA14A911AA1D8BD8794F2A348A9235F73727558E15485B4E28217883BA9F26` | 143 | oui | 143 | `1	1` | `PASS` |
| `common/journal_entries/04_mughals.txt` | `je_mughal_hindustan` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1270?1292 | `436DAE5C3471EFFFC659CFD27F12CDF518A7BF9D34B1D0ABE7ED2D7A0E924CA0` | `663F7276660930C3294769DEDB9A3F6678F0127A95D0FADEE1826C446B100502` | 62 | oui | 62 | `1	1` | `PASS` |
| `common/journal_entries/04_princely_states.txt` | `je_princely_states` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2011?2033 | `633F01424545ABD21F7E71AA90FA7713BC1436F900EFC0EE5C7ED44574847531` | `3D9B1BBE97AAA3621E22BB56813C3501E9433539BAB692A36EB5FF3CD2530CFA` | 97 | oui | 97 | `1	1` | `PASS` |
| `common/journal_entries/04_sepoy_mutiny.txt` | ? | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 16040?16040 | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` | 622 | oui | 622 | `0/0` | `N/A` |
| `common/journal_entries/04_sikh_empire.txt` | `je_sikh_sovereignty` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 4009?4031 | `66CFB926DB678EE8F2CEEB39B100E667B51E3885E9D77993787E853F05A573CE` | `0074B52992403404504BD3C3DD860D23578FE1514D68E9DEED93C2C1FC15366F` | 201 | oui | 201 | `1	1` | `PASS` |
| `common/journal_entries/04_victoria_terminus.txt` | `je_victoria_terminus` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2857?2879 | `274C37F6EE9E0B542ACE188DB1FD40BB6E802E0EE96E2270935F0CB2B8ABF5CC` | `87637E25CE512E3FD17BC46D04EBAFAFF5BD7F794F69368C9F1D22B989C586BC` | 105 | oui | 105 | `1	1` | `PASS` |
| `common/journal_entries/05_austria_journal_entries.txt` | `je_austrian_neo_absolutism`, `je_matter_of_hungary` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 9617?9661 | `BB7EBDB77C75362301ABF2DBD155A9D2181E93ABA0163732EBA002D8A300E7C6` | `4D64F02D8C5778A412B60EBDE880463217E35845B0F458E8D021B8FAC08AC268` | 427 | oui | 427 | `2	2` | `PASS` |
| `common/journal_entries/05_austrian_fascism.txt` | `je_standestaat` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 5932?5954 | `5202FB8745E4A94D0C6CDD84DD880A3CCEBE168E5F077FF7714A821217F2B820` | `07E0C98C4DB9FB6DAAE1F441C883C84268A8617F635F093FEBF463F83F5EBB8D` | 263 | oui | 263 | `1	1` | `PASS` |
| `common/journal_entries/05_balkan_national_awakening.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2437?2437 | `B5D2D5D89735490444B4F95D6F6015C503F50CB3A4DB7B5173588F676621CB98` | `B5D2D5D89735490444B4F95D6F6015C503F50CB3A4DB7B5173588F676621CB98` | 128 | oui | 128 | `0/0` | `N/A` |
| `common/journal_entries/05_balkan_wars.txt` | `je_spoils_of_war`, `je_the_balkan_league` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 9967?10011 | `2F2EA1370DFE73F87CACA62EAD5D23F073B50BBEA403186346AD632ECA568134` | `8D961CDA6BDD00003ADDC263D088EFC70A741E16B80D66CB964665813FD4A506` | 474 | oui | 474 | `2	2` | `PASS` |
| `common/journal_entries/05_bulgaria_je.txt` | `je_prussia_of_the_balkans` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 3144?3166 | `036B416D7C572006014F3C0152F73B7780DC6BC9525AFFCFCC756CDD4777C8B4` | `1365E64A0C1A86D7AFC26F11D763627959972312997FBACD0ADD107E457CCC8C` | 180 | oui | 180 | `1	1` | `PASS` |
| `common/journal_entries/05_creation_of_yugoslavia.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3032?3032 | `4371E202B494B2F7FA1FCF06BDFE1E0562895480E160AD37E551E3587606E46C` | `4371E202B494B2F7FA1FCF06BDFE1E0562895480E160AD37E551E3587606E46C` | 145 | oui | 145 | `0/0` | `N/A` |
| `common/journal_entries/05_danubian_federation.txt` | `je_danubian_federation`, `je_danubian_federation_observer` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 16795?16839 | `ABAFD3671FFE52D38DB5CC7AC71B89452EB10DC9EBE60EB7769EFDF369B94206` | `2EBD8901AA094D937E58A15D607B96A8FF2D70E5ACE6D3AA5CDDDAC3359DE4F9` | 690 | oui | 690 | `2	2` | `PASS` |
| `common/journal_entries/05_eastern_question.txt` | `je_eastern_question_austria`, `je_eastern_question_russia` | 2 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 4819?4863 | `DA61A784FD0F8A76E3D0D6F39566D1574AC0E63634BCC78A7AC74B7E13C026C9` | `085711B8A9B52DA92A9EA894AA4DC78868E89F94C778390D46D6156BB5D770D3` | 274 | oui | 274 | `2	2` | `PASS` |
| `common/journal_entries/05_great_eastern_crisis.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7995?7995 | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | 335 | oui | 335 | `0/0` | `N/A` |
| `common/journal_entries/05_greece.txt` | `je_bavarocracy` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2606?2628 | `26E809FD74D9428CE751BA2F46157D2DA70F139C74708BACD13B618A05F37EBB` | `2E362E3F97AB4A2B2EA8BCA0DB1810064BBBF79DF3635B050304D3A7DE19C8FA` | 149 | oui | 149 | `1	1` | `PASS` |
| `common/journal_entries/05_grunderzeit.txt` | ? | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 9054?9054 | `11300E647F370D0C0BD924AC32CDB9665D1C560E3FD7FBC82876838440DA51AB` | `11300E647F370D0C0BD924AC32CDB9665D1C560E3FD7FBC82876838440DA51AB` | 340 | oui | 340 | `0	0` | `PASS` |
| `common/journal_entries/05_hungary_je.txt` | `je_hungarian_revolution` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2514?2536 | `58A2880C740EA5ADFFE879FBE502BAD0FE669C5A642AFCDE92F90437AD611D8B` | `F65B11415EA76284045B2159CEBF0AE13F12B7589C3CBB7D016EC6278BF8EAE7` | 127 | oui | 127 | `1	1` | `PASS` |
| `common/journal_entries/05_hungry_forties.txt` | `je_the_hungry_forties` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 745?767 | `68A500F358F3FCE010C03CB4E561D93CD83973F94950F6FDDCFBD82EA313E746` | `6C628D44690669B77D6503F369FFDB575B0B7EAB81D79D0B32D561C56984B104` | 39 | oui | 39 | `1	1` | `PASS` |
| `common/journal_entries/05_metternich.txt` | `je_metternich` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2829?2851 | `0D5148962ABF3E2AC9057D7557A9FBCBD3FAF612DD24C31E18E8512FB777CE52` | `84257192774869AE11B3818E6B2209AC4829EAB5F8190AE0785915ACF779BF45` | 158 | oui | 158 | `1	1` | `PASS` |
| `common/journal_entries/05_montenegro_je.txt` | `je_mon_austria_alliance`, `je_mon_state_formation`, `je_montenegrin_raiding`, `je_tur_raided` | 5 | 0 | 4 | 0 | 1 | 5 | 4 | 1 | 1 | 15482?15570 | `7F7CC9A9915B062617D45BDB9A2F41A12709180653BCD3A32A6F1EBAA01A0181` | `735FA463466FB24CEE9704C10823DED885A37A282EEE0091F0C90D2BFAA97DB7` | 800 | oui | 800 | `4	4` | `PASS` |
| `common/journal_entries/05_national_awakening_monument.txt` | `je_kaiserforum` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 7459?7481 | `001D357A55DBB679FF0F4423A77B09329F64D3DF23269E8D24A6236ECFF18A7B` | `DF72A7F0D43C0EC269CC8A339801714E7922B88258AF27B04C01C1BEDEC515C5` | 241 | oui | 241 | `1	1` | `PASS` |
| `common/journal_entries/05_prestige_goods.txt` | `je_prestige_goods_artillery`, `je_prestige_goods_clothes`, `je_prestige_goods_coffee`, `je_prestige_goods_explosives`, `je_prestige_goods_fertilizer`, `je_prestige_goods_fish`, `je_prestige_goods_furniture`, `je_prestige_goods_grain`, `je_prestige_goods_groceries`, `je_prestige_goods_meat`, `je_prestige_goods_merchant_marine`, `je_prestige_goods_opium`, `je_prestige_goods_paper`, `je_prestige_goods_small_arms`, `je_prestige_goods_steel`, `je_prestige_goods_tools` | 16 | 0 | 16 | 0 | 0 | 16 | 16 | 0 | 0 | 55001?55353 | `632F808607E84B3C27E161333B9399AA9C2DBB07904F295DF7C9A44937B18B76` | `7955865CDA1D5A0C991EB97864D8F1A5CA7BD1FE8074632C144B5C4FC87C6812` | 2063 | oui | 2063 | `16	16` | `PASS` |
| `common/journal_entries/05_struggle_for_the_highveld.txt` | `je_struggle_for_the_highveld` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 7117?7139 | `0E4BEB12EBF7253B06A9E4C049508ADF7D0D4AACE52F26D8AA1E92AD37299873` | `D95164692525083DA4535425CD601013DB131D464EE1EA34DF6D41F7E7AC399A` | 276 | oui | 276 | `1	1` | `PASS` |
| `common/journal_entries/05_technocracy.txt` | `je_technocracy` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1754?1776 | `5AC2BBF559405F61A6746B25107ACDEA350F0B69487633DFA52A33BEDC50CEB8` | `565C85F5E125B2DBBB09D608B21A08F42B39FE263E811825063528E4BF519D92` | 75 | oui | 75 | `1	1` | `PASS` |
| `common/journal_entries/05_the_grand_collapse.txt` | `je_the_grand_collapse` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2919?2941 | `BE9747A331A2408F393B606CBAB0C4C47D9247FE557F0FDFD48DFF0DBDCF51BF` | `DA5B38D5374BC652240B8C88EEE3DBED631D6600FC158648C945FC41E6076530` | 161 | oui | 161 | `1	1` | `PASS` |
| `common/journal_entries/06_cuba.txt` | `je_cuba_espanol`, `je_cuba_independencia`, `je_cuba_la_vida_dulce` | 3 | 0 | 3 | 0 | 0 | 3 | 3 | 0 | 0 | 12627?12693 | `269A3ACECA7C79FD32C1B43D5EF8DB2D354F1798EBF39A4F5FE071F681461614` | `8E97E53851CC5D7A656A71205AE53C0961843EDE48435C505CC721E9F4F1A396` | 497 | oui | 497 | `3	3` | `PASS` |
| `common/journal_entries/06_dominican_content.txt` | `je_la_trinitaria` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2304?2326 | `D4590F7F2490EDC187319DA0DC6DE95F931FCAB5EEE7F4EDC2710E6ECF1B02D4` | `468A6748AA633BB19E619444392D73EC142F92F8596033B7A482308284E538E8` | 123 | oui | 123 | `1	1` | `PASS` |
| `common/journal_entries/06_economic_regeneration.txt` | `je_spa_economic_regeneration_land_reform`, `je_spa_economic_regeneration_light_industry`, `je_spa_economic_regeneration_master`, `je_spa_economic_regeneration_mining`, `je_spa_economic_regeneration_modernise_agriculture`, `je_spa_economic_regeneration_railways`, `je_spa_economic_regeneration_ultramar` | 7 | 0 | 7 | 0 | 0 | 7 | 7 | 0 | 0 | 47971?48125 | `6D83619823696F7BFF9AAD9BC848175406E4E0EC68A8C94D19A26660A384F5E8` | `6AC13878ABDD9BFE6C1D7B767E4A632A4DD96D05197B6A216E1DE0F6AB6C1EEF` | 1489 | oui | 1489 | `7	7` | `PASS` |
| `common/journal_entries/06_french_revolution_mod.txt` | `je_fr_rev_summon_estates` | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 3986?4008 | `2CE90A9CDFE38F6AA67828C59CD409822E0E3FA4DE13B0E4AA40E4F74B785C33` | `816985646B257FC7351C6A9585748222B36C8764C1971F8261DEFC7B1F7CC820` | 179 | oui | 179 | `1	1` | `PASS` |
| `common/journal_entries/06_iberian_twilight_monuments.txt` | `je_atocha_railway`, `je_gran_teatro`, `je_manila_cathedral`, `je_pena_palace`, `je_sagrada_familia` | 5 | 0 | 5 | 0 | 0 | 5 | 5 | 0 | 0 | 18064?18174 | `8BA91A9EE0832C2FB449704712E0176E8AEC83646C8648BCCFB7317E7548945C` | `50023ADF9A6033D6CC89D89C1C7402765459AAD2A98A05A3C23A58A82F9EDDF7` | 652 | oui | 652 | `5	5` | `PASS` |
| `common/journal_entries/06_language_policy.txt` | `je_vernacular_policy` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 8792?8814 | `63F50FBB250B5506C4F4BC453F6E90ADFA7B116B1B4B433C853E94240440F7F0` | `30ABA0968A3214DAB89E5CCAB4A36BF3C6C3E47871047D27D10F55F88572E56A` | 420 | oui | 420 | `1	1` | `PASS` |
| `common/journal_entries/06_morocco_lands_of_anarchy.txt` | `je_lands_of_anarchy` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 5639?5661 | `5284F9A3090268A639B05AAA590CCBACAFED5AE0DAA14E291A7EF523A238A711` | `1D1C477D4976A38162CBB73F7F0500C399E273DEB7015352656C34C4666AB379` | 218 | oui | 218 | `1	1` | `PASS` |
| `common/journal_entries/06_new_imperialism.txt` | `je_new_imperialism` | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 1866?1888 | `1B3F2CC9F54842D2BB4A39358A8566A602E1850BD4AE1DDD16E2B2DC522A5A73` | `5F9FAA0B8E30ABCB7562C98D292D02C946AC00090A5ACD4A5BFFC787AEA30822` | 58 | oui | 58 | `1	1` | `PASS` |
| `common/journal_entries/06_philippines_je.txt` | `je_filipino_ethnogenesis`, `je_philippines_development`, `je_philippines_main` | 3 | 0 | 3 | 0 | 0 | 3 | 3 | 0 | 0 | 12435?12501 | `3A1FCB5B09832D3DB37FC29B1362F39A5C3AAD80F75986F650B51092179E7F68` | `7CAC91756AFB3445EB4E7B4285553597094D4DDF09B4D5DF09C882D6244ECB27` | 464 | oui | 464 | `3	3` | `PASS` |
| `common/journal_entries/06_portugal_politics.txt` | `je_devorismo`, `je_portugal_regeneration`, `je_portugal_regeneration_agriculture`, `je_portugal_regeneration_institutions`, `je_portugal_regeneration_public_works`, `je_second_liberalism` | 6 | 0 | 6 | 0 | 0 | 6 | 6 | 0 | 0 | 14489?14621 | `95E3C0BFFC98092D82BD79F77F459908CDB10888BACC6AA9B27FA970B1561233` | `579BC26CE5C34857788CF3DED710D90DB31168A3ECD49E8D59B8BC62D0A73A53` | 689 | oui | 689 | `6	6` | `PASS` |
| `common/journal_entries/06_portuguese_colonialism.txt` | ? | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5308?5308 | `99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126` | `99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126` | 305 | oui | 305 | `0/0` | `N/A` |
| `common/journal_entries/06_spanish_africa.txt` | `je_conquest_of_tetouan`, `je_guinean_conquest`, `je_moroccan_conquest`, `je_western_saharan_conquest` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 7697?7785 | `416CE6A8CEF2C3F56D7DA2F2BE28D3FA1A5DFFAB4A95810910BEE8049D93B209` | `3D06B391F8934C812CFCFD72905A55DA8D5F698BD5FB35631F67ECFD01659AC8` | 396 | oui | 396 | `4	4` | `PASS` |
| `common/journal_entries/06_spanish_new_world.txt` | `je_hispanoamerica`, `je_reconquista`, `je_spanish_american_independence`, `je_spanish_new_world_dummy` | 4 | 0 | 4 | 0 | 0 | 4 | 4 | 0 | 0 | 7063?7151 | `AB9846DEDE17C0BCC23F0EF20D8F39B97E1E53EE917FCA7CB130EAF8390CD644` | `F15D9A4A3D0EAA468746A0F825BA52B99E34BC5D48866F56F6256F12F68350FF` | 380 | oui | 380 | `4	4` | `PASS` |
| `common/journal_entries/06_usa_independence_mod.txt` | `je_usa_independence`, `je_usa_independence_fra` | 2 | 0 | 0 | 2 | 0 | 2 | 2 | 0 | 0 | 2749?2793 | `FC2EF9E593D1DAB1910EB28896467D1CD74623C48950BB0FF76730418C02310D` | `86800653EF7329DDF254ED4F1C04DD9937A424933238CEA8EF981A46CA527EA0` | 154 | oui | 154 | `2	2` | `PASS` |
| `common/journal_entries/07_american_mod_jes.txt` | `je_buying_florida_mod`, `je_northwest_frontier_mod`, `je_sale_of_florida_mod` | 3 | 0 | 0 | 3 | 0 | 3 | 3 | 0 | 0 | 4867?4933 | `EB820389AA53CEE24C1058E3C1B5BE1D2FDACB31A48C21481B9EADCD60B621ED` | `46847DFD2E296CA34DBD7E2811992A5DEC64EB415B50E6E842C45C8AB678C1DB` | 257 | oui | 256 | `3	3` | `PASS` |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt` | ? | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 980?980 | `FCC68B3032EDCB9B2E6CA0420171B3DE00F34BB7CAE47CB59F844A3F02BF883D` | `FCC68B3032EDCB9B2E6CA0420171B3DE00F34BB7CAE47CB59F844A3F02BF883D` | 51 | oui | 51 | `0	0` | `PASS` |
| `common/journal_entries/07_hokkaido.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8180?8180 | `114CBFEEFD77C158402D8EC8079487446E26BCFC8EF35AA15EC843553F593729` | `114CBFEEFD77C158402D8EC8079487446E26BCFC8EF35AA15EC843553F593729` | 283 | oui | 283 | `0/0` | `N/A` |
| `common/journal_entries/07_iran_troubles_mod.txt` | `je_deputy_of_the_people` | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 1880?1902 | `8F31F385EC3EA9FDECFE1A0DC3758B4A283C243369751E021B14599E8987610D` | `B3141DA1EFFB77620E77ED853385545155CDA4C140E372F0C2E3F7D6BED5B43E` | 99 | oui | 99 | `1	1` | `PASS` |
| `common/journal_entries/07_irish_question_mod.txt` | `je_irish_question` | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 1293?1315 | `ED7463A3F2318C8486C68CD7058F09A5D8CABE2A3342BE07111828FF75B0519D` | `4C6C7D5C4AB2A85975822E411900F38A64BDF60220B4490DC65CBDF87A935A4E` | 78 | oui | 78 | `1	1` | `PASS` |
| `common/journal_entries/07_poland_lithuania_mod.txt` | `je_plc_reform`, `je_plc_reform_education`, `je_plc_reform_farming`, `je_plc_reform_great_power`, `je_plc_reform_industry`, `je_plc_reform_military`, `je_plc_reform_railways`, `je_plc_reform_trade` | 8 | 0 | 0 | 8 | 0 | 7 | 8 | 0 | 0 | 12575?12751 | `5D3EFE884DE36B6B379FCE1A81D3DC39979DA137D329BD5B4B1D7F9ACC13B1C5` | `F6A8EFBFAACED48A004240EBE47169FA0B1177C48FBB323705A35E33DB8E6F20` | 605 | oui | 604 | `8	8` | `PASS` |
| `common/journal_entries/07_sakoku.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2530?2530 | `74D89C1DE540CFA4DDB30B2959A4885FC73C1A2654A748853BA309C087B38922` | `74D89C1DE540CFA4DDB30B2959A4885FC73C1A2654A748853BA309C087B38922` | 106 | non | 106 | `0/0` | `N/A` |
| `common/journal_entries/07_tenpo_crisis.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2833?2833 | `37E7BF5859DD585D512CFE0B39E7383765598B7E8B69D4D4BD48AFBB76C90AC2` | `37E7BF5859DD585D512CFE0B39E7383765598B7E8B69D4D4BD48AFBB76C90AC2` | 141 | oui | 141 | `0/0` | `N/A` |
| `common/journal_entries/07_zaibatsu.txt` | ? | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8793?8793 | `CBCADE9B9F356123356BC720D4BD2ADE815CCEAE21076FDB01D705F630E1F94D` | `CBCADE9B9F356123356BC720D4BD2ADE815CCEAE21076FDB01D705F630E1F94D` | 389 | oui | 389 | `0/0` | `N/A` |
| `common/journal_entries/99_test_global_je.txt` | `je_global_test` | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2566?2588 | `A5B44990101ABBC135231E16EB0EACF438A240DCB6CABBC860012C365DCAC719` | `5FD5B45F6049F34F8562B6B2FEAD3D591AF70B82AEDD3F19C6F2DE95A3E636FF` | 138 | oui | 138 | `1	1` | `PASS` |

## 10. Protection et non-régression

Le validateur byte-level confirme que toutes les plages modifiées correspondent
uniquement au passage de l'ancien au nouveau nom de propriété. Les API
`has_role`, `is_ruler`, `has_interest_marker_in_region`, `has_journal_entry`,
`has_template`, `is_involved_in_journal_entry`, `add_journal_entry` et
`has_amendment` sont inchangées.

Les deux fichiers BIC protégés restent sur leur ancienne propriété. La loi
`activate_law = law_type:law_frontier_colonization` est préservée et
`law_colonial_exploitation` n'est pas restaurée. NAVY, ADMIN, MARATH, le stash,
les recherches technologiques non suivies, les localisations, descripteurs et
sauvegardes sont inchangés.

## 11. Validation documentaire et Git

Les quatre CSV ont été relus intégralement avec un véritable parseur :

| Registre | Lignes de données | Colonnes | Unicité requise |
|---|---:|---:|---|
| `HOTFIX_REPORT_INDEX.csv` | 154 | 22 | deux nouvelles identités 6A.24F/6A.25 présentes une fois |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | 55 | 17 | `block_id` uniques |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | 512 | 20 | chemins uniques ; aucune ligne perdue |
| `HOTFIX_6A25_GLOBAL_JE_PINNING_INVENTORY.csv` | 399 | 28 | occurrences chemin/ligne/classe uniques |

Les 126 lignes de remaining work correspondant à des fichiers corrigés et déjà
enregistrés pointent vers la preuve 6A.25. Les 12 fichiers corrigés requis pour
le merge sont `P1_RUNTIME_PENDING` et recommandent uniquement 6A.25Q. Aucun
fichier n'est déclaré pleinement terminé ni `ALREADY_MERGED` par ce sweep.

Le diff gameplay est exactement `129 files / 356+ / 356-`, `git diff --check`
est propre, l'index Git reste vide et le stash NAVY-3C-3 conserve son hash.

## 12. Phase suivante unique

La validation statique passe avec 14 exceptions bornées. La seule phase
sélectionnée est :

```text
HOTFIX_6A25Q_GLOBAL_JE_PINNING_1_13_RUNTIME_QA
```

Elle devra utiliser une seule ouverture humaine : manifeste complet des logs
avant/après, commit 6A.25 exact, fork exact monté sous `release/1.13.0`, partie
1776 neuve avec un pays témoin stable, aucune JE forcée, fermeture du jeu et du
launcher, extraction des seuls nouveaux segments, déduplication, comparaison
globale et par fichier des 355 diagnostics ciblés vers zéro, contrôle des
hashes gameplay et absence de nouvelle erreur attribuable au sweep. Aucun
comportement UI ne devra être revendiqué sans observation naturelle.

## 13. Verdicts

```text
HOTFIX_6A25_GLOBAL_JE_PINNING_1_13_ATOMIC_SWEEP_COMPLETE
GLOBAL_JE_PINNING_1_13_INVENTORY_COMPLETE
GLOBAL_JE_PINNING_LEGACY_API_BASELINE_CONFIRMED
GLOBAL_JE_PINNING_ATOMICITY_CLASSIFICATION_COMPLETE
GLOBAL_JE_PINNING_PROVEN_ATOMIC_MIGRATIONS_APPLIED
GLOBAL_JE_PINNING_BATCH_BYTE_INVERSION_PASS
GLOBAL_JE_PINNING_ONLY_PROPERTY_NAMES_CHANGED
GERMAN_UNIFICATION_FIVE_JE_PINNING_INCLUDED_IN_GLOBAL_SWEEP
HOTFIX_6A24F_SUPERSEDED_NOT_EXECUTED
AFGHANISTAN_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
POLAND_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
NON_PINNING_APIS_UNCHANGED
NO_RUNTIME_EXECUTED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A25Q_GLOBAL_JE_PINNING_1_13_RUNTIME_QA

LEGACY_PINNING_OCCURRENCES_BEFORE = 370
LEGACY_PINNING_OCCURRENCES_CORRECTED = 356
LEGACY_PINNING_OCCURRENCES_EXCEPTIONS = 14
LEGACY_PINNING_OCCURRENCES_AFTER = 14

TARGET_RUNTIME_PINNING_DIAGNOSTICS_BEFORE = 355
EXPECTED_TARGET_RUNTIME_PINNING_DIAGNOSTICS_AFTER = 0

GLOBAL_JE_PINNING_STATIC_MIGRATION_COMPLETE_WITH_BOUNDED_EXCEPTIONS
PINNING_SWEEP_EXCEPTIONS = 14
```
