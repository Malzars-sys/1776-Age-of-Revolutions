# HOTFIX-4E1 - Corrections Sakoku isolees

## 1. Resume

Cette phase importe exactement deux corrections isolees du hotfix dans `events/japan_events/ep2_sakoku_events.txt` : une ponderation IA identique pour les trois choix commerciaux de `ep2_sakoku.2`, puis une protection du scope etranger dans l'option A de l'incident Morrison.

Aucun autre hunk Sakoku, Tenpo ou Japon n'a ete importe.

## 2. Fichier compare

Le fichier suivant a ete compare entre le fork, le hotfix upstream et la vanilla The Great Wave :

- `events/japan_events/ep2_sakoku_events.txt`

Avant modification, les blocs cibles du fork etaient identiques a la vanilla. Le hotfix ajoutait les ponderations IA et utilisait un unique scope optionnel pour la relation Morrison.

## 3. Trois AI chances ajoutees

Un bloc identique a ete ajoute dans chacune des options commerciales A, B et C de `ep2_sakoku.2` :

```txt
ai_chance = {
    base = 10
}
```

Les options concernees sont :

| Option | Loi activee | Ponderation ajoutee |
|---|---|---:|
| `ep2_sakoku.2.a` | `law_mercantilism` | 10 |
| `ep2_sakoku.2.b` | `law_free_trade` | 10 |
| `ep2_sakoku.2.c` | `law_protectionism` | 10 |

Aucun trigger, stance, effet, modifier ou nom d'option n'a ete modifie.

## 4. Relations Morrison avant / apres

Avant, l'option `ep2_sakoku.3.a` appliquait :

1. `change_relations` depuis le Japon vers `scope:morrison_incident_country` ;
2. un second `change_relations` depuis le pays etranger vers le Japon ;
3. la notification dans un second bloc de scope non optionnel.

Apres, l'option utilise un seul bloc protege :

```txt
scope:morrison_incident_country ?= {
    change_relations = {
        country = root
        value = -30
    }
    post_notification = morrison_incident_has_incidented
}
```

Les autres effets et la ponderation IA existante de l'option sont conserves.

## 5. Pourquoi la relation n'est plus potentiellement doublee

`change_relations` modifie la relation entre les deux pays. La version precedente executait cette penalite une fois depuis chaque cote du lien diplomatique. La version hotfix ne l'execute qu'une fois depuis le pays etranger vers `root`, ce qui evite une penalite cumulee potentielle.

L'operateur `?=` empeche egalement l'execution du bloc si `scope:morrison_incident_country` n'est pas disponible. La notification est placee dans la meme garde.

## 6. Fichiers modifies

- `events/japan_events/ep2_sakoku_events.txt`

## 7. Ce qui n'a pas ete importe

- La selection des interest groups de `ep2_sakoku.2`.
- Les changements de comparaisons de stance.
- La suppression ou mutualisation de `forced_transition_from_tradition`.
- Le bloc `after` de `ep2_sakoku.2`.
- `modifier_ended_sakoku_movement`.
- L'option C de `ep2_sakoku.3`.
- `government_ig_dislikes_sakoku_tt`.
- Les changements de `caved_to_foreign_pressure_opposition` ou `light_hand_with_foreigners`.
- Toute variable ou tout trigger Sakoku.
- Tout changement Tenpo, Meiji, Iwakura, Ryukyu, Hokkaido/Ezo ou Zaibatsu.

## 8. Risques restants

- Les trois ponderations etant egales, elles ne changent pas la preference relative entre les options disponibles ; elles rendent seulement le comportement IA explicite.
- Les options B et C restent conditionnees par les scopes d'interest groups existants.
- Le scope Morrison est normalement cree par l'effet `immediate`. Si aucun pays eligible n'est trouve, la nouvelle garde evite l'effet de relation et la notification au lieu de produire un scope invalide.
- Les autres hunks identifies par HOTFIX-4E-AUDIT restent volontairement non traites.

## 9. Tests a faire en jeu

1. Declencher la fin forcee de Sakoku et verifier que les trois options commerciales apparaissent selon leurs conditions.
2. Laisser l'IA choisir chaque option sur plusieurs tests ou via sauvegardes reproductibles.
3. Declencher l'incident Morrison et choisir l'option A.
4. Verifier que la relation diminue de 30, et non de 60.
5. Verifier que le pays etranger recoit bien la notification.
6. Surveiller `error.log` pour `ep2_sakoku.2`, `ep2_sakoku.3`, `morrison_incident_country`, `invalid scope` et `change_relations`.

## 10. Liste exacte des fichiers modifies ou crees

- Modifie : `events/japan_events/ep2_sakoku_events.txt`
- Cree : `docs/reports/hotfix/HOTFIX_4E1_SAKOKU_ISOLATED_FIXES.md`

## 11. Confirmation de perimetre

- Aucun changement Tenpo.
- Aucun changement dans la JE Sakoku.
- Aucun changement de localisation.
- Aucun changement Meiji ou Iwakura.
- Aucun changement Ryukyu, Hokkaido/Ezo ou Zaibatsu.
- Aucun changement SKH/ULT, NAVY, ADMIN, IR1, BIC ou Inde.
- Le stash MARATH n'a pas ete applique ni modifie.
- Aucun commit n'a ete cree.
