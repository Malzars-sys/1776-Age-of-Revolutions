# HOTFIX-6A.3R — Résolution des hunks DEI Cape/Ceylon

Date : 2026-07-23  
Périmètre : résolution statique documentaire, aucun runtime, aucun gameplay

## 1. Résumé

Les deux décisions sont fermées. La boucle actuelle de `dei_breakup.1.a` ne peut transférer ni la portion DEI de Ceylon ni les portions DEI de Cape Colony et Eastern Cape. Les bénéficiaires sûrs sont les tags existants `CEY` et `SAF`, dont les capitales déclarées sont respectivement `STATE_CEYLON` et `STATE_CAPE_COLONY`. Les deux pays doivent être créés indépendants depuis la portion DEI de leur État si le tag n’existe pas, ou recevoir cette portion par `set_state_owner` s’ils existent déjà. Les sept écarts DEI identiques hotfix/vanilla 1.13 sont admis comme alignements ciblés.

## 2. Verdicts d’entrée

- `HOTFIX_6A3_DEI_TARGETED_AUDIT_COMPLETE`
- `NO_REQUIRED_HOTFIX_DELTA_IDENTIFIED`
- `DEI_CAPE_CEYLON_OUTCOME_UNVERIFIED`
- `DEI_VANILLA_1_13_ALIGNMENT_REQUIRES_RESOLUTION`
- `NAVY_PROTECTED`
- `ADMIN_PROTECTED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## 3. État Git

Racine et branche conformes, HEAD `770ca6c Audit DEI breakup hotfix deltas`, zéro fichier suivi modifié au départ, zéro staged, stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` intact et aucun processus Victoria/launcher. Les seuls chemins non suivis sont `bject` et `docs/research/technology/`, protégés et laissés intacts.

## 4. Sources

Ont été lus : audit et delta map 6A.3, C1AI, roadmap, inventaire global, registre restant, audit upstream DLC, clôture Inde/BIC, NAVY-2B-bis, les trois versions de `events/dei_breakup.txt`, les historiques d’États/bâtiments/pops/diplomatie/traités, les définitions de pays, les journaux et événements dépendants, ainsi que les scripts vanilla 1.13 servant de preuve d’API.

## 5. Méthode

Les blocs ont été extraits par ancre et équilibre d’accolades. Les références ont été contrôlées avec `Get-ChildItem`, `Get-Content`, `Select-String`, `Get-FileHash`, Git et comparaison trois voies. L’adjacence terrestre a été reconstruite statiquement depuis `map_data/provinces.png`, puis recroisée avec les listes de provinces vanilla 1.13 et l’ownership 1776. Aucun `rg`, runtime ou changement de source externe.

## 6. Changelog DEI

Le changelog hotfix annonce que la rupture de DEI doit faire perdre Cape Colony et Ceylon. Le fork et la source hotfix possèdent pourtant le même setup territorial 1776, et le bloc DEI hotfix est identique à vanilla 1.13. Il faut donc un hunk territorial local explicite ; aucun import complet n’est justifié.

## 7. Fonction actuelle de `dei_breakup.1`

Dans l’option `dei_breakup.1.a`, la boucle choisit un pays qui est sujet de ROOT ou possède une culture primaire de langue malaise, mais seulement s’il détient un État voisin d’un État non capital, non homeland javan, appartenant à ROOT. Elle transfère ensuite un État ROOT voisin avec `set_state_owner`. Après la boucle, les sujets de DEI deviennent indépendants, puis le pays change de tag en `JAV`. Les options `b` et `c` n’exécutent pas cette boucle.

## 8. Setup Ceylon

`STATE_CEYLON` contient quinze provinces. DEI en possède treize : `xA0EFCC xA0A0D0 x23CE5A x8D6FA8 xDF2050 xDAB923 x1DA090 xC18817 x8A707A x967CCE x602050 xC23350 x47B038`; MLD possède `x95AAA3`; GBR possède `x5B5C22`. Homelands : tamil et sinhala. La portion DEI contient les populations et bâtiments documentés, dont port, administration, pêcherie, thé et café.

## 9. Bénéficiaires Ceylon

`KND` n’existe ni dans les définitions ni dans l’historique. `BIC` existe mais n’a ni capitale, culture ni relation justifiant Ceylon et son workflow Inde est protégé. `BCE` existe comme tag colonial britannique à culture britannique mais ne détient aucun territoire en 1776. `MLD` détient une île de la région mais n’est pas adjacent à la portion DEI. `CEY` existe, a pour culture primaire `sinhala`, pour capitale `STATE_CEYLON`, et possède ses définitions de drapeau. C’est le bénéficiaire local exact.

