# HOTFIX-5C2E4C1AF — Préparation statique du contrôle négatif Sepoy E-3

## 1. Résumé

Le contrôle négatif jetable E-3 est préparé sur l’état initial naturel de BIC. Il ouvre manuellement `sepoy_mutiny_events.2` sans mutation et doit permettre de constater que 2.e est bloquée lorsque West Bengal est présent mais Bombay absent. Verdict : `READY_FOR_COMBINED_BOMBAY_TRIGGER_RUNTIME_TEST`.

## 2. État Git initial

Racine exacte du fork, branche `hotfix-dlc-audit`, HEAD `2530f45 Fix Sepoy Bombay retreat trigger`. Aucun fichier suivi modifié ; le stash MARATH attendu est présent. Victoria 3 et le launcher étaient fermés.

## 3. Exception docs/research/technology/

`docs/research/technology/` était la seule entrée non suivie initiale. Elle est restée intacte et hors périmètre.

## 4. Vérification de la copie

Avant E-3 : 980 fichiers, 36 harnais, dont 4 E-2, 4 E-1, 4 E1D et 24 legacy ; aucun `.git`, aucun `remote_file_id`. Les 44 lignes non auto-référentielles du manifeste AE correspondaient, hors différence launcher explicitement attendue.

## 5. Correction AE

AE a remplacé uniquement le test West Bengal du trigger de 2.e par Bombay. Le Sepoy corrigé du fork et de la copie fait 63 653 octets, SHA-256 `66465CB840A5D7348E342F233205F0389E46E5E1C5ECA97B17870ED09D93C6BB`, BOM UTF-8, LF uniquement, et reste identique octet par octet.

## 6. Objectif E-3

Tester la direction négative : posséder West Bengal ne doit plus suffire à ouvrir 2.e lorsque BIC ne possède aucune portion réelle de Bombay.

## 7. Trigger Bombay corrigé

Le root du `country_event` est BIC. Le trigger actuel est exclusivement :

```text
trigger = {
	any_scope_state = {
		state_region = s:STATE_BOMBAY
	}
}
```

Il ne teste plus `STATE_WEST_BENGAL`, ne contient aucune alternative et conserve `ai_chance = { base = 40 }`. Les exclusions Bombay C1W des lignes de garde et de sélection restent inchangées ; West Bengal reste redistribuable.

## 8. Nécessité du contrôle négatif

E-2 établira que Bombay suffit même sans West Bengal. E-3 doit exclure le faux positif inverse : West Bengal présent ne doit pas autoriser la retraite vers Bombay si Bombay est absent.

## 9. Baseline West Bengal BIC

La portion BIC est réelle, peuplée et contrôlée par son owner BIC : state sérialisé 487, provinces internes attestées `40292` et `40306`, population 17 269 307. Elle contient la capitale initiale de BIC.

## 10. Baseline West Bengal COO

La portion COO est réelle, peuplée et contrôlée par son owner COO : state sérialisé 488, province interne `40305`, population 243 388. COO est sujet de BIC et sa capitale est dans West Bengal.

## 11. Baseline Bombay

Bombay est partagé naturellement entre POR, MARATH, SAT et KHP. La portion POR contient `x51F0A0` (identifiant sérialisé `39686`) et 446 391 habitants. MARATH/SAT/KHP conservent respectivement 25/10/3 provinces.

## 12. Absence Bombay BIC

L’état initial ne contient aucune portion réelle `STATE_BOMBAY` possédée par BIC. Aucune préparation territoriale n’est donc nécessaire pour E-3.

## 13. Baseline East Bengal

La portion BIC est réelle et non vide : state sérialisé 14, 30 provinces encodées `{40309 29}`, population 21 556 674, owner/controller BIC. E-3 la vérifie sans la modifier.

## 14. État E-3 recherché

West Bengal BIC présent et peuplé ; West Bengal COO présent et peuplé ; East Bengal BIC présent et peuplé ; Bombay BIC totalement absent ; Bombay POR présent et peuplé. C’est exactement la baseline naturelle d’une nouvelle partie BIC.

## 15. Namespace et identifiants

Namespace `zz_sepoy_test_e3`, décision `zz_sepoy_test_e3_open`, événement `zz_sepoy_test_e3.1` et sept clés de localisation prescrites. La recherche préalable dans fork, copie, source hotfix et vanilla a produit zéro conflit.

## 16. Décision E-3

Une seule décision, visible et possible uniquement pour `is_player = yes` et `c:BIC ?= this`, vérifie les cinq préconditions territoriales et possède une chance IA nulle.

## 17. Event de confirmation

Le `country_event` BIC contient exactement deux options manuelles : `OPEN_REAL_EVENT` et `CANCEL`. Cancel ne contient aucun effet.

## 18. Appel manuel à event 2

L’option d’ouverture revérifie tout l’état E-3 puis contient l’unique appel `trigger_event = { id = sepoy_mutiny_events.2 popup = yes }` sur le scope root BIC.

## 19. Absence de mutation

Zéro `set_state_owner`, `add_radicals_in_state`, `set_variable`, `make_independent`, changement de marché, relation, capitale ou scripted effect gameplay. Aucun marqueur n’est posé.

## 20. Absence de sélection automatique

Aucun `default_option`, choix automatique, hasard, boucle ou console. Le harnais ouvre l’événement réel sans choisir l’une de ses options.

## 21. Custom tooltips

Deux `custom_tooltip` réels et évalués portent les préconditions complexes : un dans la décision et un dans le trigger de l’option d’ouverture.

## 22. Localisations

