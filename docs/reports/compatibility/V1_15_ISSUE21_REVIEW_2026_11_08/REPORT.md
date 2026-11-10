# Mission 21 — implémentation terminée, review

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — 8 novembre 2026.** Les cinq tâches d'implémentation de la mission sont terminées : **5/5, soit 100 % côté code**. Le sixième point d'origine, les essais moteur, reste différé à la passe groupée demandée par le mainteneur. Ce chiffre ne signifie ni validation moteur, ni acceptation de tous les contenus 1.15. La mission doit rester ouverte en **In review**.

Demande : « Je ferai les tests moteurs quand on atteindra la limite de choses en review. Donc, continue la mission 21 jusqu'à ce qu'elle est finie pour la passer à 100% en review. » Aucun lancement ou pilotage du jeu effectué par cet agent.

## Version, périmètre et sources

- Entrée du workspace : `0396b1133168c1721b61cee5ae5334f1a4f5e4e1`, branche observée `main`. Cette révision a été constatée, pas créée par cette mission. Le rapport non suivi du lot précédent de proportions de population et le chantier économique concurrent #23 ont été préservés.
- Vanilla canonique consulté en lecture seule : `C:/Games/Victoria 3/game`. Exécutable observé : **1.15.0** ; captures de `code_revisions` : `release/1.15.0`, build **6338547985**. `ENGINE_VERSION_OBSERVED.json` conserve les en-têtes et empreintes réellement lus.
- [Notes officielles de la mise à jour 1.15, Dev Diary 196](https://steamcommunity.com/app/529340/announcements/) : révision du soutien de guerre, cible pays des proportions de cultures primaires, portée militaire de l'IA et nouveaux liens de détroits. La lecture du digest a servi d'index ; les remplacements ci-dessous sont vérifiés dans les fournisseurs locaux effectifs, pas déduits d'un nom ressemblant.
- Les contrats précis, fichiers natifs et empreintes sont conservés sous `native/` et dans `NATIVE_REFERENCES.json`. `MIGRATIONS.json` documente chaque ancien site, son contexte, la transformation exacte et sa raison. `CHANGES.patch` comprend aussi les sept nouveaux fichiers.

La passe couvre les API obsolètes identifiées par les logs capturés et l'inventaire global des familles concernées sous `common/` et `events/`. Elle ne constitue pas une conversion intégrale de tous les contenus, pays, lois, portraits et journaux du mod vers 1836 vanilla.

## Corrections de cette continuation

**229 interventions bornées dans 34 fichiers existants, plus 7 nouveaux fichiers de support.** Les instantanés `before/`, les candidats installés `candidate/` et `INSTALLED_FILES.json` permettent de contrôler les octets et les différences. Les seules corrections d'indentation concernent les lignes déjà modifiées ; BOM et fins de ligne des fichiers existants sont conservés.

| Famille | Sites | Migration et sens conservé |
| --- | ---: | --- |
| Portée militaire de l'IA | 33 | 24 cibles pays et 9 cibles états, vers les helpers natifs de conquête, soumission, contrainte ou protection selon chaque usage. Les refus restent des `NOT`, les cibles sont explicites. |
| Désir territorial de l'IA | 2 | Désir fort vers `ai_state_has_core_ambition` ; désir général vers l'union des ambitions natives. Les scores, bonus historiques et multiplicateurs existants restent en place. |
| Cultures primaires des décrets | 6 | Bloc avec `target_country = owner` et `value`, mêmes opérateurs et fractions. Les deux appels déjà corrects de la stratégie par défaut restent inchangés. |
| Détroits des actions diplomatiques | 4 | Dans le scope du pays cible : possession hiérarchique et contrôle évalués avec un booléen, comme dans les actions natives. |
| Pertes et soutien de guerre | 3 | Deux principes et la technologie de télégraphe militaire : `country_war_support_casualties_mult`, valeurs **−0,15 / −0,15 / −0,25** conservées. Aucun prérequis technologique modifié. |
| Rôles de personnages | 91 | Anciennes valeurs `admiral/general/politician/agitator` de `has_role` vers `has_role_of_type`. Les véritables identifiants `character_role_*` ne sont pas modifiés. |
| Souverain et héritier | 35 | 27 `is_ruler` et 8 `is_heir` vers les prédicats natifs relatifs au pays du personnage, mêmes booléens. |
| Dates | 8 | `current_date` vers `game_date`, sans déplacer les bornes des noms dynamiques ni la fenêtre d'initialisation des fortifications. |
| Navires | 20 | 8 proportions pays et 12 proportions de flotte vers les proportions de types de navires et leurs cibles typées `ship_type:`. Fractions et opérateurs conservés. |
| Ports | 2 | `has_port_state`, dans les mêmes états et avec les mêmes booléens. |
| Itérateurs ibériques | 2 | Itérateur natif `every_country_in_iberia_old`, correspondant à la liste géographique de l'ancienne région ibérique. Conditions et effets inchangés. |
| Anciens callbacks | 4 | Suppression d'une branche morte d'objectifs IA du Grand Jeu ; deux appels de succession EIC vers un helper local ; modernisateurs vers le helper actuel, au scope pays propriétaire de la loi. |
| Principes impériaux | 3 | Retrait des trois clés malformées contenant `REPLACE_OR_CREATE:` à l'intérieur d'un nom de modificateur. Un seul rabais de sécurité au travail reste présent par palier : **−10 / −20 / −30 %**. |
| Poids IA neutres des PM | 16 | Retrait des seuls `ai_weight = 1` rejetés par le parseur observé. Aucune recette, technologie, affectation initiale ou autre valeur du PM modifiée. |

### Décisions nécessitant une attention en review

**Types de navires.** Il n'existe pas une substitution universelle correcte pour l'ancien type « battleship ». Les événements du canular naval et du Potemkine ciblent les pré-dreadnoughts dans leurs équivalents natifs. `naval_tech_events.3` cible spécifiquement les **super-dreadnoughts**. Les porte-avions utilisent `ship_type_aircraft_carrier`. Les cinq événements technologiques sont contrôlés individuellement contre leurs propres objets natifs ; une cible valide mais incorrecte pour son événement est rejetée par le contrôle négatif.

**Ambitions de l'IA.** Le désir général est représenté par l'union des neuf ambitions natives, les cinq ambitions fondamentales étant regroupées dans `ai_state_has_core_ambition`. Il s'agit du remplacement explicite du prédicat supprimé, en conservant le calcul 1776 autour de cette condition. Cette passe n'importe pas toute la nouvelle formule vanilla des valeurs territoriales.

**Fonctions masquées.** L'inventaire des fournisseurs trouve 24 définitions natives masquées par les anciens fichiers du mod ; quatre sont utilisées dans les consommateurs effectifs observés. Seules ces quatre fonctions et une dépendance de préparation de l'exil sont restaurées, avec des corps identiques aux natifs : protection temporaire d'un personnage, révocation, exil vers un pool et éligibilité socialiste étatique. Le fallback mensuel d'expiration est également repris, via une action enfant additive. Il évite de rendre permanente une protection dont l'événement ne termine pas normalement ; le cas déjà immortel reste distingué par les fonctions natives. Aucun remplacement complet de fichier de helpers n'a été fait.

**Succession EIC.** La politique déjà écrite dans les deux callbacks du mod reste en place : promotion du chef industrialiste au poste de souverain, puis création de son successeur de groupe avec `create_character`, `ig_leader = yes`, `interest_group = ig_industrialists`. Le helper est local et nommé `aor1776_generate_eic_government_leader`. Ce fallback restaure l'opération manquante ; il ne prétend pas reproduire une ancienne liste de personnages nommés. Aucun gouvernement ou pays initial n'est réécrit.

**Score social-démocrate.** Les quatre lectures existantes de `owner.ideology_social_democrat_disfavoured_laws` étaient dépourvues de fournisseur en 1.15. L'idéologie propre au mod est conservée. Un score local compte un point par groupe de lois à son avis le moins favorable, suivant l'unité de comptage des valeurs natives : **0 à 7**, avec les positions réellement présentes dans les sept groupes du mod. `SOCIAL_DEMOCRAT_SCORE.json` décrit les lois comptées. Ce choix rétablit un fournisseur cohérent avec l'idéologie conservée ; aucune identité parfaite avec un ancien calcul disparu n'est revendiquée. Les soutiens, positions législatives, poids et lois initiales ne sont pas modifiés.

**Modificateurs manquants.** Les types de débit de carrière de calcaire et de coût de l'institution de sécurité au travail sont enregistrés explicitement, sur le modèle des types vanilla analogues. Les bâtiments et institutions cibles existent. Les effets déjà écrits restent de **+15 %** pour la compagnie concernée et **−10 / −20 / −30 %** pour les principes. Les libellés et descriptions sont fournis en français et en anglais.

**Documentation des PM contradictoire.** `production_methods.md` mentionne encore `ai_weight = fixed_point`, par défaut 1.0. La capture 1.15 contient pourtant les rejets exacts des 16 champs scalaires actuels, dont celui de `pm_no_rail_network`. Les exemples natifs n'utilisent pas ce champ. Le retrait des valeurs neutres redondantes satisfait les deux interprétations sans introduire de préférence économique nouvelle. La disparition effective des messages reste à confirmer après redémarrage.

## Contrôles exécutés

| Vérification | Résultat effectif |
| --- | --- |
| `python -B tools/compatibility/issue21_api_audit.py` | **485/485**, statique uniquement ; aucune occurrence des API retirées auditées. |
| Contrôles négatifs de cette passe, substitutions en mémoire | **5/5 détectés** : mauvaise cible navale pourtant valide, mauvaise portée pour une guerre limitée, protection d'un personnage déjà immortel inversée, expiration neutralisée, valeur IA hors périmètre modifiée. |
| Préservation hors lot | **2 875 fichiers** contrôlés par empreinte ; aucune évolution concurrente de ces fichiers observée au contrôle final. |
| Définitions, mission 26 | **1 732/1 732**, statique. |
| Effets de guerre, mission 28 | **38/38**, et **10/10** contrôles négatifs détectés. |
| Péages, mission 29 | **86/86**, et **10/10** contrôles négatifs détectés. |
| Objectifs de guerre, mission 32, témoin externe | **27/27**, et **12/12** contrôles négatifs détectés. |
| Mission 30, projection navale | Contrôle original brut : **15/16**, seul échec sur l'empreinte de tous les autres tokens du fichier de principes. C'est la conséquence attendue des deux clés de pertes désormais migrées ici. Contrôle isolant l'état antérieur de ces seules clés : **16/16**. Les cinq valeurs de projection navale sont préservées. Le contrôle original n'a pas été modifié pour masquer cet écart. |
| `git --no-optional-locks diff --check` | Aucun diagnostic final. |

Les résultats bruts sont conservés dans `VALIDATION_INSTALLED.json`, `NEGATIVE_CONTROLS.json`, `DEFINES_RECHECK.json`, `PRIOR_LOTS_BEFORE.json`, `PRIOR_LOTS_AFTER.json`, `PRIOR_LOTS_NEGATIVE_CONTROLS.json` et `TOLL_RECHECK.json`. Les appels Python ponctuels utilisent le parseur du dépôt et le runtime Python disponible. Le validateur répétable est en lecture seule par défaut ; `--output` écrit seulement son rapport.

## Erreurs restantes et frontières entre missions

`LOGS_BEFORE.json` est une capture d'entrée avec les empreintes et dates de fichiers, pas une mesure après correctif. Le jeu a été relancé par ailleurs pendant le travail ; aucune baisse de décompte ni résultat sur le code final n'en est déduit. Le suivi `LOG_TRIAGE.json` classe les familles et conserve leurs sites.

- **Mission 27** : champs directs de conclusion et de présentation des journaux (`complete/on_complete/fail/...`). Les journaux touchés ici pour une condition de rôle ne sont pas déclarés entièrement fonctionnels. Le lot précédent des quatre proportions de population reste documenté séparément.
- **Mission 24**, avec coordination de **17** pour toute décision de politique historique : définitions de lois, idéologies, personnages, traits, journaux et contenus DLC manquants derrière des références natives ou héritées. Restaurer une API de rôle ou un helper n'ajoute pas automatiquement ces données. Aucun choix de loi initiale ou historique n'est modifié dans cette passe.
- **Missions 23/24** : anciennes références à `building_naval_base` dans les événements et l'IA. Les contrats de proportions navales sont corrigés ici ; le remplacement du bâtiment et la conversion de ses seuils restent un chantier de données navales à traiter explicitement. Aucun événement concerné n'est certifié jouable sur la seule correction du trigger.
- **Mission 24 / contrôle 20** : erreurs de cultures, religions et régions dans des scopes hérités. La présence de `region` dans le vanilla courant empêche de le traiter comme un mot-clé supprimé. Leur cause doit être isolée avec les données de carte/pays et un contrôle vanilla, pas par une substitution générale.
- **Mission 25** : validation globale du démarrage, sauvegardes, simulation et intégration. Les identifiants manquants de notifications, les assets et l'audio ne sont pas renommés au hasard alors que leurs API restent natives.

Le chantier #23 a publié un audit de références économiques pendant cette passe. Ses sources et résultats n'ont pas été réécrits ici. Les trois suppressions de champs neutres de PM ci-dessus sont postérieures à sa baseline ; ce décalage de lecture est explicite et n'affecte ni ses recettes ni ses cibles économiques.

## État de livraison

Implémentation #21 : **100 %** ; essais et acceptation moteur : **en attente**, selon `RUNTIME_PROTOCOL.md`. Le compteur GitHub de sous-issues est distinct : #26 et #28 sont fermées, #29 et #30 restent ouvertes en review pour leurs essais. Il peut donc encore afficher **2/4, 50 %**, sans que cela représente la part de code restant à écrire. Les fermer uniquement pour changer ce compteur certifierait une acceptation non obtenue.

Toutes les corrections sont installées localement et reviewables. Aucun fichier vanilla modifié, aucune opération Git d'écriture, aucun commit, push, changement de branche ou merge effectué par cette mission. Les preuves et changements de cette continuation ne sont pas encore publiés dans une nouvelle PR. Une ancienne PR ne doit pas être présentée comme contenant ces nouveaux fichiers.
