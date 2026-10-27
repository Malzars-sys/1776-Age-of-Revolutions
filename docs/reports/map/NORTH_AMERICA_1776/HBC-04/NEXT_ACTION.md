# Prochaine action — implantation HBC avec passage loyaliste réservé

Complément esthétique du joueur : [HBC-05](../HBC-05/REPORT.md) élargit les raccords en blocs compacts (265 provinces HBC, 103 ONT), en conservant ce témoin de passage. La proposition active est `../HBC-05/COMPACT_BLOCKS.json` ; suivre [sa prochaine action](../HBC-05/NEXT_ACTION.md). Les preuves et sélections HBC-04 restent les références du raccord initial.

Proposition active : `LAND_LINK_CANDIDATE.json` et `LAND_LINKS.png` (233 provinces HBC). Réserves pour les futurs lots : `PROTECTED_PROVINCES.csv` (sélection HBC et passage ONT vers USA). Socle de conservation : `../HBC-03/CONSERVATION_BASELINE.json`, à conserver sans écrasement.

1. Réutiliser les recherches R8 et HBC-01 à HBC-04. Régler les affectations et la démographie propre des territoires retirés à HBC, sans prélever ni dupliquer sa population protégée. Préciser les positions et postes encore omis/approximatifs.
2. Préparer le patch limité aux RGB étudiés en conservant les cinq provinces du raccord HBC–ONT et un chemin ONT jusqu'à une vraie frontière USA. Ne pas couper cette chaîne par un pays décentralisé dans un autre lot. Garder les remplissages côtiers ; ne pas prolonger jusqu'à Kuujjuarapik sans nouveau motif autorisé.
3. Mettre en place les transferts de données nécessaires, avec conservation des 108 626 habitants et de tous les bâtiments, niveaux, PM, réserves et propriétaires économiques ; vérifier les références aux États partagés.
4. Relancer le contrôle HBC-03 de conservation et un calcul de chemin sur le bitmap/propriétaires après patch. Les fichiers de diagnostic ne doivent pas remplacer une ancienne version du bitmap ni les travaux concurrents.
5. Tester une nouvelle partie : HBC et ONT dans le même camp britannique contre USA, mouvements réels d'une formation HBC à travers ONT puis d'une formation ONT jusqu'au front, ressources/infrastructures et accès au marché. Comparer population/bâtiments, avancer un mois et sauvegarder/recharger. Ne pas déclarer le passage militaire validé à partir des seules cases colorées ou des types de sujets.

Aucune intégration ou validation moteur effectuée dans HBC-04. Aucun changement de statut WORLD/SERG.
