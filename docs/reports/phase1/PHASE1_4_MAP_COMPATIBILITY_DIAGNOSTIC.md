# Phase 1.4 - Diagnostic de compatibilite carte Victoria 3 1.13 / The Great Wave

## 1. Description du probleme observe

Le mod lance une partie et peut tourner au moins un mois sans crash apres les phases 1.1, 1.2 et 1.3. Le probleme restant est visuel et gameplay : zones blanches, zones infranchissables ou provinces mal rattachees sur la carte, observees surtout autour du Japon, de Sakhaline et de l'Australie.

Hypothese generale : The Great Wave / 1.13 a modifie certaines state regions, provinces et sorties navales. Le mod conserve des fichiers d'historique et deux fichiers `map_data/state_regions` issus d'une version anterieure.

## 2. Regions touchees ou suspectes

### Japon

Risque critique. Le mod ne remplace pas `map_data/state_regions/11_east_asia.txt`, donc il utilise la carte vanilla 1.13 pour le Japon. En revanche, `common/history/states/00_states.txt`, `common/history/buildings/11_east_asia.txt` et `common/history/pops/11_east_asia.txt` contiennent encore l'ancien decoupage.

Constats compares a la vanilla 1.13 :

- `STATE_TOKAI` existe en vanilla 1.13 mais pas dans l'historique du mod.
- `STATE_HOKUSHINETSU` existe en vanilla 1.13 mais pas dans l'historique du mod.
- `STATE_KYOTO` existe en vanilla 1.13 mais pas dans l'historique du mod.
- `STATE_CHUBU` existe encore dans l'historique du mod, les buildings et les pops, mais n'existe plus comme state region vanilla 1.13 active.
- `STATE_KANTO` a 1 province vanilla non attribuee par l'historique du mod : exemple `x800111`.
- `STATE_RYUKYU_ISLANDS` a 1 province vanilla non attribuee par l'historique du mod : exemple `xBB27F6`.

### Sakhaline

Risque critique. La vanilla 1.13 a un decoupage plus detaille de Sakhaline.

Constats :

- `STATE_SAKHALIN` vanilla 1.13 contient 31 provinces.
- L'historique du mod n'en attribue que 26.
- Provinces presentes dans la state region vanilla mais absentes de l'historique du mod : exemples `x1E5261`, `x5B9D2D`, `x601140`.
- La vanilla 1.13 utilise aussi des pays/entites absents ou incomplets dans le mod : `SKH`, `ULT`, `RYU` existent en vanilla, mais `SKH`, `ULT`, `RYU` ne sont pas definis dans `common/country_definitions/00_countries.txt` du mod.

### Australie et Nouvelle-Zelande

Risque important. Le mod remplace directement `map_data/state_regions/13_australasia.txt`.

Constats compares a la vanilla 1.13 :

- Les listes de provinces et les hubs principaux sont globalement alignees avec le fichier carte du mod.
- Les divergences principales sont les `naval_exit_id` :
  - `STATE_QUEENSLAND` : mod `3124`, vanilla 1.13 `3129`.
  - `STATE_WESTERN_AUSTRALIA` : mod `3123`, vanilla 1.13 `3110`.
  - `STATE_NORTHERN_TERRITORY` : mod `3126`, vanilla 1.13 `3125`.
  - `STATE_SOUTH_ISLAND` : mod `3122`, vanilla 1.13 `3156`.
- `STATE_SOUTH_AUSTRALIA` a un nombre d'impassables different : mod 98, vanilla 92.
- Le contenu historique australien est tres minimal cote buildings, mais les states/pops existent bien dans :
  - `common/history/states/00_states.txt`
  - `common/history/buildings/13_australasia.txt`
  - `common/history/pops/13_australasia.txt`

### Autres regions suspectes

Le mod remplace aussi `map_data/state_regions/08_middle_east.txt`. Ce n'est pas lie directement aux observations Japon/Sakhaline/Australie, mais la comparaison vanilla 1.13 montre des divergences de `naval_exit_id` :

- `STATE_OMAN` : mod `3048`, vanilla 1.13 `3073`.
- `STATE_SISTAN` : mod `3046`, vanilla 1.13 `3048`.
- `STATE_TRABZON` : mod `3036`, vanilla 1.13 `3094`.
- `STATE_KARS` : mod `3036`, vanilla 1.13 `3094`.

## 3. Fichiers du mod qui remplacent ou modifient la carte vanilla

Fichiers `map_data` presents dans le mod :

- `map_data/state_regions/13_australasia.txt`
- `map_data/state_regions/08_middle_east.txt`

