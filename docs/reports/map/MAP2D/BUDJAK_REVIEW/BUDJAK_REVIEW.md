# Budjak : contrôle ciblé après le test MAP-2D

## Résultat

La capture du joueur correspond à **deux ensembles territoriaux CRI détachés de la Crimée**, plus **un artefact d'un pixel** dans le secteur nord. Il ne s'agit pas de plusieurs morceaux de `x5F2259`.

| Ensemble avant contrôle | Géométrie | Origine | Décision |
| --- | --- | --- | --- |
| Yedisan, à l'est du Dniestr | 14 RGB, cœur continu de 2 812 pixels | Déjà CRI avant MAP-2D ; les transferts russes et ottomans ont accentué son isolement | Maintien comme approximation documentée |
| Budjak intérieur, `x5F2259` | 347 pixels, une seule composante, même en connectivité stricte à quatre voisins | MOL → CRI dans MAP-2D ; contours inchangés | CRI → TUR |
| Fragment septentrional de `xDCE378` | 1 pixel à `(4768,891)`, sans contact même diagonal avec le cœur de son RGB | Déjà CRI dans la baseline antérieure à MAP-2D | Rejoint `xFF7D57`, province PLC voisine |

Après correction : **un ensemble territorial CRI subsiste dans ce périmètre, le Yedisan**. Il compte toujours 14 identifiants de province et 2 812 pixels continus. Le petit secteur rond dans le Budjak devient ottoman ; le point isolé au nord disparaît. Le reste du khanat, notamment la péninsule et les territoires hors périmètre, n'est pas annexé.

« Enclave » est employé ici au sens visuel du jeu : il s'agit d'exclaves du khanat bordées par plusieurs pays, pas nécessairement d'enclaves entourées par un seul pays. Les pixels sont des unités du bitmap, **pas des km² ni des habitants**.

## Fondement historique et limites

Les recommandations R2-0008 distinguaient déjà Moldavie, rayas ottomanes et groupes du Budjak, sans prouver une souveraineté du khanat pour chaque RGB. R3 insistait sur la séparation entre autonomie tatare et administration territoriale. Le contrôle réutilise ces dossiers et la baseline MAP-2D.

