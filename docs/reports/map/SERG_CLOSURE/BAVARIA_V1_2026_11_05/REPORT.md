# SERG TERRITORIAL 1.0 — PROGRESSION : 45,11 %

**L'accord prussien est enregistré ; le premier lot bavarois est installé : Innbaiern, 175 cellules AUS → BAV, catégorie B, prêt à la validation joueur.** Aucun nouveau reçu moteur n'est créé.

## Progression

Le joueur approuve explicitement le gel prussien et les quatre reports P1, puis demande la Bavière. [Accord reçu](PRUSSIAN_DECISION_RECEPTION/USER_APPROVED_V1_DECISION.json). SC3-BRANDENBURG, SC3-SILESIA-LUSATIA, SC5-PRUSSIAN-WEST et SC5-EAST-FRISIA-SOUTH deviennent DEFERRED_APPROVED. Leurs réserves restent documentées ; les 14 noyaux déjà reçus conservent leur portée exacte.

**Avant/après cette mission : 93/235 → 106/235, 39,57 % → 45,11 %, 32/81 → 36/81.** Les treize points proviennent des reports P1 approuvés ; la nouvelle installation bavaroise ne gagne aucun point avant ses critères et sa réception. Périmètre 1.0.0, 81 tâches et 235 points inchangés.

## Premier lot bavarois livré

La sélection est SC2-AUSTRIA, P0, sans dépendance, pour l'interface Innbaiern/BAV-AUS : problème déjà compris dans son périmètre. Aucun 82e item créé. [Périmètre](SELECTION_AND_SCOPE.md), [sources et décision B](SOURCES.md).

- La province existante xFDA6CB, 175 cellules, devient bavaroise. Son tracé et tous les pixels du bitmap sont conservés ; aucune nouvelle province ni région économique créée.
- Le noyau Obernberg PAS, xEDC000 et 1 400 habitants, reste intact, ainsi que le noyau PAS originel de 40 cellules et le noyau SLZ de 12 cellules. Freising/Ratisbonne, la Prusse gelée et tous les autres territoires sont conservés.
- Les dix autres provinces AUS de STATE_AUSTRIA, les repères Linz/Freistadt/Vienne, les ressources, terrains et capacités agraires restent inchangés.
- La nouvelle portion BAV est nommée **Innbaiern** en français et en anglais, uniquement sous les conditions BAV/STATE_AUSTRIA/province concernée. Aucun locator physique, ville ou capitale nationale déplacé.
- **106 900 habitants** sont transférés du groupe south_german existant d'AUS vers BAV. Estimation régionale arrondie d'après le total 106 898 des cinq ressorts du relevé 1771/81, pas recensement exact de 1776 ni population tirée d'un nombre de pixels. Voir méthode et incertitudes dans SOURCES.md. AUS/Autriche passe de 1 636 657 à 1 529 757 ; PAS/Autriche reste à 1 400. Total mondial, profils culturels/religieux mondiaux et tous les autres groupes inchangés.
- Aucun bâtiment, niveau, PM, détenteur économique, unité, recrutement ou technologie modifié. Aucun nouveau TAG. Les travaux BUILD, fortifications/génie, diplomatie, Afrique, Balkans, économie, technologies et autres chantiers restent conservés hors liste d'installation.
- **599 titres impériaux inchangés en nombre et en étendue.** Seul le bénéficiaire de xFDA6CB passe d'AUS à BAV ; Obernberg reste PAS. Aucun membre ou électeur supplémentaire. Quatre dérivés impériaux sont régénérés après précontrôle sans divergence concurrente.

[Avant/après](BEFORE_AFTER.png), [géométrie exacte](GEOMETRY.json), [plan](PLAN.json), [12 fichiers installés, dont quatre nouveaux](INSTALLATION.json). Dix fichiers fonctionnels, un registre documentaire actif et un outil de chaînage sont concernés ; chaque préimage existante est sauvegardée.

## Limites assumées

