# Victoria 3 1.15 — Évaluation initiale de compatibilité

Date : 6 novembre 2026. Chantier : issue #20, coordination #19.
Statut : analyse statique livrée ; protocole de lancement et comparaison à durée égale encore incomplets. **L’issue #20 doit rester ouverte.**
Aucune compatibilité en jeu n’est certifiée.

## 1. État de référence et protections

- Installation canonique consultée en lecture seule : `C:\Games\Victoria 3\game`.
- Build attesté par `code_revisions.log` : `release/1.15.0`, `6338547985dbc271523e149f362a6fd93dc62975`, construit le 3 novembre 2026 à 16:16:50 UTC. Le checksum visible en menu n’a pas été relevé.
- State and Revolution : installé et activé selon l’utilisateur. Le `content_load.json` capturé indique `enabledMods: []`, `enabledUGC: []`, `disabledDLC: []`. La liste exhaustive des licences/DLC effectivement chargés n’a pas été certifiée.
- Le lancement vanilla debug était encore en cours lors du message de l’utilisateur. Deux captures provisoires ont été conservées, sans interrompre le jeu. La seconde montre l’initialisation des pays dans `debug.log` ; elle ne prouve ni un premier jour simulé ni une observation humaine des écrans.
- Workspace initial : `main`, HEAD `52c42808bdb0748e69fbde3423bb5004b5b1f20a`, avec **77 chemins suivis modifiés et 1 044 fichiers non suivis** dans le relevé détaillé. Ce HEAD seul ne reproduit donc pas l’installation locale.
- Deux autres worktrees locaux existent : `codex/map-0-collaborator-integration` et `codex/sc4-massa-carrara-finalisation-20261031`. La branche distante historique `hotfix-dlc-audit` est un autre chantier, pas une preuve de migration 1.15.
- Aucune modification locale de gameplay, de carte, de souveraineté, de POPs, de rapports SERG/WORLD ou de données de départ. Le travail de Sarah/Yekatarina sur `contrib/yekatarina` et #17 est exclu.
- Contrôle final : statut Git local inchangé ; empreintes des **1 202 surcharges de fichiers** inchangées. Les 24 fichiers du contrôle séparé carte/cuivre sont également identiques.
- La création locale de `hotfix/1.15` a échoué : accès en lecture seule à `.git`. Le workspace actif est resté sur `main`. La branche **GitHub** `hotfix/1.15` a été créée depuis le HEAD ci-dessus pour la seule exception d’icônes autorisée ensuite.

## 2. Surface de compatibilité

L’inventaire par chemin identique trouve **1 202 surcharges**, dont **18 identiques** au vanilla local et **1 184 différentes**. C’est une mesure de surface, pas un décompte de bugs.

| Domaine | Fichiers de même chemin que le vanilla |
| --- | ---: |
| Historique sous common/history | 504 |
| Événements | 304 |
| Journaux | 162 |
| Lois | 21 |
| Carte et régions d’État | 21, dont 16 fichiers de régions |
| Bâtiments | 12 |
| Méthodes de production | 10 |
| Articles de traité | 24 |
| Interface GUI | 12 |
| Types de buts de guerre | 3 |
| Définitions globales | 1 fichier complet |

Le tableau n’épuise pas les domaines. `overrides.tsv` fournit l’inventaire complet avec empreintes.

Les ajouts à noms distincts peuvent aussi masquer des définitions vanilla par identifiant. Ils ne figurent pas tous dans l’inventaire des chemins identiques : c’est précisément le cas du cuivre.

Les deux métadonnées du mod annoncent encore la 1.13 : `descriptor.mod:2` déclare `1.13.*` ; `.metadata/metadata.json:5` déclare `1.13.9`. La métadonnée moderne remplace cinq répertoires, dont les historiques de personnages/diplomatie/conflits et les technologies ; le descriptor classique ne liste que les deux répertoires de technologies. Le lancement de test devra conserver et identifier le descripteur réellement utilisé.

## 3. Journaux préservés et attribution des erreurs

Les captures `logs_provisional_01` et `logs_provisional_02` contiennent les journaux actifs et leurs rotations. Ce sont des copies successives de fichiers en cours d’écriture, pas des captures atomiques d’un lancement terminé. Les empreintes des fichiers livrés sont dans le manifeste de l’archive.

