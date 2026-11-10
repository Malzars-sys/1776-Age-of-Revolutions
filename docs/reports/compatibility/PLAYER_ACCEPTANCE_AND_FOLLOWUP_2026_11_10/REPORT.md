# Acceptation et nouveaux ajustements — 10 novembre 2026

## Missions précédentes acceptées

Le mainteneur a explicitement confirmé avoir tout testé avec succès et demandé
de passer les missions en review dans Done. Les issues **23, 42, 43, 44, 45,
46 et 47** ont été clôturées sur GitHub avec la raison **completed**. Leur
ancien contenu est conservé sous le reçu d'acceptation ajouté en tête.

`HUMAN_ACCEPTANCE.json` contient la citation exacte et les sept états avant
clôture. Aucun numéro de build, nom de sauvegarde, date simulée, durée ni
résultat individuel d'une branche avancée n'a été inventé. L'acceptation
explicite est suffisante pour cette clôture ; aucune métadonnée supplémentaire
n'est demandée au joueur.

Les deux nouveaux changements ci-dessous, demandés après cette acceptation,
restent **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, suivis par **48 et 49**.
Ils ne sont pas rétroactivement couverts par les tests précédents.

## Deux ports initiaux — mission 48

Nouveau fichier isolé :
`common/history/buildings/1776_british_guatemala_mosquito_ports.txt`.

| État et propriétaire | Port | Méthode initiale | Capacité nominale à plein emploi |
| --- | ---: | --- | --- |
| Guatemala, partie GBR | 1 | Port de base | 1 000 emplois ; 6 clippers consommés, 9 marine marchande produits ; +3 infrastructures |
| Nicaragua, partie MKT | 1 | Port commercial traditionnel | 700 emplois ; bois 9 et tissu 3 consommés, marine marchande 6 produite ; +2 infrastructures |

Les deux groupes de méthodes sont sélectionnés explicitement, dont le groupe
de données de recherche laissé désactivé. Le PM britannique a pour prérequis
`enclosed_dock_systems`, déjà recherché par GBR. Le PM MKT n'en ajoute aucun.
Aucune technologie n'est accordée ; aucun PM partagé n'est modifié.

Les déclarations préexistantes des deux portions d'État ne contenaient aucun
bâtiment. Les positions de port définies par la carte appartiennent aux bons
propriétaires : `x02073E` pour GBR et `xAD9EE8` pour MKT. Chacune utilise la
sortie navale 3026. Les limites, propriétaires, POPs et relations diplomatiques
ne changent pas. Les fichiers de POP déclarent 5 190 personnes dans le Guatemala
britannique et 44 640 dans le Nicaragua MKT ; ce ne sont pas des effectifs de
travailleurs disponibles.

Les quantités du tableau sont les flux hebdomadaires des PM à effectif plein,
sans extrapolation de rentabilité. À 50 % de l'effectif, les flux et bonus
proportionnels à la main-d'œuvre valent respectivement 3/4,5 clippers/marine et
+1,5 infrastructure pour GBR, puis bois 4,5/tissu 1,5/marine 3 et +1
infrastructure pour MKT. Recrutement, qualifications, salaires, prix et liaison
maritime effective restent à observer en jeu. Le niveau construit n'atteste
pas à lui seul 100 % d'accès au marché.

## Choix japonais — mission 49

Les **14 choix des événements 1 à 5** de
`events/phase1_japan_tenpo_events.txt` ont de vrais effets économiques ou
administratifs. Le sixième événement et son pont vers la crise Tenpō restent
identiques octet pour octet. Les dates, déclencheurs, drapeaux historiques,
gardes d'exécution unique, images, dispatch annuel et contenus natifs de 46
sont préservés.

| Événement et choix | Coût ou contrepartie | Avantage |
| --- | --- | --- |
| 1 — Constituer des réserves | Trésor −0,5 % du PIB affiché ; −10 ordres de vente de grain par État producteur pendant 2 ans ; radicalisation de 2 % des paysans ; approbation rurale −2 pendant 5 ans | **+15 points de sécurité alimentaire permanents dans chaque État actuellement possédé** ; propriétaires +2 pendant 5 ans ; réseau de réserves établi |
| 1 — Secours aux villages | Trésor −0,3 % du PIB | Sécurité alimentaire +10 points pendant 3 ans ; loyalistes populaires +2 % ; approbation rurale +2 pendant 3 ans |
| 1 — Laisser les domaines agir | Légitimité −5 pendant 5 ans ; radicaux populaires +2 % | Pas de dépense immédiate ; propriétaires +2 pendant 5 ans |
| 2 — Discipline Kansei | Radicaux paysans +2 % ; intelligentsia −2 pendant 5 ans | Autorité +10 % et légitimité +5 pendant 5 ans |
| 2 — Secours rural | Trésor −0,2 % du PIB ; bureaucratie −5 % pendant 5 ans | Sécurité alimentaire +5 points et approbation rurale +2 pendant 5 ans |
| 2 — Autonomie des domaines | Autorité −10 % pendant 5 ans | Bureaucratie +5 % et propriétaires +2 pendant 5 ans |
| 3 — Appliquer l'édit | Trésor −0,2 % du PIB ; influence −10 % et industriels −2 pendant 5 ans | Défense dans les provinces possédées +5 % et forces armées +2 pendant 5 ans |
| 3 — Prudence | Trésor −0,1 % du PIB ; autorité −5 % pendant 5 ans | Influence +10 % et industriels +2 pendant 5 ans |
| 3 — Ne pas intervenir | Légitimité −5 et forces armées −2 pendant 3 ans | Pas de dépense immédiate |
| 4 — Surveiller les greniers | Trésor −0,1 % du PIB ; bureaucratie −5 % pendant 3 ans | Sécurité alimentaire +5 points et approbation rurale +2 pendant 3 ans |
| 4 — Réserves imposées aux domaines | −10 ordres de vente de grain par État producteur pendant 1 an ; radicaux paysans +2 % ; propriétaires −2 pendant 3 ans | Sécurité alimentaire +10 points pendant 3 ans ; réserves mobilisables après les achats |
| 5 — Ouvrir les réserves | Nécessite des réserves constituées, achats terminés ; consomme le drapeau des réserves mobilisables | +10 ordres de vente de grain par État pendant 1 an ; loyalistes populaires +2 % ; ruraux +2 pendant 3 ans ; les greniers permanents sont conservés |
| 5 — Réquisitionner les stocks accaparés | Trésor −0,2 % du PIB ; industriels et propriétaires −2 pendant 3 ans | +5 ordres de vente de grain par État pendant 1 an ; ruraux +2 pendant 3 ans |
| 5 — Laisser agir les autorités locales | Légitimité −5 pendant 3 ans ; sécurité alimentaire −5 points pendant 2 ans ; radicaux populaires +2 % | Pas de dépense immédiate ; propriétaires +2 pendant 3 ans |

