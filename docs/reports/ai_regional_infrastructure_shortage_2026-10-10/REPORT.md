# Infrastructures régionales : correctif de la boucle de pénurie

10 octobre 2026 — dossier de travail uniquement, Victoria 3 **1.13.11**.

## Résultat et statut

Le correctif est appliqué aux scripts du mod. Les validations statiques et les
scénarios exécutant les scripts dans un interpréteur de test passent.
**Il n'a pas encore été exécuté par le moteur du jeu : la correction économique
en campagne, les performances et l'absence d'erreurs de scope restent à confirmer.**
Il n'y a donc aucun résultat budgétaire ou nombre de constructions réellement
mesuré en jeu dans ce rapport. Les anciens logs ne valident pas le correctif.

Aucun commit, push, merge, changement de version ou remplacement du Steam Build.
Les modifications préexistantes de l'icône chimique, des descriptions Steam et
des métadonnées sont conservées. Les 31 fichiers MAP-1C sont inchangés.

## 1. Diagnostic

- `building_railway` représente les infrastructures régionales, avec quatre
  groupes : routes, canaux, locomotives, wagons.
- Son score de construction était constamment de **2000**, augmenté de **10000**
  pour certains journaux. Aucun veto de pénurie n'était appliqué à ce score.
- `should_auto_expand` exigeait occupation >= 80 %, transport cher ou déficit
  d'infrastructure <= -20, et absence de construction en cours, **sans vérifier
  les intrants**. Une baisse de production due à une pénurie pouvait donc
  provoquer une nouvelle extension consommant davantage des mêmes biens.
- La hiérarchie réelle est `bg_land_transport_network` →
  `bg_private_infrastructure` → `bg_infrastructure`. Elle hérite de
  `is_government_funded = no`, de subventions initiales et du modèle de propriété
  ferroviaire vanilla. Ce n'est donc pas exclusivement un bâtiment gouvernemental.
  L'auto-extension, les décisions de construction publiques et l'investissement
  privé sont trois chemins distincts à protéger.
- Le contrôleur de début de partie/mensuel imposait le dernier PM accessible,
  sans vérifier production, commandes, prix ni accès au marché. Les poids
  statiques allaient jusqu'à **200000**, entretenant cette préférence même si
  l'approvisionnement ne suivait pas.
- Les routes, trains et wagons utilisent `most_productive`. Les canaux conservent
  leur comportement natif ; le contrôleur les limite aux dix premiers États par
  PIB. Les stratégies par défaut favorisent déjà charbon/moteurs après le chemin
  de fer et électricité après sa technologie ; certaines stratégies administratives
  favorisent plutôt les exportations de matières premières. Aucun nouveau choix
  de stratégie administrative n'est imposé : les scores des fournisseurs agissent
  indépendamment de ces variantes.
- Les anciens logs signalent aussi des positions de classement PIB hors limites
  pour les petits pays. Un test `num_states > position` protège désormais chaque
  accès ; les positions défavorables ne sont pas ignorées dans les validations.

## 2. Construction : trois protections séparées

Le trigger d'État `aor1776_ai_regional_infrastructure_shortage` exige propriétaire
IA et pénurie effective d'au moins un intrant du bâtiment régional existant.

1. **Auto-extension** : refus en pénurie pour l'IA. Les conditions précédentes
   sont conservées, y compris le seuil de déficit et l'occupation. Le pays joueur
   garde ses règles d'auto-extension antérieures.
2. **Score de construction** : multiplication par zéro en pénurie, exécutée
   **après** les bonus des journaux. Base 2000 et bonus historiques restent
   exactement identiques hors pénurie.
3. **Éligibilité native publique et privée** : `can_build_government` et
   `can_build_private` refusent de nouvelles extensions dans l'État IA en pénurie.
   Le veto protège aussi contre une décision native ignorant le score.

