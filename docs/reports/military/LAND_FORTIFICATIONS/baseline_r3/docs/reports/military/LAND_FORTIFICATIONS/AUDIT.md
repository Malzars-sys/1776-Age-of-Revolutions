# Passe préalable — fortifications navales et remplacement terrestre

19 octobre 2026. Audit effectué avant l’écriture des définitions de jeu du lot.

**Historique R1 :** le calibrage terrestre ci-dessous a ensuite été remplacé par la révision R2 à la demande de l’utilisateur : valeurs annoncées appliquées par niveau, avec un plafond de 85 % pour la protection territoriale. Les valeurs actuelles sont dans [REPORT.md](REPORT.md).

Les fortifications navales actuelles suivent le vanilla local, sauf le rattachement des déblocages à l’arbre technologique du mod.

| Propriété | Base | Renforcée | Avancée |
|---|---:|---:|---:|
| Technologie du bâtiment | Fortification et poliorcétique | même bâtiment | même bâtiment |
| Technologie de la méthode | aucune supplémentaire | Forts casematés | Fortifications en béton |
| Défense contre débarquement | +100 | +250 | +500 |
| Soutien au combat naval | +5 % | +10 % | +20 % |
| Résistance au bombardement | +250 | +1 000 | +2 000 |
| Résistance au blocus | +25 | +100 | +200 |
| Contrôle des détroits | oui | oui | oui |
| Armes légères / artillerie / fer / acier / munitions | 5 / 0 / 5 / 0 / 0 | 5 / 3 / 0 / 5 / 0 | 5 / 5 / 0 / 10 / 5 |
| Soldats / officiers | 900 / 100 | 850 / 150 | 800 / 200 |

Les quatre effets numériques sont proportionnels à la garnison employée et au nombre de niveaux. Le contrôle des détroits est non proportionnel. Le plafond naval de cinq niveaux provient des valeurs de base du moteur, via le modificateur généré du bâtiment. Construction très peu coûteuse, financement public, infrastructure de 0,2 par niveau, sans économie d’échelle.

**À conserver pour le terrestre** : les trois étapes technologiques, les coûts de construction et d’entretien, les emplois, les icônes de méthode et le plafond de cinq niveaux. Le bâtiment reçoit l’icône fournie, détourée. La condition côtière est inversée.

**À supprimer pour le terrestre** : les cinq effets maritimes, y compris le contrôle des détroits. Aucun bonus naval, résistance au débarquement, au blocus ou au bombardement n’est transmis au nouveau bâtiment.

## Effets natifs retenus

- `unit_provinces_lost_mult` : modifie les provinces perdues en bataille défensive. Le vanilla utilise notamment −65 % dans les modificateurs défensifs de la guerre du Caucase ; cette valeur exceptionnelle n’est pas copiée par niveau.
- `battle_casualties_mult` : pertes subies par le côté concerné. La condition native de manœuvre prudente utilise −10 %.
- `unit_army_defense_mult` : défense terrestre. La condition native de retranchement donne +20 %. Le trait d’arpenteur utilise aussi +10 % de défense sur territoire national via `battle_defense_owned_province_mult`.

Ces champs natifs sont utilisés dans des **conditions de bataille**, afin de cibler le côté défendant le territoire possédé et contrôlé du pays dans l’État où se trouve le fort. Ils ne sont pas placés dans un modificateur national permanent ni présentés comme un effet de mortalité civile.

Calibrage retenu à garnison complète, pour **cinq niveaux** : base −10 % de provinces perdues, −5 % de pertes et +5 % de défense ; renforcée −20 % / −10 % / +10 % ; avancée −30 % / −15 % / +15 %. Il s’agit d’un équilibrage du mod à partir des effets natifs constatés, pas de trois bâtiments terrestres préexistants dans le vanilla.

## Références vérifiées

Sources primaires locales dans `C:\Games\Victoria 3\game` : `common/buildings/05_military.txt`, `common/building_groups/00_building_groups.txt`, `common/production_methods/05_military.txt`, `common/production_method_groups/05_military.txt`, `common/battle_conditions/battle_condition.md`, `common/battle_conditions/00_battle_conditions.txt`, `common/modifier_type_definitions/00_modifier_types.txt`, `common/static_modifiers/00_code_static_modifiers.txt`, `common/static_modifiers/106_modifiers.txt` et `common/character_traits/skill_traits.txt`.

La documentation locale des conditions de bataille expose le lieu, le propriétaire du côté et les mécanismes `possible` et `instant_switch`. La documentation générée du moteur 1.13 publiée dans [Modding Digests — effects.log](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/blob/main/1.13.0/docs/effects.log) confirme que `add_modifier` n’accepte pas un côté de bataille comme portée. Le lot ne crée donc pas un faux effet d’ajout de modificateur à cette portée.

L’implémentation préservera les conséquences natives de poursuite, retraite paniquée et retraite contrôlée, en leur ajoutant la protection du fort quand il est applicable. Les conditions ordinaires restent intactes hors combat défensif dans un État fortifié. Aucun essai moteur n’a été réalisé pendant cette passe préalable.
