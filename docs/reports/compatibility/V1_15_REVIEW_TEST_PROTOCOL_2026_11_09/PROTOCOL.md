# Protocole unifié - missions 23, 42, 43, 44, 45

## Valider les cinq missions en revue

*1776 Age of Revolutions | Victoria 3 1.15*

Protocole unifié du 9 novembre 2026. Périmètre : missions 23, 42, 43, 44 et 45. Ce document prépare les essais ; aucune case n’est déjà validée.

| Mission | Ce que tu vérifies |
| --- | --- |
| 23 | Derniers ajustements économiques britanniques et recettes communes |
| 42 | Deux pénalités temporaires de popularité dans les événements d’agitateurs |
| 43 | Récompense « Institutions socialistes » |
| 44 | Avènement russe, coup soutenu de l’étranger, disparition du système Edo |
| 45 | Raccord annuel : événements japonais et séisme de Manille |

### Préparer une seule session de tests

1. Redémarre complètement le jeu et active le playset chargeant ce dossier du mod. Note la version exacte, le checksum s’il est affiché et les DLC actifs. La référence relue pour ce protocole est 1.15.0.
2. Lance une NOUVELLE partie en 1776. Les bâtiments de départ modifiés par 23 ne se réinitialisent pas dans une ancienne sauvegarde.
3. Commence en Grande-Bretagne. Sauvegarde immédiatement sous REVIEW_BASE_GBR_1776. Pour la Russie, le Japon et les essais de dates, utilise des parties ou des copies séparées.
4. Pour les événements tardifs, active le mode debug depuis les options de lancement du jeu. Les manipulations ci-dessous ne nécessitent aucune modification des fichiers du mod.
5. Après chaque résultat significatif, relève la date, le pays et le nom de sauvegarde. Garde une capture du résultat et des erreurs nouvelles éventuelles.

### Ordre conseillé

Grande-Bretagne : économie 23, puis récompense 43 dans une copie. Ensuite : agitateurs 42 sur un pays éligible, événements 44, puis Japon/Manille 45. Termine chaque branche par sauvegarde, rechargement et quelques jours de simulation.

> Trois réponses possibles : RÉUSSI, ÉCHOUÉ, NON TESTÉ. Un événement absent parce que ses conditions ne sont pas réunies reste NON TESTÉ. Un appel debug vérifie l’effet appelé ; il ne prouve pas, à lui seul, son déclenchement naturel.

## 1. Économie : les nouveaux réglages

*Mission 23 | Nouvelle partie britannique en 1776*

Vérifie ce lot avant toute commande debug. Les anciennes demandes de sortie d’outils en subsistance et de quatrième PM forestier sont dépassées par tes réglages du 9 novembre.

### 23-A. Répartition des industries

| État | Fabriques d’outils attendues | Verreries attendues |
| --- | --- | --- |
| Lancashire | 1 | 1 |
| Yorkshire | 4 | 1 |
| Midlands | 8 | 2 |

Dans les bâtiments, relève les niveaux de ces trois États. L’outillage doit totaliser 13 niveaux dans ce périmètre ; le déplacement demandé conserve le total. Les verreries gagnent un niveau dans chacun de ces États. Ces valeurs sont l’attendu du correctif : le chargement réel doit justement confirmer le modèle des déclarations de départ.

### 23-B. Verre et chimie

1. Les verreries des trois États utilisent « Verre plombé » et « Céramique ». Elles peuvent aussi conserver leur PM de façonnage manuel.
2. L’usine chimique des Midlands utilise déjà le procédé à chambres de plomb. Vérifie la sélection ; aucune nouvelle technologie n’a été accordée pour l’activer.

### 23-C. Routes à péage

Ouvre un réseau routier britannique : « Routes à péage » doit être sélectionné. Dans les valeurs par niveau / sans modificateurs, sa recette consomme 5 bois et aucun outil. Le total réel varie avec les niveaux, l’emploi et les effets. Vérifie aussi les sorties de transport et l’infrastructure. Les neuf États de Grande-Bretagne sont concernés par l’activation initiale ; l’Irlande est exclue de cette demande.

### 23-D et 23-E. Foresterie et subsistance

