# 1776 — Ajustement de la bureaucratie ottomane

## Résultat et périmètre

Réduction de **10 niveaux**, pas de dix bâtiments, dans les seules administrations directement ottomanes du départ. Les trois bâtiments restent présents, avec leurs propriétaires, réserves et méthodes de production inchangés.

| État | Avant ce lot | Après | Niveaux retirés | Fichier d’historique |
|---|---:|---:|---:|---|
| Thrace orientale / Constantinople | 30 | 26 | 4 | `common/history/buildings/01_south_europe.txt` |
| Ankara | 23 | 19 | 4 | `common/history/buildings/08_middle_east.txt` |
| Syrie | 11 | 9 | 2 | `common/history/buildings/08_middle_east.txt` |
| **Total directement ottoman** | **64** | **54** | **10** | |

Ces centres conservent donc une administration importante. Aucune administration égyptienne ou d’un autre sujet n’est réduite. Aucun État, population, technologie, unité ou autre bâtiment n’est modifié par ce lot.

Les seules modifications des historiques sont les trois valeurs `levels` des blocs d’administration possédés par `c:TUR`. La comparaison avec la révision Git antérieure prend en compte le transfert égyptien déjà effectué dans le lot précédent : ses 22 niveaux ne sont pas une suppression de ce lot.

## Journaux : conditions renforcées

Pour les **deux** journaux, il faut désormais :

- Police **et** éducation au niveau **3** au minimum, y compris pour les voies de compromis et de rétablissement administratif du journal politique.
- Rechercher **Rainurage** (`rifling`) et **Abolitionnisme** (`abolitionist_mobilization`). Ces technologies ne sont pas accordées gratuitement au départ.
- Ne plus appliquer la loi **Commerce d’esclaves**, ni ses variantes (`law_slave_trade`). Cela interdit le commerce demandé, sans ajouter une obligation non demandée d’abolir toutes les autres formes d’esclavage.

Les deux technologies et la condition légale sont des prérequis supplémentaires, **hors du compteur des dix objectifs administratifs**. Les valeurs des malus et de l’allégement temporaire sont inchangées. Le maintien de tous les objectifs et prérequis est nécessaire aux 12 mois de consolidation ; leur perte interrompt la séquence. Le journal politique conserve ses trois voies, ses 36 points de stabilité, son échéance de 1836 et son mécanisme d’échec anticipé.

Le critère « pas de pénurie imminente » exige maintenant explicitement un solde de bureaucratie **≥ 0** en plus de l’absence de pénurie imminente. Un déficit ne peut donc plus le valider.

## Interface et localisation

Les logs de la version testée identifient précisément le défaut d’affichage : `Country.MakeScope.Var(...)` demande un contexte `Country` absent des descriptions de statut. Les compteurs utilisent désormais `ROOT.GetCountry.MakeScope.Var(...).GetValue|v0`, comme les statuts des journaux du jeu installé. Correction appliquée en français et en anglais, aux compteurs des deux journaux.

Le statut du fardeau administratif distingue explicitement :

- **Bonus actuel pour les conditions remplies** : bureaucratie et réduction du gaspillage calculées depuis le score courant, avec une explication de leur caractère temporaire et variable.
- **Si terminé** : le malus du journal et l’allégement temporaire disparaissent ensemble, puis l’événement **Les comptes de l’Empire** est déclenché. Le retrait technique du bonus est masqué dans les effets détaillés afin de ne plus ressembler à une pénalité ou à une récompense permanente.

Le calcul d’affichage du gaspillage (`score × 10`) est un script value de présentation seulement. Les descriptions narratives et les explications de gameplay précédentes sont conservées ; seuls les ajouts et ajustements nécessaires aux nouvelles règles sont effectués.

## Vérifications réalisées

