# CLEANUP-2D-3E-R2F — recrutement effectif et nommage

## Résultat

`CLEANUP2D3E_R2F_STATIC_FIX = PASS`

La correction s'arrête à 2D-3E-R2F. Victoria 3 n'a pas été lancé et CLEANUP-2D-4 n'a pas été commencé.

Les 150 blocs R1 de conscription ont été recalculés à partir de l'éligibilité effective vanilla 1.13.9 et remplacés par des blocs R2F. Les 214 formations terrestres scriptées ont désormais un total runtime attendu strictement positif. Les totaux réguliers 3B restent inchangés à 2 557; seules des régions de recrutement ont été déplacées pour les unités qui ne se matérialisaient pas.

## Audit vanilla 1.13.9

Sources canoniques auditées sous `C:\Games\Victoria 3\game` :

- `common/laws/00_army_model.txt` : taux de conscription, plafond par État, plafond de casernes et règle `country_can_only_conscript_peasants_bool`;
- `common/laws/00_church_and_state.txt` : `law_state_religion` n'applique aucune réduction de conscription; `law_millet_system` et `law_people_of_the_book` appliquent `state_conscription_rate_mult = -0.4`;
- `common/combat_unit_types/00_land_combat_unit_types.txt` : les infanteries compatibles portent `conscript_peasant_levies = yes`; le modèle de levées n'autorise donc que le groupe infanterie, hors infanterie mécanisée;
- `localization/english/interfaces_l_english.yml` : les refus exposés par l'interface sont absence de loi reconnue, absence de diplomatic play, population civile insuffisante, occupation, centre déjà actif, absence de centre disponible et plafond d'État atteint;
- `localization/english/modifiers_l_english.yml` : confirmation textuelle de la restriction d'infanterie des levées paysannes.

La décision complète du bouton `+` est interne au moteur, et non un scripted trigger réutilisable. Elle est néanmoins reproduite par les données exposées : loi active reconnue, propriété de la portion d'État, population/workforce, incorporation et modificateurs d'État, plafond de la loi, type d'unité compatible et technologie correspondante. Le moteur tronque le niveau effectif à l'entier inférieur; le `ceil` de R1 n'est qu'un plafond brut et surestime donc les blocs matérialisables.

Le modèle R2F est :

```text
RAW_STATE_CENTER_CAP = min(law_state_cap, ceil(workforce * state_conscription_rate_add / 1000))

FINAL_STATE_EFFECTIVE_CAP =
  0 si un gate obligatoire échoue,
  sinon min(law_state_cap, floor(workforce * effective_state_conscription_rate / 1000))
```

`effective_state_conscription_rate` inclut les multiplicateurs réellement actifs. Les niveaux observés dans le save R2 priment sur l'estimation historique lorsque le moteur fournit une mesure exacte.

## Save R2 lu en diagnostic

Le save identifié sans ambiguïté est `CLEANUP2D3E_R2.v3`, SHA-256 original `0A6D78422661728ED75279AF0F2BD738740D1FBC5F08AD9A5F0E99DF39CDC24D`. Seule une copie temporaire a été fondue avec Rakaly; la copie, le binaire temporaire et leur répertoire de diagnostic ont été supprimés après l'audit. Le save original conserve exactement le même SHA-256.

La corrélation objet explique les écarts :

