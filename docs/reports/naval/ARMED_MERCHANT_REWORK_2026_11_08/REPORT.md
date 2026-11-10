# Marchands armés et icônes navales — livraison du 8 novembre 2026

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** L’audit économique #23 est laissé de côté à la demande du joueur. Cette intervention traite les trois icônes de PM et le concepteur des marchands armés ; elle ne reprend pas la mission #21. Vanilla consulté : installation canonique 1.15.0.

## Installation

- Trois PM reliés à leurs DDS : construction navale artisanale ocre, doublage en cuivre violet et variante barrée entièrement violette. Le joueur a validé l’aperçu par « Oui, installe ces trois icônes ». Le contrôle des deux fichiers de PM confirme que seuls les chemins de textures changent, sans retouche des recettes, emplois ou technologies.
- Quatre familles obligatoires et une fonction facultative, chacune avec trois variantes bronze, argent et or : **15 équipements distincts**. Les cinq identifiants bronze sont conservés ; les déclarations de la flotte américaine initiale, dont ses cinq marchands, ne sont pas modifiées.
- Le marchand devient un croiseur d’escorte pour l’IA, avec une capacité de transport et des provisions supérieures à la caravelle mais une puissance offensive inférieure. L’IA reçoit un poids de construction de 0,25 et utilise le multiplicateur vanilla de doctrine marchande pour ses équipements.
- La fonction propre au navire est l’escorte des convois : protection +15/+25/+35 %, efficacité d’approvisionnement +5/+10/+15 points de pourcentage et dégâts subis par l’équipage −5/−10/−15 %. L’ancien bonus de blocus de la fonction est supprimé. Ces valeurs s’ajoutent aux équipements obligatoires ; la fonction reste facultative.
- Silhouette nouvelle de marchand à deux mâts. Ajout de sa définition graphique manquante avec l’entité native complète `sail_transport_ship_01_entity`. C’est un modèle à voile réutilisé du jeu, pas une nouvelle création 3D. Son rendu moteur reste à vérifier.
- Noms et description mis à jour en français et anglais, avec BOM. Les autres textes du fichier révolutionnaire sont conservés.

## Valeurs comparées

Unités du concepteur. Dans chaque cellule : **marchand / caravelle**, avec les quatre équipements obligatoires du même palier et sans fonction facultative. Il s’agit de totaux de définitions, pas d’une mesure de combat en jeu.

| Palier | Dégâts à la coque | Capacité de transport | Provisions |
| --- | --- | --- | --- |
| bronze | 6.0 / 13.0 | 0.5 / 0.1 | 20.0 / 8.0 |
| silver | 7.0 / 18.0 | 0.55 / 0.1 | 26.0 / 14.0 |
| gold | 9.0 / 21.0 | 0.6 / 0.1 | 36.0 / 24.0 |

Les navires militaires transportent et escortent. Aucun modificateur de commerce de portée pays/État n’est injecté dans leurs composants : ces navires ne créent pas eux-mêmes des routes commerciales ou des convois économiques supplémentaires pour les ports. Les capacités affichées ne sont pas des tonnes de marchandises.

## Progression technologique

Chaque flèche correspond aux paliers bronze → argent → or ; le graphe technologique existant est conservé.

| Famille | Bronze | Argent | Or |
| --- | --- | --- | --- |
| Coque | `organized_workshops` | `scientific_naval_architecture` | `diagonal_ship_framing` |
| Canons | `organized_workshops` | `scientific_naval_architecture` | `copper_sheathing` |
| Gréement | `organized_workshops` | `scientific_naval_architecture` | `marine_chronometry` |
| Provisions | `organized_workshops` | `scientific_naval_architecture` | `hydrographic_surveying` |
| Escorte | `organized_workshops` | `standardized_naval_signals` | `maritime_safety_standards` |

Les prérequis bronze restent ceux du marchand initial. Les paliers suivants réutilisent les recherches existantes, avec des ères croissantes, plutôt que de copier les deux premiers paliers de caravelle parfois déverrouillés ensemble. Aucune technologie n’est distribuée aux pays.

## Images et sources

**19 DDS installés** : 3 PM, 15 équipements et 1 silhouette. Références vanilla effectivement décodées : PM `wooden_ships`, `reinforced_wooden_ships`, `furniture_handicraft`, `hardwood_selection` et sa variante barrée ; série `ship_designer_*_low/mid/high` du jeu.

Les anciens masters métalliques et la note de transfert bloqué sont conservés. Les anciens fichiers corrigés de bibliothèque n’étaient pas disponibles localement ; de nouveaux masters ont été générés avec l’outil d’image intégré, sur ces références vanilla, puis le trio de PM a été soumis au joueur. Le premier nouvel essai avec halo est écarté. La coque bronze a reçu une retouche supprimant une superstructure pouvant évoquer une cheminée ; son brouillon reste archivé.

Les maîtres finaux, prompts, provenances, références et empreintes sont dans `docs/reports/assets/ARMED_MERCHANT_2026_11_08/ART_PROVENANCE.json`. Le registre existant est étendu sans supprimer d’entrée. Les exportations conservent l’alpha et les proportions : PM 208 × 208/8 mipmaps, équipements 120 × 120/7 mipmaps, silhouette 240 × 160/8 mipmaps, format natif BGRA8. Les seules opérations après génération sont cadrage enregistré, redimensionnement et encodage DDS ; aucune recoloration cachée.

Sources techniques en lecture seule : `C:/Games/Victoria 3/game/common/ship_types/ship_types.md`, `ship_modifications/ship_modifications.md`, les deux fichiers de composants natifs, le transport de troupes ancien, les catégories IA natives et `common/modifier_type_definitions/00_modifier_types.txt`. L’entité 3D est déclarée dans `gfx/models/infrastructure/ships/sail_transport_ship_01.asset`.

## Contrôles et concurrence

- `tools/validate_armed_merchant_20261108.py --negative-controls --output …/VALIDATION.json` : **375/375 contrôles**, trois fautes injectées en mémoire détectées (technologie introuvable, modificateur inexistant, mauvais emplacement). Aucun fichier de jeu n’est modifié par ces injections.
- Audit naval IA #36 sur la superposition actuelle : **PASS_STATIC_ONLY**, aucune catégorie absente ou invalide.
- Reconstruction exacte des **19 DDS** depuis leurs masters et empreintes : **PASS_EXACT_REBUILD**.
- Comparaison des PM avec la révision de départ : seuls les trois chemins de textures changent.
- Le premier passage signalait 374/375 : le fichier des navires anciens avait été modifié en parallèle. L’écart est exactement le renommage `ship_type_cog` → `ship_type_early_troop_ship` ; inverser ce seul nom reproduit l’empreinte initiale du fichier. Toutes ses statistiques sont donc conservées. Cet écart est documenté dans `CONCURRENT_CHANGE.json`, pas annulé ; le résultat initial reste archivé. Le contrôle réconcilié accepte uniquement cette transformation précise, pas d’autres modifications.
- Les équipements de caravelle/galère et le fichier des technologies navales restent identiques aux empreintes capturées. Les autres changements du workspace appartiennent aux chantiers concurrents et sont préservés. Aucun Git d’écriture, aucun fichier vanilla, frontière, POP ou suivi SERG/WORLD modifié par cette intervention.

La validation du trio d’images ne vaut pas validation moteur. Le protocole borné est dans [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md) : chantier naval, flotte américaine, concepteur et technologies, fonctions, coûts, sauvegarde/rechargement. Aucune attestation de test en jeu n’est créée.
