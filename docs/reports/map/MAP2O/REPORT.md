# MAP-2O — Emden et noyau côtier de Frise orientale

Date : 16 octobre 2026. Situation historique cible : 1er janvier 1776.

**MAP2O_PARTIAL — correction appliquée, validation statique séparée dans VALIDATION.json. Aucun test moteur de MAP2O.**

## Modification installée

| Province | State_ID | Avant | Après | Cellules | Géométrie |
|---|---|---|---|---:|---|
| xF9DCA2 | STATE_HANNOVER, définition numérique 69 | HAN | PRU | 319 | Inchangée |

Le noyau côtier d'Emden devient prussien. Le transfert est une **simplification B par province existante**, pas un tracé cadastral ni une certification de chaque cellule. Aucun nouveau RGB, aucune recoloration, aucun corridor et aucune modification physique de côte ou d'île. La province reste dans le grand État partagé de Hanovre ; cet État administratif du jeu n'implique pas une souveraineté hanovrienne.

Le nombre de 319 résulte de la conservation de l'enveloppe existante après examen des voisins, et non de l'utilisation du seul locator portuaire. La carte Schenk conservée montre un ensemble côtier distinct à l'ouest de Jever/Oldenburg et au nord du Niederstift ; les archives prussiennes établissent sa souveraineté depuis 1744. Cette correspondance est qualitative à l'échelle du jeu : aucune transformation locale suffisamment vérifiée n'a permis de figer une nouvelle ligne pixel par pixel. Le profil baltique de MAP2M n'est pas extrapolé ici comme une vérité géographique.

**Ce résultat ne termine pas toute la Frise orientale historique.** Leer, le Rheiderland, la marge méridionale et la restitution distincte des petites juridictions orientales restent ouverts. Ne pas interpréter la conservation des voisins comme une validation historique de leurs frontières actuelles. Voir UNRESOLVED.csv.

## Conservation et dépendances

- 142 528 habitants sont réaffectés de HAN à PRU dans STATE_HANNOVER. Allocation entière déterministe par profil, au prorata de 319/1 618 cellules de la subdivision HAN initiale ; plus forts restes. Il s'agit d'une allocation technique, pas d'un recensement historique d'Emden.
- Aucun habitant ajouté : total mondial 835 804 980. Cultures, religions explicites et religions par défaut conservées.
- Bâtiments, niveaux, PM, propriétés économiques, infrastructures, formations et recrutements conservés. Aucun port construit ou déplacé : il n'y avait pas de bâtiment portuaire HAN à transférer dans cet État.
- Hub portuaire natif 69 : X 4256,644043 ; Y bitmap 748,069336. Il reste sur xF9DCA2, désormais PRU. Cette coordonnée n'est pas certifiée comme centre historique d'Emden.
- Registre impérial : 504 entrées, une seule modification de titulaire, HAN → PRU pour xF9DCA2. L'étendue territoriale impériale et les deux cartes DDS restent identiques. Aucune autre possession prussienne ajoutée au SERG.
- Les conditions et effets de rétrocession, prévisualisation et mémorisation de réponse ciblant ce RGB sont adaptés à PRU ; les autres mécanismes impériaux restent intacts.
- MAP2N et la Poméranie suédoise sont protégés par comparaison avec l'état courant figé. L'acceptation manuelle MAP2N est rappelée par attestation additive, sans modifier les anciennes preuves ni prétendre à un test moteur automatisé.
- Prototype de pont et compagnon d'infrastructures conservés sans modification. Aucun changement de HEAD/index Git, commit, push ou fichier d'installation du jeu.

## Fichiers modifiés pour le jeu

1. common/history/states/00_states.txt : titulaire du seul RGB concerné.
2. common/history/pops/00_west_europe.txt : redistribution déterministe HAN/PRU.
3. common/scripted_triggers/1776_imperial_constitution.txt : titulaire légitime.
4. common/scripted_effects/1776_imperial_constitution.txt : cinq lignes ciblées de restitution/aperçu/réponse.
5. localization/french/1776_imperial_feedback_l_french.yml et son équivalent anglais : titulaire affiché dans l'aperçu de rétrocession.

Également : docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json, migration additive MAP2O et outils/tests de validation. Les anciens tests MAP2N rejouent désormais les migrations explicitement approuvées ultérieures ; leurs baselines ne sont pas réécrites.

## Vérification

Consulter VALIDATION.json pour les résultats réellement exécutés. Les 44 doublons RGB et 12 références invalides hérités sont distingués des nouvelles erreurs. Les assertions différentielles contrôlent les pixels mondiaux, chaque propriétaire, les profils démographiques, les historiques inchangés, les dépendances impériales et les empreintes des fichiers protégés. Les images avant/après représentent les propriétaires réellement installés, pas une hypothèse dessinée.

Résultats exécutés : **94/94 contrôles différentiels**, **52/52 tests** MAP2L-registre / MAP2N-île / MAP2N-complétion / MAP2O, et **57/57 fichiers concordant avec le générateur impérial** après correction des deux textes d'aperçu. Voir UNIT_TEST_VALIDATION.json et COMPILER_VALIDATION.json. Le générateur a été exécuté en vérification sans réécrire les fichiers du jeu.

Le chargement, l'accès maritime de la subdivision PRU, l'économie et le passage du mois restent à vérifier par le joueur en nouvelle partie. Pour rejouer la vérification statique : `python -B -X utf8 tools/map2o_east_frisia.py validate` ; tests : même outil avec `tests`. Ne pas relancer `capture` pour écraser la référence initiale : cette opération est explicitement refusée.

## Recherche locale

Un appel à ColGrep-Agent-2B a été exécuté avec le modèle local configuré. Il a surtout retourné des pistes générales de MAP2M, sans retrouver un tracé exploitable de Frise orientale. Chemins et lignes vérifiés ; recours aux recherches exactes et aux cartes déjà conservées. Pas de nouvelle intégration ni reconstruction complète d'index. Le temps local exact et le compteur de tokens Codex n'ont pas été relevés ; aucun gain de quota exact n'est revendiqué. Dans cette passe, l'apport du 2B à la localisation spécifique a été faible.
