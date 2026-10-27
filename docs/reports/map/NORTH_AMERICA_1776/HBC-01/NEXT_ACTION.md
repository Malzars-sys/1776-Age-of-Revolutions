# HBC-02 — localisation des noyaux et souverainetés locales

Mise à jour du 25 octobre : le test de localisation/continuité HBC-02 a été produit dans [HBC-02/REPORT.md](../HBC-02/REPORT.md). Il ne constitue pas une implantation territoriale. La prochaine action active est désormais [HBC-03](../HBC-02/NEXT_ACTION.md) ; la liste ci-dessous conserve les exigences initiales du lot.

Autorisation de travail : demande du joueur du 25 octobre, Amérique du Nord en commençant par HBC. Aucun changement aux phases/validations du suivi WORLD ou SERG.

Contrainte obligatoire ajoutée par le joueur : appliquer [la continuité des postes avancés](../GAMEPLAY_CONSTRAINTS.md). Chaque poste doit être relié au territoire principal par un corridor étroit de provinces du même pays ; vérifier les adjacences et l'accès réel au marché avant livraison. Ce corridor de jouabilité doit rester distinct des preuves historiques de contrôle. Aucun poste isolé.

1. Partir des neuf documents R8 figés dans `REUSED_WORK.json`, du bitmap et des historiques **actuels**. Ne pas restaurer MAP1/MAP0.
2. Constituer les repères locaux indépendants autour de York, Churchill, Moose, Albany, Henley, Cumberland et Eastmain ; vérifier les sites de 1776 plutôt qu'un village moderne déplacé. Garder des repères de contrôle hors ajustement et chiffrer l'incertitude en pixels.
3. Consulter les journaux/chronologies de 1775–1776 pour Albany, Severn, Henley et Eastmain. Rupert House : rechercher la date exacte de réoccupation de 1776 ; ne pas la rétroprojeter automatiquement au 1er janvier.
4. Définir les seules emprises de poste défendables et montrer les candidats RGB en regard des sources. Si une province est trop grande, documenter le besoin d'un découpage du bitmap ; aucune taille arbitraire de fort ne résulte du rayon d'un point.
5. Cartographier les autorités autochtones en parallèle. Éviter NNV centralisé sur tout le Nunavut du jeu, IRC sur tous les Cris ou ATB sur toute terre non colonisée. Les identifiants existants ne déterminent pas les territoires historiques.
6. Établir séparément les revendications de la charte et leurs limites contestées. Ne pas utiliser une revendication de State Region entière si elle englobe des bassins extérieurs à la concession proposée.
7. Préparer un patch réversible uniquement sur les blocs HBC concernés : propriété politique, capitales/ports, POPs par culture/religion, niveaux/PM et propriétaires économiques, relations HBC/GBR/compagnie. Conserver les totaux et les travaux concurrents.
8. Vérifier les références et propriétaires uniques ; nouvelle partie, un mois et sauvegarde/rechargement pour la validation moteur. Ne pas annoncer le lot historique entier terminé à partir d'un seul noyau corrigé.

Les coordonnées GPS ne doivent pas être converties par un modèle européen non contrôlé en Amérique du Nord. Les cartes HBCA de tous les postes ne sont pas datées de 1776. La couche de connaissance géographique ne doit jamais effacer une société autochtone parce que les Européens la cartographiaient mal.
