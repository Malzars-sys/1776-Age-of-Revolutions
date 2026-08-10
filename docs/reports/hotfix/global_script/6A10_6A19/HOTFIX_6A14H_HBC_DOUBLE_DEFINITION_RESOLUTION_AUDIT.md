# HOTFIX-6A.14H — Audit de résolution de la double définition HBC

## 1. Phase, date et verdict

| Champ | Valeur |
| --- | --- |
| Phase | `HOTFIX_6A14H_HBC_DOUBLE_DEFINITION_RESOLUTION_AUDIT` |
| Date | 30 juillet 2026 |
| Nature | audit fonctionnel et documentaire, sans correction gameplay |
| Branche | `hotfix-dlc-audit` |
| HEAD initial | `4758547b88adf8256076077870126f397ea957da` |
| Sujet du HEAD | `Audit Navigation Acts starting law conflicts` |
| HEAD final | `4758547b88adf8256076077870126f397ea957da`, inchangé |
| Verdict principal | `HBC_DUPLICATE_HISTORY_UNKNOWN_REQUIRES_REVIEW` |
| Phase corrective | aucune sélectionnée |

Les preuves statiques, les logs existants et le runtime humain démontrent que
les deux blocs HBC sont chargés et composés. L'état visible complet correspond
à une fusion stable : les valeurs conflictuelles finales viennent de `hudson`,
tandis que plusieurs lois, le gouvernement, l'idéologie et les institutions
proviennent de `hubson` ou de son effet conservateur. Cette composition
technique n'est toutefois pas une preuve d'intention de design. Aucune
suppression, fusion, correction ou activation de Navigation Acts n'est donc
autorisée par cet audit.

## 2. Préflight Git et protections

État Git initial :

```text
?? bject
?? docs/research/technology/
```

L'index staged était vide. Le stash protégé était :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
```

Son hash objet initial était
`518df704fa14599c0f254fae13859210663dd976`. Son contenu n'a pas été lu.
`bject` et les sept fichiers technologiques non suivis n'ont pas été inspectés.
Le jeu et le launcher n'ont pas été lancés.

## 3. Sources lues

Les sources documentaires obligatoires ont été lues intégralement avant toute
écriture :

- `HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT.md`;
- `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW.md`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`;
- `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv`;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`;
- `HOTFIX_MERGE_REMAINING_WORK.csv`;
- les `Changelog.txt` complets du fork et de la source hotfix.

Ont également été lus les deux historiques HBC dans le fork et la source,
l'historique HBC vanilla, toutes les références `c:HBC` dans les historiques,
la définition du tag, la relation de sujétion, les possessions initiales et les
définitions nécessaires de lois, technologies, institutions et idéologie. La
source hotfix ne possède pas de dépôt Git local et son changelog n'explique pas
la coexistence des deux fichiers.

Racines de comparaison, en lecture seule :

- source : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`;
- vanilla 1.13 : `C:\Games\Victoria 3 The Great Wave\game`.

## 4. Présence, hashes et structure

| Variante | Présence | SHA-256 | Octets | Encodage | Fins de lignes | Saut final | Accolades |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| fork `hubson` | oui | `C88CB029FA2A0A32C549A6EA0A54802D614E5ED46DFADE4C0083F055826DE154` | 1432 | UTF-8 BOM | 46 CRLF | non | 7/7 |
| source `hubson` | oui | `C88CB029FA2A0A32C549A6EA0A54802D614E5ED46DFADE4C0083F055826DE154` | 1432 | UTF-8 BOM | 46 CRLF | non | 7/7 |
| vanilla `hubson` | absent | — | — | — | — | — | — |
| fork `hudson` | oui | `35377A3E896833E6DC9784440CDECBC3C8489043149C7B250EB5DF395FB9CC4F` | 925 | UTF-8 BOM | 27 LF | oui | 3/3 |
| source `hudson` | oui | `8D0C3B40CF258B97BD322DA6FDC1EE940AB523B28574ED4005D9180A89A1CD84` | 941 | UTF-8 BOM | 27 LF | oui | 3/3 |
| vanilla `hudson` | oui | `776EDBD71F79D43CB77459CB9FFE522967FAE5382EF6844BE7D9F8EA2B2CFE40` | 748 | UTF-8 BOM | 22 LF | oui | 3/3 |

