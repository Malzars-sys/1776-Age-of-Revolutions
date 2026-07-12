# HOTFIX-5B1-AUDIT - Compagnie des Indes orientales unique

## 1. Resume executif

Cet audit compare le fork, le hotfix upstream et la vanilla The Great Wave 1.13 sans modifier le gameplay.

Conclusions :

- Le fork charge `common/journal_entries/06_new_imperialism.txt`, tandis que le hotfix fournit `06_new_imperialism_mod.txt`. Copier ce second fichier dans le fork definirait une seconde fois `je_new_imperialism` : il faut modifier la JE locale existante par hunks.
- Les cinq strategic regions indiennes utilisees par le fork (`region_bengal`, `region_bombay`, `region_central_india`, `region_madras`, `region_punjab`) ne sont pas definies par la vanilla 1.13. Les cibles valides sont `region_north_india` et `region_south_india`.
- Le systeme actif peut etre reduit a trois boutons : creation d'une compagnie unique, expansion de la compagnie dynamique et expansion de la BIC historique.
- Les cinq boutons regionaux de creation fabriquent chacun un pays dynamique distinct, mais ils sont deja masques. Les cinq boutons regionaux d'expansion ne doivent plus etre appeles par la JE.
- Pour une correction conservatrice, les definitions regionales seront conservees temporairement mais rendues inaccessibles en retirant leurs callers de la JE. Cela limite le risque pour les anciennes sauvegardes.
- Les gardes `india_mod_subject_var` et `new_imperialism_mod_var` empechent un meme overlord de creer a la fois une compagnie dynamique et une nouvelle compagnie en presence de BIC. La variable temporaire `newly_formed_colonial_nation_var` securise la creation et permet a l'event de retrouver le nouveau sujet.
- Aucune nouvelle localisation n'est requise pour HOTFIX-5B2 : les deux paires generiques utiles existent deja en anglais et en francais. Le bouton BIC doit reutiliser la paire d'expansion generique au lieu de la paire trompeuse « Inde centrale ».
- La BIC historique doit conserver `law_frontier_colonization`. La compagnie dynamique recoit actuellement `law_colonial_exploitation` dans `new_imperialism_events.3`; cette difference exige une decision de design separee et ne doit pas etre modifiee implicitement.

## 2. Etat Git

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD | `8b233d2 Fix BIC strategic region targeting` |
| Commit audit HOTFIX-5 | `b9f043e Audit India and Battle for India hotfix` present |
| Commit HOTFIX-5A | `8b233d2 Fix BIC strategic region targeting` present |
| Stash MARATH | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

Le stash MARATH n'a ete ni applique, ni restaure, ni supprime, ni modifie.

## 3. Comparaison des fichiers

| Fichier | Fork | Hotfix | Vanilla 1.13 | Conclusion |
|---|---|---|---|---|
| `common/journal_entries/06_new_imperialism.txt` | Definit `je_new_imperialism` avec les cinq anciennes regions et les boutons regionaux | Absent sous ce nom | Absent | Fichier local a adapter |
| `common/journal_entries/06_new_imperialism_mod.txt` | Absent | Definit la meme JE avec `region_north_india` et `region_south_india` | Absent | Ne jamais copier comme second fichier |
| `common/scripted_buttons/00_new_colonial_admins.txt` | Contient les boutons globaux et regionaux | Version differente, partiellement alignee sur nord/sud | Absent | Trois blocs seulement a adapter par hunks |
| `events/new_imperialism_events_mod.txt` | Present | Identique au fork, SHA-256 `BCC6CF0C494FE579BAD0B913675180A2FD2D100F11A010198BD3124B6C99DDA2` | Absent | Aucun import ni changement |
| `localization/english/mod_journal_entries_l_english.yml` | Localisations regionales EN | Equivalent EN | Absent | Aucun changement requis |
| `localization/french/mod_journal_entries_l_french.yml` | Localisations regionales FR | Pas d'equivalent FR hotfix | Absent | Aucun changement requis |
| `localization/*/mod_v2content_l_*.yml` | Paires generiques EIC presentes en EN et FR | EN identique | Contenu mod | Reutiliser les cles existantes |
| `common/strategic_regions/west_south_asia_strategic_regions.txt` | Non surcharge par le mod | Non surcharge | Definit `region_south_india` ligne 29 et `region_north_india` ligne 43 | Reference normative |

