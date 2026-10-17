# Chine — vingt niveaux de plantations de thé uniquement

**PASS_STATIC_PENDING_RUNTIME** — 15 octobre 2026. Nouvelle partie requise ; aucun test moteur effectué.

La dernière consigne du joueur remplace les demandes simultanées sur l'armement, le Rhône et le centre de commerce : ces éléments ne sont pas modifiés, et aucune technologie n'est accordée.

| État chinois | Niveaux de thé ajoutés | Marge d'infrastructure nominale après ajout |
|---|---:|---:|
| Hunan | 5 | +14 |
| Sichuan | 5 | +16,5 |
| Nankin (`STATE_NANJING`) | 5 | +86,5 |
| Suzhou | 5 | +52,5 |
| **Total ajouté** | **20** | |

Chaque État possède la ressource agricole autorisant le thé, suffisamment de terres arables et une infrastructure nominale existante supérieure aux besoins de tous ses bâtiments écrits, nouveaux niveaux compris. La dépense d'infrastructure du thé est d'un point par niveau. Aucun réseau, port ou canal n'est construit ou modifié. Les technologies, lois et traits régionaux pertinents ont aussi été examinés : aucun multiplicateur d'infrastructure négatif supplémentaire n'a été trouvé pour ces quatre États dans cette lecture.

Les capacités sont calculées avec les bâtiments et méthodes de production de départ, à plein recrutement nominal. Ce n'est pas une simulation du recrutement réel, des prix, des pénuries ou de la rentabilité : vérifier l'accès au marché et les embauches en jeu.

Nouveau fichier fonctionnel unique : `common/history/buildings/99_1776_china_tea_addon.txt`. Quatre déclarations distinctes de cinq niveaux, détenus par des domaines locaux chinois. Méthodes débloquées : `default_building_tea_plantation`, `default_labour`, `pm_road_carts`. Aucun thé existant n'est supprimé ou remplacé.

Validation reproductible : `tools/china_tea_2026_10_15.py validate` — **48/48 contrôles réussis**. Comparaison de l'inventaire mondial : exactement les vingt niveaux demandés en plus, tous les autres bâtiments inchangés. Empreintes de tous les fichiers fonctionnels antérieurs inchangées, y compris frontières MAP-2M-R2, infrastructures britanniques, cantons chinois, manufactures d'armes et pays. Populations, cultures, religions, unités et propriétaires territoriaux préservés ; monde : **835 804 980** habitants. HEAD et index Git inchangés ; aucun commit ni push.

Référence avant modification conservée dans `BASELINE.json`. Calculs avant/après : `INFRASTRUCTURE_BEFORE.json` et `INFRASTRUCTURE_AFTER.json`. Résultats : `VALIDATION.json`. Ces fichiers n'écrasent aucune attestation antérieure.
