# Mission 52 — précision des coûts de fortification

10 novembre 2026 — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**.
Issue : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/52

## Correction installée

Le journal actuel du joueur rejette trois nombres de
`common/static_modifiers/1776_land_fortification_construction.txt` avec
`Malformed token`. La capture complète est conservée dans
`OBSERVED_ERROR_LOG.txt` ; les quatre diagnostics pertinents et l'empreinte de
la capture figurent dans `BASELINE.json`. Aucun journal n'a été effacé et le
jeu n'a pas été lancé par cette mission.

Seuls les trois littéraux rejetés changent dans ce fichier :

| Coefficient | Avant | Après |
| --- | ---: | ---: |
| Un niveau déjà construit | −0,181818 | **−0,1818** |
| Deux niveaux déjà construits | −0,307692 | **−0,3077** |
| Quatre niveaux déjà construits | −0,470588 | **−0,4706** |

Le troisième palier reste −0,4. Tous les autres octets du fichier, ses IDs,
icônes, BOM et fins de ligne sont préservés. Aucun script de sélection,
callback, PM, emploi, technologie, fort naval ou limite de niveau n'est modifié.
La constante de base demeure **900 points**.

La référence canonique 1.15.0 contient un exemple de modificateur statique à
quatre décimales dans `00_code_static_modifiers.txt` :
`state_trade_advantage_from_capacity_add = 0.0005`. Les nouveaux coefficients
sont les arrondis à quatre décimales les plus proches des fractions idéales
du barème. Cela fournit un format de référence compatible ; seule une lecture
par le moteur après redémarrage confirmera la disparition des diagnostics.
Le rapport n'infère pas la précision maximale interne du moteur.

## Écart théorique du barème

Hypothèse : aucun autre bonus ou malus et calcul décimal de
`900 / (1 + coefficient)`. Ce sont des points de construction effectifs,
pas une mesure en jeu du budget, du temps réel ou des salaires.

| Niveau à construire | Cible | Équivalent après arrondi | Écart en points |
| --- | ---: | ---: | ---: |
| 1 | 900 | 900 | 0 |
| 2 | 1 100 | 1 099,97556 | −0,02444 |
| 3 | 1 300 | 1 300,01444 | +0,01444 |
| 4 | 1 500 | 1 500 | 0 |
| 5 | 1 700 | 1 700,03778 | +0,03778 |

Maximum absolu : **moins de 0,04 point par palier**. Somme des cinq extensions
successives : environ **6 500,02778 points**, contre la cible de 6 500.
Les autres bonus, le plancher natif et l'arithmétique fixe du moteur peuvent
modifier le résultat effectif ; la borne du tableau vaut pour le cas neutre.
Le coût requis affiché reste 900 : le barème agit par efficacité de construction.

## Vérifications

- **20/20 contrôles candidats et 20/20 installés**.
- **54 projections de l'AST réel** : niveaux construits 0 à 5, trois PM et
  trois taux d'effectif. Les choix de palier restent corrects, indépendants
  des PM/effectifs ; le niveau déjà au plafond conserve son dernier palier
  sans autorisation d'un sixième niveau.
- **Trois contrôles de régression en mémoire détectés** : retour des anciens
  littéraux, changement du coefficient exact du niveau 3, changement du bonus
  alimentaire japonais. Aucun contrôle n'est installé dans le jeu.
- **Six contrôles de protection** : deux fichiers exactement conformes aux
  candidats, aucun ajout/suppression de runtime, sources canoniques et HEAD/index
  inchangés, autres fichiers du système de fortification inchangés.
- **2 532 sources préexistantes capturées**. Une modification concurrente du
  journal marocain `06_morocco_lands_of_anarchy.txt` a été observée hors
  manifeste, capturée et préservée. Elle n'est pas attribuée à cette mission.

L'outil neuf réutilise la classe de projection de
`validate_land_fortification_construction.py`, sans lancer son ancien `main`
qui écrirait dans les preuves d'octobre. Le contrat ancien visant un écart
inférieur à 0,01 point et ses résultats restent historiques : il ne tient pas
compte des littéraux désormais rejetés par le moteur. Le nouveau contrat
chiffré accepte l'arrondi de format et exige moins de 0,05 point dans le cas
neutre ; il ne supprime aucun échec pour prétendre reproduire l'ancien contrat.

## Suivi d'encodage de la mission 49

Le même journal signalait que mon nouveau fichier
`common/static_modifiers/1776_japan_famine_choices.txt` n'avait pas le BOM UTF-8
attendu. Le seul changement dans ce second fichier est l'ajout des trois octets
`EF BB BF`. Le contenu décodé est identique : aucun bonus, coût, durée, drapeau
ou choix n'est changé. Ce suivi est enregistré sur l'issue 49 ; il ne constitue
pas une réécriture japonaise dans la mission 52. Les anciens manifestes de 49
restent les preuves de sa première livraison, avec ce suivi explicite de hash.

## Reproduction et prochaine vérification

Preuves : `before/`, `candidate/`, `diff/`, `CANDIDATE_MANIFEST.json`, les deux
validations, `NEUTRAL_COSTS.json`, `INSTALLATION_RECEIPT.json` et
`SOURCE_PROTECTION.json`.

```powershell
python -B tools/compatibility/issue52_fort_precision_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE52_FORT_NUMERIC_PRECISION_2026_11_10/RECHECK_NEW_TIMESTAMP.json
```

Choisir un nouveau nom : le validateur refuse l'écrasement d'une preuve et ne
modifie pas les scripts. Suivre `RUNTIME_PROTOCOL.md` pour le contrôle moteur.
Aucune validation humaine, publication, écriture Git ou modification vanilla
n'est revendiquée. L'issue reste ouverte pour revue. La colonne Project ne peut
pas être modifiée directement avec les outils disponibles ; In review est le
statut demandé, sans attestation d'une mutation réelle de cette colonne.
