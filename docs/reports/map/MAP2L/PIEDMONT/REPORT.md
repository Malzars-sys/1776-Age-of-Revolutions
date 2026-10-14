# Piémont-Sardaigne — membre du bloc, Piémont seul au registre

Intégré le 13 octobre 2026 à la demande explicite du joueur.

## Résultat

- `SAR` rejoint le bloc impérial initial une seule fois. Son pays entier est membre, y compris l'île de Sardaigne ; aucune division du pays, annexion ou vassalisation autrichienne.
- Seuls les neuf RGB de `STATE_PIEDMONT` actuellement détenus par SAR sont ajoutés au registre territorial de jure : `x1140E0`, `x11C061`, `x90C060`, `xA9397D`, `xAA6958`, `xACB500`, `xD080E0`, `xDA86EA`, `xF00544`.
- Les provinces génoises de cette même région, la Sardaigne, la Savoie, Nice et les autres possessions de SAR ne sont pas ajoutées par cette autorisation. Cette limitation de périmètre ne tranche pas leur statut historique.
- Le registre passe de 315 à **324 RGB**. Les 315 entrées précédentes sont conservées intégralement, y compris leurs bénéficiaires et justifications.
- La carte principale et celle du journal sont régénérées : **2 227 pixels piémontais** rejoignent le masque jaune. L'île de Sardaigne reste hors du masque et du modificateur territorial enregistré.
- Les droits de restitution, listes, votes potentiels, relations impériales et compteurs du journal incluent SAR. Aucun titre électoral supplémentaire n'est accordé.

## Protection et architecture

La baseline de ce lot est `BASELINE.json`. Avant intégration, le compilateur impérial a été comparé à tous ses fichiers runtime actuels : aucune divergence manuelle à écraser.

L'exception territoriale de SAR est explicite dans `tools/map2l_registry.py` et utilisée par le compilateur. Elle empêche que la seule appartenance au bloc enregistre toutes les terres du pays. `EXTENSION.json` décrit les neuf droits approuvés et permet aux contrôles belges de distinguer cet ajout autorisé d'une régression.

Seize fichiers runtime impériaux compilés ont changé, plus le masque principal et les assets générés du journal. Voir `IMPERIAL_FILES.json` et `VALIDATION.json` pour les chemins exacts. Les historiques de provinces, pays, populations, bâtiments, formations, gouvernements et traités restent inchangés. Le bitmap catégoriel n'est pas redessiné.

Le registre MAP2K et toutes les baselines précédentes sont inchangés. La baseline Franconie, prise avant cette extension, est aussi conservée : lors de la reprise de ce lot, ses contrôles devront tenir compte de cette extension approuvée, sans restaurer les anciens scripts ou annuler SAR.

## Vérifications

- **227/227** contrôles Piémont et régressions impériales passent.
- **310** contrôles belges actuels passent, avec conservation du lot initial et prise en compte explicite de l'extension piémontaise.
- **16/16** contrôles graphiques hors jeu passent ; compilation du helper HLSL réussie. Aucun pixel ajouté en dehors des neuf polygones approuvés.
- Inventaire gameplay complet identique à la baseline du lot : propriétaires, population mondiale de 835 804 980, cultures/religions, bâtiments, niveaux et unités inchangés.
- Aucune nouvelle référence invalide ou double attribution. HEAD et index Git identiques. Aucun commit, push, lancement de jeu ou changement du lanceur.

Ce sont des contrôles statiques et graphiques, **pas un test du moteur de Victoria 3**. Les incompatibilités politiques de départ déjà consignées restent un problème distinct.

## À inspecter dans une nouvelle partie

Redémarrer entièrement Victoria 3 avec le mod principal, puis commencer une nouvelle partie. Vérifier SAR parmi les membres du Saint-Empire, le Piémont jaune dans le mode de jure et dans le journal, et l'île de Sardaigne non marquée. L'ancien prototype séparé ne doit pas remplacer les fichiers du mod principal.

La Franconie reste en cours de calage ; cette extension ne constitue pas son découpage territorial.
