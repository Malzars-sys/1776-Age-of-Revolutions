# HOTFIX-5C2E4C0 - Preparation des tests fonctionnels Sepoy

## 1. Resume

Cette phase prepare, sans les executer, les tests fonctionnels de
`sepoy_mutiny_events.2` et de ses options 2.a, 2.b, 2.c et 2.e.

L'event 2 est structurellement isolable : il s'agit d'un `country_event`, son
scope racine attendu est BIC, et ses blocs `trigger` et `immediate` sont vides.
Il ne lit aucun scope sauvegarde par les events precedents et aucune variable
de la chaine. Son seul scope nomme, `prince_scope`, est cree puis efface dans
chaque option.

En revanche, un test utile exige plusieurs topologies territoriales et
diplomatiques qui n'existent pas toutes dans le setup 1776. La methode retenue
est donc une copie jetable du mod avec un harnais de test dedie, jamais la
branche principale. Aucun harnais et aucun test ne sont crees dans cette phase.

**Verdict : `NEEDS_DISPOSABLE_MOD_COPY`.**

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- HEAD : `1ce189d Validate Sepoy API corrections at runtime`.
- HOTFIX-5C2E4B3 est present a HEAD.
- Aucun fichier suivi n'etait modifie au debut de l'audit.
- Seule exception : `docs/research/technology/`, dossier non suivi preexistant.
- Stash detecte et non applique :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

Les sept fichiers preexistants sous `docs/research/technology/` ont ete lus
uniquement par metadonnees et sommes SHA-256 avant redaction. Ils n'ont pas ete
ouverts pour edition et ne font pas partie de HOTFIX-5C2E4C0.

## 4. Chaine d'activation complete

La chaine organique du fork est la suivante :

```text
point d'entree : je_uneasy_raj
  -> possible = { always = no } dans le fork 1776
  -> en cas d'echec ou timeout : ajout de je_sepoy_mutiny
  -> declenchement de sepoy_mutiny_events.3 sur BIC
  -> immediate de l'event 3 :
       bic_incorporated_state sur les states incorpores
       sepoy_mutiny_immediate_effects
       sepoy_mutiny_princely_states_stance_effect
       mughals_scope si MUG existe
  -> une option de l'event 3 appelle sepoy_mutiny_run_all_effects
  -> creation des revoltes et diplomatic plays Sepoy
  -> sepoy_mutiny_events.4 pour les princes a faible loyaute
  -> sepoy_mutiny_events.1 seulement pour SAT entre 1845 et 1870
  -> echec de je_sepoy_mutiny apres resolution du play/retrait territorial
  -> sepoy_mutiny_events.2 sur le scope racine BIC
  -> choix 2.a, 2.b, 2.c ou 2.e
  -> independances, transferts, redistribution et eventuels radicaux
  -> aucun event suivant n'est appele directement par l'event 2
```

`sepoy_mutiny_events.1` n'est donc pas le predecesseur obligatoire de l'event
2. Il est programme par un scripted effect uniquement pour la branche Satara,
avec une garde 1845-1870. Le predecesseur direct de l'event 2 est l'echec de
`je_sepoy_mutiny`.

Le hotfix et la vanilla 1.13 possedent la meme liaison `je_sepoy_mutiny.on_fail`
vers l'event 2. Leur `je_uneasy_raj` n'a pas le verrou 1776 du fork. Cette
difference ne doit pas etre importee pour effectuer les tests.

## 5. Scopes et variables requis