La vanilla ne contient aucun equivalent direct de la JE, des boutons ou de l'event du mod. Elle sert ici uniquement de reference pour les strategic regions valides.

## 4. Inventaire des boutons Inde

| Bouton | Fork | Hotfix | Regions | Cree un pays ? | Transfere des states ? | Statut propose |
|---|---|---|---|---|---|---|
| `..._east_india_company` | Lignes 215-360, appele par la JE | Present, nord + sud | Fork : cinq invalides ; hotfix : nord + sud | Oui, un pays colonial | Oui, via `cede_state_trigger` | Adapter par hunk et conserver |
| `..._expand_east_india` | Lignes 1377-1483, appele | Present, nord + sud | Fork : cinq invalides ; hotfix : nord + sud | Non | Oui vers `india_mod_subject_var` | Adapter par hunk et conserver |
| `..._expand_for_bic` | Lignes 2201-2328, appele | Present, nord + sud | Fork : cinq invalides ; hotfix : nord + sud | Non | Oui vers `new_imperialism_mod_var` | Adapter par hunk et conserver |
| `..._central_india` | Defini, appele, `visible = always = no` | Remplace fonctionnellement par un bouton legacy nord masque | `region_central_india` | Oui | Oui a la creation | Retirer le caller, conserver temporairement la definition |
| `..._madras` | Defini, appele, masque | Absent comme bouton actif | `region_madras` | Oui | Oui a la creation | Retirer le caller, conserver temporairement |
| `..._bengal` | Defini, appele, masque | Absent comme bouton actif | `region_bengal` | Oui | Oui a la creation | Retirer le caller, conserver temporairement |
| `..._bombay` | Defini, appele, masque | Absent comme bouton actif | `region_bombay` | Oui | Oui a la creation | Retirer le caller, conserver temporairement |
| `..._punjab` | Defini, appele, masque | Absent comme bouton actif | `region_punjab` | Oui | Oui a la creation | Retirer le caller, conserver temporairement |
| `..._expand_central_india` | Defini et appele | Absent de la JE hotfix | `region_central_india` | Non | Oui vers une compagnie legacy | Retirer le caller, conserver temporairement |
| `..._expand_madras` | Defini et appele | Absent de la JE hotfix | `region_madras` | Non | Oui vers une compagnie legacy | Retirer le caller, conserver temporairement |
| `..._expand_bengal` | Defini et appele | Absent de la JE hotfix | `region_bengal` | Non | Oui vers une compagnie legacy | Retirer le caller, conserver temporairement |
| `..._expand_bombay` | Defini et appele | Absent de la JE hotfix | `region_bombay` | Non | Oui vers une compagnie legacy | Retirer le caller, conserver temporairement |
| `..._expand_punjab` | Defini et appele | Absent de la JE hotfix | `region_punjab` | Non | Oui vers une compagnie legacy | Retirer le caller, conserver temporairement |
| `..._north_india` | Absent du fork | Present dans le hotfix, masque | `region_north_india` | Oui | Oui a la creation | Ne pas importer |
| `..._expand_north_india` | Absent du fork | Present et appele dans la JE hotfix | `region_north_india` | Non | Oui vers `central_india_subject_var` | Ne pas importer |
| Boutons `south_india` | Absents | Localisations EN presentes, aucun bloc actif equivalent releve | `region_south_india` | Sans objet | Sans objet | Ne pas creer |

