# Mayence–Rheingau, Aschaffenburg et Palatinat occidental

13 octobre 2026 — situation recherchée : 1er janvier 1776.

**Sous-lot de noyaux appliqué et validé statiquement. Ce n'est pas le découpage intégral de toutes les possessions mayençaises et palatines.** Le test dans Victoria 3 reste reporté, comme demandé, à la fin des lots du Saint-Empire.

## Modifications effectives

| Secteur | Région économique / State_ID natif | RGB parent conservé | Nouvelle province | Résultat |
| --- | --- | --- | --- | --- |
| Bande conservatrice du Rheingau | `STATE_HESSE` / 74 | `x90C020` | `xEDA400` | 18 pixels HES → KMZ ; 15 463 habitants transférés |
| Fragment d'Aschaffenburg / Spessart intérieur | `STATE_FRANCONIA` / 72 | `x9040A0` | `xEDA401` | 20 pixels BAV → KMZ ; 14 752 habitants transférés |
| Raccord septentrional Otterberg–Lautern | `STATE_RHINELAND` / 63 | `x11C021` | `xEDA402` | 17 pixels subdivisés, **déjà KPF**, sans transfert de souveraineté ni de population |

Ces trois valeurs RGB sont des identifiants techniques du bitmap, pas des identifiants historiques. Les State_ID ne sont pas renumérotés ; les régions restent partagées entre propriétaires. Les six composantes (parents et enfants) sont connexes et attribuées chacune exactement une fois. Les anciennes identités restent présentes ; Kaiserslautern conserve son hub dans `x11C021`. Tous les autres hubs et locators restent inchangés.

Mayence acquiert une subdivision dans `STATE_FRANCONIA` et complète sa subdivision hessoise. Aucun nouveau pays, capital, gouvernement, lien de sujétion, loi, armée, flotte ou recrutement n'est ajouté ou déplacé. BAV et HES conservent leurs subdivisions, notamment pour ne pas invalider leurs détenteurs économiques.

La population mondiale demeure **835 804 980**. Chaque profil régional, culture, religion explicite ou implicite et attribut écrit est conservé. Les transferts sont proportionnels à la surface dans le pool de départ de chaque subdivision, avec arrondis entiers conservatifs : **ce n'est pas un recensement historique**. Pour ces petites fractions, aucune allocation entière de bâtiment ne change : tous les fichiers historiques de bâtiments restent **identiques octet pour octet**, y compris les PM et détenteurs.

Le registre impérial passe de **363 à 366 RGB**, avec les bons titulaires pour la restitution. Les droits belges, piémontais et du Neckar restent identiques. La carte principale et celle du journal ont été régénérées ; leur étendue jaune demeure **62 516 pixels**, les trois masques parents étant déjà impériaux.

## Sources réutilisées, calage et limites

Les dossiers MAP1/MAP2K, les cartes et décisions des lots précédents sont réutilisés. Le fond dynastique de 1789 ne permet pas de distinguer ces souverainetés et n'a pas été utilisé pour décider des propriétaires. La reproduction Vaugondy/Santini déjà conservée a été relue ; sa coloration des cercles ne sert pas automatiquement de frontière d'État.

