# Correction de la fermeture au démarrage de la mesure

Le joueur signale que le bouton Mesurer ferme l'assistant et Victoria 3. Le reçu `MANUAL_20261116T234705029Z/CONTROL1/INTERRUPTED_20261116T235317972Z.json` indique une fermeture pendant la capture ; le journal du jeu reçoit ensuite `Quit: Quit event from OS`. Le reçu de sortie indique -1 après le nettoyage borné du processus possédé. Aucun CSV CPU ou relevé de performance valide n'a été produit dans cette tentative.

La fenêtre était ouverte avec `ShowDialog()`. L'appel `Hide()` au début de la mesure termine cette boîte modale et déclenche son nettoyage `FormClosing`, qui ferme le processus du jeu. Le remplacement par `Application.Run(form)` maintient la boucle de messages et le minuteur pendant que l'assistant est masqué.

Le code antérieur est conservé dans `Assistant_Test_BEFORE_CAPTURE_FIX_20261117.ps1`. L'initialisation de la capture a été extraite dans une fonction commune au bouton et au test. Les options SelfTest et LegacyLoop servent seulement à tester le cycle sur un processus PowerShell inactif possédé ; LegacyLoop est refusée hors SelfTest. Les données synthétiques sont explicitement marquées, rangées sous SELFTEST et ne sont jamais des mesures de Victoria 3.

Résultats effectifs :

| Contrôle | Résultat |
| --- | --- |
| Parseur PowerShell et CheckOnly sur les entrées préparées | Réussite |
| Ancienne boucle, même démarrage de capture | Échec reproduit : fermeture pendant la capture, aucun échantillon |
| Boucle corrigée, attente de cinq secondes puis capture | Réussite : 14 échantillons, 15,3113645 secondes effectivement observées |
| Assistant visible après la capture corrigée | Oui, propriété de fenêtre vérifiée par le test |
| Processus synthétique encore vivant après la capture | Oui, avant sa fermeture volontaire de fin de test |
| Fermeture pendant la capture corrigée | Non |
| Victoria 3 lancé par les deux tests de régression | Non |

Les reçus détaillés sont dans `SELFTEST_LEGACY_20261116T235849869Z/RESULT.json` et `SELFTEST_FIXED_20261116T235925333Z/RESULT.json`. Le scénario de régression passe par le même démarrage de capture et le même minuteur/collecteur que le bouton réel. Cela valide le défaut de durée de vie de la fenêtre et une collecte complète ; cela ne valide ni la fluidité du jeu, ni les états de son arbre, ni sa latence d'ouverture.

L'assistant et le guide sont corrigés. La sauvegarde commune, les variantes et les réglages préparés passent encore CheckOnly. Les empreintes de l'index Git et des trois fichiers du chantier Russie–KZH sont conservées. Aucun fichier du mod principal, du vanilla ou du profil normal n'a été modifié par cette correction. La série réelle doit reprendre au premier témoin, puisque la tentative interrompue ne comporte aucune mesure valide.