Un déficit sans pénurie reste constructible. Le script ne crée, ne supprime et
ne déplace aucun niveau, ne confisque rien et n'annule pas les commandes déjà
présentes dans la file. Une extension déjà engagée peut donc encore se terminer.
Les éligibilités sont évaluées selon le propriétaire de l'État : les investissements
transfrontaliers vers un État IA en crise sont également concernés.

## 3. PM soutenables et stabilisation

Les 19 candidats des quatre groupes sont contrôlés. Les technologies et principes
restent vérifiés par `can_activate_production_method`, avec conservation d'un PM
déjà actif. Aucun déblocage, coût, emploi, intrant, rendement ou visuel n'est changé.
Les poids statiques des routes/trains/wagons sont ramenés à **1**, leur valeur
native neutre. La préférence devient conditionnelle dans le contrôleur plutôt
qu'un multiplicateur technologique permanent.

Pour chaque bien réellement demandé par un candidat :

- Pas de pénurie locale et prix local au maximum **+25 %**.
- Soit marché effectivement connecté : accès >= **95 %**, non isolé, aucune
  pénurie de marché, commandes de vente **strictement positives** et réserve
  suffisante ; soit production réelle dans l'État et réserve locale suffisante.
- L'électricité exige la seconde voie : un producteur éloigné n'est pas considéré
  comme une solution à un manque local d'électricité.
- Une importation théoriquement possible ne suffit jamais à prouver l'approvisionnement.

Réserve locale : production >= 90 % de (consommation courante + demande maximale
à pleine occupation des infrastructures de cet État).

Réserve du marché : ventes >= 90 % de (achats courants + demande maximale de cet
État + demandes réservées des États déjà modifiés pendant ce contrôle).

La demande maximale est calculée à partir des **recettes existantes**, par bien,
en additionnant les maxima de chaque groupe et en multipliant par les niveaux.
Le pays réserve ensuite la demande complète des PM actifs des États modifiés.
Cela évite que dix États utilisent simultanément la même marge commerciale.
Les consommations actuelles ne sont pas soustraites : c'est volontairement
conservateur, notamment pour les bâtiments partiellement employés.

Le classement ferroviaire privilégie l'infrastructure nominale : diesel avec
principe (32), électrique avec principe (24), diesel (17), électrique et vapeur
avec principe (14), vapeur (9), premiers trains (5), aucun réseau. Le 24 d'un
électrique avec principe n'est plus ignoré au profit du 17 d'un diesel normal.

### Pénurie et récupération

- Première observation de pénurie : mémorisation, pas de changement des routes
  ou trains uniquement pour ce choc. Les extensions sont néanmoins déjà refusées.
- Deux observations consécutives, normalement espacées d'un mois : sélection
  du meilleur ensemble approvisionnable. Routes traditionnelles, absence de
  trains/wagons/canaux restent les replis sans intrants disponibles.
- Après un changement réel : **180 jours** avant une nouvelle sélection en
  situation saine. Réappliquer un PM inchangé ne prolonge pas ce délai.
- Une nouvelle pénurie persistante peut justifier un autre repli pendant ce délai.
- Aucun wagon sans train. Les canaux hors top 10 sont supprimés au contrôle
  mensuel sans attendre le délai, puisqu'il s'agit d'une réduction de demande.
- À la récupération effective, la construction normale peut reprendre même
  pendant le délai ; il ne faut pas bloquer un véritable déficit sans pénurie.

Deux observations ne prouvent pas une pénurie continue entre les contrôles.
La sévérité est celle du signal natif de pénurie, pas un nouveau seuil de prix.

## 4. Fournisseurs : soutien limité et ciblé

Les recettes demandent **12 biens** : bois, outils, calcaire, ciment, produits
pétroliers lourds, carburants raffinés, charbon, moteurs, électricité, fer, acier,
aluminium. Le contrôleur ne confond donc pas pétrole brut, carburant diesel et
produits lourds des routes asphaltées. Le fer des canaux est également inclus.

