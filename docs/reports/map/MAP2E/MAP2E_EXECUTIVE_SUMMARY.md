# MAP-2E — Caucase au 1er janvier 1776

## Résultat intégré localement

**45 provinces RGB réattribuées et neuf doubles attributions supprimées.** Aucun redessin du bitmap, aucune nouvelle province et aucune modification des contours des State Regions. **32 contrôles statiques réussis. Le test de chargement natif reste à effectuer.**

Le lot distingue désormais les autorités géorgiennes et les principaux khanats orientaux de l'administration impériale directe. La population mondiale reste exactement **835 804 980 habitants**. Le total des neuf régions étudiées reste **3 749 856 habitants**.

Sept TAGs régionaux sont ajoutés : `IMR` Iméréthie, `KRB` Karabakh, `GJA` Gandja, `SHK` Chaki, `NAK` Nakhitchevan, `TAL` Talysh et `SRV` Chirvan. Les TAGs existants `ARM`, `AZB` et `ABK` sont réutilisés pour Erevan, Kouba et Abkhazie. `GEO` conserve la Kartl-Kakhétie et Héraclius II.

## Changements territoriaux

| Région | Changement | RGB concernés |
| --- | --- | --- |
| Géorgie occidentale | GEO → ABK, 2 provinces ; GEO → IMR, 7 provinces | Détail province par province dans le manifeste territorial |
| Akhaltsikhé / Samtskhé | GEO → TUR, 3 provinces | `xC27075`, `x74A861`, `xC0CF80` |
| Erevan / Nakhitchevan | PER → ARM, 5 provinces ; PER → NAK, 2 provinces | Les sept provinces de `STATE_ARMENIA` auparavant persanes |
| Gandja / Chaki / Karabakh | PER → GJA, 3 ; PER → SHK, 4 ; PER → KRB, 4 | Les onze provinces persanes de `STATE_ELIZAVETPOL` |
| Kouba / Chirvan / Talysh | PER → AZB, 7 ; PER → SRV, 3 ; PER → TAL, 1 | Les onze provinces persanes de `STATE_AZERBAIJAN` |
| Derbent / Samur | CAUC → AZB, 2 provinces | `xDA5ABE`, `x9F1D8F` |
| Kizliar | CAUC → RUS, 1 province | `x01D041` |
| Mozdok | CAUC → RUS, 1 province | `x891792` |
| Kouban | Suppression de la revendication CRI concurrente ; CIR conservé | `xBCF376` |
| Caucase septentrional | Suppression de huit scopes CAUC concurrents ; CHC/CIR conservés | `x019041`, `xDA8EF4`, `x83F33B`, `x2790A8`, `x56FD87`, `x668A47`, `xC05001`, `x23F98B` |

Les monts caucasiens ne sont pas annexés uniformément à la Russie. Aucun protectorat géorgien de 1783 ni annexion de 1801 n'est anticipé. Les positions russes du présent lot sont les deux districts des forts septentrionaux.

Quatre références de hubs sont alignées sur leurs locators physiques sans déplacement de ces derniers : Telavi et Bolnisi, Armavir, Blagodarny. Les noms de pays et subdivisions concernés disposent de localisations françaises et anglaises et d'un effet ciblé de nommage au démarrage.

## Populations : redistribution, aucun ajout

Chaque groupe initial est réparti par surface de terre des RGB, avec arrondi entier au plus fort reste. Cette allocation technique **n'est pas un recensement historique**. Tous les champs démographiques sont conservés : culture, religion explicite ou par défaut, statut libre/esclave et autres attributs existants.

| Région | Répartition avant | Répartition après |
| --- | --- | --- |
| Greater Caucasus | GEO 1 162 712 | GEO 474 455 ; IMR 435 680 ; ABK 131 674 ; TUR 120 903 |
| Armenia | PER 196 443 | ARM 127 100 ; NAK 69 343 |
| Elizavetpol | PER 202 523 | GJA 63 417 ; SHK 58 312 ; KRB 80 794 |
| Azerbaijan | PER 221 540 | AZB 125 975 ; SRV 67 737 ; TAL 27 828 |
| Dagestan | CAUC 133 456 ; CHC 163 447 | CAUC 87 702 ; CHC 163 447 ; AZB 33 348 ; RUS 12 406 |
| Stavropol | CAUC 396 460 | CAUC 373 471 ; RUS 22 989 |
| Kuban | CIR 472 000 ; CRI 344 160 | Identique |
| North Caucasus | CAUC 157 848 ; CHC 82 680 ; CIR 55 231 | Identique |
| Kars | TUR 161 356 | Identique |

La suppression d'un scope territorial concurrent ne supprime pas les populations du pays concerné : les bassins préexistants du Kouban et du Caucase septentrional sont conservés. Le CSV démographique contient 191 lignes de groupes et une ligne de total, avec zéro variation totale.

