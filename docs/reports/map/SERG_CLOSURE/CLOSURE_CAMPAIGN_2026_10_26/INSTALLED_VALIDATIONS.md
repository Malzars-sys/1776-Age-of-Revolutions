# Huit installations — audit de réception du 26 octobre 2026

**11 points possibles, zéro point nouveau justifié.** Les contrôles sont statiques ; aucun test moteur ou reçu humain nouveau. Les sources exactes et empreintes sont dans [SOURCE_INDEX.json](SOURCE_INDEX.json).

| Tâche | Points | Présence statique / évolution | Portée des reçus retrouvés | Contrôles humains manquants |
| --- | --- | --- | --- | --- |
| SC2-MAP2A-VALIDATION | 2 | 8/8 contrôles ; noyau conservé | Anciennes missions A–E/A–H testés en jeu ; aucun mois ou détail individuel MAP2A ajouté. | périmètre des quatre RGB en nouvelle partie 1776 ; bâtiments et recrutement associés ; un mois complet sur ce périmètre |
| SC2-LUXEMBOURG-VALIDATION | 1 | 4/6 contrôles ; deux anciens blocs administratifs absents après recalibrage BUILD ; autres transferts conservés | Intégration approuvée et inspection belge ancienne ; pas de reçu spécifique complet. | Luxembourg BEO et LUX absent en nouvelle partie 1776 ; administration et formation de trois unités ; un mois sur ce périmètre |
| SC4-MILAN-VALIDATION | 2 | 3/3 contrôles ; noyau conservé | Reçu ancien Belgique/Franconie/Rhénanie, pas MILAN_CREMONESE. | raccord AUS de 64 cellules et voisins VEN/SWI ; nouvelle partie et un mois |
| SC4-PIEDMONT-VALIDATION | 1 | 10/10 contrôles ; noyau conservé | Autorisation d’inclusion précise, distincte d’un test attesté. | SAR membre, neuf RGB piémontais reconnus et Sardaigne exclue ; nouvelle partie et un mois |
| SC5-MINDEN-VALIDATION | 1 | 9/9 contrôles ; noyau conservé | Exclusion explicite de Minden dans RUNTIME_USER_VALIDATION.json. | propriétaires, noyaux et mécanismes impériaux du lot nommé ; nouvelle partie et un mois |
| SC5-COLOGNE-VALIDATION | 1 | 18/18 contrôles ; noyau conservé | Aucun reçu nommant ce lot ultérieur. | propriétaires, noyaux et mécanismes impériaux du lot nommé ; nouvelle partie et un mois |
| SC5-MAINZ-VALIDATION | 2 | 48/48 contrôles ; noyau conservé | Aucun reçu couvrant explicitement les trois couches. | propriétaires, noyaux et mécanismes impériaux du lot nommé ; nouvelle partie et un mois |
| SC6-SWABIA-CONTINUATION-VALIDATION | 1 | 33/33 contrôles ; noyau conservé | SWABIA_FINISH exclut la validation automatique de la continuation. | propriétaires, noyaux et mécanismes impériaux du lot nommé ; nouvelle partie et un mois |

Les deux écarts Luxembourg restent des écarts réels à la conservation littérale des anciennes déclarations, expliqués par [le recalibrage ultérieur](LUXEMBOURG_SCOPE_RECONCILIATION.json). Ils ne prouvent pas un crash et ne sont pas restaurés automatiquement. La clôture de cette ligne demande de réconcilier cette nouvelle portée administrative, puis de tester la version réellement retenue.

Les approbations anciennes ne sont ni supprimées ni déclassées. Leurs parties effectivement attestées restent utilisables ; les détails absents ne sont pas inventés. Pour MAP2A, le contrôle Teschen récent ne valide pas automatiquement les trois autres corrections ni le recrutement. Pour la Souabe, FINISH et COMPLETION ne se substituent pas à CONTINUATION.

Le [protocole groupé](PLAYER_TEST_PROTOCOL_GROUPED.md) complète uniquement les lacunes ; il ne redécoupe aucun territoire.

Après examen de la matrice runtime finale, SC2-LUXEMBOURG-VALIDATION est reclassée BLOCKED P1 : un objectif administratif reste attribué à LUX sans État initial. Les sept autres tâches restent IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Ce conflit ne doit pas bloquer leurs tests indépendants.
