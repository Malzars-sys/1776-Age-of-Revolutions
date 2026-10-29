# Agra — stabilisation provisoire installée

Le **29 octobre 2026**, le joueur a choisi explicitement : « Appliquer la stabilisation provisoire des terres arables ». L'installation ne dépend donc plus d'une confirmation historique préalable des 24 millions d'habitants. Cette population reste provisoire et non certifiée comme recensement de 1776.

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**.

**Retour ultérieur du joueur, 29 octobre 2026 :** la famine d'Agra a disparu après l'ajout de terres. Cet effet est confirmé par le joueur ; la durée de simulation et les autres critères ci-dessous ne sont pas attestés. Reçu : `AGRA_HISTORICAL_REVIEW/USER_RUNTIME_ATTESTATION_2026_10_29.json`. [Recherche historique complémentaire](AGRA_HISTORICAL_REVIEW/REPORT.md) : les 24 millions ne sont pas validés historiquement et paraissent probablement trop élevés, sans nouveau total de 1776 assez étayé pour modifier les POPs.

## Changement effectif

Dans `map_data/state_regions/10_india.txt`, seul `STATE_AGRA.arable_land` passe de **483 à 764**, soit **281 terres supplémentaires** pour toute la région. La population et tous les autres champs restent identiques. Aucun autre État n'est corrigé dans cette installation.

À parts territoriales inchangées, la projection est de **444 → 702 terres** pour MARATH et **39 → 62** pour GAR. Le supplément de 258 niveaux de subsistance dans la portion marathe correspond à une capacité théorique supplémentaire de **2 580 000 emplois**, comparée aux **2 571 967 sans-emploi observés avant correction**. Ces nombres n'affirment pas que toutes les places seront occupées, ni que les revenus et la nourriture suffiront.

Ce réglage élargit aussi le potentiel futur d'agriculture commerciale. Il n'est pas présenté comme une hausse historiquement démontrée de 58 % de la surface cultivable. La reconstruction démographique reste un travail distinct.

## Contrôles réalisés

Commande : `python -X utf8 tools/apply_agra_arable_scenario.py --apply-provisional`.

Neuf contrôles statiques réussis : un seul fichier runtime modifié ; différence exactement limitée à la valeur arable ; valeur finale et empreinte conformes au plan ; populations, bâtiments et propriétaires inchangés ; autres régions inchangées ; sauvegarde originale de diagnostic conservée. **2 854 autres fichiers runtime conservent leur empreinte** pendant l'installation.

Preuves : `installation/AUTHORIZATION.json`, `installation/BASELINE.json`, `installation/APPLY_COMMAND.json`, `installation/VALIDATION.json`, `AGRA_PROVISIONAL_APPLIED.json`. Le plan et les préimages d'origine restent intacts. Les anciens contrôles qui exigeaient l'empreinte entière antérieure de ce fichier régional décrivent une version précédente ; ils ne sont pas réécrits.

## Contrôle en jeu restant

**Relancer Victoria 3 puis créer une nouvelle partie au 1er janvier 1776.** La session déjà ouverte et sa sauvegarde de diagnostic sont antérieures au changement. Charger l'ancienne sauvegarde ne constitue pas un contrôle fiable des nouvelles données initiales.

1. Vérifier le total régional et les deux portions d'Agra : projection 702 / 62, sous réserve des règles effectives d'allocation du moteur.
2. Comparer population et bâtiments à la référence : aucun changement prévu. Relever paysans, places vacantes et sans-emploi.
3. Relever la faim modérée, la grande famine, les revenus et prix alimentaires au départ puis après une période de simulation explicitement notée. La capacité nouvelle peut réduire le chômage sans résoudre toute la faim paysanne.
4. Vérifier sauvegarde et rechargement. Conserver les dates et empreintes des nouvelles observations.

**Le contrôle moteur complet reste à effectuer ; la disparition de la famine est désormais attestée par le joueur.** Le tableau `delivery/TABLEAU.html`, ses 61 crises et ses pourcentages d'Agra demeurent le relevé **avant stabilisation**, pas un résultat après correction. Aucun commit, push ou changement du vanilla.