**S1 — traité de Küçük Kaynarca, 1774.** L'article 3 reconnaît les communautés tatares sous leur khan et prévoit explicitement les terres entre Bug et Dniestr jusqu'à la frontière polonaise, sauf Ochakiv. L'article 16 restitue la Bessarabie méridionale et Bender à la Porte, en distinguant les principautés. Les articles 18 et 19 concernent Kinburn et Kerch/Yeni-Kale. Ces dispositions soutiennent le maintien du Yedisan, mais pas l'inférence précédente « population tatare = territoire CRI » pour `x5F2259`. [Texte du traité, articles 3, 16, 18–19](https://www.vostlit.info/Texts/Dokumenty/Turk/XVIII/1760-1780/Traktat_Kucuk_Karnaji_1774/text.phtml).

**S2 — Olena Bachynska, pp. 62–63.** Son étude documente l'organisation ottomane de cette frontière, les districts des forteresses et une association territoriale nogaïe du Budjak. Elle traite une période plus large que janvier 1776 : elle ne constitue pas un relevé cadastral daté de chaque pâturage. Elle renforce néanmoins la distinction entre autonomie des communautés et propriété territoriale exclusive du khanat. [Article original, DOI 10.26650/gaad.794259](https://doi.org/10.26650/gaad.794259).

**Décision C pour `x5F2259` :** attribution à TUR, par inférence documentée à l'échelle du jeu. Cette représentation privilégie l'administration territoriale du Budjak, sans nier l'autonomie nogaïe, les droits pastoraux ni les liens nominaux avec le khan. Le moteur ne représente pas ces juridictions superposées. La correction ne revendique donc pas une preuve village par village et ne modifie pas les lois ou la composition des populations.

**Décision A pour le Yedisan :** maintien, fondé sur la disposition territoriale explicite du traité, et non sur la seule présence de Tatars. Les limites de chaque RGB restent des approximations ; le contrôle effectif et les influences ottomane/russe ne se réduisent pas à une couleur uniforme. Aucun couloir artificiel n'est creusé à travers Bender pour relier le Budjak au Yedisan.

Il ne s'agit pas d'attribuer automatiquement tout le Budjak à TUR : seul le RGB nouvellement attribué à CRI est corrigé. Les districts ottomans existants et le reste moldave sont conservés. Hotin n'est pas rouvert. La Moldavie reste une principauté tributaire distincte.

## Géométrie, voisins et locators

Le bitmap avant contrôle était identique, octet par octet, à celui d'avant MAP-2D. L'isolement territorial créé dans le Budjak venait donc du **propriétaire**, pas d'une retouche des contours.

`x5F2259` touche les RGB ottomans `x1E1DEF`, `x23621B`, `xB0E0A0` et les RGB moldaves `x8955DF`, `xFDE796`. Aucun hub enregistré de type ville, port, ferme, bois ou mine ne se trouve dans ce RGB. Cela ne prouve pas l'absence historique d'habitat. Les forteresses citées dans les sources ne sont pas assimilées à des centres géométriques de province.

Le Yedisan constitue une seule composante terrestre, voisinant MOL, PLC, TUR et RUS. Ses 14 RGB sont détaillés dans le CSV. `xDCE378` avait deux morceaux : 382 pixels continus et le pixel parasite. Ce dernier est entouré de `x98E808` et `xFF7D57`, tous deux PLC. Il rejoint le voisin sud `xFF7D57`, dans `STATE_KIEV`. Aucun RGB n'est créé ou supprimé.

`x716121`, sur la côte ottomane de Hadjibey, a un contact diagonal : deux composantes à quatre voisins mais une seule à huit voisins. Son pixel côtier est adjacent à d'autres terres TUR ; ce n'est pas une enclave CRI. La côte est préservée. Les fragments tauridiens visibles à l'est de la fenêtre de calcul ne sont pas comptés comme des enclaves du Budjak et ne sont pas modifiés.

Les hubs de Chişinău, Akkerman, Ishmael, Balti et Beltsy et ceux de Cherson sont préservés. Aucun locator n'est déplacé. Les noms de hubs hérités, dont certains anachroniques, ne sont pas corrigés dans cette tâche.

## Conservation démographique et économique

| Bessarabie, subdivision | Avant contrôle | Après contrôle |
| --- | ---: | ---: |
| MOL | 326 587 | 326 587 |
| TUR | 107 570 | 157 139 |
| CRI | 49 569 | 0 |
| Total régional | 483 726 | 483 726 |

Les huit groupes anciennement dans la subdivision CRI rejoignent le sélecteur TUR **sans changer aucun attribut ni leur taille**. Aucune assimilation, conversion, migration ou redistribution proportionnelle supplémentaire. La population mondiale reste **835 804 980**. Les groupes autochtones, religieux et statuts sociaux restent identiques.

La ferme de blé de niveau 1 suit le transfert territorial. Son manoir économique moldave, ses PM et ses réserves sont conservés. Le ranch ottoman existant et tous les autres bâtiments restent inchangés. La subdivision CRI désormais sans province est retirée des historiques ; aucune référence de population, bâtiment ou recrutement ne reste orpheline du fait de cette suppression. Les unités, formations, lieux de recrutement et généraux ne changent pas.

Le pixel parasite n'a pas de population indépendante dans le moteur : les populations sont définies par subdivision d'État. Les pools Cherson/CRI et Kiev/PLC restent donc intacts. La différence de surface d'un pixel est une correction géométrique, pas une migration. Aucun accès au marché ou recrutement après transfert n'est garanti sans test natif.

## Fichiers de jeu modifiés

- `common/history/states/00_states.txt` : `x5F2259` passe de CRI à TUR ; suppression de la subdivision CRI vide.
- `common/history/pops/15_russia.txt` : déplacement des huit groupes de cette subdivision vers TUR.
- `common/history/buildings/98_build_start_1776_world_redistribution.txt` : ferme de blé transférée vers TUR, propriétaire économique inchangé.
- `map_data/provinces.png` : **un seul pixel** `(4768,891)`, `xDCE378` → `xFF7D57`.

La sauvegarde différentielle contient seulement les trois fichiers texte touchés, soit **1 029 500 octets**. Le bitmap original est réutilisé depuis `../provinces_before.png`, contrôlé par empreinte ; aucune seconde copie intégrale du mod ou archive ZIP n'a été créée. `DIFFERENTIAL_BACKUP/MANIFEST.json` permet de retrouver les quatre originaux.

## Validation et observation en jeu

`BUDJAK_VALIDATION.json` : contrôles statiques réussis. Exactement les quatre fichiers ci-dessus ont changé. Un transfert de propriétaire et un pixel modifié, univers RGB identique, aucune nouvelle discontinuité, aucun nouveau doublon ou défaut de référence. Les 62 doubles attributions et 13 défauts de référence hérités restent inchangés et ne sont pas dissimulés.

Les populations et attributs, niveaux de bâtiments, PM, réserves, détenteurs économiques et effectifs sont conservés. Les historiques hors Bessarabie sont identiques structurellement. Les autres fichiers de jeu sont identiques octet par octet, notamment MAP-2A/B/C, Avignon/Frioul, Kerch/Kinburn, technologies, correctifs IA et diplomatie. Les modèles existants ont été réexécutés : 1 024 combinaisons administratives ottomanes, 192 chemins politiques et 10 scénarios d'infrastructures réussis. Ce sont des tests de scripts, pas une exécution du moteur.

Le test natif **MAP-2D avant ce complément** est positif selon le joueur : chargement, frontières, PLC et CRI maintenus dans le bloc russe pendant la période observée. Le statut de protectorat de CRI n'est pas établi par cette observation et n'est pas qualifié d'échec. **Aucun bonus ni mécanisme diplomatique n'a été modifié.**

Le complément doit encore être vérifié dans une **nouvelle partie** : regarder le secteur intérieur au sud de Bender devenu ottoman, le petit point au nord du Yedisan disparu, puis les populations TUR/MOL et la ferme de blé. `before.png` et `after.png` sont des vues calculées du bitmap, pas des captures natives. Le CSV distingue les provinces des lignes de détail non additives.

`before_after.png` juxtapose les deux vues politiques. `isolated_pixel_before_after.png` agrandit le seul pixel corrigé, encadré en rouge. La colonne des voisins du CSV exclut la mer ; ses surfaces et composantes sont calculées sur l'intégralité des RGB, pas uniquement sur la fenêtre d'aperçu.

**Aucun commit, merge ou push. Aucune autre région commencée.**
