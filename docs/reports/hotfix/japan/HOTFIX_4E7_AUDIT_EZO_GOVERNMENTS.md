# HOTFIX-4E7-AUDIT - Gouvernements EZO

## 1. Resume executif

Les identifiants `gov_ezo_republic` et `gov_ezo_republic_colonial` utilises dans `common/journal_entries/07_hokkaido.txt` ne sont pas des government types valides dans l'installation examinee.

La recherche exhaustive ne trouve aucune definition ni localisation correspondante dans le fork, le hotfix upstream ou la vanilla The Great Wave. Le systeme Victoria 3 ne genere pas automatiquement un government type a partir d'un nom commencant par `gov_` : chaque type est un objet statique declare dans `common/government_types`, avec ses conditions `possible` et ses localisations.

La vanilla 1.13 fournit deja `gov_domain_frontier`, un government type explicitement reserve a EZO lorsque le pays possede `law_presidential_republic`, est vassal et a un suzerain de culture principale japonaise. EZO commence precisement avec `law_presidential_republic`, `law_oligarchy` et un pacte de vassalite envers JAP. Son government type initial probable est donc `gov_domain_frontier`. Si EZO devient independant sans changer ses lois, il doit retomber sur un type generique tel que `gov_presidential_oligarchy`.

Classification principale : **C. IDENTIFIANTS ERRONES OU OBSOLETES**.

La branche EZO de `is_shown_when_inactive` est probablement toujours fausse, ou produit une validation de reference selon le niveau de controle du moteur. Elle empeche EZO d'acceder normalement a `je_taming_the_north`, tandis que la branche JAP reste fonctionnelle.

La correction future recommandee est de remplacer uniquement les deux tests de government type par un test de la loi `law_presidential_republic` dans le scope EZO. Le reste de la JE distingue deja EZO vassale et EZO independante par le statut de sujet ; recreer deux government types serait redondant et plus risque.

## 2. Etat Git

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `72d03a3 Fix Ryukyu English localization indentation` |
| HOTFIX-4E5 | Commit `f5eac82 Validate Japan hotfix integration` present |
| Stash MARATH | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. Occurrences exactes

Les deux occurrences runtime se trouvent dans la meme condition de `je_taming_the_north` :

```txt
is_shown_when_inactive = {
    has_dlc_feature = ep2_content
    OR = {
        c:JAP ?= this
        AND = {
            c:EZO ?= this
            OR = {
                has_government_type = gov_ezo_republic
                has_government_type = gov_ezo_republic_colonial
            }
        }
    }
    # ownership de Hokkaido
}
```

| Identifiant | Bloc | Syntaxe | Scope | Role attendu | Risque si invalide |
|---|---|---|---|---|---|
| `gov_ezo_republic` | `je_taming_the_north.is_shown_when_inactive` | `has_government_type = gov_ezo_republic` | Pays courant, deja limite a `c:EZO ?= this` | Autoriser une EZO republicaine vraisemblablement independante | La branche EZO ne devient jamais visible |
| `gov_ezo_republic_colonial` | meme bloc | `has_government_type = gov_ezo_republic_colonial` | Meme scope EZO | Autoriser une EZO republicaine sous statut colonial ou vassal | Meme consequence |

Le test ne controle ni la completion ni l'echec de la JE. Il controle son affichage inactif et donc son acces initial pour EZO.

## 4. Recherche exhaustive

| Racine recherchee | Utilisations | Definitions | Localisations | Commentaires / rapports |
|---|---:|---:|---:|---:|
| Fork runtime (`common`, `events`, `localization`) | 2, dans `07_hokkaido.txt` | 0 | 0 | 0 |
| Fork documentation | 0 runtime | 0 | 0 | Plusieurs mentions dans HOTFIX-4B et HOTFIX-4E5 |
| Hotfix upstream | 2, dans sa copie de `07_hokkaido.txt` | 0 | 0 | 0 |
| Vanilla 1.13 EN/FR | 0 | 0 | 0 | 0 |

La copie hotfix est donc incomplete par rapport aux references qu'elle ajoute. La vanilla actuelle possede son propre `07_hokkaido.txt`, mais celui-ci limite `is_shown_when_inactive` a JAP et ne contient pas la branche EZO du hotfix.

La recherche dans le dernier `error.log` disponible ne retourne aucun de ces identifiants. Cette absence ne prouve pas leur validite : la JE ou la branche EZO peut ne pas avoir ete evaluee pendant ce lancement.

## 5. Fonctionnement vanilla des government types

Un government type est declare sous la forme :

```txt
gov_nom = {
    transfer_of_power = ...
    male_ruler = "..."
    female_ruler = "..."
    possible = {
        # lois, pays, statut et autres conditions
    }
}
```

Le moteur choisit parmi les types dont le bloc `possible` correspond aux lois et au contexte du pays. Le trigger `has_government_type = gov_nom` compare ensuite le type effectivement selectionne a un objet declare. Il ne transforme pas dynamiquement les lois en un nouvel identifiant arbitraire.

