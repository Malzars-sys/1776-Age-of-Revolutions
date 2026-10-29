# ARABLE-01 — Population, terres et famines de départ

Ouvrir **[le tableau interactif](delivery/TABLEAU.html)** dans un navigateur local. Recherche par État ou pays, tri par colonne, filtres de famine et de pression d'emploi, activation/désactivation des chiffres moteur. Cliquer une ligne pour les détails, sources et réserves.

Le tableau conserve la sauvegarde locale du **1er janvier 1776 avant stabilisation d’Agra**. Il ne réécrit aucune donnée du mod et distingue saturation d’emploi et crise alimentaire moteur. Le correctif provisoire **483 → 764 terres** a ensuite été installé sur demande explicite : [reçu et contrôle restant](PROVISIONAL_INSTALLATION.md). Les nombres de crises et pourcentages du tableau ne sont pas un résultat après ce correctif.

- [Résultats et méthode](REPORT.md)
- [Agra : recherche et scénario](AGRA_RESEARCH.md)
- [Liste de travail historique](delivery/REVIEW_QUEUE.csv)
- [Diagnostic complet](delivery/DIAGNOSIS.json)
- [Données statiques](delivery/STATES.csv) et [données moteur](delivery/RUNTIME_STATES.csv)
- [Observations directes de l'interface](UI_OBSERVATIONS.json)
- [Protocole pour les prochaines passes](NEXT_PASSES.md)

## Régénérer après de futures modifications

Depuis le dépôt, avec Python et les dépendances déjà utilisées par ses autres validateurs :

```powershell
python -X utf8 tools/audit_arable_population_1776.py --out docs/reports/economy/ARABLE_POPULATION_1776/ARABLE-02/diagnostic
```

Le dossier de sortie doit être nouveau : un résultat antérieur n'est jamais écrasé. Aucun argument ne déclenche une correction automatique. Ajouter `--save-text chemin/vers/une_copie_texte.txt` pour comparer à une sauvegarde décompressée en lecture seule. Les originaux `.v3` ne sont pas réécrits.

```powershell
python -X utf8 tools/audit_arable_population_1776.py --save-text .asset-cache/arable_1776/initial_readonly.txt --observations docs/reports/economy/ARABLE_POPULATION_1776/ARABLE-01/UI_OBSERVATIONS.json --out docs/reports/economy/ARABLE_POPULATION_1776/ARABLE-02/comparison
```

Ce deuxième exemple réemploie la sauvegarde **antérieure aux corrections futures**. Il ne les valide pas ! Les observations d'interface sont liées à son empreinte SHA-256 et sa date. Pour une autre sauvegarde, créer de nouvelles observations ; ne pas recycler les pourcentages d'Agra.

La conversion déjà utilisée dans ce dépôt est `rakaly melt --format vic3 -u stringify -o <nouveau fichier texte> <original.v3>`. L'exécutable existant est dans `.asset-cache/oct09_balance_revision/rakaly/rakaly-0.8.21-x86_64-pc-windows-msvc/`. La commande lit l'original et écrit seulement la copie de travail.

Tests : `python -X utf8 tools/test_audit_arable_population_1776.py` et `node tools/test_arable_dashboard.cjs <TABLEAU.html>`. Le second exécute le script livré dans un environnement DOM de contrôle hors navigateur ; il ne certifie pas son rendu visuel.
