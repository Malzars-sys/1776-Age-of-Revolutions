# WORLD 1776 — CHANTIER TERRITORIAL AUTONOME N° 2

**Passe BALKANS-01 — 24 octobre 2026.** Référence historique : **1er janvier 1776**.

Statut du lot : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Les Balkans restent **IMPLEMENTATION_IN_PROGRESS**. Aucun `PASS_RUNTIME_USER_VALIDATED`, aucune région déclarée complète et aucune phase ultérieure commencée.

## Progression des cinq phases

| Phase | Statut | Critères entièrement vérifiés statiquement | Couverture technique | Validation joueur nouvelle |
| --- | --- | ---: | ---: | ---: |
| Balkans | IMPLEMENTATION_IN_PROGRESS | 3 / 80 | 3,75 % | 0 |
| Italie méridionale | NOT_STARTED | 0 / 40 | 0 % | 0 |
| Afrique subsaharienne | NOT_STARTED | 0 / 80 | 0 % | 0 |
| Maghreb | NOT_STARTED | 0 / 48 | 0 % | 0 |
| Amériques | NOT_STARTED | 0 / 72 | 0 % | 0 |
| Ensemble | INCOMPLETE | 3 / 320 | 0,94 % | 0 |

La mesure porte sur 40 sous-régions et huit critères fixes, non sur le nombre de documents. Seuls souveraineté/géométrie, compatibilité technologique des actifs transférés et contrôles statiques des deux cellules cycladiques sont entièrement crédités. Les corrections institutionnelles partielles et recherches sur le Monténégro ne donnent aucun point. Les reçus humains antérieurs d'autres chantiers ne sont pas étendus à ce lot. [Modèle et registre](../ROADMAP_STATE.json).

## Recherches antérieures effectivement réutilisées

Les quatre fichiers MAP-1776 canoniques et les 36 livrables des neuf agents régionaux ont été retrouvés et référencés avec leurs empreintes. Leur simple présence ne constitue pas une lecture de toutes les phases : seul le dossier balkanique R2 et les installations pertinentes ont été exploités ici. Recommandations R2 -0059/-0060, -0061/-0063 et -0102/-0104, fiche centrale -0104, atlas technique et locators natifs ont fourni les pistes.

La baseline MAP-0 ne décrit plus exactement le workspace courant. Les corrections installées en Bessarabie et autour de la mer Noire, ainsi que tous les travaux SERG, sont conservés. Un nouveau suivi indépendant se trouve dans `WORLD_1776_CLOSURE/`, avec périmètre, progression, historique additif, blocages, prochaine action et contrôle de concurrence.

## Pays et propriétaires concernés

| TAG | Examen de cette passe | Résultat |
| --- | --- | --- |
| VEN | Souveraineté sur les deux cellules cycladiques | Retirée ; propriété économique vénitienne conservée |
| TUR | Réception des cellules, habitants et actifs locaux | Souveraineté ottomane installée ; aucun octroi de technologie |
| MOL | Cadre institutionnel initial | Deux activations anachroniques retirées |
| WAL | Cadre institutionnel initial | Deux activations anachroniques retirées |
| MON | Objection du joueur, sources et état réel | Noyau autonome conservé ; aucune annexion ni extension |

Aucun nouveau pays, TAG, souverain, personnage, institution, bâtiment, unité ou type de relation n'est créé.

## Corrections territoriales installées

| State_ID | RGB réel du bitmap | Avant | Après | Pixels représentés |
| --- | --- | --- | --- | ---: |
| STATE_WEST_AEGEAN_ISLANDS | x6090A0 | VEN | TUR | 401 |
| STATE_WEST_AEGEAN_ISLANDS | x6960A0 | VEN | TUR | 52 |

**Deux cellules réattribuées, zéro nouveau RGB, zéro pixel recolorié.** Les State Regions, ressources, hubs et sorties maritimes ne changent pas. La méthode A utilise les provinces existantes ; les agrégats cycladiques ne sont pas présentés comme des frontières cadastrales exactes. Les locators de Tinos et Thera ont été échantillonnés dans le raster courant. [Correspondance géographique](GEOGRAPHIC_CROSSWALK.json), [carte avant/après](AEGEAN_BEFORE_AFTER.png), [données du transfert](TERRITORIAL_CHANGES.json).