Le hotfix conserve donc lui-meme un reliquat `north_india`. Il n'est pas necessaire au modele d'une compagnie unique et ne doit pas etre importe.

## 5. Comparaison de la journal entry

| Bloc JE | Fork | Hotfix | Hunk minimal recommande | Risque |
|---|---|---|---|---|
| `is_shown_when_inactive` | Cinq marqueurs Inde invalides, plus les autres regions du fork | Deux marqueurs Inde valides et plusieurs renommages hors Inde | Remplacer uniquement les cinq lignes Inde par nord + sud ; laisser les regions hors Inde hors scope | Faible si le hunk reste cible |
| `possible` | Pays non colonial/reconnu, independant, heritage europeen, technologie `colonization` | Meme logique | Aucun changement | Aucun |
| Bouton BIC | `expand_for_bic` | Identique | Conserver | Aucun apres adaptation du bloc cible |
| Creation Inde | Bouton principal plus cinq boutons regionaux | Bouton principal plus un reliquat nord | Conserver seulement le bouton principal ; retirer les cinq callers regionaux ; ne pas ajouter le reliquat nord | Moyen pour anciennes sauvegardes, attenue par conservation des definitions |
| Expansion Inde | Bouton principal plus cinq expansions regionales | Bouton principal plus expansion nord legacy | Conserver seulement l'expansion principale ; retirer les cinq callers regionaux ; ne pas ajouter le reliquat nord | Moyen pour anciennes sauvegardes |
| Autres regions | Arabic, Oceania, Indochina, Persia, Malaya | Liste partiellement modernisee | Ne pas modifier pendant HOTFIX-5B2 | Hors scope |
| Nom de fichier | `06_new_imperialism.txt` | `06_new_imperialism_mod.txt` | Modifier le fichier local existant | Eleve si le fichier hotfix est copie : JE dupliquee |

Hunks JE exacts proposes :

1. Lignes 15-19 : remplacer les cinq `has_interest_marker_in_region` indiens par deux lignes utilisant `region_north_india` et `region_south_india`.
2. Lignes 45-46 et 48-50 : retirer les cinq appels de creation Bengal, Bombay, Punjab, Madras et Central India.
3. Lignes 58-59 et 61-63 : retirer les cinq appels d'expansion correspondants.
4. Ne modifier ni `possible`, ni les boutons hors Inde, ni le nom du fichier.

## 6. Flux de creation et d'expansion

Schema :

```text
JE je_new_imperialism
  -> bouton east_india_company (root = overlord)
  -> selection d'une capitale et marquage state_to_cede sur les states Inde
  -> create_dynamic_country (origin = root, type colonial)
  -> cession des states marques pendant la creation
  -> on_created : india_mod_subject_var + garde temporaire
  -> pacte chartered_company avec l'overlord
  -> new_imperialism_events.3 apres un jour
  -> l'event retrouve le sujet par newly_formed_colonial_nation_var
  -> applique lois, hierarchie, strategie et modifier
  -> expansions suivantes vers le meme sujet par india_mod_subject_var

BIC historique
  -> porte new_imperialism_mod_var des le setup
  -> expand_for_bic retrouve ce sujet
  -> transfere les states eligibles vers BIC
```

