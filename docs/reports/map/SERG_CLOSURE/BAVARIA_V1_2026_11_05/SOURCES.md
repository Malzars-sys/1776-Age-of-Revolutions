# Bavière V1 — sources et décision d'Innbaiern

Situation de référence : 1er janvier 1776. Aucun ancien profil de géoréférencement n'est modifié ou recalé.

## Souveraineté

Le [traité de Teschen, transcription de l'original du 13 mai 1779](https://www.ooegeschichte.at/ausstellungen/mit-brief-und-siegel/friede-von-teschen), art. IV, énumère les offices bavarois cédés à l'Autriche. La cession est postérieure au scénario. Une copie courante de la page est dans EVIDENCE/TESCHEN_PAGE.html ; ce traité ne lance pas la tâche distincte SC2-TESCHEN.

La carte Seutter de Haute-Autriche [1740–1760], [UB Bern, Ryhiner 4604:7](https://doi.org/10.3931/e-rara-121854), avait été réellement acquise dans SC2-AUSTRIA. Elle est relue ici : le secteur Braunau/Ried/Schärding reste à l'ouest de la frontière autrichienne, entre Inn/Salzach et Hausruck. Les fichiers historiques sont conservés ; une demande de meilleure définition a répondu HTTP 500, consignée sans relance répétitive.

Une [carte de l'Innviertel reproduite par le Forum OÖ Geschichte](https://www.ooegeschichte.at/media/bilder/allgemein/themen/religionundkirche/kirchengeschichte_dal/dal/2503/image-thumb__2503__media-gallery/dal_karte_innviertel.20cf9718.jpg) est nouvellement obtenue et examinée. Son titre représente le territoire sous l'Autriche : elle sert à comparer l'enveloppe acquise, et non à attribuer l'Autriche en 1776. La date exacte et l'auteur de cette reproduction ne sont pas certifiés à partir du petit cartouche. Elle distingue l'ensemble bordé par Inn/Salzach, Hausruck et les exceptions passauviennes ; aucun détail cadastral n'en est extrait.

## Choix de représentation B

L'ancien blocage portait notamment sur le transfert indistinct des 179 cellules originelles et sur un recalage R4 non homologué. Cette passe ne reprend pas ce recalage. Depuis, quatre cellules ont été séparées et validées sous Passau pour Obernberg. Elles sont explicitement préservées.

La solution V1 est une généralisation politique régionale : le résidu natif xFDA6CB, 175 cellules continues, devient BAV ; les dix autres provinces AUS de STATE_AUSTRIA restent autrichiennes, dont les repères Linz/Freistadt et le Hausruck oriental agrégé. Le noyau Obernberg PAS de quatre cellules, les quarante cellules PAS originales, le noyau SLZ de douze cellules et toute autre province sont immuables. La province est située sur la rive orientale de l'Inn natif, en amont du confluent documenté vers [4400,902], à l'ouest des autres provinces autrichiennes. Le réseau fluvial et les provinces sont comparés dans INNVIERTEL_NATIVE.png.

C'est un cartogramme politique B de l'Innbaiern, pas la découverte d'une équivalence cadastrale entre un RGB vanilla et les cinq ressorts historiques. Les parties de Salzbourg encore agrégées dans BAV/AUS/Tyrol, les limites de Vichtenstein, Neuburg/Wernstein et les petites juridictions intercalées ne sont pas certifiées ni clôturées. Aucune portion native PAS/SLZ n'est annexée. Les diagnostics R5/Miller sont conservés seulement comme avertissements : leurs points urbains ne sont pas utilisés pour déplacer un noyau protégé.

Ce choix régional, appuyé par les cartes et les voisins et autorisé pour une approximation B, remplace dans ce périmètre la recherche d'une précision urbaine non accessible. Il ne transforme pas les anciennes conclusions d'audit en fausses validations et ne clôt pas toute SC2-AUSTRIA.

## Population

L'[Österreichische Akademie der Wissenschaften, Historisches Ortslexikon Oberösterreich, partie 1](https://www.oeaw.ac.at/fileadmin/subsites/Institute/VID/PDF/Publications/diverse_Publications/Historisches_Ortslexikon/Ortslexikon_Oberoesterreich_Teil_1.pdf), page PDF 4, rubrique Innviertel, donne 106 898 habitants pour le relevé bavarois 1771/81. Les cinq ressorts cités totalisent ce chiffre : Braunau 34 084, Friedburg 7 735, Mattighofen 2 016, Ried 21 421, Schärding 41 642. C'est une période composite, pas un recensement exactement daté de 1776.

L'initialisation retenue est 106 900 habitants pour le proxy politique régional, arrondi de deux habitants. La fourchette de travail 100 000–116 000 exprime une sensibilité de scénario, pas un intervalle statistique. Le même répertoire situe les valeurs ultérieures autour de 115 700 ; ces chiffres ultérieurs ne sont pas rétroprojetés comme recensement de janvier 1776. La source distingue Obernberg/Vichtenstein de l'acquisition bavaroise.

Ces habitants sont prélevés sur le groupe south_german existant de la portion AUS/Autriche : 1 595 998 → 1 489 098. La nouvelle portion BAV reçoit 106 900, profil catholique par défaut de cette culture. C'est une hypothèse de groupe dominant, pas une mesure historique des minorités. Les autres profils autrichiens et les populations de Passau/Salzbourg sont conservés. Aucun habitant n'est créé dans un pays sans rapport ; le total mondial reste inchangé comme conséquence de ce transfert, non comme obligation de compensation artificielle. Aucun nouveau recensement national bavarois n'est proclamé.

## Dépendances

BAV existe déjà avec son profil technologique, ses lois et son économie : aucun nouveau TAG, recette, bâtiment, niveau militaire ou PM n'est ajouté. Les ressources, capacités agraires et repères physiques des régions économiques restent identiques. La portion reçoit le nom historique Innbaiern par un effet limité à BAV, STATE_AUSTRIA et la possession du RGB concerné. Le fonctionnement du marché, de la subsistance et des moyens administratifs de cette nouvelle portion reste à contrôler en jeu.
