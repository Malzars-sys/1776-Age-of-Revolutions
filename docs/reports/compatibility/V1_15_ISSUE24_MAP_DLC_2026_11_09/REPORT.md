# Mission 24 — carte, États et dépendances DLC, 9 novembre 2026

## Livraison vérifiée

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION pour le sous-lot structurel.** La reprise après coupure est terminée : les résultats interrompus ont été retrouvés, les fichiers installés vérifiés et les contrôles finaux exécutés. **31/31 contrôles du candidat, 6/6 cas témoins et 24/24 contrôles de livraison passent.** Aucun résultat moteur nouveau n'est revendiqué.

La mission 24 reste **In progress** comme suivi global : journaux sous 39, cultures sous 40, autres constats qualifiés ci-dessous et acceptation moteur restent ouverts. Aucun score de clôture globale n'est calculé à partir de ce seul lot.

## Changements installés

| Objet | Correction |
| --- | --- |
| Région stratégique russe | Retirer les références inexistantes à Tula et Kostroma ; remplacer Saratov et Vologda par les États existants Tartaria et Galich. Les provinces des deux premiers sont déjà dans des États du même groupe. |
| Europe orientale | Remplacer la référence inexistante à Lithuania par Kaunas. |
| Asie du Nord-Est | Ajouter Chukotka à la même région stratégique que ses provinces vanilla d'origine. |
| Mindanao | Rétablir le port terrestre `xF0014A` à la place de la province maritime `x16C9FB`. Conserver la sortie navale 3125, mer des Moluques. |

Les quatre rattachements ont une correspondance technique unanime à la région canonique : Tartaria **46/46** provinces, Galich **282/282**, Kaunas **23/23**, Chukotka **474/474**. Il s'agit de rattachements de références aux régions stratégiques, sans nouvelle affirmation historique ni modification de frontière. `REGION_PROVENANCE.json` conserve les donneurs et les dénominateurs.

Deux fichiers nouveaux masquent intentionnellement les fichiers vanilla de même chemin :

- `common/strategic_regions/europe_strategic_regions.txt` ;
- `common/strategic_regions/east_asia_strategic_regions.txt`.

Tous leurs objets et champs canoniques hors listes ciblées sont conservés. Ces deux masquages devront être recomparés lors d'une prochaine mise à jour vanilla. Le troisième chemin, `map_data/state_regions/12_indonesia.txt`, change uniquement le champ de port de Mindanao. Le défaut de port remonte au commit `f34a6b88d` du 14 octobre 2026 ; il est enregistré comme dette structurelle antérieure, sans l'attribuer à la 1.15.

Les pixels, territoires, propriétaires, populations, ressources — dont le cuivre propre au mod —, lois, technologies, sorties navales, locators et champs climatiques restent préservés. Le vanilla n'a reçu aucune écriture. Aucune opération Git ni publication n'a été réalisée pour cette mission.

## Contrôles et portée

L'inventaire effectif compte **783 régions d'État, dont 677 terrestres**, **142 régions stratégiques**, **1 074 définitions de pays** et **322 cultures**. Ce sont des objets et écritures de scripts, pas des pays ou populations observés en jeu. Le témoin canonique 1.15.0 compte 782 régions d'État, dont 676 terrestres.

Les contrôles couvrent les fournisseurs effectifs, masquages de fichiers et remplacements explicites, unicité des identifiants, appartenance des provinces/hubs, présence des couleurs dans le raster, rattachements stratégiques, sorties navales, bornes climatiques et références de départ. Les six témoins isolés comprennent un cas valide puis des erreurs délibérées de référence, rattachement double, port extérieur, identifiant numérique dupliqué et culture absente. Aucun témoin ne modifie le jeu actif.

La passe complète reprend **1 378 fichiers fournisseurs**. Les paramètres du lanceur restent inchangés pendant la reprise. Les références inconnues de régions stratégiques et le port extérieur détectés avant correction ont disparu. Les audits restent volontairement `FINDINGS_STATIC_ONLY` à cause des autres données énumérées ci-dessous ; ils ne sont pas transformés en validation globale du mod.

Le contrôle final de conservation a d'abord refusé un événement du plan quinquennal modifié en parallèle. L'échec reste dans `FINAL_INPUT_GUARD_FIRST_ATTEMPT.json`. `CONCURRENT_EVENT_RECONCILIATION.json` vérifie séparément la nouvelle version avec le même parseur et les mêmes fournisseurs : aucune référence littérale inconnue dans le périmètre contrôlé et aucun nouveau portail DLC. Cela ne valide pas les effets ni conclusions de la mission 39. Le résultat complet d'origine est conservé, puis sa seule tranche de dépendances est explicitement réconciliée dans `FINAL_AUDIT_RECONCILED.json`.

