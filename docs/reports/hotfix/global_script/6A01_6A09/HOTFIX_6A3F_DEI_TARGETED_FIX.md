# HOTFIX-6A.3F — Correction ciblée de la dissolution de la DEI

Date de travail : 28 juillet 2026  
Branche : `hotfix-dlc-audit`  
HEAD de départ : `f617b0812d2998cba42bda28237ebcbd03115c21`

## Statut

- `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`
- `HOTFIX_6A3F_DEI_TARGETED_FIX_STATIC_PASS`
- `DEI_TERRITORIAL_RELEASE_HUNKS_APPLIED`
- `DEI_VANILLA_1_13_ALIGNMENT_APPLIED`
- `DEI_RUNTIME_CORE_PASS`
- `DEI_POST_VOC_FLAG_RUNTIME_PASS`
- `DEI_POST_COMPANY_ECONOMY_GATE_RUNTIME_PASS`
- `DEI_POST_COMPANY_LAW_PERSISTENCE_RUNTIME_PASS`
- `DEI_INDONESIA_BRANCH_RUNTIME_PASS`
- `DEI_REFUSAL_BRANCH_RUNTIME_PASS`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Le correctif territorial et l’ensemble de la transition DEI/VOC sont validés en jeu. Le runtime confirme le drapeau post-VOC, l’apparition naturelle de `dei_breakup.1`, l’ouverture de l’événement économique, le masquage correct de l’interventionnisme avec le servage et des Industriels faibles, l’activation persistante du Mouvement agraire après sauvegarde/rechargement, la branche Indonésie et l’option de refus. La phase reçoit donc le verdict final `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`.

## 1. Résultats runtime déjà acquis

Le fork monté a été testé depuis une sauvegarde indépendante de la DEI.

- l’option Java crée correctement `CEY` et `SAF` ;
- Ceylan appartient à `CEY` et les portions DEI du Cap et du Cap-Oriental appartiennent à `SAF` ;
- `CEY` et `SAF` sont indépendants ;
- la DEI devient `JAV` et le nom visible devient `Java` après le tick de mise à jour ;
- les modificateurs `colonial_administration_76` et `modifier_india_company_rule` disparaissent ;
- la variable `malaya_subject_var` disparaît, ce qui empêche le retour du nom dynamique `Malaisie` ;
- `dei_breakup.1` apparaît naturellement par le pulse mensuel, sans commande console ;
- le drapeau rouge, blanc et bleu choisi pour Java apparaît correctement ;
- « L’économie après la Compagnie » s’ouvre après « Jour de l’indépendance » ;
- avec le servage et des Industriels faibles, seules les options Traditionalisme et Mouvement agraire sont visibles : l’interventionnisme reste correctement indisponible ;
- le choix du Mouvement agraire remplace effectivement `law_extraction_economy` ;
- après sauvegarde et rechargement, le nom `Java`, le drapeau post-VOC et le Mouvement agraire restent constants ;
- la branche `IDN` produit correctement l’Indonésie, avec son nom, son drapeau, ses cultures et les événements d’indépendance et d’économie post-compagnie ;
- l’option de refus conserve l’identité « Indes orientales », son drapeau et les caractéristiques de la compagnie, sans appliquer les nettoyages réservés à la dissolution.

Ce test a révélé deux dettes supplémentaires :

1. la suppression de `malaya_subject_var` supprimait aussi le drapeau malaisien souhaité et rétablissait le drapeau vert et blanc par défaut de Java ;
2. le pays indépendant conservait `law_extraction_economy`, une loi conçue pour une compagnie sujette.

L’opérateur a explicitement autorisé l’extension du périmètre pour corriger et documenter ces deux points.

## 2. Drapeau post-VOC de Java

`malaya_subject_var` ne peut pas être conservée : elle gouverne à la fois le drapeau `MAA_oligarchy` et le nom dynamique colonial `Malaisie`.

La solution sépare les deux responsabilités :