| Element | Classe | Besoin pour invocation isolee | Commentaire |
|---|---|---|---|
| Scope racine pays BIC | MANDATORY | Oui | Toutes les boucles `any_scope_state` et `every_scope_state` partent de root. |
| BIC vivant | MANDATORY | Oui | L'event doit etre affiche et execute dans ce pays. |
| GBR overlord de BIC | MANDATORY pour 2.a, RECOMMENDED sinon | Oui pour reproduire la fin 2.a | 2.a joue GBR puis annexe root si BIC est sujet de GBR. |
| GBR vivant | RECOMMENDED | Oui | Les retraits de leverage sont optionnels via `c:GBR.power_bloc ?=`. |
| Sujets directs de BIC | OPTION_SPECIFIC | Pour tester `make_independent` | Leur capitale doit etre dans North/South India, Pashtunistan ou Quetta. |
| Receveurs sud-asiatiques voisins | OPTION_SPECIFIC | Pour tester la boucle generique | Heritage sud-asiatique et capitale dans une zone admise. |
| States BIC dans North/South India | MANDATORY | Oui | Matiere territoriale principale des quatre options. |
| Himalaya/Pashtunistan/Quetta | OPTION_SPECIFIC | Seulement F-1/F-2/F-3 | Exceptions explicites a tester separement. |
| Pops hindous ou sunnites | RECOMMENDED | Pour mesurer les radicaux | 2.b vise North India ; 2.c et 2.e visent South India. |
| `raj_scope` | NOT_REQUIRED | Non | Cree par `je_uneasy_raj`, jamais lu dans l'event 2. |
| `eic_ig` | NOT_REQUIRED | Non | Cree par `je_sepoy_mutiny`, jamais lu dans l'event 2. |
| `mughals_scope` | NOT_REQUIRED | Non | Cree par l'event 3, jamais lu dans l'event 2. |
| Scopes de l'event 1 | NOT_REQUIRED | Non | `nana_saheb_scope` et `other_revolter_nation_scope` sont absents de l'event 2. |
| `prince_scope` | LOCAL | Non en entree | Sauvegarde dans chaque boucle puis efface dans la meme option. |
| Variables de presidency | NOT_REQUIRED | Non | Aucune lecture dans l'event 2. |
| `sepoy_mutiny_revolter_var` | NOT_REQUIRED | Non | Utilisee en amont, pas dans l'event 2. |
| `je_uneasy_raj`/`je_sepoy_mutiny` | NOT_REQUIRED | Non | L'event 2 n'interroge aucune JE. |
| Diplomatic play ou guerre active | NOT_REQUIRED | Non | Aucun test de play ou de guerre dans l'event 2. |
| Cultures du root | NOT_REQUIRED | Non | Le filtre culturel porte sur les receveurs. |

## 6. Comparaison des methodes de declenchement

| Methode | Preuve locale | Bons scopes | Reproductibilite | Risque | Decision |
|---|---|---|---|---|---|
| Commande console d'event | `console_history.txt` contient des essais `event <id> <TAG>`, dont les events Japon ; aucune aide capturee ni execution de l'event 2 | Probable mais non prouve pour BIC | Bonne pour A/B/E-3, insuffisante pour construire tous les setups | Resultat trompeur si le tag n'est pas le root reel | `UNVERIFIED` |
| Chaine complete | Autorite script locale | Oui | Tres faible en 1776 | Exigerait de retirer `always = no` ou de reconstruire toute la revolte | Rejetee |
| Edition de sauvegarde | `autosave_exit.v3` existe, date du 14/07/2026 22:05 | Possible en theorie | Faible sans outil local valide | Sauvegarde compressee, references dynamiques, corruption possible | Non retenue |
| Copie jetable du mod | Methode filesystem reproductible | Oui, via effets de test limites a BIC | Haute | Faible si nom et chemin distincts | **Retenue** |
| Branche/worktree de test | Git le permet | Oui | Haute | Risque de charger le mauvais descripteur ou de committer le harnais | Solution de repli |
| Scripted button seul | API non verifiee dans cette phase | Oui en theorie | Moyenne | Integration GUI et scope a confirmer | A utiliser seulement dans la copie, apres validation vanilla |

La console n'est pas declaree fonctionnelle simplement parce que sa syntaxe
est habituelle dans les jeux Paradox. L'historique local prouve que la commande
a ete saisie, pas qu'elle a fourni le bon root BIC a cet event destructif.

## 7. Methode recommandee

Creer dans une phase suivante une copie jetable distincte, par exemple :

```text
C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test
```

Nom launcher recommande : `1776 Sepoy Functional Test (Disposable)`.

Le harnais ne devra ajouter que des fichiers de test dedies, sans modifier les
deux fichiers Sepoy reels. Une implementation candidate est une decision de
debug BIC et un event de preparation par scenario, apres verification de leur
syntaxe dans la vanilla locale. Chaque scenario doit :

1. refuser tout root autre que BIC ;
2. preparer ownership, sujets, receveurs et capitales de facon deterministe ;
3. prendre un instantane manuel avant activation ;
4. declencher l'event 2 sur le meme root BIC ;
5. ne jamais etre charge avec le mod principal dans le meme playset.

Fichiers temporaires candidats dans la copie uniquement :

- `common/decisions/zz_sepoy_functional_test.txt` ;
- `events/zz_sepoy_functional_test_events.txt` ;
- localisations EN/FR strictement reservees au harnais ;
- un `descriptor.mod` avec nom et remote id distincts.

La sauvegarde `autosave_exit.v3` peut servir de baseline a condition d'etre
dupliquee sous un nom de test. L'original ne doit jamais etre edite.

Suppression apres test : fermer le jeu et le launcher, supprimer uniquement le
dossier jetable dont le chemin aura ete verifie, puis retirer son descripteur
launcher. La branche principale reste prouvee intacte par `git status` et les
sommes des deux fichiers gameplay avant/apres.

## 8. Risques de la methode

- Charger simultanement le fork et la copie provoquerait des definitions en
  double ; un playset separe est obligatoire.
