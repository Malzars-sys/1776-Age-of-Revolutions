# Reprise Erfurt–Eichsfeld — 13 octobre 2026

**NON IMPLÉMENTÉ : le placement des frontières reste bloqué.** Ce dossier apporte des vérifications supplémentaires ; il ne change aucun fichier de jeu et ne constitue pas un lot territorial approuvé. Il n'est pas ajouté à la chaîne des migrations impériales.

## Périmètre réutilisé

Possessions mayençaises d'Erfurt et de l'Eichsfeld au 1er janvier 1776, sans assimiler Eichsfeld à Eichstätt, ni incorporer la ville libre de Mühlhausen. Réutilisation des cartes Schreiber/Homann conservées dans MAINZ_COMPLETION et de son rapport, sans refaire la recherche historique générale. Erfurt, Vargula, Mühlberg et Tonndorf nécessitent des scopes géographiques distincts ; les minuscules enclaves ne doivent pas être agrandies.

Les anciennes matrices rejetées restent intactes. Leur principal problème est que le locator rural « Erfurt » n'est pas établi comme un centre géographique urbain : il ne peut pas servir à déplacer arbitrairement l'ensemble de la carte source.

## Nouveaux essais, non retenus comme frontières

Un modèle cylindrique utilisant la [formule de Miller documentée par PROJ](https://proj.org/en/stable/operations/projections/mill.html) est testé empiriquement. **Ce n'est pas une identification prouvée du système de coordonnées du moteur.** Cinq repères urbains déjà conservés sont utilisés, plutôt que les fermes/mines contestées. Les résidus d'ajustement sont : Hannover 2,438 pixels, Magdeburg 0,311, Frankfurt 0,155, Brunswick 2,906, Dresden 0,470. Leur amélioration n'est pas une validation indépendante.

Contrôle physique supplémentaire contre les géométries Natural Earth 1:10 millions déjà conservées et le bitmap natif des rivières, sans ajuster la matrice sur les rivières :

- Weser : 375 sommets ; distance médiane 3,263 pixels, 90e percentile 6,496, maximum 7,730.
- Elbe : 235 sommets ; médiane 2,615, 90e percentile 4,598, maximum 5,980.
- Bande de latitude ciblée 50,9–51,6 sur la Weser : 135 sommets ; médiane 1,720, 90e percentile 6,288, maximum 6,968. Restreindre la comparaison au voisinage ciblé ne supprime donc pas les écarts.

Ces distances sont au réseau le plus proche, pas à des landmarks uniques identifiés : elles peuvent sous-estimer l'erreur en présence de branches voisines. La relecture de MILLER_RIVERS_DIAGNOSTIC.png confirme également la schématisation des cours d'eau. Le bitmap n'offre pas de jonctions explicites Werra/Fulda/Saale utilisables comme trois nouveaux points indépendants dans la fenêtre inspectée. Une confluence supposée d'après la proximité ne suffit pas.

MILLER_HYPOTHESIS.json et MILLER_PHYSICAL_CHECKS.json restent **DIAGNOSTIC_NOT_APPROVED**. Les points affichés en bleu dans l'aperçu sont des hypothèses non validées ; aucune ligne ni surface n'est transformée en frontière. Le placement projeté d'Erfurt est encore à environ seize pixels du repère rural étiqueté Erfurt. Ce contraste ne prouve pas, à lui seul, quelle position il faut retenir.

## Blocage essentiel

La souveraineté générale de Mayence est établie, mais le rattachement des limites détaillées aux pixels actuels n'est pas suffisamment localisé. Sur ces petits territoires, une erreur de plusieurs pixels peut changer de province ou transférer une part importante d'un territoire voisin. Il manque un calage local revu reliant des positions identifiables dans la carte du jeu aux villes/limites des cartes conservées : Erfurt et des localités voisines, puis Duderstadt/Heiligenstadt/Worbis et Mühlhausen. Une image générale du Saint-Empire sans raccordement au raster ne résout pas ce point.

L'aperçu des propriétaires actuels est fourni pour permettre cette revue. On ne demande pas de substituer un souverain conjectural à un autre : le préalable est d'établir le placement. Sans ce préalable, aucun transfert de RGB, de population ou de bâtiments n'est préparé ou appliqué.

## Recherche locale

Un appel réussi à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent`, limité à `./tools`, code 0, **127,70 secondes**. Question : retrouver les outils/contrôles de projection et de calage local du centre de l'Allemagne, sans édition ni décision de frontières. Résultats vérifiés : `tools/map2l_mainz_completion.py:114` et `:50-55`, tous deux déjà connus et sans nouveau calage exploitable. L'utilité du modèle local est faible sur cette reprise. Aucune configuration, intégration ou modèle n'est changé ; aucun gain exact de quota Codex n'est mesurable ici.

Les identifiants, listes de hubs et dépendances connues sont consultés par recherches exactes et lectures ciblées. Les images et coordonnées sont contrôlées séparément, pas confiées au modèle sémantique pour attribuer des territoires. Aucun index n'est effacé ou reconstruit volontairement.

## Vérifications de protection

READ_ONLY_VALIDATION.json contrôle les empreintes du dernier bitmap approuvé (lot Milan), du registre impérial courant et des deux cartes historiques conservées. La dernière implémentation reste 394 RGB impériaux et 62 580 pixels. Les fichiers de jeu, leurs propriétaires et les données de départ ne sont pas modifiés par cette reprise. Aucun commit, staging, merge, rebase, push ou lancement du jeu.

## Atelier de géoréférencement réutilisable

Prototype livré dans `tools/georeference/` et `tools/map_georeference.py`, documenté dans le dossier voisin `GEOREFERENCE_PROTOTYPE`. Grille, conversions, séparation FIT/CHECK/TARGET, export transparent et quatre modèles diagnostiques sont testés. Les coordonnées d’Erfurt, Duderstadt et Heiligenstadt fournies le 13 octobre sont conservées sans leur attribuer de pixel observé fictif. Le dessin d’équateur natif est à Y = 2097,28 ; la projection exacte reste non établie. Les contrôles européens montrent des écarts substantiels, et aucun intervalle de précision locale n’est revendiqué. Le statut territorial ci-dessus reste NON IMPLÉMENTÉ ; aucune limite n’est déplacée par le prototype.

## Recalage physique terminé — 14 octobre 2026

Résultats détaillés dans `LOCAL_RECALIBRATION/REPORT.md`. La translation robuste ajustée uniquement sur la Weser–Werra vaut X −5,728 / Y −4,359, soit 7,198 pixels. Sur l'Elbe exclue de l'optimisation, moyenne 3,432 → 2,057 et maximum 7,828 → 4,758 ; dans la bande de latitude des trois villes, moyenne 2,996 → 2,445 et maximum 4,995 → 4,015. Ce sont des distances à un tracé physique, pas des erreurs certifiées de landmarks homologues. Les variantes d'échelle/rotation dégradent le contrôle et sont rejetées. Le relief et les trois cartes historiques ont aussi été revus ; aucun centre urbain pixel indépendant n'est prétendu identifié. Un profil réutilisable diagnostique et un comparatif visuel sont livrés, mais le seuil fiable demandé n'est pas atteint. Le découpage reste NON IMPLÉMENTÉ, avec 2 091 fichiers runtime/registre inchangés et aucune population, aucun bâtiment ou propriétaire modifié.
