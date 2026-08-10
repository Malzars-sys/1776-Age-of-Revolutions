# HOTFIX-6A.9R — Audit de la chaîne ottomane Tanzimat en 1776

## 1. Identification

- Date : 29 juillet 2026.
- Phase : `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial et final :
  `e319d1e6caccb90166a8f5aa3c8e99362007365f`.
- Commit d’entrée :
  `e319d1e Align Great Eastern Crisis with Victoria 3 1.13`.
- Nature : audit documentaire strict, sans gameplay et sans runtime.

## 2. Préflight Git

Le préflight obligatoire passe :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.8F présent dans le HEAD avec ses verdicts statique, runtime et de
  clôture ;
- 6A.8F commitée manuellement ;
- worktree suivi et index propres ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash exact présent :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, dowser ou Paradox.

État initial :

```text
?? bject
?? docs/research/technology/
```

## 3. Hashes protégés du préflight

| Élément | SHA-256 |
| --- | --- |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` |
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3DDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

## 4. Hashes de référence

| Fichier | Fork | Source hotfix | Vanilla 1.13 |
| --- | --- | --- | --- |
| `common/history/countries/tur - ottoman empire.txt` | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` | `15FC3CA4F1185B714B821EEE7B3DF400325AFEFA19C26BD92091B375D8C72375` | `93D02B1F8732205F8DCE570639B220CF32DF58A43741FC68D6604B4DED8EBF09` |
| `common/journal_entries/00_sick_man.txt` | `DC6AC302555035C574CFC61A91FBF667BE981FEFA2C1D8FA271A6F530B3054D8` | `E48405BFABB52F6CE757880E436C8D44C67111E246AF3215FD3F96EC4F3477F9` | `1EAD43BE40DAF22D585712442AFD379C893C3075007CDA0AADDB126CCF1DCA41` |
| `common/journal_entries/05_great_eastern_crisis.txt` | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | — | — |
| `events/sick_man_events.txt` | hérité | `D110D1FD83CD98E131D4C2769B606CC908F17844EFF88EF65F51FEBF313A0C2B` | même hash |
| `events/tanzimat_events.txt` | hérité | `F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30` | même hash |

Tous correspondent à la baseline imposée. La source hotfix et vanilla sont
restées strictement en lecture seule.

## 5. Sources consultées

Ont été lus et comparés :

- les trois versions intégrales de l’histoire ottomane, de `00_sick_man.txt`
  et de `05_great_eastern_crisis.txt` ;
- les événements complets `sick_man_events.txt` et `tanzimat_events.txt` ;
- les références pertinentes dans on-actions, stratégies IA, lois, scripted
  triggers/effects, static modifiers, journal entries, événements et
  localisations anglaises/françaises ;
- les rapports 6A.4 à 6A.8R, 6A.7F, 6A.8F, roadmap, matrice de blocs, index,
  inventaire global et prompt courant ;
- les changelogs complets du fork et de la source hotfix ;
- l’historique Git et le blame de l’histoire ottomane ;
- `debug.log` de 6A.8F, uniquement comme preuve historique.

Repères historiques externes :

- TÜBİTAK date la proclamation du programme Tanzimat au 3 novembre 1839 et
  décrit ses antécédents du début du XIXe siècle :
  <https://ansiklopedi.tubitak.gov.tr/ansiklopedi/tanzimat_fermani> ;
- l’Encyclopédie de l’Islam TDV identifie le rescrit de Gülhane de 1839 comme
  ouverture de l’ère Tanzimat :
  <https://islamansiklopedisi.org.tr/gulhane-hatt-i-humayunu> ;
- l’International Review of Social History situe le Land Code en 1858 :
  <https://www.cambridge.org/core/journals/international-review-of-social-history/article/peasant-protest-in-the-late-ottoman-empire-moral-economy-revolt-and-the-tanzimat-reforms/71E8BB89C36FE8160E4B939E62BE668A>.

## 6. Comparaison trois voies du setup ottoman

| Arbre | Lignes | Résultat |
| --- | ---: | --- |
| Fork | 31–41 | `sick_man.1`, `sick_man_of_europe` et `outmoded_bureaucracy` commentés |
| Source hotfix | 29–39 | même groupe commenté |
| Vanilla 1.13 | 29–39 | événement et deux modificateurs actifs, permanents |

Le fork ajoute aussi des adaptations 1776 absentes ou différentes de la source
et de vanilla : technologies 1836 commentées, `law_serfdom`,
`law_professional_navy` et `law_slave_trade`. Le commentaire de ligne 27 sur
Mehmed Emin Rauf Pasha reste explicitement formulé pour 1836, signe que le
fichier n’a pas été entièrement réécrit pour 1776.

Git montre que le groupe commenté était déjà présent au commit d’import initial
`b602804` et n’a jamais été réactivé. Le changelog du fork et celui de la source
ne documentent ni Tanzimat, ni `sick_man.1`, ni la raison de cette désactivation.
La source 2.3 conserve toutefois la même omission après son adaptation à une
version plus récente du jeu.

Conclusion factuelle : les commentaires constituent une désactivation
délibérée dans le fichier importé et persistante dans la source hotfix, mais sa
justification historique ou de design n’est pas explicitement documentée. Il
est donc incorrect de la qualifier de simple oubli prouvé, comme il serait
incorrect de prétendre que son intention 1776 est formellement prouvée.

## 7. Cause exacte de l’absence de Tanzimat

Le fork ne possède aucune autre référence active déclenchant `sick_man.1`.
L’unique appel du fork est commenté dans l’histoire ottomane. En conséquence :

1. `sick_man.1` n’est pas déclenché ;
2. `sick_man_var` et `sick_man_separatist_var` ne sont pas initialisées ;
3. `je_sick_man_main` et les six entrées secondaires ne sont pas ajoutées ;
4. `je_sick_man_egypt`, qui n’est ajouté que par l’achèvement de l’entrée Syrie
   quand l’Égypte n’est pas déjà contrôlée, ne peut pas apparaître ;
5. les deux modificateurs permanents du setup vanilla ne sont pas ajoutés.

L’événement `sick_man.1` ne remplace pas à lui seul le setup complet : son bloc
`show_as_tooltip` annonce les deux modificateurs, tandis que l’histoire vanilla
les applique réellement. Une future activation différée devra donc concevoir
explicitement l’initialisation de l’événement **et** des modificateurs, avec
garde anti-doublon.

## 8. Chaîne d’initialisation et événements

`events/sick_man_events.txt`, hérité de vanilla :

- `sick_man.1`, lignes 4–69 : met les deux compteurs à zéro, ajoute
  `je_sick_man_main`, puis Syrie, économie, éducation, séparatisme, armée et
  bureaucratie ;
- `sick_man.2`, lignes 72–173 : succès, pose `sick_man_complete`, retire
  `outmoded_bureaucracy` et accorde une récompense liée aux objectifs achevés ;
- `sick_man.3`, lignes 176–245 : échec, pose `sick_man_complete`, retire
  `outmoded_bureaucracy`, rend le pays non reconnu, libère certains sujets et
  expose la Grande Crise orientale avec `ip3_content`.

`events/tanzimat_events.txt`, hérité de vanilla :

- `.1` : réforme de l’affermage fiscal ;
- `.2` : code foncier ;
- `.4` : égalité juridique / `Islâhat Hatt-ı Hümâyûnu` ;
- `.5` à `.8` : paranoïa, émeute, massacre et retour à l’ordre ;
- `.9` : résistance à l’enregistrement foncier ;
- `.10` : conscription des dhimmis.

Les événements `.1`, `.2`, `.4` et `.10` sont branchés sur
`on_law_checkpoint_debate` aux lignes 4372–4375 du on-action du fork. `.5`,
`.9` et `.10` sont aussi appelés par les pulses des entrées séparatisme, armée
et bureaucratie.

Le log 6A.8F contient, en plus des huit erreurs de pinning, trois diagnostics
distincts d’ID Tanzimat invalide aux lignes `debug.log:1170`, `1173` et `1176`.
Ils ne sont pas causés par les huit propriétés de pinning et ne bloquent pas
leur substitution isolée. Ils interdisent en revanche de déclarer aujourd’hui
la chaîne Tanzimat prête à être activée sans audit de design/runtime propre.

## 9. Journal entries, succès, échec et durée

| Objet | Création | Succès / progression | Échec / timeout |
| --- | --- | --- | --- |
| `je_sick_man_main` | immédiat de `sick_man.1` | `sick_man_var >= 4` | 10 950 jours, soit environ 30 ans |
| `je_sick_man_syria` | option de `sick_man.1` | possède entièrement six régions ; +1, puis +1 si Égypte déjà contrôlée | invalidé par `sick_man_complete` |
| `je_sick_man_egypt` | seulement depuis Syrie si Égypte non contrôlée | Égypte sujette ou quatre régions possédées ; +1 | invalidé par `sick_man_complete` |
| `je_sick_man_economy` | option de `sick_man.1` | pas en défaut et 75 % des États incorporés avec centre urbain ; +1 | invalidé par `sick_man_complete` |
| `je_sick_man_education` | option de `sick_man.1` | université niveau 5 occupée et +20 points de littératie ; +1 | invalidé par `sick_man_complete` |
| `je_sick_man_separatism` | option de `sick_man.1` | 180 mois sous 50 % de sécession ; +1 | échoue au-dessus de 50 %, pose `failed_sick_man_separatism` |
| `je_sick_man_army` | option de `sick_man.1` | armée 100, `napoleonic_warfare`, approvisionnement et moins de 25 % d’irréguliers ; +1 | invalidé par `sick_man_complete` |
| `je_sick_man_bureaucracy` | option de `sick_man.1` | abandon de trois lois archaïques et bureaucratie non déficitaire ; +1 | invalidé par `sick_man_complete` |

## 10. Variables

| Variable | Initialisation / mutation | Dépendance |
| --- | --- | --- |
| `sick_man_var` | 0 dans `sick_man.1`, +1 par objectif, bonus Syrie/Égypte possible | obligatoire pour le compteur principal et les événements Tanzimat |
| `sick_man_separatist_var` | 0 dans `sick_man.1`, +1 par mois sous 50 % | obligatoire pour l’objectif 180 mois |
| `failed_sick_man_main` | timeout de l’entrée principale, avec `ip3_content` | ouvre la voie 2 de la Grande Crise |
| `failed_sick_man_separatism` | échec de l’entrée séparatisme | ouvre la voie 2 de la Grande Crise |
| `failed_tanzimat` | timeout principal, durée 20 ans | conséquences politiques séparées |
| `sick_man_complete` | succès ou échec final | invalide les secondaires et bloque Grand Collapse |
| `completed_*` | un drapeau par objectif achevé | sélection des récompenses de `sick_man.2` |
| `tanzimat_*`, `paranoia_state_var`, `mob_state_var` | événements Tanzimat | cooldowns et séquences événementielles, non requis par la Grande Crise |

## 11. Modificateurs

| Modificateur | Effets | Durée / retrait | Impact de son absence en 1776 |
| --- | --- | --- | --- |
| `sick_man_of_europe` | prestige -33 %, approbation Intelligentsia +5, force politique Intelligentsia +100 %, soutien modernizer +50 % | permanent dans le setup vanilla ; retiré au succès ou timeout | plus de prestige, mais moins de pression réformatrice |
| `outmoded_bureaucracy` | bureaucratie -25 %, capacité fiscale -25 %, gaspillage fiscal +25 % | permanent ; retiré par bureaucratie, succès ou échec | État nettement plus performant |
| `dead_man_of_europe` | résistance au séparatisme -50 %, conscription et récupération de moral -25 %, soutien cultural-majority +25 % | très long et décroissant après timeout | absent tant que la chaîne ne peut échouer |

L’Empire ottoman sans les deux modificateurs initiaux est donc globalement plus
fort en prestige, administration et fiscalité, mais aussi moins poussé vers les
réformes. Ce n’est pas une simple neutralisation.

## 12. Lois, technologies, territoires et IA

Le setup 1776 active notamment monarchie, autocratie, système des millets,
subjecthood, traditionalisme, taxation foncière, esclavage, servage et marine
professionnelle. Les lois cibles des objectifs existent et leurs pondérations
IA Tanzimat sont présentes. La stratégie
`ai_strategy_tanzimat_reforms` est héritée de vanilla mais n’est possible
qu’avec `je_sick_man_main`; l’IA diplomatique du fork devient aussi plus neutre
pendant cette entrée.

Le tier technologique initial ne donne ni `nationalism` ni
`napoleonic_warfare`. `napoleonic_warfare` est une technologie militaire
d’ère 1 nécessitant `line_infantry` et `artillery`; `line_infantry` est
précisément commentée dans le setup 1776. `nationalism` est d’ère 2 et demande
`mass_communication` et `international_relations`. Les deux restent
recherchables : absence initiale n’est pas impossibilité.

L’histoire des États du fork donne à TUR, dès 1776 :

- Alep, Syrie, Liban, Palestine, Transjordanie et Adana ;
- Sinaï, Haute-Égypte, Moyenne-Égypte et Basse-Égypte ;
- Attique, Péloponnèse, Crète, Serbie occidentale et Serbie orientale.

Ainsi l’entrée Syrie serait déjà satisfaite et accorderait deux points
immédiatement; l’entrée Égypte ne serait pas créée. Les textes « reprendre la
Syrie », « reprendre l’Égypte » et « nous avons déjà perdu la Grèce et la
Serbie » sont factuellement incompatibles avec le setup 1776.

## 13. Anachronismes et compatibilité 1776

Le lancement vanilla direct échoue au test de compatibilité totale :

- le titre « homme malade de l’Europe » renvoie au contexte de 1853 ;
- le texte de départ suppose l’« Auspicious Incident » et la dissolution des
  janissaires de 1826 ;
- Tanzimat commence historiquement en 1839 ;
- `Islâhat Hatt-ı Hümâyûnu` est un intitulé de 1856 ;
- le code foncier et son enregistrement renvoient à 1858 ;
- Syrie, Égypte, Grèce et Serbie sont décrites selon la géopolitique 1836,
  contraire aux possessions 1776 du fork ;
- le timeout ferait conclure la chaîne vers 1806, bien avant ces repères.

Les objectifs économiques, éducatifs, militaires et bureaucratiques sont
mécaniquement réalisables dans une campagne de trente ans, mais leur ensemble,
leurs textes, leur géopolitique et leur calendrier ne constituent pas une
chaîne 1776 cohérente. Restaurer le setup vanilla au 1er janvier 1776 n’est donc
pas acceptable.

## 14. Grande Crise orientale : deux voies séparées

`05_great_eastern_crisis.txt:50–65` contient deux branches :

1. `nationalism` recherché **et** `highest_secession_progress >= 0.50` ;
2. `failed_sick_man_main` **ou** `failed_sick_man_separatism`.

La voie 1 utilise un trigger moteur, pas `sick_man_var` ni
`sick_man_separatist_var`. La progression dépend d’un mouvement sécessionniste
effectif : ferveur culturelle, discrimination, soutien de population,
technologie nationalisme, soutien extérieur et résistance de l’État. Le
setup crée seulement un mouvement modernizer pour TUR, pas une sécession
initiale; la voie est donc différée et contingente, mais syntaxiquement et
fonctionnellement accessible par les mécaniques de mouvements héritées.

La voie 2 est inaccessible tant que les deux entrées Tanzimat ne sont jamais
créées, car leurs effets sont les seuls setters directs des deux variables
d’échec. La Grande Crise peut néanmoins apparaître sans Tanzimat par la voie 1.
Il serait faux de la déclarer impossible.

Les pays impliqués, observateurs, scopes, modificateurs de crise et variable
globale `eastern_crisis_happened` sont initialisés par la journal entry elle-
même, indépendamment de `sick_man.1`. Le runtime 6A.8F a déjà validé les vues
ottomane et britannique de l’entrée potentielle, pas son déclenchement.

## 15. Grand Collapse et dépendances balkaniques

`je_the_grand_collapse` ne requiert aucune variable Tanzimat initialisée. Sa
condition exige au contraire l’absence de `sick_man_complete`, puis un
changement de régime ou une révolution avancée. Sans chaîne Tanzimat,
`sick_man_complete` reste absent : Grand Collapse reste donc accessible.

La Balkan League accepte `eastern_crisis_happened`, les deux variables d’échec
Tanzimat ou `grand_collapse_started`. Les systèmes postérieurs disposent donc
encore de routes non Tanzimat. Aucun événement de Grande Crise ou Grand
Collapse n’exige `sick_man_var` ou `sick_man_separatist_var`.

## 16. Comparaison trois voies de `00_sick_man.txt`

Les huit objets existent dans les trois arbres. Le fork conserve l’ancienne
propriété; source hotfix et vanilla convergent exactement sur
`should_be_pinned_by_default_uninvolved_or_context = yes`.

Il existe d’autres écarts dans l’objet Syrie : modificateur actif, vérification
de type de sujet égyptien et pulse `egyptian_crisis_events.1`. Ils sont
fonctionnels mais indépendants des huit API. Ils doivent rester exclus de la
future migration atomique et être réexaminés seulement avec un design
d’activation Tanzimat.

### 16.1 `je_sick_man_main`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_main` |
| Ligne fork | objet 1 ; propriété 91 |
| Ligne source hotfix | objet 1 ; propriété 92 |
| Ligne vanilla | objet 1 ; propriété 92 |
| Propriétaire attendu | TUR, ajouté par `sick_man.1` |
| Visibilité | lobby TUR lignes 6–8, puis propriétaire |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte |
| Erreur runtime actuelle | `debug.log:1164`, near line 91 |
| Dépendance à `sick_man.1` | directe |
| Dépendance aux autres entrées | compteur alimenté par les secondaires |
| Localisation | EN `content_1:576–577`; FR `content_1:565–566` |
| Impact 1776 | nul tant que non créée |
| Risque | faible, substitution API uniquement |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

