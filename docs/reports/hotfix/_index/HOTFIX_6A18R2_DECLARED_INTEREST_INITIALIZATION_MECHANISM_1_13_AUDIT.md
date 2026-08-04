# HOTFIX-6A.18R2 — Audit du mécanisme d'initialisation des intérêts 1.13

## 1. Phase, date et résultat

- phase : `HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT`;
- date : 4 août 2026;
- branche : `hotfix-dlc-audit`;
- HEAD initial et final attendu :
  `f9635de7fefbfa1790e43930e39847acd971935d`;
- message du HEAD :
  `Validate declared interest history runtime for 1.13`;
- nature : audit statique et documentaire en lecture seule;
- gameplay : inchangé;
- runtime : aucun nouveau lancement, aucune console et aucun nouveau journal.

Le moteur 1.13 expose bien un effet script enregistré nommé
`add_involvement`. Sa signature est prouvée et deux événements vanilla
l'utilisent. Cet effet ajoute toutefois une valeur à l'**implication
courante**; il ne modifie pas l'**implication cible**, n'enregistre pas une
source durable et ne définit pas directement un rang. Il n'est donc pas un
remplacement sémantiquement équivalent de `add_declared_interest`.

Les intérêts durables de 1.13 découlent de sources naturelles calculées par le
moteur : capitale et voisinage de capitale, possession et revendications, PIB,
armées, flottes, articles de traité et pactes diplomatiques, notamment les
relations de sujet. Aucune API générique ne permet d'ajouter une source
historique personnalisée à ce calcul. Aucun exemple vanilla/DLC n'emploie
`add_involvement` dans `common/history` au jour 1.

Une conversion automatique des 91 lignes modifierait donc soit une valeur
courante temporaire, soit les traités, pactes, sujets, possessions,
revendications ou forces militaires du setup 1776. Elle changerait
l'équilibrage et ne satisfait pas les conditions de sélection d'une correction.

## 2. Préflight et état Git d'entrée

Le préflight obligatoire passe :

| Contrôle | Résultat |
| --- | --- |
| racine | fork exact |
| branche | `hotfix-dlc-audit` |
| HEAD | `f9635de7fefbfa1790e43930e39847acd971935d` |
| message | exact |
| rapport 6A.18Q dans le HEAD | présent, verdicts requis présents |
| arbre suivi | propre |
| index staged | vide |
| non suivis | seulement `bject` et les sept recherches technologiques protégées |
| `git diff --check` | PASS |
| stash | exact et inchangé |
| Victoria 3 / Dowser / launcher Paradox | aucun processus |

Le premier filtre de processus a produit un faux positif en reconnaissant le
texte de sa propre ligne de commande PowerShell. Le contrôle a été immédiatement
refait en excluant les shells et le PID courant et en appliquant uniquement les
trois critères autorisés : `victoria3.exe`, `dowser.exe` ou chemin contenant
`Paradox Interactive\launcher`. Ce second contrôle est vide.

Stash protégé :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

## 3. Sources lues

Les sources obligatoires ont été lues avant écriture :

- rapports 6A.18, 6A.18R et 6A.18Q;
- index global, roadmap canonique et prompt courant;
- matrice des blocs et index CSV des rapports;
- trois inventaires canoniques;
- changelogs complets du fork et de la source hotfix;
- journaux complets de la session 6A.18Q;
- scripts, métadonnées Markdown, définitions, GUI et localisations anglaises
  nécessaires du vanilla 1.13 installé;
- chaînes ASCII lisibles de `victoria3.exe` nécessaires à la distinction entre
  effet script, commande debug et tâche moteur;
- occurrences autorisées dans les événements égyptien et indochinois.

Arbres consultés en lecture seule :

