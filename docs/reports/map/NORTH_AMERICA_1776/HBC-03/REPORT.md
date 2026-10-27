# HBC-03 — conservation du pays et arc jusqu'à Eastmain

Date : 25 octobre 2026. **Proposition et plan préparés ; aucun transfert territorial, démographique ou économique appliqué au jeu.** Ce lot répond aux deux précisions du joueur : garder intégralement la population et les bâtiments HBC pour le gameplay, et vérifier les installations sur la côte québécoise tournée vers les baies James/Hudson.

Complément ultérieur demandé par le joueur : [HBC-04](../HBC-04/REPORT.md) réserve le lien terrestre HBC → Haut-Canada → Treize Colonies. La proposition active passe à 233 provinces HBC ; les 228 provinces de ce dossier restent la base conservée et le socle démographique/économique demeure inchangé.

Vérification ultérieure de la demande conditionnelle concernant Kuujjuarapik : voir [KUUJJUARAPIK_CHECK.md](KUUJJUARAPIK_CHECK.md). Aucun poste actif au 1er janvier 1776 n'est établi par les sources consultées ; la proposition n'est donc pas prolongée au-delà d'Eastmain. Les fichiers cartographiques et le socle de conservation restent inchangés.

## Conservation protégée

Le socle figé `CONSERVATION_BASELINE.json` recense **108 626 habitants**, ventilés par culture et religion, et **21 commandes de création/propriété de bâtiments** réparties dans les historiques effectifs. Ces commandes comprennent les niveaux, les PM, les réserves et les propriétaires économiques. Les créations répétées entre fichiers ne sont pas additionnées comme si elles représentaient nécessairement des bâtiments distincts ; leur interprétation finale dépend du moteur.

Le nouveau contrôle `python tools/hbc03_quebec_arc.py --check-conservation` vérifie le total du pays, les effectifs par culture/religion et les commandes économiques ordonnées par type. Il exige aussi que toutes les portions d'État portant ces POPs et bâtiments existent encore sous propriété HBC : laisser les mêmes chiffres dans un scope devenu orphelin ne peut pas faire passer le contrôle. Il ne remplace pas le socle existant. Les seules références à l'État de localisation dans une commande de bâtiment sont normalisées pour autoriser un déplacement cohérent au sein de HBC ; les champs de propriétaire, PM, niveaux et réserves restent protégés.

Le plan `CONSERVATION_PLAN.json` maintient les bâtiments dans les portions HBC de Manitoba, Ontario et Québec. Eastmain conserve justement une portion québécoise au pays. Seuls les POPs du Nunavut nécessitent une réaffectation dans ce scénario : **17 362 habitants vers le Manitoba HBC conservé**. C'est une abstraction explicite de gameplay, pas une migration historique attestée. Rien n'est appliqué ici.

| Portion HBC prévue | Population conservée après réaffectation proposée |
|---|---:|
| Manitoba | 49 873 |
| Ontario | 23 440 |
| Québec | 24 028 |
| Saskatchewan | 11 285 |
| **Total** | **108 626** |

Aucun POP ne doit être copié à la fois dans HBC et dans un pays décentralisé. La démographie de ces nouveaux détenteurs reste à traiter séparément ; le présent plan ne crée ni leur population ni leurs frontières et ne prétend pas résoudre ce problème en laissant des pays vides. Toute modification des scénarios de population devra respecter le total HBC protégé demandé par le joueur.

## Vérification de la côte québécoise en 1776

**Eastmain House : retenu comme présence antérieure au départ.** La biographie universitaire de George Atkinson documente le sloop d'Eastmain en 1769, sa direction du poste en 1772–1773 puis le retour de Thomas Moore en 1773. La thèse de Scott P. Stephen précise une occupation à l'année à partir de 1771. Sources : [Dictionnaire biographique du Canada, George Atkinson](https://www.biographi.ca/fr/bio/atkinson_george_1792_4F.html), [Stephen, *Masters and Servants*, 2006, p. 155, page PDF 163](https://www.collectionscanada.gc.ca/obj/s4/f2/dsk3/MWU/TC-MWU-230.pdf#page=163). Passages pertinents effectivement lus, pas les 372 pages du document.

**Rupert House : réouverture durant 1776, sans date exacte établie pour le 1er janvier. Richmond : fermé en 1759.** Ces deux indications figurent dans le même passage de Stephen. Le plan ne les initialise pas comme postes actifs pour fabriquer un arc plus étendu. Le corridor méridional peut traverser une zone de la future réouverture de Rupert, sans qu'un poste soit pour autant créé ou annoncé actif au départ.

Le point moderne de l'embouchure utilisé pour Eastmain est **52°15′N, 78°30′W**, issu des [instructions nautiques du Service hydrographique du Canada, baie James, ch. 5, §98](https://publications.gc.ca/collections/collection_2022/mpo-dfo/Fs74-6-2021-12-eng.pdf). C'est un repère approché ; il ne certifie pas l'emplacement des bâtiments de 1776. Le calage HBC-02 garde ses limites, et le RGB candidat `x33C3E1` n'est pas annoncé comme une emprise historique exacte.

## Proposition cartographique

L'aperçu `EASTMAIN_ARC.png` et le registre `PROVINCES.csv` prolongent la proposition côtière vers Eastmain : **228 provinces**, soit **5 supplémentaires** par rapport aux 223 de la version précédente. Les cinq postes sont dans la même composante terrestre. Le chemin favorise les provinces proches du littoral, puis remplit les terres entre cette nouvelle ligne et la côte, en miroir du côté occidental.

Toutes les provinces retenues appartiennent déjà à HBC dans les historiques actuels ; aucune terre d'un autre pays ni cellule de mer n'a été ajoutée à la sélection. Ce constat n'autorise pas à les appeler toutes historiquement contrôlées en 1776 : les remplissages et corridors restent des concessions de gameplay explicitement demandées. Le prolongement concerne la rive intérieure des baies, pas la façade atlantique du Québec.

## Vérifications et limites

Les treize contrôles de `VALIDATION.json` passent : conservation démographique et culturelle/religieuse, conservation des commandes économiques, existence des portions HBC portant POPs/bâtiments, maintien de la proposition précédente, connexion des cinq postes, adjacences par bords, propriété actuelle HBC, absence de mer, totaux du plan et absence de modification des fichiers du jeu pendant le calcul. Le contrôle séparé de conservation et huit essais de détection de pertes sont conservés dans `CONSERVATION_CHECK.json` et `CONSERVATION_TESTS.json`. Ces essais couvrent une personne perdue, un changement de culture à total égal, un bâtiment supprimé, un niveau modifié, un PM modifié, un propriétaire économique changé et des scopes orphelins de POPs ou de bâtiments.

À l'implantation, vérifier aussi les références `region_state`, les propriétaires économiques et leurs régions sources, les capacités de ressources dans les États partagés, les hubs/capitales, les infrastructures et le marché. La présence d'une commande d'historique ne garantit pas que le bâtiment a réellement été créé en jeu. Aucune nouvelle partie ni sauvegarde/rechargement exécutés dans ce lot. Aucun fichier runtime modifié et aucun commit.

Les outils et fichiers nécessaires étaient déjà connus : pas de nouvel appel ColGrep ni de reconstruction d'index pour ce complément ciblé. Les erreurs d'accès web (PDF de synthèse fédérale trop volumineux, version anglaise d'une biographie temporairement limitée) n'ont pas été présentées comme des lectures accomplies ; la version française de la biographie et le passage précis de Stephen ont été accessibles.