### 16.2 `je_sick_man_syria`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_syria` |
| Ligne fork | objet 94 ; propriété 178 |
| Ligne source hotfix | objet 95 ; propriété 177 |
| Ligne vanilla | objet 95 ; propriété 181 |
| Propriétaire attendu | TUR, ajouté par `sick_man.1` |
| Visibilité | propriétaire après création |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte pour le pinning |
| Erreur runtime actuelle | `debug.log:1165`, near line 178 |
| Dépendance à `sick_man.1` | directe |
| Dépendance aux autres entrées | peut ajouter Égypte; alimente main |
| Localisation | EN `content_1:580–581`; FR `content_1:569–570` |
| Impact 1776 | inactive; si activée, déjà complète et vaut deux points |
| Risque | faible pour pinning; design Syrie séparé |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

### 16.3 `je_sick_man_egypt`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_egypt` |
| Ligne fork | objet 181 ; propriété 222 |
| Ligne source hotfix | objet 180 ; propriété 223 |
| Ligne vanilla | objet 184 ; propriété 227 |
| Propriétaire attendu | TUR, ajouté conditionnellement par Syrie |
| Visibilité | propriétaire après création |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte |
| Erreur runtime actuelle | `debug.log:1166`, near line 222 |
| Dépendance à `sick_man.1` | indirecte |
| Dépendance aux autres entrées | dépend de Syrie; alimente main |
| Localisation | EN `content_1:583–584`; FR `content_1:572–573` |
| Impact 1776 | ne serait pas créée car Égypte déjà possédée |
| Risque | faible |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

