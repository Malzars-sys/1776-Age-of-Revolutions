# HOTFIX-4E8 - Correction de la condition EZO pour Hokkaido

## 1. Resume

La branche EZO de `je_taming_the_north.is_shown_when_inactive` teste maintenant directement `law_presidential_republic`. Les deux government types inexistants herites du hotfix ont ete retires. La branche JAP et tout le reste de l'entree de journal sont inchanges.

## 2. Probleme corrige

La condition d'acces d'EZO utilisait `gov_ezo_republic` et `gov_ezo_republic_colonial`. L'audit HOTFIX-4E7 a confirme que ces identifiants ne sont definis ni dans le fork, ni dans le hotfix upstream, ni dans la vanilla The Great Wave. Cette condition pouvait donc rendre `je_taming_the_north` inaccessible a EZO.

## 3. Condition avant modification

```txt
AND = {
    c:EZO ?= this
    OR = {
        has_government_type = gov_ezo_republic
        has_government_type = gov_ezo_republic_colonial
    }
}
```

## 4. Condition apres modification

```txt
AND = {
    c:EZO ?= this
    has_law_or_variant = law_type:law_presidential_republic
}
```

## 5. Couverture d'EZO vassale et independante

Le test porte sur la loi politique d'EZO et non sur le nom de son government type. Il reste donc vrai tant qu'EZO conserve `law_presidential_republic`, qu'elle soit vassale de JAP ou independante. Les distinctions entre ces deux statuts sont deja gerees plus loin par les scopes et les conditions de sujet de la journal entry et de ses evenements.

## 6. Government type vanilla

La vanilla The Great Wave fournit toujours `gov_domain_frontier` pour une EZO vassale de JAP qui possede `law_presidential_republic`. Aucun government type local n'a ete cree ou remplace. Si EZO devient independante, le moteur peut selectionner un government type republicain generique sans bloquer cette porte d'acces.

## 7. Fichiers modifies

- `common/journal_entries/07_hokkaido.txt` : remplacement limite de la condition EZO.
- `docs/reports/hotfix/HOTFIX_4E8_FIX_EZO_HOKKAIDO_GATE.md` : present rapport.

## 8. Elements non modifies

La branche JAP, l'ownership de Hokkaido, les blocs `possible` et `immediate`, les boutons, les barres de progression, ainsi que les conditions de completion et d'echec sont inchanges. Aucun event Hokkaido, government type, historique de pays, state, pop, batiment, on_action, fichier de carte ou fichier de localisation n'a ete modifie.

Aucun changement ne concerne SKH, ULT, Sakhalin, Ryukyu, Sakoku, Tenpo, Zaibatsu, Iwakura/Meiji, NAVY, ADMIN, IR1, BIC ou l'Inde.

## 9. Risques restants

- Une EZO qui abandonne `law_presidential_republic` ne satisfera plus cette condition, ce qui est coherent avec la portee republicaine du chemin importe.
- La visibilite effective depend encore des autres conditions existantes, notamment du DLC et de la possession d'une partie de `STATE_HOKKAIDO`.
- Une validation en jeu reste necessaire pour confirmer le comportement du moteur avec EZO vassale puis independante.

## 10. Tests a faire en jeu

1. Lancer une partie avec EZO vassale de JAP et verifier que `je_taming_the_north` peut apparaitre lorsque les autres conditions sont remplies.
2. Tester EZO independante en conservant `law_presidential_republic` et verifier le meme acces.
3. Lancer JAP et confirmer que son affichage et son comportement sont inchanges.
4. Surveiller `error.log` pour `07_hokkaido.txt`, `je_taming_the_north`, `gov_ezo_republic`, `gov_ezo_republic_colonial` et `law_presidential_republic`.

## 11. Liste exacte des fichiers modifies ou crees

- Modifie : `common/journal_entries/07_hokkaido.txt`.
- Cree : `docs/reports/hotfix/HOTFIX_4E8_FIX_EZO_HOKKAIDO_GATE.md`.

## 12. Confirmations

- La branche JAP est inchangee.
- Aucun government type n'a ete cree.
- Aucun event Hokkaido n'a ete modifie.
- Aucun state, pop ou batiment n'a ete modifie.
- Aucun changement Sakoku, Tenpo, Ryukyu ou Zaibatsu n'a ete effectue.
- Aucun changement NAVY, ADMIN, IR1, BIC ou Inde n'a ete effectue.
- Le stash MARATH n'a pas ete applique, modifie ou supprime.
- Aucun commit automatique n'a ete cree.