- USA : les six États R1 recevaient chacun un `ceil`; leurs niveaux effectifs font 22 + 15 + 11 + 9 + 9 + 8 = 74. Six niveaux valides sont déplacés au Massachusetts;
- FRA : les seize centres R1 totalisent 64 après troncature; huit niveaux libres dans Alsace-Lorraine, Champagne, Franche-Comté, Lorraine et Provence portent la cible effective à 72;
- PRU : les centres R2 totalisent exactement 24. Le plafond effectif observé est conservé;
- TUR : `law_millet_system` réduit le taux de 40 %. Les douze États choisis par R1 plafonnent à 84, mais les autres États incorporés portent la capacité native exacte et conservatrice à 139. Les 139 conscrits restent de l'infanterie irrégulière compatible avec les levées paysannes;
- GBR : seuls les neuf centres britanniques utilisables observés produisent 43 niveaux. Les quinze niveaux R1 supplémentaires venaient de petits territoires/possessions dont le niveau effectif est nul;
- SPA : le save contient un objet de loi `law_peasant_levies`, mais l'interface et la matérialisation prouvent que le moteur ne reconnaît aucune loi de conscription active pour l'Espagne dans ce scénario (`0/0`, tooltip `must have a conscription law`). Ce gate runtime est autoritaire : les 70 blocs espagnols sont retirés sans modifier loi, technologie ou modificateur.

## Corrections régulières et formations 0+0

- RUS : les 25 unités concentrées en Dobrudja, dont sept objets étaient absents et la majorité sans manpower, sont déplacées vers Moscou et Nijni Novgorod. Total inchangé : 215;
- FRA : une unité de la formation coloniale est déplacée des Antilles vers Alsace-Lorraine. Total inchangé : 165;
- PRU : six unités excédant la matérialisation observée d'Anhalt/Basse-Silésie sont déplacées au Brandebourg. Total inchangé : 158;
- GBR : les 9 unités de `Mediterranean Garrison` et les 9 de `India Crown Detachment` recrutent désormais en East Anglia, État directement détenu et doté d'une marge de casernes. Total inchangé : 49;
- SIC : les cinq unités recrutées dans la portion de Sicile détenue par GR3 sont déplacées en Calabre. Total inchangé.

L'audit agrégé vérifie pour chaque unité finale la propriété directe, le plafond national de casernes, le total affecté dans l'État, le type et la formation. Résultat : `REGULAR_MATERIALIZATION_MISMATCHES = 0` et `EXPECTED_RUNTIME_EMPTY_SCRIPTED_LAND_FORMATIONS = 0`.

## Noms affichés et formations automatiques

Les sept noms russes ont été translittérés en russe latin, identiquement en EN et FR. Les noms prussiens ont été remis en allemand et les quatre noms ottomans en turc latin. Les deux fichiers restent en UTF-8 BOM.

L'audit vanilla n'a trouvé aucun pool de noms d'armée/flotte par tag, aucune base de noms nationale et aucun hook scripté permettant de remplacer le nom ordinal d'une formation créée automatiquement. Le save confirme ce chemin : ces objets ont un nom/localizable name vide et seulement un `ordinal_number`; le moteur compose ensuite le libellé générique. Modifier une clé de localisation générique affecterait tous les pays, pas un tag particulier.

Conséquence : `AUTO_FORMATION_NAMING_SUPPORTED = NO` pour les 210 tags et `SPANISH_COLONIAL_GENERIC_NAME_POOL_FIXED = NOT_SUPPORTED_BY_ENGINE`. Les tags CUB, PCO, SC1, SC2, SC3, SC4 et GR5 sont marqués en priorité dans l'audit. Aucune fausse armée et aucun effectif n'ont été créés pour contourner cette limite.

## Bilan quantitatif

