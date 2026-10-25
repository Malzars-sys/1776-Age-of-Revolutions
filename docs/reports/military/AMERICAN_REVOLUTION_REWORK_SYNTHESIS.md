> **Rapport historique R1.** La livraison courante est décrite dans [la synthèse R6](AMERICAN_REVOLUTION_R6/SYNTHESIS.md) : ouverture française avant l’invitation américaine, et Minutemen à la place de la milice dans la liste des lois américaine. Les corrections R5, le financement natif, la dette à dix ans et l’appel espagnol restent intégrés. Les validations de fichiers sont distinguées des essais moteur restant à effectuer. Les mentions ci-dessous décrivent la situation avant R2.

# MIL-START & American Revolution Rework — synthèse

17 octobre 2026. Base : `main`, `f97dc56`. Travail laissé dans le répertoire courant, sans staging, commit, changement de branche ou modification de l'installation vanilla. Les modifications concurrentes MAP-2W-R2 restent sous la responsabilité de l'autre agent ; elles ne font pas partie du présent lot.

| Lot | Livrable | Statut |
|---|---|---|
| 1 MIL-START-AUDIT | corrections de quatre pays et audit américain préservé | READY_FOR_RUNTIME_VALIDATION |
| 2 BAL-USA-REVOLUTION-R1 | bonus de guerre américain réduit | READY_FOR_RUNTIME_VALIDATION |
| 3 USA-COMMANDERS-1776 | sept profils déterministes, cinq nouveaux généraux | READY_FOR_RUNTIME_VALIDATION |
| 4 CONTENT-USA-DESIGN | cinq systèmes spécifiés, dépendances et tests | DESIGN_ONLY |
| 5 MIL-CAVALRY-AUDIT | statistiques, exposition et proposition séparée | AUDIT_AND_PROPOSAL_ONLY |

**Aucun de ces statuts signifie validation moteur.** Aucun lot n'est marqué PASS_RUNTIME_USER_VALIDATED. L'anomalie navale américaine découverte reste ouverte.

## A. Armées de départ

Les technologies, lois, populations et relations coloniales des cinq pays sont conservées.

| Pays / TAG | Réguliers avant → après | Conscrits avant → après | Flotte avant → après |
|---|---|---|---|
| États-Unis / USA | 12 mousquets + 1 canon de campagne → inchangé | 15 mousquets non levés → inchangé | 5 caravelles → inchangé |
| Nouvelle-Grenade / SC2 | 23 ligne + 6 irréguliers + 5 cuirassiers → 23 mousquets + 6 irréguliers + 5 lanciers | 0 → 0 | 0 → 0 |
| Río de la Plata / SC4 | 6 ligne + 1 cuirassier → 6 mousquets + 1 lancier | 0 → 0 | 1 caravelle inaccessible → 0 |
| Brésil / BRZ | 1 ligne + 2 irréguliers + 1 cuirassier → 3 irréguliers + 1 lancier | 0 → 0 | 9 → 9 |
| Portugal / POR | 18 ligne + 4 dragons + 2 canons → 18 mousquets + 4 dragons + 2 canons | 30 ligne → 23 mousquets | 12 → 12 ; vaisseau de ligne remplacé par caravelle |

Les mousquets requièrent light_infantry_tactics : disponible chez SC2/SC4/POR, absent au Brésil, qui reçoit des irréguliers. Les lanciers sont un repli technique disponible, pas une affirmation que tous les cavaliers coloniaux étaient des lanciers. Le plan portugais 9/8/6 conscrits est prudent ; les capacités moteur exactes restent à mesurer. Le commandement portugais peut aussi demander une promotion volontaire après la levée complète.

Six noms de formations sont remplacés par des noms coloniaux en FR/EN. Les dates et sources, les populations régionales, les capacités et la provenance Git sont détaillées dans [MIL_START_AUDIT/REPORT.md](MIL_START_AUDIT/REPORT.md), avec inventaires BEFORE/AFTER et contrôles JSON.

