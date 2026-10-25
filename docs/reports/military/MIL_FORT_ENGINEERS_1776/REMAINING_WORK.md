# Reprise du chantier militaire

La consigne de mission limite l'installation à un premier sous-lot testable. **A1 est le point de contrôle livré ; aucune passe mondiale massive n'est lancée.**

| Sous-lot | Statut | Travail restant |
| --- | --- | --- |
| A1 — premier réseau occidental | IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION | Douze implantations ; test de démarrage, entretien, un mois et sauvegarde/reprise |
| A2 — autres places occidentales | NOT_STARTED | Pyrénées/Alpes françaises, façades maritimes, Carthagène péninsulaire, Pampelune, Valença, Bergen-op-Zoom ; vérifier dates, propriétaires et PM |
| A2 — Maastricht | BLOCKED | Recouper condominium et commandement de la place ; province actuelle `x0000DF`, `STATE_GELRE`, propriétaire BEO. Ne pas déplacer un fort pour compenser |
| B — Europe centrale et orientale | NOT_STARTED | Autriche, Prusse, Russie, Saxe, Bavière, Ansbach, Pologne-Lituanie et autres principautés ; préserver les passes territoriales validées |
| C — Nord et Méditerranée | NOT_STARTED | Suède, Danemark-Norvège, Sardaigne, Venise, Gênes, Malte, États italiens ; TAGs et subdivisions réels |
| D — Amériques | NOT_STARTED | Places espagnoles/britanniques et autres colonies ; contrôle effectif au 1er janvier 1776, pas les occupations intervenues plus tard |
| E — Inde, Asie, Afrique, monde ottoman | NOT_STARTED | Tradition fonctionnelle d'artillerie démontrée ; cohérence technologique à examiner séparément |
| F — génie et bataille | RESEARCH_PARTIAL | Organisations A1 documentées partiellement ; aucun bataillon ajouté. Autres pays à rechercher ; essai réel du contre des forts |

Les entrées individuelles et les exclusions chronologiques sont conservées dans [FORTRESS_INVENTORY.csv](FORTRESS_INVENTORY.csv). Une entrée `NOT_STARTED` est une piste issue du cahier de mission, **pas une preuve de fort opérationnel**. Les TAGs indicatifs sont explicitement marqués lorsqu'ils restent à vérifier.

## Priorités pour le génie

1. **Pays-Bas** : registres/états du régiment de mineurs et sapeurs en 1776, effectifs et garnisons. Sa permanence depuis 1748 est attestée ; son nom ne justifie pas un bataillon de 1 000 hommes.
2. **France** : compagnies de mineurs encore rattachées à l'artillerie au 1er janvier, effectifs effectivement mobilisables et lieux. Ne pas ajouter les pionniers créés en juillet ni rétroprojeter la désignation de fin d'année.
3. **Portugal** : service d'officiers et spécialistes dans les autres armes avant 1776. Le bataillon identifié de 1812 est exclu ; cela ne classe pas le pays en absence totale de génie.
4. **Prusse** : régiment de pionniers de 1742 et transformations ultérieures ; vérifier qu'il existe encore sous une forme pertinente en 1776.
5. **Autriche, Russie, Suède, Saxe** : distinguer officiers, mineurs, pionniers, pontonniers et auxiliaires temporaires.
6. **BIC et autres présidences** : ingénieurs de Madras vers 1770 ; ne pas confondre officiers précoces et corps de sapeurs constitués plus tard.
7. **TUR** : rechercher les Lağımcı malgré l'absence de technologie du génie dans le tableau. Une exception technologique exige son propre examen d'effets secondaires.
8. Tous les autres pays avec technologie du génie restent des lignes `UNRESEARCHED` dans l'inventaire ; aucune classe D automatique.

## Limites techniques à garder visibles

- La construction au démarrage est projetée statiquement ; ordre natif et embauche à confirmer en jeu.
- Les ouvrages historiques sont représentés à l'échelle de l'État économique. Aucun bâtiment n'est ancré artificiellement sur une province de citadelle.
- Les États côtiers reçoivent les bâtiments navals existants à la demande du joueur. Le génie ne contre actuellement que le système des forts intérieurs.
- Aucune réforme fiscale ou compensation budgétaire n'est incluse. Les besoins à plein emploi doivent être comparés aux budgets observés.
- Les contrôles des anciens rapports gardent leurs baselines historiques. Ne pas les modifier pour absorber les changements des autres chantiers.

## Prochaine action

Exécuter le [protocole joueur A1](PLAYER_TEST_PROTOCOL.md), conserver ses résultats, puis sélectionner un sous-lot suivant. Ne pas modifier la progression SERG : ce chantier possède son suivi militaire distinct.
