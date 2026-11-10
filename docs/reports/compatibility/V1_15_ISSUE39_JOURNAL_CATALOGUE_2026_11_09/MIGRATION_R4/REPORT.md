# #39 — Migration des conclusions, livraison locale du 9 novembre 2026

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Les corrections ci-dessous sont installées dans le mod courant. La mission reste ouverte : aucun essai moteur, rendu GUI, test DLC ou reçu humain supplémentaire n'est acquis. Le catalogue initial reste conservé au niveau parent ; ses chiffres décrivent l'état avant migration.

Référence consultée en lecture seule : `C:/Games/Victoria 3/game`, exécutable **1.15.0**. HEAD au départ : `0396b1133168c1721b61cee5ae5334f1a4f5e4e1`. Aucune opération Git d'écriture. Le candidat d'intégration préparé sous #25 et ses rapports ne sont pas modifiés par cette livraison locale.

## Installation

- **400 journaux**, dans **166 fichiers**, passent des anciens champs de conclusion à **856 outcomes** explicites. Les **1 381** champs de conclusion directs recensés au départ ont disparu du catalogue effectif.
- Les en-têtes personnalisés et les aperçus d'événements/effets sont transférés dans leurs outcomes respectifs : 16 en-têtes de réussite, 12 en-têtes d'effet de réussite, 12 en-têtes d'échec, 11 en-têtes d'effet d'échec ; 55 descriptions de réussite et 43 aperçus d'effets de réussite, 26 descriptions d'échec et 14 aperçus d'effets d'échec, 9 descriptions d'expiration et 3 aperçus d'effets d'expiration. Leurs contenus et leurs scopes sont conservés.
- Trois objets natifs masqués sont rétablis dans `common/journal_entries/zz_1776_v115_restored_journals.txt` : `je_five_year_plan`, `je_meiji_imperial_marriage`, `je_state_and_revolution`. Leurs corps sont identiques au vanilla courant. Aucun `is_shown_when_inactive` ni ajout d'historique n'est introduit : ils conservent leur activation par effet. L'ancien `je_5_year_plan` et les choix communistes du mod restent distincts.
- `events/zz_1776_v115_five_year_plan.txt` restaure exactement les événements natifs `communism.13` (continuation du plan) et `communism.12` (chiffres falsifiés, demandé par un bouton natif du plan). Aucun événement local existant n'est écrasé.
- Seize anciens identifiants reçoivent leur nom et leur raison manquants dans **les deux langues**, soit **32 clés FR et 32 clés EN**, dans deux fichiers propres au correctif. Les anciens fichiers de localisation sont préservés. La vérification du rendu reste à faire ; les autres proses et barres ne sont pas déclarées éditorialement validées.
- Quatre références à des boutons inexistants, Niger/Éthiopie et leurs variantes d'expansion, sont retirées de l'ancien hub `je_colonial_administration`. Ces noms ne se résolvent ni dans le mod ni dans le catalogue natif courant. Les huit autres boutons et tous les autres champs sont conservés ; aucune nouvelle action coloniale ou modification géographique n'est créée.

Au total : **167 fichiers de jeu existants modifiés et 4 nouveaux fichiers**, soit 171 fichiers livrés. Le premier montage a été installé en **neuf lots de vingt fichiers au maximum**, chacun contrôlé indépendamment. Les corrections ultérieures de présentation sont tracées séparément ; les révisions R1/R2/R3 restent conservées.

## Correspondance technique et cas particuliers

[MANIFEST.json](MANIFEST.json) contient pour chaque entrée ses prédicats, handlers, délais, champs de présentation, ordre et empreintes. Le générateur utilise les champs directs du parseur et les ancrages de ce manifeste, pas une substitution regex globale. Les conditions imbriquées et les corps d'effet sont comparés comme séquences de jetons, y compris `ROOT`, `scope:journal_entry`, les paramètres, variables et événements retardés.

| Ancien champ | Destination |
| --- | --- |
| `complete`, `fail`, `invalid` | `outcome.trigger`, dans l'ordre de déclaration des prédicats |
| `on_complete`, `on_fail`, `on_invalid`, `on_timeout` | `outcome.effect` associé |
| `on_*_all_involved` | `outcome.effect_all_involved`, en contexte sans pays racine |
| `timeout` | champ de durée inchangé ; outcome `flags = { timeout }`, sans déclencheur |
| `custom_*_header` | `header` / `effect_header` de l'issue correspondante |
| `event_outcome_*_desc`, `event_outcome_*_effect_desc` | `event_outcome_desc` / `event_outcome_effect_desc` correspondants |