Fichiers historiques qui peuvent casser une carte 1.13 meme sans remplacer `map_data` :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`
- `common/history/buildings/13_australasia.txt`
- `common/history/pops/13_australasia.txt`
- `common/history/buildings/08_middle_east.txt`
- `common/history/pops/08_middle_east.txt`
- `common/country_definitions/00_countries.txt`
- `common/history/countries/jap - japan.txt`

Traits de states utilises par les remplacements carte :

- `common/state_traits/13_mod_traitsSX.txt`

## 4. Comparaison avec la vanilla Victoria 3 1.13

Vanilla locale utilisee :

- `C:/Games/Victoria 3 The Great Wave/game`

Comparaisons principales :

- `map_data/state_regions/13_australasia.txt` existe dans le mod et diverge de la vanilla 1.13 surtout par `naval_exit_id`, quelques traits et ressources.
- `map_data/state_regions/08_middle_east.txt` existe dans le mod et diverge legerement de la vanilla 1.13, surtout par traits et `naval_exit_id`.
- `map_data/state_regions/11_east_asia.txt` n'existe pas dans le mod : la carte Japon/Sakhaline vient donc de la vanilla 1.13.
- L'historique du mod pour le Japon/Sakhaline est ancien et ne correspond pas au decoupage vanilla 1.13.

Decoupage japonais vanilla 1.13 identifie :

- `STATE_SAKHALIN`
- `STATE_HOKKAIDO`
- `STATE_TOHOKU`
- `STATE_KANTO`
- `STATE_TOKAI`
- `STATE_HOKUSHINETSU`
- `STATE_KANSAI`
- `STATE_KYOTO`
- `STATE_KYUSHU`
- `STATE_RYUKYU_ISLANDS`
- `STATE_CHUGOKU`
- `STATE_SHIKOKU`

Ancien decoupage encore present dans le mod :

- `STATE_CHUBU`
- `STATE_KANSAI` avec anciennes provinces aujourd'hui reparties en partie vers `STATE_KYOTO`
- `STATE_KYUSHU` avec anciennes provinces aujourd'hui reparties en partie vers `STATE_RYUKYU_ISLANDS`

## 5. Hypotheses probables

### Provinces nouvelles non attribuees

Tres probable au Japon et a Sakhaline :

- `STATE_TOKAI` : 10 provinces vanilla 1.13 sans historique mod.
- `STATE_HOKUSHINETSU` : 9 provinces vanilla 1.13 sans historique mod.
- `STATE_KYOTO` : 4 provinces vanilla 1.13 sans historique mod.
- `STATE_SAKHALIN` : au moins 5 provinces vanilla 1.13 non attribuees par l'historique mod.
- `STATE_KANTO` et `STATE_RYUKYU_ISLANDS` : au moins 1 province chacune a verifier.

### Provinces anciennes supprimees ou deplacees

Probable :

- `STATE_CHUBU` est encore reference dans le mod alors qu'il ne correspond plus au decoupage vanilla 1.13.
- Certaines provinces anciennement dans `STATE_KANSAI` et `STATE_KYUSHU` ont ete deplacees vers `STATE_KYOTO` ou `STATE_RYUKYU_ISLANDS`.

### State regions obsoletes

Critique pour :

- `STATE_CHUBU` dans `common/history/states/00_states.txt`
- `STATE_CHUBU` dans `common/history/buildings/11_east_asia.txt`
- `STATE_CHUBU` dans `common/history/pops/11_east_asia.txt`

Important pour :

- `map_data/state_regions/13_australasia.txt`
- `map_data/state_regions/08_middle_east.txt`

### Naval exit IDs invalides ou obsoletes

Probable en Australie et secondairement au Moyen-Orient :

- Queensland, Western Australia, Northern Territory et South Island ont des `naval_exit_id` differents de la vanilla 1.13.
- Oman, Sistan, Trabzon et Kars ont aussi des `naval_exit_id` divergents.

### Ports ou hubs invalides

Moins probable en Australie : les hubs principaux compares restent identiques entre mod et vanilla 1.13.

Plus probable au Japon si des buildings ou regions d'ownership pointent vers des states obsoletes :

- `region="STATE_CHUBU"` existe dans `common/history/buildings/11_east_asia.txt`.
- Les buildings/pops de `STATE_TOKAI`, `STATE_HOKUSHINETSU` et `STATE_KYOTO` sont absents.

### Ownership / pops / buildings lies a des states modifies

Tres probable pour le Japon :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`

Important pour Sakhaline :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`
- `common/country_definitions/00_countries.txt`

Important pour l'Australie :

- `map_data/state_regions/13_australasia.txt`
- `common/history/states/00_states.txt`
- `common/history/buildings/13_australasia.txt`
- `common/history/pops/13_australasia.txt`

## 6. Liste precise des fichiers a corriger plus tard

Priorite critique :

- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`
- `common/country_definitions/00_countries.txt`

Priorite importante :

- `map_data/state_regions/13_australasia.txt`
- `common/history/buildings/13_australasia.txt`
- `common/history/pops/13_australasia.txt`
- `common/history/countries/jap - japan.txt`
- `common/history/countries/alk - alyaska.txt`

Priorite secondaire :

