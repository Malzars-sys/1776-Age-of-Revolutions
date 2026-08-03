# HOTFIX 6A.17R — Audit fonctionnel 1.13 d'Imperialism of Promise

Date : 2026-08-04

Phase : `HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT`

## 1. Résultat

L'objet `je_imperialism_of_promise` a été audité en lecture seule dans le fork,
la source hotfix et vanilla 1.13. Les trois différences principales sont bien
séparables statiquement : vivier de personnages, tooltip de bureaucratie et
pinning. Elles ne forment pas une correction unique.

Aucune correction future n'est sélectionnée. Le dernier runtime survivant ne
reproduit aucun diagnostic parser ou PostValidate attribuable au fichier cible.
Les deux erreurs `has_role` ne subsistent que dans une rotation ancienne et la
preuve du pinning est uniquement historique/statique. Les quatre avertissements
actuels « already has a journal entry » appartiennent à des transferts massifs
de journal entries vers des révoltes et ne prouvent aucun défaut propre à cet
objet.

## 2. État d'entrée et preflight

| Contrôle | Résultat |
| --- | --- |
| Racine | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| HEAD initial | `4ae07bef5c1f81787a36eff629cc393e1166cda8` |
| Message | `Select Imperialism of Promise functional audit` |
| Rapport 6A.17 dans HEAD | présent; 12 verdicts requis présents exactement une fois |
| Changements suivis initiaux | aucun |
| Index staged | vide |
| Non suivis | uniquement `bject` et sept recherches technologiques protégées |
| `git diff --check` | PASS |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Objet stash | `518df704fa14599c0f254fae13859210663dd976` |
| Processus | 0 Victoria 3, 0 Dowser, 0 chemin `Paradox Interactive\launcher`; Ankama ignoré |

`bject`, les sept recherches technologiques et le contenu du stash n'ont pas
été ouverts, modifiés, stagés, déplacés ou supprimés.

## 3. Sources lues

Ont été lus intégralement : 6A.17, 6A.16R, 6A.16, 6A.15R, 6A.15F, la
roadmap, la matrice des blocs, l'index des rapports, les trois inventaires
globaux, le prompt courant, les deux changelogs, les trois versions complètes
du fichier cible et les logs courants/rotations pertinents.

Les CSV ont été chargés avec `Import-Csv`, jamais découpés sur les virgules.
Les frontières BIC/Inde/Sepoy ont été établies depuis la clôture canonique Inde,
la validation finale Sepoy et son retest API. Aucun fichier gameplay BIC ou
Inde n'a été ouvert. Les événements utilitaristes n'ont pas été ouverts : leur
carte ci-dessous est limitée aux appels et scopes visibles dans l'objet audité.

## 4. Preuves trois voies

| Arbre | Octets | Lignes | SHA-256 |
| --- | ---: | ---: | --- |
| Fork | 2912 | 142 | `80E38C181A5AEB547E8F98EBFD03844F3522CADC59426D9FC16588B908105C3B` |
| Source hotfix | 3182 | 151 | `F97A929A3CC9FAA98A8CE3824A4A6196866AFBA18A89E477600DDA230153D7FC` |
| Vanilla 1.13 | 3143 | 150 | `AB08635DC8EAA5C3A1523F70693BADB58A607576B06C5EF979E682008B0D4C0C` |

Les valeurs recalculées correspondent exactement aux preuves d'entrée.

## 5. Validation structurelle

Les trois fichiers sont du texte UTF-8 avec BOM `EF BB BF`, fins de ligne LF,
aucun CRLF ni CR isolé et saut final présent. Chacun contient un seul objet
racine. Les accolades sont équilibrées : fork `42/42`, source `44/44`, vanilla
`44/44`.