### 16.4 `je_sick_man_economy`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_economy` |
| Ligne fork | objet 225 ; propriété 258 |
| Ligne source hotfix | objet 226 ; propriété 260 |
| Ligne vanilla | objet 230 ; propriété 264 |
| Propriétaire attendu | TUR, ajouté par `sick_man.1` |
| Visibilité | propriétaire après création |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte |
| Erreur runtime actuelle | `debug.log:1167`, near line 258 |
| Dépendance à `sick_man.1` | directe |
| Dépendance aux autres entrées | alimente main |
| Localisation | EN `content_1:585–586`; FR `content_1:574–575` |
| Impact 1776 | inactive; objectif mécaniquement réalisable |
| Risque | faible |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

### 16.5 `je_sick_man_education`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_education` |
| Ligne fork | objet 262 ; propriété 306 |
| Ligne source hotfix | objet 264 ; propriété 309 |
| Ligne vanilla | objet 268 ; propriété 313 |
| Propriétaire attendu | TUR, ajouté par `sick_man.1` |
| Visibilité | propriétaire après création |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte |
| Erreur runtime actuelle | `debug.log:1168`, near line 306 |
| Dépendance à `sick_man.1` | directe |
| Dépendance aux autres entrées | alimente main |
| Localisation | EN `content_1:587–588`; FR `content_1:576–577` |
| Impact 1776 | inactive; objectif long mais réalisable |
| Risque | faible |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

