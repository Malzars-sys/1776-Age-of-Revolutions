# TECH-R2 — protocole joueur groupé

**INSTALLÉ — EN ATTENTE DE VALIDATION HUMAINE.** R1 est validé dans sa version exacte ; son reçu ne couvre pas R2. Le moteur n’a pas été lancé par l’agent. Utiliser une **nouvelle partie au 1er janvier 1776**, avec le mod courant, et observer les pays par changement de pays/observateur si nécessaire. Une ancienne sauvegarde peut conserver les anciens choix.

## 1. Technologies et témoins, avant de laisser passer du temps

Aucun savoir initial ajouté ou retiré pour les 470 pays. Pour les six pays dont les procédés changent :

| TAG | Technologies avant R2 | Après R2 | Ajouts / retraits |
| --- | ---: | ---: | --- |
| BIK | 5 | 5 | 0 / 0 |
| CAR | 7 | 7 | 0 / 0 |
| GEN | 22 | 22 | 0 / 0 |
| KND | 4 | 4 | 0 / 0 |
| RUS | 43 | 43 | 0 / 0 |
| VEN | 27 | 27 | 0 / 0 |

Contrôler les listes, pas seulement les nombres : TECH_BEFORE_AFTER.csv et STARTING_TECH_AUDIT_1776_AFTER.csv. Vérifier quelques témoins : BGT, BRX, TRT et LGE conservent leurs corrections R1 ; BGT garde sa mine native publique niveau 1 et son PM sans collecte de données. Conserver aussi les noyaux SERG et des témoins FRA/GBR/USA/CHI. Aucun effet au premier jour ne doit attribuer un paquet de technologies supplémentaire.

## 2. Sous-lots indépendants : bâtiments et procédés

Une seule partie permet ces contrôles ; chaque groupe peut être rapporté séparément. Les noms internes ci-dessous servent uniquement à identifier sans ambiguïté les recettes. Examiner leur infobulle et la liste réelle de PM du bâtiment.

| Sous-lot | Pays | État technique | Bâtiment | Ancien → nouveau PM |
| --- | --- | --- | --- | --- |
| R2-A | RUS | BREST | logging_camp | `pm_saw_mills` → `pm_simple_forestry` |
| R2-A | GEN | PIEDMONT | furniture_manufactory | `pm_lathe` → `pm_handcrafted_furniture` |
| R2-A | GEN | PIEDMONT | logging_camp | `pm_saw_mills` → `pm_simple_forestry` |
| R2-A | GEN | PIEDMONT | tooling_workshop | `pm_pig_iron` → `pm_crude_tools` |
| R2-A | VEN | ISTRIA | tooling_workshop | `pm_pig_iron` → `pm_crude_tools` |
| R2-B | KND | CEYLON | government_administration | `pm_horizontal_drawer_cabinets` → `pm_simple_organization` |
| R2-B | VEN | VENETIA | government_administration | `pm_horizontal_drawer_cabinets` → `pm_simple_organization` |
| R2-B | KND | CEYLON | railway | `pm_industrial_canals` → `pm_no_canal_network` |
| R2-B | BIK | RAJPUTANA | textile_mill | `pm_craftsman_sewing` → `pm_no_luxury_clothes` |
| R2-C | KND | CEYLON | trade_center | `pm_trade_center_trade_quantity_normal` → `pm_trade_center_trade_quantity_limited` |
| R2-C | CAR | CIRCARS | trade_center | `pm_trade_center_trade_quantity_normal` → `pm_trade_center_trade_quantity_limited` |
| R2-C | CAR | MADRAS | trade_center | `pm_trade_center_trade_quantity_normal` → `pm_trade_center_trade_quantity_limited` |

R2-A : production et recrutement des ateliers/forêts, accès au bois, aux tissus et aux outils. Les flux écrits diminuent pour bois/meubles/outils ; cela ne doit pas être masqué par des subventions ou des technologies ajoutées. Vérifier les approvisionnements voisins et les qualifications.

R2-B : administration de VEN et KND, recrutement des employés, bureaucratie et capacité fiscale. **Bureaucratie 50→10 et capacité fiscale 10→2 par niveau à activité comparable**, papier 10→0 : relever tout déficit bloquant. À Ceylan, routes traditionnelles conservées, canaux industriels désactivés, aucun rail/train actif. Le PM supprimé représentait 800 postes et 1 infrastructure par niveau à plein fonctionnement ; ne pas exiger leur maintien. À Bikaner, vêtements de base conservés, conversion en luxe désactivée, aucun nouvel artisanat inventé.

R2-C : commerce limité à Kandy et dans les deux centres CAR. Le mod applique **−50 % à la quantité commerciale** et la demande de marine marchande du PM passe de 4 à 3 par niveau à plein fonctionnement. Vérifier échanges, accès au marché et absence de blocage économique excessif. Les titres de propriété et les niveaux des centres sont conservés. Aucun résultat de prix, revenu ou emploi n’est annoncé à l’avance.

BUILDING_TECH_FIXES.csv contient tous les écarts de paramètres, y compris changement des métiers, des intrants et des sorties. Les valeurs décrivent les scripts, pas une économie déjà observée. Une méthode visible mais impossible à garder sélectionnée, un arrêt de recrutement, un déficit administratif rédhibitoire ou une pénurie persistante doivent être rapportés comme anomalie avec pays/état/bâtiment.

## 3. R2-D : alliages et absence de déblocages tardifs

Dans l’arbre, `alloysworking` doit dépendre de `shaft_mining` et `organized_workshops`, plus de `coke_smelting`. AUS/BEO/FRA/PRU/RUS/SAX/SWE gardent les alliages déjà acquis sans recevoir le coke. Les autres détenteurs CHI/GBR/MGL/XIN/YUN restent inchangés.

Comparer un témoin possédant les nouveaux parents sans avoir encore les alliages : il peut remplir leurs parents directs sans obtenir la technologie gratuitement. L’étude globale recense 93 pays dans ce cas de prérequis satisfaits, dont les détenteurs ; cela ne certifie pas les autres critères du bouton de recherche. Vérifier que bauxite/Bayer, électricité, procédés électrolytiques, vapeur et rail ne sont pas débloqués artificiellement. La recette initiale de l’usine d’alliages reste identique ; si une usine existe, inspecter intrants, recrutement et sortie, sans en construire une gratuitement pour le test.

## 4. Un mois puis sauvegarde/rechargement

Laisser tourner un mois complet. Surveiller les six pays, l’administration, le commerce et les chaînes ateliers/forêts ; noter les pénuries, déficits ou PM remplacés par défaut par le moteur. Le recrutement peut être partiel ; l’absence de plein emploi n’est pas à elle seule un échec. Vérifier les ressources réellement disponibles dans les portions nationales concernées.

Sauvegarder puis recharger. Retrouver technologies, bâtiments, PM et économie sans crash ni anomalie bloquante. Rendre un résultat par sous-lot R2-A/B/C/D avec les seules observations réellement faites. Ne pas étendre une réussite à tout l’audit mondial, aux huit historiques absents ou aux tâches territoriales SERG/WORLD.

Le lot concurrent BALKANS-01 a son propre protocole et son propre suivi. Le tester éventuellement dans la même partie ne le valide pas automatiquement : son attestation doit préciser ce périmètre distinct. RG-D-CITY reste également indépendant.