MIL-USA-1776 était identique à la version intégrée dans main au début du travail. Le lot 1 a conservé le fichier entier. Le lot 3 change ensuite les créations de personnages, **sans modifier le texte ni les données des formations américaines** ; leurs empreintes sont vérifiées séparément. Le rapport MIL-USA antérieur reste intact.

## B. Liberty Or Death!

| Champ | Avant | Après |
|---|---:|---:|
| Attaque / défense | +20 % / +20 % | 0 / 0 |
| Instruction | +50 % | +15 % |
| Récupération du moral | +50 % | +15 % |
| Perte de moral | −35 % | −10 % |
| Dégâts de moral | +25 % | 0 |
| Désir de liberté, valeur additive | +0,35 | +0,35 |
| Revenu fixe | +60 000 | 0 |

Durée et conditions du journal inchangées : activation pendant la guerre contre le suzerain britannique, retrait lors de la résolution à la paix. Aucun renforcement britannique. Le retrait du revenu est une modification économique majeure à vérifier ; aucune aide étrangère fictive ne le remplace. Le journal et les événements financiers hérités ne sont pas réécrits dans R1. [Rapport et protocole de campagne](BAL_USA_REVOLUTION_R1/REPORT.md).

## C. Commandants

Washington reçoit persistent + défense de base ; Hopkins direct. S'ajoutent Lee (défense de base), Ward (cautious + sickly), Putnam (brave), Schuyler (meticulous) et Greene (inexperienced). Les profils utilisent les traits existants et désactivent leur génération aléatoire initiale ; la progression ultérieure reste native.

Washington, Lee, Ward et Putnam sont affectés à l'armée existante ; Hopkins à la flotte. Schuyler et Greene sont disponibles sans création de troupes ou d'une armée supplémentaire. Le moteur doit confirmer le maintien de ces deux disponibilités. Les cinq nouveaux généraux ont le rang de jeu 1, avec un coût total nominal de 50 bureaucratie ; ce n'est pas une traduction littérale des grades historiques.

Aucun personnage n'est promu expert à partir de sa célébrité ultérieure. Les âges, nominations, rôles, traits et sources sont dans [USA_COMMANDERS_1776/REPORT.md](USA_COMMANDERS_1776/REPORT.md). Les commandants des autres pays restent inchangés.

## D. Mécaniques révolutionnaires

| Proposition | Résultat de conception | État |
|---|---|---|
| Minutemen | variante nationale du modèle d'armée, plafonds compatibles avec les 13 réguliers ; pas de copie des effets de sécurité intérieure | planifiée |
| Ferveur | score borné, événements de victoire/défaite et décisions, trois effets de moral exclusifs ; pas de décroissance par le seul temps | planifiée |
| Aide française | dons, livraisons et principal séparés ; transfert financé, accord bilatéral, échéancier après grâce ; remplacement de la chaîne héritée indispensable | planifiée |
| Échos internationaux | sélection de destinataires et de relais, choix locaux, aucun destin révolutionnaire imposé | planifiée |
| Fondateurs | existence, vie, disponibilité, emploi et âge contrôlés ; options liées à une fonction réelle | planifiée |

Le [rapport CONTENT-USA-DESIGN](CONTENT_USA_DESIGN/REPORT.md) fournit les sources, les données observables, les calculs, les cas d'échec, les fichiers envisagés et l'ordre d'implémentation. Les mesures de pertes et de ravitaillement fines ne sont pas inventées lorsque leur déclencheur n'est pas démontré. Aucun nouveau script périodique, loi, journal ou événement actif n'est introduit par ce lot de conception.

Le registre financier est prioritaire avant toute refonte narrative : le système existant peut prélever 57 700 sur 84 mois et infliger 25 d'infamie sans registre de prêts. Il reste une dette héritée visible, pas une fonctionnalité historique validée. Les textes de nouveaux journaux demeurent à la première passe technique interne ; la seconde passe immersive FR/EN suivra la validation humaine de leurs prototypes.