Tous les hashes attendus correspondent. Le fork et la source ont un `hubson`
bit-identique. Dans `hudson`, la source diffère du fork uniquement par
`law_mercantilism_navigation_acts` au lieu de `law_mercantilism`. Le vanilla
emploie le même squelette que `hudson`, avec le tier technologique 2 et sans les
quatre technologies explicites ajoutées par le mod.

Ordre lexical ordinal des chemins :

```text
hbc - hubson bay company.txt
hbc - hudson bay company.txt
```

`hubson` précède donc `hudson`. Cet ordre de noms est prouvé; une règle générale
documentée imposant au moteur de trier tous les chemins par nom n'a pas été
trouvée.

## 5. Tag, sujétion et territoire

Le fork définit HBC comme `country_type = colonial`, culture
`anglo_canadian`, capitale `STATE_MANITOBA`; vanilla emploie
`country_type = company`. Dans les trois ensembles de données, GBR crée avec
HBC un pacte de type `chartered_company`. Le fork attribue initialement à HBC
des portions de `STATE_NUNAVUT`, `STATE_SASKATCHEWAN`, `STATE_MANITOBA`,
`STATE_ONTARIO` et `STATE_QUEBEC`.

Ces éléments établissent que l'objet existe avant l'application des historiques
et qu'il est bien une compagnie à charte dans la relation diplomatique, même si
son `country_type` local a divergé de vanilla.

## 6. Comparaison exhaustive des deux historiques

### 6.1 Technologies, gouvernement et effets

| Élément | `hubson` | `hudson` fork | Effet d'une composition |
| --- | --- | --- | --- |
| effet technologique | `effect_starting_technology_tier_4_tech` | identique | appelé deux fois, ensemble identique |
| tier 4, économie | `enclosure`, `manufacturies`, `steelworking`, `shaft_mining`, `distillation`, `prospecting` | identique | union identique |
| tier 4, militaire | `military_drill`, `standing_army`, `navigation`, `admiralty`, `gunsmithing`, `artillery`, `drydocks` | identique | union identique |
| tier 4, société | `urbanization`, `rationalism`, `tech_bureaucracy`, `centralization`, `democracy`, `international_relations`, `international_trade` | identique | union identique |
| technologies explicites | `academia`, `colonization`, `line_infantry` | mêmes trois + `mandatory_service` | 24 technologies uniques au total |
| effet politique | `effect_starting_politics_conservative` | absent | plusieurs lois survivantes confirmées en jeu |
| groupes au pouvoir | Industrialistes, puis Industrialistes de nouveau, puis Propriétaires terriens | aucun ajout explicite | Industrialistes seuls au gouvernement; Propriétaires terriens dans l'opposition |
| idéologie ajoutée | `ideology_colonialist` aux Industrialistes | aucune | Colonialiste confirmée |
| institution scolaire | `institution_schools`, niveau 1 | absente | Éducation niveau 1 confirmée |
| institution coloniale | clé invalide `colonial_affairs`, niveau 1 | `institution_colonial_affairs`, niveau 2 | niveau 1 rejeté; Affaires coloniales niveau 2 confirmé |
| institution de police | activée indirectement par `law_local_police` | absente | Maintien de l'ordre public niveau 1 confirmé |
| bien taxé | aucun | `g:grain` | grain taxé confirmé |

