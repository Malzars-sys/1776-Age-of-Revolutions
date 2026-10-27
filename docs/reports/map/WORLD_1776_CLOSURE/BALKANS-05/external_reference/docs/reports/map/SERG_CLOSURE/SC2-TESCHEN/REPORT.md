# SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %

Passe du 25 octobre 2026. **TE-R-CORE installé, IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. SC2-TESCHEN demeure BLOCKED P1 pour sa correspondance territoriale/démographique complète.** Aucun reçu humain Teschen ; aucun point nouveau.

## Réception d’Ortenbourg et sélection

Le joueur a explicitement réussi l’intégralité du protocole OR-I-CORE. Les 26 contrôles de conservation ont permis d’enregistrer le [reçu borné](../SC1-ORTENBURG/RUNTIME_USER_ATTESTATION_2026_10_25.json), sans date effective de test, capture ou mesure supplémentaire. Les anciennes preuves sont intactes. Les évolutions de fichiers partagés depuis la livraison ont été contrôlées au niveau du bloc et des quatre cellules ORT, sans restauration.

SC1-ORTENBURG reste **BLOCKED P1** : villages souverains, possessions médiates et démographie rurale comparable ne sont pas clos. Aucun point régional n’est attribué. Le contrôle canonique après réception donne **82/235 = 34,89 %, 24/81 jalons qualifiés**, puis sélectionne **SC2-TESCHEN**, P1, sans dépendance. C’est l’unique nouvelle tâche de cette passe ; [preuve de sélection](SELECTION.json).

## Conclusion historique et correction retenue

Les [sources examinées](SOURCES.md) distinguent le fief ducal de Marie-Christine et Albert, le cadre politique habsbourgeois et l’appartenance impériale territoriale. Elles ne justifient pas un nouveau pays souverain ni un nouvel électeur. Le titre personnel ne remplace pas le souverain du TAG AUS et ne confond pas les domaines ducaux avec les seigneuries voisines.

La carte Seutter déjà disponible a été relue ; aucun recalage infructueux n’est répété. Le registre corrige le défaut démontré de la représentation B existante. Le dénombrement régional de **112 850 habitants en 1770–1771** reste à rapprocher du ressort effectivement modélisé ; il ne remplace pas automatiquement les **135 753 habitants** du pool technique actuel. Aucune correction de POP n’est installée sur une équivalence spatiale non démontrée.

## Installation bornée TE-R-CORE

| Élément | Avant | Après |
| --- | --- | --- |
| RGB `x9061E0` | 179 cellules AUS, STATE_WEST_GALICIA | Identique : aucun transfert ni changement de bitmap |
| Droit impérial de ce RGB | Absent | Une entrée AUS explicite, catégorie B |
| Registre | 580 titres | 581 titres ; les 580 antérieurs sont identiques |
| Emprise reconnue | Portion omise | +179 cellules impériales reconnues ; aucune nouvelle terre physique |
| Autres portions de WEST_GALICIA | Non inscrites par cette passe | Identiques ; aucune inclusion générale de la Galicie |
| Membres et électeurs | Liste antérieure, neuf électeurs | Identiques ; aucun nouveau pays, membre ou électeur |
| POPs, bâtiments, PM, propriété économique, ressources, unités, lois et technologies | État courant du workspace | Aucun changement par cette passe |

La chaîne versionnée reçoit une migration de **droits uniquement** : aucune migration de souveraineté. Le compilateur dispose d’une exception explicite `(RGB, région, propriétaire)` ; sa liste générale de régions ne reçoit pas WEST_GALICIA. Le contrôle négatif doit refuser une autre province, un autre titulaire ou une extension non déclarée.

Les scripts de détection, restitution, suivi et liste de réponse sont régénérés à partir du contenu courant et des droits explicites. La restitution éventuelle ne cible que `x9061E0`, jamais toute la région. Le dénominateur interne du mécanisme de cohésion passe de 580 à 581 titres ; il est distinct du dénominateur **235 points** de la feuille de route. Quatre localisations techniques FR/EN sont ajoutées en suivant les clés déjà consommées. Aucun texte immersif validé n’est réécrit.

Les préimages et sorties attendues sont archivées dans `TEXT_BEFORE.json` et `EXPECTED_TEXT.json`. Avant chaque écriture, la préimage courante est vérifiée ; les fins de ligne et BOM sont conservés. Une sortie identique après normalisation des fins de ligne est laissée intacte.

## Limites et prochaine action

Le registre répare TE-R-CORE ; il ne certifie pas les limites historiques complètes, les juridictions particulières de Frýdek/Fryštát/Bielitz ou leur correspondance démographique. Il reste à rapprocher cartes et dénombrements de périmètres comparables, sans multiplier les populations par la surface ni imposer un cadastre parfait comme préalable.

La région reste **BLOCKED P1**, avec le seul sous-lot de registre en attente de test. [Protocole joueur](PLAYER_TEST_PROTOCOL.md) : nouvelle partie autrichienne en 1776, contrôle de la portion impériale et des portions galiciennes exclues, témoins antérieurs, un mois puis sauvegarde/rechargement. Aucun scénario conditionnel de restitution après conquête n’est déclaré observé.

Les blocages Innviertel et Autriche antérieure ne sont pas rouverts. WORLD/Balkans, TECH, économie, génie, fortifications et autres travaux concurrents restent hors périmètre. Les anciennes archives et validations sont conservées ; les différences externes éventuelles sont consignées séparément. Aucune écriture Git ou vanilla.

Les résultats statiques, ciblés et cumulatifs sont consignés dans les pièces de validation de cette passe, après leur exécution. La progression reste fondée sur les seuls statuts qualifiés ; la prochaine candidate indépendante sera calculée sans être commencée.

## Résultats finaux exécutés

Teschen : 123/123 contrôles statiques, 18/18 ciblés, suite cumulative brute 510/530 avec 19 échecs classés et une exclusion héritée. Quatorze assertions déjà classées ; cinq nouveaux écarts expliqués par couche/reçu/autorisation explicites et 41 pixels externes antérieurs à la capture Teschen. Garde négatif Ortenbourg recontrôlé, aucun ancien test modifié, aucun échec inexpliqué. TE-R-CORE seul en attente du joueur ; région BLOCKED P1 et 82/235=34,89 % inchangés. SC3-HOLSTEIN seulement identifiée.

Le contrôle final et ses limites sont dans FINAL_CHECKS.json. Les 19 traces brutes sont conservées ; les nouvelles divergences ne sont pas appelées toutes « échecs hérités ». Aucun moteur lancé et aucune validation humaine de Teschen.
