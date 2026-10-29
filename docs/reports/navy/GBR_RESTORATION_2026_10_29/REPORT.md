# Grande-Bretagne : restauration de la flotte et modernisation partielle

29 octobre 2026 — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**.

## Changement demandé et installé

Le joueur rapporte que les finances britanniques sont redevenues excédentaires. Il demande de revenir sur la réduction budgétaire de flotte et de convertir environ 30 % des galères et caravelles en vaisseaux de ligne/man-o'-war et frégates classiques. L'excédent est un retour humain ; aucun montant ni nouveau solde après intervention n'est inventé.

La référence préalable a été retrouvée dans `.asset-cache/british_colonial_start_2026-10-08/baseline.json`, champ `naval_raws`. Elle contient **120 navires britanniques**, dans sept stations encore présentes. Le générateur historique `tools/audit_british_colonial_start.py`, fonction `target_ships`, applique bien une réduction à environ quatre cinquièmes par formation. Les totaux actuels avant cette intervention sont **97**. Il ne faut pas confondre cette réduction budgétaire avec l'ancien prototype NAVY-1A, qui utilisait une autre échelle.

Seuls les nombres de navires sont repris de cette référence. Les amiraux, QG, points de ravitaillement, noms, rattachements et autres corrections intervenues depuis sont conservés. Les bâtiments anciens ne sont pas restaurés en bloc.

| Station, identifiant courant | Avant | Après |
|---|---:|---:|
| Mediterranean_Station | 10 | 12 |
| North_America_and_West_Indies_Station | 10 | 12 |
| cleanup2d3b_gbr_naval_6 | 4 | 5 |
| cleanup2d3b_gbr_naval_5 | 6 | 7 |
| cleanup2d3b_gbr_naval_1 | 40 | 50 |
| cleanup2d3b_gbr_naval_2 | 22 | 28 |
| cleanup2d3b_gbr_naval_7 | 5 | 6 |
| **Total** | **97** | **120** |

## Conversion des coques

Le mod classe actuellement la caravelle dans les capitaux et la galère dans les croiseurs côtiers primitifs. Le choix retenu est donc **caravelle → vaisseau de ligne** et **galère → frégate**, conformément à ces rôles courants. Il ne reprend pas le sens des substitutions économiques d'un ancien générateur, antérieur à cette reclassification.

Les 23 navires rétablis sont d'abord répartis entre les coques économiques de chaque station, proportionnellement aux effectifs actuels. Les 16 navires classiques déjà présents sont conservés. On convertit ensuite 30 % de chaque famille économique à l'échelle du pays, avec répartition par plus forts restes entre stations. Arrondir séparément chaque petite station aurait artificiellement amplifié la conversion.

- **12 caravelles sur 41** converties : 29,27 %.
- **19 galères sur 63** converties : 30,16 %.
- Total : **31 coques sur 104**, soit **29,81 %**.

| Classe | Avant intervention | Après restauration et conversion |
|---|---:|---:|
| Vaisseaux de ligne | 7 | **19** |
| Frégates classiques | 9 | **28** |
| Caravelles | 30 | **29** |
| Galères | 51 | **44** |
| **Total** | **97** | **120** |

Aucune définition de coque, équipement, technologie, loi ou flotte étrangère n'est modifiée. La modernisation partielle ne signifie pas un retour à 120 navires tous classiques.

## Équipages et budget

Avec les définitions effectives et leurs équipements par défaut, le besoin nominal passe de **31 400 à 48 200 marins**. Les classes concernées utilisent des multiples complets des emplacements natifs de 100 marins ; les équipements par défaut n'ajoutent ici aucun équipage fractionnaire.

La dernière sauvegarde de diagnostic conservée chargeait 15 niveaux d'administration navale à Home Counties, 4 au Lancashire, 9 au West Country et 4 en Haute-Andalousie. Les 28 niveaux métropolitains étaient remplis ; ceux de Gibraltar ne représentaient que 1,025 niveau équivalent en effectif. Ce relevé ancien n'est pas une nouvelle validation moteur de la présente installation.

