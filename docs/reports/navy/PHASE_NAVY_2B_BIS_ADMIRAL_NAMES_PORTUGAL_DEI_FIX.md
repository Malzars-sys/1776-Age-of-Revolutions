# Phase NAVY-2B-bis - Noms d'amiraux, Portugal et DEI

## 1. Resume

Cette phase corrige uniquement les points observes apres test en jeu de NAVY-2B :

- noms des amiraux NAVY-2B non affiches correctement ;
- ajout d'Arthur Phillip comme amiral portugais simple ;
- renforcement minimal de `DEI` / `Koloniale_Marine` de 1 a 3 fregates.

Aucune flotte NAVY-2B principale n'a ete reequilibree a nouveau. Aucune loi, technologie, pop, frontiere, batiment ou PM n'a ete modifie.

## 2. Probleme observe en jeu

Les flottes NAVY-2B apparaissaient correctement, mais les amiraux historiques ajoutes en NAVY-2B etaient remplaces par des noms generes :

| Pays | Nom attendu | Nom observe |
|---|---|---|
| `SWE` | Henrik af Trolle | Carl Fredrik Samuelsson |
| `DENNOR` | Frederik Christian Kaas | Hans Trampe |
| `NET` | Jan Hendrik van Kinsbergen | Marius van Diemen |

Deux autres ajustements etaient demandes :

- `POR` devait recevoir Arthur Phillip comme amiral simple de `Marinha_Real_Portuguesa`.
- `DEI` devait passer de 1 a 3 fregates, sans vaisseau de ligne et sans amiral.

## 3. Cause probable du probleme de noms

Les blocs `create_character` NAVY-2B utilisaient deja le meme modele que les amiraux russes NAVY-1A :

- `is_admiral = yes`
- `first_name = navy_*`
- `last_name = navy_*`
- `historical = yes`
- `save_scope_as`
- `transfer_to_formation`

La difference la plus probable etait l'encodage de localisation en francais :

- `localization/french/phase_navy_1a_russian_admirals_l_french.yml`, qui fonctionne en jeu, commence par un BOM UTF-8.
- `localization/french/phase_navy_2b_admirals_l_french.yml`, cree en NAVY-2B, ne l'avait pas.

Comme le jeu est lance en francais, le fichier francais NAVY-2B a probablement ete ignore ou mal charge, ce qui a empeche les cles `navy_*` de stabiliser les noms.

Correction appliquee :

- `phase_navy_2b_admirals_l_english.yml` reecrit en UTF-8 BOM par securite.
- `phase_navy_2b_admirals_l_french.yml` reecrit en UTF-8 BOM, comme le fichier russe fonctionnel.
- Ajout des cles d'Arthur Phillip dans les deux langues.

## 4. Modele fonctionnel utilise

Modele repris des amiraux russes NAVY-1A dans `common/history/military_formations/00_military_formations_europe.txt` :

```txt
create_character = {
    is_admiral = yes
    first_name = navy_...
    last_name = navy_...
    historical = yes
    ...
    save_scope_as = ...
}
scope:... = {
    transfer_to_formation = scope:...
}
```

Aucune nouvelle syntaxe n'a ete inventee.

## 5. Amiraux corriges

Les trois amiraux NAVY-2B restent dans leurs blocs existants. La correction porte sur le chargement fiable des localisations.

| Pays | Amiral | Cles utilisees |
|---|---|---|
| `NET` | Jan Hendrik van Kinsbergen | `navy_jan_hendrik`, `navy_van_kinsbergen` |
| `DENNOR` | Frederik Christian Kaas | `navy_frederik_christian`, `navy_kaas` |
| `SWE` | Henrik af Trolle | `navy_henrik_af`, `navy_trolle` |

Les valeurs de localisation sont presentes en anglais et en francais.

## 6. Amiral portugais ajoute

Arthur Phillip a ete ajoute comme amiral simple pour `POR`.

Details :

- fichier : `common/history/military_formations/00_military_formations_europe.txt`
- flotte : `Marinha_Real_Portuguesa`
- scope flotte : `por_marinha_real_portuguesa`
- amiral : Arthur Phillip
- scope amiral : `por_phillip_adm`
- `is_admiral = yes`
- `historical = yes`
- `commander_rank = default`
- culture : `cu:british`
- religion : `rel:protestant`

Justification : Arthur Phillip est le candidat demande. Il est ajoute de facon minimale, sans biographie, sans lien Wikipedia et sans fiche detaillee.

## 7. DEI / VOC

Correction appliquee dans `common/history/military_formations/06_military_formations_asia.txt` :

| Pays | Flotte | Avant | Apres |
|---|---|---:|---:|
| `DEI` | `Koloniale_Marine` | 1 fregate | 3 fregates |

Confirmation :

- 0 vaisseau de ligne ;
- 3 fregates ;
- `hq_region = sr:region_indonesia` conserve ;
- nom `Koloniale_Marine` conserve ;
- aucun amiral DEI ajoute ;
- aucune loi navale DEI ajoutee.

## 8. Fichiers modifies

Fichiers modifies par cette phase :

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/06_military_formations_asia.txt`
- `localization/english/phase_navy_2b_admirals_l_english.yml`
- `localization/french/phase_navy_2b_admirals_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_2B_BIS_ADMIRAL_NAMES_PORTUGAL_DEI_FIX.md`

Note : le depot contient encore des changements non committes de NAVY-2B dans les fichiers pays et le rapport NAVY-2B. Ils n'ont pas ete modifies par cette phase bis.

## 9. Confirmation de perimetre

Non modifies dans cette phase :

- grandes puissances : `GBR`, `FRA`, `SPA`, `RUS` ;
- Mediterranee et puissances regionales : `TUR`, `VEN`, `SIC`, `GEN`, `SAR`, `PAP`, `TUS`, `MOR`, `MAS`, `TUN`, `TRI`, `OMA` ;
- frontieres ;
- pops ;
- technologies ;
- batiments ;
- PM ;
- lois navales ajoutees en NAVY-2B ;
- tailles de flotte `NET`, `POR`, `DENNOR`, `NOR`, `SWE`.

## 10. Tests a refaire en jeu

1. Lancer une nouvelle partie 1776.
2. Verifier `NET` :
   - amiral affiche : Jan Hendrik van Kinsbergen.
3. Verifier `DENNOR` :
   - amiral affiche : Frederik Christian Kaas.
4. Verifier `SWE` :
   - amiral affiche : Henrik af Trolle.
5. Verifier `POR` :
   - amiral affiche : Arthur Phillip.
6. Verifier `DEI` :
   - `Koloniale_Marine` ;
   - 3 fregates ;
   - 0 navire capital ;
   - pas d'amiral ajoute.
7. Verifier que les tailles `NET`, `POR`, `DENNOR`, `NOR`, `SWE` n'ont pas change.
8. Verifier que `GBR`, `FRA`, `SPA`, `RUS` n'ont pas change.
9. Laisser tourner un mois.
10. Surveiller `error.log` pour :
    - `invalid character` ;
    - `missing localization` ;
    - `invalid localization` ;
    - `create_military_formation` ;
    - `invalid hq_region` ;
    - `PostValidate`.

## 11. Risques restants

- Si les noms restent generes, le probleme ne vient pas seulement du BOM : il faudra alors verifier si Victoria 3 exige une autre methode pour verrouiller les noms historiques dans ces blocs precis.
- Arthur Phillip est ajoute comme personnage simple ; son exactitude historique fine n'a pas ete approfondie dans cette phase.
- DEI reste volontairement modeste : 3 fregates representent une presence coloniale/VOC, pas une battlefleet.
