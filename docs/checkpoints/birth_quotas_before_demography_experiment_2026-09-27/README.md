# Point de restauration — quota de naissance

Créé le 27 septembre 2026 avant l'essai de compensation démographique.
Les trois fichiers copiés ici sont les versions exactes de départ. Le fichier
`common/defines/00_defines.txt` contient déjà les réglages démographiques du
mod : ce point de restauration ne correspond **pas** à la version vanilla.

| Fichier de départ | Copie ici | SHA-256 de départ |
|---|---|---|
| `common/laws/10_1776_birth_quotas.txt` | `10_1776_birth_quotas_law.txt` | `BE9BCF63D06F2EA885F6CCBE3F9BEB1CAB284D045E015B6F0958E716D254EAE6` |
| `common/on_actions/10_1776_birth_quotas.txt` | `10_1776_birth_quotas_on_actions.txt` | `47A54CB6A9FE6BA1F93CFDAF131FDCA3ABECB5EC2DED3E72FF1552684DE12B9B` |
| `common/defines/00_defines.txt` | `00_defines.txt` | `45017F640479DFB6ECE59407D4E123C4EDE108ED91F22725B96C3A07B4DF7107` |

Pour annuler **uniquement cet essai**, remettre seulement la copie
`10_1776_birth_quotas_on_actions.txt` à la place de
`common/on_actions/10_1776_birth_quotas.txt`, puis retirer les fichiers créés
spécifiquement pour l'essai :
`common/static_modifiers/10_1776_birth_quota_demography.txt`,
`common/script_values/10_1776_birth_quota_demography.txt` et
`common/scripted_effects/10_1776_birth_quota_demography.txt`.
Supprimer également la clé `birth_quota_demographic_countermodifier` ajoutée
aux deux fichiers `localization/french/1776_birth_quotas_l_french.yml` et
`localization/english/1776_birth_quotas_l_english.yml`.
Ne pas restaurer tout le dépôt : d'autres travaux non liés sont présents.
Les copies de la loi et des constantes sont conservées comme références, mais
les restaurer effacerait des changements faits **après** ce point de contrôle,
notamment la nouvelle icône et la description de la loi.

## Portée de l'essai

Le code ne modifie pas directement `literacy_penalty` ni les constantes
globales de natalité. Il ajoute à chaque État du pays concerné un
contre-modificateur calculé à partir de son niveau de vie moyen et du taux
d'alphabétisation du pays. Le jeu calcule normalement la natalité et la
pénalité d'alphabétisation par population : la compensation est donc une
**approximation**, particulièrement dans les États où coexistent des groupes
riches et pauvres. À niveau de vie moyen 25, le correctif de niveau de vie
seul approche +418 % ; c'est l'ordre de grandeur nécessaire pour remonter de
0,00110 à 0,00510 naissance mensuelle par personne avec le bonus de loi de
+15 %. Vérifier ce résultat en jeu avant toute publication.

## Vérification en jeu

1. Charger une partie avec la loi, noter natalité, mortalité et niveau de vie
   dans deux États de niveaux de vie différents, puis laisser passer un mois.
2. Vérifier que le modificateur « Compensation nataliste » apparaît dans ces
   États, sans apparaître chez un pays qui n'a pas cette loi.
3. Remplacer la loi et vérifier que le modificateur disparaît immédiatement.
4. Consulter `Documents/Paradox Interactive/Victoria 3/logs/error.log` après
   le lancement pour toute erreur liée à `birth_quota_*` ou
   `refresh_birth_quota_demography`.
