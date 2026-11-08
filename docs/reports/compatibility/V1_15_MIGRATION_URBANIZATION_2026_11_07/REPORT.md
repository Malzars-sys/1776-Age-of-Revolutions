# Migration des journaux de migration et d'urbanisation — 7 novembre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Installé dans le mod local habituel. Contrôles statiques réussis ; aucun lancement du jeu ni validation humaine nouvelle. Aucune écriture Git, modification du vanilla ou réactivation du partage polonais.

Le lot porte sur les journaux de migration et les deux étapes d'urbanisation. Il ne prétend pas terminer l'ensemble de l'issue #27. Les suffragistes, la Grande Crise orientale et les autres chaînes de conclusions restent hors de ce lot.

## Livraison

| Fichier sous `common/journal_entries` | Journal | Conclusions migrées |
| --- | --- | --- |
| `00_urbanization.txt` | `je_urbanization_events_1` | Réussite. |
| `00_urbanization.txt` | `je_urbanization_events_2` | Réussite. |
| `02_south_america_migration.txt` | `je_south_america_migration` | Réussite et invalidation silencieuse. |
| `02_south_america_migration.txt` | `je_central_america_migration` | Réussite et invalidation silencieuse. |
| `02_south_america_migration.txt` | `je_american_west_migration` | Réussite et invalidation silencieuse. |

**Deux fichiers de gameplay, cinq journaux, treize anciens champs remplacés par huit `outcome`.** Les effets de réussite, scopes, conditions d'annulation, fréquences, variables et champs hors conclusions sont conservés. Les anciens gestionnaires d'invalidation absents restent des effets vides ; aucun nouveau nettoyage n'est copié du vanilla.

### Correction de l'urbanisation

Dans les trois blocs `pop_type_percent_country` du premier journal, remplacer les anciens arguments `pop_type = peasants` et `percent` par les arguments 1.15 `target = pop_type:peasants` et `value`.

Les deux conditions d'entrée restent strictement supérieures à 0,6 ; la condition de réussite reste strictement inférieure à 0,35. Dans le second journal, **`percent >= 0.75` est conservé** : il appartient à l'itérateur d'États et ne doit pas être renommé. Les centres urbains de niveaux 5 et 10, les conditions légales et les événements annuels restent inchangés.

La syntaxe est celle du vanilla canonique actuel, `C:/Games/Victoria 3/game/common/journal_entries/00_urbanization.txt:10-52`. Les erreurs répétées de l'ancienne syntaxe avaient été observées dans les logs lors de l'audit précédent. Leur disparition effective après redémarrage reste à mesurer.

### Comportement des migrations conservé

Conserver les conditions de rang, niveau de vie, paix, indépendance, cultures et lois, ainsi que les événements `sa_migration.2` et `.3`, le bouton et l'annulation. Les objectifs sont recalculés aux mêmes endroits et avec les mêmes coefficients.

Point hérité à ne pas confondre avec une régression : les objectifs d'Amérique centrale et de l'Ouest américain commencent à 1 500 000 habitants par État incorporé, puis leur recalcul hebdomadaire emploie 1 000 000. Cette différence préexistante n'a pas été rééquilibrée dans une migration de syntaxe. Les effets `show_as_tooltip` ne deviennent pas des récompenses réelles supplémentaires.

### Contrat 1.15 et textes

Référence : `C:/Games/Victoria 3/game/common/journal_entries/journal_entries.md:134-197`. Réussites avec présentation native positive ; invalidations avec `flags = { hidden invalid_outcome }`. Les en-têtes et descriptions de conclusion emploient les clés natives FR/EN existantes, vérifiées sans surcharge inattendue. Aucun nouveau texte joueur n'est introduit.

Les nettoyages supplémentaires présents dans les exemples vanilla de migration ne sont pas recopiés dans les effets du mod : cela constituerait un changement de comportement distinct, à établir en jeu. Aucune activation, échéance ou dépendance nouvelle n'est ajoutée.

## Contrôles et preuves

Outil en lecture seule : `tools/compatibility/issue27_migration_urbanization_audit.py`. Il réutilise le lecteur et les contrôles du validateur historique, laissé inchangé. Les sauvegardes exactes des deux fichiers avant intervention sont conservées dans `BASELINE/common/journal_entries`.

```text
python -B tools/compatibility/issue27_migration_urbanization_audit.py --mod-root . --baseline-root docs/reports/compatibility/V1_15_MIGRATION_URBANIZATION_2026_11_07/BASELINE --vanilla-root "C:/Games/Victoria 3/game" --self-test
git diff --check -- common/journal_entries/00_urbanization.txt common/journal_entries/02_south_america_migration.txt
```

Exécution avec Python 3.12.14 du runtime installé : **PASS_STATIC_ONLY**, cinq journaux, huit issues, zéro erreur. La comparaison autorise uniquement les trois renommages d'arguments documentés dans le premier journal d'urbanisation ; tous les autres tokens de conditions, effets et champs hors conclusions doivent rester égaux.

Les dix contrôles négatifs détectent un seuil paysan modifié, une cible de population non typée, un pourcentage d'États modifié, un événement de réussite substitué, un poids annuel modifié, un objectif migratoire modifié, un scope pays modifié, la perte du flag d'invalidation, une condition d'annulation modifiée et la réintroduction d'un ancien champ. Ils opèrent en mémoire et ne changent aucun script installé.

