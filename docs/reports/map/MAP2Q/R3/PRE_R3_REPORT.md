# MAP-2Q — Eutin, prince-évêché de Lübeck

## Livraison partielle, non validée en jeu

Un pays distinct **HLB**, protestant et épiscopal, est installé dans `STATE_SCHLESWIG_HOLSTEIN` (66). La ville de Lübeck conserve **LUB**. L'union personnelle native **OLD → HLB** a été expressément choisie par le joueur ; les territoires et membres impériaux ne sont pas fusionnés.

**État courant après R2 : 7 600 habitants installés**, estimation historique approximative acceptée par le joueur, fourchette de travail 6 500–9 000, pas recensement exact. Voir la [méthode et le bilan R2](CONTINUATION_R2/POPULATION_METHODOLOGY.md). Les 11 325 de la phase initiale sont remplacés, sans compensation ailleurs : monde 835 804 980 → 835 801 255. Schwartau et les possessions capitulaires restent ouverts ; ne pas annoncer tout MAP-2Q terminé. Aucun test moteur de R2 n'est attesté.

## Modifications réellement appliquées

- **31 cellules** transférées au noyau d'Eutin : **19 LUB → HLB**, **12 HOL → HLB**.
- Deux provinces HLB : `xEDB202` (19 cellules) et `xEDB203` (12 cellules).
- Deux nouveaux RGB supplémentaires conservent les fragments LUB : `xEDB200` (4 cellules), `xEDB201` (1 cellule). Ce sont des subdivisions techniques, pas deux nouveaux pays.
- **36 cellules recolorées**, dont 31 changent de souveraineté. Aucun State_ID nouveau ; région 66 partagée.
- Province/capitale administrative du nouveau pays : région 66. Eutin est sa résidence historique ; aucun nouveau locator de ville 3D n'est inventé. Le hub régional existant demeure à sa place.
- Registre impérial : **504 → 508 RGB**, même étendue impériale au pixel près. HLB est un membre impérial distinct, **pas une ville libre**.
- Terrains des enfants hérités des parents. Tous les bâtiments, niveaux, PM, détenteurs économiques, infrastructures écrites, unités et recrutements existants sont conservés sans migration cachée.

Les textes français/anglais couvrent le pays, l'adjectif, le gouvernement et sa description. Le drapeau est une simplification héraldique, non une restitution complète des quartiers dynastiques.

## Fondement et limites du dessin

Le périmètre est lu sur **Reilly, Wagrien, n° 300**, vers 1790–1795, donc avant la sécularisation. La souveraineté du noyau est recoupée avec les notices archivistiques et l'étude de la résidence d'Eutin. Le raccord au bitmap est une **approximation B**, pas un cadastre.

Le fichier `TRACING.json` expose cinq correspondances de symboles urbains, une projection diagnostique baltique **extrapolée hors de son domaine validé**, et un contrôle de cohérence technique à Kiel. Les résidus d'ajustement ne mesurent pas une erreur géographique indépendante. Le symbole d'Eutin est projeté vers **X 4335,07 / Y 732,14** ; il ne faut pas présenter ce point comme une localisation native certifiée. La différence avec la projection des coordonnées modernes reste une incertitude.

Le tracé est rasterisé aux centres des cellules, sans translation arbitraire ni agrandissement d'une cellule. Une cellule isolée du prolongement de Bosau n'est pas installée ; aucun corridor de raccord n'est créé. Les distinctions internes entre propriétés capitulaires et pouvoir temporel ne sont pas entièrement reconstituées.

**Schwartau/Kaltenhof, les domaines dispersés, les possessions du chapitre cathédral et du chapitre collégial restent ouverts.** Le comparatif Schwartau montre intentionnellement une zone inchangée. Ahrensbök et les acquisitions tardives ne sont pas importés. Aucun chantier voisin n'est rouvert.

## Population : nouvelle priorité du cahier des charges

Voir [la règle permanente](../MAP_POPULATION_POLICY.md). La conservation du total mondial n'est plus une contrainte pour les nouveaux découpages impériaux. R2 applique effectivement un delta historique estimé de **−3 725**.

La ventilation initiale avait transféré 3 698 habitants depuis HOL et 7 627 depuis LUB, soit 11 325. Elle reste documentée comme phase technique antérieure. R2 ajuste HLB à 7 600 en conservant les profils culturels/religieux à l'arrondi entier près, sans modifier les voisins. Leur composition héritée n'est pas certifiée par un recensement local. Les anciens CSV Q décrivent la phase initiale ; `CONTINUATION_R2/POPULATION_BEFORE_AFTER.csv` décrit la correction actuelle. Aucun chiffre de la ville de Lübeck ou de la principauté agrandie de 1803 n'est appliqué globalement au noyau.

## Union personnelle