- `map_data/state_regions/08_middle_east.txt`
- `common/history/buildings/08_middle_east.txt`
- `common/history/pops/08_middle_east.txt`
- `common/state_traits/13_mod_traitsSX.txt`
- `descriptor.mod`
- `.metadata/metadata.json`

## 7. Plan de correction recommande region par region

### Japon

1. Comparer `map_data/state_regions/11_east_asia.txt` vanilla 1.13 avec les blocs japonais de `common/history/states/00_states.txt`.
2. Remplacer l'ancien bloc `STATE_CHUBU` par `STATE_TOKAI` et `STATE_HOKUSHINETSU`.
3. Creer ou adapter `STATE_KYOTO`.
4. Repartir les anciennes provinces de `STATE_KANSAI`, `STATE_KYUSHU` et `STATE_CHUBU` selon le decoupage vanilla 1.13.
5. Adapter `common/history/buildings/11_east_asia.txt`.
6. Adapter `common/history/pops/11_east_asia.txt`.
7. Verifier `common/history/countries/jap - japan.txt` pour les variables et claims japonais.

### Sakhaline

1. Reprendre la liste vanilla 1.13 de `STATE_SAKHALIN`.
2. Decider si le mod conserve son modele 1776 simple ou importe le decoupage vanilla `SKH` / `ULT` / `AIN` / `EZO` / `ALK`.
3. Si le decoupage vanilla est repris, ajouter ou adapter les country definitions manquantes : `SKH`, `ULT`, eventuellement `RYU`.
4. Adapter pops et buildings de Sakhaline.
5. Verifier les claims Russie/Japon/Chine.

### Australie / Nouvelle-Zelande

1. Decider si `map_data/state_regions/13_australasia.txt` doit rester remplace par le mod ou etre realigne sur vanilla 1.13.
2. Mettre a jour prudemment les `naval_exit_id` divergents :
   - Queensland
   - Western Australia
   - Northern Territory
   - South Island
3. Verifier les impassables de `STATE_SOUTH_AUSTRALIA`.
4. Re-tester les ports et la navigabilite autour de l'Australie.
5. Ne pas toucher aux ownership/pops tant que la carte n'est pas validee visuellement.

### Moyen-Orient

1. Reporter cette correction apres Japon/Sakhaline/Australie.
2. Comparer uniquement les `naval_exit_id` divergents.
3. Tester mer Rouge, golfe Persique, mer Noire et Caucase.

## 8. Risques si correction trop large

- Importer brutalement les fichiers vanilla 1.13 peut effacer le setup historique 1776 du mod.
- Modifier `map_data/state_regions` sans adapter `common/history/states` peut creer des provinces blanches ou sans proprietaire.
- Adapter les states sans adapter pops/buildings peut creer des economies vides ou des crashes de validation.
- Ajouter des pays vanilla manquants sans historique complet peut creer des flags, localisations, pops ou diplomatie incoherents.
- Changer trop de `naval_exit_id` en une fois peut masquer la cause exacte des problemes de navigation.
- Corriger le Japon, Sakhaline, Australie et Moyen-Orient dans une seule passe rendrait les regressions difficiles a attribuer.

## 9. Tests a faire apres une future correction

1. Lancer le jeu avec uniquement le mod active.
2. Ouvrir la selection pays et inspecter visuellement :
   - Japon complet
   - Hokkaido
   - Sakhaline
   - Ryukyu
   - Australie est/ouest/nord
   - Nouvelle-Zelande
3. Lancer une partie au 1 janvier 1776.
4. Activer les modes carte :
   - politique
   - states
   - population
   - infrastructures
   - naval / sea nodes si disponible
5. Verifier qu'aucune province terrestre visible n'est blanche ou sans proprietaire.
6. Verifier que les ports australiens et japonais s'affichent correctement.
7. Tester la creation d'une route maritime depuis :
   - Japon
   - Hokkaido/Sakhaline
   - Australie orientale
   - Australie occidentale
   - Nouvelle-Zelande
8. Laisser tourner au moins un mois.
9. Surveiller :
   - `Documents/Paradox Interactive/Victoria 3/logs/error.log`
   - `Documents/Paradox Interactive/Victoria 3/logs/game.log`
   - `Documents/Paradox Interactive/Victoria 3/logs/debug.log`
10. Rechercher apres test :
    - `STATE_CHUBU`
    - `STATE_TOKAI`
    - `STATE_HOKUSHINETSU`
    - `STATE_KYOTO`
    - `STATE_SAKHALIN`
    - `naval_exit_id`
    - `province`
    - `hub`
    - `port`
    - `state region`

## 10. Statut Git initial et perimetre

Avant creation de ce rapport, `git status --short` etait propre.

Aucune correction gameplay, carte, localisation, building, pop, pays ou history n'a ete faite pendant cette phase. Le seul fichier cree par cette etape est :

- `PHASE1_4_MAP_COMPATIBILITY_DIAGNOSTIC.md`
