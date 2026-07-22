# HOTFIX-5C2E4C1AC — Préparation statique du scénario Sepoy E-2

## 1. Résumé

Le scénario jetable E-2 est préparé sans modifier le gameplay du fork. Il place une portion réelle de `STATE_BOMBAY` chez BIC, retire toute portion réelle de `STATE_WEST_BENGAL` à BIC en l’agrégeant à COO, puis permet d’ouvrir manuellement `sepoy_mutiny_events.2` sans choix automatique. Verdict : `READY_FOR_E2_AVAILABILITY_RUNTIME_TEST`.

## 2. État Git initial

Racine exacte : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD : `f995f2a Validate Sepoy Bombay radical behavior`. Aucun fichier suivi modifié.

## 3. Exception docs/research/technology/

`docs/research/technology/` était la seule entrée non suivie initiale. Elle appartient à l’utilisateur et n’a pas été ouverte, modifiée ou incluse dans les livrables C1AC.

## 4. Vérification initiale de la copie

La copie comptait exactement 976 fichiers et 32 harnais. Elle contenait quatre fichiers E-1 et quatre fichiers E1D, aucun `.git` et aucun `remote_file_id`. Sepoy faisait 63 658 octets, SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`. Les scripts E1D faisaient 858 et 2 449 octets avec les SHA attendus et leur BOM corrigé. Les 36 contrôles du manifeste C1AA correspondaient sans divergence.

## 5. Résultat final E-1/AB

AB a établi que `SMALL_BOMBAY`, `LARGE_BOMBAY` et 2.e produisent leurs radicaux immédiatement et complètement. Bombay reste BIC après la correction C1W, tandis que la portion BIC de West Bengal est redistribuée à COO. Le défaut radical C1X est non reproductible ou dépendant du timing ; `WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED` reste séparé.

## 6. Objectif E-2

Prouver en runtime la disponibilité fonctionnelle de 2.e lorsque BIC possède un noyau Bombay réel mais aucune portion réelle de West Bengal. Aucun effet réel de 2.e ne doit être exécuté pendant ce test.

## 7. Trigger réel de 2.e

Dans le fork et la copie, le trigger occupe les lignes 1434–1438 (`STATE_WEST_BENGAL` ligne 1436) ; dans la source hotfix et la vanilla 1.13, les lignes 1418–1422 (`STATE_WEST_BENGAL` ligne 1420). Dans les quatre fichiers, le country scope est le root BIC de `sepoy_mutiny_events.2` et le trigger est exactement :

```txt
trigger = {
	any_scope_state = {
		state_region = s:STATE_WEST_BENGAL
	}
}
```

Une portion réelle de West Bengal possédée par BIC rend donc ce prédicat vrai ; son absence doit le rendre faux.

## 8. Absence de Bombay dans le trigger

Le trigger ne contient ni `STATE_BOMBAY`, ni vérification d’une portion Bombay réelle, ni contrôle de propriétaire Bombay. Il dépend exclusivement de West Bengal malgré le nom et la localisation de retraite vers Bombay.

## 9. Comportement UI attendu

Le modèle local des options d’événement emploie `option.trigger` comme condition de sélection et expose les conditions évaluées dans le tooltip. L’attente principale est donc une option 2.e visible mais désactivée avec échec West Bengal. Une option entièrement cachée reste un résultat bloqué acceptable ; le runtime doit distinguer `OPTION_2E_HIDDEN`, `OPTION_2E_DISABLED` et `OPTION_2E_AVAILABLE_UNEXPECTEDLY` au lieu de présumer la présentation exacte.

## 10. Baseline West Bengal

L’historique crée un split state : 16 provinces BIC et une province COO. La sauvegarde E-1 pré‑2.e sérialise la portion BIC en state 487, provinces internes `40292` et `40306`, population 17 269 307, et la portion COO en state 488, province `40305`, population 243 388. Owner et controller suivent respectivement BIC et COO ; aucun controller distinct n’est déclaré. Les deux portions sont incorporées par défaut.

## 11. Portion BIC West Bengal

La portion BIC contient l’essentiel de la population et les bâtiments historiques explicites : administration, centre de commerce, construction, mines de fer et charbon, exploitation forestière, plantations d’opium, soie, tabac et teinture, armement, verrerie, chantier naval, textile, papier, pêche et port. West Bengal est la capitale initiale attestée de BIC. Le transfert emporte le state et ses pops/bâtiments sans les éditer séparément.

## 12. Portion COO West Bengal

COO possède initialement une portion distincte, réelle et peuplée dans la même state region. Aucun bâtiment propre n’est explicitement créé dans son bloc historique. COO est sujet de BIC avant l’événement, sa capitale est dans West Bengal, et C1V/AB attestent que l’agrégation BIC vers COO fonctionne : COO survit et reçoit la portion voisine sans owner nul ni double attribution.

## 13. Baseline East Bengal

`STATE_EAST_BENGAL` est un state BIC distinct de 30 provinces, avec pops et bâtiments propres. E-2 ne le scope dans aucun effet. La décision d’ouverture exige encore un region state BIC réel, peuplé et possédé par root ; ce contrôle sûr confirme sa présence sans le muter.

## 14. Baseline Bombay

L’historique crée quatre portions Bombay : POR, MARATH, SAT et KHP. Le scénario n’utilise que la portion POR attestée par E-1 et ne touche jamais les trois portions indiennes.

## 15. Portion POR Bombay

Scope exact : `s:STATE_BOMBAY.region_state:POR`. Province `x51F0A0`, identifiant sérialisé `39686`, population 446 391, dont 75 852 hindous. Portion non incorporée, avec centre de commerce, rizière niveau 2 et port niveau 1. POR conserve de nombreux autres territoires, sa capitale et son existence après transfert ; POR → BIC est donc sûr.

## 16. Portions MARATH/SAT/KHP

MARATH conserve 25 provinces, SAT 10 et KHP 3. Leurs populations, propriétaires, sujets, capitales, bâtiments et relations ne sont ni scopés ni modifiés. Aucune donnée MARATH n’est écrite.

## 17. État E-2 recherché

Après préparation : `x51F0A0` appartient à BIC et forme un Bombay BIC réel/non vide ; BIC ne possède aucun state réel West Bengal ; COO conserve sa portion initiale et reçoit toute l’ancienne portion BIC ; East Bengal reste BIC ; MARATH/SAT/KHP restent à 25/10/3 provinces.

## 18. Première mutation

La première mutation est exactement `s:STATE_BOMBAY.region_state:POR = { set_state_owner = c:BIC }`. Elle a déjà été validée par E-1 et ne détruit pas POR.

## 19. Deuxième mutation

La seconde mutation est exactement `s:STATE_WEST_BENGAL.region_state:BIC = { set_state_owner = c:COO }`. Elle a déjà été matérialisée par 2.e dans C1V/AB : l’ancien state BIC devient vide/sans owner réel et ses provinces sont agrégées au state COO.

## 20. Ordre des mutations

L’option de préparation exécute strictement : (1) Bombay POR → BIC ; (2) West Bengal BIC → COO ; (3) `set_variable = zz_sepoy_test_e2_ready`.

## 21. Effets secondaires

Aucun controller, capitale, culture, religion, bâtiment, sujet, relation, indépendance ou radical n’est modifié explicitement. BIC conserve East Bengal, Bombay et de nombreux autres states ; COO et POR survivent. La perte du state-capitale West Bengal peut provoquer une relocalisation automatique interne de la capitale BIC par le moteur, mais le harnais n’appelle aucun effet de capitale et cette conséquence doit seulement être relevée au runtime.

## 22. Namespace et identifiants

Namespace `zz_sepoy_test_e2`; décisions `zz_sepoy_test_e2_prepare` et `zz_sepoy_test_e2_open_event`; événement `zz_sepoy_test_e2.1`; marqueur `zz_sepoy_test_e2_ready`. Les dix clés EN/FR prescrites existent. La recherche préalable dans fork, copie et vanilla a trouvé zéro conflit.

## 23. Décision de préparation

Visible uniquement pour le joueur BIC, elle exige `is_player = yes`, `c:BIC ?= this` et l’absence du marqueur. Son tooltip évalué confirme Bombay POR réel/peuplé, aucun Bombay BIC, West Bengal BIC réel/peuplé et West Bengal COO réel/peuplé. Sa chance IA est nulle ; `when_taken` ouvre seulement l’événement E-2 de préparation.

## 24. Event de préparation

`zz_sepoy_test_e2.1` est un `country_event` BIC avec exactement deux options : préparation explicite et annulation vide. La préparation contient seulement les deux `set_state_owner` puis l’unique `set_variable`.

## 25. Décision d’ouverture

Visible uniquement au joueur BIC marqué prêt, elle vérifie Bombay BIC réel/peuplé, zéro West Bengal réel BIC via `NOT any_scope_state`, West Bengal COO réel/peuplé et East Bengal BIC réel/peuplé. Elle ne mute rien et appelle exactement une fois `sepoy_mutiny_events.2` sur le root BIC.

## 26. Absence d’effet automatique

Il n’existe aucun `default_option`, aucun choix d’option réelle, aucune boucle, aucun hasard et aucun appel de l’événement réel pendant la préparation. L’événement réel n’est ouvert que par la seconde décision manuelle.

## 27. Méthode d’inspection sans sélection

Créer la sauvegarde immuable `HOTFIX_5C2E4C1AD_E2_PRE_EVENT`, ouvrir l’événement, inspecter 2.e et son tooltip, ne cliquer sur aucune option, puis recharger immédiatement la sauvegarde pré‑ouverture dans la même session.

## 28. Recharge de sécurité

La recharge annule l’instance d’événement ouverte et garantit qu’aucun état post‑choix ne sert de base. Après recharge, contrôler territoires, sujets, relations et radicaux, puis fermer Victoria une seule fois. Cette méthode évite toute contamination par une autre option réelle.

## 29. Custom tooltips

Trois vrais `custom_tooltip` évalués encapsulent les préconditions complexes : préparation dans la décision, préparation dans l’event, et ouverture. Ils exécutent les conditions qu’ils décrivent ; aucun texte décoratif ne remplace la logique.

## 30. Localisations

Les dix clés minimales existent en anglais et français. Elles expliquent le caractère jetable, les deux transferts, East Bengal et MARATH inchangés, l’inspection exclusive de 2.e, la sauvegarde immuable, l’interdiction de choisir une option réelle, la recharge obligatoire, l’absence de restauration automatique et la distinction E-1/E-2/E-3.

## 31. Contrôles BOM/LF

Les quatre fichiers E-2 commencent par `EF BB BF`, sont UTF-8 valides, utilisent uniquement LF et contiennent zéro CR. Les scripts ont 32/32 et 17/17 accolades ouvrantes/fermantes.

## 32. Validation statique

Le harnais contient deux décisions, un event, deux options, exactement deux `set_state_owner`, un `set_variable`, zéro `add_radicals_in_state`, un appel à `sepoy_mutiny_events.2`, zéro option automatique, zéro console, zéro boucle et zéro hasard. Les scopes exacts POR Bombay, BIC West Bengal et COO West Bengal sont attestés par historique et runtime antérieur.

## 33. Résumé du manifeste

Le manifeste inventorie les 36 harnais (4 E-2, 4 E1D, 4 E-1, 24 antérieurs), les contrôles Sepoy/journal fork et copie, les trois descripteurs/marqueurs, et les deux livrables C1AC. Les 36 contrôles C1AA existants ont zéro divergence.

## 34. Plan runtime condensé

Une ouverture Victoria, une nouvelle partie BIC, une recharge et une fermeture finale : relever Bombay/West Bengal ; préparer E-2 ; confirmer Bombay BIC, West Bengal entièrement COO, East Bengal et MARATH/SAT/KHP inchangés ; créer `HOTFIX_5C2E4C1AD_E2_PRE_EVENT` ; ouvrir l’événement ; classer 2.e ; capturer le tooltip ; ne rien choisir ; recharger ; confirmer zéro fuite ; éventuellement sauvegarder le contrôle ; fermer ; analyser après fermeture.

## 35. Critères du futur runtime

`PASS_E2_OPTION_BLOCKED` si 2.e est absente ou désactivée sans effet et la recharge est propre. `FAIL_E2_OPTION_AVAILABLE_WITHOUT_WEST_BENGAL` si elle est sélectionnable. `FAIL_E2_PREPARATION` si la topologie est incorrecte. `FAIL_E2_EVENT_EFFECT_LEAK` si un effet part sans sélection. `BLOCKED_E2_RELOAD_FAILED` si la base ne se recharge pas proprement.

## 36. Interprétation fonctionnelle possible

Si 2.e est bloquée, West Bengal gouverne effectivement l’accès malgré le noyau Bombay et la contradiction localisation/script est prouvée. Si elle reste disponible, il faudra rechercher un autre chemin UI/script. Aucun trigger n’est corrigé dans C1AC.

## 37. WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED

Le statut fonctionnel reste différé jusqu’au résultat E-2 et, si nécessaire, E-3. C1AC ne protège pas West Bengal, ne remplace pas le trigger et ne prépare pas E-3.

## 38. Risques restants

La présentation UI exacte peut être cachée ou désactivée ; la relocalisation automatique de la capitale BIC après perte de West Bengal doit être relevée ; l’agrégation COO doit être confirmée sur une nouvelle partie ; une mauvaise sélection d’option réelle contaminerait le test, d’où la recharge obligatoire.

## 39. Verdict

`READY_FOR_E2_AVAILABILITY_RUNTIME_TEST`.

## 40. Fichiers créés

Copie : quatre fichiers `zz_sepoy_functional_test_e2*`. Fork : ce rapport et `HOTFIX_5C2E4C1AC_E2_HARNESS_MANIFEST.csv`. Aucun autre fichier n’est créé par C1AC.

## 41. Confirmation Sepoy et journal

Le fichier Sepoy fork/copie reste byte-identique à 63 658 octets et au SHA attendu. `common/journal_entries/04_sepoy_mutiny.txt` reste byte-identique entre fork et copie. Aucun trigger ou gameplay réel n’est modifié.

## 42. Confirmation anciens harnais

Les quatre E1D, quatre E-1 et vingt-quatre autres harnais sont inchangés. Les scripts E1D conservent leurs tailles, SHA et BOM corrigés.

## 43. Confirmation Bengal/Madras/Bombay/Travancore/MARATH

Aucune protection Bengal, Madras ou Bombay, aucun fichier Travancore, aucun state East Bengal et aucune donnée MARATH ne sont modifiés. Seul le harnais jetable contient les deux mutations futures explicitement autorisées.

## 44. Confirmation docs/research/technology/

Le dossier non suivi `docs/research/technology/` reste intact et hors manifeste fonctionnel.

## 45. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est intact. Aucun apply, pop ou drop n’a été exécuté.
