# CENTRAL-01 — Amérique centrale et Caraïbes au 1er janvier 1776

**27 octobre 2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Cinq transferts territoriaux et trois régions de revendication corrigés. Pas de nouvelle partie testée, pas de certification complète des frontières régionales. Aucun commit, merge, rebase ou push.

## Modifications installées

| Région | Avant | Après | Portée |
|---|---|---|---|
| Littoral oriental du Honduras | SC1 : 23 provinces ; MKT absent de la région | SC1 : 20 ; MKT : 3 | Extension de la représentation miskitu vers la Mosquitia hondurienne et Cabo Gracias a Dios ; sphère miskitu et établissements britanniques imbriqués |
| Nicaragua | SC1 : 19 ; MKT : 4 | Identique | Les trois provinces honduriennes rejoignent les quatre MKT existantes par terre |
| Sainte-Lucie | Grande-Bretagne | France | Règlement de 1763 ; la conquête britannique de 1778 n'est pas anticipée |
| Trinité | Grande-Bretagne | Espagne | La conquête britannique de 1797 n'est pas anticipée ; Tobago reste britannique |
| Guatemala/Belize, Honduras, Nicaragua | Aucune revendication explicite | Claim SC1 ajouté dans chacune des trois State Regions | Prétention espagnole séparée du contrôle effectif ; ne donne pas ces terres à SC1 |

Les RGB précis sont `x600AC6`, `x907080`, `x528F3B` pour la Mosquitia hondurienne, `x5299CA` pour Sainte-Lucie et `x707080` pour la Trinité. `PLAN.json` et `PROVINCES.json` donnent les correspondances. Les deux îles sont identifiées par leur géométrie réelle et un calage insulaire distinct. **Aucun pixel du bitmap n'est modifié.**

La frontière miskitu suit les provinces existantes : c'est une approximation régionale, pas une frontière de royaume documentée au mètre. Le secteur du Río Tinto comporte un établissement anglais attesté ; sa représentation au sein de MKT, déjà sous protectorat britannique dans le mod, abstrait cette coexistence. Aucun transfert de toute la côte à GBR et aucun nouveau comptoir isolé installés. La relation MKT–GBR est conservée, sans prétendre qu'elle restitue toutes les formes de négociation locale.

## Attributions conservées après examen

- **Chiapas, Guatemala et provinces administrées de l'Amérique centrale : SC1**, abstraction coloniale existante dans l'orbite espagnole. La capitainerie du Guatemala possède une organisation propre ; ce maintien n'en fait pas une province administrée uniformément depuis Mexico. Aucun État indépendant UCA créé artificiellement.
- **Panama : SC2 / Nouvelle-Grenade**, conservé. Cela ne prouve pas une occupation espagnole de tout le Darién.
- **Belize : trois provinces GBR conservées**, représentant les établissements de coupe britanniques. Leur enveloppe héritée est trop proche d'un Belize ultérieur pour être certifiée en 1776 ; aucune frontière des accords de 1783/1786 n'a été importée pour la remplacer.
- **Saint-Domingue française, Santo Domingo espagnole, Cuba et Porto Rico espagnols** conservent leurs dépendances initiales. Aucun transfert d'Hispaniola selon le traité de 1777.
- Jamaïque, Bahamas, Bermudes, Dominique, Grenade, Saint-Vincent et Tobago conservent leur attribution britannique ; Guadeloupe/Martinique restent françaises, les ABC néerlandaises et les îles danoises sont conservées. Pour Saint-Vincent, le titre colonial ne certifie pas le contrôle effectif des territoires caraïbes. Les micro-îles partageant des RGB ne sont pas certifiées individuellement.

## Population, bâtiments et dépendances

La seule redistribution de POPs déplace **1 803 Miskitu déjà présents dans STATE_HONDURAS**, dont le commentaire hérité indique Cabo Gracias a Dios, de SC1 à MKT dans cette même région. Culture, religion éventuelle, type et effectif sont conservés. Les 231 380 autres habitants SC1 du Honduras restent chez SC1. Aucun ajout démographique ni conversion culturelle.

Dans la State Region partagée des Antilles, les cohortes nationales existantes demeurent inchangées. Le format ne donne pas de recensement par île : le transfert d'une province ne permet pas de déduire le nombre exact de ses habitants. Cette conservation technique ne vaut pas correction historique des effectifs de Trinidad ou Sainte-Lucie. Plusieurs valeurs héritées, notamment les anciennes calibrations insulaires et commentaires de recensements postérieurs, réclament une passe démographique spécialisée ; aucune population n'a été inventée ou réduite pour cette carte.

