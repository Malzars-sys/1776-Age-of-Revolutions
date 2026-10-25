# ECON-ALLOYS-1776 — Quincaillerie et débouchés des alliages

Révision du 24 octobre 2026 : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

Cette version remplace les meubles supplémentaires par le bien distinct **Quincaillerie / Hardware**, selon la nouvelle demande du joueur. Les documents et résultats précédents sont conservés dans `V1_ARCHIVE/`. La baseline initiale reste intacte ; `HARDWARE_BASELINE.json` photographie le workspace immédiatement avant cette révision.

## Bien courant et recettes

`aor1776_hardware` : catégorie native **staple**, prix de base 30 £, échangeable, quantité commerciale 8, coût en convois 0,25, coût de taxe de consommation 300, facteur de prestige 4. Ce sont les conventions des biens courants comparables, sans besoin de luxe ni nouveau besoin général.

Le groupe secondaire de la manufacture de meubles se nomme **Fabrication de quincaillerie**. Ses identifiants historiques `_utensils` sont conservés pour préserver les références. Les recettes principales et de luxe restent inchangées par cette révision. Valeurs par niveau pleinement employé et par semaine :

| PM | Entrants | Quincaillerie | Emplois ajoutés | Technologies existantes |
|---|---|---:|---|---|
| Aucune fabrication | Aucun | 0 | Aucun | Aucune |
| Forgée et moulée | Fer 4, alliages 4 | 20 | Ouvriers 450, machinistes 50 | `organized_workshops` + `alloysworking` (II) |
| Cuivre et laiton | Fer 6, cuivre 3, alliages 5 | 40 | Ouvriers 700, machinistes 150 | Mêmes technologies (II) |
| Usinée | Acier 6, cuivre 4, plomb 3, alliages 7 | 80 | Ouvriers 900, machinistes 400, ingénieurs 100 | `mechanical_tools` (V) + `alloysworking` |
| Industrialisée | Acier 10, cuivre 6, plomb 4, alliages 10, aluminium 8 | 160 | Ouvriers 1 200, machinistes 700, ingénieurs 300 | `mechanical_tools` + `bayer_process` (X) |

Tous les paliers actifs consomment des alliages, dès le premier. Le nombre de matières augmente de 2 à 3, 4 puis 5 ; les sorties passent de 20 à 40, 80 puis 160, contre les anciens 2/5/8/16 meubles. La dernière recette comporte bien les cinq métaux demandés, avec l'acier à la place du fer.

Le groupe ne produit **aucun meuble**, à aucun palier. La quincaillerie a son propre marché ; les groupes de meubles/luxe conservent leurs propres sorties. Le neutre, premier dans la liste suivant les modèles natifs, retire intégralement les effets secondaires. Le choix effectif du moteur/IA reste à observer. Les matières et sorties sont en `workforce_scaled`, les emplois en `level_scaled`.

Les matières représentent différents objets d'un assortiment, pas une composition unique d'alliage. Le plomb tardif représente notamment poids et garnitures non alimentaires. Aucun mercure.

## Besoins domestiques

Ajout uniquement dans `popneed_household_items`, dont les paniers commencent à richesse 10 :

| Bien | Poids | Plancher d'offre | Plafond d'offre |
|---|---:|---:|---:|
| Alliages, faible demande directe conservée | 0,02 | 0,01 | 0,05 |
| Quincaillerie, objets finis courants | 1 | 0,02 | 0,35 |

Les valeurs pondèrent une substitution selon l'offre ; ce ne sont pas des pourcentages littéraux de toutes les dépenses. Meubles, verre, papier, paniers et produit par défaut restent inchangés. La demande de quincaillerie est volontairement plus significative que l'achat direct d'alliages. Les richesses inférieures à 10 n'ont pas ce besoin dans les paniers actuels ; « courant » désigne sa catégorie et son usage, sans imposer un nouveau panier à tous les ménages.

## Métallurgie et artillerie conservées

La première refonte reste appliquée : **3 fer + 4 cuivre + 1 plomb + 2 charbon → 20 alliages**, 2 200 emplois, au lieu de 25/15/10/10 → 60 avec 5 000 emplois. Le nom reste **Fabrication traditionnelle d'alliages**. À prix de base et salaire annuel d'ouvrier de référence de 10 £ : +108,85 £/semaine après salaires pour le PM seul ; +285,31 £ pour la combinaison initiale examinée avec les autres groupes du bâtiment. Aucun profit à tous les prix n'est garanti.

L'artillerie en bronze reste **10 fer + 10 bois dur + 4 alliages → 25 artillerie**. L'alternative fer reste 15 fer + 10 bois dur → 25, avec les mêmes emplois et le même coût matière de base. Déblocage bronze : `standardized_field_artillery` et `alloysworking`.

