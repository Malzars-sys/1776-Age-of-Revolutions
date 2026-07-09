# Phase NAVY-1A-ter - Admiral Name Display Fix

## 1. Resume du probleme

Apres NAVY-1A-bis, les blocs d'amiraux GB/FRA/SPA contenaient bien des noms historiques comme `Keppel`, `Howe`, `Hood`, `dOrvilliers` ou `de_Cordova_y_Cordova`.

En test de nouvelle partie, le jeu affichait encore des noms generes :

- Michel Stevenot
- Jean Baptiste Bougueret
- Richard Peppercorn
- Richard Craufurd
- Luis Galatas

Le probleme ne venait donc pas seulement des scopes ou des affectations, mais aussi de la resolution des noms par le jeu.

## 2. Pourquoi NAVY-1A-bis ne suffisait pas

NAVY-1A-bis utilisait des valeurs directes comme :

- `first_name = Augustus`
- `last_name = Keppel`
- `last_name = dOrvilliers`

La vanilla montre que les noms non generes sont soit :

- des templates de personnages ;
- des noms entre guillemets dans `common/character_templates/*` ;
- des cles de noms localisees dans les fichiers `localization/*/names_l_*.yml`.

Dans une partie lancee en francais, les cles ajoutees par NAVY-1A-bis n'avaient pas de localisation explicite dans le mod. Le jeu pouvait donc retomber sur le pool culturel et generer un nom aleatoire malgre la presence d'un token dans `first_name` ou `last_name`.

## 3. Syntaxe vanilla trouvee

Exemples vanilla The Great Wave observes dans :

- `C:\Games\Victoria 3 The Great Wave\game\common\character_templates\country_arg.txt`
- `C:\Games\Victoria 3 The Great Wave\game\localization\*\names_l_*.yml`

Exemple de template vanilla :

```txt
ARG_William_Brown = {
	is_admiral = yes
	first_name = "William"
	last_name = "Brown"
	historical = yes
	...
}
```

La vanilla utilise aussi des tokens de noms, mais ceux-ci sont presents dans les fichiers de localisation de noms, par exemple `William: "William"` ou `Brown: "Brown"`.

## 4. Correction appliquee aux noms

Les amiraux GB/FRA/SPA gardent leurs blocs `create_character`, leurs scopes et leurs transferts vers les flottes. Seules les valeurs `first_name` et `last_name` ont ete remplacees par des cles explicites `navy_*`.

Exemples :

```txt
first_name = navy_augustus
last_name = navy_keppel
```

```txt
first_name = navy_louis_guillouet
last_name = navy_dorvilliers
```

Ces cles sont maintenant localisees en anglais et en francais.

## 5. Localisation ajoutee

Fichiers ajoutes :

- `localization/english/phase_navy_1a_admirals_l_english.yml`
- `localization/french/phase_navy_1a_admirals_l_french.yml`

Le fichier francais a ete converti en UTF-8 avec BOM.

Les noms propres sont localises de maniere minimale. Les valeurs anglaises et francaises sont volontairement presque identiques, sauf accents utiles :

- Pierre Andre / Pierre Andre en anglais, Pierre Andre avec accent en francais.
- de Cordova y Cordova en anglais, de Cordova avec accents en francais.

## 6. Flotte -> amiral

| Pays | Flotte | Amiraux vises |
|---|---|---|
| GBR | Portsmouth Station | Augustus Keppel, Peter Parker, Richard Kempenfelt |
| GBR | Plymouth Station | Samuel Barrington, Francis Geary |
| GBR | Mediterranean Station | Samuel Hood |
| GBR | North America and West Indies Station | Richard Howe |
| GBR | East Indies and China Station | Edward Hughes |
| FRA | Escadre du Nord | Louis Guillouet d'Orvilliers, Toussaint-Guillaume Picquet de la Motte, Luc Urbain de Guichen |
| FRA | Escadre de la Mediterranee | Pierre Andre de Suffren, Jean-Baptiste d'Albert de Rions, Charles Hector d'Estaing |
| SPA | Real Armada Espanola | Luis de Cordova y Cordova, Antonio de Ulloa |

## 7. Confirmation des limites

Cette phase n'a pas modifie :

- les `count` de navires ;
- les `hq_region` ;
- les `ship_type` ;
- les batiments ;
- les lois ;
- les technologies ;
- le Japon ;
- l'Australasie ;
- le Moyen-Orient ;
- les pays hors GB/FRA/SPA.

## 8. Verifications effectuees

Commande demandee pour les noms generes :

```powershell
Select-String -Path "common/history/military_formations/00_military_formations_europe.txt" -Pattern "Michel","Stevenot","Bougueret","Peppercorn","Craufurd","Galatas"
```

Resultat : aucun retour.

Commande demandee pour les noms historiques :

```powershell
Select-String -Path "common/history/military_formations/00_military_formations_europe.txt" -Pattern "Keppel","Parker","Kempenfelt","Barrington","Geary","Hood","Howe","Hughes","Orvilliers","Picquet","Guichen","Suffren","Rions","Estaing","Cordova","Ulloa"
```

Resultat : les anciennes valeurs directes ont ete remplacees par des cles `navy_*`, et les noms apparaissent dans les fichiers de localisation ajoutes.

## 9. Tests a refaire en jeu

1. Lancer une nouvelle partie propre en 1776.
2. Verifier les flottes GB/FRA/SPA.
3. Confirmer que les amiraux affichent les noms historiques localises.
4. Confirmer que Michel Stevenot, Jean Baptiste Bougueret, Richard Peppercorn, Richard Craufurd et Luis Galatas ne commandent plus ces flottes.
5. Verifier que les navires restent inchanges par rapport a NAVY-1A.
6. Laisser tourner un mois.
7. Surveiller `error.log` et `debug.log` pour `create_character`, `admiral`, `localization`, `fleet`, `PostValidate`.
