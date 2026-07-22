# HOTFIX-3A - Import base IR1 / Mamluk Iraq

## 1. Resume

Cette phase importe uniquement l'infrastructure minimale du tag `IR1` / Mamluk Iraq depuis le hotfix upstream.

Le tag est maintenant defini techniquement, avec blason, drapeau, gouvernement special, history country, ruler et localisation EN/FR minimale.

La carte, les states, les pops, les batiments, les formations militaires, la diplomatie et le diplomatic play n'ont pas ete importes.

## 2. Pourquoi cette phase est limitee a l'infrastructure IR1

HOTFIX-3-AUDIT a montre que le paquet Mamluk Iraq depend de nombreux fichiers sensibles :

- `common/history/states/00_states.txt`
- `common/history/buildings/08_middle_east.txt`
- `common/history/pops/08_middle_east.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt`

Ces fichiers ne sont pas touches ici afin d'eviter une activation partielle du pays sur la carte ou une regression des corrections locales NAVY/ADMIN.

## 3. Fichiers hotfix utilises

| Fichier hotfix | Utilisation |
|---|---|
| `common/country_definitions/02_modded_countries.txt` | bloc `IR1` |
| `common/coat_of_arms/coat_of_arms/03_new.txt` | blason `IR1` |
| `common/flag_definitions/07_NM_Flags.txt` | drapeau `IR1` |
| `common/government_types/00_mod_gov_types.txt` | bloc `gov_pashalik` |
| `common/history/countries/ir1 - mamluk iraq.txt` | history country IR1 |
| `common/history/characters/ir1 - mamluk iraq.txt` | ruler Omar Ahmad |
| `localization/english/mod_v2content_l_english.yml` | cles EN `IR1`, `IR1_ADJ`, `gov_pashalik`, `RULER_TITLE_PASHA` |

## 4. Fichiers modifies

| Fichier fork | Changement |
|---|---|
| `common/country_definitions/02_modded_countries.txt` | ajout du bloc `IR1` |
| `common/coat_of_arms/coat_of_arms/03_new.txt` | ajout du blason `IR1` |
| `common/flag_definitions/07_NM_Flags.txt` | ajout de la definition de drapeau `IR1` |
| `common/government_types/00_mod_gov_types.txt` | nouveau fichier avec `gov_pashalik` uniquement |
| `common/history/countries/ir1 - mamluk iraq.txt` | nouveau fichier dedie a IR1 |
| `common/history/characters/ir1 - mamluk iraq.txt` | nouveau fichier dedie a IR1 |
| `localization/english/hotfix_ir1_l_english.yml` | localisation anglaise minimale |
| `localization/french/hotfix_ir1_l_french.yml` | localisation francaise minimale |
| `docs/reports/hotfix/HOTFIX_3A_IMPORT_IR1_BASE.md` | rapport de phase |

## 5. Tag IR1 ajoute

| Champ | Valeur |
|---|---|
| Tag | `IR1` |
| Nom hotfix | Mamluk Iraq |
| Couleur | `{ 122 132 110 }` |
| Country type | `unrecognized` |
| Tier | `principality` |
| Cultures | `georgian`, `mashriqi` |
| Religion | `shiite` |
| Capitale | `STATE_BAGHDAD` |

La capitale reference `STATE_BAGHDAD`, mais aucun ownership de state n'a ete modifie dans cette phase.

## 6. Blason / drapeau ajoutes

Blason ajoute dans `common/coat_of_arms/coat_of_arms/03_new.txt` :

- `pattern_solid.tga`
- couleur principale jaune ;
- croissant blanc ;
- etoile blanche.

Drapeau ajoute dans `common/flag_definitions/07_NM_Flags.txt` :

- `coa = IR1`
- `allow_overlord_canton = no`
- `priority = 1`

Aucun autre drapeau n'a ete modifie.

## 7. Gouvernement `gov_pashalik` ajoute

Le fichier `common/government_types/00_mod_gov_types.txt` a ete cree avec uniquement `gov_pashalik`.

Conditions principales :

- `has_law = law_type:law_monarchy`
- `exists = c:IR1`
- `exists = c:TUR`
- `c:IR1 ?= ROOT`
- `is_subject_of = c:TUR`
- pas de `subject_type_crown_land`

Important : comme la relation de protectorat TUR -> IR1 n'est pas importee dans HOTFIX-3A, `gov_pashalik` ne devrait pas encore devenir actif en jeu. Il deviendra pertinent lors de la phase qui importera la diplomatie.

## 8. History country IR1 ajoute

Nouveau fichier :

- `common/history/countries/ir1 - mamluk iraq.txt`

Contenu importe :

