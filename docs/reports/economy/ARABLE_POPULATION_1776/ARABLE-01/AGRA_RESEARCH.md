# Agra — ce qui est établi et ce qui ne l'est pas

**Complément historique du 29 octobre 2026, après retour du joueur :** [contrôle géographique et comparaison avec les districts de 1911](AGRA_HISTORICAL_REVIEW/REPORT.md). La valeur installée provient bien d'une allocation provisoire, pas d'une estimation locale de 1776. Le contrôle fournit un indice de surestimation, mais aucun chiffre de remplacement historiquement établi. Le joueur confirme la disparition de la famine après le correctif ; cette attestation est bornée à cet effet, sans homologation démographique. Les analyses et mesures initiales ci-dessous restent un avant-correction.

**Mise à jour du 29 octobre 2026 :** le joueur a explicitement choisi le scénario provisoire, désormais installé. Voir [PROVISIONAL_INSTALLATION.md](PROVISIONAL_INSTALLATION.md). La recherche et le relevé initial ci-dessous restent conservés ; les chiffres en jeu sont ceux d’avant correction.

## Origine de la population installée

`docs/research/population/POPULATION_1776_BASELINE.csv` donne 20 933 434 habitants pour la portion MARATH et 192 822 pour GAR avant la première passe. La matrice `POPULATION_1776_STATE_TARGETS.csv`, méthode **INDIA_LOW_REGIONAL_TARGET**, les porte respectivement à **23 928 236** et **220 411**. Son commentaire indique que les proportions provinciales sont héritées et provisoires.

Le rapport de cette passe explique que le fichier indien entier passe de 166 219 721 à 190 millions. L'ancrage national Clio Infra ne documente donc **pas** 23 928 236 habitants dans le périmètre propre de STATE_AGRA en 1776. Les proportions culturelles, administrateurs britanniques et ventilations héritées ne doivent pas non plus être promues en recensement de 1776.

Le problème ne vient pas d'une confusion entre ville et province dans le nom affiché : STATE_AGRA est une grande région de jeu, partagée entre plusieurs propriétaires. Cependant ni cette région, ni la ville d'Agra, ni la province britannique d'Agra au XIXe siècle ne sont des périmètres interchangeables.

## Source démographique primaire vérifiée

Le *Census of India, 1911, United Provinces of Agra and Oudh*, chapitre II, §23, première page du chapitre, **page PDF 56**, discute l'incertitude des premiers comptages. [Fac-similé conservé par l'Université de Chicago](https://storage.lib.uchicago.edu/pres/2014/pres2014-0779-1911-15-01.pdf). Copie locale : `sources/UNITED_PROVINCES_CENSUS_1911.pdf` ; texte et rendu de la page conservés et effectivement examinés.

Il distingue l'estimation de 1826, fragile, les estimations ultérieures sur des périmètres différents, et les premiers dénombrements simultanés. **Il ne fournit pas un recensement de STATE_AGRA en 1776.** Il ne permet donc ni de confirmer les 24 millions, ni d'en déduire arbitrairement un chiffre de remplacement par simple règle de trois. Une reconstitution devrait raccorder les districts et juridictions aux cellules actuelles, puis dater les estimations et leurs hypothèses.

La documentation sur les famines des Provinces du Nord-Ouest situe notamment une grande crise en **1783–1784**, après le départ. [Gazetteer transcrit par le projet Famine and Dearth, Université d'Exeter](https://famineanddearth.exeter.ac.uk/displayhtml.html?id=fp_00103_en_impgazetteerindia_vol10). Le passage a été retrouvé par recherche ; son ouverture directe a échoué en HTTP 502. Il reste une corroboration limitée, pas un fac-similé intégralement vérifié ni une preuve qu'aucune disette n'existait en 1776. La crise de 1783 ne doit pas être avancée de sept ans pour excuser une famine chronique de démarrage.

**Conclusion historique : population locale non confirmée ; famine historique justifiant le déséquilibre de départ non établie.** Aucune nouvelle population ou famine historique n'est inventée pour résoudre le gameplay.

## Mesure dans la session ouverte

Victoria 3 **Macha 1.13.11**, somme de contrôle affichée `cab5`, date 1er janvier 1776. Lecture réelle de l'État et de l'infobulle de crise, puis sauvegarde locale distincte sans avancer la date. Empreintes : `SAVE_RECEIPT.json`.

| Indicateur MARATH / STATE_AGRA | Interface | Sauvegarde exacte ou précision |
|---|---:|---|
| Population | environ 23,9 millions | 23 928 236 |
| Main-d'œuvre totale | — | 7 178 467 |
| Paysans | 4,42 millions | 4 420 000 |
| Sans emploi | 2,57 millions | 2 571 967 selon la statistique moteur |
| Terres de la portion marathe | 444 | 444 |
| Région entière | — | 483 dans les définitions, dont 39 pour GAR |
| Habitants affamés | 23,5 M, 98 % | Lecture arrondie de l'interface |
| Famine modérée | 14,8 M, 62 % | Lecture arrondie de l'interface |
| Grande famine | 8,62 M, 36 % | Lecture arrondie de l'interface |
| Crise active | oui | entrée correspondante dans famine_manager |
| Morts depuis ce début de crise | 0 | Session encore au premier jour ; aucun taux annuel mesuré |

Les 444 terres ne sont pas la valeur entière de STATE_AGRA : la région contient 37 cellules, dont 34 marathes. `round(483 × 34/37)` donne bien 444 ; GAR détient les 39 autres. C'est une concordance locale de l'allocation estimée, pas une preuve universelle pour tous les états et modifiers.

L'instance de subsistance chargée porte 444 niveaux, mais sa main-d'œuvre est d'environ 442 niveaux équivalents. La sauvegarde ne contient aucune ferme commerciale dans cette portion, alors que les historiques déclarent une ferme de blé dans deux fichiers. Les outils conservent cette divergence au lieu d'additionner silencieusement des niveaux qui ne sont pas chargés. Sa cause précise — initialisation, restriction ou autre version chargée — reste à examiner.

## Scénario provisoire chiffré, distinct de la recherche historique

Si l'on décide de **conserver provisoirement les 23 928 236 habitants**, 2 571 967 / 10 000 donne 257,1967 niveaux de subsistance supplémentaires, arrondis à **258**. À parts de provinces inchangées, viser 702 terres marathes conduit à environ **764 terres pour toute la région**, contre 483 actuellement. GAR recevrait également sa part du supplément. La proposition conserve populations, propriétaires, bâtiments, PM, ressources, provinces et State_ID ; seul `arable_land` serait augmenté.

Cette hausse d'environ 58 % est un **calibrage de gameplay** et élargit aussi le potentiel futur de construction agricole. Ce n'est pas une démonstration que la surface cultivable historique était sous-estimée de 58 %. Les autres emplois, les ratios de travailleurs et les parts territoriales sont maintenus constants dans ce calcul. La création de nouveaux propriétaires et les effets de salaire peuvent modifier la projection.

Ce scénario traite la place disponible pour l'emploi. Il ne prouve pas la disparition de la faim modérée des paysans, la rentabilité, le paiement des impôts, l'accès aux biens, ni un futur taux de mortalité. Une nouvelle partie et une simulation bornée restent nécessaires. Le plan et ses préimages sont conservés dans `AGRA_PROVISIONAL_PLAN.json` et `proposal/`. Son éventuelle installation a un reçu séparé ; la sauvegarde de référence demeure un **avant**.
