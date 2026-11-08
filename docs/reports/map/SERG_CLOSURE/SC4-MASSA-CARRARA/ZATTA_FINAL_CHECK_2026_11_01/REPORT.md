# SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %

**SC4-MASSA-CARRARA — dernière tentative ciblée, 1er novembre 2026. Décision : NO-GO.** Recherche terminée ; **suspension des recherches actives recommandée**, sans report accepté, reclassification P2, clôture ou point. Aucun autre chantier commencé.

## 1. Zatta permet-elle de tracer une frontière pour 1776 ?

La référence Rumsey **11598.169** correspond au titre demandé, à **Venise 1783**, dans l’*Atlante novissimo*, tome III, feuille **F. III**. L’accès direct Rumsey présente une vérification d’accès ; sa reproduction n’a pas été téléchargée. Une **autre épreuve de la même feuille**, Antiquarius **MS4840**, a été téléchargée et réellement examinée : titre et date imprimés, éditeur Antonio Zatta, mentions G. Zuliani inc. et G. Pitteri scr. documentées au catalogue. Elle n’est pas présentée comme l’exemplaire physique Rumsey. [Sources et accès](SOURCES.md).

Le dessin montre des limites de territoires nommés et des contours colorés, distincts du réseau hydrographique. Leur interprétation politique générale est cohérente avec les notices d’archives. **Coloriage et titre ne suffisent pas à établir un droit de souveraineté ou chaque segment de frontière.** Aucun acte de cession ni légende juridique ne transforme cette carte d’atlas en bornage.

Marie-Thérèse reste souveraine de Massa-Carrare de 1731 à 1790 ; son titre de **consorte de Modène à partir de 1780** ne démontre pas une annexion. SIUSA conserve Montignoso dans le cadre lucquois et date son rattachement temporaire à Massa de **1807**, pas de 1776–1783. Les notices ciblées n’identifient pas de cession locale pendant ces sept années. Cela soutient l’emploi de Zatta comme **témoin d’ensemble**, sans prouver par silence la stabilité de tous les petits segments ni les franges GEN/TUS.

## 2. Concordances et différences avec Robert 1750

| Repère | Comparaison effectivement lue | Correspondance au jeu |
| --- | --- | --- |
| Carrare et Massa | Même ordre relatif, Carrare au nord-ouest de Massa. | Noyau politique reçu conservé ; aucune position géodésique des villes n’en est déduite. |
| Avenza | **Nom et symbole visibles chez Zatta**, sans équivalent suffisamment identifié sur le détail Robert employé. | Toujours aucune cellule identifiée de façon indépendante. |
| Villages et relief | Zatta précise notamment Torano, Moneta et les montagnes apuanes ; réseau local plus détaillé. | Les villages ne correspondent pas à des locators certifiés dans les cellules candidates. |
| Cours d’eau | Carrione/Frigido et vallées aident la lecture de Zatta. | **Aucun tracé fluvial local dans le secteur examiné de `rivers.png`** ; pas d’ancrage indépendant utilisable. |
| Sarzana/Lerici | Repères visibles dans Robert ; la feuille Zatta est coupée à l’ouest du secteur utile pour ces deux villes. | Aucun témoin génois supplémentaire permettant de trancher les pixels. |

Les différences de dessin du relief et de la côte ne sont pas traitées comme des cessions. Aucun ancien recalage rejeté, ajustement sur les mêmes locators ou transfert par proximité n’a été relancé. Images lues : détail Robert préexistant, Zatta entière et détail, bitmap courant et diagnostic hydrographique.

## 3. Quel contour est le mieux étayé ?

**Aucun contour de cellules n’est historiquement départagé.** Les trois options restent des hypothèses, y compris B :

| Option | Cellules ajoutées | MCA / parent MOD simulés | Connexité locale |
| --- | ---: | ---: | --- |
| A | 2 | 10 / 106 | Conservée |
| B | 5 | 13 / 103 | Conservée |
| C | 7 | 15 / 101 | Conservée |
| Anciennes trois | 3 | 11 / 105 | **MOD 104 + 1 : rejetée** |

Ces résultats sont recalculés sur le bitmap actuel, sans installation. Zatta améliore l’identification des lieux historiques mais **ne fournit pas le raccordement indépendant entre ces lieux et la grille du jeu**. Retenir B pour sa seule connexité resterait arbitraire.

## 4. Les 8 010 habitants sont-ils utilisables ?

La lecture de Lazzoni acquise le 31 octobre n’est pas recommencée. Les 3 700 citadins sont inclus dans les 8 010 communaux. La liste SIUSA des quatorze localités et la carte Zatta ne ventilent pas ce total et ne prouvent pas la concordance du *Comune* statistique avec le territoire représenté. **Pas de transfert : MCA reste 10 000, MOD/Émilie 495 752** ; 18 010 et 487 742 demeurent conditionnels. Population mondiale actuelle **837 328 654**, inchangée.

## 5. Arrêt et unique condition de reprise

Les cartes originales **Avenza 1775 b.84–86 / Carrare 1775 b.87–88** restent identifiées dans l’inventaire AS Massa, *Comune di Carrara, I Serie*. Les rubriques officielles « Archivio digitale-Massa » et « Fotoriproduzione » ont été retrouvées, mais répondent **HTTP 403**. Aucune reproduction exploitable de ces pièces n’a été obtenue ; cela ne prouve pas qu’elles ne sont pas numérisées.

**Reprise seulement à réception d’un dossier primaire communal de 1775 exploitable** : plans légendés avec ressort/localités, permettant leur raccordement à des repères indépendants et la concordance communale. Le relevé de maisons b.65 et les pièces b.250 peuvent orienter cette concordance ; ils ne sont pas assimilés à un recensement d’habitants. [Demande précise préparée, non envoyée](ARCHIVE_REQUEST_DRAFT.md). **Pas de nouvelle recherche identique proposée.**

## 6. Installation, contrôles et suivi

**Aucun gameplay modifié, aucune PR, aucun test moteur ni reçu nouveau.** MC-I-CORE, ses huit cellules et son attestation sont intacts ; 581 titres et neuf électeurs conservés. Seuls le présent dossier et les cinq fichiers canoniques de suivi sont actualisés dans le worktree courant ; [manifeste](FILES_MODIFIED.json).

Exécutions nouvelles : **28/28 contrôles ciblés PASS** ; suite Massa **10/11 PASS**, un ancien test de dernière couche obsolète conservé en échec ; suite canonique **27 PASS, un SKIP prévu**, aucun échec. Journaux bruts et [résultats statiques](STATIC_RESULTS.json) conservés. Les chiffres de contrôle du 31 octobre ne sont pas revendiqués comme nouveaux.

**Avant → après : 93/235 → 93/235 ; 39,57 % → 39,57 % ; 32/81 tâches qualifiées ; BLOCKED P0 maintenu, trois points non attribués.** Aucun nouveau test joueur nécessaire sans installation. Le protocole d’une éventuelle extension reste conditionnel, sans demander de refaire MC-I-CORE.