Les recettes électriques et d'aluminium restent intactes ; l'arc produit toujours 90. Aucun nœud, parent technologique ou profil national n'est modifié par cette révision, aucun coke distribué. La faiblesse de marge du PM électrique isolé à certains salaires est préexistante et reste différée.

## Rentabilité et capacité

Le ratio valeur produite/coût matière croît : **1,667 → 1,875 → 2,474 → 2,581**. Aux prix de base et au salaire annuel de référence de 10 £, les marges incrémentales après salaires sont **+139,04 / +382,12 / +1 083,85 / +2 334,23 £ par semaine**. Les quatre paliers restent positifs avec matières +25 %. Les emplois augmentent réellement : 500/850/1 400/2 200.

Une usine traditionnelle fournit cinq premiers paliers, quatre deuxièmes ou deux derniers si elle ne fournit rien d'autre. Les volumes accrus exigent donc une expansion réelle de la métallurgie. La vente de toute cette quincaillerie dépend de la demande et des prix locaux ; les cas statiques ne prouvent pas un équilibre mondial.

Voir [BALANCE_REVIEW.md](BALANCE_REVIEW.md), `HARDWARE_PM_MATRIX.csv`, `HARDWARE_BEFORE_AFTER.csv`, `ALLOY_DEMAND_BEFORE_AFTER.csv` et `BASE_PRICE_STRESS.json`.

## Image, fichiers et localisations

L'image du joueur est détourée avec imagegen intégré : fond et cadre retirés, transparence réelle autour et entre les objets, notamment dans l'anse. PNG maître : `workshop_assets/source/aor1776_hardware_transparent.png`. Texture de jeu : `gfx/interface/icons/goods_icons/aor1776_hardware.dds`, 256 × 256, BGRA8 natif, neuf mipmaps, alpha conservé. Le premier PM réutilise aussi cette icône. [Aperçu](HARDWARE_ICON.png), [prompt et provenance](ARTWORK.md).

Créations de cette révision : définition du bien dans `common/goods/1776_hardware.txt`, quatre types de modificateurs dans `common/modifier_type_definitions/1776_hardware.txt`, symbole dans `gui/1776_hardware_texticons.gui`, PNG/DDS et `tools/build_hardware_icon.py`.

Modifications ciblées : `common/production_methods/1776_alloys_utensils.txt`, une entrée de `common/pop_needs/00_pop_needs.txt`, les deux localisations `1776_alloys_utensils_l_*.yml`, outils/tests et rapports. Trente et une clés par langue, UTF-8 BOM, sans collision recensée ; variantes de modificateurs simples et préfixées couvertes. Inventaire : `FILES_MODIFIED.json`.

## Tests, coexistence et ColGrep

**16 tests ciblés réussis** : syntaxe/références, bien courant, modificateurs et symbole, recettes/emplois, alliages à tous les paliers, progression, absence de sortie de meubles, neutralité/cumul, technologies, langues/BOM et alpha PNG/DDS. Comparaison des autres objets aux empreintes d'avant cette révision ; aucun changement externe observé pendant cette révision dans ce relevé.

Les chantiers antérieurs Raguse, carte et ports restent présents et consignés séparément. Aucun fichier territorial, population, diplomatie, registre impérial ou validation humaine n'est écrit par cette révision. Aucun staging/commit/push ni modification de HEAD ou de l'index.

L'ancien validateur garde les mêmes quatre erreurs : trois attentes relatives aux trains de voyageurs et une ancienne attente de parent unique pour `alloysworking`. **Aucune nouvelle erreur**. Voir `TEST_RESULTS.json`.

Un appel local ColGrep `--agent` a abouti, après une première tentative empêchée par l'accès au cache. Les pistes vérifiées ont retrouvé un bien courant (sel), le bloc domestique et les conventions d'enregistrement/localisation des modificateurs. L'extrait de 455 lignes était trop large mais utile pour cette dépendance. Aucun changement de modèle ou d'intégration, aucune reconstruction d'index. Temps d'inférence et tokens Codex non mesurés, aucune économie exacte annoncée. Voir `COLGREP_METRICS.json`.

## Validation restante

Le moteur n'a pas été lancé. Le rendu, les choix de l'IA, les dépenses domestiques et la rentabilité aux prix locaux restent à valider. [PLAYER_TEST_PROTOCOL.md](PLAYER_TEST_PROTOCOL.md) prévoit une nouvelle partie, un mois complet puis sauvegarde/rechargement. Une ancienne sauvegarde n'est pas certifiée compatible avec cette nouvelle marchandise.
