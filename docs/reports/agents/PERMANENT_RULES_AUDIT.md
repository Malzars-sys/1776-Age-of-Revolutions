# Audit des instructions permanentes

Date : 25 octobre 2026. Mission : consolidation documentaire uniquement. Aucun chantier territorial, technologique ou économique n’est repris.

## Méthode et périmètre

Lecture des instructions du dépôt, du guide existant et de ses références, des index `docs/`, puis recherche ciblée des consignes récurrentes dans les feuilles SERG/WORLD, les missions TECH et les rapports démographiques, économiques et graphiques. Inventaire raisonné des règles applicables, pas certification historique exhaustive de tous les rapports. Les prompts archivés dans le dépôt sont des sources ; la mission de consolidation présente fournit l’autorisation de modifier les instructions.

Les empreintes des sources sont dans [SOURCE_INDEX.json](SOURCE_INDEX.json). La capture de protection est dans [WORKSPACE_BASELINE.json](WORKSPACE_BASELINE.json). Elle porte sur les dossiers fonctionnels indiqués et les fichiers racine des principaux suivis ; elle ne prétend pas inventorier chaque fichier binaire de `gfx/` ou chaque ancienne archive. Aucun de ces éléments n’est déplacé dans `.agents/`.

## Instructions existantes conservées

| Emplacement | Règles déjà permanentes | Traitement |
| --- | --- | --- |
| `AGENTS.md` avant consolidation | Lecture du guide, vanilla canonique, exemples comme données, deux passes éditoriales, absence d’étiquette fictive ; protocole SERG, progression, preuves et accord humain | Texte préexistant conservé ; ajout de routage explicite |
| `.agents/agent.md`, préambule et §§ 1–2 | Portée, autorité des consignes, vérité mécanique, contexte 1776, consultation des consommateurs et exemples | Conservé sans réécriture |
| Guide §§ 3–4 | Noms et titres, majuscules, fonctions distinctes des champs d’événement et des options | Conservé sans réécriture |
| Guide §§ 5–6 | Descriptions des technologies, unités, navires et équipements selon leur fonction réelle | Conservé sans réécriture |
| Guide §§ 7–9 | Concepts, effets et conditions d’interface, références dynamiques, diplomatie et scopes réciproques | Conservé sans réécriture |
| Guide § 10 | Explication technique interne puis texte immersif après validation humaine ; suivi éditorial distinct ; pas de changement mécanique | Conservé sans réécriture |
| Guide § 11 | Autres familles : lois, biens, bâtiments, institutions, personnages, scénarios, etc. ; revenir au consommateur pour les cas nouveaux | Conservé sans réécriture |
| Guide § 12 | Français/anglais, idiome, grammaire dynamique, sources natives faillibles | Conservé sans réécriture |
| Guide § 13 | UTF-8 BOM, en-têtes et suffixes, ligne physique unique, échappements, clés, scopes et collisions | Conservé sans réécriture |
| Guide §§ 14–15 | Exemples illustratifs, contrôle des langues et références, dette de doublons, pas de déduplication destructive automatique | Conservé sans réécriture |
| `.agents/references/localisation-vanilla.md` | Références natives observées avec clés et lignes | Conservé comme relevé, sans en faire des instructions de mission |
| Consignes ColGrep fournies dans la session | Préférence de recherche, repli sur `rg`, vérification des pistes locales | Instructions de session respectées ; pas de recopie d’une configuration globale dans le dépôt |

## Règles centralisées

Les identifiants ci-dessous sont ceux des documents spécialisés. Les dispositions communes sont lues pour toute mission ; les autres ne s’appliquent qu’aux domaines explicitement routés par `AGENTS.md`. Aucune valeur locale n’est consacrée comme norme.