- starting technology tier 4 ;
- `academia` recherchee ;
- tax level medium ;
- taxes sur `tobacco`, `wine`, `liquor` ;
- lois : monarchy, autocracy, millet system, subjecthood, traditionalism, land-based taxation, slave trade, tenant farmers ;
- landowners au gouvernement ;
- starting politics traditional.

Le fichier est entierement dedie a `c:IR1`.

## 9. Characters IR1 ajoutes

Nouveau fichier :

- `common/history/characters/ir1 - mamluk iraq.txt`

Personnage importe :

| Personnage | Role | Culture | IG | Ideologie | Traits |
|---|---|---|---|---|---|
| Omar Ahmad | ruler | `cu:georgian` | `ig_armed_forces` | `ideology_jingoist_leader` | `basic_artillery_commander`, `tactful` |

Le fichier ne contient pas de general lie a une formation militaire. Aucune formation militaire IR1 n'a ete importee.

## 10. Localisation EN/FR ajoutee

Fichier EN :

- `localization/english/hotfix_ir1_l_english.yml`

Clés :

- `IR1: "Mamluk Iraq"`
- `IR1_ADJ: "Mamluk"`
- `gov_pashalik: "Autonomous Pashalik"`
- `gov_pashalik_desc`
- `RULER_TITLE_PASHA: "Pasha"`
- `RULER_TITLE_MUTASARRIF: "Mutasarrif"`

Fichier FR :

- `localization/french/hotfix_ir1_l_french.yml`

Clés :

- `IR1: "Irak mamelouk"`
- `IR1_ADJ: "irako-mamelouke"`
- `gov_pashalik: "Pachalik autonome"`
- `gov_pashalik_desc`
- `RULER_TITLE_PASHA: "Pacha"`
- `RULER_TITLE_MUTASARRIF: "Mutasarrif"`

Les deux fichiers sont en UTF-8 BOM.

## 11. Ce qui n'a pas ete importe

| Element | Statut |
|---|---|
| Ownership des states | non importe |
| Claims TUR sur Basra/Baghdad/Mosul/Deir ez-Zor | non importes |
| Pops IR1 | non importees |
| Batiments IR1 | non importes |
| Formations militaires IR1 | non importees |
| Protectorship TUR -> IR1 | non importe |
| Diplomatic play PER / IR1 / ARB / OMA | non importe |
| Secret goal IA IR1 -> TUR | non importe |
| Changements TUR | non importes |
| Changements PER | non importes |
| Changements ARB / OMA | non importes |

## 12. Dependances restantes

Pour activer IR1 proprement sur la carte, il faudra encore une phase separee pour :

1. transferer les states pertinents vers `IR1` dans `00_states.txt` ;
2. ajouter les pops `region_state:IR1` ;
3. ajouter les batiments `region_state:IR1` ;
4. ajouter l'armee IR1 si desire ;
5. ajouter la relation de protectorat TUR -> IR1 ;
6. verifier puis importer le diplomatic play `00_otto_iraqi_persia_war.txt` ;
7. tester les logs sur `STATE_BASRA.region_state:IR1`, `STATE_KHUZESTAN.region_state:ARB` et `gov_pashalik`.

## 13. Risques

- `IR1` existe maintenant comme tag technique, mais il ne possede pas encore de state.
- `gov_pashalik` depend d'une relation de sujet avec `TUR`, non importee ici.
- La capitale `STATE_BAGHDAD` est referencee dans la country definition, mais Baghdad appartient encore au setup local actuel.
- Le pays peut rester invisible ou non jouable tant que les states ne sont pas attribues.
- Les titres de gouvernement ont ete localises avec la cle `RULER_TITLE_MUTASARRIF`, distincte de la cle vanilla `RULER_TITLE_MUTSARRIF`.

## 14. Tests a faire

Avant activation carte :

1. Lancer le jeu jusqu'au menu.
2. Verifier `error.log` pour `IR1`, `gov_pashalik`, `RULER_TITLE_PASHA`, `RULER_TITLE_MUTASARRIF`.
3. Confirmer qu'aucune province/state n'a change autour de l'Iraq.

Apres future activation carte :

1. Verifier Baghdad, Basra, Mosul et Deir ez-Zor.
2. Verifier que Mamluk Iraq a son drapeau.
3. Verifier que le gouvernement ne s'affiche pas en cle brute en francais.
4. Tester TUR et PER pendant au moins un mois.

## 15. Confirmation de perimetre

- aucun state modifie ;
- aucun batiment modifie ;
- aucune pop modifiee ;
- aucune formation militaire modifiee ;
- aucune diplomatie modifiee ;
- aucun diplomatic play importe ;
- aucun changement a TUR/PER/ARB/OMA ;
- aucun changement BIC/Japon/Inde/NAVY/ADMIN ;
- aucune modification des lois HOTFIX-2 ;
- stash MARATH non touche.
