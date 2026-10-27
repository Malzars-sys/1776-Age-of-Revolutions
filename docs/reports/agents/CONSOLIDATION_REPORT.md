# Consolidation des instructions permanentes

25 octobre 2026. Périmètre exclusivement documentaire.

## Livraison

`AGENTS.md` conserve les instructions antérieures pertinentes et fournit un chargement explicite des neuf documents spécialisés : travail commun, recherche, validation, territoires/démographie, SERG, WORLD, technologies, économie et images. Le guide éditorial `.agents/agent.md` et son relevé de références sont conservés sans modification.

Les **37 règles identifiées** sont rapprochées de leurs sources dans [PERMANENT_RULES_AUDIT.md](PERMANENT_RULES_AUDIT.md). Leurs champs d’application sont distincts ; elles ne lancent pas de nouvelle mission. Les doublons sont regroupés autour de la concurrence, des preuves et du suivi, sans créer de deuxième guide éditorial.

[CONFLICTS.md](CONFLICTS.md) présente les remplacements établis, les différences de périmètre et un arbitrage ouvert sur la portée des confirmations humaines brèves. Aucune donnée de reçu ou de progression n’est rectifiée dans cette passe.

## Éléments écartés des consignes permanentes

- Résultats historiques locaux et propositions non approuvées, y compris approximations territoriales particulières.
- Chiffres démographiques, répartitions culturelles/religieuses, coordonnées, RGB et masques de carte.
- Recettes, prix, emplois, illustrations particulières et parents exacts des technologies : décisions de leurs chantiers, pas règles universelles.
- Validations humaines, dates effectives de test, historiques, scores, preuves et résultats de contrôles.
- Numéros de version moteur mentionnés dans les anciennes passes et anciennes autorisations Git.
- Autorisations ponctuelles de lots et ordre de mission, sauf barrières explicitement maintenues dans les feuilles canoniques et seulement dans leur périmètre.

Ces informations restent dans `docs/` ou leurs emplacements fonctionnels ; aucune archive n’est déplacée ou supprimée. Les règles ColGrep de la session ne sont pas recopiées comme configuration propre au mod.

## Vérification documentaire

Les résultats finaux sont consignés dans [CONSOLIDATION_CHECKS.json](CONSOLIDATION_CHECKS.json) : liens locaux, routage explicite, unicité et traçabilité des règles, conservation des instructions existantes, empreintes des fichiers protégés et état Git. La couverture et les limites de la capture figurent dans [WORKSPACE_BASELINE.json](WORKSPACE_BASELINE.json) ; les sources consultées sont identifiées dans [SOURCE_INDEX.json](SOURCE_INDEX.json).

Résultat : **60 contrôles réussis sur 61**. Les contrôles documentaires passent ; le contrôle d’identité globale signale cinq évolutions externes dans les historiques des États et POPs d’Europe du Sud, le terrain, les régions et le bitmap des provinces. Elles sont consignées dans [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json), avec empreintes avant/après, et ne sont ni restaurées ni présentées comme des modifications de cette passe. Ce signal n’est pas une panne du jeu ni une validation de ces changements.

Les **2 345 fichiers préexistants protégés** ont été comparés (hors `AGENTS.md`, volontairement modifié) : 2 340 identiques et ces cinq différences externes. Les 24 sources consultées sont toujours identiques à leurs empreintes de lecture ; le guide éditorial et son relevé sont intacts. HEAD, branche et index Git restent identiques pendant la consolidation. La couverture n’inclut pas tous les binaires de `gfx/` ni l’ensemble récursif des anciennes archives.

Aucun validateur territorial ou technologique générant des vues n’est lancé : cela écrirait un suivi actif hors mission. Aucun test moteur n’est annoncé. Les comparaisons d’empreintes servent à protéger les travaux concurrents, pas à certifier leur exactitude historique ou leur fonctionnement.

La passe se termine avec cette consolidation ; aucune autre mission n’est commencée.
