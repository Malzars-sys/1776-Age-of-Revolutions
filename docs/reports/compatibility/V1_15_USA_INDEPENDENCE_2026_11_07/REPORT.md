# Révolution américaine : conclusions 1.15 — 7 novembre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Correctif installé dans le mod local ; contrôle statique réussi, affichage et issues encore à vérifier après redémarrage. Aucun lancement du jeu, modification de sauvegarde ou écriture Git.

## Symptôme et correction

Le joueur montre le journal **American Revolution** des Treize Colonies avec sa raison, mais sans conditions de réussite ou d'échec. `06_usa_independence_mod.txt` employait encore les anciens champs `complete`, `on_complete`, `fail` et `on_fail`, rejetés par la 1.15.

Les deux définitions de ce même fichier sont migrées :

| Journal | Réussite conservée | Échec conservé |
| --- | --- | --- |
| `je_usa_independence` | Le pays n'est plus sujet **et** n'est plus en guerre. | Le pays n'est plus en guerre **et** reste sujet. |
| `je_usa_independence_fra` | Les États-Unis ne sont plus sujets **et** la France n'est plus en guerre. | La France n'est plus en guerre **et** les États-Unis restent sujets. |

**Un fichier de gameplay, deux journaux, huit champs hérités remplacés par quatre issues.** Les présentations positives/négatives emploient les clés natives françaises et anglaises déjà disponibles. Aucun texte de raison n'est remplacé et aucune nouvelle condition n'est inventée.

Tous les prédicats, effets et champs hors conclusions sont conservés comme suites de tokens ordonnées. Cela inclut les modificateurs de guerre/liberté/répression, les lois de l'échec, les changements d'idéologie, les variables, le nettoyage du soutien français et du contenu révolutionnaire, les offres de réorganisation militaire et l'événement français d'échec. Le groupe Destin des Amériques et les conditions d'activation restent inchangés.

L'effet immédiat américain conservait déjà une variable globale liée à l'Espagne : elle reste identique. Aucun journal ou événement espagnol n'est modifié, conformément à la demande de laisser ce chantier en attente.

## Vérifications

Le validateur `tools/compatibility/issue27_journal_outcomes_audit.py` accepte désormais le lot borné `american-independence`. Ses contrôles de préservation ne sont pas assouplis. La copie exacte avant intervention est conservée sous `BASELINE/common/journal_entries/06_usa_independence_mod.txt`.

```text
python -B tools/compatibility/issue27_journal_outcomes_audit.py --batch american-independence --mod-root . --baseline-root docs/reports/compatibility/V1_15_USA_INDEPENDENCE_2026_11_07/BASELINE --vanilla-root "C:/Games/Victoria 3/game"
git diff --check -- common/journal_entries/06_usa_independence_mod.txt tools/compatibility/issue27_journal_outcomes_audit.py
```

Résultat effectif : **PASS_STATIC_ONLY**, deux journaux, quatre issues, zéro erreur. Les six clés de conclusion sont présentes en français et en anglais dans les fichiers natifs non masqués. Sept contrôles négatifs détectent une condition d'indépendance inversée, une condition de paix inversée, un nettoyage altéré, une loi d'échec substituée, un scope français/américain erroné, un événement français remplacé et un ancien champ réintroduit.

**525 fichiers protégés** conservent leurs empreintes : autres journaux, groupes, localisations et événement d'ouverture espagnol. La preuve machine est dans `VALIDATION.json`. L'inventaire après ce lot comporte 1 381 champs hérités dans 166 fichiers, concernant 400 identifiants de journal ; ce n'est pas un nombre de bugs.

## Confirmation canadienne bornée

Le joueur confirme dans cette conversation : **« Il n'y a plus de clés brutes pour le Canada. »** Cette confirmation accepte la correction d'affichage des clés canadiennes. Elle ne valide pas l'unification, ses événements ou toutes les issues du journal. La localisation réutilise déjà les textes natifs immersifs ; aucune réécriture supplémentaire n'est nécessaire pour cette seule correction.

## Contrôle en jeu restant

Après redémarrage, rouvrir la Révolution américaine et vérifier les deux issues et leurs effets affichés. Tester séparément une paix avec indépendance et une paix en restant sujet, puis le nettoyage appliqué une fois, la conclusion des journaux de soutien et sauvegarde/rechargement. Le pays doit être en paix, et pas seulement avoir obtenu un changement diplomatique pendant qu'une autre guerre continue.

La branche française conserve ses propres conditions de paix et son événement d'échec ; elle n'est pas certifiée par le test des Treize Colonies. Les nouveaux résultats de rendu et d'exécution restent à recevoir. La prose existante est préservée en attendant la validation des mécanismes.
