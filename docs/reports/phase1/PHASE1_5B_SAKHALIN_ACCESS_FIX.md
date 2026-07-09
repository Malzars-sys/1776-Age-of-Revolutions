# Phase 1.5b - Correction ciblee de Sakhaline

## 1. Cause probable de Sakhaline infranchissable

Sakhaline etait bien referencee dans l'historique du mod, mais son proprietaire `c:SKH` n'etait pas defini dans `common/country_definitions/00_countries.txt`.

Les fichiers de la Phase 1.5 utilisaient deja `SKH` pour `STATE_SAKHALIN` :
- `common/history/states/00_states.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/pops/11_east_asia.txt`

La state region vanilla Victoria 3 1.13 `STATE_SAKHALIN` n'est pas marquee comme `impassable`, et ses provinces sont presentes dans l'historique de `STATE_SAKHALIN`. L'hypothese la plus probable est donc un proprietaire invalide ou incomplet plutot qu'un probleme de provinces encore manquantes.

## 2. Verification de SKH

- `c:SKH` est utilise dans `common/history/states/00_states.txt`.
- `region_state:SKH` est utilise dans `common/history/buildings/11_east_asia.txt`.
- `region_state:SKH` est utilise dans `common/history/pops/11_east_asia.txt`.
- Avant correction, `SKH` n'etait pas defini dans `common/country_definitions/00_countries.txt`.
- Le mod ne contient pas de fichier `common/history/countries/skh - sakhalin.txt`.
- Le mod contient seulement une localisation de flavor text pour `SKH_FLAVOR_TEXT`, pas une definition pays complete.
- Le dossier `common/cultures` n'existe pas dans le mod.

Comparaison vanilla 1.13 locale :
- Vanilla definit `SKH` dans `common/country_definitions/00_countries.txt`.
- Vanilla donne a `SKH` le type `decentralized`, le tier `principality`, la culture `siberian` et la capitale `STATE_SAKHALIN`.
- Vanilla possede aussi un fichier `common/history/countries/skh - sakhalin.txt`, mais il ne contient que des effets de depart generiques.

## 3. Choix entre Option A et Option B

Option A retenue.

Le mod utilise deja explicitement `c:SKH` pour Sakhaline. La correction la plus sure est donc de rendre `SKH` valide au lieu de reattribuer temporairement la region a un autre pays.

Option B non retenue :
- reattribuer Sakhaline a `JAP`, `RUS`, `AIN` ou `EZO` aurait change le sens historique et gameplay ;
- cela aurait aussi force des ajustements dans les pops et buildings deja structures autour de `region_state:SKH`.

## 4. Fichiers modifies

- `common/country_definitions/00_countries.txt`
- `PHASE1_5B_SAKHALIN_ACCESS_FIX.md`

## 5. Pourquoi la correction est minimale

La correction ajoute seulement le tag pays `SKH`, en reprenant la definition minimale vanilla Victoria 3 1.13 :

```txt
SKH = { # Sakhalin
	color = { 54 102 190 }

	country_type = decentralized

	tier = principality

	cultures = { siberian }
	capital = STATE_SAKHALIN
}
```

Aucun fichier de carte, d'historique de states, de pops, de buildings, de localisation, de technologies ou de formations militaires n'a ete modifie.

Les tags `ULT` et `RYU` n'ont pas ete ajoutes.

## 6. Risques restants

- Si Sakhaline reste grisee, le prochain point a tester sera l'absence d'un fichier minimal `common/history/countries/skh - sakhalin.txt`.
- Comme la localisation pays n'a pas ete modifiee, le nom affiche peut rester dependant de la localisation vanilla ou d'une cle brute selon les replace paths actifs.
- Cette correction ne traite pas les problemes de carte encore possibles en Australie ou ailleurs.
- Cette correction ne change pas l'equilibrage historique ou economique de Sakhaline.

## 7. Tests a faire ensuite

1. Lancer Victoria 3 avec uniquement le mod active.
2. Demarrer une partie en 1776.
3. Aller directement sur Sakhaline.
4. Verifier que Sakhaline n'apparait plus comme zone blanche, grisee ou infranchissable.
5. Cliquer sur Sakhaline et verifier que l'etat appartient a un pays valide.
6. Faire tourner au moins un mois.
7. Surveiller `error.log` pour `SKH`, `STATE_SAKHALIN`, `invalid country`, `invalid owner`, `region_state:SKH` et `PostValidate`.
8. Si le probleme persiste sans erreur de log, comparer ensuite le comportement avec un ajout controle de `common/history/countries/skh - sakhalin.txt`.