L'effet politique conservateur active d'abord `law_monarchy`,
`law_state_religion` pour HBC non islamique, `law_oligarchy`,
`law_appointed_bureaucrats`, `law_religious_schools`, `law_local_police`,
`law_per_capita_based_taxation`, `law_national_supremacy`,
`law_interventionism`, `law_mercantilism`, `law_no_workers_rights`,
`law_censorship`, `law_migration_controls`, `law_professional_army`,
`law_tenant_farmers` et `law_combination_acts`. Les activations explicites
placées plus bas dans `hubson` remplacent plusieurs groupes, mais laissent
notamment les écoles religieuses, la police locale, l'absence de droits des
travailleurs, l'armée professionnelle et les Combination Acts sans concurrent
ultérieur dans ce fichier.

### 6.2 Lois explicites

Le fork ne fournit aucune définition locale de ces lois : il s'appuie sur les
définitions vanilla montées. La colonne « fork » signifie donc « définition
locale dans `common/laws` », non « indisponible au montage ».

| Identifiant | `hubson` | `hudson` fork | Définition fork | Vanilla 1.13 | Groupe | Concurrence / exclusivité |
| --- | --- | --- | --- | --- | --- | --- |
| `law_colonial_administration` | oui | oui | non | oui | `lawgroup_governance_principles` | même loi; remplace la monarchie implicite |
| `state_religion` | oui | non | non | non | aucun; intention `lawgroup_church_and_state` | clé invalide; `law_state_religion` implicite existe déjà |
| `law_total_separation` | non | oui | non | oui | `lawgroup_church_and_state` | exclusive de `law_state_religion`; valeur finale confirmée |
| `law_autocracy` | oui | oui | non | oui | `lawgroup_distribution_of_power` | même loi; remplace l'oligarchie implicite |
| `law_land_based_taxation` | oui | oui | non | oui | `lawgroup_taxation` | même loi; remplace la taxation par tête implicite |
| `law_cultural_exclusion` | oui | non | non | oui | `lawgroup_citizenship` | exclusive de `law_racial_segregation` |
| `law_racial_segregation` | non | oui | non | oui | `lawgroup_citizenship` | valeur finale composée confirmée |
| `law_homesteading` | oui | oui | non | oui | `lawgroup_land_reform` | même loi; remplace les fermiers locataires implicites |
| `law_religious_schools` | oui | non | non | oui | `lawgroup_education_system` | également activée par l'effet conservateur; persiste dans les logs |
| `law_mercantilism` | oui | oui | non | oui | `lawgroup_trade_policy` | même loi dans le fork; la source `hudson` demande Navigation Acts |
| `law_extraction_economy` | oui | non | non | oui | `lawgroup_economic_system` | exclusive de l'interventionnisme |
| `law_interventionism` | implicite puis remplacée | oui | non | oui | `lawgroup_economic_system` | valeur finale composée confirmée |
| `law_hereditary_bureaucrats` | oui | non | non | oui | `lawgroup_bureaucracy` | remplace les bureaucrates nommés implicites |
| `law_no_migration_controls` | oui | non | non | oui | `lawgroup_migration` | remplace les contrôles migratoires implicites |
| `law_slave_trade` | oui | non | non | oui | `lawgroup_slavery` | aucune concurrente dans `hudson` |
| `law_right_of_assembly` | oui | oui | non | oui | `lawgroup_free_speech` | même loi; remplace la censure implicite |
| `law_frontier_colonization` | oui | oui | non | oui | `lawgroup_colonization` | même loi |

Le runtime confirme donc un composite : lois finales de `hudson` dans les
groupes en conflit, lois et effets additifs de `hubson` ailleurs, technologies
des deux, Industrialistes seuls au gouvernement, idéologie colonialiste,
Éducation niveau 1, Maintien de l'ordre public niveau 1, Affaires coloniales
niveau 2 et grain taxé. Les Propriétaires terriens sont dans l'opposition
malgré leur ajout initial par `hubson`, ce qui montre qu'une normalisation
supplémentaire du gouvernement intervient au démarrage. Cette configuration
n'est ni `hubson` seul ni `hudson` seul.

## 7. Identifiants suspects

### 7.1 `law_type:state_religion`

