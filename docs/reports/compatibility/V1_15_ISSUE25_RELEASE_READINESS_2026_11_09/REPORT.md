# Mission 25 — revue d'intégration du hotfix 1.15

Date : **9 novembre 2026, Europe/Paris**. Mission choisie dans le Backlog à la demande du mainteneur, puis observée en **In progress** sur Project 1. La mission 22 venait d'être prise par un autre agent ; ses fichiers et son suivi ne sont pas modifiés ici.

**Résultat : dossier de préparation livré ; autorisation de sortie non acquise.** Aucun lancement moteur, changement de gameplay, changement du vanilla, commit, push, changement de branche, merge ou publication de version n'est effectué dans cette passe. Les preuves sont celles du workspace et des traces conservées, complétées par les validations déclarées par le mainteneur.

## Configuration et preuves

- Workspace : `main`, HEAD `0396b1133168c1721b61cee5ae5334f1a4f5e4e1`, avec les modifications locales préexistantes. Le HEAD seul ne reproduit donc pas le mod testé.
- `BASELINE.json` conserve l'état Git en lecture seule, l'empreinte de l'index et **2 515 fichiers de scripts, interface, localisations, carte et consignes**. Les évolutions concurrentes seront distinguées par `SOURCE_PROTECTIONS.json` ; elles ne seront ni restaurées ni attribuées à cette passe.
- `LOG_SNAPSHOT.json` décrit **11 fichiers copiés**, dont les six journaux d'erreurs conservés. Les sources actives ne sont pas effacées. Les copies ne constituent pas une capture atomique du moteur.
- Le `code_revisions.log` copié atteste `release/1.15.0`, build `6338547985dbc271523e149f362a6fd93dc62975`, démarrage indiqué à **22:08:07** dans cette cohorte. Le dernier message d'erreur retenu est à 23:44:13. Ces heures sont celles inscrites dans les traces ; elles ne sont pas une durée de simulation.
- Les DLC et pays exacts de chaque manipulation du test groupé n'ont pas été fournis individuellement. L'activation de State and Revolution est déclarée par le mainteneur dans la conversation ; aucune nouvelle vérification exhaustive de licences n'est revendiquée.

Le reçu [du test groupé](../V1_15_GROUPED_REVIEW_TEST_2026_11_08/HUMAN_ACCEPTANCE_2026_11_08.json) accepte les missions **21, 27, 29, 30 et 33**, avec **conquête et annexion** acceptées dans la 32 et **unification explicitement non testée**. Il porte sur les sept points du résumé. Il ne contient pas des mesures distinctes pour toutes les situations avancées de l'annexe. Ce reçu n'est ni remplacé ni étendu par l'analyse des logs.

## Contrôles rejoués sur les données actuelles

| Contrôle | Résultat effectif | Limite |
| --- | --- | --- |
| API de la mission 21 | Premier passage : **485/485**, PASS_STATIC_ONLY. Après changements concurrents : **484/485**, FAIL_STATIC conservé. | Le second passage relève uniquement `events/technology_events.txt.only_authorized_spans` : le fichier a changé hors des modifications de l'ancien lot 21. Aucun appel d'API retirée n'est retrouvé dans ce recontrôle. Ce changement concurrent n'est ni restauré ni accepté automatiquement. Aucun nouvel essai moteur. |
| Cuivre de la mission 31 | **154/155**, FAIL_STATIC conservé ; **6/6** contrôles négatifs détectés ; 28 coefficients natifs contrôlés | Une assertion ancienne exigeait la conservation de tous les champs des PM personnalisés, y compris leurs anciennes textures. |
| Réconciliation de cet échec cuivre | **Deux champs de texture seulement** diffèrent : doublage en cuivre et coque non traitée, désormais avec les icônes demandées | Toutes les autres feuilles de ces méthodes et des autres méthodes personnalisées sont identiques à la référence de cette assertion. Le validateur n'a pas été modifié pour afficher un succès artificiel. |
| Références économiques du mod | **26 230 références**, aucun identifiant cible manquant, aucune erreur de parsing, aucun PM initial incompatible détecté | **Sept références ambiguës** dues à des doublons restent à vérifier dans le moteur sous la mission 23. |
| Témoin économique vanilla | **18 181 références**, PASS_STATIC_ONLY | Témoin de résolution de fichiers, pas économie simulée ni comparaison exhaustive des logs vanilla. |