**184 fichiers protégés** gardent leurs empreintes : les autres journaux, dont les seize déjà migrés, l'ancien validateur, les groupes illustrés, leur master et leurs DDS. Encodages/BOM et fins de ligne des deux scripts conservés. Le passage de formatage retire seulement dix-huit lignes contenant des espaces ou tabulations nouvellement introduits ; les sources originales n'en avaient aucune. `VALIDATION.json` contient les empreintes et les résultats effectifs.

## Examen du partage de la Pologne

La copie voisine `../1776_Age_of_Revolutions_hotfix_source` s'identifie comme **1776 - Age of Revolutions, Total Conversion Mod, version 2.3.1, jeu 1.13.11**. Son fichier `common/journal_entries/07_poland_lithuania_mod.txt` contient le mécanisme recherché.

La recherche des quatre identifiants dans les scripts de cette copie et du mod actuel ne trouve **aucune définition ni référence active** :

| Identifiant | État dans les versions examinées |
| --- | --- |
| `je_polish_partitions` | Clés de localisation, sans journal distinct. |
| `je_polish_partition_russia` | Clés de localisation, sans journal distinct. |
| `je_polish_partition_prussia` | Clés de localisation, sans journal distinct. |
| `je_polish_partition_austria` | Clés de localisation, sans journal distinct. |

La nuance est donc importante : ce qui a été retiré n'est pas attesté comme quatre journaux autonomes. Le partage fonctionnel était la branche **`timeout = 6000` / `on_timeout` de `je_plc_reform`**.

Le rapport `docs/reports/diplomacy/DIPLOMACY_OTTOMAN_1776_2026-10-09.md:88` documente la raison du retrait : éviter une annexion imposée par la seule expiration du délai, sans négociation ou guerre. Le commit **`4b299b14b1f30c26f51c2c03250c12e503c594d1`**, daté du 10 octobre 2026, supprime cette branche et ajoute un commentaire demandant un futur mécanisme conditionnel. Le corps de l'ancien effet retrouvé dans la copie source est identique, comme suite de tokens, à celui du parent de ce commit.

Les douze opérations de transfert prescrites par cet ancien script sont :

| Destinataire | Régions d'État nommées dans le code retiré |
| --- | --- |
| RUS | MINSK, KAUNAS, VILNIUS, BREST, VOLHYNIA, KIEV, COURLAND |
| PRU | POSEN, MAZOVIA, WEST_PRUSSIA |
| AUS | LESSER_POLAND, GREATER_POLAND |

Ce tableau décrit le code, sans valider historiquement ces périmètres. Les transferts effectifs dépendaient des États trouvés et des conditions de propriété. Il n'y avait pas de procédure d'accord ou de paix dans cette branche.

Le journal de réforme actuel conserve ses objectifs, récompenses et journaux de modernisation, sans échéance ni transfert forcé. Il est resté **strictement inchangé** pendant cette mission. L'ancien effet est archivé sous `RETIRED_POLISH_PARTITION_EFFECT.txt`, uniquement dans ce dossier documentaire inactif. Les sources, empreintes et contrôles figurent dans `POLISH_PARTITIONS_EVIDENCE.json`.

Le plan antérieur prévoyait une crise diplomatique conditionnelle, des initiatives séparées des voisins, des choix polonais et des transferts seulement après accord ou paix. Cela reste un chantier de conception à valider séparément. Les quatre titres ne sont pas réactivés ni transformés artificiellement en nouveaux journaux.

## Validation en jeu restante

1. Redémarrer complètement le jeu et utiliser une nouvelle partie en 1776. Vérifier que les anciennes erreurs `pop_type_percent_country` de l'urbanisation ne reviennent pas dans les nouveaux logs.
2. Vérifier les deux entrées d'urbanisation : conditions initiales, seuils stricts de 60 % et 35 %, proportion de 75 % des États, niveaux 5/10 et événement de conclusion appliqué une seule fois.
3. Sur un pays éligible, activer chaque journal de migration, laisser recalculer l'objectif, tester réussite et annulation ; pour l'Ouest américain, tester aussi la perte des États requis. Vérifier arrêt des pulses et comportement des modificateurs, y compris en cas de conditions simultanées.
4. Sauvegarder/recharger avant et après conclusion et comparer les logs tournants. Ne pas confondre les autres erreurs de scopes ou les autres chaînes encore héritées avec ce lot.
5. Pour la Pologne, vérifier le maintien des réformes sans réapparition du compte à rebours d'annexion. Aucun nouveau partage ne doit être ajouté par ce correctif.

Ces tests et leur acceptation humaine restent à faire. Le passage immersif des textes suit la validation du fonctionnement ; ce lot conserve la prose existante et ne certifie pas sa finition éditoriale globale.

## Retour joueur et logs après redémarrage

Le joueur confirme un redémarrage et une sauvegarde/rechargement. Dans l’instantané des six logs conservés du 7 novembre, aucune erreur ne désigne les deux fichiers de ce lot ; l’urbanisation est observée en Potentiel et aucun parcours de réussite des migrations n’a été exercé. Cela constitue une observation partielle, pas une validation complète. Les conditions d’éligibilité et les corrections suivantes, notamment la fenêtre polonaise et le titre canadien, sont documentées dans [le retour runtime](../V1_15_RUNTIME_FEEDBACK_2026_11_07/REPORT.md).
