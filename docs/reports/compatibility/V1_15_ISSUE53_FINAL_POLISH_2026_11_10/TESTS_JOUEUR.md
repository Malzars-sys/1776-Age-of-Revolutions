# Session de tests regroupés — toutes les missions en revue

Périmètre vérifié dans le tableau GitHub : **48, 49, 50, 51, 52 et 53**, toutes en **In review** le 10 novembre 2026. Les nouveaux arrivants 48, 49 et 52 sont inclus. Aucun résultat moteur n'est encore déduit de ce statut.

L'ordre ci-dessous permet de tout regrouper dans une session. Il faudra plusieurs parties ou copies pour les pays et les choix incompatibles entre eux ; une seule partie ne permet pas de choisir toutes les options. Les missions déjà acceptées n'ont pas à être rejouées.

## Console : lancer les essais immédiatement

Lancer le jeu en mode débogage (`-debug_mode` dans les options de lancement, ou le bouton de lancement en débogage du launcher). Ouvrir la console avec `²` sur un clavier français ; selon la disposition, utiliser la touche de console `~` ou `§`. Travailler dans une copie de test, en pause avant chaque commande.

**Chaque ligne ci-dessous est une commande complète à saisir séparément.** `tag` change le pays joué ; `event` ouvre un événement ; `add_journal_entry` ajoute une entrée au journal du pays joué. Ne pas saisir seulement un identifiant tel que `phase1_japan_tenpo.1`. Après ajout, fermer la console et ouvrir le panneau **Journal**, puis développer le groupe correspondant et survoler les conditions. Ne pas ajouter une seconde fois une entrée déjà active.

L'aide intégrée permet de consulter la syntaxe de cette version :

```text
help event
help add_journal_entry
help effect
```

Ces commandes servent à tester directement l'affichage et les effets. Un ajout forcé ne valide pas les conditions naturelles d'apparition. Les entrées ajoutées pour lire une infobulle peuvent se terminer ou échouer au prochain tick : rester en pause pour cet examen. Les lignes `effect` ci-dessous sont vérifiées contre les identifiants et les exemples du mod/vanilla local, sans exécution moteur par l'agent.

## Préparation et sélection des pays — 50

- [ ] Redémarrer complètement le jeu avec le mod courant et les DLC habituels. Commencer les essais depuis de nouvelles parties en 1776 pour charger les nouveaux bâtiments. Garder la même version du mod pendant la session.
- [ ] Sur la sélection des pays, consulter les aperçus de journaux de plusieurs pays, dont une grande puissance et un pays sud-américain existant. Le différend de l'Acre ne doit pas être proposé à un pays étranger à sa condition bolivienne ; aucune Bolivie ne doit apparaître par ce correctif.

Pour cette mission, **ne pas forcer l'ajout du différend de l'Acre** : cela contournerait précisément le filtre d'affichage à contrôler. Le test se fait immédiatement dans la sélection des pays, sans attendre une date ou un événement.

## Ports britanniques et du royaume de Mosquito — 48

Pour prendre le contrôle des deux propriétaires, successivement :

```text
tag GBR
tag MKT
```

- [ ] Dans le **Guatemala britannique**, vérifier un port niveau 1 utilisant le port de base.
- [ ] Au **Nicaragua du royaume de Mosquito**, vérifier un port niveau 1 utilisant le port commercial traditionnel.
- [ ] Laisser passer quelques semaines et vérifier, pour chacun, recrutement, intrants et liaison maritime effective. Le niveau construit ne garantit pas un plein emploi au jour 1.

## Japon : choix économiques et texte du journal — 49 et 53

Prendre le Japon puis ouvrir immédiatement le premier événement :

```text
tag JAP
event phase1_japan_tenpo.1
```

Les événements suivants se lancent de la même façon, **un à la fois**, après avoir réglé la fenêtre précédente. Il n'est pas nécessaire d'attendre leurs années historiques :

