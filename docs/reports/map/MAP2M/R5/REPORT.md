# MAP-2M-R5 — Calage empirique régional et examen conditionnel

Date cible : **1er janvier 1776**. Statut : **MAP_2M_R5_PARTIAL**. **Aucun transfert territorial appliqué.**

R5 livre une transformation réelle→bitmap réutilisable, des observations physiques natives explicites et des tests réservés. Elle ne livre pas une frontière intégrale certifiée. Les conditions historiques et géométriques cumulatives de la classe A ne sont atteintes pour aucune nouvelle cellule ; les fichiers fonctionnels restent inchangés conformément à la clause de repli de la mission.

## A. Peut-on placer les coordonnées réelles sur le bitmap ?

**Oui à titre régional approximatif, pas avec une précision exacte garantie à toute position.** Un nouveau profil empirique à axes séparés est calculé depuis cinq homologues physiques : caps de Darss, Arkona, Buk, extrémité de Hel, confluent de la basse Narew/Bug avec la Vistule. Il n'est pas un décalage de l'ancienne hypothèse Miller et n'utilise aucun locator de ferme.

Quatre contrôles d'origine, jamais utilisés dans l'ajustement :

| Contrôle | Écart R5 |
| --- | ---: |
| Fehmarn, cap nord | 2,50 px |
| Jasmund, extrémité est | 1,28 px |
| Nordperd, cap est | 1,34 px |
| Confluent Warta–Oder | 3,19 px |
| **Moyenne / maximum** | **2,08 / 3,19 px** |

Ces valeurs sont des écarts à des formes physiques schématisées, pas à des positions géodésiques certifiées. La mesure de Fehmarn et celle de Warta–Oder sont hors du support convexe des ancrages : elles testent aussi l'extrapolation. Les deux contrôles originaux internes Jasmund/Nordperd ne suffisent pas à garantir la précision de toutes les zones intérieures. La sélection du modèle a tenu compte de ces contrôles ; il n'existe pas ensuite un troisième jeu de test final totalement aveugle.

Sur les **mêmes quatre contrôles**, le premier profil à axes séparés, ajusté aux seuls caps, donnait moyenne **2,28 px**, maximum **3,74 px**. L'ajout d'un ancrage méridional distinct améliore cette comparaison sans absorber Warta–Oder dans les points d'ajustement. Ce n'est pas une comparaison à la métrique « plus proche rivage » de R3/R4, qui mesure autre chose.

Un premier contrôle « Usedom » était mal identifié dans notre propre fenêtre d'extraction : elle rencontrait la pointe sud de Rügen. Son observation initiale et son erreur sont conservées. Le cap d'Usedom est corrigé après examen morphologique ; sa nouvelle erreur est **0,17 px**, mais il est marqué **REVISED_CHECK** et exclu de la moyenne à quatre contrôles. Ce n'est pas une précision indépendante miraculeusement acquise.

Les quatre modèles comparés, les données brutes, les retraits d'ancrages et 300 perturbations reproductibles figurent dans les JSON. Les transformations affines libres extrapolent nettement moins bien ; leurs résultats restent disponibles et ne sont pas dissimulés. Une projective ou un polynôme n'est pas ajouté à cet ensemble clairsemé pour améliorer artificiellement les résidus.

### Outil livré

`query.py` lit le profil `TRANSFORMATIONS.json` sans écrire dans le mod. Il convertit longitude/latitude↔X/Y et refuse par défaut une requête hors du support convexe des ancrages ; `--allow-extrapolation` doit être explicite pour un diagnostic extérieur. Le profil n'est pas applicable à Erfurt ou à toute la planète par simple extension de domaine.

Exemple Anklam (coordonnées de diagnostic, pas preuve de souveraineté) : **X=4408,20 ; Y=741,12**. Wolgast : **4410,14 ; 735,05**. Les écarts entre modèles, retraits de points et perturbations sont des diagnostics de sensibilité, pas des intervalles de confiance ni des erreurs totales garanties des villes.

## B. Les 18 cellules de la Peene et les 77 de la Netze sont-elles résolues ?

**Non.** Les 18 cellules de la Peene restent B. Les 77 cellules de la Netze sont reclassées C pour la décision de transfert : leur ancien masque ne possède toujours pas de conversion politique source→réel suffisamment validée. Cela ne prouve pas que leur attribution historique proposée est fausse ; cela signifie qu'elle ne peut pas être installée sur la base disponible.

L'examen n'est pas restreint à ces95cellules. Le nouveau calage physique de Mayer, avec ses variantes, a servi à un balayage de toutes les cellules restantes de `xE1A03A` dans la fenêtre **X4384–4411 / Y730–747**. Il révèle **149 autres cellules diagnostiques B**. Ce sont des pixels à réexaminer, pas un lot de corrections prêt. Au total : **244 lignes, 167 B, 77 C, 0 A**. Les cellules déjà suédoises, Thorn et les autres régions ne sont pas incluses comme transferts nouveaux.

## C. Peut-on délimiter des portions supplémentaires des quatre districts ?

**Pas encore avec la chaîne complète de preuves demandée.** Les deux rectos N1146/1 et les cinq feuilles Pfau sont conservés et leurs emprises réutilisées. Aucune nouvelle acquisition documentaire générale n'est faite.