## 10. Décision Ceylon

`CEYLON_SHOULD_BECOME_INDEPENDENT`. Si `CEY` existe, la portion `s:STATE_CEYLON.region_state:DEI` lui est transférée. Sinon `create_country` crée `CEY` depuis cette portion avec `origin = ROOT`. Un éventuel lien de sujet préexistant est rompu par `make_independent`. MLD et GBR conservent leurs provinces. Aucun fichier d’historique territorial n’est modifié.

## 11. Setup Cape Colony

DEI possède vingt-sept provinces de `STATE_CAPE_COLONY`; NAM en possède seize. Homelands : boer, sotho et khoisan. DEI dispose d’un claim initial. La portion DEI contient ferme, vignoble, pêcherie et port, avec ownerships DEI.

## 12. Setup Eastern Cape

DEI possède vingt-et-une provinces de `STATE_EASTERN_CAPE`; XHO en possède dix-sept. Homelands : xhosa, boer et khoisan. DEI dispose d’un claim initial. La portion DEI contient ferme et élevage, avec manor houses détenus par DEI.

## 13. Bénéficiaires Cape

`SAF` n’est pas territorialement actif au départ mais son tag existe, sa capitale est `STATE_CAPE_COLONY`, et les scripts ultérieurs attendent explicitement un `region_state:SAF` à Eastern Cape. `ORA` et `WBL` existent, mais leurs provinces ne touchent pas directement les portions DEI ciblées. `XHO`, `NAM`, `TSW`, `BST` et `PHL` touchent une portion DEI, mais représentent des pays régionaux distincts et aucun ne porte le rôle global prévu par `SAF`. `KND` est absent et non pertinent.

## 14. Décision Cape

`CAPE_SHOULD_BECOME_INDEPENDENT`. Si `SAF` existe, il reçoit les portions DEI de `STATE_CAPE_COLONY` et `STATE_EASTERN_CAPE`. Sinon `create_country` crée `SAF` depuis la portion DEI de Cape Colony, puis `set_state_owner` lui attribue la portion DEI d’Eastern Cape. Un éventuel lien de sujet préexistant est rompu par `make_independent`. Les portions NAM et XHO restent inchangées.

## 15. Adjacence

La portion DEI de Ceylon ne touche que des provinces maritimes ; elle n’a aucun voisin terrestre détenu. Eastern Cape DEI touche Cape Colony DEI, XHO, TSW, BST et PHL. Cape Colony DEI touche Eastern Cape DEI, NAM et TSW. Aucun de ces pays n’est sujet de DEI ou porteur d’une culture primaire de langue malaise. La condition de la boucle est donc fausse pour ces territoires.

## 16. Sujets DEI

Les seuls pactes sujets initiaux de DEI sont les puppets `YOG`, `SRK` et `COC`. Aucun ne touche Ceylon ou le Cap. BCE est commenté sous GBR et n’existe pas territorialement. SAF, CEY, ORA, WBL, XHO, NAM, TSW, BST, PHL et MLD ne sont pas sujets de DEI.

## 17. Cultures primaires

DEI : dutch; CEY : sinhala; BCE, BIC et SAF : british; ORA : boer; WBL et PHL : griqua; XHO : xhosa; NAM : khoisan; TSW : tswana; BST : sotho; MLD : sinhala; YOG/SRK : javan; COC : malayalam. Les seuls sujets malais admissibles sont ceux déjà utilisés dans l’archipel, pas les bénéficiaires Cape/Ceylon.

## 18. `change_tag`

`change_tag = JAV` ou `IDN` conserve l’entité pays, ses territoires, claims, traités, bâtiments détenus et personnages ; il ne cède aucun État. Il doit rester après les transferts, afin que ROOT soit encore DEI lors de la sélection des portions territoriales.

## 19. `make_independent`

`make_independent = yes` rompt la relation de sujet des pays existants. Il ne crée pas CEY/SAF et ne transfère aucune portion d’État. Les pays créés par `create_country` sont indépendants tant qu’aucun pacte sujet n’est ajouté.

## 20. `independence.2`