1. Camp de bûcherons : trois choix dans le groupe de base, exploitation forestière rudimentaire, scieries, scieries électriques. « Foresterie organisée » n’est plus un PM ; sa technologie reste existante.
2. Subsistance : l’atelier domestique ne produit plus d’outils. Vêtements, meubles et alcools restent les autres sorties prévues. Vérifie chaque type effectivement disponible : ferme, verger, pâturage, pêche, rizière. Note les variantes absentes comme non testées.

Simule environ 4 à 8 semaines, puis sauvegarde/recharge. Les sélections et niveaux doivent persister, sans référence de PM invalide. Relève emploi, pénuries et résultat financier des bâtiments inspectés ; aucune rentabilité fixe n’est promise par ce correctif.

> Il n’est pas nécessaire de refaire toute la passe cuivre, ports et commerce déjà acceptée. Une anomalie nouvelle doit néanmoins être signalée.

## 2. Récompense socialiste

*Mission 43 | Essai court dans une copie britannique*

Le test porte sur la récompense de l’ancien événement, pas sur l’achèvement de toute la chaîne communiste ou du DLC.

1. Charge une copie de REVIEW_BASE_GBR_1776 et mets en pause. Capture l’infobulle de bureaucratie avant le test.
2. Dans la console debug, exécute la commande ci-dessous en jouant le pays qui doit recevoir la récompense.
3. L’événement « Notre Révolution » doit s’ouvrir. Choisis « Le socialisme est construit sur de telles bases. ».
4. Vérifie le modificateur « Institutions socialistes », son icône de document positif, le bonus de +20 % de bureaucratie et une durée initiale de 3 650 jours, soit environ dix ans.
5. Sauvegarde sous REVIEW_43_REWARD, recharge et avance quelques jours. Le bonus doit rester présent avec une durée restante cohérente.

```text
event communism.6
```

> Vérifie la ligne du modificateur dans le détail de bureaucratie. Le solde net final n’a pas à être exactement l’ancien solde multiplié par 1,20 : les dépenses et les autres bonus interviennent aussi.

### Ce qui permet de conclure

RÉUSSI pour la récompense si le bon pays reçoit le bon nom, le bon effet et la bonne durée, puis les conserve après rechargement. Si tu n’attends pas dix ans, indique « expiration complète non testée ». L’autre parcours aor1776_v115_ai_progression.1 n’est pas validé par cet essai.

### Où exécuter les blocs de script des pages suivantes

La console accepte les commandes « event … » et « date … ». Les blocs contenant des accolades se lancent dans l’outil de script : ouvre « Script explorer » depuis la console, ou la commande explorer ; choisis le fournisseur Countries et le pays voulu, puis Script Runner > Effect. Colle le bloc sans ajouter « effect = { … } » autour. Les intitulés de l’outil peuvent rester en anglais.

Pour lire une variable ou l’immortalité d’un personnage, utilise son inspecteur debug. Ces outils servent uniquement aux copies de test. Les commandes et blocs fournis sont préparés d’après les scripts et l’aide de l’installation ; ils n’ont pas été exécutés dans le moteur par cet agent.

## 3. Deux événements d’agitateurs

*Mission 42 | Deux destinataires distincts à contrôler*

Il faut un projet de loi en cours et les personnages prévus par l’événement. Ne lance pas ces commandes sur le pays de départ sans vérifier son contexte.

### 42-A. « C’est un scandale ! »

1. Dans un pays avec une loi en cours de promulgation, repère un agitateur qui s’y oppose. Il faut aussi au moins un groupe d’intérêt dont la position sur le projet est neutre ou favorable.
2. Sauvegarde avant l’événement. Lance la commande 42-A ci-dessous, puis vérifie que les noms du texte et des options sont correctement remplis.
3. Choisis la première option : « Notre gouvernement est tenu de respecter les standards les plus élevés. ».
4. Le dirigeant de GI désigné par l’événement reçoit « Scandale de notoriété publique » : -50 de popularité pendant 1 825 jours, soit environ cinq ans. Vérifie la ligne de modificateur, car la popularité affichée peut aussi subir d’autres effets.
5. L’agitateur opposant reçoit son effet de lanceur d’alerte ; ce n’est pas lui le destinataire de la pénalité corrigée. Vérifie aussi l’effet affiché sur la promulgation.

```text
event agitator_legal_events.5
```

### 42-B. « Des alliés désespérés »

