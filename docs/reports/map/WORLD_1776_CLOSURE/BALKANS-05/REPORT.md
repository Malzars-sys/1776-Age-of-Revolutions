# BALKANS-05 — Albanie et Épire ottomanes

Livraison : 26 octobre 2026. Référence : 1er janvier 1776.
Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Recherche régionale : INCOMPLETE. Moteur : NOT_RUN. Nouvelle validation joueur : 0.

## Corrections installées

Deux maisons provinciales deviennent visibles dans les forces ottomanes : **Mustafa Bushati**, chef de la maison de Scutari, et **Ahmed Kurt**, mutasarrıf d’Avlonya. Deux traits d’office sans bonus et leurs textes français/anglais accompagnent les personnages. Les offices représentent leurs fonctions ; les généraux et formations sont une approximation du moteur, pas des gouvernements autonomes complets.

| Formation | Installation | Origine des unités |
| --- | --- | --- |
| Maison de Scutari | Mustafa Bushati, 2 bataillons réguliers d’infanterie irrégulière | Les 2 déjà présents dans l’armée de Roumélie, STATE_ALBANIA |
| Contingent d’Avlonya | Ahmed Kurt, 2 bataillons réguliers de cavalerie du type hussards | 2 des 4 déjà présents dans cette même armée/région ; 2 y restent |

**4 bataillons réaffectés, zéro ajouté ou supprimé.** Tous les effectifs mondiaux par pays, région, type et service sont identiques. Les conscrits, flottes, anciennes formations et affectations des anciens commandants sont conservés. Deux commandants supplémentaires sont créés : leur rémunération éventuelle, la composition de l’armée de cavalerie et leur comportement restent à observer au test groupé ; aucune gratuité budgétaire n’est affirmée.

## Cellules, frontières et populations

**Zéro cellule/RGB changé, zéro nouveau TAG, zéro transfert démographique.** Toutes les attributions existantes sont conservées. Les postes vénitiens B04 — xE8D211 Butrinto, xE8D212 Parga, xE8D213 Prévéza, xE8D214 Vonitsa — ainsi que Cérigo xE8D215, les anciennes Ioniennes, MON, RAG et les passages adriatiques restent identiques. Aucun tracé administratif des maisons n’est prétendu résolu.

| Périmètre technique | Avant | Après |
| --- | ---: | ---: |
| STATE_ALBANIA, portion TUR | 1 073 901 | 1 073 901 |
| STATE_ALBANIA, portion VEN | 500 | 500 |
| STATE_THESSALIA, portion TUR | 958 024 | 958 024 |
| STATE_THESSALIA, portion VEN | 4 700 | 4 700 |
| Monde | 834 936 539 | 834 936 539 |

Ces totaux sont ceux du scénario technique actuel ; cette passe ne les certifie pas comme des dénombrements de 1776. Tous les fichiers de POPs sont identiques, donc leurs ventilations également. Les régions natives ne sont pas assimilées aux limites historiques d’une province ottomane ou de l’Épire.

## Institutions, technologies et économie

L’appartenance TUR est conservée sans nier l’autorité effective des maisons locales. Aucune loi, succession impériale, relation diplomatique, fiscalité provinciale, ressource, bâtiment, recette ou PM n’est changé. L’autorité fiscale, les clans et les autres juridictions d’Épire restent une obligation régionale. Aucun gouvernement futur d’Ali Pacha n’est installé.

Les **23 technologies effectives TUR** sont identiques. L’audit commun avant/après reste FAIL_STATIC avec les mêmes trois observations : technologie de recrutement horse_artillery manquante pour les hussards déjà présents ; avertissement de ressource régionale à Diyarbakır ; profil historique impérial non certifié. L’infanterie irrégulière n’a pas de gate technologique. La réaffectation n’introduit aucun type d’unité ou constat nouveau, mais le recrutement des hussards reste restreint et leur fonctionnement initial n’est pas prouvé. **Aucun crédit T** ni grant automatique pour masquer cette dette.

## Sources et incertitudes

Le choix des titulaires est motivé dans SOURCES.md : travaux de Gjeli fondés sur les rapports consulaires, registre de nominations analysé par İnbaşı, comparaison avec Stamatović et notice TDV d’Ali. La direction effective de Scutari est distinguée du titre nominal. Les juridictions précises, dates de naissance, effectifs réellement présents et recrutement local restent incertains. Âges techniques : Mustafa 40, Ahmed 55 ; pas de naissance prétendument vérifiée. Les 2 000 cavaliers mentionnés par İnbaşı sont une obligation, pas un recensement de garnison. La divergence sur le décès ultérieur d’Ahmed Kurt est conservée.

## Contrôles, concurrence et progression

**52/52 contrôles statiques réussis**, après correction d’une différence de représentation tuples/listes dans le comparateur de preuves. La première trace 50/52 est conservée dans VALIDATION_RUN01.json ; aucun script du jeu n’a été changé pour résoudre ces deux faux écarts. L’audit technologique impérial reste explicitement en échec hérité, distinct du contrôle de non-régression du lot.

Un seul fichier partagé est retouché dans deux nœuds d’unités ; quatre fichiers spécifiques sont nouveaux. Les 2526 fichiers fonctionnels antérieurs hors patch sont identiques à la capture d’application ; 261 preuves des lots WORLD précédents sont préservées. Les 964 preuves SERG présentes à l’application restent identiques. Entre l’entrée de recherche et l’application, 3 documents SERG avaient évolué avec la clôture externe de Teschen ; copies courantes et empreintes archivées dans EXTERNAL_SERG_UPDATE.json. Aucun crédit humain WORLD n’en découle.

TECH-R1/R2/R3, ECON-ALLOYS/quincaillerie, fortifications/génie et autres travaux concurrents sont préservés. Aucune écriture Git, vanilla ou suivi SERG ; aucune ancienne baseline restaurée.

Seul **S de P1-05** reçoit un point : **10/80 Balkans (12,50 %) ; 10/320 WORLD (3,125 % exacts)**. O/I/D/E/T/R restent partiels, V non commencé. Aucun territoire ni région clos. Prochaine candidate : **BALKANS-06 — Grèce continentale, Péloponnèse et Crète**. Test balkanique groupé à la fin du travail techniquement réalisable ; aucune autre région avant confirmation explicite.