- aucune définition `state_religion = {` n'existe dans le fork ou vanilla;
- la forme 1.13 valide est `law_state_religion`, dans
  `00_church_and_state.txt`;
- la clé invalide apparaît dans plusieurs historiques legacy du fork, mais pas
  comme loi vanilla;
- aucun diagnostic ciblé sur cette ligne n'est conservé dans les logs examinés;
- elle peut donc avoir été ignorée silencieusement dans ces sessions;
- elle ne suffit pas à elle seule à prouver `hubson` obsolète, car l'effet
  conservateur placé avant elle active déjà la forme valide
  `law_state_religion`.

La ligne est néanmoins une preuve forte d'ancienneté syntaxique. Elle ne
constitue pas une activation de loi 1.13 valide.

### 7.2 `institution = colonial_affairs`

- aucune institution `colonial_affairs` n'existe dans le fork ou vanilla;
- la forme valide est `institution_colonial_affairs`;
- la forme invalide n'apparaît dans le fork que dans `hubson` et son très proche
  parent `org -oregan.txt`;
- `debug.log:3330`, `debug.2.log:2143` et `debug.4.log:978` signalent
  `PostValidate of effect 'set_institution_investment_level' returned false`
  sur `hubson` ligne 33;
- le niveau colonial 1 de `hubson` n'est donc pas une institution valide
  appliquée avec succès dans les sessions journalisées.

Ce diagnostic prouve un défaut fonctionnel 1.13. Il renforce l'origine legacy
de `hubson`, sans prouver que tout le fichier était destiné à être supprimé.

## 8. Provenance Git

Les deux fichiers ont été ajoutés ensemble dans le commit :

```text
b602804c446ad5834fde3827427acd66c7427ff8
2026-07-04T14:00:20+02:00
Malzars-sys
Initial import of 1776 Age of Revolutions fork
```

`git log --follow`, `git blame` et le diff racine de ce commit attribuent toutes
les lignes des deux fichiers à cet import. Aucun commit ultérieur de la branche
n'en modifie, renomme ou supprime un. Il est donc impossible d'établir lequel
est apparu le premier avant l'import, et aucune preuve Git locale ne montre
qu'un renommage ou une suppression a été oublié.

`hubson` est presque un clone de `org -oregan.txt` : même format CRLF legacy,
même commentaire « effectively dominated by the HBC », mêmes deux clés
invalides et même architecture politique. Les principales différences sont le
tag, trois lois de régime/citoyenneté et un second bloc Industrialistes avec
`ideology_colonialist`. Cela rend probable une origine comme adaptation 1776
spécifique ou copie de travail ancienne.

`hudson` suit directement le fichier canonique vanilla : même ordre de lois,
même institution coloniale niveau 2 et même grain taxé. Le mod remplace le tier
2 par le tier 4 et ajoute quatre technologies explicites. Il s'agit donc de la
lignée techniquement canonique de vanilla, mais pas d'une preuve suffisante de
l'intention canonique du mod 1776.

## 9. Sémantique de `?=`

### Faits prouvés

- les données vanilla emploient `?=` pour un accès de scope optionnel;
- un commentaire vanilla sur `var:emperor_var ?= {` dit explicitement
  `Silence the error log`;
- `c:HBC ?= { ... }` signifie donc que les effets sont exécutés si le scope HBC
  se résout, sans diagnostic d'accès nul;
- HBC existe dans le montage;
- le fork est le seul ensemble où deux fichiers de
  `common/history/countries` ciblent le même tag; vanilla n'a aucun doublon de
  tag dans ce domaine;
- le diagnostic de `hubson` et l'état légal HBC des logs prouvent que les deux
  historiques ont contribué à la même initialisation.

### Comportement probable

`?=` n'est pas une affectation « seulement si non déjà défini » et ne protège
pas contre un second bloc visant le même pays. Les effets additifs s'accumulent;
les activations d'un même groupe de lois sont remplacées par une activation
ultérieure.

### Non démontré

