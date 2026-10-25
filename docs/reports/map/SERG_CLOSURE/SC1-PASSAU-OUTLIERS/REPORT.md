**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

# SC1-PASSAU-OUTLIERS — Obernberg installé, périphéries encore bloquées

**82/235 → 82/235, 34,89 % → 34,89 %**, 24 tâches qualifiées sur 81. Périmètre 1.0.0 et poids inchangés. Votre demande de poursuivre pendant l'attente du test autorise cette seule nouvelle tâche ; Berchtesgaden n'est pas déclaré validé. Le validateur confirme SC1-PASSAU-OUTLIERS P1 sans dépendance après calcul séparé du verrou de test.

## Recherches et choix

SOURCES.md et JURISDICTION_MATRIX.csv distinguent les frontières de 1765, les cessions de 1782, les biens médiats et la souveraineté. HLB et la commune d'Obernberg étayent l'enclave ; Seutter 1740–1760 est réellement relu, avec détail conservé. L'atlas Veit complet n'a pas été obtenu et le rendu PDF ÖAW a échoué ; seule sa partie textuelle consultée est utilisée. Aucune ancienne calibration R4, frontière moderne, carte postérieure de 1791 recopiée ou carte haute résolution non lue n'est invoquée.

B_PROPOSAL.md compare le territoire complet différé, le noyau de marché B retenu et le diagnostic seul. Le chiffre **1400** est arrondi d'après l'estimation publiée de 1441 en 1783 pour Obernberg et ses faubourgs ; ce n'est pas un recensement direct de 1776 ni toute la paroisse. Les limites de cette comparaison sont explicites.

## Installation réellement effectuée

**PS-OB-CORE IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** : PAS existant, nouveau xEDC000, quatre cellules **[[4393, 911], [4393, 912], [4394, 911], [4394, 912]]**, AUS→PAS dans STATE_AUSTRIA ; xFDA6CB **179→175**, connecté. Petit cartogramme sur la rive droite de l'Inn en amont du confluent, pas restitution cadastrale. Aucun corridor ni nouveau TAG. Les **40 cellules PAS xEDBA00** et son parent BAV sont strictement identiques. Aucun hub physique, ressource, arable ou trait déplacé.

**1400 habitants transférés** depuis le groupe south_german AUS, confession catholique par défaut, aucune profession inventée : AUS/Autriche **1638057→1636657**, sud-germaniques **1597398→1595998**. PAS/Bavière **14267 inchangés** ; PAS/Autriche **1400** ; total PAS **15667**. Monde **834926252**, cultures/confessions globales conservées.

Firmian, gouvernement, lois, drapeau et capitale nationale de Passau dans STATE_BAVARIA restent inchangés. Un effet enfant nomme seulement la portion PAS/Autriche **Obernberg am Inn** ; le point local automatique reste à observer. Aucun bâtiment spécial ou standard, industrie, fort, armée, traité ou technologie ajouté pour Obernberg. L'activité de marché et l'équilibre de la nouvelle portion ne sont pas prétendus simulés par un bonus : leurs moyens réels sont à observer en jeu.

Registre impérial **578→579**, un seul titre borné nouveau ; tous les anciens droits et l'emprise physique conservés. PAS déjà membre, sans nouvelle admission, ville libre ou dixième électeur. Sept fichiers impériaux sont régénérés après comparaison exacte du générateur avec l'état courant ; aucune restauration depuis une ancienne baseline.

## Conservation et blocages

**133/133 contrôles statiques PASS**, détails VALIDATION.json. Tests cumulatifs et contrats ciblés consignés dans TESTS.json/SCOPED_TESTS.json ; les anciennes assertions de dernière couche restent conservées et classées, jamais supprimées pour obtenir un faux résultat vert. Contrôle final de suivi et conservation dans FINAL_CHECKS.json.

Tous les anciens noyaux, attestations et travaux concurrents sont conservés. Les six fichiers de la correction mine standard BGT restent identiques ; aucun bâtiment spécial du sel n'est rétabli. BR-I-CORE et TR-I-CORE gardent leurs reçus bornés ; Brixen et Trente restent régionalement bloqués. Aucun reçu humain BGT ou Obernberg, aucune écriture Git ou vanilla.

SC1-PASSAU-OUTLIERS reste **BLOCKED P1** : Vichtenstein/Riedenburg, Abteiland/Wolfstein/Freyung, frontière de 1765 et autres juridictions non attribuées, Rent-/Waldgütleramt et possessions dispersées restent ouverts. Le voisinage d'Obernberg, historiquement bavarois hors enclaves, demeure techniquement dans AUS avec le blocage SC2-AUSTRIA/Innviertel inchangé ; sa conservation définitive n'est pas approuvée. Ce noyau B n'est pas une clôture de l'ensemble passavien. Autres blocages canoniques inchangés.

**Prochaine action : protocole commun Berchtesgaden + Obernberg**, une nouvelle partie 1776, les deux installations, un mois, sauvegarde/rechargement. Aucun moteur exécuté par l'agent. La candidate indépendante suivante est identifiée après calcul du suivi sans être commencée.

Résultats finaux exécutés : 14/14 contrats ciblés, 463/473 cumulatifs réussis, neuf assertions anciennes classées et une exclusion héritée ; aucun échec inexpliqué. 17/17 contrôles finaux PASS. Prochaine candidate SC1-REGENSBURG-DEMOGRAPHY identifiée sans commencement.