Les [archives de Hesse, fonds 108](https://arcinsys.hessen.de/arcinsys/showFondsDetails.action?fondsId=1943&request_locale=en) confirment l'appartenance du Rheingau à Kurmainz jusqu'en 1802/03. L'[histoire publiée par Eltville](https://www.eltville.de/freizeit-tourismus/erleben-entdecken/stadtportrait/stadtteile/eltville/) corrobore cette continuité. Les [archives municipales d'Aschaffenburg](https://aschaffenburgzweinull.stadtarchiv-digital.de/episode-19-aschaffenburg-im-uebergang-von-mainz-zu-bayern/) situent le passage à la Bavière en 1814, pas en 1776. La [municipalité d'Otterberg](https://www.otterberg.de/) et la [chronologie de sa paroisse](https://otterberg.evpfalz.de/index.php?id=5633) documentent le noyau palatin. Aucune union palatino-bavaroise de 1777 n'est projetée rétroactivement sur 1776.

La carte détaillée [De Wit, Universitätsbibliothek Bern](https://www.e-rara.ch/bes_1/content/titleinfo/29609156), déjà conservée, fournit les contours mayençais. Pour le raccord occidental, les accès publics à un scan plus lisible du fond Vaugondy n'ont pas abouti (expiration ou contrôle anti-robot), sans contournement. Une consultation **strictement ciblée**, pas une nouvelle recherche mondiale, a obtenu le scan [Schenk, MUE Ryh 3002:28, Berne](https://www.e-rara.ch/doi/10.3931/e-rara-112447), avec manifeste, provenance et empreinte enregistrés dans `SCHENK_SOURCE.json`.

Schenk est catalogué **après 1695**, De Wit **après 1688** : ni l'une ni l'autre n'est une photographie politique certifiée de 1776. Seules des enveloppes prudentes de possessions dont la continuité est corroborée sont employées ; les territoires et couleurs voisins ne sont pas automatiquement réattribués.

Un nouveau calage local Schenk est établi par cinq villes vérifiées sur le scan : Mayence, Francfort, Kaiserslautern, Mannheim et Heidelberg. Les résidus sont **4,191 ; 3,355 ; 1,976 ; 2,369 ; 2,372 pixels du jeu**. De Wit est raccordé à Schenk par trois villes communes ; Mannheim sert de contrôle de ce raccord (2,265 pixels par rapport au locator natif, qui participe par ailleurs au calage Schenk). Ce n'est donc **pas** un contrôle indépendant de tout le modèle. Le contrôle éloigné de Gießen dérive de **12,708 pixels** : ce modèle n'autorise pas le découpage du nord de la Hesse. Le mauvais calage nord tenté avec les seuls locators Mayence–Francfort–Gießen a été écarté, sans application au runtime.

Les contours de `TRACING.json` sont tracés dans les scans puis intersectés exclusivement avec trois masques parents. Ce sont des **approximations de gameplay à l'échelle native**, pas des limites cadastrales ni une précision d'un pixel. Aucun rayon autour d'une ville, agrandissement d'enclave ou annexion d'une province entière par son nom n'est utilisé. `SCHENK_OVERLAY.png`, `DE_WIT_OVERLAY.png` et `ALIGNMENT.json` rendent le choix et ses limites auditables.

## Fichiers modifiés et contrôles

`PLAN.json` contient cinq fichiers textuels :

- `common/history/states/00_states.txt` : propriétaires et nouvelles références RGB.
- `map_data/state_regions/00_west_europe.txt` : listes des trois régions uniquement ; ID, ressources et hubs préservés.
- `common/history/pops/00_west_europe.txt` : conservation et transferts des profils.
- Registre `MAP2L/IMPERIAL_DE_JURE_REGISTRY.json` et manifeste `MAINZ_PALATINATE/REGISTRY_MIGRATION.json`.

S'ajoutent le bitmap et les terrains générés, les sorties impériales explicitement listées dans `IMPERIAL_FILES.json`, la DDS du journal et les deux DDS de la carte principale. Les sept sorties impériales modifiées couvrent les triggers, l'identité du bloc, les effets de restitution et les localisations anglaises/françaises des listes. Aucun autre changement gameplay n'est introduit.

Les scripts `tools/map2l_mainz.py` et `tools/validate_map2l_mainz.py` produisent et vérifient ce lot. `map2l_registry.py` ordonne une nouvelle migration explicite ; les validateurs antérieurs suivent les couches de subdivisions exactes, sans autoriser des changements extérieurs ni ignorer les attributions antérieures. Les baselines et candidats précédents restent immuables ; la nouvelle baseline réutilise le bitmap post-Neckar déjà sauvegardé, sans copier tout le mod.

Résultats :

- Nouveau lot : **365/365 PASS_STATIC_ENGINE_DEFERRED**.
- Franconie cumulative : **495/495**.
- Belgique cumulative : **315/315**.
- Piémont : **232/232**, extension exacte de 2 227 pixels préservée.
- Neckar : **327/327**.
- Carte principale : **16/16 hors moteur**, masque exact, DDS sans perte, helper HLSL compilé. Il ne s'agit ni d'un test de chargement ni de la compilation complète du shader par Victoria 3.

Les propriétaires, profils démographiques, bâtiments, ressources, locators, références, droits et fichiers protégés sont contrôlés contre la baseline de cette passe. HEAD et index Git restent inchangés. Aucun commit, staging, merge, rebase ou push.

Les **44 RGB doublement attribués et 12 erreurs de référence préexistants** sont conservés exactement et ne sont pas comptés comme nouvelles régressions. Les détails se trouvent dans `VALIDATION.json`.

## Ce qui reste ouvert

Le grand polygone historique de gameplay `x1141A0` autour de Mayence n'a pas été redessiné ici : **il n'est pas certifié comme frontière historique**. Le fragment du Rheingau n'en représente pas encore l'intégralité. Aschaffenburg est un noyau, pas tout l'Oberstift : Lohr, Orb, Rieneck, Klingenberg et Miltenberg demandent leur propre confrontation géographique. La Bergstraße/Starkenburg reste également partielle.

Le Palatinat occidental n'est pas terminé par la seule subdivision d'Otterberg : les anciens grands masques KPF, les possessions discontinues et les voisinages de Deux-Ponts, Leiningen, Worms, Spire et Sponheim restent à distinguer. Le raccord examiné était déjà KPF ; la tentative de le transférer depuis un parent PRU ne croisait pas ce parent et a été rejetée. Aucun nouveau transfert PRU → KPF n'est donc affirmé ou appliqué. Les franges inchangées BAV/HES/PRU/KPF restent **non certifiées historiquement**, et non une conclusion selon laquelle elles auraient toutes appartenu à ces pays en 1776.

Pour la suite, terminer ces dépendances rhénanes avant de présenter le lot Mayence–Palatinat comme complet. Aucun périmètre extérieur au Saint-Empire n'est modifié.

## ColGrep et mesure

**Zéro nouvel appel à ColGrep-Agent-2B pendant cette passe** : les dossiers, générateurs et identifiants avaient déjà été localisés et vérifiés. Les relocaliser aurait été une recherche redondante, contraire aux instructions. Les contrôles exacts se font avec `rg`, CSV/JSON et les validateurs existants. Les numéros de lignes des trois State_ID ont été vérifiés directement dans le fichier courant (63, 72, 74).

Le statut de l'index a été consulté. L'actualisation incrémentale finale, si elle aboutit, est consignée dans `COLGREP_REFRESH.md` ; ce n'est pas une exécution du modèle agent. Les formats raster PNG/JPG/DDS et les cartes SVG ne sont pas une source de décisions historiques déléguées au 2B ; ils sont inspectés ou validés directement. La couverture de chacun de ces formats n'a pas été remesurée lors de ce lot.

Les compteurs de tokens Codex par opération ne sont pas accessibles ; aucun comptage fiable couvrant tous les appels classiques de ce tour n'a été conservé. Aucune économie exacte, durée totale de recherche 2B ou comparaison A/B n'est revendiquée. Cette passe n'est pas un benchmark du 2B : son intérêt est la localisation initiale de code inconnu, pas la substitution à la lecture cartographique, à l'attribution historique ou aux tests.
