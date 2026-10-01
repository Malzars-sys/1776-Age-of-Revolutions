# Laboratoires expérimentaux — état de préparation de l'intégration 1776

> État historique avant clarification. Les décisions et le prototype réalisés ensuite sont consignés dans [TECH8C](TECH8C_RESEARCH_LABORATORY_PROTOTYPE_2026-09-30.md) ; les propositions ci-dessous ne remplacent pas les demandes ultérieures de l'utilisateur.

Date : 30 septembre 2026. Statut : **conception partiellement définie ; intégration non lancée**.

Cette passe clôt le travail demandé sur la loi des quotas et reprend uniquement le dossier des laboratoires. Elle ajoute ce rapport, sans modifier la loi, l'économie, les technologies, l'IA ou les sauvegardes.

## 1. Conclusion

Les livrables existent et l'ancrage dans l'arbre est prêt. En revanche, ils ne constituent pas encore une spécification exécutable : le nombre de biens de connaissance, leurs producteurs, le commerce, la taille des laboratoires et leurs effets ne sont pas arrêtés.

Le dernier audit ciblé, **TECH8A du 27 septembre**, termine expressément par « audit terminé, laboratoire non implémenté » et demande un chiffrage et un test séparés. La demande actuelle autorise l'intégration si le dossier est sans ambiguïté ; ces choix changent matériellement le fonctionnement du système. La branche retenue est donc le rapport d'avancement, pas une implémentation fondée sur des décisions silencieuses.

**Avancement vérifié :** audit de référence terminé, point d'entrée technologique existant, mécanismes de modificateurs disponibles ; chaîne économique et bâtiment absents, équilibrage et validation en partie non réalisés pour ce système.

## 2. Livrables relus et niveau d'autorité

| Livrable | Ce qu'il établit | Limite actuelle |
|---|---|---|
| [TECH1C — système Tech & Res](../../research/technology/TECH1C_TECH_RES_SYSTEM_AUDIT.md) | Centre appliqué, intrants de connaissance, spécialisations, décision/site/journal et construction de secours pour l'IA. | Référence à réimplémenter localement, pas modèle à copier. |
| [TECH1C — exigences IA 1776](../../research/technology/TECH1C_1776_AI_REQUIREMENTS.md) | Producteur avant consommateur, réponse aux pénuries, universités distinctes des centres, aucune dépendance obligatoire à un autre mod. | Contrat de capacités, pas recettes ni critères d'accès chiffrés. |
| [TECH1C — audit comparatif](../../research/technology/TECH1C_EXTERNAL_ECONOMY_AI_AUDIT.md) et [dépendance IA](../../research/technology/TECH1C_AI_DEPENDENCY_AUDIT.md) | Risques de démarrage sans offre/demande et limites d'une simple priorité de construction élevée. | Les comportements nécessaires à la boucle 1776 restent à éprouver en partie. |
| [Society V1](TECH_SOCIETY_1700_1836_V1.md), section Industrial Knowledge Loop | Ancrage historique dans la recherche expérimentale ; universités pour l'enseignement/recherche fondamentale, centres pour la recherche appliquée. | Bien de connaissance, production/consommation et commerce explicitement non figés. |
| [Arbre intégré V1](TECH_TREE_1700_1836_INTEGRATED_V1.md), sections 18 et 20 | Industrial Knowledge différé et lié aux tests de rythme de recherche. | Ne vaut pas approbation d'une nouvelle boucle économique. Les biens industriels intégrés depuis doivent être évalués sur le code actuel. |
| [TECH6B3D](TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_REPORT.md), section Q | Bonus initial de +5 au plafond d'innovation sur la technologie ; rééquilibrage demandé. | Ce bonus n'est ni un laboratoire ni une production d'innovation. |
| [TECH8A — données et laboratoire](../../research/technology/TECH8A_DATA_RESEARCH_AUDIT.md) | Proposition plus récente : observations/registres → compilation → laboratoire, sans électronique ni construction annuelle forcée. | Quantités, prix, propriétés du bâtiment, commerce et effets restent à définir. |
| [TECH0P — douze ères](TECH_0P_12_ERA_RUNTIME_VALIDATION.md) | Acceptation technique des douze ères, recherche et sauvegarde dans un ancien harnais. | Ce test ne valide pas le rythme du nouvel arbre ni le fonctionnement des futurs laboratoires. |

