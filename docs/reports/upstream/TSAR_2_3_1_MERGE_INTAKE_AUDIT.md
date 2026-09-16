# Audit d'admission — mise à jour Tsar 2.3.1 / 2.3.1.1

Date de l'audit : 2026-09-16  
Version Victoria 3 ciblée : 1.13.11  
Objet : déterminer ce qui doit être repris depuis la version originale mise à jour, sans écraser les refontes du fork.

## Conclusion exécutive

La mise à jour Tsar ne doit **pas** être fusionnée fichier par fichier ni copiée en bloc.

Le fork a déjà remplacé en profondeur l'arbre technologique, la distribution des technologies de départ, les routes/canaux/voies ferrées, de nombreuses méthodes de production et plusieurs chaînes de biens. Les apports Tsar utiles doivent donc être intégrés par **ensembles fonctionnels cohérents**, avec adaptation aux identifiants et aux équilibres du fork.

Décision générale :

- **reprendre manuellement** les refontes historiques et géopolitiques (Inde, Vietnam, personnages, ajustements de départ) ;
- **reprendre manuellement** le contenu narratif autonome (Portugal–Brésil, certaines lois et idéologies) après audit de ses dépendances ;
- **ne pas reprendre** les arbres technologiques, les technologies de départ, les routes et les méthodes de production Tsar en bloc ;
- **ne pas reprendre** le manifeste et ses `replace_paths` en bloc ;
- importer les localisations et ressources graphiques uniquement avec le contenu effectivement accepté.

## Sources comparées

