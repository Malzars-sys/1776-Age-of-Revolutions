# Grande-Bretagne : agriculture, routes et effectifs — 9 octobre 2026

Cette vague complète les modifications navales précédentes. Elle concerne le
départ d'une **nouvelle partie** ; elle ne migre pas une sauvegarde existante.

## Bâtiments et méthodes britanniques

- Outilleries : Lancashire 6 → 5, Midlands 8 → 6, soit **−3 niveaux**.
- Mines de fer : Yorkshire 6 → 5, Midlands 6 → 5, soit **−2 niveaux**.
  Les pompes à feu restent actives pour le fer et le charbon.
- Calcaire métropolitain : Lancashire 2 → 1, Midlands 3 → 2, soit **−2 niveaux**.
  Les carrières coloniales ne sont pas réduites.
- Seigle : **58 → 48 niveaux**, répartis entre Home Counties (−2), Lancashire
  (−1), Yorkshire (−2), Midlands (−2), Est-Anglie (−2), Lowlands (−1).
- Les dix niveaux de seigle supprimés sont remplacés dans les mêmes États par
  **dix niveaux d'élevage**, avec **Collecte de laine accrue** (`pm_sheep_farms`).
  À plein effectif et avant bonus, ces nouveaux élevages produisent 150 tissus,
  consomment 100 céréales et produisent 25 engrais en plus de la viande.
- **Pommeraies** actives sur toutes les cultures de seigle britanniques.
  Les cultures de blé et de riz des Treize Colonies ne sont pas modifiées.
- Treize Colonies : **six plantations de coton**, trois en Virginie et trois en
  Caroline du Nord, avec propriétaires locaux dans les manoirs. Ces États ont
  des ressources compatibles et une marge de main-d'œuvre estimée suffisante.

## Infrastructures régionales

Routes à péage actives dans les dix États demandés. Les canaux déjà actifs sont
conservés ; aucun chemin de fer ni nouveau PM de voyageurs n'est ajouté.

| Pays | État | Niveaux avant → après |
|---|---|---:|
| Grande-Bretagne | Home Counties | 38 → 16 |
| Grande-Bretagne | Midlands | 15 → 8 |
| Grande-Bretagne | Est-Anglie | 7 → 5 |
| Grande-Bretagne | Highlands | 2 → 1 |
| Grande-Bretagne | Jamaïque | 6 → 3 |
| Grande-Bretagne | Bahamas | 2 → 1 |
| Grande-Bretagne | Terre-Neuve | 4 → 2 |
| France | Aquitaine | 2 → 1 |
| France | Auvergne-Limousin | 2 → 1 |
| France | Languedoc | 2 → 1 |

Home Counties conserve 112 points d'infrastructure routière à plein effectif,
avant les effets de population, ports, traits et multiplicateurs, pour les 106
points utilisés visibles sur la capture. Les autres États conservent au moins
leur ancienne contribution directe des routes et canaux, sauf les écarts
d'arrondi éventuels compensés par le bonus de population des routes à péage.
Le recrutement effectif doit néanmoins être vérifié en jeu.

Canaux industriels : bonus au plafond des économies d'échelle **0,05 → 0,1**.
Canaux aménagés : **0,1 → 0,5**. Portée, consommation et autres effets inchangés.

## Population et qualifications

Avec l'accord explicite de l'utilisateur, seuls les effectifs locaux de
**Terre-Neuve (63 343 → 200 000)** et de **Jamaïque (274 778 → 520 000)** sont
augmentés. Les proportions culturelles, religions et types de population
préexistants sont conservés, à l'arrondi d'une personne près.

Les emplois prescrits par les PM actifs sont estimés à 44 200 à Terre-Neuve et
114 700 en Jamaïque. Avec une hypothèse prudente de 25 % de travailleurs, les
populations ajustées donnent respectivement 50 000 et 130 000 travailleurs :
une réserve supérieure à 10 % pour les propriétaires, l'urbanisation et les
ajustements de mise en place. Ce calcul n'est pas un relevé du moteur du jeu.

Un plancher local d'alphabétisation initiale de 35 % est appliqué aux populations
non esclaves des dix États concernés par les routes à péage, après les effets
initiaux nationaux. Les populations plus alphabétisées ne sont pas abaissées.
Le seuil dépasse celui utilisé par la formule native de qualification des
bureaucrates (20 %) et aide le recrutement des employés. Il ne change ni la
loi éducative nationale ni les cultures et ne garantit pas à lui seul un
recrutement immédiat : acceptation culturelle, salaires, intrants et accès au
marché restent déterminants. Le moteur recalcule également l'alphabétisation
durant l'initialisation ; les effectifs du premier jour restent à vérifier.

## Garnison et déblocages navals

- Mediterranean Garrison : point de stationnement initial dans la partie
  britannique des Baléares, QG d'Europe méridionale conservé. Les neuf unités,
  leur origine de recrutement et le commandant ne sont pas modifiés.
- **Navire de ligne : Chronométrie marine.**
- **Frégate : Architecture navale.**
- La liaison Signaux navals → Charpente diagonale → Coques en fer est conservée.
  Aucun nouveau nœud technologique ou visuel n'est créé.

## Vérifications

`tools/audit_gbr_agriculture_followup.py` conserve la référence immédiatement
précédente, contrôle les changements exacts, les PM, les technologies de départ,
les cultures inchangées, les ressources, les niveaux et les marges de
main-d'œuvre estimées. Il protège les autres fichiers d'exécution par empreinte.
L'audit cumulatif `tools/plan_oct09_balance_revision.py --check` tient compte
de cette nouvelle vague sans écraser les références des modifications antérieures.

**Contrôles statiques uniquement : aucun redémarrage ni test en jeu effectué.**