Les anciens rapports ne sont pas traités comme plus autoritatifs que le code actuel. En particulier, l'ancien owner proposé pour l'accès aux universités ne doit pas être rétabli automatiquement.

## 3. État effectif du mod, contrôlé dans les fichiers

- `common/technology/technologies/30_tech3a_society.txt:592` définit `experimental_research_laboratories`, en **ère 5**, catégorie Society. Prérequis actuels : `polytechnical_education`, `institutionalized_scientific_exchange`, `scientific_metrology`. Effet direct : `country_weekly_innovation_max_add = 5`. Poids de recherche IA : 1. L'icône reste temporaire (`gfx/error_manul.dds`).
- L'ère 5 coûte actuellement **7 500** points avant les pénalités et autres modificateurs. Le découpage documentaire la situe vers 1800–1824 ; ce repère n'est pas un verrou automatique de date dans cette définition.
- `common/buildings/07_government.txt:31` définit l'université, actuellement débloquée par `specialized_technical_academies`. Il ne faut pas changer cet accès au passage.
- `common/production_methods/07_government.txt` fournit les quatre niveaux universitaires : 1 / 1,5 / 2 / 3 d'innovation hebdomadaire par niveau pleinement employé, plus des qualifications et une consommation de papier. Ils sont réellement reliés au PMG universitaire.
- Aucun bâtiment `building_research_center`, ni chaîne active `raw_data`, `organized_data`, `business_data` ou Industrial Knowledge n'a été trouvé dans les définitions de gameplay du mod. Le nom de la technologie ne signifie donc pas qu'un bâtiment soit déjà intégré.
- Les types de modificateurs du jeu installé définissent bien innovation produite, plafond d'innovation, vitesse de recherche générale et vitesses par catégorie. Leur existence ne prouve pas encore leur comportement en pénurie dans une nouvelle méthode de production.

Différence essentielle : **augmenter le plafond permet d'utiliser davantage d'innovation ; cela ne crée pas les points d'innovation manquants**. L'université doit conserver un rôle utile.

## 4. Ce que l'on peut reprendre de Tech & Res

La lecture de l'installation locale confirme le précédent audit. Son centre est réservé à l'État, non extensible, débloqué par une technologie de physique moderne et soumis à un site obtenu par décision/journal. Le premier PM emploie 30 000 personnes et consomme notamment 100 données organisées, 50 papier, 25 imprimés et 25 composants électroniques ; les niveaux suivants utilisent robotique, ordinateurs et systèmes d'IA. Il existe aussi un rattrapage annuel qui crée directement le bâtiment pour l'IA.

À retenir : un établissement de recherche appliquée, des intrants documentaires, des coûts de fonctionnement, une spécialisation et une offre préalable de connaissances.

À ne pas reprendre littéralement : électronique/informatique, trois biens numériques, 30 000 emplois pour un premier établissement, conditions d'accès de grande métropole moderne, priorité IA 50 000 ou création gratuite annuelle. Aucun code, texte ni asset de Tech & Res n'est copié par cette passe.

La boucle d'origine n'est pas une chaîne simple : les rapports manuels produisent déjà des données organisées, sans données brutes. Les données brutes sont surtout issues des PM numériques tardifs. Une adaptation 1776 doit donc définir son propre sens historique au lieu de renommer mécaniquement les trois biens.

## 5. Axes à résoudre avant intégration