## Bâtiments et armées

- Les niveaux déclarés de tous les bâtiments sont conservés. Les inventaires par State Region, PM, réserves et propriétaires économiques sont identiques dans le modèle statique.
- Erevan reçoit les bâtiments de son ancienne subdivision persane. Le vignoble est affecté à Nakhitchevan. Les quatre niveaux routiers existants sont répartis en trois à Erevan et un à Nakhitchevan, avec les mêmes PM.
- Les bâtiments de l'ancienne subdivision persane d'Azerbaijan sont affectés à Kouba. Aucun niveau neuf n'est créé pour remplir artificiellement les petits khanats.
- En Géorgie, une manufacture textile et une ferme de blé passent à l'Iméréthie. Les deux niveaux routiers sont répartis un à l'est et un à l'ouest. Les outils, le commerce et le vignoble restent à GEO.
- Les historiques natifs et le fichier de redistribution mondiale sont corrigés ensemble. La conservation de leurs inventaires écrits est testée ; le comportement exact de leur chargement doit encore être vérifié par le moteur.
- Les détenteurs économiques persans restent persans. Leurs références de siège devenues orphelines en Armenia/Azerbaijan/Elizavetpol sont redirigées vers leur subdivision existante de Tabriz. Cela ne modifie pas les niveaux de propriété.
- Les **25 unités permanentes persanes** recrutées en Armenia — 13 irréguliers, 10 hussards, 2 canons — et **une unité de conscription** conservent leur pays, leur type et leur formation, avec un recrutement déplacé à Tabriz. Aucun effectif national, général ou flotte n'est supprimé ou ajouté.
- Aucun recrutement fictif ni nouveau bâtiment militaire n'est attribué aux TAGs créés.

La présence d'un siège ou d'une route valide ne prouve pas l'emploi, l'accès effectif au marché ou l'équilibre budgétaire. Les petits États sans infrastructure dédiée et Tabriz doivent être observés en jeu. Aucun correctif général de connexion des enclaves n'est lancé.

## Dépendances et approximations

**Aucune nouvelle alliance, garantie, dépendance ou protectorats n'est inventé.** Les mécanismes russes concernant CRI/PLC, les sujets ottomans et les relations avec l'Égypte sont conservés.

Le manifeste classe les 45 transferts comme `DOCUMENTED_GAMEPLAY_APPROXIMATION` : les autorités sont documentées, mais les RGB ne correspondent pas exactement aux anciennes juridictions. Les sources précises et les limites de projection sont regroupées dans `MAP2E_GEOGRAPHIC_EVIDENCE.md`.

Points importants restant abstraits :

- IMR regroupe Iméréthie, Mingrélie, Gourie et Svanétie. Cela ne signifie pas que ces principautés formaient un royaume uniformément administré.
- AZB/Kouba regroupe Bakou et Salyan et reçoit le secteur de Derbent. Les cours locales et les rapports d'influence sont simplifiés.
- SRV représente une administration locale du Chirvan, sous forte influence de Kouba en 1774. **L'indépendance native de ce TAG n'est pas une affirmation d'indépendance historique totale.** L'absorption directe de 1786 n'est pas appliquée. Une traduction diplomatique plus précise pourrait faire l'objet d'une passe distincte.
- Jar/Ilisu, les sultanats de Gazakh et les melikats arméniens restent des juridictions locales abstraites dans les États régionaux.
- Les limites d'Akhaltsikhé, surtout `xC0CF80`, et les districts entiers de Kizliar/Mozdok dépassent une restitution cadastrale.
- CAUC/CHC restent des regroupements de communautés. Le nom initial de CHC est corrigé, mais sa loi théocratique et les anciens journaux de guerre caucasienne n'ont pas été reconstruits dans ce lot.
- Les sept nouveaux pays utilisent des drapeaux génériques à textures natives et des dirigeants générés. Aucun drapeau n'est présenté comme une reconstruction authentique ; les portraits et biographies historiques restent à traiter séparément.
- Plusieurs noms de hubs natifs demeurent postérieurs à 1776. Leur position sert de repère géographique, pas de preuve d'existence de ces villes à cette date.

## Validations

`MAP2E_VALIDATION.json` : **PASS_STATIC, 32 tests**.

