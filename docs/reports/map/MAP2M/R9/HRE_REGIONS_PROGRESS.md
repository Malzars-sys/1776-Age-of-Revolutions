# Avancement territorial du SERG — inventaire R9

Les statuts portent sur les sous-secteurs nommés, pas sur des régions entières implicitement certifiées. VALIDATED signifie seulement validation manuelle des modifications inspectées, sans test moteur automatisé ni certification historique. IMPLEMENTED signifie installé et statiquement contrôlé, sans reçu manuel spécifique suffisant. PARTIAL conserve les portions non résolues. RESEARCHED_ONLY ne signifie pas NOT_STARTED : une recherche existe, mais pas une véritable correction dédiée. AUDITED_ONLY décrit le contrôle R9 sans transfert. UNKNOWN signale les limites du corpus.

Le CSV couvre tous les State_ID du registre impérial actif, les sous-lots différenciés et le contexte extérieur prusso-polonais. Une ligne automatique « autre secteur enregistré » est volontairement prudente : elle ne transforme pas une attribution gelée de gameplay en travail cartographique achevé. Les territoires institutionnellement mixtes ne sont pas déclarés intégralement impériaux du seul fait de leur State_ID.

## Comptage des lignes, non des provinces

- AUDITED_ONLY : 4
- IMPLEMENTED : 7
- PARTIAL : 4
- RESEARCHED_ONLY : 13
- UNKNOWN : 2
- VALIDATED : 8

## Sous-secteurs et preuves

### Belgique et Pays-Bas autrichiens : secteurs inspectés

VALIDATED — Liège, Stavelot-Malmedy et subdivisions belges ; 37 nouveaux RGB du lot belge.

Validation : MAP2L/RUNTIME_USER_VALIDATION.json.

Reste ouvert : Bouillon, Saint-Hubert, Maastricht et franges non inspectées restent distincts du noyau validé.

Rapports : MAP2L/BELGIUM.

### Franconie : noyaux des deux passes inspectées

VALIDATED — Ansbach-Bayreuth, Bamberg, Würzburg, Nuremberg, Eichstätt et Cobourg ; continuation de185cellules.

Validation : MAP2L/RUNTIME_USER_VALIDATION.json.

Reste ouvert : Ne valide ni toutes les franges bavaroises ni chaque petite juridiction.

Rapports : MAP2L/FRANCONIA;MAP2L/FRANCONIA_CONTINUATION.

### Franconie et Bavière : juridictions résiduelles

PARTIAL — Noyaux précédents conservés ; aucun nouveau transfert R9.

Validation : Aucune attestation exhaustive des résidus.

Reste ouvert : Restes provisoires BAV, petites villes et possessions épiscopales périphériques.

Rapports : MAP2L/FRANCONIA/UNRESOLVED.csv;MAP2L/FRANCONIA_CONTINUATION/REPORT.md.

### Rhin–Westphalie : noyaux inspectés

VALIDATED — Neckar palatin, Münster, Paderborn et Juliers-Berg ;1081cellules du lot rhénan.

Validation : MAP2L/RUNTIME_USER_VALIDATION.json.

Reste ouvert : Validation des seules zones inspectées ; petits États et limites non tracées restent ouverts.

Rapports : MAP2L/RHINE_CENTRAL;MAP2L/RHINE_WESTPHALIA.

### Mayence–Rheingau–Aschaffenburg–Bergstraße–Tauber-Jagst

IMPLEMENTED — Lots de noyaux et raccords appliqués ; Erfurt exclue.

Validation : Pas de reçu nommant exhaustivement ces trois lots ; ne pas étendre une validation voisine.

Reste ouvert : Quelques franges et minuscules enclaves non certifiées.

Rapports : MAP2L/MAINZ_PALATINATE;MAP2L/MAINZ_ESTATES;MAP2L/MAINZ_COMPLETION.

### Erfurt–Eichsfeld

RESEARCHED_ONLY — Aucun transfert du tracé rejeté.

Validation : Aucune.

Reste ouvert : Repères physiques locaux non homologués ; translation7.20px refusée et non appliquée.

Rapports : MAP2L/ERFURT_EICHSFELD;MAP2L/ERFURT_EICHSFELD/LOCAL_RECALIBRATION.

### Minden : noyau restauré

IMPLEMENTED — 76cellules HAN vers PRU et quatre nouveaux RGB.

Validation : Exclusion explicite dans le premier reçu ; aucun reçu autonome de Minden retrouvé.

Reste ouvert : Ravensberg et franges ; ne pas promouvoir par une attestation du lot voisin.

Rapports : MAP2L/MINDEN_RAVENSBERG.