L'ordre des 18 propriétés de premier niveau est identique jusqu'à la dernière :
`icon`, `group`, `is_shown_when_inactive`, `possible`, `immediate`, `complete`,
`fail`, `invalid`, `on_complete`, trois descriptions d'issue avec leurs hooks,
`on_yearly_pulse`, `timeout`, `weight`, puis le pinning. Seul le nom de cette
dernière propriété diffère dans le fork.

## 6. Diff complet et numstat

| Comparaison | Numstat | Hunks | Lignes fonctionnelles | Objet |
| --- | --- | ---: | --- | --- |
| Fork → source | `14+/5-` | 3 | fork 18–19, 38–39, 140 | `je_imperialism_of_promise` |
| Fork → vanilla | `13+/5-` | 3 | fork 18–19, 38–39, 140 | même objet |
| Source → vanilla | `1+/2-` | 2 | source 20 et espace avant pinning | même objet |

Le `14+` source, contre `13+` vanilla, vient du rôle IG source-only. La seconde
différence source/vanilla est uniquement un blanc. Aucun remplacement complet
du fichier n'est justifié.

Répartition des hunks fork → source/vanilla :

1. lignes 15–25 environ : API de rôles **et** changement de vivier; hunk API +
   gameplay, avec scopes personnage, rôles et prominence;
2. lignes 35–49 environ : enveloppe `custom_tooltip`; hunk d'interface, sans
   modification des deux triggers internes;
3. fin de fichier : propriété de pinning; hunk d'interface/chargement `1+/1-`,
   indépendant des scopes, rôles, lois et progression.

Il n'existe aucun hunk de géographie, de progression, de loi ou de condition
d'échec dans ces diffs. Les dépendances protégées sont appelées par le contenu
identique, mais ne sont pas modifiées par les trois hunks.

## 7. Dernier runtime survivant

Le dernier runtime du 3 août 2026 est réparti entre `error.1.log`, `error.log`
et `game.log` : session visible de 19:13:35 à 19:48:33, avec rotation d'erreur
à 19:42:35.

| Signal cible | `error.1.log` | `error.log` | `game.log` | Statut |
| --- | ---: | ---: | ---: | --- |
| chemin `04_imperialism_of_promise.txt` | 0 | 0 | 0 | aucun diagnostic actuel attribué |
| ancien pinning | 0 | 0 | 0 | non reproduit |
| `has_role` lignes 18/19 | 0 | 0 | 0 | non reproduit |
| warning JE déjà présente | 4 | 0 | 4 miroirs | 4 occurrences uniques, génériques |

Le manifeste en lecture seule des 60 logs au début de l'audit est
`44D5DC1416711339F6B18E54D7E73C7C7967219197E986D09FE4CAE02504C219`.

## 8. Rotation ancienne et preuve historique

`game.3.log`, session du 2 août 2026 de 18:39:50 à 18:41:06, contient :

| Log / ligne | Heure | Message | Chemin / ligne | Objet | Statut |
| --- | --- | --- | --- | --- | --- |
| `game.3.log:3540` | 18:40:58 | `has_role` : objet `agitator` invalide | cible :18 | condition `possible` | rotation ancienne, lien prouvé |
| `game.3.log:3544` | 18:40:58 | `has_role` : objet `politician` invalide | cible :19 | condition `possible` | rotation ancienne, lien prouvé |

La recherche des logs survivants ne trouve aucune chaîne de pinning et aucun
chemin cible associé à ce diagnostic. Les rapports 6A.16/6A.17 conservent la
preuve publiée d'un ancien diagnostic de pinning. Les trois diagnostics
historiques documentés sont donc : un pinning publié mais non survivant, plus
les deux `has_role` encore présents dans `game.3.log`. Ils ne sont pas actuels.

## 9. Avertissements de révolution

Les quatre occurrences uniques actuelles sont : Salvador libéral à 19:20:19,
Pérou du Nord paysan à 19:20:56, Hadiya esclaves à 19:32:07 et Bolivie libérale
à 19:41:36. Elles sont dupliquées entre `error.1.log` et `game.log`; elles ne
doivent pas être comptées comme huit.