Le type natif partage le souverain d'OLD : aucun doublon de Frédéric-Auguste n'est créé. Le moteur exige normalement deux monarchies pour maintenir une union. Une exception **HLB théocratique sous OLD seulement** est ajoutée dans la copie locale de `22_subject_personal_union.txt`, sans modifier l'installation du jeu ni autoriser globalement les unions théocratiques. Les autres clauses natives sont conservées.

La succession future suit les règles natives choisies par le joueur, pas une reconstitution du mécanisme historique des coadjuteurs. La survie de l'union à J30 doit être testée. Le rattachement préexistant de LUB à la Suède n'est pas modifié dans ce lot : c'est une configuration antérieure, non une nouvelle validation historique.

## Vérifications et fichiers

Résultats effectifs : `VALIDATION.json`, `UNIT_TESTS.json`, `IMPERIAL_COUNTERFACTUAL_COMPARISON.json`. Fichiers runtime touchés et empreintes : `INSTALLED_MANIFEST.json`. Liste complète des changements territoriaux : `TERRITORIAL_CHANGES.csv` ; allocations : `POPULATION_VALIDATION.csv`.

Les contrôles distinguent les **44 doublons RGB et 12 références invalides préexistants** des nouvelles erreurs. Les anciennes baselines et rapports restent intacts, sauf l'évolution expressément requise du registre impérial actif. HEAD et index Git sont protégés. Aucun commit, merge ou push.

### Résultats observés

- Contrôles ciblés MAP-2Q : **164/164 réussis** ; cinq nouveaux tests unitaires et négatifs réussis.
- Les **57 sorties** du compilateur impérial, avec les entrées d'avant le lot, correspondent aux fichiers antérieurement installés, après prise en compte du BOM. Aucun correctif impérial manuel n'a été absorbé comme une simple divergence de modèle.
- Les six anciennes suites totalisent **68 tests : 62 réussites, six échecs**. Trois échecs R8/R9 sont reproduits avec le bitmap et le registre exacts d'avant MAP-2Q. Les trois autres supposent que le bitmap mondial ou le registre ne contient aucun lot postérieur à Poel, à sa continuation ou à MAP-2O. Ils ne sont pas marqués PASS : leur portée historique figée est consignée dans `UNIT_TEST_RECONCILIATION.json`. Le replay ciblé MAP-2Q vérifie séparément la totalité du delta et l'absence de changement hors périmètre.
- Cinq CSV contrôlés avec conservation des types ; les populations historiques inconnues sont laissées **vides**, pas mises à zéro. Aperçu tabulaire vérifié pour éviter les colonnes tronquées.
- Deux espaces de fin de ligne introduits par ce lot ont été retirés. Les espaces préexistants des autres blocs ne sont pas reformattés ; `git diff --check` sur tout l'historique modifié reste donc averti par ces anciennes lignes.
- **Aucun lancement moteur, aucune certification historique exhaustive.** Après R2, la démographie est une estimation acceptée et installée ; les candidats C empêchent encore de présenter l'ensemble de MAP-2Q comme terminé. Le contrôle cumulatif courant réussit **167/167** vérifications en acceptant le delta démographique autorisé. Les résultats 164/164 ci-dessus décrivent la phase antérieure, archivée dans R2.

## Reprise avec la règle démographique — R1

La [continuation R1](CONTINUATION_R1/REPORT.md) contrôle directement les pages originales de Kohli : ville d'Eutin 2 652 habitants et Amt Eutin 6 824, explicitement datés de **1819**, pas de 1776. Ces valeurs ne sont pas installées sans justification du périmètre et de la rétroprojection. Aucun nouveau fichier runtime n'a été modifié pendant R1 ; la population de 11 325 reste provisoire. Les baselines et attestations antérieures sont conservées, et le replay est publié séparément dans la continuation.

## R2 — Estimation désormais installée

La [méthodologie R2](CONTINUATION_R2/POPULATION_METHODOLOGY.md) utilise l'interpolation urbaine 1755–1791 et une estimation rurale de Hennings vers 1769 rapprochée de l'AGGSH de 1819. L'écart avec Kohli reste explicitement non résolu. Le joueur a accepté l'approximation de 7 600 après correction de sa première réponse. Seules six valeurs de population HLB changent ; bitmap, droits impériaux, économie écrite, armées et union OLD–HLB sont préservés. Les validations avant R2 et l'ancien validateur sont archivés dans cette continuation. Les [limites et le test manuel restant](CONTINUATION_R2/UNRESOLVED.md) demeurent ouverts.

## Recherche locale ColGrep — appel du lot initial

Un appel `colgrep --agent` dans `./common`, modèle configuré `colgrep-agent-2B-Q8_0.gguf`, a réellement été exécuté : **92,5 s**, 10 tours, 3 recherches internes et 6 commandes internes. Il n'a pas soumis de localisation valide et ses pistes étaient peu pertinentes ; les identifiants ont ensuite été vérifiés directement. Ce résultat ne démontre aucune économie de quota. Les tokens Codex et une comparaison contrôlée ne sont pas disponibles.
