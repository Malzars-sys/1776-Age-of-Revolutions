# Reprise du chat « Évaluer compatibilité 1.15 » — état vérifié

Date : 7 novembre 2026. Mission : examiner les travaux laissés par le chat interrompu et identifier la suite. Aucun changement de gameplay, lancement du jeu, écriture Git ou modification de GitHub pendant cet audit.

Le travail déjà installé est conservé. **La migration globale reste incomplète ; les deux lots livrés sont techniquement prêts pour validation en jeu.** Les rapports anciens décrivent leurs étapes respectives : leur liste de prochaines actions ne doit pas être relancée sans vérifier les livraisons suivantes.

## Travail effectivement présent

| Livraison | État constaté aujourd'hui |
| --- | --- |
| Premier lot de migration #27 | Six fichiers, huit journaux, quinze `outcome`. Support français aux États-Unis, esprit révolutionnaire, réformes ottomanes, centralisation impériale, situation/vote impérial, essai de quota des naissances. |
| L'homme malade de l'Europe | Un fichier, huit journaux, dix-sept `outcome`. Journal principal et réformes de Syrie, Égypte, économie, éducation, séparatisme, armée et bureaucratie. |
| Ensemble des deux lots | **Sept fichiers, seize journaux, trente-deux issues ; quarante-huit anciens champs remplacés**, selon les mappings publiés et les fichiers recontrôlés. |
| Déclin ottoman | Groupe illustré installé, onze entrées. Bazar et mosquée : référence native du Grand Jeu. |
| Destin des Amériques | Groupe installé, onze entrées. Bandeau dérivé du Washington traversant le Delaware déjà utilisé par le mod. |
| État et révolution | Groupe installé, quatorze entrées. Révolution française, réformes/restauration polonaises, Printemps des peuples, Forêt de baïonnettes et Hungry Forties. |

Les trente-six appartenances aux groupes ne représentent pas trente-six migrations de conclusions. Plusieurs de ces entrées emploient encore l'ancien système.

Le délai de 10 950 jours et les quatre réformes requises de L'homme malade sont conservés. Le contrôle ne trouve pas de changement des conditions, effets ou champs hors conclusions, sauf les changements de groupe explicitement demandés et documentés.

## Vérifications exécutées sur les fichiers actuels

- Comparaison des **vingt et un fichiers** répertoriés dans les reçus des groupes : toutes les empreintes finales correspondent. Aucun indice de perte ou d'écriture partielle dans ce périmètre.
- Réexécution des vérifications de `issue27_journal_outcomes_audit.py` par import avec Python 3.12.14, depuis les sauvegardes originales conservées dans le dossier temporaire. Huit journaux/quinze issues pour `first`, huit/dix-sept pour `sick-man` : tous les contrôles passent.
- Le validateur historique compare aussi les groupes. Pour ce contrôle cumulatif, seuls les changements de groupe figurant dans les reçus sont appliqués **en mémoire à la baseline** avant `check_journal`. Aucun fichier de référence ni validateur n'est réécrit et aucune autre différence n'est ignorée.
- Inventaire de tous les fichiers `.txt` de `common/journal_entries` avec le lecteur de champs directs du validateur : **1 425 champs hérités, 170 fichiers, 418 identifiants de journal concernés**. Aucun échec de lecture ni identifiant de journal dupliqué dans cet inventaire local. Ces chiffres incluent du contenu hérité, conditionnel ou non actif en 1776 ; ils ne mesurent pas des bugs distincts ni un pourcentage de migration.
- `build_historical_journal_banners.py --mod-root . --vanilla-root "C:/Games/Victoria 3/game"`, sans `--write` : **PASS_ASSET_STATIC_ONLY** pour les deux DDS. Dimensions 1108 × 200, DXT5, onze niveaux de mipmaps ; exports reproductibles et lecture réussie.

La preuve machine, l'inventaire complet et les empreintes des scripts lus sont dans `V1_15_RECOVERY_AUDIT_2026_11_07.json`. Un contrôle de tokens ou de texture ne vaut pas validation du moteur ou de l'affichage.

## Ce qui reste à faire

### Poursuivre les migrations par lots bornés

| Fichier | Champs hérités encore présents | Motif de reprise |
| --- | ---: | --- |
| `00_urbanization.txt` | 4 | Erreurs de scope de population réellement observées, en plus des anciennes conclusions. |
| `00_suffragists.txt` | 3 | Dette de conclusions déjà repérée dans le diagnostic initial. |
| `05_great_eastern_crisis.txt` | 7 | Continuation directe de l'échec ottoman avec le DLC concerné ; son regroupement ne l'a pas migrée. |
| `06_usa_independence_mod.txt` | 8 | Chaîne d'indépendance américaine principale. |
| `00_canada_australia.txt` | 10 | Fichier partagé ; isoler les entrées canadiennes si c'est le périmètre retenu. |
| `06_spanish_new_world.txt` | 19 | Chaînes hispano-américaines. |
| `06_cuba.txt` | 11 | Fichier partagé ; tout son contenu n'appartient pas au groupe des Amériques. |
| `06_french_revolution_mod.txt` | 5 | Révolution française regroupée mais pas migrée. |
| `07_poland_lithuania_mod.txt` | 16 | Réformes polono-lituaniennes. |
| `00_poland.txt` | 4 | Restauration polonaise. |
| `00_peoples_springtime_je.txt` | 11 | Situation internationale : préserver contexte global et effets de tous les pays impliqués. |
| `05_hungry_forties.txt` | 1 | Ancien champ encore présent. |
| `09_forest_of_bayonets.txt` | 0 | Déjà au format natif ; surcharge ajoutée uniquement pour le groupe. |

