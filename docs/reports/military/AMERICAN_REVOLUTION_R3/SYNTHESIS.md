# American Revolution Rework R3

> **Rapport historique.** Le système courant est décrit dans [la synthèse R4](../AMERICAN_REVOLUTION_R4/SYNTHESIS.md). Les montants, le financement périodique scripté et l’entrée espagnole ci-dessous sont remplacés. Les essais utilisateur R3 ont aussi révélé des erreurs moteur corrigées dans R4.

18 octobre 2026. **Implémenté ; validation moteur et rendu en jeu non effectués.**

Cette passe remplace le financement R2 et son ancien déclenchement par une
demande américaine volontaire, un traité de crédit et une dette suivie. Les
rapports R1/R2 conservent leur valeur historique ; leurs montants de subsides,
limites de six tranches et calendrier d'offre automatique ne décrivent plus
le système courant.

## Parcours américain

1. Au lancement, seul le journal de ferveur est ajouté par l'historique.
2. Après **trois jours écoulés**, un événement américain présente la
   correspondance : depuis le 1er janvier, cela vise le **4 janvier 1776**.
   Son option ouvre « Les voies discrètes du secours ».
3. Le bouton du journal ouvre le choix des promesses américaines. Aucune
   demande française n'est lancée automatiquement par les pulsations.
4. Le Congrès propose l'un de deux crédits. La France accepte ou refuse.
5. Une approbation française adresse un événement d'offre au Congrès. Son
   acceptation crée **un traité natif ratifié**, visible en diplomatie.
   Le refus ne crée ni dette ni obligation.

L'offre est donc présentée par un **événement**, puis transformée en traité
actif après consentement. Ce n'est pas un brouillon natif laissé sans envoi,
et ce n'est pas une proposition envoyée par la fenêtre native de rédaction
des traités : aucun effet natif d'envoi de cette proposition n'a été établi.

| Promesse et secours | Crédit modéré | Crédit renforcé |
|---|---:|---:|
| Avance monétaire hebdomadaire | 14 000 £ | 21 000 £ |
| Intérêts à la clôture | aucun | 5 % du capital, une seule fois |
| Armes légères transférées par la clause native | 6 unités | 12 unités |
| Artillerie transférée par la clause native | 1 unité | 1 unité |
| Instruction / gain d'expérience américains | +10 % / +10 % | +10 % / +10 % |
| Coût français des biens militaires pour les instructeurs | +5 % | +5 % |
| Contrepartie diplomatique | obligation | obligation |

Les chiffres monétaires sont des valeurs d'équilibrage héritées de l'audit
R2, pas des montants historiques convertis en livres sterling : déficit USA
observé autour de 26 585 £ par semaine et excédent français initial autour
de 53 088 £ dans la dernière sauvegarde examinée. Ces deux niveaux couvrent
approximativement la moitié ou les trois quarts du déficit avant les effets
de prix et de mobilisation. Ils ne garantissent pas l'équilibre budgétaire
ni la survie américaine jusqu'en 1778.

Le traité a une **période d'engagement de dix ans**. Les clauses de secours
cessent à la fin de la guerre ou après le **3 septembre 1783**, y compris si
la guerre dure davantage. La clause de reconnaissance de cette dette
révolutionnaire cesse également après cette date ; le **pacte de dette**
distinct conserve la créance jusqu'au paiement ou à la répudiation.
La période d'engagement d'un traité natif n'est pas assimilée à une date
automatique d'expiration de toutes ses clauses.

Une décision de récupération permet de recevoir l'événement d'ouverture
après le 4 janvier si celui-ci a été manqué. Elle n'accepte pas un prêt.
Un refus de négocier impose un délai de 90 jours.

## Comptabilité et remboursement

Le [fonctionnement interne](TECHNICAL_DESIGN.md) détaille les scopes et les
limitations. Chaque avance débite réellement la France du même montant que
celui ajouté aux réserves américaines ; le capital augmente seulement après
ce versement. Les armes et les instructeurs constituent une aide distincte
et ne sont pas transformés en dette.

