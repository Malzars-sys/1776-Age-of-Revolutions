# Soutien des propriétaires terriens aux institutions coutumières

15 octobre 2026 — contrôles statiques réussis, vérification en jeu à effectuer.

## Correctif

Les préférences des propriétaires terriens ne mentionnaient ni `law_chiefdom`
ni `law_elder_council`. Une idéologie de groupe contextuelle, **Notables
coutumiers**, est maintenant ajoutée à leurs idéologies existantes pendant
`on_game_started`, lorsque l'initialisation du scénario est achevée.

Seuls les pays possédant effectivement la chefferie **ou** le conseil des
anciens à ce moment sont concernés. Il ne s'agit pas d'une préférence globale
imposée aux aristocraties monarchiques ou républicaines.

- Chefferie : `strongly_approve` ; monarchie/théocratie : `approve`.
- Conseil des anciens : `strongly_approve` ; autocratie/oligarchie : `approve` ;
  vote foncier : `neutral`.
- Les autres alternatives ont des préférences inférieures à ces deux favoris.
- Priorité 100 entre idéologies de groupe : les anciennes préférences ordinaires
  ne neutralisent pas ce soutien. Les opinions des dirigeants ne sont pas modifiées.
- Aucun changement de loi, de chef, de poids politique ou de trait. Aucune
  idéologie existante supprimée, aucun verrou de réforme, aucune réapplication
  mensuelle. Les groupes des pays non concernés restent inchangés.

La chefferie est techniquement une loi de **principes de gouvernance** ; le
conseil des anciens relève de la **répartition du pouvoir**. Les positions sont
définies dans leurs groupes respectifs.

## Fichiers ajoutés

- `common/ideologies/16_1776_customary_landowners.txt`
- `common/on_actions/15_1776_customary_law_support.txt`
- `localization/french/1776_customary_landowners_l_french.yml`
- `localization/english/1776_customary_landowners_l_english.yml`
- `tools/test_customary_law_support.py`

## Vérifications

`tools/test_customary_law_support.py` : **8/8 tests réussis** : syntaxe,
références/groupes de lois, préférences strictes, portée conditionnelle,
initialisation par action enfant sans écraser les effets de départ, protection
contre l'ajout répété, localisations UTF-8 avec BOM et icône existante.

Les cas d'historiques Kaurna/Kuki sont ciblés ; Chine/Prusse ne le sont pas.
Ce sont des contrôles de données, pas une simulation du moteur.

Les empreintes de **tous les fichiers fonctionnels déjà présents** sont
identiques avant/après. Le correctif ajoute seulement quatre fichiers
fonctionnels ; il préserve donc les lois chinoises récemment corrigées, les
territoires, populations, bâtiments et unités. Aucun ancien rapport MAP ou
baseline n'est réécrit pour masquer ce nouvel ajout autorisé.

En nouvelle partie : inspecter les propriétaires terriens d'un pays coutumier
(par exemple Kaurna), leurs deux préférences et l'opposition aux remplacements ;
comparer un pays monarchique non coutumier. Aucune validation moteur revendiquée.
Une campagne existante ne reçoit pas cet ajout automatiquement à son chargement.

Aucun commit, push, merge ou changement d'index.
