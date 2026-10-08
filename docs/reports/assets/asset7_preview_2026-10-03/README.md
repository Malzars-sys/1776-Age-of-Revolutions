# Lot 4 — Standards et recherche scientifique

Date : 3 octobre 2026. **Lot repris après confirmation par le joueur de ses vérifications en jeu des couleurs corrigées.** Trois aperçus à créer et à valider avant intégration. Aucun essai moteur effectué par l'agent n'est revendiqué.

**Livraison intégrée le 3 octobre 2026 après accord du joueur pour les trois icônes.** La métrologie approuvée est conservée ; la lettre et la recherche expérimentale utilisent leurs V2 retouchées. Les trois technologies sont reliées à leurs nouveaux DDS natifs.

## Intégration approuvée

- [Manifeste et accord d'intégration](integration_manifest.json), [contrôle indépendant des DDS et des définitions](integration_static_validation.json), [planche décodée depuis les DDS](LOT_4_DDS_INTEGRES_QA.png).
- DDS natifs BGRA8/A8R8G8B8, 256 × 256, neuf mipmaps. Chaque niveau décodé conserve exactement les couleurs RGBA et l'alpha de la réduction préparée à l'export. Aucun filtre de recoloriage.
- Seuls les trois champs `texture` dans `common/technology/technologies/30_tech3a_society.txt` ont changé ; 1 209 autres fichiers protégés restent identiques, trois DDS sont ajoutés. Aucun effet, prérequis ou paramètre de gameplay ne change.
- Aucun essai moteur effectué par l'agent n'est revendiqué : le rendu en jeu devra être vérifié après rechargement ou redémarrage. Les validations d'aperçu ci-dessous restent les preuves historiques antérieures à l'intégration.

- [Échanges scientifiques — master PNG retenu V2](previews/institutionalized_scientific_exchange_v2.png).
- [Métrologie scientifique — master PNG retenu V2](previews/scientific_metrology_v2.png).
- [Recherche expérimentale — master PNG retenu V2](previews/experimental_research_laboratories_v2.png).
- [Planche du lot et lectures réduites](LOT_4_APERCU.png), [comparaison avec deux technologies vanilla](LOT_4_COMPARAISON_VANILLA.png), [transparence sur damier](LOT_4_ALPHA_DAMIER.png).
- [Prompts réellement envoyés à l'outil intégré](generation_requests.json), [provenance des sorties initiales](generation_results.json), [prompt et provenance de la révision](metrology_revision.json).
- [Prompts complets des deux retouches demandées](user_revision_requests_v2.json), [provenance de leurs sorties](user_revision_results_v2.json).

Les masters font 1 254 × 1 254 pixels avec une véritable couche alpha ; des PNG 256 × 256 sont préparés séparément dans `target_size_png/`. Les contrôles confirment les quatre coins transparents, les versions réduites, les empreintes des masters et la conservation des **1 210 fichiers `common` et `gfx`** de l'état de référence repris. Les images affichées pour la lecture sur fonds d'interface sont des compositions de contrôle ; ces fonds ne sont pas ajoutés aux masters.

La première métrologie avait un résidu alpha de 1/255 dans un coin vide. Une seule révision ciblée a été demandée à l'outil intégré, sans nettoyage automatique ou filtre de couleur ; les quatre coins de la V2 ont un alpha de zéro. L'original reste conservé dans `previews/scientific_metrology.png`. Cette révision reste une sortie générative : elle préserve visuellement le sujet et la composition, mais aucune identité pixel par pixel de la peinture avec la V1 n'est revendiquée.

Inspection visuelle actualisée : enveloppe blanche sans écriture extérieure, fermée par son cachet rouge, avec feuilles manuscrites dessous ; trois poids de tailles distinctes dans un coffret en bois et règle grise ; microscope en laiton à côté de la bouteille à trois cols et de la cornue. Les masses restent identifiables à 32/48/64 px sur les deux fonds, aucun tube ni instrument essentiel n'est coupé. Les petits caractères sont des évocations manuscrites, pas du texte à lire en jeu. Pas de cadre ou médaillon dessiné dans les technologies. Le montage de verrerie est une convention illustrative, pas une reconstitution scientifique certifiée.

## Retouches demandées par le joueur

Deux éditions distinctes ont été réalisées avec l'outil intégré imagegen. La lettre conserve sa plume et son cachet, mais son enveloppe est maintenant blanche et vierge ; l'écriture est limitée aux feuilles libres en dessous. La recherche expérimentale ajoute le microscope de la [photographie fournie par le joueur](references/user_microscope.png), traduit dans le même style peint, sans les boîtes de rangement et le fond de la photographie. La date et le fabricant de ce microscope ne sont pas vérifiés ; aucune attribution précise à 1776 n'est revendiquée.

La métrologie n'a été ni régénérée ni retouchée : son empreinte reste `9d33c29e8fa3989b5272a8e1126b7aaf3b97d195844c59dfbb8610cfebdab22e`. Les premières versions des deux autres masters restent dans `previews/`. Les anciennes planches et preuves de contrôle restent dans `before_user_revision_v2/`. Les nouvelles éditions sont génératives : la conservation visuelle du style ne signifie pas une identité pixel par pixel avec les originaux.

Contrôles avant intégration, après retouches : masters 1 254 × 1 254 RGBA, quatre coins exactement transparents, lecture réduite inspectée sur deux fonds et sur damier, **1 210 fichiers `common` et `gfx` inchangés** par rapport à la référence d'aperçu. L'accord ultérieur « tu peux tout intégrer » approuve aussi les deux nouvelles retouches ; les sources restent conservées sans modification.

Trois technologies complètent la chaîne scientifique : **Échanges scientifiques**, **Métrologie scientifique** et **Recherche expérimentale**. Avant intégration, les deux dernières utilisaient une image d'erreur et la première une illustration externe provisoire. Elles utilisent maintenant les trois créations approuvées, sans adaptation de cette illustration externe.

Les biens de données, le laboratoire et ses PM sont conservés. Les statistiques d'État et l'éducation polytechnique possèdent déjà des réemplois vanilla et ne sont pas remplacées dans ce lot. La chaîne du cuivre reste exclue.

## Références recherchées avant génération

Les recherches d'images précèdent la création. Les notices suivantes documentent la forme des objets ; les photographies ne sont pas téléchargées, copiées dans le mod ou injectées dans le générateur.

- Correspondance : [collections de la Royal Society](https://makingscience.royalsociety.org/collections), séries Early Letters et Letters and Papers. La notice indexée décrit les échanges scientifiques du XVIIIe siècle ; l'ouverture directe a rencontré une erreur 502. Une [lettre de Richard Waller, 1714](https://makingscience.royalsociety.org/items/el_w3_93/letter-from-richard-waller-to-prince-alexander-menzicoff-menshikov-dated-at-london) a aussi été trouvée en recherche d'images, sans reproduction de son texte.
- Poids et mesures : [coffret de balance et poids, 1763, Science Museum Group](https://collection.sciencemuseumgroup.org.uk/objects/co57836/box-of-scales-and-weights) ; [ensemble britannique, probablement XVIIIe siècle, Metropolitan Museum](https://www.metmuseum.org/art/collection/search/204745). Laiton, acier et bois ; la règle du futur dessin est une convention illustrative des mesures, pas une copie attribuée à ces ensembles.
- Expérimentation : [bouteille de Woulfe, 1801–1850, Science Museum Group](https://collection.sciencemuseumgroup.org.uk/objects/co116857/woulfes-bottle) et [cornue en verre soufflé, 1750–1850](https://collection.sciencemuseumgroup.org.uk/objects/co131677/green-glass-retort). Le montage simplifié est une convention de technologie, pas une reconstitution technique exacte. Aucun brûleur Bunsen, fiole Erlenmeyer ni matériel électrique moderne.

Les ères sont celles des définitions actuelles : I, IV et V. Une ère n'est pas arbitrairement traduite en année précise. Les références du début du XIXe siècle ne sont pas présentées comme des objets fabriqués en 1776.

## Règles et livrables

Mode : outil intégré de génération d'images, une création distincte par technologie. Les [prompts complets et raccordements proposés](generation_plan.json) conservent les contraintes et les références de style.

Références locales de style : `academia` et `mechanical_tools` du jeu installé, déjà décodées pour ASSET5 et inspectées visuellement. Elles servent uniquement de comparaison, sans redistribution comme nouvelles créations.

Objets peints, silhouette compacte, matières naturelles et patinées. La règle initiale d'un accessoire signifiant au maximum est adaptée à la demande explicite du joueur : feuilles libres sous l'enveloppe et microscope supplémentaire auprès de la verrerie. L'écriture est autorisée uniquement sur ces feuilles libres ; l'enveloppe cachetée reste vierge. Papier blanc chaud, pas de sépia uniforme. Aucun cadre de bâtiment, médaillon, fond factice, chiffre décoratif, badge ou filigrane. Vraie transparence demandée au générateur et conservée sans détourage ou recoloriage automatique.

Masters PNG carrés d'au moins 1024 px ; réductions de contrôle à 256, 64, 48 et 32 px, sur fonds clair/sombre et damier. Format de jeu intégré : 256 px avec neuf mipmaps. **Les DDS et références n'ont été intégrés qu'après validation du joueur.** Les prix, recettes, recherche, emplois et autres paramètres ne changent pas.

Le script `tools/build_asset7_preview_sheet.cjs` prépare un état de référence des fichiers `common` et `gfx`, puis vérifie leur conservation, les dimensions, les coins transparents et les nouvelles cibles. La comparaison native et la lecture réduite demandent également une inspection visuelle ; un contrôle technique seul ne garantit pas une bonne illustration.

Le premier état de référence, enregistré avant la correction des DDS, est conservé comme instantané historique. La reprise utilise explicitement `gameplay_and_gfx_baseline_after_color_fix.json`, enregistré après les corrections confirmées par le joueur ; l'ancien fichier n'est ni écrasé ni contourné. Voir le [diagnostic de compatibilité de toutes les familles](../all_asset_color_layout_2026-10-03/README.md). Les futurs exports devront utiliser le stockage BGRA natif et être contrôlés après export, pas seulement sur les PNG.

Nouvelle recherche d'images avant génération le 3 octobre : lettre de la Royal Society, coffret de 1763, bouteille de Woulfe et cornue en verre (sources ci-dessus). Les notices du Science Museum sont accessibles ; l'ouverture directe de leurs photographies échoue dans l'outil de recherche, et la page Royal Society renvoie 502. Les résultats de recherche d'images documentent néanmoins les formes ; aucun téléchargement de ces photographies ni injection comme image de référence dans le générateur. Les deux icônes vanilla locales sont inspectées pour guider la description du style, sans servir de cible d'édition.
