# PHASE NAVY-3C-2 - BIC / Bombay Marine

## 1. Resume

Cette phase verifie si la British East India Company (`BIC`) peut recevoir une flotte minimale de type `Bombay Marine` sans contredire le setup territorial actuel du mod.

Decision : aucune flotte BIC n'est creee dans cette phase.

Raison principale : la recherche historique justifie bien une presence navale de la Compagnie, mais le setup 1776 du mod ne donne pas Bombay a BIC. `STATE_BOMBAY` est partage entre `POR`, `MARATH`, `SAT` et `KHP`, et le fichier de batiments ne contient pas de bloc `region_state:BIC` a Bombay. Creer une `Bombay_Marine` sans Bombay forcerait une incoherence territoriale ou pousserait a toucher a MARATH, ce qui est explicitement interdit.

## 2. Resultat de la recherche historique

La recherche historique fournie pour cette phase conclut :

- la British East India Company possedait bien une force navale propre autour de 1776 ;
- le nom le plus solide est `Bombay Marine` ;
- son role etait regional : escorte locale, protection du commerce, patrouille, hydrographie et petits batiments armes ;
- ce n'etait pas une seconde Royal Navy ;
- aucun vaisseau de ligne ne doit etre cree ;
- aucun amiral historique fiable ne doit etre ajoute ;
- une seule unite navale symbolique serait le compromis maximal acceptable ;
- la Royal Navy reste la force lourde britannique.

Cette conclusion historique est acceptee, mais elle doit rester compatible avec le setup territorial du mod.

## 3. Verification du setup territorial BIC / Bombay

| State | Owner / ownership | Ports | Chantiers | Pertinence BIC |
| --- | --- | --- | --- | --- |
| `STATE_BOMBAY` | `POR`, `MARATH`, `SAT`, `KHP` dans `common/history/states/00_states.txt` | `POR` niveau 1 ; `MARATH` niveau 2 | `MARATH` niveau 1 | BIC n'a pas d'ownership direct. BIC a seulement une revendication. |
| `STATE_WEST_BENGAL` | `BIC` et `COO` | `BIC` niveau 6 | `BIC` niveau 2 | Base BIC la plus solide pour une flotte future non nommee Bombay. |
| `STATE_EAST_BENGAL` | `BIC` | `BIC` niveau 1 | Aucun detecte | Presence BIC claire, mais pas Bombay. |
| `STATE_CIRCARS` | Presence BIC dans les batiments | `BIC` niveau 1 | Aucun detecte | Presence cotiere BIC secondaire. |
| `STATE_PEGU` | `BIC` possede une province dans l'historique d'etat | `BIC` niveau 1 dans `11_east_asia.txt` | Aucun detecte | Presence BIC extra-indienne, non liee a Bombay. |

Constats directs :

- `common/history/states/00_states.txt` : `STATE_BOMBAY` ne contient aucun `create_state` pour `c:BIC`.
- `common/history/states/00_states.txt` : `STATE_BOMBAY` ajoute `add_claim = c:BIC`, ce qui n'est pas une possession.
- `common/history/buildings/10_india.txt` : `STATE_BOMBAY` contient `region_state:POR` et `region_state:MARATH`, mais pas `region_state:BIC`.
- `common/history/buildings/10_india.txt` : le port principal de Bombay cote indien appartient a `MARATH`, et le chantier naval de Bombay appartient aussi a `MARATH`.

Conclusion : BIC ne possede pas clairement Bombay dans le setup actuel.

## 4. Decision

Decision : flotte non creee.

Le prompt demande de privilegier l'absence de creation si Bombay n'est pas BIC. C'est exactement le cas ici. Ajouter une flotte `Bombay_Marine` demanderait soit :

- de baser BIC dans un state que BIC ne possede pas ;
- de renommer artificiellement une flotte basee au Bengal ;
- de toucher a `MARATH` ou a l'ownership de Bombay ;
- ou de creer une abstraction trop fragile pour une phase qui doit rester prudente.

