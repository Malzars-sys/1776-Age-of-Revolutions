# TECH6A-1 — Architecture de découverte du sel gemme

Statut : `AUDIT_ONLY` · référence La Gabelle `1.0.2` · comparateur vanilla `1.13.9` · aucune implémentation.

## Conclusion

`RESOURCE_DISCOVERY_NATIVE_COMPATIBLE = PARTIAL`

`RECOMMENDED_DISCOVERY_ARCHITECTURE = NATIVE_DISCOVERY_ONLY`

Le moteur 1.13.9 sait représenter, pour un même type de bâtiment-ressource, une part visible et une part cachée :

```txt
resource = {
    type = "building_salt_mine"
    discovered_amount = KNOWN_1776
    undiscovered_amount = HIDDEN_DISCOVERABLE
}
```

Ce format est attesté directement, par exemple pour le caoutchouc dans `map_data/state_regions/07_south_america.txt:253-257`. Les exemples pétrole utilisent `type + undiscovered_amount`, notamment `00_west_europe.txt:282-285`. Il n’est donc pas nécessaire de créer une monnaie, une variable ou un potentiel parallèle.

La compatibilité n’est toutefois pas immédiate : La Gabelle rattache `building_salt_mine` à `bg_mining`, tandis que `common/building_groups/00_building_groups.txt:227-243` ne marque pas ce groupe `discoverable_resource = yes`. Les seuls groupes vanilla qui le font sont `bg_gold_fields`, `bg_rubber` et `bg_oil_extraction` (`:245-265`, `:289-310`, `:353-371`). La Gabelle n’utilise aucun bloc `resource`, `discovered_amount` ou `undiscovered_amount`; elle rend tout son potentiel visible avec `change_resource_potential` dans `common/history/states/lagab_states.txt`.

La solution native exige donc, lors d’une phase ultérieure, un groupe de bâtiment sel gemme adapté à la découverte — idéalement un nouveau groupe enfant de `bg_mining`, avec `discoverable_resource = yes`, `depletable_resource = no` et `default_building = building_salt_mine` — puis des blocs `resource` dans les fichiers de State Region. Cette adaptation reste native : elle ne constitue pas un système de ressources parallèle.

## Invariants à préserver

- Les 97 relations `building_salt_pan` restent visibles en 1776 et ne reçoivent pas de part cachée.
- Seules les 64 relations `building_salt_mine` sont candidates à une division connue/cachée.
- Aucun nouveau State Region salifère ne doit être ajouté pendant la division.
- Pour chaque relation mine : `KNOWN_1776 + HIDDEN_DISCOVERABLE <= TOTAL_LA_GABELLE`.
- Pour une conservation géographique et quantitative stricte : utiliser l’égalité avec le potentiel La Gabelle du CSV de carte.
- Les niveaux initiaux doivent rester inférieurs ou égaux au potentiel visible de départ.
- Aucun chiffre `KNOWN/HIDDEN` n’est fixé par cet audit.

## Ce que fait réellement vanilla 1.13.9

| Élément | Preuve directe | Conséquence |
|---|---|---|
| Ressource de région typée par bâtiment | `resource { type = "building_oil_rig" ... }` dans les fichiers `map_data/state_regions` | `building_salt_mine` peut être le type natif. |
| Part connue | `discovered_amount = 1` dans `07_south_america.txt:256` | Une part exploitable peut exister dès 1776. |
| Part cachée | `undiscovered_amount` est largement utilisé dans les 16 fichiers de régions | Le reliquat peut être découvert progressivement. |
| Éligibilité du groupe | commentaire de schéma `discoverable_resource = yes/no` à `00_building_groups.txt:9` | `bg_mining` actuel est insuffisant. |
| Chance moteur | `BASE_RESOURCE_DISCOVER_CHANCE = 0.02` par jour dans `common/defines/00_defines.txt:521` | Aucun pulse mensuel custom n’est nécessaire. |
| Taille d’une découverte | fractions min/max `.2/.5` à `00_defines.txt:523-524` | Le moteur consomme progressivement le reliquat caché. |
| Effet forcé | `force_resource_discovery` localisé à `common/effect_localization/00_state_region_effects_loc.txt:107-109` | Disponible seulement si une accélération scénarisée devient nécessaire. |
| On-action | `on_resource_discovered` à `common/on_actions/00_code_on_actions.txt:4137-4147` | Notification et événements arrivent après une découverte gérée par le code. |
| Potentiel scripté | `add/remove/change_resource_potential` sont exposés à `00_state_region_effects_loc.txt:115-128` | Ces effets modifient le potentiel visible; ils ne remplacent pas le compteur caché initial. |

Les technologies vanilla `shaft_mining`, `atmospheric_engine` et `aniline` montrent aussi des modificateurs ou portes de production, mais la découverte native n’expose pas dans les scripts inspectés un trigger par type de ressource. `shaft_mining` doit donc rester la porte de construction/exploitation du bâtiment, pas être présenté sans preuve comme une condition moteur de chaque jet de découverte.

## Comparaison des options