- fork : `1776_Age_of_Revolutions_fork`;
- source : `1776_Age_of_Revolutions_hotfix_source`;
- vanilla : `C:\Games\Victoria 3 The Great Wave\game`;
- journaux :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs`.

L'annonce officielle de la mise à jour 1.13 décrit le remplacement du système
binaire par des niveaux d'implication construits par patrouille côtière,
traités ou implantation territoriale. Cette description concorde avec les
définitions et scripts installés :
[annonce officielle de la mise à jour 1.13](https://store.steampowered.com/news/posts/?enddate=1776952804&feed=steam_community_announcements).

## 4. Validation des CSV canoniques

Les CSV ont été chargés intégralement avec `Import-Csv`; aucun découpage naïf
sur les virgules n'a été utilisé.

| CSV | Lignes de données | Colonnes | Lignes mal formées | Lignes vides | Clés dupliquées | SHA-256 d'entrée |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv` | 541 | 21 | 0 | 0 | 0 | `363BFA7B42DDFB46B3402A68614EC175BD6E3A48B04246B0ABB39CD312644C6D` |
| `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` | 534 | 22 | 0 | 0 | 0 | `5833FD2258BED8912960329160277F6595026870BCF96144708A46BAEE3EDDE3` |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | 512 | 20 | 0 | 0 | 0 | `4AFDCF3B34F7229593036EE3A03255A800C0DEE62ED1B50F0B4E410247ABE9CD` |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | 44 | 17 | 0 | 0 | 0 | `460528E36665B0B2E6779834A89B6C359CB9F0C6F6E637563CE2706E2A2BF1C9` |
| `HOTFIX_REPORT_INDEX.csv` | 135 | 22 | 0 | 0 | 0 | `95B84D3BBC86900CE25481FA418F926AD6DBC15767522C6DF25554745C42A2D4` |

Les trois inventaires contiennent chacun les trois lignes pertinentes :
`00_interests.txt`, `egyptian_crisis_events.txt` et `indochina.txt`. Les
inventaires n'autorisent pas un remplacement global et les deux événements
conservent des décisions de merge distinctes.

## 5. Baseline runtime 6A.18Q conservée

Le fichier testé reste :

```text
common/history/interests/00_interests.txt
SHA-256 = A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD
```

Le `debug.log` de la session 6A.18Q reste à :

```text
9DE3CD6BE2E2A6CEBB3E647A9A97893059C4D4E920D5B02EB39DB12DD8881D3A
337201 octets
2485 lignes
```

Sa lecture complète retrouve 116 lignes contenant `interest_marker`,
`involvement` ou `add_declared_interest` : 93 diagnostics
`Unknown effect add_declared_interest` — 91 dans le fichier historique et un
dans chacun des deux événements — et 23 échecs de PostValidate du trigger
`has_interest_marker_in_region`. Aucun nouveau journal n'a été produit.

La preuve fonctionnelle de 6A.18Q reste inchangée : Autriche au 1er janvier
1776, six implications européennes naturelles visibles, aucune implication au
Sud de la Chine malgré la ligne 126 et aucune au Canada témoin.

## 6. Modèle d'implication 1.13 prouvé

### 6.1 Valeur courante, valeur cible et rang

Le moteur maintient séparément :

- l'implication courante, lue par
  `Country.GetCurrentInvolvementIn(StrategicRegion)`;
- l'implication cible, lue par
  `Country.GetTargetInvolvementIn(StrategicRegion)`;
- la croissance hebdomadaire, lue par
  `Country.GetInvolvementGrowth(StrategicRegion)`;
- la ventilation de la cible, lue par
  `Country.GetTargetInvolvementDescIn(StrategicRegion)`;
- le niveau actif, lue par
  `Country.GetCurrentInterestTierTypeIn(StrategicRegion)`.

Ce sont des getters GUI/tooltip. Ils ne constituent aucun effet d'écriture.
La GUI compare explicitement cible et valeur courante, affiche la flèche de
hausse ou de baisse et calcule le niveau à partir de la valeur courante.

### 6.2 Les cinq niveaux actifs

`common/interest_tier_types/interest_tier_types.txt` définit six intervalles,
dont cinq actifs :

| Rang | Type | Implication |
| ---: | --- | ---: |
| 0 | `interest_tier_none` | 0–99 |
| 1 | `interest_tier_observant` | 100–999 |
| 2 | `interest_tier_engaged` | 1000–2499 |
| 3 | `interest_tier_influential` | 2500–4999 |
| 4 | `interest_tier_pervasive` | 5000–8999 |
| 5 | `interest_tier_hegemonic` | 9000–10000 |

La métadonnée `interest_tier_types.md` dit que ces intervalles classent une
valeur d'implication. Elle documente les effets `on_activate` et
`on_deactivate`, mais aucun setter de niveau. Les cinq niveaux ne sont donc pas
des objets historiques à activer directement.

### 6.3 Sources naturelles de la cible

`common/defines/00_defines.txt` et la ventilation UI anglaise établissent les
sources suivantes :

