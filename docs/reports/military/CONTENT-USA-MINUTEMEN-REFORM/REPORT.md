# CONTENT-USA-MINUTEMEN-REFORM

18 octobre 2026 — **CONTENT_USA_MINUTEMEN_REFORM_READY_FOR_RUNTIME_VALIDATION**

La victoire du journal d’indépendance propose désormais **La réorganisation des milices révolutionnaires**. Le Congrès peut engager la promulgation d’une **Milice nationale réorganisée**, ou conserver les Minutemen. Une décision permet aussi d’examiner le projet pendant la guerre. Le premier choix ouvre une procédure politique ; la loi actuelle reste en vigueur jusqu’à l’adoption effective.

**La défaite conserve le retour automatique des Minutemen aux levées paysannes.** La dernière instruction directe de l’utilisateur maintient cette exception et remplace sur ce point la règle générale et le test D du document de mission. La nouvelle promulgation est annulée si les États-Unis redeviennent sujets après la défaite, sans annuler une autre loi en cours.

Résultat : **464/464 contrôles statiques réussis**, zéro fichier protégé différent parmi **1 594**, HEAD et index inchangés. [Résultats détaillés](VALIDATION.json), [projections de scénarios](SCENARIOS.json). **Victoria 3 n’a pas été exécuté pour ce lot.** Les projections lisent les scripts réels ; elles ne prouvent ni l’exécution des événements ni la promulgation ou le rechargement natif.

## 1. Audit de l’existant

L’audit repose sur l’état local, et non uniquement sur les rapports antérieurs. [Relevé avant modification](AUDIT.json) et [empreintes initiales](BASELINE.json).

- `law_aor1776_minutemen` existe déjà dans `common/laws/00_army_model.txt`. C’est une variante de `law_national_militia`, dans le groupe **Type d’armée**, active au départ via `common/history/countries/zz_1776_usa_revolution_r2.txt`. Ses effets sont conservés.
- La milice nationale standard est masquée aux USA depuis R6 pour laisser sa place initiale aux Minutemen. Cette correction d’affichage est conservée. Le nouveau choix institutionnel devient visible aux USA après son déblocage technologique.
- `law_national_guard` appartient à **Sécurité intérieure**, comporte une institution de répression et ne constitue pas la destination de cette réforme militaire.
- La milice nationale standard utilise déjà `permanent_engineer_services`, localisée **Corps du génie / Engineer Corps**. Les USA ne la possèdent pas au départ. L’arbre du mod la place en ère 4, après `organized_military_establishments`, déjà recherchée par les USA. Aucun déblocage, niveau d’ère ou coût de recherche n’est modifié.
- Le Massachusetts possède **8 bataillons réguliers d’infanterie et 1 d’artillerie**. Le plafond standard de 5 casernes de la milice nationale serait inférieur à cette implantation. La variante réorganisée conserve donc le plafond de 25 des Minutemen.
- La base américaine reste **12 bataillons réguliers d’infanterie à mousquet, 1 d’artillerie, 15 conscrits potentiels non levés et 5 navires de la variante existante**. Formations, personnages, bâtiments et méthodes de production sont inchangés.
- L’ancien effet de fin de contenu comporte déjà le retour des Minutemen aux levées paysannes lorsque le pays est sujet. Ce bloc est préservé, ainsi que les autres conséquences de la défaite et la suppression de la ferveur.

## 2. Événement, accès et choix

Événement : `aor1776_usa_minutemen_reorganization.1`, pays USA. Titre français demandé, titre anglais **The Reorganization of the Revolutionary Militias**. Illustration existante `ep2_intellectual_writer`, icône militaire native ; aucun asset créé.

Conditions communes : loi Minutemen effectivement active, guerre d’indépendance en cours **ou** pays indépendant, et contexte compatible avec la restriction de la milice nationale concernant les chefs de bloc militaire. L’événement doit être non résolu.

Deux chemins d’accès :

1. La décision **Examiner la réorganisation des milices** ouvre le débat pendant la guerre ou après l’indépendance. Elle n’est pas prise automatiquement par l’IA au lancement.
2. Le `on_complete` du journal américain appelle le même effet d’offre après les effets de victoire existants. Il ne force aucune nouvelle loi. Une réforme ou un choix déjà enregistré empêche une seconde offre.

Aucune date du 4 juillet ou de 1783, aucune nouvelle impulsion quotidienne, mensuelle ou annuelle. L’accroche de victoire utilise la définition actuelle du journal : USA indépendants et en paix. Si une autre guerre maintient le journal ouvert, la décision reste le chemin d’accès lorsque le contexte le permet.

### « Réorganisons nos milices ! »

Le choix exige la recherche **Corps du génie**, aucune promulgation active, une légitimité d’au moins 25, une chance native de promulgation strictement positive, et aucune variante conflictuelle du système Edo. Les restrictions de pays, de statut et de bloc sont revérifiées au moment du clic.

