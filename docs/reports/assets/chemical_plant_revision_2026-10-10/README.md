# Usine chimique — vue plongeante et biens sans support

Révision demandée le 10 octobre 2026. Le décor frontal de l'usine est remplacé par des toitures et une cour vues depuis le dessus, sans ciel ni horizon, d'après les icônes chimiques et sidérurgiques vanilla locales.

Après la correction demandée par le joueur, le support en bois est entièrement supprimé. Le pot et les quatre flacons sont des biens flottants au premier plan, sans caisse, table ou socle. Le cadre et les identifiants visuels de l'usine restent présents.

- Master final : `assets/icon_sources/chemical_plant_overhead_2026-10-10.png`.
- Texture utilisée en jeu : `gfx/interface/icons/building_icons/1776_chemical_plant.dds`.
- Ancien master conservé : `assets/icon_sources/chemical_plant_approved.png`.
- Méthode : deux retouches avec imagegen intégré, puis export mécanique sans redessin. Les prompts complets, références et empreintes sont dans `manifest.json`.

Contrôles : inspection à 48/64/96/256 pixels, coins extérieurs transparents, absence de trous dans le décor, alpha généré préservé (intérieur quasi opaque, minimum 248/255), DDS natif BGRA8 de 256 × 256 avec neuf mipmaps et reconstruction exacte depuis le registre. Un seul fichier de jeu est modifié ; les 1 411 autres fichiers de `common/` et `gfx/` restent identiques. Les aperçus et références décodées sont uniquement dans le cache ignoré.

Aucun essai en jeu, push, merge ou commit effectué. Les paramètres du bâtiment et ses méthodes de production ne changent pas.
