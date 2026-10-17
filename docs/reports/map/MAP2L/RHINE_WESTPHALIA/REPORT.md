# MAP-2L — Rhin / Westphalie, noyaux territoriaux appliqués

14 octobre 2026 ; démarrage visé : **1er janvier 1776**.

**Mise à jour : PASS_RUNTIME_USER_VALIDATED.** Le joueur rapporte le bon fonctionnement des territoires Rhin–Westphalie et principautés impériales inspectés dans une nouvelle partie. Il s'agit d'un test manuel déclaré, pas d'un test automatisé, ni d'une certification de toutes les frontières ou de tous les mécanismes. Le nouveau sous-lot de Minden réalisé pendant le tour suivant n'est pas inclus. `../RUNTIME_USER_VALIDATION.json` conserve cette portée ; les anciennes mentions « moteur non testé » décrivent la situation avant cette confirmation. Les anomalies héritées et juridictions incomplètes demeurent ouvertes.

L'écart Git documenté plus bas correspond au commit personnel `f34a6b8`, explicitement autorisé ensuite par le joueur. Vérification fraîche avant reprise : vingt RGB et 1 081 cellules intacts, aucun échec de gameplay. Les anciennes baselines et attestations brutes ne sont pas réécrites ; voir `AUTHORIZED_GIT_EVENT.json`.

**Modifications réelles : huit RGB mixtes subdivisés en 28 composantes, vingt nouveaux RGB et 1 081 cellules changeant de propriétaire.** Deux pays épiscopaux sont restaurés ; des fragments de Juliers–Berg rejoignent le Palatinat existant. Ce sous-lot ne prétend pas achever tout le Rhin et la Westphalie, ni valider le résultat en jeu.

## Propriétaires avant / après

Les chiffres concernent les portions transférées, pas la surface historique exhaustive d'une principauté. Les restes de chaque parent sont maintenus à PRU sans certification générale de leur souveraineté historique.

| RGB parent | Région économique / ID | Avant | Portion transférée après | Cellules |
| --- | --- | --- | --- | ---: |
| x1DD141 | STATE_WESTPHALIA / 61 | PRU | WPM : x1DD141, xEDA903 | 302 |
| x910095 | STATE_WESTPHALIA / 61 | PRU | WPM : x910095 | 125 |
| x218061 | STATE_WESTPHALIA / 61 | PRU | WPD : x218061 | 203 |
| x4101A0 | STATE_WESTPHALIA / 61 | PRU | WPD : xEDA90B | 93 |
| x2101E0 | STATE_RUHR / 584 | PRU | KPF : x2101E0 | 167 |
| xD08021 | STATE_RUHR / 584 | PRU | KPF : xD08021 | 96 |
| x8001E0 | STATE_NORTH_RHINE / 64 | PRU | KPF : xEDA912 | 47 |
| x834B66 | STATE_NORTH_RHINE / 64 | PRU | KPF : xEDA913 | 48 |
| **Total** | | | | **1 081** |

Les huit masques parents représentent 2 061 cellules : **aucune n'est perdue**. Le changement de couleur du bitmap concerne 683 cellules seulement : certains anciens RGB restent présents mais changent de contrôleur. Propriété et identité RGB sont donc contrôlées séparément. Aucun RGB original n'est supprimé ; les nouveaux vont de `xEDA900` à `xEDA913`.

`TERRITORIAL_CHANGES.csv` liste les 28 composantes, y compris les restes prussiens. `GEOMETRY.json` garde les cellules et filiations exactes. Les State Regions restent des régions économiques partagées : **61, 64 et 584 ne deviennent pas des identifiants d'États historiques**.

## Juridictions et preuves réutilisées

Les recommandations originales R2-0030/0032 et R2-0054/0055/0056 sont relues directement dans `MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv`. Elles avertissaient déjà que les régions rhénanes et westphaliennes ne pouvaient pas être intégralement prussiennes. Ce sont des conclusions de souveraineté et des domaines d'examen, **pas une correspondance RGB suffisante à eux seuls**. Les dossiers séparés de ces cinq lignes « inchangées » n'existent pas : leurs données sont dans le CSV conservé.

