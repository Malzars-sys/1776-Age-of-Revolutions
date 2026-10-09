# Ajustements du 9 octobre 2026

Les changements ci-dessous sont intégrés aux fichiers du mod. Les contrôles sont statiques ; aucune nouvelle partie n’a été lancée pour les valider dans le moteur. Les captures et la sauvegarde existante servent au diagnostic, pas à confirmer le résultat de cette révision.

## Industrie britannique

| Recette | Avant | Après |
| --- | --- | --- |
| Fonte au coke | 35 fer, 35 charbon → 55 acier | 25 fer, 25 charbon → 40 acier |
| Procédé Thomas | 65 fer | 55 fer ; autres valeurs inchangées |
| Outils en fer forgé | 20 fer, pas d’acier | 15 fer, 3 acier ; bois et sortie inchangés |

Toutes les fabriques d’outils britanniques définies au départ utilisent le fer forgé. Le tarif d’exportation des outils est `low_subventions`.

Le seigle perd 20 niveaux au total : Home Counties −3, Lancashire −3, Yorkshire −5, Midlands −4, East Anglia −3, Lowlands −2. Le placement final de chaque État est modifié une fois ; les niveaux de propriété sont ajustés avec lui. Aucune exploitation n’est supprimée.

### Correction du déficit de fer signalé ensuite

Les mines britanniques de fer et de charbon commencent désormais avec les **pompes à feu**, dans tous leurs placements d’historique, y compris l’overlay final. Les autres méthodes de production, les propriétaires et les mines étrangères sont conservés. La technologie nécessaire est déjà recherchée par GBR.

Huit niveaux de mines de fer sont ajoutés : Yorkshire **2 → 6**, Midlands **2 → 6**. Ces deux États disposent de gisements suffisants. Le pays de Galles n’est pas agrandi : malgré un ancien placement de mine de fer, sa définition de ressources dans le mod ne déclare pas de capacité pour le fer.

À plein effectif, les huit niveaux produisent **320 fer** de base, contre les **278 manquants** indiqués sur la capture. Ils consomment aussi 80 outils et 80 charbon de base ; ces besoins et le passage des mines de charbon aux pompes à feu peuvent modifier l’équilibre après quelques jours. Les bonus de rendement ne sont pas comptés dans les 320. Le supplément réel dépendra du recrutement, des intrants et de l’accès au marché : il n’est pas présenté comme un surplus garanti dès le premier jour.

Contrôle supplémentaire : `tools/audit_gbr_mines_followup.py`. Le changement concerne le départ d’une nouvelle partie, pas les bâtiments d’une sauvegarde existante.

## Formations américaines

- North American Command et West Indies Garrison : QG canadien, avec point de ravitaillement britannique à Terre-Neuve ; origine du recrutement régulier conservée.
- North American Command : deux unités supplémentaires d’artillerie améliorée, donc trois au total ; dix conscrits d’infanterie de ligne affectés, cinq depuis Home Counties et cinq depuis Lancashire.
- L’effet natif `fully_mobilize_army` est appliqué après la création de cette armée. **La levée effective des dix conscrits au premier jour n’est pas confirmée.** Aucun effet de script distinct de levée des conscrits n’a été retrouvé ; l’action interactive possède en outre une restriction outre-mer. Il faudra vérifier ce point en jeu. Les dix unités ne sont pas présentées comme déjà recrutées.
- Garnisons coloniales : Ontario 5, Québec 5, Nouveau-Brunswick 2, Nouvelle-Écosse 3, Compagnie de la Baie d’Hudson 2. Infanterie seulement, au meilleur niveau permis par les technologies existantes ; aucune technologie supplémentaire accordée pour les moderniser artificiellement.
- Western Approaches Fleet : départ aux Bermudes, dans le QG de la côte atlantique. Cinq galères remplacées par cinq frégates : six frégates, cinq caravelles, deux vaisseaux de ligne et neuf galères ; total de 22 navires conservé.
- Rhode Island : une administration navale ajoutée aux Treize Colonies.

## Marins : diagnostic et correction

La sauvegarde locale `autosave_exit.v3`, version 1.13.11, est datée du **31 janvier 1776**, pas du premier jour. Elle a été lue sans modification et sans envoi à un service distant.

Les paramètres natifs fixent 100 marins par emplacement d’affectation et 1 000 par niveau d’administration navale. Dans cette sauvegarde, les caravelles normalement remplies reçoivent un emplacement de 100 malgré un maximum de 150 ; les galères en reçoivent deux de 100 malgré un maximum de 240. Ce résultat concorde avec les sous-effectifs des captures : ce n’est pas seulement une limite nationale trop basse.