| Mecanisme | Exemple vanilla | Definition necessaire ? | Applicabilite a EZO |
|---|---|---:|---|
| Government type specialise | `gov_domain_frontier` dans `02_presidential_republics.txt` | Oui | Correspond exactement a EZO vassale de JAP |
| Government type republicain generique | `gov_presidential_oligarchy` | Oui | Candidat probable si EZO devient independante avec oligarchie |
| Test depuis une JE | `has_government_type = gov_dual_monarchy` dans les JE autrichiennes | Oui | Le type teste est toujours declare ailleurs |
| Localisation du nom | `gov_domain_frontier` et `gov_domain_frontier_desc` | Oui pour l'affichage | Disponible en anglais et francais vanilla |
| Generation dynamique d'un ID `gov_*` | Aucun exemple trouve | Non supporte par les fichiers examines | Ne peut pas rendre valides les deux IDs EZO inconnus |

### Government type vanilla specifique a EZO

`gov_domain_frontier` exige :

- `c:EZO ?= this` ;
- un suzerain ou super-suzerain de culture principale japonaise ;
- `law_presidential_republic` ;
- `subject_type_vassal`.

Il utilise le titre `RULER_TITLE_KARO` et est localise comme "Domain Frontier" / "Domaine frontalier". Il s'agit du candidat direct pour la situation initiale d'EZO.

## 6. Setup politique actuel d'EZO

Les fichiers pays fork, hotfix et vanilla sont fonctionnellement identiques.

| Element politique | Fork | Hotfix | Vanilla | Consequence pour la JE |
|---|---|---|---|---|
| Distribution du pouvoir | `law_oligarchy` | Identique | Identique | Rend probable `gov_presidential_oligarchy` hors vassalite |
| Principe de gouvernance | `law_presidential_republic` | Identique | Identique | EZO est bien une republique au sens des lois |
| Commerce | `law_isolationism` | Identique | Identique | Sans effet direct sur les deux IDs |
| Armee | `law_warrior_caste` | Identique | Identique | Sans effet direct |
| Statut | Vassal de JAP | Vassal de JAP | Vassal de JAP | Satisfait le contexte de `gov_domain_frontier` |
| Politique coloniale explicite | Aucune loi coloniale propre trouvee dans le fichier EZO | Identique | Identique | Ne justifie pas un type `gov_ezo_republic_colonial` distinct |

Le fork ne remplace pas le repertoire `common/government_types`. Les government types vanilla, dont `gov_domain_frontier`, restent donc disponibles en plus des fichiers locaux.

### Government type probable au depart

EZO satisfait les conditions visibles de `gov_domain_frontier` : pays EZO, republique presidentielle, vassal de JAP, suzerain japonais. Sous reserve de priorite interne entre types eligibles, c'est le type specialise attendu au depart.

Si EZO devient independante tout en gardant `law_presidential_republic` et `law_oligarchy`, `gov_domain_frontier` cesse d'etre possible. Un type republicain generique declare, vraisemblablement `gov_presidential_oligarchy`, devient alors le candidat naturel.

## 7. Intention du bloc Hokkaido

La branche hotfix ajoute un chemin complet pour jouer la modernisation de Hokkaido avec EZO :

- `is_shown_when_inactive` autorise JAP ou une EZO supposee republicaine ;
- `possible` possede des branches separees pour `region_state:JAP` et `region_state:EZO` ;
- `immediate` sauvegarde JAP si ROOT est JAP ou sujet de JAP ;
- le commentaire indique explicitement que `japan_scope` doit etre invalide si la Republique d'Ezo est independante ;
- `hokkaido_events.1` possede titres et descriptions distincts pour ROOT JAP et ROOT EZO ;
- plusieurs evenements ulterieurs possedent des branches EZO dediees.

La distinction voulue est donc :

1. EZO vassale de JAP, correspondant au domaine frontalier colonial ;
2. EZO republicaine independante.

Toutefois, apres l'entree dans la JE, cette distinction est deja realisee par `is_subject_of = c:JAP`, l'existence de `japan_scope` et les tests `c:EZO ?= ROOT`. Les noms de government type ne sont utilises qu'a la porte d'entree de la JE et ne sont pas necessaires au fonctionnement ulterieur.

## 8. Classification du probleme

### Classification principale : C. IDENTIFIANTS ERRONES OU OBSOLETES

Justification :

- aucune declaration n'existe dans les trois sources ;
- aucune localisation n'existe ;
- les government types ne sont pas generes dynamiquement ;
- la vanilla 1.13 a un nom specialise different, `gov_domain_frontier` ;
- le setup independant retombe sur des types republicains generiques declares ;
- la JE vanilla actuelle n'utilise pas les deux identifiants.

La classification B n'est pas retenue comme principale : rien ne montre l'existence d'un fichier hotfix manquant contenant deux designs complets de gouvernement, et le systeme vanilla couvre deja les deux situations avec un type specialise et des fallbacks generiques.

La classification D decrit bien la correction recommandee, mais pas la cause principale. La cause est l'usage de deux IDs inexistants ; remplacer la condition par une loi est la solution la plus robuste.

