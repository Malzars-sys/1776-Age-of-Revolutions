# Fezzan — contour vanilla rétabli

27 octobre 2026. Demande explicite du joueur : privilégier la forme vanilla, même moins historique. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, aucun reçu humain créé.

Le ruban de neuf provinces est remplacé par le périmètre natif dédoublonné : **48 provinces dans STATE_TRIPOLI et 30 dans STATE_LIBYAN_DESERT, soit 78**. Soixante-dix provinces passent de ZWY à FZN ; x3B68A8 revient de FZN à ZWY. Les autres propriétaires sont conservés.

La référence locale C:/Games/Victoria 3/game donne 80 entrées FZN mais xAFD438 et xD5C61D sont également attribuées à TRI et ZWY dans le même fichier. Leurs corrections MAGHREB-03, attribution unique TRI, sont préservées. Cette réserve est explicite : les 78 provinces non ambiguës reproduisent exactement leurs pixels vanilla, sans restaurer de doubles propriétaires. Le choix esthétique ne certifie aucune nouvelle frontière historique de 1776.

**Un seul fichier fonctionnel modifié** : common/history/states/00_states.txt, dans quatre listes owned_provinces des blocs FZN/ZWY de deux régions. Aucun pixel peint, nouveau RGB, pays, population, bâtiment, unité, terrain, ressource ou hub ajouté. Les lois et technologies du pays, son lien tributaire, les corrections Tripoli, Maroc–Tekna, Siwa égyptienne, détroits et autres chantiers restent conservés. Les fichiers de POP sont strictement inchangés : 11 067 habitants FZN déjà déclarés, sans nouvelle estimation ou redistribution liée à la surface.

[Comparaison avant/après](BEFORE_AFTER.png) ; [contrat géométrique et conflits natifs](GEOMETRY.json). Le bitmap de la carte et la référence vanilla restent inchangés ; c’est une correction des propriétaires initiaux, visible en nouvelle partie.

**17/17 contrôles ciblés réussis**, dont égalité des masques natifs résolus, unicité des attributions affectées, absence de nouvelle province, conservation des autres propriétaires, des données FZN et des anciennes preuves. Le contrôle global git diff --check signale des espaces de fin de ligne hérités du fichier d’États partagé ; aucun nouvel espace fautif n’est introduit par les quatre substitutions. Le résultat brut et la comparaison avant/après sont consignés dans FINAL_CHECKS.json.

L’ancien rapport MAGHREB-03, ses résultats bruts et sa règle du noyau en ruban sont conservés comme archives. Cette révision explicite remplace uniquement leur géométrie Fezzan. [Protocole Maghreb–Égypte actualisé](GROUPED_RUNTIME_ITEMS.md), sans validation humaine inventée. WORLD conserve son périmètre, ses critères et sa progression ; SERG n’est pas modifié. Aucun nouveau chantier commencé, aucune opération Git d’écriture, aucune modification du vanilla.