Aucun README ou commentaire vanilla ne documente le contrat complet des
doublons de fichiers d'histoire, ni une garantie générale de tri lexical. Les
logs ne listent pas chaque valeur finale et ne prouvent pas que ce comportement
restera identique dans tout contexte de montage ou de version.

## 10. Ordre de chargement et composition observée

Les faits suivants convergent :

1. `hubson` précède lexicalement `hudson`;
2. `hubson` active valablement Religion d'État via l'effet conservateur et
   Écoles religieuses;
3. `hudson` active ensuite Séparation totale;
4. les logs de la même série de lancement signalent pour HBC à la fois
   Séparation totale et Écoles religieuses comme lois conservées mais
   incompatibles.

`hudson` seul ne peut pas produire Écoles religieuses; `hubson` seul ne peut
pas produire Séparation totale. Le couple de messages prouve donc une
composition effective et soutient fortement l'ordre `hubson` puis `hudson`,
cohérent avec l'ordre lexical. Il ne prouve pas une intention de complément.

Le fichier `hudson` du mod porte le même chemin relatif que vanilla : selon la
convention d'override du montage, il doit masquer le fichier homonyme vanilla.
Les logs ne nomment toutefois pas `hudson` par son chemin et ses lois
déterminantes sont communes à vanilla; ce remplacement précis n'est donc pas
prouvé indépendamment par un message de log. `hubson`, chemin supplémentaire,
est en revanche explicitement traité. Le comportement le mieux étayé est donc
un override probable du chemin homonyme, plus une contribution supplémentaire
et certaine de `hubson`.

## 11. Analyse des logs existants

Tous les `.log` présents sous
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs`, rotations
comprises, ont été recherchés sans lancer le jeu.

| Recherche | Résultat |
| --- | --- |
| `hubson` | 3 hits : même échec PostValidate institution dans `debug.log`, `.2`, `.4` |
| `hudson` | 4 hits : deux messages HBC dupliqués dans `game.log` et `error.log` |
| `c:HBC` | 0 |
| `HBC` | 3 hits, les chemins `hubson` |
| `state_religion` | 3 hits, tous dans un événement sans rapport avec HBC |
| `colonial_affairs` | 0 texte brut; le diagnostic pointe l'effet et le fichier |
| `Invalid law` | 0 |
| `Invalid institution` | 0 |
| `already exists` | 0 |
| `duplicate` | 1515, localisations ou diagnostics sans rapport avec HBC |
| `Unexpected token` | 1230, aucun couplé à HBC, `hubson` ou `hudson` |

Preuves HBC déterminantes :

```text
[03:46:23][jomini_effect.cpp:141]: PostValidate of effect
'set_institution_investment_level' returned false at
common/history/countries/hbc - hubson bay company.txt:33

[03:57:12][country_law_manager.cpp:466]: Country Compagnie de la Baie
d’Hudson is not permitted to retain law Séparation totale, fix this or
consider Religion d’État instead