- l’option Java supprime toujours `malaya_subject_var` ;
- elle pose ensuite `jav_post_voc_flag_var` ;
- une définition de drapeau propre à `JAV` utilise `MAA_oligarchy` lorsque cette nouvelle variable est présente ;
- sa priorité `10` surpasse le drapeau Java par défaut de priorité `1` ;
- le drapeau théocratique de priorité `20` reste prioritaire si le régime évolue ultérieurement ;
- aucun canton de suzerain n’est admis pour ce drapeau indépendant.

Le nouveau mécanisme ne pilote aucun nom dynamique et ne restaure aucun état colonial.

## 3. Nettoyage de l’héritage de la compagnie

Les options Java et Indonésie exécutent toutes deux les nettoyages suivants :

```txt
remove_variable = malaya_subject_var
remove_modifier = colonial_administration_76
remove_modifier = modifier_india_company_rule
```

L’option Java ajoute seule :

```txt
set_variable = jav_post_voc_flag_var
```

L’option de refus ne reçoit aucun de ces nettoyages : la continuité de la compagnie et de ses effets y reste intentionnelle.

## 4. Événement économique post-compagnie

Les options Java et Indonésie programment `dei_breakup.2` deux jours après la dissolution, soit après `independence.2` programmé à un jour.

L’événement ne peut s’ouvrir que si :

- le pays courant est `JAV` ou `IDN` ;
- il est indépendant ;
- il possède encore `law_extraction_economy`.

Il ne propose jamais le laissez-faire.

### Traditionalisme

Le traditionalisme est le choix de sécurité. Il ne demande aucune technologie, mais respecte les incompatibilités principales de la loi : anarchie, conseils ouvriers et formes d’imposition avancées incompatibles.

### Mouvement agraire

Le Mouvement agraire n’est proposé que si :

- `romanticism` est recherché ;
- aucune loi incompatible n’est active ;
- les Ruraux ou les Propriétaires terriens sont puissants ;
- ce même groupe puissant participe au gouvernement.

### Interventionnisme

L’interventionnisme n’est proposé que si :

- `manufacturies` est recherché ;
- le servage, l’anarchie, les conseils ouvriers et le travail des femmes aux champs ne sont pas actifs ;
- les Industriels sont puissants ;
- les Industriels participent au gouvernement.

Ces verrous empêchent une compagnie nouvellement indépendante de recevoir automatiquement une loi économique avancée par simple choix d’événement. Dans la situation runtime observée — servage actif et Industriels faibles — l’interventionnisme doit rester absent.

## 5. Fichiers gameplay et localisation modifiés

- `events/dei_breakup.txt`
- `common/flag_definitions/00_flag_definitions.txt`
- `localization/english/mod_v2content_l_english.yml`
- `localization/french/mod_v2content_l_french.yml`

L’extension de périmètre est strictement limitée au drapeau post-VOC, au nouvel événement et à ses six clés de localisation par langue.

Après le premier contrôle visuel, les textes `dei_breakup.2.d` et `dei_breakup.2.f` ont été développés pour reprendre la structure narrative de « Jour de l’indépendance » : 42 mots de présentation et 94 mots d’ambiance en français, contre respectivement 27 et 90 pour l’événement de référence. Le nouveau récit s’appuie sur les registres de la Compagnie et le débat entre propriétaires, villages, négociants et industriels.

## 6. Validation statique

Contrôles passés :

- profondeur finale des accolades : `0` pour l’événement et les définitions de drapeaux ;
- profondeur minimale : `0` ;
- une définition de `dei_breakup.2` ;
- deux programmations de `dei_breakup.2`, uniquement dans les options Java et Indonésie ;
- une pose de `jav_post_voc_flag_var`, uniquement dans l’option Java ;
- deux suppressions de chaque reliquat VOC ;
- une activation de chaque loi autorisée : traditionalisme, Mouvement agraire, interventionnisme ;
- zéro activation de laissez-faire ;
- trois options économiques exactement ;
- verrous technologiques et politiques présents ;
- `alk_breakup.1` identique à HEAD après l’ancre `namespace = alk_breakup` ;
- `git diff --check` propre ;
- index Git vide.

