# Contrôle groupé ultérieur — EUROPE-LAWS-R1

Ce protocole est préparé, non exécuté. Relancer le jeu avec le mod de travail, nouvelle partie au 1er janvier 1776. La passe n'a pas été copiée dans Steam Build. Le changement de pays par console utilise `tag TAG` ; conserver le jeu en pause pour les contrôles initiaux.

1. `tag GBR`, puis FRA, POR, BEO, PRU, PAP, SWE, DENNOR et MON : citoyenneté **Sujétion**. Vérifier que leurs groupes de lois économiques, militaires et religieux restent ceux d'avant. MON conserve Sava et sa théocratie ; PRU conserve son amendement d'austérité militaire.
2. Échantillon allemand : `tag ANH` (ancienne suprématie nationale), `tag ANS` (citoyenneté auparavant non explicitée), `tag EIC` (théocratie auparavant non explicitée), puis AUS et BGT (sujétion préexistante). Vérifier la même loi de citoyenneté, les titulatures et les relations impériales.
3. `tag SWI` : **Oligarchie** à la place du Suffrage censitaire. La république parlementaire et la citoyenneté restent volontairement dans leur état antérieur ; elles ne sont pas présentées comme historiquement finalisées.
4. `tag TUR` : vérifier spécialement la présence effective de **Censure**. Si la demande n'a pas été appliquée, relever la loi active et l'erreur éventuelle : le gate `periodical_print_networks` manque et reste explicitement connu. Ne pas rechercher toute une ère pour dissimuler ce résultat.
5. Témoins réservés : `tag SPA` (pas de variante russe, pas de nouveau nationalisme), `tag PLC` (roi et amendements électif/liberum veto conservés), NET, VEN, GEN et LUC (aucune conversion monarchique forcée), HAM et NUR (montages républicains conservés).
6. Laisser passer quelques jours, sauvegarder et recharger ; vérifier que les lois explicitement installées ne reviennent pas au défaut. Consulter le journal d'erreurs frais sur le nom du nouvel historique, `activate_law` et les pays testés.

Le tableau exhaustif des cibles, sans obligation de visiter les 70 pays à la main, est dans `COUNTRY_MATRIX.csv`. Ne pas utiliser la commande de console de promulgation pour valider la bonne initialisation : elle remplacerait précisément ce qu'on cherche à observer.
