# Lois 1.15 / State and Revolution — Russie et entourage, départ 1776

Date : 7 novembre 2026. Statut : `AUDIT_ONLY_NO_GAMEPLAY_EDITS_RUNTIME_NOT_TESTED`.

L'audit constate sept lois natives absentes du catalogue effectif parce que leurs fichiers vanilla sont masqués par les fichiers homonymes du mod. Les bureaucrates militaires et l'administration communale sont déjà hérités du vanilla. La colonisation interne vient d'être rétablie et initialisée par le chantier russe parallèle ; elle est exclue de toute écriture ici.

Il faut distinguer la disponibilité des nouvelles lois, leur raccordement à notre arbre technologique, et leur pertinence au 1er janvier 1776. Copier le profil russe vanilla de 1836 confondrait ces trois questions.

## Périmètre et concurrence

- Consultation du mod et de `C:/Games/Victoria 3/game`, version de l'exécutable vérifiée : **1.15.0** (`FileVersion` et `ProductVersion`).
- Pays examinés : Russie (`RUS`), Pologne-Lituanie (`PLC`), pays balte (`UBD`), Alaska (`ALK`), Petite jüz (`KZH`), Crimée (`CRI`).
- Aucun script chargé par le jeu, profil initial, amendement, fichier de carte, technologie ou localisation n'a été modifié par cette mission.
- Écritures propres : le présent dossier de preuves et `tools/compatibility/v115_russian_laws_audit.py`.
- Réservés au chantier parallèle : `common/history/countries/rus - russia.txt`, `common/laws/1776_world_russia01.txt`, `common/laws/01_colonial_affairs.txt`, les defines cosaques/frontaliers, les pays, États, bâtiments et populations du lot russe. Aucune restauration depuis une ancienne baseline.
- Pendant l'examen, le chantier parallèle a ajouté la loi de colonisation interne dans son fichier distinct, remplacé la colonisation de peuplement russe par cette loi, ajouté l'amendement cosaque et demandé un investissement colonial de niveau 1. Ces changements sont attribués à ce chantier, pas au présent audit. Leur fonctionnement en jeu n'est pas certifié ici.
- L'issue [#17](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/17) porte déjà un audit général des lois initiales et des prérequis. Ce diagnostic ciblé ne ferme pas cette issue et ne remplace pas les travaux attribués à sa contributrice.

## Catalogue des nouvelles lois

Les noms français proviennent de la localisation vanilla locale. « Absente » désigne une définition manquante après masquage de fichiers, et non une simple loi verrouillée dans l'interface.

| Loi native | État effectif relevé | Condition ou difficulté principale | Traitement proposé |
| --- | --- | --- | --- |
| Bureaucrates militaires (`law_military_bureaucrats`) | Présente, fichier vanilla `00_bureaucracy.txt` hérité | Pas de verrou technologique explicite ; la Russie demande encore les bureaucrates héréditaires | Candidate à une révision du profil russe, avec justification du modèle administratif ; pas de propagation automatique aux sujets |
| Césaropapisme (`law_caesaropapism`) | Absente ; `00_church_and_state.txt` masqué | Variante de religion d'État ; visibilité Russie ou certains sujets orthodoxes ; exclut la théocratie | Réintégrer la définition ; candidate solide pour la Russie de 1776, voir H1 |
| Nationalité officielle (`law_official_nationality`) | Absente ; `00_citizenship.txt` masqué | Variante de statut de sujet ; le code de visibilité ne permet que `RUS` | Contenu futur, ne pas initialiser en 1776 ; la doctrine d'Ouvárov est attestée en 1833, voir H3 |
| Troisième section (`law_third_section`) | Absente ; `00_internal_security.txt` masqué | Monarchie russe ; demande `law_enforcement`, alias non recherchable ; fenêtre avant `central_archives` | Contenu futur, institution fondée en 1826 ; résoudre également sa progression technologique, voir H2 |
| Okhrana (`law_okhrana`) | Absente ; même fichier masqué | Monarchie russe ; demande `central_archives`, alias non recherchable | Réintégration future avec prérequis adaptés ; aucune proposition d'initialisation en 1776 |
| Colonisation interne (`law_internal_colonization`) | Présente dans `1776_world_russia01.txt`, ajout concurrent | Technologie `colonization` ; type colonial ou au moins un État non incorporé pour promulgation normale | Appartient au chantier russe parallèle ; conserver son contrôle de l'initialisation et des frontières |
| Administration communale (`law_communal_administration`) | Présente, vanilla hérité | `socialism` et république des conseils ou conseils d'usine | Maintenir dans la progression future |
| Droit de vote des travailleurs (`law_labour_suffrage`) | Absente ; `00_distribution_of_power.txt` masqué | `socialism` et république des conseils | Restaurer la disponibilité future, sans octroi initial |
| Garde révolutionnaire (`law_revolutionary_guard`) | Absente ; `00_army_model.txt` masqué | `enlistment_offices` et république des conseils ou conseils d'usine | Restaurer la disponibilité future, sans octroi initial |
| Commission extraordinaire (`law_extraordinary_commission`) | Absente ; `00_internal_security.txt` masqué | `political_agitation` | Restaurer la disponibilité future, sans octroi initial |

