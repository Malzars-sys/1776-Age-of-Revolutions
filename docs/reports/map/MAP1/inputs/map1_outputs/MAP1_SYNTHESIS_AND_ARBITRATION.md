# MAP-1 — Synthèse documentaire mondiale et préparation du mapping (1776-01-01)

**Statut : SYNTHÈSE DOCUMENTAIRE RÉALISÉE ; MAPPING TECHNIQUE À EFFECTUER ; AUCUNE MODIFICATION CARTOGRAPHIQUE AUTORISÉE.** 10 octobre 2026.

## 1. Périmètre et traçabilité

Trente-six livrables originaux (recommandations, sources, couverture, incertitudes) provenant de neuf recherches indépendantes ont été rassemblés. Une copie additionnelle `R8_NORTH_AMERICA_CARIBBEAN_RECOMMENDATIONS(1).csv` est identique octet pour octet à la version sans suffixe (SHA-256) ; elle est exclue du total pour éviter un double comptage. Les empreintes de chaque original figurent dans `MAP1_INPUT_MANIFEST.csv`.

Le fichier `MAP_1776_BASELINE.csv` est issu de la branche principale **avant intégration définitive** du candidat `georg3mx-map-rework`; ne pas y incorporer ce dernier tacitement. La géométrie vanilla signalée dans MAP-0 est en 8192 × 3616, avec 40 875 couleurs/provinces (40 717 terre, 106 mer, 52 lacs). Une correspondance historique ne se déduit ni de la couleur RGB seule ni du nom de State_ID.

## 2. Résultats quantifiés et limites

| Mesure | Résultat |
|---|---:|
| Recommandations originales réunies | 1 005 |
| Sources bibliographiques réunies | 374 |
| Couples propriétaire/État dans les couvertures | 1 043 / 1 043 attendus |
| Couverture marquée CHANGE_PROPOSED | 181 |
| Couverture marquée UNRESOLVED | 598 |
| Couverture marquée REVIEWED_NO_CHANGE | 264 |
| Mapping MAPPING_REQUIRED | 982 |
| Mapping PROPOSED non vérifié | 23 |
| Mapping VERIFIED | **0** |
| Méthode A proposée | 295 |
| Méthode B proposée | 6 |
| Méthode C proposée | 0 |
| Méthode NONE / UNDETERMINED | 283 / 421 |
| Coordination interrégionale ou contestation déclarée | 150, dont 15 DISPUTED |
| Enregistrements `Requires_New_Tag=YES` | 75 (pas 75 TAGs distincts démontrés) |
| Recommandations proposant explicitement un autre propriétaire ou NEW_TAG_REQUIRED | 80 (pas 80 transferts autorisés) |
| Références Source avec `Document_Date=UNKNOWN` | 161 (non bloquant seul : de nombreuses sources sont des ouvrages modernes) |
| Dossiers sélectionnés P0 | 20 |
| Dossiers de mapping/coordination dans la file MAP-1 | 410 |

**Lecture correcte des statuts** : `REVIEWED_NO_CHANGE` signifie qu'aucun changement n'est proposé à ce niveau de revue, pas que chaque province historique a été validée. `Confidence=HIGH` exprime une confiance documentaire locale, **pas** une correspondance RGB prouvée. Les 23 `PROPOSED` n'ont pas d'IDs géographiques validés et ne doivent jamais devenir `VERIFIED` par conversion automatique.

Les tests de cohérence des CSV ont confirmé des en-têtes compatibles, l'unicité des `Change_ID` et `Source_ID`, la couverture unique des 1 043 couples et le rattachement des recommandations à leurs bibliographies. **Aucun contrôle externe exhaustif de validité des 374 sources ni des faits historiques n'a été réalisé.** Des liens ou pages peuvent être approximatifs, secondaires, postérieurs à 1776 ou nécessiter une confrontation. Ce n'est pas un visa scientifique.

## 3. Décisions opératoires de synthèse

