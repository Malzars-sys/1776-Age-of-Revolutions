# HOTFIX-4E3 - Effets communs de sortie Sakoku

## 1. Resume

Cette phase mutualise l'application de `forced_transition_from_tradition` dans `ep2_sakoku.2`. Les trois copies placees dans les options commerciales A, B et C ont ete retirees et remplacees par une seule application commune dans `after`.

Le modifier commun utilise maintenant `is_decaying = yes`, conformement au hunk hotfix retenu. Aucun effet Meiji ou Iwakura n'a ete importe.

## 2. Situation avant modification

Chaque option commerciale appliquait separement le meme effet a tous les interest groups favorables a `law_isolationism` :

```txt
every_interest_group = {
    limit = {
        law_stance = {
            law = law_type:law_isolationism
            value > neutral
        }
    }
    add_modifier = {
        name = forced_transition_from_tradition
        days = normal_modifier_time
    }
}
```

Le fichier contenait donc trois copies fonctionnellement identiques.

## 3. Situation apres modification

Les options A, B et C conservent leurs lois, leurs effets propres et leurs ponderations IA. Une fois l'option choisie, le bloc `after` execute une seule application commune de `forced_transition_from_tradition`.

## 4. Trois doublons retires

Les trois blocs retires se trouvaient dans :

- `ep2_sakoku.2.a`, apres les effets propres au mercantilisme ;
- `ep2_sakoku.2.b`, apres les effets propres au libre-echange ;
- `ep2_sakoku.2.c`, apres les effets propres au protectionnisme.

Aucun autre modifier ou effet n'a ete retire.

## 5. Effet commun ajoute dans after

Le bloc commun conserve exactement la meme condition :

- parcours de tous les interest groups ;
- stance envers `law_isolationism` strictement superieure a `neutral` ;
- duree `normal_modifier_time`.

Il s'execute apres n'importe laquelle des trois options, ce qui garantit une seule application par resolution de l'evenement.

## 6. Confirmation de is_decaying

L'application commune contient explicitement :

```txt
is_decaying = yes
```

Le modifier decroit donc selon la duree configuree au lieu de rester a pleine intensite jusqu'a son expiration.

## 7. Absence du modifier Meiji

`modifier_ended_sakoku_movement` n'a pas ete ajoute. Aucun scope vers `movement_meiji_restorationist`, aucune variable Meiji et aucun effet Iwakura ne figurent dans le nouveau bloc `after`.

## 8. Fichier modifie

- `events/japan_events/ep2_sakoku_events.txt`

## 9. Ce qui n'a pas ete importe

- La selection des interest groups dans `immediate`.
- Les changements de comparaisons de stance du hotfix.
- `modifier_ended_sakoku_movement`.
- `movement_meiji_restorationist`.
- Tout effet Meiji ou Iwakura.
- Tout changement dans l'incident Morrison.
- Tout changement Tenpo ou dans les JE Sakoku/Tenpo.
- Tout contenu Ryukyu, Hokkaido/Ezo ou Zaibatsu.

## 10. Risques restants

- Le passage a `is_decaying = yes` modifie la courbe temporelle du malus, comme prevu par le hotfix.
- Il faut confirmer en jeu que le moteur execute `after` une seule fois pour chacune des trois options.
- Les autres differences de `ep2_sakoku.2` identifiees par l'audit restent volontairement hors perimetre.

## 11. Tests a faire en jeu

1. Declencher `ep2_sakoku.2` et choisir successivement A, B puis C sur trois sauvegardes.
2. Verifier que chaque loi commerciale attendue est activee.
3. Verifier que `forced_transition_from_tradition` est applique une seule fois aux interest groups eligibles.
4. Verifier que le modifier est marque comme decroissant et expire normalement.
5. Confirmer que les effets `overdue_break_with_tradition` propres a chaque choix sont inchanges.
6. Surveiller `error.log` pour `ep2_sakoku.2`, `forced_transition_from_tradition`, `after`, `invalid scope` et `unknown modifier`.

## 12. Liste exacte des fichiers modifies ou crees

- Modifie : `events/japan_events/ep2_sakoku_events.txt`
- Cree : `docs/reports/hotfix/HOTFIX_4E3_SAKOKU_COMMON_EXIT_EFFECTS.md`

## 13. Confirmation de perimetre

- Aucun changement Tenpo.
- Aucun changement dans la JE Sakoku.
- Aucun changement Morrison.
- Les corrections HOTFIX-4E1 et HOTFIX-4E2 sont conservees.
- Les trois `ai_chance = { base = 10 }` sont conservees.
- `caved_to_foreign_pressure_opposition` est conserve.
- Aucun changement Meiji ou Iwakura.
- Aucun changement Ryukyu, Hokkaido/Ezo ou Zaibatsu.
- Les tooltips francais Sakoku locaux et le declenchement Tenpo differe sont conserves.
- Le stash MARATH n'a pas ete applique ni modifie.
- Aucun commit n'a ete cree.
