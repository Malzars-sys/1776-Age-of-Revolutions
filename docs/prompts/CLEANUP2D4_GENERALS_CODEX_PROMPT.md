Tu travailles sur le mod Victoria 3 `1776_Age_of_Revolutions_fork`.

BRANCHE CIBLE
`cleanup-post-release`

MODÈLE RECOMMANDÉ
GPT-5.6 Thinking avec raisonnement élevé.

PHASE
CLEANUP-2D-4 — Starting Generals 1776

OBJECTIF
Implémenter les généraux terrestres du setup 1776 à partir du paquet de recherche historique fermé.
Cette phase concerne UNIQUEMENT les commandants terrestres. Ne touche pas aux amiraux.

SOURCE DE VÉRITÉ — À LIRE INTÉGRALEMENT AVANT TOUTE MODIFICATION
- `docs/research/military/GENERALS_1776_MASTER.csv`
- `docs/research/military/GENERALS_1776_SOURCES.md`
- `docs/research/military/GENERALS_1776_COMMAND_STRUCTURE_NOTES.md`
- `docs/research/military/GENERALS_1776_REJECTED_CANDIDATES.csv`
- `docs/research/military/CLEANUP2D4_GENERALS_1776_RESEARCH_COMPLETE.md`

RÈGLE ABSOLUE
Le MASTER contient une décision pour chacune des 214 formations terrestres post-2D3.
Ne fais PAS de nouvelle recherche historique et n’invente PAS une identité pour remplacer un champ vide.

RÈGLES D’IMPLÉMENTATION
1. Si `implementation_decision` vaut `IMPLEMENT_NAMED_HISTORICAL_GENERAL` ou
   `IMPLEMENT_NAMED_MILITARY_OFFICEHOLDER`, utilise exactement `recommended_character`.

2. Si la ligne vaut `PROCEDURAL_ALLOWED`, `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` ou
   `PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK`, crée/attache un général techniquement valide mais sans identité
   historique fixe. Préfère la génération culturelle/native du jeu si l’API le permet.
   - ne mets pas `historical = yes`;
   - n’invente pas de date de naissance;
   - n’invente pas d’office;
   - n’invente pas de biographie.

3. Ne transforme jamais un gouverneur ou souverain en général sauf si le MASTER le recommande explicitement en raison
   d’un rôle militaire distinct.

4. `HIGHER_COMMAND_ABSTRACTION` et `NAMED_MILITARY_OFFICEHOLDER` sont des mappings de gameplay. Ne prétends pas dans
   les commentaires qu’ils commandaient littéralement une formation portant le nom généré par CLEANUP-2D-3.

5. Respecte `GENERALS_1776_REJECTED_CANDIDATES.csv`. Ne réintroduis notamment pas les anachronismes prussiens ni
   Suvorov au 1er janvier 1776 sur la base d’une mission criméenne plus tardive.

INVARIANTS
- Vérifie HEAD et working tree avant de commencer.
- Conserve exactement les 214 formations terrestres post-2D3.
- Ne crée ni ne supprime de formation pour satisfaire la règle de commandant.
- Ne modifie pas `count`, `service_type`, `hq_region`, ownership, lois, diplomatie, bâtiments ou technologies.
- Ne touche pas aux flottes ni aux amiraux.
- Préserve les scopes de formation stabilisés en 2D-3.
- Aucun fichier technologique protégé ne doit être modifié.

DETTE LEGACY À NETTOYER DANS CE PÉRIMÈTRE
- GBR : dette `colborne_gen` / `aylmer_gen`.
- BIC : dette `maitland_gen` / `madras_army`.
- PRU : personnages militaires legacy anachroniques/non validés.
- Un bloc `create_character` existant n’est pas réputé historique simplement parce qu’il existe.
  S’il n’est pas accepté par le MASTER, applique la décision du MASTER pour cette formation.

MÉTHODE
A. Construis d’abord une matrice statique des 214 formations :
   formation, scope(s), commandant(s) actuel(s), ligne MASTER, action prévue.
B. Produit un AVANT/APRÈS avant modification.
C. Implémente avec des changements minimaux.
D. Si le MASTER ne retient aucun nom, reste procédural.
E. N’ajoute pas de traits, idéologies ou âges historiques spéculatifs.

CONTRÔLES STATIQUES OBLIGATOIRES
- `git diff --check`
- exactement 214 formations terrestres après modification;
- 214/214 disposent d’au moins un général attaché/transféré de façon résoluble;
- 0 `transfer_to_formation` vers un scope inexistant;
- 0 scope de personnage ambigu/dupliqué;
- 0 commandant historique fixe absent du MASTER;
- 0 candidat REJECTED réintroduit;
- 0 modification de flotte/amiral;
- 0 modification de fichier technologique protégé;
- localisations EN/FR complètes pour les noms fixes réellement ajoutés;
- aucun doublon de localisation.

RUNTIME QA — À CONDENSER DANS UNE SEULE OUVERTURE DE VICTORIA 3
Planifie les tests avant le lancement. Le démarrage du jeu est coûteux; utilise plusieurs chargements/sauvegardes dans
la même session plutôt que plusieurs relances.

Dans la session :
1. nouvelle partie 1776;
2. vérifier au minimum USA, GBR, AUS, RUS, SPA, PLC, BIC, MYS, PAN, MARATH, GWA, TRA, MUG, SIA, BUR;
3. vérifier plusieurs cas procéduraux Europe/Afrique/Asie;
4. confirmer que les formations inspectées ont un général et qu’aucun amiral n’a été modifié;
5. surveiller les logs `create_character`, `transfer_to_formation`, scopes inexistants, localisations brutes;
6. recharger au moins une sauvegarde dans la même session et reconfirmer quelques cas.

LIVRABLES À CRÉER
- `docs/reports/cleanup/CLEANUP2D4_STARTING_GENERALS_1776_IMPLEMENTATION.md`
- `docs/research/military/GENERALS_1776_IMPLEMENTATION_MATRIX.csv`

Le rapport doit inclure :
- HEAD initial/final;
- liste exacte des fichiers gameplay modifiés;
- total formations = 214;
- nombre de named historical assignments;
- nombre de procedural assignments;
- legacy commanders supprimés/remplacés;
- contrôle des scopes;
- résultats statiques;
- résultats runtime;
- `git diff --check`;
- confirmation explicite : aucun fichier technologique protégé modifié;
- confirmation explicite : aucune flotte/amiral modifié.

GIT
Ne fais aucun commit/push sauf instruction humaine explicite.
Laisse les modifications non stagées si aucun ordre contraire n’est donné.
