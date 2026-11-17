# Revue exhaustive du catalogue de journaux — 11 novembre 2026

Le catalogue actuel a été vérifié avant les essais moteur annoncés par le
mainteneur. Référence technique : installation canonique Victoria 3 **1.15.0**,
notamment `common/journal_entries/journal_entries.md`, réellement consultée.
Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucun test moteur ni
nouvelle acceptation humaine n'est prétendu exécuté.

## Couverture

| Ensemble vérifié | Résultat actuel |
| --- | --- |
| Catalogue effectif | 494 identifiants uniques, 203 fichiers effectifs, aucun fournisseur ambigu ni erreur de parsing |
| Conclusions | 491 entrées avec 1045 outcomes ; aucun ancien champ de conclusion ou de présentation directe |
| Lot initial de migration | Les 400 entrées prévues sont toutes retrouvées, y compris `REPLACE_OR_CREATE:je_colonize_korea` après normalisation de la directive |
| Autres entrées | 91 entrées avec outcomes déjà compatibles ou ajoutées depuis, et 3 entrées sans conclusion classées individuellement |
| Métadonnées et structure | En-têtes visibles, descriptions de conclusion, déclencheurs ordinaires, échéances, flags, invalidation cachée et contexte des effets pour tous les impliqués vérifiés pour chaque entrée |
| Localisation FR/EN | Aucune clé requise absente parmi titres, raisons statiques/dynamiques et métadonnées des outcomes ; 22 occurrences de clés définies à la fois dans le natif et les overrides `replace` existants sont conservées comme telles |
| Dépendances directes et boutons | Auditeur existant : 494 journaux, zéro constat ; 65/65 vérifications auxiliaires, 491 liaisons de boutons |
| Consommateurs effectifs après correctif | 2920 références de journal examinées, dont 525 instructions d'ajout (524 cibles littérales et une paramétrée) ; zéro cible littérale non résolue dans ce périmètre |

`ENTRY_REVIEW.json` donne une ligne de vérification détaillée pour chacune des
494 entrées. `CATALOGUE.csv` et `INVENTORY.json` restent les inventaires complets.
Ces contrôles ne déclarent pas la prose immersive de tous les journaux relue
manuellement, ni leurs conditions effectivement atteintes dans le moteur.

## Raccordement oublié trouvé et corrigé : Commune de Paris

La conversion des outcomes était complète, mais l'audit étendu aux portées
`je:` a trouvé **39 références optionnelles au journal natif absent
`je_paris_commune`**. Elles proviennent de deux boutons et de quatorze effets
automatiques natifs. Les deux boutons sont attachés au journal français du
mod ; les quatorze effets sont appelables depuis ses deux agrégateurs
d'opposition. L'absence de cible est donc pertinente pour la famille conservée,
même si la syntaxe optionnelle peut éviter une erreur de scope.

Le mod conserve trois anciennes entrées de Commune et utilise
`global_var:paris_commune_progress_var`. Les choix initiaux mettent ce compteur
à 40 ou 60 ; les journaux français et communard lisent le même compteur et
concluent aux bornes 0/100. Les événements authored modifient déjà cette
variable. Les effets natifs hérités essayaient au contraire d'ajouter des
points à `je_paris_commune_progress_bar` sur une entrée non définie.

Deux fichiers ajoutés rétablissent ce seul raccordement :

- `common/scripted_effects/00_victoria_adversarial_scripted_effects.txt` : masque
  du fichier natif actuel, avec exactement 37 blocs de progression remplacés.
  Tous les autres octets et objets natifs sont conservés. **Ce masque devra
  être recomparé aux mises à jour du jeu.**
- `common/scripted_buttons/1776_v115_paris_commune_progress.txt` : deux
  remplacements d'objets explicites, conservant les boutons natifs sauf leur
  bloc de progression. Le fichier natif partagé des boutons n'est pas masqué.

Les 39 blocs ajoutent au compteur global existant les mêmes valeurs signées
que leurs sources : +5, -5, +10 ou -10. Chaque ajout vérifie d'abord que le
compteur a été initialisé par la chaîne. Aucun journal natif n'est réactivé,
aucun choix, événement, récompense, condition de visibilité, cooldown ou
outcome de journal n'est réécrit. Les taux de tirage et tous les effets
politiques des branches automatiques restent ceux déjà hérités du natif.

