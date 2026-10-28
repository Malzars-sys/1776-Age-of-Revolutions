# SERG TERRITORIAL 1.0 — RÉCEPTION HUMAINE DE MAP2A

## Mission unique

Enregistre le reçu humain de `SC2-MAP2A-VALIDATION` et recalcule la progression canonique du SERG.

Lis `AGENTS.md`, les instructions applicables de `.agents/` et les documents du suivi `docs/reports/map/SERG_CLOSURE/`.

Réutilise les rapports historiques `MAP2A`, les anciens contrôles de conservation et le protocole groupé établi après la réception du Luxembourg.

Ne commence aucune nouvelle correction territoriale.

## 1. Déclaration explicite du joueur

**Je confirme avoir testé personnellement et réussi l'intégralité du protocole `SC2-MAP2A-VALIDATION` dans Victoria 3.**

Les contrôles suivants ont réussi :

- Nouvelle partie au 1er janvier 1776.
- Les Trois Ligues sont représentées par `SWI` dans la portion concernée de Lombardie.
- Bergame reste sous souveraineté vénitienne (`VEN`).
- Les deux portions de Silésie autrichienne sont correctement attribuées à `AUS` dans la région technique de Moravie (`x71E080` et `xF0E080`).
- Teschen appartient à `AUS` dans `STATE_WEST_GALICIA`, sur `x9061E0`.
- Les populations associées aux corrections MAP2A sont présentes et cohérentes avec la livraison.
- Les bâtiments, notamment les deux niveaux textiles et le niveau d'infrastructure associés à Teschen, sont conservés.
- Le recrutement autrichien est correctement présent.
- Aucune disparition anormale des unités ou des formations concernées n'a été constatée.
- Un mois complet de simulation s'est déroulé sans anomalie.
- La sauvegarde et le rechargement ont réussi.

Cette attestation concerne les corrections MAP2A effectivement inspectées.

N'invente aucune capture, date effective de test, statistique économique, mesure d'emploi ni observation supplémentaire.

## 2. Reçu humain

Après vérification de la conservation des éléments livrés, j'autorise explicitement l'enregistrement de :

`SC2-MAP2A-VALIDATION = PASS_RUNTIME_USER_VALIDATED`

Créer un reçu distinct, conforme aux conventions du suivi SERG, avec :

- L'identifiant stable de la tâche.
- La déclaration du joueur.
- Le périmètre exact des corrections inspectées.
- Les références aux rapports MAP2A.
- Les preuves techniques effectivement disponibles.
- Les limites de l'attestation.

**Ne pas propager ce reçu à d'autres tâches.**

En particulier :

- `SC2-TESCHEN` reste distinct.
- `TE-R-CORE`, correction ultérieure du registre impérial, n'est pas automatiquement validé.
- Les autres tâches de validation groupée conservent leurs statuts.
- Le reçu Luxembourg déjà enregistré reste inchangé.
- La validation MAP2A n'homologue pas les frontières cadastrales de tous les secteurs silésiens.

## 3. Contrôles de conservation

Avant toute écriture :

1. Relire le workspace actuel.
2. Vérifier les RGB, propriétaires et State Regions des quatre corrections MAP2A.
3. Vérifier la conservation des populations, bâtiments, PM et unités associés.
4. Contrôler les différences éventuelles introduites par les agents concurrents.
5. Exécuter les tests ciblés de MAP2A et les contrôles canoniques du SERG applicables.
6. Conserver les résultats bruts et classifier les échecs éventuels.

Ne restaure aucune ancienne baseline.

Ne modifie ni la carte, ni les populations, ni les bâtiments pour forcer la réussite des tests.

Si une régression fonctionnelle nouvelle affecte la portée du reçu, ne force pas la clôture : documente précisément le problème.

## 4. Recalcul de la progression

État canonique attendu avant cette réception :

- 83/235 points.
- 35,32 %.
- 25/81 tâches qualifiées.

Poids de `SC2-MAP2A-VALIDATION` : **2 points**.

Si les contrôles et le validateur canonique confirment la clôture, l'état attendu devient :

- **85/235 points.**
- **36,17 %.**
- **26/81 tâches qualifiées.**

Le résultat doit être calculé par le validateur canonique, pas saisi arbitrairement.

Mettre à jour les fichiers pertinents :

- `ROADMAP_STATE.json`
- `ROADMAP.md`
- `NEXT_ACTION.md`
- `BLOCKERS.md`
- L'historique additif et les vues générées nécessaires.

Ne modifie pas les 81 tâches, les poids, le dénominateur de 235 points ni le périmètre 1.0.0.

## 5. Suite du chantier

Les validations encore attendues sont :

- `SC4-MILAN-VALIDATION`
- `SC4-PIEDMONT-VALIDATION`
- `SC5-MINDEN-VALIDATION`
- `SC5-COLOGNE-VALIDATION`
- `SC5-MAINZ-VALIDATION`
- `SC6-SWABIA-CONTINUATION-VALIDATION`

Elles représentent **8 points supplémentaires conditionnels**.

Actualise le protocole groupé en retirant Luxembourg et MAP2A, tous deux reçus, si la clôture MAP2A aboutit.

Conserve séparément les protocoles encore ouverts pour Teschen `TE-R-CORE` et la mine de sel de Berchtesgaden.

Ne commence aucun nouveau territoire, notamment `SC3-HOLSTEIN`.

## 6. Restrictions

- Aucune écriture Git : commit, push, staging, merge, reset, rebase ou changement de branche.
- Aucune modification du vanilla.
- Aucune modification fonctionnelle du mod dans cette mission de réception.
- Protection intégrale des travaux concurrents.
- Conservation des preuves historiques et des anciens résultats bruts.

## 7. Rapport final attendu

Commencer par :

**SERG TERRITORIAL 1.0 — PROGRESSION : XX,XX %**

Présenter :

1. Reçu MAP2A enregistré et périmètre exact.
2. Contrôles de conservation exécutés.
3. Tests réussis, échecs et exclusions éventuelles.
4. Progression avant/après.
5. Statut de la tâche.
6. Liste actualisée des six validations restantes.
7. Prochaine validation joueur recommandée.

**Instruction finale : enregistrer exclusivement le reçu humain de `SC2-MAP2A-VALIDATION` si les vérifications le permettent, recalculer la progression canonique et ne commencer aucune autre tâche.**