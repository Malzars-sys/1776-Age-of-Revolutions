# HRE-CENTRALIZATION-01 — retour utilisateur R1

## Corrections installées

- Une seule description FR/EN : `concept_aor1776_hre_protectorate_desc`. Les descriptions du pacte constitutionnel initial, de la fiche diplomatique, du type de sujet et de l’ancien alias la réutilisent. Les mots liés ouvrent des concepts réels du jeu.
- Réduction : Lien impérial → État impérial, ou Électorat impérial si `aor1776_hre_elector` reconnaît la dignité électorale. Le choix est explicite dans l’effet, pas déduit de l’ordre des deux types natifs.
- Augmentation : État impérial / Électorat impérial → Lien impérial. Cela conserve le pays et sa relation de sujet, sans indépendance, annexion ou suppression des privilèges électoraux. Le même traitement est prévu pour l’action du suzerain et la demande acceptée du sujet.
- Paiement natif hebdomadaire : État impérial15 %, Électorat impérial10 %, Lien impérial0 %. Un paiement par pacte, du sujet au suzerain, sur les revenus du sujet. Les descriptions et le paramétrage utilisent les mêmes taux.
- Infobulles de la liste : chaîne impériale distincte de l’annexion et de l’indépendance ; repli natif inchangé pour les autres types de sujets. Les États/électorats restent protégés contre une nouvelle diminution conduisant à l’annexion.

## Portée et sécurité

Les transitions individuelles concernent les pactes de sujets natifs impériaux. Les liens constitutionnels virtuels présents en1776 ne deviennent pas tous des sujets par cette correction. Les boutons de centralisation générale restent verrouillés et le prototype de succession isolé reste à valider. Aucun changement à ses fichiers ou à la procédure de transfert électif.

La diminution native d’un Lien est réservée à l’empereur, hors élection, pour un pays déjà admissible à la dépendance impériale. Les pays mixtes demeurent exclus du filtre conservateur existant. Les conditions natives de désir de liberté, délai et conflit sont conservées. Les effets d’augmentation conservent les règles natives d’approbation et de délai. Les unions personnelles et les types de sujets non impériaux gardent leurs effets natifs exacts, vérifiés par normalisation des branches.

Aucun nouveau type « province impériale » n’est créé. « État impérial » et « Électorat impérial » sont les deux noms retenus.

## Vérifications

151/151 contrôles statiques. 44 tests réussis (contrats R1, centralisation courante et préservation Anhalt). Le compilateur complet reproduit 71/71 fichiers installés. Les tests de contrat ont été mis à jour pour la nouvelle règle explicite de retour vers le Lien, sans modifier les anciennes attestations ni les baselines territoriales.

Les14 fichiers fonctionnels modifiés figurent dans VALIDATION.json. Aucun changement aux historiques, frontières, populations, bâtiments, PM, propriétés économiques, unités, gouvernements, lois, souverains ou icônes. Population mondiale835801255. Les44 doublons RGB et12 références invalides préexistants restent identiques. Les anciens échecs de snapshots MAP déjà documentés ne sont pas requalifiés en réussites et ne sont pas réparés par cette passe.

**STATIC_PASS_RUNTIME_PENDING. Aucun test moteur exécuté.** Les captures du joueur sont des preuves des problèmes d’affichage précédents, pas une validation de ces nouveaux effets.

## À vérifier en jeu après redémarrage

1. Comparer la description du Lien dans la liste et dans un pacte diplomatique : même texte, mêmes liens d’infobulle.
2. Vérifier la flèche de diminution du Lien et la flèche d’augmentation des deux types centralisés. Pas d’annonce d’annexion ou d’indépendance dans cette chaîne.
3. Dans une partie de test avec de vrais sujets natifs impériaux déjà installés, diminuer un Lien ordinaire puis un Lien électoral : destination correcte, aucun territoire ni pays disparu, vote conservé.
4. Augmenter l’autonomie de chacun par le suzerain, puis tester une demande acceptée par le sujet : retour au Lien sous le même suzerain, privilège électoral conservé, pas d’indépendance.
5. Contrôler les contributions après une échéance hebdomadaire :15 % /10 % /0 %. Les revenus réels et les arrondis dépendent du moteur.
6. Tester un sujet vanilla : descriptions et effets de ses transitions restent natifs. Ne pas activer une centralisation de tout l’Empire pour ce contrôle.

Aucun commit, merge, push, changement de branche ou écriture de l’index. Aucune écriture dans l’installation du jeu. MAP-2S et ses conclusions cartographiques ne sont pas modifiés.

Recherche locale : un appel ColGrep-Agent abouti a retrouvé le verrou d’autonomie et la description du concept, lignes vérifiées. Les clés exactes et le comportement d’interface ont ensuite été contrôlés dans les fichiers installés du jeu. Aucune mesure exacte d’économie de quota.