À chacun de ces horodatages, le journal manager émet respectivement 135, 133,
136 et 135 avertissements du même type pour des JE très diverses, de
`je_sale_of_alaska` à `je_zaibatsu`. Le message ne fournit ni chemin, ni ligne,
ni hunk du fichier cible. Le lien avec l'objet est nominal seulement. La cause
la mieux étayée est le transfert générique d'un ensemble de journal entries
lors de la création d'une révolte, pas une erreur fonctionnelle propre à
`je_imperialism_of_promise`.

## 10. Audit du pinning

Fork ligne 140 : `should_be_pinned_by_default = yes`. Source ligne 149 et
vanilla ligne 148 :
`should_be_pinned_by_default_uninvolved_or_context = yes`.

La convergence source/vanilla est exacte et la substitution est isolable en un
hunk `1+/1-`. Elle ne change pas l'activation, les scopes ou la progression;
elle change le comportement de pinning/présentation pour un pays non impliqué
ou dans le contexte prévu par l'API 1.13. Le candidat byte-preserving donne :

```text
future_size = 2934
future_sha256 = EF5200E0B9E7A58AF904C73CDD82F3CC4009FFE0CA9364952F793AB4F3E2A682
```

Rollback exact : remplacer la propriété moderne par l'ancienne; le résultat
doit restaurer `2912` octets et le hash fork initial. Un smoke de chargement
pourrait vérifier l'acceptation parser sans déclencher les événements BIC;
valider la visibilité fonctionnelle exige toutefois un contexte BIC/sujet. En
l'absence de diagnostic actuel, aucune 6A.17F n'est autorisée.

## 11. Agitator et politician

Le scope est chaque personnage parcouru par `any_scope_character`. La
condition d'idéologie utilitariste reste extérieure à l'OR dans les trois
versions et s'applique donc à tout personnage retenu.

- `agitator` : source et vanilla convergent exactement sur
  `has_role_of_type = agitator`. La substitution isolée est `1+/1-`, ne touche
  aucune condition voisine et conserve le rôle fonctionnel visé.
- `politician` : source et vanilla convergent exactement sur
  `has_role_of_type = politician`, mais placent ce test dans un `AND` avec le
  seuil de prominence. La seule modernisation de la ligne est isolable; copier
  le bloc source/vanilla ne l'est pas, car cela restreint le vivier.

Hashes théoriques byte-preserving :

| Candidat | Taille | SHA-256 |
| --- | ---: | --- |
| agitator seulement | 2920 | `81D67A3A686326207297ACCFC67B3C18F13CC3A41828786F66C720C30EB9EC10` |
| politician API seulement | 2920 | `E917604F8EEE5A814D616B83F4901B67B6487F925D71CB2F4836B835F7BE0F82` |
| les deux API seulement | 2928 | `2341D61C0FE08F44EE49DC0466B52824360E3BA664AC0AE235CA0A2F8FB540EF` |

Le rollback remet chaque `has_role_of_type` en `has_role` sur la même ligne et
doit restaurer le hash fork. Ces candidats n'ont aucun diagnostic actuel.

## 12. Ruler, chef IG, prominence et vivier

Le rôle `ruler` est ajouté par source et vanilla. Ce n'est pas une simple
correction d'API : il rend éligible un dirigeant utilitariste même s'il n'est ni
agitateur ni politicien selon la branche du fork.

`character_role_ig_leader` est un identifiant valide en 1.13 : vanilla le
définit dans `common/character_roles/01_appointment_roles.txt`, type
`politician`, et l'ajoute/retire dans un scripted effect. Sa syntaxe spécifique
`has_role = character_role_ig_leader` est donc distincte de l'ancienne forme
erronée `has_role = politician`. Il n'existe aucune occurrence dans le périmètre
fork non protégé recherché. La source l'ajoute ici, mais vanilla l'omet de cet
objet. Les changelogs parlent de changements New Imperialism et de personnages
historiques BIC, jamais de cet élargissement précis. Sa validité technique ne
prouve donc ni son intention pour le mod ni son équilibre 1776.