| Etape | Fichier | Scope root | Scope cible | Variable/garde | Risque |
|---|---|---|---|---|---|
| Affichage creation | `00_new_colonial_admins.txt:219` | Overlord | Ses states et sujets | Absence de `india_mod_subject_var` et `new_imperialism_mod_var` sous lui | IDs regionaux invalides avant adaptation |
| Validation | Meme bloc, ligne 241 | Overlord | States Inde | Au moins deux plus grands states, paix, pas de play engage, pas de sujet temporaire | Le comptage echoue si region invalide |
| Selection capitale | Lignes 272-313 | Overlord | State aleatoire, priorite au decret greener grass | Scope `newly_formed_colonial_nation_capital_scope` | Choix aleatoire mais comportement existant |
| Selection territoires | Lignes 314-325 | Overlord | Tous les states Inde scopes | `state_to_cede` | Marqueur temporaire a preserver |
| Creation | Lignes 326-349 | Overlord | Nouveau pays colonial | `india_mod_subject_var`; `newly_formed_colonial_nation_var` pendant 3 mois | Une erreur de scope casserait event et expansion |
| Statut sujet | Lignes 350-354 | Overlord | Proprietaire de la capitale creee | Pacte `chartered_company` | L'event recree aussi ce pacte ; comportement existant |
| Event | `new_imperialism_events_mod.txt:456` | Overlord declencheur | Sujet trouve par variable | `newly_formed_colonial_nation_var` | Choix aleatoire si plusieurs sujets temporaires, normalement bloque |
| Lois dynamiques | Event lignes 500-542 | Overlord puis nouveau sujet | Compagnie dynamique | `law_colonial_exploitation` notamment | Question de design separee |
| Expansion dynamique | Bouton lignes 1377-1483 | Overlord | Sujet `india_mod_subject_var` | Variable persistante | IDs regionaux invalides avant adaptation |
| Expansion BIC | Bouton lignes 2201-2328 | Overlord | Sujet `new_imperialism_mod_var` | Variable posee dans l'historique BIC | Label actuel trompeur et IDs invalides |

## 7. Cartographie des regions invalides

Il ne faut pas tenter de reproduire les cinq anciennes zones avec des strategic regions qui n'existent plus. Pour les trois actions portant sur une Compagnie des Indes unique, chaque ancienne zone contribue au perimetre national complet ; la cible fonctionnelle est donc l'union nord + sud.

| Fichier | Bloc | Ancien ID | Cible proposee | Justification | Confiance |
|---|---|---|---|---|---|
| `06_new_imperialism.txt` | Marqueurs d'interet | Chacun des cinq IDs | Consolider en `region_north_india` + `region_south_india` | La JE doit apparaitre pour un interet dans l'une des deux regions vanilla | Haute |
| `00_new_colonial_admins.txt` | `east_india_company.visible` | Les cinq | OR nord + sud | Detecter toute implantation indienne | Haute |
| Meme bloc | `possible` | Les cinq | OR nord + sud | Compter les states sur tout le perimetre de la compagnie unique | Haute |
| Meme bloc | Selection capitale avec/sans decret | Les cinq | OR nord + sud | Choisir la capitale dans l'ensemble indien valide | Haute |
| Meme bloc | Marquage `state_to_cede` | Les cinq | OR nord + sud | Creer une seule compagnie couvrant les possessions indiennes | Haute |
| `00_new_colonial_admins.txt` | `expand_east_india.possible/effect` | Les cinq | OR nord + sud | Etendre la meme compagnie dynamique sur toute l'Inde | Haute |
| `00_new_colonial_admins.txt` | `expand_for_bic.possible/effect` | Les cinq | OR nord + sud | Permettre a GBR de transferer ses acquisitions indiennes a BIC | Haute |
| Definitions regionales heritees | Chaque bouton dedie | ID correspondant | Aucun remplacement en HOTFIX-5B2 | Definitions conservees mais sans caller pour compatibilite transitoire | Moyenne |

La cartographie ne doit pas etre appliquee globalement au fichier : d'autres blocs hors des trois boutons actifs peuvent avoir une semantique regionale differente.

## 8. Analyse des boutons regionaux

