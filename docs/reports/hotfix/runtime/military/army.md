# Hotfix des formations militaires — créé par l’humain

## Périmètre

Cette mise à jour rapproche les historiques de formations militaires du fork de
la source hotfix de travail, puis applique les corrections nécessaires pour
Victoria 3 1.13.

Sources comparées :

- `HEAD` du fork : `843f54b Resolve DEI breakup target hunks` ;
- source hotfix en lecture seule :
  `1776_Age_of_Revolutions_hotfix_source` ;
- vanilla Victoria 3 1.13 :
  `C:\Games\Victoria 3 The Great Wave\game`.

Le commit est limité aux fichiers encore modifiés sous
`common/history/military_formations/` et au présent rapport. Le fichier
accidentel `bject`, `docs/research/technology/` et le stash
`WIP NAVY-3C-3 Maratha Konkan Flotilla` restent hors périmètre.

## Provenance des fichiers

- `00_military_formations_europe.txt` suit la source hotfix, avec nettoyage
  des espaces finaux.
- `01_military_formations_north_america.txt` suit la source hotfix, avec une
  correction supplémentaire de région stratégique.
- `02_military_formations_south_america.txt` suit la source hotfix, avec
  nettoyage des espaces finaux.
- `03_military_formations_north_africa.txt` a été restauré exactement depuis
  `HEAD` : cette version était déjà compatible avec la syntaxe navale 1.13.
- `04_military_formations_middle_east.txt`,
  `05_military_formations_india.txt` et
  `07_military_formations_subsaharan_africa.txt` suivent la source hotfix.
- `06_military_formations_asia.txt` suit la source hotfix, sauf pour le bloc
  japonais restauré depuis `HEAD` et vanilla 1.13.
- `99_military_formations_example.txt` suit la référence vanilla 1.13 pour la
  région commentée de l’exemple.

## Corrections bloquantes

### Afrique du Nord

La copie de travail contenait un second bloc `MILITARY_FORMATIONS` concaténé à
`STATE_TRIPOLI`, des blocs `TUN` et `MAS` dupliqués et une flotte exprimée avec
`combat_unit`/`unit_type`.

Le fichier de `HEAD` contient déjà :

- un seul bloc racine ;
- `ship = { ... }` pour les flottes ;
- `ship_type:ship_type_frigate` ;
- les blocs uniques `TUN`, `TRI` et `MAS` ;
- uniquement des régions et types existants en vanilla 1.13.

Décision : restauration du seul fichier Afrique du Nord depuis `HEAD`. Aucun
contenu de la source hotfix n’avait à être conservé dans ce fichier.

### Amérique du Nord

La source hotfix conservait `sr:region_new_england` pour la formation
`Regular_Army`. Cette région n’existe pas parmi les 142 régions stratégiques
définies par vanilla 1.13.

`region_atlantic_coast` est définie dans
`common/strategic_regions/north_america_strategic_regions.txt` de vanilla 1.13
et correspond aux autres formations américaines migrées. La valeur a donc été
remplacée par `sr:region_atlantic_coast`.

### Japon

La source hotfix supprimait entièrement les trois formations :

- `Edo_Guard_Army` ;
- `Kinai_Guard_Army` ;
- `Kyushu_Guard_Army`.

Cette suppression retirait dix groupes d’unités à un pays existant, sans
formation de remplacement. Le bloc de `HEAD` est identique au bloc vanilla
1.13, utilise `sr:region_northeast_asia` et des types d’unités valides.

Décision : suppression accidentelle, bloc japonais restauré intégralement.

## Validation des suppressions importantes

### Personnages, généraux et amiraux européens

Le bilan exact n’est pas une suppression brute de 22 personnages :

- 24 anciens amiraux sont retirés ;
- 2 nouveaux amiraux espagnols sont créés ;
- aucun général n’est supprimé ;
- bilan net : 22 créations de personnages en moins.

Amiraux retirés, groupés par pays :

- Venise : Angelo Emo ;
- France : Louis Guillouet d’Orvilliers, Toussaint-Guillaume Picquet de la
  Motte, Luc-Urbain de Guichen, Pierre-André de Suffren,
  François-Hector d’Albert de Rions et Charles-Hector d’Estaing ;
- Grande-Bretagne : Augustus Keppel, Peter Parker, Richard Kempenfelt,
  Samuel Barrington, Francis Geary, Samuel Hood, Richard Howe et Edward
  Hughes ;
- Russie : Vasily Chichagov, Samuil Greig et Alexei Senyavin ;
- Suède : Henrik af Trolle ;
- Danemark-Norvège : Frederik Christian Kaas ;
- Pays-Bas : Jan Hendrik van Kinsbergen ;
- Portugal : Arthur Phillip ;
- Espagne : Luis de Córdova y Córdova et Antonio de Ulloa.

Les deux créations ajoutées sont `spanishnavy1_gen` et `spanishnavy2_gen`.

Les 24 suppressions correspondent exactement à la source hotfix et accompagnent
la suppression des anciens `save_scope_as` de flottes ou la reconstruction des
escadres. Aucun de ces scopes ou amiraux n’est recréé ailleurs dans la source.
Les restaurer isolément produirait des transferts vers des formations
inexistantes. Ils sont donc conservés comme changement intentionnel de la
réorganisation navale, et non comme une perte de copie accidentelle.