La classification E est une consequence : la sous-branche EZO de la condition d'affichage est actuellement inaccessible avec les government types reels.

## 9. Consequence probable en jeu

Pour JAP, aucun impact direct : la premiere branche `c:JAP ?= this` reste suffisante.

Pour EZO :

- au depart, son type probable est `gov_domain_frontier`, qui ne correspond a aucun des deux tests ;
- apres independance, un type generique comme `gov_presidential_oligarchy` ne correspond toujours pas ;
- `is_shown_when_inactive` reste faux pour EZO ;
- EZO ne peut donc probablement pas voir ni activer normalement `je_taming_the_north` ;
- les nombreuses branches EZO dans la JE et les evenements deviennent du contenu mort.

Selon le comportement de validation de la version du moteur, les IDs inconnus peuvent aussi produire un warning ou une erreur de post-validation lors du chargement. Aucun message correspondant n'a ete trouve dans le dernier log disponible, mais un test ciblant EZO est requis.

## 10. Solutions possibles

| Rang | Solution | Fichiers necessaires | Avantages | Risques | Tests necessaires |
|---:|---|---|---|---|---|
| 1 | Remplacer l'OR des deux government types par `has_law_or_variant = law_type:law_presidential_republic` dans le scope EZO | `common/journal_entries/07_hokkaido.txt` seulement, plus rapport | Minimal, couvre EZO vassale et independante, suit le setup reel, ne duplique aucun gouvernement | N'autorise pas une future EZO parlementaire sans adaptation | Visibilite JE pour EZO vassale puis independante, JAP inchangee, logs propres |
| 2 | Tester une liste de types existants : `gov_domain_frontier` plus les variantes presidentielles generiques pertinentes | `07_hokkaido.txt` seulement | Compare des objets valides et conserve une logique par government type | Fragile, liste longue et susceptible d'oublier une variante apres changement de lois | Tester chaque franchise et distribution du pouvoir |
| 3 | Creer `gov_ezo_republic` et `gov_ezo_republic_colonial` localement avec leurs localisations | Nouveau fichier dans `common/government_types`, localisations EN/FR, eventuellement JE | Preserve exactement les noms hotfix | Risque eleve de priorite avec `gov_domain_frontier`, duplication conceptuelle, titres et transferts de pouvoir a concevoir | Matrice complete sujet/independant, lois, succession, reformes et affichage |

## 11. Solution recommandee

La solution 1 est recommandee.

Condition future proposee, a confirmer dans une phase de correction dediee :

```txt
AND = {
    c:EZO ?= this
    has_law_or_variant = law_type:law_presidential_republic
}
```

Cette condition exprime directement l'intention observable : EZO doit etre republicaine. Le statut colonial ou independant est deja gere plus loin par `is_subject_of = c:JAP` et par la validite de `japan_scope`.

Il ne faut pas remplacer les deux IDs uniquement par `gov_domain_frontier`, car cela exclurait precisement le chemin d'EZO independante documente dans la JE.

## 12. Perimetre recommande pour une future correction

Fichiers autorises :

- `common/journal_entries/07_hokkaido.txt` ;
- un rapport dedie a la correction.

Fichiers a ne pas modifier pour la solution recommandee :

- `events/japan_events/ep2_hokkaido_events.txt` ;
- `common/government_types/*` ;
- historique EZO/JAP ;
- states, pops et buildings ;
- localisations.

## 13. Tests en jeu recommandes

1. Avant correction, lancer EZO et confirmer le government type affiche au depart.
2. Rechercher les deux IDs et `07_hokkaido.txt` dans `error.log` apres chargement d'EZO.
3. Apres future correction, confirmer que `je_taming_the_north` est visible pour EZO vassale avec `law_presidential_republic`.
4. Rendre EZO independante sans changer ses lois et confirmer que la JE reste visible.
5. Changer EZO vers une monarchie et confirmer que la JE ne devient plus nouvellement disponible par la branche republicaine.
6. Lancer JAP et verifier que son acces a la JE est strictement inchange.
7. Tester `hokkaido_events.1` avec ROOT EZO et les quatre options.
8. Verifier que `japan_scope` existe pour EZO vassale et reste volontairement invalide pour EZO independante.
9. Faire progresser et terminer la JE dans les deux statuts.
10. Surveiller `error.log` pour `gov_ezo_republic`, `gov_ezo_republic_colonial`, `gov_domain_frontier`, `je_taming_the_north`, `hokkaido_events`, `invalid government type` et `invalid scope`.

## 14. Fichier cree

- `docs/reports/hotfix/HOTFIX_4E7_AUDIT_EZO_GOVERNMENTS.md`

## 15. Confirmation de perimetre

- Aucun fichier gameplay n'a ete modifie.
- Aucune localisation n'a ete modifiee.
- Aucun fichier hotfix ou vanilla n'a ete copie.
- Aucune reference n'a ete corrigee automatiquement.
- Aucun commit n'a ete cree.
- Le stash MARATH n'a pas ete applique, restaure ou modifie.
