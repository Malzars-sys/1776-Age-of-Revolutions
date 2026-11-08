# Mission 29 — articles de péage, 8 novembre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Correctif installé dans le mod local régulier, sans opération Git d’écriture ni modification du vanilla. La mission reste ouverte ; aucune validation moteur n’est revendiquée.

## Mission retenue et concurrence

Le mainteneur a demandé de choisir une autre mission du tableau, de laisser la **32** à l’autre agent et de classer la **28** comme faite. Le tableau GitHub a été mis à jour : **28 → Done**, **29 → In progress**. Le passage de la 28 en Done a également fermé son issue via le workflow du projet. Cette instruction de clôture n’apporte pas de détails supplémentaires sur ses essais moteur.

La 29 était disponible, sans assignataire. Elle porte sur les deux articles `toll_exemption` et `no_tolls`, dans `common/treaty_articles/31_toll_exemption.txt` et `32_no_tolls.txt`. Les fichiers d’objectifs de guerre de la mission 32 ne sont pas modifiés par cette livraison. Leur état déjà modifié a été conservé dans la baseline, comme les autres travaux concurrents.

## Référence effectivement consultée

- Vanilla canonique, en lecture seule : `C:/Games/Victoria 3/game` ; exécutable **1.15.0**. Le journal système existant identifie le build `6338547985` ; il ne constitue pas une exécution après correctif.
- Deux articles natifs de même nom : blocs `visible`, `possible` et `ai`.
- `common/treaty_articles/treaty_articles.md`, notamment les scopes de visibilité/possibilité et les sections de calcul IA.
- `common/defines/00_defines.txt` : `STRAIT_GRIEVANCE_MIN_DEPENDENCE = 5`.
- Localisations natives FR/EN de `DIPLOMATIC_ACCEPTANCE_STRAIT_DEPENDENCE` et `DIPLOMATIC_ACCEPTANCE_NO_STRAIT_DEPENDENCE` : présentes, sans fichier homonyme du mod masquant `diplomacy_l_*`. Aucune nouvelle clé de localisation nécessaire.

Les copies d’entrée et leurs empreintes figurent dans `inputs/` et `BASELINE.json`.

## Diagnostic et correction bornée

Les huit anciens liens alimentaient une formule quadratique divisée par le PIB. Le vanilla utilise désormais une dépendance commerciale de 0 à 100, un seuil et des griefs de péage. Une substitution du seul nom de lien aurait conservé une formule et des échelles erronées.

La comparaison a également révélé un blocage préalable : dans `visible` et `possible`, `scope:source_country` n’existe pas. Le contrat natif précise que `root` est déjà la source prospective d’un article dirigé. Les logs antérieurs comportent des erreurs de type aux six sites concernés ; leur extrait est conservé dans `LOG_BEFORE_EXCERPT.txt`. Les deux blocs sont donc remplacés par leurs versions natives : possession d’une province de détroit dans la hiérarchie et contrôle du détroit, exprimés avec `yes` sur le pays courant.

Seuls les trois blocs `visible`, `possible` et `ai` changent dans chaque fichier. Les blocs IA reprennent exactement leur AST natif, y compris les griefs et préférences de libre-échange nécessaires à une proposition cohérente. Les autres octets, le BOM et les fins de ligne du mod sont conservés.

### Correspondance des huit expressions

Notations : **S** est `source_country`, le contrôleur ; **T** est `target_country`, le bénéficiaire. **D(T,S)** désigne exactement `scope:target_country` → `strait_trade_dependence_by(scope:source_country)` ; **D(S,T)** est la dépendance inverse. Les lignes indiquées ci-dessous sont celles des entrées sauvegardées avant intervention.

| Article et anciens sites | Sens du remplacement |
| --- | --- |
| Exemption, lignes 133 et 139, évaluateur S | Les deux occurrences de la même importance commerciale ne sont plus multipliées entre elles. La réticence combine **0,5 × D(T,S) + 0,5 × D(S,T)**, multiplie par **−0,25** et applique un plancher de **−25**, auquel s’ajoute la réticence de base **−10**. |
| Exemption, lignes 163 et 169, évaluateur T | Le couple numérateur/multiplicateur devient un test **D(T,S) < 5**, donnant **−10** sans dépendance suffisante ; sinon **0,25 × D(T,S)**, plafonné à **25**. |
| Aucun péage, lignes 131 et 137, évaluateur S | Les deux anciennes occurrences deviennent une seule mesure **D(T,S)**, multipliée par **−0,5**, avec plancher **−50**, plus la base **−10**. La dépendance inverse n’intervient pas dans cet article natif. |
| Aucun péage, lignes 161 et 167, évaluateur T | Test **D(T,S) < 5** : **−10** ; sinon **0,15 × D(T,S)**, plafonné à **15**. |

