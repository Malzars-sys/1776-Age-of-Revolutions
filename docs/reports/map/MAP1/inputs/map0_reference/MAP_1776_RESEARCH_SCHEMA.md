# MAP-0 — Contrat commun des recherches territoriales

Date cible : **1776-01-01**. Version du contrat : MAP-0/1, 2026-10-10.
Les CSV fournis sont un inventaire du mod, pas une carte historique validée.

## Fichiers attendus de chaque chef

`<Region_ID>_RECOMMENDATIONS.csv`, `<Region_ID>_SOURCES.csv`,
`<Region_ID>_UNCERTAINTIES.md`, `<Region_ID>_COVERAGE.csv` et, si utile,
cartes annotées dont l'échelle, la date, la provenance et la légende sont indiquées.
CSV UTF-8, séparateur virgule, guillemets CSV standards; listes internes séparées par `|`.
Une ligne de couverture par couple initial Owner_TAG + State_ID :
`Region_ID,State_ID,Current_Owner_TAG,Review_Status,Change_IDs,Notes`.
`Review_Status` : `REVIEWED_NO_CHANGE`, `CHANGE_PROPOSED`, `UNRESOLVED`.
Les territoires absents du catalogue mais historiquement nécessaires sont signalés
dans une section `OUTSIDE_BASELINE`, jamais inventés comme provinces du jeu.

## En-tête obligatoire des recommandations

```csv
Region_ID,Change_ID,Province_ID,Province_IDs,State_ID,Current_Owner_TAG,Proposed_Owner_TAG,Historical_Polity_Name,De_Jure_Sovereign,Effective_Controller,Relationship_Type,Control_Status,Historical_Date,Source_IDs,Confidence,Evidence_Summary,Gameplay_Representation,Map_Edit_Method,Requires_New_Tag,Requires_State_Split,Cross_Region_Conflict,Research_Notes,Mapping_Status,Geographic_Location,Historical_Conclusion,Geographic_Correspondence,Gameplay_Approximation,Unresolved_Uncertainty,Secondary_Region_ID
```