Ordre proposé : corriger l'urbanisation et traiter les suffragistes comme petit lot, puis migrer la Grande Crise orientale pour fermer la dépendance ottomane, avant les chaînes américaines et franco-polonaises. Ce diagnostic ne lance pas ces lots.

### Résoudre les écarts de contenu et de livraison

1. Les quatre identifiants `je_polish_partitions`, `je_polish_partition_russia`, `je_polish_partition_prussia` et `je_polish_partition_austria` existent dans les localisations FR/EN, mais la recherche dans `common` et `events` ne trouve ni définition active ni consommateur. Ils ne peuvent donc pas simplement être déplacés dans un groupe. Leur cause historique et leur éventuelle restauration demandent une investigation distincte ; aucune mécanique n'est inventée ici.
2. Le visuel d'État et révolution est un **master adapté**, comme le précise le reçu précédent, et non une copie exacte de l'image fournie. Son export est valide ; sa conformité visuelle à la demande reste à apprécier.
3. Au moment de la consultation, la [PR #34](https://github.com/Malzars-sys/1776-Age-of-Revolutions/pull/34) est ouverte, en brouillon, non fusionnée, à la révision `6d2d9f7684f1c5618b9c17ec6e558b44b6f7deab`. Sa liste de vingt-quatre fichiers contient les deux lots migrés, mais **pas les nouveaux groupes, leurs localisations ni leurs assets**. Ces derniers sont présents localement et restent à livrer sur la branche selon l'autorisation Git d'une mission ultérieure.
4. L'[issue #27](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/27) est ouverte et demande encore revue et acceptation en jeu. Aucun statut de projet n'a été modifié ni certifié par cet audit.

## Logs observés et validation restante

Le jeu a laissé un enregistrement `release/1.15.0`, révision `6338547985dbc271523e149f362a6fd93dc62975`, avec un début de session à 15 h 55 le 7 novembre, heure de Paris. Les logs d'erreurs disponibles vont jusqu'à 18 h 43. Il existe donc une exécution postérieure aux premiers correctifs, mais aucun manifeste de la version effectivement chargée ne permet de certifier tous les chemins migrés. Le regroupement étendu a été livré après le début de cette session ; ses fichiers actuels ne prouvent pas qu'il était chargé.

L'ensemble disponible `error.log` et `error.1.log` à `error.5.log` contient notamment **2 709 emplacements d'erreur désignant `00_urbanization.txt:7` ou `:18`**. Le fichier local emploie encore `pop_type = peasants` et `percent`, alors que l'exemple canonique 1.15 emploie `target = pop_type:peasants` et `value`. Cela confirme un chantier concret ; remplacer uniquement les wrappers de conclusion ne résoudrait pas ce problème.

D'autres erreurs de région, culture, religion et connexions navales figurent dans ces logs. Elles ne sont pas attribuées aux deux lots migrés et ne sont pas corrigées dans cette mission. Les fichiers sont tournants : leur absence d'un message ne prouve pas sa disparition.

Avant de clore #27 : nouvelle partie en 1776 après redémarrage complet, contrôle des trois groupes et bandeaux, succès/échec/invalidation/délai, compteurs et nettoyage appliqués une seule fois, cas DLC, sauvegarde/rechargement et comparaison des logs avec la baseline #20. La priorité des conclusions simultanées et le nettoyage lors d'un retrait forcé restent à vérifier. Les alertes d'initialisation de ferveur américaine et d'ajouts impériaux en double restent des dettes distinctes à reproduire.

La seconde passe immersive des textes attend la validation humaine des mécanismes correspondants. Aucune validation humaine nouvelle n'est déduite du simple passage de ces contrôles. Les correctifs navals #36 déjà acceptés et les autres travaux concurrents sont préservés.

## Suite de mission — migration et urbanisation

Le lot demandé ensuite est installé : deux fichiers, cinq journaux, treize champs hérités remplacés par huit issues, avec correction des trois comparaisons paysannes. Statut IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Les preuves et le protocole sont dans [le rapport du lot](V1_15_MIGRATION_URBANIZATION_2026_11_07/REPORT.md). L’inventaire actualisé comporte 1412 champs hérités dans 168 fichiers ; ce n’est pas un nombre de bugs.

L’investigation polonaise retrouve le mécanisme de partage dans la copie source voisine 2.3.1 et son retrait au commit 4b299b14. Les quatre clés sont des localisations sans définitions actives dans les deux versions inspectées ; le code supprimé était le délai de 6 000 jours et les transferts forcés de je_plc_reform. Cette conclusion documentée complète l’incertitude du diagnostic initial. Le journal actuel reste inchangé.

## Retour joueur — corrections canadiennes, polonaises et du Nord-Ouest

Le redémarrage du joueur et ses captures ont permis de confirmer la clé canadienne brute et l’absence des conclusions polonaises. Un nouveau lot installe onze journaux migrés dans trois fichiers, avec les alias canadiens FR/EN, sans restaurer le partage automatique. L’urbanisation et les trois migrations du lot précédent ne sont pas désignées par des erreurs dans les logs conservés ; leurs parcours complets restent à tester. Voir [le rapport de retour joueur](V1_15_RUNTIME_FEEDBACK_2026_11_07/REPORT.md).