Le seuil `PROMINENCE_IMPORTANT_THRESHOLD` est commun à source et vanilla. Il
n'est pas requis par `has_role_of_type`; il rend seulement les politiciens
importants éligibles. C'est un changement fonctionnel de disponibilité et
d'équilibrage.

Vivier exact, toujours avec idéologie utilitariste :

- fork : agitateur **ou** politicien;
- vanilla : ruler **ou** agitateur **ou** politicien dont la prominence atteint
  le seuil important;
- source : vivier vanilla **ou** détenteur du rôle spécifique de chef IG.

Le bloc rôle complet au format vanilla donnerait 3049 octets et
`DE14DEE3FA2DCC858C5ABEFE2AE2347C12AB1F2353A09EFFDCAA33559A173BF1`;
le bloc source donnerait 3090 octets et
`EF5EBA438B1213F1808C03A85C08A78C4C254499707AD0C2BFBAB7B84DFAE672`.
Ces hashes décrivent des variantes de gameplay, pas des correctifs autorisés.

## 13. Tooltip de bureaucratie

Le fork exécute déjà `bureaucracy >= 0` et
`approaching_bureaucracy_shortage = no`. Source et vanilla les enveloppent dans
un `custom_tooltip` nommé `bureaucrats_no_shortage_trigger`. Dans un bloc de
triggers, les deux sous-conditions restent évaluées : le delta observé change
la présentation groupée du critère, pas sa vérité logique.

Aucun diagnostic actuel ou historique ciblé ne concerne ce tooltip. La
convergence source/vanilla est exacte mais ne suffit pas à sélectionner un
hunk. Le candidat tooltip seul ferait 2981 octets, hash
`82C894F75AD127FE44ECACA55C54958BFF6DEC2312DBDFDC3BE828CC49048164`;
son rollback enlève seulement l'enveloppe et restaure les deux lignes fork.

## 14. Visibilité et dépendances protégées

`is_shown_when_inactive` est identique : DLC `ip2_content`, pays `BIC` égal au
pays courant et sujet `subject_type_chartered_company`. L'objet n'est donc pas
une JE générale pour tous les sujets; sa visibilité inactive dépend du pays BIC
et du type de sujet. Le pinning moderne affecterait sa présentation pour
non-impliqué/contexte, sans modifier ces trois gates.

`immediate` sauvegarde `c:BIC` sous `BIC_scope`, sauvegarde
`ig:ig_industrialists` sous `industrialists_ig`, puis appelle `utilitarian.9`.
Les trois versions sont identiques. La clôture Inde confirme que BIC, Sepoy,
Bombay, Travancore, régions et géographie sont clos et protégés. Cette phase ne
les rouvre pas. BIC conserve notamment la loi de colonisation de frontière;
aucune loi BIC n'a été inspectée ou modifiée.

## 15. Échec, progression, lois et géographie

Les blocs suivants sont identiques dans les trois versions :

- réussite : niveau de vie moyen 10, bureaucratie non négative, aucune pénurie,
  droits des femmes, écoles obligatoires/publiques, abolition de l'esclavage et
  fiscalité proportionnelle ou graduée;
- échec : `BIC_scope` porte `je_sepoy_mutiny`, variable `bic_collapse_var`, ou
  guerre civile dont le mouvement est culturel minoritaire;
- invalidation : BIC n'existe plus ou la culture primaire n'est plus britannique;
- timeout : 10950 jours; poids 100; variable `utilitarianism_done` posée sur les
  trois issues;
- géographie : aucun identifiant géographique direct dans l'objet.

La chaîne Sepoy est close et validée séparément, mais son activation organique
1776 et ses scénarios territoriaux ont leurs propres gardes. L'appel depuis
cette JE reste une dépendance protégée, pas une autorisation de rouvrir le
gameplay Inde.