L’événement `independence.2` ne transfère aucun État. Ses options activent une loi de gouvernement et sa cancellation trigger exige que le pays ne soit plus sujet. Le délai d’un jour vanilla évite l’ouverture imbriquée avant la stabilisation du changement de tag et des cultures.

## 21. API de transfert

Vanilla 1.13 utilise `create_country = { origin = root tag = TAG state = STATE_SCOPE }` pour créer un tag depuis une portion d’État et `set_state_owner = COUNTRY_SCOPE` depuis un state scope. Le scripted effect vanilla `transfer_state` est seulement un wrapper autour de `set_state_owner`; il n’est pas requis. `release` n’est pas un effet script utilisé. Les hunks retenus n’inventent aucune API.

## 22. Hunk territorial minimal

À insérer uniquement au début de l’effet de l’option `dei_breakup.1.a`, avant le `while` existant :

```txt
		# Release the non-Indonesian colonial territories before the breakup loop.
		if = {
			limit = {
				s:STATE_CEYLON = {
					any_scope_state = { owner = ROOT }
				}
			}
			if = {
				limit = { exists = c:CEY }
				s:STATE_CEYLON.region_state:DEI ?= { set_state_owner = c:CEY }
			}
			else = {
				create_country = {
					origin = ROOT
					tag = CEY
					state = s:STATE_CEYLON.region_state:DEI
				}
			}
			c:CEY ?= {
				if = {
					limit = { is_subject = yes }
					make_independent = yes
				}
			}
		}
		if = {
			limit = {
				s:STATE_CAPE_COLONY = {
					any_scope_state = { owner = ROOT }
				}
			}
			if = {
				limit = { exists = c:SAF }
				s:STATE_CAPE_COLONY.region_state:DEI ?= { set_state_owner = c:SAF }
			}
			else = {
				create_country = {
					origin = ROOT
					tag = SAF
					state = s:STATE_CAPE_COLONY.region_state:DEI
				}
			}
			c:SAF ?= {
				if = {
					limit = { is_subject = yes }
					make_independent = yes
				}
			}
		}
		if = {
			limit = { exists = c:SAF }
			s:STATE_EASTERN_CAPE.region_state:DEI ?= { set_state_owner = c:SAF }
		}
```

## 23. Bâtiments et pops

`create_country` et `set_state_owner` déplacent les state scopes existants ; les pops et bâtiments restent dans leur portion et ne sont pas recréés. Les ownerships économiques DEI/NET restent attachés à l’entité propriétaire, qui continue d’exister après `change_tag`; ils ne sont donc pas orphelins. Aucun hunk buildings/pops n’est requis.

## 24. Claims et diplomatie

Les claims DEI sur Cape Colony et Eastern Cape restent attachés à l’entité qui devient JAV/IDN ; ils ne sont pas orphelins. Les retirer dépasserait le minimum prouvé et n’est pas retenu. Les traités de transit DEI–ORA et PHL–DEI suivent également l’entité après changement de tag et ne sont pas territoriaux. Aucun traité, pacte ou claim n’est modifié dans le hunk.

## 25. Ulema JAV

`ADMIT_VANILLA_1_13_ALIGNMENT`. Le bloc `ig:ig_devout` applique le nom Sunni Ulema et les trois traits pious fiction, sharia et da’wat avant `change_tag = JAV`. Objets et localisations anglaises/françaises existent dans vanilla 1.13.

## 26. Cultures/personnages JAV

`ADMIT_VANILLA_1_13_ALIGNMENT`. `every_primary_culture`, `save_temporary_scope_as`, `remove_primary_culture`, `every_scope_character` et `retire_character` sont des APIs 1.13 utilisées ailleurs. Le hunk retire génériquement les cultures coloniales, retire leurs personnages de la vie publique, réajoute javan et conserve le reset sunnite. `remove_from_public_life` n’est ni nécessaire ni utilisé par le hunk vanilla.

## 27. Délai JAV

`ADMIT_VANILLA_1_13_ALIGNMENT`. `trigger_event = { id = independence.2 days = 1 }` est valide et sépare l’événement de gouvernement du changement de tag/culture.

## 28. Ulema IDN

`ADMIT_VANILLA_1_13_ALIGNMENT`, pour les mêmes objets, scopes et localisations que JAV.

## 29. Cultures/religion/personnages IDN