La souveraineté ottomane sur les Cyclades en 1776 est défendable après la perte de Tinos en 1715 et le règlement de 1718. Les privilèges des communautés locales ne sont pas assimilés à une souveraineté vénitienne. Les deux RGB techniques des îles ioniennes sont inchangés. Le cas de Cythère n'est ni corrigé ni certifié par ce lot. Les frontières de Moldavie, Bucovine, Dalmatie, Istrie et du Monténégro sont inchangées.

## Populations et économie

| Mesure | Avant | Après | Variation |
| --- | ---: | ---: | ---: |
| Population mondiale déclarée dans les historiques effectifs | 834 936 539 | 834 936 539 | 0 |
| Habitants du scope cycladique VEN | 80 404 | 0 | −80 404 |
| Habitants du scope cycladique TUR | 0 | 80 404 | +80 404 |

Le bloc de POP grec est conservé, avec sa religion orthodoxe par défaut culturel et ses professions initiales inchangées. Aucun chiffre de recensement nouveau, aucune conversion religieuse et aucune population compensatoire ne sont introduits. Ce contrôle ne certifie pas l'exactitude démographique des 80 404 habitants pour 1776. [Mesures](POPULATION_BEFORE_AFTER.json).

Le niveau de pêche et le port sont déplacés vers le scope politique TUR avec les mêmes niveaux, PM et réserves. Leurs titres de propriété économique situés dans les districts financiers vénitiens ne sont pas confisqués. L'emploi nominal des recettes et les ressources sont inchangés. Les effets économiques réels du changement de marché et de gouvernement attendent le test moteur. Le trait préexistant Hermoupolis et la représentation des communautés catholiques nécessitent encore une étude distincte.

## Souverains, institutions et diplomatie

Les historiques contiennent toujours Abdulhamid Ier pour TUR, Alvise IV Mocenigo pour VEN, Grigore III Ghica pour MOL, Alexandru Ipsilanti pour WAL et Sava II Petrović-Njegoš pour MON. Aucun de leurs fichiers de personnages ne change ; ce relevé n'est pas une nouvelle certification biographique exhaustive.

Dans MOL et WAL, les activations de `law_organic_regulation` et `law_elected_bureaucrats` sont retirées. Le cadre traditionnel déjà appelé conserve la monarchie, l'autocratie et la bureaucratie héréditaire. C'est une approximation institutionnelle B des offices et élites traditionnels, distincte de la nomination des hospodars par la Porte. Les autres lois, institutions, dirigeants et relations demeurent en place.

MOL et WAL restent des entités distinctes liées à TUR par les protectorats natifs existants. Ce type de pacte demeure une approximation du statut tributaire historique ; aucun nouveau taux de tribut ni droit diplomatique n'est inventé ici. Le règlement organique appartient à 1831–1832 ; sa disponibilité dans une campagne ultérieure n'est pas modifiée.

Pour MON, les sources attestent une autorité locale autour de Cetinje. Le mod ne lui donne déjà qu'une cellule intérieure, avec côte vénitienne et districts ottomans distincts. **La suppression de MON n'est donc pas retenue à ce stade.** Le degré exact d'autonomie, les limites et la répartition entre clans, guvernadur et métropolite restent ouverts. [Décision détaillée](MONTENEGRO_DECISION.md).

## Technologies, bâtiments, ressources et armées

Les profils initiaux existants sont relus de manière ciblée : TUR 23 technologies explicites, VEN 27, MOL 10, WAL 10, MON 9 ; aucune référence de technologie inconnue ni effet technologique non résolu dans ce relevé. Ce n'est pas une reprise de l'audit technologique mondial ni une validation historique de tous ces profils.

TUR possède déjà `enclosed_dock_systems`, nécessaire au port transféré. Les autres PM initiaux concernés ne demandent aucune technologie absente du bénéficiaire. **Zéro technologie ajoutée**, aucune infrastructure technologique commune modifiée. [Contrôle ciblé](STARTING_TECH_CHECK.json).

