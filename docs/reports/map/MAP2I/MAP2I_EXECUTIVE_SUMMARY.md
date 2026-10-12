# MAP-2I — Perse et frontières au 1er janvier 1776

## Résultat intégré localement

- **75 provinces RGB de `STATE_KHORASAN` passent de PER à AFH**, nouveau pays « Khorassan afsharide », capitale Machhad et dirigeant Shahrokh Afshar. **555 868 habitants** changent de subdivision politique, sans déménagement ni modification de leurs attributs.
- PER reste le même TAG. Sa capitale passe de `STATE_IRAKAJEMI` à **`STATE_FARS`, Chiraz**. Aucun bâtiment n'est déplacé pour simuler ce changement.
- Le nom dynamique devient **« Perse zand » / « Zand Persia »** pendant le règne du template de Karim Khan. Le mécanisme qajar préexistant est conservé ; le nom zand n'est plus appliqué à toute monarchie future sans condition de dirigeant. Son titre affiché devient **Vakil al-Ra‘aya**, avec le gouvernement existant, sans nouvelle loi politique.
- Le conflit existant de Bassora est conservé et passe uniquement de **`war = no` à `war = yes`**. Bassora reste IR1 au départ ; Oman reste soutien du défenseur. Aucun deuxième conflit, occupation initiale ou événement garantissant une conquête en avril n'est ajouté.
- La Perse garde **32 unités permanentes et 38 conscriptions**, les mêmes types, formation et commandant. Une infanterie permanente quitte le Khorasan pour Kerman. Quatre conscriptions sont réparties une par une entre Luristan, Kurdistan perse, Ourmia et Mazandéran. **Tabriz, Chiraz, Ispahan, Irak-Ajemi et Semnan ne reçoivent pas de recrutement supplémentaire.**
- Aucun pixel, ressource, technologie existante, PM ou recette n'est changé. Aucun lot suivant n'est commencé.

**Contrôle final : `PASS_STATIC`, 45 contrôles. Aucun test natif n'a été effectué par Codex.** Les comparatifs `persia_before.png` et `persia_after.png` sont des aperçus des véritables RGB du bitmap, pas des captures du jeu.

## Décisions historiques et limites

### Zand et Afsharides

Karim gouverne depuis Chiraz, sans prendre le titre de shah. Le Khorasan n'est pas son administration directe. Le transfert supprime cette confusion majeure tout en conservant le noyau occidental et méridional de PER. [John R. Perry, Zand Dynasty, Encyclopædia Iranica](https://www.iranicaonline.org/articles/zand-dynasty/).

