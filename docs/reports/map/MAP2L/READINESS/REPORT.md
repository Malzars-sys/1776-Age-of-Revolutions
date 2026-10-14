# Saint-Empire, 1776-01-01 — état d'intégration et blocages

Passe du 13 octobre 2026. **Le découpage détaillé de tout le Saint-Empire n'est pas terminé. Aucun nouveau transfert territorial ni tracé bitmap n'a été appliqué pendant cette passe.**

## 1. Territoires réellement intégrés

Les travaux précédents sont conservés, sans réapplication :

- MAP2K : les quatre électorats représentés par KPF, KTR, KMZ et KCL, avec cinq transferts de RGB déjà approuvés comme approximations de jeu. Leurs enveloppes ne sont pas des limites cadastrales certifiées.
- MAP2L belge : Liège (LGE), y compris son fragment de Looz en Flandre, et Stavelot-Malmedy (STM), indépendants dans le bloc impérial ; BEO conserve les Pays-Bas autrichiens représentés dans ce lot.
- Quatorze identités natives belges subdivisées en 51, avec 37 nouveaux RGB et 413 pixels recolorés lors de la passe précédente. Flandre et Wallonie restent des régions économiques partagées.
- Registre impérial actif : 315 RGB. Chaque RGB a été retrouvé dans le bitmap, dans sa State Region déclarée, avec un unique titulaire correspondant au registre. Le registre MAP2K initial reste immuable.

La géométrie belge reste une approximation documentée, à partir de l'atlas de 1789 confronté au corpus Ferraris des années 1770. Elle ne devient pas une preuve cadastrale de 1776 du seul fait que les tests passent. Bouillon, Saint-Hubert, Maastricht et les fragments extérieurs n'ont pas reçu d'arbitrage supplémentaire.

## 2. Blocages historiques précis

Les recherches n'ont pas été recommencées. Les conclusions et sources existantes ont été confrontées à leur **statut réel**, puis aux fichiers actuels.

### Franconie : STATE_FRANCONIA, identifiant numérique natif 72

Les huit RGB sont toujours attribués à BAV : `x0B0DBA`, `x51C0A0`, `x648AD1`, `x9040A0`, `xA55FB1`, `xD041A0`, `xD0C0A0`, `xF91154`. Ils ne sont pas des identifiants d'États historiques.

Le dossier MAP1 R2-0031 conclut à plusieurs autorités impériales autonomes, mais reste `MAPPING_REQUIRED` / `NO_DEFENSIBLE_LINEAR_BORDER`. Les villes natives de Nuremberg, Coburg, Bayreuth et Würzburg ne démontrent pas la souveraineté sur la totalité de leur province.

Les sources déjà stockées ne lèvent pas encore le blocage :

- Le Rouge / BSB : métadonnée « 1743 [published after 1764] », statut `SOURCE_MAP_NOT_YET_ALIGNED_OR_CORROBORATED_FOR_1776`.
- Homann / StadtAN A4/IV nº 74 : la notice enregistrée ne précise pas la date ; pas de calage territorial validé.
- Cliopatria : trois objets candidats en 1776, dont des agrégats ; aucune table détaillée de ces huit RGB vers les principautés et villes.

Il manque un tracé calé et une correspondance explicite des morceaux vers Ansbach/Bayreuth, Bamberg, Würzburg, les villes libres et les autres juridictions. Une partition par proximité des villes ou un transfert en bloc à un nouveau TAG serait inventé. Aucun redécoupage de ce type n'a été fait.

### Autres zones

- Rhin/Ruhr : R2-0030/0032, distinction Clèves, Mark, Ravensberg et possessions ecclésiastiques encore sans correspondance fine validée. Les électorats MAP2K déjà appliqués ne résolvent pas cette totalité.
- Westphalie : R2-0054 à 0056, attribution de chaque RGB non confirmée.
- Souabe/Wurtemberg : R2-0057/0058, même manque de limites locales vérifiées.
- Bade, Bavière, Anhalt, Brunswick, Hesse et Saxe : juridictions et enclaves encore ouvertes dans les recommandations originales.

`AUDIT.json` conserve 27 lignes de recherche concernées et les propriétaires/populations actuels de leurs régions. Les anciens statuts MAP1 ne sont pas utilisés pour annuler les lots ultérieurs. Les anciennes fiches ne sont pas toutes des fichiers Markdown : plusieurs dossiers restent dans les CSV de recherche.

La prochaine étape territoriale est le **calage et la validation des sources de Franconie déjà conservées**, avec contrôle chronologique de 1776, puis l'établissement d'un manifeste de polygones/RGB avant création des pays. Il ne s'agit pas de reprendre l'histoire générale depuis zéro.

## 3. Fichiers de cette passe

- Ajout de `tools/audit_map2l_hre_readiness.py` : contrôles en lecture seule, génération de rapport uniquement.
- Ajout de `docs/reports/map/MAP2L/READINESS/AUDIT.json`, `METRICS.json` et ce rapport.
- Régénération du rapport existant `BELGIUM/VALIDATION.json` par son validateur.

Aucun fichier runtime, pays, province, population, bâtiment, formation, traité, sauvegarde ou paramètre du lanceur n'a été modifié. Pas de commit, staging, merge, rebase ou push. Les changements antérieurs et collaborateurs sont conservés.

## 4. Vérifications