| Bouton regional | Callers gameplay | Localisation | Effet | Peut etre retire ? | Risque |
|---|---|---|---|---|---|
| Creation Bengal | Seulement `06_new_imperialism.txt` | EN + FR | Cree une compagnie dynamique separee | Retirer le caller oui ; definition plus tard | Sauvegardes/mods externes |
| Creation Bombay | Seulement la JE | EN + FR | Cree une compagnie separee | Meme decision | Meme risque |
| Creation Madras | Seulement la JE | EN + FR | Cree une compagnie separee | Meme decision | Meme risque |
| Creation Central India | Seulement la JE | EN + FR | Cree une compagnie separee | Meme decision | Meme risque |
| Creation Punjab | Seulement la JE | EN + FR | Cree une compagnie separee | Meme decision | Meme risque |
| Expansion Bengal | Seulement la JE | EN + FR | Etend le sujet regional legacy | Retirer le caller oui | Anciennes sauvegardes avec variable legacy |
| Expansion Bombay | Seulement la JE | EN + FR | Etend le sujet regional legacy | Meme decision | Meme risque |
| Expansion Madras | Seulement la JE | EN + FR | Etend le sujet regional legacy | Meme decision | Meme risque |
| Expansion Central India | Seulement la JE, plus cles reutilisees a tort par BIC | EN + FR | Etend le sujet regional legacy | Retirer le caller ; conserver les cles | BIC doit changer de paire de cles |
| Expansion Punjab | Seulement la JE | EN + FR | Etend le sujet regional legacy | Retirer le caller oui | Meme risque |

Les recherches dans `common`, `events` et `localization` ne trouvent aucun autre caller gameplay. Les localisations ne sont pas des callers. HOTFIX-5B2 doit donc detacher les boutons de la JE mais laisser leurs definitions et localisations en place. Une phase ulterieure, apres test de nouvelles parties et decision sur la compatibilite des sauvegardes, pourra les supprimer.

## 9. Variables et gardes anti-doublon

| Variable | Porteur | Duree | Role | A preserver |
|---|---|---|---|---|
| `india_mod_subject_var` | Compagnie dynamique | Persistante | Identifie la compagnie unique creee par le bouton principal et sa cible d'expansion | Oui |
| `new_imperialism_mod_var` | BIC historique | Persistante | Identifie BIC comme administration historique et cible de `expand_for_bic` | Oui |
| `newly_formed_colonial_nation_var` | Nouveau sujet | 3 mois | Permet a l'event de retrouver le pays cree et bloque une nouvelle creation immediate | Oui |
| `state_to_cede` | States selectionnes | Temporaire, retire `on_created` | Delimite les states cedes au pays dynamique | Oui |

Analyse anti-doublon :

- Le bouton principal est masque si l'overlord a, parmi ses sujets ou sous-sujets, un pays portant l'une des deux variables persistantes.
- BIC porte `new_imperialism_mod_var` dans `common/history/countries/bic - british east india company.txt`. Un overlord de BIC ne devrait donc pas pouvoir creer en plus une compagnie dynamique.
- Une compagnie dynamique recoit `india_mod_subject_var` des sa creation. Son overlord ne devrait pas pouvoir recreer une autre compagnie.
- Le controle de `newly_formed_colonial_nation_var`, le cooldown de 90 jours et la duree de trois mois protegent la fenetre entre le clic et la resolution de l'event.
- Les boutons regionaux de creation ne partagent pas tous la garde persistante de la compagnie unique. Bien qu'ils soient masques, les laisser attaches a la JE entretient un chemin historique vers plusieurs compagnies. Leur retrait comme callers ferme ce risque dans l'interface normale.
- Deux compagnies peuvent exister mondialement sous des overlords differents. Le systeme garantit l'unicite par arbre de sujets, pas une unicite mondiale absolue ; ce comportement est coherent avec un outil colonial utilisable par plusieurs puissances.

Risque residuel : l'event utilise `random_subject_or_below` pour retrouver le sujet temporaire. Si un autre systeme creait simultanement plusieurs sujets portant la meme variable sous le meme overlord, la cible serait aleatoire. Les gardes et cooldowns rendent ce cas improbable, mais il ne faut pas supprimer ces protections.

## 10. BIC historique et compagnie dynamique

