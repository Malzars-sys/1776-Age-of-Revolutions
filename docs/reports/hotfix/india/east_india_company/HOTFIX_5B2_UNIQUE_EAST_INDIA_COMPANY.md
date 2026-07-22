# HOTFIX-5B2 - Compagnie des Indes orientales unique

## 1. Resume

Le systeme actif de Compagnie des Indes utilise maintenant uniquement les deux strategic regions vanilla The Great Wave 1.13 :

- `region_north_india` ;
- `region_south_india`.

La journal entry ne propose plus les dix chemins regionaux Bengal, Bombay, Madras, Central India et Punjab. Elle conserve trois chemins indiens actifs :

1. creation d'une compagnie dynamique unique ;
2. expansion de cette compagnie dynamique ;
3. expansion de la BIC historique.

Les definitions regionales legacy restent intactes dans le fichier global de scripted buttons pour limiter le risque de compatibilite avec les sauvegardes.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `a8678d6 Audit unique East India Company workflow` |
| Commit HOTFIX-5B1 | Present |
| Stash MARATH | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |

Le stash MARATH etait present au debut de la phase et n'a fait l'objet d'aucune operation.

## 3. Modifications de la journal entry

Fichier : `common/journal_entries/06_new_imperialism.txt`.

Dans `je_new_imperialism.is_shown_when_inactive`, les cinq marqueurs indiens invalides ont ete remplaces par les deux marqueurs valides nord et sud. Les marqueurs hors Inde sont inchanges.

Les cinq callers regionaux de creation et les cinq callers regionaux d'expansion ont ete detaches. Les boutons hors Inde, `possible`, `weight`, `should_be_pinned_by_default` et le nom de la JE sont inchanges.

Les trois callers indiens conserves sont :

- `je_colonial_administration_button_expand_for_bic` ;
- `je_colonial_administration_button_east_india_company` ;
- `je_colonial_administration_button_expand_east_india`.

Aucun fichier `06_new_imperialism_mod.txt` n'a ete cree ; il n'existe donc pas de seconde definition locale de `je_new_imperialism`.

## 4. Bouton de creation unique

Bloc modifie : `je_colonial_administration_button_east_india_company` dans `common/scripted_buttons/00_new_colonial_admins.txt`.

Les filtres regionaux ont ete adaptes dans :

- `visible` ;
- `possible` ;
- la recherche d'une capitale prioritaire avec le decret `decree_greener_grass_campaign` ;
- la selection de cette capitale ;
- la selection de capitale de secours ;
- le marquage des states par `state_to_cede`.

Chaque OR actif contient maintenant uniquement `region_north_india` et `region_south_india`.

La creation dynamique, le type colonial, le tier, la capitale, la cession des states, le pacte de sujet et l'appel d'event sont inchanges.

## 5. Expansion de la compagnie dynamique

Bloc modifie : `je_colonial_administration_button_expand_east_india`.

Les filtres regionaux de possibilite, de selection et de transfert des states utilisent maintenant l'union nord/sud. La visibilite continue de retrouver la compagnie existante par `india_mod_subject_var` et ne contenait aucun filtre regional a remplacer.

Les conditions de paix, de diplomatic play, de colonisation, le cooldown, les scopes de transfert et le mecanisme d'annexion d'un eventuel second sujet portant la meme variable sont inchanges.

## 6. Expansion de la BIC historique

Bloc modifie : `je_colonial_administration_button_expand_for_bic`.

Les changements sont limites a :

- la possibilite, maintenant fondee sur `region_north_india` ou `region_south_india` ;
- deux transferts de states, un pour le nord et un pour le sud, en remplacement des cinq transferts regionaux invalides ;
- la reutilisation des cles generiques existantes `je_colonial_administration_button_east_india` et `je_colonial_administration_button_east_india_desc`.

La recherche de la BIC historique par `new_imperialism_mod_var`, le cooldown, les conditions diplomatiques et le scope destinataire sont inchanges. Le transfert Indochine supplementaire present dans le hotfix upstream n'a pas ete importe car il sort du perimetre indien ferme de cette phase.

## 7. Regions avant et apres

| Avant | Statut 1.13 | Apres dans le systeme actif |
|---|---|---|
| `region_bengal` | Invalide/non definie | `region_north_india` + `region_south_india` selon le perimetre unique |
| `region_bombay` | Invalide/non definie | Union nord/sud |
| `region_central_india` | Invalide/non definie | Union nord/sud |
| `region_madras` | Invalide/non definie | Union nord/sud |
| `region_punjab` | Invalide/non definie | Union nord/sud |

La verification ciblee confirme zero reference aux cinq IDs invalides dans la JE et dans chacun des trois blocs actifs. Des occurrences restent volontairement dans les definitions legacy non appelees.

## 8. Callers regionaux detaches

Callers de creation retires de la JE :

- `je_colonial_administration_button_bengal` ;
- `je_colonial_administration_button_bombay` ;
- `je_colonial_administration_button_madras` ;
- `je_colonial_administration_button_central_india` ;
- `je_colonial_administration_button_punjab`.