Les sept ambiguïtés sont les mêmes familles documentées dans la mission 23 : groupe forestier, automatisation ferroviaire du caoutchouc et cinq ateliers de subsistance. Aucun doublon n'est supprimé ici. La distribution des gisements du mod reste hors des modifications de cette passe.

### Travaux concurrents observés au contrôle final

Le contrôle du dossier passe **17/18 assertions** ; l'assertion exigeant l'identité de toutes les sources avec le début de passe relève **six changements concurrents**, conservés sans restauration :

- `common/ideologies/01_character_ideologies.txt` ;
- `common/scripted_effects/00_victoria_scripted_effects.txt` ;
- `events/heavenly_kingdom_events.txt` ;
- `events/technology_events.txt` ;
- `events/election_events/election_contextual_events.txt` ;
- `events/tech_events/aviation.txt`.

La passe 25 n'écrit aucun de ces fichiers. L'auteur et l'acceptation de ces nouveaux changements ne sont pas déduits de leurs seules empreintes. L'index Git reste identique. L'échec de cette assertion de conservation est gardé dans `VALIDATION.json`, avec un recontrôle API séparé dans `API21_RECHECK_AFTER_CONCURRENT.json` après observation de ces évolutions. Les erreurs des logs copiés ne constituent pas un retest des modifications concurrentes plus récentes.

Commandes :

```powershell
& $taskPython -B tools/compatibility/issue21_api_audit.py --output docs/reports/compatibility/V1_15_ISSUE25_RELEASE_READINESS_2026_11_09/API21_RECHECK.json
& $taskPython -B tools/compatibility/issue31_copper_alignment_audit.py --negative-controls
& $taskPython -B tools/compatibility/issue23_economy_reference_audit.py --output docs/reports/compatibility/V1_15_ISSUE25_RELEASE_READINESS_2026_11_09/ECONOMY_MOD.json
& $taskPython -B tools/compatibility/issue23_economy_reference_audit.py --native --output docs/reports/compatibility/V1_15_ISSUE25_RELEASE_READINESS_2026_11_09/ECONOMY_NATIVE.json
& $taskPython -B tools/compatibility/issue25_release_readiness_audit.py --evidence docs/reports/compatibility/V1_15_ISSUE25_RELEASE_READINESS_2026_11_09
```

`$taskPython` est le chemin de l'interpréteur Python du runtime utilisé pour ces exécutions. Les stdout et JSON sont conservés dans ce dossier ; aucun outil tiers n'est installé. Le nouvel outil lit les copies explicites des logs. Deux états intermédiaires de classification sont conservés : une erreur de scope dans un journal ne doit pas être confondue avec une ancienne clé de conclusion ; `fail` doit aussi être compté parmi les anciennes clés. Les chiffres ci-dessous sont ceux de la dernière classification.

## Triage des logs conservés

Les six fichiers d'erreurs contiennent **14 047 messages**, regroupés en **5 812 signatures normalisées** par le lecteur existant. Ce sont des messages, pas 14 047 bugs indépendants, pas un décompte de crashs et pas six parties distinctes.

| Famille | Messages | Interprétation |
| --- | ---: | --- |
| Scopes ou cibles invalides | 7 056 | Mélange de surcharges du mod et de consommateurs hérités du vanilla. |
| Autres diagnostics moteur | 4 469 | Groupe conservé pour qualification, sans gravité universelle inventée. |
| Anciennes clés de conclusion des journaux | 1 368 | Rejets explicites de jetons dans des journaux hérités encore présents. |
| Avertissements d'encodage | 872 | Le moteur annonce essayer d'utiliser les fichiers ; pas une preuve de panne à chaque occurrence. |
| Clés ou références non résolues | 259 | À qualifier par contexte et fournisseur effectif. |
| Doublons de localisation | 22 | Dette distincte des anciennes collisions cuivre corrigées. |
| Version du mod déclarée 1.13 | 1 | Avertissement du lanceur confirmé ; candidat de correction préparé. |

Exemples prioritaires :

