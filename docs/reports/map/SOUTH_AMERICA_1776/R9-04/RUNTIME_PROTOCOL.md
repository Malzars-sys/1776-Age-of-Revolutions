# R9-04 — Protocole joueur, nouvelle partie 1776

Version : SHA dans PATCH.json et CURRENT_RUNTIME_MANIFEST.json. Statut attendu jusqu'au retour joueur : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Un contrôle statique n'est pas une validation moteur.

1. Créer une **nouvelle partie au 1er janvier 1776**, avec le mod courant. Une sauvegarde antérieure conserve ses anciennes provinces et populations ; ne pas l'utiliser pour certifier cette installation.
2. Vérifier le maintien espagnol des forts de la frontière, Valdivia/Corral, Maullín/Calbuco et Chiloé ; comparer avec `R9_04_AVANT_APRES.png`. Vérifier les 9 cellules Mapuche et les 7 cellules huilliches, sans enclave vide ou contrôle espagnol continu par Osorno.
3. Vérifier la présence de **Huilliches du Futahuillimapu**, son caractère décentralisé, son drapeau lisible et ses deux localisations sans clé brute. Son territoire initial doit contenir la portion d'Osorno, avec 2 246 habitants de la cohorte transférée. Vérifier les 33 682 habitants transférés vers PAT dans LOS_RIOS ; les comptes affichés après démarrage peuvent évoluer, donc relever la date exacte.
4. Vérifier que les anciens bâtiments de LOS_RIOS restent espagnols et que le port ajouté dans ARAUCANIA est de niveau 1 avec ses PM commerciaux. Examiner emploi, marchandises maritimes, liaisons, convois et accès au marché **séparément pour Valdivia et Chiloé**. La simple présence du port ne certifie pas leur ravitaillement.
5. Laisser tourner quelques mois en relevant les dates réellement jouées : évolution de l'emploi, ravitaillement, prix, faim et effectifs. En cas de famine, conserver les informations de marché et les captures pour distinguer manque de ressources, transport, emploi et pauvreté ; ne pas conclure sans diagnostic que les populations ont disparu du scénario.
6. Vérifier les témoins : Sacramento est toujours la portion BRZ de l'Uruguay partagé, corrections CENTRAL et autres pays inchangés ; la Patagonie orientale ne doit pas être colonisée dès le départ par une nouvelle implantation espagnole de 1779.
7. Sauvegarder/recharger et vérifier la persistance des propriétaires et l'absence de crash. Conserver les logs avec leurs dates. Relever séparément les erreurs déjà présentes avant ce lot et les éventuelles régressions R9-04.

Le reçu humain doit préciser version, date du scénario, observations et durée réellement simulée. Aucun résultat positif n'est prérempli. Les noms de hubs modernes, les limites ethniques fines et les réserves historiques de SOURCES.md ne sont pas certifiés par ces essais.
