# Froid, doublage en cuivre et transport à voiles

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — 8 novembre 2026.** Corrections installées localement. Aucun lancement de partie, simulation ou test moteur réalisé par l'agent. Le mainteneur effectuera la passe moteur groupée. Aucun fichier vanilla modifié ni opération Git d'écriture.

## Froid et saisons

Le système mécanique de froid appartient à la mise à jour gratuite 1.15 ; les effets visuels saisonniers appartiennent à State and Revolution. Cette distinction est explicite dans le [Dev Diary 189 officiel](https://steamcommunity.com/games/529340/announcements/detail/698776157349216523) et dans les [notes de sortie 1.15](https://steamcommunity.com/app/529340/announcements/).

Les définitions de froid et le fichier maritime `99_seas.txt` étaient déjà hérités du vanilla. Les anciennes surcharges des seize fichiers d'états terrestres masquaient en revanche les nouveaux champs `min_cold_effect` et `max_cold_effect`.

- **520 états** reprennent exactement les deux valeurs de leur état vanilla de même identifiant.
- **Six états propres au mod** reçoivent un héritage climatique régional explicite, détaillé ci-dessous.
- Frontières, identifiants de provinces, ressources, terres arables, sorties navales, hubs et autres champs des états sont conservés. Les comparaisons structurelles avant/après retirent seulement les deux champs climatiques.
- Aucun paramètre de saison, seuil ou effet n'est rééquilibré. Les mers restent natives. Les fichiers d'effets visuels et de paramètres graphiques saisonniers ne sont pas masqués par le mod.

| État propre au mod | Donneur vanilla | Minimum estival | Maximum hivernal |
| --- | --- | ---: | ---: |
| `STATE_WEST_FLORIDA` | `STATE_FLORIDA` | 0,00 | 0,07 |
| `STATE_UNALASKA_TRADING_POST` | `STATE_ALASKA` | 0,14 | 0,93 |
| `STATE_TARTARIA` | `STATE_SARATOV` | 0,02 | 0,60 |
| `STATE_CHUKOTKA` | `STATE_KAMCHATKA` | 0,08 | 0,80 |
| `STATE_KAUNAS` | `STATE_LITHUANIA` | 0,00 | 0,61 |
| `STATE_GALICH` | `STATE_VOLOGDA` | 0,11 | 0,88 |

Les correspondances Saratov, Kamchatka et Lituanie couvrent toutes les provinces d'origine reconnues des trois subdivisions concernées. Galich est très majoritairement issu de Vologda ; Floride occidentale recoupe plusieurs régions et reprend sa composante dominante par nombre d'identifiants de provinces. Le poste d'Unalaska utilise conventionnellement son ensemble régional d'Alaska. Ces six affectations sont des **approximations de gameplay à la granularité vanilla**, pas des relevés météorologiques locaux ni une nouvelle recherche territoriale. Les donneurs et valeurs sont conservés dans `CLIMATE_DONORS.json`.

Valeurs mécaniques observées dans l'installation 1.15.0 : froid modéré à partir de 0,50, sévère à partir de 0,75 ; vitesse navale −50/−95 %, accès au marché mondial −15/−33 %, besoin supplémentaire de navires de ravitaillement +33/+66 %. Ces valeurs décrivent les modificateurs de base, avant les autres facteurs. Le chiffre provisoire de +50 % d'un ancien carnet de développement n'est pas repris comme valeur finale.

**Rendu visuel : non certifié.** La section utilisateur `seasons` observée est vide, donc aucun choix explicite n'a été constaté dans ce fichier. Le paramètre graphique natif `SEASONS_STRENGTH` vaut 1 ; `season_settings.txt` comporte aussi un `seasons_enabled = 0` natif. Ce dernier fichier ne suffit pas à prouver l'état du réglage utilisateur ou de l'activation DLC. Aucun de ces paramètres n'a été forcé. Vérifier dans le jeu **« Activer les saisons »**, puis le rendu réel ; les données et effets mécaniques de froid sont distincts de ce choix visuel.

## Doublage des frégates et vaisseaux de ligne

Les quatre modules de coque intermédiaires et supérieurs avaient conservé leurs coûts antérieurs sans le nouveau cuivre. Ajout des quantités natives de construction :

| Module | Cuivre ajouté |
| --- | ---: |
| Frégate, coque intermédiaire | 35 |
| Frégate, coque supérieure | 35 |
| Vaisseau de ligne, coque intermédiaire | 60 |
| Vaisseau de ligne, coque supérieure | 60 |

Ce sont les coefficients de `construction_goods`, pas un nouvel entretien hebdomadaire. Les autres intrants, caractéristiques, poids IA et portes technologiques du mod restent identiques. Les coques légères continuent de permettre de construire sans cuivre. Les anciens commentaires de valeur totale des matériaux, devenus inexacts après ajout du cuivre, sont retirés. Aucun prix ni gisement de cuivre n'est modifié.

## Deux paliers de transport suffisent

La cogue avait déjà les améliorations demandées. Sa capacité augmente avec ses aménagements, sans changer de coque. Valeurs théoriques de coque plus module de portée, avant les autres bonus, pénalités et effets d'état du navire :

| Transport | Premier aménagement | Deuxième aménagement | Troisième aménagement |
| --- | ---: | ---: | ---: |
| Cogue du mod | 0,55 | 0,65 | 0,80 |
| Transport précoce vanilla, témoin | 0,90 | 1,00 | 1,20 |
| Transport moderne du mod | 1,10 | 1,25 | 1,50 |

Unité : capacité en bataillons par navire, selon les coefficients du moteur. Cela ne certifie pas la quantité effectivement embarquée dans une flotte donnée. Les modules de débarquement agissent aussi sur les marines/l'efficacité d'invasion et ne sont pas ajoutés à tort à cette capacité de transport.

**Décision : conserver cogue améliorée → transport moderne.** Le transport précoce natif joue déjà le rôle fonctionnel couvert par la cogue ; une troisième coque n'est pas nécessaire pour satisfaire la progression demandée. Aucun gain de capacité, coût, équipage, vitesse ou technologie de la cogue n'est modifié dans cette passe.

Une correction technique est toutefois nécessaire : l'absence de `ship_type_early_troop_ship` cassait les références natives de noms et de représentation des transports. La cogue existante reprend **cet identifiant natif**, en gardant son nom français/anglais, sa description, sa silhouette 2D, ses caractéristiques et ses modules. Les listes propres au mod suivent ce même identifiant ; la représentation 3D native complète du transport précoce est héritée. L'ancien fallback 3D de la cogue est retiré. Aucun troisième type jouable n'est ajouté.

**Sauvegardes :** l'ancien identifiant `ship_type_cog` n'est plus un type enregistré. Une sauvegarde contenant cet identifiant peut ne plus charger correctement. Le test de cette livraison doit donc commencer par une **nouvelle partie**, après redémarrage complet du jeu. Aucune conversion automatique de sauvegarde ni conversion gratuite entre coques n'est revendiquée.

## Preuves et contrôle

`BASELINE.json`, `before/`, `installed/`, `INSTALLED_FILES.json`, `MIGRATIONS.json` et `CHANGES.patch` permettent de vérifier les changements bornés. Les références canoniques sont conservées sous `native/`. L'installation comprend **22 fichiers existants modifiés et deux nouveaux fichiers de localisation de remplacement**.

`FINAL_VALIDATION.json` donne les résultats du dernier contrôle : **1 181/1 181 vérifications statiques réussies**, correspondance des 526 paires climatiques, préservation du contenu territorial, des autres champs des modules et de toute la cogue hors identifiant, unicité du type précoce, résolution de **25 références effectives** natives ou locales et calcul des capacités. Le comptage filtré des identifiants `STATE_*` relève 677 états terrestres, dont 671 communs au vanilla. Le contrôle compare aussi 2 898 fichiers hors lot ; quatre fichiers du chantier concurrent de navire marchand ont évolué et sont explicitement conservés. Ces changements ne sont ni réécrits ni attribués à cette livraison. Le premier `VALIDATION.json` reste le reçu de la phase d'installation.

Les outils historiques `audit_british_colonial_start.py` et `audit_naval_admin_revision.py` comportent encore leur ancien identifiant dans des plans archivés et des hypothèses d'équipage antérieures. Ils ne constituent pas les validateurs de cette livraison et leurs modes de préparation ne doivent pas être utilisés pour réinstaller ces anciennes données.

## Test moteur à faire

1. Redémarrer complètement le jeu et créer une nouvelle partie 1776 avec ce dossier de mod chargé.
2. Avec State and Revolution actif pour le visuel, vérifier **Activer les saisons**, puis comparer une région froide de Russie en hiver et en été. Vérifier aussi une région chaude témoin. L'absence de neige à un endroit ne prouve pas l'absence de froid mécanique.
3. Vérifier une route maritime froide et ses effets sur vitesse, ravitaillement et accès au marché ; la Baltique septentrionale a un maximum natif de 0,70, donc du froid modéré au pic hivernal, pas du froid sévère.
4. Dans le concepteur naval, vérifier le cuivre des quatre améliorations de coque et la possibilité de rester sur les coques légères. Respecter les technologies et l'approvisionnement requis.
5. Vérifier qu'une seule cogue apparaît comme transport à voiles, que les trois aménagements augmentent la capacité, puis comparer au transport moderne sur une partie de test éligible. Vérifier noms et représentation 3D.
6. Simuler une durée mesurée, sauvegarder/recharger et lire les nouveaux logs. Rechercher notamment les anciens rejets de `ship_type_early_troop_ship`. Aucun de ces résultats n'est encore attesté par l'agent.