1. **Historiques** : comparaison de l’intégralité des deux fichiers de bâtiments concernés avec leurs versions antérieures, en autorisant seulement les trois changements de niveaux prévus. Total vérifié : **64 → 54**, trois bâtiments conservés, production et propriété inchangées.
2. **Préservation de l’état de travail** : les empreintes SHA-256 des 16 familles d’historique sont inchangées par rapport au début de ce lot, hors les deux fichiers autorisés. L’empreinte du fichier des modificateurs ottomans est également identique. Cela couvre notamment les populations, les États, les technologies initiales, les armées, les autres bâtiments, les sujets et la diplomatie.
3. **Régressions du lot précédent** : armée ottomane de **72 permanents et 114 conscrits**, armée égyptienne inchangée, 41 blocs de bâtiments égyptiens et leurs technologies de PM, journaux héritables, icônes existantes, privilèges diplomatiques, bloc russe et corrections de l’Homme malade contrôlés statiquement.
4. **Modèle des scripts réels** : 1 024 combinaisons d’entrées des dix objectifs ; les combinaisons « déficit mais pas de pénurie imminente » ne donnent plus de point de réserve. Vérification des seuils 90 % / 75 % / 80 %, de l’absence de doublons de modificateurs, de la migration, de la consolidation et des résolutions indépendantes.
5. **Nouvelles conditions** : cas bureaucratiques négatifs, nuls et positifs ; institutions aux niveaux 2 et 3 ; chacune des technologies absente ; commerce d’esclaves encore actif ; **96 combinaisons** des nouveaux prérequis sur les trois voies politiques. Une technologie manquante interrompt la consolidation sans créer de onzième point de bonus.
6. **Atteignabilité structurelle** : vérification de 17 technologies dans les chaînes utiles, sans prérequis manquant, cycle ou technologie explicitement non recherchable. La police civile professionnelle permet d’augmenter le plafond de police de 3 ; les technologies scolaires pertinentes permettent également d’augmenter le plafond éducatif de 3. Les lois et institutions devront naturellement être mises en place et financées en partie.
7. **Présentation** : références de variables corrigées, calcul du bonus comparé au modificateur inchangé pour les scores 0 à 10, parité des clés FR/EN, UTF-8 avec BOM et existence des icônes. Ces contrôles ne remplacent pas une vérification visuelle en jeu.
8. **Syntaxe et espaces** : validation structurelle des fichiers modifiés et `git diff --check`.

Commande de régression :

```text
python tools/validate_diplomacy_ottoman_1776.py
```

## Validation en jeu encore nécessaire

La dernière version précédente a été testée par l’utilisateur : deux journaux actifs, nouvelles unités présentes et maintien de la Pologne-Lituanie / Crimée dans le bloc russe après un mois. Mesures rapportées : environ **+30,3 K£ par semaine** et **+62 de bureaucratie**.

**Le présent lot n’a pas été lancé en jeu par l’agent.** La cible **+17 K£** est une estimation, pas un résultat mesuré. Retirer des administrations affecte à la fois les salaires, les achats, la capacité fiscale et la bureaucratie ; le résultat net n’est pas garanti.

Pour mesurer la nouvelle version :

1. Relancer le jeu avec ce fork seul et créer une **nouvelle partie au 1er janvier 1776**, pas une ancienne sauvegarde.
2. Vérifier les niveaux 26 / 19 / 9, le budget initial et le solde bureaucratique. Relever aussi les valeurs après la première impulsion hebdomadaire et après un mois, à fiscalité et salaires constants, pour distinguer initialisation et stabilisation.
3. Vérifier que les compteurs numériques s’affichent, que le bonus courant ne figure plus comme une récompense future, et que le critère de réserve est rouge en déficit.
4. Vérifier les nouvelles technologies / loi / institutions dans la liste de complétion, ainsi que la remise à zéro après perte d’une condition.
5. Contrôler les nouveaux logs pour confirmer l’absence des erreurs de contexte de localisation.

Aucun push, merge ou commit automatique effectué. Les autres changements déjà présents dans le répertoire ont été conservés.
