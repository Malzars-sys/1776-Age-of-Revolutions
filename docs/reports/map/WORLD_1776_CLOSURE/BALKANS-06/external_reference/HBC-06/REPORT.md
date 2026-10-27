# HBC-06 — intégration du contour approuvé

26 octobre 2026. Départ : 1er janvier 1776. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**.

## Résultat

Contour HBC-05 installé exactement : **278 provinces HBC et 103 ONT**. Neuf anciennes provinces HBC passent à ONT. Les **1 959 autres provinces retirées à HBC** sont réparties entre 13 nouveaux pays décentralisés, sur les seules terres de ce lot. Les provinces des anciens IRC/ATB, du Québec, des États-Unis et des autres voisins restent à leurs propriétaires. Bitmap, terrains, ressources, arable, hubs et locators inchangés. L'ancien doublon x8D15CB est supprimé de la liste HBC réécrite.

**108 626 habitants HBC préservés**, toutes cultures/religions comprises, et les 21 commandes de bâtiments avec niveaux, PM, réserves et propriétaires économiques inchangés. La population HBC du Nunavut, 17 362, est conservée dans HBC Manitoba selon le plan HBC-03 ; aucune migration historique alléguée. **2 400 000 habitants autochtones ajoutés volontairement**, selon la nouvelle autorisation anachronique du joueur. Ce n'est pas une estimation historique. Variation mondiale déclarée : **+2 400 000**, aucun autre prélèvement ou compensation.

| Ensemble régional | TAG | Provinces | Population ajoutée |
|---|---|---:|---:|
| Cris des bois | H01 | 151 | 185,050 |
| Cris des marais | H02 | 71 | 136,539 |
| Dénésulines | H03 | 112 | 178,411 |
| Sayisi Dene | H04 | 63 | 17,422 |
| Mushkegowuk | H05 | 36 | 210,219 |
| Anishinabeg | H06 | 101 | 589,781 |
| Eeyou | H07 | 120 | 238,214 |
| Naskapis | H08 | 153 | 303,722 |
| Inuit du Nunavik | H09 | 130 | 258,064 |
| Inuit du Kivalliq | H10 | 221 | 61,105 |
| Netsilingmiut | H11 | 182 | 50,322 |
| Iglulingmiut | H12 | 326 | 90,138 |
| Inuit de Baffin | H13 | 293 | 81,013 |

Les [sources et limites](SOURCES.md) distinguent présence des peuples, répartition régionale, approximation de frontières et choix de gameplay. Ni centralisation politique des bandes, ni bannières, ni chiffres de population ne sont présentés comme reconstitution exacte.

## Revendications

Claims HBC sur Saskatchewan, Manitoba, Ontario et Québec ; contrôle politique séparé. Ce sont des claims par State Region, plus larges que le bassin exact dans les États partagés. Le claim préexistant sur l'ensemble de Nunavut est retiré pour ne pas revendiquer tout l'Arctique. Sa partie méridionale relevant du bassin d'Hudson nécessiterait une division plus fine pour un claim distinct. Les autres régions de la concession historique ne sont pas modifiées par cette passe limitée. **La concession historique entière n'est donc pas cartographiée exactement.**

## Fichiers du jeu modifiés ou ajoutés

- `common/history/states/00_states.txt`
- `common/history/pops/05_north_america.txt`
- `common/country_definitions/1776_hbc_indigenous.txt`
- `common/history/countries/1776_hbc_indigenous.txt`
- `common/flag_definitions/1776_hbc_indigenous.txt`
- `common/coat_of_arms/coat_of_arms/1776_hbc_indigenous.txt`
- `common/history/pops/1776_hbc_indigenous.txt`
- `localization/french/1776_hbc_indigenous_l_french.yml`
- `localization/english/1776_hbc_indigenous_l_english.yml`

Les fichiers partagés sont patchés sur leur version courante avec contrôle d'empreinte ; les copies immédiatement antérieures sont dans `before/`, les données exactes installées dans `patch/`. Aucun fichier restauré depuis Git, aucune écriture vanilla ou Git. Aucun changement aux suivis WORLD/SERG. Le tableau provincial complet est `PROVINCES.csv`.

## Vérifications

- 25 contrôles statiques positifs : attributions uniques, State_ID/RGB, contour exact, terres voisines conservées, chaîne HBC–ONT–USA par arêtes passables, cinq postes reliés, capitales possédées, homelands, démographie et patrimoine HBC, ajouts autochtones et claims. Résultats dans `VALIDATION.json`.
- 16 tests unitaires HBC réussis : diagonales, bords interdits, faux raccord par enclave, fragments détachés, propriétaire manquant/erroné/double et mauvais State_ID. Commande : `python -X utf8 -m unittest discover -s tools -p test_hbc*.py -v`.
- Audit des 13 profils technologiques : zéro P0/P1 ; six `PASS_STATIC_ONLY`, sept `REVIEW` pour profils dénés/inuit sans nœud industriel initial, choix explicitement documenté. Pas de bâtiment industriel ou de formation régulière neuf demandant une technologie absente. Aucun tier européen distribué pour faire disparaître ces avertissements.
- L'audit initial signalait une demande conditionnelle de mercantilisme issue du rappel générique de politique traditionnelle. Les nouveaux profils utilisent désormais les lois natives explicitement ; le résultat initial est gardé dans `TECHNOLOGY_AUDIT_INITIAL.json`, le résultat final dans `TECHNOLOGY_AUDIT.json`. Aucun effet partagé modifié.
- Les textures vanilla des bannières ont été trouvées ; localisations FR/EN avec BOM, définitions, religions et références contrôlées. Aperçu géométrique `INTEGRATED_MAP.png` inspecté.

**Aucun chargement Victoria 3, mouvement réel, stabilité mensuelle, absence de famine ou sauvegarde/rechargement certifié.** Le protocole est dans [NEXT_ACTION.md](NEXT_ACTION.md). La validation du dessin par le joueur n'est pas un test moteur. Dettes préexistantes, notamment démographie coloniale anachronique, autres revendications HBC et profils voisins, non refondus.

## ColGrep

Un appel local `--agent`, terminé code 0 ; quatre emplacements retournés et vérifiés. Il a retrouvé les décisions HBC existantes, mais aucune attribution RGB autochtone prête à appliquer. Pas de reconstruction d'index. Les identifiants exacts et formats bitmap/DDS ont été vérifiés directement. La trace ne fournit pas de compteur de tokens ou de durée instrumentée fiable ; aucune économie exacte de quota ne peut être affirmée. Métadonnées dans `COLGREP.json`. L'intérêt constaté est la localisation des décisions antérieures ; l'analyse historique, les allocations et les contrôles restent effectués par Codex.