En pénurie effective du bâtiment, seuls les biens de ses **PM actifs** dont la
marge d'approvisionnement échoue génèrent une demande d'aide. La demande dure
180 jours pour ne pas disparaître immédiatement lors d'un repli.

- Score du fournisseur multiplié par **4**, sur sa valeur antérieure, sans
  effacer ses éventuels bonus natifs/historiques.
- Pas de multiplication si ce fournisseur a déjà une construction en cours ou
  souffre lui-même d'une pénurie. Sa priorité normale n'est pas supprimée.
- Vérification d'au moins un PM producteur technologiquement accessible : une
  usine d'alliages ne reçoit pas un bonus aluminium avant les procédés adéquats.
- État isolé ou pénurie strictement locale : demande uniquement dans cet État.
- Manque du marché connecté : autres États du même pays admissibles seulement
  avec accès >=95 % et sans isolement. Électricité toujours locale.
- Technologies des bâtiments, lois, potentiel minier/forestier, coûts, emploi,
  profit attendu, budgets et choix de commerce restent traités par l'IA native.
  Les recettes des fournisseurs et les stratégies commerciales sont inchangées.

**Aucune construction forcée, ressource gratuite, technologie offerte, subvention
imposée ou priorité mondiale permanente.** Si l'État isolé n'a pas la ressource,
le bonus ne lui invente pas un potentiel : le repli et la restauration de l'accès
au marché restent nécessaires. Le score n'offre aucune garantie que l'IA puisse
financer un fournisseur ni acquérir ses propres intrants.

## 5. Syntaxe vérifiée et limites du moteur

Sources primaires consultées dans l'installation locale 1.13.11 :

- `game/common/buildings/buildings.md` : portée État de `ai_value` et principe de
  `should_auto_expand`. Le document générique mentionne encore `can_build` ; les
  champs séparés sont attestés dans `common/buildings/08_monuments.txt` (767/771)
  et le centre de commerce natif/modifié, ainsi que dans l'exécutable.
- `game/common/production_methods/production_methods.md` : `ai_weight` est un
  nombre fixe, pas un score conditionnel, et `required_input_goods` contrôle
  l'accessibilité d'intrants.
- `game/common/production_method_groups/production_method_groups.md` : seules
  les options `most_profitable` et `most_productive` sont documentées. Aucune
  option inventée pour désactiver la sélection native n'est utilisée.
- `game/common/alert_types/00_alert_types.txt` : pénurie locale et commandes
  d'achat ; `00_gfx_route_graphics_values.txt` : commandes de vente comme valeur.
- `game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt` : classement
  sur `b:building_barrack.level`, variables temporaires ; valeurs natives :
  scopes sauvegardés et `scope:...var:...` ; effets natifs : `change_variable/add`.
- `game/common/defines/00_ai.txt` : base de bâtiment productif **1000**.
- `game/common/defines/00_defines.txt` : déclenchement de la pénalité de manque
  lorsque le rapport offre/demande passe sous **0,5** ; valeurs non modifiées.
- Documentation incorporée à l'exécutable : triggers de pénurie bâtiment,
  pénurie marché et pénurie locale, comparateurs de production/consommation et
  commandes. Le trigger local exclut explicitement les pénuries de tout le
  marché : il **ne remplace pas** le test du marché.

Version confirmée par `VersionInfo` et `logs/system.log`. Le hash de l'exécutable
et les positions des symboles sont enregistrés dans `VALIDATION.json`.
Cette reconnaissance des commandes et le parsing local **ne sont pas un chargement
réussi du mod dans le moteur**.

Limites et risques :

1. Le moteur peut sélectionner un PM entre deux contrôles. Le délai stabilise
   ce contrôleur, pas chaque décision autonome du moteur. Les poids neutres
   atténuent le forçage antérieur, sans constituer une interdiction native de PM.
2. Le classement utilise une infrastructure nominale sous approvisionnement
   viable. Il ne prédit pas parfaitement recrutement, salaires, pollution,
   bonus liés aux populations, contraintes automobiles ou coût des subventions.