`ADMIT_VANILLA_1_13_ALIGNMENT`. Toutes les cultures primaires précédentes sont retirées, les huit cultures IDN sont réajoutées, la religion d’État devient sunnite et les personnages correspondants sont retraités. Les huit cultures correspondent exactement à la définition vanilla 1.13 d’IDN.

## 30. Délai IDN

`ADMIT_VANILLA_1_13_ALIGNMENT`. Même justification que le délai JAV.

## 31. Délai refus

`ADMIT_VANILLA_1_13_ALIGNMENT`. L’option `dei_breakup.1.c` garde son comportement et ne fait que différer `independence.2` d’un jour.

## 32. Validation API 1.13

Les neuf effets/triggers ciblés existent et sont utilisés dans vanilla 1.13. Comptages observés hors simple déclaration : `every_primary_culture` 27, `remove_primary_culture` 62, `save_temporary_scope_as` 308, `every_scope_character` 89, `retire_character` 104, `kill_character` 162, `set_state_religion` 33, `add_primary_culture` 157 et `trigger_event ... days = 1` 43. `create_country`, `set_state_owner`, `change_tag` et `make_independent` ont également des usages vanilla directs.

## 33. Localisations

`ig_sunni_madrasahs`, `ig_trait_pious_fiction`, `ig_trait_sharia` et `ig_trait_da_wat` existent en anglais et en français dans vanilla 1.13. CEY et SAF possèdent leurs définitions de pays et drapeaux. Aucun fichier de localisation, notamment français, n’est requis.

## 34. Collisions 1776

Les transferts ne changent aucune province MLD, GBR, NAM ou XHO. Ils ne modifient ni BIC/Travancore/Inde, ni les historiques de bâtiments/pops, ni les traités. L’insertion reste limitée à l’option `a`; les choix IDN/refus conservent leur disposition territoriale actuelle.

## 35. Rollbacks

Rollback territorial : supprimer exactement les trois blocs `if` ajoutés avant le `while`. Rollback des alignements : retirer chaque bloc Ulema, restaurer les blocs cultures/personnages fork exacts pour JAV et IDN, retirer `set_state_religion = rel:sunni` du bloc IDN, puis retirer uniquement `days = 1` des trois appels. Aucun rollback ne touche `alk_breakup.1`.

## 36. Runtime futur

Après correction, un seul lancement devra vérifier : option `a`, existence/indépendance CEY et SAF, ownership exact des trois portions, maintien MLD/GBR/NAM/XHO, pops/bâtiments, claims/traités, JAV cultures/religion/Ulema/personnages, puis option IDN et refus via sauvegardes préparées si possible. Scanner `error.log` pour scopes, `create_country`, `set_state_owner`, cultures, traits et événements. Aucun runtime n’a lieu en 6A.3R.

## 37. Liste fermée des fichiers

Phase de correction autorisée : `events/dei_breakup.txt`, son rapport de correction, la delta map 6A.3 et les index/roadmap explicitement nommés par le prompt suivant. La présente phase ne modifie que les sept documents autorisés dans son prompt.

## 38. Protections NAVY

`Koloniale_Marine`, trois frégates, aucun capital ship et aucun amiral restent `NAVY_PROTECTED`. Aucun fichier de formation, pays naval ou localisation NAVY n’est touché.

## 39. Protections ADMIN

Les PM et ownerships de bâtiments restent inchangés. Aucun fichier buildings n’est modifié.

## 40. Protections BIC/Travancore

Les journaux Inde, la chaîne Sepoy, Travancore et les fichiers BIC restent clos. `activate_law = law_type:law_frontier_colonization` est préservé ; `law_colonial_exploitation` n’est pas restaurée pour BIC.

## 41. Confirmation blocs clos

Russie, Autriche/Croatie/Suisse, Japon, Mamluk Iraq, Inde, BIC, Travancore et MARATH ne sont pas rouverts. Les six fichiers gameplay 6A.2 restent hors diff.

## 42. Confirmation `docs/research/technology/`

Le répertoire non suivi est resté intact et hors périmètre.

## 43. Confirmation `bject`

Le fichier non suivi `bject` est resté intact et hors périmètre.

## 44. Confirmation stash MARATH

Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est intact; son contenu n’a pas été inspecté.

## 45. Verdict final

- `HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION_COMPLETE`
- `READY_FOR_DEI_TARGETED_FIX`
- `CEYLON_SHOULD_BECOME_INDEPENDENT`
- `CAPE_SHOULD_BECOME_INDEPENDENT`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