Le relevé complet des lois natives confirme **exactement sept identifiants manquants**, tous inclus ci-dessus. Aucun doublon de loi ordinaire n'a été trouvé dans les fichiers effectifs analysés. Les directives d'injection sont inventoriées séparément ; elles ne sont pas comptées comme des lois distinctes.

## Pré requis : une copie du vanilla ne suffit pas

Les deux technologies ci-dessous existent encore comme identifiants de compatibilité, mais portent explicitement `can_research = no` dans `90_tech3a_vanilla_post1836_compatibility.txt`.

| Loi proposée à la réintégration | Référence native | Problème dans le mod |
| --- | --- | --- |
| Troisième section | Déblocage `law_enforcement` | Ne peut pas être atteint par la recherche normale de cet identifiant |
| Troisième section | Visibilité restreinte après `central_archives`, sauf loi déjà active | Le seuil de remplacement est lui aussi un alias consommé ; adapter le déblocage seul ne préserverait pas la succession des institutions |
| Okhrana | Déblocage `central_archives` | Ne peut pas être atteint par la recherche normale de cet identifiant |

Le rapport existant `docs/reports/technology/TECH3B_VANILLA_SEAM_RECONNECTION_REPORT.md` et la matrice `TECH2H_VANILLA_SPLIT_UNLOCK_MATRIX.csv` expliquent cette neutralisation. Les consommateurs ont été répartis selon leur fonction : par exemple, la police secrète existante dépend maintenant de `professional_civil_policing`, tandis que d'autres usages des archives centrales passent par `central_statistical_offices` ou `systematic_administrative_statistics`.

Il ne faut donc ni réactiver globalement les anciens alias, ni appliquer un remplacement textuel unique. Donner le même nouveau seuil aux deux institutions russes risquerait de rendre la Troisième section indisponible au moment même où elle se débloque. La succession Troisième section → Okhrana demande une décision propre au modèle technologique du mod, avec vérification des trois conditions concernées.

Les prérequis `socialism`, `political_agitation` et `enlistment_offices` restent recherchables dans les définitions consultées. `colonization` appartient déjà à l'arbre du mod et figure dans les technologies directement demandées pour la Russie. Cela ne certifie ni toutes les conditions politiques ni le chargement moteur.

## Lois initiales : six profils distincts

Le tableau résume les demandes de scripts après développement des deux macros politiques conservatrice et traditionnelle, puis application des remplacements explicites dans chaque profil. Les groupes omis n'ont pas de valeur certifiée par cet audit. Les demandes de lois initiales ne sont pas assimilées à une promulgation normale soumise aux mêmes prérequis.