Les sept délais calculés des pétitions/négociations sont identiques à leurs expressions natives correspondantes et restent des expressions ; aucune durée fixe ne leur est substituée. Une durée sans handler garde une expiration à effet vide, comme les exemples natifs d'Alaska et de reconstruction américaine.

Six issues sont explicitement dormantes, sans création d'un objectif nouveau : expiration sans durée dans `je_scramble_for_africa` et `je_the_paris_commune_display`, handler d'échec sans prédicat dans les deux tutoriels d'expansion et `je_spa_economic_regeneration_master`, ancien en-tête d'échec inutilisé dans `je_tenpo_crisis`. Elles restent cachées et ne reçoivent ni condition de réussite inventée ni échéance ajoutée. Les handlers présents restent conservés. Leur comportement sous suppression forcée ou commande externe relève du test moteur, pas d'une preuve statique.

Les issues d'invalidation sont cachées et portent `invalid_outcome`. Les priorités de prédicats concurrents sont préservées dans les déclarations ; l'ordre d'évaluation effectif du moteur lorsque plusieurs deviennent vrais simultanément reste à tester.

L'audit compare les champs non déplacés dans leur ordre original : activation, visibilité inactive, pulses, boutons, barres, progression, variables, widgets, transfert et héritage. Un contrôle inverse rétablit exactement les octets originaux hors des spans autorisés. Les espaces des blocs relocalisés ont été nettoyés sans changer leurs jetons.

## Catalogue final et limites de contenu

**493 identifiants effectifs**, sans fournisseur ambigu ni erreur de lecture : 490 disposent d'outcomes, trois ne possèdent pas de conclusion authored. Aucun champ legacy direct ni métadonnée minimale d'outcome manquante n'est trouvé.

Les trois exceptions sont recensées individuellement, sans conclusion artificielle : `je_colonial_administration` (hub de boutons), `je_new_imperialism` (suivi conservé sans conclusion authored), `je_spain_glorious_revolution_dummy` (dummy espagnol conservé). Cette conservation ne vaut pas une nouvelle validation humaine de leur conception. Les chaînes espagnoles désactivées et les partitions polonaises supprimées ne sont pas réactivées.

Cinq nouveaux identifiants natifs restent masqués par les anciennes familles du mod : `je_australia`, `je_canada`, `je_extraordinary_commission`, `je_paris_commune`, `je_social_revolution`. Les familles existantes australiennes/canadiennes, communistes et de la Commune sont conservées et leurs conclusions sont migrées. Réintroduire en parallèle les familles natives complètes demanderait une décision de contenu et une revue de leurs consommateurs, sous le volet DLC de #24 ; ce n'est pas une autorisation de remplacer les branches authored ou de modifier les lois du chantier #17.

La définition native d'« État et Révolution » est de nouveau résoluble pour le journal bolchevik hérité. **Aucune nouvelle transition vers cette famille n'est câblée dans les anciens choix de `communism.2`.** Il faut distinguer cette réparation de référence et la migration des journaux existants d'un portage fonctionnel complet de toutes les nouvelles chaînes DLC. Cette limite reste ouverte sous #24/#39 et ne doit pas être présentée comme une parité DLC acquise.

## Contrôles réellement exécutés

| Vérification sur la version livrée | Résultat |
| --- | --- |
| Mapping, prédicats, effets, scopes conservés, présentation, délais, ordre et réversibilité des 400 entrées | **11 117/11 117**, statique seulement |
| Régressions volontaires : prédicat, récompense, all-involved, invalidation visible, délai, handler dormant, en-tête, aperçu d'événement, champ legacy, réactivation d'une chaîne, progression, mauvais scope, syntaxe | **14/14 détectées par le contrôle attendu** |
| Objets restaurés comparés exactement au natif, lois/modificateurs/helpers natifs référencés, textes, boutons et reproduction depuis les captures | **65/65** |
| Liens littéraux directs du catalogue : groupes, boutons, barres, événements, journaux et textes d'outcomes | **493 entrées, zéro constat** dans ce périmètre |
| Témoins des conclusions #27 déjà acceptées | **8 fichiers inchangés**, empreintes identiques |
| Inventaire final et cas de contrôle du classificateur | zéro ancien champ, zéro fournisseur ambigu, **6/6 cas réussis** |