| Rôle | Source | État constaté |
|---|---|---|
| Base historique fiable | commit Git `b602804` — import initial du fork | 778 fichiers de jeu ; meilleure référence disponible pour l'ancien original |
| Original Tsar actuel | `C:\Program Files (x86)\Steam\steamapps\workshop\content\529340\3617930953` | version 2.3.1, compatible 1.13.11, changelog 2.3.1.1 |
| Copie dite hotfix | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source` | 904/904 fichiers identiques à l'abonnement Tsar actuel ; ce n'est plus une archive ancienne |
| Fork de travail | dépôt local courant | 1 518 fichiers de jeu, refontes TECH et contenu additionnel non commité |
| Ancien build Steam du fork | `Age of revolution Fork [Steam Build]` et Workshop `3780935876` | build du fork, pas une source Tsar ancienne fiable |

Le précédent rapport qui assimilait l'item Workshop `3780935876` au mod principal ne doit donc pas servir de base à cette nouvelle fusion.

## Résultat du différentiel à trois versions

Comparaison : base Git initiale / Tsar actuel / fork actuel.

| Catégorie | Nombre |
|---|---:|
| Déjà identique à Tsar | 160 |
| Nouveau uniquement dans le fork | 723 |
| Fork modifié, Tsar inchangé depuis la base | 5 |
| Ajouté différemment des deux côtés | 22 |
| Modifié des deux côtés | 593 |
| Supprimé dans le fork, modifié par Tsar | 7 |
| Supprimé par Tsar, modifié dans le fork | 14 |
| Nouveau uniquement chez Tsar, à examiner | 117 |
| Modification Tsar seule directement admissible | 1 |
| Suppression Tsar seule directement admissible | 1 |

Ce résultat interdit une fusion automatique : 636 fichiers représentent des conflits sémantiques potentiels entre deux évolutions indépendantes.

## Matrice de décision

| Domaine Tsar | Décision | Contenu à reprendre | Contraintes pour le fork |
|---|---|---|---|
| Refonte du sous-continent indien | **REPORTER AU CHANTIER CARTE — source partielle** | réutiliser seulement les choix historiques confirmés lors de la future refonte | la suppression d'un Pendjab unifié en 1776 est défendable, mais son attribution intégrale aux Durrani ne l'est pas : les Afghans avaient perdu Lahore dès 1765 face à la montée des Sikh misls ; le lot Tsar ne peut donc pas être repris gratuitement |
| Changements de carte de l'Inde | **PRENDRE — inclus dans le lot Inde** | la capture de changelog est incomplète : le changement est surtout politico-historique dans `history/states`, pops, bâtiments, armées et relations, pas seulement une géométrie de provinces | ne jamais importer seulement `00_states.txt` : cela créerait des pays sans populations, bâtiments, armées ou relations cohérentes |
| Refonte du Vietnam | **REPORTER AU CHANTIER CARTE — bonne base à corriger** | conserver l'idée d'un acteur Tây Sơn en Annam et d'une représentation séparée des Nguyễn | la situation est globalement cohérente avec la révolte commencée en 1771, mais la maîtrise du Sud change rapidement en 1776–1777 ; `NGU` possède en outre une histoire de pays sans définition ni territoire et doit être supprimé ou réconcilié |
| Personnages historiques des grandes puissances | **CONSERVER LE FORK ; PRENDRE LES ADN APPARIÉS** | reprendre uniquement un ADN Tsar quand il représente exactement le même dirigeant que notre fiche | nos recherches, dates, idéologies, religions et traits font autorité ; seuls les ADN de Frédéric II et d'Abdülhamid Ier satisfont actuellement cette règle et ont été intégrés |
| Ajustements Inde 2.3.1.1 | **PRENDRE dans le lot Inde** | Agra/Hindustan, Malwa/Marathes, suppression du Khalsa autonome, Durrani, comptoirs européens, bâtiments et armées indiens, conditions mogholes | vérifier que chaque changement reste cohérent avec les futurs pays voués à disparaître lors de la refonte de carte du fork |
| Ajustements de départ hors Inde | **PRENDRE SÉLECTIVEMENT** | Carnatic danois-norvégien, armée perse réduite, canons durranis, censure ottomane, Pegu danois, revendications perses sur Basra, navires/troupes néerlandais et DEI | fusion par blocs nationaux et faire un contrôle runtime de chaque pays touché |
| Portugal–Brésil | **PRENDRE — adaptation manuelle** | journaux, événements, boutons et effets permettant l'Union ou l'Union personnelle | contrôler les sujets, lois, tags, localisations et effets déjà modifiés par le fork ; ne pas copier les fichiers généraux contenant aussi du contenu vanilla non lié |
| Idéologie `enlightened_absolutism_mod` | **PRENDRE SÉLECTIVEMENT** | idéologie et affectations historiquement justifiées | vérifier les positions de lois et les doublons avec les idéologies du fork ; fournir localisation française |
| Loi `law_peasant_republic` et gouvernement associé | **PRENDRE avec le lot Vietnam** | loi nécessaire notamment aux Tây Sơn | auditer les groupes de lois, déclencheurs, gouvernement et localisations ; ne pas importer les autres lois du fichier sans examen |
| Autres lois Tsar | **EXAMINER PAR ID** | seulement les lois absentes du fork et utiles au design | `law_merchant_banking` et les Navigation Acts existent déjà dans le fork : ne pas les dupliquer |
| Nouveaux types de troupes | **RETENIR POUR UNE VAGUE MILITAIRE DÉDIÉE** | `combat_unit_type_musket_infantry` et `combat_unit_type_improved_cannon_artillery` | les deux paliers sont simples mais bien placés entre irréguliers/infanterie de ligne et canon/artillerie mobile ; les raccorder respectivement à `regulated_small_arms` et `standardized_field_artillery`, puis migrer les formations de départ sans copier le fichier Tsar complet |
| Arbre technologique Tsar | **NE PAS PRENDRE** | aucun fichier complet | le fork possède désormais trois arbres restructurés, des ères et des dépendances contrôlées ; une copie réintroduirait l'ancien réseau et des incohérences chronologiques |
| Technologies de départ Tsar | **NE PAS PRENDRE EN BLOC** | éventuellement une information historique ponctuelle comme référence | conserver la distribution mondiale auditée du fork et la fermeture complète de ses prérequis |
| Routes Tsar (`building_roads_mod`) | **NE PAS PRENDRE** | éventuellement réutiliser une ressource graphique après vérification | le fork utilise le bâtiment unifié route/canal/rail ; importer le bâtiment Tsar créerait un doublon et casserait le modèle TECH7A |
| Nouvelles méthodes de production Tsar | **NE PAS PRENDRE** | aucune méthode actuelle ne justifie une importation directe | routes et ports contredisent TECH7A ; rotations et outils agricoles concurrencent nos chaînes ; la rotation Tsar produit même de l'engrais au lieu d'en consommer ; élevage, exploitation forestière et construction navale sont trop sommaires ou déséquilibrés |
| Nouveaux bâtiments Tsar | **NE PAS PRENDRE DANS CETTE VERSION** | aucun bâtiment actuel | `building_roads_mod` est remplacé par notre réseau terrestre unifié ; le remplacement de la mine d'or par `shaft_mining` et l'injection agricole ne justifient pas de nouveaux overrides globaux |
| Événements et journaux généraux | **NE PAS COPIER EN BLOC** | prendre uniquement les chaînes propres à une fonctionnalité acceptée | beaucoup de fichiers sont des ombres ou copies de contenu vanilla ; une copie globale risquerait des régressions 1.13.11 et d'écraser les corrections du fork |
| Localisations anglaises | **PRENDRE avec chaque fonctionnalité admise** | clés requises par les lots acceptés | ne pas importer des clés de technologies/PM rejetés ; corriger les doublons et les erreurs de clés |
| Localisations françaises | **CRÉER/COMPLÉTER dans le fork** | traduction de tout contenu accepté | la version Tsar est surtout anglaise ; aucun contenu admis ne doit rester brut en jeu français |
| Ressources graphiques | **PRENDRE avec leurs dépendances** | drapeaux, armoiries, portraits et icônes strictement requis | éviter les fichiers orphelins et préserver les remplacements `error_deer` décidés dans le fork |
| Manifeste et `replace_paths` Tsar | **NE PAS PRENDRE EN BLOC** | aucun remplacement automatique | Tsar remplace beaucoup plus de répertoires historiques que le fork ; chaque extension de portée doit être justifiée et validée séparément |
| Suppression de `00_french_revolution_cheat.txt` | **PRENDRE** | aligner avec le remplacement Tsar `_mod` si la référence existe bien dans le fork | petite correction ciblée, à vérifier avec les appels du bouton |
| `mod_journal_entries_l_english.yml` | **PRENDRE SÉLECTIVEMENT** | c'est la seule modification Tsar seule sans conflit de contenu détecté | vérifier les clés françaises correspondantes avant intégration |

## Lot Inde : périmètre minimal obligatoire

La « carte de l'Inde » ne peut pas être réduite à un seul fichier. Le lot doit être traité comme une migration cohérente comprenant au minimum :

- définitions et histoires des pays concernés ;
- propriétaires et frontières politiques dans l'histoire des États ;
- relations de sujet, alliances, intérêts et diplomatie initiale ;
- populations et bâtiments de départ ;
- formations militaires et déploiements ;
- personnages et dirigeants ;
- revendications, journaux, événements et conditions de formation ;
- armoiries, drapeaux, noms dynamiques et localisations ;
- réapplication des technologies de départ et des bâtiments ajoutés par le fork.

Une intégration partielle de ce lot est interdite : elle produirait des États sans économie, des armées sans pays, des sujets sans suzerain ou des références de `region_state` invalides.

## Ordre de fusion recommandé

1. **Geler une base de travail** : enregistrer l'état actuel du fork avant toute admission Tsar.
2. **Lot Inde** : intégrer et tester comme une vague autonome.
3. **Lot Vietnam** : tags, carte politique, guerre, loi et personnages.
4. **Personnages historiques** : garder les fiches du fork et ne reprendre que les ADN strictement appariés.
5. **Portugal–Brésil** : chaîne narrative autonome.
6. **Ajustements nationaux ponctuels** : Perse, Ottomans, Danemark-Norvège, Pays-Bas/DEI.
7. **Idéologies, lois et unités** : adaptation aux arbres et systèmes du fork.
8. **Ressources et localisations** : seulement celles requises par les lots retenus.
9. **Validation finale** : références, doublons d'identifiants, localisations EN/FR, parser, démarrage 1776 et runtime ciblé.

Chaque vague doit rester réversible et faire l'objet d'un diff ciblé. Aucun répertoire complet ne doit être copié depuis l'abonnement Steam.

## Risques particuliers à surveiller

- Le fork annonce 1.13.9 dans `.metadata/metadata.json` alors que le descripteur accepte `1.13.*` et que Tsar cible 1.13.11 : harmoniser seulement au moment de la préparation de release.
- Le manifeste Tsar remplace notamment les États, bâtiments, pops, déploiements, événements et journaux ; le fork n'a pas la même portée. Copier le manifeste changerait silencieusement la résolution de centaines de fichiers.
- Les 593 fichiers modifiés des deux côtés doivent être considérés conflictuels même si une comparaison textuelle paraît simple.
- Les technologies et méthodes de production Tsar utilisent leur propre chronologie ; tout contenu admis doit être raccordé à la chronologie du fork, jamais l'inverse.
- Les personnages `TEMPORARY` ou sans DNA ne sont pas automatiquement meilleurs que les personnages déjà reconstruits dans le fork.

## Statut

Audit d'admission terminé.  
Aucune fusion Tsar n'a été exécutée pendant cet audit.  
La prochaine action sûre est l'ouverture d'une vague autonome « Inde 2.3.1.1 », après sauvegarde explicite de l'état actuel du working tree.