| Échantillon | Résultat observé | Interprétation autorisée |
| --- | --- | --- |
| Vanilla 1.15 en cours, capture 01, error.log | 38 messages, 38 signatures exactes | Première étape de chargement seulement. |
| Même lancement, capture 02, error.log | **219 messages, 209 signatures exactes** | Le chargement a avancé ; plusieurs erreurs de scripts/localisation sont aussi présentes sans mod déclaré. |
| Ancien essai moddé 1.15, error.1.log de la capture 01 | 70 messages ; 8 présents à l’identique dans la capture vanilla 02, 62 autres | Essai très précoce, configuration historique et cause de sortie non certifiées ; pas un test complet. |
| Anciens error.4.log / error.5.log | Nombreuses erreurs de parsing/références | Les révisions correspondantes indiquent **1.13.11, 15aa89ae42** ; ne pas les appeler régressions 1.15. |

La déduplication utilise le composant et le message complet, sans l’horodatage ni la ligne C++ du composant. Elle conserve les chemins et lignes de scripts. Les signatures communes ne constituent pas une comparaison de scénarios équivalents.

Les 219 messages vanilla comprennent notamment 8 doublons de textures, 52 messages `gamedatabase.h`, 19 `pdx_persistent_reader.cpp` et 18 `pdx_data_localize.cpp`. Deux clés GUI non localisées figurent déjà dans la référence : `STATE_PRICE_CARD_BALANCE_TOOLTIP` et `MARKET_PRICE_CARD_BALANCE_TOOLTIP`. Les anomalies du jeu local doivent être soustraites avec leur contexte avant attribution au mod. L’intégrité de l’installation par rapport à une distribution officielle n’a pas été contrôlée.

Les anciens essais moddés signalent déjà les collisions de localisation cuivre anglais/français, des doublons CHE/HOH/REB/MSC et deux localisations navales sans BOM. Leur ancienneté varie ; il ne faut pas attribuer toute cette dette à la 1.15.

**Aucun crash fatal du mod en 1.15 n’a été reproduit dans cette mission.** Aucun lancement, arrêt, changement de playset ou contrôle du jeu n’a été effectué par l’agent.

## 4. Triage actionnable

« Confirmé statique » désigne un écart explicitement prouvé par les fichiers et la documentation 1.15. Cela ne certifie pas une conséquence observée en jeu. « Majeur » porte sur le fonctionnement ; « bloquant » sera réservé à un échec de lancement/initialisation démontré.

