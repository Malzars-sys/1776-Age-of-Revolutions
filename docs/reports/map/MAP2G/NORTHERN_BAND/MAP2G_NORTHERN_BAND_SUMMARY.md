# MAP‑2G — Bande septentrionale Qing : correctif complémentaire

## Résultat appliqué

136 RGB réattribués à deux administrations existantes, toutes deux demeurant vassales des Qing. Aucun nouveau pays et aucune retouche du bitmap. Les frontières extérieures de l'ensemble impérial ne changent pas.

| Ensemble | Avant | Après | RGB transférés | Population correspondante |
|---|---|---|---:|---:|
| `STATE_JETISY`, totalité | CHI | XIN, Gouvernement militaire d'Ili | 121 | 133 642 |
| `STATE_ALTAI`, corridor méridional | CHI | MGL, Administration d'Ouliastaï | 15 | 7 840 |
| `STATE_ALTAI`, secteur septentrional conservé | CHI | CHI | 0 ; 39 RGB conservés | 23 160 |

`MGL` est renommé **Administration d'Ouliastaï** / **Uliastai Frontier Administration**, en français et en anglais. Cela représente une administration impériale regroupée, comprenant notamment des communautés uriankhaïes et oïrates : le nom n'affirme plus qu'elles seraient toutes khalkhas. Ni la culture des populations, ni les cultures principales du pays ne sont modifiées.

La bande occidentale identifiée dans le bitmap relève de **Jetisy**, et pas seulement de l'Altaï. Jetisy constitue ici une interface limitée avec l'ancien périmètre R3 : aucune autre correction de cette région n'est entreprise. La dernière capture fournie montre le nord du Jilin, pas la bande d'Ili ; l'identification de cette bande repose donc sur les historiques et le bitmap, et devra être confirmée visuellement par le joueur.

## Justification et limites historiques