| Option | Faisabilité 1.13.9 | Changements conceptuels futurs | Save/load et idempotence | Coût/performance | Verdict |
|---|---|---|---|---|---|
| `OPTION_A_NATIVE_DISCOVERY_ONLY` | Oui après adaptation du groupe | Groupe sel gemme discoverable; blocs `resource` avec parts connue/cachée; fichiers de régions shadowés | Compteurs connus/cachés possédés par le moteur; pas d’incrément script répété | Pas de scan scripté | **Recommandée** |
| `OPTION_B_NATIVE_PLUS_CUSTOM_TRIGGER` | Oui | Même ressource native, plus événements/conditions et éventuellement `force_resource_discovery` | Risque de répétition à borner; le forçage doit viser uniquement un reliquat existant | Un pulse ciblé peut rester acceptable; un scan pays × États ne l’est pas | Réserve si une chronologie conditionnelle stricte est exigée |
| `OPTION_C_FULL_CUSTOM` | Techniquement possible mais non justifiée | Variables, événements, migration et reconstruction manuelle du potentiel | Risques maximaux de double ajout, divergence et sauvegardes anciennes | Scans et bookkeeping coûteux | Rejetée faute de nécessité |

## Option A — dessin recommandé

1. Conserver les IDs canoniques relevés : `building_salt_mine` et `building_salt_pan`.
2. Conserver `shaft_mining` comme technologie du bâtiment mine. La Gabelle utilise déjà exactement cette porte.
3. Rendre seulement la famille mine apte à la découverte native au moyen d’un groupe dédié. Ne pas marquer tout `bg_mining` discoverable : cela changerait aussi la sémantique de toutes les mines vanilla.
4. Pour chaque mine du CSV, convertir le potentiel de départ en un bloc `resource` qui porte les deux compteurs. Ne pas créer un second building type « caché ».
5. Garder les salines visibles. Leur `change_resource_potential` peut rester une piste de migration, mais une implémentation propre doit vérifier l’ordre et l’idempotence du setup.
6. Ne pas fournir `depleted_type` au sel gemme si le groupe est `depletable_resource = no`. Le champ vanilla est réservé ici au passage `building_gold_field -> building_gold_mine`.

La doctrine de shadowing 1776 implique de copier les fichiers vanilla de State Region au même chemin relatif avant d’ajouter les blocs. Les 159 régions sont réparties dans les fichiers vanilla `00_west_europe.txt` à `15_russia.txt`. Le dépôt 1776 shadowe déjà `08_middle_east.txt` et `13_australasia.txt`; 15 relations La Gabelle se trouvent dans ces deux fichiers et devront être fusionnées avec leur contenu actuel, pas écrasées.

## Option B — cas d’usage limité

Option B n’est utile que si le design futur exige une règle que le jet natif ne sait pas exprimer, par exemple une découverte garantie après une décision de prospection. Le potentiel resterait un bloc `resource` natif et le script appellerait `force_resource_discovery = building_salt_mine` sur un State Region précisément sélectionné.

Garde-fous minimaux :

- aucune utilisation de `change_resource_potential` pour simuler la découverte;
- événement one-shot ou cooldown persistant;
- vérification qu’un reliquat caché existe avant tout forçage;
- aucune boucle mensuelle sur tous les pays et tous les États;
- `on_resource_discovered` réservé aux conséquences/notifications, pas à l’ajout du même potentiel;
- test fresh start, save, reload, puis plusieurs découvertes jusqu’à épuisement du reliquat.

Le code inspecté ne prouve pas qu’un `force_resource_discovery` contourne ou respecte la porte technologique du bâtiment. Cette question doit être testée en runtime avant toute Option B conditionnée par `shaft_mining`.

## Save/load, idempotence et performance

### Système natif

- Le compteur `undiscovered_amount` diminue sous contrôle moteur; un on-action de notification ne réajoute pas la ressource.
- La somme géologique vient des compteurs initialisés dans la State Region, ce qui évite de dépasser le total par répétition d’effets.
- Aucun pulse custom n’est requis, donc aucun coût de scan mensuel/trimestriel n’est ajouté.
- Le chargement d’une sauvegarde reprend l’état courant des ressources au lieu de réexécuter un setup mensuel.
- Les changements de `map_data/state_regions` sont naturellement une architecture de nouvelle partie. Il ne faut pas supposer qu’ils injecteront rétroactivement un reliquat caché dans une sauvegarde créée avant le patch.

### Risques d’un script custom

- `change_resource_potential` répété peut augmenter plusieurs fois le plafond visible.
- Deux événements ou deux on-actions peuvent appeler le même effet après reload si leur verrou n’est pas sauvegardé.
- Une variable parallèle peut diverger du compteur natif après découverte, conquête ou scission d’État.
- Un scan global mensuel multiplie pays × États × tests et n’apporte rien si le moteur effectue déjà les jets.
- Une migration d’ancienne sauvegarde est difficile : les effets exposés prouvent la modification du potentiel visible, pas l’écriture directe d’`undiscovered_amount`.

## Décision auditée

```txt
OPTION_A_NATIVE_DISCOVERY_ONLY = RECOMMENDED
OPTION_B_NATIVE_PLUS_CUSTOM_TRIGGER = FALLBACK_ONLY
OPTION_C_FULL_CUSTOM = NOT_JUSTIFIED

LA_GABELLE_CURRENT_DISCOVERY = NONE
LA_GABELLE_CURRENT_GROUP_DISCOVERABLE = NO
NATIVE_SCHEMA_SUPPORTS_KNOWN_PLUS_HIDDEN = YES
BUILDING_GROUP_ADAPTATION_REQUIRED = YES
RESOURCE_DISCOVERY_NATIVE_COMPATIBLE = PARTIAL
RECOMMENDED_DISCOVERY_ARCHITECTURE = NATIVE_DISCOVERY_ONLY
```
