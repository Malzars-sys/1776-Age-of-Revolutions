# #39 — Prise en charge et inventaire initial

**Mise à jour du 9 novembre 2026 :** cet inventaire décrit la situation avant correction. La migration locale est désormais installée ; voir [la livraison MIGRATION_R4](MIGRATION_R4/REPORT.md) et son reçu. Les 400 anciens contrats décrits ici ne sont plus présents dans le catalogue courant. Ce rapport initial est conservé sans réécrire ses résultats historiques.

9 novembre 2026, Hawk. **In progress — INVENTORY_ONLY_NOT_FULL_SEMANTIC_REVIEW.** La mission n'est ni terminée ni prête à être acceptée dans le moteur. Cette première passe termine la prise en charge et l'inventaire structurel, sans migration de fichiers de jeu.

La mission a été sélectionnée dans le Backlog réel du Project #1 après la livraison de #22 en In review. Son périmètre est le catalogue complet des journaux. L'ordre de travail de la fiche #39 réserve la priorité à la préparation d'intégration de #25 : aucun remplacement massif de journaux n'est lancé en parallèle dans cette passe. #21, #27 accepté, #38, la carte, les lois, les technologies et l'économie sont préservés.

## Résultats calculés sur le workspace courant

| Objet compté | Résultat |
| --- | ---: |
| Fichiers natifs de journaux | 183 |
| Fichiers locaux de journaux | 180 |
| Fichiers effectifs après les masques de chemin | 201 |
| Chemins natifs masqués par un fichier local homonyme | 162 |
| Directive de remplacement explicite | 1 |
| Identifiants effectifs distincts | **490** |
| Fournisseurs ambigus dans ce modèle | 0 |
| Entrées avec anciens champs de conclusion directs | **400** |
| Champs de conclusion hérités dans ces entrées | **1 381** |
| Entrées possédant des outcomes, sans anomalie dans les métadonnées minimales inspectées | 87 |
| Entrées sans outcome et sans ancien champ de conclusion | 3 |
| Ajouts `add_journal_entry` repérés dans les scripts effectifs common/events | 526 |
| Cibles littérales d'ajout non définies | 2 |

Les 400 entrées sont réparties dans 166 fichiers. Il s'agit d'un inventaire de contrats anciens, pas de 400 pannes observées dans une partie. L'absence d'anomalie dans les métadonnées inspectées des 87 autres entrées ne certifie ni leurs scopes, ni leurs dépendances, ni leur fonctionnement moteur. Aucune activation au 1er janvier 1776 n'est déduite d'une simple définition.

Les copies natives masquées, leurs identifiants et les fournisseurs effectifs sont conservés dans [INVENTORY.json](INVENTORY.json). Le tableau [CATALOGUE.csv](CATALOGUE.csv) contient les 490 identifiants, leur source, ligne, classification, anciens champs et nombre d'ajouts référents. Le modèle tient compte du `REPLACE_OR_CREATE` local ; aucun `INJECT` non résolu n'est présent ici. Les seuls `replace_path` du descripteur portent sur les technologies, pas sur les journaux.

## Dépendances à examiner avant les migrations

Huit identifiants natifs sont absents du catalogue effectif : `je_australia`, `je_canada`, `je_extraordinary_commission`, `je_five_year_plan`, `je_meiji_imperial_marriage`, `je_paris_commune`, `je_social_revolution`, `je_state_and_revolution`. Une absence n'autorise pas leur rétablissement automatique : les nouvelles chaînes natives peuvent remplacer des chemins plus anciens du mod ou dépendre de suppressions historiques volontaires.

Deux ajouts littéraux sont toutefois privés de définition :

- `je_five_year_plan`, demandé par le bouton natif hérité `common/scripted_buttons/00_ip5_04_buttons.txt`, ligne 53 ; le mod possède encore `je_5_year_plan` dans son ancien ensemble communiste. Un alias mécanique risquerait de déclencher deux chaînes ou de changer les conditions, et n'est pas installé.
- `je_meiji_imperial_marriage`, demandé dans le fichier local `events/japan_events/ep2_meiji_restoration.txt`, ligne 320. Examiner le contrat, les gardes DLC et les consommateurs avant de proposer la définition appropriée.