- Les boucles `random_scope_state` rendent les resultats non deterministes si
  plusieurs receveurs partagent la meme frontiere. A-3 doit etre repete depuis
  le meme point de sauvegarde.
- Un scenario mal isole peut activer les transferts prioritaires vers BUR, BER,
  SIA, COC, TRA, HYD, MUG, NAG, SAT ou KHP avant la boucle generique.
- 2.a change le pays joue vers GBR et annexe BIC si la relation de sujet existe.
- Les radicaux ne sont observables que si des pops hindous ou sunnites restent
  dans les states BIC de la region cible apres redistribution.
- Le test ne doit pas etre sauvegarde par-dessus la baseline.

## 9. Scenario 2.a

### A-1 - Breakup general

- Root BIC, sujet de GBR.
- Au moins un state BIC en North India et un en South India.
- Au moins un sujet direct eligible et un receveur sud-asiatique voisin.
- Relever les capitales avant le choix.
- Attendu : sujets eligibles independants, transferts prioritaires, puis
  redistribution generique des states restants vers des voisins eligibles.
- Fin attendue : si BIC reste sujet de GBR, passage du joueur a GBR puis annexion
  du reliquat BIC. Aucun effet final de radicaux n'est defini.

### A-2 - Aucun receveur

Isoler un state redistribuable hors des listes prioritaires, sans voisin dont
le pays remplit les filtres culturels et de capitale. Les preconditions des
receveurs prioritaires doivent aussi etre rendues fausses pour ce state.

Attendu : la boucle generique ne demarre pas pour ce state ; aucun owner nul ;
le reliquat reste BIC jusqu'a l'annexion finale par GBR en 2.a.

### A-3 - Plusieurs receveurs

Un state BIC redistribuable doit toucher exactement deux pays eligibles. Le
test est a rejouer au moins cinq fois depuis la meme sauvegarde pre-option.

Attendu : le state part vers un seul receveur valide par execution. La repartition
entre les deux tags peut varier ; aucune boucle infinie ni double ownership.

## 10. Scenario 2.b - Retraite Bengal

Prerequis d'acces : BIC possede un region state dans `STATE_WEST_BENGAL`.
`STATE_EAST_BENGAL` n'est pas une garde d'acces, mais son absence applique une
penalite IA et reduit la qualite du test du noyau Bengal.

Noyau attendu par l'intention : West Bengal et East Bengal. Reprises prioritaires
possibles : Madras, Mandalay/Pegu, Gujarat, Tenasserim, Travancore,
Circars/Kurnool, Delhi/Agra/Awadh, Central Provinces et Bombay. La boucle
generique reste large ; la conservation effective du noyau doit donc etre
observee, pas presupposee.

Radicaux attendus : pops hindous et sunnites des states encore possedes par BIC
dans `region_north_india`.

## 11. Scenario 2.c - Retraite Madras

Prerequis d'acces : BIC possede un region state dans `STATE_MADRAS`.

Noyau attendu par l'intention : Madras. Le setup 1776 actuel ne satisfait pas
cette garde : Madras est partage entre FRA, DENNOR et PUD, BIC n'y possede
qu'une claim. Le harnais doit donc fournir a BIC un region state Madras avant
l'event.

Reprises prioritaires : Mandalay/Pegu, Gujarat, Tenasserim, Travancore,
Delhi/Agra/Awadh, Central Provinces et Bombay. Radicaux attendus dans les states
BIC restants de `region_south_india`.

## 12. Scenarios 2.e - Retraite Bombay

| Scenario | West Bengal | Bombay | Disponibilite selon le code | Resultat a verifier |
|---|---:|---:|---|---|
| E-1 | Present | Present | Oui | Intention Bombay, puis redistribution et radicaux South India. |
| E-2 | Absent | Present | Non | L'option est bloquee malgre le noyau suggere par le texte. Aucun effet ne doit partir. |
| E-3 | Present | Absent | Oui | L'option est proposee sans noyau Bombay reel ; comportement territorial a relever. |

Le setup 1776 courant est deja proche d'E-3 : BIC possede West Bengal mais pas
Bombay. Bombay appartient a POR, MARATH, SAT et KHP. E-3 peut donc etre le
premier test de disponibilite dans la copie, sans alterer la baseline.

## 13. Analyse STATE_WEST_BENGAL / STATE_BOMBAY

La seule garde de 2.e est :

```txt
trigger = {
    any_scope_state = {
        state_region = s:STATE_WEST_BENGAL
    }
}
```

`STATE_BOMBAY` n'apparait nulle part dans 2.e. Le texte et le tooltip annoncent
cependant un repli vers Bombay. Le noyau reel n'est pas protege par une garde
Bombay ni par une exclusion explicite de la boucle generique. Les listes
prioritaires de 2.e omettent Bombay, ce qui traduit une intention de le garder,
mais ne garantit pas sa conservation lors de la redistribution finale.