Aucune de ces options n'est acceptable dans cette phase.

## 5. Flotte non creee

Raison precise :

- `STATE_BOMBAY` n'est pas un state BIC ;
- aucun bloc `region_state:BIC` n'existe a Bombay ;
- le port de Bombay appartient a `POR` et `MARATH` selon les blocs de batiments ;
- le chantier naval de Bombay appartient a `MARATH` ;
- les restrictions interdisent de toucher a `MARATH`, aux frontieres et aux ownerships ;
- la solution alternative `East India Company Marine` serait possible techniquement au Bengal, mais le prompt demande de preferer ne rien creer si Bombay n'est pas BIC.

Recommandation future :

- creer une phase future distincte si le mod decide de representer une marine BIC non-bombayenne ;
- nom possible pour cette future phase : `East India Company Marine` plutot que `Bombay Marine` ;
- base future la plus propre techniquement : `STATE_WEST_BENGAL`, car BIC y possede 6 niveaux de port et 2 niveaux de chantier naval ;
- garder la limite stricte : 1 fregate maximum, aucun vaisseau de ligne, aucun amiral.

## 6. Confirmation des restrictions

| Restriction | Resultat |
| --- | --- |
| Aucun vaisseau de ligne | Confirme : aucun navire cree. |
| Pas plus d'une fregate | Confirme : aucune fregate creee. |
| Aucun amiral | Confirme : aucun personnage cree. |
| Aucune loi navale | Confirme : `common/history/countries/bic - british east india company.txt` non modifie. |
| Aucun changement a GBR | Confirme. |
| Aucun changement a MARATH | Confirme. |
| Aucun changement a TRA / Travancore | Confirme. |
| Aucune technologie modifiee | Confirme. |
| Aucune PM modifiee | Confirme. |
| Aucune pop modifiee | Confirme. |
| Aucune frontiere ou ownership modifiee | Confirme. |
| Aucune localisation inutile | Confirme : pas de fichier de localisation cree. |

## 7. Risques restants

- La presence historique de la Bombay Marine n'est pas encore representee en jeu.
- BIC reste sans flotte propre malgre ses ports et chantiers au Bengal.
- Une future flotte `East India Company Marine` pourrait etre justifiee techniquement, mais elle devra etre documentee comme une abstraction regionale et non comme la vraie Bombay Marine.
- Si une future refonte historique donne Bombay a BIC, alors `Bombay_Marine` pourra etre creee proprement.

## 8. Tests a faire en jeu

Comme aucune flotte n'a ete creee, les tests sont surtout des tests de non-regression :

1. Lancer une nouvelle partie 1776.
2. Verifier que BIC reste sans flotte propre.
3. Verifier que `GBR`, `MARATH` et `TRA` n'ont pas change.
4. Verifier que Bombay reste controlee par les tags actuels du mod.
5. Surveiller `error.log` pour confirmer qu'aucune nouvelle erreur de formation navale, de localisation ou de batiment n'apparait.

## 9. Liste exacte des fichiers modifies

Fichier cree :

- `docs/reports/navy/PHASE_NAVY_3C_2_BIC_BOMBAY_MARINE.md`

Aucun fichier gameplay n'a ete modifie.
Aucun fichier de localisation n'a ete cree.

## 10. Fichiers consultes

- `docs/reports/navy/PHASE_NAVY_3C_INDIAN_NAVAL_AUDIT.md`
- `docs/reports/navy/PHASE_NAVY_3A_NON_EUROPEAN_NAVAL_AUDIT.md`
- `docs/reports/navy/PHASE_NAVY_3C_2_BIC_NAVAL_DECISION.md`
- `common/history/buildings/10_india.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/states/00_states.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/history/diplomacy/00_relations.txt`
- `common/history/countries/bic - british east india company.txt`
- `common/history/military_formations/05_military_formations_india.txt`