| Element | BIC historique | Compagnie dynamique |
|---|---|---|
| Identification | Tag `BIC`, variable `new_imperialism_mod_var` | Pays colonial dynamique, variable `india_mod_subject_var` |
| Creation | Setup historique | Bouton `east_india_company` |
| Expansion | `expand_for_bic` | `expand_east_india` |
| Loi coloniale a preserver | `law_frontier_colonization` | `law_colonial_exploitation` dans `new_imperialism_events.3` |
| Decision HOTFIX-5B2 | Ne pas modifier le fichier pays ni sa loi | Ne pas modifier l'event ni sa loi |

La difference de loi est classee **a conserver provisoirement et a soumettre a une decision de design separee**. Elle ne doit pas etre alignee implicitement pendant une correction de strategic regions.

## 11. Audit des localisations

| Cle | EN | FR | Caller actuel | Caller futur | Action future |
|---|---|---|---|---|---|
| `je_colonial_administration_button_india` | Oui, `mod_v2content` | Oui, `mod_v2content` | Creation EIC principale | Identique | Conserver |
| `je_colonial_administration_button_india_desc` | Oui | Oui | Creation EIC principale | Identique | Conserver |
| `je_colonial_administration_button_east_india` | Oui, `mod_v2content` | Oui, `mod_v2content` | Expansion dynamique | Expansion dynamique et BIC | Reutiliser aussi pour `expand_for_bic` |
| `je_colonial_administration_button_east_india_desc` | Oui | Oui | Expansion dynamique | Expansion dynamique et BIC | Reutiliser aussi pour `expand_for_bic` |
| Paires `bengal`, `bombay`, `madras`, `central_india`, `punjab` | Oui, `mod_journal_entries` | Oui, `mod_journal_entries` | Boutons regionaux attaches | Aucun caller gameplay apres B2 | Conserver temporairement, ne pas supprimer |
| Paires `expand_bengal`, `expand_bombay`, `expand_madras`, `expand_central_india`, `expand_punjab` | Oui | Oui | Expansions regionales ; Central India sert aussi par erreur a BIC | Aucun caller actif apres B2 | Conserver temporairement |
| Paires `north_india` / `south_india` | EN dans le hotfix | Absentes du fork FR | Aucun caller local | Aucun | Ne pas importer ni creer |
| Cle dediee `expand_for_bic` | Absente | Absente | Le bouton reutilise a tort Central India | Non necessaire | Ne pas creer ; reutiliser la paire generique East India |

Aucune cle requise n'est presente en anglais mais absente en francais dans le chemin recommande. Aucune modification de `localization/` n'est donc necessaire pour HOTFIX-5B2.

## 12. Risques

| Risque | Niveau | Mesure |
|---|---|---|
| Double definition de `je_new_imperialism` si le fichier hotfix est copie | Eleve | Modifier uniquement `06_new_imperialism.txt` |
| Remplacement integral de `00_new_colonial_admins.txt` ecrasant des adaptations locales | Eleve | Trois hunks nommes uniquement |
| Remplacement global des cinq IDs modifiant des boutons hors scope | Eleve | Limiter aux trois blocs actifs et a la JE |
| Ancienne sauvegarde dependant d'un sujet regional | Moyen | Conserver temporairement definitions, variables et localisations legacy |
| Label BIC « Inde centrale » | Moyen, visuel | Reutiliser les cles generiques East India existantes |
| BIC historique et compagnie dynamique sous le meme overlord | Faible apres correction | Preserver les deux gardes persistantes |
| Event ciblant le mauvais sujet temporaire | Faible | Preserver cooldown et variable temporaire |
| Changement involontaire de loi BIC/dynamique | Eleve | Ne modifier ni fichier pays BIC ni event |
| Perimetre nord + sud plus large que les anciennes zones | Moyen | Test territorial en jeu ; c'est cependant le perimetre choisi par le hotfix et valide par la vanilla |

## 13. Plan ferme HOTFIX-5B2

### Fichiers autorises

HOTFIX-5B2 pourra modifier exactement :

