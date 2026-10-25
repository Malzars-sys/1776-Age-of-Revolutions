# Validation joueur — version quincaillerie

Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. Aucun résultat moteur ou humain déclaré.

1. Commencer une **nouvelle partie au 1er janvier 1776**, par exemple en Autriche/Prusse pour tester les alliages et le bronze. Une ancienne sauvegarde ne certifie pas l'ajout d'une nouvelle marchandise.
2. Chercher **Quincaillerie** parmi les biens courants : prix de base 30, marché distinct et icône fournie. Vérifier l'absence de fond et de cadre, y compris dans l'anse et entre les objets, dans le marché et les infobulles.
3. Dans une manufacture de meubles, ouvrir **Fabrication de quincaillerie**. Confirmer le choix initial réel du moteur pour un bâtiment neuf et un bâtiment existant ; le neutre est premier dans la liste et ne doit rien ajouter.
4. Vérifier les recettes de base ci-dessous. Les chiffres réalisés varient avec le débit et l'emploi.

| Palier | Entrants | Sortie de quincaillerie | Emplois ajoutés |
|---|---|---:|---:|
| Forgée/moulée | 4 fer, 4 alliages | 20 | 500 |
| Cuivre/laiton | 6 fer, 3 cuivre, 5 alliages | 40 | 850 |
| Usinée | 6 acier, 4 cuivre, 3 plomb, 7 alliages | 80 | 1 400 |
| Industrialisée | 10 acier, 6 cuivre, 4 plomb, 10 alliages, 8 aluminium | 160 | 2 200 |

5. Les deux premiers demandent ateliers organisés + élaboration des alliages ; l'usinage demande `mechanical_tools` + alliages ; le dernier demande `mechanical_tools` + `bayer_process`. Tester les blocages sans technologie dans une partie distincte. Aucun nouveau nœud.
6. La sortie doit être de la quincaillerie, **jamais les anciens 2/5/8/16 meubles**. Les groupes de meubles normaux/de luxe doivent conserver leurs recettes. Revenir au neutre enlève seulement matières/emplois/produit de quincaillerie.
7. L'usine d'alliages traditionnelle reste à 3 fer + 4 cuivre + 1 plomb + 2 charbon → 20 alliages et 2 200 emplois pour son PM seul. Les autres groupes ajoutent notamment papier, données et emplois de bureau : ne pas confondre les totaux.
8. Artillerie bronze : 10 fer + 10 bois dur + 4 alliages → 25 artillerie ; option fer : 15 fer + 10 bois dur → 25. Vérifier que les deux restent disponibles selon leurs technologies.
9. Observer des POPs de richesse 10 et plus : quincaillerie dans les objets domestiques ordinaires, plus une faible substitution directe d'alliages. Pas de besoin de luxe créé.
10. Laisser tourner **un mois complet**. Relever prix locaux, production/ventes/commandes, emplois, salaires et solde des manufactures et usines. Observer le choix de PM de l'IA et la montée de demande d'alliages : cinq premiers paliers consomment déjà 20.
11. En partie avancée, vérifier le dernier palier à cinq métaux et les recettes électriques/aluminium conservées.
12. Sauvegarder/recharger ; vérifier persistance des PM et commandes. Contrôler français et anglais si possible, sans clé brute ni icône absente.

Retour utile : pays, date, technologies, PM, prix/salaires, emploi, solde et nouvelles erreurs. Les quatre erreurs anciennes du validateur (trains et attente de prérequis) sont distinguées dans `TEST_RESULTS.json`. Aucune validation humaine avant ce retour.
