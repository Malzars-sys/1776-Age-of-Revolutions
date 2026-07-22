# HOTFIX-5A - Strategic region BIC pour Ryotwari

## 1. Resume

Le ciblage regional du modifier Ryotwari de BIC utilise maintenant la strategic region vanilla valide `region_south_india`. Les deux anciennes references `region_bombay` et `region_madras` ont ete retirees uniquement de ce bloc.

## 2. Probleme initial

Le fork ciblait deux IDs de strategic regions absents de Victoria 3 The Great Wave 1.13 :

- `region_bombay` ;
- `region_madras`.

Le mod ne fournit aucun dossier `common/strategic_regions` et ne definit donc pas localement ces IDs. Leur utilisation pouvait empecher le bloc Ryotwari de selectionner correctement les states de l'Inde du Sud ou produire une erreur de validation.

## 3. Bloc avant correction

```txt
every_scope_state = {
    limit = {
        OR = {
            region = sr:region_bombay
            region = sr:region_madras
            state_region = s:STATE_ASSAM
        }
    }
    add_modifier = {
        name = modifier_ryotwari_system
    }
}
```

## 4. Bloc apres correction

```txt
every_scope_state = {
    limit = {
        OR = {
            region = sr:region_south_india
            state_region = s:STATE_ASSAM
        }
    }
    add_modifier = {
        name = modifier_ryotwari_system
    }
}
```

## 5. Definition vanilla

`region_south_india` est definie dans la vanilla locale The Great Wave :

```txt
C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt
```

Cette region contient notamment Bombay, Hyderabad, Kurnool, Madras, Mysore, Circars, Travancore et Ceylon. Elle correspond au regroupement regional utilise par le hotfix pour le systeme Ryotwari.

## 6. Anciennes regions

La recherche des declarations de strategic regions confirme :

- aucune definition vanilla de `region_bombay` ;
- aucune definition vanilla de `region_madras` ;
- aucune definition locale de ces deux IDs dans le fork ;
- aucune definition locale concurrente dans le hotfix.

Les noms peuvent encore apparaitre ailleurs dans le contenu du mod, mais ils ne sont plus utilises par le fichier pays BIC apres cette correction.

## 7. Loi BIC preservee

La ligne locale suivante est conservee strictement :

```txt
activate_law = law_type:law_frontier_colonization
```

Elle n'a pas ete remplacee par `law_colonial_exploitation`.

## 8. Autres lois et setup preserves

Aucune loi autre que le controle de presence de `law_frontier_colonization` n'a ete modifiee. `law_mercantilism_navigation_acts` n'a pas ete ajoutee.

Les technologies, niveaux technologiques, modifiers, variables, personnages, capitale, cultures, religion, institutions, relations diplomatiques, claims et sujets de BIC sont inchanges.

## 9. Fichiers modifies

- Modifie : `common/history/countries/bic - british east india company.txt`.
- Cree : `docs/reports/hotfix/HOTFIX_5A_BIC_STRATEGIC_REGIONS.md`.

## 10. Risques restants

- Les cinq anciennes strategic regions indiennes restent utilisees dans d'autres fichiers du mod. Elles doivent etre traitees dans des phases separees.
- La vanilla applique Ryotwari avec deux anciens geographic regions plus Assam, tandis que le hotfix choisit la strategic region complete `region_south_india`. Ce choix est techniquement valide mais plus large ; son effet exact doit etre controle en jeu.
- Le setup technologique, militaire et historique BIC de 1776 reste volontairement hors scope.

## 11. Tests en jeu recommandes

1. Lancer BIC au 1er janvier 1776 et passer le premier jour.
2. Verifier les states BIC situes en `region_south_india` et confirmer l'application attendue de `modifier_ryotwari_system`.
3. Verifier Assam separement, car son ciblage explicite est conserve.
4. Confirmer que BIC commence toujours avec `law_frontier_colonization`.
5. Surveiller `error.log` pour `bic - british east india company.txt`, `region_bombay`, `region_madras`, `region_south_india`, `modifier_ryotwari_system` et `PostValidate`.

## 12. Batiments et formations

Aucun batiment, port, shipyard ou military formation n'a ete modifie. Les fichiers `common/history/buildings/10_india.txt` et `common/history/military_formations/05_military_formations_india.txt` sont inchanges.

## 13. Perimetres preserves

NAVY, ADMIN et MARATH n'ont pas ete touches. Aucun event, fichier de localisation, scripted button ou journal entry n'a ete modifie.

## 14. Stash MARATH

Le stash suivant reste present et intact :

```txt
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
```

Il n'a ete ni applique, ni supprime, ni modifie.

## 15. Confirmation finale

La correction gameplay se limite au remplacement de deux references regionales par une reference vanilla valide dans le bloc Ryotwari de BIC. Aucun commit automatique n'a ete cree.