**Home Counties passe de 15 à 36 niveaux**, soit 21 niveaux ajoutés. La capacité métropolitaine potentielle atteint ainsi **49 000 marins**, suffisante pour 48 200 sans dépendre du recrutement incomplet observé à Gibraltar. La capacité totale potentielle britannique atteint 53 000, Gibraltar compris. Le PM de recrutement est conservé : les niveaux supplémentaires représentent **18 900 emplois de soldats et 2 100 d'officiers** à plein effectif. Aucun habitant n'est créé ou converti.

Le minimum métropolitain est arrondi au millier supérieur ; aucune réserve forfaitaire supplémentaire n'est ajoutée. Cela ne garantit pas que les nouveaux emplois seront remplis immédiatement : qualifications, recrutement et affectation des équipages restent à contrôler.

Les sommes de ravitaillement des seules définitions de coque passent de **32,2 à 61,6 grain** et de **3,22 à 6,16 bois dur** dans les unités de `materiel_goods`. Ce sont des sommes de paramètres de base, pas une dépense hebdomadaire complète : elles excluent équipements, prix effectifs, salaires, niveau de ravitaillement et modificateurs. Les coûts de construction de nouveaux navires ne sont pas présentés comme une facture de construction rétrospective au départ.

**Le maintien de l'excédent budgétaire et la première place des grandes puissances ne sont pas démontrés par ces contrôles statiques.** Le rétablissement et la modernisation renforcent la flotte ; aucun prestige artificiel, aucun bonus de rang et aucune réduction de coût cachée ne sont ajoutés pour forcer le classement.

Le fichier `WORLD_FLEET_COMPARISON.json` donne un inventaire indicatif : GBR 120 navires/48 200 marins nominaux, France 41/12 100, Espagne 40/11 800. Les équipages nominaux ne sont pas la formule native de projection navale ni de prestige. Ce tableau ne certifie donc ni le rang général en jeu ni une hiérarchie historique universelle de 1776.

## Fichiers et vérification

Deux fichiers runtime changent :

1. `common/history/military_formations/00_military_formations_europe.txt` : nombres et classes des seuls navires britanniques.
2. `common/history/buildings/00_west_europe.txt` : uniquement `levels=15 → 36` de l'administration navale britannique de Home Counties.

Plan détaillé, références et empreintes : `PLAN.json`. Préimages, préparation et différence : `preimages/`, `staged/`, `CHANGES.diff`. Reçu : `APPLIED.json`.

Outil gardé par empreintes : `tools/restore_british_fleet_1776.py`, actions `prepare`, `apply`, `validate`. L'installation ne peut pas être appliquée deux fois. Les générateurs anciens n'ont pas été relancés.

**5 tests de calcul réussis** et **10 contrôles statiques réussis** : totaux par station, taux de conversion, références technologiques effectives déjà disponibles chez GBR, correspondance des fichiers préparés, préservation des armées et flottes étrangères, des amiraux, QG, ravitaillements et scopes, changement unique de niveau dans les bâtiments et couverture théorique des équipages. Les populations et terres arables récemment corrigées sont préservées par empreintes.

Le vieux parseur général `all_placements` échoue sur une syntaxe préexistante de `1776_r904_chiloe_port.txt`. Ce fichier n'est pas modifié : l'audit AST utilisé pour la présente mission lit les placements actuels et permet de vérifier le seul bâtiment concerné. Les anciens contrôles d'égalité globale d'une version précédente ne doivent pas être réécrits pour masquer les deux nouveaux changements autorisés.

ColGrep : un appel tenté, accès au verrou de l'index refusé ; aucune exécution du modèle local 2B n'est revendiquée. Repli sur chemins exacts et outils existants.

## Vérification en jeu restante

Après redémarrage, créer une **nouvelle partie au 1er janvier 1776** et choisir GBR. Vérifier les sept stations et les 120 navires, la composition 19/28/29/44, les 36 niveaux de Home Counties, les marins recrutés et affectés. Relever le rang, le prestige, le solde budgétaire, les salaires et les prix de ravitaillement au premier jour puis après une simulation bornée ; vérifier sauvegarde et rechargement. Une ancienne sauvegarde ne reçoit pas automatiquement ces modifications d'historique.

Aucun commit, push, changement du vanilla ou modification des autres pays.
