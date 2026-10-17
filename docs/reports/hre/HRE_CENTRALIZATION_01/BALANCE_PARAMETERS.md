# Paramètres courants — retour utilisateur R1

Source unique de configuration : dictionnaire CONFIG dans `tools/hre_centralization_01.py`, puis compilation impériale.

| Paramètre | État impérial | Électorat impérial |
|---|---:|---:|
| income_transfer natif |0.15|0.10|
| coût de pacte en influence |0|0|
| niveau d’autonomie |1|1|

Ces pourcentages sont un équilibrage provisoire, pas une reconstitution des impôts impériaux de1776. Le paiement est explicitement calculé sur le second pays et versé au premier. Aucun prélèvement additionnel par script, aucun événement de taxe ni modificateur de revenu ajouté.

Taux relevés à la demande du joueur : 15 % pour les États impériaux et 10 % pour les électorats. Les anciens comptes rendus et baselines restent des photographies de leur étape ; le correctif courant est documenté dans FEEDBACK_R1/REPORT.md. Le Lien impérial reste à 0 %.

Le coût0 évite de rendre des dizaines de sujets incompatibles avec le budget diplomatique. Il n’affecte aucun coût global des sujets vanilla. Il pourra être relevé dans CONFIG après mesure en jeu.

Les interactions natives d’augmentation/réduction des versements peuvent affecter les paiements réels : vérifier leur effet séparément. Le maintien d’un gouvernement et d’un dirigeant distinct ne signifie pas une immunité contre toutes les autres interactions natives.

La compilation injecte les taux CONFIG dans les descriptions françaises/anglaises. Un test temporaire à12,5% vérifie cette propagation sans écrire ce taux dans le mod. Pas de formule mensuelle parallèle.
