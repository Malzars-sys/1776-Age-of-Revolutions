# Luxembourg — sources de la correction administrative

Consultation : 26 octobre 2026. Périmètre : administration du Luxembourg intégré à BEO au départ de 1776 ; aucune nouvelle attribution territoriale.

## Sources historiques consultées

1. [Archives nationales de Luxembourg, Fonds anciens](https://anlux.public.lu/fr/rechercher/fonds-collections/fonds-anciens.html), page mise à jour le 26 août 2016, section « Fonds anciens », liste des institutions des fonds de 762–1795. L’institution archivistique signale le Conseil provincial comme autorité administrative et judiciaire du duché et les Trois États du Luxembourg. Ce constat justifie une représentation administrative provinciale propre ; il ne fournit ni effectif d’employés en 1776, ni nombre de niveaux Victoria 3. Le titre composé du fonds ne sert pas à antidater un changement de compétence judiciaire.
2. [Ville de Luxembourg, UNESCO](https://www.vdl.lu/fr/visiter/art-et-culture/architecture-et-patrimoine/unesco), sections « Valeur universelle exceptionnelle » et « Identifier le paysage urbain historique ». La ville décrit le caractère de place forte et la présence de l’administration dans la ville haute. Contexte institutionnel et urbain, pas preuve d’un volume exact d’administration.

**Interprétation retenue** : un seul niveau ordinaire, catégorie B, rend une capacité provinciale minimale au ressort BEO de Wallonie qui contient le Luxembourg. Ce niveau ne représente pas seulement les 137 881 habitants transférés ni une commune séparée. Le choix du niveau est une abstraction de gameplay explicite ; aucune source n’est présentée comme certifiant 1 500 emplois historiques.

## Sources documentaires existantes réutilisées

- `docs/reports/map/LUX_BEO_INTEGRATION_2026-10-10/REPORT.md` et `BASELINE.json` : transfert des quatre groupes, du RGB et de la formation ; deux déclarations administratives antérieures, cumul moteur non démontré.
- `docs/reports/map/SERG_CLOSURE/CLOSURE_CAMPAIGN_2026_10_26/INSTALLED_VALIDATION_AUDIT.json` : 133/135, deux écarts conservés dans leur résultat brut.
- `LUXEMBOURG_SCOPE_RECONCILIATION.json`, `BLOCKED_MATRIX.md`, `FINAL_CHECKS.json` de cette campagne : discordance BEO/Wallonie = 0 contre LUX/Wallonie = 1 et absence de reçu complet.
- `docs/reports/buildings/BUILD_START_1776_FINAL_IMPLEMENTATION_REPORT.md`, §1 : la matrice runtime est le contrat actif. Les états et PM ont évolué depuis les anciens catalogues ; leurs diagnostics ne remplacent pas les scripts actuels.

## Contrat technique effectivement lu

- `common/history/states/00_states.txt` : Wallonie partagée entre BEO, LGE et STM ; xD001A0 appartient à BEO. Flandre distincte, partagée BEO/LGE. Aucun LUX initial.
- `common/history/buildings/00_west_europe.txt` et `98_build_start_1776_world_redistribution.txt` : blocs régionaux BEO et LGE distincts ; aucune administration BEO wallonne avant correction. Les déclarations répétées des autres bâtiments sont conservées, sans prétendre démontrer leur cumul moteur.
- `common/production_methods/07_government.txt` : `pm_simple_organization` déclare +10 bureaucratie nationale et +2 capacité fiscale de l’État, à effectif plein avant autres modificateurs. Les bâtiments flamands ne portent pas cette capacité locale sur la portion BEO de Wallonie ; ceux de LGE relèvent d’un autre propriétaire.
- `common/history/countries/beo - belgium old.txt` et définitions des PM : loi demandée `law_crownland_diets`, compatible avec `pm_hereditary_bureaucrats`. Les PM professionnels existants ailleurs sont conservés ; ils ne sont pas copiés dans le nouveau niveau.
- Groupe de rapport administratif et `pm_1776_no_organized_data_reporting` : quatrième groupe explicitement désactivé, sans ajout de technologie.

Les empreintes des préimages réelles, y compris du contrat BUILD actif, sont conservées dans le nouveau `BASELINE.json`. Aucune ancienne baseline n’est remplacée.