| Source | Valeur ou plafond 1.13 | Nature |
| --- | ---: | --- |
| capitale dans la région | 2500 | cible moteur |
| région voisine de la capitale | 1500 | cible moteur |
| possession/revendication | jusqu'à 7500, minimum 1500 | cible moteur pondérée par localité |
| revendication | poids de localité 0,20 | composante de possession/revendication |
| PIB régional | multiplicateur 2500 | cible moteur proportionnelle |
| armée présente | conversion 0,33, plafond 5000 | cible moteur |
| flotte présente/en mission | conversion 0,33, plafond 5000 | cible moteur |
| mission couvrant plusieurs régions | bonus 0,75 par région | cible moteur |
| articles de traité et pactes | plafond agrégé 5000 | cible moteur |

La cible additionne ces composantes, sous leurs plafonds de catégorie puis le
plafond global de 10000. La valeur courante converge ensuite vers cette cible;
elle n'est donc pas elle-même la somme instantanée des sources.

Le tutoriel anglais confirme qu'une implication augmente par stationnement
d'armées et de flottes, missions navales adjacentes, fronts, possessions,
revendications, déplacement de capitale, traités et actions diplomatiques avec
des pays locaux.

### 6.4 Traités, accords et relations de sujet

Les définitions d'articles et de pactes utilisent :

```text
max_target_involvement = <valeur>
target_involvement_applies_to = source_country|target_country|mutual
```

La valeur s'applique dans les régions où l'autre partie est un pays local. Un
pays est local si sa capitale est dans la région, s'il y possède au moins 25 %
de la localité ou si au moins 25 % de ses États incorporés s'y trouvent.

Exemples directement pertinents :

| Mécanisme | Maximum de cible | Sens |
| --- | ---: | --- |
| privilège commercial | 1000 | pays bénéficiaire vers les régions locales de l'autre partie |
| port de traité | 3000 | idem |
| droits d'investissement | 2000 | idem |
| alliance | 3000 | mutuel |
| pacte défensif | 2000 | mutuel |
| accès militaire | 1000 | dirigé |
| protectorat | 5000 | sujet vers régions locales du suzerain |
| vassal / union personnelle | 5000 | sujet vers régions locales du suzerain |
| tributaire | 2500 | sujet vers régions locales du suzerain |
| dominion / puppet / colonie / Terre de la Couronne | 8000 | sujet vers régions locales du suzerain |
| compagnie à charte | 5000 | sujet vers régions locales du suzerain |

Cela confirme l'interprétation fonctionnelle de l'opérateur : un intérêt
durable hors de la présence territoriale doit être soutenu par une présence
militaire, un accord, un port de traité ou une relation diplomatique réelle.
Créer ces objets dans le setup demeure néanmoins un changement gameplay et
d'équilibrage, pas une migration pure d'API.

## 7. Effet script `add_involvement`

### 7.1 Registre et signature

La preuve positive est complète pour l'existence et la syntaxe de l'effet :

- la classe enregistrée `CAddInvolvementEffect` et son entrée de registre sont
  lisibles dans `victoria3.exe`;
- la métadonnée technique lisible donne :

```text
Adds involvement for the scoped country in the given strategic region
add_involvement = {
    strategic_region = sr:poland
    value = 10
}
```

- `common/effect_localization/00_country_effects_loc.txt` enregistre sa
  localisation d'effet;
- la localisation anglaise décrit un pays gagnant une valeur d'implication
  dans une région stratégique.

Signature exacte prouvée :

```text
scope d'entrée = Country
strategic_region = scope/tag StrategicRegion
value = CFixedPoint compris entre 0 et INTEREST_MAX_INVOLVEMENT (10000)
```

### 7.2 Exemples vanilla exécutables

Deux exemples installés emploient exactement cette forme :

```text
# egyptian_crisis_events.4, option a
add_involvement = {
    strategic_region = sr:region_near_east
    value = 2500
}

# opium_wars.2, option a
add_involvement = {
    strategic_region = sr:region_south_china
    value = 2500
}
```

L'effet est donc utilisable depuis un événement à scope pays.

### 7.3 Sémantique : courante, pas cible

Les chaînes techniques distinguent explicitement :

```text
add_involvement <region_id> <value>:
Adjust current involvement ... (does NOT change target involvement).
```

Cette phrase documente la commande console homonyme. Le registre de l'effet
est distinct, mais les autres preuves convergent : l'effet est
`CAddInvolvementEffect`, la valeur cible est recalculée séparément par
`RecalculateCachedTargetInvolvement`, les ventilations de cible ne contiennent
aucune source scriptée et les exemples historiques de crises utilisent un
ajout ponctuel. Il est donc établi que `add_involvement` agit sur la valeur
courante et ne crée aucune composante de cible.