Les modifications de population emploient le script value existant
`small_radicals`. La capture utilisateur affiche 2 % pour cette valeur. Les
réactions de groupe s'ajoutent aux autres sources d'approbation existantes.

### Portée de la protection alimentaire et du grain

`state_food_security_add = 0.15` ajoute **15 points**, affichés comme un
pourcentage par le moteur. Ce n'est pas un coefficient de 0,85 appliqué aux
dégâts de toutes les conditions de récolte. La sécurité alimentaire agit sur
la faim, conformément au concept vanilla ; les effets climatiques sur les
rendements agricoles et les infrastructures ne sont pas modifiés.

Le bonus permanent est ajouté directement aux États actuels, sans expiration.
Il ne s'étend pas automatiquement à de futures conquêtes. La protection
alimentaire limite la vulnérabilité ; elle ne supprime pas l'ouverture
historique de la crise Tenpō ni son journal.

Les achats sont représentés par un retrait temporaire d'ordres de vente et un
coût au Trésor ; la distribution emploie l'effet inverse. Le prix est calculé
par le marché. Aucun prix fixe ou pourcentage de hausse/baisse n'est promis.
Ce modèle n'est pas un inventaire physique de tonnes de riz : le drapeau de
réserves représente des stocks d'urgence mobilisables une fois, et le délai
interdit de les distribuer avant la fin de leur constitution. Les greniers
représentent une infrastructure durable, pas des sacs de grain conservés
intacts pendant plusieurs décennies.

Deux nouveaux fichiers FR/EN fournissent les 15 noms de modificateurs et les
quatre infobulles effectivement consommées. Quatre libellés de choix sont
précisés dans chacune des localisations existantes. Titres, descriptions et
ambiances restent inchangés. Tous les fichiers de localisation gardent leur
BOM UTF-8 ; aucun texte de développement n'entre dans les événements.

## Vérification et périmètre

- **25/25 contrôles candidats puis 25/25 contrôles installés** : scripts,
  références des modificateurs, types natifs, icônes, FR/EN, bonus permanent,
  coûts négatifs, stock mature/consommé, garde DLC et pont Tenpō, deux ports.
- Audit économique effectif : **26 210 références**, aucune cible manquante ou
  ambiguë, aucune erreur de parsing, PM initial hors groupe ou incompatibilité
  de prérequis entre méthodes du même bâtiment.
- TECH : **six constats GBR et onze MKT préexistants**, aucun nouveau ni retiré.
  Ce n'est pas un PASS global TECH ; les anciennes dettes ne sont pas masquées
  par des dons de technologies.
- **Sept fichiers de gameplay/localisation installés** : trois existants
  modifiés et quatre nouveaux. Candidats et installation ont les mêmes octets.
  Sources vanilla capturées et HEAD/index restent inchangés. Aucun travail Git
  d'écriture, publication ou lancement du jeu dans cette passe.

La première protection globale a correctement signalé un changement concurrent
hors manifeste : `common/journal_entries/02_acre_dispute.txt`. Son constat
d'échec est conservé dans `SOURCE_PROTECTION.json`. La révision R2 sépare cette
différence de nos sept fichiers, capture sa version courante sans l'écrire et
constate sa préservation. Aucun auteur n'est inféré. Les **2 528 sources
préexistantes** deviennent 2 532 par les seuls quatre ajouts du manifeste.
Le fichier Acre reste hors mission et n'a pas été restauré depuis un état ancien.

## Preuves et suivi

Lire `BASELINE.json`, `CANDIDATE_MANIFEST.json`, `before/`, `candidate/`, `diff/`,
`CANDIDATE_VALIDATION.json`, `LIVE_VALIDATION.json`, `INSTALLATION_RECEIPT.json`,
`ECONOMY_AFTER.json`, les trois rapports TECH, et `SOURCE_PROTECTION_R2.json`.
`RUNTIME_PROTOCOL.md` ne concerne que les nouveaux ports et choix ; aucun
nouveau relevé détaillé de sauvegarde n'est exigé.

Le suivi GitHub des sept missions acceptées est effectivement fermé en completed.
Les nouvelles issues 48 et 49 restent ouvertes pour leur propre revue. Les
outils actuels n'exposent pas de modification directe des champs Project ; la
position réelle des cartes et les éventuelles automatisations ne sont pas
attestées. Statuts demandés : Done pour les sept acceptées, In review pour les
deux nouvelles livraisons.
