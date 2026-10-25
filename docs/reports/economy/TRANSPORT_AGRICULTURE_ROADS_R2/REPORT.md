# Transport agricole et tickets routiers — R2

Révision du 23 octobre 2026, après la passe Anzin R1. La précision finale du joueur limite l’extension aux exploitations agricoles : aucun ajout aux centres urbains, qui conservent leurs propres transports.

## Changements appliqués

| Routes | Production précédente | Nouvelle production par niveau à plein emploi |
| --- | ---: | ---: |
| À péage | 3,2 | **5 tickets** |
| Pavées | 4 | **10 tickets** |
| Goudronnées | 6 | **15 tickets** |

Les valeurs sont les productions totales demandées, pas des ajouts à l’ancienne production. Aucun changement aux intrants, salaires, emplois, infrastructures ou technologies. Les routes en terre gardent leurs 400 emplois et leur infrastructure de 3, sans tickets marchands.

Le groupe de transport existant est ajouté aux six exploitations qui n’avaient aucune variante : seigle, blé, riz, maïs, millet et élevage. Il réutilise directement les mêmes PM que les mines : charrettes neutres par défaut ; transport ferroviaire après `railways`, avec 5 tickets consommés, −1 000 emplois d’ouvriers et +10 de pollution par niveau à plein emploi. Aucun PM agricole distinct aux valeurs divergentes n’est créé.

Les vignobles et plantations, y compris les épices, conservent leurs variantes déjà présentes sans doublon. Les exploitations de subsistance ne sont pas assimilées à de nouvelles industries agricoles constructibles. Les vingt manufactures équipées lors de R1 ne sont pas réécrites.

## Exclusions et préservation

- `building_urban_center` : aucun groupe ajouté ; `pmg_public_transport` conservé.
- Ports et bâtiments gouvernementaux : aucun ajout.
- Aucun ajout aux centrales, écoles d’art, centres de commerce ou autres bâtiments à la suite de la précision du joueur.
- Anzin, son bien de prestige et son icône, Saint-Gobain, carte et populations, fortifications, génie, États-Unis, Minutemen et accords franco-américains : fichiers hors périmètre inchangés.
- Deux fichiers fonctionnels seulement sont modifiés : les PM routiers et `common/buildings/02_agro.txt`. Seules trois valeurs de production et six lignes de références de groupe changent.
- **2 423 fichiers** hors périmètre conservés contre l’instantané de début de passe. Aucun fichier vanilla écrit ; HEAD, branche et index Git inchangés.

## Validation et économie indicative

**50/50 contrôles statiques réussis** : objectifs de tickets, conservation de tous les autres paramètres routiers, couverture agricole, variantes préexistantes, absence de doublons, PM identiques aux mines, technologie ferroviaire et exclusions.

Avec les prix et salaires fixes de référence de R1, les soldes hebdomadaires théoriques par niveau du module routier deviennent : terre −21 £, péage −78,75 £, pavées +12,50 £, goudronnées −146,25 £. Le détail est dans `REFERENCE_ECONOMICS.json`. Ces chiffres n’intègrent pas la baisse possible du prix local quand l’offre augmente et ne sont **pas des subventions observées en jeu**.

Les points de vigilance de R1 restent applicables : le débouché ferroviaire exige sa technologie et les réductions d’emplois peuvent se cumuler avec les autres automatisations. Aucun autre PM n’est rééquilibré dans cette révision.

## Vérification en jeu restante

Après redémarrage, vérifier les productions 5/10/15 dans les trois PM routiers, le nouveau choix dans les six exploitations et la conservation du transport propre aux centres urbains. Vérifier aussi les variantes déjà présentes des vignobles et plantations. Observer le prix local des tickets, les emplois et le budget pendant un mois, puis sauvegarder et recharger. Aucun test moteur, prix local ou résultat de sauvegarde/rechargement n’est revendiqué ici.

`BASELINE.json`, ses copies des deux sources, `VALIDATION.json` et `MANIFEST.json` conservent les preuves de cette passe. Le rapport R1 reste un relevé historique ; les objectifs routiers de cette R2 le remplacent pour ces trois productions.
