# SC4-MASSA-CARRARA — Carrare/Avenza, reprise ciblée du 29 octobre 2026

**Date de référence : 1776-01-01.** `SC4-MASSA-CARRARA`, priorité **P0**, poids **3 points conditionnels**. Ce document est une **instruction historique et géométrique préparatoire**, et **ne constitue ni un reçu moteur ni une autorisation de transfert**.

## Situation acquise et protégée

- `MC-I-CORE` reçu par le joueur : `MCA`, RGB `xEDBC00`, **8 cellules** côtières de `STATE_EMILIA`, **10 000** habitants reclassés depuis `MOD`, Marie-Thérèse Cybo-Malaspina, un bâtiment administratif, régime souverain et droit impérial borné ; un mois, sauvegarde/rechargement confirmés lors de la réception du noyau.
- Province résiduelle `xF08021` : **108 cellules MOD** après le détachement du noyau (116 initialement) ; ensemble connexe avant nouvelles modifications.
- Donneur modénais : **495 752** habitants de l'Émilie après `MC-I-CORE`. Les sources historiques utilisées pour les 10 000 massais ne représentent **pas** la population totale de Massa + Carrare.
- LUC, GEN, TUS, PAR, voisins italiens, 9 électeurs et droits impériaux déjà livrés doivent rester protégés. Pas de nouveau pays, pas de reconstitution générale de Lunigiana, pas de réexamen de Teschen.

## 1. Fait nouveau : périmètre de la principauté de Carrare

La notice d'archive officielle `SIUSA — Comune di Carrara` donne la composition de la principauté élevée en 1663 : **Avenza, Bedizzano, Carrara, Castelpoggio, Codena, Colonnata, Fontia, Fossola et Moneta, Gragnana et Noceto, Miseglia, Sorgnano et Torano**.

Source : https://siusa-archivi.cultura.gov.it/cgi-bin/siusa/pagina.pl?Chiave=2257&RicExtInquisizione=on&RicLin=en&TipoPag=prodente

Cette liste rend le ressort de Carrare politiquement bien plus précis que l'étiquette géographique générique `Massa-Carrara`. Elle ne justifie **pas** d'attribuer à MCA les seigneuries Malaspina voisines, Sarzana/Lerici, Montignoso lucquois, Pietrasanta/Seravezza toscanes ni la Garfagnana modénaise. Elle n'est pas en elle-même un cadastre de 1776 au pixel.

L'ancien rapport `B_PROPOSAL.md` et la carte Robert de Vaugondy de 1750 restent la base cartographique de comparaison ; aucun ancien recalage R4 rejeté n'a été relancé.

## 2. Fait nouveau : dénombrement de Carrare quasiment contemporain de 1776

**Emilio Lazzoni**, *Carrara e la sua Accademia di belle arti. Riassunto storico*, Pisa, fratelli Nistri, **1869**, série statistique reproduisant une situation de **1775** :

| Année | Ville de Carrara | Commune de Carrara | Interprétation |
|---|---:|---:|---|
| **1775** | **3 700** | **8 010** | La ville est comprise dans la commune : **ne jamais additionner** ces deux valeurs. |
| **1790** | 4 003 | 9 346 | Témoin de variation postérieure, pas population de 1776. |

Fac-similés numérisés en accès public :
- https://upload.wikimedia.org/wikipedia/commons/0/06/Carrara_e_la_sua_Accademia_di_belle_arti._Riassunto_storico_%28IA_carraraelasuaac1869lazz_0%29.pdf
- https://commons.wikimedia.org/wiki/File%3ACarrara_e_la_sua_Accademia_di_belle_arti._Riassunto_storico_%28IA_carraraelasuaacc1869lazz%29.pdf

**Niveau de preuve :** passage identifié dans l'index textuel des **deux scans** (table démographique vers la fin du livre), sans nouvelle vérification visuelle intégrale des pages de 11–12 Mo dans cette passe. Cette statistique rétrospective de 1869 n'est pas assimilée à l'original d'un recensement de 1775. Vérifier la page numérisée et le sens administratif précis de `Comune` avant installation. Le périmètre des villages doit être confronté à la liste SIUSA.

Témoin partiel plus proche : une étude fondée sur les archives de la paroisse de S. Pietro cite **836 habitants à Avenza en 1779**. Le chiffre provient d'une source locale de seconde main ; il est **inclus a priori dans le total communal** s'il relève du même ressort et **ne doit pas être ajouté** à 8 010.
- https://www.valdaveto.net/pdf/Una_famiglia_Cella_tra_Carrara_e_Massa.pdf
- https://www.carraraonline.com/chiesina_di_s_giuseppe.php

