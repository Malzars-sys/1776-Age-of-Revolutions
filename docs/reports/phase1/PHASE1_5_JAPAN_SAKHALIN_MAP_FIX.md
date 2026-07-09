# Phase 1.5 - Correction carte Japon / Sakhaline

## 1. Probleme corrige

Cette phase corrige le decalage entre la carte vanilla Victoria 3 1.13 / The Great Wave et l'historique du mod autour du Japon et de Sakhaline.

Le probleme principal etait que l'historique du mod utilisait encore l'ancien decoupage :

- `STATE_CHUBU`
- ancien `STATE_KANSAI`
- ancien `STATE_KYUSHU`
- ancien rattachement partiel de Sakhaline/Hokkaido

La carte vanilla 1.13 utilise maintenant :

- `STATE_TOKAI`
- `STATE_HOKUSHINETSU`
- `STATE_KYOTO`
- `STATE_RYUKYU_ISLANDS` avec une province supplementaire
- `STATE_SAKHALIN` avec 31 provinces

## 2. Fichiers modifies

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`
- `PHASE1_5_JAPAN_SAKHALIN_MAP_FIX.md`

Aucun fichier de localisation, technologie, formation militaire, batiment naval global, Australie ou Moyen-Orient n'a ete modifie.

## 3. States corriges

- `STATE_SAKHALIN`
- `STATE_HOKKAIDO`
- `STATE_KANTO`
- `STATE_TOKAI`
- `STATE_HOKUSHINETSU`
- `STATE_KANSAI`
- `STATE_KYOTO`
- `STATE_KYUSHU`
- `STATE_RYUKYU_ISLANDS`

Apres correction, les provinces vanilla 1.13 de ces states sont toutes attribuees dans `common/history/states/00_states.txt`.

## 4. Anciennes references a STATE_CHUBU

`STATE_CHUBU` a ete supprime/remplace dans :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`

L'ancien contenu de `STATE_CHUBU` a ete scinde entre :

- `STATE_TOKAI`
- `STATE_HOKUSHINETSU`

## 5. Nouveaux states ajoutes ou adaptes

### STATE_TOKAI

Ajoute dans :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`

Ownership conserve :

- `c:JAP`

### STATE_HOKUSHINETSU

Ajoute dans :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`

Ownership conserve :

- `c:JAP`

### STATE_KYOTO

Ajoute dans :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`

Ownership conserve :

- `c:JAP`

## 6. Correction de STATE_SAKHALIN

`STATE_SAKHALIN` a ete complete avec la liste de provinces vanilla 1.13.

Provinces ajoutees a Sakhaline ou deplacees vers Sakhaline :

- `x1E5261`
- `x5B9D2D`
- `x601140`
- `x7F67EF`
- `xA060DF`

Les provinces qui etaient dans `STATE_HOKKAIDO` mais appartiennent maintenant a `STATE_SAKHALIN` ont ete retirees de Hokkaido.

`xA060DF` a ete retiree de `STATE_KAMCHATKA` pour eviter un doublon avec Sakhaline.

## 7. Choix faits pour ownership, pops et buildings

Ownership :

- Les nouveaux states japonais restent sous `c:JAP`.
- `STATE_RYUKYU_ISLANDS` reste sous `c:JAP`, comme dans le setup existant du mod.
- `STATE_SAKHALIN` reste sous `c:SKH`, comme dans le bloc existant du mod.
- Aucun pays vanilla nouveau (`ULT`, `RYU`, etc.) n'a ete ajoute.

Pops :

- Les pops de l'ancien `STATE_CHUBU` ont ete reparties entre `STATE_TOKAI` et `STATE_HOKUSHINETSU`.
- Une partie des pops de l'ancien `STATE_KANSAI` a ete deplacee vers `STATE_KYOTO`.
- Les cultures et religions existantes ont ete conservees.

Buildings :

- Les types de batiments de l'ancien `STATE_CHUBU` ont ete conserves et repartis entre `STATE_TOKAI` et `STATE_HOKUSHINETSU`.
- `STATE_KYOTO` recoit un petit set conservateur de batiments civils japonais.
- Les niveaux globaux ont ete limites pour eviter une refonte economique.

## 8. Choix volontairement non faits

- Pas d'ajout automatique de `SKH`, `ULT` ou `RYU` dans `common/country_definitions`.
- Pas d'import complet du setup vanilla Japon/Sakhaline 1.13.
- Pas de refonte politique du Japon.
- Pas de correction Australie.
- Pas de correction Moyen-Orient.
- Pas de modification des technologies, localisations ou formations militaires.
- Pas de reequilibrage economique global.

## 9. Risques restants

- `c:SKH` est deja utilise par le mod dans Sakhaline, mais n'est pas defini dans `common/country_definitions/00_countries.txt`. Cette phase ne cree pas ce pays pour respecter le perimetre demande.
- `STATE_RYUKYU_ISLANDS` reste sous Japon au lieu d'importer le pays vanilla `RYU`.
- Les batiments de `STATE_TOKAI`, `STATE_HOKUSHINETSU` et `STATE_KYOTO` sont conservateurs, pas une simulation historique fine.
- `xEF50C0` a ete retiree de `STATE_KYUSHU` car elle appartient a une state region indonesienne vanilla 1.13 ; il faudra verifier plus tard l'Indonesie si une zone blanche apparait la-bas.

## 10. Tests a faire ensuite

1. Lancer Victoria 3 avec uniquement le mod active.
2. Ouvrir la selection pays.
3. Inspecter visuellement :
   - Japon central
   - Kyoto/Kansai
   - Tokai
   - Hokushinetsu
   - Hokkaido
   - Sakhaline
   - Ryukyu
4. Lancer une partie au 1 janvier 1776.
5. Laisser tourner au moins un mois.
6. Surveiller :
   - `Documents/Paradox Interactive/Victoria 3/logs/error.log`
   - `Documents/Paradox Interactive/Victoria 3/logs/game.log`
   - `Documents/Paradox Interactive/Victoria 3/logs/debug.log`
7. Rechercher dans les logs :
   - `STATE_CHUBU`
   - `STATE_TOKAI`
   - `STATE_HOKUSHINETSU`
   - `STATE_KYOTO`
   - `STATE_SAKHALIN`
   - `xEF50C0`
   - `xBB27F6`
   - `xA060DF`
8. Verifier qu'aucune province blanche ne reste autour du Japon et de Sakhaline.
