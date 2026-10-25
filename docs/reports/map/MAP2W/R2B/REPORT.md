# MAP2W-R2-B — Complément Hesse–Nassau–Fulda

17 octobre 2026. Situation historique visée : **1er janvier 1776**.

**MAP2W_R2B_READY_FOR_SCOPED_RUNTIME_VALIDATION** : les corrections défendables ci-dessous sont installées. Ce statut ne signifie ni que toutes les juridictions de Hesse sont achevées, ni que les cas C ont été validés. **R2-B n’a pas été testé dans le moteur.**

## Ce qui n’a pas été refait

L’ordre chronologique des migrations et les fichiers actuels ont primé sur les anciennes listes de réserves. Les ensembles déjà reconstruits en Franconie, Rhin–Westphalie, Souabe, Anhalt et Thuringe, ainsi que Belgique, Poméranie, Wismar/Poel, Emden et Eutin, sont protégés. R1 : 39 cellules de Fulda et les quatre RGB xEDB600–603 ; R2-A : 72 transferts et les neuf RGB xEDB700–708. Aucun de ces nouveaux RGB ne sert de parent à R2-B. Erfurt–Eichsfeld est inchangé. Les sources, polygones et empreintes de cellules effectivement retenues sont conservés, pas seulement un aperçu dessiné.

La validation générale déclarée par le joueur pour les lots récents est enregistrée dans `../RUNTIME_USER_ATTESTATION_R2B.json` et les rapports R1/R2-A. Aucun détail d’inspection ou mois de simulation non indiqué n’y est ajouté. Les validations statiques datées de ces anciens lots restent conservées ; elles ne sont pas réécrites pour les faire correspondre au nouvel état.

## Corrections installées

| Secteur intérieur | Avant → après | Cellules | Population technique transférée |
| --- | --- | ---: | ---: |
| Sarrebruck–Saint-Jean–Ottweiler | KPF → **NSB**, Nassau-Sarrebruck | 15 | 16 814 |
| Hadamar–Ellar | NAS → NOU | 6 | 6 703 |
| Diez | NAS → NOU | 2 | 2 236 |
| Merenberg–Löhnberg | NAS → NWB | 2 | 2 235 |
| Usingen-centre | HES → NAS | 5 | 4 294 |
| Wiesbaden | FRM → NAS | 6 | 3 747 |
| Geisa–Rasdorf | MEI → FUL | 6 | 1 515 |
| Dermbach | MEI → FUL | 2 | 505 |
| Herbstein | HEK → FUL | 1 | 891 |
| **Total** | | **45** | **38 940** |

KPF est le pays palatin du mod, non Nassau-Sarrebruck ; son reste n’est pas annexé. Le nouveau **NSB** a Ludwig von Nassau-Saarbrücken, né le 3 janvier 1745, comme prince, une monarchie héréditaire, des localisations françaises et anglaises et les armes nassoviennes simplifiées existantes. Sa capitale technique est `STATE_RHINELAND` ; les locators de la région économique commune ne sont pas déplacés. Aucune sujétion native, union personnelle ou dignité électorale ajoutée.

**Institution A, géométrie B** : les souverainetés sont recoupées avec les archives et notices datées ; les cellules sont une généralisation prudente d’intérieurs sur les cartes historiques. Voir `HISTORICAL_EVIDENCE_R2B.md`. Pas de frontières modernes rétroprojetées, pas d’échanges de 1777/1781 ni d’acquisitions de 1799/1803. Pas de corridor ajouté pour relier les noyaux. Les résidus techniques laissés à leur propriétaire ne sont pas certifiés historiquement.

Treize couleurs nouvelles **xEDB800 à xEDB80C**, terrain hérité, registre impérial **554 → 567 RGB**. Un des nouveaux RGB conserve un morceau HES devenu déconnecté : changement de couleur technique, pas transfert de souveraineté. Les régions économiques restent `STATE_HESSE` **74**, `STATE_RHINELAND` **63**, `STATE_SAXONY` **73**. Les ID numériques sont lus dans les définitions, pas déduits des RGB.

