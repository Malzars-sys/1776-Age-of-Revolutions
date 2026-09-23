# Centres de commerce — mécanique effective Victoria 3 1.13.11 + fork

Date de l’audit : 2026-09-16  
Portée : audit technique uniquement, sans modification du système.

## Résultat direct

- **ID exact :** `building_trade_center`.
- **Placement historique :** oui, via `create_building` dans `common/history/buildings`, sous le couple `s:STATE_*` / `region_state:TAG`. Ce n’est pas une entrée de `common/history/states`.
- **Génération par routes commerciales :** non dans le système 1.13.11. Les centres de commerce sont des bâtiments construits ou préplacés qui donnent la capacité utilisée par le commerce mondial autonome ; une route commerciale ne crée pas automatiquement un niveau.
- **Niveaux manuels actuels :** 242 implantations, 383 niveaux au total dans le working tree.
- **Conservation :** un niveau créé dans l’historique est chargé comme tout autre niveau de bâtiment. Il peut ensuite être agrandi ou réduit selon l’activité et les règles normales.

## Emplois et capacité

Le PM de base `pm_trade_center` ajoute par niveau 800 employés de bureau et 200 commerçants. À effectif complet, il fournit par niveau :

- `state_weekly_trades_add = 1` ;
- `state_trade_capacity_add = 10`.

Le PM quantitatif normal, actif par défaut, consomme `goods_input_merchant_marine_add = 4` à l’échelle de la main-d’œuvre. Le groupe `bg_trade` consomme aussi 0,5 infrastructure par niveau, n’emploie pas l’économie d’échelle et porte les revenus commerciaux.

## Interaction avec le commerce, les ports et le marché

- Le niveau ne représente pas une route individuelle : il fournit de la capacité et un nombre de transactions hebdomadaires au commerce autonome.
- Le centre n’a pas besoin d’être côtier. En revanche, l’accès au marché mondial demeure nécessaire ; un pays enclavé doit disposer d’un accès ou de droits de transit.
- Les ports produisent le bien `merchant_marine` consommé par le centre de commerce. Leur relation est donc économique et logistique, pas une relation de génération automatique.
- Les avantages commerciaux, accords, ports de traité, embargos, guerres, intérêts et péages influencent où et comment la capacité est utilisée.
- La construction publique ou privée appelle `trade_center_construction_allowed`. L’isolationnisme l’interdit normalement ; les lois Canton System et Sakoku imposent des États et plafonds spécifiques.

## Risques d’un niveau manuel

Un niveau préplacé sans volume commercial correspondant peut créer des emplois non rentables, une demande de marine marchande, une consommation d’infrastructure et de la capacité inutilisée. Le moteur peut ensuite envisager une réduction automatique lorsque la capacité inutilisée dépasse ses seuils. Il n’existe pas de risque de « doublon par route », mais il existe un risque de surcapacité si l’historique et la construction ultérieure sont tous deux trop généreux.

## Sources techniques

- `common/buildings/11_private_infrastructure.txt` — définition et règles de construction ;
- `common/production_method_groups/11_private_infrastructure.txt` — PMG ;
- `common/production_methods/11_private_infrastructure.txt` — emplois, capacité et marine marchande ;
- `common/building_groups/00_building_groups.txt` (vanilla effectif) — groupe `bg_trade` ;
- `common/scripted_triggers/00_building_triggers.txt` (vanilla effectif) — restrictions de construction ;
- `common/defines/00_defines.txt` (vanilla effectif) — sélection, avantage et réduction automatique ;
- `common/history/buildings/*.txt` — niveaux initiaux du fork.
