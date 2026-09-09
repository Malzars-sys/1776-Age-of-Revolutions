# TECH6C5D — Fiche opérateur Victoria 3

## Résultat attendu de cette fiche

Cette fiche couvre uniquement les contrôles que le smoke parser/log ne peut pas prouver. À la fin, renvoyer les captures demandées, les trois lignes d’offre, les quatre scénarios de demande et les journaux de la session.

Ne modifier aucun fichier du mod pendant le test. Ne pas ajouter de consommateur aluminium et ne pas rééquilibrer les ressources.

## 0. Préparation

1. Vérifier Victoria 3 `1.13.11`.
2. Activer uniquement `1776 - Age of Revolutions Fork` depuis le dossier courant.
3. Lancer en mode debug.
4. Créer une nouvelle partie de test et une sauvegarde de base avant les technologies tardives.
5. Les commandes `fastresearch` et `fastbuild` sont confirmées par le fichier vanilla 1.13.11 `common/console_command_macros/00_macros.txt`. Elles sont des bascules : les saisir une seconde fois pour les désactiver. Ne pas utiliser `research_all_technologies` comme commande certaine : sa syntaxe n’a pas été confirmée localement.

## 1. Biens personnalisés

Dans le marché, ouvrir successivement : cuivre, aluminium, produits chimiques industriels, carburants raffinés, lubrifiants et produits pétroliers lourds.

Pour chacun, vérifier : nom localisé, icône cerf temporaire, texticon dans le texte, prix, ordres d’achat/vente et absence de clé brute. Prendre une capture du cuivre, une de l’aluminium et une vue regroupant les quatre biens de régression.

## 2. Mine de cuivre et ressources

Après `shaft_mining`, ouvrir la construction dans ces États et noter le maximum :

| Palier | État | Maximum attendu |
|---|---|---:|
| WORLD_CLASS | Katanga | 60 |
| VERY_HIGH | Utah | 48 |
| HIGH | West Country | 36 |
| MEDIUM | Svealand | 24 |
| MODEST | Götaland | 16 |
| LOW | Lowlands | 8 |
| NONE | Scania | aucune mine de cuivre |

Construire une mine de cuivre dans un État valide avec `fastbuild`. Vérifier que la limite ne peut pas être dépassée et que les cinq familles de PM sont visibles : extraction, explosifs, automatisation vapeur, transport ferroviaire et concentration du minerai.

Tester les quatre extractions et capturer leur tooltip :

| PM | Intrants | Cuivre | Emploi | Pollution |
|---|---|---:|---:|---:|
| manuel | 5 outils | 15 | 5 000 | 0 |
| atmosphérique | 10 outils + 10 charbon | 30 | 5 000 | 5 |
| condensation | 15 outils + 15 charbon | 45 | 5 000 | 15 |
| Diesel | 15 outils + 3 carburants raffinés | 55 | 5 000 | 10 |

Le Diesel ne doit afficher aucun pétrole brut.

Avant `geological_surveying`, la concentration avancée doit être verrouillée. Après recherche, elle doit consommer 5 outils et 5 produits chimiques industriels pour ajouter 10 cuivre.

Vérifier aussi : Ashio est une mine de cuivre en Kanto ; Shikoku a un potentiel cuivre mais aucune mine de plomb Besshi inventée ; le trait Copper Coast donne +10 % aux mines de cuivre et conserve +10 % aux mines de fer.

## 3. Cinq demandes cuivre

Activer chaque usage séparément et relever l’augmentation des ordres d’achat cuivre par niveau :

| Usage | Demande attendue | Contrôle supplémentaire |
|---|---:|---|
| doublage des chantiers navals | 5 | +5 clippers et option neutre disponible |
| téléphones | 15 | aucun plomb dans cette recette |
| moteurs électriques | 10 | PM toujours rentable selon le marché |
| radios | 2 | conversion des téléphones conservée |
| conducteurs cuivre des centrales | 2 | choix normal/par défaut |

Capturer le tooltip de chaque PM et le total des ordres cuivre avant/après.

## 4. Double verrou de l’aluminium

Partir de trois copies de la sauvegarde de base. Utiliser `fastresearch`, sélectionner les technologies dans l’interface et laisser le jeu valider la recherche.

| Sauvegarde | Technologies | Résultat attendu |
|---|---|---|
| A | `industrial_alkalis` oui ; `electrical_capacitors` non | usine non ferreuse indisponible |
| B | `electrical_capacitors` oui ; `industrial_alkalis` non | usine non ferreuse indisponible |
| C | les deux oui | usine et Hall-Héroult disponibles |

