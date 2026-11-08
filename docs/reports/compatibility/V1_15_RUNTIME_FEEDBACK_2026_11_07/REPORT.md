# Retour joueur après redémarrage — 7 novembre 2026

Statut des nouveaux correctifs : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Ils sont installés dans le mod local. La session examinée précède leur installation ; un nouveau redémarrage est nécessaire pour les charger. Aucun arrêt du jeu, modification de sauvegarde, lancement automatique ou écriture Git n'a été effectué.

## Observations et limites du test joueur

Source : message du joueur dans cette conversation, avec deux captures jointes. Le joueur rapporte avoir redémarré, puis « fait sauvegarder et recharger ». Il observe une entrée d'urbanisation en Potentiel, aucune migration activable trouvée, le titre brut `je_canada_gbr`, l'absence des chaînes espagnoles dans le groupe et une entrée polonaise sans conditions de conclusion.

La capture polonaise montre le titre, la raison et une barre de progression à 23,5 % ; aucune conclusion n'est affichée. La capture britannique montre les bandeaux et noms des groupes État et révolution et Destin des Amériques, ainsi que le titre canadien brut. Cela atteste ces affichages dans cette session, sans valider toutes les issues, récompenses ou images du mod.

Le signalement de sauvegarde/rechargement est enregistré comme action effectuée. Aucune réussite, invalidation, application unique de récompense ou absence totale d'erreurs n'en est déduite. Aucun lot n'est déclaré entièrement accepté en jeu.

## Logs effectivement examinés

`code_revisions.log` indique une session commencée à **20 h 32 le 7 novembre, heure de Paris**, sur `release/1.15.0`, révision `6338547985dbc271523e149f362a6fd93dc62975`.

Les six fichiers `error.log` et `error.1.log` à `error.5.log` ont été figés en copie privée avant rotation. L'instantané contient des messages de 20 h 32 min 35 s à 21 h 22 min 23 s. `LOG_REVIEW.json` conserve leurs empreintes, plages et extraits ciblés ; les logs complets restent hors du dépôt.

| Périmètre | Résultat dans cet instantané |
| --- | --- |
| `00_urbanization.txt` | Aucune occurrence d'erreur retrouvée. |
| `02_south_america_migration.txt` | Aucune occurrence d'erreur retrouvée. |
| `07_poland_lithuania_mod.txt` | Seize messages de lecture concernant les anciens champs de conclusion. |
| `00_canada_australia.txt` | Dix messages de lecture concernant les anciens champs de conclusion, dont les définitions australiennes non modifiées ici. |
| `07_american_mod_jes.txt` | Six messages de lecture concernant les anciens champs de conclusion ; seule la Frontière du Nord-Ouest est reprise ici. |
| `06_spanish_new_world.txt` | Dix-neuf messages ciblés ; cette chaîne reste désactivée et hors du correctif. |
| `06_cuba.txt` | Vingt-cinq messages ciblés ; hors de ce correctif. |

Les 499 erreurs `pop_type_percent_country` encore présentes dans l'instantané désignent les mouvements politiques (`00_ideological_movements.txt:527` et `:6289`), pas l'urbanisation corrigée. D'autres dettes persistent : régions d'administration coloniale, stratégie IA, variable ottomane non initialisée, cultures et religions. Aucune correction globale ni disparition de ces erreurs n'est revendiquée.

L'absence d'une erreur dans les logs conservés n'est pas une preuve de réussite d'un journal. Le début exact du chargement peut être incomplet dans des logs tournants.

## Correctifs installés

### Réformes polonaises : restaurer les conclusions

Le moteur rejette `complete` et `on_complete`, ce qui correspond à la fenêtre vide signalée. Les **huit définitions** du fichier `07_poland_lithuania_mod.txt` sont migrées : réforme principale, industrie, commerce, éducation, chemins de fer, agriculture, armée et grande puissance.

Chaque prédicat et effet est conservé comme suite de tokens, avec son ordre et ses scopes. La réforme principale garde notamment : alphabétisation strictement supérieure à 20 %, niveau de vie strictement supérieur à 8, objectif de PIB de 9 millions, petite bourgeoisie et intelligentsia non marginales. Les récompenses, changements idéologiques et ajouts des réformes suivantes restent inchangés.

