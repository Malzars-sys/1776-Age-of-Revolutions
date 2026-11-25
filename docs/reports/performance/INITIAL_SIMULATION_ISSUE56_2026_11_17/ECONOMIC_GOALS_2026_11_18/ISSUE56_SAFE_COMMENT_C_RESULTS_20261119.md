### Point d'étape expérimental — 19 novembre 2026

**Aucune optimisation préservant le gameplay n'est validée.** Les mesures suivantes sont acquises ; les répétitions encore en cours ne sont pas comptées comme terminées.

#### Signal des contrôleurs IA

Durées réelles cumulées pour les mêmes 14 / 28 / 56 jours du monde initial de 1776 :

| Passage | Condition | 14 j | 28 j | 56 j |
|---|---|---:|---:|---:|
| AI_OFF3R | Tous contrôleurs désactivés | 8 s | 15 s | 30 s |
| AI_ON3 | IA normale, premier lot | 46 s | 88 s | 155 s |
| AI_DEC1 | Décentralisés seuls désactivés | 33 s | 65 s | 120 s |
| AI_OTHER1 | Les 400 autres seuls désactivés | 7 s | 15 s | 30 s |
| AI_DEC2 | Répétition décentralisés désactivés | 35 s | 68 s | 123 s |
| AI_ON4R | IA normale, nouveau lot | 39 s | 72 s | 122 s |
| AI_OFF4 | Tous désactivés, ordre inversé | 7 s | 15 s | 30 s |
| ECN1 | Témoin économique ultérieur | 35 s | 69 s | 124 s |

Les états ont été vérifiés dans les sauvegardes natives. AI_DEC1 perd un contrôleur avant son POST de juillet ; la cause reste inconnue, et la répétition AI_DEC2 conserve tous les contrôleurs. AI_ON4 interrompu n'a pas de résultat sur 56 jours.

L'inventaire initial est désormais complet : **246 décentralisés et 400 autres, soit 646**. Les deux contrôleurs précédemment non classés sont des décentralisés possédant chacun un État, avec statistique de population nulle ; l'absence physique de tout objet POP n'est pas établie.

La paire 122/30 reproduit le contraste global en ordre inversé. **Les contrastes ne sont pas additifs.** L'écart entre témoins de 155 et 122 secondes interdit de mélanger arbitrairement les lots. Le surcoût est fortement associé aux 400 contrôleurs, mais leur fonction responsable reste inconnue.

#### Extension des bâtiments : ablation invalidée

EXB1 retire uniquement les 400 objectifs sérialisés `expand_production_buildings`. La PRE native confirme leur absence, les 646 contrôleurs actifs et les autres objectifs conservés. **Les 400 objectifs sont revenus dans la POST de mars.** Le chronométrage brut 39/75/130 secondes ne peut donc pas mesurer leur désactivation.

Le contrôle court EXB3 les retrouve déjà le **4 janvier 1776 au soir**. Leur recréation est établie, pas son instant exact ni son mécanisme. Le retrait des objectifs de sélection des PM est préparé mais non exécuté ; il n'innocente pas cette charge.

#### Nouvelle isolation : priorités de construction moddés

Une variante diagnostique remplace seulement **12 blocs de score `ai_value` dans neuf fichiers** par leurs constantes de base. Tous les contrôleurs, objectifs natifs, PM, pays, POP, bâtiments, marchés et routines HRE/régionales sont conservés. Le moteur confirme que seuls les neuf fichiers attendus diffèrent dans ses ressources chargées.

Cette variante peut changer les choix de construction : **ce n'est pas une optimisation équivalente à intégrer**.

- SCORQ1 : 52/101/174 secondes, traitement conservé au POST ; aucun témoin contemporain terminé, donc pas de conclusion de performance.
- Nouveau témoin ECNG1 : **35/67/119 secondes**.
- SCORG1 : **29/57/103 secondes**, 646 contrôleurs actifs et objectifs intacts au POST natif ; surcharges effectivement chargées. **Une différence de panneau/vue pendant la mesure est observée. Cette comparaison est marquée comme confondue et ne valide pas un gain causal.**