**Conséquence dans le budget :** ces crédits sont des avances de trésorerie,
pas une recette fiscale ni une ligne native de subvention hebdomadaire. Le
solde ordinaire affiché peut rester déficitaire, même quand les réserves
reçoivent les avances. Aucun revenu américain gratuit n'est réintroduit.

L'absence de défaut et la couverture de chaque paiement par les réserves
françaises sont contrôlées. Une absence de réserves suspend les avances et
n'augmente pas le capital. Le versement initial et les versements du pacte
sont protégés par un verrou temporaire contre les doublons. Un accord resté
vide peut être fermé après la fin du secours, sans bloquer les futurs prêts.

« **Accord de remboursement différé** » est aussi une interaction générique,
utilisable par d'autres pays : prêt accepté de **10 000 £ sans intérêts**,
avec un seul créancier en cours par débiteur. Un créancier peut financer
plusieurs débiteurs. La clause de traité générique permet de reprendre cet
engagement déjà ouvert dans un traité ; elle n'invente pas un prêt implicite.

Quand le débiteur est en paix, son créancier dispose de « **Réclamer le
remboursement de la dette** ». Le débiteur peut :

- payer le capital et les intérêts convenus ; la somme est versée au
  créancier et l'accord est soldé ;
- refuser : **+10 d'infamie et −40 de relations** avec ce créancier. Le crédit
  cesse, le montant répudié et son créancier restent enregistrés. Cette
  créance ne peut plus déclencher une série de sanctions répétées.

Un nouveau prêt volontaire reste possible ; son principal correspondra à
un nouveau versement effectif. Les subsides des versions précédentes ne sont
jamais convertis rétroactivement en dette.

## Intervention française et espagnole