## 16. Événements utilitaristes

Carte prouvable depuis l'objet audité :

| Entrée | Appel |
| --- | --- |
| `utilitarian.9` | immédiat, popup, après sauvegarde de `BIC_scope` et `industrialists_ig` |
| `.1` | réussite; puis `utilitarianism_done` |
| `.2` | échec; puis `utilitarianism_done` |
| `.3` | timeout; puis `utilitarianism_done` |
| `.4`, `.5`, `.6`, `.7`, `.10` | tirages annuels de poids 10; poids vide 100 |
| `.8` | commentaire : déclenché par le pulse d'adoption, pas par le pulse annuel |

Les effets internes, consommations de scopes et modifications de progression
ne peuvent pas être établis sans franchir la frontière gameplay protégée. Ils
restent donc protégés et inchangés; aucune conclusion supplémentaire n'est
inventée.

## 17. Matrice fonctionnelle — preuve et classification

| ID | Lignes fork/source/vanilla | Fork | Source | Vanilla | Convergence | Diag. actuel / historique | Scope / rôle | Effet gameplay | Dépendances / protection | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIN | 140/149/148 | ancien pinning | moderne | moderne | exacte S=V | 0 / 1 publié | objet JE | présentation/pinning | contexte BIC, code isolé | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| AGI | 18/19/19 | `has_role=agitator` | `has_role_of_type` | idem | exacte S=V | 0 / 1 rotation | personnage / agitator | restaure l'éligibilité visée | aucune ligne protégée | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| POL | 19/23/22 | `has_role=politician` | API moderne dans AND | idem | API exacte, structure couplée | 0 / 1 rotation | personnage / politician | API seule neutre; bloc restreint | prominence voisine | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| RUL | —/18/18 | absent | ruler | ruler | exacte S=V | 0 / 0 | personnage / ruler | élargit le vivier | choix design | `UNKNOWN_REQUIRES_REVIEW` |
| IGL | —/20/— | absent | rôle IG spécifique | absent | absente | 0 / 0 | personnage / chef IG | élargit source seulement | intention non documentée | `UNKNOWN_REQUIRES_REVIEW` |
| PRO | —/22/21 | absent | seuil important | idem | exacte S=V | 0 / 0 | personnage / politician | restreint les politiciens | équilibrage 1776 | `UNKNOWN_REQUIRES_REVIEW` |
| ORP | 17–20/17–25/17–24 | A ou P | R ou A ou IG ou P important | R ou A ou P important | partielle | 0 / 2 API | tout personnage utilitariste | change le vivier | rôles + prominence | `UNKNOWN_REQUIRES_REVIEW` |
| TIP | 38–39/43–47/42–46 | triggers directs | tooltip englobant | idem | exacte S=V | 0 / 0 | pays | affichage, logique conservée | localisation tooltip | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| VIS | 5–10 partout | DLC+BIC+chartered | identique | identique | exacte | 0 / 0 | pays BIC | visibilité inactive | BIC protégée | `ALREADY_MERGED` |
| BIC | 27–33 partout | scopes BIC/IG | identique | identique | exacte | 0 / 0 | BIC_scope, industrialists_ig | prépare `.9` | BIC protégée | `PROTECTED_CONCURRENT_WORK` |
| SEP | 52–73 partout | Sepoy/collapse/sécession | identique | identique | exacte | 0 / 0 | BIC + guerre civile | échec | Inde/Sepoy protégés | `PROTECTED_CONCURRENT_WORK` |
| GEO | aucune ligne directe | aucune clé | idem | idem | exacte | 0 / 0 | indirect | aucun delta local | Inde/Bombay/Travancore | `PROTECTED_CONCURRENT_WORK` |
| PRG | 35–50, 75–138 | progression/timeout/pulses | identique hors tooltip | identique | exacte logique | 0 / 0 | pays + JE | progression inchangée | événements externes séparés | `ALREADY_MERGED` |
| UTL | 31, 80–137 | `.1`–`.10` référencés | identique | identique | exacte | 0 / 0 | scopes sauvegardés | chaîne événementielle | gameplay protégé | `PROTECTED_CONCURRENT_WORK` |
| LAW | 40–49, 52–73 | lois + échec | identique | identique | exacte | 0 / 0 | pays/BIC | conditions identiques | Sepoy protégée séparément | `ALREADY_MERGED` |

