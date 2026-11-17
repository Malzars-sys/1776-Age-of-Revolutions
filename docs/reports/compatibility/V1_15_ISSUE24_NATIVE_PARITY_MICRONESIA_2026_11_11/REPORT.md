# Mission 24 — attributions initiales et dépendance russe du DLC

Livraison locale du 11 novembre 2026, sur l'installation canonique **1.15.0**.
Statut du lot : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. La mission 24
reste ouverte pour son acceptation, dont le catalogue de journaux 39 ; la
clôture générale de 19 reste conditionnée à 24 et à la validation intégrée 25.

## Correctifs installés

Dans `common/history/states/00_states.txt`, un seul jeton est ajouté :
`xEF50C0`, jusque-là sans attribution, rejoint le bloc **PHI** existant de
`STATE_WEST_MICRONESIA`. Le bloc possédait déjà `xA7F7E3`, les Mariannes du Sud
dont Guam. Aucun propriétaire existant n'est remplacé. Les autres octets du
fichier partagé sont conservés, y compris ses fins de ligne et son encodage.

Trois fichiers isolés `1776_v115_russian_civil_war.txt` rétablissent exactement
l'objet natif **RSR**, respectivement dans `common/country_definitions`,
`common/flag_definitions` et `common/dynamic_country_names`. Le mod masquait
ces trois objets alors que l'effet natif `rcw_mark_partition_owners` contient
`change_tag = RSR`. Ses deux autres consommateurs de pays et le déclencheur
de sélection sont également hérités du natif. Ce n'est pas du contenu
espagnol : cette association dans le rapport du 9 novembre était erronée.

Le tag reste dormant : aucun État, habitant, bâtiment, historique national,
loi ou technologie ne lui est initialisé. Il sert à renommer une faction
créée par le mécanisme existant ; aucun déclenchement de guerre civile n'est
ajouté. Le drapeau inclut la définition RUS existante. Les dix variantes de
nom reprennent les cinq camps natifs, avec leurs conditions et priorités.
Les sept clés nécessaires par langue sont déjà fournies par les fichiers
natifs effectifs : aucune localisation ni traduction supplémentaire n'est
installée. Les deux candidats de localisation vides préparés restent
uniquement des preuves ; le contrat d'installation révisé ne retient que les
trois fichiers de scripts.

## Mariannes : preuve physique et choix de représentation

Le raster actuel mesure 8192 × 3616. La province contient **184 pixels** en
huit composantes, dans la boîte inclusive x7399–7418 / y1634–1720. La carte
physique de l'USFWS, figure 1, p. 59428 du *Federal Register* du 1er octobre
2015, identifie la chaîne au nord de Saipan. Trois points USGS servent au
diagnostic affine local : Farallon de Pajaros, Pagan, Anatahan. Asuncion,
réservé au contrôle indépendant, présente un résidu de **3,65 pixels**.
La carte du jeu est stylisée : cette correspondance identifie un archipel,
elle ne certifie pas un cadastre ni une liste exhaustive des îles physiques.

Le travail historique de Hezel, publié en 1988, décrit la soumission des îles
septentrionales en 1698, leur déplacement forcé de population et la
concentration ultérieure de la présence espagnole sur Guam. Russell (1998)
corrobore, dans son résumé effectivement consulté, l'évacuation des îles du
Nord à la fin des années 1690. Cela soutient le rattachement à l'ensemble
colonial espagnol, sans attester une garnison permanente sur chaque île en
1776 ni donner un effectif à attribuer à cette province.

**PHI est ici une approximation politique explicite** : on complète le
regroupement colonial déjà choisi par le scénario pour Guam et les Mariannes
du Sud, sous la souveraineté espagnole représentée par sa relation de colonie
existante. On ne prétend pas que les Mariannes dépendaient littéralement du
gouvernement philippin en 1776. La notice historique de la Library of Congress
retrouvée par recherche place leur subordination au vice-roi du Mexique avant
1821 ; son ouverture directe est refusée. Aucune pièce d'archive de cette
collection n'est déclarée consultée. Une refonte des juridictions espagnoles
du Pacifique relève du chantier historique 18, pas de ce correctif ponctuel.

Les POP authored restent inchangées, dans leurs blocs MCR et PHI existants.
Aucune population n'est inventée ou transférée par proportion de pixels.
Le poids territorial de PHI dans cet État peut changer ses parts calculées
en jeu ; la conservation des fichiers n'est pas une mesure de cet effet.

