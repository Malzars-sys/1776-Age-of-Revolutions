# Russie : bureaucratie et accès aux lois nationales

> Révision R2 : le verrou de nationalisme a été retiré à la demande du joueur. Voir [l'état courant et ses preuves](R2/REPORT.md). Le présent rapport conserve la description et les contrôles de R1.

7 novembre 2026 — `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

La Russie demande désormais les **bureaucrates militaires** au départ, avec l'amendement **Héritage noble**, qui augmente de **15 % la force politique des propriétaires terriens**. La Troisième section et la nationalité officielle sont rétablies comme lois propres à la Russie, à débloquer par la recherche. Elles ne sont pas activées au départ de 1776.

## Choix historique : militaires avec un héritage nobiliaire

La définition native des bureaucrates héréditaires décrit des postes transmis traditionnellement aux enfants. Celle des bureaucrates militaires décrit une haute administration largement recrutée dans l'armée. Cette seconde abstraction correspond mieux aux administrateurs de Catherine II, sans signifier que chaque fonctionnaire est militaire.

L'étude de John P. Le Donne, *Catherine's governors and governors-general, 1763–1796*, Cahiers du monde russe, 20/1, 1979, p. 15–42, décrit le recrutement majoritairement militaire des gouverneurs et les carrières mêlant fonctions militaires, civiles et diplomatiques. Elle souligne également les liens de famille et le patronage. Passages consultés : p. 18–19 sur les carrières des gouverneurs, puis discussion des gouverneurs généraux et des familles. [Article et DOI](https://www.persee.fr/doc/cmr_0008-0160_1979_num_20_1_1345). La consultation de la page principale et des passages indexés ne constitue pas un dépouillement de toutes ses biographies.

Le Donne, *The territorial reform of the Russian Empire, 1775–1796. I. Central Russia, 1775–1784*, 23/2, 1982, p. 147–185, notamment p. 148, décrit une administration provinciale encore dominée par des officiers nommés, démobilisés ou retraités. [Article](https://www.persee.fr/doc/cmr_0008-0160_1982_num_23_2_1942). La réforme de 1775 entre progressivement en vigueur : elle ne doit pas être considérée comme achevée au 1er janvier 1776.

La synthèse institutionnelle de la Bibliothèque présidentielle sur la [réforme provinciale de 1775](https://www.prlib.ru/history/619731), passages sur les gouverneurs nommés, les fonctions élues par la noblesse et les gouverneurs généraux, confirme cette articulation entre nomination impériale et influence nobiliaire. Elle a été consultée le 7 novembre 2026. Son statut est celui d'une synthèse institutionnelle, pas d'une lecture intégrale de l'original de 1775.

**Interprétation retenue pour le jeu :** conserver le recrutement militaire de la haute administration tout en matérialisant le poids durable des familles propriétaires par un amendement. Le bonus de 15 % est un choix de gameplay demandé pour représenter la transition, pas une mesure historique du pouvoir de la noblesse.

## Résultat installé

| Objet | Comportement |
| --- | --- |
| Bureaucratie russe initiale | `law_military_bureaucrats` remplace uniquement l'activation de `law_hereditary_bureaucrats` |
| Héritage noble | Amendement russe, compatible avec les bureaucrates héréditaires et militaires ; attaché à la bureaucratie militaire de départ ; sponsor : propriétaires terriens |
| Effet de l'amendement | `interest_group_ig_landowners_pol_str_mult = 0.15` |
| Abrogation | Seuil normal `legitimacy_to_repeal_amendment`, actuellement 50 dans les valeurs natives ; aucune technologie ou date supplémentaire imposée |
| Comportement IA de l'amendement | Les propriétaires terriens peuvent le soutenir ; l'IA peut souhaiter le révoquer lorsqu'ils ne sont plus au gouvernement, sous réserve du système normal d'abrogation |
| Troisième section | Visible seulement pour `RUS` sous monarchie ; recherche `professional_civil_policing` requise ; effets et parent `law_secret_police` conservés du vanilla |
| Nationalité officielle | Visible seulement pour `RUS` ; conditions natives de régime conservées ; recherche `nationalism` requise ; effets et parent `law_subjecthood` conservés |

Les deux technologies futures ne figurent pas dans les connaissances russes initiales résolues par le validateur. Elles restent normalement recherchables. Aucune technologie n'a été accordée et aucun graphe de recherche n'a été réécrit.

Les bureaucrates militaires demeurent une loi native disponible selon ses règles générales. Le changement de profil initial est limité à la Russie ; aucun profil de sujet ou de voisin n'a été modifié.

### Transition et effets politiques

| Effet natif ou ajouté | Bureaucrates héréditaires | Bureaucrates militaires + Héritage noble |
| --- | --- | --- |
| Coût bureaucratique de base lié à la population | −25 % | −25 % |
| Force politique des aristocrates | +25 % | Pas de bonus de cette loi aux aristocrates |
| Force politique des officiers | Pas de bonus de cette loi | +25 % |
| Force politique des bureaucrates | Pas de bonus de cette loi | +25 % |
| Force politique du GI des propriétaires terriens | Pas de bonus spécifique de cet amendement | +15 % par Héritage noble |

Les bonus de force politique d'une profession et d'un groupe d'intérêt ne sont pas interchangeables. Le +15 % ne prétend pas remplacer exactement l'ancien +25 % des aristocrates. Les attractions politiques natives liées à la loi militaire restent héritées. Les parts réelles des groupes et le budget demandent une observation en jeu.

### Fenêtre de la Troisième section

Le vanilla masque cette loi lorsque `central_archives` est recherché, sauf si elle est déjà active. Cet identifiant est un alias non recherchable du mod ; l'Okhrana n'est pas encore réintégrée. Le test de disparition a été retiré pour ce lot : la Troisième section demeure sélectionnable après son déblocage, au lieu de dépendre d'une succession non implémentée.

Son déblocage passe de l'alias consommé `law_enforcement` à `professional_civil_policing`. Tous ses autres champs sont comparés structurellement à la définition vanilla et conservés. Une future réintégration de l'Okhrana devra définir sa progression et son éventuelle obsolescence, sans remettre les anciens alias en recherche.

Pour la nationalité officielle, le nationalisme fournit un préalable à cette doctrine future sans imposer un calendrier rigide à l'histoire alternative. L'origine dans les années 1830 reste documentée dans le précédent audit ; elle n'est pas rétroprojetée au départ.

## Soutiens des groupes d'intérêt

Le soutien natif des forces armées suffit comme base pour les bureaucrates militaires : l'idéologie loyaliste approuve cette loi et reste intacte. Les propriétaires terriens conservent leur préférence native pour les bureaucrates héréditaires. L'amendement représente leur influence dans le nouvel appareil sans modifier cette préférence générale.

La Troisième section hérite des opinions sur la police secrète. L'idéologie militariste native l'approuve, face à la neutralité sur l'absence d'affaires intérieures. Aucun soutien global supplémentaire n'est ajouté.

Pour la nationalité officielle, l'héritage des opinions sur le statut de sujet ne crée pas de préférence nouvelle entre ces deux lois. Une seule position explicite a été ajoutée à **l'idéologie tsariste** : approbation de la nationalité officielle. Cette idéologie est donnée aux forces armées russes par leur `on_enable` natif. Toutes ses autres positions sont conservées à l'identique. Cela offre un acteur favorable identifié, sans réécrire les groupes d'intérêt mondiaux ni forcer leur entrée au gouvernement.

La modification est réalisée par une définition `REPLACE:ideology_tsarist`, selon le mécanisme déjà employé dans le dépôt, avec comparaison des anciens champs au vanilla. Les autres idéologies et les fichiers de groupes d'intérêt restent inchangés. Les opinions des dirigeants, l'appartenance au gouvernement et les chances réelles de promulgation ne sont pas simulées par cet audit.

## Périmètre d'écriture et concurrence

Six fichiers chargés par le jeu sont concernés :

- `common/history/countries/rus - russia.txt` : remplacement d'une activation de loi et ajout d'un bloc d'amendement sur la bureaucratie ; comparaison exacte de tous les autres octets avec la préimage immédiate.
- `common/laws/1776_v115_russian_laws.txt` : deux définitions restaurées, avec les adaptations de prérequis ci-dessus.
- `common/ideologies/17_1776_russian_law_stances.txt` : préférence tsariste ciblée.
- `common/amendments/17_1776_russian_noble_legacy.txt` : amendement.
- `localization/french/1776_russian_laws_l_french.yml` et son équivalent anglais : nom et description de l'amendement, UTF-8 avec BOM.

La préimage russe inclut déjà les travaux concurrents de colonisation. Colonisation interne, Cosaques, institution coloniale, États, populations, bâtiments et defines de ce chantier sont préservés. Parmi les **880 autres fichiers protégés** par empreinte lors de cette passe, aucun changement n'a été relevé pendant le contrôle final. Aucune écriture Git ou vanilla.

Le présent lot remplace les conclusions provisoires de l'audit antérieur seulement pour le choix bureaucratique et les deux lois rétablies. Le rapport antérieur reste conservé. Les autres lois manquantes du DLC n'ont pas été réintégrées par ce sous-lot.

## Vérification

Commande : `python -B tools/compatibility/v115_russian_laws_implementation_audit.py --output docs/reports/compatibility/V1_15_RUSSIAN_LAWS_IMPLEMENTATION_2026_11_07/VALIDATION.json`.

- Contrats de disponibilité, restrictions russes, effets natifs, changement initial borné, amendement et localisations : **PASS_STATIC_ONLY**.
- Huit contrôles négatifs en mémoire sont rejetés : retour à l'alias non recherchable, mauvaise restriction de pays, altération d'un bonus natif, suppression de la préférence tsariste, suppression du poids nobiliaire, mauvaise loi initiale, amendement initial manquant et mauvais en-tête de langue.
- Aucun nouvel écart de technologie initiale sur six pays témoins ; les technologies connues sont identiques avant/après.
- Les six profils conservent leur statut global antérieur `FAIL_STATIC` : RUS 4 constats, PLC 8, UBD 9, ALK 3, KZH 4, CRI 6. Ces dettes ne sont pas supprimées pour valider ce lot. Pour la Russie, elles concernent notamment le recrutement initial des cuirassiers, un signalement historique des signaux navals, l'absence d'attestation historique complète du profil et un avertissement sur le modèle régional du sel à Perm.
- Les localisations nouvelles n'ajoutent pas de doublon de leurs clés ; aucune activation de l'amendement n'a été ajoutée à un autre pays.
- `git diff --check` sur le profil russe ne relève pas d'erreur ; les nouveaux scripts et localisations n'ont pas d'espaces de fin de ligne.

Preuves : `BASELINE.json`, `rus_before.txt`, `SCOPE_EXTENSION.json`, `INSTALLATION.json`, `native_inputs/`, `CHANGES.patch`, `STARTING_TECH_BEFORE.json`, `VALIDATION.json`. Le validateur dédié ne modifie pas les données du jeu ; ses contrôles négatifs n'écrivent rien dans le workspace.

## Contrôle en jeu à effectuer

1. Redémarrer le jeu, lancer une nouvelle partie russe en 1776 et vérifier la loi Bureaucrates militaires, l'amendement Héritage noble et son bonus +15 % aux propriétaires terriens.
2. Vérifier que les deux lois futures ne sont pas actives, mais apparaissent dans les lois russes avec leur prérequis de recherche. Vérifier l'absence de nouveaux messages d'erreur concernant leurs identifiants, leurs effets ou l'amendement.
3. Sur une sauvegarde de test distincte, rechercher ou accorder temporairement les deux technologies pour vérifier l'accès : forces armées au gouvernement, opinions affichées et lancement de la promulgation. Le lot lui-même ne distribue aucune technologie initiale.
4. Vérifier l'abrogation d'Héritage noble avec le seuil normal de légitimité ; si la bureaucratie est ensuite réformée vers une troisième loi, contrôler le traitement normal de l'amendement devenu incompatible.
5. Vérifier les témoins PLC et UBD pour l'absence des deux lois propres à la Russie ; contrôler que la colonisation interne et les Cosaques russes restent présents.
6. Faire avancer le jeu puis sauvegarder/recharger. Une sauvegarde ancienne ne reçoit pas automatiquement la nouvelle loi initiale ni l'amendement de départ.

Aucun de ces contrôles moteur n'a été effectué pendant cette passe. Aucune validation humaine n'est déclarée.
