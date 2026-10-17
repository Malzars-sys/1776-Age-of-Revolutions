# MAP-2L — Souabe : continuation territoriale après validation du joueur

## Résultat et portée

Deux juridictions supplémentaires intégrées au **1er janvier 1776** : **SFU, principauté de Fürstenberg**, et **SEW, prévôté princière d’Ellwangen**. **92 cellules réattribuées**, **12 RGB nouveaux `xEDAE00`–`xEDAE0B`**, **93 cellules recolorées**. Le registre passe de **464 à 476 RGB**, sans agrandir son empreinte de **62 580 cellules**.

Ce sous-lot n’achève pas toute la Souabe. Les juridictions non reconstruites et les limites incertaines restent ouvertes dans [UNRESOLVED.csv](UNRESOLVED.csv). Aucune nouvelle région lancée automatiquement et aucun changement d’Erfurt–Eichsfeld. **Les ajouts de cette continuation ne sont pas encore validés en jeu.**

## Avant / après

| Domaine représenté | Avant | Après | Cellules |
|---|---|---|---:|
| Haslach–Wolfach, noyau du Kinzigtal | BAD 17 + WUR 1 | SFU | 18 |
| Baar, noyau autour de Donaueschingen | BAD | SFU | 26 |
| Stühlingen–Engen, noyau distinct de Nellenburg | BAD | SFU | 11 |
| Meßkirch, noyau distinct de Sigmaringen | BAD | SFU | 8 |
| Heiligenberg, sans attribution de Salem ou Meersburg | BAD | SFU | 9 |
| Ellwangen, noyau septentrional distinct d’Aalen | BAV 18 + WUR 2 | SEW | 20 |
| Total | | | **92** |

Les six parents explicitement subdivisés sont `xB00160`, `xEDAD00`, `x8F0060`, `xAEBA2A`, `x118060`, `xEDA218`. Leur attribution RGB par RGB, y compris les franges conservées, figure dans [TERRITORIAL_CHANGES.csv](TERRITORIAL_CHANGES.csv). Les cellules entières et les identifiants figurent dans [GEOMETRY.json](GEOMETRY.json).

Les **211 cellules effectivement restaurées de la première passe souabe** et tous leurs RGB de noyau sont identiques. Les **14 identifiants RGB ajoutés lors de cette passe survivent**. Seul `xEDAD00`, identifié alors comme frange BAD non certifiée, est subdivisé : son identifiant est conservé sur 338 cellules, une cellule BAD détachée reçoit un RGB distinct, et 34 cellules passent à SFU. Ce n’est pas un écrasement des noyaux autrichiens, d’Ulm, de Sigmaringen ou des établissements ecclésiastiques validés.

**Dépendance technique à `STATE_FRANCONIA`** : le noyau d’Ellwangen chevauche la limite native des State Regions. Seules 18 cellules de `xEDA218`, une frange BAV conservée dans la première Franconie, changent. Le même RGB subsiste sur 194 cellules. Aucun noyau franconien restauré ni les 185 transferts de la continuation franconienne n’est revisité. La baseline globale initiale contient déjà tous les fichiers sources de cette State Region : aucune nouvelle capture ne remplace ses données immuables.

## Justification et approximations

La feuille Homann de Souabe **vers 1693**, déjà conservée et identifiée dans `../SWABIA/HOMANN_SOURCE.json`, est réutilisée sans téléchargement ni nouvelle optimisation. [TRACING.json](TRACING.json) conserve les enveloppes retenues et leur correspondance avec le bitmap. Elles représentent des **noyaux territoriaux de jeu**, pas un cadastre. Les contours du cercle, la juridiction spirituelle et les marqueurs urbains ne deviennent pas automatiquement des possessions souveraines.

