# TECH6C5D — Validation runtime et économique cuivre + aluminium

> **Addendum de clôture opérateur — 9 septembre 2026.** L’opérateur a exécuté la fiche manuelle et déclaré les contrôles fonctionnels **PASS**. Le test de sélection des méthodes de production par l’IA est transféré à la bêta joueurs et n’est plus bloquant pour TECH6C5. Les mesures numériques aux jalons 10/25/50 ans et les temps de réaction IA n’ayant pas été transmis, aucune valeur n’est inventée. **Statut final de TECH6C5 : FROZEN.**

## 1. TECH6C5D RESULT

**TECH6C5D RESULT: USER_RUNTIME_REQUIRED**

La validation statique et le smoke parser/log sont propres pour le périmètre cuivre/aluminium. Les comportements interactifs, les portes technologiques réellement observées, le choix des PM par l’IA et les mesures économiques doivent encore être exécutés par l’opérateur dans une partie complète. Aucun PASS runtime n’est fabriqué.

## 2. Validation statique

| Contrôle | Résultat |
|---|---|
| `tools/tech6c5b_validate.py` | PASS — 675 États, 302 potentiels non nuls, total 5 924, 285 technologies, zéro cycle, zéro nouvelle technologie cuivre |
| `tools/tech6c5c_validate.py` | PASS — 285 technologies, zéro cycle, zéro nouvelle technologie aluminium, zéro changement de carte imputable à 5C |
| `git diff --check` | PASS — code retour 0 ; avertissements LF/CRLF informatifs seulement |
| branche | PASS — `tech6c-goods-buildings-pm-implementation` |

Les définitions des deux biens, les quatre modificateurs de chacun, les texticons, les localisations EN/FR, les références PM/PMG/bâtiments, les verrous technologiques, les accolades et les clés `goods_input/output` sont couvertes par les validateurs 5B/5C et le validateur consolidé 5D.

## 3. Résultat du démarrage

**STARTUP/PARSER SMOKE: PASS_LIMITED.**

- Victoria 3 : `1.13.11`, branche vanilla `release/1.13.11`.
- Mod actif confirmé dans `content_load.json` : dossier courant `1776_Age_of_Revolutions_fork`.
- Lancement direct : `victoria3.exe -gdpr-compliant -debug_mode -mod=".../descriptor.mod"`.
- Fenêtre de smoke : environ 40 secondes.
- Le chargement a atteint la localisation, l’initialisation des textures et l’analyse GUI.
- Le processus créé a été arrêté ; un processus enfant transitoire a disparu ; aucun `victoria3.exe` ne reste actif.
- `game.log` est resté vide au moment de l’arrêt forcé : le smoke ne prouve ni l’arrivée au menu, ni l’ouverture d’une partie.

Manifestes frais :

| Journal | Taille | SHA-256 |
|---|---:|---|
| `error.log` | 159 707 | `D2F830E9F1025950BEC9DD37D65EF98BB94B4D21378B7E09FCECF26A77FACFFF` |
| `game.log` | 0 | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |
| `warning.log` | 6 234 | `9541C988EB9B1604B09425B37CB491189166A77E5C52AC6D5999ED25BBE57FBA` |
| `debug.log` | 18 465 | `F9479A17819251664DC8B6FADE4AF4CADA4BC4994B9D8A9E5FDA99F9BA3C4299` |

## 4. Nouvelles erreurs TECH6C dans les journaux

**NEW_TECH6C_ERROR = 0.**

Le scan frais de `error.log`, `warning.log`, `debug.log` et `game.log` ne trouve aucune occurrence des identifiants cuivre/aluminium ou des quatre biens de régression, et aucun diagnostic générique de bien, bâtiment, PM, PMG, modificateur, texture ou parsing invalide.

Constats hors périmètre :

- `PRE_EXISTING_ERROR` — métadonnée « Age of revolution /Fork » annoncée en 1.13.9 face au jeu 1.13.11 ; déjà documentée dans les smokes antérieurs ; le `descriptor.mod` courant accepte `1.13.*`.
- `PRE_EXISTING_ERROR` — doublons de localisation historiques, notamment objectifs et technologies.
- `WARNING_ONLY` — collisions de noms de données globales du moteur.
- `PRE_EXISTING_ERROR` — trois textes GUI non localisés dans `custom_tooltip.gui`, `map_markers.gui` et `military_formation_panel.gui`, déjà documentés hors TECH6C.

Aucun nettoyage large n’a été tenté.

## 5. Runtime cuivre

### Mine

Statique : bâtiment unique, verrou `shaft_mining`, cinq PMG résolus, quatre extractions exactes, Diesel sur `refined_fuels` et non pétrole, états par défaut présents. **Runtime/UI : USER_RUNTIME_REQUIRED.**

### Ressources

La matrice et les fichiers de carte correspondent statiquement sur les 675 États. Échantillon préparé : Katanga 60, Utah 48, West Country 36, Svealand 24, Götaland 16, Lowlands 8, Scania 0. Ashio est migré vers la mine de cuivre ; Shikoku reçoit son potentiel sans mine Besshi artificielle ; Copper Coast donne +10 % au cuivre et conserve +10 % au fer. **Caps visibles en jeu : USER_RUNTIME_REQUIRED.**