```text
RAW_GLOBAL_STATE_CONSCRIPTION_CAP = 4627
EFFECTIVE_GLOBAL_NATIVE_CONSCRIPTION_CAP = 3382
FINAL_SCRIPTED_CONSCRIPTS = 1635
COUNTRIES_WITH_NO_CONSCRIPTION_LAW = 1
COUNTRIES_WITH_RAW_CAP_BUT_ZERO_EFFECTIVE_CAP = 64

EFFECTIVE_CONSCRIPT_MATERIALIZATION_MISMATCHES = 0
REGULAR_MATERIALIZATION_MISMATCHES = 0
EXPECTED_RUNTIME_EMPTY_SCRIPTED_LAND_FORMATIONS = 0

SPA_REGULAR = 95
SPA_EFFECTIVE_CONSCRIPT = 0
SPA_CONSCRIPT_SHORTFALL_LAW = 70
SPA_NAVY = 40

RUS_REGULAR = 215
RUS_CONSCRIPT = 120

TUR_REGULAR = 65
TUR_CONSCRIPT = 139
TUR_CONSCRIPT_ROOT_CAUSE = MILLET_RATE_MULT_MINUS_40_PERCENT_PLUS_STATE_TRUNCATION_AND_R1_OVERCONCENTRATION

GBR_REGULAR = 49
GBR_EFFECTIVE_CONSCRIPT = 43
GBR_NAVY = 120
GBR_FLEETS = 7
EAST_INDIES_STATION = PRESENT

USA_REGULAR = 20
USA_CONSCRIPT = 80
USA_NAVY = 5
USA_SOL = 0

FRA_REGULAR = 165
FRA_CONSCRIPT = 72
PRU_REGULAR = 158
PRU_CONSCRIPT = 24
MYS_CONSCRIPT = 10
CHI_CONSCRIPT = 150
MARATH_CONSCRIPT = 79
```

## Validation statique finale

```text
RUSSIAN_CYRILLIC_FORMATION_NAMES_AFTER = 0
NON_LATIN_FORMATION_DISPLAY_NAMES_AFTER = 0
GENERIC_SCRIPTED_FORMATION_NAMES_AFTER = 0
AUTO_GENERATED_FORMATION_NAMING_SYSTEM_AUDITED = YES
SPANISH_COLONIAL_GENERIC_NAME_POOL_FIXED = NOT_SUPPORTED_BY_ENGINE
FORMATION_NAME_LOCALIZATION_DUPLICATES = 0

NEW_CONSCRIPT_PARSER_ERRORS_EXPECTED = 0
NEW_SERVICE_TYPE_ERRORS_EXPECTED = 0

DEFINES_CHANGED = 0
LAW_CHANGED = 0
TECH_CHANGED = 0
POP_CHANGED = 0
OWNERSHIP_CHANGED = 0
MAP_CHANGED = 0
STATE_REGIONS_CHANGED = 0
NAVAL_INFRA_CHANGED = 0

PROTECTED_TECH_FILES_CHANGED = 0
PROTECTED_TECH_FILES_UNTRACKED = 7
BJECT_PATH_PRESENT = 0
TEMP_DIAGNOSTIC_COPY_PRESENT = 0

CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
git diff --check = PASS
```

## Livrables

- `docs/research/military/CLEANUP2D3E_R2F_EFFECTIVE_CONSCRIPTION_CAPACITY.csv` — 740 lignes État/pays;
- `docs/research/military/CLEANUP2D3E_R2F_CONSCRIPT_MATERIALIZATION.csv` — affectation et motif de rejet par État;
- `docs/research/military/CLEANUP2D3E_R2F_REGULAR_MATERIALIZATION.csv` — matérialisation régulière par formation/État/type;
- `docs/research/military/CLEANUP2D3E_R2F_RUNTIME_EMPTY_FORMATION_AUDIT.csv` — 214 formations terrestres;
- `docs/research/military/CLEANUP2D3E_R2F_AUTOMATIC_FORMATION_NAMING_AUDIT.csv` — 210 tags.

## Runtime R3 condensé à exécuter par l'utilisateur

1. Charger un nouveau démarrage 1776 et contrôler seulement SPA, GBR, USA, TUR et RUS.
2. Relever : SPA `95 + 0`, GBR `49 + 43`, USA `20 + 80`, TUR `65 + 139`, RUS `215 + 120`.
3. Ouvrir `Mediterranean Garrison` et `India Crown Detachment` : chacune doit afficher 9 réguliers, jamais 0+0.
4. Vérifier visuellement les sept noms russes translittérés et l'absence de tout alphabet non latin dans les noms R2F.
5. Créer/observer une formation automatique d'une colonie espagnole : le nom ordinal générique est une limite moteur documentée, pas un échec de pool R2F.
6. Quitter normalement; ne poursuivre vers 2D-4 qu'après ce contrôle.