| Axe | Ambiguïté ou risque | Travail nécessaire | Proposition à valider |
|---|---|---|---|
| **P0 — taille de la boucle** | Les anciens documents parlent d'un bien de connaissances industrielles ; TECH8A propose deux étapes documentaires distinctes. | Choisir zéro, un ou deux nouveaux biens avant de modifier les bâtiments producteurs. | Suivre TECH8A : observations/registres puis dossiers scientifiques compilés ; exclure les données commerciales numériques. |
| **P0 — premiers producteurs** | Administration, universités, ports et industries sont cités, sans liste finale ni recettes. Un consommateur absent peut empêcher le démarrage de la production commerciale. | Fixer une courte liste de PM optionnels, leurs gates et leur contrepartie ; vérifier leur sélection par l'IA et leur financement. | Pilote sur bâtiments existants : relevés administratifs et compilation universitaire. Étendre ensuite aux industries réellement utiles, pas à tous les bâtiments. |
| **P0 — utilité du laboratoire** | Innovation fixe, plafond et accélération ne sont pas interchangeables ; les multiplier tous peut accélérer excessivement la recherche. | Comparer les variantes à coût et emploi comparables, avec une université de référence. | Garder la production principale d'innovation aux universités ; tester d'abord un laboratoire relevant le plafond. Spécialisations de vitesse dans un second lot. |
| **P0 — taille et cumul** | Un établissement national unique, plusieurs sites régionaux ou un bâtiment extensible créent des équilibres très différents. | Arrêter limite, extensibilité, coût de construction, effectifs et conditions de site ; tester les contournements de limite. | Pilote public limité à un site par pays, de taille adaptée aux effectifs universitaires du mod. Ce n'est pas encore une limite implémentée. |
| **P0 — commerce et accès** | Un bien exportable permet d'acheter les intrants de recherche à l'étranger ; un bien non exportable peut bloquer les petites économies. Les marchés communs posent une autre question. | Définir explicitement échange extérieur, prix, quantité échangée et comportement dans un marché commun. | Ne pas utiliser une quantité commerciale nulle comme substitut à une décision. Commerce des connaissances à choisir expressément. |
| **P0 — pénuries et bonus** | `workforce_scaled` relie les effets à l'emploi, mais ne prouve pas qu'une pénurie annule directement un bonus de recherche. | Tests sans intrants à emploi comparable, puis baisse d'emploi ; si nécessaire, activation conditionnelle locale et idempotente. | Aucun bonus permanent gratuit lorsque le laboratoire ne fonctionne pas ; ne pas promettre cette propriété avant test moteur. |
| **P0 — démarrage IA** | Les types natifs plafond/vitesse ont une valeur IA déclarée de 0 ; une forte priorité fixe ne résout pas la chaîne ni le budget. | Tester séparément premier producteur, compilation, construction, emploi, changement de PM et réaction à la pénurie. | Pondérations contextuelles locales, liées aux capacités et au budget ; aucune construction annuelle forcée ni dépendance Kuromi. |
| **P1 — rythme et bonus existant** | Le +5 actuel peut se cumuler avec le bâtiment ; les tests des douze ères ne démontrent pas un besoin d'accélération générale. | Mesurer le rythme avant/après, puis décider conserver, réduire ou transférer le +5. | Ne pas supprimer ni déplacer le +5 tant que la nouvelle contrepartie n'est pas arrêtée. |
| **P1 — localisation, assets et sauvegardes** | Nouveaux biens/PM/bâtiment sans identité visuelle ni migration prévue. | FR/EN, infobulles séparant plafond et production, assets locaux/vanilla pertinents, nouvelle partie et sauvegarde existante. | Pas de photographie/électronique anachronique ni de reprise d'asset tiers ; aucune attribution rétroactive de bâtiment sans décision. |

Les quantités et coefficients peuvent être conçus pendant un prototype après choix d'architecture. Ce n'est pas chaque détail numérique qui exige un arbitrage utilisateur ; les véritables décisions préalables sont la complexité de la boucle, la diffusion des connaissances, l'échelle des établissements et leur rôle dans la recherche.

