# Diplomatie et réforme ottomane — départ du 1er janvier 1776

**Mise à jour :** les règles des journaux (dix objectifs, échéance 1836), le bloc russe et l’armée ottomane ont été modifiés depuis ce rapport. Voir le [rapport de refonte et de validation](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/diplomacy/OTTOMAN_REFORMS_RUSSIAN_STABILITY_2026-10-09.md>). Les anciens paliers et la date de 1853 ci-dessous sont conservés comme historique, pas comme règles actuelles.

Rapport du 9 octobre 2026. État de référence : branche `main`, révision `a62be0b`, initialement sans modifications locales. Jeu installé : Victoria 3 1.13.11 ; les deux descripteurs locaux ciblent 1.13.*. Aucun push, fusion, changement de branche, lancement ou redémarrage du jeu effectué.

Les changements sont intégrés aux fichiers locaux et leurs contrôles statiques passent. **L’équilibrage ottoman et le comportement du moteur restent à valider dans une nouvelle partie.** L’étude comptable d’une ancienne sauvegarde et les tests de logique ne constituent pas un test en jeu de cette version.

## Rectificatif : audit du lancement utilisateur du 9 octobre, 21 h 50

Le lancement utilisateur a révélé des erreurs que les tests statiques initiaux n'avaient pas détectées. Les corrections ci-dessous sont intégrées aux fichiers, **mais aucun nouveau lancement après correction n'a été effectué par l'agent**. Les paragraphes suivants décrivent le lot initial ; cette section fait autorité pour son activation et sa validation.

### Corrections effectuées

| Défaut constaté | Preuve avant correction | Correction locale |
|---|---|---|
| Journaux ottomans absents de la liste active | `error.log:994–995` : doublons refusés ; sauvegarde du 8 janvier 1776 : objets 6941/6942 `active=no`, objectifs nuls, aucun modificateur administratif | Initialisation des variables seulement ; activation automatique par `possible` et visibilité par `is_shown_when_inactive`, réservées aux pays initialisés ; gardes de fin/échec contre la réactivation. |
| Dates des scripts ottomans rejetées | `error.1.log:143,152,264` : `Unknown trigger type: current_date` | `game_date`, confirmé dans les scripts du jeu 1.13.11, remplace `current_date` dans les trois fichiers. |
| Chantier naval et deux entrées d'université égyptiennes non créés | `error.log:358,362,666` ; aucun chantier/université en Basse-Égypte dans la sauvegarde | Technologies minimales de création et des PM transférés : arsenaux d'État, bassins fermés, routes à péage/canaux industriels, échanges scientifiques/académies techniques. Ni nouveaux bâtiments, ni duplication, ni augmentation des niveaux. |
| PM transférés en Égypte remplacés par les défauts | Sauvegarde : canaux industriels remplacés par absence de canaux ; port utilisant mouillage | Les mêmes technologies minimales couvrent aussi les méthodes explicitement configurées. Vérification de 41 entrées d'historique égyptiennes, bâtiments et PM. |
| Deux erreurs polono-lituaniennes plus anciennes, dans un fichier du lot | `error.1.log:261–263`, `error.log:99` : `value` en portée État et bloc invalide de suppression | `count >= 5` États avec université ; `remove_modifier = the_white_eagle_reborn`. Aucune modification des objectifs de partage supprimés précédemment. |

Le modèle de tests reproduit désormais l'éligibilité de journaux précréés inactifs et leur modificateur pendant l'activité. Il vérifie qu'ils ne s'activent pas ailleurs, ne redémarrent pas après résolution/échec et que les dates utilisent la véritable clé du moteur. **Il ne simule pas le moteur** : son succès initial avait laissé passer la fausse clé de date et le problème de double ajout.

### Audit complet et éléments réellement chargés

Lecture des **60 fichiers `.log` disponibles**, y compris les rotations ; 19 appartiennent au dernier lancement, identifié par `code_revisions.log` (21:50:31). Comparaison des messages avec les rotations plus anciennes, en normalisant numéros de ligne et identifiants temporaires de tooltips. Les répétitions entre `debug`, `error` et `game` ne représentent pas des incidents indépendants. L'outil `tools/audit_1776_runtime_logs.py` permet de répéter cette lecture sans écrire dans les logs ni les sauvegardes.