| Colonne | Valeurs et validation |
|---|---|
| Region_ID | Un des neuf identifiants exacts de MAP_1776_9_REGIONS.csv. Responsable principal unique. |
| Change_ID | Identifiant unique : `<Region_ID>-0001`, etc. Stable lors des révisions. |
| Province_ID | Un `xRRGGBB` présent dans la baseline, ou vide avec MAPPING_REQUIRED. Aucun numéro ordinal inventé. |
| Province_IDs | Liste `|` de provinces vérifiées; vide si mapping absent. Ne pas répéter Province_ID dans cette liste. |
| State_ID | Identifiant exact présent dans l'inventaire; vide seulement si le mapping n'est pas établi. Plusieurs États : lignes distinctes sous Change_ID suffixé, avec lien explicite. |
| Current_Owner_TAG | TAG exact de la baseline, pas le propriétaire supposé historique. Propriétés multiples contestées : lignes séparées et conflit explicite. Vide seulement pour une zone non mappée. |
| Proposed_Owner_TAG | TAG existant vérifié, `NEW_TAG_REQUIRED`, `UNCHANGED`, ou vide si non déterminé. Ne pas attribuer un TAG moderne par défaut. |
| Historical_Polity_Name | Nom historique documenté, texte libre; préciser endonyme/exonyme lorsqu'utile. |
| De_Jure_Sovereign | Nom de souverain ou d'entité attesté; `NONE_ATTESTED`, `DISPUTED`, `UNKNOWN` si approprié. Ce n'est pas automatiquement un TAG. |
| Effective_Controller | Autorité locale attestée; `DISPUTED`, `UNKNOWN` possibles. Distinguer contrôle et revendication. |
| Relationship_Type | `DIRECT`, `PERSONAL_UNION`, `VASSAL`, `TRIBUTARY`, `PROTECTORATE`, `COLONY`, `CHARTERED_COMPANY`, `CONFEDERAL`, `AUTONOMOUS`, `INDEPENDENT`, `CLAIM_ONLY`, `DISPUTED`, `UNKNOWN`. Types de recherche, pas garantie de disponibilité moteur. |
| Control_Status | `DIRECT_ADMINISTRATION`, `MILITARY_CONTROL`, `LOCAL_AUTONOMY`, `INDIGENOUS_SOVEREIGNTY`, `TRADE_POST_ONLY`, `CLAIM_ONLY`, `DISPUTED`, `FLUCTUATING`, `NO_DEFENSIBLE_LINEAR_BORDER`, `UNKNOWN`. |
| Historical_Date | Toujours `1776-01-01`; événements ultérieurs séparés dans Research_Notes avec dates exactes. |
| Source_IDs | Une ou plusieurs références existantes dans le CSV SOURCES, séparées par `|`. Au moins une source probante pour chaque correction. |
| Confidence | `HIGH`, `MEDIUM`, `LOW`, `UNRESOLVED`; justifier les contradictions, ne pas calculer une certitude depuis le seul nombre de sources. |
| Evidence_Summary | Synthèse factuelle : fiscalité, juridiction, implantation, garnison, traité, administration, etc.; citer les pages/cartes. |
| Gameplay_Representation | `EXISTING_OWNER`, `SUBJECT`, `NEW_POLITY`, `DECENTRALIZED_POLITY`, `TREATY_PORT_ONLY`, `CLAIM_ONLY`, `SPLIT_CONTROL`, `NO_CHANGE`, `UNRESOLVED`; proposition, pas édition. |
| Map_Edit_Method | `A_EXISTING_PROVINCES`, `B_STATE_REGIONS`, `C_GEOMETRY`, `NONE`, `UNDETERMINED`. Ne proposer C qu'avec preuve que A/B échouent. |
| Requires_New_Tag / Requires_State_Split | `YES`, `NO`, `UNDETERMINED`. Une autorité historique ne suppose pas automatiquement un nouvel État jouable. |
| Cross_Region_Conflict | `NONE`, `COORDINATION_REQUIRED`, `DISPUTED`; décrire le désaccord et citer les Change_IDs liés. |
| Research_Notes | Texte libre, limites des sources, calendrier, précautions VEN/GEN, liens de discussion. |
| Mapping_Status | `VERIFIED`, `PROPOSED`, `MAPPING_REQUIRED`. VERIFIED exige superposition vérifiable avec provinces du jeu; PROPOSED n'est pas validé pour intégration. |
| Geographic_Location | Toponymes, coordonnées/zone, rivière, côte, district ou carte annotée; obligatoire si MAPPING_REQUIRED. |
| Historical_Conclusion | Ce qui est historiquement établi, indépendamment de ce que le moteur peut représenter. |
| Geographic_Correspondence | Comment l'espace historique correspond ou ne correspond pas aux provinces actuelles. |
| Gameplay_Approximation | Compromis proposé; `NONE` possible; expliciter les pertes de précision. |
| Unresolved_Uncertainty | `NONE` ou question non résolue, avec sources en conflit et ce qui permettrait de trancher. |
| Secondary_Region_ID | Vide ou l'un des huit autres IDs; un interlocuteur, jamais un second propriétaire de mission. |

Les noms historiques et résumés sont des textes libres sourcés; les valeurs contrôlées
ci-dessus ne doivent pas servir à masquer un manque de preuve. Une contradiction
non résolue reste UNRESOLVED et n'est pas intégrée automatiquement.

## Sources

En-tête : `Source_ID,Author,Title,Publication_Date,Document_Date,URL_or_Bibliographic_Reference,Pages_or_Map,Source_Type,Access_Date,Temporal_Relevance,Limitations`.
Source_ID unique préfixé par Region_ID; dates ISO si connues, sinon date bibliographique
exacte et mention `UNKNOWN` sans inventer. Source_Type : `PRIMARY_TREATY`,
`PRIMARY_ADMINISTRATIVE`, `PERIOD_MAP`, `ACADEMIC_MONOGRAPH`, `ACADEMIC_ARTICLE`,
`HISTORICAL_ATLAS`, `OTHER_EXPLAINED`. Fournir l'auteur, le titre, la date,
l'URL ou référence complète et les pages/cartes. Une URL seule est insuffisante.
Comparer les cartes d'époque à leur objectif et à leur biais : revendication,
itinéraire, commerce et administration ne signifient pas la même chose.

## Procédure de synthèse centrale

1. Vérifier couverture exhaustive du périmètre, sources et date exacte.
2. Résoudre doublons et interfaces par Change_ID, sans vote automatique entre sources.
3. Séparer conclusion historique, correspondance géographique et compromis de jeu.
4. Mapper les MAPPING_REQUIRED dans un lot technique dédié; ne jamais inventer un ID.
5. Faire approuver les transferts de population, bâtiments, capitales, ports et sujets.
6. Priorité A, puis B, et C seulement si nécessité documentée. Les chercheurs ne modifient aucun fichier du mod.

VEN et GEN restent inclus; leurs historiques spécifiques de population/bâtiments
sont protégés et exigent une décision explicite avant toute redistribution.