| ID, état, gravité, issue | Fichiers et lignes | Ancien comportement et attente 1.15 | Correction proposée et validation requise |
| --- | --- | --- | --- |
| D01 — confirmé statique, **majeur / P0**, #21 puis #22 | `common/defines/00_defines.txt:1147`, `:2041` et suivants ; témoin vanilla `:1152`, `:1153`, `:2092` | Surcharge intégrale héritée : `MIN_WAR_SUPPORT = -100` et anciens paramètres d’épuisement/capitulation. Le vanilla utilise un minimum à 0 et de nouveaux paramètres de variation du soutien. Un relevé lexical trouve 263 noms de paramètres du fichier vanilla absents de cette surcharge ; ce nombre est une piste, pas 263 bugs établis. | Faire un diff de migration et isoler les réglages 1776 intentionnels dans une surcharge réduite ; préserver notamment le scénario et l’équilibrage. Vérifier soutien initial, bornes, variations, pénalités, paix et enlisement dans deux conflits. Ne pas simplement recopier toutes les valeurs vanilla. |
| D02 — confirmé statique, **majeur / P0**, #24 avec #21 | `common/journal_entries/1776_usa_french_support.txt:15,17` ; `1776_ottoman_reforms.txt:19,32,41,76,81,85,96,101` ; `1776_imperial_centralization.txt:5,6` ; nombreuses surcharges vanilla | Le mod conserve `complete/on_complete`, `fail/on_fail`, `invalid/on_invalid`. La documentation locale `common/journal_entries/journal_entries.md:138` décrit leur remplacement par des `outcome` associant condition, effet, textes et flags. | Migrer journal par journal en conservant conditions, nettoyage, portée et priorité des conclusions ; traiter aussi les expirations lorsqu’elles existent. Nouveau départ, affichage, conclusion positive/négative/invalidation, absence de double effet, sauvegarde/rechargement. |
| D03 — confirmé statique, **majeur**, #21 / #22 | `events/agitators_events/revolution_events_01.txt:188,213` ; `events/election_events/election_contextual_events.txt:253,294` | Deux effets `add_war_exhaustion` et deux conditions `has_war_exhaustion`. Les équivalents observés sont `add_war_support_change` (vanilla :209,234) et `has_war_support_change` (vanilla :261,303). | Examiner scopes, sens du signe et seuils de chaque branche avant remplacement ; tester les quatre branches avec effets/conditions observés et relire le journal. |
| D04 — confirmé statique, **majeur**, #21 / #22 | `common/treaty_articles/31_toll_exemption.txt:133,139,163,169` ; `32_no_tolls.txt:131,137,161,167` | Huit expressions utilisent `strait_trade_importance_by`, lien remplacé en 1.15. Les calculs vanilla utilisent désormais des notions de dépendance et de grief de péage/accès. | Reprendre la logique d’acceptation de chaque article en tenant compte de ses participants, pas une substitution nominale unique. Tester offre/demande d’exemption, absence de péage et acceptation IA. |
| D05 — confirmé statique, **majeur**, #21 | `common/laws/00_navy_model.txt:17,154` ; `common/power_bloc_principles/00_power_bloc_principles.txt:2069,2098,2120` | Cinq usages de `ship_interest_gain_mult`. Le vanilla emploie `ship_power_projection_mult` et dispose aussi d’une variante additive. | Migrer les cinq modificateurs selon leur intention ; contrôler les infobulles et la projection navale. Toute autre anomalie de loi ou prérequis historique reste du ressort séparé de #17. |
| D06 — collisions confirmées, **risque majeur**, #23 | `common/goods/13_tech6c5b_copper.txt:1` versus vanilla `common/goods/00_goods.txt:314` ; `common/production_method_groups/13_tech6c5b_copper_pmgs.txt:1,11,20,28` versus vanilla `03_mines.txt:183,193,202,210` | Le bien cuivre et quatre groupes ont les mêmes identifiants dans des fichiers différents effectivement présents. Le bien du mod vaut 50, celui du vanilla 40 ; l’ordre effectif ne doit pas être présumé. Les définitions de mine et des six PM partagent aussi des noms, mais leurs fichiers vanilla sont déjà masqués par les surcharges du mod : ce n’est pas le même type de doublon. | Rendre les surcharges intentionnelles non ambiguës ; inspecter la définition résolue en jeu. **Conserver les gisements, capacités, recettes et rendements du mod**, conformément à l’utilisateur ; ne pas importer la répartition vanilla. Vérifier coûts, groupes, PM sélectionnés et marchés. |
| D07 — divergence confirmée, **risque majeur**, #22 | `common/war_goal_types/00_annex_country.txt`, `03_conquer_state.txt:58`, `27_unification.txt` ; témoins vanilla `03_conquer_state.txt:62,101`, `00_annex_country.txt:112`, `27_unification.txt:60` | Les trois surcharges ne contiennent pas les nouveaux blocs `mirrored_wargoal`. Le calcul d’infamie de conquête conserve sa formule antérieure au lieu de `state_infamy_value`. | Diff ciblé des buts et de leurs interactions avec application en cours de guerre et contre-objectifs. Tester la Révolution américaine et un autre conflit, transferts avant la paix, reprise, participants, fronts et résultat final. Ce n’est pas encore une panne observée. |
| D08 — omissions confirmées, **risque majeur à instruire**, #24 | `common/country_definitions/00_countries.txt` masque les entrées vanilla `RSR:81`, `BKH:4180`, `MNL:4789`, `SVN:4805`, `TKI:4817` ; `common/buildings/08_monuments.txt` omet cinq nouveaux monuments russes (vanilla :1526,1555,1584,1613,1642) | Définitions absentes du mod alors que des historiques vanilla 1.15 existent. Plusieurs historiques sont masqués, d’autres peuvent rester hérités ; une absence en 1776 peut être intentionnelle. | Cartographier les consommateurs réellement hérités et leurs gardes DLC avant toute correction. Ne créer aucun TAG, bâtiment initial ni nouveau partage territorial pour faire taire des erreurs. Tester Russie avec DLC activé, puis sans lorsque faisable. |
| D09 — **risque majeur**, #24 / #23 | 16 `map_data/state_regions/*.txt`, `map_data/provinces.png`, terrains, reliefs et rivières ; `gui/goods_state_panel.gui`, `gui/building_details_panel.gui`, `gui/production_methods.gui`, `common/buildings/07_trade.txt` | Anciens fichiers complets peuvent masquer des changements de carte, de navigation, de marchés/hubs et d’interface ; aucune incompatibilité précise de géométrie ou de marché n’a été démontrée ici. | Audit de références/chargement puis inspection d’un échantillon de pays et marchés. Tout correctif cartographique doit être minimal et soumis séparément ; aucune modification de carte dans cette phase. |
| D10 — avertissement confirmé, **mineur**, #20 / #25 | `descriptor.mod:2`, `.metadata/metadata.json:5`, ancien essai moddé `error.1.log:1` | Métadonnées déclarées 1.13 ; avertissement de version sur un exécutable 1.15. | Mettre à jour la déclaration quand la configuration livrée aura été validée. Changer le numéro seul ne constitue pas une migration. |
| D11 — dette observée avant mise à jour, **gravité variable**, #20 puis #21 si reproduit | Exemples des anciens journaux 1.13.11 : `common/production_methods/11_private_infrastructure.txt:99` (`ai_weight`), `common/static_modifiers/1776_land_fortification_construction.txt:5`, `common/dynamic_country_names/00_dynamic_country_names.txt:1293` | Erreurs antérieures de syntaxe, de nombre ou de scope. Elles ne sont pas prouvées nouvelles ni reproduites dans une session complète 1.15. | Conserver la dette séparée ; ne retenir pour le hotfix que ce qui est reproduit et attribué après comparaison de la baseline actuelle. |

