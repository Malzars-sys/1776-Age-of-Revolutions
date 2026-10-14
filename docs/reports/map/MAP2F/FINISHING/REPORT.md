# MAP-2F — Finitions des noms et couleurs

## Changements

| Élément | Avant | Après |
| --- | --- | --- |
| Pays CAR | Carnatique / Carnatic | **Arcot**, en français et anglais |
| Portion britannique de STATE_MADRAS | Nom régional suivi de l'adjectif du propriétaire | **Madras** |
| Portion française de STATE_MADRAS | Nom régional suivi de l'adjectif du propriétaire | **Pondichéry** / **Pondicherry** |
| Région géographique, en français | Carnatic, localisation héritée du jeu | **Carnatique** |
| Couleur de Kandy | RGB 181, 84, 51, brun-orangé | **RGB 45, 128, 153, bleu-vert** |

Arcot désigne le pouvoir de Muhammad Ali Wallajah représenté par CAR, plutôt qu'une région générique. Ses adjectifs et les articles français sont adaptés pour éviter « le Arcot » ou « du Arcot ». Le nom géographique Carnatique est conservé pour la région, indépendamment du nom politique.

Aucune occurrence littérale de « Carnartic » n'a été trouvée dans les textes actifs. Les nouvelles localisations utilisent les graphies correctes.

Les noms des enclaves s'appliquent seulement à STATE_MADRAS divisée et aux propriétaires BIC/GBR ou FRA. Les autres portions, notamment PUD, MYS, CAR et DENNOR, conservent leur système de noms. Les actions additives suivent le modèle déjà utilisé et testé pour les noms d'Avignon et de Venise, sans modifier ces derniers.

La Compagnie reste RGB 188, 113, 61. Kandy reçoit une teinte froide nettement différente. Son statut, ses lois et ses relations diplomatiques restent inchangés : aucune dépendance n'est créée.

## Forme et préservation

**Aucune retouche de forme ni réattribution de province.** Le compromis territorial MAP-2F validé est conservé. Le bitmap, les locators, populations, cultures, religions, bâtiments, PM, unités, marchés et les autres corrections sont identiques à l'état avant cette passe.

## Vérification

**67 contrôles statiques réussis**, dont les 32 contrôles de conservation MAP-2F, avec uniquement la nouvelle couleur attendue de Kandy. Contrôle des graphies, des clés françaises/anglaises, de l'encodage, des propriétaires visés, des actions de nommage et des empreintes des autres fichiers. Les anciens rapports restent inchangés. Résultats : [VALIDATION.json](VALIDATION.json).

MAP-2F a été validé globalement en jeu par le joueur. Les finitions de cette passe restent à observer après relancement dans une nouvelle partie. Aucun pilotage du jeu ni lecture des logs n'a été effectué ici ; les logs seront examinés si le joueur signale un problème.

## Fichiers

- Modifié : `common/country_definitions/04_1776_kandy.txt`, couleur uniquement.
- Ajoutés : `common/scripted_effects/1776_map2f_state_names.txt` et `common/on_actions/14_1776_map2f_state_names.txt`.
- Ajoutées : `localization/english/replace/1776_map2f_finishing_l_english.yml` et `localization/french/replace/1776_map2f_finishing_l_french.yml`.
- Vérificateur ciblé : `tools/validate_map2f_finishing.py` ; baseline légère par empreintes, sans nouvelle copie complète du mod.

**Aucun commit, merge ou push.** HEAD, références et index du dépôt principal inchangés. Les tests en jeu restent au joueur.