Cette correction est une généralisation politique V1 de l'Innbaiern sur une province native déjà séparée d'Obernberg. Elle ne certifie pas une équivalence cadastrale parfaite, toutes les possessions de Salzbourg ou les limites détaillées de Vichtenstein/Neuburg/Wernstein. Ces juridictions sont distinguées dans les sources et leurs réserves restent visibles ; aucun noyau PAS/SLZ validé n'est absorbé. Le recalage R4 ancien n'est ni repris ni rendu artificiellement valide. Les diagnostics R5/Miller ne certifient pas des points de ville.

La population est une estimation de scénario pour ce proxy régional ; le profil catholique south_german dominant n'est pas un dénombrement des minorités. Aucun recensement de toute la Bavière ni équilibre économique moteur n'est proclamé.

**SC2-AUSTRIA reste IN_PROGRESS**, avec le sous-lot BV-INNBAIERN-175 en IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. La Bavière entière n'est pas déclarée terminée ; la Haute-Palatinat et les grands raccords franconiens restent candidats à une prochaine passe. Aucun deuxième lot commencé automatiquement.

## Contrôles et traitement des écarts

**42/42 contrôles de conservation validés** : delta mondial d'un seul propriétaire, 175 cellules exactes sans changement du bitmap, transfert démographique précis, totalité des bâtiments/PM/propriétaires/unités/pays, noyaux protégés, chaîne et couverture actuelle des 599 titres, fichiers partagés et archives. [VALIDATION.json](VALIDATION.json).

Le premier essai a obtenu 38/40. Son résultat brut reste dans VALIDATION_INITIAL_FULL_REPLAY.json. Deux assertions globales ont été examinées dans VALIDATION_METHOD_REVIEW.json : une relecture à partir de MAP2K seul omettait des bases/extensions approuvées séparément, avec les mêmes 60 écarts avant/après ; un ancien snapshot de x567452/Poméranie indiquait 341 cellules contre 400, identiquement avant/après. Aucun de ces écarts ne provient de l'Innbaiern. Les contrôles corrigés vérifient strictement la migration depuis le registre courant complet de 599 titres et sa concordance entière avec les règles du compilateur, tout en conservant les résultats initiaux. Aucun ancien rapport ou territoire n'est réécrit.

Les 11 références globales invalides et 14 clés dupliquées héritées restent documentées, sans nouvelle erreur.

Exécution ciblée finale : **79 tests exécutés, 78 réussis et une exclusion documentée**, aucun échec ni erreur. L'exclusion concerne le contrôle global fondé sur le snapshot initial antérieur aux livraisons autorisées ; la conservation actuelle est vérifiée par différence. **22/22 contrôles finaux passent** : 2 875 fichiers fonctionnels hors périmètre et 1 802 archives antérieures inchangés. Le contrôle des différences de cette passe est propre. Le contrôle global signale toujours deux espaces terminaux dans un fichier de formations militaires africaines, identique à son état avant la passe ; ce constat hérité n'est pas effacé ni présenté comme un résultat global propre. Les tests ciblés, le contrôle canonique, les différences et la conservation finale sont consignés dans TEST_RESULTS.json, CANONICAL_CHECK.json, DIFF_CHECK.json et FINAL_CHECKS.json. Aucun résultat antérieur n'est présenté comme une nouvelle exécution.

Aucune opération Git d'écriture, aucun vanilla modifié. Aucune validation moteur exécutée par l'agent.

## Test joueur et prochaine action

[Protocole ciblé](PLAYER_TEST_PROTOCOL.md) : relancer le mod principal, nouvelle partie 1776, vérifier Innbaiern/BAV et les voisins protégés, population/marché/subsistance, droits impériaux accessibles, un mois et sauvegarde/rechargement. Aucun test n'est présumé réussi.

Après réception de ce lot, prochaine candidate bavaroise : **Haute-Palatinat et grands raccords franconiens**, en préservant les noyaux déjà validés et en distinguant Bavière/Palatinat avant leur réunion postérieure au départ du scénario. Cette candidate n'est pas commencée dans cette passe.