## E. Cavalerie

| Unité | Attaque/défense actuelles | Proposition P1 | Rôle proposé |
|---|---:|---:|---|
| Lanciers | 16 / 10 | 16 / 10 | cavalerie accessible et économique |
| Dragons | 20 / 24 | 22 / 18 | polyvalence |
| Hussards | 24 / 18 | 18 / 12 | mobilité, exploitation et poursuite |
| Cuirassiers | 32 / 28 | 28 / 20 | choc lourd coûteux, protection relative |

**Proposition non installée.** Moral, ravitaillement, mobilité, coûts, déblocages, méthodes, améliorations et risques sont dans [MIL_CAVALRY_AUDIT/REPORT.md](MIL_CAVALRY_AUDIT/REPORT.md). Les 117 pays et 505 bataillons exposés justifient un lot mondial séparé. Le CSV permet de sélectionner les pays de test sans supposer que tous ont la technologie du type qui leur est scripté.

## F. Vérifications et limites

Le validateur reproductible `tools/validate_mil_start_american_rework.py` est en lecture seule. Résultat final : **96 contrôles statiques réussis, aucun échec**, détails dans [AMERICAN_REVOLUTION_REWORK_VALIDATION.json](AMERICAN_REVOLUTION_REWORK_VALIDATION.json). Les cinq rapports ont chacun un fichier de validation distinct ; les contrôles documentaires des lots 4/5 ne sont pas des tests de fonctionnalités installées.

Contrôles : syntaxe des fichiers touchés ; types et déblocages ; quantités exactes ; conservation des formations américaines par empreinte ; conservation des autres pays dans les fichiers partagés ; pays/technologies/populations inchangés ; modèles, traits, naissances et scopes ; 16 nouvelles clés uniques par langue avec BOM ; journal, événements, lois, unités et diplomatie protégés ; modificateurs voisins inchangés ; index et HEAD inchangés. Le contrôle des espaces ajoutés passe après retrait d'une ligne vide indentée.

Anomalies conservées et limites :

1. **NAV-USA-TECH** : les cinq caravelles américaines requièrent enclosed_dock_systems, absent au départ. L'audit élargi initial a détecté cet échec ; il n'est pas effacé sous une prétendue réussite globale des déblocages. Les unités terrestres américaines sont compatibles. La flotte reste intacte en attendant un examen naval moteur distinct.
2. BRZ et SC4 héritent d'une armée professionnelle malgré un prérequis absent ; lois préservées. Une activation religieuse mal nommée chez SC2/SC4 reste hors lot militaire.
3. Le calcul des conscrits portugais ne garantit pas les capacités exactes après restrictions d'emploi et arrondis. La réduction américaine 80 → 19 signalée auparavant n'a pas été reproduite en jeu par l'agent.
4. Revenu américain supprimé, coût de cinq commandants et approvisionnement de l'artillerie doivent être testés ensemble. Aucun rendement de marché n'est simulé statiquement.
5. Les soutiens franco-espagnols de la guerre initiale et la chaîne de dette française sont des héritages à traiter dans un lot spécifique ; leur conservation ne signifie pas validation historique.

L'installation vanilla n'a été consultée qu'en lecture. Aucun fichier cartographique, impérial, de population du Saint-Empire ou outil MAP-2W n'est dans le manifeste d'écriture de ce travail. L'arbre de travail contient leurs changements concurrents : ne pas le remettre à zéro pour isoler ce lot.

## G. Guide moteur

