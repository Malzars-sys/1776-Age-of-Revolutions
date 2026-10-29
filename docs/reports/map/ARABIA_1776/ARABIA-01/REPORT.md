# ARABIA-01 — Première installation territoriale, 1er janvier 1776

**Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Installation du 29 octobre 2026. Aucune validation en jeu réalisée ou attribuée au joueur pour ce lot.

## Résultat installé

- Réactivation de **NEJ, Émirat de Diriyah**, sur cinq provinces du noyau Riyad/Diriyah–Washm–Sudayr. Abdulaziz ben Muhammad ben Saoud remplace les personnages vanilla de 1836 ; l'âge est une approximation à partir de l'année 1720.
- Création de **A91, Banu Khalid**, sur vingt provinces côtières et oasiennes : dix-sept de `STATE_HAIL`, trois de `STATE_NEJD`. Il s'agit du noyau al-Hasa/Qatif, pas d'une certification de toutes les zones d'influence tribale. Souverain personnel non nommé faute de succession suffisamment vérifiée après 1774.
- Création de **A92, Communautés du Qatar**, sur deux provinces de `STATE_ABU_DHABI`. Ensemble décentralisé collectif ; ce n'est ni un État Al Thani ni une conquête de Bahreïn anticipée.
- **BHN** conserve l'île de Bahreïn, sous un nouveau lien de sujet envers **PER**. Le pacte `puppet` sert d'approximation du gouvernorat perse de Nasr al-Madhkur ; ses droits et prélèvements vanilla ne sont pas un traité historique reproduit.
- Les cinq provinces yéménites de Tihama précédemment données à **HDJ** passent à **ZAI**. Le reste du Hedjaz et sa relation ottomane sont préservés, ainsi que Lahj, Mahra, Hadramawt et Oman existants.

Total : **32 transferts de provinces**, deux nouveaux TAGs et un TAG réactivé. Aucun State_ID ni RGB nouveau ; bitmap inchangé. Les nouvelles bannières sont décoratives, pas des drapeaux historiques attestés.

## Population, économie et démarrage

Le stock entier du fichier moyen-oriental reste de **17 882 499 habitants avant/après**, sans ajout démographique. Toutes les combinaisons culture/religion/statut et leurs effectifs sont conservées à l'échelle de chaque State_ID. La répartition entre propriétaires au Najd et au Qatar est un **choix technique de gameplay**, pas un recensement de 1776 ni une estimation par surface. Voir `POP_REDISTRIBUTION_LEDGER.json`. Les catégories héritées discutables, dont les 231 Bédouins orthodoxes orientaux, n'ont pas été effacées ni présentées comme vérifiées historiquement.

| Région du jeu | Populations initiales après transfert |
| --- | --- |
| STATE_NEJD | NEJ : 53 000, A91 : 29 700, NBB : 21 847 |
| STATE_HAIL | JBB : 39 012, A91 : 61 914 |
| STATE_HEDJAZ | HDJ : 393 635 |
| STATE_OMAN | OMA : 198 900 |
| STATE_ABU_DHABI | ABB : 51 102, OMA : 4 106, BHN : 15 619, A92 : 9 286 |
| STATE_YEMEN | ZAI : 859 690, MBB : 30 770, KBB : 37 315, LAH : 62 985 |

Les niveaux des bâtiments civils déjà présents sont conservés dans les deux fichiers qui les déclarent. Le ranch et la route du Najd vont à NEJ, le ranch côtier à A91, la pêche du bloc BHN à A92. Les plantations de café ZAI et HDJ sont fusionnées à trois niveaux pour éviter deux créations concurrentes du même bâtiment ; le port de Tihama est transféré à ZAI. Les participations de propriété suivent les nouveaux détenteurs.

Ajouts explicites : **un port commercial traditionnel A91 et un BHN**, sans chantier naval moderne ; **une unité de conscription irrégulière NEJ et une A91**. Ces deux levées sont des minima de gameplay, pas une mesure des armées de 1776. Aucun habitant n'est ajouté pour les créer. Le recrutement est confié au mécanisme natif, sans caserne dupliquée dans l'histoire civile.

Profils technologiques explicites modestes pour NEJ/A91/A92, sans copie d'un palier industriel. Le commerce caravanier et côtier utilise une variante locale du mercantilisme, limitée à ces TAGs et sans exiger une technologie bancaire postérieure. Les autres lois génériques restent des abstractions du moteur, pas une description exhaustive de leurs institutions historiques.

**Accès au marché, emploi, nourriture et rentabilité ne sont pas certifiés par ces fichiers.** Bahreïn nécessite le contrôle maritime ci-dessous. Les capitaux des portions partagées et les ports secondaires peuvent être déplacés par les choix de hubs du moteur.

## Vérifications exécutées

Commandes : `tools/arabia01.py --plan`, `tools/arabia01_install.py --prepare`, `--apply`, `--repair-profiles`, `--audit`, puis `tools/arabia01_closeout.py`, avec le Python local. Préparation en staging, sauvegarde de chaque préimage et comparaison de toutes les empreintes avant écriture. Pas de restauration générale d'une baseline ancienne.

