# HBC-02 — postes et continuité sur le bitmap actuel

Date : 25 octobre 2026. Statut : **LOCALISATION_APPROXIMATIVE_ET_RESEAU_TESTES — TRANSFERT_HISTORIQUE_NON_APPLIQUE**.

**Complément actif ultérieur : [HBC-03](../HBC-03/REPORT.md)** prolonge la proposition jusqu'à Eastmain (228 provinces) et protège intégralement les 108 626 habitants ainsi que les bâtiments HBC existants. Les versions de 42 et 223 provinces ci-dessous restent les étapes antérieures conservées pour comparaison ; aucune de ces propositions n'est appliquée au jeu.

**Ajustement visuel demandé ensuite par le joueur :** la proposition active est désormais [COASTAL_CANDIDATE.png](COASTAL_CANDIDATE.png), avec 223 provinces : les 42 provinces du réseau initial et 181 provinces entre la ligne et le littoral, y compris du côté côtier de Cumberland. Les quatre postes restent dans une même composante terrestre. Les six contrôles de `COASTAL_VALIDATION.json` passent. Aucun transfert au jeu. Le résultat initial de 42 provinces décrit ci-dessous est conservé comme référence du corridor, pas comme proposition visuelle finale.

Le remplissage utilise les provinces entières existantes. Elles conservent aussi quatre petits fragments détachés de 6, 5, 4 et 4 pixels, sans poste cible : ils ne sont pas maquillés comme une seule composante. La composante principale de 50 451 pixels contient les quatre postes ; aucun nouveau poste isolé n'est créé. Total de la proposition : 50 470 pixels. La vérification de ravitaillement moteur demeure à faire.

## Résultat concret

Un scénario de **42 provinces / 9 086 pixels** relie York Factory, Moose Factory, Prince of Wales/Churchill et Cumberland House. Les quatre points et tous les pixels de la sélection appartiennent à **une seule composante connexe**, par des bords de cellules, sans simple contact diagonal. Le registre détaillé est `PROVINCE_CANDIDATES.csv`, les chemins sont dans `CORRIDOR_CANDIDATE.json` et l'aperçu dans `CONNECTED_CANDIDATE.png`.

Ce résultat démontre la faisabilité géométrique de la contrainte du joueur. Il ne détermine pas la frontière historique, ne répartit pas les terres autochtones et ne représente pas encore tous les postes. **Aucun fichier du jeu n'a été modifié ; aucun contrôle moteur de l'accès au marché n'a été effectué.** Les 2 246 RGB / 522 774 pixels de l'actuelle HBC restent donc présents dans les données de départ.

Le coût des chemins pénalise la superficie des provinces ; il ne connaît ni route historique, ni portage, ni souveraineté. En particulier, le trajet direct vers Cumberland ne doit pas être adopté comme un corridor historique sans confrontation aux itinéraires fluviaux. Ce n'est pas une proposition de remplacer immédiatement toute la HBC par ces seules 42 provinces.

## Travaux réutilisés et contrôle des positions

Les dossiers R8 et HBC-01 restent la base historique. Le catalogue MAP1 des hubs apporte des noms de repères, mais leurs positions ont été **relues dans les fichiers de locators effectifs**, puis échantillonnées sur le bitmap actuel et confrontées aux RGB des définitions actuelles. Les coordonnées modernes proviennent principalement du `cities1000.zip` déjà archivé, avec ses empreintes et son attribution GeoNames ; aucune nouvelle indexation mondiale ni restauration d'une ancienne carte.

Le calage nord-américain utilise six repères FIT et onze CHECK séparés, avec trois modèles comparés. Pour Miller affine : RMS FIT **5,81 px**, RMS CHECK **9,04 px**, maximum CHECK **15,12 px** ; sur les six CHECK intérieurs au domaine FIT : RMS **8,43 px**, maximum **12,47 px**. Ces écarts aux hubs **ne sont pas une marge garantie sur un site historique**. Aucun CHECK n'est un relevé indépendant d'un site ancien : la précision historique certifiée reste `NOT_ESTABLISHED`.

Les RGB diagnostics sont : York `x92E099`, Moose `x627826`, Churchill `xEB9647`, Cumberland `x1BC323`. Pour York et Moose, ils viennent des hubs nommés actuels ; les deux autres sont les cellules HBC les plus proches des prédictions approximatives. Tous restent **candidats non certifiés historiquement**. Les variantes de modèle et l'ensemble des RGB HBC voisins sont conservés dans `POST_CANDIDATES.json` pour éviter de masquer l'incertitude.

Deux homonymes Fort Smith existent dans l'atlas : celui d'Arkansas a été écarté du domaine nord-canadien avant tout ajustement. Le modèle local ColGrep n'a pas fait cette décision géographique ; les résultats de recherche ont été contrôlés.