### 16.6 `je_sick_man_separatism`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_separatism` |
| Ligne fork | objet 312 ; propriété 388 |
| Ligne source hotfix | objet 315 ; propriété 392 |
| Ligne vanilla | objet 319 ; propriété 396 |
| Propriétaire attendu | TUR, ajouté par `sick_man.1` |
| Visibilité | propriétaire après création |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte |
| Erreur runtime actuelle | `debug.log:1171`, near line 388 |
| Dépendance à `sick_man.1` | directe, deux compteurs requis |
| Dépendance aux autres entrées | alimente main; son échec ouvre Grande Crise |
| Localisation | EN `content_1:590–591`; FR `content_1:579–580` |
| Impact 1776 | inactive; texte Grèce/Serbie anachronique |
| Risque | faible pour pinning; activation à haut risque de design |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

### 16.7 `je_sick_man_army`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_army` |
| Ligne fork | objet 394 ; propriété 449 |
| Ligne source hotfix | objet 398 ; propriété 454 |
| Ligne vanilla | objet 402 ; propriété 458 |
| Propriétaire attendu | TUR, ajouté par `sick_man.1` |
| Visibilité | propriétaire après création |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte |
| Erreur runtime actuelle | `debug.log:1174`, near line 449 |
| Dépendance à `sick_man.1` | directe |
| Dépendance aux autres entrées | alimente main |
| Localisation | EN `content_1:593–594`; FR `content_1:582–583` |
| Impact 1776 | inactive; texte janissaires et tech napoléonienne anachroniques |
| Risque | faible pour pinning |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

