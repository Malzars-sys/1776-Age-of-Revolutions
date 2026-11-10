# Mission 25 — contextes de l'IA, lot du 9 novembre 2026

Hawk — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** pour ce lot. La mission 25 reste ouverte pour les validations intégrées de sortie ; aucune publication ou acceptation moteur n'est acquise ici.

Référence : exécutable canonique **1.15.0**, HEAD local `0396b1133168c1721b61cee5ae5334f1a4f5e4e1`. Le workspace contient les modifications locales des autres chantiers : le HEAD seul ne représente pas le candidat à tester.

## Résultat installé

### Règle de rapprochement diplomatique

Dans `common/ai_strategies/00_default_strategy.txt`, l'ancien contrôle de présence russe en Asie du Nord-Est utilisait `building_naval_base` au niveau 15. Cet identifiant n'a plus de fournisseur. La branche native homologue utilise `building_naval_administration` au niveau 3, dont le mod possède déjà la définition.

Ces **deux valeurs seulement** sont remplacées. La branche entière de rapprochement, après correction, est équivalente à la branche native actuelle. Tous les autres octets du fichier, ses conditions géographiques, les autres scores et les corrections précédentes restent identiques. Ce changement ne construit aucun bâtiment et ne modifie pas sa recette ou son niveau de départ.

Source native : `C:/Games/Victoria 3/game/common/ai_strategies/00_default_strategy.txt:7380`. Source du mod avant correction : ligne 5132. Empreintes et positions exactes : `CONTRACT.json`, copies `before/`, `candidate/`, `native/` et `INSTALLATION_RECEIPT.json`.

### Dépendances révolutionnaires masquées

Les anciennes surcharges du mod cachaient quatre définitions encore demandées par les scripts d'IA natifs. Leur vérification a identifié une dépendance supplémentaire, le mouvement anticommuniste. Cinq fichiers additionnels rétablissent six objets :

| Nouveau fichier | Objets et portée |
| --- | --- |
| `common/ai_strategies/zz_1776_v115_restored_agendas.txt` | stratégies natives de consolidation de l'État et de confrontation révolutionnaire |
| `common/laws/zz_1776_v115_revolutionary_guard.txt` | garde révolutionnaire, avec ses conditions natives, dont `enlistment_offices` |
| `common/political_movements/zz_1776_v115_anti_communist.txt` | mouvement blanc natif ; création conditionnée à une loi de république des conseils |
| `common/journal_entries/zz_1776_v115_social_revolution.txt` | journal natif de révolution sociale et ses deux conclusions |
| `events/zz_1776_v115_ai_social_revolution.txt` | récompense et nettoyage natifs, sous un identifiant distinct |

Les deux stratégies, la loi et le mouvement conservent exactement les champs natifs. Le journal et l'événement conservent les champs natifs à deux adaptations d'identifiant documentées près : le journal appelle `aor1776_v115_ai_progression.1`, et l'événement natif est enregistré sous cet identifiant. Les textes FR/EN, icônes et image sont hérités des fournisseurs existants et vérifiés ; aucune nouvelle image ou localisation n'est nécessaire.

L'ancien `communism.6` donne la récompense du journal communiste historique du mod. L'écraser changerait ce contenu déjà porté par 39 ; le réutiliser pour le nouveau journal donnerait une récompense différente de son aperçu et omettrait son nettoyage. Le nouvel événement conserve donc la récompense native `modifier_social_revolution`, sa durée `very_long_modifier_time` et `je_social_revolution_cleanup`. L'ancien événement et toutes les entrées existantes de 39 restent identiques.

La technologie, les lois politiques, les idéologies, les groupes d'intérêt, les mouvements liés, les institutions, les barres et les helpers requis se résolvent dans le modèle contrôlé. Aucun historique, loi active ou technologie de départ n'est écrit. Le relevé des instructions effectives de lois initiales ne trouve ni république des conseils ni garde révolutionnaire activée. Aucun raccord automatique de l'ancienne chaîne communiste vers la nouvelle n'est ajouté par ce lot. La disponibilité des définitions ne certifie pas toute la progression révolutionnaire du DLC.

Stratégie préalable et décision de séparation des événements : `DEPENDENCY_STRATEGY.md`. Candidat, contrat de six objets, références et installation : `dependencies_R2/`.

## Qualification des anciens logs

Les six fichiers d'erreurs copiés par la première passe 25 contiennent **14 047 messages**, dont **4 143** citent les stratégies IA ou `00_ai_triggers.txt`. Ils datent du test antérieur ; ils ne sont ni une nouvelle partie, ni un comptage de bugs indépendants.

| Famille du périmètre sélectionné | Messages | Conclusion actuelle |
| --- | ---: | --- |
| Lien `region` invalide | 4 127 | Appels également présents dans les scripts natifs. Les quatre affectations stratégiques manquantes ont été réparées par 24 ; les 677 États terrestres ont actuellement une affectation unique. C'est une explication plausible des anciennes cibles nulles, pas une causalité moteur démontrée ni une disparition de messages certifiée. Aucun remplacement global de l'API géographique n'est effectué. |
| Stratégies politiques absentes | 3 | Les deux fournisseurs sont désormais rétablis. |
| `je_state_and_revolution` absent | 2 | Déjà rétabli par 39 avant ce lot ; sa définition est préservée. |
| `je_social_revolution` absent | 1 | Fournisseur rétabli avec son événement de récompense séparé. |
| Ancienne base navale | 1 | Identifiant et seuil alignés sur la branche native actuelle. |
| Garde révolutionnaire absente | 1 | Fournisseur rétabli. |
| Messages secondaires de postvalidation sans identifiant | 7 | Conservés, sans les compter comme sept défauts indépendants ni leur inventer une attribution objet par objet. |
| Avertissement d'encodage préexistant | 1 | Le fichier d'intervention américaine concerné reste préservé ; les cinq nouveaux fichiers sont avec BOM. |