1. `common/journal_entries/06_new_imperialism.txt` ;
2. `common/scripted_buttons/00_new_colonial_admins.txt` ;
3. un rapport dedie `docs/reports/hotfix/HOTFIX_5B2_UNIQUE_EAST_INDIA_COMPANY.md`.

Aucun fichier EN/FR n'est necessaire. Aucun autre fichier ne doit entrer dans le diff.

### Hunks autorises dans la JE

1. Dans `is_shown_when_inactive`, remplacer uniquement les cinq marqueurs Inde invalides par `region_north_india` et `region_south_india`.
2. Retirer uniquement les cinq callers de creation regionaux.
3. Retirer uniquement les cinq callers d'expansion regionaux.
4. Conserver `expand_for_bic`, `east_india_company` et `expand_east_india`.
5. Ne pas toucher a `possible`, aux regions hors Inde, au pinning ou au poids.

### Hunks autorises dans les scripted buttons

1. Bloc `je_colonial_administration_button_east_india_company` : remplacer chaque OR des cinq regions par un OR nord + sud, sans changer la creation, les scopes, variables, cooldown, pacte ou event.
2. Bloc `je_colonial_administration_button_expand_east_india` : meme adaptation regionale, sans changer la recherche du sujet ni les transferts.
3. Bloc `je_colonial_administration_button_expand_for_bic` : meme adaptation regionale et remplacer seulement `name`/`desc` par les cles generiques `..._east_india` existantes.
4. Ne modifier aucune definition de bouton regional legacy pendant cette phase.

### Elements a preserver strictement

- `india_mod_subject_var` ;
- `new_imperialism_mod_var` ;
- `newly_formed_colonial_nation_var` ;
- `state_to_cede` ;
- cooldown de 90 jours ;
- pacte `chartered_company` ;
- appel `new_imperialism_events.3` ;
- `law_frontier_colonization` de BIC ;
- `law_colonial_exploitation` actuelle de la compagnie dynamique, jusqu'a une decision separee ;
- definitions et localisations regionales legacy, temporairement.

### Tests HOTFIX-5B2

1. Rechercher les cinq IDs invalides dans les trois blocs actifs et dans la JE : aucun ne doit y rester.
2. Confirmer que `region_north_india` et `region_south_india` existent dans la vanilla et sont presentes dans chaque hunk adapte.
3. Lancer une partie avec GBR/BIC existante : le bouton de creation ne doit pas permettre une seconde compagnie ; `expand_for_bic` doit transferer une acquisition du nord puis du sud a BIC.
4. Lancer une puissance europeenne sans BIC : creer une seule EIC dynamique, verifier le pacte, les states cedes, l'event `.3`, puis l'expansion nord/sud.
5. Verifier qu'aucun bouton Bengal/Bombay/Madras/Central India/Punjab n'apparait dans la JE.
6. Tester en anglais et en francais : aucun label brut et aucun libelle « Inde centrale » sur l'expansion BIC.
7. Passer plusieurs mois et surveiller `error.log` pour `region_bengal`, `region_bombay`, `region_central_india`, `region_madras`, `region_punjab`, `create_dynamic_country`, `new_imperialism_events.3` et erreurs de scope.
8. Executer `git diff --check`, `git status --short` et `git diff --name-only`.

## 14. Fichiers crees par l'audit

- `docs/reports/hotfix/HOTFIX_5B1_AUDIT_UNIQUE_EAST_INDIA_COMPANY.md`

## 15. Confirmation gameplay

Aucun fichier `common/`, `events/`, `localization/`, `map_data/` ou autre fichier gameplay n'a ete modifie. Aucun fichier hotfix ou vanilla n'a ete copie. Aucun merge et aucun commit n'ont ete effectues.

## 16. Confirmation stash MARATH

Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est reste present et intact. Il n'a pas ete applique, inspecte comme contenu courant, restaure, supprime ou modifie.
