# Mission 23 — résolution des sept fournisseurs en doublon, 9 novembre 2026

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Les sept ambiguïtés restantes de l'audit économique précédent sont corrigées localement. **26/26 contrôles passent sur le candidat puis sur l'installation ; quatre contrôles négatifs sont détectés.** Le chargement effectif, les sélections implicites du moteur et les marchés restent à valider en jeu.

## Changement

Deux nouveaux fichiers de même chemin que le vanilla reprennent ses définitions courantes en retirant uniquement les sept objets qui entraient en concurrence avec les objets spécifiques du mod :

| Nouveau fichier | Objets natifs retirés du fournisseur masqué | Fournisseur conservé |
| --- | --- | --- |
| `common/production_method_groups/09_misc_resource.txt` | Groupe de base des camps de bûcherons et groupe de transport des plantations de caoutchouc | Les deux fichiers `99_tech_tree_*_pmgs.txt` existants |
| `common/production_methods/12_subsistence.txt` | Cinq méthodes d'ateliers domestiques de subsistance | `99_tech_start_1776_subsistence_tools.txt` existant |

Il ne s'agit pas d'un renommage : les identifiants et leurs consommateurs restent les mêmes. Les sept objets spécifiques conservent exactement leurs octets, recettes, prérequis, icônes et autres champs. L'ordre de chargement de deux définitions ordinaires de même identifiant ne détermine plus le choix attendu.

Les objets natifs non concernés, y compris les règles de servage/propriété et les autres groupes de ressources, sont conservés dans leur ordre et avec des contenus identiques. `NATIVE_PAYLOAD_PRESERVATION.json` compare indépendamment les objets retenus, champ par champ. Ces deux masquages devront être recomparés lors d'une future mise à jour vanilla.

## Contenu du mod préservé

- Foresterie : les quatre méthodes restent présentes, dont la foresterie organisée avec son prérequis `organized_forestry` ; les rendements, intrants et emplois existants ne changent pas.
- Caoutchouc : conserver les charrettes et le transport ferroviaire spécifique à la plantation. Ce dernier garde son prérequis `rubber_mastication`, son coefficient de transport et sa réduction d'emploi. Aucune technologie n'est attribuée pour rendre la méthode disponible.
- Ateliers domestiques : conserver les coefficients d'outils **0,10** pour ferme, verger, pâturage et village de pêche, et **0,20** pour rizière. Ce sont les valeurs écrites dans `workforce_scaled`, pas une production nationale mesurée ni une garantie de rentabilité. Les autres biens sortants et la restriction liée à l'agriculture collectivisée sont identiques.

`CONSUMER_REVIEW.json` recense les **sept types de bâtiments** concernés, leurs groupes cumulés, les méthodes et leurs champs. Son extraction est confirmée après restauration complète du candidat ayant servi aux contrôles négatifs. Les sélections explicites de départ restent compatibles avec les groupes conservés ; le choix implicite d'une méthode par le moteur n'est pas attesté statiquement.

## Résultats

| Contrôle | Avant | Après installation |
| --- | ---:| ---:|
| Références économiques ambiguës | 7 | **0** |
| Cibles manquantes | 0 | **0** |
| Erreurs du parseur statique | 0 | **0** |
| PM initiaux explicitement hors groupe | 0 | **0** |
| Prérequis de PM incompatibles avec leur bâtiment | 0 | **0** |
| Références recensées | 26 230 | **26 205** |

La diminution de 25 références correspond à la suppression des objets natifs en double et de leurs arêtes de liste/bien/loi. Ce n'est pas une baisse de consommation ou de production. Les inventaires uniques restent inchangés : **72 biens, 134 bâtiments, 74 groupes de bâtiments, 273 groupes de production, 623 méthodes, 291 technologies et 190 lois**.

Le témoin natif courant **1.15.0** passe séparément ses **18 181 références**, sans cible manquante ni ambiguïté. Les quatre témoins négatifs réintroduisent successivement le doublon forestier, le doublon du caoutchouc, les cinq doublons de subsistance, puis une dérive du coefficient d'outils. Chaque cas produit le refus attendu ; les entrées erronées sont archivées et la copie de contrôle est restaurée. Aucun test n'injecte ces erreurs dans le mod actif.

La protection finale compare les **278 fournisseurs** de l'audit installé et le témoin natif aux fichiers courants. Les **2 489 fichiers de jeu/localisation capturés avant le lot sont inchangés**. Seuls les deux nouveaux fichiers décrits ci-dessus sont ajoutés aux scripts actifs ; aucun fichier existant de gameplay n'est réécrit. Index Git inchangé. Aucun vanilla, gisement de cuivre, prix, technologie, loi, POP, frontière, journal ou donnée de la mission 40 n'est modifié.

## Statut et limites

Le volet statique de la mission 23 est prêt pour **In review**. La mission reste ouverte pour l'acceptation des bâtiments, flux de marché, ports et échanges représentatifs ; les résultats statiques ne prouvent ni rentabilité ni comportement moteur. Les anciens constats et reçus de l'audit initial sont conservés. Les statuts et acceptations des missions 31/33, 39 et 40 ne sont pas modifiés.

Les fichiers et rapports de ce lot ne sont pas engagés ni publiés. Aucune opération Git d'écriture, aucun lancement moteur et aucune nouvelle acceptation humaine n'ont été effectués.

## Preuves

`BASELINE.json`, `REFERENCES_BEFORE.json`, `PLAN.json`, `native/`, `candidate_mod/`, `CHANGES.patch`, `CANDIDATE_VALIDATION.json`, `NEGATIVE_CONTROLS.json`, `INSTALLATION_RECEIPT.json`, `INSTALLED_VALIDATION.json`, `NATIVE_CONTROL.json`, `SOURCE_PROTECTION.json` et `NATIVE_PAYLOAD_PRESERVATION.json` conservent les données et contrôles de cette passe.

Validateur : `tools/compatibility/issue23_duplicate_provider_audit.py --evidence <ce dossier> --output <nouveau fichier JSON dans ce dossier>`. Le mode normal lit le mod ; `--candidate` utilise la copie de preuve. `--controls` écrit uniquement des témoins dans cette copie, archive leurs entrées et la restaure. Aucun de ces modes n'installe de fichier actif. Conserver les preuves existantes et utiliser un nouveau nom de sortie.