Pour Pfau, R5 teste une cause précise : une mauvaise rotation ou réflexion globale du repère. Les rotations90/180/270° et la réflexion, appliquées uniformément aux mêmes points, donnent les **mêmes prédictions affines réservées à moins de 0,000001m**. Les désaccords de4,25km et2,13km de l'affine R4 ne sont donc pas corrigibles par ce seul changement de cadre. Les rapports de distance source/réel varient aussi fortement. En revanche, cela ne prouve pas que la carte elle-même est fausse : l'identité des croix d'églises et la déformation locale restent deux explications non départagées. Les contrôles d'Inowrocław/Pakość n'ont pas été promus en ancrages.

Il n'existe pas encore de réseau de raccords physiques indépendamment homologués entre les feuilles. Leur assemblage géographique par simple collage est refusé. Aucun nouveau profil Pfau accepté n'est fabriqué en réajustant des symboles ambigus.

Pour N1146/1, les tracés politiques, les limites internes, les noms de propriétés privées écrits en rouge et les ajouts non datés restent distincts. Une géométrie source→réel non établie interdit de produire des cellules à partir d'une interprétation colorée du brouillon. Deutsch Krone, Kamin et Bromberg restent des secteurs B ; l'extension méridionale d'Inowrocław reste C, partiellement hors de l'emprise détaillée du manuscrit. La date[1772] ne règle pas à elle seule les changements1776/1777.

`BORDER_RECONSTRUCTION.csv` contient les projections diagnostiques du tracé déjà lu sur Mayer, avec distinction des **bords de cadre non politiques**, et une ligne d'état pour chacun des quatre districts. Il ne présente pas ces dernières lignes comme des segments géographiques reconstruits alors qu'aucun tracé qualifié n'est disponible.

## D. Transferts réellement appliqués et vérifiés

**Zéro.** `TERRITORIAL_CHANGES.csv` contient son en-tête et aucune ligne de transfert. Les images avant/après ont des fonds de propriétaires identiques ; les cadres et courbes supplémentaires sont des couches diagnostiques explicitement légendées.

Référence préservée : `x567452`357cellulesSWE ; `xEDB010`85PRU ; `xFCC7B7`142PLC ; population835804980. Pas de nouveauRGB, d'historique modifié, de redistribution démographique ou de changement de bâtiment/PM/propriétaire économique/unité/recrutement. Thorn `x41A021` reste inchangé. Les44doublonsRGB et12références invalides hérités restent ouverts séparément.

Les résultats exacts des contrôles d'intégrité, tests mathématiques, tests de syntaxe, références de candidats, empreintes R4 et comparaison de l'inventaire effectif sont dans `VALIDATION.json`. Ils ne sont pas une validation historique ou un test moteur. R3 conserve son **PASS_RUNTIME_USER_VALIDATED** manuel ; aucune validation en jeu R5 n'est revendiquée.

## E. Obstacles exacts et suite utile

1. **Natif** : une précision régionale de quelques pixels devient mesurable ; elle reste insuffisante pour une attribution incertaine à une cellule près. Les observations de caps ont elles-mêmes une incertitude de généralisation/lecture, déclarée. Une prochaine sélection doit conserver un nouveau contrôle final non utilisé pour choisir le modèle.
2. **Peene** : le nouveau calage de Mayer repose encore surtout sur les caps au nord ; son extrapolation à la frontière méridionale n'a pas de contrôle historique physique suffisamment distribué. Les variantes déplacent les décisions près du Peenestrom. Le plan d'Anklam ne résout pas Wolgast.
3. **Échelle urbaine** : la dispersion des cinq édifices/moulin du plan d'Anklam projetés couvre environ **0,15×0,20pixel**. Cette estimation explique pourquoi une position urbaine plus précise ne permet pas d'attribuer une grande surface à Peendamm. Ce n'est pas une mesure exacte de sa frontière.
4. **Pfau** : identifier les édifices ou configurations physiques exacts avant un nouveau calage ; pas de nouvelle optimisation des mêmes trois croix provisoires.
5. **Netze politique** : extraire une ligne de frontière datée, contrôlée source→réel, en distinguant1772,1776et1777. Un profil natif amélioré ne remplace pas cette étape.

Les actions concrètes et les fichiers à employer figurent dans `NEXT_STEPS.md`. **MAP-2M n'est pas clos artificiellement.**

## Reproduction et ColGrep

Quatre scripts autonomes de dossier, `work.py`, `review.py`, `finish.py`, `query.py`, réutilisent uniquement les sources locales R3/R4 ; aucune acquisition extérieure n'est nécessaire. La procédure complète figure dans `NEXT_STEPS.md`. Ne pas relancer la capture initiale pour remplacer la référence.

ColGrep a été invoqué deux fois pour localiser les anciens outils : échec initial de verrou en environnement restreint, puis recherche agent réussie avec autorisation d'accès à son index. Les chemins `tools/map2l_thuringia_calibration.py:142–183` et `docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/native_miller_hypothesis.json:9–22` ont été relus et vérifiés. Aucune configuration d'intégration n'a changé. La commande était `colgrep.exe --agent "Locate explicit native map projection parameters, geographic longitude latitude to bitmap pixel metadata, and reusable coastline or river extraction/calibration code. Return exact file paths and line ranges. Search only; do not modify project files." .` ; sortie finale code0. Les informations GPU/modèle et compteurs exacts de tokens n'ont pas été capturés : aucun gain de quota ni chronométrage exact non mesuré n'est annoncé.

Aucun commit, merge, reset, push, changement de branche ou modification d'index.