Les scopes temporaires `actor`/`target` sont ceux du natif dans chacune des deux orientations. La base −10 de l’ancien bénéficiaire ne subsiste pas en plus du bonus lorsque sa dépendance atteint le seuil : le nouveau branchement natif la remplace.

### Griefs et libre-échange

- La chance d’examen conserve son facteur de rang et ajoute le grief de péage le plus élevé × 0,005, pour l’article correspondant à la politique commerciale du pays.
- Le poids d’une proposition vaut 1 + grief envers S × 0,04. Lorsqu’il est le bénéficiaire, un pays libre-échangiste privilégie l’absence générale de péages ; les autres privilégient leur exemption personnelle.
- Le poids IA de poursuite de l’article comme objectif vaut zéro sans grief positif ou sans la préférence commerciale correspondante ; sinon 1 + grief × 0,15.
- `toll_exemption` conserve l’usage IA `request` et `offer` ; `no_tolls` conserve `request` seulement.

Ce dernier point concerne **le choix IA des deux articles**. Le bloc `wargoal` de chaque article, les trois fichiers `common/war_goal_types/` de la mission 32 et les guerres initiales sont intégralement préservés.

## Préservation

Les deux articles gardent leurs identifiants `REPLACE_OR_CREATE`, le prérequis de 1776 `commercial_insurance_markets`, leurs coûts 10/25, les bénéficiaires des coûts et de l’implication, leurs drapeaux et icônes, les interdictions de doublon, les effets de ratification/retrait/rupture et les calculs de manœuvres/infamie existants. Le prérequis natif `international_relations` et son drapeau supplémentaire `show_in_lens` ne sont pas importés. Aucune carte, ressource, loi initiale ou technologie de pays ne change.

## Contrôles réellement exécutés

Commande, avec le Python du runtime disponible dans la session :

```text
python -B tools/compatibility/issue29_toll_treaties_audit.py --candidate
python -B tools/compatibility/issue29_toll_treaties_audit.py
```

- **86/86 contrôles statiques** sur la proposition puis sur les deux fichiers installés.
- **10 contrôles négatifs détectés**, dont les deux baselines anciennes, un lien réintroduit, un sens de dépendance inversé, un signe, un seuil, un scope de visibilité invalide, une modification de prérequis, une modification du bloc de guerre et une inversion de préférence libre-échangiste.
- AST natif exact dans les trois blocs autorisés ; octets hors blocs inchangés.
- **2 482 autres fichiers de scripts/données vérifiés par empreinte**, sans changement observé pendant cette exécution.
- Zéro ancien `strait_trade_importance_by` dans ces deux articles.

Le petit évaluateur exerce les formules des scripts sur des données synthétiques, avec les deux sens d’évaluation, des dépendances 0/4,99/5/20/100 et des préférences commerciales opposées. Il ne calcule pas l’acceptation diplomatique finale et ne simule ni routes commerciales ni économie. À titre de témoin arithmétique, avec D(T,S)=20 et D(S,T)=60 :

| Contribution propre à l’article | Exemption | Aucun péage |
| --- | ---: | ---: |
| Évaluateur S, base incluse | −20 | −20 |
| Évaluateur T | +5 | +3 |
| Évaluateur T avec D(T,S)=4,99 | −10 | −10 |

L’audit ne modifie aucun fichier. Le contrôle initial du candidat a révélé un défaut de son évaluateur de test : un `value = 0` conditionnel devait remplacer l’accumulateur courant. Cet évaluateur a été corrigé avant installation ; aucun ajustement des scripts natifs n’a été fait pour faire passer les tests.

## État de livraison et limites

`INSTALLATION.json`, `CHANGES.patch`, `CANDIDATE_VALIDATION.json` et `VALIDATION.json` décrivent l’installation exacte. Aucun commit, push, changement de branche, merge ni publication de ces fichiers n’a été effectué. Le `supported_version` hérité du descripteur n’a pas été modifié dans cette mission.

**À faire en jeu :** vérifier la visibilité des articles avec les technologies requises, les deux orientations d’exemption, la demande d’absence générale de péages, les branches de libre-échange, les effets réels sur les détroits et la persistance après sauvegarde/rechargement. Le protocole est dans `RUNTIME_PROTOCOL.md`. Les logs après correctif et la validation humaine restent à obtenir avant Done.
