# Artillerie : trois filières de matériaux, deux paliers

8 novembre 2026 — `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` pour les recettes et noms.

Les canons conservent les trois possibilités demandées : fer, cuivre directement, ou alliages préparés. Le même choix est maintenant disponible pour les canons lisses. Les identifiants existants sont conservés pour les sauvegardes et historiques ; une seule nouvelle méthode est ajoutée : `pm_aor1776_bronze_smoothbores`.

## Recettes installées

Valeurs additives par niveau à effectif plein, en unités du jeu, avant les autres modificateurs. Les six méthodes emploient chacune 5 000 personnes ; les professions restent celles de leur palier.

| Palier | Nom français | Métal consommé | Bois dur | Artillerie produite |
| --- | --- | ---: | ---: | ---: |
| Canons | Canons en fer | 15 fer | 10 | 25 |
| Canons | Canons de bronze (cuivre) | 10 cuivre | 15 | 25 |
| Canons | Canons de bronze (alliages) | 4 alliages | 10 | 30 |
| Canons lisses | Canons lisses en fer | 20 fer | 15 | 45 |
| Canons lisses | Canons lisses de bronze (cuivre) | 20 cuivre | 20 | 45 |
| Canons lisses | Canons lisses de bronze (alliages) | 7 alliages | 15 | 55 |

Les variantes en alliages produisent respectivement **20 %** et **22,2 %** de pièces supplémentaires à effectif égal. Leur consommation de métal par pièce tombe à 0,133 puis 0,127 unité, contre 0,4–0,6 pour les autres variantes du premier palier et 0,444 pour celles du second. Il s'agit d'efficacité des recettes ; le coût des usines d'alliages, des salaires et de l'approvisionnement doit encore être observé dans l'économie complète.

Le fer autrefois ajouté à l'ancienne variante bronze est retiré. Les alliages qui étaient cumulés dans la recette fer des canons lisses sont transférés dans une option distincte et plus efficace. Les deux recettes cuivre natives, leurs quantités et leurs emplois sont inchangés.

Le mot « bronze » est conservé pour la filière native qui utilise directement le bien cuivre. Les parenthèses identifient clairement l'intrant effectivement requis ; elles ne prétendent pas décrire un canon historique fabriqué en cuivre pur.

## Prérequis et conservation

- Fer et cuivre de premier palier : prérequis existants conservés.
- Bronze préparé de premier palier : `standardized_field_artillery` et `alloysworking`, conservés.
- Nouvelle variante de canons lisses en alliages : `shell_gun` et `alloysworking`.
- Tous ces identifiants sont définis et normalement recherchables. Aucun octroi de technologie initiale, changement de bâtiment ou sélection de PM initial n'a été ajouté.
- Les méthodes à chargement par la culasse et à mécanismes de recul restent inchangées.

## Autres méthodes examinées

Les 22 consommateurs d'alliages sont inventoriés dans `VALIDATION.json`. Les canons lisses présentaient le même chevauchement direct que le premier palier : il est corrigé ci-dessus.

Les autres cas portent sur l'outillage, les meubles mécanisés, les navires métalliques, les automobiles, les armes à feu tardives, l'éclairage, les bâtiments modernes et les ustensiles. Dans ces groupes, les intrants mixtes correspondent à des procédés ou paliers distincts ; aucune autre paire de variantes natives et personnalisées « bronze » de même palier n'a été trouvée. Leurs recettes et leurs noms sont conservés. Le groupe de conducteurs cuivre/aluminium, déjà traité dans la passe précédente, conserve sa substitution et n'est pas remodifié.

## Lecture économique

Prix de définition utilisés pour le calcul : fer 40, cuivre 50, alliages 50, bois dur 40, artillerie 70. La collision de prix du cuivre natif/mod, 40/50, reste une dette séparée ; ces chiffres ne certifient pas le prix effectivement observé dans le marché.

| Palier | Filière | Valeur des intrants | Valeur des sorties | Écart avant salaires et autres coûts |
| --- | --- | ---: | ---: | ---: |
| Canons | Fer | 1 000 | 1 750 | 750 |
| Canons | Cuivre, prix 50 | 1 100 | 1 750 | 650 |
| Canons | Alliages | 600 | 2 100 | 1 500 |
| Canons lisses | Fer | 1 400 | 3 150 | 1 750 |
| Canons lisses | Cuivre, prix 50 | 1 800 | 3 150 | 1 350 |
| Canons lisses | Alliages | 950 | 3 850 | 2 900 |

Avec un cuivre à 40, l'écart brut de la filière cuivre serait respectivement 750 et 1 550. Ces écarts représentent les seuls flux de la méthode à effectif plein, et non un bénéfice garanti de bâtiment ou de chaîne complète. Une variation du prix relatif des alliages peut modifier le choix rentable ; l'avantage de production par emploi reste celui du tableau tant que l'approvisionnement et les autres modificateurs sont comparables.

## Contrôles

`tools/compatibility/v115_artillery_materials_audit.py` : **PASS_STATIC_ONLY**.

- Six méthodes distinctes, chacune reliée une seule fois au groupe des fonderies.
- Trois intrants métalliques distincts sur chaque palier, sans cumul obligatoire de fer et d'alliages dans ces six variantes.
- Quantités, sorties, effectifs égaux et avantage des alliages vérifiés.
- **620 autres recettes existantes conservées** ; deux anciennes recettes changées, une nouvelle ajoutée.
- Noms français et anglais uniques et définis une fois dans les localisations du mod.
- Quatre contrôles négatifs détectent la perte de l'avantage de sortie, une consommation d'alliages devenue trop élevée, le retour des alliages obligatoires dans la recette fer, et une quantité native de cuivre modifiée.
- **821 fichiers protégés** inchangés lors de cette exécution, en dehors des fichiers explicitement réservés à cette passe et aux références des icônes navales.

Preuves : `BASELINE.json`, `before/`, `BEFORE_RECIPES.json`, `INSTALLATION.json`, `CHANGES.patch`, `VALIDATION.json`. Le nouveau lot remplace les anciennes contraintes de conservation de ces deux recettes dans la passe cuivre du 7 novembre ; les preuves de cette passe antérieure restent historiques et ne sont pas réécrites.

Après redémarrage du jeu, vérifier les six choix de fonderies et leurs intrants à effectif comparable, le passage aux variantes en alliages, les emplois, les verrous technologiques, puis sauvegarde/rechargement. Aucun contrôle moteur ni bénéfice observé n'est certifié.

## Icônes navales

Les trois dessins corrigés sont les versions en papier en bas-relief, ocre pour la construction artisanale, violet pour le doublage et sa variante barrée. Leur intégration est un suivi distinct dans `docs/reports/assets/NAVAL_PM_ICONS_2026_11_08/revision_v2/STATUS.md`. Les premières versions métalliques sont rejetées et ne doivent pas être utilisées comme remplacement.