Le filewatcher a rechargé `events/dei_breakup.txt` à `22:23:54` avec trois événements. L’erreur temporaire `Event not found! EventID: dei_breakup.2`, produite lors d’une première disposition en référence avant définition, a été éliminée en plaçant `dei_breakup.2` avant `dei_breakup.1`.

Le runtime a ensuite révélé que `law_women_in_the_fields` est une variante de loi et ne doit pas être passée à `has_law_or_variant`. Les deux gardes concernées utilisent désormais `has_law`. Le rechargement de `22:46:15` ne contient plus cette erreur et charge toujours les trois événements.

Les erreurs restantes signalées aux lignes ALK (`region_manchuria`, `region_east_siberia`, rôle `politician`) existaient hors du bloc DEI et n’ont reçu aucun hunk.

## 7. Validation runtime finale

La clôture repose sur trois scénarios opérateur :

1. **Java** : dissolution, libération de `CEY` et `SAF`, nettoyage des reliquats VOC, bon nom, bon drapeau, apparition de l’événement économique, choix du Mouvement agraire, puis sauvegarde/rechargement. Le nom, le drapeau et la loi persistent.
2. **Indonésie** : l’option pan-indonésienne transforme correctement la DEI en `IDN`; le nom et le drapeau indonésiens apparaissent, les cultures prévues sont présentes et les deux événements différés sont actifs.
3. **Refus** : la compagnie conserve son identité « Indes orientales », son drapeau et ses caractéristiques coloniales. Les nettoyages post-VOC ne sont pas appliqués.

Le verrouillage économique est également validé : le laissez-faire n’est jamais proposé et l’interventionnisme reste absent dans la situation observée avec servage actif et Industriels faibles.

## 8. Périmètre historique différé

Le mod ne contient pas encore de chaîne distincte permettant à la Grande-Bretagne de prendre les possessions VOC du Cap et de Ceylan tant que la compagnie reste sujette des Pays-Bas. L’audit a confirmé que ce résultat dépend historiquement de l’invasion française des Provinces-Unies, des lettres de Kew de 1795 et des guerres révolutionnaires puis napoléoniennes.

Cette chaîne n’appartient pas à HOTFIX-6A.3F. Elle est explicitement reportée au futur développement consacré à la Révolution française et aux guerres napoléoniennes. Aucun événement Kew et aucun transfert britannique daté n’ont été ajoutés pendant cette phase.

## 9. Rollback exact

- retirer les deux appels `trigger_event = { id = dei_breakup.2 days = 2 }` ;
- retirer entièrement `dei_breakup.2` ;
- retirer les six clés `dei_breakup.2.*` de chaque fichier de localisation ;
- retirer `set_variable = jav_post_voc_flag_var` ;
- retirer uniquement la définition de drapeau Java de priorité `10`.

Le rollback de cette extension ne doit pas retirer les libérations `CEY`/`SAF`, les alignements vanilla 1.13, ni les nettoyages VOC déjà justifiés par le runtime.

## 10. Protections

- `alk_breakup.1` : contenu après son namespace identique à HEAD ;
- `bject` : SHA-256 inchangé `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` ;
- les sept fichiers non suivis de `docs/research/technology/` conservent leurs hashes initiaux ;
- stash MARATH non inspecté et non modifié ;
- aucun fichier staged ;
- aucun lancement de Victoria 3 par l’agent.

## 11. Verdict final

`HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`  
`HOTFIX_6A3F_DEI_TARGETED_FIX_STATIC_PASS`  
`DEI_TERRITORIAL_RELEASE_HUNKS_APPLIED`  
`DEI_VANILLA_1_13_ALIGNMENT_APPLIED`  
`DEI_POST_VOC_LEGACY_CLEANUP_RUNTIME_PASS`  
`DEI_POST_VOC_FLAG_RUNTIME_PASS`  
`DEI_POST_COMPANY_ECONOMY_GATE_RUNTIME_PASS`  
`DEI_POST_COMPANY_LAW_PERSISTENCE_RUNTIME_PASS`  
`DEI_INDONESIA_BRANCH_RUNTIME_PASS`  
`DEI_REFUSAL_BRANCH_RUNTIME_PASS`  
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
