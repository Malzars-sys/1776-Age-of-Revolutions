# NORDIC-01 — Scandinavie et Finlande

**29 octobre2026 ; référence1er janvier1776. IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Autorisation directe dans USER_REQUEST.json. Le joueur déclare le test africain groupé passé et l'Afrique terminée pour le moment ; reçu borné AFRICA_USER_ACCEPTANCE.json. Cette acceptation lève la transition, sans inventer durée/version/rechargement ni certification historique totale.

## Corrections installées

**Cinq RGB existants, trois fichiers ciblés ; aucun pixel redessiné, nouveau TAG ou territoire SERG.**

| Secteur | RGB | Avant | Après | Portée |
|---|---|---|---|---|
| Savonlinna/Nyslott | xB81268 | SWE | RUS | Cession1743 ; polygone natif entier, pas périmètre cadastral du château |
| Sud du Varangerfjord, Neiden/Pasvik | x2495FE, xFEC50D, x7005BB, x6480A4 | DENNOR | RUS | Approximation de la juridiction russe dans les districts communs, pas annexion exclusive ni suppression attestée des droits danois-norvégiens |

Les deux ensembles touchent directement un territoire russe conservé. La côte nord du Varangerfjord reste danoise-norvégienne. La majorité de la Finlande, Åland, la Suède proprement dite et Gotland restent suédoises ; la Vieille Finlande demeure russe. Norvège, Danemark, Islande et Féroé restent dans DENNOR. Les contacts du Schleswig-Holstein, Poméranie/Wismar/Poel sont réservés au SERG. Les colonies et le Groenland ne sont pas repris sous cette autorisation.

## Populations et capacités

Monde **837,328,654 → 837,328,654**, delta0. Kuopio : SWE160946→155916 et RUS0→5030. Norvège septentrionale : DENNOR233686→226658 et RUS0→7028. Total réaffecté12058 ; aucune assimilation ni variation mondiale, cohortes culture/religion/profession conservées.

La ventilation par1/32 et4/133 des pools donne uniquement une allocation technique, arrondie séparément par cohorte ; ce n'est pas une estimation démographique1776. Les populations héritées, notamment majoritairement norvégiennes dans le secteur septentrional, restent des proxies et ne certifient pas le peuplement des siida. Les effectifs historiques fins sont différés.

Institutions, lois, capitales nationales, technologies, PM, niveaux bâtis, recettes et unités inchangés. Aucun nouveau pays à initialiser. Le seul centre agricole natif nommé Savonlinna change de propriétaire territorial ; les bâtiments existants restent aux portions conservées. Les hubs et ressources partagés de région moteur demeurent un compromis à observer ; aucune rentabilité ni localisation physique exacte n'est attestée.

## Sources et incertitudes

[SOURCES.md](SOURCES.md) distingue documents réellement lus, données, interprétation et lacunes. Carte Wetterstedt1775, Merovuo2017 p286–289 et fig1, Archives nationales finlandaises, NOU1994:21 §3.5 et convention1826. Savonlinna : contour natif plus large que le rayon historique ; poches contestées de Kerimäki non représentées. Nord : le moteur a un propriétaire unique, ne reproduit pas les fiscalités superposées ou tous les usages sámi ; limite occidentale/siida approximative. Pas de nouveau TAG artificiel ni frontière arbitraire au pixel. Courbes volontairement non lissées.

## Contrôles et concurrence

**33/33 contrôles statiques réussis**, VALIDATION.json. Syntaxe, patch exact, extérieur des scopes inchangé, cinq affectations uniques, connexion directe à la Russie, conservation des cohortes/totaux et Git/index. La première exécution28/30 reste INITIAL_VALIDATION.json : deux échecs venaient de la comparaison avec la capture d'avant l'installation indienne concurrente ; ils n'ont pas été masqués par une restauration. La normalisation des clés RGB minuscules a ensuite été corrigée dans le comparateur des préimages. Les entrées et sorties du pair sont vérifiées exactement, sans exemption générale.

Le contrat technologique courant SWE/DENNOR/RUS a également été exécuté (TECH_CURRENT.json). **FAIL_STATIC hérité**, pas validation de leurs profils historiques : trois demandes de lois sans gate par pays pour SWE/DENNOR et gate de recrutement des cuirassiers russes. Les mêmes entrées nationales, lois, technologies et unités sont inchangées dans notre lot ; aucun grant n'est distribué pour les masquer. Deux avertissements de ressources et les réserves historiques restent séparés des erreurs de frontière. Ce contrat ne prouve ni loi effectivement active ni panne d'unité existante.

Le lot **DURRANI_PUNJAB_1776/DP-02** a installé81 réattributions et42 sorties pendant cette passe. Manifestes, préimages et sorties relus ; états nordiques identiques dans ses versions, puis notre patch appliqué sur son état courant. Dix fichiers fonctionnels existants modifiés extérieurement sont rapprochés de ses reçus, nouvelles sorties également contrôlées. EXTERNAL_COMPOSITION_REVIEW.json conserve les preuves. Aucune écriture de ses fichiers ou suivis. Afrique entière, Amériques, Arabie, SERG, TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie préservés. Aucun Git/vanilla/SERG écrit.

## Suite

Cette passe livre les deux corrections défendables trouvées dans les19 régions et contacts examinés. Carte de repères CARTE_REPERES.png. Contrôle moteur groupé de la Scandinavie encore NOT_RUN : nouvelle partie1776, propriétaire des deux repères, Åland et Finlande suédoises, côte nord du Varangerfjord DENNOR, population/chargement des portions RUS, puis simulation et sauvegarde/rechargement lors du test groupé. Pas de demande de test par sous-lot.

L'Afrique est acceptée pour le moment par le joueur. Extension documentaire WORLD1.0.2 pour la Scandinavie hors de l'ancien registre à320 critères : aucune progression artificielle ni nouveau dénominateur SERG. Le calcul historique WORLD reste10/320 (3,13%) ; aucun critère V entier nouveau certifié à partir d'un retour global sans détails.