Le compte à rebours de partage de 6 000 jours n'est pas réintroduit. Aucun `timeout`, `on_timeout` ou transfert territorial n'est ajouté aux réformes. La décision de retrait documentée dans le lot précédent reste respectée.

### Canada : traductions et conclusions

La 1.15 a fusionné les anciens journaux canadien et métropolitain en une entrée globale `je_canada`. Le mod conserve ses deux perspectives de pays ; les anciennes clés de titre et de raison ne sont plus fournies par le vanilla. Cette divergence explique `je_canada_gbr` dans la capture.

Deux fichiers de localisation dédiés, avec BOM et en-tête de langue corrects, ajoutent chacun quatre alias : titres et raisons de `je_canada_can` et `je_canada_gbr`, vers les textes natifs `je_canada` et `je_canada_reason`. Le titre français devient **Confédérer le Canada**. Les cibles natives sont présentes dans les fichiers effectivement hérités ; les nouvelles clés sont uniques.

Les deux définitions canadiennes sont aussi migrées vers `outcome`, avec conservation de l'invalidation silencieuse du journal colonial. Le nationalisme, les neuf régions requises parmi onze, le bouton, les événements et leurs effets sont conservés. Le bouton natif vérifié opère avec le pays courant ; aucune nouvelle entrée globale n'est importée dans ce lot.

Les deux journaux australiens présents dans ce fichier partagé restent exactement inchangés et conservent leur dette de migration séparée.

### Frontière du Nord-Ouest : clarification et migration bornée

La Frontière du Nord-Ouest (`je_northwest_frontier_mod`) concerne **Ohio, Wisconsin, Indiana, Michigan et Illinois**. Son activation exige les États-Unis indépendants et un État dans la région d'Ohio, directement ou via un sujet. Ce n'est pas le journal de peuplement de l'Ouest américain ni l'ensemble des conquêtes mexicaines.

Ses anciennes conclusions sont également migrées : réussite avec le bonus d'origine, et expiration native avec **2 300 jours**, sans effet ajouté. L'événement immédiat, les États requis, l'héritage/transfert et le groupe sont conservés. Le délai reste un champ du journal et l'issue d'expiration n'a pas de trigger, conformément au contrat 1.15.

Les ventes et achats de Floride du même fichier restent strictement inchangés. Le joueur n'a pas à terminer une campagne ou la guerre d'indépendance pour que l'audit statique puisse vérifier ces conditions ; leur exécution en jeu demeure un test distinct.

## Pourquoi les autres entrées ne s'activent pas au lancement

### Urbanisation

Deux définitions existent, avec des conditions différentes :

| Journal | Visibilité / activation | Réussite |
| --- | --- | --- |
| Des fermes aux usines | Plus de 60 % de paysans pour être proposé ; sortie du servage et de l'impôt foncier pour s'activer. | Moins de 35 % de paysans, maintien des conditions légales, industrialistes non marginaux. |
| Urbaniser la nation | Centre urbain dans un État incorporé pour être proposé ; centre de niveau 5 et absence d'agrarianisme pour s'activer. | Centres de niveau 5 dans au moins 75 % des États incorporés, et au moins un centre incorporé de niveau 10. |

Une ligne verrouillée dans Potentiel présente d'abord ses conditions d'activation. Le nombre d'entrées visibles dépend du pays ; les conditions de réussite ne sont pas testées par cette seule observation. Les lois, bâtiments et seuils n'ont pas été abaissés pour forcer un test en 1776.

### Migrations

Les trois entrées migrées sont des programmes de peuplement, et non des journaux de conquête. Elles demandent toutes `civilizing_mission`, qui existe dans l'arbre du mod en **ère 8**, au sein du fichier de compatibilité post-1836. Elles demandent également le rang de puissance mineure ou supérieur, un niveau de vie d'au moins 10, la paix, l'indépendance et des lois acceptant le programme.

L'Ouest américain demande en plus au moins trois États incorporés dans les régions des Grandes Plaines ou de la côte pacifique. Ces prérequis expliquent l'impossibilité pratique d'en faire un test de démarrage en 1776. Aucune technologie n'a été distribuée aux pays pour rendre ce test possible. Les prérequis sont documentés, pas modifiés.

### Espagne et colonies

