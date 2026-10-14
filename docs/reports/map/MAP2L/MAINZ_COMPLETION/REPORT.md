# MAP2L — Tauber–Jagst appliqué ; Erfurt–Eichsfeld non appliqué

Référence historique : 1er janvier 1776. Résultat **partiel de la demande** : le prolongement méridional est intégré et validé hors moteur ; le secteur septentrional reste bloqué sur son calage géographique. Ne pas présenter ce dossier comme l'achèvement de toutes les possessions de Mayence.

« Tauber–Jagst » désigne les vallées de deux rivières. « Erfurt–Eichsfeld » désigne les possessions séparées de Mayence autour d'Erfurt et dans l'Eichsfeld.

## 1. Modifications territoriales

Le raccord méridional reprend le modèle local et la carte détaillée de l'Oberstift conservés dans `MAINZ_ESTATES`, sans recommencer les recherches générales. Il représente les terres mayençaises autour de Buchen/Walldürn, Tauberbischofsheim et Krautheim/Ballenberg, ainsi que le petit fragment de Billigheim. Les contours sont des enveloppes à la résolution du jeu, pas un cadastre.

- `STATE_BADEN`, ID numérique 68 : **86 pixels BAD → KMZ**.
- `STATE_WURTTEMBERG`, ID numérique 67 : **11 pixels WUR → KMZ**, répartis entre le raccord principal (6) et Billigheim (5).
- **9 nouveaux RGB**, `xEDA600` à `xEDA608` ; **129 pixels recolorés**. Une recoloration peut séparer deux fragments restant au même propriétaire : elle n'est pas toujours un transfert de souveraineté.
- Les State_ID demeurent partagés entre plusieurs propriétaires. Le registre passe de 384 à **393 RGB**.
- L'étendue impériale jaune reste exactement **62 516 pixels**, car les deux parents étaient déjà impériaux. La carte principale et celle du journal sont régénérées ; les textures restent identiques lorsque cette étendue ne change pas.

Les enclaves figurées comme non mayençaises sont exclues, notamment Schöntal et les franges de Hardheim. Les résidus non réattribués ne sont pas certifiés historiquement corrects. Les micro-enclaves invisibles ne sont pas agrandies. Aucun territoire ni propriétaire au nord n'est modifié.

## 2. Sources et calage méridional