- **45 contrôles ciblés réussis** dans `VALIDATION.json` : les 32 changements correspondent au plan ; les 637 provinces des six régions ont chacune un propriétaire ; aucune cellule cible impassable ; noyaux NEJ/A91/A92 connectés par des arêtes de pixels.
- Stock de POPs et niveaux civils conservés ; contenus syntaxiques des régions extérieures identiques aux préimages dans les quatre fichiers partagés.
- NEJ/A91/A92 : `PASS_STATIC_ONLY` pour technologies, recettes, lois demandées et unités. Les premières erreurs détectées sur les nouveaux profils ont été corrigées ; les résultats finaux ne les masquent pas par suppression des contrôles.
- Définitions et références nouvelles, localisation française/anglaise avec BOM et clés uniques, bannières et souverain NEJ contrôlés séparément dans `REFERENCE_AUDIT.json` et `LOCALIZATION_AUDIT.json`.
- Les pays hérités NBB/BHN/ZAI/HDJ gardent des avertissements ou erreurs antérieurs, notamment des demandes de lois avec prérequis absents. `TECH_BEFORE.json`, `TECH_AFTER.json`, `TECH_DELTA.json` et `PREEXISTING_WARNINGS.json` les distinguent : **aucun nouveau signal dans ces pays**. Ce lot ne rend pas l'ensemble du Moyen-Orient techniquement exempt de dette.
- Changements de runtime concurrents hors fichiers de ce lot depuis la préparation : **8**, conservés et recensés dans `CONCURRENT_RUNTIME_DELTA.json`. Les travaux africains présents avant la préparation ne sont pas écrasés. Aucun fichier des corrections américaines, du suivi WORLD ou du SERG n'a été édité par ce lot.

Un contrôle statique n'est ni un chargement moteur, ni une validation visuelle, ni une homologation humaine. Les détails de quartiers, les villes historiques supplémentaires et les frontières exactes ne sont pas créés par les repères de l'aperçu.

## Réserves et suite bornée

1. **Koweït** : le RGB natif du port `x00F060`, `STATE_BASRA`, reste IR1. Lorimer p. 1002 le décrit comme dépendant de Bassora en 1775, tout en attestant une chefferie locale Sabah. Le degré de dépendance à traduire en pacte, le partage démographique et le port de Bassora doivent être traités ensemble. Ne pas installer une indépendance pleine sur le seul nom du chef.
2. **Qawasim / Musandam** : le repère de Ras al-Khaimah et Khasab partagent `x0DC972`. Le transfert intégral ferait perdre Musandam à Oman sans preuve. Un découpage de province doit précéder une correction sûre.
3. **Qasim et frontières intérieures** : chronologies contradictoires et contrôle tribal discontinu ; aucune extension saoudienne maximale des années 1780–1810 anticipée. Les enveloppes des provinces restent des approximations.
4. **Oman, Bani Yas, Asir et chefferies méridionales** : les noyaux existants sont conservés ; la granularité tribale et les dépendances ne sont pas déclarées historiquement closes.
5. Démographie fine, équilibre fiscal et militaire, placement de hubs secondaires : réserves ouvertes. Les coordonnées modernes des aperçus ne créent pas de villes accessibles à la recherche interne.

Ce lot ne clôture donc pas la péninsule à 100 %. La prochaine passe territoriale utile est **Koweït et interface du Golfe**, puis le découpage Qawasim/Musandam après correspondance historique plus précise. Aucun dénominateur WORLD ou SERG n'a été modifié pour lui donner des points.

## Fichiers de runtime modifiés ou créés

- `common/history/states/00_states.txt`
- `common/history/pops/08_middle_east.txt`
- `common/history/buildings/08_middle_east.txt`
- `common/history/buildings/98_build_start_1776_world_redistribution.txt`
- `common/country_definitions/1776_arabia01.txt`
- `common/history/countries/1776_arabia01.txt`
- `common/history/diplomacy/1776_arabia01.txt`
- `common/history/characters/nej - nejd.txt`
- `common/flag_definitions/1776_arabia01.txt`
- `common/coat_of_arms/coat_of_arms/1776_arabia01.txt`
- `common/history/buildings/1776_arabia01.txt`
- `common/history/military_formations/1776_arabia01.txt`
- `localization/french/replace/1776_arabia01_l_french.yml`
- `localization/english/replace/1776_arabia01_l_english.yml`
- `common/country_definitions/00_countries.txt`
- `common/history/countries/nej - nejd.txt`
- `common/laws/1776_arabia01.txt`

Outils et preuves : `tools/arabia01.py`, `tools/arabia01_install.py`, `tools/arabia01_closeout.py` et ce dossier. `PREPARED.json`, `APPLIED.json`, les préimages et les reçus de réparation conservent la trace des versions. Aucun commit, merge, rebase ou push. Vanilla consulté en lecture seule.

## ColGrep local

Un appel exploratoire `C:/Users/simeo/.cargo/bin/colgrep.exe --agent <question de localisation Arabie> .` a été tenté. Échec après environ **1,94 seconde**, au verrou d'index sous `%APPDATA%/colgrep/indices/1776_Age_of_Revolutions_fork-9f9c61cb/.lock`, accès refusé (erreur système 5). Aucune configuration ni intégration modifiée, aucun index reconstruit, aucun modèle installé. Repli sur `rg` et lecture ciblée des dossiers R3 et des dépendances.

**L'exécution du modèle 2B n'est pas confirmée pour cette passe.** Aucun décompte fiable des recherches classiques ou des tokens Codex n'est exposé ; aucune économie de quota n'est revendiquée.
