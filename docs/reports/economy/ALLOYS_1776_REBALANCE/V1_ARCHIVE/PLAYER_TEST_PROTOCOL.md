# Validation joueur — alliages et ustensiles

Statut initial : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. Aucun des contrôles ci-dessous n'est déclaré réalisé dans le moteur.

## 1. Charger le contenu

Lancer une **nouvelle partie au 1er janvier 1776** avec le mod courant. L'Autriche ou la Prusse constituent de bons témoins de l'accès technologique : les profils contiennent alliages, ateliers et artillerie standardisée. Comparer ensuite un pays sans alliages, puis un pays industrialisé dans une partie de test séparée. Les lois peuvent interdire un bâtiment malgré une technologie acquise.

Vérifier qu'aucune clé brute ni icône manquante n'apparaît dans les choix décrits ci-dessous. Vérifier en français, puis en anglais si possible. Les sorties indiquées sont les valeurs de base ; débit et emploi peuvent modifier les valeurs réalisées.

## 2. Usine d'alliages

1. Vérifier le bâtiment disponible avec `alloysworking`, sans exiger du coke ni distribuer une technologie.
2. Sélectionner **Fabrication traditionnelle d'alliages** : 3 fer + 4 cuivre + 1 plomb + 2 charbon → 20 alliages ; 100 commerçants, 2 000 ouvriers et 100 machinistes pour ce PM.
3. Vérifier les autres groupes : les données industrielles ajoutent notamment leurs propres employés, intrants et sorties ; ne pas confondre leur total avec celui du PM de fonte.
4. Enregistrer prix locaux, emploi, salaire, revenu, dépenses et solde. Vérifier le recrutement progressif et la rentabilité une fois la demande/les intrants disponibles.
5. Dans une partie avancée de test, vérifier l'arc électrique à 90 et les procédés d'aluminium conservés. Le changement de PM ne doit pas créer une sortie totale négative d'alliages.

## 3. Artillerie

1. Comparer **Canons** et **Artillerie en bronze** avec les technologies requises. Le bronze exige aussi `alloysworking` ; l'option fer reste présente.
2. Vérifier 15 fer + 10 bois dur pour le fer ; 10 fer + 10 bois dur + 4 alliages pour le bronze ; 25 artillerie dans les deux cas, mêmes emplois.
3. Comparer le coût réel et le choix de l'IA selon les prix. Le bronze n'est pas toujours le choix le moins cher et ne doit pas être imposé à tous les arsenaux.

## 4. Manufactures de meubles

1. Vérifier le groupe **Fabrication d'ustensiles**. Le premier choix de la liste est le PM neutre ; confirmer le choix effectif du moteur pour un nouveau bâtiment et pour un bâtiment déjà présent.
2. Au neutre : aucun coût/emploi/produit supplémentaire. Vérifier que le bâtiment conserve sa production habituelle.
3. Fer forgé : 1 fer → +2 meubles ; 50 ouvriers.
4. Cuivre/laiton : 1 fer + 0,5 cuivre + 0,5 alliages → +5 meubles ; 100 ouvriers et 10 machinistes.
5. Usiné, avec `mechanical_tools` et `alloysworking` : 1 acier + 0,5 cuivre + 0,5 plomb + 0,5 alliages → +8 meubles ; 100 ouvriers, 50 machinistes, 10 ingénieurs.
6. Industrialisé, avec `mechanical_tools` et `bayer_process` : 1,5 acier + 0,75 cuivre + 0,5 plomb + 0,75 alliages + 1 aluminium → +16 meubles ; 120 ouvriers, 50 machinistes, 30 ingénieurs.
7. Tester un PM de luxe en parallèle : les choix se cumulent normalement sans multiplier toutes les sorties. Revenir au neutre doit retirer seulement les effets d'ustensiles.
8. Contrôler qu'un pays sans la technologie correspondante ne peut pas sélectionner le palier concerné. Le dernier palier doit rester tardif.

## 5. Consommation et équilibre

Dans les détails de consommation des POPs de richesse 10 et plus, vérifier la présence d'une petite substitution d'alliages parmi les objets domestiques. Ne pas lire « max_supply_share 0,05 » comme une limite de 5 % de toute la dépense.

Après stabilisation, relever les commandes d'achat des POPs, arsenaux, manufactures et anciennes industries. Relever le prix de l'alliage et celui du cuivre. Dans un pays industrialisé, vérifier que la demande domestique ne domine pas durablement les industries. Les scénarios du rapport n'imposent pas un volume mondial cible ni un prix fixe.

## 6. Stabilité et retour attendu

Laisser passer **au moins un mois complet**, sauvegarder et recharger. Vérifier la persistance des PM sélectionnés, les emplois, les commandes et les prix. Noter les nouvelles erreurs de chargement distinctement des erreurs connues ci-dessous.

Pour le retour : pays, date, technologies, PM actifs, prix des intrants/produits, emploi/salaires, solde, commandes POP/industrielles, captures des choix, et éventuels messages d'erreur. Les problèmes préexistants du validateur de trains et l'ancienne attente technologique figurent dans `TEST_RESULTS.json` ; aucun d'eux n'est une nouvelle validation moteur.

Ne passer le lot en validation humaine qu'après ce retour ; les statuts existants d'autres chantiers restent intacts.