La carte Vaugondy de 1753, édition 1777, déjà conservée dans `RHINE_CENTRAL`, sert à la confrontation régionale. Le SVG dynastique de 1789 conservé est rendu uniquement comme comparaison : ses catégories agrègent les autorités ecclésiastiques et Bavière/Palatinat ; elles ne sont **pas** utilisées comme classes d'attribution automatique. L'atlas Freeman/Bury de 1780 cité par R2 demeure une référence générale ; sa reproduction en ligne n'a pas été récupérée par l'outil web et n'est pas présentée comme une nouvelle carte finement exploitée.

Un seul complément cartographique ciblé est acquis : **Peter Schenk, cercle du Bas-Rhin–Westphalie, 1710/1730**, présenté par le [LWL, contexte historique 1648–1770](https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=33&url_tabelle=tab_websegmente), avec une reproduction lisible [Commons, source attribuée au LWL](https://commons.wikimedia.org/wiki/File:Reichskreis_Niederrhein-Westfalen_1710.jpg). Les deux versions sont conservées séparément : petite reproduction LWL 581 × 700 et reproduction Commons 1 978 × 2 400. Métadonnées, dates, URLs et hashes dans leurs fichiers `.SOURCE.json`. La grande reproduction sert au tracé ; le titre de cercle n'est pas assimilé à une juridiction souveraine unique.

- **Münster, WPM** : noyau de l'Oberstift, séparé des enclaves et comtés identifiables de Steinfurt et de Rietberg. Le [LWL, période 1770–1815](https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=34&url_tabelle=tab_websegmente) distingue l'État épiscopal et sa sécularisation ultérieure. Maximilian Friedrich, également électeur de Cologne, est représenté par une seconde instance native du même titulaire : **deux juridictions, pas deux personnes historiques ni une fusion administrative**. L'union personnelle n'est pas un nouveau mécanisme de sujet.
- **Paderborn, WPD** : enveloppe conservatrice du territoire épiscopal, sans transformer Lippe ou Corvey en possessions paderbornaises. [L'archidiocèse confirme Wilhelm Anton von der Asseburg, titulaire de 1763 à 1782](https://www.erzbistum-paderborn.de/news/sedisvakanz-im-kriegsgeschehen/). Son âge de départ est 68 ans. La [prise de possession prussienne documentée en 1802](https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=338&url_tabelle=tab_chronologie) n'est pas anticipée.
- **Berg et fragment de Juliers, KPF** : des portions des enveloppes nommées de la carte rejoignent Charles-Théodore et le Palatinat-Sulzbach existant. Pas de nouveau tag pour Berg, pas de transfert à la Bavière avant 1777–1778. Les administrations restent distinguables par leurs régions économiques ; un même TAG représentant leur souverain n'est pas l'affirmation d'une administration unique. Le partage Clèves/Mark/Ravensberg d'une part et Juliers/Berg d'autre part est confronté au contexte institutionnel du LWL, sans recopier les changements postérieurs.

Les acquisitions postérieures à la carte Schenk, notamment la Gueldre prussienne, ne sont pas déduites automatiquement d'une carte de 1710. Les seigneuries non représentables ne reçoivent pas chacune un nouveau pays.

## Approximation géographique explicitement conservée

Les polygones sont des **enveloppes conservatrices de juridictions nommées**, simplifiées à l'échelle du jeu et intersectées uniquement avec les huit parents listés. Ce n'est ni un cadastre, ni une partition par ville la plus proche, ni un transfert de province entière décidé par un nom de bâtiment.

Le nouveau raccord local Schenk utilise les symboles imprimés de Münster, Paderborn et Düsseldorf et leurs correspondances approximatives dans le jeu. Les deux premiers sont des locators rural/minier : ils ne sont pas présentés comme des centres urbains géodésiques certifiés. Les trois points d'ajustement ont un résidu nul **par construction** ; cela ne prouve pas l'exactitude physique des limites.

Contrôles non ajustés, comparés aux locators du jeu : **Cologne 10,930 pixels, Bonn 7,992 pixels**, moyenne 9,461, maximum 10,930. `CALIBRATION_DIAGNOSTICS.json` conserve ces écarts. Ce modèle ne doit pas servir à déplacer la ville libre de Cologne, une petite enclave ou une frontière disputée de quelques pixels. L'implémentation accepte seulement l'approximation politique de grands noyaux autorisée pour cette reprise. Les anciennes allocations de Cologne et les petits territoires non établis restent exclus des transferts ; aucune précision inférieure à deux pixels n'est revendiquée.

Les anciens modèles de Mayence et d'Erfurt ne sont ni remplacés ni réoptimisés. La translation d'Erfurt–Eichsfeld reste rejetée ; aucun de ses territoires n'est modifié. Les superpositions `SK_OVERLAY.png` et les lectures quadrillées permettent de vérifier les enveloppes sources, indépendamment de la carte politique générée.

## Conservation et dépendances

Les habitants sont répartis une seule fois à partir des profils initiaux et du poids de la subdivision source complète, avec arrondis conservatifs. **Aucune population artificielle, conversion religieuse ou modification culturelle.** Ce n'est pas un recensement des districts de 1776.

| Destination | Population transférée depuis PRU |
| --- | ---: |
| Münster, WPM | 140 455 |
| Paderborn, WPD | 97 365 |
| KPF dans STATE_RUHR | 97 279 |
| KPF dans STATE_NORTH_RHINE | 40 070 |
| **Total** | **375 169** |

Population mondiale : **835 804 980**, inchangée, avec conservation de tous les profils régionaux et des religions résolues. Lippe et Schaumbourg-Lippe gardent leurs provinces et populations.

**Tous les bâtiments, niveaux, PM et propriétaires économiques sont inchangés dans cette passe.** Aucun niveau entier n'est transféré par l'allocation conservatrice ; aucun fichier d'historique de bâtiments n'est modifié. Les trois subdivisions prussiennes subsistent, permettant de conserver les détenteurs privés et recrutements. Armées, marines, formations et effectifs restent identiques ; aucun contingent hypothétique n'est ajouté.

Deux références de hubs changent, **sans déplacement de leurs coordonnées** :

- `STATE_WESTPHALIA.wood`, Essen : `x1DD141` → `xEDA900`, à (4263, 808). Le fragment reste PRU ; cette correction de référence n'attribue pas l'abbaye ni la ville entière à Münster.
- `STATE_RUHR.mine`, Wuppertal : définition `xD08021` → `xEDA90D`, à (4268, 822). Avant la passe, le locator échantillonnait déjà `x2101E0` plutôt que le RGB déclaré : ce décalage de référence préexistait. Il est corrigé vers la cellule effective, sans traiter le nom Wuppertal comme une preuve géographique de souveraineté. Ce locator reste sur une frange non transférée.

Les listes de `prime_land` s'étendent à tous les descendants des parents concernés : **leur empreinte en pixels est exactement conservée**, ainsi que les ressources, quantités de terres arables et identifiants des régions. Les capitales des nouveaux pays se trouvent dans une région économique effectivement possédée ; cela ne certifie pas l'emplacement d'un nouveau centre urbain. Aucun nouveau State_ID ou locator physique.

Les deux pays reçoivent le modèle de départ épiscopal déjà utilisé pour Bamberg, sans technologies supplémentaires ni preset politique incompatible. Les deux variantes de lois de départ sont limitées à WPM/WPD ; les anciennes variantes et gouvernements ne sont pas retouchés. Noms, titulaires et descriptions sont localisés en français/anglais. Les bannières procédurales servent à les identifier ; ce ne sont pas des armoiries historiques certifiées.

WPM/WPD rejoignent le bloc et le registre impériaux, **sans nouveaux électorats**. Les règles de restitution, vote, succession et centralisation restent celles du mod ; seules leurs listes et dépendances sont recompilées. Aucune ville libre nouvelle n'est inventée. Les droits déjà intégrés de Cologne, Mayence, Trèves, du Palatinat et des villes libres sont conservés.

Registre actif : **403 → 423 RGB**, empreinte impériale inchangée à **62 580 cellules**. Cartes principale et du journal régénérées ; leurs textures sont sans ajout ni omission d'étendue. Belgique, Liège, Stavelot-Malmedy, Piémont, Franconie et ses neuf RGB, Mayence et Milan sont contrôlés cumulativement.

## Fichiers modifiés

Chemins exacts des fichiers textuels : `PLAN.json` et `IMPERIAL_FILES.json`. Principaux groupes :

- Bitmap/terrain : `map_data/provinces.png`, `map_data/province_terrains.txt`.
- Géographie/historiques : `map_data/state_regions/00_west_europe.txt`, `common/history/states/00_states.txt`, `common/history/pops/00_west_europe.txt`.
- Nouveaux pays : `common/country_definitions/1776_map2l_westphalian_estates.txt`, historiques `wpm - westphalian estate.txt` et `wpd - westphalian estate.txt`, personnages `1776_map2l_westphalian_rulers.txt`, variantes `1776_map2l_westphalian_start_variants.txt`, drapeaux et localisations `1776_map2l_westphalia`.
- Registre : `MAP2L/IMPERIAL_DE_JURE_REGISTRY.json`, `REGISTRY_MIGRATION.json` de ce dossier et chaîne explicite dans `tools/map2l_registry.py`.
- Intégration : les 16 fichiers impériaux listés dans `IMPERIAL_FILES.json` ; les trois textures DDS listées par les outils de cartes.
- Outils : `tools/map2l_westphalia.py`, `tools/render_map2l_westphalia_source.cjs`, `tools/validate_map2l_westphalia.py`, `tools/test_map2l_registry.py`. Extensions ciblées de `map2l_mainz.py` et des validateurs cumulés `validate_map2l_mainz.py`, `validate_map2l_franconia.py`, `validate_map2l_rhine.py`, `validate_map2l_franconia_continuation.py`, `validate_map2l_mainz_completion.py`.

Les validateurs n'acceptent pas une liste blanche vague : nouvelles définitions exactes déclarées, anciennes définitions inchangées, et rebindings de champs précis. Des tests négatifs rejettent l'écrasement d'un pays existant, une addition non déclarée, une mauvaise référence antérieure, une mutation de ressource/ID et une modification hors région approuvée. Les instantanés originaux ne sont pas remplacés. Le nettoyage d'espaces concerne seulement les lignes ajoutées dans les deux historiques.

## Vérifications et alerte Git distincte

Le nouveau lot obtient **540 contrôles techniques/cartographiques réussis sur 540**, plus une attestation Git qui échoue. **Le résultat brut du validateur reste donc FAIL, 540/541** ; il n'est pas maquillé en succès global. Les dix tests unitaires des migrations passent. Les 16 contrôles de la carte principale passent hors moteur, y compris la compilation du helper HLSL dans son harnais — pas la compilation complète du shader par Victoria 3.

Les suites cumulées Belgique, Piémont, Franconie, Rhin central, Mayence–Palatinat, possessions de Mayence, prolongement méridional, Milan et prolongement franconien passent leurs contrôles de gameplay. Chaque suite conserve la même attestation Git échouée ; résultats et noms exacts des échecs dans `NON_REGRESSION.json`. Aucun nouvel échec de conservation, référence, propriété, compilation des textes ou géométrie.

**Pourquoi Git échoue :** la baseline figeait HEAD `c891b1d9bb2a21bc42409acbdccc268518110260`. Pendant la passe, le commit `f34a6b88db749a8be77ec558fd55ad196b45f72a`, signé *Malzars-sys*, daté du 14 octobre 2026 à 10:43:12 +02:00 et intitulé « First batch of the historical map's v1 », est apparu comme son successeur. HEAD et l'index ont changé hors de ce workflow. Aucune commande de commit, staging, merge, rebase, reset ou push n'a été exécutée par l'assistant ; le commit observé n'est pas annulé et les baselines ne sont pas réécrites pour faire disparaître l'alerte.

Incidents réparés pendant la vérification : références de hubs distinctes d'un même ancien RGB, ordre d'insertion des deux nouveaux boutons de vote, et ancienne assertion de Mayence qui interdisait tout changement ultérieur en Westphalie. Les contrôles sont désormais cumulés avec les seules migrations exactes approuvées ; la géométrie rejetée d'Erfurt reste explicitement protégée. La différence d'ordre des boutons a été corrigée et toutes les sorties du compilateur correspondent aux fichiers runtime.

**Préexistant, séparé des régressions :** mêmes 44 RGB doublement attribués et 12 erreurs de références héritées hors de ce lot. Les défauts de formatage déjà présents ne sont pas nettoyés globalement. Le décalage déclaré/échantillonné du locator Wuppertal est documenté ci-dessus.

**Moteur non testé.** Ne pas lancer avant la fin des lots impériaux, selon la consigne conservée. À vérifier ensuite dans une nouvelle campagne au 1er janvier 1776 : sélection et portraits WPM/WPD, gouvernements/lois, capitales économiques partagées, provinces restaurées, les deux références de hubs, carte principale, journal, restitutions et logs. Une ancienne sauvegarde ne valide pas ces historiques.

## Ce qui reste ouvert

- Le **duché de Westphalie** devra rejoindre KCL sur son propre tracé, pas devenir un pays souverain. Il n'est pas redistribué dans ce sous-lot ; ne pas interpréter les restes PRU comme une certification de leur souveraineté.
- Clèves/Mark/Minden/Ravensberg et la Gueldre prussienne : distinguer les possessions déjà détenues des gains de 1802–1815. Leurs limites fines ne sont pas toutes validées ici ; la Gueldre et Hannover sont exclus de toute modification de cette passe.
- Osnabrück, Niederstift Münster, Bentheim, Nassau et ses branches : conserver leurs statuts particuliers et les distinguer administrativement. Pas de fusion anticipée dans un duché de Nassau de 1806.
- Aix-la-Chapelle, Cologne ville libre, Dortmund et Essen : souveraineté et juridictions doivent rester distinctes des princes voisins. La [ville de Cologne documente son statut libre](https://www.stadt-koeln.de/mediaasset/content/verwaltung/stk_br_ko%CC%88lner_rathaus_a5_rz_web-pdf__003_.pdf) ; ce statut ne fournit pas à lui seul un polygone jouable. Cette passe n'invente pas de frontières rurales à partir d'un symbole de ville, ni de pays pour chaque micro-enclave. Les représentations actuelles non résolues sont signalées, pas approuvées historiquement.
- Les franges restantes de Juliers–Berg et des évêchés, Steinfurt/Rietberg/Corvey et autres petites autorités nécessitent leur attribution propre. Les portions exclues ne sont pas données par proximité à Münster ou Paderborn.

Ces suites sont indépendantes d'Erfurt–Eichsfeld : ce dernier demeure volontairement inchangé et ne bloque pas les lots suivants.

## Recherche locale et aperçu

**Zéro appel à ColGrep-Agent-2B dans cette passe.** Les chemins R2, les CSV, outils et sources conservées étaient connus : lecture directe et recherches exactes, conformément à la demande de ne pas répéter les appels de plus de 100 secondes. Aucun rebuild d'index ni modification d'intégration. Pas de mesure instrumentée complète des recherches classiques ou de tokens Codex ; aucune économie exacte de quota affirmée.

`BEFORE_AFTER.png` est un aperçu technique du bitmap effectivement appliqué : PRU bleu, KPF or, KCL violet, WPM vert, WPD saumon. La comparaison ne certifie pas toutes les franges encore inchangées. `SK_OVERLAY.png` montre les enveloppes sur la carte source. Ce ne sont pas des captures de jeu.
