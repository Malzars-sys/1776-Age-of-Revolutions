# MAGHREB-01-GIBRALTAR — 26 octobre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Correctif ciblé de compatibilité du découpage MAGHREB-01. Le joueur a précisé ne pas avoir testé le Maroc : son signalement constitue une inquiétude à vérifier, pas une attestation de panne du journal marocain.

Le vanilla rattache la rive africaine du détroit à `xA0B0C0`. Depuis MAGHREB-01, ce grand parent appartient exclusivement au Maroc ; Ceuta espagnole est la nouvelle province `xE8D231`. Le point de contrôle était donc resté dans l'arrière-pays marocain. Le correctif le rattache à Ceuta, sans agrandir les possessions espagnoles.

Un seul fichier fonctionnel ajouté : `common/strait_definitions/strait_definitions.txt`, surcharge de même chemin que le fichier natif courant. Un seul champ diffère : `strait_gibraltar.second_land_endpoint`, de `xA0B0C0` vers `xE8D231`. Les onze autres détroits sont identiques ; rive nord britannique `xBC6ED3`, points maritimes et conditions de contrôle complet conservés. L'Espagne ne reçoit pas le contrôle de Gibraltar britannique ni un droit de fermeture totale avec sa seule rive. Le fichier natif reste intact.

Cellule concernée comme référence : Ceuta `(3973,1252)`. Aucun pixel, terrain, propriétaire, hub ou frontière modifié. Melilla et Oran–Mers el-Kébir sont préservés. Aucun bâtiment ou bonus de contrôle artificiel ajouté. Institutions, technologies, PM, recettes, armées et diplomatie inchangés.

Le journal marocain `06_morocco_lands_of_anarchy.txt` accorde à son achèvement une revendication sur AL_RIF s'il subsiste une portion détenue par un autre pays ; les deux noyaux espagnols remplissent toujours cette condition territoriale. Cela ne signifie pas qu'une mission marocaine exige explicitement le contrôle du détroit. Les journaux espagnols qui demandent tout AL_RIF restent distincts du contrôle de sa rive : posséder seulement Ceuta/Melilla ne remplit pas cette conquête régionale. Aucun script de mission retouché.

Population mondiale capturée avant/après : **837 328 539 → 837 328 539**, delta **0**. Aucun transfert de population. **36/36 contrôles statiques réussis**, dont conservation de 3 644 fichiers existants fonctionnels et de preuves antérieures ; aucune différence extérieure observée. Aucun Git d'écriture, changement du vanilla ou écriture SERG. TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie préservés par empreintes.

Sources techniques locales : fichier natif `common/strait_definitions/strait_definitions.txt` et sa documentation `.md` ; `localization/english/concepts_l_english.yml`, `concept_strait_control_desc` ; carte/historique AL_RIF actuels ; les deux fichiers de journaux cités ci-dessus et `06_spanish_africa.txt`. Référence native exacte archivée avec son empreinte. Aucune nouvelle affirmation historique ou démographique n'est nécessaire à ce raccordement.

Limites : chargement moteur, affichage du contrôleur, occupation en guerre et sauvegarde/rechargement **non testés**. Le moteur associe les points aux États des propriétaires ; la vérification statique ne remplace pas leur observation en jeu. La surcharge des douze définitions doit être comparée à nouveau si le jeu de base met ce fichier à jour. Les limites cartographiques et économiques de MAGHREB-01 demeurent ouvertes. Aucun critère régional supplémentaire ni reçu humain : progression WORLD inchangée, **10/320 (3,13 %)**.

Prochaine action proposée : MAGHREB-02, frontières de la régence d'Alger et autres possessions côtières, sur autorisation ; contrôle de Gibraltar inclus dans le prochain test groupé.
