# SC2-BOHEMIA — livraison du 19 octobre 2026

**SERG TERRITORIAL 1.0 — PROGRESSION : 28,09 %**

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — livraison `READY_FOR_SCOPED_RUNTIME_VALIDATION`. La nouvelle installation n'a aucun reçu humain. Le dossier comprend un audit daté des grands contours et juridictions et une correction démographique; aucune nouvelle frontière dessinée.

## Progression et sélection

Début de demande : 60/235 = 25,53 %, 19 jalons justifiés. Le reçu utilisateur explicite est enregistré pour le seul noyau Salzbourg de 12 cellules B : 66/235 = 28,09 %, 20 jalons justifiés. Le validateur sélectionne alors SC2-BOHEMIA, P0 sans dépendance. Après cette installation en attente : **66/235 = 28,09 %**, poids de la Bohême non acquis. Aucun changement de barème, de périmètre 1.0.0 ou de dénominateur.

Le reçu salzbourgeois est [conservé dans son dossier](../SC1-SALZBURG/RUNTIME_USER_ATTESTATION_2026_10_19.json). Il reprend uniquement le protocole global confirmé, un mois et sauvegarde/rechargement sans anomalie. Aucune langue, date réelle de test, mesure moteur ou observation détaillée supplémentaire n'est inventée.

## Correction installée et preuve de périmètre

Un seul fichier fonctionnel : `common/history/pops/00_west_europe.txt`, seulement **neuf valeurs size** dans STATE_BOHEMIA / AUS. Total **3 375 003 → 2 500 000**, soit **−875 003 habitants**. Le total est une estimation arrondie de scénario; les repères comparables de Bohême seule et les limites de méthode sont exposés dans [SOURCES.md](SOURCES.md) et [DEMOGRAPHY.json](DEMOGRAPHY.json). Ce n'est pas un recensement exact de 1776.

Les neuf groupes sont redimensionnés au prorata par plus forts restes, en conservant cultures, religions, métiers et ordre. Totaux initiaux attendus : tchèque 1 550 934, allemand du Sud 903 287, ashkénaze 45 779. Ces proportions héritées ne sont pas présentées comme un nouveau relevé historique. La population mondiale écrite passe de **835 801 255** à **834 926 252**; tout l'écart provient de Bohême, sans population déplacée ailleurs.

21 RGB, **4 412 cellules**, State_ID **52**, propriétaire **AUS**, inchangés. Liste exhaustive avant/après et contacts voisins dans [BOUNDARY_AUDIT.json](BOUNDARY_AUDIT.json); inventaire [NATIVE_INVENTORY.png](NATIVE_INVENTORY.png). Le statut B signifie une enveloppe politique généralisée conservée, sans précision cadastrale. [SECTOR_AUDIT.md](SECTOR_AUDIT.md) explique séparément BOH-W/N/E/S/I/D, les cartes effectivement lues et les décisions.

Aucun changement de province, pays, capitale, personnage, gouvernement, loi, bâtiment, niveau, propriétaire économique, PM ou unité. AUS conserve Marie-Thérèse, la capitale nationale Vienne, le centre régional Prague et son abstraction des états provinciaux. Le gubernium historique n'est pas transformé en souverain indépendant. Une substitution de PM bureaucratique a été rejetée car incompatible avec la loi AUS; aucune loi nationale n'est modifiée pour contourner cette contrainte.

Registre impérial **574 entrées**, neuf électeurs et fichiers compilés identiques à la capture immédiate. Pas de nouveau membre BOH ni duplication de son titre. Les noyaux déjà acquis, notamment Salzbourg, et toutes les autres populations régionales sont conservés. Le fichier de population est partagé avec Salzbourg : sa seule empreinte globale change, tandis que **tous les octets hors des neuf tailles bohémiennes restent identiques**, dont le bloc SLZ.

## Vérifications effectuées

- **35/35 contrôles statiques et de non-régression réussis** : portée textuelle exacte, analyse syntaxique, propriétaires/géométries, populations hors Bohême, variations globales culture/confession, bâtiments/unités, registre, preuves archivées, acquis et Git. [VALIDATION.json](VALIDATION.json).
- Suite cumulative : **313 réussites sur 317**, **3 échecs hérités**, **1 exclusion d'initialisation**. Les trois échecs sont les mêmes assertions d'ancienne dernière couche déjà identifiées avant SC2; elles attendent une couche antérieure à Salzbourg en fin de registre. Elles ne sont ni supprimées ni rendues artificiellement vertes. **Aucun nouvel échec inexpliqué.** [TESTS.json](TESTS.json), [journal brut](TESTS.log), [analyse](TEST_REVIEW.json).
- Contrats courants de Bohême, Salzbourg et feuille de route : **56 réussites sur 57**, aucune erreur et une exclusion d'initialisation. Tests négatifs : refus d'un changement de région, culture, religion, métier, nombre de groupes, commentaire ou total; invariants de progression et de passage au joueur. [SCOPED_TESTS.json](SCOPED_TESTS.json).
- Les **44 RGB dupliqués et 12 références invalides hérités** restent identiques à la capture; aucune nouvelle anomalie de ce type. Ce résultat ne les résout pas et ne signifie pas que l'ensemble du mod est sans défaut.
- Aucun moteur exécuté par l'agent. Aucun commit, push, staging, merge, reset, rebase ou changement de branche; HEAD, branche et empreinte de l'index sont conservés.

## Attente et limites restantes

Le total annuel exact de 1776, les proportions culturelles/sociales, micro-limites Eger/Asch, enclaves et détails près de Glatz ne sont pas établis. Les cartes anciennes sont contrôlées par les cessions de 1635/1742/1763 et les réformes de 1751/1763; leurs couleurs ou douze cercles ne deviennent pas le droit de 1776. Aucune correspondance source-vers-cellule assez précise n'a été établie pour justifier une retouche. Les régions Moravie, Silésie et Teschen ne sont pas déclarées auditées intégralement par cette passe.

La baisse de population agit sur emploi, fiscalité, consommation et recrutement; ces effets doivent être examinés dans une nouvelle partie. Les bâtiments et conscrits sont conservés, sans compensation arbitraire. **Validation utilisateur en attente.** [Protocole détaillé](PLAYER_TEST_PROTOCOL.md) : Autriche au 1er janvier 1776, contrôles par sous-lot, un mois, sauvegarde/rechargement. Tout résultat non observé doit rester signalé comme tel.

Prochaine action : **test joueur SC2-BOHEMIA**. Prochain candidat d'implémentation après résultat : **SC2-MORAVIA**, P0, dépendances actuelles satisfaites, **NOT_STARTED**. Aucune recherche ou installation de ce lot n'a été entreprise. La sélection sera recalculée à la réception du test et d'une mission autorisée.

Les événements de progression restent additifs : RM-0004 reçoit Salzbourg, RM-0005 livre la Bohême sans point supplémentaire. Les autres 80 fiches restent identiques à la capture qui suit l'acceptation salzbourgeoise. [Vérification du suivi](TRACKER_VALIDATION.json), [conservation](TRACKER_PRESERVATION.json), [manifeste final](DELIVERY_MANIFEST.json).
