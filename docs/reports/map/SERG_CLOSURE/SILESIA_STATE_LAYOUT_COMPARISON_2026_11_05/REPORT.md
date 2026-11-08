# Silésie — comparaison des régions de jeu, 5 novembre 2026

**Comparaison demandée : « Comparer aussi une Silésie partagée ». Aucun changement fonctionnel installé ; aucune option nouvelle approuvée, aucun reçu humain.** Date historique : 1er janvier 1776. Progression avant/après : **93/235, 39,57 %, 32/81 tâches qualifiées**, calculée par le validateur canonique.

## Conclusion proposée

Pour la V1, conserver le découpage actuel et concentrer les corrections futures sur la frontière politique démontrable. Une Silésie autrichienne économiquement distincte constitue une piste ultérieure plus cohérente avec l'institution territoriale de 1776 et évite de créer un partage PRU/AUS. La variante partagée est possible techniquement, mais exige une migration économique et des essais comparatifs de l'IA. **Elle n'est ni installée, ni certifiée sans risque.**

La décision déjà approuvée pour `SC2-AUSTRIAN-SILESIA` demeure `NOT_APPLICABLE_VERIFIED` dans son périmètre exact. La comparaison ne la révoque pas. `SC3-SILESIA-LUSATIA` reste `BLOCKED` ; son noyau lusacien installé attend toujours le joueur. Teschen n'est ni rouvert ni clôturé par cette étude.

## État réellement présent

Inventaire des déclarations effectives : [CURRENT_INVENTORY.json](CURRENT_INVENTORY.json). Les nombres de cellules décrivent le bitmap, pas une superficie cadastrale ni une population.

| Région technique | Portions nationales actuelles | Périmètre utile |
| --- | --- | --- |
| `STATE_UPPER_SILESIA`, ID 924 | PRU seulement | 6 RGB, 1 042 cellules ; 300 385 habitants écrits |
| `STATE_LOWER_SILESIA`, ID 155 | PRU et SAX | 418 cellules SAX issues de la livraison lusacienne ; ce partage est conservé |
| `STATE_MORAVIA`, ID 53 | AUS seulement | Deux RGB silésiens `x71E080` et `xF0E080`, 311 cellules, dans l'agrégat morave |
| `STATE_WEST_GALICIA`, ID 161 | GAL et AUS | Portion AUS/Teschen `x9061E0`, 179 cellules ; nom de région purement technique |

**Il n'existe actuellement aucune région silésienne partagée entre PRU et AUS.** Il existe déjà un partage PRU/SAX en Basse-Silésie et un partage GAL/AUS dans la région technique de Galicie occidentale. Les trois variantes maintiennent les propriétaires politiques actuels, les pixels et les corrections saxonnes ; elles ne prétendent pas certifier leurs micro-frontières.

## Trois configurations comparées

| Option | Découpage proposé | Conséquences et limites | Installation |
| --- | --- | --- | --- |
| A — conserver l'actuel | Silésie prussienne distincte ; noyaux autrichiens dans Moravie et région technique de Galicie occidentale | Moindre risque et coût pour la V1 ; office d'Opava peu lisible | Configuration déjà présente, aucune nouvelle correction |
| B — Haute-Silésie partagée | Rattacher les trois RGB autrichiens à `STATE_UPPER_SILESIA`, toujours sous AUS ; PRU conserve ses six RGB | 9 RGB, 1 532 cellules ; partage PRU/AUS nouveau, partage GAL/AUS supprimé sur ces noyaux. Répartition économique et intérêt de conquête à tester | Hypothèse non installée |
| C — région autrichienne distincte | Regrouper ces trois RGB dans une nouvelle région AUS ; Haute-Silésie PRU et Basse-Silésie PRU/SAX inchangées | Institution territoriale plus lisible, pas de nouveau partage PRU/AUS ; nouveau périmètre, repères et économie à préparer | Hypothèse non installée, aucun ID réservé |

Ces trois RGB sont un **périmètre technique candidat**, pas une nouvelle homologation des frontières d'Opava, Krnov, Nysa et Teschen. Ni B ni C n'autorise à prendre toute la Moravie ou toute la Galicie occidentale. Aucun nouveau pays n'est nécessaire.

## Risque d'IA : mécanisme confirmé, effet moteur non mesuré

Le mod effectif contient une règle dans `common/ai_strategies/00_default_strategy.txt`, bloc `state_value`, lignes 1390–1407 : la valeur d'une portion étrangère est multipliée par **2** si la région est partagée avec une portion non portuaire appartenant à l'évaluateur, **ou** s'il possède une revendication. Preuve avec lignes et empreinte : [AI_EVIDENCE.json](AI_EVIDENCE.json).

À conditions de portée et d'accessibilité remplies, B peut activer cette branche entre PRU et AUS dans les deux sens. Une revendication déjà présente active la même branche : les deux motifs ne s'additionnent pas en ×4. Aucune revendication PRU/AUS n'est déclarée dans les blocs initiaux de Haute-Silésie et de Moravie inspectés ; cette observation n'exclut pas les revendications ajoutées ultérieurement par d'autres scripts.