### Cologne : duché de Westphalie et Vest

IMPLEMENTED — 84cellules PRU vers KCL ; EDAB00-07.

Validation : Pas de reçu nommant spécifiquement ce sous-lot.

Reste ouvert : Raccords périphériques non certifiés ; aucun agrandissement à toute la Westphalie.

Rapports : MAP2L/DUCHY_WESTPHALIA.

### Osnabrück–Niederstift–Lingen–Tecklenburg : noyaux inspectés

VALIDATED — WPO159cellules, WPM265, PRU65 ;489transferts.

Validation : MAP2L/RUNTIME_USER_VALIDATION_RHINE_SWABIA.json.

Reste ouvert : Damme-Neuenkirchen et franges non certifiées.

Rapports : MAP2L/RHINE_WESTPHALIA_COMPLETION.

### Petites juridictions de Westphalie et Nassau

PARTIAL — Corrections principales voisines installées ; aucune nouvelle correction R9.

Validation : Pas de validation exhaustive de ces juridictions.

Reste ouvert : Bentheim, Steinfurt, Rietberg, Corvey, Essen-Werden, Dortmund, branches Nassau et Gueldre.

Rapports : MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv.

### Souabe : première passe inspectée

VALIDATED — Premiers noyaux impériaux souabes.

Validation : MAP2L/RUNTIME_USER_VALIDATION_RHINE_SWABIA.json.

Reste ouvert : Ne certifie pas les dépendances minuscules non tracées.

Rapports : MAP2L/SWABIA.

### Souabe : continuation

IMPLEMENTED — Continuation appliquée avant les passes de finition.

Validation : Aucune promotion automatique : exclusions des reçus suivantes conservées.

Reste ouvert : Portée manuelle exacte non fournie pour cette continuation entière.

Rapports : MAP2L/SWABIA_CONTINUATION.

### Souabe : finition des grands noyaux

VALIDATED — Salem, quatre branches Waldburg, Fürstenberg, Ellwangen, Constance/Augsbourg préservés.

Validation : MAP2L/RUNTIME_USER_VALIDATION_SWABIA_FINISH.json.

Reste ouvert : Condominia, propriétés éloignées et offices périphériques.

Rapports : MAP2L/SWABIA_FINISH.

### Souabe : villes libres et dernière passe majeure

VALIDATED — Augsbourg et Kempten une cellule chacune ; autres villes et noyau de Weingarten.

Validation : MAP2L/RUNTIME_USER_VALIDATION_SWABIA_COMPLETION.json.

Reste ouvert : Abstractions urbaines approuvées, pas mesure des territoires historiques complets.

Rapports : MAP2L/SWABIA_COMPLETION.

### Montbéliard et quatre seigneuries

RESEARCHED_ONLY — Aucun transfert du comté.

Validation : Aucune.

Reste ouvert : Frontière du comté distincte des seigneuries françaises après1748 ; ne pas rétroprojeter1786.

Rapports : MAP2L/SWABIA_FINISH/UNRESOLVED.csv;MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv.

### Milanais–Crémonais

IMPLEMENTED — 64cellules VEN vers AUS et continuité terrestre rétablie.

Validation : Aucun reçu manuel spécifique retrouvé.

Reste ouvert : Autres frontières lombardes non certifiées par cette liaison.

Rapports : MAP2L/MILAN_CREMONESE.

### Piémont : intégration institutionnelle et registre

IMPLEMENTED — SAR membre du bloc ; neuf RGB piémontais enregistrés ; pas de découpage nouveau.

Validation : Pas de reçu de test moteur spécifique.

Reste ouvert : Savoie, Nice et Sardaigne non ajoutées au registre par ce lot.

Rapports : MAP2L/PIEDMONT.

### Poméranie suédoise : noyau antérieur MAP2L

VALIDATED — 341cellules du noyau côtier attribuées à SWE.

Validation : MAP2L/RUNTIME_USER_VALIDATION_PRUSSIAN_CORE.json.

Reste ouvert : Ne valide pas automatiquement R2–R9.

Rapports : MAP2L/PRUSSIAN_BORDERS.

### Peene R8 et Wolgast R9

IMPLEMENTED — R8 +41 puis R9 +2 ; SWE400cellules ; clôture pratique avec Peendamm abstrait.

Validation : Aucune validation manuelle R8 ou R9 communiquée.

Reste ouvert : Précision géodésique et représentation de tous les bâtiments non certifiées.

Rapports : MAP2M/R8;MAP2M/R9/WOLGAST_CORRECTION.md.

### Prusse–Pologne et Thorn, contexte extérieur au SERG

PARTIAL — Noyau Bromberg85PRU conservé ; aucun nouveau transfert R9.

