# Contrôles exécutés

`python tools/world1776_maghreb01.py --apply` : installation unique, quatre empreintes partagées vérifiées immédiatement avant écriture, préimages courantes archivées. Refuse une seconde application.

`python tools/world1776_maghreb01.py --validate` : 35/35, sortie 0. Détail dans VALIDATION.json. Aucun test moteur. Les doubles propriétaires restants hors Rif sont montrés dans la trace ; ils ne sont pas transformés en erreurs nouvelles de ce lot.

`python tools/world1776_maghreb01.py --render` : comparaison locale avant/après examinée ; représentation du chargement effectif non attestée. Les hauteurs et tout pixel hors des quatre points sont identiques.

Test groupé ultérieur : nouvelle partie 1776, propriétaires des trois noyaux et des arrière-pays, absence de double attribution, maintien des témoins RAG/B04/HBC/SERG ; vérifier rendu des portions sans POP et sauvegarde/rechargement. NOT_RUN, aucune demande intermédiaire.