3. Réserve prudente : certains progrès peuvent être retardés sur un marché
   tendu mais pas encore en pénurie. Il faut contrôler les États pauvres et
   les pays possédant beaucoup d'États ; la réserve ne couvre pas les décisions
   simultanées des autres pays d'un marché partagé.
4. Un recul jusqu'aux routes traditionnelles peut nécessiter plus de niveaux
   pour assurer l'accès au marché. La correction empêche d'augmenter la demande
   du bien manquant ; elle ne garantit pas une infrastructure abondante et
   bon marché en l'absence durable de production, d'emploi ou de ressources.
5. Veto de construction : bâtiments existants seulement. Le premier niveau,
   avant consommation effective des intrants, n'a pas encore de signal bâtiment.
   Les pénalités natives apparaissent/cessent progressivement ; des commandes
   engagées avant le signal peuvent persister.
6. Le soutien n'est pas un ordonnanceur de chaînes industrielles : les intrants
   propres d'une raffinerie/aciérie et les importations restent gérés nativement.
7. Les variables temporaires de secours expirent. Les compteurs de réservation
   sont remis à zéro à chaque contrôle ; aucun historique de population n'est
   modifié. Le changement mensuel peut temporairement affecter rentabilité/emploi
   comme tout changement de PM normal.

## 6. Tests réalisés

`VALIDATION.json` contient les résultats et traces des **10 familles** de fixtures.
Elles exécutent l'arbre des scripts réellement présents, avec données d'entrée
explicites, et non une deuxième implémentation indépendante de la sélection.

| Scénario | Résultat de script observé |
| --- | --- |
| Déficit sans pénurie | Construction admissible, meilleurs PM approvisionnables |
| Outils en pénurie | Aucun repli au premier contrôle ; routes traditionnelles au deuxième |
| Ciment/calcaire en pénurie | Repli vers routes à péage avec bois/outils disponibles |
| Moteurs en pénurie | Aucun réseau ferroviaire, aucun wagon |
| Bien sans production dans le marché | Le PM utilisant ce bien n'est pas activé malgré son déblocage |
| Retour à la normale | Pas de remontée prématurée ; retour après 180 jours |
| Pays humain | Aucun changement après 13 contrôles ; règles de construction préservées |
| États connectés/isolés | Repli indépendant ; aide locale ne déborde pas vers un producteur éloigné |
| Réserve de marché partagée | Une seule montée en gamme sur dix États avec marge limitée dans la fixture |
| Fournisseurs | Bonus limité, refus du bonus en file/pénurie, expiration et prérequis aluminium |

Autres contrôles : pays de 1/5/10/11 États, égalités de PIB, État riche sans
bâtiment, sortie du top 10 pendant le délai, entrée après délai, technologies
verrouillées/intermédiaires, idempotence, comparaison 24 contre 17, marge anticipée
insuffisante, références PM/technologies/triggers/valeurs, bonus historiques et
recettes conservés, absence de création de bâtiments ou de populations.

Les chocs durables des fixtures sont observés pendant huit contrôles mensuels,
la récupération pendant huit mois et le pays joueur pendant douze mois.
Les indicateurs de pénurie sont imposés comme entrées du test, sans reconstruire
l'économie du jeu. Un bâtiment qui n'est plus en pénurie en campagne doit
retrouver son éligibilité native ; une fixture prolongeant le signal ne mesure
pas le temps de décroissance réel de la pénalité.

Validations complémentaires réussies :

- `tools/validate_ai_regional_infrastructure_1776.py` : point d'entrée conservé,
  maintenant relié à la suite adaptée aux pénuries.
- `tools/validate_regional_infrastructure_permissions.py` : héritage, propriété,
  subventions et échelle des bâtiments inchangés.
- `tools/validate_diplomacy_ottoman_1776.py` : objectifs, événements, institutions,
  bâtiments/armées ottomans et indépendance des journaux toujours conformes.