Le hub minier de Rhénanie à **(4268, 879)** pointe désormais sur xEDB800, à la même position physique. C’est une mise en cohérence de référence avec le bitmap, **pas un transfert des mines ni des ressources**. À examiner en jeu : le rendu des bâtiments dans une région partagée ne prouve pas leur propriétaire économique.

## Populations et économie

Population mondiale **835 801 255 → 835 801 255** ; chaque profil culturel/religieux est conservé par nombres entiers. La conservation est ici un transfert technique, **pas une estimation démographique historique de 1776**. Aucune population artificielle n’a été ajoutée pour rendre NSB viable. Les séries historiques manquent pour substituer un recensement territorial défendable à cette allocation. Les 20 047 habitants techniques déjà attribués à FUL ne sont pas retirés ; 2 911 habitants techniques provenant des nouvelles possessions s’ajoutent.

| Pays | Avant R2-B | Après R2-B |
| --- | ---: | ---: |
| NSB | 0 | 16 814 |
| NAS | 309 489 | 306 356 |
| NOU | 27 710 | 36 649 |
| NWB | 12 265 | 14 500 |
| FUL | 20 047 | 22 958 |

La répartition de diagnostic par RGB dans `TERRITORY_POPULATION_DETAIL.json` décompose les transferts par profils ; le moteur conserve ses pops au niveau de la subdivision économique, pas dans chaque pixel. Ne pas additionner les lignes de détail par profils et les lignes de transfert du CSV comme deux populations différentes.

Tous les bâtiments, niveaux, PM et propriétaires économiques sont identiques à la capture immédiate. MAP ne modifie aucune formation ou unité ; les changements américains simultanés sont séparés, et les unités non américaines restent identiques à la capture. Les donneurs gardent leurs bâtiments dans leur subdivision survivante : aucune localisation industrielle n’est inventée d’après une proportion de pixels. Aucun plafond de ressource, capacité arable ou trait n’a été augmenté. Le nouveau NSB commence sans usine arbitraire ; subsistance, emploi et marché restent à contrôler en jeu.

## Contrôles et limites

- **1 670 / 1 670** contrôles statiques : bitmap mondial exact, propriétaires uniques selon les références existantes, connexité de chaque RGB, profils de population, titres du registre, replay chronologique des migrations, ressources/ID/hubs et protection des autres régions.
- **26 / 26** tests ciblés R2-B, dont rejets d’une attribution prussienne de Sarrebruck, d’une cellule hors périmètre et d’un parent provenant d’un noyau antérieur.
- **67 / 67** contrats cumulatifs impériaux et tests de l’icône Saint-Gobain.
- **40 / 40** tests des attestations statiques de livraison R1/R2-A ; ce ne sont pas de nouveaux tests moteur de ces lots.
- Anciens instantanés T/U : **30 / 39**, les **mêmes neuf identifiants de tests déjà en échec** en R2-A. Sept comparent un stade ancien avec la carte/pays désormais étendus ; deux couvrent des divergences économiques/militaires antérieures. `EARLIER_TEST_COMPARISON.json` ne masque ni ne corrige leurs baselines. Les invariants actuels sont vérifiés indépendamment contre la capture immédiate.
- **44 doublons RGB et 12 références invalides préexistants**, inchangés ; aucune nouvelle référence invalide dans l’inventaire. Références effectives de NSB contrôlées séparément : technologies, lois, effets, culture, religion, idéologie, gouvernement et armes.
- **73 / 73** sorties du compilateur impérial reproduites avant la passe ; 17 sorties actualisées avec le nouveau membre, et les 73 sorties attendues comparées à l’installation. Neuf électeurs et règles conservés : lien 0 %, état 15 %, électorat 10 %.
- Quatre CSV typés, calculés/inspectés et rendus avec le workflow tableur ; chaque cellule exportée relue. Comparatifs et empreintes sur les cartes sources examinés visuellement. Aucun de ces contrôles n’est un test exécuté par Victoria 3.

Restent C : Hesse-Hombourg, statut moteur de Hanau-Münzenberg, branches/apanages hessois, condominiums et franges complémentaires de Nassau/Fulda, périphérie de Sarrebruck et Sarrewerden. Les gouvernements de NAS/NOU/NWB de R2-A sont conservés : vérifier séparément les titres européens prince/duc, dont le filtrage vanilla ne dépend pas du seul rang technique. NSB dispose d’un type princier borné. Drapeau et démographie historique restent des abstractions documentées.