### Armées européennes

Les comparaisons structurelles montrent que plusieurs armées anonymes signalées
par un diff ligne à ligne sont en réalité conservées après réorganisation.

Les suppressions effectives sont :

- les formations conditionnelles de Norvège et de Finlande ;
- les deux armées conditionnelles grecques ;
- l’armée conditionnelle serbe ;
- `Divisao_Auxiliar_a_Espanha` du Portugal.

Les blocs norvégien, finlandais, grec et serbe concernent des pays absents de la
configuration politique de départ 1776. La division portugaise est explicitement
liée dans l’ancien commentaire aux guerres carlistes, donc anachronique pour
1776. Ces suppressions correspondent exactement à la source hotfix et sont
conservées comme nettoyage intentionnel.

### Flottes européennes

La majorité des flottes apparemment supprimées sont renommées, réparties ou
reconstruites :

- les escadres françaises du Nord et de Méditerranée sont conservées et deux
  stations supplémentaires sont ajoutées ;
- les cinq stations britanniques deviennent dix stations plus petites ;
- la flotte russe d’Okhotsk est remplacée par la flotte de la mer Noire ;
- les marines prussienne, autrichienne, danoise, sicilienne et néerlandaise
  restent présentes sous une structure, un nom ou un scope ajusté ;
- les anciennes flottes vénitienne, génoise, suédoise et portugaise sont
  remplacées ou réduites conformément à la source hotfix ;
- les flottes conditionnelles norvégienne et finlandaise disparaissent avec
  leurs blocs pays non applicables au départ 1776.

Ces changements sont cohérents avec les nouveaux groupes navals et les régions
stratégiques consolidées de la source. Aucune autre formation japonaise ou
formation active sans remplacement n’a été identifiée après restauration du
bloc `JAP`.

## Dette technique / correctifs ultérieurs

Les anomalies suivantes existaient déjà dans `HEAD` et ne sont pas introduites
par cette mise à jour. Elles restent volontairement hors de ce commit :

1. `05_military_formations_india.txt` référence `maitland_gen` et
   `madras_army`, sans création correspondante dans la version modifiée du
   fichier.
2. Le même fichier contient `ideology = moderate`, alors que l’identifiant
   défini est vraisemblablement `ideology_moderate`.
3. `00_military_formations_europe.txt` réutilise `colborne_gen` pour Matthew
   Whitworth puis référence `aylmer_gen`, qui n’est pas créé.

Le fichier Moyen-Orient contient par ailleurs deux blocs top-level `c:PER`.
Cette structure était déjà identique dans `HEAD` et dans la source hotfix :
elle crée successivement deux armées persanes distinctes et reste valide pour
le moteur. Elle n’est donc ni une duplication introduite par la migration ni
une correction à intégrer à ce commit.

Ces dettes doivent être traitées dans une phase dédiée afin de ne pas mélanger
des corrections historiques antérieures avec la migration des formations.

## Validations statiques

Contrôles prévus et exécutés avant staging :

- comparaison avec `HEAD`, la source hotfix et vanilla 1.13 ;
- inventaire structurel des personnages, armées et flottes ;
- un seul bloc racine actif par fichier ;
- équilibre des accolades sans profondeur négative ;
- validation des 142 régions stratégiques vanilla 1.13 ;
- validation des HQ, régions d’État, types d’unités et types de navires ;
- absence de `sr:region_new_england` dans les fichiers modifiés ;
- absence d’ancien type naval dans un bloc de flotte ;
- confirmation du bloc japonais identique à `HEAD` et vanilla 1.13 ;
- confirmation du fichier Afrique du Nord identique à `HEAD` ;
- contrôle des scopes et duplications, avec dette antérieure séparée ;
- fins de fichiers et espaces finaux propres ;
- `git diff --check` propre ;
- staging limité aux formations militaires modifiées et à ce rapport.

Aucun runtime de jeu n’est inclus dans ce commit statique.

## Addendum runtime

La migration a ensuite été testée sous Victoria 3 1.13.0. Le premier lancement
a révélé douze formations dont le QG, bien que valide dans les définitions 1.13,
n’avait aucun ancrage territorial pour le pays concerné. Le correctif séparé
`3b02b2a` modifie uniquement ces douze valeurs `hq_region`.

La partie neuve corrigée, la sauvegarde du 1er février 1776, sa recharge et deux
progressions distinctes jusqu’au 1er mai sont validées. Les trois armées
japonaises, `Regular_Army` à `region_atlantic_coast`, les deux armées persanes,
l’Afrique du Nord et une formation subsaharienne ont passé les contrôles.

Les dettes `maitland_gen` / `madras_army`, `ideology = moderate` et
`colborne_gen` / `aylmer_gen` se reproduisent dans les logs et restent hors du
correctif. Voir le
[rapport de QA runtime](HOTFIX_MILITARY_FORMATIONS_1_13_RUNTIME_QA.md).

Verdict : `MILITARY_FORMATIONS_1_13_RUNTIME_QA_COMPLETE`.