[03:57:12][country_law_manager.cpp:466]: Country Compagnie de la Baie
d’Hudson is not permitted to retain law Écoles religieuses, fix this or
consider Pas d’écoles instead
```

Les logs ne contiennent ni erreur d'objet HBC déjà défini, ni diagnostic
explicite sur `state_religion`. L'absence de message n'est pas une preuve de
validité.

Les logs courants transmis après le runtime ont aussi été audités :

| Log | Octets | Dernière écriture | SHA-256 |
| --- | ---: | --- | --- |
| `debug.log` | 20930 | 2026-07-30 17:17:17 | `7BCE9248BD292019378E6885A52D86A04F4BDED0C7C2501E39DAD67DA3CAE18C` |
| `error.log` | 152012 | 2026-07-30 17:16:58 | `22C171DA0315FAA5E14EE001E314442D4145EC3FF2AADB411E8C91F98310D0B3` |
| `game.log` | 444707 | 2026-07-30 17:16:58 | `F233A0579346E98E7C8E0B1E0AF8BD1916242D8DF6F01AB46E36D889584B82F4` |

Ces trois logs courants contiennent zéro hit pour `hubson`, `hudson`, `c:HBC`,
`HBC`, `state_religion`, `colonial_affairs`, `Invalid law`,
`Invalid institution`, `already exists`, `duplicate` et `Unexpected token`.
Ils n'ajoutent donc aucun diagnostic HBC ciblé au constat visuel. L'opérateur
confirme en outre qu'aucune clé brute n'a été observée.

## 12. Cohérence historique de HBC en 1776

Les Archives de la Compagnie de la Baie d'Hudson décrivent une compagnie fondée
par charte royale en 1670. Le contrôle appartenait au gouverneur, au
vice-gouverneur et à un comité de sept membres, tous actionnaires, sous
approbation de la General Court; les établissements de la baie rendaient compte
à Londres. Cela soutient une forte représentation des investisseurs et
marchands, mais pas un État territorial ordinaire
([Library and Archives Canada](https://recherche-collection-search.bac-lac.gc.ca/eng/home/record?app=fonandcol&idnumber=4193599&resource=folderlist),
[Archives of Manitoba](https://www.gov.mb.ca/chc/archives/hbca/about/)).

Parks Canada rappelle qu'en 1774 Cumberland House inaugure l'expansion des
postes HBC à l'intérieur pour répondre à la concurrence, et que les échanges
dépendent des peuples autochtones, notamment des intermédiaires cris et
assiniboines. `law_extraction_economy` et une forme de colonisation de frontière
sont donc défendables comme abstractions; homesteading, migration libre et une
institution coloniale étatique élevée le sont beaucoup moins
([York Factory](https://parks.canada.ca/lhn-nhs/mb/yorkfactory/culture/histoire-history),
[The Forks, 1760–1821](https://parks.canada.ca/lhn-nhs/mb/forks/culture/histoire-history/period)).

Évaluation par thème :

| Thème | `hubson` | `hudson` | Conclusion 1776 |
| --- | --- | --- | --- |
| compagnie à charte | Industrialistes au pouvoir + idéologie colonialiste | seulement porté par tag/relation externes | avantage `hubson` |
| rôle de la Couronne | administration coloniale + autocratie | identique | abstraction défendable, sans modéliser la gouvernance actionnariale |
| économie | extraction | interventionnisme + grain taxé | extraction plus fidèle au commerce des fourrures |
| religion | Religion d'État implicite + écoles religieuses | Séparation totale | deux abstractions excessives; écoles institutionnelles et séparation totale sont anachroniques |
| peuples autochtones et Métis | exclusion culturelle | ségrégation raciale commentée par George Simpson | aucune n'exprime la dépendance commerciale réciproque; le commentaire Simpson est postérieur à 1776 |
| esclavage | traite des esclaves | aucun choix explicite | `law_slave_trade` n'est pas étayée comme loi structurante de la compagnie |
| colonisation | frontière + institution invalide niveau 1 | frontière + institution valide niveau 2 | expansion des postes défendable; appareil colonial niveau 2 très étatique |
| migration | aucun contrôle | aucun choix explicite | migration libre contredit le recrutement et l'établissement très contrôlés |
| armée | armée professionnelle implicite | `mandatory_service` technologique | les deux sont des abstractions de gameplay; service obligatoire particulièrement peu adapté |
| administration | bureaucrates héréditaires | aucune loi dédiée | hiérarchie réelle, mais caractère héréditaire non défendable |
| technologie | tier 4 + 3 ajouts | tier 4 + 4 ajouts | calibrage du mod, non description littérale de 1776 |

Le commentaire `hudson` attribue la ségrégation aux politiques de George
Simpson. Une notice archivistique situe l'obtention de ses services par HBC en
1820; cette justification est donc manifestement anachronique pour le
1er janvier 1776
([Archives of Manitoba](https://www.gov.mb.ca/chc/archives/_docs/hbca/biographical/c/colvile_andrew.pdf)).

Historiquement, `hubson` saisit mieux la domination des investisseurs et
l'économie d'extraction; techniquement, il porte des clés invalides et plusieurs
lois étatiques peu défendables. `hudson` est plus propre et plus proche de
vanilla, mais conserve des choix postérieurs ou anachroniques. L'histoire ne
permet donc pas de désigner avec certitude l'un comme intention canonique
complète du mod.

## 13. Classifications

| Fichier | Classification unique | Motif |
| --- | --- | --- |
| `hbc - hubson bay company.txt` | `UNKNOWN_REQUIRES_REVIEW` | contenu 1776 distinct et historiquement partiellement défendable, mais origine legacy, deux clés invalides et composition concurrente |
| `hbc - hudson bay company.txt` | `UNKNOWN_REQUIRES_REVIEW` | lignée vanilla techniquement propre, mais anachronismes, delta Navigation Acts bloqué et rôle canonique non prouvé face à `hubson` |

La coexistence n'est pas classée complément intentionnel : aucun changelog,
commit ou commentaire ne l'affirme, et elle produit une combinaison de lois
incompatible.

## 14. Runtime humain unique exécuté

Une seule ouverture a complété les preuves. Codex n'a lancé ni le jeu ni le
launcher.

Protocole suivi :

1. Monter le fork exact au HEAD
   `4758547b88adf8256076077870126f397ea957da`.
2. Lancer une nouvelle partie avec HBC au 1er janvier 1776.
3. Relever toutes les lois actives, groupe par groupe.
4. Relever les groupes d'intérêt au gouvernement et les idéologies visibles.
5. Relever le niveau de chaque institution, notamment écoles et affaires
   coloniales.
6. Vérifier les technologies visibles pertinentes, dont `mandatory_service`.
7. Vérifier si le grain est taxé.
8. Avancer plusieurs jours et noter tout changement ou retrait automatique.
9. Noter toute clé brute, incompatibilité, notification ou anomalie.
10. Prendre des captures des lois, gouvernement, institutions, technologies et
    biens taxés.
11. Fermer le jeu et le launcher.
12. Transmettre le compte rendu et tous les nouveaux logs.

Sept captures ont été transmises : gouvernement, lois, Industrialistes,
Propriétaires terriens, institutions, technologie et budget.

Résultats observés :

| Domaine | État runtime |
| --- | --- |
| gouvernement | Industrialistes seuls; Propriétaires terriens dans l'opposition; gouvernement instable 46 |
| idéologie distinctive | Colonialiste présente chez les Industrialistes |
| principes de gouvernance | Administration coloniale (Monarchie) |
| répartition du pouvoir | Autocratie |
| citoyenneté | Ségrégation raciale |
| Église et État | Séparation totale |
| bureaucratie | Bureaucrates héréditaires |
| armée | Armée professionnelle |
| marine | Marine marchande |
| sécurité intérieure | Pas d'affaires intérieures |
| système économique | Interventionnisme |
| politique commerciale | Mercantilisme |
| imposition | Fiscalité foncière |
| réforme agraire | Homestead Act (Propriété paysanne) |
| colonisation | Colonisation des frontières |
| maintien de l'ordre | Force de police locale |
| éducation | Écoles religieuses |
| santé | Pas de système de santé |
| liberté d'expression | Droit de réunion |
| droits du travail | Aucun droit des travailleurs |
| droits des enfants | Travail des enfants autorisé |
| droits des femmes | Tutelle légale |
| aide sociale | Pas de sécurité sociale |
| migration | Aucun contrôle migratoire |
| esclavage | Commerce d'esclaves |
| associations de travailleurs | Combination Act |
| institutions | Affaires coloniales 2; Éducation 1; Maintien de l'ordre public 1 |
| technologie discriminante | Service obligatoire recherché |
| bien taxé | grain, visible dans les impôts de consommation |
| texte brut | aucune clé brute observée |
| stabilité temporelle | aucune loi ni aucun groupe d'intérêt modifié après plusieurs jours |
| fermeture | Victoria 3 fermé avant transmission; état du launcher non attesté séparément |

Attribution discriminante :

- `hudson` est prouvé par Ségrégation raciale, Séparation totale,
  Interventionnisme, Affaires coloniales niveau 2, Service obligatoire et le
  grain taxé;
- `hubson` ou son effet conservateur est prouvé par les Industrialistes au
  gouvernement, l'idéologie Colonialiste, Bureaucrates héréditaires, Écoles
  religieuses niveau 1, Force de police locale, Armée professionnelle, Aucun
  droit des travailleurs, Aucun contrôle migratoire, Commerce d'esclaves et
  Combination Act;
- les lois communes aux deux fichiers ne discriminent pas leur contribution;
- Marine marchande et les groupes sans activation dans ces deux fichiers sont
  des éléments de baseline supplémentaires.

Le scénario observé est sans ambiguïté une fusion. Il n'est pas classé comme
complément intentionnel, car aucun historique Git, changelog ou commentaire
n'établit cette intention et la fusion conserve Séparation totale avec Écoles
religieuses.

## 15. Phase corrective

`HOTFIX_6A14HF_HBC_HISTORY_CANONICALIZATION` n'est pas sélectionnée. Le runtime
confirme l'état complet, mais une décision humaine de design doit encore
désigner l'intention canonique et les lois à conserver. Navigation Acts,
GBR/NAVY, BIC et tous les autres scopes protégés restent exclus.

Rollback futur, seulement si une phase est ultérieurement autorisée : un
changement chirurgical borné aux historiques HBC, avec restauration du ou des
fichiers depuis le HEAD de départ. Aucun tel changement n'est exécuté ici.

## 16. Documentation écrite

Cette phase crée ou met à jour uniquement :

- `HOTFIX_6A14H_HBC_DOUBLE_DEFINITION_RESOLUTION_AUDIT.md`;
- `docs/reports/hotfix/INDEX.md`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` reste inchangé, puisqu'aucune phase
corrective précise n'est sélectionnée. Aucun fichier gameplay n'est modifié.