1. Prépare une autre copie : loi en cours, agitateur favorable au projet alors que son propre GI est neutre, et GI au gouvernement favorable au projet avec un dirigeant valide et non marginal.
2. Lance la commande 42-B. Choisis la deuxième option : « Calomniez l’opposition pour la faire sombrer dans l’oubli. ».
3. Le dirigeant gouvernemental ciblé reçoit la même pénalité temporaire de -50, pour 1 825 jours. Le dirigeant du GI ambivalent reçoit l’autre effet de rumeurs ; ne confonds pas les deux personnes.
4. Pour chaque option, sauvegarde/recharge et vérifie le bon personnage, le modificateur et sa durée restante.

```text
event agitator_legal_events.12
```

> Le trait permanent « scandaleux » est distinct du modificateur temporaire corrigé. Si les personnages requis manquent, si la loi s’est terminée ou si les noms restent vides, note le cas NON TESTÉ et conserve la sauvegarde de préparation. Une erreur issue d’un appel à vide ne permet pas de conclure sur le correctif.

## 4. Les trois événements rétablis

*Mission 44 | Russie, Japon et coup étranger*

### 44-R. Avènement russe

Nouvelle partie russe, pause et sauvegarde. Note le souverain et son état d’immortalité initial dans l’inspecteur. Pour exercer le helper de succession existant et sa branche générique, lance dans Script Runner > Effect, sur la Russie :

```text
ruler = {
    character_russia_ruler_succession_chain_effect = yes
}
```

Vérifie l’événement d’avènement, le bon nom et le bon portrait. La branche générique ciblée est russia_monarchy.12 ; si un autre événement de souverain est choisi, ce cas précis reste non exercé. Ferme normalement l’événement : temporary_immortality_var doit être nettoyée. Un souverain initialement mortel retrouve cet état ; un souverain déjà immortel ne doit pas perdre son état initial. Recharge et vérifie à nouveau. Cela exerce le raccord helper/événement, pas une succession naturelle complète.

### 44-J. Disparition du système Edo

Joue le Japon dans une copie où la hiérarchie Edo est présente. Le test isolé ci-dessous doit la remplacer par la hiérarchie par défaut et afficher la notification de disparition du système Edo pour le bon pays. L’événement est caché : aucune fenêtre de choix n’est attendue.

```text
event set_hierarchy_event.3
```

Sauvegarde/recharge et contrôle la nouvelle hiérarchie. Si la décision d’abolition est naturellement disponible, utilise-la pour vérifier aussi le parcours normal. Elle exige notamment une sortie de la sujétion, le système Edo assoupli, une légitimité d’au moins 50 et ses conditions de réforme ; un test isolé ne valide pas ces conditions.

### 44-C. Coup soutenu par une puissance étrangère

Avec le contenu DLC ep2_content actif, utilise l’action diplomatique « Orchestrer un coup d’État » depuis un pays de rang supérieur vers une cible éligible. La cible doit avoir un lobby favorable au commanditaire, un général ou amiral admissible, une force de coup suffisante et aucun coup déjà actif ; l’infobulle de l’action donne les blocages précis. Les pays ne doivent pas être en guerre entre eux.

Sauvegarde avant l’action. Dans le pays cible, vérifie ip4_coup.11 : noms du commanditaire et du chef du coup, texte complet et deux options. Teste le soutien dans une copie, la résistance dans l’autre. Le journal de coup doit s’ouvrir dans les deux cas ; le chef reçoit le soutien dans la première branche, le pays la résistance dans l’autre. Sauvegarde/recharge et vérifie le journal.

> Ne lance pas « event ip4_coup.11 » seul : ses portées viennent de l’interaction diplomatique. Si aucune cible n’est éligible ou si le DLC manque, marque 44-C NON TESTÉ. La mission 44 ne peut alors être déclarée entièrement testée.

## 5. Le raccord annuel Japon / Manille

*Mission 45 | Copies distinctes pour les dates de test*

### 45-J. Branche japonaise et garde contre la répétition