Chaque groupe reçoit exactement une classification autorisée.

## 18. Matrice fonctionnelle — atomicité, hashes et décision

| ID | Hunk minimal théorique | Taille / SHA éventuels | Rollback | Correction atomique possible | Future phase possible | Sélection |
| --- | --- | --- | --- | --- | --- | --- |
| PIN | `1+/1-` | 2934 / `EF5200…A682` | propriété moderne → ancienne | oui, statiquement | non sans diagnostic actuel | non |
| AGI | `1+/1-` | 2920 / `81D67A…C10` | API moderne → ancienne ligne | oui | non sans diagnostic actuel | non |
| POL | `1+/1-` API seule | 2920 / `E91760…0F82` | API moderne → ancienne ligne | oui, séparé du seuil | non sans diagnostic actuel | non |
| RUL | ajout `1+` | inclus dans bloc vanilla | retirer la ligne | techniquement oui, fonctionnellement non prouvé | audit design seulement | non |
| IGL | ajout `1+` source-only | inclus dans bloc source | retirer la ligne | syntaxiquement oui, intention inconnue | audit design seulement | non |
| PRO | AND `4+/1-` avec politician | inclus dans bloc vanilla/source | restaurer politician direct | non comme correctif API | audit équilibre | non |
| ORP | bloc complet | 3049 / `DE14DE…BF1` ou 3090 / `EF5EBA…E672` | restaurer deux lignes fork | non atomique | audit design | non |
| TIP | enveloppe `5+/2-` | 2981 / `82C894…164` | retirer enveloppe | oui, présentation | non sans diagnostic/besoin prouvé | non |
| VIS | aucun | hash fork | aucun | sans objet | non | non |
| BIC | aucun hunk cible | non calculé | sans objet | non | phase protégée distincte seulement | non |
| SEP | aucun hunk cible | non calculé | sans objet | non | phase protégée distincte seulement | non |
| GEO | aucun | non calculé | sans objet | non | backlog protégé | non |
| PRG | aucun | hash fork | aucun | sans objet | non | non |
| UTL | aucun | non calculé | sans objet | non | phase protégée distincte seulement | non |
| LAW | aucun | hash fork | aucun | sans objet | non | non |

Les hashes abrégés de cette table sont donnés intégralement dans les sections
10 à 13. Tout rollback théorique byte-preserving doit restaurer le hash fork
`80E38C…05C3B`.

## 19. Réponses aux quinze questions obligatoires

1. Non, le pinning n'a aucun diagnostic dans le dernier runtime.
2. Sa preuve est historique publiée et statique; elle n'est pas actuelle.
3. Oui, sa ligne peut être substituée sans toucher un autre groupe.
4. Oui, les deux `has_role` subsistent dans `game.3.log`, rotation ancienne.
5. Oui, agitator converge exactement sur `has_role_of_type = agitator`.
6. Oui, politician converge exactement au niveau API; le bloc complet ajoute
   séparément prominence.
7. Oui, ruler ajoute les dirigeants utilitaristes au vivier.
8. Le seuil de prominence est un changement fonctionnel de disponibilité et
   d'équilibrage, pas une nécessité API.
9. Oui, `character_role_ig_leader` est défini et utilisé comme rôle en 1.13.
10. Sa justification pour le mod n'est pas prouvée : source-only dans l'objet,
    absent de vanilla et non annoncé précisément par le changelog.