- **IA géographique** : 2 144 messages avec `region` invalide, passant par `00_ai_triggers.txt:1001` et la surcharge `00_default_strategy.txt:2024` ; 1 970 autres à `00_default_strategy.txt:2027`. À transmettre au périmètre 22, sans modifier ses fichiers.
- **Culture et religion** : 811 messages de culture invalide dans le mouvement culturel et 660 de religion invalide dans le groupe dévot. Ces deux fichiers sont **hérités du vanilla** dans la résolution actuelle. Cela ne prouve pas une cause vanilla : le contexte fourni par le scénario doit être isolé avant attribution.
- **Journaux non couverts par le lot accepté** : rejets `complete` / `on_complete` dans le didacticiel et d'autres fichiers hérités, dont l'ancien Grand Jeu. Le correctif de sélection des objectifs n'a pas migré automatiquement toutes ces conclusions.
- **Contenu communiste/DLC** : références rejetées à `ideology_communist_leader` et `je_paris_commune` dans des effets hérités. Le chargement d'un consommateur natif ne suffit pas lorsque le mod masque ou ne fournit plus son objet de contexte.

`LOG_SOURCE_RESOLUTION.json` distingue surcharge locale, héritage natif et chemin non résolu. Les responsabilités et gravités restent bornées : aucun nouveau crash du mod n'est démontré par cette passe de lecture.

### Comparaison avec la référence initiale

Le rapport du 6 novembre est disponible et distingue déjà des erreurs présentes sans mod : il cite notamment **350 messages / 340 signatures** dans sa troisième capture vanilla, ainsi que des doublons et localisations GUI communes. Ses archives brutes `vanilla_russia_loaded_03` ne sont pas retrouvées parmi les preuves locales consultées ici.

On peut donc comparer les familles décrites et constater les corrections ciblées actuelles, mais **pas soustraire les 350 messages du total actuel**, ni annoncer une réduction globale chiffrée, ni attribuer tous les scopes natifs au mod. Une comparaison exhaustive exigera de réutiliser l'archive initiale identifiée ou de capturer une nouvelle référence de scénario comparable.

## Intégration : main et hotfix ont divergé

Les lectures GitHub directes attestent :

| Référence | SHA |
| --- | --- |
| `main` distant et HEAD local | `0396b1133168c1721b61cee5ae5334f1a4f5e4e1` |
| `hotfix/1.15` distant | `b72dc3584e1225f8c675b7c6c9f295cde122b821` |
| Ancêtre commun | `52c42808bdb0748e69fbde3423bb5004b5b1f20a` |

La comparaison `main...hotfix/1.15` retourne **diverged**, 16 commits propres au hotfix et un propre à main. La PR 34 est **ouverte, draft, non fusionnée**, avec `mergeable=false` et `mergeable_state=dirty`. Son champ `base_sha` conserve l'ancien SHA ; le head actuel de main est vérifié séparément par l'API des branches. Les réponses résumées sont dans `REMOTE_INTEGRATION_STATE.json`.

La validation du workspace sale n'est donc pas automatiquement celle de cette PR. Il faut préparer une intégration bornée des changements retenus sur le main actuel, résoudre les conflits en conservant les travaux concurrents, puis tester le candidat exact. Aucune fusion ni réécriture de branche n'a été tentée.

## Livrables et suite

- [Notes de version préparatoires](RELEASE_NOTES_DRAFT.md), sans publication ni numéro de version du mod inventé.
- [Conditions restant à satisfaire](RELEASE_GATES.md), distinguant dette observée, limites de couverture et actions d'intégration.
- `LAUNCHER_VERSION_CANDIDATE.patch` et deux fichiers candidats : déclarations de prise en charge **1.15**, sans changement de version **2.5.0** ni des chemins de remplacement. **Candidats seulement, non installés.**
- Les empreintes, contrôles et preuves détaillés restent dans les JSON de ce dossier. Les copies brutes des logs restent locales et ne sont pas publiées dans le corps de l'issue.

La mission 25 reste **In progress** : la préparation documentaire et les contrôles statiques sont livrés, mais le candidat intégré exact, les points encore non testés et l'acceptation finale de sortie ne le sont pas. La coordination 19 n'est pas clôturée. Les missions déjà acceptées ne sont pas rouvertes par cette analyse.
