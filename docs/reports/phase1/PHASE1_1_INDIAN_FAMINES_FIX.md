# Phase 1.1 - Correction Indian Famines

Branche : `phase1-critical-log-cleanup`

## Erreur corrigee

`error.log` et le diagnostic Phase 1 signalaient une pollution massive :

```text
Invalid right side during comparison 'sr'
Script location: common/journal_entries/04_indian_famines.txt
```

Les lignes les plus visibles dans les logs etaient dans le bloc `possible`, notamment `31`, `36`, `41`, `46` et `52-56`.

## Lignes modifiees

Fichier modifie :

- `common/journal_entries/04_indian_famines.txt`

Modification appliquee :

- remplacement de `region = sr:region_*` par `region = region_*`

Lignes concernees apres correction :

- `14-18`
- `26`
- `31`
- `36`
- `41`
- `46`
- `52-56`
- `79-83`
- `94`
- `101-105`
- `117`
- `124-128`
- `140`
- `147-151`
- `163`
- `170-174`
- `186`
- `193-197`
- `215`
- `226`
- `237`
- `248`
- `259`
- `271-275`

## Pourquoi la correction est minimale

La logique gameplay n'a pas ete reorganisee : les memes regions indiennes sont conservees, les memes seuils de famine sont conserves, les memes variables de journal entry sont conservees.

La correction retire seulement le prefixe type `sr:` dans ce fichier, afin que Victoria 3 1.13 ne lise plus `sr` comme cote droit invalide d'une comparaison `region = ...`.

Aucun autre fichier n'a ete modifie : pas de shipyards, pas de formations militaires, pas de localisation.

## Tests a faire ensuite

1. Lancer Victoria 3 1.13 avec uniquement le mod active.
2. Entrer en partie, idealement avec `BIC`, `DUR`, `MARATH`, `HYD` ou une grande puissance impliquee en Inde.
3. Laisser tourner au moins un mois.
4. Verifier `logs/error.log`.
5. Confirmer que l'erreur suivante a disparu :

```text
Invalid right side during comparison 'sr'
common/journal_entries/04_indian_famines.txt
```

Si l'erreur persiste ailleurs, traiter les autres fichiers separement dans une phase dediee, sans les melanger avec cette correction.