**Proposition démographique conditionnelle, jamais appliquée :** si `Comune` de 1775 et ressort politique de la principauté sont comparables, envisager un transfert comptable **de 8 010 résidents existants** de MOD à MCA, distinct des 10 000 massais déjà reçus, soit **MCA 18 010** et **MOD 487 742** dans les déclarations pertinentes, toutes choses égales par ailleurs, et **population mondiale inchangée**. Ce n'est pas une interpolation de 1775 vers 1776 ni une preuve qu'un chiffre exact de 1776 serait 8 010. Les minorités, métiers et champs existants doivent être conservés ; ne créer aucun nouvel habitant.

**Attention au piège statistique :** une reconstruction de la *province moderne* de Massa-Carrara mêle plusieurs autorités historiques (Pontremoli, Modène, Lucca, Toscane et fiefs) et **ne saurait remplacer** le ressort politique de MCA en 1776.
- https://www.researchgate.net/publication/345670919_A_Reconstruction_of_the_Italian_Provincial_Population

## 3. Résultats géométriques obtenus sur les listes de cellules déjà archivées

Données inspectées : `SC4-MASSA-CARRARA/GEOMETRY.json`, source installée du noyau. Tests de connexité **4-voisins** recomptés sur les listes actuelles, sans lire ni modifier le bitmap.

`xF08021` MOD comporte 108 cellules et `xEDBC00` MCA en comporte 8.

Les **trois cellules candidates historiques du blocage** `[4324,1028], [4325,1028], [4326,1028]` sont bien MOD et adjacentes au noyau, mais **les céder toutes les trois isolerait une cellule MOD** : résultat MOD [104, 1], bien que MCA passe à 11 cellules. **Cette découpe est rejetée topologiquement en l'état**.

Alternatives à titre de **pré-étude topologique uniquement**, sans preuve géographique Carrare/Avenza :

| Option candidate | Pixels transférés MOD→MCA | MOD restant | MCA total | Connexité 4-voisins |
| --- | --- | ---: | ---: | --- |
| A, minimale | `[4325,1028], [4326,1028]` | 106 | 10 | 1 bloc MOD, 1 bloc MCA |
| **B, pointe de cinq cellules** | `[4325,1028], [4326,1028], [4325,1027], [4324,1027], [4324,1026]` | **103** | **13** | **1 bloc MOD, 1 bloc MCA** |
| C, extension de sept cellules | `[4325,1028], [4326,1028], [4325,1027], [4324,1027], [4326,1027], [4324,1026], [4325,1026]` | 101 | 15 | 1 bloc MOD, 1 bloc MCA |

Ces pixels **ne sont pas homologués comme Carrare/Avenza**. Ils doivent être confrontés visuellement au détail Robert 1750, à l'orientation des localités répertoriées, à la côte, aux voisins et à la province actuelle. Les deux critères *géographie prouvée* et *connexité du parent* sont indépendants ; le passage du seul second ne suffit jamais.

Si une extension connexe de l'actuel `xEDBC00` est historiquement démontrée, il devrait être possible d'étendre **la même province RGB**, sans créer un nouveau pays ni un second titre impérial. Les changements fonctionnels exigeraient alors de mettre à jour **ensemble** le bitmap, les coordonnées déclarées, les contrôles de topologie/protection, le domaine impérial pour le RGB existant et le transfert démographique conservatif.

## 4. Décision pour cette passe

**SC4-MASSA-CARRARA reste `BLOCKED P0`, sans point supplémentaire, mais la réserve démographique possède désormais une cible chiffrée proche de 1776 (8 010).** L'autorité politique des lieux est fondée par SIUSA ; le maillon réellement manquant est un appariement satisfaisant des principales localités de la principauté à un contour B connexe, tout en confirmant le périmètre du total communal.

**Aucune installation de pixels ou POPs, aucune écriture du tracker canonique et aucun reçu utilisateur** dans cette passe. Le noyau `MC-I-CORE` et ses validations sont conservés ; les fichiers originaux restent source de vérité.

### Prochaine intervention unique, sans refaire un audit général

1. Lire visuellement les pages pertinentes du scan Lazzoni de 1869 pour confirmer l'intitulé `Città` / `Comune` et sa couverture politique vers 1775.
2. Superposer les localités SIUSA et le détail Robert de Vaugondy 1750 au secteur de `xF08021` : valider ou rejeter les trois **options de cellules** ci-dessus, ou proposer une alternative documentée.
3. Une fois **périmètre + population comparable + géométrie connexe** prouvés, livrer **une seule** extension MCA accompagnée de tests statiques/CI et protocole de validation en jeu en PR brouillon, avec relecture des droits impériaux et conservation des voisins.
4. Si le recoupement topographique reste impossible, proposer explicitement au joueur une catégorie B bornée avec réserve historique substantielle, **sans** faire passer tacitement un P0 en P2 ni attribuer les 3 points.

Teschen demeure suspendu de recherche active, non fermé et sans point nouveau. Ne pas rouvrir Piombino, Holstein, l'Autriche ni les chantiers économiques dans cette mission.