Le correctif passe **13/13 contrôles statiques**, dont identité des objets
natifs après inversion structurelle du seul raccordement, et **3/3
contre-exemples** portant sur une valeur changée, une garde retirée et un
mauvais compteur. Les seize fournisseurs effectifs sont uniques et vérifiés
après installation. Les preuves et contrats se trouvent dans `PARIS_BRIDGE/`.
Le mouvement réel de la barre, l'affichage des infobulles, l'exécution des
branches et leur comportement après conclusion restent à tester.

## Écarts anciens expliqués, sans effacer les échecs

L'audit historique de migration R4, rejoué sur les fichiers actuels, garde son
échec brut **11107/11111**, avec quatre assertions et trois spans devenus
différents. Il s'agit exclusivement des correctifs ultérieurs 50 (garde du
pays Acre), 51 (variables marocaines) et 53 (tutoriel maritime).

Pour chacun des trois fichiers, la copie capturée à la migration correspond
exactement à l'empreinte « avant » de son correctif ultérieur ; le fichier
actuel correspond à son reçu d'installation et à son contrat borné. En
revenant à la vue R4 **uniquement en mémoire**, l'audit original réussit ses
**11117/11117 contrôles**, et ses **14/14 régressions volontaires** restent
détectées. Aucune donnée du mod n'est restaurée à l'ancien état, aucun
validateur historique n'est modifié, et l'échec brut reste consultable.

Le premier lecteur de consommateurs comptait aussi des sélecteurs tels que
`je:ENTRY.var:NAME` comme des identifiants complets. `CONSUMER_SCOPES.json`
conserve ce résultat de 76 candidats. La révision distingue l'identifiant de
sa propriété et isole les 39 véritables cibles absentes ; le résultat final
après correction est nul. Le lecteur applique aussi les remplacements de
sous-dossiers indiqués dans les métadonnées et les remplacements d'objets.
Les 529 ajouts du premier inventaire large deviennent donc 525 ajouts dans
la vue effective précise ; aucune entrée n'est retirée du catalogue. Deux
références paramétrées, une condition et un ajout, restent explicitement hors
de la résolution des cibles littérales.

## Exceptions conservées individuellement

La documentation 1.15 autorise zéro outcome. Les trois cas suivants ne sont
pas des champs de conclusion oubliés :

| Entrée | Raison de conservation |
| --- | --- |
| `je_colonial_administration` | Hub authored de boutons coloniaux, sans conclusion générale définie |
| `je_new_imperialism` | Hub authored de boutons, sans objectif final unique |
| `je_spain_glorious_revolution_dummy` | Dummy natif conservé tel quel ; aucune conclusion inventée |

Quatre identifiants natifs restent masqués par des familles distinctes du mod :

| Identifiant natif absent | Famille conservée |
| --- | --- |
| `je_canada` | `je_canada_can` / `je_canada_gbr` |
| `je_australia` | `je_australia_aus` / `je_australia_gbr` |
| `je_paris_commune` | Les trois entrées `je_the_paris_commune_*`, avec leur compteur rétabli par ce lot |
| `je_extraordinary_commission` | L'ancienne famille communiste et d'avant-garde, migrée en outcomes |

L'adaptation exhaustive de toutes les nouvelles fonctionnalités des familles
natives n'est pas certifiée par cette correspondance. Aucune de ces entrées
n'est ajoutée en parallèle pour faire disparaître un diagnostic. Après le
raccordement de la Commune, aucune référence littérale manquante à ces quatre
identifiants n'est retrouvée dans les consommateurs effectifs inspectés.

## Conservation, suivi et suite

`FINAL_PROTECTION_AND_ACCOUNTING.json` vérifie les sources du début de revue,
les nouvelles définitions effectives et la comptabilité 400 + 91 + 3 = 494.
Aucun fichier de journal existant, événement, localisation, carte, population,
loi ou technologie n'est modifié par ce lot. Les seuls ajouts de runtime sont
les deux fichiers de raccordement. Les travaux 17, 18, 25 et les précédents
correctifs sont préservés ; aucune opération Git d'écriture ou du vanilla.

La revue statique du catalogue est terminée, avec le défaut découvert corrigé.
La validation moteur de 39, puis l'acceptation globale 24/25 et la clôture 19,
restent ouvertes. Le protocole court actuel est dans `RUNTIME_PROTOCOL.md` ;
les essais déjà acceptés et les anciens rapports ne sont pas annulés.
