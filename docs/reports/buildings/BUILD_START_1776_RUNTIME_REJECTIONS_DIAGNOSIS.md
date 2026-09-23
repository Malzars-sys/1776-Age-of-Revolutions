# Diagnostic des bâtiments refusés ou réduits au démarrage 1776

Source : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs\error.1.log`, session du 22 septembre 2026 à 21:11. Ce document est un diagnostic ; aucun placement ni potentiel régional n'a été modifié pendant cette passe.

## Bilan

| Cause signalée par le jeu | Messages | Effet |
| --- | ---: | --- |
| `state.cpp:7313` : type absent des `arable_resources` de la région | 55 | Bâtiment supprimé |
| `state.cpp:7329` : niveaux supérieurs aux `capped_resources` de la région | 32 | Niveaux réduits, parfois à zéro |
| **Total étudié** | **87** | |

Deux messages `state.cpp:7337` sur un dépassement des terres arables sont volontairement exclus de ce total et laissés sans correction, conformément à la consigne.

### Répartition par type

| Type de bâtiment affiché dans le journal | Refusés | Réduits |
| --- | ---: | ---: |
| Cultures de blé | 27 | 0 |
| Cultures de millet | 11 | 0 |
| Plantations de coton | 7 | 0 |
| Cultures de riz | 4 | 0 |
| Plantations de soie | 3 | 0 |
| Cultures de maïs | 1 | 0 |
| Élevages de bétail | 1 | 0 |
| Plantations de cannes à sucre | 1 | 0 |
| Salines | 0 | 10 |
| Mines d'or | 0 | 7 |
| Mines de sel | 0 | 6 |
| Mines de cuivre | 0 | 2 |
| Ports de chasse à la baleine | 0 | 2 |
| Quais de pêche | 0 | 2 |
| Mines de fer | 0 | 1 |
| Mines de plomb | 0 | 1 |
| Camps de bûcherons | 0 | 1 |

## Vérifications représentatives

- **Scanie, blé refusé.** La définition `STATE_SCANIA` dans `map_data/state_regions/00_west_europe.txt` n'autorise que `building_rye_farm` et `building_livestock_ranch` comme ressources arables. Le placement d'une ferme de blé dans `common/history/buildings/00_west_europe.txt` ne peut donc pas être chargé.
- **Mysore, millet refusé.** `STATE_MYSORE` dans `map_data/state_regions/10_india.txt` autorise le riz et plusieurs plantations, mais pas `building_millet_farm`. L'historique de `common/history/buildings/10_india.txt` place pourtant ce type dans cet État.
- **Bengale occidental, saline réduite à zéro.** `STATE_WEST_BENGAL` dans `map_data/state_regions/10_india.txt` ne déclare pas `building_salt_pan` dans ses ressources plafonnées, tandis que `common/history/buildings/10_india.txt` y place des salines. Le moteur traite leur potentiel comme nul.
- **Minas Gerais, mine d'or réduite.** `STATE_MINAS_GERAIS` dans `map_data/state_regions/07_south_america.txt` plafonne `building_gold_mine` à 2 ; `common/history/buildings/07_south_america.txt` place 4 niveaux. Le journal confirme la réduction de 4 à 2.

La cause immédiate est donc une **discordance entre l'historique des bâtiments et les potentiels de `map_data/state_regions`**, et non un doublon résiduel de bloc d'État. Il est plausible que la consolidation récente des définitions d'États ait rendu visibles des placements auparavant masqués ; le journal seul ne permet pas de le prouver. Le validateur actuel vérifie la concordance des placements avec la matrice de construction, mais pas systématiquement leur compatibilité avec les potentiels régionaux : un résultat de matrice valide ne garantit donc pas l'absence de ces 87 avertissements.

Pour une passe corrective ultérieure, chaque cas devra être arbitré entre un placement historique alternatif, une réduction de niveau, ou une modification explicite du potentiel régional. Aucun potentiel n'a été ajouté automatiquement, et aucun dépassement de terres arables n'a été traité ici.
