# Mission 40 — stratégie avant installation

Date : 9 novembre 2026. Statut : stratégie technique retenue ; fonctionnement moteur non validé.

## Choix

Restaurer les deux identifiants culturels historiques `north_caucasian` et `siberian` dans un fichier additionnel de compatibilité. Ce sont des définitions réelles, pas des alias vers une culture actuelle. Aucun groupe de population, foyer, pays, personnage ou consommateur d'événement n'est renommé ou redistribué.

La provenance figée est le [fichier de cultures au commit fc8143b](https://github.com/tjysdsg/Victoria-3-files/blob/fc8143b83f54f8abed97fc556b556e4085b6e691/game/common/cultures/00_cultures.txt), publié dans un miroir de données du jeu. Son commit annonce la mise à jour 1.8.7 vers 1.9.0, le 18 juin 2025. Les deux blocs et les deux noms FR/EN ont été effectivement consultés à cette révision et sont conservés dans `LEGACY_PROVENANCE.json`. Ce n'est ni un dépôt officiel de Paradox, ni une attestation du payload exact de 1.13/1.14, ni une source de proportions démographiques en 1776.

## Adaptation à 1.15

Conserver exactement couleur, religion par défaut, listes de noms, graphismes et poids d'ethnicités des deux blocs antérieurs. Vérifier les fournisseurs et localisations actuels correspondants. Les champs anciens `traits` ne sont pas réintroduits : la version canonique utilise `heritage`, `language` et `traditions`.

| Catégorie conservée | Héritage actuel | Langue de compatibilité | Tradition |
| --- | --- | --- | --- |
| nord-caucasienne | `heritage_north_caucasian` | ensemble géographique propre, sans rattachement forcé à l'avar, au vainakh ou au circassien | `tradition_caucasian` |
| sibérienne | `heritage_siberian` | ensemble géographique propre, sans rattachement forcé au groupe turcique, toungouse ou tchouktche | aucune |

Deux traits de langue et deux groupes dédiés portent les noms « Langues nord-caucasiennes » et « Langues de Sibérie ». Ces ensembles sont une approximation de compatibilité des catégories héritées, pas l'affirmation d'une langue ou famille linguistique unique. Chaque trait appartient à son propre groupe de type `language`, selon le contrat canonique `common/discrimination_traits/discrimination_traits.md`. Aucune culture native n'est modifiée pour partager ces groupes.

Cette séparation évite de faire passer toutes les populations sibériennes pour des Iakoutes ou des Evenks, ou tous les Nord-Caucasiens pour des Avars/Circassiens. Elle conserve les limites de l'agrégation historique du mod ; une désagrégation scientifique demanderait une autre mission avec sources par État et par groupe. Aucun pourcentage de 1836 n'est importé.

## Acceptation et assimilation : conséquences et limites

L'héritage nord-caucasien actuel appartient au groupe européen, comme dans les définitions natives actuelles des Circassiens, Tchétchènes et Daghestanais. C'est un changement de classement mécanique par rapport au vieux trait `middle_eastern_heritage`, explicitement assumé pour suivre le modèle régional 1.15 ; aucune équivalence exacte d'acceptation avec l'ancien moteur n'est promise. L'héritage sibérien reste dans le groupe nord-asiatique actuel. La tradition caucasienne suit les exemples natifs actuels.

Les deux langues agrégées n'accordent de bonus de langue ou de famille qu'à leur propre catégorie ; elles n'ajoutent aucun bonus linguistique arbitraire envers une culture native distincte. Les bonus d'héritage et, au Caucase, de tradition restent possibles selon les lois effectivement actives. Les cultures principales conservent le mécanisme d'acceptation des cultures principales. Les lois, seuils et taux d'assimilation ne sont pas modifiés ; les foyers culturels restent identiques. L'absence actuelle des fournisseurs interdit de promettre un résultat économique ou d'acceptation avant/après mesuré : cela reste un test moteur.

## Installation et preuves prévues

Seulement cinq fichiers de jeu additionnels : deux cultures, deux traits de langue, deux groupes linguistiques et leurs localisations FR/EN (six clés par langue). Aucun masque d'un fichier vanilla. Préparer d'abord un candidat, vérifier unicité, références, contrat des traits/groupes, noms et apparences ; comparer les enregistrements et totaux de populations avant/après. Contrôler les consommateurs, les protections des missions 21/27/39 et les modifications concurrentes par empreintes. Conserver les résultats négatifs de contrôle et fournir un protocole moteur sans attestation fictive.
