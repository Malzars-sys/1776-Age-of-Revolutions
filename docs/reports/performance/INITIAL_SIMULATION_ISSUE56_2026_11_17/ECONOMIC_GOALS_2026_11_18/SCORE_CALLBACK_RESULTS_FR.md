# Douze scores de construction — série contrôlée terminée le 19 novembre

**Aucun gain de performance observé.** Retirer les douze blocs moddés de priorité de construction ne résout pas le ralentissement initial dans cette série. Cela n'exonère pas le calcul natif de rentabilité, l'extension des bâtiments, l'investissement ou la sélection des PM, qui restent actifs.

## Traitement et vérification native

Le pack externe remplace seulement douze blocs `ai_value` par leur propre base, dans neuf fichiers de bâtiments. Toutes les autres données restent présentes. Aucun contrôleur ni objectif natif n'est désactivé ; les routines HRE et régionales restent normales. Le diagnostic peut changer les préférences de construction : il ne constitue pas une optimisation équivalente à intégrer.

Les deux comparaisons de ressources effectivement chargées par le moteur confirment **exactement neuf fichiers modifiés sur 7 412 chemins virtuels**, sans ajout ni retrait. Les autres ressources, dont l'interface de mesure commune, sont identiques. Preuves : `SCORC1_RUNTIME_SCORE_PROOF.json` et `SCORC2_RUNTIME_SCORE_PROOF.json` dans le laboratoire.

La source initiale commune conserve le même monde France du 1er janvier 1776, avec la vitesse de chargement commune réglée à 5. Son intégrité est vérifiée avant et après les essais. **Chacune des quatre autosaves natives du 1er avril confirme 646 contrôleurs actifs, leurs objectifs attendus et aucun contrôleur ajouté ou manquant.** Les contrôles sont des preuves de source préparée et POST natif ; aucune PRE manuelle n'est inventée.

## Mesures réellement exécutées

Ordre : diagnostic → témoin → témoin → diagnostic, soit B–A–A–B si A désigne le comportement normal. Secondes cumulées, horodatages natifs DAY du 2 janvier au 27 février :

| Passage | Condition | 14 j | 28 j | 56 j | CPU moyen du processus sur 56 j, % des 16 processeurs logiques |
|---|---|---:|---:|---:|---:|
| SCORC1 | Douze scores remplacés par leur base | 30 | 56 | 100 | 22,31 % |
| ECNC1 | Témoin normal | 30 | 55 | 96 | 22,13 % |
| ECNC2 | Témoin normal répété | 27 | 52 | 94 | 21,24 % |
| SCORC2 | Diagnostic répété | 31 | 59 | 102 | 22,17 % |

Les diagnostics sont plus lents dans les deux paires. Moyennes descriptives : témoins 95 s, diagnostics 101 s, soit +6,3 % de durée. **Deux processus par condition ne prouvent pas une aggravation intrinsèque**, et aucun test statistique artificiel ne traite les trois fenêtres imbriquées comme trois répétitions indépendantes. Ces prises ne justifient surtout aucun gain à annoncer.

La résolution de la différence des horodatages est inférieure à une seconde d'erreur absolue. Les autres applications, fréquences, conditions thermiques et pauses physiques ne sont pas totalement contrôlées. CPU comprend aussi le rendu et ne donne pas un temps exclusif de fonction. Aucun FPS n'est mesuré.

## Préparation, affichage et comparabilité

Même Steam 1.15.1 sans DLC de gameplay, même réglage initial `9a759fceadc82095774b75030159250f67b51b488d192d0239f96f42a27e26c4`. Les quatre signatures DLC natives sont identiques. L'installation 1.15.0 avec DLC reste distincte et en lecture seule.

Fenêtre 1600×900 exclusivement sur l'écran secondaire GAOMON, panoramique par bord d'écran désactivé. L'interface commune du laboratoire déplace ses seuls boutons et déclare une animation de 16 pixels visible uniquement en pause. L'ancien overlay reste intact. Les captures répétées vérifient la date initiale, la vitesse et une vue d'Europe occidentale sans panneau d'État supplémentaire. Voir [PROTOCOL_STABLE_FR.md](PROTOCOL_STABLE_FR.md) et les reçus `*_SOURCE_UI.json` / `*_VIEW_COMPARABILITY.json`.

La préparation en pause n'est pas identique à la seconde près : ses durées réelles sont conservées dans ces reçus. Dans la première paire, les vingt dernières secondes avant reprise présentent environ 3,50 % et 3,79 % de CPU machine. C'est de la CPU de préparation, comprenant le rendu, **pas une mesure de débit ni une attribution de coût**. Elle ne prouve pas l'absence de tout cache ou travail différé.

Après le départ, aucune nouvelle entrée de l'agent n'est enregistrée. Les événements visibles ne sont pas cliqués. La sauvegarde trimestrielle et les copies interviennent après les 56 jours. Le lanceur ferme uniquement son propre processus après les preuves et le vidage des journaux ; EXIT −1 documente cette fermeture contrôlée.

## POST à date identique

Dans **chacune des deux paires**, la comparaison des sauvegardes natives au même 1er avril trouve **83 sections strictement identiques ; seul `local_date_time` diffère**, sans section ajoutée ou retirée. Reçus : `ECNC1_SCORC1_MATCHED_POST_SECTIONS.json` et `ECNC2_SCORC2_MATCHED_POST_SECTIONS.json`. La même observation existe dans l'ancienne paire G, dont les temps restent confondus par une différence de panneau.

Cela décrit l'état sérialisé à cette date. Ce n'est pas la preuve d'une identité des décisions intermédiaires, d'une fréquence d'appel des callbacks, ni d'une équivalence dans d'autres campagnes ou plus tard. Définition chargée, fonction exécutée et coût exclusif sont des preuves différentes. Un profil d'appels effectifs reste utile pour distinguer un score rarement sollicité d'un score peu coûteux.

## Conséquence pour l'enquête

Cette couche moddée de priorité perd du soutien comme explication dominante du surcoût initial. Le retrait des objectifs d'extension dans les sauvegardes reste invalidé par leur recréation : **l'extension native n'est pas innocentée**. Le prochain contrôle informatif doit porter sur une catégorie native persistante ou sur un profil exploitable des appels réels, plutôt que sur de nouveaux retraits de blocs qui se régénèrent.

Le pack demeure externe au dépôt et n'est pas intégré au mod principal. Aucun changement de fréquence IA, pays, POP, structure économique ou contenu historique n'est proposé comme correctif validé. Les anciennes prises SCORQ1 et SCORG1 restent séparées, avec leurs limites ; elles ne sont pas agrégées aux C.

Une collecte native ultérieure a effectivement observé huit de ces douze emplacements dans le runtime normal, avec des temps rapportés faibles. Les quatre absences ne sont pas assimilées à des coûts nuls. Voir [SCRIPT_PROFILE_FR.md](SCRIPT_PROFILE_FR.md) pour les appels, unités et limites ; cette collecte n'est pas agrégée aux chronométrages ci-dessus.
