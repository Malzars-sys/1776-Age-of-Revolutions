# R9 — Contrôle final technique et passage de relais

Rapport terminé le 29 octobre 2026. Audit des fichiers et essai moteur réalisés le 28 octobre. Le nom du dossier conserve la date de début des preuves.

**Conclusion : propriétaires et populations confirmés au chargement ; validation visuelle, simulation et rechargement incomplets.** Les lots conservent `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. Aucun `PASS_RUNTIME_USER_VALIDATED` n'est attribué, notamment à R9-02. Ce rapport ne clôt pas historiquement l'Amérique du Sud.

## Périmètre et conservation

Contrôle des installations R9-01 à R9-07 et de la correction Sacramento partagé avec l'Uruguay : 53 régions, 75 portions d'États possédées, 3 692 provinces. Les anciens dossiers, baselines, amendements et protocoles sont préservés. Aucun fichier de données du mod ni du vanilla n'a été modifié par cet audit ; seuls outils de contrôle, nouvelles preuves et renvoi de suivi sont ajoutés. Aucune opération Git d'écriture.

Les contrôles portent notamment sur Ica/La Paz, Rio Grande et Santa Tecla, Sacramento, Araucanie/Huilliche, Amazonie/Tabatinga, Guyanes/Wayuu, Chaco/Cuyo/Pampas et Malouines. Les réserves historiques des rapports de livraison restent ouvertes, dont le secteur britannique provisoire des îles composites. CENTRAL-01/02 n'est ni refait ni homologué ici.

## Fichiers : résultats

`tools/r9_final_validation.py` : **20 contrôles stricts réussis sur 22**. Les deux échecs d'identité exacte avec les livraisons sont conservés dans `STATIC_VALIDATION.json`, puis expliqués dans `FOLLOWUP_RECONCILIATION.json`.

- Les **212 transferts documentés** sont tous présents. Les attributions de toute la zone correspondent aux livraisons. Aucune province R9 sans propriétaire, doublement attribuée ou rattachée à une mauvaise région.
- Références de pays/capitales, cultures et religions résolues ; portions de populations et bâtiments dotées d'un propriétaire et de terres praticables. Identifiants numériques de régions uniques, RGB présents dans le bitmap.
- Sacramento reste une portion BRZ de `STATE_URUGUAY`, avec sa cellule de 51 pixels. L'ancienne région indépendante n'est pas réintroduite. Le doublon de propriété de Guayana reste corrigé.
- Le total démographique est **8 082 506**, soit les effectifs antérieurs à R9 augmentés des seuls 115 habitants documentés à Puerto Soledad. Les redistributions territoriales conservent les cohortes existantes.
- Changements concurrents préservés : professions réaffectées à Lima, Potosí et Santiago, sans changement des totaux régionaux ; administrations de Lima de 3 à 12 niveaux et de Santiago de 1 à 6 ; PM de Potosí et de chantiers navals modifiés. Aucun bâtiment déclaré supprimé ni niveau réduit dans le fichier sud-américain hérité. Le fichier mondial de redistribution a également évolué en Érythrée et Katanga, hors R9.
- L'inventaire global signale aussi 14 RGB à attributions multiples et 11 sélecteurs orphelins **hors R9**, présents au relevé initial. Ils ne sont pas corrigés par cette mission.

Le fichier partagé `00_states.txt` a encore évolué pendant le travail d'autres agents. `R9_OWNERSHIP_AT_HANDOVER.json` vérifie séparément ses portions R9 ; ne pas comparer uniquement son empreinte globale pour restaurer une ancienne version.

## Essai réellement effectué dans Victoria 3

Skill utilisé : Computer Use. Une nouvelle partie bac à sable a été créée avec l'Espagne, **1er janvier 1776, en pause**, dans Victoria 3 **Macha 1.13.11**, checksum affiché **0352 modifié**. Le menu initial, la sélection du pays et la partie ont été observés. Une copie locale à suffixe `_R9_fresh_initial_20261028` a été enregistrée sans écraser les sauvegardes existantes.

La session chargée avant la relance était plus ancienne que certaines modifications du disque. Elle a été sauvegardée séparément avant de quitter, en décochant la sauvegarde de sortie afin de préserver l'ancienne `autosave_exit`. La relance automatique ayant échoué, l'utilisateur a relancé le jeu. La nouvelle partie, et non l'ancienne sauvegarde, fournit les résultats suivants.

Les deux sauvegardes ont été converties en lecture seule avec l'exécutable **rakaly 0.8.21 déjà installé**, `melt --format vic3 -u stringify -o <nouveau fichier de preuve>`. Aucune sauvegarde originale n'a été réécrite. Archives et empreintes : `RUNTIME_RECEIPT.json`.

| Contrôle dans la nouvelle sauvegarde moteur | Résultat |
| --- | --- |
| Propriétaires des 75 portions et nombre de provinces par portion | Concordance exacte avec les entrées du mod ; 3 692 provinces |
| Population par portion d'État | Concordance exacte pour les 75 portions ; total 8 082 506 |
| Port BRZ de Sacramento, port SC3 de Chiloé, port SC4 de Puerto Soledad | Tous présents, niveau 1 chacun |
| Correspondance individuelle RGB ↔ numéro interne de province sauvegardé | Non testée ; ces deux identifiants ne sont pas confondus |
| Tour visuel des frontières et noms R9 | Non terminé |
| Simulation, ravitaillement durable, sauvegarde puis rechargement | Non effectués |

### Réserves sur les bâtiments chargés

Additionner tous les `create_building` des fichiers superposés donne 83 écarts apparents : ce total déclaré ne constitue pas une attente moteur fiable. Un diagnostic utilisant le maximum déclaré par type/portion ramène les écarts à **8 cas**, sans prétendre démontrer la règle générale de superposition du moteur.

Les huit cas ont les **mêmes niveaux dans la sauvegarde de la session antérieure** : plantations de coton de Guayana et Maranhão ; chantier naval de Bolívar ; mines d'or d'Antioquia, Cauca et Goiás ; université de Lima ; mine d'or de Minas Gerais (2 chargés contre 4 déclarés). Ils sont détaillés dans `PREEXISTING_ENGINE_BUILDING_DIFFERENCES.json`. Leur origine et leurs éventuelles conversions/restrictions restent à établir. La session antérieure n'est pas une baseline avant tous les lots R9 : cette comparaison ne prouve donc pas leur absence de lien avec l'ensemble du chantier.

### Limite du contrôle et journaux

Après la sauvegarde, la capture a renvoyé `FrameArrived timed out: timed out waiting on channel`, puis le même échec après récupération de la fenêtre. Les entrées ont été interrompues conformément au skill. Ce résultat établit une panne de capture, sans établir à lui seul un crash du jeu. Le joueur reprend les contrôles visuels.

Les journaux initiaux sont archivés dans `runtime_before`, les journaux relevés au passage de relais dans `runtime_followup_2026-10-29`. Ces derniers incluent des relances ultérieures et ne sont pas tous attribuables à cet essai. La recherche bornée des mentions R9 relève notamment des collisions de clés GNI/PAT entre fichiers généraux et surcharges, ainsi que des avertissements UTF-8 BOM de scripts R9. Plusieurs avertissements étaient déjà visibles au relevé initial ; la liste conserve cette distinction. Ils ne sont pas masqués ni assimilés à des erreurs territoriales résolues. L'absence d'autres mentions dans ce filtre ne certifie pas l'absence d'erreurs moteur.

## Suite manuelle

Voir `MANUAL_CHECKLIST.md`. R9-02 et les autres lots restent en attente des contrôles explicitement indiqués. Un chargement réussi ne certifie ni accès au marché durable, ni bonne alimentation, ni stabilité après simulation/rechargement.

## Outils et délégation

Outils ajoutés : `tools/r9_final_validation.py`, `tools/r9_validation_followup.py`, `tools/r9_saved_validation.py`, `tools/r9_validation_receipt.py`. Ils lisent les données et écrivent uniquement ce nouveau dossier de preuves. Les anciennes validations ne sont pas réexécutées en écrasant leurs preuves.

Aucun appel ColGrep pour cette validation : les chemins et identifiants nécessaires étaient déjà connus. Aucun sous-agent distant. Les recherches exactes ont employé `rg` ; aucun compteur fiable de tokens Codex ni comparaison de coût n'est disponible. Aucune économie chiffrée n'est donc revendiquée.