Callers d'expansion retires :

- `je_colonial_administration_button_expand_bengal` ;
- `je_colonial_administration_button_expand_bombay` ;
- `je_colonial_administration_button_expand_madras` ;
- `je_colonial_administration_button_expand_central_india` ;
- `je_colonial_administration_button_expand_punjab`.

Aucun de ces dix IDs n'est encore appele par `06_new_imperialism.txt`.

## 9. Definitions legacy conservees

Les dix definitions correspondant aux callers detaches restent presentes dans `00_new_colonial_admins.txt`. Une comparaison bloc par bloc avec `HEAD` confirme qu'elles sont strictement identiques avant et apres HOTFIX-5B2.

Leurs anciennes regions, variables, effets, visibilites et localisations n'ont pas ete modifies. Elles pourront etre supprimees dans une phase ulterieure seulement apres une decision explicite concernant les anciennes sauvegardes.

## 10. Variables et gardes anti-doublon preservees

Les comptages avant/apres dans les trois blocs actifs confirment la conservation de :

- `india_mod_subject_var` ;
- `new_imperialism_mod_var` ;
- `newly_formed_colonial_nation_var` ;
- `state_to_cede` ;
- `new_imperialism_events.3` ;
- `chartered_company` ;
- chaque cooldown de 90 jours ;
- la duree de trois mois de la variable temporaire.

Le bouton de creation reste masque si un sujet portant la variable dynamique ou historique existe deja. L'expansion dynamique cible toujours `india_mod_subject_var`, tandis que l'expansion BIC cible toujours `new_imperialism_mod_var`.

## 11. Lois preservees

Aucune ligne de loi n'entre dans le diff. En particulier :

- `law_frontier_colonization` de BIC reste intacte ;
- `law_colonial_exploitation` de la compagnie dynamique reste intacte ;
- aucune ligne `activate_law` n'a ete modifiee ;
- `law_mercantilism_navigation_acts` n'a pas ete ajoutee ou modifiee.

## 12. Localisations reutilisees

Aucun fichier de localisation n'a ete cree ou modifie.

Le bouton d'expansion BIC reutilise les cles EN/FR deja presentes :

- `je_colonial_administration_button_east_india` ;
- `je_colonial_administration_button_east_india_desc`.

Cela retire le libelle trompeur « Central India / Inde centrale » sans introduire de nouvelle cle. Les localisations regionales legacy sont conservees.

## 13. Risques restants

- Les anciennes strategic regions restent dans les definitions legacy. Elles ne sont plus appelees par la JE active, mais peuvent encore etre referencees par une ancienne sauvegarde, une console ou un autre mod.
- L'union nord/sud est plus large que chaque ancienne sous-region. Elle correspond au modele d'une compagnie unique, mais l'etendue exacte des states cedes doit etre verifiee en jeu.
- Une puissance europeenne possedant des states dans les deux regions peut ceder l'ensemble de ses possessions indiennes eligibles en une seule creation ou expansion ; c'est le comportement recherche, mais son equilibre reste a tester.
- La compagnie dynamique et BIC conservent des lois coloniales differentes. Cette question reste une decision de design separee.
- Les erreurs concernant d'autres anciennes strategic regions dans des fichiers hors de ce perimetre ne sont pas traitees ici.

## 14. Tests en jeu recommandes

1. Lancer GBR avec BIC comme sujet et confirmer que le bouton de creation d'une seconde EIC n'apparait pas.
2. Donner a GBR un state eligible dans `region_north_india`, utiliser l'expansion BIC et verifier le transfert.
3. Refaire le test dans `region_south_india`.
4. Lancer une puissance europeenne sans BIC, posseder au moins deux states indiens eligibles et creer une compagnie dynamique unique.
5. Verifier le pacte `chartered_company`, l'event `new_imperialism_events.3`, les states cedes et la variable de la compagnie.
6. Acquerir ensuite un state au nord puis au sud et verifier que le meme sujet est etendu.
7. Confirmer l'absence des dix boutons regionaux dans la JE.
8. Tester les libelles du bouton BIC en anglais et en francais.
9. Passer au moins trois mois et surveiller `error.log` pour les cinq anciennes regions, les erreurs de scope, `create_dynamic_country` et `new_imperialism_events.3`.

## 15. Fichiers modifies et crees

Fichiers gameplay modifies :

- `common/journal_entries/06_new_imperialism.txt` ;
- `common/scripted_buttons/00_new_colonial_admins.txt`.

Fichier cree :

- `docs/reports/hotfix/HOTFIX_5B2_UNIQUE_EAST_INDIA_COMPANY.md`.

## 16. Confirmation du perimetre gameplay

Aucun autre fichier gameplay n'a ete modifie. Aucun event, fichier de localisation, historique BIC, building, formation militaire, on_action ou fichier Battle for India n'a ete touche. Aucun fichier entier n'a ete remplace et aucun merge automatique n'a ete effectue.

## 17. Confirmation stash MARATH

Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est reste present et intact. Il n'a ete ni applique, ni restaure, ni supprime, ni modifie.
