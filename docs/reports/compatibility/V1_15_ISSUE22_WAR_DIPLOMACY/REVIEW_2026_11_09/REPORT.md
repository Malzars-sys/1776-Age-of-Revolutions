# #22 — Guerre et diplomatie, livraison du 9 novembre 2026

Statut technique : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Destination du tableau : **In review**. L'issue reste ouverte. Aucun nouveau test moteur ni reçu joueur n'est acquis par cette livraison.

Périmètre : compatibilité 1.15, soutien de guerre restant, définitions diplomatiques masquées, objectifs et déclarations des deux guerres de départ. Exécutable canonique consulté : `C:\Games\Victoria 3\binaries\victoria3.exe`, FileVersion/ProductVersion **1.15.0**. HEAD du workspace : `0396b1133168c1721b61cee5ae5334f1a4f5e4e1`. Les modifications sont locales, sans commit ni push.

## Corrections installées

Treize valeurs, dans six fichiers, reprennent les commandes, opérateurs, cibles et valeurs du vanilla courant. Le contrat conserve chaque site et ses empreintes : [CONTRACT.json](CONTRACT.json).

| Fichier / objet | Avant | Après |
| --- | --- | --- |
| `common/ideologies/01_character_ideologies.txt`, `ideology_pacifist`, deux branches | soutien `< 0` | `< 50` |
| `common/scripted_effects/00_victoria_scripted_effects.txt`, `calculate_national_identity_progress` | bandes `50 / 25 / 0` | bandes natives `80 / 65 / 50`, mêmes opérateurs stricts/inclusifs |
| `events/election_events/election_contextual_events.txt`, événement `.7`, déclencheur et sélection de guerre | `> 70` | `> 85` |
| `events/tech_events/aviation.txt`, `aviation.1` | soutien immédiat `+10` | `+5` |
| `events/technology_events.txt`, `technology_events.30` | soutien immédiat `−10` | `−5` |
| `events/heavenly_kingdom_events.txt`, `heavenly.4`, deux options conservées | soutien du coup diplomatique `+100` | `+50` |

Les seuils négatifs étaient inaccessibles sur l'échelle 0–100. Les autres calibrages sont alignés sur les objets natifs correspondants, sans interpolation générale des valeurs. Les effets de variation déjà portés en #28 restent à `−5` ; ils ne sont pas divisés à nouveau. Le Taiping conserve ses deux branches propres au mod, contre une occurrence correspondante dans le vanilla. Seuls les nombres changent : les octets restants et les BOM sont comparés aux copies prises avant intervention.

L'ancien remplacement de `common/diplomatic_plays/00_diplomatic_plays.txt` cachait quatre définitions natives. Elles sont rétablies, sans réécrire ce fichier partagé, dans `common/diplomatic_plays/zz_1776_v115_restored_war_plays.txt` :

- `dp_return_state_to_subject` : rendre une revendication à un sujet ;
- `dp_release_as_subject` : libérer comme sujet ;
- `dp_unify_russia` : coup d'unification russe ;
- `dp_polish_uprising` : soulèvement polonais.

Les quatre objets sont identiques aux objets du vanilla courant. Leurs deux fichiers de déclencheurs auxiliaires sont hérités sans masque local ; les identifiants requis se résolvent. Les contenus russe et polonais ne sont pas forcés en 1776. L'exception historique du mod sur l'infamie d'annexion russe, documentée en #32, reste inchangée.

## Audit des objectifs, sujets et guerres

Le catalogue effectif, constitué des fichiers natifs puis des remplacements locaux, compte **45 objectifs** et **60 coups diplomatiques**, contre 39 et 56 natifs. Chaque identifiant natif possède désormais une définition dans le catalogue effectif ; ce contrôle de présence ne certifie pas l'équivalence de chaque comportement. Aucun doublon ordinaire n'est trouvé dans ces deux catalogues. Les types d'objectif, drapeaux, références de miroirs et objectifs des coups diplomatiques se résolvent.

Les trois miroirs territoriaux installés en #32 restent présents. L'indépendance hérite de `restore_subject`. Les objectifs politiques et partiels propres au mod ne reçoivent pas arbitrairement de miroir territorial : l'absence de miroir conserve leur résolution par capitulation ou paix négociée, selon le moteur. Les hooks de paix, capitulation, exécution d'objectif et fin de guerre sont déclarés ; leur simple présence ne prouve pas leur émission ni l'ordre de leurs callbacks.

Les deux déclarations de guerre de départ sont inchangées, empreinte à l'appui :

| Guerre | Participants déclarés | Objectifs explicites examinés |
| --- | --- | --- |
| Indépendance américaine | USA initiateur, GBR cible ; Espagne neutre dans cette déclaration | `dp_independence`, objectif natif d'indépendance |
| Irak ottoman / Perse | IR1 initiateur, PER cible ; OMA avec IR1, ARB avec PER | Perse : Bassora IR1 ; IR1 : Khuzestan ARB ; Oman : port de traité au Fars PER |

Les TAG, coups et types d'objectifs se résolvent. La cohérence des propriétaires chargés, des sujets, des fronts et des conséquences de paix reste à vérifier dans le moteur. Le montage IR1 initiateur conserve l'approximation déjà approuvée permettant sa contre-offensive sans faire de son suzerain le défenseur principal. Aucun nouveau réglage territorial, militaire ou diplomatique initial n'a été ajouté ici.