**La série contemporaine avec vue stabilisée est maintenant terminée**, dans l'ordre diagnostic → témoin → témoin → diagnostic :

| Passage | Condition | 14 j | 28 j | 56 j |
|---|---|---:|---:|---:|
| SCORC1 | Douze scores remplacés par leur base | 30 s | 56 s | 100 s |
| ECNC1 | Témoin normal | 30 s | 55 s | 96 s |
| ECNC2 | Témoin normal répété | 27 s | 52 s | 94 s |
| SCORC2 | Diagnostic répété | 31 s | 59 s | 102 s |

Les quatre passages conservent 646 contrôleurs actifs et leurs objectifs dans les autosaves natives d'avril. Les deux paires confirment les neuf surcharges prévues, sans autre différence de ressources virtuelles. **Aucun gain observé.** Les diagnostics sont plus lents dans ces prises ; deux processus par condition et la variabilité ne prouvent pas une aggravation intrinsèque. Les 14/28/56 jours sont des fenêtres imbriquées.

Dans chacune des deux paires, les POST du même 1er avril ont **83 sections sérialisées strictement identiques ; seul l'horodatage local diffère**. Cela ne prouve ni l'identité des décisions intermédiaires, ni l'exécution de chaque callback, ni l'équivalence dans d'autres campagnes. Ces douze scores ne paraissent pas expliquer l'essentiel du surcoût initial. L'extension native, la rentabilité, l'investissement et les PM restent à isoler.

Un contrôle global IA contemporain et la paire vanilla inversée sont en cours ; leurs résultats ne sont pas anticipés.

#### Référence vanilla terminée

Même instrumentation entre ses deux conditions, monde standard de 1836 :

| Condition | 14 j | 28 j | 56 j |
|---|---:|---:|---:|
| IA normale | 13 s | 23 s | 45 s |
| Tous contrôleurs désactivés | 10 s | 18 s | 34 s |

Les 449 contrôleurs initiaux sont retrouvés. Un nouveau pays apparaît dans le passage normal : les 450 contrôleurs présents sont actifs ; les 449 du passage OFF sont inactifs. Cette évolution est explicitement prise en compte.

Cette seule paire est exploratoire. Le monde, la date, l'économie, les pays et la vue diffèrent de 1776 : elle ne mesure pas directement la pénalité du mod. Une paire inversée distincte est préparée.

#### Interprétation et limites

La baisse des profits négatifs, la réorganisation des objets POP et des investissements autonomes échoués existent aussi dans des mondes rapides avec les flags IA désactivés. Les snapshots ont des dates/branches différentes : aucune corrélation n'est présentée comme cause. Les stratégies sérialisées peuvent rester identiques tout en étant réévaluées.

Les temps utilisent les horodatages **natifs** des DAY, jamais l'arrivée tamponnée des journaux. Les 14/28/56 jours sont imbriqués, pas trois répétitions indépendantes. Chargement, menus, sauvegarde et copie des preuves sont exclus. La nouvelle méthode vérifie la source préparée puis une autosave native postérieure aux fenêtres ; elle ne prétend pas disposer d'une PRE native manuelle. Aucun FPS ni coût exclusif de fonction n'est revendiqué.

Le profilage moteur disponible reste partiel ; aucune restriction de sécurité n'a été contournée. Les explications « travail nécessaire », « réévaluations redondantes », « décisions natives face à l'économie initiale » et « état persistant » restent à discriminer.

Les expériences demeurent isolées. Aucun contenu historique ni population supprimé, aucune modification expérimentale intégrée au mod principal, aucun commit/push/merge. Les versions courantes des fichiers normaux et les travaux existants sont conservés sans restauration aveugle. Les rapports détaillés et preuves techniques restent locaux ; l'audit final sera ajouté après les répétitions.

**Enquête ouverte ; aucun correctif de production validé.**