1. Conserver **l'intégralité** des 1 005 recommandations dans `WORLD_BORDERS_1776_MASTER.csv`, avec leurs 29 champs d'origine et des champs MAP-1 explicites. Ne pas réduire à 181 : une question non résolue peut être plus importante qu'un `CHANGE_PROPOSED`.
2. Conserver les 374 sources et les 1 043 lignes de couverture sans déduire de nouvelles conclusions historiques.
3. Traiter les 80 lignes proposant un autre propriétaire uniquement comme **candidats**, dans `WORLD_BORDERS_1776_IMPLEMENTATION_DRAFT.csv`. Le CSV ne comprend aucune province RGB approuvée, aucun destinataire final confirmé, et chaque ligne porte `DO_NOT_APPLY`.
4. Classer comme **vérifications géographiques, sans transfert accepté** les recommandations avec `Proposed_Owner_TAG=UNCHANGED` et une méthode A/B. Cette mention n'autorise aucune réattribution.
5. Classer les 150 recommandations avec `Cross_Region_Conflict != NONE` dans le registre de conflits; coordination ne signifie pas contradiction factuelle. Les issues techniques MAP-0 BLOCKER/ERROR sont ajoutées séparément au registre; le même incident peut être répété dans main et le candidat sans constituer deux erreurs indépendantes.
6. La file `WORLD_BORDERS_1776_MAPPING_QUEUE.csv` regroupe les A/B, les changements de propriétaire explicites et les arbitrages interrégionaux. Priorités P0 de revue, puis dossiers à autre propriétaire, puis mapping général.
7. Aucune décision officielle n'est prise sur les frontières, les TAGs, les migrations d'habitants ni les effets diplomatiques. `MAP1_Approval_Status` reste `NOT_APPROVED` partout.

## 4. Vingt dossiers prioritaires

Détails et liens par `Change_ID`, `State_ID` et `MAP0_Issue_IDs` dans `MAP1_PRIORITY_ARBITRATION.csv`. Il s'agit de **dossiers de vérification**, non de vérités historiques nouvellement établies.

| Zone | Question fondamentale |
|---|---|
| Luxembourg / Wallonie | Le Luxembourg habsbourgeois doit-il rester entité distincte ? Que couvre `xD001A0` ? Que deviennent 37 881 habitants manquants et références de LUX dans le candidat ? |
| Lombardie austro-vénitienne | Résoudre `x867A90` attribué deux fois et le changement de `x9AC196` avec source historique et géométrie. |
| Silésie/Moravie/Galicie | Propriétés et scopes historiques incohérents; ne pas utiliser un ancien `State_ID` de script comme géolocalisation. |
| Bessarabie | Retirer hors du flux cartographique les commandes Git parasites du candidat, sans perdre le contenu historique. |
| Bassora | Assiégée au 1er janvier, occupation ultérieure dans l'année, chronologie à préserver. |
| Khorasan | Distinguer dynastie afsharide et domination zand; ne pas généraliser le TAG PER. |
| Bombay / Salsette | Île administrée par la Compagnie vs Salsette contestée; vérifier les limites des provinces. |
| Northern Circars / Guntur | Ne pas projeter sur Guntur un contrôle de compagnie acquis ultérieurement. |
| Mandchourie extérieure | Ne pas rétroagir les cessions russo-qing de 1858/1860. |
| Mindanao | Doubles propriétaires et répétitions, distinction défaut technique/autorité locale. |
| Micronésie occidentale | Province `xEF50C0` sans propriétaire initial; localisation nécessaire. |
| Kenya / Tanganyika | Doubles propriétaires enregistrés; à identifier géographiquement avant tout choix politique. |
| Alaska | Propriétés `ALK|ATB` répétées; distinguer établissements russes et autorité des peuples locaux. |
| Nunavut | Revendication HBC, activités de traite et souverainetés locales à dissocier. |
| Nouveau-Mexique | 11 provinces écrites SC1/COM; distinguer présidios, pueblos et autonomies autochtones. |
| Guyanes | `x6C6251` AP7/NET; contrôler littoral colonial, intérieur et source de frontières. |
| Rio Grande do Sul | Ne pas appliquer en janvier les occupations ayant changé plus tard en 1776. |
| Uruguay | Colônia do Sacramento portugaise au départ, opérations de 1777 ultérieures. |
| Pastaza / Maynas | Ne pas appliquer mécaniquement des réformes de 1802 au 1er janvier 1776; historique des bâtiments SC2 distinct. |

