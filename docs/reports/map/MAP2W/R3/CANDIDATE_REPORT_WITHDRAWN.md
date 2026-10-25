# ARCHIVE — CANDIDAT RETIRÉ, NON LIVRÉ

Le texte ci-dessous décrit un candidat installé puis intégralement retiré après découverte d’une contradiction de calage. Il ne décrit pas le mod livré. Le statut courant est MAP2W_R3_BLOCKED ; voir REPORT.md et VALIDATION.json.

# MAP-2W-R3 — Premier sous-lot Hohenlohe, 1776

Date de livraison : 18 octobre 2026. Référence historique : 1er janvier 1776.

**MAP2W_R3_READY_FOR_SCOPED_RUNTIME_VALIDATION**, limité à **R3-A1 : noyaux de Langenbourg et Kirchberg**. R3-B, R3-C et les autres possessions de Hohenlohe ne sont pas annoncés terminés. Aucun test moteur exécuté par l’agent.

## Résultat installé

| Pays | Souverain initial | Avant → après | RGB | Cellules | Population technique |
| --- | --- | --- | --- | ---: | ---: |
| Hohenlohe-Langenbourg, HLN | Christian Albrecht, né le 27 mars 1726 | BAV → HLN | xEDA218 → xEDB903 | 3 | 2 213 |
| Hohenlohe-Kirchberg, HKI | Christian Friedrich Karl, né le 19 octobre 1729 | BAV → HKI | xEDA218 → xEDB902 | 4 | 2 950 |

Les deux pays ont leur capitale technique dans **STATE_FRANCONIA, ID numérique 72**. Ils sont des principautés impériales héréditaires distinctes, non électorales ; aucune union personnelle ou vassalité dynastique native n’est inventée. Un gouvernement borné à ces deux TAGs évite que le filtre européen vanilla leur attribue un titre ducal. Les descriptions FR/EN conservent le sous-texte dynamique de succession.

Quatre nouveaux RGB connexes : les deux pays ci-dessus et **xEDB900 (2 cellules BAV), xEDB901 (1 cellule BAV)**. Ces derniers sont des résidus techniques, pas de nouveaux micro-États. xEDA218 conserve 184 cellules BAV. Les 194 cellules du parent sont toutes conservées : **7 transferts souverains, 10 cellules recolorées**, 187 restant bavaroises sans certification historique supplémentaire. La frontière commune des régions économiques n’est pas redessinée.

Le registre passe de **567 à 571 RGB**. Ses droits, listes de membres, effets, scrutins, événements, bloc et carte du journal sont recompilés par les outils existants. Neuf électeurs et contributions Lien 0 % / État 15 % / Électeur 10 % inchangés. Aucune frontière de l’étendue physique impériale n’est ajoutée ou retirée.

## Vérification préalable des anciennes passes

FRANCONIA, FRANCONIA_CONTINUATION, les migrations ultérieures et les propriétaires réellement présents ont été confrontés. Ansbach, Bayreuth, Bamberg, Würzburg, Nuremberg, Eichstätt et Cobourg ne sont pas reconstruits une seconde fois. Le parent xEDA218 était un **résidu BAV**, issu de xD0C0A0 déjà BAV dans la baseline franconienne ; ce n’est pas un noyau souverain antérieurement transféré.

Tous les autres RGB impériaux sont protégés ; les cellules acceptées des anciennes migrations sont comparées à la capture R3. Belgique, Hesse–Nassau–Fulda, Souabe, Rhin–Westphalie et Thuringe sont conservés. Erfurt–Eichsfeld reste inchangé. La protection cumulative ne réécrit aucune ancienne baseline.

La validation R2-B déclarée dans le prompt est enregistrée séparément dans `../R2B/RUNTIME_USER_ATTESTATION.json` : nouvelle partie 1776, neuf vérifications, un mois, aucune anomalie signalée. C’est une attestation du joueur, pas un test automatisé ni une certification historique des catégories C ou des ajouts R3.

## Géographie et limites

La souveraineté et les successions sont recoupées avec l’atlas institutionnel du Bade-Wurtemberg, les archives territoriales et les notices d’autorité. La géométrie utilise les corps principaux de deux Ämter sur une reconstruction détaillée de Gerabronn vers 1800, **pas l’ensemble de cette carte tardive**. Continuité des noyaux dynastiques recoupée ; Werdeck 1797, achats de Niedernhall 1799, compensations de 1803 et condominiums exclus.

Les petites possessions détachées, dont les fragments orientaux proches des régularisations avec Ansbach, sont différées. Une cellule candidate WUR est laissée inchangée car son parent n’a pas été autorisé dans ce sous-lot. Aucun corridor ni agrandissement pour rendre un fragment visible.

**Institution A, géométrie B** : cellules sélectionnées par leur centre dans le tracé enregistré. Le contour carré peut empiéter sur des juridictions plus petites ; cela reste une généralisation de jeu documentée. Les contrôles de feuille Gerabronn/Schrozberg donnent 0,079/0,222 pixel **contre le même modèle diagnostique hérité**, pas contre des homologues physiques indépendants du bitmap. Ils ne démontrent donc pas une précision native subpixel. Aucune nouvelle optimisation d’Erfurt n’a été réalisée.

`SOURCE_ACCEPTED_REVIEW.png` montre chaque cellule replacée sur la source ; `BEFORE_AFTER.png` montre le changement dans le bitmap. `PLAYER_LOCATION_GUIDE.png` sert au contrôle en jeu. Voir `HISTORICAL_EVIDENCE.md` pour les sources et les anachronismes exclus.