```text
event phase1_japan_tenpo.2
event phase1_japan_tenpo.3
event phase1_japan_tenpo.4
event phase1_japan_tenpo.5
```

Pour comparer les trois choix de l'événement 1, sauvegarder **avant** de le lancer, puis recharger cette copie pour chaque branche. Répéter le même événement dans une partie déjà modifiée cumulerait ses effets.

Pour rendre immédiatement disponible l'ouverture des réserves dans l'événement 5, utiliser cette préparation dans une copie de test, puis lancer l'événement :

```text
effect c:JAP = { set_variable = aor1776_japan_grain_reserves remove_variable = aor1776_japan_grain_procurement_active every_scope_state = { remove_modifier = aor1776_japan_grain_procurement } }
event phase1_japan_tenpo.5
```

Cette préparation simule un stock prêt et la fin des achats ; elle ne valide pas l'expiration naturelle de ces achats. Les greniers permanents éventuellement construits sont conservés.

- [ ] Dans l'événement des réserves (`phase1_japan_tenpo.1`), survoler les trois choix : les coûts du Trésor, les achats de grain, les réactions des groupes d'intérêt et la durée des effets doivent être lisibles.
- [ ] **Constitution des réserves :** constater le coût du Trésor, les greniers permanents et **+15 points de sécurité alimentaire** dans les États possédés. Les achats retirent temporairement **10 unités de grain par État producteur pendant deux ans**.
- [ ] Depuis une copie antérieure au choix, vérifier **le secours direct** : **+10 points pendant trois ans**, coût du Trésor inférieur et absence du réseau permanent. Depuis une autre copie, vérifier **le laisser-faire** : coût immédiat évité, perte de légitimité et mécontentement.
- [ ] Lancer les événements 2–5 avec les commandes ci-dessus, inspecter leurs choix et essayer quelques effets : discipline, autonomie, surveillance, diplomatie/défense et réquisition. Pour l'ouverture des réserves dans l'événement 5, vérifier que le choix exige un stock constitué et des achats terminés ; il rend du grain au marché pendant un an, consomme le stock mobilisable et conserve les greniers permanents.
- [ ] Dans la restauration Meiji encore inactive, l'objectif doit afficher une phrase lisible : propriétaires terriens exclus du gouvernement, paix, absence d'insurrection, possession de tout le Kantō et légitimité d'au moins 50 ou propriétaires marginaux. La clé restaurée est utilisée avant l'activation : consulter d'abord l'entrée parmi les entrées potentielles.

Pour remettre cette entrée dans son état inactif et lire cette branche de texte, toujours en pause au Japon :

```text
effect c:JAP = { remove_journal_entry = je_meiji_restoration remove_variable = shogunate_var }
```

Puis, pour ouvrir sa version active sans attendre ses conditions politiques :

```text
add_journal_entry je_meiji_restoration
```

L'activation initialise sa variable de progression. Ne pas enlever cette variable d'une entrée active ; ne pas dépauser ce test d'affichage si les propriétaires sont encore au gouvernement, car son échec serait alors normal.

Les +15 et +10 sont des **points** de sécurité alimentaire, pas une baisse garantie de tous les dégâts de récolte. Le prix du grain dépend aussi du marché. Les événements déjà résolus dans une ancienne sauvegarde ne se rejouent pas automatiquement. Le sixième événement conserve son pont vers la crise Tenpō et sa condition DLC ; ne pas attendre toutes ces chaînes au début de 1776.

## Maroc : trois régions, puis sauvegarde et rechargement — 51 et témoin 50

Prendre le Maroc. La seconde ligne ajoute le journal **uniquement s'il manque**, sans réinitialiser une entrée existante :

```text
tag MOR
effect c:MOR = { if = { limit = { NOT = { has_journal_entry = je_lands_of_anarchy } } add_journal_entry = { type = je_lands_of_anarchy } } }
```

Pour créer immédiatement trois valeurs différentes et vérifier que chaque pénalité lit bien sa propre barre :