1. Lance une nouvelle partie japonaise en 1776. Sauvegarde avant manipulation. À cette date, le raccord annuel ne doit pas lancer les événements japonais tardifs ni le séisme de Manille.
2. Dans une copie, mets la date au 1er janvier 1787 avec la commande ci-dessous. Le saut de date ne simule pas les onze années intermédiaires.
3. Dans Script Runner > Effect sur le Japon, lance le raccord annuel parent avec le bloc ci-dessous. Ne lance pas directement phase1_japan_tenpo.1 : cela contournerait précisément le raccord à tester.
4. « Les leçons de la famine Tenmei » doit apparaître une fois. Fais un choix, puis vérifie la variable phase1_japan_tenmei_lessons_done dans l’inspecteur du Japon.
5. Relance le même raccord : aucun second exemplaire de cet événement. Sauvegarde/recharge, relance encore : la garde doit toujours empêcher sa répétition.

```text
date 1787.1.1.12
```

```text
trigger_event = { on_action = on_yearly_pulse }
```

### 45-M. Branche principale de Manille

Repars d’une copie fraîche, avec PHI existant, sans ruines de la cathédrale de Manille et sans variable manila_cathedral_earthquake. Mets la date au 1er janvier 1852 puis lance le même bloc de raccord parent. Dans le pays PHI, la variable manila_cathedral_earthquake doit être créée ; dans Luçon, la condition de séisme doit démarrer. Relance immédiatement le raccord : le séisme ne doit pas redémarrer. Sauvegarde/recharge, vérifie la variable et l’absence de nouveau déclenchement.

```text
date 1852.1.1.12
```

### Ce que cet essai couvre

Les deux branches du même raccord parent et leurs gardes sont exercées, à leurs dates respectives. Note séparément « raccord manuel réussi » et « impulsion annuelle automatique observée ». Pour le second témoin, laisse passer une véritable impulsion annuelle dans une sauvegarde éligible ; ne le déduis pas du seul saut de date. Les étapes japonaises 1789, 1825 et 1832-1835 ainsi que la crise Tenpō restent des extensions facultatives, pas une certification implicite.

> Si PHI n’existe pas, si les ruines sont déjà construites ou si le séisme a déjà eu lieu, le témoin Manille n’est pas préparé : NON TESTÉ. Ne supprime pas ces gardes pour prétendre avoir testé le parcours normal.

## 6. Retour de test et critères de validation

*À compléter uniquement après les essais*

Pour chaque ligne : indique RÉUSSI / ÉCHOUÉ / NON TESTÉ, puis pays, date et sauvegarde. Pour un échec, joins une capture et les nouvelles lignes pertinentes du journal d’erreurs.

| Cas | Résultat / sauvegarde |
| --- | --- |
| 23-A : niveaux outils et verre |  |
| 23-B : PM verre et chimie |  |
| 23-C : routes, 5 bois / 0 outil |  |
| 23-D : trois PM forestiers |  |
| 23-E : subsistance sans outils ; types vus |  |
| 43 : récompense +20 %, durée, rechargement |  |
| 42-A : scandale, première option |  |
| 42-B : alliés, deuxième option |  |
| 44-R : avènement et nettoyage |  |
| 44-J : hiérarchie et notification Edo |  |
| 44-C : coup, soutien / résistance |  |
| 45-J : Japon, garde, rechargement |  |
| 45-M : Manille, garde, rechargement |  |

### À joindre au compte rendu

Version / checksum : ____________________   DLC : ____________________
Playset : ____________________   Session du : ____________________
Impulsion annuelle automatique observée : oui / non
Cas faits en debug : ____________________
Nouveaux problèmes, pays et date : ____________________

### Conserver les logs de cette session

Après les essais et avant un autre lancement, conserve le dossier « Documents\Paradox Interactive\Victoria 3\logs » et les sauvegardes utiles. Ne supprime pas les anciennes preuves. L’absence d’erreurs seule ne remplace pas la vérification de l’effet visible.

### Limites et suivi

Les cinq missions restent In review pendant la préparation du protocole. Une ligne NON TESTÉE ne devient ni une réussite ni un échec. Le lot 45 conserve six références manquantes déjà identifiées : marx_events.3, japan_events.32 à .35 et on_memento_mori. Si elles apparaissent dans les logs, relève-les séparément ; elles n’ont pas été corrigées par 45. Ce protocole ne valide pas les autres missions encore en cours.

Sources relues : état courant des cinq issues GitHub, scripts installés, rapports et protocoles propres aux missions ; pour 23, le suivi économique PLAYER_FOLLOWUP_2026_11_09 prime sur les attentes forestières et outils des anciens protocoles. Le relevé des sources et empreintes est conservé à côté de la version Markdown du protocole.