Les quatre États réparés par 24 sont Tartaria et Galich dans `region_russia`, Kaunas dans `region_eastern_europe` et Chukotka dans `region_northeast_asia`. L'auxiliaire `should_carve_up_china` reste hérité du natif, sans masque local ; ses deux tests `region` ne sont pas réécrits. La vérification statique des régions ne simule pas les objets effectivement chargés dans une sauvegarde.

Preuve détaillée : `HISTORICAL_LOG_TRIAGE.json` conserve les messages, emplacements et empreintes des six logs, sans recopier ou effacer les logs actifs. `CONTEXT_BEFORE.json`, `CONTEXT_AFTER.json` et `CONTEXT_FINAL.json` séparent les étapes de résolution.

## Contrôles effectivement exécutés

- Correctif des deux valeurs : **12/12**, avant et après installation ; **7/7** défauts injectés détectés. Reconstruction inverse exacte des octets, seuil/opérateur, contexte, syntaxe, fournisseur et équivalence native de la branche.
- Premier candidat de dépendances : **155/160**. Deux échecs correspondaient au mouvement manquant, ajouté au candidat R2. Deux autres venaient du lecteur qui omettait les valeurs de script scalaires, et un du classement erroné d'un déclencheur moteur comme helper scripté. Le résultat reste conservé dans `dependencies/` ; aucun faux fournisseur n'est créé pour faire passer ces contrôles.
- Dépendances R2, candidat puis installation réelle : **213/213** et **8/8** contrôles négatifs. Les six suppressions d'objet, le mauvais routage vers l'ancien événement et une syntaxe cassée sont détectés.
- Outil existant de dépendances des journaux : **494 entrées, zéro constat** dans ses références typées et métadonnées. Ce total inclut la seule nouvelle entrée de 25 ; les 493 antérieures et leurs preuves ne sont pas remplacées.
- Inventaire final de ce périmètre IA : **39 stratégies, 191 lois, 494 journaux**, zéro référence manquante parmi les stratégies, bâtiments et journaux examinés ; la garde révolutionnaire a aussi un fournisseur unique. Aucun échec de lecture. Ce contrôle ne constitue pas un audit de tous les types de référence du jeu.
- Les **677 États terrestres** ont une affectation stratégique unique dans le modèle de fichiers courant.
- `git diff --check` sur le fichier partagé retourne **0**, sans diagnostic. Le contrôle `--no-index --check` entre avant/candidat retourne 1 pour les différences de contenu, sans diagnostic d'espacement ; ce code n'est pas présenté comme un échec moteur.

Une première invocation du contrôle des deux valeurs a été lancée avant la fin de la génération du contrat et s'est arrêtée sur son absence ; elle n'a validé ni modifié les données. Le contrôle a ensuite été exécuté sur le contrat terminé. Les échecs de modèle et les candidats initiaux sont distingués des corrections de gameplay, sans écraser leurs preuves.

### Reproduction en lecture seule

Depuis la racine, avec le Python disponible ; choisir de nouveaux noms de sortie sous ce dossier, car les outils refusent d'écraser les preuves :

```powershell
python -B tools/compatibility/issue25_ai_context_audit.py --negative-controls --output docs/reports/compatibility/V1_15_ISSUE25_AI_SCOPE_TRIAGE_2026_11_09/VERIFY_AI_NEW.json
python -B tools/compatibility/issue25_ai_dependencies_audit.py --negative-controls --output docs/reports/compatibility/V1_15_ISSUE25_AI_SCOPE_TRIAGE_2026_11_09/VERIFY_DEPENDENCIES_NEW.json
python -B tools/compatibility/issue39_dependency_audit.py --output docs/reports/compatibility/V1_15_ISSUE25_AI_SCOPE_TRIAGE_2026_11_09/VERIFY_JOURNALS_NEW.json
```

Ne pas relancer `--prepare` sur le dossier existant et ne pas recréer une baseline antérieure depuis les fichiers corrigés. Ces outils ne comportent pas d'installation automatique de leurs candidats.

## Préservation, incertitudes et suite

La surface installée est **un fichier partagé avec deux valeurs modifiées et cinq fichiers neufs**. Les autres champs de la stratégie, anciens événements et journaux, lois actives, technologies et recettes ne sont pas réécrits. Les corrections 22/23/24/39/40, les données de population, frontières et suivis WORLD/SERG restent protégés. La première barrière de conservation, avant les cinq ajouts, retrouve 5 909 sources avec uniquement les deux valeurs attendues ; la preuve finale après ajouts est `FINAL_SOURCE_PROTECTION_R2.json`.

Le vanilla est consulté en lecture seule. Aucune écriture Git, fusion, publication, simulation ou attestation humaine nouvelle. L'ancienne autorisation de fusion distante de 25 n'est pas réutilisée. Les résultats statiques ne prouvent pas l'élection des stratégies, la sélection des lois, les révolutions, le rendu ou la persistance en partie.

Le lot est prêt à relire et à tester selon `RUNTIME_PROTOCOL.md`. La mission 25 reste ouverte pour les tests intégrés du candidat local exact et la décision de sortie. Les autres familles de contenu et limites déjà documentées par 39 restent distinctes ; aucune parité complète du DLC ni réduction globale du nombre d'erreurs n'est proclamée.
