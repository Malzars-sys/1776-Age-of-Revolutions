# USA-COMMANDERS-1776

Statut : **READY_FOR_RUNTIME_VALIDATION**. Profils initiaux déterministes ; aucun test moteur.

## Personnages et affectations

| Personnage | Âge au 1/1/1776 | Fonction historiquement acquise | Trait(s) initial(aux) retenu(s) | Installation |
|---|---:|---|---|---|
| George Washington | 43 | commandant en chef, élu le 15/6/1775 | persistent ; basic_defensive_strategist | corrigé ; armée existante conservée |
| Esek Hopkins | 57 | commandement naval décidé en novembre, commission du 22/12/1775 | direct | corrigé ; flotte existante conservée |
| Charles Lee | 43 | major général, élu le 17/6/1775 ; aile nord du siège de Boston | basic_defensive_strategist | ajouté à l'armée existante |
| Artemas Ward | 48 | premier major général, élu le 17/6/1775 ; aile droite de Boston | cautious ; sickly | ajouté à l'armée existante |
| Israel Putnam | 57 | major général, élu le 19/6/1775 | brave | ajouté à l'armée existante |
| Philip Schuyler | 42 | major général, élu le 19/6/1775 ; département du Nord | meticulous | ajouté, disponible sans affectation forcée |
| Nathanael Greene | 33 | brigadier général continental du 22/6/1775, brigade de Rhode Island à Boston | inexperienced | ajouté, disponible sans affectation forcée |

Les grades natifs restent au rang 1 pour les cinq ajouts. Ce rang est une capacité et un coût de jeu, pas une traduction exacte de brigadier/major général. Aucun corps, bataillon ou flotte supplémentaire n'est créé. MIL-USA garde 13 réguliers, 15 conscrits non levés, ses états d'origine et ses cinq navires.

Le jeu ne représente pas une hiérarchie en chef/département/brigade à l'intérieur d'une formation. Quatre généraux sont affectés à l'unique armée de Boston ; Schuyler reste disponible pour un détachement du Nord décidé par le joueur. Greene n'est pas placé artificiellement à la tête d'une seconde armée autonome : il est disponible pour une affectation ultérieure. Cette réserve est une abstraction du moteur ; elle ne signifie pas qu'ils étaient sans emploi historique.

## Sources, décisions et incertitudes

