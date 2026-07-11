# HOTFIX-4E2 - Presentation de l'option C de l'incident Morrison

## 1. Resume

Cette phase adapte uniquement la presentation de l'option `ep2_sakoku.3.c`. Sa condition d'interest group est maintenant visible, l'option peut rester affichee comme indisponible, et la comparaison avec `neutral` est strictement inferieure.

Une localisation dediee a ete ajoutee en anglais et en francais. Les effets existants de l'option, dont `caved_to_foreign_pressure_opposition`, sont conserves.

## 2. Situation avant modification

La condition utilisait :

- un `hidden_trigger` pour verifier l'absence de `je_sakoku_maybe_we_should_open_up` ;
- un `any_interest_group` au gouvernement ;
- une stance envers `law_isolationism` avec `value <= neutral`.

Lorsque la condition n'etait pas satisfaite, l'option et sa raison d'indisponibilite n'etaient pas presentees clairement au joueur.

## 3. Situation apres modification

Le trigger utilise maintenant un `custom_tooltip` nomme `government_ig_dislikes_sakoku_tt`. Il contient :

- l'existence d'au moins un interest group au gouvernement ;
- une stance strictement opposee a `law_isolationism`, avec `value < neutral` ;
- l'absence de la variable `je_sakoku_maybe_we_should_open_up`.

Un bloc `show_as_unavailable` permet d'afficher l'option dans son etat indisponible lorsque la variable d'ouverture n'a pas encore ete posee.

## 4. Condition visible ajoutee

La condition visible exprime qu'un groupe d'interet membre du gouvernement doit s'opposer a la politique d'isolement. Elle remplace uniquement la presentation cachee de cette condition et ne modifie aucun effet de l'option.

## 5. Localisations EN/FR ajoutees

La cle suivante a ete definie dans deux fichiers dedies :

| Cle | Anglais | Francais |
|---|---|---|
| `government_ig_dislikes_sakoku_tt` | An Interest Group in government must oppose the policy of isolation. | Un groupe d'interet au gouvernement doit s'opposer a la politique d'isolement. |

Les deux fichiers utilisent leur en-tete correct et l'encodage UTF-8 avec BOM.

## 6. Conservation du modifier d'opposition

Le modifier `caved_to_foreign_pressure_opposition` est conserve sans changement. Le hunk hotfix qui le remplace par `light_hand_with_foreigners` n'a pas ete importe.

Les autres effets conserves incluent :

- `je_sakoku_maybe_we_should_open_up` ;
- `caved_to_foreign_pressure_government` ;
- la ponderation IA existante de l'option C ;
- le tooltip `end_sakoku_button_now_available`.

## 7. Ce qui n'a pas ete importe

- Aucun changement dans `ep2_sakoku.2`.
- Aucun changement dans les options A ou B de `ep2_sakoku.3`.
- Aucun changement des triggers generaux de l'evenement.
- Aucun remplacement par `light_hand_with_foreigners`.
- Aucun contenu `modifier_ended_sakoku_movement`.
- Aucun contenu Tenpo, Meiji, Iwakura, Ryukyu, Hokkaido/Ezo ou Zaibatsu.
- Aucun changement des JE Sakoku ou Tenpo.

## 8. Risques restants

- La condition stricte `< neutral` exclut les interest groups exactement neutres, contrairement a la version locale precedente.
- `show_as_unavailable` doit etre confirme visuellement dans l'interface de l'evenement.
- La variable d'ouverture et les effets politiques restent ceux du fork ; cette phase ne change pas leur fonctionnement.

## 9. Tests a faire en jeu

1. Declencher l'incident Morrison sans interest group gouvernemental oppose a l'isolation.
2. Verifier que l'option C reste visible mais indisponible.
3. Verifier que le tooltip EN et FR explique la condition sans cle brute.
4. Ajouter un interest group gouvernemental avec une stance strictement inferieure a `neutral` et verifier que l'option devient disponible.
5. Choisir l'option et confirmer que `je_sakoku_maybe_we_should_open_up` est posee.
6. Verifier que les opposants recoivent `caved_to_foreign_pressure_opposition`.
7. Surveiller `error.log` pour `government_ig_dislikes_sakoku_tt`, `ep2_sakoku.3`, `show_as_unavailable`, `custom_tooltip` et `invalid scope`.

## 10. Liste exacte des fichiers modifies ou crees

- Modifie : `events/japan_events/ep2_sakoku_events.txt`
- Cree : `localization/english/hotfix_sakoku_morrison_l_english.yml`
- Cree : `localization/french/hotfix_sakoku_morrison_l_french.yml`
- Cree : `docs/reports/hotfix/HOTFIX_4E2_MORRISON_OPTION_C.md`

## 11. Confirmation de perimetre

- Aucun changement Tenpo.
- Aucun changement dans la JE Sakoku.
- Aucun changement dans `ep2_sakoku.2`.
- Aucun changement dans les options A ou B de `ep2_sakoku.3`.
- Aucun changement Meiji ou Iwakura.
- Aucun changement Ryukyu, Hokkaido/Ezo ou Zaibatsu.
- Les corrections HOTFIX-4E1 sont conservees.
- Les tooltips Sakoku locaux et le declenchement Tenpo differe sont conserves.
- Le stash MARATH n'a pas ete applique ni modifie.
- Aucun commit n'a ete cree.
