# Guidage joueur — copie chargée différente, 5 novembre 2026

Les villes historiques citées ne sont pas des repères de recherche disponibles dans le jeu. Les nouvelles vérifications doivent employer les limites politiques et leurs propriétaires, avec Eindhoven, Nimègue et Düsseldorf comme repères réellement visibles. Aucun nouveau cliché n'est nécessaire pour établir le problème de version ci-dessous.

## Diagnostic vérifié en lecture seule

`content_load.json` active `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Les corrections de cette mission sont dans le worktree `C:/Users/simeo/.codex/worktrees/massa-carrara-finalisation/1776_Age_of_Revolutions_fork`.

Les cinq fichiers fonctionnels de la dernière installation concordent avec sa livraison dans le worktree, mais diffèrent tous dans la copie configurée pour le jeu. Les cellules de Venlo/Beesel et deux témoins du précédent noyau PRU sont encore `x0000DF` dans cette copie, au lieu des nouveaux RGB `xEEC700`, `xEEC701` et `xEEC600`. Les captures ne permettent donc pas de recevoir les dernières installations. Ce constat n'est ni une défaillance moteur du correctif ni une attestation humaine. Les anciens reçus restent inchangés.

## Intégration à préparer avant la prochaine nouvelle partie

Cible identifiée : le dossier de mod indiqué par `content_load.json`, pas le vanilla. Le transfert devra être une fusion ciblée des corrections prussiennes autorisées et de leurs dépendances, avec inventaire des passes absentes, comparaison des fichiers courants et protections des changements concurrents. Il ne faut copier ni l'arborescence entière du worktree ni ses fichiers partagés par remplacement intégral.

Pour le dernier lot seul, les cinq dépendances fonctionnelles sont : `map_data/provinces.png`, `map_data/state_regions/00_west_europe.txt`, `common/history/states/00_states.txt`, `common/history/pops/00_west_europe.txt` et `map_data/province_terrains.txt`. La présence du noyau PRU précédent doit être réconciliée avant ce lot ; d'autres passes prussiennes peuvent également manquer. L'outil de registre et les preuves restent dans le suivi du projet et ne sont pas des fichiers moteur à déployer seuls.

Aucune intégration, modification du lanceur, écriture Git, modification du vanilla ou réception humaine n'est réalisée dans ce diagnostic. La copie jouée est extérieure au dossier de travail autorisé en écriture ; son intégration nécessite une autorisation explicite et un plan de fusion contrôlé, sans écraser les travaux des autres agents.

Preuves et empreintes : [DIAGNOSIS.json](DIAGNOSIS.json). Les anciens protocoles restent archivés ; leur réception est conditionnée à la présence de la livraison dans la copie effectivement chargée et à une nouvelle partie.
