# Définition des statuts

| Statut | Paiement hebdomadaire initial | Diplomatie propre | Guerres du suzerain | Annexion initiale |
|---|---:|---|---|---|
| Lien impérial |0%|Autonome|Pas d’obligation native générale|Bloquée|
| État impérial |10%|Non autonome|Règle native des sujets dépendants|Bloquée|
| Électorat impérial |5%|Non autonome|Règle native des sujets dépendants|Interdite sans exception implémentée|

Les nouvelles définitions sont des types natifs, avec désir de liberté et possibilités de contestation relevant des règles natives et du coup impérial de sécession conservé. Aucun paiement par événement, aucune annexion lors d’une formation de pays, aucun dirigeant partagé, aucune loi imposée automatiquement. Les lois et gouvernements ne sont pas figés contre toute interaction future du jeu.

Le pacte générique Lien impérial historique, les titres territoriaux du registre et les appartenances au bloc restent des mécanismes distincts. Le pays entier n’est jamais converti du seul fait d’un titre territorial.

Le statut électoral effectif est le trigger existant `aor1776_hre_elector`, augmenté de deux variables de privilège accordé/révoqué. Les listes initiales sont le défaut1776, pas une limite permanente. Les effets grant/revoke exigent une autorisation constitutionnelle consommée et interdisent la mutation pendant un scrutin. Ils appellent `aor1776_hre_sync_imperial_subject_status` seulement sur un sujet déjà centralisé. Le désir de liberté est mémorisé puis une restauration différentielle est demandée ; son résultat réel reste à tester.

Toute autre future modification du droit électoral devra appeler ce même effet ; une modification de loi extérieure qui ne l’appelle pas n’est pas synchronisée magiquement.
