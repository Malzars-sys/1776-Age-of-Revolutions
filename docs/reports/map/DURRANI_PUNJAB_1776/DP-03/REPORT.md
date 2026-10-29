# DP-03 — Troisième passe Durrani et Pendjab

Référence : **1er janvier 1776**. Installation du 29 octobre 2026. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucun lancement de Victoria 3 ni contrôle joueur n'est attesté pour cette version. L'Asie centrale n'est pas commencée.

## Résultat installé

Six cellules existantes réattribuées dans deux State_ID, sans nouveau bitmap ni découpage de province :

| RGB du bitmap | Région | Avant | Après | Motif |
|---|---|---|---|---|
| x251424 | STATE_HILL_PUNJAB | Kangra | Chamba | Noyau de Chamba confirmé par le nouveau calage physique |
| xE31B4E | STATE_HILL_PUNJAB | Bashahr | Kullu | Noyau de Kullu |
| x0003C6 | STATE_HILL_PUNJAB | Garhwal | Bashahr | Noyau de Rampur |
| x5990A7 | STATE_KASHMIR | Durrani | Ladakh | Kargil/Purig ; rattachement au Ladakh en 1758 |
| x5A0252 | STATE_KASHMIR | Durrani | Gilgit, D3G | Gouvernement local sous Guritham |
| x6326A6 | STATE_KASHMIR | Durrani | Skardu, D3S | Gouvernement local sous Murad Khan II |

Les trois premiers transferts remplacent explicitement trois attributions de DP-02. Les autres attributions de DP-02 et les 19 transferts de DP-01 sont protégés. Leurs rapports et baselines restent immuables : leurs anciennes assertions sur les trois cellules remplacées ne décrivent plus la version courante.

Gilgit et Skardu reçoivent définitions, profils nationaux explicites, dirigeants, lois locales, formations de conscrits, localisation française et anglaise et pavillons provisoires. Skardu conserve une allégeance durranie très lâche, par le type existant, sans prélèvement régulier ; sa portée historique précise reste une réserve, pas une preuve d'administration afghane directe. Gilgit est indépendant dans cette représentation. Aucun souverain du XIXe siècle n'est avancé à 1776.

Dans STATE_KASHMIR, **ID natif 463**, le hub urbain « Srinagar », auparavant placé vers Skardu, est déplacé dans la vallée du Cachemire ; le hub minier « Kargil », auparavant vers Khaplu, est déplacé dans la cellule de Purig. Les pointeurs `city` et `mine` de la région suivent exactement les pixels des nouveaux locators. Aucun autre hub n'est déplacé. Les six chiffres hexadécimaux du tableau sont des couleurs de province, pas des identifiants de principauté ou des State_ID.

Jammu est conservé après contrôle de son noyau. Bahawalpur reste à dix cellules, Makran à dix-huit, Kharan à quatre, Las Bela à six et Kalat à dix-sept. Les sources et le calage ne justifient pas une nouvelle extension ou réduction précise de leurs confins ; cette conservation n'est pas un certificat d'exactitude de chaque frontière.

## Population, bâtiments et unités

Le fichier `10_india.txt` conserve **190 000 000 habitants**, les tailles de cohortes et tous leurs champs explicites. Gilgit reçoit la cohorte kho existante de **34 533** personnes ; Skardu deux cohortes existantes totalisant **23 220**. Les petites corrections entre propriétaires des collines ne servent pas à inventer une densité de population par pixel : leurs stocks nationaux sont conservés.

Cette allocation est **technique, pas un recensement de 1776**. La cohorte tibétaine de Skardu conserve notamment sa religion implicite héritée ; les cultures `tibetan` et `kho` ne sont pas des représentations fines du balti et du shina. La composition religieuse et démographique des nouveaux pays demeure à reprendre dans une passe spécialisée. Aucun changement de confession des POPs n'est caché dans ce transfert. La religion chiite de la dynastie de Gilgit est une inférence explicite à partir de Keene, pas une mesure de sa population.

**Tous les fichiers de bâtiments restent identiques** à la baseline courante. Les propriétaires restants possèdent encore une portion des régions référencées ; aucune installation n'est supprimée. Deux conscrits existants sont réaffectés, un à Gilgit et un à Skardu : la formation durranie du Cachemire passe de sept à cinq. Le stock régional par type et service reste identique, sans nouvel effectif régulier.

## Vérifications

