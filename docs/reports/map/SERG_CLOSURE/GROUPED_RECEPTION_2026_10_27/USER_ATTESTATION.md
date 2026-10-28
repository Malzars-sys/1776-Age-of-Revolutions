# SERG TERRITORIAL 1.0 — RÉCEPTION HUMAINE GROUPÉE DE SIX TÂCHES

## Mission

Enregistre les six validations humaines explicitement confirmées par le joueur, vérifie la conservation des corrections existantes, puis recalcule la progression officielle du SERG.

**Mission de réception uniquement : aucune nouvelle correction fonctionnelle ni création territoriale.**

Commence par lire `AGENTS.md`, les instructions applicables de `.agents/` et les documents canoniques de `docs/reports/map/SERG_CLOSURE/`.

Réutilise les rapports de livraison, les anciens tests et le protocole groupé établi après les validations Luxembourg et MAP2A.

Ne recommence aucun audit historique général.

## 1. Attestation explicite du joueur

Je confirme avoir personnellement effectué et réussi l'intégralité des six protocoles suivants dans Victoria 3 :

1. `SC4-MILAN-VALIDATION`
2. `SC4-PIEDMONT-VALIDATION`
3. `SC5-MINDEN-VALIDATION`
4. `SC5-COLOGNE-VALIDATION`
5. `SC5-MAINZ-VALIDATION`
6. `SC6-SWABIA-CONTINUATION-VALIDATION`

### Conditions communes réellement confirmées

- Nouvelle partie commencée au **1er janvier 1776**.
- Tous les contrôles propres aux six lots ont été effectués et réussis.
- Un mois complet de simulation s'est déroulé sans anomalie sur les lots contrôlés.
- Sauvegarde et rechargement réussis.

Ces conditions communes peuvent être référencées dans les six attestations, mais chaque tâche doit conserver son propre périmètre et son propre reçu.

N'invente aucune date effective de test, capture, statistique économique ou autre observation non communiquée.

## 2. Périmètre exact des six validations

### SC4-MILAN-VALIDATION — 2 points

Le joueur confirme :

- Raccord Milanais–Crémonais correctement attribué à l'Autriche.
- Conservation des territoires vénitiens voisins.
- Conservation des territoires suisses voisins.
- Aucune anomalie dans le fonctionnement et les frontières inspectées.

### SC4-PIEDMONT-VALIDATION — 1 point

Le joueur confirme :

- `SAR` correctement représenté dans le bloc impérial.
- Neuf portions piémontaises reconnues.
- Île de Sardaigne exclue de l'emprise impériale.
- Fonctionnement des droits impériaux concernés sans anomalie.

### SC5-MINDEN-VALIDATION — 1 point

Le joueur confirme :

- Noyau de Minden sous souveraineté prussienne (`PRU`).
- Voisinage et propriétaires conservés.
- Mécanismes impériaux fonctionnels.
- Périmètre de Minden correctement distingué de Ravensberg.

### SC5-COLOGNE-VALIDATION — 1 point

Le joueur confirme :

- Duché de Westphalie et Vest correctement représentés sous `KCL`.
- Territoires voisins préservés.
- Fonctionnement des droits impériaux concernés.
- Absence de restitution abusive de toute la Westphalie à Cologne.

### SC5-MAINZ-VALIDATION — 2 points

Le joueur confirme :

- Première couche : Rheingau et Spessart.
- Deuxième couche : Bergstraße.
- Troisième couche : Tauber.
- Propriétaires et mécanismes impériaux corrects.
- Erfurt exclue de ces trois couches.

### SC6-SWABIA-CONTINUATION-VALIDATION — 1 point

Le joueur confirme :

- Fürstenberg (`SFU`) : territoires, propriétaire et capitale corrects.
- Ellwangen (`SEW`) : territoires, propriétaire et capitale corrects.
- Voisinage préservé.
- Fonctionnement en jeu sans anomalie.

Cette attestation concerne spécifiquement CONTINUATION, et non une extension rétroactive des attestations FINISH ou COMPLETION.

## 3. Enregistrement des six reçus

Après les contrôles de conservation, j'autorise explicitement l'enregistrement de :

- `SC4-MILAN-VALIDATION = PASS_RUNTIME_USER_VALIDATED`
- `SC4-PIEDMONT-VALIDATION = PASS_RUNTIME_USER_VALIDATED`
- `SC5-MINDEN-VALIDATION = PASS_RUNTIME_USER_VALIDATED`
- `SC5-COLOGNE-VALIDATION = PASS_RUNTIME_USER_VALIDATED`
- `SC5-MAINZ-VALIDATION = PASS_RUNTIME_USER_VALIDATED`
- `SC6-SWABIA-CONTINUATION-VALIDATION = PASS_RUNTIME_USER_VALIDATED`

**Créer six reçus distincts, un dans le dossier de chaque tâche.**

Chaque reçu doit comporter :