| Source consultée | Usage et limite |
| --- | --- |
| [USFWS, 2015, figure 1, p. 59428](https://www.govinfo.gov/content/pkg/FR-2015-10-01/pdf/2015-24443.pdf) | Géographie physique actuelle ; aucune souveraineté de 1776 déduite de cette carte |
| [USGS Farallon de Pajaros](https://www.usgs.gov/volcanoes/farallon-de-pajaros), [Pagan](https://www.usgs.gov/volcanoes/pagan), [Anatahan](https://www.usgs.gov/volcanoes/anatahan), [Asuncion](https://www.usgs.gov/volcanoes/asuncion) | Coordonnées des trois repères et du contrôle indépendant |
| [Hezel, 1988, paragraphes sur la réduction et l'administration](https://micsem.org/article/from-conquest-to-colonization-spain-in-the-marianas-1690-1740/) | Texte de recherche consulté ; distinguer souveraineté et occupation locale |
| [Russell, 1998, résumé de Gani Revisited](https://digitalcollections.byuh.edu/pacific-studies-journal/vol21/iss3/6/) | Résumé consulté ; le téléchargement du texte intégral est refusé, il n'est pas présenté comme lu |
| [LoC, notice historique de la collection Mariana Islands Records, révision 2011](https://findingaids.loc.gov/repositories/19/resources/5103) | Contexte administratif retrouvé par recherche ; accès direct refusé, archives non consultées |

`GEOGRAPHIC_IDENTIFICATION.json` et `CURRENT_MARIANAS_GEOMETRY.png` conservent
les mesures, repères, limites et l'image analytique issue du raster courant.
Le vieux dossier MAP1-P0-011 reste intact ; sa correspondance géographique
non résolue est complétée par cette nouvelle preuve datée, sans score WORLD.

## Treize attributions contradictoires conservées

| État | Paires d'instructions | Provinces |
| --- | --- | --- |
| Kenya | SKY / WTU ; SKY / MJK | 2 |
| Tanganyika | NYM / MSI | 3 |
| Mauritanie | OUA / ADR | 6 |
| Himalaya oriental | TIB / BHU | 2 |

Pour chacune des treize provinces, le lecteur compare les instructions
effectives du mod et du vanilla : mêmes États, pays, opérateurs, absence de
contrôle conditionnel et même séquence de lecture des sources. Ce sont des
anomalies **héritées identiques**, pas treize régressions établies de la
migration. Cela ne prouve ni leur exactitude historique ni leur innocuité en
jeu. Le propriétaire effectivement retenu par le moteur n'est pas déduit de
l'ordre textuel. L'arbitrage historique reste visible sous 18 et les anciens
échecs ne sont ni effacés ni transformés en PASS global.

Le nouvel outil `tools/compatibility/issue24_native_parity_audit.py` conserve
intégralement la qualification brute, ajoute cette provenance et contrôle
huit contre-exemples, dont changement d'État, propriétaire, opérateur,
multiplicité, ordre et condition. Il n'édite aucun fichier de jeu.

## Vérification et limites

Les résultats finaux et leurs contrôles de conservation figurent dans
`FINAL_MAP.json`, `FINAL_QUALIFICATION.json`, `CURRENT_JOURNAL_DEPENDENCIES.json`
et `FINAL_VALIDATION_R2.json`. Le premier scan post-attribution est conservé sous
`POST_INSTALL_MAP.json`, avant la restauration supplémentaire de RSR. Les
chiffres définitifs distinguent donc 1074 puis 1075 définitions de pays, sans
augmentation du nombre de pays possédant initialement un territoire.

Le premier contrôle de conservation, `FINAL_VALIDATION.json`, garde son échec
26/27 : les positions de caractères des anciens constats ont été décalées par
les huit caractères insérés. La comparaison brute était donc trop stricte.
La révision suivante exige le décalage exact de huit pour ces seules positions
situées après l'insertion et l'identité de tous les autres champs. Aucun
constat ni ancien résultat n'est supprimé pour obtenir la validation du lot.

La carte conserve son statut brut **FINDINGS_STATIC_ONLY** pour les treize
attributions héritées. Les références résiduelles optionnelles aux pays
absents de 1776 restent tracées avec leur opérateur et leur contexte ; le
déclencheur IA BKH est transmis à 25. La référence espagnole différée au
détroit de Gibraltar n'est pas réactivée ni renommée. Aucun nouveau défaut
de province, région stratégique, capitale ou culture POP n'est établi dans
le périmètre du lecteur.

Le catalogue de 494 journaux a été relu par son auditeur de dépendances,
avec zéro constat typé/métadonnée. Cela ne remplace pas son acceptation
fonctionnelle sous 39. Les gardes DLC restent celles du scénario et des
fournisseurs natifs, notamment `dlc019` sur le gouvernement provisoire russe.
Leur inventaire est statique ; ni simulation, ni rendu, ni parcours complet
de guerre civile, ni parité transitive avec et sans DLC ne sont certifiés.

Le protocole court est dans `RUNTIME_PROTOCOL.md`. Aucun test déjà accepté
par le mainteneur n'est annulé, et aucune date de partie ou sauvegarde non
fournie n'est inventée. Aucune opération Git d'écriture, publication ou
modification du vanilla n'est effectuée.
