# Icônes des méthodes de quincaillerie — 25 octobre 2026

Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. Création et intégration demandées par le joueur ; rendu moteur non testé.

La [galerie vanilla indiquée par le joueur](https://vic3.paradoxwikis.com/Category:Production_methods_icons) a été consultée dans le navigateur : silhouettes simples, contours marqués, détails limités. La lecture Web directe renvoyait 401, mais le navigateur a chargé la catégorie normalement. Les icônes `furniture_handicraft.dds` et `lathes.dds` ont aussi été inspectées dans l'installation canonique en lecture seule.

La référence rouge est bien celle des **canaux**, selon la correction du joueur : `1776_industrial_canals_pm.dds` et `1776_engineered_canals_pm.dds`. Leur palette corail, les traits bordeaux et le fond transparent servent de références visuelles au service intégré imagegen. Quatre appels distincts ; prompts conservés dans `PROMPTS.json`. Aucun modèle/API CLI supplémentaire.

| PM | Nouveau dessin | Texture dans `gfx/interface/icons/production_method_icons/` |
|---|---|---|
| Forgée et moulée | Enclume, marteau, moule de boutons | `1776_hardware_forged_cast_red.dds` |
| Cuivre et laiton | Bouilloire, bougeoir, plat | `1776_hardware_copper_brass_red.dds` |
| Usinée | Tour, roue dentée, charnière | `1776_hardware_machined_red.dds` |
| Industrialisée | Presse, plaques embouties, cuillères | `1776_hardware_industrial_red.dds` |

Le neutre pointe directement vers **`gfx/interface/icons/production_method_icons/unused/disabled.dds`**, la même référence que `pm_no_canal_network`. Aucun dessin ou fichier dupliqué pour le neutre.

Les quatre PNG maîtres sont conservés dans `workshop_assets/source/hardware_pm_icons/` : `01_forged_cast_red.png`, `02_copper_brass_red.png`, `03_machined_red.png`, `04_industrial_red.png`. Export DDS natif BGRA8 à 208 × 208 avec huit mipmaps complets, comme les références de canaux du mod. Alpha réel conservé ; aucune recoloration ou retouche du PNG après génération. Le script effectue uniquement la réduction et la conversion de stockage.

Fichiers de code concernés : cinq propriétés `texture` dans `common/production_methods/1776_alloys_utensils.txt`, ajout de `tools/build_hardware_pm_icons.py`, adaptation du contrôle du PM neutre dans `tools/test_econ_alloys_1776.py`. Quatre entrées sont ajoutées à `docs/reports/assets/source_registry.json`, avec sources et empreintes ; les autres entrées sont comparées et préservées. Le rapport économique principal est actualisé pour distinguer icône du bien et icônes de PM.

Contrôles : décodage exact du premier niveau DDS, ordre BGRA, chaîne de mipmaps, alpha 0–255 et coins transparents, famille rouge, existence et correspondance des cinq références, égalité des définitions de PM après retrait des seuls champs `texture`. Recettes, emplois, technologies, artillerie, icône du bien et dessins des canaux ne changent pas. Sources et empreintes : `VALIDATION.json`, avant : `BASELINE.json` et `REGISTRY_BEFORE.json`.

Les 16 contrôles économiques ont aussi été exécutés ; résultat dans `ECONOMIC_TESTS.json`. Le premier passage a signalé uniquement un garde Git historique devenu périmé : le HEAD courant `7ed0f574` diffère de la baseline de la session précédente `9b1764e3`. La baseline est conservée. Le garde vérifie désormais l'absence de modification de HEAD/index pendant chaque exécution des tests et consigne séparément cette dérive historique dans `GIT_BASELINE_AUDIT.json`, sans restaurer ni réécrire Git. Les autres contrôles du premier passage étaient réussis.

[Planche de contrôle](PREVIEW.png) inspectée sur fonds sombre/clair à 208, 32, 48 et 64 pixels. En jeu, vérifier les cinq choix dans la manufacture, l'absence de fond opaque et les infobulles. Aucun résultat moteur ni validation humaine n'est inventé. Aucun commit/staging/push.