### 16.8 `je_sick_man_bureaucracy`

| Champ | Résultat |
| --- | --- |
| Objet exact | `je_sick_man_bureaucracy` |
| Ligne fork | objet 456 ; propriété 499 |
| Ligne source hotfix | objet 461 ; propriété 505 |
| Ligne vanilla | objet 465 ; propriété 509 |
| Propriétaire attendu | TUR, ajouté par `sick_man.1` |
| Visibilité | propriétaire après création |
| Ancienne propriété | `should_be_pinned_by_default = yes` |
| Nouvelle propriété | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Convergence hotfix/vanilla | exacte |
| Erreur runtime actuelle | `debug.log:1177`, near line 499 |
| Dépendance à `sick_man.1` | directe |
| Dépendance aux autres entrées | alimente main; retire `outmoded_bureaucracy` |
| Localisation | EN `content_3:136,138`; FR `content_3:116,118` |
| Impact 1776 | inactive; objectif de loi réalisable |
| Risque | faible |
| Rollback | restaurer exactement l’ancienne ligne |
| Classification exclusive | `REQUIRED_1_13_ALIGNMENT` |

## 17. Erreurs parser et autonomie de la migration

`debug.log` de 6A.8F contient exactement huit erreurs distinctes
`Unexpected token: should_be_pinned_by_default` pour ce fichier, aux lignes de
jeu 91, 178, 222, 258, 306, 388, 449 et 499.