| Règle | Destination et contenu | Sources |
| --- | --- | --- |
| W01 | [workflow.md](../../../.agents/workflow.md) — Délimiter la mission autorisée avant toute intervention. | [S02](#s02), [S03](#s03), [S06](#s06) |
| W02 | [workflow.md](../../../.agents/workflow.md) — Par défaut, aucune opération Git d’écriture : staging, commit, push, merge, reset, rebase, changement de branche ou de checkout. | [S03](#s03), [S20](#s20) |
| W03 | [workflow.md](../../../.agents/workflow.md) — Le vanilla canonique est `C:\Games\Victoria 3\game` : consultation seule pour les missions du mod. | [S01](#s01), [S03](#s03) |
| W04 | [workflow.md](../../../.agents/workflow.md) — Avant chaque écriture, relire le contenu courant et contrôler son évolution (empreinte ou comparaison). | [S03](#s03), [S06](#s06), [S13](#s13) |
| W05 | [workflow.md](../../../.agents/workflow.md) — Préserver les travaux approuvés et concurrents, y compris dans un même fichier partagé. | [S02](#s02), [S04](#s04), [S05](#s05), [S21](#s21) |
| R01 | [research.md](../../../.agents/research.md) — Réutiliser d’abord les recherches existantes, puis vérifier les sources nécessaires. | [S05](#s05), [S07](#s07), [S08](#s08), [S09](#s09), [S23](#s23) |
| R02 | [research.md](../../../.agents/research.md) — Pour le scénario initial, raisonner au 1er janvier 1776. | [S02](#s02), [S05](#s05), [S06](#s06), [S07](#s07), [S23](#s23) |
| R03 | [research.md](../../../.agents/research.md) — Décrire les lacunes, périmètres exclus, sources contradictoires et incertitudes. | [S04](#s04), [S07](#s07), [S08](#s08) |
| V01 | [validation.md](../../../.agents/validation.md) — Exécuter les contrôles adaptés au changement sur la version réellement présente. | [S02](#s02), [S03](#s03), [S15](#s15) |
| V02 | [validation.md](../../../.agents/validation.md) — Distinguer incompatibilité de scripts, restriction de construction, incertitude historique, effet économique théorique et panne observée en jeu. | [S03](#s03), [S11](#s11), [S12](#s12) |
| V03 | [validation.md](../../../.agents/validation.md) — Pour une nouvelle installation fonctionnelle en attente de test joueur, utiliser `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` lorsque c’est le statut du suivi. | [S02](#s02), [S03](#s03), [S05](#s05) |
| V04 | [validation.md](../../../.agents/validation.md) — Un reçu humain cite la confirmation et sa source, le sous-lot et la version concernés. | [S02](#s02), [S03](#s03), [S19](#s19) |
| V05 | [validation.md](../../../.agents/validation.md) — Dans une passe autorisée de chantier, mettre à jour ses seules tâches et preuves, ajouter l’historique sans effacer les événements, puis recalculer la progression avec le validateur et le dénominateur canonique. | [S02](#s02), [S05](#s05), [S06](#s06) |
| T01 | [territory.md](../../../.agents/territory.md) — Avant un transfert ou découpage, rapprocher cartes historiques et géométrie actuelle. | [S02](#s02), [S06](#s06), [S23](#s23) |
| T02 | [territory.md](../../../.agents/territory.md) — Distinguer redistribution technique et correction démographique historique. | [S04](#s04), [S05](#s05), [S07](#s07), [S23](#s23) |
| T03 | [territory.md](../../../.agents/territory.md) — Comparer des populations de périmètres compatibles (ville, territoire, Amt, chapitre, possessions incluses/exclues). | [S04](#s04), [S07](#s07) |
| T04 | [territory.md](../../../.agents/territory.md) — Pour tout nouveau TAG, initialiser explicitement un profil technologique historiquement défendable et contrôler les prérequis des bâtiments, PM et unités réellement installés ; aucune copie uniforme d’un voisin ou de sa métropole. | [S02](#s02), [S03](#s03), [S05](#s05), [S09](#s09), [S23](#s23) |
| T05 | [territory.md](../../../.agents/territory.md) — Ne pas déduire désincorporation ou changement politique de la seule population, distance ou optimisation fiscale. | [S14](#s14) |
| S01 | [serg.md](../../../.agents/serg.md) — Au début de chaque passe SERG, lire dans cet ordre `docs/reports/map/SERG_CLOSURE/ROADMAP.md`, `ROADMAP_STATE.json`, `NEXT_ACTION.md`, `BLOCKERS.md`, puis l’historique et les rapports du sous-lot utile. | [S02](#s02) |
| S02 | [serg.md](../../../.agents/serg.md) — Appliquer les trois règles : P0/P1 avant micro-enclaves P2 ; recherche réutilisée et suivie des corrections défendables autorisées ; lots régionaux cohérents divisés en sous-lots indépendamment testables. | [S02](#s02), [S04](#s04), [S24](#s24) |
| S03 | [serg.md](../../../.agents/serg.md) — Préserver les noyaux validés hors régression démontrée. | [S02](#s02) |
| S04 | [serg.md](../../../.agents/serg.md) — En fin de passe SERG, actualiser l’état, les preuves, les événements additifs, la progression calculée et les vues selon l’outil canonique. | [S02](#s02) |
| D01 | [world.md](../../../.agents/world.md) — Avant une passe WORLD, lire sa feuille de route, `ROADMAP_STATE.json`, `NEXT_ACTION.md`, `BLOCKERS.md` et `OWNERSHIP_BOUNDARIES.md` dans `docs/reports/map/WORLD_1776_CLOSURE/`, puis les preuves du lot. | [S05](#s05), [S06](#s06), [S23](#s23) |
| D02 | [world.md](../../../.agents/world.md) — Conserver un suivi indépendant de SERG. | [S06](#s06), [S23](#s23) |
| D03 | [world.md](../../../.agents/world.md) — Respecter l’ordre et les barrières de phase de la feuille canonique. | [S05](#s05) |
| D04 | [world.md](../../../.agents/world.md) — Calculer séparément couverture technique et progression validée par le joueur selon les critères canoniques ; aucun crédit partiel ni `REGION_COMPLETE` avec obligations essentielles ouvertes. | [S05](#s05) |
| K01 | [technology.md](../../../.agents/technology.md) — Examiner le profil explicite et les définitions effectives mod/vanilla. | [S03](#s03), [S09](#s09) |
| K02 | [technology.md](../../../.agents/technology.md) — Distinguer existence d’un bâtiment historique, droit d’en construire, disponibilité d’un PM, sélection initiale explicite, défaut moteur non observé et fonctionnement économique réel. | [S03](#s03) |
| K03 | [technology.md](../../../.agents/technology.md) — Avant une correction de prérequis partagé, auditer ses consommateurs, descendants, profils nationaux et PM initiaux affectés. | [S03](#s03), [S10](#s10) |
| K04 | [technology.md](../../../.agents/technology.md) — Prioriser les incompatibilités explicites et blocages fonctionnels démontrés, puis les anomalies de disponibilité/prérequis, avant le rééquilibrage conjectural. | [S03](#s03) |
| K05 | [technology.md](../../../.agents/technology.md) — TECH prend en charge technologies, prérequis, disponibilité et initialisation des PM ; l’économie conserve les recettes et l’équilibrage. | [S03](#s03), [S06](#s06), [S11](#s11) |
| E01 | [economy.md](../../../.agents/economy.md) — Avant de corriger une chaîne, examiner ses recettes et groupes de PM cumulés : intrants, sorties, emplois, prérequis, niveau construit, capacité de ressource, propriété, accès au marché et demande. | [S03](#s03), [S11](#s11), [S12](#s12) |
| E02 | [economy.md](../../../.agents/economy.md) — Publier les unités et hypothèses des calculs (par niveau, effectif plein ou partiel, semaine/année, prix et salaires), puis une sensibilité pertinente. | [S11](#s11), [S12](#s12) |
| E03 | [economy.md](../../../.agents/economy.md) — Les poids et bornes de substitution des besoins ne sont pas des parts littérales de toutes les dépenses. | [S03](#s03), [S11](#s11), [S12](#s12) |
| A01 | [assets.md](../../../.agents/assets.md) — Conserver les masters finaux approuvés, leur provenance et les DDS utilisés ; le nom `previews/` ne rend pas un master jetable. | [S15](#s15) |
| A02 | [assets.md](../../../.agents/assets.md) — Préserver alpha, proportions, dimensions et stockage attendus par la référence native ; contrôler les mipmaps et références. | [S15](#s15), [S16](#s16), [S17](#s17) |
| A03 | [assets.md](../../../.agents/assets.md) — Distinguer vérification et installation : `tools/rebuild_asset_icons.cjs --verify` contrôle les exports ; `--install-approved --asset=nom_exact` écrit un DDS et exige le périmètre autorisé. | [S15](#s15) |

## Doublons et portée

- Concurrence et anciennes baselines : consigne commune W04, réutilisée par les chantiers sans répéter toutes les listes de pays ou fichiers.
- Statique, moteur et humain : V01–V04 portent le contrat commun ; chaque chantier conserve ses critères canoniques.
- Recherche et estimation : R01–R03 portent la méthode ; T02–T03 précisent la démographie, sans importer de chiffre accepté.
- Suivi : V05 interdit la remise à zéro ; SERG et WORLD conservent des dénominateurs et validateurs distincts.
- Le guide éditorial reste la référence détaillée ; les résumés de routage n’en remplacent pas les sections.

## Remplacements établis et cas non généralisés

Voir [CONFLICTS.md](CONFLICTS.md). Seuls sont reconnus comme remplacements explicites : la politique démographique SERG pour son périmètre, la barrière de test groupé WORLD pour quitter les Balkans, et les décisions locales nouvelles expressément demandées dans leurs lots. Les dates seules ne suffisent pas.

## Éléments exclus des instructions permanentes

Restent dans `docs/` : frontières et souverainetés particulières, données démographiques, chiffres d’économie et recettes, parents exacts d’un nœud technologique, coordonnées/RGB, listes de témoins et noyaux, attestations humaines, historiques, scores, preuves, versions de moteur constatées et résultats de tests. Une suggestion de désincorporation n’est pas une autorisation. Les recherches préliminaires non vérifiées ne deviennent pas une source historique validée.

Aucune validation, installation ou progression nouvelle n’est accordée par cette consolidation.

## Sources documentaires

### S01

[.agents/agent.md](../../../.agents/agent.md)

§§ Référence vanilla, Portée, 1–15 ; guide éditorial existant conservé intégralement.

### S02

[docs/reports/map/SERG_CLOSURE/ROADMAP.md](../../../docs/reports/map/SERG_CLOSURE/ROADMAP.md)

Lignes 7–16, 48–58, 890–908 : protocole, profils, preuves, progression et référence canonique.

### S03

[docs/reports/technology/STARTING_TECH_AUDIT_1776_R3/USER_MISSION.txt](../../../docs/reports/technology/STARTING_TECH_AUDIT_1776_R3/USER_MISSION.txt)

§§ 1–3, 5–6, 10–20 et 22 : attestations, disponibilité, concurrence, version, contrôles et Git.

### S04

[docs/reports/map/MAP_POPULATION_POLICY.md](../../../docs/reports/map/MAP_POPULATION_POLICY.md)

Règle prioritaire et justification : remplacement explicite des anciennes contraintes, limité au Saint-Empire.

### S05

[docs/reports/map/WORLD_1776_CLOSURE/ROADMAP.md](../../../docs/reports/map/WORLD_1776_CLOSURE/ROADMAP.md)

Reprise, progression, phases et Consigne prioritaire du joueur — 24 octobre 2026.

### S06

[docs/reports/map/WORLD_1776_CLOSURE/OWNERSHIP_BOUNDARIES.md](../../../docs/reports/map/WORLD_1776_CLOSURE/OWNERSHIP_BOUNDARIES.md)

Répartition, interfaces réservées et fichiers partagés ; seuls les principes sont centralisés.

### S07

[docs/reports/map/MAP2Q/CONTINUATION_R2/POPULATION_METHODOLOGY.md](../../../docs/reports/map/MAP2Q/CONTINUATION_R2/POPULATION_METHODOLOGY.md)

Périmètre, comparabilité, interpolation, incertitudes, non-double comptage et bilan mondial.

### S08

[docs/research/technology/README.md](../../../docs/research/technology/README.md)

Statuts de recherche : usage préparatoire, bibliographie non vérifiée, aucune autorité historique automatique.

### S09

[docs/reports/technology/recherche régional/TECH_START_1776_AMERICAS_CARIBBEAN_RESEARCH.md](../../../docs/reports/technology/recherche%20régional/TECH_START_1776_AMERICAS_CARIBBEAN_RESEARCH.md)

Méthode : effets réels, invention/diffusion/institutionnalisation et profils coloniaux.

### S10

[docs/reports/technology/recherche régional/TECH_START_1776_WORLD_SYNTHESIS.md](../../../docs/reports/technology/recherche%20régional/TECH_START_1776_WORLD_SYNTHESIS.md)

Dette de prérequis et refus de la fermeture automatique des profils nationaux.

### S11

[docs/reports/economy/ALLOYS_1776_REBALANCE/REPORT.md](../../../docs/reports/economy/ALLOYS_1776_REBALANCE/REPORT.md)

§§ Bien courant, besoins domestiques, rentabilité, coexistence, validation restante.

### S12

[docs/reports/economy/ALLOYS_1776_REBALANCE/BALANCE_REVIEW.md](../../../docs/reports/economy/ALLOYS_1776_REBALANCE/BALANCE_REVIEW.md)

Lignes 3–20 : unités, hypothèses, calcul du groupe et sensibilité aux prix.

### S13

[docs/reports/economy/ECON_PAPER_1776/REPORT.md](../../../docs/reports/economy/ECON_PAPER_1776/REPORT.md)

§ Fichiers : comparaison des blocs, changements bornés et conservation des données étrangères.

### S14

[docs/reports/buildings/BUILD_START_1776_DEINCORPORATION_HISTORICAL_CRITERIA.md](../../../docs/reports/buildings/BUILD_START_1776_DEINCORPORATION_HISTORICAL_CRITERIA.md)

Critères historiques, raccourcis exclus et statut diagnostique ; aucune autorisation de modification.

### S15

[docs/reports/assets/README.md](../../../docs/reports/assets/README.md)

§§ Sources, cache, reconstruction, double flèche et palette ; règles de méthode séparées des installations datées.

### S16

[docs/reports/assets/pm_palette_rules.json](../../../docs/reports/assets/pm_palette_rules.json)

Contrat de palettes et politique de validation des dessins individuels.

### S17

[docs/reports/assets/HARDWARE_PM_ICONS/REPORT.md](../../../docs/reports/assets/HARDWARE_PM_ICONS/REPORT.md)

Demande particulière du joueur, palette rouge et quatre dessins ; exception locale non généralisée.

### S18

[tools/serg_closure_roadmap.py](../../../tools/serg_closure_roadmap.py)

terminal_evidence / partial_runtime_evidence, notamment lignes 248–249 et 274 ; schéma technique, pas preuve du test.

### S19

[docs/reports/map/SERG_CLOSURE/SC1-REGENSBURG-DEMOGRAPHY/RUNTIME_USER_ATTESTATION_2026_10_25.json](../../../docs/reports/map/SERG_CLOSURE/SC1-REGENSBURG-DEMOGRAPHY/RUNTIME_USER_ATTESTATION_2026_10_25.json)

Confirmation brève, explicitly_reported, protocol, new_game_date et simulation_months : cas d’arbitrage, non modifié.

### S20

[docs/reports/technology/TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_REPORT.md](../../../docs/reports/technology/TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_REPORT.md)

Ancienne création de branche : action contextualisée, pas permission Git permanente.

### S21

[docs/reports/README.md](../../../docs/reports/README.md)

Index des familles de rapports, validations et crédits.

### S22

[.agents/references/localisation-vanilla.md](../../../.agents/references/localisation-vanilla.md)

Relevé des exemples natifs : observations de référence, pas nouvelle autorité de mission.

### S23

[docs/reports/map/WORLD_1776_CLOSURE/USER_MISSION.txt](../../../docs/reports/map/WORLD_1776_CLOSURE/USER_MISSION.txt)

§§ 5, 11–19 : méthode historique, TAGs, démographie, blocs testables, frontières, preuves ; transition initiale remplacée selon S05.

### S24

[docs/reports/map/SERG_CLOSURE/SC2-INNER-AUSTRIA/USER_MISSION_2026_10_19.txt](../../../docs/reports/map/SERG_CLOSURE/SC2-INNER-AUSTRIA/USER_MISSION_2026_10_19.txt)

Trois règles permanentes, approximation B documentée et absence de validation automatique.