1. **Nouvelles parties à la date de départ 1776**, successivement USA, SC2, SC4, BRZ et POR. Conserver une sauvegarde à la pause, après un jour, une semaine, un mois et trois mois. Les anciennes sauvegardes ne relisent pas automatiquement les créations historiques.
2. Panneaux **Armée/Formations**, infobulles des types, bâtiments militaires et conscription : USA 13 réguliers + 15 conscrits potentiels non levés ; SC2 7/18/9 dans les trois formations ; SC4 7 ; BRZ 4 ; POR 24 + 23 potentiels (9 Douro, 8 Beira, 6 Estremadura). Distinguer nombre de bataillons et hommes employés. Consigner toute disparition, conversion automatique ou différence entre potentiel et capacité réelle, avec sa date.
3. Panneau **Marine** : BRZ 9 ; POR 12 dont 8 caravelles, 3 galères et 1 frégate ; SC4 aucune flotte scriptée ; USA 5 caravelles conservées. Examiner pour USA la conservation des navires et les options de construction/remplacement, sans ajouter une technologie de test à la partie de référence.
4. Panneaux **Lois/Technologies/Population** : vérifier les lois héritées, déblocages des nouveaux types et absence de population ajoutée. Pour POR, lever les trois contingents puis comparer le remplissage et les centres après un mois. Ne pas considérer une pénurie d'hommes ou d'armes comme une preuve immédiate d'erreur de syntaxe.
5. USA, panneau **Commandants** : 6 généraux et 1 amiral ; contrôler noms, âges, traits, quatre affectations à l'armée, Hopkins à la flotte, Schuyler et Greene disponibles. Refaire sur trois graines de création. Réaffecter volontairement les deux réserves sur une sauvegarde de test. Contrôler budget et bureaucratie avant/après ; les compétences peuvent évoluer ensuite selon le moteur.
6. USA, panneau **Budget**, détails des unités et **Journal** : revenu +60 000 absent ; bonus guerre +15 % instruction, +15 % récupération, −10 % perte de moral, aucune attaque/défense générale. Noter les effets séparés des chefs et lois. Surveiller prix des armes/artillerie, importations et dette aux mois 1/3/6/12.
7. Tester séparément victoire américaine et paix sous suzeraineté : bonus guerre retiré dans les deux cas, application des modificateurs d'issue existants. Observer l'événement financier français .2 après victoire, et .1/.4 selon la branche héritée ; aucun nouvel événement Minutemen, Ferveur, Échos ou Fondateurs n'est attendu dans cette livraison.
8. Pour juger l'équilibre, jouer/observer trois campagnes USA et trois GBR jusqu'à l'issue ou trois ans, mêmes paramètres et versions de mod. Relever forces survivantes, pertes, territoire, finances et intervention des alliés. Une campagne gagnée ne valide pas une probabilité de victoire.
9. Lire les journaux d'erreurs de la session lancée après ces modifications, en distinguant erreurs nouvelles et dette antérieure. Ne pas prendre des journaux d'un ancien lancement pour une preuve moteur actuelle. En cas de disparition initiale, fournir sauvegardes avant/après et nombre exact ; ne pas corriger en ajoutant des bataillons jusqu'à masquer le recalcul.

Après confirmation humaine des résultats, compléter les statuts runtime des lots concernés et traiter les points ouverts dans leurs lots propres. Le lot de conception doit garder ses propres critères avant activation.

## Nouvelle vérification après réception identique de la mission

Le document reçu dans la pièce jointe `64db9239-b18d-4826-9d33-dca9e92300ee` est identique octet pour octet au précédent. Les empreintes des neuf fichiers de jeu correspondent toujours au manifeste de livraison ; aucun changement fonctionnel n'est réappliqué.

Le dépôt a avancé indépendamment jusqu'à `d0763d6f6f970bd18e8e4ffedd8adcd36cb33e34`. Le validateur conserve `f97dc56` comme référence historique des corrections, mais vérifie désormais la stabilité de HEAD pendant son exécution plutôt que d'interdire toute intégration ultérieure par l'utilisateur. Il renvoie également STATIC_VALIDATION_FAILED si un contrôle échoue.

Nouvelle exécution : **96 contrôles réussis, aucun échec**. Le fichier de validation indique la révision effectivement contrôlée. NAV-USA-TECH reste ouvert, les tests moteur restent à faire et les lots de conception conservent leurs statuts. Aucun fichier de jeu ni fichier du chantier concurrent n'a été modifié pendant cette nouvelle vérification.
