# NET 1776 — Nourriture épicée et approvisionnement en sel

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Lot indépendant de la PR #10 (administration / infrastructure) et de la PR #11 (séchage des épices). Ne pas fusionner avant la validation en nouvelle partie.

## Demande

- Activer `pm_spiced_food_preparations` sur les industries alimentaires de la métropole néerlandaise.
- Résoudre la pénurie de sel qui rend les industries alimentaires non rentables, sans attribuer fictivement de gisement massif au pays.

## Constat technique avant correctif

- `NET` possède déjà `distillation`, technologie déverrouillant `pm_spiced_food_preparations`.
- `STATE_HOLLAND` : `building_food_industry` à **2 niveaux**, base `pm_sweeteners`, sans PM épices sélectionné dans l'historique.
- `STATE_FRIESLAND` : `building_food_industry` à **1 niveau**, base `pm_bakery` et `pm_no_spiced_food`.
- Les deux PMs de base consomment du sel : `pm_sweeteners` **10 sel/niveau** et `pm_bakery` **5 sel/niveau**, soit **25 sel** pour les trois niveaux à plein effectif.
- `building_salt_pan` produit **20 sel/niveau** à plein effectif, avec une base de 500 commerçants + 2 000 ouvriers/niveau et sans intrants marchands supplémentaires.
- `STATE_HOLLAND` est un ensemble englobant, dans l'histoire des POPs du mod, la Hollande, la Zélande et Utrecht. Sa carte comprend un port. Un producteur côtier y est plausible.
- Friesland a cinq `building_salt_mine` non découverts dans sa carte ; ce **n'est pas** une extraction de mines de sel exploitable en 1776 et ce lot n'y touche pas.

## Historique / interprétation

**Oui, les Provinces-Unies possèdent des zoutziederijen (sauneries / ateliers de sel raffiné)**. Historiquement, après les restrictions sur l'exploitation de la tourbe salée, les Hollandais importent du sel brut marin et gemme (France, péninsule Ibérique, etc.) qu'ils font dissoudre, épurer et évaporer dans des ateliers côtiers. Une technique locale de concentration de l'eau de mer est aussi attestée au XVIIIe siècle.

Le bâtiment existant `building_salt_pan` est une **approximation de cette activité d'évaporation et raffinage** et non la preuve que les deux niveaux de marchandises produits proviennent uniquement de marais salants néerlandais. Il n'y a pas de nouveau gisement de sel gemme ni de ressource gratuite par décret.

Références :
- DBNL, `Techniek in Nederland`, chapitre sel : https://www.dbnl.org/tekst/lint011tech02_01/lint011tech02_01_0006.php
- National Gallery of Art, historique de la quête néerlandaise du sel : https://www.nga.gov/stories/articles/deadly-business-dutch-quest-salt
- Zeeuwse Ankers, sel de Zélande (commerce et raffinage des imports au-delà du Moyen Âge) : https://www.zeeuwseankers.nl/en/stories/salt-zeeland-gold
- Historique du sel de Zierikzee : https://zeeuwschezoute.nl/en/history/

## Modifications

1. `map_data/state_regions/00_west_europe.txt` : `STATE_HOLLAND.capped_resources` permet **2** niveaux de `building_salt_pan`.
2. `common/history/buildings/00_west_europe.txt` : création en `region_state:NET` de Hollande de **2 niveaux** de `building_salt_pan`, propriété de son `building_financial_district` (`c:NET`, région `STATE_HOLLAND`), PM `default_building_salt_pan`.
3. Dans les mêmes historiques, `pm_spiced_food_preparations` activé pour les **deux niveaux de Hollande** et pour le niveau unique de **Frise**. Toutes les autres méthodes, les niveaux des industries alimentaires et la propriété des bâtiments sont inchangés.

### Bilan nominal, sans prétendre mesurer les prix du marché

- Offre de sel ajoutée **2 × 20 = 40** par semaine de jeu à plein effectif.
- Besoins de sel initiaux de la seule industrie alimentaire métropolitaine : **2 × 10 + 1 × 5 = 25**.
- Marge nominale pour les autres consommateurs : **15**, avant variations de PM, disponibilité des travailleurs, accès au marché, consommation privée et autres installations (existantes ou futures).
- La nourriture épicée consomme **par niveau** 5 épices, 5 café et 10 vin, réduit la production de denrées ordinaires de 15 et ajoute 20 mets raffinés ; les trois niveaux seraient donc une demande nominale de 15 épices, 15 café et 30 vin **en plus** des intrants de base, si tous recrutent.

## À vérifier dans le jeu

- Nouvelle partie 1776 : 2 salines en Hollande ; vérifier leur emplacement, recrutements, production effective de sel, présence au marché néerlandais et disponibilité de ressources dans le panneau de construction.
- Industrie alimentaire Hollande (2) et Frise (1) : méthode Nourriture épicée sélectionnée et légalement/technologiquement utilisable.
- Prix et pénurie de sel, café, vin, épices et autres intrants ; vérifier rentabilité **après 1–4 semaines** ; le sel ne garantit pas à lui seul la rentabilité.
- Comparer les modifications de Hollande avec celles de la PR #10 avant fusion, puisque les deux touchent des segments différents d'un même fichier d'historique.
- Aucun test moteur, recrutement, profits, ni mise à jour d'anciennes sauvegardes n'a été effectué.