## Résultats exécutés

| Contrôle sur la version livrée | Résultat |
| --- | --- |
| `tools/compatibility/issue22_war_diplomacy_audit.py --negative-controls --output …/VALIDATION.json` | **276/276**, statique seulement |
| Réintroduction en mémoire des treize anciennes valeurs et suppression de chacune des quatre actions restaurées | **17/17 détectées** |
| Audit #26, appel `audit()` sans réécriture de son suivi | **1 732/1 732** |
| Audit #32, appel `audit()` | **27/27**, et **12/12** contrôles négatifs détectés |
| Contrat historique #28, lecture brute | **37/38** ; son empreinte de tout le reste du fichier électoral est devenue obsolète avec les deux nouveaux seuils de `.7` |
| Non-régression #28, seuls les deux seuils de #22 rétablis en mémoire pour comparaison | **38/38** ; les six sites de #28 et tous les autres jetons sont préservés |

Preuves : [VALIDATION.json](VALIDATION.json), [PREDECESSORS_FINAL.json](PREDECESSORS_FINAL.json), [PROTECTIONS.json](PROTECTIONS.json). L'ancien audit #28 et son contrat ne sont ni modifiés ni affaiblis. Sa divergence brute est conservée.

`git diff --check` signale une indentation espace-tabulation préexistante sur la ligne modifiée d'`aviation.txt`. Le changement de valeur conserve exactement cette indentation ; aucun nouveau défaut d'espacement n'est introduit. Les avertissements LF/CRLF de Git sont conservés dans la preuve. Ils ne constituent pas un test moteur.

## Dette héritée et limites

Le premier audit a échoué à son contrôle global « aucune ancienne référence effective » : le vanilla 1.15.0 fournit encore `common/script_values/war_exhaustion_values.txt`, qui mentionne `war_exhaustion_from_acceptance_of_dead` et `additional_war_exhaustion`. Ce résultat initial est conservé dans [INITIAL_VALIDATION_INHERITED_RESIDUE.json](INITIAL_VALIDATION_INHERITED_RESIDUE.json). L'audit final distingue explicitement l'absence de ces appels dans les scripts du mod de cet unique reliquat natif, dont il vérifie l'empreinte. La recherche de l'identifiant exact `war_exhaustion` dans les `.txt` common/events du mod et du vanilla ne trouve que sa définition dans ce fichier. Cela ne prouve pas l'absence de consommateur interne au moteur. Le vanilla reste inchangé et cette réserve doit accompagner tout diagnostic de journal d'erreurs.

La fin du journal américain attend actuellement la paix globale (`is_at_war = no`), même si le lien de sujet a déjà changé. C'est une limite de conception préexistante à observer séparément d'une régression 1.15. Le rework américain #38, les prêts, les Minutemen, Join Ongoing War et les frontières sont hors périmètre. L'unification territoriale de #32 reste explicitement non testée ; son issue n'est pas clôturée par cette livraison.

Le reçu joueur du 8 novembre accepte plusieurs missions précédentes et seulement les branches annexion/conquête de #32. Il ne certifie ni ces treize nouveaux calibrages, ni les quatre actions restaurées, ni deux guerres complètes au titre de #22. Aucun reçu humain supplémentaire n'est créé.

## Préservation et review

Sur les **2 483 sources** relevées avant intervention, seuls les six fichiers autorisés ont changé ; le seul nouveau fichier de jeu est celui des quatre actions restaurées. Aucun autre changement concurrent n'est réécrit. HEAD et empreinte de l'index Git sont inchangés. #21, les travaux territoriaux, TECH, économie, PM, navires, sujets et localisations sont préservés. Aucun fichier vanilla n'est écrit.

Le protocole restant est [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md). La review doit enregistrer le build effectivement lancé et les résultats observés avant de valider les critères moteur et de passer l'issue en Done.

## Sources techniques

- Fichiers canoniques homonymes des six correctifs et `common/diplomatic_plays/00_diplomatic_plays.txt` ; empreintes et sites dans le contrat.
- `C:/Games/Victoria 3/game/common/war_goal_types/war_goal_types.md` : miroirs, délai d'occupation, `restore_subject`, capitulation et scopes d'exécution.
- `C:/Games/Victoria 3/game/common/scripted_triggers/00_scripted_triggers.txt` et `00_diplomacy_triggers.txt` : auxiliaires des actions restaurées.
- Consommateurs natifs : `common/journal_entries/08_ip5_congress_poland.txt`, `events/russia_events/congress_poland_events.txt`, `common/scripted_effects/05_russian_civil_war_scripted_effects.txt`.
- [Notes officielles 1.15 / Dev Diary 196 du 5 novembre 2026](https://steamcommunity.com/app/529340/announcements/?l=french) : nouvelle échelle du soutien, exécution d'objectifs pendant la guerre et suppression des anciennes commandes. La référence exacte des calibrages demeure l'installation locale, pas une formule déduite de l'annonce.
- [Issue #22](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/22), livraisons #26/#28/#29/#32 et reçu `V1_15_GROUPED_REVIEW_TEST_2026_11_08/HUMAN_ACCEPTANCE_2026_11_08.json`.