11. Le tooltip groupe l'affichage; les deux triggers et leur logique restent.
12. Non, les quatre warnings ne sont pas attribuables au fichier/hunk cible.
13. Oui, les rafales de 133 à 136 types par révolte étayent un transfert
    générique des journal entries.
14. Oui pour une substitution de ligne techniquement bornée; non pour une
    validation fonctionnelle exhaustive du pinning, qui dépend du contexte BIC.
15. Oui pour vérifier le chargement parser sans déclencher la chaîne; non pour
    valider la visibilité BIC complète sans sélectionner ce contexte protégé.

## 20. Critères de sélection

Le pinning possède le fichier, l'objet, les lignes, le hash initial, la forme
moderne convergente, un hunk isolé, le hash final et le rollback exacts. Il
échoue néanmoins au critère 1 : aucun diagnostic actuel. Sa validation UI
complète recoupe aussi le contexte BIC/Inde du critère 16. Les API de rôles
échouent également au diagnostic actuel; le bloc complet échoue en plus aux
critères de vivier, rôle et prominence. Le tooltip échoue au diagnostic actuel
et à la preuve d'une nécessité technique.

Les vingt conditions cumulatives ne sont donc satisfaites par aucun groupe.
Aucune phase 6A.17F n'est sélectionnée.

## 21. Documents écrits et CSV

Documents créés ou mis à jour : ce rapport, `INDEX.md`,
`HOTFIX_REPORT_INDEX.csv`, `HOTFIX_MERGE_BLOCK_STATUS.csv` et la roadmap. Le
prompt 6A.17R reste inchangé comme preuve historique; aucun prompt F n'est
inventé.

Validation `Import-Csv` :

- report index : `131 × 22` avant, `132 × 22` après; nouvelle clé 6A.17R
  unique, prédécesseur 6A.17, aucun successeur;
- matrice des blocs : `43 × 17` avant et après; ligne de sélection convertie en
  audit terminé, clé toujours unique;
- champs structurels requis de la nouvelle ligne : aucun vide;
- champs optionnels vides de la nouvelle ligne : `superseded_by`, `successor`,
  `companion_csv_path` seulement;
- lignes mal formées : 0;
- doublons historiques du report index : groupes `S` (2 lignes) et `INDEX`
  (6 lignes), préexistants et inchangés; aucun doublon dans la matrice des
  blocs;
- inventaires non modifiés et valides : trois voies `541 × 21`, différences
  globales `534 × 22`, travail restant `512 × 20`.

## 22. Contrôles finaux

| Contrôle | Résultat |
| --- | --- |
| Branche finale | `hotfix-dlc-audit` |
| HEAD final | `4ae07bef5c1f81787a36eff629cc393e1166cda8` |
| Message final | `Select Imperialism of Promise functional audit` |
| Hash gameplay cible | `80E38C181A5AEB547E8F98EBFD03844F3522CADC59426D9FC16588B908105C3B` |
| Fichiers gameplay modifiés | 0 |
| Index staged | vide |
| `git diff --check` | PASS |
| Stash final | ligne et objet inchangés |
| Processus finaux | 0 Victoria 3, 0 Dowser, 0 launcher Paradox |
| Runtime / logs nouveaux | aucun; manifeste des 60 logs inchangé |
| Commit automatique | aucun |

Les fichiers BIC/Inde, les événements utilitaristes, les lois, scopes,
localisations, descripteurs et sauvegardes n'ont pas été modifiés. Le fichier
cible conserve son hash initial exact.

## 23. Verdicts finaux

```text
HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT_COMPLETE
IMPERIALISM_OF_PROMISE_THREE_WAY_COMPARISON_COMPLETE
IMPERIALISM_OF_PROMISE_FUNCTIONAL_GROUPS_CLASSIFIED
BIC_INDIA_GEOGRAPHY_PROGRESSION_DELTAS_PROTECTED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NO_NEXT_EXECUTION_PHASE_SELECTED
```