| Pays | Relation scriptée avec la Russie | Bureaucratie demandée | Religion et État demandés | Observation |
| --- | --- | --- | --- | --- |
| `RUS` | Métropole | Héréditaire | Religion d'État | Césaropapisme et bureaucrates militaires méritent une révision spécifique ; aucun octroi initial des lois du XIXe siècle proposé |
| `PLC` | Membre du bloc russe, aucun pacte de sujétion russe trouvé | Nommée, issue de la macro conservatrice | Religion d'État | République présidentielle + monarchie élective ; oligarchie + liberum veto : préserver cet ensemble |
| `UBD` | Fantoche (`puppet`) | Nommée, issue de la macro conservatrice | Liberté de conscience | Le type fantoche n'entre pas dans la liste native des sujets éligibles au césaropapisme |
| `ALK` | Colonie (`colony`) | Héréditaire | Religion d'État | Le type et la religion orthodoxe inférée rendent une éligibilité au césaropapisme plausible ; cela ne justifie pas son adoption initiale automatique |
| `KZH` | Protection nominale kazakhe propre au mod | Héréditaire, issue de la macro traditionnelle | Gens du Livre, issue de la macro traditionnelle | Type de sujet non prévu par le déclencheur du césaropapisme ; religion sunnite inférée |
| `CRI` | Membre du bloc russe, aucun pacte de sujétion russe trouvé | Héréditaire | Système des millets | Conserver un profil propre ; aucun motif technique d'importer les lois russes |

La recherche dans l'historique diplomatique effectif retrouve trois sujets russes : `UBD`, `ALK`, `KZH`. Aucun sujet indirect supplémentaire n'est apparu dans la fermeture des pactes reconnus. Le JSON conserve les branches d'initialisation des pactes ; il ne simule pas les événements ultérieurs.

### Particularité polonaise à préserver

Le profil `PLC` ne correspond pas au `POL` du scénario vanilla de 1836. La monarchie élective est explicitement représentée par `amendment_elective_monarchy`, autorisé uniquement sur `law_presidential_republic`. Le liberum veto est autorisé uniquement sur `law_oligarchy`. Leurs clauses `possible` contrôlent également ces lois et le TAG `PLC`.

Remplacer isolément la république présidentielle par une monarchie ferait donc sortir son amendement de ses conditions actuelles. Ce n'est pas une correction de compatibilité à faire automatiquement. Ne pas importer non plus le Statut organique, les restrictions du Royaume du Congrès ou le profil russe du `POL` vanilla dans la Pologne-Lituanie de 1776.

### Portée réelle des lois russes chez les sujets

Le césaropapisme accepte, hors Russie, un sujet **orthodoxe** de type colonie, dominion, compagnie à charte, terre de la Couronne ou union personnelle, et exclut la théocratie. Le helper effectif est hérité de `00_ip5_victoria_scripted_triggers.txt`.

La nationalité officielle possède un commentaire annonçant la Russie et ses sujets, mais son test effectif contient seulement `c:RUS ?= this`. Le commentaire n'étend pas la portée du code. La Troisième section et l'Okhrana sont également limitées par leur visibilité à la monarchie russe.

Les religions mentionnées ici sont des inférences à partir de la première culture primaire de la définition initiale : russe orthodoxe, polonaise catholique, lettone protestante, kazakhe et tatare sunnites. Le modèle ne prétend pas observer la religion d'État en jeu, et n'infère pas une conversion après changement de culture primaire.

## Amendements du nouveau contenu

Les quatre définitions de `00_amendments_ip5_04.txt` sont héritées : conversions orthodoxes, conseils d'usine, spécialistes bourgeois et cosaques. Il n'existe pas de masquage homonyme de ce fichier dans le mod.

- L'amendement cosaque est demandé par le profil russe modifié dans le chantier parallèle.
- L'amendement de conversions orthodoxes est possible pour `UBD`, sur la liberté de conscience ; aucune activation initiale n'a été trouvée dans son profil. Une possibilité de gameplay ne démontre pas sa pertinence comme institution déjà active en 1776.
- Les amendements polonais du mod sont également définis et leurs lois de rattachement correspondent aux lois demandées par le profil.
- L'Alaska conserve son amendement de statut de sujet racialisé ; sa définition et sa loi de rattachement sont présentes.

## Appuis historiques et limites

**H1 — Administration synodale, 1721–1722.** La présentation institutionnelle de la Bibliothèque présidentielle décrit le Règlement spirituel publié le 25 janvier / 5 février 1721, le Saint-Synode et l'obér-procureur établi en 1722, directement subordonné au monarque. Cela soutient l'interprétation du césaropapisme comme abstraction jouable de la Russie de 1776. La correspondance avec une loi du jeu reste une interprétation, pas le nom juridique d'une loi russe de 1776. Page effectivement consultée le 7 novembre 2026 : [Le Synode dans l'histoire de l'État russe](https://www.prlib.ru/node/1827019).

