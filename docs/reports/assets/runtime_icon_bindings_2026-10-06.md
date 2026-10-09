# Raccordements d'icônes et approvisionnement allemand en tissu

## Icônes

Sept glyphes de biens utilisaient encore `gfx/error_deer.dds`, indépendamment
des grandes illustrations : calcaire, ciment, combustibles raffinés,
lubrifiants, produits pétroliers lourds, phosphates et machines de précision.
Ils utilisent maintenant exactement la texture de leur définition de bien.

Les 71 PM hors cuivre encore reliés au cerf d'erreur utilisent désormais des
symboles vanilla appropriés ou des icônes de PM déjà approuvées. Cela couvre
notamment l'absence de rail, les canaux, le traitement du minerai, les machines
de précision, la chimie, les équipements électriques et les services médicaux.
Les PM d'une même famille peuvent partager un symbole ; aucune nouvelle
illustration de bâtiment ou de technologie n'est utilisée à la place d'un PM.
Les chemins de certains symboles livrés avec le jeu incluent `unused/` : ces
textures existent réellement et ne sont pas recopiées dans le dépôt.

Le cuivre conserve son exclusion. Les sept icônes et les définitions du
laboratoire restent identiques. Les recettes, nombres, prérequis, couleurs et
dimensions d'interface ne changent pas. Le manifeste JSON voisin contient les
78 liaisons avant/après et leurs empreintes de contrôle non visuel.

## Élevages supplémentaires

Le déficit de la capture est de 540 unités de tissu. La demande confirmée porte
sur **108 niveaux supplémentaires**, à cinq tissus par niveau de simple élevage.
Ils sont ajoutés dans les régions existantes du fichier de redistribution de
départ, sans créer de nouveaux blocs d'État ni modifier les potentiels agricoles.

| Pays | Niveaux ajoutés |
| --- | ---: |
| Prusse | 40 |
| Bavière | 20 |
| Wurtemberg | 12 |
| Bade | 10 |
| Saxe | 10 |
| Hesse | 6 |
| Hesse-Cassel | 6 |
| Mecklembourg | 4 |
| Total | 108 |

Les 13 régions-pays sont propriétaires de leurs terres et membres du bloc
commercial autrichien du SERG. La capacité arable de chaque portion d'État est
contrôlée ; les manoirs propriétaires restent locaux. Le PM `pm_simple_ranch`
et les trois autres PM de départ des élevages sont conservés.

540 représente la production **brute théorique à plein emploi**, avant effet
des fermes de subsistance remplacées, du débit de production et des variations
du marché. Ce n'est pas une garantie d'un déficit net nul en partie.
Les ajouts d'historique nécessitent une nouvelle campagne ; ils ne modifient
pas les bâtiments d'une sauvegarde existante.

## Contrôles

```powershell
python tools/audit_runtime_icon_bindings.py --check --baseline docs/reports/assets/runtime_icon_bindings_2026-10-06.json
python tools/validate_german_fabric_supply.py --baseline docs/reports/buildings/german_fabric_supply_2026-10-06.json
```

Contrôles statiques seulement : liaisons cohérentes, textures décodables non
vides et non copiées des erreurs, identité des recettes/PM protégés, delta exact
de 108 niveaux, terres et propriétaires valides, autres bâtiments inchangés.
Aucun contrôle visuel en jeu, commit, push ou mise à jour du Steam Build.
Les aperçus et autres diagnostics temporaires restent dans `.asset-cache/`.