## Chronologie : compléments ciblés

- **York Factory** : le site de 1776 est York II (1715–1788), pas le complexe actuel de York III. Parcs Canada situe les deux anciens établissements environ un kilomètre en aval, désormais érodés. Le point moderne est donc explicitement un repère approché, pas l'emplacement exact de 1776. [Parcs Canada, intégrité commémorative](https://www.parks.canada.ca/lhn-nhs/mb/yorkfactory/info/commemoration).
- **Cumberland House** : fondation en 1774, déplacement de deux kilomètres vers l'ouest en 1793. Le point du parc actuel ne doit pas devenir rétroactivement le poste original exact. [Parcs Canada, désignation](https://www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=736), [Tourism Saskatchewan, coordonnées du parc](https://www.tourismsaskatchewan.com/listings/1421/cumberland-house-provincial-historic-park).
- **Severn** : le catalogue de BAC contient explicitement une correspondance reçue et envoyée en 1775–1776. C'est un indice plus précis de continuité que le seul inventaire multiépoque des postes. Les lettres n'ont pas été dépouillées et le site original reste à cartographier. [BAC, William Falconer, MG19-D2](https://recherche-collection-search.bac-lac.gc.ca/eng/Home/Record?IdNumber=115489&app=fonandcol&q=LASTER).
- **Henley/Albany** : les extraits de travaux universitaires et de notes citant les journaux HBC signalent les préparatifs de bateaux pendant l'hiver 1775 et des échanges en 1776. Ils renforcent la continuité, sans fournir ici une emprise RGB ni un dépouillement direct des originaux. [Thèse, extrait indexé p. 158](https://mspace.lib.umanitoba.ca/server/api/core/bitstreams/6331c6cc-718f-4662-bdcc-c159112d0c7f/content), [notes Jenkin Daniel, références HBCA B.86](https://www.metismuseum.ca/media/document.php/07207.Notes%20on%20Jenkin%20Daniel.pdf).
- **Eastmain/Rupert** : une thèse décrit Eastmain occupé à l'année à partir de 1771 et une maison à Rupert en 1776. Extrait indexé seulement ; la date dans l'année demeure essentielle pour Rupert. Pas de poste automatiquement créé au 1er janvier. [Thèse, extrait indexé p. 155](https://www.collectionscanada.gc.ca/obj/s4/f2/dsk3/MWU/TC-MWU-230.pdf).

## Contrôles et défauts détectés

Le premier réseau de provinces paraissait continu mais conservait quatre pixels détachés via le RGB `x257105`. Le calcul écarte désormais ce RGB et prend un autre passage : **une composante de 9 086 pixels**, aucune enclave résiduelle dans ce scénario. Le bitmap original n'a pas été retouché ; la petite composante est un constat technique préexistant, pas une nouvelle attribution historique.

Les sept contrôles de `VALIDATION.json` passent : cohérence des repères échantillonnés, quatre cibles, chemins accessibles dans le graphe, contacts par bords, points dans une même composante, totalité des pixels sélectionnés connectée et empreintes des fichiers du jeu inchangées pendant le calcul. Cinq tests unitaires couvrent notamment les contacts diagonaux, les fragments d'un même RGB et un poste injoignable. Le fichier `TESTS.json` conserve leur résultat.

**Limites restantes avant implantation :** contrôler physiquement les positions de Churchill/Cumberland et les itinéraires retenus ; compléter Albany, Henley, Severn et Eastmain ; déterminer les propriétaires autochtones par secteur et leurs abstractions politiques ; répartir POPs, bâtiments et capitales sans perte ; vérifier infrastructures et connexion au marché britannique dans une nouvelle partie. Une liaison dessinée ne suffit pas à prouver le ravitaillement. L'incorporation administrative d'un État ne se déduit pas d'une ligne de provinces.

## Recherche locale

Deux lancements ColGrep dans ce lot : un échec de verrou avant recherche, puis une exécution locale terminée avec code 0. Les pistes `tools/map2m_r8.py:269–284` et `common/history/countries/hbc - hudson bay company.txt:1–56` ont été contrôlées. La première est un exemple réutilisable de lecture des locators/adjacences, situé dans une passe de Poméranie ; elle n'est pas une source géographique nord-américaine. L'agent a aussi renvoyé des dossiers R8 déjà connus malgré la consigne d'éviter ces répétitions. Son apport est donc limité à quelques pistes de code. Durée complète de l'inférence et tokens Codex non instrumentés ; aucune économie exacte ni utilisation GPU mesurée n'est affirmée.

## Prochaine action

Suivre `NEXT_ACTION.md`. Ne pas lancer une réaffectation massive à partir de ce prototype. Le statut des suivis WORLD/SERG et leurs validations n'est pas modifié par ce lot nord-américain.