L’effet appelle **`start_enactment = law_type:law_aor1776_reorganized_militia`**. Il ne fait aucun `activate_law`, n’accorde aucune technologie et ne remplace pas une autre promulgation. Les Minutemen conservent leurs effets pendant la procédure. À l’adoption, le système natif des lois remplace la loi du même groupe ; aucun modificateur parallèle permanent n’est ajouté.

Si la technologie ou le soutien manque, le choix reste visible mais indisponible avec une explication. Le pays peut conserver les Minutemen puis adopter ultérieurement la nouvelle organisation dans l’écran normal des lois. Le seuil de légitimité 25 est une précaution explicite du contenu, cohérente avec le seuil de confirmation présent dans les defines ; il ne prétend pas reproduire toutes les vérifications internes de l’interface.

### « Les Minutemen ont fait leurs preuves ! »

Le choix enregistre la résolution narrative, sans changer la loi, les unités, les commandants ou les bonus. La loi réorganisée ne dépend pas du drapeau de résolution : son adoption normale reste possible après recherche. Un échec ou l’annulation ultérieure de la promulgation n’impose pas non plus la réforme.

### Unicité et sauvegarde

Une variable d’attente de 45 jours empêche les demandes concurrentes pendant l’événement de 30 jours. Un choix définit une résolution sans expiration et retire l’attente. La procédure engagée relève ensuite de l’état natif de promulgation. Un événement devenu invalide peut laisser l’attente expirer, ce qui rétablit la décision si les conditions redeviennent valides. Il n’existe pas de boucle automatique de relance.

Les choix enregistrés évitent une nouvelle offre à la victoire. Une promulgation commencée pendant la guerre continue après une paix indépendante. La fin de guerre annule uniquement cette nouvelle promulgation si le pays est sujet ; le retour ancien aux levées paysannes reste appliqué lorsque les Minutemen sont encore actifs. Une autre loi déjà en cours n’est pas annulée par ce lot.

## 3. Valeurs et justification

Les valeurs ci-dessous sont les **contributions propres à chaque loi**, avant cumul avec les autres effets. Les valeurs absentes valent zéro ; les plafonds sont des ajouts au plafond natif. Un point de pourcentage n’est pas une hausse relative du même pourcentage.

| Effet | Minutemen existants | Milice réorganisée | Milice nationale standard du mod |
|---|---:|---:|---:|
| Taux de conscription ajouté | +4 points | +5 points | +5 points |
| Vitesse d’instruction | +10 % | +15 % | 0 |
| Vitesse de mobilisation | +20 % | +5 % | 0 |
| Coût des biens militaires | +5 % | +10 % | 0 |
| Plafond des casernes par État | +25 | +25 | +5 |
| Plafond des centres de conscription | +25 | +50 | +100 |
| Perte de moral | 0 | −5 % | −5 % |
| Coût administratif direct en bureaucratie | 0 | 0 | 0 |
| Résistance à l’influence / pouvoir des officiers | 0 / 0 | 0 / 0 | +50 % / −25 % |

La nouvelle organisation renforce le recrutement et l’instruction, avec un plafond de conscription intermédiaire entre les Minutemen et la loi standard. Elle garde la capacité permanente actuelle pour préserver l’implantation continentale. La réduction de perte de moral reprend la valeur standard de la milice nationale. En contrepartie, la mobilisation perd 15 points et le coût des biens militaires gagne 5 points par rapport aux Minutemen. Le coût administratif est représenté par cette dépense supplémentaire ; aucune institution ni ponction de bureaucratie fictive n’est ajoutée.

La réforme n’est pas une armée professionnelle : elle ne reçoit aucun bonus d’attaque ou de défense, de répression, de sécurité intérieure ou de salaire. Le nombre de conscrits effectivement disponible après adoption dépendra du recalcul natif, de la population et des autres plafonds. Le taux passe de 4 à 5 points pour la seule contribution de la loi ; les **15 conscrits potentiels initiaux** ne constituent pas une promesse de total fixe après réforme.

## 4. Interactions préservées

- **Liberty Or Death** reste à +15 % d’instruction, +15 % de récupération du moral, −10 % de perte de moral et −30 % de terrain perdu en défaite. Ce lot ne modifie ni ses valeurs ni sa suppression à la fin de la guerre.
- **Revolutionary Fervour** conserve ses niveaux et ses ±5 % de récupération/perte de moral. Le nettoyage existant à la paix est inchangé.
- **Aide française** : le traité garde les mêmes articles, conditions, argent, armes, instructeurs et dette. Les instructeurs donnent déjà +10 % d’instruction et d’expérience aux USA. Pour les seules contributions loi + Liberty + instructeurs, l’instruction passe de +35 % à +40 % si les trois sont actifs ; les autres effets du jeu peuvent encore intervenir.
- Pour les seules contributions loi + Liberty + ferveur, la perte de moral varie de −5 % à −15 % avec les Minutemen, et de −10 % à −20 % avec la loi réorganisée. La réforme n’ajoute aucune récupération de moral ou résistance territoriale.
- Le renforcement des conscrits peut accroître les dépenses si davantage d’hommes sont levés. Aucun montant fixe en livres n’est revendiqué sans mesure du budget et des prix en jeu. Qualifications, emplois militaires et vitesse réelle de remplissage relèvent du moteur.
- États, carte impériale, pops, compagnies françaises, technologies, commandants, économie et localisations existantes sont protégés par empreinte avant/après. Les 1 594 fichiers suivis sont identiques à l’état initial du lot.

