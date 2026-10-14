# Rhin central — premier sous-lot du Neckar appliqué

Date : 13 octobre 2026. Situation recherchée : 1er janvier 1776.

**Statut : implémenté et contrôlé statiquement ; ensemble Mayence–Palatinat encore partiel.** Le jeu n'a pas été lancé : le test moteur reste reporté par l'utilisateur à la fin de tous les lots impériaux.

## Changements réels

Deux provinces du Bade sont subdivisées, sans modifier leurs régions économiques : `x318061` et `xE0A2B9`, dans `STATE_BADEN`. Quatre nouvelles identités RGB sont créées : `xEDA300` à `xEDA303`. Les deux anciennes restent présentes. Les six composantes obtenues sont connexes et ont un seul contrôleur.

- **KPF** reçoit le noyau conservateur Heidelberg–Ladenburg–Neckar : 60 pixels et **47 508 habitants** issus du pool initial BAD. Le locator Heidelberg reste sur `xE0A2B9`, désormais KPF ; il n'est ni déplacé ni utilisé pour transférer tout son ancien polygone.
- **KMZ** reçoit un fragment représentable des possessions de Viernheim/Lorsch : 5 pixels et **3 959 habitants**. Ce n'est ni l'intégralité de la Bergstraße ni un nouveau pays artificiellement agrandi.
- **BAD** conserve 1 217 pixels et **963 625 habitants** dans cette région économique. Les franges non retracées ne sont pas certifiées historiquement badoises.

La population régionale reste **1 015 092**, chaque culture/religion étant conservée ; le total mondial reste **835 804 980**. Répartition proportionnelle à la surface de chaque profil existant, avec arrondis conservatifs ; ce n'est pas un recensement historique.

Les niveaux de bâtiments, PM, attributs pondérés par niveau et détenteurs économiques privés sont préservés. Les allocations entières n'inventent pas de bâtiments pour les petits fragments. Les détenteurs BAD conservent une subdivision valide. Les armées, flottes, formations et recrutements ne changent pas. Aucun pays, capital, gouvernement ou loi préexistante n'est modifié.

Les droits impériaux suivent les nouveaux titulaires. Le registre actif atteint **363 RGB**. Les cartes principale et du journal sont régénérées ; l'étendue jaune reste exactement **62 516 pixels**, car les territoires subdivisés étaient déjà enregistrés. Les droits belges, piémontais et franconiens ne sont pas changés.

## Sources et précision

Les dossiers antérieurs de MAP1/MAP2K sont réutilisés. Les deux anciens polygones du Palatinat et le noyau ancien de Mayence restent des approximations de gameplay non retracées ici.