Ce facteur porte sur **la valeur territoriale calculée**, pas directement sur une relation diplomatique, une attitude hostile ou une probabilité de guerre. Aucun essai moteur comparatif n'a été exécuté. Le partage actuel GAL/AUS peut lui aussi satisfaire la branche correspondante pour ces pays ; B et C déplaceraient donc également ce problème local. Une exception dans l'IA globale serait un chantier séparé, sans garantie de supprimer les autres causes de rivalité.

Le journal officiel de la mise à jour 1.13 confirme la fusion de la Haute-Silésie autrichienne dans la Moravie. Le passage consulté **n'en donne pas le motif diplomatique** ; le lien causal avec l'hostilité reste une explication rapportée par le joueur, confortée par le mécanisme local, sans mesure de son ampleur. [Annonce officielle](https://store.steampowered.com/news/posts/?enddate=1776952823&feed=steam_community_announcements).

## Référence historique et frontières allemandes ultérieures

Le dossier historique réutilisé décrit la partition de 1742 et sa confirmation en 1763. L'office royal d'Opava existe en 1776 ; l'union administrative avec la Moravie ne survient qu'en 1782–1783. C a donc un fondement institutionnel, sans imposer automatiquement un découpage économique particulier au jeu. Une limite reprise par des États ultérieurs peut coïncider avec celle de 1776 ; elle doit être justifiée par les accords et domaines de l'époque, sans projeter les découpages de 1920 ou de 1945. [Atlas historique, chapitres 1.3–1.5](https://mapa.atlas-slezska.cz/en.html).

Les mauvais calages MAP1B restent archivés et ne sont pas relancés. L'étude ne produit aucune nouvelle frontière cadastrale. [Sources anciennes et limites de la preuve](../SC2-AUSTRIAN-SILESIA/SOURCES.md), [décision approuvée inchangée](../SC2-AUSTRIAN-SILESIA/DECISION_USER_APPROVED_2026_10_19.json).

## Migration qu'exigeraient B ou C

1. Déplacer les références des seuls RGB retenus, leurs propriétaires restant AUS ; conserver le bitmap et toute autre attribution, notamment les 418 cellules SAX. Auditer ensuite registre impérial, terrains, régions stratégiques et repères.
2. Reprendre la provenance des populations. Les pools techniques MAP2A de 191 139 habitants Opava/Krnov et 135 753 Teschen ne sont pas un recensement certifié de 1776. Le premier est aujourd'hui mêlé à l'agrégat morave de 1 570 622 habitants : aucune extraction automatique de cet agrégat sur un simple ratio de pixels.
3. Revoir ressources, bâtiments, propriété et unités sans duplication. La Haute-Silésie déclare notamment un potentiel charbonnier de 110, la Moravie 56 : aucun chiffre n'est transférable proportionnellement aux cellules sans justification. Contrôler les PM, intrants et restrictions de construction ; aucun recalibrage économique n'est installé ici.
4. Examiner l'administration de chaque portion. L'administration morave ne peut pas être supposée desservir automatiquement un nouvel État autrichien hors Moravie. Ni déplacement intégral ni ajout d'un niveau n'est décidé par cette comparaison.
5. Vérifier les listes de pays libérables et les consommateurs de régions : `common/country_creation/00_releasable_countries.txt` référence Haute-Silésie pour les clés `POL`, `BOH` et `PRU` ; ces clés ne sont pas toutes les propriétaires initiaux. Les journaux et événements liés à la Moravie/Galicie peuvent aussi changer de périmètre. Une présence dans une liste ne prouve pas l'activation d'un événement en 1776.

## Vérifications et suite

[FINAL_CHECKS.json](FINAL_CHECKS.json) contrôle l'identité des fichiers fonctionnels, des trois livraisons prussiennes précédentes, des preuves silésiennes approuvées, des 81 tâches, des anciens événements et de l'index Git ; [TEST_RESULTS.json](TEST_RESULTS.json) contient le résultat de la suite canonique réellement exécutée. Les onze références orphelines héritées de l'inventaire global sont conservées dans l'inventaire brut, hors de cette comparaison ; aucun écart territorial de scope n'est relevé pour les quatre régions inspectées.

Résultats de cette passe : **14/14 contrôles de conservation réussis**, dont les empreintes identiques de **2 859 fichiers fonctionnels** ; validateur canonique `PASS` ; **28 tests canoniques exécutés, 27 réussis, 1 ignoré** (contrôle de non-écriture propre à l'initialisation ancienne), aucun échec ni erreur. `git diff --check` sur les fichiers de cette passe retourne 0 ; seuls des avertissements de conversion LF/CRLF sont émis pour les documents suivis. Aucun ancien résultat prussien n'est présenté comme une nouvelle exécution.

Aucun nouveau test joueur n'est demandé pour cette passe documentaire. Les installations prussiennes précédentes restent à vérifier suivant leur [protocole groupé](../PRUSSIA_POLAND_2026_11_05/PLAYER_TEST_PROTOCOL.md). Un [plan conditionnel](PLAYER_TEST_PLAN.md) précise les essais nécessaires si B ou C est installé ultérieurement.

Après cette comparaison, la candidate indépendante pour l'ouest prussien est `SC5-PRUSSIAN-WEST`, **P1, NOT_STARTED, sans dépendance**, partage de 1713 et possessions antérieures au XIXe siècle. Elle est identifiée sans être commencée dans cette étude. Aucun lot bavarois ou micro-État relancé ; aucun point supplémentaire.