## 5. Fondement historique et abstraction

Le National Park Service distingue la milice ordinaire du Massachusetts et les compagnies de volontaires de minute men organisées en 1774, avec des obligations d’entraînement différentes. Cette situation locale ne représente pas toutes les colonies de manière uniforme. [NPS — The Militia and Minute Men of 1775](https://www.nps.gov/mima/learn/historyculture/the-militia-and-minute-men-of-1775.htm).

La création de l’armée continentale en juin 1775 précède le début du scénario. La date du 14 juin est notamment attestée par l’histoire institutionnelle de l’armée. [U.S. Army — Celebrating Army and Signal Corps birthdays](https://www.army.mil/article/266945/celebrating_army_and_signal_corps_birthdays).

L’histoire publiée par l’AMEDD décrit les difficultés des engagements expirant fin 1776, la réorganisation pour un service de trois ans ou la durée de la guerre, ainsi que l’appel continu aux milices pendant la transition. Une réforme des cadres et du service ne signifie donc pas que les milices locales disparaissent physiquement. [U.S. Army, AMEDD — Reorganization of the Army](https://achh.army.mil/history/book-rev-medmen-medmench07/).

Les deux pages CMH initialement demandées, **The Continental Army** et **Army Branch Birthdays**, ainsi que le PDF direct, ont renvoyé un accès 403 lors de la consultation. Leurs résultats indexés ont servi de pistes, et les pages officielles accessibles ci-dessus de références consultables ; aucune lecture intégrale du livre inaccessible n’est revendiquée.

**Choix de conception** : les deux variantes de loi sont des abstractions de coordination, de recrutement et de durée du service. Ni l’événement ni ses textes ne présentent la réforme comme une abolition nationale des Minutemen à une date donnée. Le passage aux levées paysannes après défaite demeure une règle explicite de l’utilisateur, et non une conclusion historique déduite des sources.

## 6. Fichiers livrés

Fichiers de jeu créés :

- `common/laws/1776_usa_reorganized_militia.txt`
- `common/scripted_triggers/1776_usa_minutemen_reform.txt`
- `common/scripted_effects/1776_usa_minutemen_reform.txt`
- `common/decisions/1776_usa_minutemen_reform.txt`
- `events/1776_usa_minutemen_reform.txt`
- `localization/french/1776_usa_minutemen_reform_l_french.yml`
- `localization/english/1776_usa_minutemen_reform_l_english.yml`

Fichiers de jeu modifiés localement :

- `common/journal_entries/06_usa_independence_mod.txt` : un appel d’offre dans le seul `on_complete` américain. Toutes les autres entrées et les effets de défaite sont préservés.
- `common/scripted_effects/1776_usa_content_r1.txt` : annulation ciblée de la nouvelle promulgation en cas de défaite avec retour au statut de sujet. Le bloc initial Minutemen → levées paysannes et les autres effets sont inchangés.

Validation : `tools/validate_usa_minutemen_reform.py`, utilisant les validations R5/R6 existantes et des projections supplémentaires des conditions et effets réellement écrits. Les nouveaux textes FR/EN ont des clés uniques, un BOM UTF-8 et les mêmes consommateurs. L’index documentaire reçoit un lien vers ce rapport.

[Manifeste et empreintes](MANIFEST.json). Aucun staging, commit, changement de branche, écriture vanilla ou travail sur la carte.

## 7. Vérifications et limites

Les **464 contrôles statiques** incluent les régressions R6 et les contrôles de déclenchement, recherche, soutien politique, autre promulgation, conservation, victoire, défaite, paix indépendante, unicité, syntaxe, références, illustration, localisation et préservation. Les projections de variables utilisent les scripts analysés, sans exécuter le moteur. Le passage JSON d’états projetés teste uniquement la persistance des données attendues, **pas une sauvegarde Victoria 3**.

Les contrôles natifs de promulgation, notamment les délais de nouvelle tentative après un échec ou une annulation, doivent être confirmés dans le moteur. Le script utilise l’effet et le calcul de chance observés dans le vanilla local ; aucun trigger supposé « can enact » non vérifié n’a été inventé. Les contrôles explicites ne constituent pas une copie exhaustive des règles internes.

À vérifier également : affichage des variantes et options indisponibles, adoption effective, recalcul des centres et qualifications, budget, comportement de l’IA, chargement des sauvegardes et rendu de la vidéo DLC. Le rapport n’attribue aucun résultat moteur à ces points.

Le protocole complet A–F est dans [RUNTIME_VALIDATION.md](RUNTIME_VALIDATION.md). Ce lot ajoute un événement et une loi, sans nouvelle barre de journal à réécrire ; les descriptions immersives des journaux existants restent hors périmètre.