Pour A, B et C, faire une capture qui montre les technologies et une autre montrant la liste de construction ou le PM. Ce test est obligatoire : la documentation statique ne suffit pas.

## 5. Hall-Héroult

Dans la sauvegarde C, construire l’usine non ferreuse. Vérifier : nom français/anglais selon la langue testée, icône cerf, 5 000 emplois, pollution 20 et recette par niveau :

`20 produits chimiques industriels + 10 charbon + 50 électricité -> 40 aluminium`.

Vérifier que les quatre modificateurs d’intrant/sortie aluminium fonctionnent et qu’aucune clé brute ne s’affiche.

## 6. Avions entièrement métalliques

Vérifier le PM sous combinaisons technologiques partielles : il ne doit être disponible qu’avec `military_aviation`, `electrical_capacitors` et `industrial_alkalis` ensemble.

Sur une industrie automobile, comparer l’ancien PM et le nouveau. Le nouveau doit afficher : 10 aluminium, −10 automobiles, +20 avions et +500 ingénieurs ; aucun bois dur ni tissu. Basculer aller/retour et confirmer que l’emploi reste possible et que l’ancien PM demeure sélectionnable.

## 7. Conducteurs des centrales

Sur un groupe de centrales stable :

1. noter production électrique, emploi, rentabilité et ordres cuivre avec les conducteurs cuivre ;
2. basculer vers les conducteurs aluminium ;
3. attendre la mise à jour du marché ;
4. vérifier que 2 cuivre sont remplacés par 1 aluminium par niveau ;
5. confirmer qu’aucun niveau ne consomme les deux métaux et que production électrique/emploi ne changent pas à cause du PMG conducteur.

## 8. Choix IA

Le moteur 1.13.11 note les PM selon profit, déficit, valeur produite, emploi, pénalité des intrants chers et inertie. Les deux PM conducteurs ont le poids par défaut ; l’IA ne reçoit aucun ordre forcé d’utiliser l’aluminium. La chance de considérer un changement est de 10 % à chaque évaluation, donc observer plusieurs mois et noter la durée.

Tester si possible deux marchés comparables :

- cuivre bon marché et aluminium cher, notamment aluminium au-dessus de 100 si cuivre reste à 50 ;
- cuivre cher et aluminium bon marché.

Pour chaque cas, fournir les deux prix au départ, le PM choisi par l’IA, le nombre de centrales observées et le délai. Un seul non-changement immédiat ne prouve pas un échec.

## 9. Offre et demande aluminium

Construire environ 10, 25 puis 50 niveaux d’usine. Après stabilisation, compléter les lignes `SUPPLY_10`, `SUPPLY_25` et `SUPPLY_50` de `TECH6C5D_ECONOMIC_OBSERVATIONS.csv`.

| Niveaux | Vente brute attendue |
|---:|---:|
| 10 | 400 |
| 25 | 1 000 |
| 50 | 2 000 |

À chaque palier relever : vente aluminium, achat aluminium, solde, multiplicateur de prix, emploi, solde financier du bâtiment, prix des produits chimiques industriels, de l’électricité et du charbon.

Tester ensuite les quatre profils : économie paisible, économie électrifiée avec conducteurs aluminium, aviation militaire, économie tardive mixte. Un prix bas causé uniquement par la paix ou une surconstruction volontaire n’est pas une preuve qu’un troisième consommateur est nécessaire.

## 10. Demande cuivre après substitution

Avant puis après la bascule d’un nombre connu de centrales vers l’aluminium, relever les ordres cuivre. La baisse théorique est `2 × niveaux basculés`. Vérifier que chantiers navals, téléphones, moteurs électriques et radios gardent leurs demandes.

## 11. Clôture et retour à fournir

Quitter normalement après les mesures. Envoyer :

1. les captures demandées dans les sections 1 à 8 ;
2. le fichier `TECH6C5D_ECONOMIC_OBSERVATIONS.csv` complété ;
3. `error.log`, `game.log` et, si présents, `warning.log` et `debug.log` ;
4. la langue utilisée, le pays testé, la date en jeu, le nombre de semaines/mois de stabilisation et la liste exacte des autres mods actifs — attendue vide.

La décision finale sera alors : `PASS`, `REVIEW REQUIRED` ou `FAIL`. En attendant, le statut correct reste `USER_RUNTIME_REQUIRED`.
