# SC5-PRUSSIAN-WEST — passe achevée, correspondance territoriale bloquée

5 novembre 2026. Cible : **1er janvier 1776**. Autorisation : poursuite de la priorité Prusse, réponse « Ok, vas-y », puis « fini ». Périmètre : Gueldre prussienne, Clèves, Mark et Ravensberg ; conservation de Minden, Lingen et Tecklenburg. Aucune variante silésienne ni Bavière commencée.

**Résultat : aucune correction fonctionnelle installée. `SC5-PRUSSIAN-WEST` passe de `NOT_STARTED` à `BLOCKED`, P1.** Aucun reçu humain, aucun point supplémentaire. Progression calculée avant/après : **93/235, 39,57 %, 32/81**. Le blocage porte sur la correspondance avec les cellules du jeu, pas sur l'existence des possessions prussiennes.

## Ce qui a été établi

- Les acquis de Clèves, Mark, Moers et la part prussienne de Gueldre doivent être conservés ; la carte ne doit pas devenir celle des acquisitions de 1815. L'hommage des états de la part prussienne du Haut-Quartier de Gueldre en septembre 1713 est documenté par une source primaire publiée par le projet archivistique du LVR. Cela n'attribue ni toute la Gueldre ni toute une province bitmap à PRU.
- La **carte de Ravensberg de Schloenbach, 1772**, a été obtenue et lue, avec sa liste des deux villes immédiates et des quatre Ämter, ainsi que les limites des voisins Osnabrück, Münster, Lippe et Rietberg. Elle apporte une preuve territoriale nouvelle, sans résoudre à elle seule sa position exacte sur la carte du jeu.
- La feuille **Cleve, Geldern, Meurs und Mark**, Berne MUE Ryh **5106:3 B**, a été obtenue par son manifeste IIIF et lue. La notice la date de **1793** ; la feuille se dit réduite d'après Sotzmann. Elle distingue Clèves, Gueldre, Moers, Mark et les territoires voisins. Sa date postérieure impose une vérification de continuité avant toute application à 1776.
- Pour Jülich–Berg, la carte de Vaugondy de 1753, dans l'exemplaire de 1777 déjà conservé, est réutilisée. Les Archives municipales de Düsseldorf confirment le gouvernement du duc/électeur palatin Charles-Théodore avant la succession bavaroise de 1777. Aucune souveraineté nouvelle n'est créée.

Références, images réellement examinées et limites : [SOURCES.md](SOURCES.md). Les anciens rapports et mauvais raccords restent intacts.

## Diagnostic décisif : le prétendu correctif de Berg n'est pas démontré

Un intérieur conservateur du duché de Berg a été dessiné sur la carte de Vaugondy. Il ne représente pas tout son contour et laisse notamment Gimborn/Homburg et les franges de Windeck hors proposition. Le même dessin a ensuite été confronté aux **deux modèles natifs déjà présents**, sans les modifier : axes géographiques de MAP2M/R5 et Miller affine du prototype MAP2L.

| Hypothèse de positionnement | Attribution actuelle de l'intérieur projeté | Correction PRU→KPF proposée par cette hypothèse |
| --- | --- | --- |
| Axes géographiques R5 | **151 cellules déjà sous KPF** | **0 cellule** |
| Miller affine MAP2L | 62 cellules KPF et 76 PRU | **39 cellules PRU éligibles** dans les deux régions techniques retenues ; 37 autres cellules PRU hors de ce périmètre de transfert |

Les positions diffèrent d'environ dix cellules en longitude dans ce secteur. Les deux modèles sont empiriques et utilisés ici hors de leur domaine d'ajustement. Leurs anciennes statistiques de contrôle ne constituent pas une borne d'erreur locale. **Les 39 cellules ne sont donc pas une régression prussienne indépendamment démontrée.** Avec l'autre hypothèse, le noyau examiné est déjà palatin. Aucun noyau à transférer depuis PRU n'est commun aux deux lectures.

Il serait abusif de sélectionner le modèle uniquement parce qu'il produit une correction, ou d'agrandir le dessin pour obtenir un transfert. Aucune translation arbitraire, modification des anciens modèles, restauration de baseline ou migration économique n'est effectuée. L'absence de transfert commun ne démontre pas non plus que toutes les frontières actuelles sont conformes.

[TRACING.json](TRACING.json) conserve les points lus, le dessin, les matrices et leurs limites ; [BERG_HYPOTHESES.json](BERG_HYPOTHESES.json) conserve les **39 coordonnées candidates non installées** et la distribution actuelle des propriétaires. [Illustration des hypothèses](HYPOTHESES_NOT_INSTALLED.png), [lecture sur la source](BERG_SOURCE_REVIEW.jpg).