Réponses obligatoires :

1. les huit objets utilisent la même nouvelle propriété : oui ;
2. source et vanilla convergent pour les huit : oui ;
3. huit erreurs parser distinctes sont prouvées : oui ;
4. huit substitutions ciblées sont sûres même si les entrées sont inactives :
   oui, car le parser lit leurs définitions ;
5. une entrée inactive peut être migrée sans changer son activation : oui ;
6. aucune localisation n’est requise ;
7. l’API est entièrement séparable de l’activation ;
8. les huit doivent être traitées dans une phase atomique unique ;
9. le diff futur est limité à un fichier, huit objets et huit substitutions ;
10. les autres écarts de Syrie et les diagnostics d’événements existent, mais
    n’empêchent pas cette migration isolée et doivent être explicitement exclus.

Snapshot actuel : 8 703 octets, UTF-8 BOM, 501 LF, zéro CRLF, saut final,
117 accolades ouvrantes et 117 fermantes. Le remplacement ASCII en mémoire,
sans écrire, donne :

- 8 879 octets ;
- delta +176 octets ;
- SHA-256 futur
  `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A`.

## 18. Dépendances complètes et statut

| Dépendance | Provenance effective | Compatibilité 1776 | Bloquante |
| --- | --- | --- | --- |
| histoire TUR | remplacée par le fork | spécifique 1776, rationale Tanzimat non documentée | bloque activation immédiate, pas pinning |
| huit JE | remplacées par le fork | inactives; objectifs partiellement anachroniques | non pour migration API |
| événements Sick Man/Tanzimat | hérités de vanilla, égaux à la source | textes XIXe siècle | oui pour futur design, non pour pinning |
| on-actions de lois | remplacés par le fork | présents | non |
| stratégie IA Tanzimat | héritée de vanilla | activée seulement avec main | non |
| pondérations de lois | fork + vanilla | présentes | non |
| technologies | héritées de vanilla | recherchables, non initiales | non |
| static modifiers | hérités de vanilla | présents mais calibrés 1836 | oui pour futur design |
| localisations EN/FR | héritées de vanilla | complètes mais plusieurs anachroniques | aucune pour pinning; oui pour activation 1776 |
| Grande Crise orientale | fork aligné 6A.8F | voie 1 accessible | non |
| DLC `ip3_content` | requis pour Grande Crise/conséquences | monté et validé en 6A.8F | non pour pinning |

