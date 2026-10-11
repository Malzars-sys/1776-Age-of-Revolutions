# Wallonie : déficit d'infrastructure au départ de 1776

## Résultat et périmètre

Correction locale : **6 → 13 niveaux** de `building_railway` pour BEO en Wallonie, dans les deux déclarations historiques existantes. La sauvegarde prouve qu'elles chargent un seul bâtiment de 6 niveaux, et non deux bâtiments totalisant 12 niveaux. Le nouveau chargement de 13 niveaux reste à vérifier dans une nouvelle partie.

Les routes traditionnelles demeurent sans intrants. Aucun consommateur historique, population, frontière, technologie, relation diplomatique ou définition de PM n'a été modifié. Le **PM de canal initial de Wallonie est désactivé**, en accord avec le PM réellement enregistré dans la sauvegarde. Cela évite une pénurie transitoire au chargement, avant que l'IA ait pu évaluer les intrants des 13 niveaux. La technologie des canaux et leur possibilité de réactivation par le contrôleur restent intactes. Aucune augmentation générale des infrastructures.

## Preuves réelles avant modification

Source : `observateur_2.v3`, date interne **1776.1.1**, Victoria 3 **1.13.11**. Lecture d'une copie convertie, sans modifier la sauvegarde originale. Empreinte et extraction dans `SAVE_DIAGNOSIS.json`.

- Observation de l'utilisateur dans l'interface : environ 40 utilisés, 23 disponibles, accès au marché 73 %, population environ 1,09 million.
- Sauvegarde : Wallonie BEO, État 435, bâtiment 395, **6 niveaux / staffing 6**, subventionné, emploi équivalent complet.
- PM effectivement enregistrés : routes traditionnelles, aucun canal, aucun train, aucun transport de voyageurs.
- Le drapeau `aor1776_ai_regional_changed_this_pulse`, le délai de 180 jours et les transferts de professions sont présents : une intervention du contrôleur au lancement est enregistrée.
- Usage enregistré par l'État : **40,5**. Son cache d'infrastructure vaut **29,7**, différent de l'interface signalée. Ce cache n'est pas une mesure actualisée après le changement de PM et ne doit pas remplacer les 23 observés par l'utilisateur.
- Reconstruction cohérente avec les définitions : base 3, routes 6 × 3, ancien canal 6 × 1, bonus de commerce intérieur du bloc +10 %. Avant désactivation : `(3 + 18 + 6) × 1,10 = 29,7`. Sans canaux : `(3 + 18) × 1,10 = 23,1`. La seconde valeur est une reconstruction statique, pas une nouvelle lecture de l'interface.

## Cause du déficit et options examinées

1. Le plan ancien utilisait **25** points de consommation, contre **40,5** enregistrés dans la partie actuelle. Son résultat « 100 % PROJECTED » n'était pas un test moteur. Il calculait les bâtiments déclarés sans reproduire tous les consommateurs générés au chargement ; il n'a pas non plus suivi toutes les évolutions ultérieures du départ.
2. Ce plan comptait **4** points par niveau (3 routes + 1 canal). Les PM enregistrés après initialisation n'en fournissent plus que **3**. Les six niveaux sont bien présents : ni omission, ni double chargement, ni manque d'emploi n'explique le déficit.
3. Les routes effectivement actives n'utilisent aucun bien : une pénurie d'intrants ne peut pas pénaliser leur production actuelle. La sauvegarde n'enregistre pas directement les booléens de pénurie locale ni les prix recalculés des biens ; on ne peut donc pas affirmer quel critère précis du contrôleur a refusé les canaux.
4. Les routes à péage sont déjà débloquées par BEO. Mais elles exigeraient 24 bois et 12 outils supplémentaires à plein emploi. Dans les champs de production/consommation des bâtiments de Wallonie : bois **105,7815 produits / 184,00921 consommés**, outils **92,50921 / 47,28**, avant la demande des habitants. Ces chiffres excluent les échanges et ne prouvent pas à eux seuls une pénurie moteur. Ils montrent cependant que la voie d'approvisionnement strictement locale en bois échoue aux réserves du contrôleur ; avec l'accès au marché signalé de 73 %, sa voie d'approvisionnement par le marché exigeant 95 % ne peut pas la remplacer. Forcer ce PM risquerait de recréer une pénurie ou une rétrogradation.

La solution retenue couvre donc le besoin avec le PM actuel sans intrants, sans forcer un PM coûteux ni ajouter de producteurs de bois ou modifier les bâtiments historiques. **13 niveaux** constituent aussi le premier niveau qui reste légèrement positif sans le bonus de bloc, en tenant compte des consommateurs de propriété générés.

## Consommateurs réellement chargés

