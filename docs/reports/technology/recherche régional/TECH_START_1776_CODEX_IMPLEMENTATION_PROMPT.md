# Prompt Codex — Implémentation mondiale des technologies de départ 1776

Tu travailles dans le dépôt LOCAL :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Branche actuelle :

`tech6c-goods-buildings-pm-implementation`

Référence vanilla :

`C:\Games\Victoria 3\game`

Version cible :

Victoria 3 1.13.11

Date historique absolue :

**1776-01-01**

## IMPORTANT

- Le working tree LOCAL fait autorité.
- TECH6D est validé.
- TECH7A Infrastructures régionales est COMPLETE / RUNTIME PASS.
- Ne modifie ni TECH6D ni TECH7A.
- Ne modifie pas l’arbre technologique, les eras, les prérequis, les PM, les goods ou les bâtiments.
- Ne commit pas.
- Ne push pas.
- Ne crée pas de PR.
- Aucun reset / restore / checkout destructif.
- Préserve tous les changements locaux préexistants.

## FICHIERS D’AUTORITÉ

Cette phase ne demande PLUS de recherche historique.

Utilise comme autorité :

1. `docs/reports/technology/TECH_START_1776_AUDIT.md`
2. `docs/reports/technology/TECH_START_1776_COUNTRIES.csv`
3. `docs/reports/technology/TECH_START_1776_TECHNOLOGIES.csv`
4. `docs/reports/technology/TECH_START_1776_WORLD_SYNTHESIS.md`
5. `docs/reports/technology/TECH_START_1776_WORLD_MATRIX.csv`
6. `docs/reports/technology/TECH_START_1776_WORLD_COUNTRY_PLAN.csv`
7. `docs/reports/technology/TECH_START_1776_WORLD_PREREQUISITE_DEBT.csv`

Les 9 recherches régionales restent des pièces justificatives, mais
`TECH_START_1776_WORLD_COUNTRY_PLAN.csv` est l’autorité CANONIQUE pour le résultat final par TAG.

## OBJECTIF

Implémenter exactement la distribution technologique mondiale synthétisée pour les **474 TAG**.

Le résultat effectif final d’un TAG doit correspondre EXACTEMENT à la colonne :

`Final_Technologies`

de `TECH_START_1776_WORLD_COUNTRY_PLAN.csv`.

Ne réinterprète pas les décisions historiques.

---

## 1 — RÈGLE DE SYNTHÈSE DÉJÀ TRANCHÉE

Les anciens `REVIEW` régionaux ont déjà été résolus de façon conservatrice :

- technologie actuellement présente + REVIEW → elle RESTE ;
- technologie actuellement absente + REVIEW → elle RESTE ABSENTE.

Ne rouvre pas ces arbitrages.

La synthèse finale applique donc uniquement un état effectif déterministe.

Statistiques de référence :

- 474 TAG ;
- 311 TAG changent effectivement ;
- 373 relations ADD ;
- 651 relations REMOVE ;
- 808 REVIEW résolus en no-change ;
- relations technologiques totales : 3421 → 3143.

---

## 2 — STRATÉGIES PAR PAYS

La colonne `Synthesis_Strategy` du COUNTRY PLAN détermine la méthode.

### A. KEEP_TIER_AND_PATCH

Nombre attendu : **283 TAG**.

Procédure :

1. conserver l’appel actuel `effect_starting_technology_tier_*_tech = yes`;
2. conserver les grants explicites qui ne sont pas retirés ;
3. supprimer uniquement les technologies indiquées dans `Explicit_REMOVEs`;
4. ajouter chaque technologie de `ADD_Technologies` via le mécanisme local existant ;
5. ne toucher à aucune relation REVIEW.

IMPORTANT :
pour cette stratégie, `Tier_Derived_REMOVEs` doit être vide.
Si ce n’est pas le cas, STOP et rapporte une divergence entre le CSV et le working tree.

### B. EXPLICIT_SETUP

Nombre attendu : **186 TAG**.

Ces pays ont au moins une technologie issue du tier qui doit disparaître.

Procédure :

1. retirer / neutraliser TOUS les appels de tier technologique qui s’appliquent à ce TAG ;
2. ne supprimer aucun autre contenu historique du pays ;
3. accorder explicitement et UNE SEULE FOIS chaque technologie listée dans `Final_Technologies`;
4. ne rien ajouter d’autre ;
5. ne pas compléter les prérequis.

Le set effectif doit être exactement égal à `Final_Technologies`.

### C. CHANGE_TIER_AND_PATCH

Nombre attendu : **2 TAG** :

- BEL : `tier_1 → tier_4`
- SPC : `tier_3 → tier_4`

Procédure :

1. remplacer l’effet de tier actuel par `effect_starting_technology_tier_4_tech = yes`;
2. retirer les anciens grants explicites qui ne doivent plus subsister ;
3. ajouter exactement la colonne `Post_Tier_Change_Explicit_Adds`;
4. vérifier que `Post_Tier_Change_Tier_Removals` est vide ;
5. reconstruire le set effectif et le comparer à `Final_Technologies`.