## 19. Options de design

| Option | Avantages | Risques / coût | Verdict |
| --- | --- | --- | --- |
| A — préserver l’absence au départ | respecte le setup 1776; évite textes faux; conserve la voie autonome de crise | route d’échec Tanzimat absente; Ottoman plus fort | acceptable |
| B — activation différée propre à 1776 | sépare API et design; permet date/tech/crise/sécession; peut réécrire objectifs et textes | nouvelle chaîne, gardes anti-doublon, équilibrage, localisations et runtime requis | recommandée après API |
| C — restaurer vanilla au départ | rétablit toutes les routes 1836 | Syrie/Égypte auto-validées, Grèce/Serbie et janissaires faux, timeout 1806, modificateurs lourds | rejetée |
| D — décision humaine bloquante | utile seulement si A/B indécidables | retarde une migration API déjà certaine | non nécessaire |

Pour une future option B, les prérequis sont : déclencheur daté ou fondé sur
technologie/crise/sécession, événement d’initialisation idempotent, décision
explicite sur les deux modificateurs, objectifs territoriaux adaptés, textes
EN/FR nouveaux, traitement des trois diagnostics d’ID Tanzimat et runtime
humain dédié.

## 20. Décision finale

**Décision B.**

1. préserver l’absence de Tanzimat au départ 1776 ;
2. sélectionner d’abord la migration API autonome des huit propriétés ;
3. inscrire une activation différée propre à 1776 dans un backlog de design
   distinct ;