La sauvegarde `autosave_exit.v3`, datée `1776.1.8.18`, confirme : les quatre nouveaux traités et leurs six clauses attendues ; Égypte propriétaire des cinq États et marionnette ottomane ; Hanovre en union personnelle britannique ; les cinq États levantins toujours ottomans et sans incorporation. Les fichiers modifiés ont donc bien été chargés : ce n'est pas une absence générale de chargement du mod.

Le bloc russe porte bien sa date de fondation corrigée, **mais CRI et PLC ont déjà quitté leur bloc les 6 et 7 janvier** selon leurs dates de sortie dans la sauvegarde. Cela indique une évolution après initialisation, pas une erreur de lecture du fichier. Aucun verrouillage de sortie ou changement de l'IA n'a été ajouté : conserver ces pays durablement dans le bloc demanderait une décision d'équilibrage supplémentaire.

### Anomalies antérieures encore présentes, non réparées dans ce lot

- Des créations de bâtiments sont refusées ailleurs faute de technologies, notamment académies dans plusieurs pays, arsenaux ou chronométrie marine. Les erreurs d'Égypte introduites par son transfert sont corrigées ; les autres cas ne sont pas masqués par une distribution mondiale de technologies.
- Neuf clés de définition sont refusées comme doublons, dont cinq PM d'ateliers domestiques, le groupe forestier et le groupe d'automatisation ferroviaire des plantations de caoutchouc (`error.1.log:96–100,124–125`). Leurs variantes plus tardives ne remplacent donc pas nécessairement les premières définitions.
- Le traité PER/DEI est refusé parce que sa clause cible NET, absent des signataires (`error.log:958`). Il avait déjà été signalé dans le lot initial ; aucun choix de partenaire différent fait ici.
- Provinces mal référencées (`00_states.txt`, `error.log:109–117`) et populations/bâtiments dans des États inexistants ; plusieurs affectations de commandants échouent sur d'anciennes portées `cleanup2d5_reuse_*` (`error.log:858–878` pour le fichier moyen-oriental). Aucun de ces messages ne vise la nouvelle formation égyptienne.
- Scripts hérités incompatibles avec 1.13.11 : `is_ruler`, `is_heir`, anciens ratios navals, `has_port`, effet EIC manquant, ancienne propriété d'épinglage de plusieurs journaux ; références japonaises, modèles de personnages et notifications absentes.
- Trois technologies sans poids IA (`traditional_glassmaking`, `codified_practical_knowledge`, `organized_naval_establishments`) ne sont pas recherchables par l'IA selon `error.1.log:144–146` ; plusieurs actions diplomatiques anciennes sans évaluation IA ; cinq modificateurs de laboratoire à marquer comme purement scriptés.
- Avertissements de BOM, textes non localisés, collisions de localisation et paramètres obsolètes. Les doublons de localisation prévus et les simples messages de chargement graphique ne sont pas assimilés à un échec du lot. Les logs graphiques du lancement ne signalent pas une disparition des nouvelles icônes de ce lot.

Conclusion : **les corrections locales sont contrôlées statiquement, pas encore validées après relance**. Pour vérifier le départ corrigé et retrouver les bâtiments auparavant refusés, redémarrer Victoria 3 et lancer une nouvelle partie ; laisser passer au moins un jour pour l'activation automatique des journaux. Les anciennes sauvegardes ne recréeront pas les bâtiments de l'historique. La reprise des journaux sur une sauvegarde déjà initialisée est prévue, mais reste à tester.

### Demande ajoutée pendant l'audit : déblocages d'infanterie