**Le nouvel AFH est une agrégation régionale de gameplay**, pas la preuve que Shahrokh taxait uniformément les 75 provinces. Machhad constitue son centre dynastique ; les chefs Bayat, kurdes, arabes et les autorités de Nishapur, Sabzevar et Birjand conservaient leurs propres pouvoirs. Nader Mirza exerce une partie du pouvoir effectif à Machhad après le départ de Nasrallah en 1775 ; Shahrokh reste le souverain nominal représenté. Les villes et secteurs périphériques ne sont pas transformés en multiples nouveaux TAGs. [Perry, Afsharids, passages concernant les fils de Shahrokh et les campagnes durranies](https://www.iranicaonline.org/articles/afsharids-dynasty/), [Birjand, autorités de Qaenat](https://www.iranicaonline.org/articles/birjand-parent/birjand-town-and-district/).

AFH reçoit les douze technologies et les lois initiales de PER, mais pas ses journaux, ses personnages ou ses guerres. Religion du gouvernement chiite, culture primaire persane, couleur prune. Les habitants ne changent ni de culture ni de religion. Le drapeau est un **identifiant provisoire composé d'éléments natifs**, non un drapeau historique authentifié. Aucun régiment afsharide fictif n'est créé pour remplir la carte.

### Durrani

Timur Shah et la capitale Kaboul étaient déjà correctement initialisés : aucun changement. L'influence durranie est représentée par une **garantie d'indépendance native DUR → AFH**, sans annexion, tribut, alliance permanente ou statut de vassal. C'est une approximation révocable de protection extérieure, pas la transcription d'un traité de 1776. Sa date d'initialisation et son engagement d'un an sont des paramètres de jeu. Les interventions et le règlement matrimonial de 1770 motivent cette représentation prudente. [Afsharids, campagne d'Ahmad Shah et accord matrimonial](https://www.iranicaonline.org/articles/afsharids-dynasty/).

Herat, le Sistan, le Baloutchistan, le Pendjab et les frontières indiennes validées restent inchangés. **Gwadar n'est pas réattribué à Oman.** Les pouvoirs locaux baloutches et sistani ne sont pas certifiés comme une administration impériale uniforme : faute d'emprise nouvelle suffisamment établie, aucun transfert supplémentaire n'est forcé.

### Qajars et Caspienne

Agha Mohammad reste à la cour de Chiraz, pas à la tête d'un empire qajar de 1776. Hosayn Qoli, nommé à Damghan par Karim, dispute des districts du nord ; les chroniques diffèrent sur l'enchaînement des conquêtes et des retraits. Aucun transfert de tout Mazandéran, Gilan ou Semnan à un souverain unique n'est suffisamment défendable à la date exacte. **Les attributions restent en place comme abstraction existante, non comme certification d'un contrôle zand uniforme.** [Nobuaki Kondo, The Revolt of Hosein Qoli Khan Qajar, 1769–1777, Orient 25, 1989, pp. 124–128](https://www.jstage.jst.go.jp/article/orient1960/25/0/25_0_119/_pdf/-char/en), [Gorgan, période zand](https://www.iranicaonline.org/articles/gorgan-vii/).

### Arabistan, Golfe et Bassora

ARB reste une autorité locale vassale de PER, sans annexion directe de son Khuzestan. IR1 reste protectorat ottoman ; les systèmes ottomans sont inchangés. Bassora n'est prise historiquement qu'en avril 1776 : la guerre native représente les hostilités déjà engagées, mais ne reproduit pas un siège urbain exact et ne garantit aucune issue. Les objectifs secondaires Khuzestan/Fars sont conservés comme mécanismes préexistants, **pas présentés comme des revendications historiquement attestées**. [Iranica, Iraq v., passage sur le siège et la prise de Bassora](https://www.iranicaonline.org/articles/iraq-v-afsharids-to-the-end-of-the-qajars/).

Le RGB insulaire de Bahreïn **`xB80596`** est déjà BHN, avec **Nasr al-Madhkur** comme dirigeant initial, non Ahmad al-Khalifa. L'île et ses 6 152 habitants ne sont pas transférés. Les trois RGB côtiers également portés par BHN empêchent d'ajouter sans examen une dépendance zand à l'ensemble du TAG. Ce regroupement et l'attachement de l'île à Bushehr restent une limite explicite, sans anticiper la conquête de 1783. Bushehr demeure PER. [Joseph A. Kechichian, Bahrain iii., conquête de 1753 et reprise de 1783](https://www.iranicaonline.org/articles/bahrain-all/bahrain-iii-history-of-political-relations-with-iran/), [Bushehr, période de Karim Khan et comptoirs](https://www.iranicaonline.org/articles/bushehr-01-city/).

Le traité commercial PER–DEI est préservé. Son article préexistant visant NET au lieu du second signataire DEI est signalé dans les cas ouverts ; il n'est pas discrètement corrigé ni présenté comme nouvellement validé dans le moteur.

## Conservation économique et recrutement

Les **dix déclarations de création de bâtiments** du Khorasan, totalisant **douze niveaux écrits**, changent uniquement de subdivision territoriale. Les fichiers superposés répètent plusieurs types : ce total écrit n'est pas une observation du nombre effectivement chargé en jeu.

Les bâtiments physiques restent au Khorasan, avec mêmes types, PM, réserves et propriétaires économiques. Huit références de sièges privés PER sont déplacées vers le Kerman encore possédé : manoir, ferme, mine de cuivre, quartiers d'affaires et manufactures textiles. Les deux déclarations de centres commerciaux gardent leur propriétaire public PER conformément à la conservation demandée. **Le fonctionnement natif des participations étrangères, des sièges générés et des centres commerciaux est à tester.** Aucun niveau explicite civil n'est créé ou supprimé.

### Répartition militaire et capacité nominale après

| État | Permanentes avant → après | Conscrits avant → après | Population inchangée | Infrastructure nominale | Demande civile modélisée | Demande militaire permanente | Réserve de paix modélisée |
|---|---:|---:|---:|---:|---:|---:|---:|
| Khorasan | 1 → 0 PER | 4 → 0 PER | 555 868 | Routes inchangées | Bâtiments conservés | 0 PER | Marché AFH à vérifier |
| Kerman | 3 → 4 | 1 → 1 | 176 812 | 9,0 | 6,4 | 0,8 | +1,8 |
| Luristan | 1 → 1 | 2 → 3 | 252 538 | 5,4 | 3,6 | 0,2 | +1,6 |
| Kurdistan perse | 1 → 1 | 2 → 3 | 311 684 | 5,4 | 3,6 | 0,2 | +1,6 |
| Ourmia | 4 → 4 | 2 → 3 | 280 291 | 8,1 | 4,7 | 0,8 | +2,6 |
| Mazandéran | 3 → 3 | 6 → 7 | 797 458 | 12,0 | 6,4 | 0,6 | +5,0 |

Ces chiffres utilisent le modèle existant : routes à plein emploi, base et traits régionaux, dernière déclaration civile par type et proxy des propriétaires. **Ce ne sont pas des mesures en jeu.** La main-d'œuvre libre à 25 % est également un proxy, sans garantie de qualifications ni de recrutement. Les cinq destinataires ont une marge modélisée positive ; aucun niveau de route ni habitant n'est ajouté. Le recrutement transféré de conscription à Tabriz lors de MAP-2E reste intact, comme la suppression de son industrie alimentaire.

## Validations et fichiers

`MAP2I_VALIDATION.json` contient les 45 contrôles détaillés et les erreurs anciennes inchangées :

- Population mondiale **835 804 980**, profils complets et totaux par State Region conservés, dont cultures, religions explicites/défaut, esclaves, autres statuts et attributs déclarés.
- Liste exacte des 75 transferts, tous RGB et géométries conservés ; **44 doubles attributions préexistantes inchangées**, aucune nouvelle référence orpheline.
- Bâtiments écrits, PM, réserves et titulaires économiques conservés ; seules les références de sièges prévues diffèrent.
- Toutes unités, services, types, formations et commandants nationaux conservés ; seuls les cinq lieux de recrutement documentés changent.
- Capitales possédées et locators physiques de Chiraz et Machhad concordants avec leurs RGB ; scripts modifiés analysés et garantie fondée sur l'article natif.
- Tests existants des objectifs ottomans et de l'IA des infrastructures réussis.
- Empreintes des autres fichiers de gameplay et des rapports MAP-2A à MAP-2H inchangées. Comparaison du collaborateur limitée : seule la région Baloutchistan diffère, et la version actuelle validée est préservée.
- HEAD, index et références Git du workspace principal inchangés.

**17 fichiers de gameplay/localisation touchés** : deux définitions de pays, un nommage dynamique, deux historiques de bâtiments, un de population, l'historique des États, un historique militaire, le conflit existant de Bassora, puis nouveaux fichiers AFH de pays/personnage/gouvernement/diplomatie/traité/drapeau et deux localisations. Leur liste et leurs transformations exactes figurent dans `PLAN.json` et `INTEGRATION.patch`.

Les trois CSV livrent les RGB, les neuf profils démographiques transférés et les treize limites/cas ouverts. Leurs cellules, formules de différences et totaux ont été calculés, perturbés puis restaurés, relus et rendus avec le skill Spreadsheets. Cela valide les tableaux, **pas le moteur de Victoria 3**.

## Sauvegarde préalable et nettoyage

MAP-2H validé, finition incluse, est sauvegardé sur **`backup/1776-checkpoints`**, commit [79cde3ec143cab830a55c08ccbc0c5801d660c6a](https://github.com/Malzars-sys/1776-Age-of-Revolutions/commit/79cde3ec143cab830a55c08ccbc0c5801d660c6a). Restauration fraîche indépendante : **5 827 fichiers**, tous SHA-256 identiques, vérification Git réussie. Plus gros fichier : 43 598 540 octets ; paquet envoyé : 6 545 634 octets. Aucun LFS ni stockage payant, aucune archive complète ajoutée. [Limites GitHub vérifiées](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

Les seules suppressions sont les clones indépendants `prepared` et `restored`, puis leur paquet sortant et ses deux index, dans le dossier temporaire de sauvegarde. **5 139 994 341 octets logiques**, environ **5,14 Go**, récupérés ; le volume réellement alloué dépend du système de fichiers. Rien n'est supprimé du workspace principal ou des anciennes archives. Tous ces contenus nécessaires sont récupérables depuis le checkpoint vérifié. Reçus : `BACKUP_PREREQUISITE_VALIDATION.json` et `BACKUP_TEMP_CLEANUP.json`.

Points de restauration distincts conservés dans l'historique de la branche :

| Point | Commit |
|---|---|
| MAP-2D validé, contenant les étapes A/B/C | `cb401334bc58f2aa0747fa1a45567f3ab54a14fe` |
| MAP-2E validé, redistribution perse et retrait alimentaire de Tabriz | `49377485f78136bd4e2fc29ded8f6ae26c63ee7c` |
| MAP-2F validé, finition indienne incluse | `9383096b3bfd5a1354400878cc8052f8efe8301e` |
| MAP-2G validé, bande Ili/Ouliastai incluse | `98f0c049959abb933f7472ea326093f0632027a8` |
| MAP-2H validé, gouvernements, trêve et INDOP inclus | `79cde3ec143cab830a55c08ccbc0c5801d660c6a` |

Pas de point A/B/C séparé artificiellement reconstitué. **MAP-2I n'a pas été poussé**, et reste local jusqu'au test du joueur. Aucun commit dans le workspace principal, aucun merge, push sur main, force-push ou suppression de branche distante.

## Nouvelle partie à vérifier par le joueur

1. Au 1er janvier : PER à Chiraz, Karim Vakil et nom zand ; AFH à Machhad, Shahrokh, couleur/drapeau et gouvernement ; garantie DUR → AFH, Timur à Kaboul.
2. Caspienne/Qajars, Sistan, Kalat/Gwadar, Arabistan et Bahreïn : frontières inchangées hors Khorasan, pas d'annexion qajare anticipée.
3. Un seul conflit PER–IR1 sur Bassora déjà actif, OMA côté défenseur, Bassora initialement IR1. Les pachas et dépendances ottomanes restent en place.
4. Après un mois : emplois, marchés, budgets AFH/PER, participations étrangères et centres commerciaux ; recrutement de Kerman et des quatre destinataires de conscription. Vérifier particulièrement l'absence de déficit nouveau à Kerman.
5. Facultatif en avril : suivre la guerre de Bassora. Une issue différente de l'histoire n'est pas à elle seule un défaut, aucune victoire n'étant imposée.

Si un chargement ou une économie pose problème, transmettre le constat et les logs. Les chiffres statiques ne prétendent pas garantir l'emploi, l'accès au marché ni les budgets natifs.
