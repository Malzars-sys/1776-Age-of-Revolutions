# CENTRAL-02 — passe ciblée installée, 27 octobre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Cette passe ne remplace ni les baselines ni les preuves CENTRAL-01. La satisfaction exprimée par le joueur concerne cette livraison précédente ; elle n'atteste pas une nouvelle partie testée ni un résultat moteur pour CENTRAL-02.

## Corrections installées

| Secteur | Avant | Après | Population déjà présente réaffectée |
|---|---|---|---:|
| Río Frío / plaines du nord du Costa Rica | `xB0243F`, SC1 | G81, Guatusos du Río Frío, décentralisés | 1 000 |
| San Blas / Darién septentrional | `xBB820B`, SC2 | K81, noyau guna, décentralisé ; claim nominal SC2 | 2 881 |
| Saint-Vincent | toute l'île `x446C63`, GBR | 11 des 33 pixels deviennent `x446C64`, C81 ; reste GBR | 5 000 |

**8 881 habitants existants redistribués ; aucun habitant ajouté ou supprimé.** Aucun nouveau State_ID : les portions restent dans les trois State Regions existantes. Les deux noyaux continentaux utilisent les provinces disponibles ; la séparation de Saint-Vincent ne crée aucune terre et conserve exactement le littoral. Le locator minier régional est décalé sur le RGB britannique conservé pour éviter de le placer sur le nouveau territoire caraïbe. Aucun potentiel de ressource régional n'est augmenté.

G81 représente un noyau local guatuso, pas toutes les communautés des plaines du nord sous un gouvernement uniforme. K81 représente le littoral de San Blas, pas tout le Darién ni une frontière contemporaine de Guna Yala. Le reste du Panama conserve SC2 et ses places espagnoles ; ce maintien ne certifie pas leur contrôle de tous les espaces forestiers.

C81 représente l'autonomie intérieure caraïbe après le règlement de 1773. Le lien de **protectorat britannique** conserve la suzeraineté reconnue, au lieu de transformer la portion en pays sans lien avec Londres. La ligne du jeu est une réduction très grossière de la division nord/nord-est du traité ; une cellule représente plusieurs kilomètres. Les concessions amies et parcelles individuelles restent abstraites.

## Réserves démographiques et historiques

Les 1 000 Guatusos utilisent le repère estimatif publié pour **1778**, deux ans après le départ ; les 5 000 Caraïbes reprennent la borne basse d'une estimation des **années 1760**. Ce ne sont pas des recensements de 1776. La cohorte guna de 2 881 personnes est celle du mod, pas un effectif historique certifié. Ces valeurs réaffectent une partie du stock existant, sans augmenter les totaux régionaux ou mondiaux.

Les cultures de jeu `central_american`, `cariban`, `afro_caribbean` et leurs religions implicites sont conservées. Leur finesse ethnographique est insuffisante ; elles ne sont pas présentées comme un classement validé des Maleku, Guna ou Garifuna. Aucune conversion culturelle ou confessionnelle forcée n'est installée. Les drapeaux sont des marqueurs graphiques génériques hérités des conventions natives du mod, pas des drapeaux de 1776 certifiés.

**Talamanca non installé** : son autonomie est vérifiée, mais les chiffres se contredisent, les périmètres changent et le gros RGB caraïbe recoupe Matina et des secteurs de contrôle différent. Le nombre de 1801 n'a pas été rétroprojeté. En l'absence de ventilation localisée assez solide, aucune nouvelle population ni frontière artificielle n'a été ajoutée. Cette erreur de représentation héritée est explicitement ouverte, sans empêcher la transition R9 autorisée.

**Belize, Petén, Yucatán** : contrôle rapide des recommandations et des sources déjà consultées. Les claims CENTRAL-01 et ses établissements ne sont pas refaits. Aucun nouveau changement majeur suffisamment étayé et localisé dans ce contrôle ; les limites du Belize, les marges mayas et le détail des districts restent réservés. Aucun État itza indépendant postérieur à la conquête de 1697 ou de la guerre des Castes de 1847 n'est créé.

## Vérifications et fichiers

- **21/21 contrôles techniques réussis** : attributions exactes, autres propriétaires inchangés, pas de nouveau doublon ou province vide, conservation des cohortes par région, correspondance RGB/State Region, uniquement 11 pixels existants recolorés, aucun nouveau State_ID, capacités et hubs déclarés conservés, locator minier sur les terres britanniques, capitales des nouveaux pays possédées, noms FR/EN, suzeraineté de C81, bâtiments/armées et profils préexistants inchangés, cinq corrections CENTRAL-01 préservées.
- **Trois profils nationaux `PASS_STATIC_ONLY`, zéro signalement**, avec uniquement `traditional_food_processing`. Pas de paquet européen, nouvelle industrie ou unité importée.
- **8 tests de non-régression réussis**, 0,009 seconde, sortie `OK`. Contrôles statiques et tests de scripts uniquement ; aucun test moteur attesté.
- Aucune modification concurrente non listée détectée entre préparation et contrôle. Les travaux africains déjà présents sont conservés. Aucun commit, push ou autre écriture Git.

**13 fichiers runtime**, liste et empreintes dans `PATCH.json` : historique d'États, POPs d'Amérique centrale, bitmap, définitions de régions d'Amérique centrale, terrains, locator minier, relation diplomatique ; six nouveaux fichiers de définitions/histoires/flags/armoiries/localisations FR/EN. Le fichier `tools/central02.py` conserve la préparation bornée et la validation. Les sources téléchargées, pages rendues et décision d'exclusion du Talamanca restent dans ce dossier. Aperçu : `CENTRAL02_NUCLEI.png`.

Les empreintes sont celles de la livraison CENTRAL-02. Les passes R9 suivantes peuvent modifier à leur tour les mêmes grands fichiers partagés : leurs nouvelles baselines doivent préserver ces noyaux sans réécrire les copies `before/` de cette passe.

## Vérification en jeu attendue

Nouvelle partie 1776 : ouvrir G81, K81 et C81 ; vérifier population, subsistance, propriétaire de chaque noyau et suzerain britannique de C81. Contrôler les deux côtés de Saint-Vincent, le maintien de Sainte-Lucie française et Trinidad espagnole, les villes/ports de SC1 et SC2, puis simuler un mois et sauvegarder/recharger. Aucun accès au marché, équilibre économique ou comportement de l'IA n'est déclaré validé ici.

CENTRAL-02 est terminée dans ce périmètre : corrections sûres installées, réserves explicites. **La recherche et les premières corrections R9 sont autorisées et doivent suivre**, sans attendre les dossiers de micro-îles ou de démographie approfondie.