Les 491 liaisons vers des boutons ont fait l'objet d'un contrôle supplémentaire des événements et ajouts de journal littéraux. Ce contrôle a identifié le besoin de restaurer `communism.12`. Aucun nouveau constat n'est laissé sur ces liaisons dans la version finale. Les ajouts paramétrés restent distingués des identifiants littéraux ; le scan global recense 527 ajouts et ne signale plus de cible littérale manquante.

La référence native de contrôle compte 449 entrées et n'a aucun constat dans le même audit direct. Ce résultat et le zéro de l'audit moddé ne certifient pas les types de scopes à l'exécution, l'initialisation de toutes les variables, les branches DLC-on/off, la simulation ou le rendu GUI.

L'audit #21 brut passe de 484/485 avant cette passe à 480/485 : quatre de ses anciennes empreintes de fichier complet couvrent des journaux maintenant migrés. En rétablissant **uniquement ces changements de #39 en mémoire**, il revient à **484/485**, avec exactement son ancien écart pour `events/technology_events.txt` issu de la livraison #22. Aucun outil ni contrat #21 n'est modifié ou affaibli. Les résultats bruts restent conservés.

`git diff --check` reste non nul : 87 diagnostics sont rapprochés de 85 lignes des anciennes sources et de deux préfixes d'indentation exactement conservés devant un nouveau mot-clé. Les résultats bruts et cette attribution sont conservés dans [WHITESPACE_CLASSIFICATION.json](WHITESPACE_CLASSIFICATION.json). Ils ne sont pas présentés comme un contrôle de formatage vert. Les premières révisions ayant créé des lignes vides indentées sont conservées ; cette introduction a été corrigée dans la version finale.

## Préservation et reproduction

Les 2 484 sources du workspace prises avant installation servent de garde. Les évolutions concurrentes hors des 167 fichiers existants autorisés sont enregistrées et laissées intactes, notamment `map_data/state_regions/12_indonesia.txt`. Les fichiers du vanilla, l'index Git et HEAD sont préservés. Les fichiers de carte, populations, lois, technologies, PM, navires, prêts américains et les suivis #21/#25/#27 ne sont pas réécrits par ce chantier.

Commandes principales :

```text
python -B tools/compatibility/issue39_outcome_migration.py --live --negative-controls --directory docs/reports/compatibility/V1_15_ISSUE39_JOURNAL_CATALOGUE_2026_11_09/MIGRATION_R4
python -B tools/compatibility/issue39_dependency_audit.py --output …/DEPENDENCIES_FINAL.json
python -B tools/compatibility/issue39_journal_catalogue.py --self-test --output …/INVENTORY_FINAL.json
```

La reproduction a aussi été exécutée depuis `MIGRATION_R4/before` avec `--prepare --source-root` dans `REPRO_CHECK` : les 166 fichiers générés ont exactement les mêmes empreintes que le candidat final de mapping. Les auxiliaires sont vérifiés séparément contre leurs objets natifs et leur reçu. `INSTALLATION.json` identifie les 171 fichiers installés ; les anciens candidats ne doivent pas remplacer ce reçu final.

## Review restante

Le [protocole moteur groupé](RUNTIME_PROTOCOL.md) accompagne cette livraison. Les cases de simulation, rendu, comparaison de nouveaux logs et acceptation humaine restent ouvertes. Les futurs tests doivent identifier cette version locale ; elle n'est pas assimilée au candidat de branche préparé par #25 et n'est ni commitée, ni poussée, ni fusionnée.

Sources techniques : contrat canonique `common/journal_entries/journal_entries.md`, exemples `00_urbanization.txt`, `00_acw_entries.txt`, `00_alaska.txt`, `01_ryukyu_rivalry.txt`, `99_test_global_je.txt` ; objets natifs `00_communism.txt`, `00_meiji_restoration.txt`, `events/communism.txt` et leurs auxiliaires hérités. Aucun nouveau fait historique n'est utilisé pour modifier le scénario.