Image réutilisée : `../MAINZ_ESTATES/OBERSTIFT_1789_COMPARISON.jpg`, empreinte conservée, [atlas détaillé présenté par l'Historisches Lexikon Bayerns](https://www.historisches-lexikon-bayerns.de/Lexikon/Datei:Artikel_45154_bilder_value_4_oberstift2.jpg). C'est une comparaison de 1789, non une preuve automatique pour 1776, et une image documentaire sous copyright Bayerischer Schulbuchverlag, non un asset runtime.

Les continuités sont vérifiées séparément : [Buchen](https://www.buchen.de/ueber-buchen/stadtgeschichte/kurze-geschichte-der-stadt.html), [Tauberbischofsheim](https://www.tauberbischofsheim.de/start/stadt%20_%20politik/stadtgeschichte.html), [Krautheim](https://www.krautheim.de/stadt-wirtschaft/stadtteile/krautheim) et [Billigheim](https://www.billigheim.de/de/gemeinde-billigheim/die-gemeinde-im-portrait/billigheim). Le devenir postérieur en 1803/1806 n'est pas projeté sur les propriétaires de départ.

[Hardheim](https://www.hardheim.de/seite/de/cns501a31b64c702d/032%3A200/-/Geschichte.html) est sous souveraineté würzbourgeoise depuis 1656 ; ne pas le traiter comme une acquisition mayençaise ni comme une seigneurie chevaleresque indépendante. [Osterburken](https://www.leo-bw.de/en-GB/detail-gis/-/Detail/details/ORT/labw_ortslexikon/6153/ort) est bien mayençais : le petit trou tracé au nord-ouest ne constitue pas une attribution de la ville elle-même à un autre souverain. Deux identifications de minuscules poches sur le scan restent explicitement non certifiées dans le tracé ; elles sont conservées hors des nouvelles acquisitions, sans invention d'un nouveau titulaire.

La matrice locale du lot précédent est réutilisée. Trois contrôles indépendants supplémentaires de la **carte source**, non utilisés dans l'ajustement, donnent des écarts équivalents de 0,828 pixel pour Buchen, 0,872 pour Tauberbischofsheim et 0,855 pour Krautheim. Ils vérifient la cohérence du scan vers les coordonnées locales ; ce ne sont pas des preuves indépendantes d'une projection GPS exacte de Victoria 3.

Un contrôle initial au pixel strict a échoué pour Tauberbischofsheim : le symbole se projette à `x=4313.999949`, à une limite de cellule. Le tracé et les propriétaires **n'ont pas été élargis ni modifiés pour faire passer ce test**. Le validateur contrôle maintenant l'appartenance du symbole au polygone continu, puis sa représentation par une cellule mayençaise à moins de 0,75 pixel de son centre. L'approximation de rasterisation est indiquée dans le résultat ; aucun centre urbain n'est présenté comme un point cadastral exact.

## 3. Blocage précis pour Erfurt–Eichsfeld

Sources désormais conservées :

- Feuillet complet de [Schreiber, Eichsfeld et territoire de Mühlhausen](https://commons.wikimedia.org/wiki/File:J.G.Schreiber_Eichsfeld.jpg), décrit comme 1749, et sa légende séparée. Ne pas confondre ce feuillet photographié avec le volume Rumsey catalogué vers 1790.
- [Homann, territoire d'Erfurt, bibliothèque de Trente, CBT 5874825](https://commons.wikimedia.org/wiki/File:Nova_territorii_Erfordiensis_in_suas_praefecturas_accurat%C3%A8_divisi_descriptio_-_CBT_5874825.jpg), exemplaire du début du XVIIIe siècle dont l'édition exacte n'est pas certifiée ici. Le catalogue RCIN de 1762 est une autre notice ; son image n'a pas été récupérée et sa date n'est pas attribuée abusivement à l'exemplaire de Trente.

La souveraineté mayençaise d'Erfurt en 1776 est corroborée par la [ville de Mainz](https://www.mainz.de/angebote-entdecken/partnerstaedte/erfurt), celle de l'Eichsfeld par les archives et la [chronologie de Duderstadt](https://www.duderstadt.de/portal/seiten/stadtgeschichte-900000069-25420.html). Ce n'est donc pas le souverain général qui manque, mais une correspondance locale fiable entre ces limites et les RGB du jeu. Le territoire de la ville libre de Mühlhausen doit rester séparé.

L'affine géographie → jeu essayée avec Hannover, Magdeburg et le repère **rural** Erfurt échoue aux contrôles indépendants : **18,64 pixels** à Wernigerode et **9,34** à Leipzig. Le modèle utilisant seulement des repères de type ville (Hannover/Magdeburg/Frankfurt) présente encore **4,39** pixels à Brunswick et **4,22** à Dresden ; il place Erfurt à **15,42 pixels** du locator rural portant ce nom. Ces résultats ne prouvent pas à eux seuls un bug du jeu : les labels ruraux/miniers ne sont pas des points GPS établis.

Résultats et matrices : `NORTHERN_CALIBRATION_ASSESSMENT.json`, statut **REJECTED_NOT_APPLIED**. Aucun seuil n'a été relâché et aucune des deux matrices n'est installée comme frontière. Il faut encore établir des correspondances géographiques locales indépendantes, par exemple sur des points physiques identifiables dans le bitmap/réseau hydrographique, puis revoir séparément les enclaves d'Erfurt (Vargula, Mühlberg, Tonndorf, etc.). Des cartes historiques seules ne permettent pas de deviner leur position dans le raster.

## 4. Fichiers modifiés

Runtime territorial : `map_data/provinces.png`, `map_data/province_terrains.txt`, `map_data/state_regions/00_west_europe.txt`, `common/history/states/00_states.txt`, `common/history/pops/00_west_europe.txt` et `common/history/buildings/98_build_start_1776_world_redistribution.txt`.

Runtime impérial recompilé : `common/scripted_triggers/1776_imperial_constitution.txt`, `common/scripted_effects/1776_imperial_constitution.txt`, `common/power_bloc_identities/1776_imperial_federation.txt`, ainsi que les localisations anglaises/françaises `1776_imperial_feedback_l_*` et `1776_imperial_repairs_l_*`. Les autres fichiers compilés sont contrôlés identiques, pas réécrits arbitrairement.

Registre actif `../IMPERIAL_DE_JURE_REGISTRY.json`, manifeste `REGISTRY_MIGRATION.json`, baseline immuable, tracé, alignement, candidats, aperçus, allocations et validations dans ce dossier. Nouveaux outils : `tools/map2l_mainz_completion.py` et `tools/validate_map2l_mainz_completion.py`. Le générateur commun permet de sélectionner les ancrages explicites du lot ; le registre et le validateur cumulatif incluent ce manifeste nommé, sans découverte automatique de dossiers.

## 5. Conservation et résultats

Population mondiale : **835 804 980**, inchangée. **68 095 habitants** sont réaffectés de BAD à KMZ et **10 849** de WUR à KMZ, soit **78 944** au total. Chaque profil, culture, religion et attribut reste conservé par région. Les pondérations de superficie sont une approximation de gameplay, pas des données de recensement.

Un niveau d'élevage passe à une subdivision KMZ de Bade ; son propriétaire économique privé reste inchangé. Les niveaux totaux, méthodes de production, réserves et attributs des bâtiments sont conservés. Armées, flottes, recrutement, capitales, gouvernements, ressources, ID numériques et locators ne sont pas déplacés. Les tests comparent les modifications au snapshot de ce lot, sans effacer les changements antérieurs des collaborateurs.

- Nouveau lot : **414/414** contrôles statiques.
- Lot Main–Spessart/Bergstraße, validation cumulative : **539/539**.
- Lot Mayence–Palatinat initial, validation cumulative : **553/553**.
- Neckar : **438/438**.
- Franconie : **555/555**.
- Belgique : **315/315**.
- Piémont : **232/232**, extension de 2 227 pixels conservée.
- Carte principale : **16/16 hors moteur**, masque exact, DDS sans perte et helper HLSL compilé.

Les **44 RGB doublement attribués et 12 erreurs de référence préexistants** sont conservés exactement ; aucune nouvelle régression de ces types n'est ajoutée. Il ne s'agit pas d'un chargement réel dans Victoria 3. Le test en jeu reste différé jusqu'à la fin des lots impériaux demandés. Aucun commit, staging, merge, rebase ou push ; HEAD et index Git contrôlés inchangés.

## 6. ColGrep et ressources

Commande de recherche exécutée depuis la racine : `C:/Users/simeo/.cargo/bin/colgrep.exe --agent`, avec une question demandant de localiser les dossiers Tauber–Jagst/Erfurt–Eichsfeld dans `./docs`, sans modifier les fichiers ni décider des propriétaires. **Un appel réussi**, code de sortie 0, **85,43 secondes** mesurées autour de la commande entière ; une première invocation a échoué en 0,10 seconde sur une restriction d'accès, avant la recherche.

Les trois pistes retournées ont été vérifiées : `MAINZ_ESTATES/GEOGRAPHIC_EVIDENCE.md:7`, `MAINZ_ESTATES/TRACING.json:28` et `MAINZ_ESTATES/ALIGNMENT.json:54`. Elles renvoyaient au dossier méridional déjà connu, **pas** à un calage exploitable d'Erfurt/Eichsfeld. L'utilité du 2B est donc limitée pour cette passe. La sortie capturée ne fournit pas de bannière GPU/llama.cpp ; le backend effectif ne peut pas être attesté séparément et aucun modèle ni réglage n'est changé.

Les recherches exactes sont faites avec `rg`, les relevés CSV/JSON et les lectures ciblées. Leur comptage complet, le temps total de recherche classique et les tokens Codex par opération ne sont pas instrumentés ; aucune économie exacte ou comparaison A/B n'est revendiquée. Les images et les coordonnées ne sont pas confiées au modèle sémantique pour décider des frontières. La source méridionale et le générateur ont été réutilisés ; les cartes septentrionales sont de nouveaux compléments ciblés au manque identifié dans les dossiers.

Actualisation incrémentale de l'index : voir `COLGREP_REFRESH.md`. Ce n'est pas un nouvel appel à l'agent 2B et aucune reconstruction volontaire ni changement d'intégration n'est effectué.
