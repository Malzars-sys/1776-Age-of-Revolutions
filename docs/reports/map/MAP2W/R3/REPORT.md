# MAP-2W-R3 — Livraison bloquée par une contradiction de calage

Date : 18 octobre 2026. Référence historique : 1er janvier 1776.

**Statut final : MAP2W_R3_BLOCKED. Aucun transfert territorial R3 installé.**

## Ce qui a été achevé

La validation manuelle R2-B est enregistrée dans `../R2B/RUNTIME_USER_ATTESTATION.json` : nouvelle partie 1776, neuf points contrôlés, un mois de simulation, aucune anomalie déclarée. Ce n’est pas un test moteur automatisé ni une validation des frontières C ou de R3.

Les anciennes passes franconiennes et les fichiers actuels ont été confrontés avant la préparation : Ansbach, Bayreuth, Bamberg, Würzburg, Nuremberg, Eichstätt et Cobourg sont déjà traités. Aucun de ces noyaux n’est reconstruit depuis zéro. Un inventaire ciblé de 19 entrées distingue les branches de Hohenlohe, Castell, Löwenstein-Wertheim, quatre villes impériales et autres juridictions. Les sources indépendantes et les anachronismes sont documentés dans `HISTORICAL_EVIDENCE.md`.

## Candidat retiré et cause précise

Un premier candidat concernait **Langenbourg (HLN, trois cellules) et Kirchberg (HKI, quatre cellules)**, à partir du résidu bavarois xEDA218 de STATE_FRANCONIA / 72. La préparation avait ajouté les pays, les princes, quatre RGB, leurs profils démographiques et leurs dépendances impériales. **Ces ajouts ont tous été retirés ; HLN/HKI et xEDB900–xEDB903 ne sont pas actifs.**

Les contrôles syntaxiques et de conservation passaient : 1 625 contrôles, 28 tests ciblés, 67 contrats impériaux et 40 tests de livraisons. Cela ne suffisait pas à valider la géographie.

La dernière confrontation a révélé un désaccord entre le modèle Miller diagnostique hérité et les repères natifs utilisés dans l’ancienne passe franconienne : environ **7,57 pixels à Würzburg, 2,29 à Nuremberg, 1,99 à Bayreuth et 4,97 à Ratisbonne**. Ces valeurs mesurent une **contradiction entre référentiels**, pas une erreur certifiée de position des villes : les anciens hubs ne doivent pas davantage être supposés exacts.

Pour un noyau de deux ou trois cellules de large, ce désaccord rend l’attribution géographique insuffisante. Le faible écart de la feuille Gerabronn/Schrozberg contre le même modèle diagnostique (0,079/0,222 pixel) ne prouve pas sa justesse dans le jeu. Aucun déplacement moyen ou translation arbitraire n’a été appliqué. Aucune nouvelle optimisation d’Erfurt–Eichsfeld.

Voir `NATIVE_REFERENCE_CONTRADICTION.json`, `SOURCE_ALIGNMENT.json` et les cartes explicitement marquées **CANDIDAT RETIRÉ / NON INSTALLÉ**. `CANDIDATE_STATIC_VALIDATION.json` et `CANDIDATE_TESTS.json` sont des archives d’un essai retiré, non des attestations de livraison.

## État réellement livré et protections

**Zéro province transférée, zéro nouveau TAG, zéro nouveau RGB, aucun changement démographique ou économique actif.** Total mondial : **835 801 255**. Registre impérial : **567 RGB**, neuf électeurs conservés.

Le retrait a été limité aux fichiers créés ou modifiés par cet essai, après vérification de leurs empreintes. Les dix nouveaux fichiers fonctionnels propres au candidat ont été supprimés ; leurs textes restent récupérables dans `EXPECTED_TEXT.json` et les patches de préparation. La carte et les fichiers partagés ont retrouvé exactement leurs empreintes d’avant R3. Les modifications préexistantes et concurrentes n’ont pas été effacées. `WITHDRAWAL_PLAN.json` décrit cette opération ; `VALIDATION.json` vérifie l’égalité de l’inventaire mondial et de toutes les empreintes fonctionnelles avec la capture R3.

Les 44 doublons RGB et 12 références invalides préexistants restent ouverts, sans nouvelle anomalie. Populations, cultures, religions, bâtiments, propriétaires économiques, unités, papeteries, économie française, Saint-Gobain, Anzin, Saint-Domingue et mécaniques impériales sont conservés. HEAD et index inchangés ; aucun staging, commit, merge, reset, rebase, changement de branche ou push. Aucun fichier de l’installation vanilla modifié.

## Dépendance qui manque pour installer R3-A

Il faut des repères **physiques locaux homologues** dans la région Jagst–Kocher / Langenbourg–Kirchberg, observés à la fois dans une source géographique et dans les données natives du bitmap, puis un contrôle indépendant non ajusté. L’alternative est une correspondance locale documentée entre la source détaillée et un ancien calage dont les ancrages physiques sont eux-mêmes vérifiés. Une simple proximité de ville, un nom de locator ou la moyenne des écarts ne suffit pas.

La souveraineté des deux branches est établie ; leur correspondance exacte avec ces petites cellules ne l’est pas. Castell, Wertheim et les villes impériales ne sont pas installés dans un autre référentiel pour contourner ce problème. Les droits partagés d’Öhringen avant 1782, l’ancienne lignée Waldenburg, les gains de 1797/1799/1803 et les condominiums restent distincts dans l’inventaire.

## Livrables et vérification

`INVENTORY_1776.csv`, `DISCREPANCIES.csv`, `UNRESOLVED.csv`, `TERRITORIAL_CHANGES.csv` décrivent l’état final, sans transfert revendiqué. Le rapport démographique du candidat reste dans `ALLOCATION.json`, non appliqué. Carte comparative et `PLAYER_LOCATION_GUIDE.png` montrent uniquement les propositions retirées, pas des pays à chercher en partie.

**Aucun nouveau test en jeu n’est demandé pour R3 : il n’y a rien d’installé à accepter.** La prochaine action utile est la résolution locale de la contradiction, non un mois de simulation. Le statut ne doit pas être changé en READY ou PASS_RUNTIME_USER_VALIDATED sur la seule base des anciens contrôles statiques.

## Mesure de ColGrep

Un appel local `C:\Users\simeo\.cargo\bin\colgrep.exe --agent "Locate retained historical map sources and unimplemented territorial decisions specifically for Hohenlohe branches, Castell and Wertheim, and Rothenburg Schweinfurt Windsheim Weissenburg. Old FRANCONIA/TRACING and FRANCONIA_CONTINUATION are known installed cores; do not return them alone. Return at most five useful paths with line ranges, no edits and no historical decisions." .`

Sortie 0 ; **250,793 secondes**. Les résultats, relus, étaient surtout des fichiers déjà connus et un générateur de rapport trop large : aucune nouvelle source décisive ni recherche évitée démontrée. Le journal ne prouve pas indépendamment quel GGUF/backend a été chargé. Aucun modèle ou paramètre changé, aucune reconstruction forcée d’index. Tokens Codex et nombre exact de recherches classiques non instrumentés ; aucune économie de quota chiffrée revendiquée. L’agent local n’est pas responsable de la décision cartographique : l’insuffisance du premier calage a été détectée et traitée par Codex.