### PM et cinq consommateurs

Les recettes attendues sont résolues statiquement : doublage 5, téléphones 15, moteurs électriques 10, radios 2, conducteurs cuivre 2. Les effets sur ordres de marché, rentabilité et choix viables doivent être relevés dans la fiche opérateur.

## 6. Runtime aluminium

Statique : bien unique, coût 80, usine non ferreuse unique, Hall-Héroult à `20 industrial_chemicals + 10 coal + 50 electricity -> 40 aluminium`, 5 000 emplois et pollution 20. Le bâtiment et le PM listent tous deux `electrical_capacitors` et `industrial_alkalis`.

**Bien, bâtiment, modificateurs et double verrou réellement visibles : USER_RUNTIME_REQUIRED.** Les cas A/B/C sont obligatoires.

## 7. Runtime avions

`pm_all_metal_aircraft` exige statiquement les trois technologies et applique `10 aluminium`, `-10 automobiles`, `+20 aeroplanes`, `+500 engineers`, sans bois dur ni tissu. L’ancien PM reste défini. Disponibilité partielle/complète, bascule et état d’emploi : **USER_RUNTIME_REQUIRED**.

## 8. Runtime conducteurs

Le PMG est rattaché à la centrale et contient exactement les choix cuivre puis aluminium. Les méthodes demandent respectivement 2 cuivre et 1 aluminium, sans effet d’emploi ni de production électrique. Exclusivité réelle des intrants et bascule UI : **USER_RUNTIME_REQUIRED**.

## 9. Choix des PM par l’IA

Victoria 3 1.13.11 utilise un score moteur fondé notamment sur le profit, le déficit, la valeur produite, l’emploi, les pénalités d’intrants chers et l’inertie de changement (`common/defines/00_ai.txt`, lignes 968–986). La documentation PM donne `ai_weight = 1.0` par défaut ; aucun `ai_weight` particulier n’est défini sur les deux conducteurs.

Conclusion statique : l’aluminium n’est pas forcé ; l’économie du marché participe au choix. Le moteur ne considère un changement qu’avec une chance de 10 % à chaque évaluation. Les scénarios cuivre bon marché/aluminium cher et inversement restent **USER_RUNTIME_REQUIRED**.

## 10. Impact sur la demande cuivre

Aucune mesure runtime n’est disponible. Théoriquement, chaque niveau de centrale basculé retire 2 ordres cuivre, tandis que doublage naval, téléphones, moteurs électriques et radios restent intacts. L’effondrement structurel n’est pas démontré : **USER_RUNTIME_REQUIRED**.

## 11. Observations économiques aluminium

| Usines | Vente brute calculée | Vente observée | Prix | Emploi | Solde bâtiment |
|---:|---:|---|---|---|---|
| 10 | 400 | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED |
| 25 | 1 000 | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED |
| 50 | 2 000 | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED | USER_RUNTIME_REQUIRED |

L’électricité représente 57,7 % de la valeur de base des intrants Hall-Héroult. Une pression sur son prix peut être un comportement voulu et ne suffit pas à conclure à un défaut.

## 12. Suffisance de la demande aluminium

Le modèle statique reste plausible avec deux consommateurs : aviation à 10 par niveau concerné et conducteurs à 1 par niveau de centrale. Les profils paisible, électrifié, aviation militaire et mixte doivent trancher. **Aucune preuve actuelle d’insuffisance structurelle.**

## 13. Consommateur supplémentaire

**ADDITIONAL CONSUMER: NOT_NEEDED (provisoire).**

Ni automobile de masse ni matériel ferroviaire n’est recommandé ou implémenté sans preuve runtime chiffrée d’un effondrement durable.

## 14. Fichiers gameplay modifiés pendant TECH6C5D

**0.**

## 15. Fichiers et rapports créés

- `docs/reports/industry/TECH6C5D_COPPER_ALUMINIUM_RUNTIME_QA.md`
- `docs/reports/industry/TECH6C5D_RUNTIME_TEST_MATRIX.csv`
- `docs/reports/industry/TECH6C5D_ECONOMIC_OBSERVATIONS.csv`
- `docs/reports/industry/TECH6C5D_USER_RUNTIME_CHECKLIST.md`
- `tools/tech6c5d_validate.py`

## 16. Contrôles USER_RUNTIME_REQUIRED restants

Visibilité/localisation/texticons des six biens ; mine et caps ; tous les sélecteurs PM ; cinq demandes cuivre ; trois cas du double verrou ; Hall-Héroult ; avion tout métal ; exclusivité des conducteurs ; choix IA sous deux marchés ; demande cuivre avant/après ; mesures aluminium à 10/25/50 niveaux et quatre profils de demande ; journaux après fermeture normale.

## 17. Recommandation

**FREEZE TECH6C5 — seulement après un passage opérateur sans défaut mécanique et avec observations économiques acceptables.**

Aucun correctif ciblé ni changement de balance n’est justifié à ce stade. Les modifications ne sont ni commitées ni poussées.