```text
effect c:MOR = { je:je_lands_of_anarchy = { set_bar_progress = { name = lands_of_anarchy_tribes_of_al_rif_bar value = 400 } set_bar_progress = { name = lands_of_anarchy_tribes_of_marrakech_bar value = 100 } set_bar_progress = { name = lands_of_anarchy_tribes_of_inner_morocco_bar value = 260 } } }
```

Faire ce changement **après** le contrôle initial à 260. Ensuite, laisser réellement passer un changement de mois à vitesse maximale : il faut exécuter la mise à jour mensuelle. Changer seulement la date avec la console ne remplace pas cette simulation. Les valeurs peuvent encore évoluer au changement de mois ; comparer les pénalités aux barres effectivement affichées.

- [ ] Dans une nouvelle partie marocaine, inspecter les trois barres du **Rif, de Marrakech et du Maroc intérieur**, ainsi que les pénalités sur les portions marocaines correspondantes. Toutes les valeurs doivent être numériques ; valeur initiale conservée : 260, multiplicateur initial attendu : 2,55.
- [ ] Passer un changement de mois. Si une barre évolue, sa pénalité régionale doit la suivre ; les deux autres régions doivent conserver leur valeur propre.
- [ ] Sauvegarder, recharger et passer un autre mois. Vérifier à nouveau les trois barres, leurs pénalités et le fonctionnement habituel des journaux. Ce rechargement sert aussi de témoin général pour la mission 50.

Les changements de propriétaire et la reconquête du détroit ne sont pas modifiés par cette correction et ne sont pas certifiés par cet essai.

## Fort terrestre : extension et bâtiment témoin — 52

Pour disposer d'un pays et de la technologie nécessaires, prendre la France ; la seconde ligne débloque les deux technologies dans **la sauvegarde de test uniquement** :

```text
tag FRA
effect c:FRA = { add_technology_researched = organized_military_establishments add_technology_researched = scientific_fortification_siegecraft }
```

Choisir ensuite la **Bourgogne**, un État intérieur, et son fort terrestre. S'il n'y en a pas, la commande suivante permet d'accélérer la construction du premier niveau par l'interface :

```text
fastbuild
```

Vérifier que la console indique son activation. Construire le niveau de préparation, puis saisir **à nouveau `fastbuild` pour le désactiver avant de tester l'extension**. Avec la construction instantanée encore active, le ralentissement n'est pas mesurable. Les prérequis et les limites géographiques restent ceux du bâtiment.

- [ ] Dans un pays capable de construire des forts terrestres, choisir un État intérieur autorisé. Inspecter un fort existant et lancer une extension : le coût affiché reste **900**, avec une progression ralentie selon les niveaux déjà construits.
- [ ] Vérifier le palier correspondant dans cette table. Il suffit de constater le bon palier disponible et son application ; il n'est pas demandé de construire cinq niveaux ni de mesurer les coûts au centième.

| Niveaux déjà construits | Niveau à construire | Pénalité d'efficacité propre au fort | Coût effectif visé avant autres bonus |
| ---: | ---: | ---: | ---: |
| 0 | 1 | 0 % | 900 |
| 1 | 2 | environ −18,18 % | 1 100 |
| 2 | 3 | environ −30,77 % | 1 300 |
| 3 | 4 | −40 % | 1 500 |
| 4 | 5 | environ −47,06 % | 1 700 |

- [ ] Vérifier que le plafond reste à **cinq niveaux**, que les PM de garnison fonctionnent et qu'un autre type de bâtiment ne reçoit pas cette pénalité d'extension.

## Tutoriel et autres infobulles accessibles — 53

**Tutoriel :** une commande simple d'ajout laisserait sa cible manquante. Cette ligne choisit un État côtier britannique et lui transmet correctement son bien de marine marchande :

```text
tag GBR
effect c:GBR = { random_scope_state = { limit = { is_coastal = yes } sg:merchant_marine = { save_scope_as = aor1776_debug_supply_target } } add_journal_entry = { type = je_tutorial_improve_supply_network target = scope:aor1776_debug_supply_target } }
```