Validation : Référence R3 acceptée dans R4 ; ne couvre pas les portions non corrigées.

Reste ouvert : Limites des quatre districts, Inowrocław, Thorn et écart de localisation du noyau de Bromberg.

Rapports : MAP2M/R2;MAP2M/R3;MAP2M/R7;MAP2M/R8/THORN_AUDIT.md;MAP2M/R9/PRUSSIA_POLAND_AUDIT.md.

### Brandebourg et Neumark

AUDITED_ONLY — Aucun découpage territorial R9 ; économie conservée.

Validation : Test des six niveaux d'armes distinct de la certification des frontières.

Reste ouvert : Franges et biens locaux non démontrés RGB par RGB.

Rapports : MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md;MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Magdebourg–Halberstadt–Anhalt et Brunswick

AUDITED_ONLY — Aucun nouveau transfert R9.

Validation : Aucune validation territoriale détaillée retrouvée.

Reste ouvert : Limites des duchés prussiens et principautés d'Anhalt, enclaves du Harz.

Rapports : MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md;MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Frise orientale / Emden

AUDITED_ONLY — Aucun transfert R9.

Validation : Aucune.

Reste ouvert : Emden natif dans xF9DCA2 HAN ; souveraineté prussienne1744 établie, contour du RGB versus Jever et voisins non arbitré.

Rapports : MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md.

### Silésie, Glatz et frange lusacienne

AUDITED_ONLY — Économie conservée ; aucun transfert territorial R9.

Validation : Pas de certification des frontières silésiennes.

Reste ouvert : Partition1742-1743, Lusace avant1815, x71E080 xF0E080 x9061E0 et scopes hérités.

Rapports : MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/SILESIA_READING.md;MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md.

### Wismar–Poel–Neukloster

RESEARCHED_ONLY — Aucune correction historique dédiée ; MEC et MST seuls propriétaires actuels.

Validation : Aucune.

Reste ouvert : Possessions suédoises absentes ; frontières propres aux trois ensembles à établir.

Rapports : MAP1/MAP1_CASE_DOSSIERS/R2_NORTHERN_CENTRAL_EASTERN_EUROPE-0132.md.

### Saxe et principautés thuringiennes hors Erfurt

RESEARCHED_ONLY — Pas de passe dédiée dans STATE_SAXONY ; ajout franconien à Cobourg ne suffit pas.

Validation : Aucune.

Reste ouvert : COB MEI SAX SCW WEI présents ; subdivisions historiques et sens de SCW à vérifier.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Hesses, Waldeck et branches de Nassau hors lots rhénans

PARTIAL — Mayence et Neckar corrigés localement ; autres anciens propriétaires conservés.

Validation : Ne pas étendre le reçu du Rhin à tous les bailliages hessois.

Reste ouvert : Branches dynastiques et enclaves, pas de Nassau unifié1806.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv;MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv.

### Holstein, Schleswig et principauté-évêché de Lübeck

RESEARCHED_ONLY — Pays natifs HOL SCH LUB ; pas de redécoupage dédié identifié.

Validation : Aucune.

Reste ouvert : Règlement1773 et distinction Holstein impérial / Schleswig danois ; ville de Lübeck versus Eutin.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_AUSTRIA

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_BOHEMIA

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_ELBE

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_EMILIA

UNKNOWN — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : .

### Autre secteur enregistré : STATE_ISTRIA

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_SLOVENIA

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_SOUTH_TYROL

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_STYRIA

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

### Autre secteur enregistré : STATE_TUSCANY

UNKNOWN — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : .

### Autre secteur enregistré : STATE_TYROL

RESEARCHED_ONLY — Pas de passe dédiée identifiée par le corpus de migrations MAP2L et R9.

Validation : Aucune attestation régionale retrouvée.

Reste ouvert : Statut historique et frontières à qualifier ; présence au registre seule ne démontre pas une reconstruction.

Rapports : MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv.

## Prochain lot recommandé

Wismar–Poel–Neukloster, STATE_MECKLENBURG (75), exclusivement. La recherche R2-0132 établit le problème, et la propriété actuelle ne comporte aucun SWE (MEC1295, MST329). Aucun lot territorial dédié à ces possessions suédoises n’a été identifié. Ce choix ne signifie ni reprise de toute la Poméranie ni refonte de tout le Mecklembourg. Voir NEXT_HRE_REGION_RECOMMENDATION.md. Aucun travail de ce prochain lot n’est lancé.

Les acquisitions postérieures, les approximations restées ouvertes en Silésie, la Frise orientale et Thorn ne sont pas masquées par cette recommandation. Elles restent au registre des anomalies R9.