Tous les bâtiments, niveaux, PM, réserves, propriétaires économiques, formations, profils technologiques et définitions nationales sont inchangés. Les anciens propriétaires gardent des terres dans leurs régions partagées : aucun de leurs sélecteurs économiques n'est supprimé par ces transferts. Le bloc UCA vide du fichier de bâtiments du Chiapas est une dette technique héritée sans bâtiment à redistribuer ; il ne justifie pas un propriétaire UCA.

## Fichiers modifiés et résultats

**Deux fichiers runtime seulement :**

1. `common/history/states/00_states.txt` : cinq attributions et trois claims.
2. `common/history/pops/06_central_america.txt` : cohorte miskitu de 1 803 habitants.

Outils : `tools/central01_audit.py`, `tools/central01.py`. Dossier de preuves : baseline d'empreintes, inventaire régional, copies `before/` et `patch/`, `PATCH.json`, `PLAN.json`, contrôles de géométrie, deux aperçus, sources et reçus. Les recherches et livraisons précédentes restent conservées ; aucun suivi WORLD/SERG mis à jour.

**21/21 contrôles installés réussis**, dont : syntaxe des deux fichiers ; empreintes du patch ; correspondance des cinq transferts ; autres propriétaires et commandes inchangés ; aucun nouveau doublon ou RGB vide ; membership des State Regions ; claims bornés ; conservation des identités/effectifs par région ; scopes POPs dotés de terres ; bitmap/locators inchangés ; conservation des bâtiments/armées/profils ; absence de nouveau TAG. Les sept provinces MKT sont reliées dans **une composante de pixels traversables**, avec contacts par côtés, provinces infranchissables exclues et règles d'adjacence respectées. Les **501 provinces SC1** restantes conservent une seule composante du graphe terrestre ; les trois retraits ne coupent pas la Nouvelle-Espagne. Les **14 RGB à propriétaires multiples** déjà présents dans l'historique mondial restent 14 : dette extérieure inchangée, pas une nouvelle régression.

**8 tests de non-régression de la loi coloniale américaine réussis**, 0,007 seconde, sortie `OK`. Les anciennes frontières nord-américaines sont inchangées dans l'historique d'États. Les contrôles ne constituent ni un lancement moteur ni une preuve de rentabilité ou d'accès militaire réel. Aucune nouvelle modification concurrente détectée entre préparation et vérification ; `CONCURRENT_FILES.json` est vide pour cet intervalle. Les travaux africains déjà présents au début restent dans la baseline, sans être attribués à cette mission.

## Limites qui restent ouvertes

1. **Talamanca, plaines du nord du Costa Rica et Darién** : autonomie autochtone attestée ou fortement étayée ; l'enveloppe coloniale actuelle demeure trop générale. Il manque la correspondance des limites aux RGB et une répartition culturelle/démographique défendable pour installer des entités locales. Ne pas lire leur maintien comme validation historique.
2. **Belize, Petén et Yucatán** : souveraineté nominale, districts administrés, établissements britanniques et espaces mayas ne se confondent pas. Le découpage fin n'est pas clos.
3. **Petites îles composites** : plusieurs îles aujourd'hui distinctes partagent un même RGB. Une attribution complète des possessions françaises/néerlandaises dans le groupe septentrional exige des séparations par composantes et une étude insulaire ; le fait de conserver les ABC ne valide pas toutes les Antilles néerlandaises.
4. **Hispaniola et Saint-Vincent** : limite pré-accords de 1776/1777 et autonomies autochtones non redessinées. Effectifs et composition des POPs insulaires non recalibrés.
5. **Claims par State Region** : les revendications espagnoles débordent certains districts précisément attestés. Le format ne fournit pas de claim par province ; aucun claim sur toutes les Antilles n'a été créé.

Cette passe corrige les anomalies identifiées et démontre leurs effets techniques. Elle **ne clôt pas** tous les découpages de l'Amérique centrale ou des Caraïbes.

## Vérification en jeu à effectuer

Nouvelle partie au 1er janvier 1776 : vérifier MKT au Honduras et Nicaragua, la continuité et les camps diplomatiques ; contrôler SC1 dans les plaines administrées et SC2 au Panama ; ouvrir les claims du Guatemala/Honduras/Nicaragua ; vérifier Sainte-Lucie française, Trinité espagnole et Tobago britannique. Comparer les bâtiments et populations des régions partagées, l'accès aux marchés et les formations ; simuler un mois puis sauvegarder/recharger. Aucun de ces résultats moteur n'est attesté ici.

## ColGrep

Un appel local abouti en **163,54 secondes**, après une tentative bloquée par le verrou de l'index. Trois pistes : une source POP directement utile, une recherche économique de contexte, une recherche militaire périphérique. Le dossier territorial R8 a été retrouvé par recherche exacte complémentaire. Pas de compteur de tokens Codex exploitable ni de comparaison témoin ; **aucune économie exacte de quota démontrée**. Voir `COLGREP.md`.