Il ne définit :

- ni une implication cible;
- ni un rang directement;
- ni un marqueur legacy permanent;
- ni une source nommée dans la ventilation de cible.

Une valeur suffisamment grande peut indirectement placer la valeur courante
dans un niveau donné, mais elle est ensuite soumise au recalcul vers la cible.

## 8. Recalcul, durée et initialisation au jour 1

### 8.1 Recalcul hebdomadaire

Les defines 1.13 donnent :

```text
INTEREST_GROWTH_RATIO = 0.02
INTEREST_MIN_GROWTH = 10
INTEREST_DECAY_SPEED = 20
INTEREST_TIER_REDUCTION_GRACE_PERIOD_DAYS = 30
```

Chaque semaine, la valeur courante croît vers la cible de 2 % de l'écart avec
un minimum de 10, ou décroît de 20 lorsqu'elle est supérieure à la cible. Le
niveau nouvellement atteint bénéficie d'une grâce de réduction de 30 jours.

Un ajout historique fixe à cible nulle ne survivrait donc pas : il commencerait
à décroître. Une répétition périodique pour le maintenir inventerait une source
et un équilibrage absents du vanilla.

### 8.2 Initialisation moteur

Les chaînes du moteur exposent deux étapes de génération de partie :

```text
CGSG_InitInterestInvolvement
CGSG_FinalizeInterestInvolvement
```

La première précède l'exécution de l'historique des traités; la seconde suit
la mise à jour des ports de traité. Cela prouve un chemin d'initialisation
moteur distinct qui agrège les sources naturelles et diplomatiques. Le runtime
6A.18Q confirme qu'il produit déjà les six valeurs autrichiennes au 1er janvier
1776, partie en pause.

Ce chemin n'est pas un on-action script. `on_game_started` est vide et
`on_game_started_after_lobby` ne fournit aucune initialisation d'implication.
`on_country_formed` et les on-actions de libération ne fournissent aucun
setter générique comparable.

### 8.3 `common/history`

Le vanilla 1.13 ne possède plus de racine
`common/history/interests` et contient zéro usage de `add_involvement` dans
`common/history`. Aucun script DLC installé n'en donne un exemple au jour 1.

6A.18Q prouve que la racine legacy du fork est lue et que ses effets sont
évalués depuis des scopes pays. Cela rend la syntaxe `add_involvement`
plausible dans cette racine, mais ne prouve ni son ordre face à
`CGSG_InitInterestInvolvement`/`CGSG_FinalizeInterestInvolvement`, ni la valeur
finale au jour 1, ni sa persistance. Le contexte historique requis pour un
remplacement des 91 lignes reste donc non démontré.

## 9. Marqueurs, triggers et commandes internes

| Nom | Type prouvé | Usage | Verdict d'écriture script |
| --- | --- | --- | --- |
| `has_interest_marker_in_region` | trigger pays → région | teste l'existence d'un intérêt actuel | lecture seulement |
| `GetCurrentInvolvementIn` | getter GUI | valeur courante | lecture seulement |
| `GetTargetInvolvementIn` | getter GUI | cible | lecture seulement |
| `GetTargetInvolvementDescIn` | getter/tooltip | ventilation de cible | lecture seulement |
| `GetInvolvementGrowth` | getter GUI | delta hebdomadaire | lecture seulement |
| `create_interest_marker` | commande/mécanisme interne | crée l'objet interne | aucun effet script enregistré prouvé |
| `set_interest_marker` | commande/mécanisme interne | mutation interne | aucun effet script enregistré prouvé |
| `add_interest_marker_rank` | commande/mécanisme interne | mutation de rang interne | aucun effet script enregistré prouvé |
| `remove_interest_marker` | commande/mécanisme interne | suppression interne/wargoal | aucun effet script enregistré prouvé |
| `add_involvement` | effet script enregistré | ajoute à la valeur courante | oui, mais temporaire et non équivalent |

Le moteur conserve le nom interne `interest_marker` et le trigger actuel
emploie encore ce vocabulaire. Cela ne transforme pas les commandes internes
en effets scripts. Aucun des quatre setters de marqueur n'apparaît comme
affectation exécutable dans les scripts vanilla/DLC, alors que
`add_involvement` possède explicitement une classe d'effet et deux usages.

## 10. Les deux occurrences événementielles du fork

