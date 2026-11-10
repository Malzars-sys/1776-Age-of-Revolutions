# Tests moteur des missions en review — 9 novembre 2026

Liste préparée à la demande du joueur. Aucun essai n'est exécuté ni accepté par ce document. Tous les contrôles ci-dessous restent à renseigner.

## Périmètre vérifié

Le [tableau Development Roadmap](https://github.com/users/Malzars-sys/projects/1/views/1), consulté directement le 9 novembre 2026, contient cinq cartes dans **In review** : **22, 23, 32, 40 et 41**. Les fiches ouvertes ont été relues par le connecteur GitHub. Les missions 24, 25, 31 et 39 sont encore dans In progress ; elles ne sont pas ajoutées discrètement à cette acceptation. Les missions déjà Done ne sont pas à refaire intégralement.

Pour **32**, conquête et annexion sont déjà acceptées par le reçu du 8 novembre : seule l'unification demeure en attente. L'ancien protocole, intitulé NOT RUN, précède ce reçu et ne doit pas effacer cette acceptation. Pour **41**, aucun fichier de gameplay ne change : la revue concerne la qualification d'un outil ; seule une observation commune des logs est utile en jeu.

## Préparation commune

- [ ] Fermer puis relancer le jeu avec la version locale actuelle du mod ; noter la version réellement affichée, le playset, les autres mods, les DLC et la langue. L'exécutable consulté est 1.15.0.
- [ ] Commencer de nouvelles parties au **1er janvier 1776**. Une ancienne sauvegarde ne vérifie pas les populations ou déclarations de guerre initiales.
- [ ] Conserver une sauvegarde de départ, puis une avant/après un transfert territorial et avant la paix dans les scénarios de guerre.
- [ ] Après chaque session utile, sauvegarder, recharger et avancer de nouveau. Noter les dates réellement simulées ; conserver les nouveaux logs pour cette session.

Organisation proposée : une nouvelle partie américaine, une nouvelle partie perse, puis une passe russe avec inspection de la Sibérie, du Caucase et de la Pologne-Lituanie. Les inspections économiques dans les pays témoins peuvent rejoindre ces sessions. Les scénarios avancés restent séparés.

## 1 — Guerre américaine, mission 22

- [ ] Au départ, les Treize Colonies sont en guerre d'indépendance contre la Grande-Bretagne. L'Espagne est neutre à l'initialisation. Les participants, objectifs et liens de sujets s'affichent sans cible invalide.
- [ ] Les fronts fonctionnent, les armées combattent et le soutien évolue sur l'échelle 0–100. Un soutien à zéro n'implique pas l'ancienne capitulation automatique.
- [ ] Lors de l'application de l'indépendance, vérifier le bénéficiaire, le lien de sujet et les notifications, puis sauvegarder/recharger. Le changement doit persister.
- [ ] Si la branche inverse est exercée, vérifier le rétablissement de la sujétion et le bon pays cible via l'objectif miroir. Sinon noter cette branche non testée.
- [ ] À la paix : vérifier indépendance/sujétion effective, participants restants, fronts, objectifs miroirs et trêves. Vérifier le résultat du journal américain. S'il reste une autre guerre, son ancienne condition de paix globale peut retarder le journal ; distinguer ce cas d'un objectif mal exécuté.

Les prêts français, Minutemen et le rework complet américain ne sont pas des critères nouveaux de 22.

## 2 — Perse et Irak ottoman, mission 22

- [ ] Nouvelle partie en Perse : l'Irak ottoman (IR1) est l'initiateur contre la Perse ; Oman est déclaré avec IR1, ARB avec la Perse. Relever les participants que le moteur entraîne réellement, le rôle du suzerain ottoman et les liens de sujets.
- [ ] Demandes correctes : **Bassora pour la Perse** (propriétaire initial IR1), **Khuzestan pour IR1** (propriétaire initial ARB), **port de traité au Fars pour Oman** (propriétaire initial Perse).
- [ ] Occuper Bassora, suivre les conditions et le délai affichés. En cas d'exécution avant la paix, vérifier son propriétaire réel, l'objectif de reprise généré pour l'adversaire, les notifications et les fronts. La guerre doit pouvoir continuer si d'autres demandes restent à résoudre.
- [ ] Si une reprise est possible, vérifier l'effet du contre-objectif ; sinon noter la branche non testée.
- [ ] Sauvegarder/recharger après le transfert, puis conclure la guerre. Vérifier détenteurs des États/du port, relations de sujets et accord de paix, sans transfert appliqué deux fois.

## 3 — Économie, mission 23

### Méthodes de production corrigées

- [ ] **Bûcherons** : quatre méthodes de base visibles — foresterie simple, foresterie organisée, scieries, scieries électriques. Les méthodes avancées peuvent être verrouillées ; contrôler leurs conditions, intrants et emplois. Activer une méthode accessible et vérifier sa production.
- [ ] **Ateliers domestiques de subsistance** : sortie d'outils présente en plus des vêtements, meubles et alcools. Vérifier les cinq formes : ferme, verger, pâturage, village de pêche et rizière, dans les bâtiments où ces ateliers sont autorisés. Noter chaque forme réellement rencontrée. Les coefficients de script sont 0,10 pour les quatre premières et 0,20 pour la rizière ; ce ne sont pas des productions nationales fixes, l'emploi et les modificateurs interviennent.
- [ ] **Caoutchouc** : le groupe conserve les charrettes et le transport ferroviaire spécifique, avec son prérequis prévu (rubber_mastication). Si seule la fiche est accessible, noter « affichage vérifié, exploitation non testée ». Ne pas certifier une production jamais activée.

### Fonctionnement des marchés

- [ ] **France, Grande-Bretagne et Treize Colonies** : inspecter une mine, un atelier d'outillage, la chaîne alliages/quincaillerie et un port/centre de commerce lorsque présents. Après quelques semaines puis quelques mois, relever emploi, entrées/sorties, pénuries et prix locaux. Vérifier les échanges initiaux de plomb West Country–Normandie s'ils sont chargés.
- [ ] **Cuivre** : prix de base 40 £, fiche du bien/de la mine, listes de PM et production réelle avec leurs employés. Ne pas confondre potentiel de construction, niveaux construits et production. C'est un témoin économique de 23 ; cela ne clôt pas automatiquement la mission 31.
- [ ] **Russie** : hubs et liaisons des centres de commerce fonctionnels, accès au marché cohérent. Observer le froid saisonnier s'il intervient ; tester le repli de hub seulement si une interruption peut être obtenue dans une sauvegarde de test.
- [ ] **Un autre marché représentatif**, par exemple Pays-Bas, Espagne, Empire ottoman ou Chine : port et centre de commerce actifs, emploi, disponibilité des navires/convois, ordres et biens réellement échangés.
- [ ] **Transport** : sur un bâtiment doté d'un PM de transport, vérifier la consommation et son approvisionnement. Après sauvegarde/rechargement et reprise du temps, PM, commandes et connexions persistent.

Une pénurie ou une faible rentabilité ne prouve pas seule une référence cassée. Noter pays, État, bâtiment, PM, niveau, emploi, prix et symptôme précis.

## 4 — Cultures restaurées, mission 40

- [ ] Les cultures **Sibérien** et **Nord-caucasien** ont un nom, une fiche, des langues lisibles et des portraits fonctionnels, sans identifiant brut. Vérifier l'anglais aussi si cette configuration est testée.
- [ ] Repères géographiques : **Sakhaline**, île au nord du Japon ; **Tchoukotka**, extrémité nord-est de l'Asie face à l'Alaska ; **Caucase**, entre la mer Noire et la mer Caspienne. Ouvrir quelques populations sibériennes et nord-caucasiennes et les cultures principales des pays concernés.
- [ ] Exemples : Sakhaline (SKH/ULT), Tchoukotka (CKC), Caucase (CAUC/ABK/CHC). Les enregistrements précis sont dans le [relevé de populations](../V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/POPULATION_RECORDS.csv). Les tailles écrites dans les scripts ne garantissent pas un même affichage après simulation.
- [ ] Témoins Russie et Pologne-Lituanie : cultures principales, religions et lois conservées. Examiner l'acceptation des populations en rapport avec les lois et traits affichés. Les langues agrégées ne doivent pas devenir russe, polonaise, iakoute, evenke ou avare. Le groupe d'héritage européen du Nord-caucasien est une adaptation documentée de cette livraison.
- [ ] Passer le premier jour puis quelques semaines : aucune disparition massive de populations concernées. Sauvegarder/recharger et retrouver au moins un groupe de chaque culture, son propriétaire et les cultures principales.
- [ ] Tester les DLC de la bêta ; faire un lancement sans le DLC concerné si disponible. Conserver les résultats séparés. Relever les erreurs mentionnant siberian, north_caucasian, aor1776_language_ ou aor1776_language_group_, en distinguant culture et ethnicité.

## 5 — Historiques optionnels, mission 41

Cette mission n'ajoute pas de pays et ne nécessite pas une partie spéciale.

- [ ] Pendant la session Russie/Pologne-Lituanie, observer le chargement, les premiers jours et la sauvegarde/reprise déjà prévus.
- [ ] Conserver toute erreur nouvelle mentionnant **BKH, MNL, SVN ou TKI**, avec la ligne et la chaîne d'appel complètes. Les historiques concernés sont `bko - bukey orda.txt`, `mnl - mingrelia.txt`, `svn - svaneti.txt`, `tki - tarki.txt`.
- [ ] Distinguer un message issu d'un historique optionnel d'un consommateur de gouvernement, de régence ou d'IA. Aucune création manuelle de ces pays n'est demandée.

La revue technique de 41 reste distincte de l'acceptation moteur globale des parents 24/25. L'absence d'erreur sur ces quatre cibles ne valide pas toute la carte.

## 6 — Cas avancés restant à couvrir

Ces cas ne sont pas validés par un simple démarrage ou quelques mois sans leur déclenchement. Une branche inaccessible reste « non testée » ; il n'est pas nécessaire d'attendre des décennies dans une campagne normale pour le constater. Une préparation de sauvegarde de test doit rester séparée du scénario du mod.

### Mission 32 : unification seulement

- [ ] Utiliser un pays réellement éligible à un coup d'unification et une cible valide ; afficher le seul objectif ne prouve pas son éligibilité normale.
- [ ] Vérifier l'infamie nulle et les conditions de candidat/cible/conflit.
- [ ] Occuper l'objectif jusqu'à son exécution : transfert avant la paix ; objectif territorial de reprise si un adversaire éligible continue la guerre.
- [ ] Essayer la reprise si possible, vérifier paix, fronts et sauvegarde/rechargement.
- [ ] Les restrictions du lien impérial restent applicables. Un cas légitimement interdit n'est pas un échec du cas générique.

Conquête et annexion, déjà acceptées, ne sont pas remises à zéro. L'unification peut rester explicitement différée si sa préparation est trop lourde.

### Mission 22 : actions et calibrages conditionnels

- [ ] Actions « rendre une revendication à un sujet » et « libérer comme sujet » : visibilité/conditions, bon sujet et destinataire, motifs d'indisponibilité, effet réellement produit quand l'action est exercée.
- [ ] Actions d'unification russe et de soulèvement polonais : aucune guerre spontanée en janvier 1776 ; leur déroulement complet reste à vérifier dans un scénario DLC éligible.
- [ ] Poids pacifistes : les deux conditions de soutien sont **strictement < 50**. Une infobulle seule ne mesure pas un poids aléatoire.
- [ ] Identité nationale : vérifier les bandes **80 / 65 / 50**, les opérateurs de chaque borne et leur progression dans le cas concerné.
- [ ] Événement électoral `.7` : seuil **strictement > 85**, pour le déclencheur et la guerre sélectionnée.
- [ ] `aviation.1` : effet immédiat **+5** sur le soutien de la bonne guerre.
- [ ] `technology_events.30` : effet immédiat **−5**, bonne guerre/cible.
- [ ] `heavenly.4` : **+50** au soutien du coup diplomatique dans chacune des deux options conservées, lorsque leurs conditions/scopes sont réunis.

Pour les effets, comparer immédiatement avant/après et séparer la variation de l'événement des mises à jour normales. Aucun déclenchement console non documenté n'est prescrit par cette liste.

## Retour utile

Pour chaque point : **réussi / échoué / non testé**, pays, date, nom de sauvegarde et résultat observé. En cas d'anomalie, conserver la sauvegarde avant/après, une capture et les nouveaux logs. Indiquer les DLC et la langue. Une confirmation groupée n'est attribuée qu'aux cas que le joueur dit avoir réellement exécutés ; aucune case de ce fichier n'est préremplie.

## Protocoles sources

- [22 — guerres et diplomatie](../V1_15_ISSUE22_WAR_DIPLOMACY/REVIEW_2026_11_09/RUNTIME_PROTOCOL.md), complété par son REPORT.md pour les treize calibrages.
- [23 — fournisseurs de PM](../V1_15_ISSUE23_DUPLICATE_PM_PROVIDERS_2026_11_09/RUNTIME_PROTOCOL.md) et [contrôles de marché](../V1_15_ISSUE23_ECONOMY_AUDIT_2026_11_08/RUNTIME_PROTOCOL.md).
- [32 — objectifs de guerre](../V1_15_ISSUE32_WAR_GOALS_2026_11_08/RUNTIME_PROTOCOL.md), lu avec le reçu partiel du 8 novembre en tête de l'[issue 32](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/32).
- [40 — cultures](../V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/RUNTIME_PROTOCOL.md).
- [41 — historiques optionnels](../V1_15_ISSUE41_DORMANT_HISTORY_2026_11_09/RUNTIME_PROTOCOL.md).

Ce document ajoute uniquement une liste de tests. Aucun gameplay, suivi de mission, statut GitHub, fichier vanilla ou attestation humaine n'est modifié.
