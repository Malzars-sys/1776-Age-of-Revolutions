# HOTFIX-5C2E4C1Y — Audit médico-légal et préparation E1D

## 1. Résumé

L’échec radical C1X est confirmé, mais sa cause racine n’est pas prouvée. Le transfert territorial Bombay corrigé par C1W fonctionne; la seule pop hindoue ciblée reste toutefois à une variation de `-0.00001`, contre environ `-0.07585` attendu. Les contrôles réussis C1T et C1P démontrent que l’API et `large_radicals` fonctionnent dans la même installation. Un harnais différentiel E1D, sans transfert ni appel Sepoy, a donc été ajouté uniquement à la copie jetable. Verdict : **READY_FOR_E1_RADICAL_DIAGNOSTIC_RUNTIME**.

## 2. État Git

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `1f25f6a Document Sepoy Bombay radical failure`.
- Aucun fichier suivi n’était modifié au départ.
- Seule exception non suivie initiale : `docs/research/technology/`.
- Aucun processus Victoria 3, launcher ou dowser n’était actif.

## 3. Copie jetable

La copie avait exactement 972 fichiers et 28 fichiers `zz_sepoy*` avant C1Y, sans `.git` ni `remote_file_id`. Après ajout des quatre fichiers E1D, elle contient exactement 976 fichiers et 32 harnais. Le Sepoy fork/copie reste identique : 63 658 octets, SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`.

## 4. Preuves C1X

Les trois sauvegardes réglementaires ont été relues. Avant 2.e, state 482 appartient réellement à BIC, contient la province Bombay `x51F0A0`/39686 et la pop hindoue 14727. Le marqueur `zz_sepoy_test_e1_ready` est présent. Pré et post immédiat ont la même date profonde `1776.1.4.6`. `loyalists_and_radicals` passe de zéro à `-0.00001`; `radicals_increase` BIC de zéro à `0.00001`; la valeur reste identique au contrôle final `1776.1.6.6`. Les logs C1X ne contiennent aucune erreur ciblant E‑1, 2.e, Bombay, scope ou transfert.

## 5. Comparaison B-1/C-1/E-1

| Élément | B-1 | C-1 | E-1 | Différence significative | Hypothèse associée |
|---|---|---|---|---|---|
| Scope racine | `country_event`, BIC | identique | identique | non | H1 exclue comme différence racine |
| Transfert | aucun | FRA Madras → BIC | POR Bombay → BIC | oui | H2/H3 |
| Ordre | radicals → marker | owner → radicals → marker | owner → radicals → marker | C/E identiques | H2/H3, mais C réussit |
| Forme cible | boucle `every_scope_state` | `STATE_MADRAS.region_state:BIC` | `STATE_BOMBAY.region_state:BIC` | état seulement | H1/H8 |
| Religions | hindu + sunni | hindu + sunni | hindu + sunni | aucune | H4 |
| Valeur | `very_small_radicals` | identique | identique | aucune | H5 |
| Préparation | sans mutation | transfert français | transfert portugais | source différente | H2/H3 |
| Tooltip | West/East Bengal | FRA/BIC Madras | POR/BIC Bombay + West Bengal | E ajoute un contrôle | sans pouvoir explicatif direct |
| Marqueur | `b1_ready` | `c1_ready` | `e1_ready` | nom seulement | preuve d’exécution |
| Timing prévu | immédiat | immédiat après transfert | immédiat après transfert | C/E identiques | H2/H3 non démontrées |
| Encodage/accolades | conforme/équilibré | conforme/équilibré | conforme/équilibré | aucune | défaut syntaxique exclu |

Aucune différence statique ne rend compte simultanément de la baseline absente et de l’unique personne observée.

## 6. Comparaison 2.b/2.c/2.e

Les trois blocs utilisent `every_scope_state`, puis deux appels `add_radicals_in_state`, `hindu`, `sunni`, `large_radicals`, après les transferts et `clear_saved_scope`. Seul le filtre géographique diffère : 2.b = `region_north_india`; 2.c et 2.e = `region_south_india`. SHA-256 normalisés par suppression de l’indentation extérieure et LF : 2.b `7F76BAC958A54771B39F00B10EF15D9888DAEFD6AC6EB67620E6A12C2E3FD4CE`; 2.c et 2.e `4009B2CFF6707F53FD048BB1A0EC5275784840156935490C497AF40A317D8116`. La correction C1W ne touche aucun de ces appels.

## 7. Script values

La recherche a utilisé exclusivement `Get-ChildItem` et `Select-String`. `common/script_values/event_values.txt` vanilla définit `very_small_radicals = 0.01` ligne 1 et `large_radicals = 0.1` ligne 4. Aucune définition concurrente n’existe dans le fork, la copie ou les autres sources hotfix locales. Le chargement du mod réutilise donc les valeurs vanilla; aucun override ni collision n’est établi.

## 8. Exemples vanilla

La vanilla emploie `add_radicals_in_state` dans l’historique global, les scripted effects Sepoy, les scripted buttons et plusieurs événements. Les exemples couvrent les filtres religieux, les states sauvegardés, les split states et des appels après changements territoriaux. Aucun exemple ne prouve une interdiction visant une state portion récemment transférée ou une cible religieuse composée d’une seule pop.

## 9. Analyse state Bombay

La portion BIC est bien le state objet 482 avant et après 2.e, non vide, rattaché à BIC et affiché non incorporé. Son propriétaire et sa population ne changent pas entre les deux sauvegardes de même date. L’association de subsistance de la pop cible est le workplace 4159. La donnée de homeland n’est pas sérialisée comme attribut direct de pop; aucune divergence de homeland n’est donc affirmée.

## 10. Analyse pop 14727

| Champ | Valeur pré | Valeur post immédiate | Valeur finale |
|---|---:|---:|---:|
| Type/culture/religion | peasants / 285 (Marathi) / hindu | identique | identique |
| Workforce/dependents/total | 18 963 / 56 889 / 75 852 | identique | identique |
| Workplace | 4159 | 4159 | 4159 |
| Acceptation/discrimination | 0 / `violent_hostility` | identique | identique |
| Political strength | 853 | 853 | 853 |
| Literate/wealth | 2 275 / 8 | identique | identique |
| `loyalists_and_radicals` | 0 (champ absent) | `-0.00001` | `-0.00001` |

La pop existe avant/après le transfert et 2.e. Aucun attribut sérialisé relevé ne change au moment de l’échec.

## 11. Comparaison Madras

Madras 473 contient six pops hindoues totalisant 182 284 personnes et une pop sunnite de 20 098. Types : laborers, peasants, aristocrats, clergymen et slaves; workplaces 2615, 2616, 4142, 4143 ou absent pour la petite pop esclave. Toutes ont acceptation 0/`violent_hostility`. La somme ciblée passe de `-0.02425` à `-0.24683`, delta `-0.22258`; `radicals_increase` BIC augmente exactement de `+0.22258`. C’est un contrôle positif de la même API après transfert.

## 12. Comparaison Bengal

West/East Bengal contiennent 89 pops cibles non nulles : 76 hindoues (19 063 323 personnes) et 13 sunnites (19 230 242), total 38 293 565. West Bengal : hindu 13 071 323, sunni 3 822 116; East Bengal : hindu 5 992 000, sunni 15 408 126. Types, workplaces, niveaux d’acceptation, richesse et force politique sont variés. La somme passe de `-3.83315` à `-42.13557`, delta `-38.30242`, exactement reproduit dans `radicals_increase` BIC.

| Champ | Bombay échec | Madras succès | Bengal succès | Différence candidate | Capacité explicative |
|---|---|---|---|---|---|
| Nombre de pops cibles | 1 | 7 | 89 | oui | H8 plausible |
| Population ciblée | 75 852 | 202 382 | 38 293 565 | oui | seuil/arrondi à tester |
| Religion | hindu seulement | hindu + sunni | hindu + sunni | partielle | H4 exclue pour hindu |
| Acceptation Bombay | 0/violent hostility | mêmes valeurs présentes | valeurs multiples | non discriminante | faible |
| Transfert juste avant baseline | oui | oui | non | C réussit | H2/H3 affaiblies |
| Baseline 1 % | absente | présente | présente | anomalie centrale | E1D small direct |
| Large 10 % | ~1 personne | succès quantitatif | succès quantitatif | anomalie centrale | E1D large direct |

## 13. Preuve d’exécution

Le marqueur E‑1 et le state/pop attendus prouvent que la branche de préparation a atteint au moins `set_variable`. La conservation territoriale et les changements mondiaux prouvent que 2.e a été choisie. Les dates identiques excluent un tick quotidien entre pré et post immédiat. Cela ne prouve cependant pas que chacun des deux appels radical a été appliqué intégralement à Bombay.

## 14. Calcul du signal d’une personne

Pour 75 852 personnes, `large_radicals = 0.1` implique environ 7 585,2 personnes et une valeur agrégée attendue proche de `0.075852`. L’observé `0.00001` correspond, sur l’échelle profonde constatée, à `75 852 × 0.00001 = 0.75852`, donc environ une personne après quantification. Le ratio observé/attendu est `0.00001 / 0.1 = 0.0001`, soit 1/10 000 de l’effet demandé. Ce n’est pas une simple tolérance autour de 10 %. La date identique rend une cause organique quotidienne improbable; le signal est compatible avec un plancher/arrondi ou une exécution partielle, sans départager les deux.

## 15. Hypothèses H1–H12

| H | Preuves pour | Preuves contre | Statut | Test discriminant minimal |
|---|---|---|---|---|
| H1 scope `region_state` incorrect | Bombay seul échoue | scope résout state/pop; même forme C1 réussie | UNLIKELY | appels directs E1D |
| H2 trop tôt après transfert | baseline E1 absente | C1 réussit dans le même ordre | PLAUSIBLE | base stabilisée deux ticks |
| H3 cache pops non stabilisé | transfert récent et baseline absente | pop sérialisée avant 2.e; attente C1X rapportée | PLAUSIBLE | small direct après stabilisation |
| H4 religion non ciblée | aucune sunnite | pop 14727 est hindu; hindu réussit ailleurs | EXCLUDED | contrôle déjà fourni |
| H5 script value mal résolue | amplitude anormale | définition unique; C1P/C1T réussissent | EXCLUDED | West Bengal E1D contrôle chargement |
| H6 pop inéligible par attribut | Bombay unique/hostile/non incorporé | même pop avait une baseline dans C1V; attributs ordinaires | PLAUSIBLE | direct small/large sur 14727 |
| H7 state non incorporé | UI Bombay non incorporé | API agit sur d’autres states comparables; pas de règle trouvée | UNLIKELY | comparer contrôle direct |
| H8 une seule pop hindoue | différence nette B/C/E | 75 852 dépasse tout seuil d’une personne | PLAUSIBLE | small puis large Bombay |
| H9 ordre propre à 2.e | large 2.e échoue | n’explique pas la baseline E1 absente | UNLIKELY | direct vs 2.e depuis même base |
| H10 changement organique | signal minuscule | même date profonde, aucun tick | UNLIKELY | répétition même-date |
| H11 décalage date opérateur | noms de fichiers au 3 janvier | dates profondes vérifiées | EXCLUDED | aucune action supplémentaire |
| H12 erreur silencieuse moteur | absence d’erreur explicite possible | aucune preuve positive | UNPROVEN | E1D + logs frais |

## 16. Causes exclues

Sont exclues par preuve disponible : mauvaise religion (H4), collision ou mauvaise résolution globale des script values (H5), décalage de date opérateur pour le pré/post immédiat (H11), erreur d’accolades/encodage des harnais, et modification des appels radicaux par C1W.

## 17. Causes plausibles

Restent plausibles sans être prouvées : timing juste après transfert (H2), stabilisation/cache de pops (H3), éligibilité particulière de la pop 14727 (H6), et cas d’une seule pop hindoue (H8). H12 reste non prouvée, non promue comme explication.

## 18. Cause principale éventuelle

Aucune cause principale n’est établie sans ambiguïté. La meilleure famille explicative est « cible Bombay/pop unique versus moment d’exécution », précisément ce que sépare E1D. Le fait que C1 réussisse empêche de déclarer le transfert immédiat cause racine.

## 19. Pourquoi aucune correction gameplay n’est faite

Modifier `large_radicals`, le scope 2.e, la pop ou l’ordre des transferts maintenant risquerait de masquer le défaut et de casser les contrôles réussis. C1Y ne modifie donc aucune valeur, logique, protection territoriale, trigger West Bengal ou événement principal.

## 20. Harnais E1D

E1D est un namespace nouveau `zz_sepoy_test_e1d`, une décision `zz_sepoy_test_e1d_open` et un événement `zz_sepoy_test_e1d.1`. Il exige joueur BIC, marqueur E‑1, portions BIC réelles/non vides de Bombay et West Bengal, et une pop hindoue dans chaque cible. Il ne transfère rien et n’ouvre jamais `sepoy_mutiny_events.2`.

## 21. Options diagnostiques

L’événement possède exactement cinq options manuelles : SMALL_BOMBAY (`0.01`), LARGE_BOMBAY (`0.1`, après small), SMALL_WEST_BENGAL_CONTROL (`0.01`), LARGE_WEST_BENGAL_CONTROL (`0.1`, après small), CANCEL sans effet. Quatre marqueurs distincts empêchent la répétition accidentelle des effets.

## 22. Contrôles West Bengal

West Bengal n’est utilisé que comme contrôle positif direct de la même API. E1D n’y change ni propriétaire, ni diplomatie, ni trigger, ni territoire. L’ajout de radicaux lors de la future branche de contrôle est la seule mutation autorisée.

## 23. Localisations et tooltips

Les localisations anglaise et française décrivent les cinq branches, avertissent de recharger la base entre Bombay, Bengal et 2.e, emploient « diagnostic jetable » et ne prétendent pas que le gameplay est corrigé. Les exigences complexes sont de vrais `custom_tooltip` contenant des triggers évalués.

## 24. Validation BOM/LF

Les deux fichiers YML ont un BOM UTF‑8 et uniquement des LF. Toutes les clés référencées sont définies dans les deux langues. Scripts : accolades équilibrées. Contrôles : une décision, un événement, cinq options, quatre appels radicaux, zéro `set_state_owner`, zéro appel Sepoy, quatre affectations de marqueurs, zéro hasard et zéro option automatique.

## 25. Résumé du manifeste

Le manifeste C1Y contient 41 lignes de données : quatre E1D, quatre E‑1, vingt-quatre anciens harnais, deux Sepoy, deux journaux, trois descripteurs/marqueur et deux livrables C1Y. Il enregistre tailles, SHA-256, encodage, cible, valeur et compte des mutations.

## 26. Plan runtime à une ouverture

Une seule ouverture Victoria 3, une seule nouvelle partie BIC, aucune session GBR, aucune fermeture intermédiaire, deux rechargements maximum, une fermeture finale :

1. Démarrer BIC; exécuter la préparation E‑1; attendre au moins deux ticks complets; confirmer Bombay et West Bengal BIC; sauvegarder l’immuable `E1D_BASE`.
2. Branche A : SMALL_BOMBAY; sauvegarde immédiate; LARGE_BOMBAY; sauvegarde immédiate puis après un tick.
3. Recharger `E1D_BASE` sans quitter le jeu (rechargement 1).
4. Branche B : SMALL_WEST_BENGAL_CONTROL; sauvegarde immédiate; LARGE_WEST_BENGAL_CONTROL; sauvegarde immédiate puis après un tick.
5. Recharger `E1D_BASE` sans quitter le jeu (rechargement 2).
6. Branche C : ouvrir l’événement réel avec E‑1, choisir uniquement 2.e, sauvegarder immédiatement puis après un tick.
7. Fermer Victoria 3 une seule fois; seulement ensuite analyser sauvegardes/logs sur copies Rakaly et supprimer les temporaires.

## 27. Matrice d’interprétation

| Résultat | Interprétation |
|---|---|
| Bengal direct fonctionne, Bombay direct échoue | cible Bombay ou éligibilité de la pop |
| Bombay direct fonctionne, 2.e échoue | chemin/ordre propre à 2.e |
| small Bombay échoue, large fonctionne | seuil, arrondi ou valeur minimale |
| small et large Bombay fonctionnent après stabilisation | préparation E‑1 trop précoce/timing |
| Bengal et Bombay directs échouent | harnais, chargement ou script values à réauditer |
| 2.e fonctionne | C1X non reproductible ou dépendant du timing |

## 28. Verdict

**READY_FOR_E1_RADICAL_DIAGNOSTIC_RUNTIME**.

## 29. Fichiers créés

Copie : les quatre fichiers `zz_sepoy_radical_diagnostic_e1d*`. Fork : ce rapport et `HOTFIX_5C2E4C1Y_E1_RADICAL_DIAGNOSTIC_MANIFEST.csv`. Aucun autre fichier C1Y n’a été créé.

## 30. Confirmation gameplay inchangé

`events/india_events/sepoy_mutiny_events.txt`, le journal Sepoy, les protections Bengal/Madras/Bombay, les triggers, MARATH/SAT/KHP/Travancore, les sauvegardes originales et les 28 anciens harnais sont inchangés.

## 31. WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED

**WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED** demeure en vigueur. La perte de West Bengal sous 2.e n’est ni corrigée ni interprétée ici comme un second noyau intentionnel.

## 32. Confirmation docs/research/technology/

Le répertoire préexistant `docs/research/technology/` reste non suivi et entièrement hors périmètre; aucun de ses fichiers n’a été modifié.

## 33. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est intact. Aucun `stash apply`, `pop`, `drop` ou commit automatique n’a été exécuté.
