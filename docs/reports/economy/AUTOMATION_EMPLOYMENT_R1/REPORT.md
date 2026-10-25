# Emplois négatifs lors du cumul des automatisations

Date : 24 octobre 2026. Statut : **corrigé dans les fichiers, contrôle statique réussi ; validation en jeu à effectuer**.

## Problème enregistré

L'ajout du transport ferroviaire aux usines et aux exploitations agricoles cumule sa suppression de 1 000 ouvriers avec celles des autres PM. Plusieurs procédés modernes ont déjà remplacé une partie de leurs ouvriers par des professions qualifiées. Les suppressions restantes dépassaient alors les effectifs disponibles.

Le défaut existait également dans des combinaisons de ventilation minière, de production de machines de précision et de produits pharmaceutiques. L'organisation scientifique du travail pouvait supprimer des machinistes dans un atelier dont le procédé de base n'en employait aucun, ou trop d'ouvriers dans une centrale électrique.

L'inventaire effectif du mod et du vanilla canonique contient **131 bâtiments**. Avant cette passe, **30 types de bâtiments** présentaient au moins un coefficient d'emploi négatif parmi **14 513 combinaisons** respectant les dépendances entre PM. Les bâtiments touchés et les exemples exacts figurent dans [BEFORE.json](BEFORE.json).

## Correction

**36 recettes existantes ajustées et 9 variantes sectorielles ajoutées.** Les diminutions sont réparties entre ouvriers, machinistes, ingénieurs, agriculteurs et, pour les chaînes de montage des outillages, commerçants. Toutes les recettes conservent leur variation nette totale d'emplois. Les conversions entre professions sont aussi rééquilibrées : leur effet net reste nul, mais les effectifs de chaque profession changent.

Exemples, par niveau de bâtiment :

| PM | Ancien profil | Nouveau profil |
| --- | --- | --- |
| Boulangerie automatisée | −3 000 ouvriers | −2 000 ouvriers, −750 machinistes, −250 ingénieurs |
| Métiers automatiques | −2 500 ouvriers | −1 500 ouvriers, −750 machinistes, −250 ingénieurs |
| Chaînes de montage des meubles | −3 000 ouvriers | −1 500 ouvriers, −1 000 machinistes, −500 ingénieurs |
| Tracteurs | −2 000 ouvriers | −1 500 ouvriers, −500 agriculteurs |
| Tracteurs à moteur Diesel | −2 500 ouvriers | −1 500 ouvriers, −1 000 agriculteurs |
| Organisation scientifique, profil général | −500 ouvriers, −250 machinistes, +500 employés, +250 ingénieurs | −500 ouvriers, +250 employés, +250 ingénieurs |
| Organisation scientifique des centrales | Profil général inadapté à leurs effectifs | −200 ouvriers, −300 machinistes, +250 employés, +250 ingénieurs |

Les PM qui retirent des professions qualifiées demandent désormais un procédé de base qui les emploie. Ces conditions utilisent le mécanisme natif `unlocking_production_methods`. Par exemple, la boulangerie automatisée demande la levure chimique ; les chaînes de montage des meubles demandent les ateliers mécanisés. La liste complète des procédés compatibles est enregistrée dans [EMPLOYMENT_CHANGES.json](EMPLOYMENT_CHANGES.json).

Des groupes distincts évitent d'imposer aux fonderies d'artillerie les prérequis de fabrication de fusils, et aux alliages ceux de la production d'acier. L'organisation scientifique reçoit des profils adaptés à la chimie, aux explosifs, aux fibres synthétiques, aux chantiers navals et aux centrales. Dans la chimie, les conversions pharmaceutiques, le transport et l'organisation scientifique exigent qu'une production principale soit active : ils ne peuvent plus soustraire des employés à une usine entièrement désactivée.

La recette ferroviaire partagée reste à **−1 000 ouvriers et 5 unités de transport consommées**. Sa variante chimique ne change que son prérequis de production active. Les technologies, quantités produites, consommations de biens, bonus, pollution et icônes des recettes sont conservés. Les nouvelles variantes réutilisent les noms existants en français et en anglais.

La répartition entre professions modifie potentiellement les salaires et qualifications nécessaires. L'égalité porte sur le total net des coefficients d'emploi, avant tout écrêtage éventuel du moteur ; elle ne prouve pas l'égalité des emplois réellement occupés ni des dépenses salariales avec une ancienne combinaison invalide.

## Vérification

Résultat : **13 227 combinaisons autorisées, aucun effectif négatif dans aucune profession**, sur les 131 bâtiments. La diminution du nombre de combinaisons vient des prérequis de procédés de base, et non d'une suppression de bâtiments ou de groupes d'automatisation. Les minima par profession, avant et après, sont dans [PROFESSION_MINIMA.csv](PROFESSION_MINIMA.csv).

Le contrôle suppose toutes les technologies disponibles et ignore volontairement les incompatibilités de lois, principes et géographie. Il examine ainsi un ensemble conservateur plus large que celui accessible dans une partie précise. Les listes de PM requis sont interprétées comme des alternatives, conformément aux exemples vanilla : les deux types de machines à coudre d'une même catégorie ne peuvent pas être actifs simultanément. L'ancienne sensibilité industrielle R1 exigeait à tort tous les éléments d'une telle liste ; ce nouveau contrôle utilise la bonne lecture et ne réécrit pas l'ancien rapport.

Les **3 339 contrôles statiques** ont réussi. Ils vérifient notamment les recettes effectives relues sur disque, les références locales des dépendances, les variations nettes d'emplois de toutes les combinaisons, les champs non concernés, les localisations et les icônes héritées. Les **2 459 fichiers protégés**, les références vanilla, ainsi que la branche, HEAD et l'index Git sont inchangés.

Commande reproductible :

```text
python tools/rebalance_automation_employment.py --validate
```

Le mode sans argument ne fait que relire et examiner la base effective. `--apply` est réservé à la première application et refuse d'écraser la capture initiale.

## Validation en jeu restante

Aucun lancement, chargement ou mois simulé n'a été effectué. Le contrôle porte sur les configurations respectant les dépendances natives des PM. Le moteur doit encore être vérifié lors d'un changement de procédé de base, notamment d'une rétrogradation vers un procédé sans personnel qualifié.

Tester une usine d'outillages, une exploitation céréalière et une usine chimique avec toutes les automatisations compatibles, puis modifier leur procédé principal et sauvegarder/recharger. Vérifier les emplois affichés et la désactivation d'un PM dont le prérequis disparaît. Une ancienne sauvegarde peut encore mémoriser des PM des groupes remplacés : leur remise en cohérence au chargement reste à contrôler.

## Preuves et périmètre

- [BASELINE.json](BASELINE.json) : empreintes et copies antérieures aux écritures.
- [PLAN.json](PLAN.json) : profils, variantes, dépendances et remplacements de groupes.
- [AFTER.json](AFTER.json) : minima et nombre de combinaisons pour chaque bâtiment.
- [EMPLOYMENT_CHANGES.json](EMPLOYMENT_CHANGES.json) : tous les profils avant/après et variation du poids salarial.
- [VALIDATION.json](VALIDATION.json) : résultats détaillés, statut natif `NOT_RUN`.
- [MANIFEST.json](MANIFEST.json) : fichiers modifiés et nouveaux fichiers.

Aucun fichier de carte, d'histoire initiale, de fortification, d'armée ou de diplomatie n'est modifié par cette passe.