### 10.1 Crise égyptienne

Le fork contient à la ligne 187 :

```text
add_declared_interest = region_arabic
```

Vanilla 1.13 remplace le même besoin, dans la même option de
`egyptian_crisis_events.4`, par un ajout ponctuel de 2500 dans
`sr:region_near_east`. Il existe donc une migration 1.13 directement comparable
pour **cet événement**. Elle reste hors de cette phase et le fichier conserve
son hash :

```text
EE2A0881C43A14118E0347001FAA423FABA40080C106883BAD0CC6E5715A3168
```

### 10.2 Indochine

Le fork contient un garde legacy de slots puis :

```text
num_declared_interests < max_num_declared_interests
add_declared_interest = region_indochina
```

Les deux identifiants du garde sont eux aussi rejetés dans `debug.log`.
Vanilla 1.13 conserve l'événement `indochina.3`, mais supprime entièrement le
garde et l'ajout d'intérêt; il ne les remplace pas par `add_involvement`.
L'entrée fork est donc une divergence 1776 dont le besoin de design doit être
réévalué, pas un remplacement mécanique comparable à la crise égyptienne. Le
fichier conserve son hash :

```text
177A6446668E9274260FCA90B0F7B0802280CA7E086CC1290E15C862E845B2BB
```

## 11. Matrice des mécanismes candidats

| Candidat | Provenance/type | Scope et argument | Effet exact | Durée/recalcul | Historique | Équivalence legacy | Risque | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `add_involvement` | registre d'effet + vanilla | pays; région + valeur | ajoute à la courante | converge ensuite vers la cible | aucun exemple jour 1 | non | disparition ou duplication avec sources naturelles | prouvé pour événements, insuffisant pour les 91 lignes |
| capitale/territoire/revendication/PIB | moteur naturel | pays et carte | construit la cible | recalcul dynamique | initialisé par moteur | non, cause réelle | change carte/économie | durable mais gameplay |
| armée/flotte | moteur naturel | présence/mission | construit la cible | recalcul dynamique | initialisé par moteur | non, cause réelle | change déploiement/forces | durable mais gameplay |
| traité/article | données de traité | deux pays; maximum | construit la cible dans les régions locales | tant que l'article existe | historique des traités reconnu | non, relation réelle | change diplomatie/équilibrage | durable mais gameplay |
| pacte/sujet | action/pacte | deux pays; maximum | construit la cible dans les régions locales | tant que le pacte existe | histoire diplomatique reconnue | non, relation réelle | change souveraineté/diplomatie | durable mais gameplay |
| setters `interest_marker` | commandes internes | non documenté comme effet | mutation interne | non documenté | non prouvé | inconnu | parser/état moteur | rejeté |
| getter/tooltip | GUI | pays + région | lit | n/a | n/a | non | aucun | lecture seulement |

## 12. Réponses aux dix-sept questions

1. **Existe-t-il un effet 1.13 enregistré acceptant un pays et une région ?**
   Oui : `add_involvement`, depuis un scope pays, avec une région et une valeur.
2. **Nom exact ?** `add_involvement`.
3. **Signature exacte ?**
   `Country = { add_involvement = { strategic_region = <StrategicRegion>; value = <0..10000> } }`.
4. **Définit-il une implication courante ?** Oui, il l'augmente.
5. **Définit-il une implication cible ?** Non.
6. **Définit-il un rang ?** Non; le rang découle de l'intervalle de la valeur
   courante.
7. **Définit-il un marqueur legacy ?** Non démontré; il crée ou ajuste l'objet
   courant nécessaire, sans restaurer la sémantique binaire legacy.
8. **Est-il autorisé dans `common/history` au chargement du monde ?** Non
   prouvé. Aucun exemple vanilla/DLC et ordre d'initialisation non documenté.
9. **Existe-t-il un exemple vanilla/DLC prouvant la syntaxe ?** Oui, deux
   événements vanilla, mais aucun exemple historique jour 1.
10. **Les cinq niveaux actifs peuvent-ils être initialisés directement ?** Non.
    Une valeur courante peut les atteindre indirectement; aucun setter direct
    de niveau n'est exposé.
11. **Doivent-ils découler uniquement des sources naturelles ?** Pour une cible
    durable, oui selon les preuves disponibles : territoire/capitale/claims,
    forces, traités et pactes. `add_involvement` ne fournit qu'une impulsion.