Les [Journals of the Continental Congress, vol. II](https://tile.loc.gov/storage-services/service/ll/llscd/lljc002/lljc002.pdf), entrées des 15, 17, 19 et 22 juin 1775, établissent les élections et l'ordre d'ancienneté. La date d'acceptation/démission britannique de Lee le 22 juin ne remplace pas son élection du 17. Greene est brigadier au départ ; sa promotion d'août 1776 n'est pas anticipée.

Le [National Park Service sur Ward](https://www.nps.gov/people/artemas-ward.htm) fournit sa naissance, son travail d'organisation, sa prudence et les problèmes de santé déjà présents avant son retrait. `sickly` est une abstraction de santé, sans mort ou démission imposée à une date historique.

Le [NPS sur Charles Lee](https://www.nps.gov/people/charles-lee.htm) confirme sa naissance du 6 février 1732 et son expérience professionnelle, ainsi que son rôle au siège. Un seul trait de défense de base est retenu : aucune compétence experte ni personnalité punitive tirée de ses controverses ultérieures.

Le [NPS sur Putnam](https://home.nps.gov/people/israel-putnam.htm) documente son expérience de guerre, son courage et sa proximité avec les soldats. Le trait brave représente cela ; pas de génie tactique. Pour la date de nomination, les Journals du Congrès priment sur la formulation imprécise « early June » de cette notice.

Le [NPS sur Schuyler](https://www.nps.gov/people/philip-schuyler.htm) donne le 20 novembre 1733 et son département du Nord. Une notice navale donne une autre date de naissance : la date NPS est retenue explicitement. Le rôle logistique du département apparaît aussi dans [l'histoire du Quartermaster's Department, US Army CMH](https://webdoc.sub.gwdg.de/ebook/p/2005/CMH_2/www.army.mil/cmh-pg/books/revwar/risch/chpt-2.htm). meticulous est une interprétation limitée de cette fonction administrative ; pas un diagnostic psychologique établi.

La [Library of Congress sur Greene](https://www.loc.gov/item/today-in-history/august-07) donne sa naissance du 7 août 1742 et situe sa promotion à major général en août 1776. Son apprentissage initial est représenté par inexperienced, sans lui attribuer ses talents opérationnels de 1780 dès janvier 1776. Ce trait ne signifie pas que les miliciens n'étaient pas entraînés.

Le [Naval History and Heritage Command sur Hopkins](https://www.history.navy.mil/browse-by-topic/people/historical-figures/esek-hopkins.html) distingue son expérience de capitaine/corsaire et sa désignation de novembre ; la [liste des commissions navales](https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/o/officers-of-the-continental-navy-and-marine-corps.html) donne le 22 décembre. direct est une abstraction de son expérience de combat maritime ; ni héroïsation de Nassau, encore futur, ni malus anticipant sa révocation. basic_naval_commander est écarté parce que son déblocage actuel state_dockyard_systems manque aux USA.

Pour Washington, persistent et défense de base représentent la tenue du siège et l'effort d'organisation, documentés par [Washington au Congrès le 31 décembre 1775](https://founders.archives.gov/documents/Washington/03-02-02-0579). Le profil ne lui donne aucun trait expert ou bonus d'attaque général.

Les cinq nouveaux noms utilisent des clés propres au mod, traduites à l'identique en FR/EN puisqu'il s'agit de noms propres. Lee utilise la culture yankee comme abstraction de son service américain et son domicile virginien, sans prétendre qu'il était né en Nouvelle-Angleterre ; Schuyler est assimilé à cette culture faute de culture nationale hollandaise américaine distincte dans ce lot. Greene utilise le protestantisme englobant ses origines quakers, sans transformer une conviction en trait pacifiste incompatible avec son engagement.

## Mécanique et équilibre

Les modèles natifs actuels utilisent `traits = { ... }` et `trait_generation = { }` pour des personnages historiques (exemple canonique : country_arg.txt). Le défaut du mod ajoute sinon une personnalité, une compétence et parfois un trait supplémentaire selon l'âge. Chacun des sept modèles de ce lot remplace ce générateur par un bloc vide. Compliant et Pillager ne figurent dans aucun profil initial. **La progression ultérieure des traits reste native** : cette correction porte sur la création, pas sur toutes les évolutions futures possibles.

Effets pertinents des traits existants du mod, sans changement de leurs définitions :

| Profil | Effets de commandement principaux |
|---|---|
| Washington | perte de moral −15 %, défense +10 %, conditions retranché/camouflé +1 |
| Lee | défense +10 %, mêmes conditions +1 |
| Ward | perte de moral −5 % ; santé +0,30 puis −0,20, autres effets selon le rôle |
| Putnam | perte de moral −10 %, popularité +25 ; santé −0,05 |
| Schuyler | attaque/défense +5 %, récupération des hommes +0,10, conditions de manœuvre ; pas +10 % de récupération du moral |
| Greene | attaque/défense −5 %, récupération du moral +10 % |
| Hopkins | dégâts coque/équipage +5 %, vulnérabilité +5 % |

Les modificateurs de commandement s'appliquent aux troupes effectivement commandées selon les règles natives, pas comme la somme de six bonus nationaux. Les cinq ajouts de rang 1 impliquent aussi 50 de coût de bureaucratie total si tous restent employés, selon la définition native du rang. Relever leur coût réel dans le budget. Aucun de ces personnages n'est nommé chef de groupe d'intérêt, souverain ou dirigeant d'entreprise.

## Vérification à poursuivre en jeu

L'outil global vérifie les références, les sept profils, les naissances antérieures au départ, les traits, les deux localisations, les scopes et la conservation des formations. En jeu : trois nouvelles parties avec des graines différentes ; contrôler immédiatement les 6 généraux et 1 amiral, les quatre affectations à l'armée, Hopkins à sa flotte, et la disponibilité de Schuyler/Greene. Contrôler les noms, portraits générés, âges, coûts, absence initiale de Compliant/Pillager, 13/15 bataillons et 5 navires après 1 jour/1 mois/3 mois. Tester une réaffectation volontaire des deux réserves. La capacité réelle du moteur à conserver un général sans affectation reste à confirmer ; ne pas créer d'unités pour contourner un problème éventuel.