E-2 et E-3 constituent donc la preuve fonctionnelle decisive. Cette phase ne
change ni la garde ni `STATE_WEST_BENGAL`.

## 14. Etats et pays a relever avant/apres

Pour chaque scenario, produire un tableau state par state.

Avant :

- owner et controller ;
- state region et strategic region ;
- incorporation ;
- sujet direct de BIC ou non ;
- capitale, type et cultures primaires du sujet/receveur ;
- voisinages utiles ;
- option visible et cliquable ;
- population hindoue/sunnite et radicaux de reference.

Apres :

- owner et controller ;
- independance de chaque ancien sujet ;
- receveur et capitale ;
- states conserves par BIC ;
- reliquat annexe par GBR en 2.a ;
- variation des radicaux ;
- play ou guerre encore actifs ;
- pays joue ;
- erreurs nouvelles dans les logs.

Chaque test doit partir d'une copie immuable du meme instant pre-option. Une
sauvegarde apres option ne doit jamais servir de depart au scenario suivant.

## 15. Patterns de logs

Rechercher dans `error.log`, `game.log` et `debug.log` :

```text
sepoy_mutiny_events.2
sepoy_mutiny_events.3
sepoy_mutiny_events.4
random_scope_state
any_neighbouring_state
set_state_owner
make_independent
save_scope_as
STATE_WEST_BENGAL
STATE_BOMBAY
region_north_india
region_south_india
region_himalayas
STATE_PASHTUNISTAN
STATE_QUETTA
Invalid scope
Invalid right side
Script system error
PostValidate
while
```

Faux positifs connus : `Invalid right side during comparison 'sr'` existe deja
dans la baseline actuelle depuis `01_natural_borders_of_france.txt`. Il ne doit
pas etre attribue a Sepoy sans un `Script location` pointant vers les deux
fichiers Sepoy. `while`, `save_scope_as` et `set_state_owner` peuvent aussi
apparaitre dans d'autres chaines ; toujours conserver le chemin et la ligne.

## 16. Description du CSV

`HOTFIX_5C2E4C0_SEPOY_SCENARIO_REQUIREMENTS.csv` contient les onze scenarios
minimum A/B/C/E/F. Les prerequis y sont classes dans les cellules et les
attendus distinguent la logique voulue de ce qui doit encore etre confirme.
Le fichier est encode en UTF-8 avec BOM.

## 17. Verdict de preparation

**`NEEDS_DISPOSABLE_MOD_COPY`**

Les dependances de l'event 2 sont suffisamment cartographiees, mais aucune
methode locale ne permet encore de fabriquer de facon sure et repetable les
onze topologies sans environnement de test. La console reste `UNVERIFIED` pour
le root BIC et l'edition de la sauvegarde compressee n'a pas d'outil local
valide.

## 18. Action manuelle requise de l'utilisateur

Avant la phase fonctionnelle :

1. conserver `autosave_exit.v3` comme baseline et en faire une copie nommee ;
2. autoriser la creation du dossier jetable et d'un playset launcher distinct ;
3. ne jamais activer simultanement le fork et la copie ;
4. si la console doit servir de solution secondaire, ouvrir son aide et
   conserver une capture prouvant la syntaxe exacte de la commande `event` et
   du parametre pays avant toute invocation de l'event 2.

## 19. Phase fonctionnelle suivante recommandee

`HOTFIX-5C2E4C1` devrait creer uniquement la copie jetable et son harnais,
verifier sa syntaxe contre la vanilla, puis effectuer d'abord trois tests sans
edition territoriale complexe : A-1, B-1 et E-3 sur des copies separees de la
baseline. Les autres scenarios ne commencent qu'apres validation du harnais.

Ordre recommande : A-1, A-2, A-3, B-1, C-1, E-1, E-2, E-3, F-1, F-2, F-3.

## 20. Fichiers crees

- `docs/reports/hotfix/HOTFIX_5C2E4C0_SEPOY_FUNCTIONAL_TEST_PREPARATION.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C0_SEPOY_SCENARIO_REQUIREMENTS.csv`

## 21. Confirmation gameplay

Aucun fichier gameplay n'a ete modifie. En particulier,
`common/journal_entries/04_sepoy_mutiny.txt`,
`events/india_events/sepoy_mutiny_events.txt` et `STATE_WEST_BENGAL` sont
inchanges. Aucun event n'a ete declenche.

## 22. Confirmation recherche technologie

`docs/research/technology/` n'a pas ete modifie par cette phase. Ses sept
fichiers non suivis restent l'exception concurrente autorisee.

## 23. Confirmation stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present, intact et non
applique. Aucun `git stash pop` n'a ete execute.