- `validate_map2l_belgium.py` : **309 contrôles PASS_STATIC_ENGINE_PENDING**. Conservation de 835 804 980 habitants, des cultures/religions, des profils démographiques par région, des niveaux/PM/réserves pondérés des bâtiments et des unités/recrutements.
- `audit_map2l_hre_readiness.py` : **334 contrôles PASS_STATIC_READINESS_BLOCKED**. Les 315 identités impériales sont présentes, correctement référencées et attribuées une seule fois ; les neuf références finales valides du sous-agent existent et leurs bornes de lignes ont été contrôlées.
- Aucun nouveau doublon ni référence invalide dans l'inventaire. **44 RGB à attributions multiples et 12 références invalides sont hérités de la baseline**, dans l'inventaire global ; ils ne sont pas couverts par une affirmation que tout le monde est réparé. Détail dans `AUDIT.json`.
- Empreintes de 1 707 fichiers runtime protégés, HEAD et index Git identiques avant/après l'audit.

### Moteur et avertissements

Pas de nouveau lancement contrôlé de Victoria 3 pendant cette passe. Le journal de lancement antérieur indique la version **1.13.11** et des messages de départ pour LGE/STM ; cela ne constitue pas un test complet de la nouvelle carte.

Le journal `error.log:519-528` signale, pour LGE et STM, cinq lois non conservables avec leur technologie initiale : armée professionnelle, mercantilisme, imposition par tête, police locale et interdiction de l'esclavage. Des messages identiques touchent les électorats antérieurs, dont KPF aux lignes 481-485.

Les historiques appellent l'effet natif `game/common/scripted_effects/00_political_setup.txt:47-72`. Cet effet impose notamment les quatre premières lois, alors que les lois du mod demandent leurs propres technologies. Le message sur l'esclavage est aussi observé, sans l'attribuer à une commande absente de cet effet. Aucun ajout massif de technologies, changement de droit ou d'économie n'a été fait pour faire taire ces messages. Cette compatibilité de départ reste à régler séparément avec une politique explicite ; les tests statiques territoriaux ne la valident pas.

## 5. ColGrep-Agent-2B : mesures et limites

Exécutable effectivement appelé : `C:/Users/simeo/.cargo/bin/colgrep.exe`.
Les trois appels utilisaient `--agent --no-update --color never` et une question ciblée ; les questions intégrales figurent dans `METRICS.json`. Ces appels précèdent les nouvelles règles AGENTS.md réservant `--no-update` aux recherches ordinaires. Les recherches futures doivent suivre ces nouvelles règles.

La bannière d'exécution a confirmé **colgrep-agent-2B-Q8_0.gguf, llama.cpp b11476, AMD Radeon 780M Graphics**. Ce n'était pas un sous-agent Codex distant. `colgrep status .` a confirmé le chemin de l'index ; son modèle d'embeddings LateOn-Code-edge n'est pas le modèle de raisonnement 2B.

| Mesure | Résultat |
|---|---:|
| Appels à l'agent local | 3 |
| Durées annoncées par le CLI | 62,6 + 78,7 + 44,2 = 185,5 s |
| Recherches sémantiques internes | 12 |
| Commandes terminal internes | 9 |
| Tours du modèle local | 24 |
| Commandes exactes `rg` exécutées par Codex | 8 |
| Références finales valides vérifiées | 9 |
| Tokens Codex exacts pour cette passe | Compteur non accessible |

Ces durées ne comprennent pas toutes les lectures/vérifications Codex ni nécessairement tout le démarrage du serveur. Les lectures directes, listes de dossiers et filtres CSV ne sont pas assimilés aux huit commandes `rg`.

Erreurs et imprécisions relevées : chemin de dossier final inexistant (segment `/MAP1/` oublié, éliminé du résultat par le CLI), deux lectures Nassau échouées, développement fantaisiste de LGE/STM en « Large/Small Empires », référence aux dettes technologiques sans rapport avec les lois, résultats sémantiques hors sujet. La troisième délégation n'a pas trouvé la définition réelle de l'effet natif ; une recherche exacte dans les fichiers du jeu a été nécessaire.

Couverture contrôlée : `.csv` 0/561, `.gui` 0/17, `.asset` 0/3, `.mod` 0/4, `.geojson` 0/3. Le bitmap et les autres assets binaires ne sont pas une source sémantique. Les CSV territoriaux ont donc été lus directement. Les tailles et dates enregistrées pour les deux outils MAP2L et les deux historiques LGE/STM correspondent aux fichiers actuels ; aucune reconstruction de l'index n'était nécessaire pour ces recherches. Les nouveaux rapports pourront être pris en compte par la prochaine actualisation incrémentale normale.

## 6. Intérêt pour le quota

Douze recherches ont été exécutées localement, mais cela ne signifie pas douze recherches Codex économisées : plusieurs emplacements étaient déjà connus et les vérifications restent nécessaires. Aucun comparatif contrôlé ni compteur de tokens par passe n'est disponible.

L'agent peut aider à retrouver des dossiers et outils dans une grande arborescence. **L'économie nette de quota n'est pas démontrée par cette passe** : les retours hors sujet, les erreurs de chemins et les trois minutes de recherche imposent un coût de contrôle. Pour ce mod, la bonne répartition reste la délégation exploratoire ciblée, suivie de `rg` pour les identifiants et de lecture directe pour les tableaux non indexés. Le 2B ne tranche ni les souverainetés ni les frontières.