Commandes : Python fourni par l'environnement, `-X utf8 tools/dp03_audit.py --staged`, puis `tools/dp03_refine.py --apply` et `tools/dp03_audit.py`. Résultats effectifs et dénominateurs dans `PREFLIGHT.json` et `VALIDATION.json` ; le bilan final est généré dans `STATUS.json`.

- Propriétaires : exactement les six changements prévus ; une seule attribution de chaque province des deux régions, cellules dans le bon State_ID et passables.
- Continuité : tous les pays locaux concernés restent reliés par des frontières de cellule partagées d'au moins deux pixels. Ce n'est pas un test d'accès militaire moteur.
- Dépendances : cohortes conservées, bâtiments inchangés, unités conservées, références de propriétaires POP/bâtiments valides, capitales dans une région possédée, dirigeants uniques, lois et pavillons bornés aux nouveaux pays, textes FR/EN complets avec BOM et sans doublon local.
- Carte : bitmap, ressources, State_ID et autres régions préservés ; seuls deux pointeurs de hubs et deux positions ID 463 changent. Les nouveaux points correspondent à leurs cellules terrestres et ne tombent pas sur un pixel de rivière.
- Profils : Gilgit et Skardu `PASS_STATIC_ONLY` ; aucune nouvelle alerte sur les pays témoins. DUR conserve **six alertes préexistantes**, PAN **quatre**. Ces dettes ne sont pas des régressions de DP-03, ni des erreurs de chargement observées.
- Concurrence : comparaison à des préimages fraîches et contrôles d'empreinte avant écriture ; pas de restauration de fichiers partagés depuis DP-01/DP-02. Le journal final distingue tout éventuel delta extérieur. Aucune opération Git d'écriture et aucune modification du vanilla.

La première installation et son contrôle de 71 assertions restent archivés. `REPAIR_01.json` documente ensuite la correction de trois champs du profil dynastique de Gilgit, de la religion culturelle par défaut à la tradition chiite signalée par la source. Le manifeste final est `CURRENT_RUNTIME_MANIFEST.json` ; les anciennes empreintes ne sont pas réécrites pour dissimuler cette révision.

## Limites historiques et suite

Le nouveau calage s'appuie sur les rivières plutôt que sur des villes mal placées. Sa méthode, son premier essai insuffisant, les contrôles réaffectés et les extrapolations non fiables sont publiés dans [SOURCES.md](SOURCES.md). La carte Yale localise les cours ; elle ne délimite pas leurs droits en 1776. Les transferts portent donc sur des **noyaux de juridiction dans des cellules grossières**, jamais sur un cadastre reconstitué.

Hunza et Nagar partagent une cellule avec Gilgit ; Shigar partage celle de Skardu. Leur autonomie historique n'est pas résolue par cette abstraction. Khaplu reste une dépendance indirecte approximative dans LAD. Les micro-juridictions, le fort de Kangra, les limites fines de Zanskar/Spiti, Bela, les rapports fiscaux Kalat–Gichki–Kharan et les démographies locales restent des réserves V2 explicites. Pas de quatrième audit général automatique et pas de clôture historique à 100 %.

La troisième passe remédie aux erreurs de noyaux identifiées et suffit à livrer **une V1 affinée à tester**, plutôt qu'à prolonger indéfiniment ce chantier. Le protocole de chargement, marchés, mobilisation, rendu des locators et sauvegarde est dans [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md). Le passage ultérieur à l'Asie centrale demande son propre lot ; il ne constitue pas une homologation rétroactive de ces tests en jeu.

## Recherche locale et ressources

**Zéro nouvel appel ColGrep-Agent-2B** dans DP-03 : l'échec antérieur d'accès au verrou de l'index n'a pas été répété. Les chemins des outils et dossiers étaient connus ; les identifiants exacts ont été vérifiés par lecture et `rg`. Pas de nouvelle installation, changement de modèle, intégration ou reconstruction d'index. Les fichiers non indexés de carte ont été lus directement.

Aucun compteur fiable de tokens par mission ni chronométrage exhaustif des recherches n'est disponible ; le nombre total de recherches classiques et les économies supposées ne sont donc pas inventés. Ce lot ne permet **pas** de mesurer une économie de quota due au 2B, puisqu'il n'a pas été exécuté. Les archives de recherche existantes ont en revanche été réutilisées sans recommencer l'audit régional entier.