Le troisième nom non résolu de la recherche brute, `$JE$`, est un paramètre de l'effet scripté natif à la ligne 1198 de `common/scripted_effects/00_scripted_effects.txt` ; il n'est pas compté comme un identifiant littéral manquant. Les branches recensées ne sont pas nécessairement exécutables : [ADD_JOURNAL_CONSUMERS.json](ADD_JOURNAL_CONSUMERS.json) garde leurs fichiers et lignes, sans attester leur exécution.

Seize entrées n'ont pas leur clé de titre dans l'union des localisations anglaises/françaises consultées. Le détail par entrée figure dans l'inventaire, notamment les anciens noms communistes, les anciennes variantes canadiennes/australiennes et les branches de la Commune. Cette recherche d'absence ne simule pas l'ordre des doublons de localisation et ne certifie pas l'affichage de tous les textes dynamiques. Elle ne transforme pas une entrée volontairement désactivée en défaut joueur confirmé.

Les trois entrées sans outcome sont `je_colonial_administration`, `je_new_imperialism` et `je_spain_glorious_revolution_dummy`. Elles sont explicitement laissées à l'examen manuel ; aucune conclusion artificielle ne leur est ajoutée. Les six entrées présentant des gardes constantes sont également signalées sans confondre `is_shown_when_inactive = no` avec l'impossibilité d'un ajout par effet.

## Méthode, vérifications et limites

Outil : `tools/compatibility/issue39_journal_catalogue.py`, en lecture seule pour le jeu et le mod. Commande exécutée :

```text
python -B tools/compatibility/issue39_journal_catalogue.py --self-test --output docs/reports/compatibility/V1_15_ISSUE39_JOURNAL_CATALOGUE_2026_11_09/INVENTORY.json
```

Le parseur lit les champs directs en respectant accolades, chaînes et commentaires ; il ne recherche pas simplement des mots à n'importe quelle profondeur. Chaque fichier et chaque corps de définition reçoit une empreinte. Les résultats distinguent les anciens champs, les outcomes et les entrées sans conclusion. Les outcomes visibles doivent notamment fournir leurs deux en-têtes, une description de conclusion et un déclencheur hors timeout ; l'invalidation doit être cachée.

Résultats exécutés : aucune erreur de lecture des journaux ou des scripts d'ajout inspectés, aucun fournisseur effectif ambigu, **6/6 cas de contrôle réussis**. Ces cas vérifient notamment les commentaires, l'ancien contrat, les en-têtes manquants, l'invalidation cachée et le timeout avec déclencheur. Ce ne sont pas des tests du moteur Paradox.

Référence normative : `C:/Games/Victoria 3/game/common/journal_entries/journal_entries.md`, particulièrement la section outcomes ; exemples natifs `00_urbanization.txt`, `00_communism.txt`, `01_ryukyu_rivalry.txt`, `05_grunderzeit.txt` et `99_test_global_je.txt`. Les explications d'activation, les gardes DLC, les champs all-involved, les en-têtes personnalisés et les descriptions d'événements nécessitent leur propre correspondance ; une conversion générale des seuls mots `complete` et `fail` serait insuffisante.

La revue sémantique de chaque entrée, la fermeture des dépendances (boutons, événements, barres, effets et conditions), la migration, les essais d'issues concurrentes, les tests DLC activé/désactivé, l'analyse de nouveaux logs et les essais de sauvegarde/rechargement restent à faire. Aucune case d'acceptation exhaustive de #39 n'est cochée à partir de cet inventaire. La réception de #27 conserve son périmètre accepté.

## Prochaine action

Après coordination avec la préparation d'intégration #25, établir le mapping de la famille communiste et de ses consommateurs : ancien `fail` de `je_communism_1`, anciens titres et distinction `je_5_year_plan` / `je_five_year_plan`. Préparer ensuite des lots indépendants pour les entrées propres à 1776, les tutoriels/objectifs et les entrées contextless/all-involved. Pour chaque entrée : préserver les prédicats, l'ordre des conclusions, les scopes, les effets, les délais et le nettoyage ; documenter individuellement les exceptions permanentes ou désactivées.

Le travail technique et sa validation restent distincts de la réécriture immersive, qui interviendra après l'acceptation humaine du fonctionnement. Aucun contenu historique désactivé n'est réactivé pour faire disparaître un avertissement.
