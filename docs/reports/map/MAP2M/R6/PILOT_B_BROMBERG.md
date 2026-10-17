# Pilote B — Bromberg et Fordon

**Partiel : 18 candidates polonaises anciennes, directement adjacentes au noyau prussien, restent C. Aucun transfert.** Le noyau `xEDB010` conserve 85 cellules, le résidu `xFCC7B7` 142 cellules. Thorn est exclu.

## 1. Identifier la bonne ligne avant de la géoréférencer

Le manuscrit N 1146/1 possède plusieurs objets graphiques qu'il faut séparer :

- La note des noms rouges porte sur une propriété privée, celle de la générale von Skorzewska. Elle n'attribue pas une souveraineté.
- Le liseré de la rive occidentale de la Vistule vers Fordon ne peut pas être accepté en bloc comme séparation Prusse–Pologne. Le contexte de Chełmno/Culm et Fordon après 1772, et les subdivisions colorées de Güssefeld, empêchent cette lecture automatique. La fonction exacte de chaque tronçon du manuscrit reste à démontrer.
- Le liseré méridional de Güssefeld 1775, sous Bromberg, est une piste politique différente. Neuf sommets sont conservés en pixels source dans `SOURCE_LINE_OBSERVATIONS.json`, et illustrés dans `B_SOUTHERN_1775_CANDIDATE.png`. Aucun sommet réel n'est inventé.

La couleur rouge/jaune n'est pas un code universel de souveraineté. Le manuscrit est un brouillon/copie daté [1772] au catalogue ; la date de chaque ajout et son identité avec le tracé de 1775/1er janvier 1776 ne sont pas établies. Les légendes, les territoires nommés et la datation doivent être lus ensemble. Aucune ligne de 1777 ou de l'édition Pfau 1778 n'est adoptée automatiquement.

## 2. Ce qui fonctionne désormais dans le raster

Le filtre R5 omettait l'indice 15 de la palette de rivières. R6 le lit correctement : 17 pixels supplémentaires dans cette fenêtre, et une Vistule continue. Ce n'est pas une modification du jeu.

Un nouveau contrôle final est réservé par une règle fixe : minimum de longitude des sommets Vistule dans [18,04–18,26 E ; 53,08–53,22 N], face au minimum X des largeurs natives dans [4507–4518 ; 760–770]. Il vise le coude au sud de Fordon, pas son centre urbain, pas le confluent de la Brda et pas le point de rivière le plus proche d'une prédiction.

Référence réelle : **18,142334 ; 53,114765**. Milieu des cinq cellules natives ex æquo : **4510,5 ; 763,5**. Prédiction du profil figé : **4510,8183 ; 764,1002**. Désaccord au milieu : **0,6794 pixel**. Ce point est dans le support R5, hors ajustement et hors sélection R6.

Le plateau natif est toutefois étalé sur cinq cellules : rayon de lecture requis 2,5 pixels, contre 1,5 prévu initialement. Ce dépassement est déclaré et le protocole n'est pas réécrit. Il ne faut ni annoncer une précision certifiée de 0,68 pixel, ni une erreur moyenne régionale fondée sur un seul coude schématique.

## 3. Pourquoi les cellules restent C

Le raccord réel→natif a un nouveau diagnostic utile ; le raccord de la **bonne ligne politique source→réel** n'est toujours pas accepté. Aucun nouveau jeu d'objets distribués et homologués ne justifie de caler les scans sur des centres urbains choisis approximativement. Les croix ambiguës d'Inowrocław/Pakość ne sont pas réoptimisées pour contourner ce manque.

R6 n'examine que les anciennes candidates dans la fenêtre locale et partageant un côté avec `xEDB010` : **18 cellules**, pas toutes les 77 de la Netze et surtout pas les 142 du résidu annexées en bloc. Le statut d'extrapolation est calculé pour chaque centre de cellule ; cinq candidates sont hors support. Sans conversion complète et stable de la ligne souveraine, aucune n'est A.

## 4. Suite ciblée

Conserver la lecture méridionale de 1775 et comparer ce seul tronçon à une ligne souveraine datée du manuscrit. Fixer des homologues source→réel précis, de part et d'autre de ce tronçon, et des contrôles nouveaux hors ajustement. Le confluent Brda–Vistule et les îles fluviales ne sont pas supposés stables sans vérification des régularisations. Il n'est pas utile de rouvrir les quatre districts ou de réoptimiser Pfau avec les mêmes croix.