Les sept clés EN et les sept clés FR décrivent le contrôle négatif jetable, les présences West/East Bengal, l’absence Bombay, l’absence de mutation, l’interdiction de choisir une option réelle, la sauvegarde/recharge, E-2 positif séparé et la redistribution attendue de West Bengal après une vraie retraite.

## 23. Contrôles BOM/LF

Les quatre fichiers E-3 commencent par `EF BB BF`, sont UTF-8 valides, contiennent uniquement des LF et zéro CR. Les deux scripts portent l’avertissement exact `DISPOSABLE E-3 NEGATIVE TRIGGER TEST HARNESS - DO NOT COPY TO MAIN MOD`.

## 24. Validation structurelle

Décision : 17 accolades ouvrantes/17 fermantes. Événement : 17/17. Total : une décision, un événement, deux options, deux tooltips, un appel à `.2`, zéro mutation, marqueur, automatisme, hasard ou boucle.

## 25. Contrôle des anciens harnais

Les 36 harnais antérieurs correspondent au manifeste AE. E-2 conserve exactement deux mutations (`Bombay POR → BIC`, puis `West Bengal BIC → COO`) et un appel manuel ; E-1 est inchangé ; E1D conserve ses BOM ; les 24 legacy sont inchangés.

## 26. Résumé du manifeste

Le manifeste AF inventorie 49 entrées : 40 harnais, deux Sepoy, deux journaux, trois descripteurs/marqueurs et deux livrables AF. Chaque fichier matériel reçoit taille, SHA-256 et contrôles d’encodage ; le manifeste s’identifie comme auto-référentiel.

## 27. Plan runtime combiné

AG devra employer une seule ouverture de Victoria 3, une seule nouvelle partie BIC, aucune session GBR, au maximum deux rechargements, aucune fermeture intermédiaire, une seule fermeture finale et aucune option réelle sélectionnée.

## 28. Branche négative E-3

Commencer par la baseline naturelle, confirmer West Bengal BIC présent et Bombay BIC absent, créer `HOTFIX_5C2E4C1AG_E3_NEGATIVE_PRE_EVENT`, ouvrir E-3 puis l’événement réel et constater `OPTION_2E_HIDDEN_NEGATIVE` ou `OPTION_2E_DISABLED_NEGATIVE`. Ne rien choisir, recharger la sauvegarde, compter `RELOAD_1` et vérifier zéro fuite.

## 29. Branche positive E-2

Depuis la base rechargée, préparer E-2, confirmer Bombay BIC présent, West Bengal BIC absent et entièrement COO, East Bengal BIC présent, puis créer `HOTFIX_5C2E4C1AG_E2_POSITIVE_PRE_EVENT`. Ouvrir avec E-2 et constater `OPTION_2E_AVAILABLE_POSITIVE`. Ne rien choisir, recharger et compter `RELOAD_2`.

## 30. Rechargements de sécurité

Après chaque inspection, recharger la sauvegarde pré-événement correspondante et vérifier zéro fuite. `HOTFIX_5C2E4C1AG_POST_RELOAD_CONTROL` peut être créé après le second contrôle. Deux rechargements maximum, puis fermeture unique et analyse hors jeu.

## 31. Critères du futur runtime

`PASS_E3_TRIGGER_FIX_NEGATIVE` exige West Bengal BIC présent, Bombay BIC absent, 2.e cachée/désactivée, aucun choix et recharge propre. `PASS_E2_TRIGGER_FIX_POSITIVE` exige Bombay BIC présent, West Bengal BIC absent, 2.e visible/sélectionnable, aucun choix et recharge propre.

## 32. Verdict attendu

Si les deux directions passent : `PASS_BOMBAY_TRIGGER_RUNTIME_VALIDATION` et `BOMBAY_TRIGGER_ACCESS_CONFIRMED`. Échecs possibles : `FAIL_E3_TRIGGER_FIX_FALSE_POSITIVE`, `FAIL_E2_TRIGGER_FIX_STILL_BLOCKED`, `FAIL_TRIGGER_FIX_EVENT_EFFECT_LEAK`, `BLOCKED_TRIGGER_FIX_RELOAD_FAILED`, `BLOCKED_TRIGGER_FIX_FILES_CHANGED`.

## 33. WEST_BENGAL_RETREAT_TRANSFER_EXPECTED

`WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`. La correction concerne l’accès à 2.e, pas la redistribution postérieure de West Bengal après sélection réelle.

## 34. Risques restants

La présentation négative peut être cachée ou désactivée selon l’UI ; les deux résultats sont acceptables. Seul le runtime combiné AG pourra confirmer le comportement évalué après AE.

## 35. Verdict statique

`READY_FOR_COMBINED_BOMBAY_TRIGGER_RUNTIME_TEST`.

## 36. Fichiers créés

Copie : quatre fichiers E-3 prescrits. Fork : ce rapport et `HOTFIX_5C2E4C1AF_E3_HARNESS_MANIFEST.csv`. Aucun autre fichier n’est créé ou modifié.

## 37. Confirmation Sepoy et journal

Sepoy fork/copie reste identique au hash AE. Le journal `common/journal_entries/04_sepoy_mutiny.txt` du fork et de la copie est inchangé et identique au contrôle AE.

## 38. Confirmation Bengal/Madras/Bombay/Travancore/MARATH

Bengal 2.b, Madras 2.c, les protections Bombay C1W, Travancore/`STATE_TRAVANCORE`, East Bengal, COO et les données MARATH/SAT/KHP sont intacts. NAVY et ADMIN sont hors périmètre.

## 39. Confirmation docs/research/technology/

Le répertoire non suivi `docs/research/technology/` est resté intact ; aucune lecture-écriture de contenu de recherche n’a été effectuée.

## 40. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste intact. Aucun `apply`, `pop`, `drop` ni commit automatique n’a été exécuté.