Le scan localise **1 395 occurrences candidates de champs de conclusion dans 175 fichiers** : 428 `complete`, 381 `on_complete`, 188 `fail`, 139 `on_fail`, 206 `invalid`, 53 `on_invalid`. Ces localisations sont lexicales, pas un plan de remplacement automatique. Le TSV joint donne les chemins/lignes pour chaque occurrence.
Les **17 occurrences** de commandes/modificateurs/liens retirés des lignes D03–D05 sont également listées séparément.

Faux positif écarté : les trois barres personnalisées utilisent `default = yes`, une forme toujours documentée dans le fichier 1.15 `common/scripted_progress_bars/scripted_progress_bars.md`. Leur rendu reste à tester ; il n’est pas justifié de les déclarer toutes cassées. Le relevé des identifiants de technologies vanilla ne trouve aucun identifiant absent de l’ensemble des définitions du mod ; cela ne valide pas les prérequis, scopes ni profils de départ.

## 5. Exception explicitement autorisée : icônes cuivre

Seules deux lignes ont été modifiées, **sur la branche distante hotfix/1.15** :

| Objet | Fichier | Référence native utilisée |
| --- | --- | --- |
| Bien cuivre | `common/goods/13_tech6c5b_copper.txt:2` | `gfx/interface/icons/goods_icons/copper.dds` |
| Mine de cuivre | `common/buildings/13_tech6c5b_copper_mine.txt:3` | `gfx/interface/icons/building_icons/copper_mine.dds` |

Commits : `8e4ae408b86c3bae67c3ba90f863485e28cd192f`, `0eacee39055e7573b5eb2f725257a77791dcbfac`.
Les commits et les fichiers finaux ont été relus : aucun changement de recette, prix, rendement, capacité, carte ou propriété.
Les six PM miniers partagés utilisaient déjà les textures vanilla correspondantes. Les quatre PM propres au mod de concentration du minerai et de doublage en cuivre n’ont pas d’équivalent direct identifié dans les nouveaux PM cuivre : leurs placeholders restent une dette visuelle.

Contrôles : deux DDS natifs présents, en 256×256 avec 9 niveaux de mipmap ; six DDS de PM présents en 104×104 avec 7 niveaux. Le validateur existant `tools/tech6c5b_validate.py` passe : **675 États, 302 avec potentiel non nul, 373 sans, capacité totale 5 924 niveaux, 16 fichiers, graphe de 290 technologies sans cycle détecté**. Il ne teste ni l’ordre de résolution des définitions vanilla/mod ni le moteur 1.15. La capacité ne représente pas une production hebdomadaire.

Le correctif n’est **pas installé dans le workspace local actif** à cause de l’échec de branche locale. Le patch exact est fourni dans les preuves ; aucune fusion vers main n’a eu lieu.

## 6. Outils existants et portée

