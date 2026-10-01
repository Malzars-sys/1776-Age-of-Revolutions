# Audit des idéologies et du quota de naissance

Date : 30 septembre 2026.

## Résultat

27 idéologies effectives ont une position sur les droits des femmes. Toutes possèdent désormais exactement un bloc `lawgroup_rights_of_women` et une seule position explicite sur `law_birth_quotas`.

La composition a été contrôlée sur les 180 idéologies chargées par les fichiers du jeu installé et du mod, avec remplacement des fichiers de même nom puis application ordonnée des définitions `REPLACE:`. Il s'agit d'une vérification statique, pas d'un test dans le moteur.

## Correction du doublon

`INJECT:` ajoutait un second bloc de droits des femmes à la définition existante de `ideology_patriarchal`. La capture en jeu confirme le double affichage. Les injections des variantes `ideology_utilitarian_millian` et `ideology_utilitarian_movement` employaient la même méthode.

Ces trois injections sont remplacées par des définitions complètes `REPLACE:`. Les icônes, les autres groupes de lois et les autres propriétés restent ceux de leurs définitions originales.

12 autres variantes natives sont remplacées de la même façon pour compléter leur position sur le quota. Trois groupes de dirigeants déjà définis dans le mod sont complétés directement : traditionaliste, traditionaliste minoritaire et humanitaire royaliste.

## Choix historiques et limites

Le quota décrit par le mod est une contrainte d'État sur la natalité, associée au retrait des femmes du travail. Il ne doit pas être confondu avec une politique volontaire d'aide aux familles nombreuses. Les positions ci-dessous sont des interprétations de jeu, pas des déclarations historiques sur cette loi fictive.

- Féministes, égalitaires modernes, libéraux modernes et humanitaires : opposition forte, cohérente avec l'autonomie et les droits juridiques défendus dans [A Vindication of the Rights of Woman, Mary Wollstonecraft (1792)](https://www.gutenberg.org/cache/epub/3420/pg3420.html) et [The Subjection of Women, John Stuart Mill (1869)](https://www.gutenberg.org/cache/epub/27083/pg27083-images.html).
- Réformateurs et Ilustrados : opposition, sans leur attribuer rétroactivement l'ensemble d'un programme féministe contemporain.
- Patriarcaux et traditionalistes, y compris les variantes régionales : neutralité prudente sur le quota, tout en préservant leurs préférences existantes pour la tutelle et les rôles familiaux. Un attachement à la famille traditionnelle ne démontre pas un soutien à des objectifs de naissance imposés par l'État. [Rerum Novarum, Léon XIII (1891)](https://www.vatican.va/content/leo-xiii/fr/encyclicals/documents/hf_l-xiii_enc_15051891_rerum-novarum.html) distingue notamment les droits de la famille de ceux de l'État. Ce texte catholique n'est pas présenté comme une preuve des positions orthodoxes ou ibadites : leur neutralité est une inférence de conception conservatrice, faute de preuve d'un soutien à cette loi précise.
- Utilitaristes : soutien fort conservé par instruction explicite du créateur du mod. Cette position nataliste est une convention d'histoire alternative ; elle ne représente pas la pensée historique de Mill. Tutelle et propriété neutres, travail des femmes approuvé, suffrage désapprouvé.
- Natalistes et natalisme institutionnel : soutien fort, conforme à leur définition fictive.
- Anti-natalistes et opposition au quota : opposition forte, conforme à leur définition fictive.

Le libéralisme générique `ideology_liberal` reste sans position sur les droits des femmes, conformément à la demande antérieure. Il n'est donc pas inclus dans les 27 entrées. Les variantes modernes et Ilustrados conservent leurs positions propres.

L'ancienne idéologie `ideology_birth_quota_ig_support` est conservée uniquement pour les anciennes sauvegardes. Elle demeure neutre sur le quota et approuve la tutelle. L'opposition de groupe `ideology_birth_quota_ig_opposition` reste volontairement limitée au quota pour ne pas remplacer les préférences existantes sur les quatre autres lois.

## Tableau complet

| Identifiant | Position sur le quota | Définition effective |
|---|---|---|
| `ideology_anti_natalist_movement` | Désapprouve fortement | `13_1776_anti_natalist.txt` |
| `ideology_birth_quota_ig_opposition` | Désapprouve fortement | `10_1776_natalist.txt` |
| `ideology_birth_quota_ig_support` | Neutre | `10_1776_natalist.txt` |
| `ideology_egalitarian_modern` | Désapprouve fortement | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_feminist` | Désapprouve fortement | `01_character_ideologies.txt` |
| `ideology_feminist_ig` | Désapprouve fortement | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_feminist_movement` | Désapprouve fortement | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_humanitarian` | Désapprouve fortement | `01_character_ideologies.txt` |
| `ideology_humanitarian_royalist` | Désapprouve fortement | `01_character_ideologies.txt` |
| `ideology_ibadi_imamate` | Neutre | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_ilustrado` | Désapprouve | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_liberal_modern` | Désapprouve fortement | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_natalist_intelligentsia` | Approuve fortement | `13_1776_anti_natalist.txt` |
| `ideology_natalist_movement` | Approuve fortement | `10_1776_natalist.txt` |
| `ideology_oriental_orthodox_patriarch` | Neutre | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_orthodox_patriarch` | Neutre | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_patriarchal` | Neutre | `12_1776_patriarchal_quota.txt` |
| `ideology_patriarchal_suffrage` | Neutre | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_reformer` | Désapprouve | `01_character_ideologies.txt` |
| `ideology_russian_patriarch` | Neutre | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_traditionalist` | Neutre | `01_character_ideologies.txt` |
| `ideology_traditionalist_minoritarian` | Neutre | `01_character_ideologies.txt` |
| `ideology_traditionalist_minoritarian_movement` | Neutre | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_traditionalist_movement` | Neutre | `15_1776_womens_rights_quota_stances.txt` |
| `ideology_utilitarian_leader` | Approuve fortement | `01_character_ideologies.txt` |
| `ideology_utilitarian_millian` | Approuve fortement | `11_1776_utilitarian_quota.txt` |
| `ideology_utilitarian_movement` | Approuve fortement | `11_1776_utilitarian_quota.txt` |

## Vérifications réalisées

- 27 groupes de droits des femmes contrôlés ; aucun doublon de groupe ou de loi.
- Une position explicite sur le quota pour chacun.
- Valeurs comparées à la liste de positions attendues.
- Préservation des champs hors droits des femmes pour les 18 définitions modifiées.
- Préservation des avis antérieurs sur les quatre autres lois, sauf les trois variantes utilitaristes dont les positions suivent les instructions antérieures du créateur.
- Maintien de l'absence de positions pour le libéralisme générique.
- Aucun changement aux personnages, lois, mouvements, amendements, événements ou autres familles idéologiques.

## Contrôle en jeu après redémarrage

1. Patriarcal : une seule section de droits des femmes ; tutelle approuvée et quota neutre.
2. Utilitaristes (dirigeant, variante de groupe et mouvement) : une seule section ; quota fortement approuvé, tutelle neutre, suffrage désapprouvé, travail des femmes approuvé.
3. Féministes (dirigeant, groupe et mouvement) : quota fortement désapprouvé.
4. Humanitaire royaliste : même opposition au quota que la variante humanitaire ordinaire.
5. Traditionalistes et variantes patriarcales régionales : quota explicitement neutre.
6. Vérifier que les journaux du moteur n'annoncent pas de rejet de ces définitions lors du nouveau chargement.