**H2 — Troisième section, 1826.** La même bibliothèque date la création du 3 / 15 juillet 1826 et distingue les organes de police politique qui existaient au XVIIIe siècle, notamment l'Expédition secrète sous Catherine II. Le fait que la police politique existe en 1776 n'autorise donc pas à l'appeler Troisième section. Page effectivement consultée : [Création de la Troisième section](https://www.prlib.ru/history/619386).

**H3 — Doctrine de nationalité officielle.** Une transcription du mémoire d'Ouvárov, présenté le 19 novembre 1833, expose l'association orthodoxie, autocratie et nationalité. Le document primaire est consulté dans une transcription moderne, pas sur un original manuscrit. [Texte du mémoire](https://culturolog.ru/content/view/2540/88/) ; localisation vérifiée dans la transcription, passage daté et ouverture du mémoire. La notice institutionnelle [Ouvárov](https://www.prlib.ru/node/619510) corrobore l'ancrage dans les années 1830. Il n'est pas proposé d'en faire une loi initiale de 1776.

**H4 — Bureaucratie et service de rang.** La notice institutionnelle [Table des rangs de 1722](https://www.prlib.ru/node/619004) décrit des branches militaires, civiles et de cour. Le [catalogue de l'édition de 1722](https://www.prlib.ru/item/454265) est une piste documentaire ; les seize pages n'ont pas été dépouillées. La Table des rangs ne prouve pas, à elle seule, que toute l'administration de Catherine II doit être modélisée par des bureaucrates militaires. Cette loi reste une candidate argumentée à approfondir plutôt qu'une substitution automatique certifiée.

Aucune nouvelle affirmation de frontière ou de souveraineté historique n'est établie ici. Les relations du tableau sont celles des scripts actuels du mod.

## Lot d'intégration proposé, sans application

1. Réintroduire les **sept définitions manquantes** dans un nouveau fichier de lois dédié, en préservant les lois existantes du mod. Ne pas réimporter en bloc les cinq fichiers vanilla homonymes. Ne pas dupliquer la colonisation interne restaurée par l'autre chantier.
2. Traiter la progression Troisième section / Okhrana avec le responsable de l'arbre technologique, sans octroyer de technologie avancée ni réactiver les alias pour tous les pays.
3. Réserver une éventuelle modification du profil russe à un patch borné, après stabilisation du chantier parallèle : césaropapisme comme proposition prioritaire ; bureaucrates militaires après approfondissement administratif. Garder la nationalité officielle et les polices du XIXe siècle hors du départ 1776.
4. Préserver les institutions polonaises et les profils distincts des trois sujets ; ne pas étendre les lois russes en fonction du seul suzerain.

## Contrôles et preuves

- Exécution : `python -B tools/compatibility/v115_russian_laws_audit.py --output docs/reports/compatibility/V1_15_RUSSIAN_LAWS_AUDIT_2026_11_07`, avec le Python du runtime local.
- Catalogue : 148 lois natives, 186 lois effectives du mod ; sept lois natives absentes, aucun doublon ordinaire relevé.
- Six profils examinés ; deux macros politiques développées avec leurs conditions religion/type de pays ; aucun bloc conditionnel d'activation de loi non résolu dans ce sous-ensemble.
- Les technologies initiales directes et les noms des macros technologiques sont inventoriés. Les macros technologiques ne sont pas développées ; aucune certification globale des prérequis initiaux n'en est déduite.
- 329 fichiers d'entrée lus, empreintes SHA-256 et copies conservées dans `AUDIT.json` et `inputs/`. Aucun de ces fichiers n'a changé entre sa lecture et le contrôle final de cette exécution. Ce relevé n'est pas une capture atomique de l'ensemble du workspace.
- Aucun lancement du jeu, aucune observation des lois effectivement actives et aucune validation humaine du fonctionnement pendant cette mission.

Pour une future installation : nouvelle partie 1776 en Russie puis `PLC`, contrôle des lois actives et amendements, des trois sujets, des conditions de visibilité, de la colonisation dans le lot propriétaire, puis simulation et sauvegarde/rechargement. La présence d'une définition ou une analyse de script ne remplace pas ce contrôle moteur.