- Identifiant stable de la tâche.
- Déclaration explicite du joueur.
- Périmètre réellement inspecté.
- Confirmation de la nouvelle partie, du mois complet et de la sauvegarde/rechargement.
- Références aux rapports et corrections installées.
- Limites de l'attestation.
- Absence d'observations inventées.

Les reçus peuvent partager une référence à la même session de jeu, sans être fusionnés en une attestation générique.

Ne modifie aucun reçu historique.

## 4. Conservation et non-régression

Avant toute écriture, vérifie le workspace courant.

Pour chaque lot :

1. Retrouver les fichiers fonctionnels réellement livrés.
2. Vérifier leur conservation dans la version actuelle.
3. Contrôler les RGB, propriétaires et limites du périmètre validé.
4. Vérifier les droits et mécanismes impériaux correspondants.
5. Préserver les populations, bâtiments, unités et technologies.
6. Vérifier les modifications concurrentes éventuelles.
7. Exécuter les tests statiques et de non-régression applicables.

Conserver les résultats bruts, y compris les anciens échecs connus.

Ne pas rendre artificiellement un ancien test vert en modifiant son résultat ou son périmètre.

Une divergence réellement nouvelle et pertinente doit être documentée.

**Si une tâche échoue aux contrôles de conservation, ne force pas sa clôture.** Les autres tâches peuvent néanmoins être reçues indépendamment si leurs critères sont satisfaits.

## 5. Recalcul du suivi canonique

État de référence attendu :

- **85/235 points.**
- **36,17 %.**
- **26/81 tâches qualifiées.**

Poids des tâches reçues :

| Tâche | Points |
|---|---:|
| SC4-MILAN-VALIDATION | 2 |
| SC4-PIEDMONT-VALIDATION | 1 |
| SC5-MINDEN-VALIDATION | 1 |
| SC5-COLOGNE-VALIDATION | 1 |
| SC5-MAINZ-VALIDATION | 2 |
| SC6-SWABIA-CONTINUATION-VALIDATION | 1 |
| **Total** | **8** |

Si les six tâches sont acceptées par le validateur canonique :

- **93/235 points.**
- **39,57 %.**
- **32/81 tâches qualifiées.**

Ces résultats doivent être recalculés automatiquement à partir des statuts justifiés.

Ne pas saisir artificiellement le pourcentage ou les points.

Actualiser les fichiers canoniques concernés :

- `ROADMAP_STATE.json`
- `ROADMAP.md`
- `NEXT_ACTION.md`
- `BLOCKERS.md`
- Historique additif de progression.
- Vues générées nécessaires.

Conserver les 81 tâches, le dénominateur de 235 points et le périmètre 1.0.0.

## 6. Tâches expressément exclues

Cette attestation ne couvre PAS :

- `SC2-TESCHEN` et son sous-lot `TE-R-CORE`.
- `SC1-BERCHTESGADEN` et sa révision `BG-E-SALT-NATIVE-R1`.
- Les territoires périphériques non homologués des autres tâches BLOCKED.
- Les corrections futures des régions concernées.
- Les tests et modifications des agents WORLD, TECH, ECON ou d'autres chantiers.

Les validations Luxembourg et MAP2A sont déjà terminées : conserver leurs reçus, sans les recréer.

Ne pas attribuer de points aux tâches bloquées par assimilation aux six validations actuelles.

## 7. Prochaine étape après réception

Une fois les six tâches reçues :

1. Recalculer la liste effective des tâches toujours BLOCKED.
2. Identifier celles dont les sous-lots sont déjà testés, mais dont des critères historiques restent ouverts.
3. Distinguer les véritables corrections indispensables des réserves facultatives P2.
4. Proposer les trois clôtures les plus immédiatement réalisables, sur la base des preuves existantes.
5. Présenter également les vérifications humaines restantes pour Teschen et Berchtesgaden.

Il s'agit uniquement de préparer la suite.

**Ne commencer aucun nouveau chantier ni sous-lot.**

En particulier, ne pas relancer automatiquement `SC3-HOLSTEIN`.

## 8. Restrictions

- Aucune modification fonctionnelle du mod.
- Aucune modification du vanilla.
- Aucune écriture Git : commit, push, staging, merge, reset, rebase ou changement de branche.
- Préservation des modifications concurrentes.
- Conservation des preuves et anciens rapports.
- Aucun reçu humain pour une tâche non mentionnée.

## 9. Rapport final

Commencer impérativement par :

**SERG TERRITORIAL 1.0 — PROGRESSION : XX,XX %**

Présenter :

1. Les six reçus créés, avec chemins exacts.
2. Le statut final de chaque tâche.
3. Les contrôles de conservation effectués.
4. Les tests réussis, échecs classés et exclusions.
5. La progression avant/après.
6. Les tâches encore BLOCKED.
7. Les validations spécifiques restant ouvertes pour Teschen et Berchtesgaden.
8. Les trois prochaines tâches de clôture recommandées.

### Instruction finale

**Enregistre exclusivement les six reçus humains explicitement autorisés, après contrôle de conservation. Recalcule la progression canonique du SERG et ne commence aucune autre tâche.**