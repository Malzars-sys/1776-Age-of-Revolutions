# SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %

Réévaluation ciblée de **SC2-TESCHEN**, 29 octobre 2026 ; référence historique au 1er janvier 1776. **Recommandation : option C, maintien du blocage régional.** Aucune nouvelle frontière, population ou correction de gameplay installée.

La conservation sous `AUS` est politiquement cohérente : le duché central, les seigneuries de Frýdek et Fryštát et le duché distinct de Bielsko appartiennent au cadre supérieur habsbourgeois et bohémien. Ils ne sont pas tous les domaines personnels de Marie-Christine et Albert. Frýdek n'est acquis par le couple qu'en 1797. Cette distinction n'exige pas un nouveau TAG indépendant par défaut.

Les deux dénombrements proches de 112 800 habitants ne concernent pas seulement le domaine de Chambre : les seigneuries distinctes figurent dans leur couverture régionale. Le total politique inclut des Juifs ; le relevé ecclésiastique les exclut selon l'étude S1. L'étude Nesládková retrouvée et consultée fournit des localités et des précisions de méthode, mais aussi deux petites incohérences arithmétiques, conservées dans le dossier. Aucun taux régional comparable ne justifie de transformer automatiquement 112 850 en 135 753 pour 1776.

La correspondance des grands ensembles et des localités recensées avec les **179 cellules** reste non démontrée. Il serait prématuré de remplacer les 135 753 habitants, comme de les homologuer comme estimation de 1776. Aucune correction territoriale ou démographique précise n'est suffisamment étayée pour installation. Ce constat ne rétablit pas une exigence de cadastre parfait : un appariement défendable des localités structurantes et des grands ensembles, ou un arbitrage explicite de conservation avec réserve, est la prochaine dépendance historique.

## Livrables et décision proposée

1. [Rapport territorial](TERRITORIAL_REPORT.md) : autorités, domaines, seigneuries, voisins exclus et comparaison bornée avec les pixels.
2. [Rapport démographique](DEMOGRAPHIC_REPORT.md) : catégories, localités, comparabilité, écarts et absence de total de remplacement justifié.
3. [Tableau des incertitudes](UNCERTAINTIES.md) : réserves substantielles séparées des imprécisions acceptables et contradictions des sources.
4. [Arbitrage proposé](ARBITRATION_PROPOSAL.md), également [en JSON](PROPOSED_DECISION.json) : option C recommandée et proposition concrète de conservation B avec réserve, **non approuvée**. Le joueur peut arbitrer cette proposition ; l'agent ne clôture pas la région.
5. [Vérification technique](TECHNICAL_VERIFICATION.md), résultats bruts et manifeste de conservation.
6. [Contrôles humains encore nécessaires](PLAYER_CHECKS_REMAINING.md) : seulement TE-R-CORE, sans refaire les obligations MAP2A déjà attestées.

Les [sources et pages](SOURCES.md) rendent les conclusions traçables. Les PDF existants et les anciens rapports sont conservés ; le PDF Nesládková, ses extraits et les lectures visuelles sont dans `EVIDENCE/`. Aucun ancien recalage cartographique rejeté n'a été relancé.

## Résultats effectifs et conservation

- **30/30 contrôles ciblés actuels PASS** ; registre de 581 titres, seuls les 179 pixels ciblés ajoutés au masque impérial, neuf électeurs, mêmes données Teschen.
- Suite ancienne Teschen : **16/18 PASS, deux échecs de snapshot documentés**, sans modifier les tests ni effacer leurs résultats.
- Suite canonique : **27 PASS, un SKIP prévu, aucun échec** ; validateur canonique **PASS**.
- Ancien résultat de 123 contrôles consulté, pas revendiqué comme nouvelle exécution. **Aucun moteur exécuté et aucun reçu humain créé.**
- 58 fichiers protégés inchangés ; aucune dépendance fonctionnelle Teschen modifiée pendant la mission. Six suppressions de chemins musicaux concurrentes observées hors périmètre et préservées, sans restauration. Git HEAD/branche/index conservés ; vanilla non modifié.

## Suivi officiel avant / après

| Mesure | Avant | Après |
| --- | --- | --- |
| Points qualifiés | 93/235 | **93/235** |
| Pourcentage calculé | 39,57 % | **39,57 %** |
| Tâches qualifiées | 32/81 | **32/81** |
| Tâches bloquées | 23 | **23** |
| SC2-TESCHEN | BLOCKED P1, deux points non attribués | **Identique** |
| TE-R-CORE | IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION | **Identique** |

Le validateur a recalculé les valeurs, mais **aucun fichier du suivi canonique n'est écrit**, conformément à cette mission : `ROADMAP_STATE.json`, `ROADMAP.md`, `NEXT_ACTION.md`, `BLOCKERS.md`, `PROGRESS_HISTORY.md` et les preuves préexistantes restent intacts.

La prochaine validation utile est celle du **registre TE-R-CORE** selon la liste minimale préparée. L'arbitrage régional historique reste indépendant du résultat moteur. Aucun nouveau territoire, aucune seconde tâche et aucune reprise automatique de Holstein n'ont été commencés.
