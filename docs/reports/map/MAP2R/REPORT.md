# MAP-2R — Quatre principautés d’Anhalt, noyaux installés

Date de livraison : 17 octobre 2026. Date historique cible : 1er janvier 1776.

**Statut : MAP2R_PARTIAL_INSTALLED_READY_FOR_SCOPED_RUNTIME_TEST. Le chantier territorial complet n’est pas terminé.**
Les noyaux supplémentaires sont installés et prêts pour un contrôle ciblé en nouvelle partie. Aucune validation moteur MAP-2R n’est revendiquée.

## Résultat réellement installé

| Pays | TAG | Cellules de l’ancienne emprise ANH | Population technique |
|---|---|---:|---:|
| Anhalt-Dessau, avec résidus non attribués historiquement | ANH | 167 | 91513 |
| Anhalt-Bernbourg, noyau et fragments intérieurs du Harz | ABG | 23 | 12603 |
| Anhalt-Köthen, noyau et fragment de Warmsdorf | AKT | 33 | 18083 |
| Anhalt-Zerbst, noyau pré-partition | AZR | 56 | 30687 |

112 cellules changent de propriétaire, ANH vers les trois nouveaux pays. 148 cellules changent de RGB, incluant les fragments techniques dont le propriétaire reste ANH. Onze nouveaux RGB sont créés. Les 279 cellules des deux provinces initiales sont toutes comptabilisées, sans extension vers la Prusse ou Brunswick.

La carte de 1753 fournit des enveloppes de juridiction simplifiées, découpées à la résolution du jeu et limitées à l’emprise déjà détenue par ANH. Ce choix permet une correction politique réelle sans faire passer un calage diagnostique pour une mesure topographique certifiée. **Les résidus conservés à Dessau ne sont pas tous des possessions de Dessau démontrées.** Les limites exactes et les extensions manquantes restent ouvertes.

Les trois TAGs ont été autorisés par le joueur. Ils sont membres ordinaires du bloc impérial, sans nouveaux électeurs ni villes libres. Les droits de restauration distinguent désormais les quatre pays. Le registre passe de 510 à 521 RGB, à étendue physique impériale identique. La carte du journal est régénérée ; le masque physique du mode carte n’a pas besoin d’être élargi.

Les souverains de 1776 remplacent les personnages natifs de 1836 : Leopold Friedrich Franz, Friedrich Albrecht, Karl Georg Lebrecht et Friedrich August. Les trois nouveaux pays reprennent les lois et technologies de départ de l’ancien ANH comme abstraction de gameplay, pas comme quatre audits législatifs. Les armes ascaniennes partagées sont une simplification graphique explicite, pas une union politique.

## Données conservées

- Populations mondiales vérifiées : 835 801 255 avant et après. Cette égalité provient de la redistribution technique choisie ici et n’est pas une contrainte pour les travaux futurs.
- Tous les profils culture/religion sont conservés. Les quatre nombres ci-dessus ne sont ni des recensements ni des estimations historiques validées.
- HLB : 9 206 habitants et union OLD–HLB inchangés. Son [acceptation manuelle R3](../MAP2Q/R3/RUNTIME_USER_VALIDATION.json) est conservée séparément.
- Bâtiments écrits, niveaux, PM, propriétaires économiques, infrastructures écrites, armées et recrutements inchangés. Les nouveaux pays n’ont pas reçu artificiellement d’industrie ou d’armée ; vérifier leur fonctionnement économique en jeu.
- Capacités et ressources de la région économique inchangées. Leur répartition effective entre subdivisions, la subsistance et les marchés doivent être contrôlés au chargement.
- Tous les autres pixels, propriétaires et populations sont protégés par comparaison différentielle mondiale. Aucun travail à Erfurt–Eichsfeld, en Frise orientale ou dans un autre lot.
- Aucun commit, changement de branche, modification de HEAD ou de l’index.

## Limites importantes

Jever reste actuellement sous OLD dans les fichiers : c’est une **anomalie connue**, pas la conclusion historique. Sa dépendance envers Zerbst est établie, mais son contour n’est pas suffisamment homologué au bitmap. Voir [JEVER_AUDIT.md](JEVER_AUDIT.md).

Le Harz n’est corrigé que dans des intérieurs recoupant déjà ANH. Hoym n’est pas absorbé arbitrairement par Bernbourg. Les enclaves et franges prussiennes/brunswickoises non tracées ne sont pas certifiées. Zerbst–Coswig–Roßlau reste tronqué par l’ancienne emprise ANH.

Les quatre capitales utilisent la région économique **STATE_ANHALT, ID numérique 62**. Cela ne prouve pas la position historique de leurs centres urbains. Le hub natif Magdebourg reste prussien ; le locator agricole reste physiquement immobile, avec son RGB de référence réassocié au nouveau fragment de Köthen. Aucun nom de ferme n’est utilisé comme preuve de souveraineté.

## Vérifications

692/692 contrôles statiques passent. Onze nouveaux tests passent, dont deux tests négatifs sur la correction du nom ANH. Le compilateur impérial reproduisait les 57 fichiers initiaux à l’identique avant mutation ; les 57 sorties après mutation ont été comparées aux fichiers installés.

Les 44 doublons RGB et 12 références invalides antérieurs sont inchangés. Les anciennes baselines n’ont pas été réécrites. Voir [VALIDATION.json](VALIDATION.json), [UNIT_TESTS.json](UNIT_TESTS.json) et [LEGACY_TEST_TRIAGE.md](LEGACY_TEST_TRIAGE.md).

Les seules cartes avant/après présentent les modifications réellement installées. Elles ne représentent pas un achèvement cadastral d’Anhalt. Voir [comparatif](ANHALT_BEFORE_AFTER.png) et [plan de test](RUNTIME_TEST_PLAN.md).

## Fichiers modifiés

Fichiers runtime recensés exactement dans VALIDATION.json, champ `runtime_files_modified`. Ils comprennent les historiques territoriaux et démographiques, définitions des trois pays, souverains, noms anglais/français, drapeaux abstraits, terrains, bitmap et les 16 sorties impériales modifiées. Aucun fichier de bâtiments, formations militaires ou diplomatie n’est modifié.

Outils : `tools/map2r_anhalt.py`, `tools/test_map2r_anhalt.py` et extension explicitement gardée de `tools/map2l_registry.py`. Le nouveau manifeste courant est [INSTALLED_MANIFEST.json](INSTALLED_MANIFEST.json). Le manifeste Q précédent est conservé comme photographie de son étape, et non présenté comme l’état courant.

## Recherche locale ColGrep

Une tentative a échoué sur le verrou d’index, puis **un appel abouti au sous-agent local configuré** a retrouvé deux pistes vérifiées : les lignes18–19 de `RULERS_1776_EUROPE_RESIDUAL_SOURCES.md` et la ligne5 de `MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md`. Il n’a pas résolu la géométrie. La commande et les limites de mesure sont conservées dans [COLGREP_USAGE.json](COLGREP_USAGE.json).

Les durées cumulées, les tokens Codex et le nombre complet de recherches classiques n’ont pas été instrumentés sur ces reprises. Aucune économie exacte de quota ne peut être déduite. Intérêt constaté : retrouver rapidement des pistes locales pertinentes ; la vérification historique et l’implémentation restent nécessaires.
