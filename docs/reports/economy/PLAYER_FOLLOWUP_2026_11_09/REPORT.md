# Ajustements économiques demandés après la review — 9 novembre 2026

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** pour les nouveaux réglages. Le joueur a accepté la passe moteur précédente avant ces modifications ; cette acceptation ne constitue pas un essai de la nouvelle recette routière ou des nouveaux niveaux.

## Consignes et résultat

- Retrait de `pm_organized_forestry`, de sa ligne de groupe et de ses noms FR/EN. Ses cinq sélections initiales deviennent `pm_simple_forestry`. Les deux méthodes avaient les mêmes entrées/sorties et emplois. La technologie `organized_forestry`, ses bonus, déblocages et attributions restent inchangés.
- Suppression de la sortie d'outils des cinq ateliers domestiques de subsistance : ferme, verger, pâturage, village de pêche et rizière. Vêtements, meubles, alcools et restrictions de lois sont conservés. Le fichier garde son chemin pour préserver les fournisseurs uniques installés par 23. Son commentaire devenu faux et le contrôle de politique dans l'outil TECH sont adaptés.
- Routes à péage : bois **4 → 5** et outils **2 → 0**, par niveau à effectif complet avant les autres modificateurs. La recette n'a plus que le bois comme intrant. Production de transport, infrastructure, emplois, icône et prérequis restent identiques. Cette recette commune s'applique à tous ses utilisateurs ; l'activation de départ demandée concerne uniquement la Grande-Bretagne.
- Outillage britannique : **quatre** niveaux déplacés, deux vers Yorkshire et deux vers Midlands, après correction explicite du joueur : « Il y a cinq niveaux à l'encachi, pas dix. » Le bloc Lancashire du fichier 98 passe de 5 à 1 ; Midlands dans ce fichier de 6 à 8 ; Yorkshire dans le fichier régional de 2 à 4. Aucun PM, réserve, type ou destination de propriétaire de ces trois blocs n'est changé. Les autres fabriques d'outils restent intactes.
- Verreries : les deux déclarations antérieures des Midlands reçoivent `pm_leaded_glass` et `pm_ceramics`. Trois niveaux supplémentaires sont installés : +1 Midlands, +1 Lancashire, +1 Yorkshire, avec ces PM. Le façonnage manuel est conservé et les nouveaux propriétaires financiers sont locaux. Le prérequis `industrial_ceramics` est déjà attribué à GBR ; aucune technologie n'est donnée.
- L'usine chimique des Midlands utilise déjà `pm_lead_chamber_process` et reste identique.
- Les neuf États de Grande-Bretagne ont déjà leurs réseaux routiers initialisés avec `pm_turnpike_road_network`. Cette activation ne nécessite pas de réécriture. L'Irlande et les activations coloniales restent intactes, conformément à la réponse « grande bretagne pas irland ».

## Déclarations et observation moteur à distinguer

Le fichier régional contient aussi une ancienne déclaration Lancashire de six niveaux ; additionner mécaniquement cette variante à la déclaration de cinq du fichier 98 avait conduit à la mauvaise proposition initiale. Aucune installation de ce déplacement de dix niveaux n'a eu lieu. La correction finale part des **cinq niveaux observés par le joueur**, et ne déplace que quatre.

Le diagnostic de dernière déclaration donne outillage **Lancashire 1 / Yorkshire 4 / Midlands 8**, contre 5 / 2 / 6, soit 13 niveaux dans les trois États avant/après. Les trois modifications chiffrées conservent également la somme littérale des niveaux déclarés. Pour le verre, ce diagnostic donne Midlands 2 / Lancashire 1 / Yorkshire 1, contre Midlands 1 seul. Ce modèle est cohérent avec les observations du joueur, mais n'est pas un nouveau chargement moteur certifié. Les variantes historiques et la topologie globale des fichiers ne sont pas refondues dans ce lot.

## Contrôles exécutés

- **14/14** contrôles ciblés : références, cinq variantes de subsistance, disparition complète du PM retiré et de ses consommateurs actifs, recette routière, sorties de transport conservées, niveaux demandés, PM verriers, prérequis, neuf activations routières et chimie déjà active.
- Audit économique effectif existant : **26 204 références**, aucune cible manquante ou ambiguë, erreur de lecture, PM initial hors groupe ou prérequis de PM incompatible avec son bâtiment.
- Conservation de **2 516 sources préexistantes** : uniquement les dix fichiers fonctionnels et l'outil TECH prévus diffèrent ; aucun changement inattendu. Toutes les empreintes finales correspondent aux candidats relus. Aucun nouvel espace final dans les lignes ajoutées.
- Chaque écriture était conditionnée à l'empreinte courante. Les spans autorisés, versions antérieures et candidats sont conservés. Le candidat R2 corrige seulement la mise en forme des insertions ; le premier candidat reste archivé.
- Les anciens contrats de conservation de 23 qui exigeaient le quatrième PM forestier ou les coefficients d'outils sont désormais historiques pour ces champs expressément supprimés par le joueur. Ils ne sont pas réécrits pour afficher un résultat vert. Le contrôle TECH courant interdit désormais les outils et vérifie les trois autres sorties conservées.

Aucun fichier vanilla, Git, frontière, population, loi ou profil technologique n'est écrit. Aucun résultat de prix, emploi, pénurie ou rentabilité observé en jeu n'est inventé.

## Vérification utile au prochain lancement

Nouvelle partie 1776 : vérifier Lancashire 1 et les ajouts +2 Yorkshire / +2 Midlands, les trois nouveaux niveaux de verre et leurs PM ; contrôler une subsistance sans outils et une route à péage consommant uniquement 5 bois à effectif plein. Les anciennes sauvegardes ne réinitialisent pas les bâtiments de départ. Les recettes communes peuvent s'y actualiser, mais la migration automatique d'une ancienne sélection du PM forestier supprimé n'est pas certifiée.

Preuves : `FINAL_PLAN_R2.json`, `before/`, `candidate_R2/`, `INSTALLATION_RECEIPT.json`, `VALIDATION.json`, `ECONOMY_REFERENCES_AFTER.json`, `SOURCE_BASELINE.json`, `SOURCE_PROTECTION.json`. Les autres travaux locaux sont préservés.
