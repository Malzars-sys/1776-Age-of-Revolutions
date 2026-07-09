# Phase 1.6 - Alignement minimal Japon / The Great Wave 1.13

## 1. Resume des changements faits

Cette phase corrige uniquement le setup nord du Japon et les lois initiales japonaises les plus evidentes.

Changements principaux :
- ajout de `ULT` comme pays minimal valide ;
- ajout d'historiques pays minimaux pour `EZO`, `SKH` et `ULT` ;
- transfert du nord de `STATE_HOKKAIDO` de `AIN` vers `EZO` ;
- decoupage de `STATE_SAKHALIN` entre `SKH`, `AIN`, `ULT`, `EZO` et `ALK`, selon les provinces vanilla 1.13 ;
- ajout de la relation sujet `JAP -> EZO` en `vassal` ;
- activation initiale de `law_bakufu`, `law_sakoku` et `law_terakoya` pour le Japon.

Rien n'a ete change pour l'Australie, le Moyen-Orient, les technologies, les formations militaires ou la localisation generale.

## 2. Comparaison avec la vanilla 1.13 / The Great Wave

Vanilla 1.13 :
- `EZO` existe comme Ezochi.
- `JAP` a `EZO` comme vassal.
- `STATE_HOKKAIDO` est principalement `EZO`, avec une enclave japonaise.
- `STATE_SAKHALIN` est partagee entre `SKH`, `AIN`, `ULT`, `EZO` et `ALK`.
- `RYU` existe et est tributaire du Japon, mais cette phase ne l'ajoute pas au mod.
- Le Japon commence avec `law_bakufu`, `law_sakoku` et `law_terakoya`.

Mod avant Phase 1.6 :
- `EZO` etait defini mais n'avait pas de setup territorial actif.
- `STATE_HOKKAIDO` etait partage entre `AIN` et `JAP`.
- `STATE_SAKHALIN` appartenait entierement a `SKH`.
- `ULT` n'etait pas defini.
- Le Japon commencait avec `law_autocracy`, `law_isolationism` et `law_no_schools`.
- `je_terakoya` etait ajoutee directement, mais sans localisation trouvee dans le mod.

Mod apres Phase 1.6 :
- le nord de Hokkaido est attribue a `EZO` ;
- Sakhaline utilise toutes les provinces vanilla 1.13, sans doublon ni province manquante ;
- le Japon conserve la logique 1776 du mod autant que possible, notamment ses technologies et autres lois non concernees.

## 3. Setup final des entites

### Japon

`JAP` conserve son setup general du mod 1776, avec ces changements locaux :
- `law_bakufu` remplace `law_autocracy` ;
- `law_sakoku` remplace `law_isolationism` ;
- `law_terakoya` remplace `law_no_schools` ;
- `EZO` devient vassal de `JAP`.

Le Japon garde ses provinces du Japon central et son enclave sud de Hokkaido.

### Ezochi

`EZO` existe comme entite distincte :
- definition pays deja presente dans `common/country_definitions/00_countries.txt` ;
- historique pays ajoute dans `common/history/countries/ezo - ezochi.txt` ;
- controle le nord de `STATE_HOKKAIDO` ;
- controle trois provinces de `STATE_SAKHALIN` ;
- est vassal de `JAP`.

### Sakhaline

`STATE_SAKHALIN` est maintenant decoupee entre :
- `SKH` ;
- `AIN` ;
- `ULT` ;
- `EZO` ;
- `ALK`.

Le total de population de Sakhaline du mod, 40 004 habitants, a ete conserve et redistribue selon la structure vanilla 1.13. Cela evite de remplacer brutalement le setup demographique du mod 1776 par les chiffres vanilla plus faibles.

### Ainu Mosir / Evenk / autres entites locales

- `AIN` reste defini et possede une partie de Sakhaline.
- `SKH` reste proprietaire principal d'une partie de Sakhaline.
- `ULT` est ajoute comme tag minimal, avec capitale `STATE_SAKHALIN`.
- `ALK` existait deja dans le mod ; ses deux provinces vanilla de Sakhaline ont ete reprises.
- `RYU` reste volontairement non ajoute.

## 4. Relations diplomatiques ajoutees

Dans `common/history/diplomacy/00_subject_relationships.txt` :

```txt
c:JAP ?= {
	create_diplomatic_pact = {
		country = c:EZO
		type = vassal
	}
}
```

La relation `JAP -> RYU` de la vanilla n'a pas ete ajoutee dans cette phase.

