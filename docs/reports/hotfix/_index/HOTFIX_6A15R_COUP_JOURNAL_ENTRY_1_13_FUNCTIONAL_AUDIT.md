# HOTFIX-6A.15R — Audit fonctionnel 1.13 de la journal entry Coup

## 1. Phase, date et verdict

- Phase : `HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT`
- Date : `2026-07-30`
- Nature : audit statique, documentaire et fonctionnel trois voies
- Verdict principal unique :
  `COUP_JOURNAL_ENTRY_PINNING_ISOLATABLE_ADJACENT_DELTAS_DEFERRED`
- Correction gameplay : aucune
- Runtime : non requis et non lancé

Le fork contient une erreur parser ciblée et reproductible dans
`je_ip4_coup`. La source hotfix et vanilla 1.13 convergent sur la propriété
moderne. Le remplacement est limité à une ligne, un fichier, un objet et un
hunk. Les différences de scopes, lobby, événements, lois, cooldown, cleanup et
invalidation sont fonctionnelles, beaucoup plus larges et indépendantes de ce
hunk. Elles sont donc auditées mais reportées.

La future phase sélectionnée est :

`HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT`

Elle est strictement bornée au pinning. Elle n'est pas exécutée ici.

## 2. Préflight Git

| Contrôle | Résultat |
| --- | --- |
| Racine | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| HEAD initial | `e32fda991c18fb6cf12d768d450463ca6a05fc08` |
| Message HEAD | `Audit HBC duplicate country histories` |
| Index staged | vide |
| État suivi | propre |
| Non suivis | `?? bject`; `?? docs/research/technology/` |
| Processus Victoria 3 / dowser / Paradox | aucun |

`bject`, les sept fichiers de recherche technologique et le contenu du stash
n'ont pas été inspectés. Aucun reset, restore, checkout, clean, merge, rebase,
amend ou changement de stash n'a été exécuté.

## 3. Stash protégé

Avant audit :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Le même libellé et le même hash sont exigés au contrôle final.

## 4. Sources lues

Sources canoniques lues avant écriture :

- `HOTFIX_6A14H_HBC_DOUBLE_DEFINITION_RESOLUTION_AUDIT.md`;
- `HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT.md`;
- `HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`;
- `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv`;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`;
- `HOTFIX_MERGE_REMAINING_WORK.csv`;
- changelogs complets du fork et de la source.

Les rapports antérieurs non protégés trouvés par recherche de `Coup`, `coup`,
`putsch`, `01_coup` ou `je_ip4_coup` ont également été relus :
6A.4, 6A.5, 6A.6, 6A.7, 6A.7F, 6A.8R, 6A.10, 6A.10F, 6A.11, 6A.12,
6A.13 et la roadmap. Les rapports Inde qui contiennent un emploi générique du
mot ont été exclus conformément à la protection explicite Inde/BIC/Sepoy.

Le changelog source annonce les changements 2.3.0 mais aucun changement Coup.
Une égalité source/vanilla ne suffit donc pas à qualifier automatiquement un
choix de gameplay comme hotfix annoncé.

## 5. Validation des CSV

Les cinq CSV ont été lus avec `Import-Csv`, pas par découpage de chaînes.

| CSV | Lignes | Colonnes | Cellules structurelles vides |
| --- | ---: | ---: | --- |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | 39 | 17 | `canonical_report=4`, `canonical_commit=16`; autres `0` |
| `HOTFIX_REPORT_INDEX.csv` | 126 | 22 | `secondary_verdicts=42`, `superseded_by=119`, `predecessor=12`, `successor=17`, `companion_csv_path=78`; autres `0` |
| `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv` | 541 | 21 | tailles/hashes vides seulement lorsque le fichier est absent; `evidence=3`; autres champs structurels `0` |
| `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` | 534 | 22 | tailles/hashes vides seulement lorsque le fichier est absent; autres champs structurels `0` |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | 512 | 20 | `evidence_commit=511`; autres `0` |

En-têtes validés :

- block status : `block_id` à `notes`;
- report index : `phase_id` à `notes`;
- three-way inventory : `relative_path` à `notes`;
- global difference inventory : `relative_path` à `notes`;
- remaining work : `relative_path` à `notes`.

La recherche lexicale initiale trouvait deux lignes explicites :
`common/journal_entries/01_coup.txt` et
`events/iberia_events/ip4_coup_events.txt`. La jointure fonctionnelle ajoute
`events/agitators_events/coup_events.txt`, présent dans les trois inventaires
mais manqué par le motif à frontière de mot à cause de l'underscore.

Les trois fichiers sont `ALL_THREE_DIFFER` / `PENDING_REVIEW`. Les dépendances
vanilla uniquement ne figurent logiquement pas dans des inventaires de
différences fork/source. Le fichier égal fork/source
`common/scripted_progress_bars/01_mod76_progress_bars.txt` n'y figure pas non
plus. Il ne définit pas la barre Coup : son commentaire `From je_ip4_coup`
précède en réalité `je_qajar_coup_progress_bar`. C'est une référence textuelle
adjacente, non une dépendance exécutée.

## 6. Méthode de découverte

La recherche récursive a porté sur les identifiants Coup, la journal entry, les
événements, les pulses, les propriétés de pinning, les callbacks, les scopes,
les lobbies, les lois, le cooldown, les variables, les effets et les
entrypoints. Les localisations françaises protégées n'ont pas été rouvertes.
Seule la localisation anglaise vanilla nécessaire à la compréhension a été
consultée.

La chaîne effective est :

```text
on_action mensuel / décision / interaction / action diplomatique
  -> ip4_coup.1 ou ip4_coup.11
  -> je_ip4_coup
     -> je_ip4_coup_progress_bar
     -> ip4_coup.4 chaque semaine
     -> coup_pulse_events.1 à .10 chaque mois
     -> ip4_coup.2 au succès
     -> ip4_coup.3 à l'échec ou au timeout
  -> effets vanilla de victoire, lois, gouvernement et cleanup