- Changements de propriétaires exactement conformes au plan ; aucune province perdue ou ajoutée.
- Doubles attributions : **62 → 53**, aucune nouvelle. Les neuf corrigées appartiennent au périmètre.
- Treize défauts historiques de références préexistants hors périmètre subsistent, sans nouvelle référence orpheline. Leur liste exacte est conservée dans le JSON.
- Bitmap et géométrie des State Regions inchangés, y compris Avignon, Frioul et le dernier correctif du Budjak.
- Conservation exacte du total mondial, de chaque région et des groupes culturels/religieux/statuts.
- Conservation des niveaux/PM/propriétaires économiques et effectifs nationaux ; seul le recrutement persan explicitement prévu change de région.
- Sept nouveaux TAGs sans collision avec les pays existants ; capitales possédées, technologies/lois existantes, textures de drapeaux natives, localisations EN/FR avec BOM et clés correspondantes.
- Comparaison des empreintes des fichiers protégés : aucun changement non prévu dans MAP-2A/B/C/D, les réformes ottomanes, le recrutement régional et les correctifs IA.
- Tests existants des journaux ottomans : 1 024 combinaisons administratives et 192 voies politiques. Tests IA des infrastructures : dix scénarios. **Ce sont des tests de logique parsée, pas une exécution de Victoria 3.**
- CSV : valeurs typées dans le classeur de préparation, recalcul des écarts et du total, essais première/milieu/dernière ligne restaurés, scan d'erreurs et rendu visuel des trois tableaux.
- Relecture indépendante des fichiers exportés : dix contrôles réussis, notamment la correspondance des 54 décisions au plan, les 191 groupes démographiques, le total et le nettoyage des seuls clones vérifiés.

Le jeu n'a pas été lancé par l'agent. La validation native n'est donc pas acquise.

### Nouvelle partie : contrôles courts

1. **Géorgie** : Héraclius II à l'est, Iméréthie à l'ouest, Abkhazie séparée, Akhaltsikhé ottomane ; vérifier noms et frontières.
2. **Caucase oriental** : Erevan/Nakhitchevan, Gandja/Chaki/Karabakh, Kouba/Chirvan/Talysh et Derbent ; vérifier pays, drapeaux et populations.
3. **Nord** : deux districts russes de Kizliar/Mozdok, montagnes non russes et `xBCF376` circassien.
4. Au premier jour puis après un mois, contrôler les bâtiments, emploi et accès au marché des nouvelles subdivisions, ainsi que les 25 permanents persans et leur recrutement à Tabriz.
5. Confirmer que Budjak/Kerch/Kinburn, CRI/PLC dans le bloc russe et les deux journaux ottomans restent inchangés. Une ancienne sauvegarde ne constitue pas un test des historiques de départ.

## Sauvegarde et nettoyage

La branche distante [backup/1776-checkpoints](https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/backup/1776-checkpoints) contient :

- [0e1642705d4e8bd979893435b3b5b1981107bbe9](https://github.com/Malzars-sys/1776-Age-of-Revolutions/commit/0e1642705d4e8bd979893435b3b5b1981107bbe9) : point précédent MAP-2D, conservé.
- [cb401334bc58f2aa0747fa1a45567f3ab54a14fe](https://github.com/Malzars-sys/1776-Age-of-Revolutions/commit/cb401334bc58f2aa0747fa1a45567f3ab54a14fe) : MAP-2D validé et revue ciblée du Budjak, état exact avant MAP-2E.

Le second point a été préparé dans une copie Git indépendante puis vérifié par un nouveau clone distant et `git fsck`. **5 616 fichiers sources restaurés avec toutes les empreintes SHA-256 identiques**. Les deux fichiers supplémentaires du commit décrivent le checkpoint. Aucun ZIP volumineux ni Git LFS ajouté. Le pack sortant était de 4 692 511 octets ; le plus gros fichier du contenu, de 43 598 540 octets, reste sous la limite GitHub de 100 MiB par fichier ([documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)).

Après vérification, les clones temporaires `prepared/` et `restored/`, ainsi que les trois fichiers temporaires `outgoing-0d00d47f7813ebcd92483103520f886d1440ea25.{pack,idx,rev}`, ont été supprimés dans le dossier de vérification dédié. Cela retire **11 388 fichiers représentant 3 814 966 185 octets, environ 3,55 Gio de tailles logiques**. L'allocation physique du disque n'a pas été mesurée. Les preuves légères sont conservées. Les anciennes archives distinctes, fichiers de jeu et sauvegardes de parties ne sont pas supprimés.

MAP-2E reste local, avec une baseline textuelle/différentielle et un patch d'intégration. Il n'est pas encore publié sur la branche de sauvegarde. **Aucun commit dans le workspace principal, aucun merge, aucun push vers main, aucun force-push ni suppression distante.** Le seul commit/push de cette tâche concerne la sauvegarde MAP-2D autorisée dans la copie indépendante. Aucun lot suivant n'a été commencé.

## Fichiers de jeu concernés

La liste des 18 fichiers figure dans `modified_runtime_files` du JSON de validation : historiques des états, populations, bâtiments et recrutement persan ; définitions de pays et historique ARM ; deux fichiers de hubs ; noms dynamiques ; sept TAGs et initialisations locales ; noms de subdivisions, on_actions, drapeaux et localisations EN/FR. Les outils de validation et les livrables sont ajoutés sans modification des autres systèmes.