## 6. Adaptation recommandée et prochain lot

Proposition de cadrage, **pas spécification déjà approuvée** :

1. Les relevés décrivent observations, registres et comptes rendus techniques, pas des données informatiques. Ils commencent sur des bâtiments existants avant le déblocage du laboratoire.
2. Une compilation documentaire transforme ces relevés avec papier et emplois qualifiés. Un PM optionnel ne doit pas remplacer arbitrairement l'enseignement universitaire ou la production normale de bureaucratie.
3. La technologie existante débloque un laboratoire public de recherche appliquée. Il consomme les dossiers compilés et des biens compatibles avec la période, choisis dans le catalogue déjà intégré. La production pharmaceutique existante dans les travaux chimiques n'est pas dupliquée par ce bâtiment.
4. La distinction université/laboratoire reste lisible : production d'innovation et qualifications d'un côté ; capacité d'exploitation de l'innovation et, éventuellement plus tard, recherche spécialisée de l'autre.
5. Pas de mise à disposition automatique pour tous les pays en janvier 1776. L'accès suit les technologies et les capacités nationales, sans ajouter de date arbitraire ni réécrire les starting technologies dans ce lot.

Ordre recommandé : **cadrage des quatre choix → fiches économiques chiffrées → prototype local limité → essais comparatifs → intégration générale**. Les brevets, licences, espionnage et commerce de technologies restent hors de ce premier lot.

## 7. Validation à préparer

| Test | Résultat à vérifier |
|---|---|
| Intégrité statique | Biens avec producteurs/consommateurs, PM reliés aux bons PMG/bâtiments, gates et localisations valides, aucune référence externe non définie. |
| Démarrage à marché vide | Possibilité réelle de financer/activer relevés puis compilation puis laboratoire, sans création gratuite répétée. |
| Plein emploi / demi-emploi / zéro emploi | Effets de recherche mesurés et cohérents ; zéro bonus provenant d'un établissement vide. |
| Pénurie de dossiers ou de papier | Effet concret sur le fonctionnement, affichage explicite et récupération possible. L'annulation du bonus n'est pas présumée. |
| Comparaison avec universités seules | Laboratoire utile sans rendre l'université obsolète ; plafond distinct de la production ; cumul du +5 documenté. |
| Petit pays / grande puissance / faible alphabétisation | Accès réaliste, charges supportables, absence de contournement disproportionné de l'éducation. |
| Commerce et marché commun | Échanges conformes au choix retenu, notamment partenaires/subordonnés ; pas de règle implicite. |
| IA autonome sur plusieurs pays | Ordre d'investissement observable, budget, emploi et approvisionnement soutenables ; ni absence totale de construction ni surconstruction. |
| Rythme sur 20 ans et sauvegarde/rechargement | Progression comparée à la référence sans laboratoires, effets conservés correctement et pas de doublons. |

Les seuils précis de réussite (coût acceptable, gain cible, délai IA, rendement) devront être inscrits dans la fiche économique avant les essais. Aucun de ces tests du futur système n'est revendiqué comme réussi aujourd'hui.

## 8. Bilan de cette passe

- Livrables principaux relus et confrontés au code actuel : oui.
- Installation locale de Tech & Res et types de modificateurs natifs vérifiés : oui.
- Architecture économique finale sans ambiguïté : non.
- Prototype ou intégration de gameplay effectués : non, conformément à l'alternative demandée.
- Fichier ajouté : ce rapport uniquement.

**Pour avancer :** choisir entre laboratoire simple utilisant les biens existants, boucle à un bien documentaire, ou boucle à deux étapes telle que recommandée par TECH8A ; préciser commerce des connaissances, taille des établissements et effet principal. Une fois ce cadrage arrêté, le chiffrage et le prototype pourront être réalisés sans rouvrir la loi des quotas.