```

## 7. Périmètre fonctionnel exact

Treize fichiers constituent la chaîne fonctionnelle ou ses entrypoints
directs. Trois sont overridés par le fork et la source; dix sont correctement
hérités de vanilla 1.13.

| Rôle | Fichier | Présence fork/source/vanilla |
| --- | --- | --- |
| principal | `common/journal_entries/01_coup.txt` | oui / oui / oui |
| événements principaux | `events/iberia_events/ip4_coup_events.txt` | oui / oui / oui |
| dix pulses et aftermath | `events/agitators_events/coup_events.txt` | oui / oui / oui |
| victoire, lois et cleanup | `common/scripted_effects/00_victoria_ip4_scripted_effects.txt` | non / non / oui |
| barre de progression | `common/scripted_progress_bars/00_ip4_victoria_progress_bars.txt` | non / non / oui |
| déclenchement mensuel | `common/on_actions/00_on_actions_monthly.txt` | non / non / oui |
| coup soutenu de l'étranger | `common/diplomatic_actions/57_orchestrate_coup.txt` | non / non / oui |
| raisons valides | `common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt` | non / non / oui |
| sauvegarde de la raison | `common/scripted_effects/00_victoria_ep2_scripted_effects.txt` | non / non / oui |
| types de lobby | `common/political_lobbies/00_political_lobbies.txt` | non / non / oui |
| interactions de personnage | `common/character_interactions/00_character_interactions.txt` | non / non / oui |
| interactions additionnelles | `common/character_interactions/01_additional_interactions.txt` | non / non / oui |
| coup dynastique Portugal | `common/decisions/ip4_portugal_decisions.txt` | non / non / oui |

Sept fichiers vanilla supplémentaires valident les définitions, sans porter de
delta Coup : quatre fichiers de lois, deux de modificateurs et
`common/script_values/event_values.txt`. La localisation nécessaire est
`localization/english/ip4_04_l_english.yml`. Aucun de ces fichiers ne doit être
copié dans le mod.

## 8. Hashes, tailles et intégrité des trois overrides

| Fichier | Arbre | Octets | SHA-256 |
| --- | --- | ---: | --- |
| `common/journal_entries/01_coup.txt` | fork | 2932 | `3AB98023990198A9871FAEE3CF459558B36FECC11B927F1FCF34982A39E5FB2F` |
| idem | source | 3074 | `F39D26651A3200B1044A2E79D070A8BFEEBB205183079A9BB993EF6D520C5665` |
| idem | vanilla | 2741 | `3E4705DFC02785CED86F9C5967CDDC0D5AC0E411E30974F82052ACD4004C7ACB` |
| `events/iberia_events/ip4_coup_events.txt` | fork | 15957 | `8DD5A07F60A3E1C623CF48495B062AFE0388602E256CBA8384CD8540067B5AD2` |
| idem | source | 19827 | `F806A772F86EB379EBC7ED05F7808A5B16C0CACFC0CD784E94B6AA1FB9C8C9D4` |
| idem | vanilla | 19955 | `22A7B94EE4A0CB4DA7C31DA2F488CEB845473EBDF44EB32ED649F56200886E92` |
| `events/agitators_events/coup_events.txt` | fork | 25485 | `88D1B0AE45F296A84FBB997C3F089423A2240790742291DDE359A9509DA5F3CE` |
| idem | source | 25870 | `AEE3D155D3C347AC5338468F5814CC5DAAFCBB9862E801D3287643587D525990` |
| idem | vanilla | 25652 | `F1CD65506555E45D1C08C27EAA96EE6939F94D313DC44DFC2B20DD4E3106CB7F` |

Les neuf fichiers sont UTF-8 BOM, LF, avec saut final et accolades
équilibrées :

- journal entry : fork `49/49`, source `56/56`, vanilla `48/48`;
- événements ip4 : `217/217`, `274/274`, `277/277`;
- pulses : `367/367`, `369/369`, `366/366`.

Les dix dépendances vanilla uniquement sont toutes UTF-8 BOM, LF et à accolades
équilibrées. Deux fichiers EP2 n'ont pas de LF final; les huit autres en ont
un. Il s'agit de leur état vanilla, non d'une anomalie créée par le mod.

## 9. Hashes des dépendances vanilla exécutées

| Fichier | Octets | SHA-256 |
| --- | ---: | --- |
| `00_victoria_ip4_scripted_effects.txt` | 52013 | `5F9A1C57060030102CBDC1F8C80E1C69E7BC115A259F9A82E9EE9F0D77FA73AD` |
| `00_ip4_victoria_progress_bars.txt` | 2585 | `DA2C2ACA01848A91B000739CD7A9E07B751E1EF8A5B31913C4ABEBF979F29DD1` |
| `00_on_actions_monthly.txt` | 4434 | `AFC9A539B7B0B11634AD2EA36055DAE61B6F8F8415B14CF8C1CB3F9E23D9DF23` |
| `57_orchestrate_coup.txt` | 10753 | `0C0CA9CF8095A067AE80F5ED2297D52BDD376E59E8B02711DF742E589039C3A6` |
| `00_ep2_victoria_scripted_triggers.txt` | 8794 | `E66A5223C367A2C137E09248239F61C916E4EE40D2F02EAFC8301722C05EEAB6` |
| `00_victoria_ep2_scripted_effects.txt` | 54784 | `59505B659A8292B58948BA5F9BDF41B7E1871A89C62FAB0F7B9F0C895D798DA5` |
| `00_political_lobbies.txt` | 44357 | `5018B2BEECAB24F1A7F361095CBE76EE90A2D22B4DC759B22235D7068B403091` |
| `00_character_interactions.txt` | 27137 | `9E85AD2B353F730F4CDB9DD57C0A7709E31D171CEF7743468E354D2BDA09E832` |
| `01_additional_interactions.txt` | 28391 | `742334173B75F83592797D6A6A74BCB1A1631DF601E39C63C24EC61C15503142` |
| `ip4_portugal_decisions.txt` | 7814 | `ACE9D665053F76B403F6F561966C92B58C9C9EE88F68D31BCC201DC20A1C2257` |

Ils ont `0` hunk fork/source : aucun override n'existe. Leur comparaison
fork/vanilla est « héritage vanilla », pas une proposition d'ajout complet.
Aucune copie source inutile et identique à vanilla n'a été trouvée dans cette
chaîne.

## 10. Objets et statistiques de diff

| Fichier | Objets | fork → source | fork → vanilla |
| --- | --- | --- | --- |
| `01_coup.txt` | `je_ip4_coup` | 5 hunks, `40+/25-` | 5 hunks, `29+/25-` |
| `ip4_coup_events.txt` | `.1`, `.2`, `.3`, `.4`; source/vanilla ajoutent `.11` | 19 hunks, `265+/84-` | 19 hunks, `249+/58-` |
| `coup_events.txt` | pulses `.1`–`.10`, aftermath `.1`–`.4` | 11 hunks, `18+/13-` | 8 hunks, `13+/13-` |

Source → vanilla :

- journal entry : 4 hunks, `0+/11-`;
- événements ip4 : 6 hunks, `30+/20-`;
- pulses : 6 hunks, `1+/6-`.

Un remplacement complet de l'un de ces fichiers est interdit.

## 11. Audit du pinning 1.13

Fork, ligne 139 :

```txt
should_be_pinned_by_default = yes
```

Source, ligne 154, et vanilla 1.13, ligne 143 :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

Résultat :

- ancienne forme dans l'objet : 1 occurrence, 1 fichier;
- forme moderne dans l'objet fork : 0;
- source et vanilla convergent exactement;
- diagnostic ciblé : 1 par chargement concerné;
- correction théorique : 1 fichier, 1 objet, 1 hunk, `1+/1-`;
- aucune ligne de scope, événement, lobby, loi ou lifecycle dans le hunk.

Le hash théorique après substitution byte-preserving est :

`37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602`

Taille théorique : `2954` octets. BOM UTF-8, LF, saut final, indentation et
accolades sont préservés.

Rollback chirurgical :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

vers :

```txt
should_be_pinned_by_default = yes
```

Le rollback doit restaurer exactement
`3AB98023990198A9871FAEE3CF459558B36FECC11B927F1FCF34982A39E5FB2F`.

Classification : `VANILLA_1_13_ALIGNMENT_REQUIRED`.

## 12. Audit des scopes

| Delta | Fork | Source / vanilla | Effet et risque | Classification |
| --- | --- | --- | --- | --- |
| propriétaire | `root` pays de la JE | identique | aucun delta | `ALREADY_MERGED` |
| meneur | `golpista_var` puis `golpista_general` | même base, sélection modernisée | source/vanilla exigent loyauté, raison valide et APIs de rôle 1.13 | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| groupe d'intérêt | scope sauvegardé depuis le personnage | accès optionnel `interest_group ?=` | évite un scope invalide; changement fonctionnel hors pinning | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| loi en cours | absent dans la JE fork et dans son `.1` | `current_law_scope` sauvegardé | alimente les descriptions de raison; l'effet de victoire teste encore la loi en cours live | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| loi désirée | `coup_desired_law` déjà sauvegardée dans `.2` | identique | activation dynamique déjà effective via l'effet vanilla | `ALREADY_MERGED` |
| lobby/pays cible | absents | `relevant_lobby`, `coup_lobby_country`, `coupist_lobby_country` | requis pour le coup soutenu de l'étranger; gameplay distinct | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| sponsor | effet vanilla présent mais `.11` fork absent | chaîne `.11` complète | le fork hérite d'un entrypoint qui vise un événement absent de son override | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| variables de localisation source | absentes | trois `coup_loc_*_var` source seulement | jamais lues dans les scripts/localisations trouvés et absentes de vanilla | `OBSOLETE_HOTFIX_CONTENT` |
| scopes inexistants | pas de gate IG; personnage traité partiellement | source invalide si IG/personnage absent; vanilla ne reprend pas ces deux gates | nettoyage défensif source-only, non convergent | `UNKNOWN_REQUIRES_REVIEW` |

Le pays changeant de gouvernement n'invalide pas automatiquement la JE dans
les trois versions. `transferable = no` et `can_revolution_inherit = no` sont
identiques. Aucun de ces scopes n'est nécessaire au remplacement du pinning.

## 13. Audit des lobbies

Identifiants :

- `lobby_pro_country`;
- `lobby_pro_overlord`;
- variable de lobby `coup_lobby`;
- scopes `relevant_lobby`, `coup_lobby_country`,
  `coupist_lobby_country`;
- sponsor pays `coup_sponsor`.

Les types et les APIs `random_political_lobby`,
`is_political_lobby_type`, `target`, `every_political_lobby` sont utilisés par
vanilla 1.13 et leurs définitions existent. L'action
`orchestrate_coup` choisit un lobby pro-pays/pro-suzerain, sauvegarde le
sponsor et appelle `create_coup_event_from_character`, qui déclenche
`ip4_coup.11`.

Le fork override `ip4_coup_events.txt` sans définir `.11`. Sa chaîne locale ne
pose donc jamais `coup_lobby`, alors que l'effet vanilla hérité la lit. Cela
explique le warning « used but never set ».

Source et vanilla ajoutent `.11`; l'événement reste fonctionnel si aucun lobby
n'est trouvé : les blocs aléatoires ne produisent simplement aucun scope, la
description `.2` revient à son fallback et le cleanup `every_political_lobby`
est vide. Le contenu localisé propre à `.11` exige cependant le scope
`relevant_lobby`; la création normale par l'action diplomatique le fournit.

La restauration de `.11` et de sa chaîne modifierait le gameplay et ne fait
pas partie de 6A.15F. Classification :
`VANILLA_1_13_ALIGNMENT_REQUIRED`.

## 14. Audit des lois

| Loi | Usage | Groupe | Existe en 1.13 | Lecture 1776 |
| --- | --- | --- | --- | --- |
| `law_parliamentary_republic` | évite un remplacement de dirigeant direct | `lawgroup_governance_principles` | oui | plausible selon pays |
| `law_presidential_republic` | idem | `lawgroup_governance_principles` | oui | plausible selon setup |
| `law_council_republic` | idem | `lawgroup_governance_principles` | oui | anachronique en 1776 mais normalement verrouillée |
| `law_corporate_state` | idem | `lawgroup_governance_principles` | oui | anachronique en 1776 mais normalement verrouillée |
| `law_colonial_administration` | idem | `lawgroup_governance_principles` | oui | pertinent pour compagnies; aucune histoire HBC/BIC modifiée |
| `law_autocracy` | activée pour certains coups dynastiques avec franchise | `lawgroup_distribution_of_power` | oui | plausible |
| `law_secret_police` | permet l'option punitive de `.3` | `lawgroup_internal_security` | oui | condition seulement |
| `law_outlawed_dissent` | permet l'option punitive de `.3` | `lawgroup_free_speech` | oui | condition seulement |

L'effet `ip4_coup_victory_law_effects` peut :

1. annuler une loi en cours si le groupe putschiste ne l'approuve pas;
2. activer `scope:coup_desired_law.type`;
3. sinon choisir la première loi préférée, disponible et valide pour une
   pétition.

Il ne restaure aucune loi précédente. Ce mécanisme est déjà exécuté dans le
fork parce que l'effet est hérité de vanilla et que `coup_desired_law` est déjà
sauvegardée. La source ne remplace aucun identifiant de loi fixe dans le hunk
de pinning. Les verrous `law_is_available` et
`law_is_valid_for_ig_petition` limitent les options anachroniques.

Aucune loi protégée n'est changée. BIC et
`law_frontier_colonization` restent hors périmètre.

Classification du mécanisme déjà présent : `ALREADY_MERGED`. Les scopes de
raison/loi manquants restent `VANILLA_1_13_ALIGNMENT_REQUIRED`, hors 6A.15F.

## 15. Cooldown

`short_modifier_time` vaut `913` jours, soit 2,5 ans.

Fork :

- pose `coup_cooldown_var` directement dans `on_complete`, `on_fail`,
  `on_timeout` et `on_invalid`;
- l'événement `.4` utilise un cooldown distinct
  `ip4_coup_4_var = short_modifier_time`;
- l'entrypoint `.1` bloque si `coup_cooldown_var` existe.

Source/vanilla :

- retirent les quatre poses locales de la JE;
- délèguent à `ip4_coup_cleanup_effects`, qui pose la même variable pour la
  même durée;
- le moment exact passe de la fermeture de JE à la résolution/cleanup de
  l'événement;
- le cooldown `.4` reste inchangé.

Il n'y a pas de changement de durée, mais un changement de placement et de
lifecycle. Classification : `VANILLA_1_13_ALIGNMENT_REQUIRED`, hors pinning.

## 16. Cleanup

Fork :

- retire manuellement `golpista_var` et `golpista_ig_var` dans plusieurs
  branches;
- retire `coup_event_active` après `.2`;
- ne nettoie pas systématiquement lobby, sponsor, raison, pacte, modificateur
  dynastique ou commande pour le joueur;
- `.3` n'a pas d'`after` cleanup;
- `on_invalid` ne fait que poser le cooldown.

Source/vanilla :

- délèguent les chemins de succès, d'échec et d'invalidation à
  `ip4_coup_cleanup_effects`;
- retirent `coup_event_active`, `coup_lobby`, `golpista_ig_var`,
  `coup_sponsor`, `orchestrate_coup_aborted`, `coup_reason_var`,
  `golpista_var`, `commander_doing_coup_on_player_behalf` et le modificateur
  dynastique;
- retirent si nécessaire le pacte diplomatique `orchestrate_coup`;
- posent le cooldown commun.

Le cleanup moderne est nécessaire à la chaîne foreign-backed complète, mais
son adoption changerait le comportement et plusieurs branches. Classification :
`VANILLA_1_13_ALIGNMENT_REQUIRED`, hors 6A.15F.

## 17. Invalidation et risques de blocage

Commun :

- échec à progression `<= 0`;
- échec si le général meurt ou part en exil;
- succès à `>= 120`;
- timeout à `730` jours;
- `.4` hebdomadaire et dix pulses mensuels;
- aucune gate autonome `is_shown_when_inactive` ou `possible`.

Fork :

- invalide seulement si le général a `modifier_preempetive_coup`;
- ne détecte pas explicitement la disparition du groupe;
- peut garder la JE jusqu'au timeout si le scope IG disparaît;
- des variables temporaires peuvent survivre jusqu'à leur durée ou au
  cooldown, sans preuve de boucle infinie.

Vanilla :

- ajoute l'invalidation si le groupe est sécessionniste;
- délègue le cleanup.

Source :

- ajoute encore l'invalidation si le groupe ou le personnage n'existe plus;
- c'est une protection défensive source-only, non convergente avec vanilla.

Le cooldown de 913 jours empêche une répétition immédiate. Aucune boucle
infinie certaine n'est démontrée, mais le fork présente un risque de JE
stagnante jusqu'au timeout et de variables orphelines. Les ajouts partagés sont
`VANILLA_1_13_ALIGNMENT_REQUIRED`; les deux gates d'existence source-only sont
`UNKNOWN_REQUIRES_REVIEW`.

## 18. Autres deltas d'événements

Les logs et les diffs prouvent des alignements API distincts :

- `has_role` vers `has_role_of_type`;
- `is_ruler` vers `is_ruler_of_own_country`;
- accès IG optionnel;
- validation du personnage;
- raisons de coup et loyauté;
- ajout de `.11`.

Ils sont `VANILLA_1_13_ALIGNMENT_REQUIRED`, mais aucun n'est requis pour
parser la propriété de pinning.

Les différences source-only suivantes ne convergent pas avec vanilla :

- tri par `commander_coup_strength` au lieu de popularité;
- résistance basée sur la force du commandant au lieu de légitimité/part
  d'unités;
- `ROOT.capital`;
- radicaux basés sur le rang;
- `exile_character_with_role_cleanup`;
- exclusion des héritiers, retrait du rôle au lieu de retraite et exclusions
  culturelles dans les pulses/aftermath.

Elles sont `UNKNOWN_REQUIRES_REVIEW`. Elles ne peuvent pas entrer dans une
correction de pinning.

## 19. Diagnostics existants

Soixante fichiers `.log` courants et rotations ont été recherchés sans lancer
le jeu. Manifest initial :

`371617A56B249AB820A2ACABB99387D4DA5F055B691B99117AB2090A2568399E`

| Diagnostic | Total | Logs |
| --- | ---: | --- |
| tous `Unexpected token: should_be_pinned_by_default` | 1122 | `debug.1.log`, `debug.3.log`, `debug.5.log`, 374 chacun |
| pinning propre à `01_coup.txt:139` | 3 | mêmes logs, 1 chacun |
| `PostValidate has_role` dans `ip4_coup_events.txt` | 24 | mêmes logs, 8 chacun |
| diagnostics `coup_events.txt` | 24 | mêmes logs, 8 chacun : 6 `is_ruler`, 2 `has_role` |
| warning `coup_lobby` jamais posé | 3 | `debug.3.log`, `debug.5.log`, `debug.log` |
| identifiants `ip4_coup.N` écrits comme erreurs | 0 | aucun |
| lois Coup ci-dessus écrites comme erreurs | 0 | aucun |

Ligne représentative :

```text
Error: "Unexpected token: should_be_pinned_by_default, near line: 139" in file: "common/journal_entries/01_coup.txt" near line: 139
```

Les huit erreurs `ip4_coup_events.txt` pointent les anciens `has_role` aux
lignes 30, 31, 56, 57, 321, 332, 426 et 432. Les pulses signalent les anciens
`is_ruler` aux lignes 30, 41, 967, 1062, 1171 et 1253, plus `has_role` aux
lignes 29 et 40.

La baseline avant future correction reste `374` diagnostics legacy dans
`140` fichiers. 6A.15F ne devrait en retirer qu'un; ce résultat devra être
prouvé séparément et ne résoudra pas les diagnostics d'événements.

## 20. Cohérence 1776

Un coup militaire, une opposition de groupes d'intérêt, un changement
dynastique et un soutien étranger sont plausibles en 1776 comme abstractions.
Les lois modernes potentiellement anachroniques restent filtrées par leur
disponibilité; aucune n'est activée au démarrage par cet audit.

L'intégration moderne des lobbies, les raisons de coup et les formules de force
modifient néanmoins la fréquence, l'éligibilité et l'issue des coups. Ce sont
des choix fonctionnels, pas des prérequis au pinning. Leur équilibre 1776 ne
peut pas être décidé par une substitution syntaxique.

## 21. Classification exclusive des deltas

| Groupe de delta | Classification unique |
| --- | --- |
| propriété de pinning de `je_ip4_coup` | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| APIs `has_role` / `is_ruler` des deux fichiers d'événements | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| `.11`, sponsor, lobby et scopes associés | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| raison, loyauté, immunité, loi en cours et accès IG optionnel | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| cleanup partagé, cooldown déplacé, invalidation sécessionniste | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| loi désirée et effets vanilla de victoire déjà actifs | `ALREADY_MERGED` |
| dix dépendances vanilla héritées et définitions de lois/modificateurs | `ALREADY_MERGED` |
| commentaire trompeur de `01_mod76_progress_bars.txt` | `ALREADY_MERGED` |
| trois variables de localisation source-only jamais lues | `OBSOLETE_HOTFIX_CONTENT` |
| invalidation source-only des scopes inexistants | `UNKNOWN_REQUIRES_REVIEW` |
| formules, tri, capitale, radicaux et exil source-only | `UNKNOWN_REQUIRES_REVIEW` |
| deltas source-only des pulses/aftermath | `UNKNOWN_REQUIRES_REVIEW` |

Aucun delta Coup n'est classé `PROTECTED_CONCURRENT_WORK`. Les périmètres
protégés n'ont pas été inspectés ou modifiés.

## 22. Décision sur 6A.15F

Les conditions d'une correction bornée sont toutes satisfaites pour le
pinning seulement :

1. fichier exact et hash initial connus;
2. erreur parser réelle;
3. convergence source/vanilla;
4. hunk minimal `1+/1-`;
5. hash cible reproductible;
6. aucune dépendance HBC, NAVY, BIC, Inde, Amérique ou autre scope protégé;
7. aucune modification de scope, lobby, loi, cooldown ou cleanup;
8. rollback exact;
9. aucun remplacement complet.

`HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT` est donc sélectionnée avec
un périmètre fermé à `common/journal_entries/01_coup.txt`, objet
`je_ip4_coup`, propriété de pinning uniquement.

Les deux fichiers d'événements restent en audit ultérieur non sélectionné.

## 23. Documents écrits

6A.15R est autorisée à écrire uniquement :

1. ce rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun fichier gameplay n'est écrit.

## 24. Contrôles finaux

| Contrôle | Résultat |
| --- | --- |
| Branche | `hotfix-dlc-audit` |
| HEAD final | `e32fda991c18fb6cf12d768d450463ca6a05fc08` |
| Index staged | vide |
| `git diff --check` | PASS |
| Stash | `518df704fa14599c0f254fae13859210663dd976` |
| Manifest des logs | `371617A56B249AB820A2ACABB99387D4DA5F055B691B99117AB2090A2568399E` |
| Gameplay | aucun changement |
| Runtime | aucun |
| Commit automatique | aucun |

Le HEAD initial et final est identique. L'état final contient les six documents
de phase, plus uniquement les deux chemins non suivis protégés déjà présents.
Les trois hashes gameplay Coup sont strictement inchangés. Les CSV finaux sont
valides avec `127 × 22` et `40 × 17`; les doublons de clés historiques `S` et
`INDEX` du report index préexistaient et la nouvelle clé 6A.15R est unique.

## 25. Verdicts finaux

```text
HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT_COMPLETE
COUP_JOURNAL_ENTRY_THREE_WAY_COMPARISON_COMPLETE
COUP_PINNING_SCOPE_LOBBY_LAW_COOLDOWN_AUDITED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
COUP_JOURNAL_ENTRY_PINNING_ISOLATABLE_ADJACENT_DELTAS_DEFERRED
NEXT_EXECUTION_PHASE = HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT
```