Pour Fürstenberg, la réunion des branches de Heiligenberg et de Meßkirch aboutit à une concentration des possessions en **1744** : [Deutsche Biographie, article Fürstenberg](https://www.deutsche-biographie.de/gnd118694103.html). Les cinq domaines nommés sont donc rattachés à une même principauté, sans reprendre les divisions dynastiques de la feuille plus ancienne comme si elles existaient encore en 1776. Joseph-Wenceslas est le prince régnant depuis 1762, né le 21 mars 1728 : [LEO-BW, notice 116854634](https://www.leo-bw.de/en/detail/-/Detail/details/PERSON/wlbblb_personen/116854634/F%C3%BCrstenberg%20Joseph%20Wenzel%3B%20F%C3%BCrst%20zu).

Ellwangen reste une principauté ecclésiastique avant son rattachement à Württemberg en **1802/03** : [LEO-BW, Ellwangen](https://www.leo-bw.de/en/web/guest/detail-gis/-/Detail/details/ORT/labw_ortslexikon/4362/Ellwangen%2BJagst). Anton Ignaz de Fugger-Glött est représenté comme prince-prévôt nominal, pas comme un successeur de 1787. Son année de naissance 1711 est attestée : [Deutsche Biographie](https://www.deutsche-biographie.de/gnd118665774.html). Le jeu reçoit un **âge de départ approximatif de 64 ans**, sans prétendre avoir vérifié le jour exact. La source municipale sur l’administration du coadjuteur en 1780 ne justifie pas de remplacer le titulaire en 1776 : [archives de la ville](https://www.ellwangen.de/buerger/bildung-betreuung/stadtarchiv/archivalien-des-monats/jahr-2019).

La correspondance affine antérieure est conservée ; le repère indépendant économique de Lindau garde un écart d’environ **9,575 pixels**. Ce n’est ni une erreur certifiée de position du centre urbain ni une précision cadastrale. Les exclusions sont conservatrices : Villingen/Triberg autrichiens, Hornberg, Gengenbach, Nellenburg, Sigmaringen, Salem, Meersburg et Aalen ne sont pas attribués en bloc aux nouveaux pays. Les extérieurs non tracés restent provisoires, et non certifiés.

## Population, économie et institutions

**72 453 habitants redistribués**, sans création : **SFU 57 203**, **SEW 15 250**. Ventilation entière des profils existants sur les subdivisions sources complètes, une seule fois par profil. Il ne s’agit pas d’une restitution des recensements historiques des deux principautés.

- Monde : **835 804 980 habitants**, cultures, religions écrites/effectives et autres attributs conservés.
- Bâtiments : niveaux, PM, attributs pondérés et propriétaires privés conservés. Seul `98_build_start_1776_world_redistribution.txt` est effectivement modifié : un niveau existant d’élevage est réaffecté à SFU. Les allocations entières à zéro ne créent pas d’infrastructures fictives. Les autres fichiers de bâtiments restent identiques.
- Unités, formations militaires et recrutements inchangés ; subdivisions sources préservées pour les propriétés privées et recrutements. Aucune armée ajoutée aux nouveaux pays.
- SFU : capitale de State Region `STATE_BADEN`, monarchie catholique avec titre de prince. SEW : capitale `STATE_FRANCONIA`, théocratie catholique avec titre de prince-prévôt. Ces capitales de State Region ne certifient pas la position d’un centre urbain dans le bitmap.
- Deux variantes de lois de départ à portée dédiée, sans technologie tardive accordée ; aucun changement des gouvernements déjà validés. La succession de SEW réutilise le mécanisme natif `dictatorial` des théocraties : cela ne simule pas une élection canonique par chapitre.
- Deux nouveaux membres du bloc, aucun nouvel électeur ou vote électoral. Drapeaux procéduraux distinctifs, sans certification héraldique. Noms, gouvernements, titres et descriptions FR/EN avec BOM.
- Tous les locators conservent leur position et leur RGB. Les listes `prime_land` héritent des enfants avec la même empreinte physique. La carte du journal et le masque du véritable mode de carte sont régénérés depuis le registre actualisé.

## Contrôles et anomalies

[VALIDATION.json](VALIDATION.json) contient les contrôles exacts de conservation, d’attribution, de connectivité, de références et de compilation des mécanismes impériaux. [NON_REGRESSION.json](NON_REGRESSION.json) rassemble les quinze suites cumulatives. [POPULATION_VALIDATION.csv](POPULATION_VALIDATION.csv) expose les profils et allocations.

Résultats finaux : **488/488** contrôles de la continuation ; **623/623** de la première Souabe avec les migrations ultérieures ; **11 419 contrôles réussis sur 11 429** dans les quinze suites, les **dix échecs bruts** portant seulement sur les anciennes attestations HEAD/index. **Aucune nouvelle régression de données**. Les **13 tests** de registre et **5 tests** de reçus manuels passent. Le résumé conserve les échecs Git historiques, sans les maquiller en PASS brut.

Les **44 doublons RGB** et **12 références invalides hérités** restent séparés des nouvelles régressions. Les anciens échecs d’attestation Git des baselines précédant le commit utilisateur `f34a6b8` ne sont pas effacés : ils restent dans les résultats bruts, avec leur différence Git explicitement autorisée. Aucune exemption à un défaut de données ou de frontières.

Le mode de carte conserve **16 contrôles hors moteur**, dont la compilation isolée du helper HLSL. Cela ne constitue pas un chargement automatisé de Victoria 3. Le test manuel reçu pour les deux lots précédents reste valide dans sa portée et ne couvre pas automatiquement cette continuation.

Un défaut de paramètre de succession de la nouvelle prévôté a été détecté en comparant les définitions natives, puis corrigé avant livraison : `theocratic` n’est pas un type de succession natif, `dictatorial` est réutilisé avec ses effets existants. Les nouvelles espaces de fin de ligne sont retirées par patch explicite ; les deux lignes héritées restent distinguées.

## Validation manuelle, captures et checkpoint

Le témoignage d’une **nouvelle partie suivie d’un mois sans problème**, reçu pour `RHINE_WESTPHALIA_COMPLETION` et `SWABIA`, est enregistré dans `../RUNTIME_USER_VALIDATION_RHINE_SWABIA.json` comme **PASS_RUNTIME_USER_VALIDATED pour les modifications inspectées**. Pas de test moteur automatisé ni de certification historique. Les captures ont signalé les descriptions manquantes de Baden et Ulm ; leurs descriptions FR/EN et celles des principautés Hohenzollern sont corrigées. Ces affichages corrigés restent à revoir en jeu.

Le checkpoint de cette **version précédant la continuation** est publié et vérifié sur `backup/1776-checkpoints`, commit **`0a66418cc3302704f14844d70608d9755d768dc1`**. Voir `../CHECKPOINT_RHINE_SWABIA_USER_VALIDATED.json`. Tous les 6 726 blobs ont été vérifiés par SHA-256 depuis un téléchargement GitHub indépendant ; 213 fichiers de delta/suivi ont été réellement restaurés. Aucune nouvelle archive complète, aucun changement du HEAD/index principal, aucun push sur main. Le nouveau manifeste `_checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json` est la référence de ce checkpoint, les anciens fichiers `docs/backups` demeurant historiques. **Cette continuation territoriale n’est pas publiée.**

Finition de la même version sauvegardée : **`cadb544c7de706707532e26bdf19998cf7601cec`**, également vérifiée depuis GitHub, ne change que **quatre fichiers de métadonnées/vérification**. Le manifeste `docs/backups/CURRENT_CHECKPOINT_MANIFEST.json` est désormais synchronisé avec celui de `_checkpoint`, la politique précise la portée actuelle, et l’outil exige une restauration portant sur le commit exact. Les quatre blobs sont réellement restaurés et vérifiés par SHA-256 ; tous les autres identifiants de blobs et modes restent identiques au parent complètement vérifié. Voir `../CHECKPOINT_RHINE_SWABIA_METADATA_FINALIZED.json`. **Aucun gameplay de la nouvelle continuation n’est inclus dans cette finition.**

## Prochain contrôle en jeu — ajouts seulement

En nouvelle partie, vérifier SFU et ses domaines séparés, SEW et sa capitale partagée, les titres de prince/prince-prévôt et les deux dirigeants, lois actives, budgets/infrastructures de ces petits pays, accès militaire aux enclaves, leur présence dans le bloc et le journal, la carte de jure et les nouvelles descriptions de Baden/Ulm/Hohenzollern. Puis laisser passer un mois et vérifier l’ouverture du journal sans crash. Le jeu n’a pas été lancé ni la partie du joueur manipulée par l’assistant.

## Secteurs encore ouverts et clôture

**Montbéliard n’est pas appliqué** : son comté est impérial, mais les possessions wurtembergeoises sous souveraineté française ne doivent pas être confondues avec lui après 1748 : [Archives diplomatiques, dossier LIMITES](https://archivesdiplomatiques.diplomatie.gouv.fr/ark%3A/14366/ghrpcz4xsdb7). Il manque une enveloppe du comté raccordée au bitmap ; transférer une province française entière ne serait pas défendable.

**Augsbourg et Kempten libres ne sont pas appliqués** : leur souveraineté est établie, pas leur périmètre jouable. Augsbourg n’avait pas un vaste hinterland à attribuer depuis la province bavaroise ; Kempten doit être distinguée de l’abbaye voisine. Voir [Augsbourg, territoire](https://www.historisches-lexikon-bayerns.de/Lexikon/Augsburg%2C_Reichsstadt%3A_Territorium_und_Verwaltung) et [Kempten, ville impériale](https://www.historisches-lexikon-bayerns.de/Lexikon/Artikel_45421). Les marqueurs urbains ne suffisent pas à faire une frontière politique.

Weingarten/Salem, les branches Waldburg et les franges ecclésiastiques restent explicitement ouverts. Aucun pays Waldburg unifié fictif, aucun agrandissement des abbayes ou des villes pour obtenir un nombre arbitraire de cellules. **MAP-2L n’est donc pas clôturé historiquement**, même si cette continuation réalise des corrections réelles et testables. Les prochains périmètres précis nécessaires figurent dans `UNRESOLVED.csv` ; aucune nouvelle campagne historique générale n’est lancée.

## Recherche locale

Un appel ColGrep-Agent-2B, réussi, a retrouvé les rapports et outils installés ; les chemins et lignes ont été vérifiés. Il n’a pas fourni de nouvelle frontière exploitable, et ses principaux chemins étaient déjà connus : bénéfice marginal limité dans ce sous-lot. [COLGREP_METRICS.json](COLGREP_METRICS.json) conserve la question et ces limites. Les compteurs de tokens/quota Codex et un chronométrage total fiable ne sont pas disponibles ; aucune économie exacte n’est annoncée.