- `git diff --check` : aucune erreur d'espacement ; avertissements de conversion
  LF/CRLF sans effet sur la logique.
- **3247 fichiers** contrôlés par empreinte avant/après, changements limités aux
  13 fichiers runtime préexistants autorisés et deux nouvelles définitions.

## 7. Protocole en jeu restant à exécuter

Le jeu n'était pas en cours d'exécution lors du contrôle. La session ne dispose
pas d'un contrôle natif du bureau permettant de lancer, charger et observer de
façon fiable ces campagnes. Aucun lancement, sauvegarde, manipulation de partie
ou série de mesures économiques n'est prétendu.

Pour une comparaison reproductible : utiliser deux copies isolées du mod,
respectivement avant et après correctif, version 1.13.11, mêmes autres mods et
conditions de départ ; ne pas modifier ce répertoire ni MAP-1C pour reconstruire
la version témoin. Utiliser les fixtures ci-dessus comme configurations économiques,
avec une sauvegarde témoin distincte par scénario et des modifications uniquement
dans ces sauvegardes de test si nécessaires.

Mesurer au départ puis chaque mois pendant **12 mois**, et jusqu'à **18 mois**
pour un choc suivi de récupération :

| Mesure | Avant | Après |
| --- | --- | --- |
| Niveaux d'infrastructures achevés et en file | À mesurer | À mesurer |
| Infrastructure réellement produite et déficit | À mesurer | À mesurer |
| Intrants manquants, offre/demande, prix locaux | À mesurer | À mesurer |
| Fournisseurs achevés et en file, technologies | À mesurer | À mesurer |
| Dates et groupes des changements de PM | À mesurer | À mesurer |
| Accès au marché et isolement | À mesurer | À mesurer |
| Salaires, subventions, coût de construction, solde | À mesurer | À mesurer |

Provoquer/reproduire un déficit sans pénurie, trois chocs d'intrants distincts,
une absence de production, une récupération, un pays humain et un pays IA avec
États connectés et isolés. Tester aussi un fournisseur sans technologie, une file
déjà pleine et un manque de matières premières en amont. Vérifier les trois chemins
de construction, pas seulement l'auto-extension. Observer les changements natifs
entre deux contrôles mensuels et les canaux hors top 10.

Après chargement, examiner les **nouveaux** logs pour les trois fichiers de
contrôleur/triggers/valeurs, notamment scopes SG/MG, variables, comparateurs,
éligibilités de construction et classement. Garder les écarts et les cas
défavorables dans les mesures. Une preuve d'échec à l'un de ces points exige
une nouvelle correction, pas une déclaration de réussite économique.

## 8. Fichiers du correctif

Le manifeste `PATCH_MANIFEST.json` distingue les fichiers préexistants modifiés
et les ajouts, avec leurs empreintes. Il exclut les changements préexistants de
Steam/graphismes et tous les travaux MAP.

- Construction et scores de **11 fournisseurs** : neuf fichiers dans
  `common/buildings/`, dont `11_private_infrastructure.txt` pour les protections.
- Poids IA uniquement : trois fichiers `common/production_methods/` des routes,
  trains et wagons. Les PM de canaux et tous les groupes sont inchangés.
- Contrôleur : `common/scripted_effects/1776_ai_regional_infrastructure_effects.txt`.
- Ajouts : `common/scripted_triggers/1776_ai_regional_infrastructure_shortage.txt`
  et `common/script_values/1776_ai_regional_infrastructure_shortage.txt`.
- Outillage : validateur actuel, point d'entrée de validation antérieur et
  générateur de patch utilisé avec `apply_patch` pour cette intervention.
- Rapport, empreintes avant intervention et résultats JSON dans ce dossier.

Le hook de début de partie/mensuel reste inchangé. Cartes, historiques,
populations, diplomatie, unités, journaux, recettes, technologies et localisations
n'ont pas été modifiés par ce correctif.