[Join Ongoing Wars](https://steamcommunity.com/sharedfiles/filedetails/?id=3015811655),
de **The Lizerd King**, est intégré avec son icône et ses crédits. Son auteur
autorise publiquement l'intégration. L'action et la clause utilisent un même
effet de participation aux guerres en cours. L'adaptation retire la condition
de voisinage terrestre qui aurait bloqué la France et vérifie aussi les
trêves avec les ennemis effectifs. Le statut de colonie américaine n'empêche
plus le soutien à sa guerre d'indépendance.

| Date du tirage annuel | France | Espagne |
|---|---:|---:|
| 1776 | 10 % | 0 % |
| 1777 | 45 % | 10 % |
| 1778, avant l'échéance française | 75 % | 25 % |
| 1779, avant l'échéance espagnole | déjà à 100 % | 40 % |
| À partir du 17 mars 1778 | 100 % | — |
| Dernier tirage, à partir du 21 juin 1779 | — | 60 %, une seule fois |

Les premiers tirages ont lieu à une pulsation mensuelle éligible, puis sont
espacés de 365 jours. Les événements d'échéance et le contrôle mensuel
traitent les dates garanties avant ce délai. Le dernier échec espagnol
empêche de nouveaux tirages automatiques, ce qui conserve une possibilité
de neutralité. Un joueur peut toujours prendre lui-même la décision.

Ces probabilités concernent **l'IA**. Elles nécessitent encore une guerre
USA–GBR en cours, l'accès requis et l'absence de trêve ennemie bloquante ou
d'hostilité envers les États-Unis. Une France déjà en guerre contre la
Grande-Bretagne ne reçoit pas une seconde participation contradictoire.

À son entrée dans la guerre américaine, la France reçoit les objectifs :

- conquête de la part britannique des **Antilles**, si elle existe ;
- conquête de la part britannique du **Sénégal**, si elle existe ;
- **Briser la puissance britannique**, une humiliation qui exige le
  **contrôle de la capitale britannique**, sans annexion de la métropole.

Le Sénégal étant français dans le départ actuel, ce second objectif est
normalement absent. La région des Antilles regroupe plusieurs îles : le but
porte sur la part britannique de la région, pas uniquement Tobago. Il ne
modifie pas la carte ni les possessions d'autres pays.

L'Espagne reçoit ses objectifs de Floride et des Baléares uniquement lors de
son intervention, si les parts britanniques existent encore.

La stratégie française augmente fortement les objectifs d'armée, de flotte,
de navires de ravitaillement et de construction navale. Les objectifs
additionnels français sont +60 niveaux d'armée, +20 niveaux navals et +400
navires de ravitaillement ; les cibles espagnoles valent la moitié. Ce sont
des **objectifs d'investissement**, financés par leur économie, sans création
gratuite de troupes, navires ou technologies. Les pondérations françaises
des bâtiments militaires et navals sont également supérieures aux espagnoles.

La contestation par occupation de la capitale est un mécanisme natif
documenté. Le choix tactique du port, les débarquements et leur réussite
restent gérés par le moteur. **Aucun débarquement ni comportement de campagne
n'a été observé dans cette passe.** La stratégie cesse d'être éligible après
la paix avec la Grande-Bretagne.

## Départ militaire

- L'Espagne et SC1–SC4 ne sont plus les soutiens initiaux de la guerre
  américaine. Les objectifs espagnols initiaux sont retirés.
- La garnison des Antilles conserve ses **neuf unités**, leur recrutement
  et ses officiers ; seuls son quartier général et son centre de
  ravitaillement passent du Canada/Terre-Neuve à l'Amérique centrale et
  au **Guatemala britannique**.
- « La liberté ou la mort » gagne seulement **−30 % de provinces perdues
  après une défaite**. Les autres valeurs du modificateur sont conservées.

## Vérification et essai demandé

Le résultat courant est conservé dans [VALIDATION.json](VALIDATION.json).
L'audit compare les fichiers partagés à la copie de travail enregistrée avant
R3, vérifie les clauses, consentements, paiements symétriques, seuils, objectifs,
traductions et régressions R2 conservées. Les scénarios de comptabilité sont
arithmétiques ; ils n'exécutent pas le moteur. Les textes FR/EN sont présents
en UTF-8 BOM et leur rendu reste à vérifier. La passe immersive définitive
des journaux suivra la validation humaine du fonctionnement.

Pour l'essai : **quitter complètement Victoria 3**, le relancer, désactiver
le mod Join Ongoing Wars séparé s'il est coché, puis commencer une nouvelle
partie américaine. Vérifier l'événement du 4 janvier, le bouton, le choix des
promesses, l'offre française, le traité en diplomatie, les avances et le pacte
de dette. Une sauvegarde avant puis après une semaine permettra de vérifier
la variation des réserves et du principal, indépendamment du solde ordinaire.

Les essais d'intervention, de remboursement, de refus et de rechargement
figurent dans [RUNTIME_CHECKLIST.md](RUNTIME_CHECKLIST.md). Aucun résultat
joueur n'est inventé. Aucun fichier de carte, d'état, de population ou de
constitution impériale n'a été édité par cette passe. HEAD et index Git sont
préservés ; pas de staging, commit ni push.

## Sources historiques et réutilisation

- [National Archives, alliance du 6 février 1778](https://www.archives.gov/milestone-documents/treaty-of-alliance-with-france) : date du traité, distincte du seuil d'entrée en guerre.
- [Naval History and Heritage Command, H-094-2](https://www.history.navy.mil/about-us/leadership/director/directors-corner/h-grams/h-gram-094/h-094-2.html) : entrée en guerre franco-britannique en mars 1778 ; seuil retenu au 17 mars.
- [U.S. Department of State, chronologie historique](https://1997-2001.state.gov/about_state/history/time1.html) : déclaration espagnole du 21 juin 1779, date utilisée ici pour le dernier tirage.
- [National Army Museum, campagnes de la guerre américaine](https://www.nam.ac.uk/explore/american-war-independence-key-battles) : objectifs espagnols et campagnes antillaises françaises.
- [National Archives, traité de Paris](https://www.archives.gov/milestone-documents/treaty-of-paris) : 3 septembre 1783.
- [Crédits et permission de Join Ongoing Wars](../../../credits/JOIN_ONGOING_WARS.md).