Les **167 fichiers de journaux** ayant changé depuis l'entrée du chantier, le nouveau journal et l'événement concurrent sont préservés et ne sont pas attribués à cette livraison. L'index et le HEAD locaux sont inchangés.

## Constats restants

| Famille | Qualification et suite |
| --- | --- |
| Deux anciennes cultures | `siberian` et `north_caucasian` n'ont plus de fournisseur canonique. **22 références** de pays/foyers et **72 groupes de population** restent concernés. La [mission 40](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/40), en Backlog et rattachée à 24, porte cette migration démographique distincte. |
| Valeurs de population concernées | 54 groupes `north_caucasian` : **591 979** ; 18 groupes `siberian` : **150 297** ; total écrit **742 276**. Ce total ne prouve pas une perte de population moteur. Aucun groupe n'est redistribué ou supprimé. |
| Pays hérités absents | Les portées optionnelles BKH, MNL, SVN et TKI proviennent d'historiques natifs et ne figurent pas parmi les propriétaires initiaux. Ne pas recréer des pays de 1836 pour faire taire un diagnostic. Vérifier les logs et la portée réelle avant décision. |
| Attributions répétées | **14 candidats** dans le mod, contre 59 écritures répétées dans le témoin natif. Treize candidats du mod portent des propriétaires différents ; un répète le même propriétaire. Ce relevé ne prouve pas 14 conflits simultanés en jeu. Les arbitrages de souveraineté relèvent du chantier historique 18. |
| Province sans attribution relevée | `xEF50C0`, en Micronésie occidentale. Le témoin natif n'a pas de candidat équivalent. L'état de départ voulu et son chargement restent à vérifier ; aucun propriétaire n'est inventé. |
| Capitales | Le candidat PLC est expliqué par `set_capital = STATE_GREATER_POLAND` dans son historique, ligne 94. Les candidats GR7 et DIO restent à vérifier dans le contexte de départ, sans changement automatique de capitale. |
| Nom dynamique | Un effet natif facultatif conserve la portée `STATE_LITHUANIA`, alors que le mod utilise Kaunas. L'effet de nommage dynamique est à adapter séparément ; le nom par défaut et la géographie actuelle restent préservés. |
| Contenu espagnol différé | Les consommateurs `STATE_STRAIT_OF_GIBRALTAR` et RSR sont recensés dans des événements différés. La consigne de laisser l'Espagne pour plus tard est conservée ; aucun contenu n'est réactivé. |

`REMAINING_FINDINGS.json` donne les entrées, fichiers, lignes et groupes concernés. La mission 40 exige une stratégie sourcée : restauration technique d'une ancienne définition vérifiée, ou migration de chaque groupe selon son contexte de **1776**. La distribution vanilla de **1836** ne constitue pas une solution automatique.

## DLC

L'installation canonique consultée est **1.15.0**. Son descripteur `dlc019_ip5.dlc` identifie **State and Revolution**, sous `ip5_content` dans les scripts. L'inventaire des dossiers non-journaux contrôlés relève **282 portails DLC**, dont 18 pour `ip5_content`, tous de vocabulaire natif connu. Le contrôle de vocabulaire ne prouve ni accessibilité, ni possession effective du DLC, ni protection de tous les consommateurs.

Les initialisations russes et polonaises natives de 1836 ne sont pas recopiées dans la partie 1776. Les données de froid déjà livrées et les mécaniques des autres missions sont préservées. Les comparaisons DLC actif/inactif et les branches réelles restent dans le protocole moteur.

## Preuves et reproduction

`BASELINE.json`, `INSTALLATION_PLAN.json`, `candidate/`, `before/`, `native/`, `CHANGES.patch`, `INSTALLATION_RECEIPT.json`, `CANDIDATE_VALIDATION.json`, `CONTROL_CASES.json`, `FINAL_VALIDATION.json` et `FINAL_SOURCE_PROTECTION.json` permettent de retracer le lot. Les constats initiaux et l'échec intermédiaire restent conservés.

Auditeur en lecture seule : `tools/compatibility/issue24_map_dlc_audit.py --output <nouveau chemin dans docs/reports/compatibility>` ; ajouter `--native` pour le témoin. Il refuse d'écraser une preuve existante. Son succès de lecture ne remplace pas le parseur moteur, une simulation ou une validation humaine.

La [mission 24](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/24) porte le bilan ; `RUNTIME_PROTOCOL.md` fournit les vérifications de jeu à effectuer. La mission 39 n'a reçu aucun changement de script ou de suivi de cette passe.