La première commande de génération s'est arrêtée avec l'assertion `No defensible common interior`, **avant toute production ou installation de candidat fonctionnel**. La version documentaire suivante exporte le résultat `NO_GO_NATIVE_CORRESPONDENCE` au lieu d'interrompre l'analyse ; elle ne transforme pas ce refus en réussite d'une correction. [Résultats bruts des exécutions](ANALYSIS_RUNS.json).

## État des quatre ensembles

| Ensemble | Acquis de la passe | Reste à résoudre |
| --- | --- | --- |
| Clèves et Mark | Source distincte lue ; acquis prussiens conservés ; inventaire courant conservé | Raccord des grandes bordures avec les portions voisines ; aucune certification cadastrale |
| Gueldre prussienne | Part prussienne de 1713 confirmée ; carte postérieure distinguant les ensembles obtenue | Traduction des parts prussienne, néerlandaise, autrichienne et de Jülich dans les RGB ; ne pas attribuer toute une province depuis un nom de ville |
| Ravensberg | Carte primaire **1772** réellement lue, voisins et subdivisions identifiés | Positionnement défendable face aux anciens repères divergents, distinction Herford ville/abbaye et maintien des noyaux voisins |
| Interface rhénane de Berg | Proposition conservatrice chiffrée ; absence de correction indépendante démontrée dans ce noyau | Résoudre la divergence de positionnement avant une extension ; le reste du Rhin méridional n'est pas certifié |

Les diagnostics de noms et coordonnées de villes restent des **hypothèses de position**, jamais une preuve qu'un pays possède réellement cette ville en jeu. L'inventaire des propriétaires bitmap est une donnée technique actuelle, pas une preuve historique. Les données démographiques et économiques ne sont pas recalibrées sans transfert établi.

## Conservation et contrôles

La baseline de cette passe est distincte et immuable. Les fichiers fonctionnels, la carte, les terrains, populations, bâtiments, PM, unités et technologies sont identiques à cette baseline. Les trois livraisons prussiennes précédentes, la comparaison silésienne et les dossiers anciens Minden/Rhin–Westphalie sont conservés avec leurs empreintes. Aucun fichier vanilla ni index Git n'a été modifié.

[FINAL_CHECKS.json](FINAL_CHECKS.json) donne les contrôles de conservation réellement exécutés ; [TEST_RESULTS.json](TEST_RESULTS.json) et son journal donnent la nouvelle exécution des tests canoniques. Les erreurs de références globales héritées restent archivées ; une suite du suivi réussie ne prouve ni les frontières ni le chargement du moteur.

Résultats : **10/10 contrôles de conservation**, dont **2 859 fichiers fonctionnels identiques** ; **11/11 contrôles finaux**, validateur canonique `PASS` ; **28 tests canoniques exécutés, 27 réussis, 1 ignoré** (ancienne protection de non-écriture propre à l'initialisation). `git diff --check` retourne 0, avec seulement des avertissements LF/CRLF sur les documents suivis.

Une première vérification finale a échoué parce que son prédicat sélectionnait la première ancienne fiche plutôt que `SC5-PRUSSIAN-WEST`. Le prédicat a été corrigé pour sélectionner explicitement les deux versions de cette tâche ; aucune donnée de jeu ou de suivi n'a été modifiée pour faire passer ce contrôle. L'échec brut reste dans [INITIAL_FINAL_CHECKS.json](INITIAL_FINAL_CHECKS.json), avec [l'explication de la correction](VALIDATOR_CORRECTION.json). Le résultat final ci-dessus provient de la nouvelle exécution corrigée.

## Suite préparée

**Aucun nouveau protocole moteur pour cette passe sans modification fonctionnelle.** Le [protocole groupé des installations prussiennes précédentes](../PRUSSIA_POLAND_2026_11_05/PLAYER_TEST_PROTOCOL.md) reste à effectuer ; aucune confirmation supplémentaire n'est présumée.

Pour poursuivre l'ouest, il faut une correspondance locale mieux étayée avec des repères physiques indépendants ou un arbitrage explicite sur une approximation politique B concrète. Les 39 cellules sont une hypothèse de comparaison, **pas une option recommandée pour installation immédiate**. Ne pas relancer automatiquement les anciens ajustements, ni transformer ce maintien temporaire en `NOT_APPLICABLE_VERIFIED` ou `DEFERRED_APPROVED`.

La prochaine action immédiate demeure le test joueur groupé prussien déjà préparé. La priorité géographique reste la Prusse occidentale ; aucun deuxième territoire, micro-État ou lot bavarois n'est commencé.
