# Phase 1.7 - Nettoyage minimal Japon / The Great Wave

## 1. Resume des corrections faites

Corrections appliquees :
- retrait de l'ajout initial de `je_terakoya` au Japon ;
- conservation de `law_terakoya` comme loi initiale japonaise ;
- ajout de `RYU` comme pays minimal valide ;
- transfert de Ryukyu / Nansei-shoto vers le setup vanilla 1.13 : `RYU` possede deux provinces, `JAP` conserve Amami en province non incorporee ;
- ajout de la relation `JAP -> RYU` en `tributary` ;
- remplacement de `law_frontier_colonization` par `law_no_colonial_affairs` pour le Japon ;
- ajout de `je_sakoku` au demarrage du Japon ;
- ajout des trois formations militaires japonaises vanilla 1.13.

Aucune correction n'a ete faite sur l'Australie, le Moyen-Orient, les technologies, les formations militaires d'autres pays ou la localisation generale.

## 2. Terakoya

`je_terakoya` etait ajoutee dans :

- `common/history/countries/jap - japan.txt`

Ligne retiree :

```txt
add_journal_entry = { type = je_terakoya }
```

Etat apres correction :
- `je_terakoya` existe encore dans `common/journal_entries/00_meiji_restoration.txt` ;
- elle n'est plus ajoutee au demarrage du Japon ;
- `law_terakoya` reste active dans `common/history/countries/jap - japan.txt` ;
- aucune localisation ou condition de `je_terakoya` n'a ete modifiee.

Justification :
- The Great Wave utilise `law_terakoya` comme loi d'education ;
- `je_terakoya` est une ancienne entree brute dans le mod et ne doit pas etre reparee ici.

## 3. Ryukyu / RYU

Setup vanilla observe :
- `RYU` existe dans `common/country_definitions/00_countries.txt` ;
- `RYU` est un pays `unrecognized`, tier `kingdom`, culture `ryukyuan`, religion `confucian` ;
- `STATE_RYUKYU_ISLANDS` est partagee :
  - `RYU` possede `xF0F061` et `xBB27F6` ;
  - `JAP` possede `xF0D080` en `unincorporated` ;
- `JAP` a `RYU` comme `tributary`.

Setup ajoute au mod :
- ajout de `RYU` dans `common/country_definitions/00_countries.txt` ;
- ajout de `common/history/countries/ryu - ryukyu.txt` ;
- `STATE_RYUKYU_ISLANDS` alignee sur le decoupage vanilla ;
- buildings de `RYU` ajoutes dans `common/history/buildings/11_east_asia.txt` ;
- pops de `RYU` ajoutees dans `common/history/pops/11_east_asia.txt` ;
- relation `JAP -> RYU` ajoutee dans `common/history/diplomacy/00_subject_relationships.txt`.

Verification provinces :
- 3 provinces trouvees dans `STATE_RYUKYU_ISLANDS` ;
- 3 provinces uniques ;
- aucune province manquante par rapport au set vanilla `xF0F061`, `xF0D080`, `xBB27F6`.

Double dependance historique :
- la vanilla contient aussi du contenu diplomatique sur la double subordination Japon / Chine ;
- cette phase ne recree pas tout ce systeme ;
- le choix minimal est de reprendre le lien sujet direct vanilla `JAP -> RYU` en `tributary`.

## 4. Lois japonaises

Lois confirmees actives :
- `law_bakufu`
- `law_sakoku`
- `law_terakoya`

Correction de la loi coloniale :
- ID retire : `law_frontier_colonization`
- ID ajoute : `law_no_colonial_affairs`

Justification :
- le Japon vanilla 1.13 ne commence pas avec `law_frontier_colonization` ;
- `law_sakoku` est incompatible avec une politique coloniale active ;
- `law_no_colonial_affairs` est le remplacement conservateur le plus clair.

Note :
- la technologie `colonization` n'a pas ete modifiee, conformement aux restrictions.

## 5. Armees japonaises

Comparaison :
- le mod ne contenait aucun bloc `c:JAP` dans `common/history/military_formations/06_military_formations_asia.txt` ;
- la vanilla 1.13 contient trois formations japonaises :
  - `Edo_Guard_Army` ;
  - `Kinai_Guard_Army` ;
  - `Kyushu_Guard_Army`.

