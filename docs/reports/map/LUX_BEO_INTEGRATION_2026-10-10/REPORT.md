# Luxembourg → Pays-Bas autrichiens, départ de 1776

Décision explicite de l'utilisateur, appliquée le 10 octobre 2026. Ce lot ne
traite aucune autre frontière et ne réinterprète pas les conclusions historiques
des autres dossiers.

## Changements

- `xD001A0` rejoint BEO dans `STATE_WALLONIA`. Le bloc de création d'État LUX
  disparaît ; la géométrie RGB, les homelands et les revendications restent
  identiques. LUX n'a plus de territoire au départ.
- Les **137 881 habitants** sont déplacés dans le bloc de population BEO sans
  changer aucun des quatre `create_pop` : 81 113 Wallons, 56 156 Allemands du
  Nord explicitement catholiques, 447 autres Allemands du Nord et 165 Ashkénazes.
  Les religions implicites restent celles des cultures définies dans le jeu ;
  aucune conversion, assimilation ou duplication n'est ajoutée.
- Population initiale déclarée de BEO : **2 770 000 → 2 907 881**. Population
  wallonne de BEO : **961 518 → 1 099 399**.
- Les deux déclarations préexistantes d'administration luxembourgeoise,
  d'un niveau chacune, sont rattachées à BEO dans leurs fichiers respectifs.
  Leurs niveaux, réserves et PM restent identiques. Aucun autre bâtiment ne
  change. Les fichiers de base et de redistribution contenaient déjà ces deux
  déclarations : leur cumul effectif dans le moteur n'est pas démontré par un
  simple comptage des scripts. Ce lot ne modifie pas leur logique de chargement.
- `Luxemburger_Miliz`, ses deux unités d'infanterie irrégulière, son unité
  d'infanterie de ligne et son général sont déplacés dans le bloc militaire BEO.
  Même quartier général, même recrutement en Wallonie, mêmes scopes sauvegardés.
  BEO passe ainsi de **12 à 15 unités permanentes déclarées**, sans ajout global
  d'unités ni modification des conscrits.
- Suppression de la relation initiale NET–LUX et de l'ancien traité de transit
  PRU–LUX, désormais sans signataire existant. Aucun traité de remplacement.
- BEO conserve exactement sa dépendance `crown_land` envers AUS. Aucune union
  personnelle ou nouvelle dépendance luxembourgeoise.
- La définition du tag LUX, son historique protégé par `?=`, les événements
  futurs et les conditions d'achievement protégées par `exists` sont conservés.
  Ils ne créent pas un Luxembourg au départ. Les lois, technologies et dirigeants
  de BEO ne sont pas remplacés par ceux de LUX.

## Fichiers de gameplay modifiés (7)

1. `common/history/states/00_states.txt`
2. `common/history/pops/00_west_europe.txt`
3. `common/history/buildings/00_west_europe.txt`
4. `common/history/buildings/98_build_start_1776_world_redistribution.txt`
5. `common/history/military_formations/00_military_formations_europe.txt`
6. `common/history/diplomacy/00_relations.txt`
7. `common/history/treaties/00_historical_treaties.txt`

## Validations

Le validateur `tools/validate_luxembourg_beo_integration.py` compare le résultat à
un instantané du **dossier de travail réel avant cette intervention**, et non à
HEAD : les modifications locales antérieures font partie du socle à préserver.
`BASELINE.json` conserve les originaux des sept fichiers et leurs empreintes ;
`VALIDATION.json` contient le résultat détaillé.

- Parsing structurel des sept historiques modifiés.
- Comparaison de toutes les attributions de provinces : seul le propriétaire
  de `xD001A0` change ; ni ajout ni suppression de RGB.
- Conservation exacte de tous les groupes de population, avec substitution de
  propriétaire LUX → BEO uniquement ; delta BEO exactement +137 881.
- Conservation des déclarations de bâtiments et de tous leurs paramètres.
- Conservation des unités, formations, personnages militaires et références.
- Absence de référence initiale non protégée à LUX dans les autres historiques.
- Conservation du pacte AUS–BEO ; absence de dépendance LUX.
- Empreintes de tous les fichiers préexistants comparées : seuls les sept
  historiques autorisés changent, hors le nouveau validateur de ce lot.
  Les **31 fichiers MAP-1C** sont conservés à l'identique, ainsi que MAP-1B et
  les modifications locales préexistantes.
  Parmi eux, 30 sont dans l'instantané de ce lot ; l'archive `cities1000.zip`,
  ignorée par Git, est vérifiée contre l'empreinte indépendante conservée avant
  le précédent correctif d'infrastructure (31/31 fichiers identiques).
- Les 10 scénarios de régression du correctif d'infrastructure précédent passent
  également (tests du modèle des scripts, pas exécution du moteur).
- `git diff --check` : aucune erreur d'espacement. Aucun commit, merge ou push.

Des attributions RGB dupliquées et des déclarations de bâtiments répétées
existaient déjà hors de ce transfert. Elles ne sont ni masquées ni réparées :
les attributions initiales sont comparées en multiensemble pour conserver ces
anomalies sans les confondre avec une nouvelle modification de frontière.

### Chargement en jeu : à confirmer

**Aucun test natif de chargement n'a été exécuté dans cette intervention.** Le jeu
n'était pas lancé et le contrôle des applications natives n'est pas disponible
ici. Les validations statiques ne prouvent pas l'acceptation par le moteur.

Pour valider, lancer une **nouvelle partie au 1er janvier 1776**, et non une
sauvegarde existante : vérifier BEO propriétaire de Luxembourg, LUX absent,
BEO sujet autrichien, population initiale de 2 907 881, formation luxembourgeoise
de trois unités et administration en Wallonie. Vérifier le journal d'erreurs
fraîchement généré pour les scopes LUX/BEO/Wallonie, les bâtiments et formations.
La population évoluant dès que le temps s'écoule, mesurer le total en pause.

## Règle cartographique retenue pour les prochains lots

La nouvelle instruction de l'utilisateur remplace l'exigence de justification
géographique au pixel près. Les anciennes propositions MAP-1B/MAP-1C restent
des preuves consultables, pas des décisions à intégrer automatiquement ; la
proposition d'union personnelle luxembourgeoise est expressément remplacée par
la présente intégration à BEO.

- Privilégier des frontières historiquement crédibles à l'échelle de Victoria 3.
- Documenter les approximations raisonnables, sans anachronisme majeur ; réserver
  les superpositions détaillées aux désaccords importants.
- Conserver par défaut les attributions coloniales plausibles, mais distinguer
  revendications et administration effective lorsque les souverainetés locales
  sont documentées.
- Réutiliser les neuf recherches régionales et les corrections valables de
  georg3mx ; préserver les travaux et changements locaux.
- Intégrer par lots cohérents, avec conservation des populations, bâtiments et
  unités, puis validation de chargement. Aucun autre lot n'est appliqué ici.
