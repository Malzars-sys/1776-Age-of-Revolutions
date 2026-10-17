# Reproduction et décision après R6

## Reproduire sans nouvelles acquisitions

Employer le Python disposant de Numpy et Pillow. Depuis la racine du dépôt :

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python docs/reports/map/MAP2M/R6/pilot.py palette
python docs/reports/map/MAP2M/R6/pilot.py readings
python docs/reports/map/MAP2M/R6/pilot.py extra_crops
python docs/reports/map/MAP2M/R6/pilot.py source_details
python docs/reports/map/MAP2M/R6/pilot.py holdouts
python docs/reports/map/MAP2M/R6/pilot.py evidence
python docs/reports/map/MAP2M/R6/pilot.py decisions
python docs/reports/map/MAP2M/R6/deliver.py images
python docs/reports/map/MAP2M/R6/deliver.py unresolved
python docs/reports/map/MAP2M/R6/deliver.py validate
```

Ne pas relancer `capture` ou `protocol` pour remplacer les références : ces commandes refusent un fichier existant. Les données nécessaires sont conservées dans R1–R5 ; aucun téléchargement n'est nécessaire pour reproduire R6. Les scripts n'écrivent que dans R6. `R5/query.py` reste inchangé.

## Ce qu'il ne faut pas faire

- Importer les CSV B/C comme des transferts approuvés, ou annexer le résidu `xFCC7B7` entier.
- Réabsorber le contrôle Vistule dans l'ajustement ou sélectionner un modèle sur son score, puis l'appeler contrôle final indépendant.
- Omettre l'indice vert 15 des largeurs de rivières ; le confondre avec le marqueur vert 0.
- Utiliser une rive moderne, un nom de ferme, un nom rouge de propriété ou une limite administrative comme preuve de frontière souveraine de 1776.
- Transformer l'absence du chenal natif en une impossibilité absolue de tracer une frontière politique : c'est la vérification physique locale qui manque.
- Agrandir Peendamm à une cellule entière sur le seul emplacement du moulin.

## Choix à soumettre au joueur, sans application automatique

**Wolgast :** une frontière continentale généralisée pourrait être préparée sur la grille actuelle, sans chenal distinct et sans nouvelle enclave de Peendamm. Elle devrait montrer les cellules proposées et les variantes, être étiquetée approximation politique et être expressément approuvée avant application. Ce n'est pas un passage automatique en classe A des 18 candidates.

**Bromberg :** ne pas généraliser tant que le segment souverain de la source n'est pas établi. Poursuivre seulement le tronçon méridional repéré, avec contrôle de sa datation et nouveaux homologues source→réel précis. Le nouveau diagnostic natif est réutilisable, pas une preuve historique de cette ligne.

**Alternative pour une restitution plus fine :** obtenir de nouveaux repères physiques documentés et identifiables sur les scans et dans la géographie réelle, et un contrôle natif local distinct. Ne pas relancer les mêmes optimisations sans nouvelle preuve. Une augmentation globale de la résolution du bitmap serait une refonte hors périmètre, et n'est ni recommandée ni entreprise ici.

La méthode complète de transfert n'étant pas démontrée, **pas d'extension R7 automatique**. Aucun nouveau test en partie n'est nécessaire pour une frontière inchangée. Une future installation devra recevoir ses propres contrôles statiques puis sa validation manuelle, sans emprunter celle de R3.