- [ ] En pause, vérifier ses deux explications et sa cible de **marine marchande dans un État côtier**. Puis laisser passer le temps pour constater le résultat selon le prix réel. L'entrée doit se terminer quand le surcoût devient **strictement inférieur à 10 %**, sans objectif de +400 convois. Si le prix est déjà sous ce seuil, sa clôture rapide est attendue. Cette commande ne certifie pas la sélection naturelle du sous-objectif, qui exige initialement plus de 30 % de surcoût.

**Grand Jeu :** prendre la Russie et ajouter les deux objectifs. Les examiner en pause ; leurs branches de succès et d'échec sont visibles sans devoir les accomplir :

```text
tag RUS
add_journal_entry je_secure_persian_border
add_journal_entry je_pacify_kazakh_steppes
```

- [ ] Vérifier les quatre textes de succès et d'échec de la consolidation du Caucase et de la soumission des steppes kazakhes. Rester en pause : ces objectifs s'invalident en l'absence du journal principal du Grand Jeu. Il n'est pas nécessaire de lancer toute cette mécanique pour vérifier leurs textes.

**Caucase :** ces deux pays existent dans le scénario 1776. Ajouter chaque entrée chez son propriétaire puis ouvrir le journal correspondant, en pause :

```text
tag CIR
add_journal_entry je_caucasian_war_circassia
```

```text
tag CHC
add_journal_entry je_caucasian_war_imamate
```

- [ ] Dans la première, vérifier le texte concernant le Kouban ; dans la seconde, ceux du Daghestan et du Caucase du Nord. Avec l'objectif Meiji et les quatre textes du Grand Jeu, cela couvre les huit infobulles restaurées. Ne pas déclencher les victoires pour ce simple contrôle de texte.

Aucune attente de plusieurs décennies n'est nécessaire. Les commandes préparent des cas de test ; elles n'attestent pas les déclenchements naturels, la progression historique ni toutes les issues. Noter **non testé** seulement ce qui n'a effectivement pas pu être essayé, notamment un contenu DLC absent. Le français testé ne vaut pas une attestation de rendu anglais.

## Une seule vérification des erreurs, à la fin — 48 à 53

- [ ] Me signaler les nouveaux messages du journal d'erreurs issus de cette session. Je pourrai les comparer aux captures antérieures. Les diagnostics visés sont :

| Mission | Message ancien qui ne doit plus revenir dans le contexte testé |
| --- | --- |
| 49 / 52 | Avertissement d'encodage du nouveau fichier de modificateurs japonais |
| 50 | Portée bolivienne absente dans l'aperçu du différend de l'Acre |
| 51 | Valeur de type absent ou incorrect dans les six calculs des pénalités marocaines |
| 52 | Trois coefficients de construction des forts signalés comme `Malformed token` |
| 53 | `num_convoys_available` dans le tutoriel et les huit clés de texte inconnues |

Ne pas effacer le journal pour faire disparaître un constat. Une erreur différente reste à examiner séparément. Les anciens numéros de ligne peuvent avoir changé.

## Retour en une fois

Un retour **passe / problème / partiel / non testé** pour chacun suffit :

- 48 — deux ports et liaison maritime :
- 49 — choix japonais et effets :
- 50 — aperçus du journal et rechargement :
- 51 — trois régions marocaines et deux changements de mois :
- 52 — palier de fort et bâtiment témoin :
- 53 — tutoriel et infobulles effectivement consultés :
- Nouveaux messages d'erreur ou captures utiles :

Si une branche manque, préciser simplement laquelle. Aucun nom de sauvegarde ni relevé de date n'est demandé. Le cas positif de l'Acre avec une Bolivie existante et le lancement sans Colossus of the South ne sont pas requis dans cette session unique ; ils restent non testés s'ils n'ont pas été essayés.

Après ton retour, nous préparerons l'export Steam allégé de la version testée. Les outils et la documentation de développement seront exclus de la distribution, tout en restant conservés dans les sources.