12. **Une valeur historique fixe survivrait-elle au recalcul hebdomadaire ?**
    Non si la cible naturelle est inférieure; elle décroît vers cette cible.
13. **Le moteur permet-il une source personnalisée ?** Aucun registre générique
    de source pays/région n'est exposé. Un mod peut définir un article ou un
    pacte avec `max_target_involvement`, mais il crée un vrai mécanisme
    diplomatique et change le gameplay.
14. **Les 91 lignes peuvent-elles être remplacées sans rééquilibrage ?** Non.
    Choisir une valeur, un rang, un accord, un sujet ou une présence est une
    nouvelle décision d'équilibrage.
15. **Les deux événements ont-ils le même besoin sémantique ?** Non. La crise
    égyptienne a un remplacement vanilla ponctuel prouvé; vanilla supprime
    l'ajout indochinois.
16. **Le remappage des 26 régions legacy est-il utile avant la preuve du
    mécanisme ?** Non. Il ne répare ni l'effet ni la sémantique.
17. **La liste fixe est-elle conceptuellement obsolète ?** Oui pour représenter
    des intérêts durables : 1.13 les fait découler d'une implication graduée et
    de causes recalculées. Des impulsions scénarisées ponctuelles restent
    possibles avec `add_involvement`.

## 13. Décision de correction future

L'effet et sa syntaxe sont désormais prouvés, mais les conditions de sélection
d'une 6A.18F ne sont pas toutes remplies :

- aucun exemple de `common/history` au jour 1;
- ordre exact face aux deux initialiseurs moteur non prouvé;
- aucune persistance de cible;
- aucun remplacement sans choix de valeurs ou de relations;
- les 91 lignes ne portent aucun niveau 1.13;
- la crise égyptienne et l'Indochine exigent deux traitements différents;
- aucun hash théorique, diff minimal ou rollback gameplay ne peut être défini
  sans prendre ces décisions.

En conséquence, le mécanisme de remplacement reste non démontré et aucune
prochaine phase d'exécution n'est sélectionnée. Il n'existe donc ni correction,
ni hash gameplay théorique, ni diff gameplay, ni rollback gameplay dans cette
phase. Les tokens canoniques de cette décision apparaissent une seule fois dans
les verdicts finaux.

## 14. Documents écrits

- création du présent rapport;
- ajout de 6A.18R2 à l'index global et à l'index CSV;
- mise à jour de la matrice des blocs;
- ajout de la conclusion 6A.18R2 à la roadmap;
- mise à jour du prompt courant avec l'état explicite « aucune prochaine phase
  sélectionnée »; le prompt 6A.18R2 y reste archivé comme preuve historique.

Aucun autre fichier n'est créé ou modifié.

## 15. Contrôles finaux

Les contrôles finaux confirment :

- branche, HEAD et message inchangés;
- index staged vide;
- `git diff --check` PASS;
- uniquement les documents autorisés modifiés;
- `00_interests.txt` inchangé au hash
  `A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD`;
- deux événements inchangés aux hashes consignés en section 10;
- journaux inchangés;
- huit non-suivis protégés inchangés;
- stash exact;
- aucun processus Victoria 3, Dowser ou launcher Paradox;
- aucun gameplay, pays, région, traité, pacte, sujet, flotte, armée,
  localisation ou équilibrage modifié;
- aucun commit et aucun push.

État Git final constaté :

```text
branch = hotfix-dlc-audit
HEAD = f9635de7fefbfa1790e43930e39847acd971935d
message = Validate declared interest history runtime for 1.13
tracked documentation diffs = 5
new authorized report = 1
staged files = 0
git diff --check = PASS
game processes = 0
```

Les journaux de preuve restent notamment aux hashes suivants :

```text
debug.log = 9DE3CD6BE2E2A6CEBB3E647A9A97893059C4D4E920D5B02EB39DB12DD8881D3A
error.log = A43B489AAAA0610532DC167B76E0FAABE295BFEABDD5865E8F0EF39D0EE47938
game.log  = 6D9F2D88FA999EAA819579830CFF513A8F8ACFE136C49ED6424D17C251B83A8D
```

## 16. Verdicts finaux

```text
HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT_COMPLETE
DECLARED_INTEREST_1_13_INITIALIZATION_PATHS_AUDITED
DECLARED_INTEREST_LEGACY_AND_INVOLVEMENT_SEMANTICS_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_1_13_REPLACEMENT_MECHANISM_UNPROVEN
NO_NEXT_EXECUTION_PHASE_SELECTED
```