## Coexistence et fichiers

La capture immédiate tient compte des modifications locales déjà présentes, suivies ou non. Aucun fichier militaire, colonial, portugais, américain ou économique français n’est un fichier MAP de cette passe.

Une mise à jour **externe** vers `9b1764e` (PR8, prospérité de Dollfus-Mieg) a été observée dans le reflog, ainsi que les fichiers du chantier USA–France du collaborateur : **31 fichiers externes explicitement recensés**, dont sociétés françaises et fichier militaire nord-américain. Ce dernier ne diffère de HEAD que dans le bloc USA : commandants et type de navire marchand armé. Aucun bloc militaire non américain n’a changé. Ces fichiers sont préservés, jamais restaurés, et leurs empreintes observées sont séparées dans `CONCURRENT_WORK_OBSERVED.json`. Le collaborateur continuant ses écritures, ces empreintes ne sont pas un verrou global : les contrôles protègent les sorties MAP et les blocs hors USA, plutôt que d’exiger l’immobilité du chantier autorisé. Seul le bloc de prospérité DMC change dans le fichier de sociétés ; Saint-Gobain et Anzin y restent identiques. La validation de préservation ne certifie pas le fonctionnement du chantier américain. Aucune opération Git d’écriture n’a été effectuée par cet agent.

**30 fichiers d’exécution MAP** : liste exhaustive et empreintes dans `INSTALLED_MANIFEST.json` et `VALIDATION_R2B.json`, séparées des travaux externes. Principaux fichiers : bitmap, terrains, régions de carte, historiques d’états et de populations, nouveau pays/personnage/historique/drapeau/gouvernement NSB, localisations FR/EN, sorties impériales générées. Hors exécution : registre, migration, garde explicite de `tools/map2l_registry.py`, outillage, preuves et rapports. Aucun changement de l’installation canonique `C:/Games/Victoria 3`, version constatée **1.13.11**.

Reproduction locale des contrôles : `tools/map2w_r2b_completion.py validate`, puis `references`, `tests`, `csv_verify`, avec le Python du workflow. **Ne pas relancer capture/prepare/install** sur une passe installée : leurs gardes protègent la capture immuable. Les deux cartes demandées sont `HESSE_NASSAU_R2B_BEFORE_AFTER.png` et `PLAYER_LOCATION_GUIDE.png`.

## ColGrep

Deux tentatives de commande `C:/Users/simeo/.cargo/bin/colgrep.exe --agent` : la première bloquée par l’accès au verrou d’index, puis une exécution locale réussie avec accès à l’index existant, sans reconstruction complète ni modification de modèle. **112,55 secondes** chronométrées pour la commande aboutie, incluant son orchestration. Sortie : `COLGREP_SEARCH.log`.

Deux localisations utiles retournées et vérifiées : `../R2/HISTORICAL_EVIDENCE_R2.md:13–15` et `tools/map2w_r2_hesse_nassau.py:60–68`. Elles renvoient aux sources et outils déjà connus : pas une nouvelle preuve historique. La sortie ne comporte pas de bannière ou trace du fichier GGUF permettant de certifier indépendamment le backend 2B précis ; seul le succès de la commande `--agent` est constaté. La première tentative n’a pas lancé de recherche exploitable.

Identifiants et formats non indexés traités directement par recherches exactes ; compteur total de recherches classiques non instrumenté, lectures non assimilées à des recherches. Tokens Codex et temps d’inférence seul indisponibles. Aucune recherche évitée ni économie de quota chiffrée démontrable. Intérêt observé limité dans ce lot, où les emplacements étaient surtout connus ; la délégation ne remplace ni la lecture des sources ni la responsabilité de l’implémentation.

## Suite

Voir `RUNTIME_TEST_PLAN.md` pour le contrôle limité aux ajouts, et `NEXT_SEQUENCE.md` pour R3/R4. **Aucun de ces deux prochains lots n’est commencé automatiquement.**