L'infanterie à mousquet est désormais débloquée par `light_infantry_tactics` (« Infanterie légère »), l'infanterie de ligne par `armament_standardization_inspection` (« Normes d'armement », ère suivante). Seules les deux références de déblocage changent : statistiques, illustrations et effectifs de départ conservés. Les unités déjà présentes ne sont pas converties automatiquement ; les pays n'ayant pas les normes d'armement ne débloquent plus de nouvelles unités de ligne par la seule infanterie légère.

## 1. Diplomatie effectivement modifiée

| Relation | Représentation au départ | Compromis |
|---|---|---|
| Empire ottoman → France | Capitulations du 28 mai 1740, un seul privilège commercial dirigé vers la France ; relations à +20 | Aucun privilège inverse. Ne simule ni juridiction consulaire ni tarif historique précis. |
| France ↔ Espagne | Pacte de famille du 15 août 1761 : alliance et privilèges réciproques ; relations à +50 | Les clauses commerciales historiques concernaient notamment les royaumes européens ; le privilège vanilla porte plus largement sur les marchés. |
| France ↔ Autriche | Pacte défensif issu de Versailles, 1er mai 1756 ; relations conservées à +20 | Engagement juridique distinct d’une coopération militaire inconditionnelle ; pas de disparition programmée en 1781. |
| Grande-Bretagne ↔ Portugal | Alliance de Windsor, 9 mai 1386 | Durable mais dénonçable, sans verrouillage artificiel de 500 ans. |
| Grande-Bretagne ↔ Prusse | Pas d’alliance de Westminster réintroduite | Ne prolonge pas en 1776 la coalition de la guerre de Sept Ans. |
| France/Espagne ↔ insurgés américains | Suppression des soutiens à l’indépendance initialisés artificiellement en 1775 | Les accords et interventions futurs restent à développer conditionnellement. |

Les capitulations sont attestées par leur [texte de 1740](https://www.palquest.org/en/historictext/41618/ottoman-capitulation-france-1740-french). L’alliance bourbonienne et les dispositions réciproques sont documentées dans le [Pacte de famille, notamment les articles I, II et XXIV](https://www.heraldica.org/topics/france/pacte1761.htm).

Le rapprochement franco-autrichien se poursuit après 1756 et est consolidé par les mariages dynastiques, dont celui de 1770. Le pacte défensif est une approximation de gameplay, pas une affirmation selon laquelle toutes les garanties originelles seraient appliquées mécaniquement. [Musée des Habsbourg](https://www.habsburger.net/en/chapter/maria-theresa-europes-mother-law).

Le [traité de Windsor](https://portugal-uk650.com/en/alliance/) justifie une alliance anglo-portugaise durable. Le [National Army Museum](https://www.nam.ac.uk/explore/seven-years-war) replace la coalition anglo-prussienne dans la guerre achevée en 1763 ; aucun traité expiré n’a été recréé.

Le Model Treaty est un projet adopté le **17 septembre 1776**, pas un accord déjà signé au 1er janvier. Les traités franco-américains ne sont conclus qu’en 1778. [Office of the Historian](https://history.state.gov/milestones/1776-1783/model-treaty). Les futures aides clandestines, ventes d’armes, prêts et alliances peuvent devenir des choix de journal liés à la situation de guerre, plutôt que des déclenchements obligatoires à date fixe.

Le traité de la Quadruple Alliance, hérité du contexte de 1834, a également été retiré du départ 1776. Les autres accords hors périmètre n’ont pas été remaniés arbitrairement. À reprendre dans un audit régional : Adrianople rétrodaté à 1775 avec la Moldavie/Valachie, incohérence DEI/NET dans le privilège persan et droits de transit prussiens au Luxembourg.

### Durée réelle des traités

Dans cette version du moteur, `binding_period_in_years` représente une période où la dénonciation entraîne des pénalités, **pas une expiration automatique**. Les traités persistent jusqu’à leur rupture. Leurs périodes historiques de cinq ans sont déjà écoulées en 1776 : ni pacte franco-autrichien limité aux cinq prochaines années, ni Windsor verrouillé jusqu’en 2276.

Vérification dans les concepts vanilla `concept_treaty` et `concept_treaty_binding_period` de [concepts_l_english.yml](<C:/Games/Victoria 3/game/localization/english/concepts_l_english.yml:1319>).

## 2. Russie, Commonwealth et Crimée

PLC et CRI sont désormais membres initiaux du bloc russe. Leurs territoires, populations et souveraineté initiale sont conservés : rejoindre un bloc n’équivaut pas à être annexé ou automatiquement mis sous protectorat. La date de fondation russe a été ramenée de 1825 à 1721 ; le 22 octobre ancien style correspond au 2 novembre grégorien. [Document des Archives russes](https://raritety.rusarchives.ru/node/1238).

L’influence russe sur le Commonwealth est représentée comme une dépendance politique, sans l’assimiler juridiquement à une province russe. Les conflits entourant la domination russe et le premier partage sont étudiés dans cette [recherche de l’Institut d’Europe centrale et orientale](https://ies.lublin.pl/wp-content/uploads/2021/08/riesw_1732-1395_16-2-379.pdf). Le bloc reste une abstraction de gameplay.

La Crimée était déjà indépendante dans les relations de sujets : aucune nouvelle « libération » n’était nécessaire. Le [traité de Küçük Kaynarca de 1774](https://ppu.gov.ua/en/press-center/kiuchuk-kaynardzhiyskyy-myrnyy-dohovir-21-lypnia-1774-roku-250-rokiv-z-chasu-pidpysannia/) met fin à la suzeraineté ottomane officielle ; l’annexion de 1783 ne doit pas être préappliquée.

L’action vanilla de subordination des membres d’un bloc a été copiée avec une seule exception : **RUS ciblant CRI peut ignorer les cinq ans de présence dans le bloc**. Tous les autres contrôles demeurent : principe autorisant la subordination, cohésion, rapport de prestige, rang et absence de participation engagée à un jeu diplomatique. Les autres couples de pays gardent le délai. L’action aboutit au protectorat vanilla dans ce cas ; ce n’est pas une réussite automatique au lancement.

Une revendication russe sur STATE_CRIMEA existe déjà : conservée, sans en ajouter de doublon. C’est une revendication de gameplay contestable, pas la reconnaissance d’un titre de souveraineté russe valable sur tout le khanat en 1776. Kerch/Yeni-Kale et la précision de leurs provinces méritent un futur audit cartographique ; aucun transfert territorial nouveau n’a été improvisé.

### Partages de la Pologne : sécurité immédiate et plan ultérieur

L’audit a trouvé un ancien journal `je_plc_reform` qui, après **6 000 jours**, transférait sans négociation jusqu’à douze États à RUS, PRU et AUS. Cette échéance et ses transferts automatiques ont été désactivés. Les objectifs, récompenses et journaux de modernisation existants sont conservés. Aucun nouveau système complet de partage n’a été développé.

Plan proposé :

1. Journal de crise : éligibilité liée à l’existence et à la souveraineté de PLC, aux troubles internes, à l’influence étrangère et à une crise diplomatique réelle. Pas de compte à rebours conduisant nécessairement à l’annexion.
2. Initiatives séparées des voisins : revendications argumentées, négociation et possibilité de veto, soutien étranger ou guerre. Le premier partage déjà antérieur à 1776 n’est pas rejoué.
3. Choix polonais : réforme constitutionnelle, concessions limitées, recherche de garanties, résistance militaire ou maintien du statu quo.
4. Transferts uniquement après accord accepté ou paix : validation des propriétaires présents et des provinces concernées ; conservation de populations et bâtiments, sans transfert vers un pays inexistant.
5. Issues alternatives : crise résolue sans perte, partage limité, résistance victorieuse ou disparition négociée après plusieurs crises. Aucun partage global déclenché par le seul passage de l’année 1793/1795.

Ce développement et les territoires proposés nécessitent une validation séparée.

## 3. Deux journaux ottomans distincts

L'historique global initialise les variables une seule fois ; les deux journaux précréés inactifs deviennent éligibles et s'activent via leurs conditions `possible`. Voir le rectificatif d'audit ci-dessus.

### Le fardeau de la Sublime Porte

Sans échéance fixe. Trois axes de réforme :

- Administration : abandon des bureaucrates héréditaires, bureaucratie non négative sans pénurie imminente, et au moins 90 % des administrations sans pénurie de biens.
- Fiscalité : sortir de l’imposition foncière ou de consommation ; aucun impôt moderne unique n’est imposé.
- Institutions : police ou écoles de niveau 2 minimum.

Chaque axe réduit progressivement les pénalités. Les trois conditions doivent être maintenues pendant douze impulsions mensuelles pour terminer le journal. Une interruption réinitialise cette durée. Perdre une réforme avant la résolution fait disparaître son allégement.

| Réformes satisfaites | Gaspillage fiscal net ajouté | Production de bureaucratie |
|---|---:|---:|
| 0 | +80 points de pourcentage | −10 % |
| 1 | +55 points | −7 % |
| 2 ou 3, avant résolution | +25 points | −3 % |
| Résolution après 12 mois conformes | 0 | 0 |

Aucun malus religieux permanent ni pénalité supplémentaire à la production privée n’a été ajouté.

### Un empire aux multiples maîtres

La stabilité exige : contrôle d’Eastern Thrace, Ankara, Albania et Bosnia ; Égypte directement possédée ou demeurant sujet ; aucun sujet à désir de liberté ≥50 ; séparatisme <25 % ; absence de révolution, guerre ou défaut ; bureaucratie non négative.

Trois stratégies alternatives sont acceptées :

- légitimité ≥60 et police/écoles de niveau 2 ;
- légitimité ≥75 et tous les sujets à désir de liberté <25 ;
- administration réformée et légitimité ≥50.

Trente-six impulsions stables résolvent la crise politique. Une administration modernisée double la progression, ramenant ce parcours à dix-huit mois. **Résoudre l’un des journaux ne termine pas automatiquement l’autre.**

Les mois instables augmentent la pression. Pertes territoriales, forte sécession, révolution, défaut ou guerre mal administrée l’accélèrent ; une bureaucratie négative l’aggrave. La stabilité diminue progressivement la pression accumulée.

### Transition vers l’Homme malade

À partir de **1853**, si la pression accumulée atteint 120 et que l’Empire est encore instable, le journal politique échoue. Cette année correspond au contexte diplomatique du milieu du XIXe siècle, pas à une annexion obligatoire ni à une reproduction de la crise de 1836. Les [débats parlementaires sur les échanges de Seymour de 1853](https://api.parliament.uk/historic-hansard/lords/1854/mar/31/war-with-russia-her-majestys-message) documentent ce contexte.

Séquence :

`Multiples maîtres actif → échec et retrait → événement retardé d’un jour → Homme malade actif`

Le journal administratif peut rester actif. Le modificateur fiscal vanilla `outmoded_bureaucracy` n’est pas ajouté par-dessus : pas de double peine fiscale. Le modificateur politique et les objectifs de Tanzimat existants sont repris.

Un contrôle mensuel récupère la transition si l’événement différé est perdu. Les gardes empêchent de démarrer deux fois le journal ou de le superposer au précédent. Les journaux sont héritables lors d’une révolution victorieuse ; la documentation du moteur indique que les variables nationales suivent également cette succession. Ceci doit néanmoins être testé en jeu, notamment si le pays est détruit ou son tag remplacé par une autre mécanique.

Le seuil et l’année sont des choix de conception explicités, pas des constantes historiques. Une stabilisation précoce permet d’éviter cette transition.

## 4. Calibrage économique : résultat provisoire

Sauvegarde existante du 31 janvier 1776, consultée en lecture seule : solde ottoman **+65 757 £/semaine**. La fiscalité personnelle/subsistance domine les recettes. Ce relevé précède les changements actuels.

Calcul de sensibilité, à autres éléments constants :

- Retirer recettes et dépenses des cinq États égyptiens : environ +2 183 £ sur le solde ottoman.
- Désincorporer les cinq États du Levant en retirant leurs seules taxes personnelles mesurées : environ −6 057 £.
- Solde contrefactuel avant nouveau malus : **+61 883 £** ; taxes personnelles restantes estimées : **69 378 £**.

| Fuite fiscale appliquée à cette base simplifiée | Solde estimé |
|---|---:|
| 25 % | +44 539 £ |
| 50 % | +27 194 £ |
| 75 % | +9 850 £ |
| 80 % | +6 381 £ |

Ce calcul motive un malus initial plus élevé qu’un simple −20/−30 %. **Il ne garantit pas ce solde en jeu.** Les interactions additives des modificateurs, nouvelles lois égyptiennes, qualifications, recrutement, versements du sujet, changements de marché et réaction des populations ne sont pas simulés ici. Le −10 % de bureaucratie reste également à éprouver.

Les valeurs livrées sont donc provisoires : ne pas les présenter comme un équilibrage validé. Mesurer TUR et EGY après 1, 4 et 12 semaines puis un an, avec taxes et salaires fixes. Vérifier la viabilité égyptienne en particulier : les dépenses historiques de ses administrations sont élevées. Ajuster ensuite le malus, pas supprimer arbitrairement ses bâtiments.

## 5. Égypte, Levant et armée

Égypte : sujet `puppet` ottoman, faible autonomie ; désir de liberté initial réduit de 45 à 20 dans l’historique. Transfert exact de Lower Egypt, Middle Egypt, Upper Egypt, Matruh et Sinai. Le Soudan n’est pas ajouté. Populations, bâtiments, niveaux, PM et références de propriété locales ont été transférés sans suppression.

Les personnages hérités de l’Égypte de 1836 ont été remplacés par Ibrahim Bey comme représentant politique et Murad Bey comme général. Leur partage du pouvoir après 1775 est attesté par la [notice de TDV sur Ibrahim Bey](https://islamansiklopedisi.org.tr/ibrahim-bey). Le dirigeant unique et sa culture nord-caucasienne sont des approximations : ils ne font pas d’Ibrahim un souverain indépendant ni ne reproduisent exactement le gouverneur officiellement nommé par la Porte. Son titre affiché devra être vérifié. Aucun Muhammad Ali de 1805 n’a été installé.

Fiscalité égyptienne ramenée à l’imposition foncière et économie au traditionalisme, sans importer d’emblée les réformes du XIXe siècle.

Levant : Aleppo, Syria, Lebanon, Palestine et Transjordan restent ottomans mais deviennent désincorporés. Adana et les autres États du Proche-Orient ne sont pas inclus aveuglément.

| Forces | Avant | Après |
|---|---:|---:|
| Réguliers ottomans directs | 65 | 50 |
| Conscrits ottomans directs | 139 | 114 |
| Réguliers égyptiens | 0 | 15 |
| Conscrits égyptiens | 0 | 25 |
| Total impérial régulier / conscrits | 65 / 139 | 65 / 139 |

Ce sont des unités de gameplay, pas une estimation en hommes historiques. Les unités égyptiennes proviennent des unités ottomanes déjà recrutées dans ces États ; aucune duplication. Les 50 réguliers ottomans restants se répartissent entre Albania et Adana, avec quartiers généraux balkaniques/proche-orientaux ; la flotte existante n’est pas augmentée.

La faiblesse de l’armée directe et sa forte composante irrégulière sont confirmées dans les fichiers. Certaines technologies disponibles permettent une amélioration, mais ne justifient pas une modernisation générale. **Pas de doublement arbitraire effectué.** Un lot suivant devra chiffrer des renforts provinciaux balkaniques/anatoliens, leurs coûts et les capacités de mobilisation, après validation du nouveau budget.

Le journal syrien existant vérifie déjà si l’Égypte est sujet : dans ce cas, il crédite l’objectif au lieu d’ajouter le journal de reconquête. Aucun futur événement de création/libération en doublon n’a été ajouté.

## 6. Audits sans refonte

### Hanovre et Saint-Empire

L’union personnelle GBR → HAN est déjà correcte : conservée. Les sujets rejoignent automatiquement le bloc de leur suzerain.

Le Saint-Empire n’est pas absent des fichiers : bloc dirigé par AUS, identité de ligue commerciale et commerce interne niveau 3. Il compte **27 membres explicitement listés**, en plus du chef : MOD, TUS, PAR, PRU, LUB, HAM, BRE, BRA, SCM, MST, OLD, HES, BAV, WUR, BAD, SAX, HEK, MEC, NAS, WEI, SCW, COB, MEI, ANH, WLD, LIP et FRM.

Cette union douanière ne représente pas les électeurs, la Diète ou les institutions impériales. Les commentaires copiés du Zollverein/Congrès de Vienne ne correspondent pas à 1776. Aucun système dédié de convocation impériale n’a été trouvé dans les journaux et scripts examinés.

Hanovre appartient au bloc britannique et ne peut pas simultanément rejoindre le bloc autrichien dans cette représentation à un seul bloc par pays. Proposition : conserver la vraie relation de sujet britannique et représenter l’appartenance impériale par un statut/journal/variable indépendant du bloc commercial. Refondre le bloc ou la convocation religieuse exige une décision ; aucun changement fait ici.

### Présence britannique en Amérique

La correction existante est conservée : formation au quartier général Canada, hub à Newfoundland, treize réguliers recrutés à Bermuda et dix conscrits ; autre formation antillaise et station navale déjà présentes. Ce n’est pas la preuve d’une garnison répartie dans les colonies continentales : vérifier le déploiement réel dans l’interface. Pas de nouvelles unités ajoutées.

### Luxembourg et georg3mx

La branche `georg3mx-map-rework` est déjà ancêtre de `main` ; aucun commit propre à cette branche ne reste à fusionner. Ses changements intégrés sont préservés.

LUX possède encore explicitement la province `xD001A0` dans STATE_WALLONIA, avec historique national/démographique/bâtiments : sa présence n’est donc pas expliquée seulement par une ancienne sauvegarde. Le transfert éventuel doit être décidé et coordonné entre territoire, pops et propriétés. Aucun territoire ou travail du collaborateur supprimé.

### Arbre technologique et performances

| Mesure | Mod | Vanilla installé |
|---|---:|---:|
| Technologies | 292 | 179 |
| Liens de prérequis | 393 | 221 |
| Maximum de prérequis directs | 4 | 4 |
| Cycles / prérequis absents / doublons | 0 | 0 |
| Icônes absentes / placeholders repérés | 0 | 0 |
| Noms ou descriptions FR/EN manquants | 0 | 0 |
| Appels ObjectsEqual dans l’interface | 93 | 6 |

La ligne d’interface la plus longue compte 3 822 caractères. Les conditions répétées sur cartes et liaisons sont une piste de coût d’évaluation, **pas une cause démontrée des 10 FPS**. Aucun changement spéculatif à l’interface ou aux prérequis.

Les anciens logs signalent notamment des fichiers sans BOM, une règle de monument dupliquée, des localisations d’interface manquantes et un progrès technologique sans technologie acquise. Ils ne prouvent pas un défaut de cette nouvelle version ni sa performance. Les durées de menu/bookmark ne mesurent pas les FPS.

Procédure : même sauvegarde en pause et même zoom ; comparer carte puis chacun des trois arbres, sans puis avec survols ; relever FPS moyens, temps d’image et latence du panneau. Comparer vanilla/mod avec mêmes paramètres graphiques. Dans une copie de test seulement, simplifier les longues conditions de visibilité en gardant le contenu, puis mesurer avant toute correction publiée.

## 7. Demande ajoutée : pompe diesel

Les pompes diesel des mines de **fer et de plomb**, seules variantes auparavant à 70, produisent désormais **85 par niveau**. Consommations, emplois et autres variantes diesel inchangés. La comparaison avec la référence vérifie que le fichier des mines ne diffère que par ces deux rendements.

## 8. Validation et limites

Contrôles exécutés :

- Syntaxe structurelle de tous les fichiers texte modifiés.
- Conservation exacte des inventaires de provinces, pops, bâtiments et unités régionales d’Égypte/Levant par comparaison avec `a62be0b`.
- Privilège franco-ottoman à sens unique ; exception Crimée limitée au couple RUS/CRI ; reste de l’action diplomatique identique à vanilla.
- Sujet égyptien, États et personnages cohérents ; aucune échéance de partage polonais automatique.
- Existence des icônes utilisées ; localisations françaises/anglaises présentes ; nouveaux textes du jeu avec BOM.
- Tests exécutant les scripts personnalisés dans un petit modèle : initialisation répétée, résolutions indépendantes, recul des allégements, accélération administrative, interdiction de transition avant 1853, récupération mensuelle et absence de double déclenchement.
- Audit structurel des technologies ; `git diff --check`.

**Tous ces contrôles passent.** Le modèle teste la logique des scripts, pas les restrictions de portée, l’ordonnancement ou les interfaces du moteur Victoria 3.

Tests en jeu encore requis : nouvelle partie TUR/EGY ; traités et blocs ; éligibilité réelle de la subordination de CRI ; recrutement et finances égyptiens ; progression de chaque stratégie ; changement de régime ; perte de territoire ; guerre ; transition après 1853 et chargement d’une sauvegarde à chaque étape. Le jeu n’a pas été piloté pendant ce lot. Une sauvegarde antérieure ne réinitialise pas ces historiques.

Reste à approuver ou à finaliser : valeurs économiques après mesures ; renforcement militaire ottoman ; statut visuel mamelouk ; partage conditionnel de PLC ; institutions du Saint-Empire ; Luxembourg ; optimisation technique après reproduction.

Pour les recherches ultérieures : accords et obligations des petites principautés impériales ; relations Danemark–Russie et règlement Holstein/Schleswig de 1773 ; relations franco-suédoises après 1772 ; États italiens et possessions dynastiques ; accords commerciaux maritimes encore applicables en 1776. Aucune obligation non vérifiée n’a été inventée. Révolution française et ascension de Napoléon restent des développements futurs conditionnels, non implémentés ici.

## 9. Fichiers livrés

Les 25 fichiers ci-dessous regroupent les modifications, nouveaux scripts et outil de contrôle. Le présent rapport est le seul document de compte rendu ajouté ; aucun nouvel asset graphique, déclinaison ou aperçu généré.

### Diplomatie et territoires

- [common/history/treaties/00_historical_treaties.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/treaties/00_historical_treaties.txt>)
- [common/history/diplomacy/00_relations.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/diplomacy/00_relations.txt>)
- [common/history/diplomacy/00_subject_relationships.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/diplomacy/00_subject_relationships.txt>)
- [common/history/power_blocs/00_power_blocs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/power_blocs/00_power_blocs.txt>)
- [common/diplomatic_actions/31_power_bloc_force_become_subject.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/diplomatic_actions/31_power_bloc_force_become_subject.txt>)
- [common/history/states/00_states.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/states/00_states.txt>)

### Égypte

- [common/history/pops/03_north_africa.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/pops/03_north_africa.txt>)
- [common/history/buildings/03_north_africa.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/buildings/03_north_africa.txt>)
- [common/history/buildings/98_build_start_1776_world_redistribution.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/buildings/98_build_start_1776_world_redistribution.txt>)
- [common/history/countries/egy - egypt.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/countries/egy - egypt.txt>)
- [common/history/characters/egy - egypt.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/characters/egy - egypt.txt>)
- [common/history/military_formations/04_military_formations_middle_east.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/military_formations/04_military_formations_middle_east.txt>)

### Journaux et événements

- [common/history/global/99_1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/global/99_1776_ottoman_reforms.txt>)
- [common/journal_entries/1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/journal_entries/1776_ottoman_reforms.txt>)
- [common/scripted_triggers/1776_ottoman_reform_triggers.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/scripted_triggers/1776_ottoman_reform_triggers.txt>)
- [common/scripted_effects/1776_ottoman_reform_effects.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/scripted_effects/1776_ottoman_reform_effects.txt>)
- [common/static_modifiers/1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/static_modifiers/1776_ottoman_reforms.txt>)
- [events/1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/events/1776_ottoman_reforms.txt>)
- [common/on_actions/00_code_on_actions.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/on_actions/00_code_on_actions.txt>)
- [common/journal_entries/00_sick_man.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/journal_entries/00_sick_man.txt>)
- [common/journal_entries/07_poland_lithuania_mod.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/journal_entries/07_poland_lithuania_mod.txt>)

### Localisation, rendement et vérification

- [localization/english/1776_diplomacy_ottoman_l_english.yml](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/localization/english/1776_diplomacy_ottoman_l_english.yml>)
- [localization/french/1776_diplomacy_ottoman_l_french.yml](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/localization/french/1776_diplomacy_ottoman_l_french.yml>)
- [common/production_methods/03_mines.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/03_mines.txt>)
- [tools/validate_diplomacy_ottoman_1776.py](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/tools/validate_diplomacy_ottoman_1776.py>)