## 5. Provinces / states modifies

States modifies :
- `STATE_HOKKAIDO`
- `STATE_SAKHALIN`

`STATE_SAKHALIN` a ete verifiee contre la liste vanilla 1.13 :
- 31 provinces trouvees ;
- 31 provinces uniques ;
- aucune province vanilla manquante ;
- aucune province supplementaire.

## 6. Fichiers modifies

- `common/country_definitions/00_countries.txt`
- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`
- `common/history/countries/jap - japan.txt`
- `common/history/countries/ezo - ezochi.txt`
- `common/history/countries/skh - sakhalin.txt`
- `common/history/countries/ult - ulta.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `PHASE1_6_JAPAN_GREAT_WAVE_ALIGNMENT.md`

## 7. Diagnostic Bakufu

Cause probable :
- le fichier `common/history/countries/jap - japan.txt` activait encore `law_autocracy` ;
- `law_bakufu` existe en vanilla 1.13 et est localisee en francais ;
- la vanilla 1.13 active `law_bakufu` au depart pour `JAP`.

Correction faite :
- remplacement de `activate_law = law_type:law_autocracy` par `activate_law = law_type:law_bakufu`.

## 8. Diagnostic Sakoku

Cause probable :
- le fichier Japon du mod activait `law_isolationism` ;
- `law_sakoku` existe en vanilla 1.13 comme variante japonaise de l'isolationnisme ;
- la vanilla 1.13 active `law_sakoku` au depart pour `JAP`.

Correction faite :
- remplacement de `activate_law = law_type:law_isolationism` par `activate_law = law_type:law_sakoku`.

## 9. Diagnostic Terakoya

Constat :
- `law_terakoya` existe en vanilla 1.13 et est localisee en francais ;
- le mod activait encore `law_no_schools` ;
- `je_terakoya` existe dans `common/journal_entries/00_meiji_restoration.txt` ;
- `je_terakoya` est ajoutee directement dans `common/history/countries/jap - japan.txt` ;
- aucune localisation `je_terakoya` n'a ete trouvee dans le mod ni dans la recherche vanilla locale ;
- l'entree de journal se complete avec `institution_schools >= 3`, ce qui ne correspond pas clairement a la loi `law_terakoya`.

Correction faite :
- remplacement de `activate_law = law_type:law_no_schools` par `activate_law = law_type:law_terakoya`.

Correction non faite :
- pas de reecriture de `je_terakoya` ;
- pas d'ajout de localisation ;
- pas de changement des conditions de completion.

## 10. Repousse a Phase 1.7

A traiter plus tard :
- localisation de `je_terakoya` ;
- coherence entre `je_terakoya`, `law_terakoya` et `institution_schools` ;
- verification complete des journal entries japonaises The Great Wave ;
- integration eventuelle de `je_sakoku`, `je_tenpo_crisis` et du contenu DLC lie ;
- diagnostic de `RYU` et des relations Ryukyu-Japon sans ajout automatique.

## 11. Risques restants

- `ULT` n'a pas de localisation modded, mais la localisation vanilla existe normalement si elle n'est pas masquee.
- `EZO`, `SKH` et `ULT` utilisent des historiques pays minimaux ; un futur test peut reveler des besoins de lois, IG ou personnages plus precis.
- `je_terakoya` peut rester affichee en cle brute tant que sa localisation n'est pas ajoutee.
- Le decoupage de Sakhaline est technique et inspire de la vanilla 1.13 ; il n'est pas encore une refonte historique complete du contexte 1776.
- `RYU` reste volontairement non traite.

## 12. Tests a faire

1. Lancer le jeu avec uniquement le mod actif.
2. Demarrer une partie en 1776 avec le Japon.
3. Verifier que Hokkaido affiche `EZO` comme entite distincte.
4. Verifier que `EZO` est bien sujet/vassal du Japon.
5. Verifier que Sakhaline n'a aucune province blanche ou infranchissable.
6. Verifier que `SKH`, `AIN`, `ULT`, `EZO` et `ALK` apparaissent correctement sur Sakhaline.
7. Verifier les lois initiales japonaises : Bakufu, Sakoku, Terakoya.
8. Verifier si `je_terakoya` reste en cle brute.
9. Faire tourner au moins un mois.
10. Surveiller `error.log` pour `EZO`, `SKH`, `ULT`, `STATE_SAKHALIN`, `law_bakufu`, `law_sakoku`, `law_terakoya` et `je_terakoya`.