- **Jetisy → Ili.** Le gouvernement militaire créé en 1762 comprend les juridictions d'Ili et de Tarbagataï. Le correctif délègue au sujet `XIN` le territoire déjà représenté comme impérial ; il ne transforme pas une nouvelle allégeance nomade en annexion. Le découpage entier de Jetisy demeure une **approximation documentée**, notamment sur les marges pastorales kazakhes et kirghizes : il ne prouve pas une administration Qing uniforme de chaque vallée. Références : [UNESCO, History of Civilizations of Central Asia, vol. V, p. 203](https://uzbekliterature.uz/sites/default/files/history-of-civilizations-of-central-asia-vol-5.pdf), [Qing Shi Gao, vol. 206, tableaux des offices frontaliers](https://24histories.com/qingshigao/206).
- **Altaï méridional → Ouliastaï.** Le *Qing Shi Gao*, vol. 524, décrit les communautés uriankhaïes, leur réorganisation dans les années 1750–1760, les pâturages de la Chuya et les rapports avec Kobdo. Quinze provinces existantes regroupent grossièrement le corridor méridional autour des locators de Kosh‑Agach/Belyashi ; cette sélection n'est ni une limite fiscale précisément reconstituée, ni la frontière de 1864. Kobdo était une juridiction réelle, distincte des Khalkhas : son regroupement sous `MGL` est une abstraction administrative de gameplay, pas une assimilation ethnique. Références : [Qing Shi Gao, vol. 524, sections 13–16](https://24histories.com/qingshigao/524), [article du responsable de la recherche sur le Xinjiang, Académie chinoise des sciences sociales, 2024](https://www.dswxyjy.org.cn/n1/2024/0726/c244516-40286184.html).
- **Altaï septentrional conservé directement Qing, provisoirement.** Ulala et plusieurs secteurs forestiers du nord du State Region ne peuvent pas être assimilés automatiquement aux pâturages de Kobdo. Les adhésions russes de 1756 et les situations de tribut partagé rendent l'attribution globale trompeuse. La souveraineté de départ est conservée conformément au périmètre de cette tâche, sans prétendre la valider historiquement. Aucune nouvelle annexion russe n'est appliquée. Référence contradictoire conservée : [notice historique incluse dans le schéma territorial de la République d'Altaï, 2018](https://altai-gov.ru/doc/19826). Ce cas reste **UNRESOLVED**.

Il n'est donc pas créé d'Administration de Kobdo supplémentaire. Une telle création exigerait de détacher une zone plus large de l'actuel `STATE_ULIASTAI` ; cela dépasserait la correction minimale de la bande. Gansu, Alxa, Qinghai et les administrations provinciales chinoises restent inchangés. Aucun tracé de 1860–1864 ou changement administratif de 1907 n'est importé.

## Populations, économie et armée

| Région / groupe existant | Avant CHI | Après CHI | Après XIN | Après MGL |
|---|---:|---:|---:|---:|
| Jetisy — Kazakhs | 50 642 | 0 | 50 642 | 0 |
| Jetisy — Ouïghours | 43 000 | 0 | 43 000 | 0 |
| Jetisy — Kirghizes | 40 000 | 0 | 40 000 | 0 |
| Altaï — groupe `mongol`, animiste, étiqueté « Altaians » dans l'historique | 22 940 | 17 138 | 0 | 5 802 |
| Altaï — Tatars | 3 410 | 2 548 | 0 | 862 |
| Altaï — Russes | 4 650 | 3 474 | 0 | 1 176 |
| **Total des deux régions** | **164 642** | **23 160** | **133 642** | **7 840** |

Le partage de l'Altaï utilise les superficies des RGB retenus à l'intérieur de chaque groupe existant, avec arrondi conservatif. C'est une allocation technique faute de recensement par province, **pas une estimation historique**. Tous les autres attributs des populations restent identiques. Population mondiale : **835 804 980 avant et après**.

Les deux régions n'ont aucun bâtiment civil explicite ni recrutement militaire déclaré dans les historiques effectifs. Aucune caserne, administration ou unité n'a donc été supprimée ou déplacée. Le sélecteur vide des bâtiments de Jetisy suit simplement son nouveau propriétaire. Les méthodes de production, réserves, propriétaires économiques, bâtiments, unités, formations et commandants mondiaux sont conservés. Capitales et pactes de vassalité inchangés ; hubs, locators, ressources et arable également inchangés.

Il n'est ajouté aucune demande d'infrastructure provenant d'un bâtiment déclaré. Les fermes de subsistance générées, l'emploi, les budgets et l'accès au marché restent à observer en jeu : les contrôles statiques ne garantissent pas leur état effectif.

## Diagnostic séparé : les 508 habitants du nord du Jilin

Le nom affiché « Nord du Jilin » correspond à `STATE_OUTER_MANCHURIA`. Son historique contient **453 habitants de culture `siberian` et 55 Mandchous**, soit **508**. Ces deux groupes et leurs tailles étaient déjà identiques dans la baseline antérieure à MAP‑2G ; ce lot et le présent correctif ne les ont pas réduits.

La capture du joueur confirme 508 habitants, zéro paysan et une population entièrement affamée. La définition régionale possède pourtant **25 terres arables** et un bâtiment de subsistance. L'absence de paysans n'est donc pas expliquée par une définition avec zéro terre arable ; sa cause moteur n'est pas établie par l'inspection statique. Aucun recensement de 1776 ne valide ici le total de 508. Il s'agit d'une donnée héritée suspecte, à investiguer séparément, pas d'une population historique déclarée normale. Aucune création de population, conversion culturelle ou redistribution non autorisée n'est appliquée.

## Fichiers de jeu modifiés

1. `common/history/states/00_states.txt` : Jetisy et quinze RGB de l'Altaï.
2. `common/history/pops/09_central_asia.txt` : sélecteur de Jetisy, tailles et attributs inchangés.
3. `common/history/pops/15_russia.txt` : partage conservatif des trois groupes de l'Altaï.
4. `common/history/buildings/09_central_asia.txt` : sélecteur vide de Jetisy.
5. `localization/french/replace/1776_map2g_l_french.yml` : nom et adjectif de MGL.
6. `localization/english/replace/1776_map2g_l_english.yml` : même renommage en anglais.

Le script dédié et les preuves légères sont nouveaux. La baseline est un inventaire, des empreintes et des sources textuelles : aucune copie complète du mod ni ZIP volumineux. Les anciennes preuves MAP‑2G sont conservées ; leur manifeste représente le lot initial, celui du présent dossier représente son complément.

## Livrables et vérifications

- [`IMPLEMENTATION.json`](IMPLEMENTATION.json) : **liste exhaustive des 136 RGB transférés**, avant/après, populations et 39 RGB conservés directement Qing.
- [`VALIDATION.json`](VALIDATION.json) : contrôles statiques, conservation et limites du test.
- [`GEOGRAPHY.json`](GEOGRAPHY.json) : boîtes régionales et positions physiques des hubs ; aucun déplacement de locator.
- [`BAND_before.png`](BAND_before.png) et [`BAND_after.png`](BAND_after.png) : même bitmap, même cadrage, propriétaires avant/après.
- `INTEGRATION.patch` : correctif reproductible pour la baseline de ce dossier uniquement.

Les tests comparent exactement le manifeste, les profils démographiques complets, les bâtiments et les unités. Ils vérifient aussi les dépendances Qing, Ezo, Formosa, les modèles logiques ottomans et d'infrastructure IA, les anciennes régions et l'absence d'autres fichiers de jeu modifiés. Les doublons et références orphelines hérités restent identiques, sans nouvelle anomalie. **Aucun commit, merge ou push ; HEAD, index et références du workspace principal inchangés.**

Dans une **nouvelle partie**, inspecter :

1. Jetisy appartient à Ili ; le corridor méridional de l'Altaï à Ouliastaï. Le nord reste Qing et est explicitement reporté.
2. Ouliastaï et Ili restent sujets des Qing, avec leurs capitales d'origine.
3. Populations de Jetisy : 133 642 ; fragments de l'Altaï : 23 160 Qing + 7 840 Ouliastaï.
4. Après un mois, vérifier emploi de subsistance, alimentation, infrastructure et accès au marché des deux fragments. Les déficits éventuels doivent être documentés, pas comblés par des habitants inventés.
5. Confirmer que les résultats Ezo/Aïnous et Formosa déjà validés restent identiques. Le nord du Jilin n'a pas été corrigé dans ce lot.

**MAP‑2H n'est pas commencé.**