| Bâtiment | Niveaux | Usage estimé depuis les groupes |
|---|---:|---:|
| Administration gouvernementale | 1 | 1 |
| Fabriques d'outils | 3 | 4,5 |
| Mines de charbon | 4 | 8 |
| Mines de fer | 2 | 4 |
| Carrières de calcaire | 2 | 4 |
| Camps de bûcherons | 5 | 5 |
| Industries d'armement | 2 | 4 |
| Secteur de construction | 1 | 2 |
| Verreries | 2 | 3 |
| Papeteries | 1 | 1,5 |
| Centre de commerce | 1 | 0,5 |
| Quartiers d'affaires générés | 23 | 2,3 |
| Casernes générées | 3 | 0,6 |
| Centre logistique militaire généré | 1 | 0,1 |

Les infrastructures, manoirs et centres urbains de cette partie ne consomment pas d'infrastructure dans leurs groupes. Les fermes de subsistance ne sont pas comptées comme des fermes construites. Le total de cette estimation par groupes est **40,6** ; l'usage **40,5** enregistré par le moteur reste la référence, car l'estimation ne reproduit pas tous ses ajustements. L'inventaire complet, l'emploi et les PM sont dans le diagnostic JSON.

## Avant / après

| Indicateur | Avant, observation ou sauvegarde | Après, projection statique |
|---|---:|---:|
| Niveaux régionaux | 6 chargés | 13 déclarés |
| Routes seules à plein emploi | 18 | 39 |
| Infrastructure avec base et bonus de bloc existant | ≈23 interface ; 23,1 reconstruits | 46,2 |
| Usage | 40 interface ; 40,5 sauvegarde | ≈41,2 |
| Réserve | ≈−17 interface | ≈+5 |
| Accès au marché | 73 % signalés | Capacité suffisante pour 100 % ; résultat moteur non testé |

Les sept niveaux supplémentaires de propriété financière peuvent générer sept niveaux de quartier d'affaires : **+0,7** de consommation inclus dans l'estimation après. Sans bonus du bloc, la capacité projetée reste **42** contre environ **41,2** utilisés. L'accès réel dépend aussi des connexions du marché et de l'emploi.

Le coût en salaires et les recrutements supplémentaires devront être contrôlés ; leur montant après modification n'a pas été mesuré. À environ 95 % d'emploi, la capacité routière avec le bonus actuel reste proche du besoin projeté. Une réserve positive effective n'est pas garantie à emploi inférieur : la validation en jeu reste nécessaire.

## Vérification systémique, sans modification des autres États

Les **1 043 États** de la sauvegarde ont été inspectés. **69** ont un cache de capacité inférieur à leur usage enregistré ; **66 de ces 69** consomment davantage que leur ancienne estimation. Huit portent le drapeau de changement de PM au lancement. Les 69 dossiers sont conservés dans `SAVE_DIAGNOSIS.json`, avec les PM actifs et les écarts au plan ancien.

Exemples de besoin réel enregistré / ancien plan : Wurtemberg **22,5 / 6,5**, Franconie **16,5 / 6**, Fujian **52,5 / 41**, Oryol **17,7 / 7,5**. Rio de Janeiro, Washington et la Vénétie présentent également des caches déficitaires. Le problème n'est donc pas limité à la Wallonie, mais il ne justifie pas un multiplicateur universel : emploi, PM et situations locales diffèrent.

**Limite importante :** ces 69 soldes sont des valeurs sérialisées, pas 69 observations actualisées dans l'interface. Certains caches précèdent les changements de PM. Il faut mesurer les États prioritaires en jeu avant de fixer leurs niveaux. Aucun de leurs historiques n'a été changé ici.

## Validations et conservation

- Validation dédiée : seuls le nombre de parts/niveaux **6 → 13** du réseau wallon et son PM de canal initial (**canaux industriels → aucun canal**) ont changé dans chaque fichier historique ; comparaison structurelle stricte de tous les autres éléments de ces deux fichiers.
- Empreintes identiques pour tous les autres fichiers protégés de `common`, `map_data`, MAP-1C et MAP-2A. Populations, transfert du Luxembourg, administrations, unités, propriétaires provinciaux et modifications MAP-2A conservés.
- Dix scénarios du contrôleur de pénurie existant : réussis, tests de scripts sur fixtures, **pas simulation du moteur**.
- Vérification des espaces et erreurs de patch : réussie.
- Le validateur ancien MAP-2A appelle un contrôle Luxembourg qui fige l'intégralité des bâtiments de Wallonie. Il rejette désormais ce changement de niveau expressément demandé ; ce rejet de périmètre ne prouve pas une régression cartographique. La validation dédiée confirme que tous ses fichiers de carte, populations et autres historiques sont identiques au début de ce correctif. Aucun ancien rapport ou seuil de validation n'a été réécrit pour masquer cette différence.
- **Nouvelle partie après correctif : NON TESTÉE.** Sauvegarde d'avant : réellement inspectée. Pas de sauvegarde en jeu, relance, commit, merge, push ou mise à jour Steam Build effectués.

Pour le test final : redémarrer avec le dossier de travail, créer une nouvelle partie en 1776, vérifier 13 niveaux en Wallonie, le PM routier, l'emploi, les pénuries, l'infrastructure et l'accès au marché ; mesurer de nouveau après la première actualisation économique et le premier mois. Recharger `observateur_2` ne reconstruira pas les niveaux historiques.
