# Mission 31 — cuivre natif, gisements du mod

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, installé localement le 8 novembre 2026. Aucune exécution du moteur après installation n’est attestée.

Le mainteneur a demandé de prendre une autre mission, puis précisé : « suit la vanilla sur les prix de base du cuivre et à peu près tout, sauf la répartition des ressources en cuivre. Que ça, je veux qu’on la garde de notre mod. » Cette instruction remplace l’ancienne hypothèse de conservation du prix 50 et des rendements propres au mod.

La mission 31 était ouverte, sans assignataire et sans livraison locale identifiée ; la 30 et la 32 avaient déjà reçu leurs correctifs par l’autre agent. La prise en charge a été consignée dans l’issue 31. L’interface du Project s’ouvre désormais déconnectée, avec une page 404 : **le statut du tableau n’a pas pu être changé pendant cette mission**. Ce blocage n’a pas empêché la livraison locale ni la mise à jour de l’issue par le connecteur.

## Résultat livré

Le bien `copper` et les quatre groupes miniers standards sont maintenant hérités du vanilla canonique, sans seconde définition locale. Le fichier local du bien ne contient plus que des commentaires ; celui des groupes conserve seulement les extensions de concentration et de doublage. Les fichiers natifs `00_goods.txt` et `03_mines.txt` des groupes ne sont pas masqués par un fichier homonyme du mod.

| Paramètre | Avant | Après / vanilla 1.15.0 |
| --- | ---: | ---: |
| Prix de base du cuivre | 50 £ | **40 £** |
| Facteur de prestige | 5 | **3** |
| Quantité échangée | 5 | **5** |
| Pics et pelles : cuivre produit | 15 | **20** |
| Pompe atmosphérique : cuivre produit | 30 | **40** |
| Pompe à condensation : cuivre produit | 45 | **60** |
| Pompe diesel : cuivre produit | 55 | **70** |
| Nitroglycérine : cuivre supplémentaire | 8 | **12** |
| Dynamite : cuivre supplémentaire | 15 | **20** |

Les quantités de PM sont des unités scriptées par semaine et par niveau, à effectif plein, avant débit et autres modificateurs. Les explosifs ajoutent leur production au groupe d’équipement ; ces chiffres ne sont pas des productions nationales observées ni une garantie de rentabilité.

Les six PM miniers reprennent l’intégralité de leur définition native, avec une exception de progression déjà présente : `watertube_boiler` reste mappé sur `condensing_steam_engines` pour la pompe à condensation. La première technologie est dans l’ère 7 de compatibilité du mod ; la seconde est le nœud d’ère 4 utilisé par le système 1776. Aucun prérequis de pays ni PM initial n’a été changé pour déplacer ce déblocage.

Le diesel consomme désormais **5 pétrole**, comme le vanilla, au lieu de 3 combustibles raffinés. Les autres intrants, emplois, pollution et effets de mortalité des six PM correspondent au natif. Le biais local `ai_value = 1000` de la mine est retiré pour retrouver le comportement natif.

## Gisements et ajouts préservés

- Matrice du mod : **675 États**, **302 potentiels non nuls**, **373 sans cuivre**, **5 924 niveaux potentiels**, répartis dans **16 fichiers d’États**. Le potentiel n’est pas un nombre de mines construites ni une production hebdomadaire.
- Aucun fichier de carte, capacité minérale, propriétaire, population ou bâtiment initial n’a été modifié.
- Les groupes supplémentaires du mod restent attachés à la mine : concentration des minerais, ventilation et collecte de données. Leurs propres recettes et effets n’ont pas été modifiés. Une mine utilisant ces extensions peut donc différer du total d’une mine strictement vanilla.
- Les PM de doublage en cuivre et leurs technologies, les variantes d’artillerie fer/cuivre/alliage demandées précédemment et les autres consommateurs spécifiques au mod sont préservés.
- Les **28 PM consommateurs natifs** ont leurs coefficients d’entrée en cuivre vérifiés contre le vanilla actuel. Les autres recettes, dont celles de l’artillerie en alliage, ne sont pas réinitialisées.
- Les deux types de modificateurs multiplicatifs du cuivre, sans définition textuelle native identifiée et utilisés par les extensions du mod, sont conservés.

## Nettoyage des collisions et des textes

Les trois enregistrements locaux déjà présents dans les types de modificateurs natifs sont retirés : entrées additives, sorties additives et débit des mines de cuivre. Les autres biens et tous leurs enregistrements restent inchangés.