| Outil | Utilité et précaution |
| --- | --- |
| `tools/audit_1776_runtime_logs.py` | Lecture des logs actifs/rotations, signatures, et option de lecture de sauvegarde. Sa sélection par mtime ne remplace pas une identification explicite vanilla/mod/version. |
| `tools/vic3-diagnostic-bridge/` | Lecteur local de journaux et télémétrie exportée ; ne lance pas la simulation et ne valide pas les effets moteur. Aucun compagnon de diagnostic ajouté au playset dans cette mission. |
| `tools/tech6c5b_validate.py` | Exécuté, PASS ; contrôle statique cuivre hérité. Ne détecte pas toutes les collisions avec les nouvelles définitions vanilla. |
| `tools/validate_starting_technology_1776.py` | Audit par TAG, sortie optionnelle explicite ; utile après migration ciblée, sans distribution automatique de technologies. |
| `tools/validate_american_revolution_r2.py` à `r6.py` | Régressions de scripts américains ; certaines écritures de rapports imposent de lire leur interface avant exécution. Non lancés ici. |
| `tools/localization_duplicate_audit.py` | Inventaire des doublons ; dette à distinguer des nouveaux conflits cuivre. Aucun nettoyage automatique exécuté. |
| `tools/tech_tree_1776_topology_audit.py` | Peut écrire plusieurs anciens rapports ; non exécuté pour préserver ces suivis. |
| `assess_115.cjs` dans les preuves | Utilitaire nouveau, lecture du mod/vanilla et sorties uniquement dans son dossier diagnostic ; inventaire, empreintes, scan lexical et logs. Ce n’est pas le parseur du jeu. |

## 7. Ordre de traitement proposé après revue

1. **Terminer #20** : lancement vanilla debug achevé, écrans observés, nouvelle partie et premier jour ; capturer avant toute relance. Puis même protocole avec seulement le mod et les mêmes DLC. Conserver le manifeste exact du workspace.
2. **#21**, P0 : définitions de guerre puis commandes/liens/modificateurs retirés, par petits lots testables.
3. **#24, partie journaux/initialisation**, P0 : migrer d’abord les journaux actifs en 1776 et leurs nettoyages, puis les surcharges héritées utilisées.
4. **#22** : guerre américaine et second conflit ; soutien, application des objectifs, contre-objectifs et paix.
5. **#23** : résolution du cuivre et des autres chaînes, marchés, ports, transport et hubs, en conservant le modèle de ressources du mod.
6. **#24, reste du périmètre** : Russie/DLC, interface, références d’États et contrôles cartographiques sans reprise du chantier historique.
7. **#25** : nouvelle partie, plusieurs mois, sauvegarde/rechargement, journaux et économie, liste des erreurs restantes ; déclaration de compatibilité seulement après ces observations.

Tout blocage de lancement effectivement démontré remonte immédiatement avant cet ordre. Aucun travail massif sur #21–#25 n’a été entamé.

## 8. Éléments encore nécessaires

- Fin effective du lancement vanilla debug, observations menu/sélection/premier jour et checksum affiché.
- Journal final vanilla sauvegardé avant le prochain lancement ; les copies actuelles restent provisoires.
- Nouveau lancement **du mod** 1.15 debug, sans autre mod, log intégral, étape exacte atteinte et éventuel crash/gel.
- Liste des DLC réellement chargés et identité du mod/du descripteur local utilisés pour ce test.
- Confirmation visuelle ultérieure du rendu des deux icônes après installation du correctif.
- Pour la future comparaison, conserver les modifications locales existantes ou tester explicitement une branche propre en signalant cette différence : les deux scénarios ne sont pas interchangeables.

## Sources et preuves

Issues lues : [#19](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/19), [#20](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/20), [#21](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/21), [#22](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/22), [#23](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/23), [#24](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/24), [#25](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/25). #17 consultée uniquement pour identifier le périmètre protégé.

[Annonces officielles Paradox sur Steam](https://steamcommunity.com/app/529340/announcements/) : journal de développement #196 du 5 novembre 2026, notes finales 1.15, section Modding ; #194 du 22 octobre, nouveau système de conclusions des journaux. Ces annonces confirment notamment la nouvelle échelle de soutien, l’application d’objectifs durant la guerre, les commandes remplacées et le cuivre natif. Les détails de migration de ce rapport sont aussi confrontés aux scripts et documentations **locaux** de la version installée.

Preuves privées : captures brutes, manifestes SHA-256, inventaire des surcharges, localisations lexicales TSV, comparaison provisoire, utilitaire, validation cuivre et patch d’icônes. Les logs bruts ne sont pas publiés dans GitHub.