## 17. Contrôles finaux

| Contrôle | Résultat |
| --- | --- |
| Branche finale | `hotfix-dlc-audit`, inchangée |
| HEAD final | `4758547b88adf8256076077870126f397ea957da`, inchangé |
| Commit automatique | aucun |
| Index staged | vide |
| `git diff --check` | PASS |
| Hash stash final | `518df704fa14599c0f254fae13859210663dd976`, inchangé |
| `bject` | intact, non inspecté |
| sept fichiers technologiques | intacts, non inspectés |
| GEN | `7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327`, inchangé |
| VEN | `51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB`, inchangé |
| GBR | `529BAC14E5A32410ACB6E122B9F30273E2C40C32611316E6A0D925E0594E2429`, inchangé |
| BIC | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C`, inchangé |
| BIC `law_frontier_colonization` | conservée |
| BIC `law_colonial_exploitation` | non restaurée |
| Runtime HBC | exécuté, composite stable confirmé |
| Clés brutes | aucune observée |
| Victoria 3 | fermé |
| launcher | état non attesté séparément |
| fichiers gameplay modifiés | 0 |

## 18. Verdicts finaux

```text
HOTFIX_6A14H_HBC_DOUBLE_DEFINITION_RESOLUTION_AUDIT_COMPLETE
HBC_HUBSON_AND_HUDSON_THREE_WAY_COMPARISON_COMPLETE
HBC_SUSPICIOUS_IDENTIFIERS_AUDITED
HBC_DUPLICATE_OBJECT_SEMANTICS_AUDITED
NO_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
HBC_DUPLICATE_HISTORY_RUNTIME_VALIDATION_COMPLETE
HBC_COMPOSITE_START_CONFIRMED
HBC_RUNTIME_STABLE_NO_RAW_KEYS
HBC_DUPLICATE_HISTORY_UNKNOWN_REQUIRES_REVIEW
NO_NEXT_EXECUTION_PHASE_SELECTED
```