L’icône textuelle locale `@copper!` pointait encore sur `gfx/error_deer.dds`. Ce bloc est retiré ; l’icône native dans `gui/goods_texticons.gui` fournit désormais la texture cuivre, sans modifier ni générer de DDS.

Les logs antérieurs signalaient des clés anglaises en double. **32 lignes de localisation** sont retirées, soit 16 par langue : les 14 clés standard du bien, du bâtiment, du débit, des quatre groupes et des six PM, puis les deux libellés de modificateurs additifs. Elles sont toutes présentes dans les fichiers natifs FR/EN. Les six textes propres à la concentration et au doublage restent dans les fichiers du mod ; le BOM et les autres lignes sont préservés.

## Références et résolution

Référence canonique en lecture seule : `C:/Games/Victoria 3/game`, exécutable **1.15.0**. Les fichiers consultés et leurs empreintes sont enregistrés dans `BASELINE.json`, avec copies dans `native/`.

| Objet | Fournisseur après correction |
| --- | --- |
| Bien cuivre | `game/common/goods/00_goods.txt` |
| Quatre groupes standards | `game/common/production_method_groups/03_mines.txt` |
| Six PM standards | Fichier local cuivre, payload natif avec le seul mappage de technologie documenté |
| Mine | Fichier local cuivre, champs standards natifs et trois groupes propres au mod |
| Trois modificateurs additifs / débit | `game/common/modifier_type_definitions/01_building_modifier_types.txt` |
| Icône textuelle du cuivre | `game/gui/goods_texticons.gui` |

Le fichier vanilla de bâtiments et celui des PM de mines sont masqués par les fichiers homonymes du mod. Il fallait donc conserver les définitions locales de la mine et des six PM : leur cas diffère de celui du bien et des groupes. La résolution est vérifiée par identité d’objet et masquage de fichier ; elle reste une vérification statique, pas une observation du registre moteur.

## Vérifications exécutées

```text
python -B tools/compatibility/issue31_copper_alignment_audit.py --candidate --negative-controls
python -B tools/compatibility/issue31_copper_alignment_audit.py --negative-controls
python -B tools/tech6c5b_validate.py
```

- **155/155 contrôles statiques** sur le candidat final et les fichiers installés.
- **6 contrôles négatifs détectés** : doublon et ancien prix du bien, doublons des groupes, ancien rendement, mauvais carburant diesel, icône placeholder réintroduite et localisation native réintroduite en double.
- Les listes des quatre groupes hérités aboutissent à des PM définis sans ambiguïté ; les 28 consommations natives sont contrôlées.
- **2 474 autres fichiers de scripts/données** gardent leur empreinte de début de mission. Aucun changement concurrent observé pendant cette vérification, notamment dans les fichiers des missions 29, 30 et 32.
- Le validateur cuivre existant passe : carte 675/302/373/5 924, graphe de **290 technologies**, aucun cycle détecté ni nouvelle technologie cuivre.

Le validateur historique était déjà en échec avant intervention : il exigeait encore l’icône placeholder et une entrée téléphonique de 15 au lieu des 30 natives installées auparavant. Sa sortie est conservée dans `LEGACY_VALIDATOR_BEFORE.txt`. Ses contrôles sont actualisés : définitions effectives avec héritage, prix 40, prestige 3, texture native, enregistrements et icône textuelle hérités, entrée diesel native et entrée téléphonique 30. Les contrôles de carte, graphe, références, recettes propres au mod et localisation restent actifs. `LEGACY_VALIDATOR_CANDIDATE.txt` et `COPPER_VALIDATOR_AFTER.txt` contiennent les sorties réelles.

Les snapshots de départ et le contrôle d’empreinte immédiatement avant écriture ont empêché de remplacer des changements concurrents par une ancienne version. `CHANGES.patch` décrit dix fichiers de jeu et un validateur existant ; le nouveau validateur de portée est livré séparément. Aucun staging, commit, push, changement de branche, merge ou fichier vanilla modifié.

## Validation moteur restante

Nouvelle partie en 1776 avec cette installation : vérifier le prix de référence 40, les listes de PM et leurs valeurs par niveau, les capacités de quelques États du mod, le rendu de `@copper!`, les échanges et les logs après rechargement. Les PM avancés peuvent être inspectés dans leurs infobulles sans inventer leur disponibilité initiale. Le protocole détaillé est dans `RUNTIME_PROTOCOL.md`.

L’absence des anciens doublons et la bonne définition réellement chargée doivent encore être constatées dans le moteur. Les anciennes erreurs des logs ne sont pas annoncées comme disparues. La mission reste ouverte pour revue et validation humaine, sans statut Done.
