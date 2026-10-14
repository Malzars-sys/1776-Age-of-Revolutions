# Rhin central — lot engagé après la Franconie

**Mise à jour :** le premier sous-lot du Neckar est maintenant appliqué. Ce document conserve la trace du démarrage ; les formulations « aucun transfert » ci-dessous décrivent cet état préparatoire, non l'état actuel. Voir `REPORT.md` et `VALIDATION.json` pour les transferts réels, les tests et les limites restantes.

Le 13 octobre 2026, l'utilisateur demande de commencer le lot et précise qu'il ne lancera Victoria 3 qu'après la fin de tous les lots du Saint-Empire. Les validations statiques se poursuivent entre les lots ; aucun essai moteur anticipé n'est requis et aucun résultat de chargement ne doit être affirmé.

## Périmètre initial

Mayence (`KMZ`) et Palatinat (`KPF`) d'abord ; raccords dans `STATE_RHINELAND`, `STATE_HESSE`, `STATE_BADEN` et frange occidentale de `STATE_FRANCONIA`. Ces régions sont un domaine d'examen, pas l'autorisation de réattribuer toutes leurs provinces en bloc. Les territoires séparés de Mayence exigent une suite ciblée et ne sont pas automatiquement assimilés à HES ou SAX.

`BASELINE.json` fige l'état local après le lot franconien et réutilise son bitmap candidat identique, sans nouvelle copie intégrale du mod. `CURRENT_PROVINCES.csv`, `NATIVE_ANCHORS.json` et `BEFORE.png` donnent les polygones et repères effectifs avant cette passe. Le nom natif ancien de Coburg reste signalé comme repère rejeté, non réutilisé pour décider des droits de Bamberg.

## Recherches réutilisées et contrôle réel

- Dossier `MAP1/MAP1_CASE_DOSSIERS/R2_NORTHERN_CENTRAL_EASTERN_EUROPE-0029.md` : autonomie du Palatinat en 1776, mais aucune frontière RGB certifiée. Les deux anciens RGB bavarois sont des champs d'examen, pas des limites historiques prouvées.
- `tools/map2k_patch.py`, lignes 9–14 et 28–32 : transfert antérieur de `x11C021` et `x707505` à KPF, et `x1141A0` à KMZ, explicitement qualifié d'approximation par provinces entières. Ce générateur ancien ne doit pas être réexécuté sur le mod courant.
- Les cartes belges de 1789 conservées ne représentent pas les juridictions rhénanes. La carte dynastique générale de 1789 a été examinée : elle agrège Bavière/Palatinat et les principautés ecclésiastiques ; elle est impropre au tracé distinct de 1776. Elle n'est pas copiée dans le bitmap.
- Les cartes Homann/Le Rouge franconiennes couvrent le lot précédent mais ne suffisent pas à dessiner le noyau rhénan. Les dossiers disponibles ne démontrent pas encore le raccord de Mayence autour d'Aschaffenburg.

Une recherche cartographique extérieure ciblée est donc nécessaire, sans relancer l'étude mondiale. Pistes institutionnelles identifiées, pas encore calées ni approuvées pour le runtime :

- [BnF, notice d'atlas Santini](https://catalogue.bnf.fr/rechercher.do?index=AUT3&numNotice=15374344&typeNotice=p) : carte des cercles du Haut/Bas Rhin et enclaves d'après Robert de Vaugondy (1753), publiée en 1777. Distinguer la date du fond et celle de l'édition ; ne pas rétroprojeter l'union Bavière/Palatinat de décembre 1777.
- [UB Bern, carte De Wit de Mayence et régions voisines](https://www.e-rara.ch/bes_1/content/titleinfo/29609156) : après 1688, trop ancienne pour trancher seule 1776 ; utile seulement en confrontation géographique et avec vérification des mutations intervenues.
- [UB Freiburg, atlas conservant plusieurs cartes du Palatinat](https://dl.ub.uni-freiburg.de/diglit/kartensammlung_bd03/0018) : l'accès par l'outil web a échoué ; ne pas présenter la carte comme effectivement inspectée.

## Avancement concret du démarrage

- Baseline créée : 65 affectations de provinces examinables, six snapshots de fichiers pertinents, 1 720 fichiers runtime protégés, registre impérial de 359 RGB et HEAD/index inchangés.
- Contrôle `tools/map2l_rhine.py verify` réussi : inventaire, bitmap et registre identiques à la baseline ; zéro transfert et zéro nouveau RGB dans ce démarrage. Résultat dans `PREPARATION_VALIDATION.json`.
- Le repère natif Heidelberg est en `STATE_BADEN`, RGB `xE0A2B9`, actuellement BAD. C'est un candidat à subdivision et vérification, pas un transfert de tout le polygone par le nom de la ville.
- L'accès au manifeste public Gallica `btv1b10224815w` a été refusé par le service (Cloudflare) ; aucune tentative de contournement n'a été faite.
- L'exemplaire [Rumsey 3353.062](https://www.davidrumsey.com/maps2294.html) fournit une vignette de seulement 384 × 243 pixels, conservée et visuellement examinée dans `VAUGONDY_READING.jpg`. Elle est insuffisante pour tracer des limites ; aucune interpolation ne lui ajoute d'information historique.
- Une reproduction photographique publique du même fond Vaugondy, édition Santini 1777, est conservée dans `VAUGONDY_SANTINI_DETAIL.jpg` (2 851 × 2 038). Identité et titre examinés visuellement ; provenance, hash, dates et statut dans `VAUGONDY_SANTINI_SOURCE.json`. C'est un exemplaire distinct hébergé sur Commons, pas le scan de la BnF. Les dérivées techniques `READING_MAINZ_PALATINATE.png` et `READING_TRIER.png` repèrent les coordonnées de lecture ; l'original est immuable.

Prochaine opération : caler les villes/cours d'eau avec trois repères identifiés précisément et un contrôle indépendant, distinguer les contours de cercles des véritables limites de principautés, puis préparer des polygones candidats avec confrontation des mutations de 1753 à 1776. Les points approximatifs non contrôlés ne sont pas enregistrés comme géoréférencement. Ne pas transférer une province entière parce qu'elle contient Mannheim, Heidelberg, Kaiserslautern ou Mayence. Les petites enclaves restent abstraites sans agrandissement artificiel. À ce stade, **aucun nouveau découpage rhénan n'est appliqué**.

## ColGrep

Un appel à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent` a demandé la localisation des dossiers préexistants de Mayence/Palatinat et des outils. Il a retourné seulement `tools/map2k_patch.py:13` et `:15`. Ces deux lignes ont été lues et vérifiées ; elles définissent effectivement KMZ et la liste des électeurs, mais ne fournissent ni dossier historique ni source de frontière. Le résultat est donc partiellement pertinent et insuffisant ; les dossiers CSV et cartes ont été retrouvés directement avec recherches exactes et lectures structurées, sans second appel redondant au 2B.

La sortie capturée ne fournit ni statistiques détaillées d'inférence ni nom du backend ; ne pas en déduire un temps précis ou une économie de quota. Aucun compteur Codex par recherche ni comparaison A/B n'est disponible. Le modèle local reste un localisateur, pas un arbitre historique.
