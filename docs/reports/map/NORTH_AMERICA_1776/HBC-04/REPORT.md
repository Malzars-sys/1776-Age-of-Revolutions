# HBC-04 — lien terrestre HBC, Haut-Canada et front américain

25 octobre 2026. **Proposition préparée, pas d'intégration aux fichiers du jeu.** Le joueur demande une continuité terrestre HBC → Haut-Canada (`ONT`) → Treize Colonies (`USA`), sans territoire décentralisé intercalé, pour préserver l'accès loyaliste au front américain.

## Résultat cartographique

La proposition passe de **228 à 233 provinces HBC** : cinq provinces supplémentaires de sa propriété actuelle sont conservées dans le raccord méridional au lieu d'être retirées à HBC. Aucun transfert d'un autre pays n'est nécessaire. Les remplissages côtiers précédents et la limite d'Eastmain restent inchangés.

Le Haut-Canada possède déjà une frontière terrestre avec USA. Un trajet entièrement ONT, empruntant **11 provinces**, relie le contact HBC au front américain. Ces provinces ONT sont enregistrées avec le raccord HBC dans `PROTECTED_PROVINCES.csv` pour les futures passes. La règle protège la continuité ; un itinéraire de remplacement peut être préparé si le découpage change.

Deux contacts témoins :

| Contact | Province de départ | Province d'arrivée | Bords de cellules témoins |
|---|---|---|---|
| HBC → ONT | `x5B310A` | `xC0A0C0` | `(2283,903)` → `(2283,904)` |
| ONT → USA | `x24691A` | `xE217B5` | `(2295,1054)` → `(2296,1054)` |

Ce sont des RGB de provinces, pas des identifiants historiques ou des State_ID. Les cinq provinces du raccord et les onze du passage ONT sont vérifiées sur le bitmap et les propriétés **actuels**. Le témoin complet `PIXEL_PATH_WITNESS.json` n'emprunte que HBC, puis ONT, puis une cellule frontière USA. Il reste à l'intérieur de territoires conservés, sans saut diagonal, mer, propriétaire tiers ou province infranchissable.

Le calcul vérifie aussi que les cinq postes proposés de HBC sont accessibles entre eux sous les règles statiques de franchissement utilisées. Il ne confond pas la présence de frontières à deux endroits avec une continuité réelle dans le même territoire accessible.

## Préservation des modifications concurrentes

Le bitmap global a changé depuis HBC-02 : ancienne empreinte `3ee41b5124b4597145bd22bb00b0ece04983c27eafb38b7919533fe701e87da8`, actuelle `c91db6d223e61e6b00ab3a99cf5ed321a68c9cc97e38a0065c110b81a04aff4c`. L'ancienne carte n'a pas été restaurée.

`INPUT_REVALIDATION.json` établit : mêmes 2 246 RGB HBC, même surface de chaque province HBC, zéro cellule changée dans l'empreinte HBC par rapport au diagnostic antérieur en résolution 1:1, mêmes RGB sous les cinq repères et mêmes propriétaires/State_ID pour la sélection précédente. Les chemins sont recalculés sur le raster courant. Cela ne prétend pas certifier les frontières historiques ou chaque ancienne limite interne par géoréférencement ; les preuves de présence historique gardent leurs limites déjà documentées.

## Population, bâtiments et accès militaire

La sélection précédente est intégralement conservée. Le socle de **108 626 habitants** et toutes les commandes économiques protégées dans HBC-03 restent intacts ; leur vérification inclut niveaux, PM, propriétaires et existence des portions HBC portant les données. Le plan démographique et économique HBC-03 reste applicable à cette proposition élargie.

La configuration diplomatique consultée établit HBC comme compagnie à charte de GBR et ONT comme colonie de GBR. Les types natifs effectifs `subject_type_chartered_company` et `subject_type_colony` comportent `join_overlord_wars = yes`. La guerre de départ est `USA` contre `GBR`, de type indépendance. Les références et résultats statiques sont conservés dans `DIPLOMACY_STATIC_CHECK.json`.

Ces déclarations sont compatibles avec la participation du camp britannique ; elles ne sont pas une observation des camps effectivement chargés ni un test de déplacement. Aucun pacte de passage militaire supplémentaire n'a été créé. À l'intégration, vérifier que HBC et ONT sont bien dans le camp loyaliste, puis déplacer une formation HBC à travers ONT jusqu'au front USA, ainsi qu'une formation ONT à ce front. Un accès bloqué par neutralité doit être corrigé même si le tracé physique est valide.

## Contrôles

Les seize contrôles de `VALIDATION.json` passent : conservation économique/démographique, validité des portions d'État HBC, revalidation locale des entrées, maintien de la sélection précédente, propriétaires corrects, deux frontières terrestres, passage ONT cohérent, chaîne exacte des pays, absence de pas diagonal/mer/liaison interdite, connexion des postes, absence de province infranchissable sur le témoin et fichiers du jeu inchangés pendant le calcul.

Les six tests de `tools/test_hbc04_land_links.py` ciblent les erreurs de géométrie : contact diagonal, frontière native interdite, territoire intermédiaire interdit, retour involontaire à la ligne suivante du bitmap, enclave ONT distincte du front USA et orientation des contacts. Résultats dans `TESTS.json`.

Le registre d'adjacences natif est consulté en lecture seule : les traversées de mer, liaisons infranchissables et liaisons conditionnelles non démontrées sont exclues du calcul terrestre. Les provinces infranchissables des définitions actuelles sont également exclues. Les pixels de petites îles appartenant à une province conservée ne sont pas maquillés en parcours terrestre : seul le témoin continu explicitement enregistré sert de preuve du passage.

Aucune validation moteur, aucun commit, aucune modification de propriété, de POPs, de bâtiments, de guerre ou de bitmap. Les suivis WORLD/SERG ne sont pas modifiés par ce travail autorisé directement sur l'Amérique du Nord.

## Recherche locale

Un appel local ColGrep terminé avec code 0 pour localiser les dépendances militaires. La piste `common/scripted_effects/1776_join_ongoing_wars.txt:3–48` a été vérifiée dans le fichier actuel. Elle concerne surtout les interventions générales ; elle n'établit pas les camps HBC/ONT au chargement. Les autres pistes incluaient un ancien déclencheur dans une copie de rapport et des fichiers de bâtiments déjà connus : ils n'ont pas été utilisés comme configuration courante. Les identifiants précis de sujets/guerre ont ensuite été vérifiés directement. Durée d'inférence complète et tokens non instrumentés, aucune économie de quota exacte affirmée, aucun nouvel index reconstruit.