4. ne restaurer ni `sick_man.1`, ni les modificateurs, ni le setup vanilla dans
   la phase API.

Phase sélectionnée :

`HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT`

Backlog :

`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`

## 21. Runtime futur

6A.9R ne requiert aucun runtime et n’en a produit aucun.

Pour 6A.9F, aucun test fonctionnel des entrées inactives n’est nécessaire. Un
seul smoke parser humain est néanmoins requis pour prouver le passage des huit
erreurs ciblées de 8 à 0. Codex préparera les contrôles, ne lancera ni jeu ni
launcher, s’arrêtera à `RUNTIME_OPERATOR_ACTION_REQUIRED`, puis n’analysera les
logs qu’après confirmation humaine de fermeture. Aucun PASS runtime ne sera
émis sans compte rendu humain.

## 22. Rollback futur exact

Dans `common/journal_entries/00_sick_man.txt`, remplacer exactement les huit
occurrences de
`should_be_pinned_by_default_uninvolved_or_context = yes` par
`should_be_pinned_by_default = yes`, sans modifier aucune autre ligne.

Le rollback attendu restaure le hash
`DC6AC302555035C574CFC61A91FBF667BE981FEFA2C1D8FA271A6F530B3054D8`.

## 23. Protections et documents

Aucun gameplay n’a été modifié. 6A.8F, Grande Crise orientale, nationalisme
grec, blocs balkaniques clos, Inde, BIC, NAVY, MARATH, technologies, recherche,
localisations générales, descripteurs, launcher, sauvegardes et `bject` n’ont
pas été rouverts.

Six documents seulement :

1. `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md` ;
2. `docs/reports/hotfix/INDEX.md` ;
3. `HOTFIX_REPORT_INDEX.csv` ;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

BIC conserve `law_frontier_colonization`; `law_colonial_exploitation` n’a pas
été restaurée.

## 24. État Git final et commit

Le HEAD final reste
`e319d1e6caccb90166a8f5aa3c8e99362007365f`. L’index staged reste vide. Le
stash protégé reste intact. Aucun commit automatique n’est créé; le commit de
6A.9R relève de l’opérateur.

État final vérifié :

```text
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md
?? docs/research/technology/
```

Les contrôles finaux confirment : exactement six documents de phase modifiés
ou créés ; zéro diff gameplay ; les onze hashes de référence et les huit
hashes protégés inchangés ; huit objets classés exactement une fois ; deux CSV
valides (22 et 17 colonnes) ; `git diff --check` propre ; index staged vide ;
aucun processus Victoria 3, dowser ou Paradox. Source hotfix, vanilla, 6A.8F
et ses fichiers restent inchangés.

## 25. Verdicts

`HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT_COMPLETE`

`OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_DECISION_RECORDED`

`SICK_MAN_EIGHT_JE_PINNING_1_13_DECISION_RECORDED`

`OTTOMAN_TANZIMAT_START_DISABLED_IN_1776_PRESERVED`

`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`

`SICK_MAN_EIGHT_JE_PINNING_CAN_BE_ALIGNED_INDEPENDENTLY`

`NO_GAMEPLAY_CHANGED`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT`
