# SAHEL-01 — Nord de la Sénégambie

Date de référence : 1er janvier 1776. Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Premier lot borné de la bande Sénégal/Mali–mer Rouge, **pas clôture de toute la bande**. Le joueur a déclaré les contrôles du Maghreb passés et autorise cette transition ; reçu limité dans MAGHREB_USER_CONFIRMATION.json, sans durée ni version testée inventée.

## Corrections installées

- Waalo (WAA), pays indépendant non reconnu, restauré sur xEF30C0 (hors noyau côtier), xA80844 et x3A5023, auparavant français.
- Fouta-Toro (FTR) reçoit x267B18, x329831 et x339E4C, auparavant français. Ses trois provinces antérieures restent intactes. Aucune révolution de 1776 datée artificiellement au 1er janvier.
- Saint-Louis britannique : quatre pixels terrestres (3719–3722,1734), nouveau xE8D241, incluant le locator natif de la ville et un débouché côtier. Pas d’annexion britannique du Waalo.
- Gorée française : xE8D242, un pixel à (3707,1771), prélevé sur le parent côtier CAY xBCFFB5. **Proxy politique côtier** : l’île distincte n’existe pas dans le bitmap natif. Aucun pixel marin changé en terre, aucune grande cession du Cap-Vert déduite de traités de papier. Parent CAY conservé.

Géométrie : cinq pixels recolorés, deux RGB nouveaux, six provinces réattribuées. États administratifs natifs, ressources, terrains des parents, modèles de hubs et reste du bitmap conservés. Le contour Waalo/Fouta suit les provinces disponibles : approximation politique, pas cadastre exact. Les limites des royaumes au sud restent ouvertes.

## Populations et données nécessaires

Monde **837,328,539 → 837,328,539**, delta zéro. Ancien pool FRA Sénégal : 131 968. Répartition installée : FRA/Gorée 1 569 ; GBR/Saint-Louis 4 622 ; WAA 62 889 ; ajout FTR 62 888, soit FTR final 157 264. Toutes les identités de cohortes culture/religion/statut servile du pool sont conservées à l’unité à l’échelle globale. Aucun habitant ajouté ou supprimé.

Les deux totaux de comptoirs sont des observations de 1776. La ventilation des cohortes est héritée, non un recensement ethnique ou servile corrigé. Le résidu partagé entre les deux groupes de trois provinces est une allocation technique explicite, pas une estimation historique nouvelle de densité. Cette démographie reste incertaine.

WAA : monarchie/oligarchie comme représentation minimale du brak et des élites électrices ; aucun dirigeant historique inventé, aucun événement/trait/flavor ajouté. Six technologies rurales, artisanales et d’échanges explicites, dépendances valides. Loi de coutumes commerciales propre à WAA, recette strictement identique au mercantilisme courant, disponibilité via relations internationales ; évite d’attribuer l’assurance maritime pour débloquer des droits commerciaux. Aucun graphe TECH ou recette ECON commun modifié. Aucun bâtiment/PM/unité nouveau ; les centres de commerce français hérités restent dans la portion française.

## Sources, incertitudes et contrôles

SOURCES.md distingue textes consultés, extraits indexés et rendu cartographique indisponible. La date de souveraineté est étayée ; le contour de l’île et la délimitation cadastrale ne sont pas certifiés.

**48/48 contrôles statiques** : patch exact des nœuds Sénégal et composition contrôlée de deux modifications américaines indépendantes, propriétaires uniques, seulement cinq pixels terrestres, pays continus, population et cohortes conservées, index Git inchangé et preuves antérieures préservées. Profil WAA : PASS_STATIC_ONLY, six technologies, aucun constat. Aucun lancement moteur par l’agent. Protocole groupé, aucune demande de test intermédiaire.

Concurrence : trois fichiers avaient évolué depuis le premier relevé (états, populations et régions d’Amérique du Nord). Pendant les vérifications, le même chantier a transféré xBA821E de QPW à LOU et retiré une revendication USA au Texas. Le premier contrôle strict (39/42) est archivé dans VALIDATION_RUN01_CONCURRENT.json ; ses trois écarts correspondent à ces changements externes, pas à un échec du Sénégal. EXTERNAL_COMPOSITION_REVIEW.json rapproche les deux nœuds des reçus américains et conserve leurs versions exactes. Le contrôle courant utilise cette composition explicitement bornée. Application sur les versions courantes, pas sur la première baseline. Le contour Fezzan de 78 provinces demandé séparément est préservé, ainsi que Siwa, Gibraltar, Balkans, SERG, TECH-R1/R2/R3 et ECON. Aucune opération Git d’écriture, aucun suivi SERG ou vanilla écrit.

## Suite

Inventaire courant de 22 régions dans SAHEL_BELT_INVENTORY.json. TERRITORIAL_QUEUE.json ordonne les royaumes sénégambiens restants, Mali/Tombouctou, Niger, pays haoussa, bassin du Tchad/Darfour puis Nil/mer Rouge. Les gros ensembles MSN/SOK/SD1 restent des corrections à étudier et installer, pas des régions déjà validées. Travail exclusivement territorial ; personnages et raffinements de bâtiments différés.

P3-01 reste partiel : aucun critère régional entier crédité. WORLD reste **10/320, 3,13 %** selon le dénominateur historique, qui inclut des domaines désormais différés. Ce chiffre ne mesure pas le nombre de frontières corrigées.