Ne transforme pas BEL ou SPC en setup explicite complet si le passage à tier_4 + patch suffit.

### D. KEEP_CURRENT_RESEARCH_GAP

Nombre attendu : **3 TAG** :

- GAL — Galicia-Lodomeria
- MLT — Malta
- PPU — Papua

Ne modifie AUCUNE technologie de ces trois TAG dans cette passe.

Leur absence des recherches régionales est documentée dans la synthèse.

---

## 3 — CAS BHV ET ORG

Deux TAG possèdent actuellement plusieurs fichiers historiques actifs :

### BHV — Bhavnagar
Le global audit identifie deux sources actives et un effet cumulé `tier_4;tier_5`.

### ORG — Oregon
Deux sources actives produisent `tier_2;tier_4`.

Les deux sont `EXPLICIT_SETUP`.

Procédure obligatoire :

1. trouver les deux fichiers actifs de chaque TAG ;
2. auditer uniquement les blocs technologiques ;
3. supprimer / neutraliser les effets de tier technologique dans TOUS les fichiers qui les accordent ;
4. choisir un seul emplacement canonique pour les `add_technology_researched` finaux ;
5. y écrire exactement `Final_Technologies`;
6. préserver intégralement lois, politiques, personnages, variables, relations diplomatiques et tout autre contenu non technologique des fichiers doublons ;
7. ne supprime pas un fichier entier simplement parce qu’il partage le même TAG.

Rapporte précisément la méthode retenue.

---

## 4 — ANACHRONISMES P0 / C-D

Le résultat final doit impérativement vérifier :

- `railways` : aucun pays au départ ;
- `joint_stock_companies` : aucun pays au départ ;
- `romanticism` : aucun pays au départ.

Cas connus :

- BRA : REMOVE `railways`
- DEI : REMOVE `joint_stock_companies`
- AUS, CUB, FRA, GBR, GR5, PRU, USA : REMOVE `romanticism`

Après implémentation, AUCUNE technologie classée C ou D
dans `TECH_START_1776_TECHNOLOGIES.csv`
ne doit être présente dans le set de départ d’un TAG.

---

## 5 — TECHNOLOGIES FRONTIÈRE : DISTRIBUTION FINALE DE CONTRÔLE

Les sets finaux calculés par la synthèse donnent notamment :

### coke_smelting
Doit rester uniquement :
`GBR`

### precision_boring
Doit rester uniquement :
`GBR`

### mechanized_spinning
Doit rester uniquement :
`GBR`

### industrial_canals
Doit être présent uniquement chez :
`FRA;GBR;NET`

### atmospheric_engine
Doit être présent chez :
`AUS;BEL;BEO;FRA;GBR;SPC`

Ces listes servent de smoke tests, mais le COUNTRY PLAN reste l’autorité complète.

---

## 6 — PRÉREQUIS : NE PAS AUTO-RÉPARER

Le jeu accepte actuellement des enfants sans certains parents.

La recherche historique a volontairement conservé plusieurs de ces asymétries.

Après synthèse, le fichier :

`TECH_START_1776_WORLD_PREREQUISITE_DEBT.csv`

contient **434** relations avec prérequis directs manquants.

Règle absolue :

**NE JAMAIS ajouter automatiquement une technologie uniquement parce qu’elle est le prérequis d’une autre.**

Parents manquants les plus fréquents attendus :

- `institutionalized_scientific_exchange` : 248
- `periodical_print_networks` : 243
- `scientific_fortification_siegecraft` : 125
- `regulated_small_arms` : 22
- `organized_forestry` : 13
- `institutionalized_public_credit` : 5
- `coke_smelting` : 5
- `selective_breeding` : 2
- `turnpike_road_networks` : 2
- `permanent_engineer_services` : 1


Une fois l’implémentation terminée, reconstruis la dette de prérequis.

Elle doit correspondre au CSV de dette, hors différence explicitement expliquée par le working tree.

Ne transforme pas cette phase en rework de l’arbre.

---

## 7 — ORDRE D’IMPLÉMENTATION CONSEILLÉ

Travaille par vagues internes, sans commit intermédiaire obligatoire :

### Wave 0 — P0 et grants explicites anachroniques
Retirer les grants explicites REMOVE évidents :
- BRA railways
- DEI joint_stock_companies
- romanticism x7
- autres `Explicit_REMOVEs` du COUNTRY PLAN.

### Wave 1 — BEL / SPC
Appliquer les deux `CHANGE_TIER_AND_PATCH`.

### Wave 2 — EXPLICIT_SETUP
Traiter les 186 TAG par région.
Pour chacun, écrire exactement `Final_Technologies`.

### Wave 3 — KEEP_TIER_AND_PATCH
Appliquer les ADD et suppressions explicites sur les 283 TAG restants.

### Wave 4 — validation globale automatique
Ne pas se contenter de grep ponctuels.

Écrire si nécessaire un script TEMPORAIRE hors gameplay pour :
- parser les 7 effets de tier ;
- parser les historiques pays ;
- calculer le set technologique effectif de chaque TAG ;
- comparer les 474 sets à `Final_Technologies`.