## Démographie et économie

**Aucune population historique totale de ces principautés n’est revendiquée.** Les 2 213 et 2 950 habitants correspondent uniquement aux noyaux installés et à une allocation technique provisoire, par part des cellules de la subdivision donneuse BAV en Franconie. `ALLOCATION.json` conserve intégralement chaque profil culture/religion, avec arrondis entiers contrôlés. Total mondial avant/après : **835 801 255**, sans nouvelle population.

Niveaux de bâtiments, PM, propriétaires économiques, infrastructures, ressources, terres arables, locators, régiments et recrutements restent chez les subdivisions survivantes d’origine, inchangés. Aucune usine ou unité n’est répartie arbitrairement selon l’aire. Subsistance, emploi et accès au marché des nouveaux noyaux sont à inspecter en jeu ; une correction future exige ses propres preuves.

Les armes simplifiées communes aux deux branches utilisent deux léopards noirs sur fond blanc, avec des textures natives. Ce n’est pas la restitution de leurs pavillons complets.

## Contrôles

- **1 625 / 1 625** contrôles statiques cumulatifs : bitmap mondial exact, propriétaires, connexité, RGB, régions, profils démographiques, économie, capitales, personnages, références, localisations, droits impériaux et protections.
- **28 / 28** tests R3 ; **67 / 67** contrats courants du registre, centralisation, sujets, sécession et Saint-Gobain ; **40 / 40** tests conservés des livraisons R1/R2-A.
- R2-B : **25 / 26**. L’unique échec est son ancien contrat « R2-B est la dernière migration », désormais remplacé par R3. Test conservé, pas une régression de frontière.
- T/U : **30 / 39**, exactement les neuf échecs de snapshots d’étape déjà recensés, aucun nouvel identifiant. Ils sont distincts du contrôle cumulatif courant.
- **44 doublons RGB et 12 références invalides préexistants**, aucune nouvelle anomalie de ces classes.
- Références effectives vérifiées sur le mod et le vanilla canonique ; quatre tableaux CSV typés, rendus et relus cellule par cellule.
- HEAD et index inchangés ; aucun fichier militaire ou diplomatique américain écrit. Les modifications concurrentes déjà présentes dans la capture sont conservées. Aucun commit, staging, merge, reset, rebase ou push.

Résultats détaillés : `VALIDATION.json`, `TESTS.json`, `EARLIER_TEST_COMPARISON.json`, `REFERENCE_VALIDATION.json`, `INSTALLED_MANIFEST.json` et `CSV_REREAD.json`.

## Fichiers fonctionnels

Carte et géographie : `map_data/provinces.png`, `map_data/province_terrains.txt`, `map_data/state_regions/00_west_europe.txt`.

Historique : `common/history/states/00_states.txt`, `common/history/pops/00_west_europe.txt`, nouveaux historiques de pays et personnages `hln - map2w_r3.txt` / `hki - map2w_r3.txt`.

Nouveaux fichiers `1776_map2w_r3_hohenlohe.txt` de définitions de pays, drapeaux et armoiries ; gouvernement `00_1776_map2w_r3_hohenlohe.txt` ; localisations `1776_map2w_r3_l_french.yml` et `1776_map2w_r3_l_english.yml`.

Registre `MAP2L/IMPERIAL_DE_JURE_REGISTRY.json`, migration locale, garde étroite dans `tools/map2l_registry.py`, **17 fichiers impériaux dépendants recompilés** et carte DDS du journal. Le manifeste liste les chemins et empreintes exacts, y compris les fichiers partagés déjà modifiés avant ce lot.

## Suite délibérément non installée

Inventaire ciblé de 19 entrées : autres branches Hohenlohe, deux branches de Castell, deux branches de Löwenstein-Wertheim, Rothenburg, Schweinfurt, Windsheim, Weißenburg, autres juridictions et noyaux déjà traités. Les noms de branche ne sont pas une autorisation de création. Les titulaires ou contours encore non vérifiés sont indiqués explicitement.

Öhringen partagé avant 1782, Waldenburg comme ancienne lignée/possession et non septième TAG automatique, Schillingsfürst dans un noyau ANS protégé, propriétés dispersées et condominiums restent ouverts. Castell/Wertheim et villes libres attendent des sous-lots distincts ; aucune promesse de reconstruction intégrale dans cette livraison.

## ColGrep local

Un appel `C:\Users\simeo\.cargo\bin\colgrep.exe --agent "Locate retained historical map sources and unimplemented territorial decisions specifically for Hohenlohe branches, Castell and Wertheim, and Rothenburg Schweinfurt Windsheim Weissenburg. Old FRANCONIA/TRACING and FRANCONIA_CONTINUATION are known installed cores; do not return them alone. Return at most five useful paths with line ranges, no edits and no historical decisions." .`

Sortie 0, **250,793 s**. Les chemins et lignes utiles ont été relus ; l’agent a surtout rendu des emplacements déjà connus et un long fragment de générateur de rapport. **Aucune nouvelle source décisive ni recherche économisée démontrée.** Le journal ne donne pas de preuve indépendante du GGUF/backend réellement chargé : la configuration annoncée du modèle 2B ne vaut pas mesure instrumentée de son exécution. Aucun réglage changé, aucune reconstruction forcée de l’index. Les compteurs Codex et le nombre exact de recherches classiques n’ont pas été instrumentés ; pas d’économie de quota chiffrée revendiquée. Dans cette passe, le coût local est observable, son bénéfice n’est pas établi.
