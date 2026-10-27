# SC2-TESCHEN — voie de clôture proposée

26 octobre 2026. Seule tâche BLOCKED traitée après l’audit des huit installations. **Aucune nouvelle correction fonctionnelle, aucun nouveau sous-lot, aucun point.**

## Ce qui est déjà fait

- MAP2A : souveraineté AUS et rattachement physique de `x9061E0` à `STATE_WEST_GALICIA`, pool technique de 135 753 habitants, bâtiments et recrutement déjà redistribués.
- SC2-AUSTRIAN-SILESIA : décision de conservation B approuvée, mais Teschen était explicitement exclu de sa clôture ; cet accord n’est pas étendu.
- TE-R-CORE : 179 cellules existantes inscrites au registre, 580 → 581 titres, avec exclusion des autres portions galiciennes. Aucun territoire à recréer.
- Mission actuelle : résultat vérifié en jeu déclaré par le joueur. L’[observation enregistrée](TESCHEN_USER_OBSERVATION.json) ne fournit ni nouvelle partie datée, ni durée, ni sauvegarde/rechargement, ni liste complète de contrôles.

Les sources d’implémentation et historiques restent dans [MAP2A](../../MAP2A/MAP2A_EXECUTIVE_SUMMARY.md) et [SC2-TESCHEN](../SC2-TESCHEN/SOURCES.md). Les preuves et la version livrée restent intactes.

## Examen des anciens blocages

La tâche particulière demande d’établir la portion impériale des 179 cellules sans inclure toute la Galicie. Cette correction est installée. Une exactitude cadastrale village par village n’est pas une raison suffisante de rouvrir les cellules ni d’imposer une nouvelle souveraineté.

La réserve démographique est différente : 112 850 habitants sont rapportés pour le ressort historique régional de 1770–1771, contre 135 753 dans le pool technique. L’écart arithmétique de 22 903 ne mesure pas une erreur démontrée de 1776 : date et correspondance géographique ne sont pas réconciliées. Il serait aussi injustifié de remplacer automatiquement le pool que de le certifier comme recensement exact. Les juridictions de domaines ne sont pas toutes la propriété personnelle du couple ducal.

Le dossier ne classe donc pas toutes ces réserves en P2. Il sépare la précision cadastrale facultative, le défaut de registre déjà corrigé et l’arbitrage réel sur la portée d’une clôture B.

## Décision concrète soumise au joueur

La [proposition structurée](TESCHEN_PROPOSED_CLOSURE_DECISION.json) conserve les installations actuelles, sans correction supplémentaire démontrée. Elle demande de trancher explicitement si cette représentation B, avec son allocation technique conservée et ses limites documentées, suffit à la tâche bornée SC2-TESCHEN, ou si un rapprochement territorial/démographique supplémentaire est requis avant clôture.

Cette proposition est **non approuvée**. L’autorisation générale de travailler et la vérification visuelle ne sont pas transformées en approbation historique de cette option. Les obligations antérieures restent enregistrées jusqu’à décision ; elles ne sont pas effacées pour gagner deux points.

La procédure sans changement supplémentaire ne permet pas d’utiliser `NOT_APPLICABLE_VERIFIED` pour éviter le test du correctif fonctionnel TE-R-CORE déjà livré. Si la portée B est acceptée et le protocole restant réellement confirmé, la clôture pourra être réexaminée avec le validateur. **Aujourd’hui : BLOCKED P1 et zéro point.**

## Contrôles manquants

Pour TE-R-CORE : confirmer la nouvelle partie de 1776 sur la version livrée, un mois et la sauvegarde/rechargement. Ne pas refaire un contrôle déjà effectué : le préciser dans le retour. La validation globale des quatre corrections MAP2A reste une ligne distincte du [protocole groupé](PLAYER_TEST_PROTOCOL_GROUPED.md).

La prochaine réconciliation recommandée après cette revue est SC2-LUXEMBOURG-VALIDATION : résoudre l’objectif administratif attribué à un LUX sans État initial et la portée retenue pour BEO/Wallonie, en coordination avec BUILD/ECON. Aucune correction de ce dossier n’est faite ici. SC3-HOLSTEIN reste suspendu dans cette campagne.
