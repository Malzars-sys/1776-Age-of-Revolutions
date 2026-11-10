# Reproduction des contrôles 40

À exécuter depuis la racine du dépôt avec le Python disponible. Ne pas écraser les preuves existantes ; choisir de nouveaux chemins sous ce dossier si les noms proposés existent déjà. Les commandes écrivent seulement des rapports nouveaux.

## Installation réelle

```powershell
python -B tools/compatibility/issue40_culture_compatibility_audit.py --before docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/BASELINE.json --negative-controls --output docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/VERIFY_LIVE_NEW.json
```

## Candidat conservé

```powershell
python -B tools/compatibility/issue40_culture_compatibility_audit.py --before docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/BASELINE.json --candidate docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/candidate --negative-controls --output docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/VERIFY_CANDIDATE_NEW.json
```

Le candidat remplace en mémoire les seuls cinq chemins concernés, même après installation ; les autres fournisseurs ne sont pas supprimés pour masquer des doublons. La reproduction après installation a effectivement obtenu **1 793/1 793 et 15/15**, dans `REPRODUCED_CANDIDATE_VALIDATION.json`. L'installation réelle ajoute un contrôle de présence des cinq nouveaux chemins : **1 794/1 794**. Les contrôles négatifs modifient des copies des données analysées et ne touchent pas les fichiers de jeu.

## Outil du chantier 24

```powershell
python -B tools/compatibility/issue24_map_dlc_audit.py --skip-pixels --output docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/VERIFY_MAP24_NEW.json
```

Ce dernier contrôle doit être lu par catégorie : la livraison 40 retire les références culturelles invalides, mais ne résout pas les autres limites déjà documentées de 24. Il ne vérifie pas les pixels avec cette option.

`BASELINE.json` est l'état réel enregistré avant installation. Ne pas le recréer depuis le jeu déjà corrigé et le présenter comme un état antérieur. L'ancien lecteur de population reste inchangé ; ses échecs avant/après sont conservés et ne sont pas comptés comme des tests réussis.
