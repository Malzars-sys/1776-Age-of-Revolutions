# CLEANUP-2D-5O — Starting general command rank capacity

## Résultat

Statut statique : **PASS**.

- 214/214 formations terrestres auditées ;
- 214/214 généraux de départ audités ;
- 79 généraux historiques, 135 procéduraux et 20 personnages dirigeant/général réutilisés couverts ;
- 29 insuffisances initiales ;
- 29 promotions minimales de `commander_rank_1` vers `commander_rank_2` ;
- 185 rangs conservés ;
- aucune rétrogradation ;
- aucune promotion vers les rangs 3, 4 ou 5 ;
- 214/214 limites finales déterministes supérieures ou égales aux bataillons permanents ;
- aucun effectif permanent, conscrit ou naval modifié.

Le détail ligne par ligne est dans
`docs/research/military/CLEANUP2D5O_STARTING_GENERAL_COMMAND_RANK_AUDIT.csv`.

## Sources locales inspectées

L'audit utilise l'installation locale Steam, sans recherche Internet :

- version du binaire : Victoria 3 **1.13.10** ;
- `game/common/commander_ranks/00_commander_ranks.txt` ;
- `game/common/defines/00_defines.txt` ;
- `game/common/character_templates/00_default_template.txt` ;
- `game/common/character_traits/*.txt` ;
- exemples vanilla dans `game/common/history/military_formations/*.txt` et
  `game/common/history/characters/*.txt` ;
- templates et créations de personnages actuels du mod.

Les valeurs n'ont pas été supposées ni recopiées depuis la mémoire. Le
validateur les relit directement dans les fichiers vanilla locaux.

## Relation réelle entre rang et limite de commandement

`00_defines.txt` fixe :

- `COMMANDER_START_RANK = 1` ;
- `HIGHEST_PROMOTION_RANK = 5` ;
- `RULER_COMMANDER_START_RANK = 6`.

`00_commander_ranks.txt` associe chaque rang à un
`character_command_limit_add` terrestre :

| Rang | `rank_value` | Limite terrestre de base |
|---|---:|---:|
| `commander_rank_1` | 1 | 30 |
| `commander_rank_2` | 2 | 60 |
| `commander_rank_3` | 3 | 80 |
| `commander_rank_4` | 4 | 125 |
| `commander_rank_5` | 5 | 200 |
| `commander_rank_ruler` | 6 | 50 |

Le template vanilla `default` porte `commander_rank = default`. Pour un
général non dirigeant sans rang explicite, le moteur emploie donc le rang de
départ 1. Pour un dirigeant également général, il emploie le rang spécial 6.
Les fichiers vanilla confirment que `create_character` accepte directement la
syntaxe `commander_rank = commander_rank_N`. C'est le mécanisme utilisé ici.

Pour cet audit, la limite fiable est la limite de rang, corrigée uniquement par
les modificateurs de limite déterministes explicitement attachés au personnage.
Les 214 blocs ont été contrôlés. Un seul dirigeant/général réutilisé possède
des traits explicitement fixés (`meticulous`, `experienced_political_operator`,
`brave`) ; aucun de ces traits ne modifie la limite de commandement. Le nombre
de modificateurs déterministes applicables est donc **0/214** et la limite
fiable est égale à la limite de base du rang pour les 214 lignes.

## Traits aléatoires : audit séparé

Le `trait_generation` du template `default` peut générer des traits qui font
varier l'affichage runtime. Les définitions vanilla locales comprennent
notamment des multiplicateurs positifs (`traditionalist_commander` +10 %,
`popular_commander` +20 %, `celebrity_commander` +30 %, `arrogant` +25 %) et
négatifs (`erudite` -10 %, `senile` -25 % lorsque ses conditions sont
remplies).

Ces résultats aléatoires ne sont pas crédités dans le choix statique du rang :
un bonus aléatoire ne permet jamais de conserver un rang dont la limite de base
est insuffisante. Ils expliquent les valeurs runtime variables signalées : 33
correspond à 30 augmenté de 10 %, et 27 à 30 diminué de 10 %. Après promotion
au rang 2, les mêmes multiplicateurs donnent respectivement 66 et 54, ce qui
couvre les exemples de 35 et 42 bataillons.

Les traits aléatoires restent une variable de génération runtime, distincte du
rang scripté et recensée comme telle. Le CSV conserve la colonne des traits
explicites et la colonne du modificateur déterministe ; il n'invente pas un
trait pour les personnages dont le trait est généré par le moteur.

## Méthode de décision

Pour chaque ligne `GEN1776-001` à `GEN1776-214` :

1. compter séparément les `combat_unit` permanentes et celles portant
   `service_type = conscript` ;
2. résoudre le rang avant correction depuis le HEAD `bbeb8b7`, le rang par
   défaut moteur ou le rang spécial de dirigeant ;
3. calculer la limite déterministe fiable ;
4. conserver le rang lorsque cette limite couvre les permanents ;
5. sinon, sélectionner le premier rang promotionnel supérieur suffisant ;
6. ne jamais utiliser les conscrits potentiels pour sélectionner le rang ;
7. vérifier à nouveau le fichier final.

Les 29 cas insuffisants avaient entre 32 et 44 bataillons permanents. Le rang 2
est donc toujours le plus petit rang supérieur suffisant. Les 20 dirigeants
réutilisés ont entre 1 et 30 permanents : leur limite spéciale de 50 suffit et
leur rang reste inchangé.

## Répartition des corrections

| Fichier régional | Formations | Promotions |
|---|---:|---:|
| Europe | 86 | 19 |
| Amérique du Nord | 6 | 0 |
| Amérique du Sud | 5 | 0 |
| Afrique du Nord | 8 | 0 |
| Moyen-Orient | 12 | 1 |
| Inde | 25 | 1 |
| Asie | 39 | 8 |
| Afrique subsaharienne | 33 | 0 |
| **Total** | **214** | **29** |

Par catégorie, 26 généraux historiques et 3 procéduraux ont été promus. Les 20
dirigeants/généraux réutilisés sont tous conservés au rang spécial de dirigeant.

## Invariants d'effectifs

- bataillons permanents : **2 557**, inchangés ;
- conscrits potentiels : **1 705**, inchangés et audités séparément ;
- blocs `combat_unit` comparés au HEAD `bbeb8b7` : **794/794 identiques** ;
- formations terrestres : **214**, inchangées ;
- flottes et amiraux : hors périmètre et inchangés selon le validateur 2D-5.

## Validation reproductible

Commande principale :

```powershell
python tools/cleanup2d5o_validate.py
```

Résultat attendu :

```text
PASS AUDIT_ROWS = 214
PASS PROMOTIONS = 29
PASS HISTORICAL_PROMOTIONS = 26
PASS PROCEDURAL_PROMOTIONS = 3
PASS RULER_PROMOTIONS = 0
PASS DETERMINISTIC_COMMAND_MODIFIERS = 0
PASS FINAL_FAILURES = 0
PASS AUDIT_CSV_CURRENT = 214
CLEANUP2D5O_STATIC_VALIDATION=PASS
```

Le CSV peut être régénéré après un audit réussi avec :

```powershell
python tools/cleanup2d5o_validate.py --write-csv
```

La validation runtime 1776-01-01 et save/reload reste à exécuter dans le jeu ;
aucun PASS runtime nouveau n'est revendiqué par ce rapport statique.