Une seconde cause concerne Ceylan : son administration navale de trois niveaux a un effectif équivalent à 0,95898 niveau et des recrutements d’officiers échoués, avec zéro main-d’œuvre qualifiée dans l’entrée d’échec. Les emplacements qui lui sont affectés n’apportent qu’environ 31 marins chacun. D’autres administrations britanniques sont remplies ; le total national théorique ne garantit donc pas le remplissage des navires individuellement.

À la demande de l’utilisateur, l’arrondi est **vers le haut** : caravelle 200, galère 300, cogue 100. Les petits ajouts de 5/10/20 marins des améliorations de rame sont supprimés pour ne pas réintroduire des fractions d’emplacement ; leurs vitesses et coûts continuent de progresser.

Les trois niveaux de Ceylan sont transférés à Home Counties. Un niveau supplémentaire y est ajouté pour couvrir les besoins recalculés : **31 400 marins demandés pour 32 000 places théoriques**, au lieu de 31 000 auparavant. Aucun changement de population, de culture ou de frontière. Il reste à confirmer le remplissage effectif dans une nouvelle partie.

## Navires et technologies

- Correction supplémentaire demandée après vérification : Signaux navals est maintenant un prérequis de Charpente diagonale, qui mène ensuite aux coques en fer. Le prérequis Architecture navale de Charpente diagonale est conservé. Aucun nouveau nœud, aucun cycle ajouté ; le déblocage des vaisseaux de ligne reste sur Signaux navals.
- Les douze équipements de premier niveau consomment désormais des biens, donnent de petits bonus et ajoutent chacun un point de complexité de construction. Les coûts globaux restent calculés par le concepteur natif.
- Un seul emplacement de modification de fonction par caravelle, galère et cogue ; les alternatives de fonction restent disponibles, mais pas cumulables sur un même navire.
- Descriptions françaises et anglaises historiques, avec la fonction du navire, sans argument de prix ni comparaison avec un « successeur ».
- Les sept nœuds technologiques ajoutés pour les coques/équipements sont retirés. Le fichier supprimé est conservé dans la référence locale de contrôle, donc récupérable. Les déblocages utilisent uniquement des technologies navales déjà présentes : arsenaux d’État, bassins fermés, architecture navale, classification, chronométrie marine, signaux navals, doublage en cuivre et charpente diagonale.
- Construction de frégates : chronométrie marine. Vaisseaux de ligne : signaux navals. Les technologies correspondantes sont accordées au départ uniquement à GBR, FRA, SPA, RUS, POR, NET, DEN, DENNOR, NOR et SWE ; les tags optionnels ne créent pas de pays.
- Les flottes locales de TUR, VEN, GEN, SAR, SIC, PAP, TUS, AUS, TUN et TRI sont converties en galères en conservant leurs nombres de navires et commandants. La flotte ottomane compte neuf galères. Les puissances océaniques ne sont pas concernées par cette conversion.

Sources utilisées pour les descriptions : [caravelle, Royal Museums Greenwich](https://www.rmg.co.uk/collections/objects/rmgc-object-66267), [galère de Malte de 1770, Royal Museums Greenwich](https://www.rmg.co.uk/collections/objects/rmgc-object-538121), [cogue de Brême, Deutsches Schifffahrtsmuseum](https://www.dsm.museum/en/museum/exhibits/bremen-cog).

## Vérifications

- Correspondance des changements avec la référence locale préalable, complétée par deux amendements conservés séparément pour le diagnostic et le choix d’arrondi.
- 1 532 fichiers hors périmètre protégés par empreinte, dont les visuels approuvés et les portraits.
- Contrôle des recettes, méthodes de départ, nombres d’unités, QG, emplacement aux Bermudes, capacité navale théorique, technologies valides et restriction des frégates/vaisseaux aux pays autorisés.
- Reconstruction exacte des 191 icônes du registre : réussie, sans modification des fichiers du jeu/mod.
- Aucun nouvel asset graphique ou 3D ; aucun changement des icônes validées.

L’audit actuel est `tools/plan_oct09_balance_revision.py --check`. Les anciens audits et générateurs de la vague des équipements navals décrivent l’état antérieur avec sept nœuds supplémentaires et des premiers équipements gratuits : leurs attentes historiques ne sont pas réécrites pour masquer ces changements, et leurs générateurs ne doivent pas être relancés pour restaurer cet ancien état.

Une **nouvelle partie après redémarrage** est nécessaire pour vérifier les modifications de départ, notamment les équipages, le stationnement et la conscription. Les données d’une ancienne sauvegarde ne sont pas migrées par ces modifications d’historique.