Les fichiers existent, mais leur regroupement ne constitue pas une chaîne coloniale 1776 activée :

- `je_spanish_new_world_dummy` vise `c:SPC` (Espagne carliste), exige le contenu `ip4` et a `always = no` dans `possible` ; il ne s'active donc pas pour l'Espagne `SPA`.
- `je_reconquista` et `je_hispanoamerica` sont ajoutés par des options d'événement, sans visibilité inactive autonome ; leurs invalidations contiennent une condition de sujet de la Bolivie et la variable `why_is_this_on`.
- `je_spanish_american_independence` n'a pas de conditions de visibilité inactive et conserve une invalidation liée au statut de sujet de la Bolivie.
- L'événement d'ouverture conserve un commentaire `turn off`, une annulation liée au journal des Boxers et des options conditionnées à `dummy_var_mod`.

Ces blocages sont effectivement présents dans les scripts hérités. Le motif historique précis de chacun n'est pas établi ici. Les retirer ou remplacer `SPC` par `SPA` sans reconstruire la chaîne pourrait activer du contenu incomplet ou produire des issues immédiates. Aucun changement de visibilité, d'indépendance coloniale ou d'événement espagnol n'a été improvisé. Une chaîne de crises et révoltes adaptée à 1776 reste à concevoir et migrer séparément.

## Validation des changements

Outil en lecture seule : `tools/compatibility/issue27_runtime_feedback_audit.py`. Sauvegardes immédiates des trois scripts dans `BASELINE/common/journal_entries`.

```text
python -B tools/compatibility/issue27_runtime_feedback_audit.py --mod-root . --baseline-root docs/reports/compatibility/V1_15_RUNTIME_FEEDBACK_2026_11_07/BASELINE --vanilla-root "C:/Games/Victoria 3/game" --self-test
git diff --check -- common/journal_entries/00_canada_australia.txt common/journal_entries/07_poland_lithuania_mod.txt common/journal_entries/07_american_mod_jes.txt
```

Résultat effectif : **trois fichiers de gameplay, onze journaux, vingt-trois champs hérités remplacés par treize issues, zéro erreur statique**. Onze contrôles négatifs détectent les changements de seuils, PIB, cleanup idéologique, continuation, scopes et compte canadien, invalidation visible, délai/flag d'expiration, restauration du délai polonais et réintroduction d'une ancienne conclusion.

Les quatre définitions non ciblées dans les fichiers partagés sont inchangées, corps de définition compris. **523 fichiers protégés** gardent leurs empreintes : autres journaux, localisations antérieures, groupes et illustrations, dont les cinq journaux migrés au lot précédent. Les deux nouveaux fichiers FR/EN fournissent quatre clés uniques par langue. `git diff --check` passe. Une première proposition a été rejetée avant écriture des scripts parce qu'elle normalisait les fins de ligne mixtes d'un fichier partagé ; la proposition installée conserve les blocs non ciblés exactement.

Le nouvel inventaire contient **1 389 champs hérités dans 167 fichiers, concernant 402 identifiants de journal**. Il inclut du contenu conditionnel ou hérité ; ce n'est pas un nombre de bugs ni un pourcentage de compatibilité. `VALIDATION.json` conserve résultats, empreintes et observations partielles du joueur.

Les sources canoniques consultées sont le contrat des journaux 1.15, l'urbanisation, les journaux canadiens et leur bouton, ainsi que les localisations natives FR/EN. Les choix de scénario et les désactivations antérieures sont conservés.

## Prochain contrôle borné

Après redémarrage complet, rouvrir une partie polonaise pour vérifier l'apparition des conditions et effets, puis le titre canadien en vue britannique. Une nouvelle partie est préférable pour certifier l'initialisation ; la compatibilité de l'instance déjà sauvegardée n'est pas garantie par ce contrôle de scripts. La réussite des réformes, leurs récompenses et continuations, l'expiration de la Frontière du Nord-Ouest et les migrations tardives restent à tester sur des situations appropriées. Aucun succès complet n'est demandé au joueur avant de pouvoir poursuivre les corrections.

La réécriture immersive après validation humaine des mécanismes n'est pas déclenchée par une simple observation des fenêtres. Les textes polonais existants sont préservés ; seuls les alias canadiens nécessaires à l'affichage sont ajoutés.