Les conclusions détaillées se trouvent dans les neuf `*_UNCERTAINTIES.md` originaux. En cas de doute de date, de souveraineté ou de polygone, garder `UNRESOLVED` et solliciter la recherche ou la vérification cartographique complémentaire nécessaire.

## 5. Phases restantes et portes de validation

**MAP-1A : mapping géographique.** Codex lit les fichiers en lecture seule, récupère le bitmap exact et le contrôle SHA-256. Générer pour les 410 dossiers une vue géographique contrôlable : visualisation de la province du jeu, relevé des localités, comparaison de cartes d'époque sourcées, zones floues représentées par annotations et non traitées par transfert. Aucune nouvelle province ajoutée. Protéger les 16 fichiers State Regions et tous les historiques pendant cette sous-phase.

**MAP-1B : synthèse arbitrée.** Pour chaque dossier, confirmer l'autorité historique, les provinces couvrant réellement la région et le type de relation. Les interfaces R1/R2, R2/R3, R3/R4, R3/R7, R4/R5, R5/R6 et R8/R9 doivent être relues des deux côtés quand concernées. Décrire les conflits entre sources plutôt que décider par nombre de citations. Les chefs régionaux peuvent répondre aux questions strictement localisées au besoin.

**MAP-1C : manifeste de modification.** Seules les lignes revues pourront recevoir `Approved_Owner_TAG` et les `Verified_Province_IDs`; tout transfert devra inclure source, capture ou superposition de géolocalisation, autorisation, conservation des pops et bâtiments (par culture/religion, PM/propriétaire), recrutement, ports, capitales, sujets, événements et référencements. Les méthodes B/C doivent faire l'objet d'une note de compatibilité supplémentaire; C nécessite un prototype séparé et accord de l'utilisateur.

**MAP-2 uniquement après MAP-1C validée** : intégration dans une branche isolée, lots régionaux, comparaisons avant/après, nouvelle partie, logs et tests performance/sauvegarde; pas de merge/push sans accord explicite.

## 6. Différencier le candidat georg3mx de main

Dans MAP-0, Codex avait récupéré la branche et préparé un merge **sans commit** dans un worktree. Les anomalies wallonnes, lombardes et les tokens Git en Bessarabie restent des blocages; **le candidat ne constitue pas une baseline publiée**. Éviter toute fusion qui effacerait les travaux ottomans récents ou qui supprimerait des populations/bâtiments. Les travaux VEN/GEN doivent être étudiés mais les historiques spécifiques protégés tant qu'un transfert n'est pas validé.

## 7. Livrables contenus dans ce paquet

- `WORLD_BORDERS_1776_MASTER.csv` : les 1 005 fiches enrichies de statuts non approuvés.
- `WORLD_BORDERS_1776_SOURCES.csv` : les 374 notices intactes.
- `WORLD_BORDERS_1776_COVERAGE.csv` : 1 043 lignes de couverture intactes.
- `WORLD_BORDERS_1776_MAPPING_QUEUE.csv` : 410 dossiers à cartographier ou arbitrer.
- `WORLD_BORDERS_1776_CONFLICTS.csv` : coordinations des régions et problèmes techniques MAP-0 de gravité ERROR/BLOCKER, non dédoublonnés arbitrairement.
- `MAP1_PRIORITY_ARBITRATION.csv` : 20 dossiers prioritaires choisis pour revue.
- `WORLD_BORDERS_1776_IMPLEMENTATION_DRAFT.csv` : 80 propositions de changement de propriétaire **sans autorisation d'application**.
- `MAP1_INPUT_MANIFEST.csv`, `MAP1_REGIONAL_SUMMARY.csv`, `MAP1_METRICS.json` : validation des entrées et mesures.
- `MAP1_CODEX_MAPPING_PROMPT.md` : demande opérationnelle détaillée pour Codex.

Les documents originaux MAP-0 et les 36 fichiers bruts sont conservés dans le ZIP de transmission; aucune donnée historique d'origine n'a été modifiée par cette synthèse.