Le script de validation peut rester dans `docs/tools` ou être supprimé à la fin;
ne crée pas de nouvelle mécanique runtime.

---

## 8 — VALIDATION EXACTE PAR TAG

Pour chacun des 474 TAG :

`computed_starting_technologies == Final_Technologies`

Le rapport doit donner :

- MATCH : nombre attendu 474 ;
- MISMATCH : attendu 0.

Si un mismatch existe :
corrige l’implémentation avant de conclure.

Pour GAL / MLT / PPU :
le set calculé doit rester identique à l’état pré-phase.

---

## 9 — CONTRÔLES GLOBAUX

Confirmer après implémentation :

1. 474 TAG reconstruits.
2. 0 `railways`.
3. 0 `joint_stock_companies`.
4. 0 `romanticism`.
5. 0 technologie C/D distribuée.
6. `coke_smelting` uniquement GBR.
7. `precision_boring` uniquement GBR.
8. `mechanized_spinning` uniquement GBR.
9. `industrial_canals` uniquement FRA, GBR, NET.
10. aucune modification TECH6D.
11. aucune modification TECH7A.
12. aucun changement de tech tree / era / prerequisite.
13. aucun ajout automatique de parents.

---

## 10 — CONTRÔLES RÉGIONAUX DE SANITÉ

Vérifier au minimum les cas suivants :

### Europe occidentale
GBR, FRA, NET, SPA, POR, BEL, SPC.

### Europe centrale
AUS, PRU, BRA, SAX, VEN.

### Nord / Est
SWE, DEN, DENNOR, RUS, PLC.

### Ottomans / Moyen-Orient
TUR, PER, EGY, OMA.

### Asie du Sud
BIC, MYS, MARATH, MUG, BCE, BHV.

### Asie orientale
CHI, JAP, DEI, PHI, SIA.

### Amériques
USA, CUB, GR5, ORG, BRZ.

### Afrique
MOR, TUN, TRI, ETH, SAF.

### Océanie
NSW, TAS, WAS, SAS, HAW, TNG.

Pour chaque cas :
afficher le tier effectif, les grants explicites et le set final calculé.

---

## 11 — RISQUES GAMEPLAY À TESTER

Certaines suppressions touchent des nœuds structurants comme :
- `urbanization`;
- `shaft_mining`;
- `regulated_small_arms`;
- `systematic_administrative_statistics`.

Ne les rétablis pas automatiquement.

Mais signale les TAG qui perdent :
- construction sector / urban-center access via `urbanization`;
- mines via `shaft_mining`;
- industries militaires via `regulated_small_arms`.

Leur suppression est historiquement volontaire dans la matrice,
mais un runtime de jouabilité devra ensuite vérifier leurs effets.

---

## 12 — FICHIERS À NE PAS TOUCHER

Ne modifie pas :
- technologies / tech tree ;
- TECH6D ;
- TECH7A ;
- goods ;
- buildings ;
- production methods ;
- production method groups ;
- lois ;
- événements ;
- journaux ;
- localisation,

sauf si une localisation strictement nécessaire à un rapport documentaire est ajoutée,
ce qui ne devrait normalement pas être nécessaire.

La phase doit être concentrée sur les historiques de pays / effets de départ nécessaires.

---

## 13 — DOCUMENTATION

Mettre à jour ou créer :

`docs/reports/technology/TECH_START_1776_IMPLEMENTATION_REPORT.md`

Le rapport doit contenir :

- nombre de fichiers pays modifiés ;
- nombre de TAG par stratégie ;
- liste des `EXPLICIT_SETUP`;
- BEL/SPC tier change ;
- traitement BHV/ORG ;
- nombre d’ADD/REMOVE effectifs ;
- validation 474/474 ;
- comparaison des smoke tests ;
- dette de prérequis finale ;
- toute divergence entre working tree et synthèse.

Ne modifie PAS les matrices de recherche pour masquer une divergence.

---

## 14 — GIT / VALIDATION STATIQUE

À la fin :

- `git status --short`
- `git diff --stat`
- `git diff --check`

Vérifier :
- accolades ;
- syntaxe des country history ;
- aucun ID technologie inconnu ;
- aucun `add_technology_researched` dupliqué dans un même setup final ;
- aucune technologie finale non présente dans le CSV canonique.

Ne commit pas.
Ne push pas.
Ne crée pas de PR.

---

## 15 — RAPPORT FINAL DANS LE CHAT

Donne :

1. nombre de TAG MATCH / MISMATCH ;
2. nombre de pays modifiés ;
3. stratégie :
   - KEEP_TIER_AND_PATCH
   - EXPLICIT_SETUP
   - CHANGE_TIER_AND_PATCH
   - RESEARCH_GAP
4. nombre d’ADD ;
5. nombre de REMOVE ;
6. P0 corrigés ;
7. BEL/SPC ;
8. BHV/ORG ;
9. smoke tests des technologies frontière ;
10. dette de prérequis finale ;
11. fichiers créés/modifiés ;
12. `git diff --stat` ;
13. `git diff --check` ;
14. checklist runtime recommandée.

Ne fais aucune nouvelle recherche historique.
Ne commit pas.
Ne push pas.