Le fond Vaugondy/Santini conservé a été examiné ; sa coloration des cercles ne suffit pas à prouver chaque souveraineté. Pour le secteur détaillé, la carte [De Wit, conservée à l'Université de Berne](https://www.e-rara.ch/bes_1/content/titleinfo/29609156) a été obtenue via son manifeste public et réellement inspectée. Elle est postérieure à 1688, **pas une carte certifiée de 1776**. Image, manifeste, provenance et empreinte sont conservés dans ce dossier.

La chronologie corrige un anachronisme important de ce fond : Ladenburg et les possessions concernées passent de Worms au Palatinat en **1705**, selon l'[histoire officielle de Ladenburg](https://www.ladenburg.de/de/2000-Jahre-Stadtgeschichte) et le [dossier du Landesarchiv sur Ladenburg](https://www.leo-bw.de/en/themenmodul/juedisches-leben-im-suedwesten/orte/baden/ladenburg-mit-edingen). Ils ne sont donc pas attribués à Worms sur la seule couleur de la carte ancienne. [Viernheim](https://www.viernheim.de/kultur-freizeit-sport/kunst-kultur/geschichte.html) reste à Mayence jusqu'en 1803 ; le fragment correspondant ne devient pas palatin. L'[historique de Heppenheim](https://www.heppenheim.de/heppenheim-erleben/stadtgeschichte) confirme les possessions mayençaises voisines, mais leur emprise complète reste hors de cette étape.

Le calage affine local utilise quatre villes identifiées dans la carte source et leurs locators natifs : Mayence, Francfort, Mannheim, Heidelberg. Résidus respectifs : **1,615 ; 1,209 ; 3,234 ; 2,828 pixels du jeu**. Le contrôle indépendant de Gießen, hors du secteur tracé, présente **8,808 pixels d'écart**. Il interdit de présenter ce modèle comme suffisamment précis pour toute la Hesse ou Aschaffenburg. Une première lecture de Wetzlar comme Gießen a été rejetée après agrandissement : le point rejeté reste explicitement documenté dans `TRACING.json`, non utilisé dans le calcul.

Les enveloppes sont dessinées en coordonnées de la carte source, puis intersectées avec les deux masques parents seulement. Aucun partage par rayons de villes. Les principales localités et le transfert de 1705 fondent l'attribution ; les contours intermédiaires restent une **approximation prudente de gameplay**, pas des frontières cadastrales. Un pixel isolé BAD a été abstrait dans son voisin KMZ du même parent ; la cellule exacte est enregistrée dans `GEOMETRY.json`. Aucune province supplémentaire hors des deux parents n'est redessinée.

`HISTORICAL_OVERLAY.png` montre les enveloppes et repères dans le scan, `ALIGNMENT.json` les résidus, `TERRITORIAL_CHANGES.csv` chaque correspondance RGB/propriétaire et `POPULATION_VALIDATION.csv` les profils conservés.

## Fichiers modifiés

`PLAN.json` liste sept fichiers textuels, dont les deux registres documentaires. Fichiers runtime territoriaux :

- `common/history/states/00_states.txt` ; `map_data/state_regions/00_west_europe.txt`.
- `common/history/pops/00_west_europe.txt`.
- `common/history/buildings/00_west_europe.txt` ; `common/history/buildings/98_build_start_1776_world_redistribution.txt`.
- `map_data/provinces.png` ; `map_data/province_terrains.txt`.

`IMPERIAL_FILES.json` liste sept sorties impériales recompilées : triggers, identité du bloc, effets de restitution, localisations françaises et anglaises des listes/retours impériaux. Aucun nouveau membre n'est créé.

Graphismes régénérés : carte DDS du journal, masque/sentinel DDS de la carte principale et aperçus. Les scripts de génération/validation sont `map2l_rhine.py`, `map2l_rhine_patch.py` et `validate_map2l_rhine.py`. Les validateurs antérieurs acceptent seulement les migrations ordonnées explicites, leurs propriétaires exacts, cellules exactes et fichiers déclarés ; les baselines antérieures restent immuables.

## Validations exécutées

- Neckar : **327/327** — PASS_STATIC_ENGINE_DEFERRED.
- Franconie : **473/473** — les attributions et profils franconiens sont inchangés.
- Belgique : **315/315** — préservation du lot belge, avec 1 539 pixels physiques modifiés cumulés dans les trois passes (413 belges + 1 028 franconiens + 98 Neckar).
- Piémont : **232/232**, extension exacte de 2 227 pixels conservée.
- Carte principale : **16/16 hors moteur** ; masque mondial exact, DDS sans perte et helper HLSL compilé. Ce n'est pas une compilation complète ni un chargement du shader dans Victoria 3.

Aucun nouveau doublon, trou de propriété ou renvoi invalide. Les **44 RGB doublement attribués et 12 erreurs de référence préexistants** restent exactement ceux de la baseline, séparés des nouvelles corrections. HEAD et index Git restent inchangés. Aucun commit, merge, rebase ou push.

## Ce qui reste ouvert

Ce sous-lot n'est pas le découpage complet du Rhin central. Restent notamment le noyau et le Rheingau de Mayence, toute la Bergstraße/Starkenburg, Aschaffenburg, les possessions éloignées de Mayence, le Palatinat occidental et Mosbach, ainsi que les autres souverainetés contenues dans les franges actuellement BAD/PRU/HES. Ne pas considérer les anciennes provinces entières comme une validation définitive. Détails dans `UNRESOLVED.csv`.

La suite reste **Mayence–Palatinat**, avant de passer au lot suivant. Le calage du Neckar ne sera pas étendu arbitrairement aux secteurs où le contrôle indépendant montre une dérive.

## ColGrep

L'appel exploratoire du démarrage précédent est documenté dans `WORK.md` : deux lignes pertinentes mais insuffisantes. Aucun nouvel appel 2B n'a été effectué pendant cette implémentation, les fichiers et identifiants étant connus. Les RGB et CSV ont été vérifiés directement. Les recherches extérieures étaient ciblées sur le fond cartographique et les changements de titulaire nécessaires, pas une nouvelle étude mondiale. Aucun compteur de tokens fiable ni comparaison A/B ne permet de mesurer une économie précise.

Actualisation incrémentale de l'index exécutée : 21 fichiers ajoutés, 19 actualisés, 0 supprimé et 4 369 inchangés. Ce résultat n'est pas une exécution du modèle agent et aucune reconstruction complète de l'index n'a été demandée.
