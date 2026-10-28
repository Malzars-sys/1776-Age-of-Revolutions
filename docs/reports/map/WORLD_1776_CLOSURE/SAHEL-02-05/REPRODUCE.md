# Reproduire les vérifications

Depuis le workspace courant, Python du runtime local :

`python tools/world1776_sahel0205.py --validate`

`python tools/world1776_sahel0205_closeout.py --evidence --reports --final`

Les commandes de validation n'appliquent aucune frontière. L'installation et la réparation sont gardées contre le rejeu. Captures apply_inputs et repair_inputs, reçus originaux FILES_MODIFIED et COMPATIBILITY_REPAIR restent immuables. Les réexécutions actualisent les preuves du seul dossier SAHEL-02-05 ; un futur changement territorial légitime doit faire l'objet d'une réconciliation explicite, pas d'un retour à ces frontières.

Contrats techniques : `validate_starting_technology_1776.collect_snapshot()` puis `audit_country` pour chaque profil de COUNTRY_PROFILES.json. Aucun lancement de jeu et aucune opération Git d'écriture.