Aucune formation n'est recrutée ou déplacée. Les bâtiments, ressources, unités, pacts et événements extérieurs au lot sont protégés par empreinte. Les chantiers militaires, économiques et américains précédents ne sont pas réécrits.

## Sources, incertitudes et validation

Sources principales : chronologie patrimoniale *Cycladic Castles* ; corroboration de Dimitropoulos (2014), accessible sous forme d'extraits ; Oncescu (2018) pour les principautés ; Guţan pour le règlement organique ; CANU et Radosavljević pour le Monténégro. [SOURCES.md](SOURCES.md) distingue lectures effectives, notices, extraits et accès refusés. Les RGB sont établis par les données techniques, non déduits d'une notice historique.

**53/53 contrôles statiques cumulatifs réussis**, après un premier passage complet à 52/52 avant les modifications parallèles. Syntaxe des cinq historiques, attribution des deux RGB, conservation des propriétaires voisins et de toutes les autres paires État/propriétaire, populations, cultures, actifs et propriété privée, compatibilité des PM, présence des historiques et références de technologies, conservation du bitmap, des personnages, pacts, lois communes, troupes et ressources.

Le premier passage du comparateur a signalé à tort toutes les listes de propriétaires comme différentes parce que le format JSON utilisait des listes là où le lecteur retournait des tuples. Cette différence de représentation a été corrigée dans l'outil, sans nouvelle modification des données du jeu. Le diagnostic initial est conservé dans `VALIDATION_FIRST_RUN.json` ; le résultat final est [VALIDATION.json](VALIDATION.json).

Sur **2 470 fichiers fonctionnels protégés, 2 466 sont inchangés et quatre portent des corrections parallèles TECH-R2 vérifiées et conservées**. Les **873 fichiers de preuve/suivi SERG**, les références vanilla, HEAD, branche et index Git sont inchangés.

Le chantier `STARTING_TECH_AUDIT_1776_R2` a modifié cinq fichiers après notre premier contrôle, dont le fichier de bâtiments sud-européens partagé. Ses préimages, anciennes/nouvelles valeurs et empreintes finales ont été relues ; l'application exacte de ses remplacements est reconstruite sans nouvelle écriture fonctionnelle. Dans le fichier partagé, la préimage TECH-R2 contient déjà notre transfert cycladique complet, et ses modifications concernent d'autres États. **Les deux changements sont donc présents ensemble et aucune restauration de baseline n'a eu lieu.** Le contrôle ciblé des technologies et actifs cycladiques repasse dans cet état composé. Les reçus du pair sont copiés dans `concurrent_tech_r2/` ; la première validation et le manifeste de notre seule écriture restent archivés séparément.

[Suivi de concurrence](../CONCURRENT_CHANGES.json), [reconstruction des modifications parallèles](CONCURRENT_PATCH_RECONCILIATION.json), [fichiers modifiés et état composé](FILES_MODIFIED.json), [empreintes immédiatement après notre seule écriture](FILES_MODIFIED_OWN_PATCH_ONLY.json).

Les catégories qui ne sont pas modifiées sont contrôlées en conservation, pas déclarées historiquement achevées. Aucun lancement de jeu, mois simulé, observation économique ou sauvegarde/rechargement n'est fabriqué. [Protocole joueur groupé](PLAYER_TEST_PROTOCOL.md).

## Fin de passe et prochaine action

Le lot installé attend son test propre. Les limites démographiques et fiscales des Cyclades, Cythère, le statut monténégrin, Raguse, les provinces ottomanes encore peu étudiées et les interfaces réservées restent ouverts dans [BLOCKERS.md](../BLOCKERS.md).

La prochaine action d'agent est **BALKANS-02 — Raguse et Adriatique** : souveraineté, tribut, institutions, noyau Dubrovnik, voisinage des passages ottomans, technologies et population. Les lots indépendants restent autorisés sans attendre chaque validation individuelle. Les quatre phases ultérieures sont toujours non commencées. Cette passe ne clôture pas les Balkans.