Correction faite :
- ajout du bloc vanilla `c:JAP` dans `common/history/military_formations/06_military_formations_asia.txt` ;
- total ajoute : 58 unites `combat_unit_type_irregular_infantry` ;
- aucun commandant n'a ete cree ou modifie ;
- aucune formation d'un autre pays n'a ete modifiee.

Pourquoi la correction est minimale :
- elle ajoute uniquement les formations manquantes de `JAP` ;
- elle ne reequilibre pas l'armee japonaise ;
- elle ne touche pas aux personnages ni aux commandants.

## 6. The Locked Country

ID trouve :
- `je_sakoku`

Fichier vanilla :
- `common/journal_entries/07_sakoku.txt`

Correction faite :
- ajout de `add_journal_entry = { type = je_sakoku }` dans `common/history/countries/jap - japan.txt`.

Raison :
- The Locked Country / Pays verrouille correspond a la logique de `law_sakoku` ;
- le Japon commence maintenant avec `law_sakoku`, donc l'entree doit etre active des le depart.

## 7. Tenpo Crisis

ID trouve :
- `je_tenpo_crisis`

Event vanilla associe :
- `tenpo_events.1`

Fichiers vanilla observes :
- `common/journal_entries/07_tenpo_crisis.txt`
- `events/japan_events/ep2_tenpo_events.txt`
- `common/history/countries/jap - japan.txt`

Pourquoi elle ne doit pas apparaitre au debut :
- la partie du mod commence en 1776 ;
- la crise Tenpo est liee a la periode Tenpo du XIXe siecle ;
- l'ajouter au setup initial de 1776 serait anachronique.

Declenchement vanilla :
- en vanilla 1.13, `je_tenpo_crisis` et `tenpo_events.1` sont ajoutes depuis l'historique initial de `JAP`, car la vanilla commence en 1836 ;
- aucun on_action date futur equivalent n'a ete trouve dans le mod.

Blocage par le mod :
- le mod ne semble pas bloquer les fichiers vanilla `07_tenpo_crisis.txt` ou `ep2_tenpo_events.txt` ;
- en revanche, comme le depart est en 1776, le declenchement futur de Tenpo demande probablement une phase dediee avec trigger date/event/on_action ;
- aucune correction Tenpo n'a ete faite dans cette phase.

## 8. Fichiers modifies

- `common/country_definitions/00_countries.txt`
- `common/history/countries/jap - japan.txt`
- `common/history/countries/ryu - ryukyu.txt`
- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/history/military_formations/06_military_formations_asia.txt`
- `PHASE1_7_JAPAN_DLC_CLEANUP.md`

## 9. Volontairement repousse

- reecriture ou suppression de `common/journal_entries/00_meiji_restoration.txt` ;
- localisation de `je_terakoya` ;
- systeme complet de rivalite Ryukyu Japon / Chine ;
- personnages de Ryukyu ;
- declenchement date de `je_tenpo_crisis` depuis un depart 1776 ;
- refonte complete des armees japonaises ou des commandants.

## 10. Risques restants

- `je_tenpo_crisis` ne devrait pas apparaitre en 1776, mais ne dispose pas encore d'un declencheur futur adapte au start date du mod.
- `RYU` peut manquer de personnage historique si le jeu ne genere pas un dirigeant satisfaisant.
- `je_sakoku` depend du contenu vanilla The Great Wave ; si un replace path externe le masque, il faudra importer ou adapter le fichier.
- Le maintien du modifier `hokkaido_colonization_modifier` dans le setup Japon peut demander un diagnostic separe, car cette phase ne corrigeait que la loi coloniale.

## 11. Tests a faire ensuite

1. Lancer une partie 1776 avec le Japon.
2. Verifier que `je_terakoya` n'apparait plus au demarrage.
3. Verifier que `law_terakoya` reste active.
4. Verifier que `je_sakoku` / The Locked Country apparait au demarrage.
5. Verifier que `law_bakufu`, `law_sakoku` et `law_no_colonial_affairs` sont actives.
6. Verifier que Ryukyu existe comme `RYU`.
7. Verifier que `RYU` est tributaire du Japon.
8. Verifier que `STATE_RYUKYU_ISLANDS` n'a aucune province blanche.
9. Verifier que le Japon commence avec trois formations : Edo, Kinai et Kyushu.
10. Faire tourner au moins un mois et surveiller `error.log` pour `RYU`, `je_sakoku`, `je_terakoya`, `je_tenpo_crisis`, `law_no_colonial_affairs` et les formations japonaises.
