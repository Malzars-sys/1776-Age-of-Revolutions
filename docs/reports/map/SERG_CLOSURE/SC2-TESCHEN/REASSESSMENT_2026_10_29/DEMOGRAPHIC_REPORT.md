# Teschen : comparaison des populations et de leurs périmètres

**Aucun nouveau total de 1776 suffisamment comparable n'a été établi.** Le pool de 135 753 reste conservé comme donnée technique. Son remplacement par 112 850 ou 112 752 serait prématuré ; inversement, les sources ne permettent pas de certifier qu'il représente correctement la population du périmètre historique.

Références détaillées : [SOURCES.md](SOURCES.md), S1 et S2.

## Trois objets statistiques différents

| Nombre | Date et portée | Catégories et qualité | Comparabilité avec le mod |
| --- | --- | --- | --- |
| **112 850** | Dénombrement politique/militaire 1770–1771, ensemble de la Silésie de Teschen : huit villes et 240 villages ; 14 806 maisons selon S2 p. 41. | S1 p. 197 inclut **680 Juifs** ; 60 837 hommes + 52 013 femmes. Biais militaire et déséquilibre des sexes expressément signalés. | Total régional antérieur de cinq à six années ; pas un relevé des seuls domaines personnels du couple, ni un compte déjà apparié aux 179 cellules. |
| **112 752** | Statistique ecclésiastique fondée sur 1770, publiée par Adamus dans un classement comprenant aussi des paroisses ultérieurement créées. | S1 p. 283 : 78 406 catholiques + 34 346 non-catholiques, **sans les Juifs**. S2 p. 41 imprime 34 342 et une différence de 108, deux incohérences arithmétiques explicites ci-dessous. | Paroisses, villes, faubourgs et localités : unités non interchangeables avec domaines, juridictions ou pixels. Édition complète Adamus non directement consultée. |
| **135 753** | Initialisation actuelle du split `STATE_WEST_GALICIA/AUS` en 1776, sept groupes de POP. | Pool conservé lors de la réparation MAP2A ; origine technique, pas estimation reconstruite ici à partir d'un recensement comparable. | Le propriétaire et le nom régional ne constituent pas une correspondance territoriale avec le dénombrement. Aucun transfert ou changement de composition réalisé. |

Les chiffres de 112 850 et 112 752 couvrent notamment Bielsko et Frýdek, juridictions distinctes du duché central. L'hypothèse « les 22 903 habitants supplémentaires seraient simplement les seigneuries absentes du dénombrement politique » est donc **écartée**. Ces seigneuries sont déjà comprises dans sa portée régionale telle que décrite par S1/S2.

## Localités : correspondance documentaire, pas découpage inventé

| Localité / ensemble | Donnée reprise des sources | Portée et risque de confusion | Correspondance actuelle aux cellules |
| --- | --- | --- | --- |
| Cieszyn/Teschen | 3 831 ; S2 p. 41 distingue 3 218 sous juridiction urbaine et 613 des villages suburbains. | Ne pas assimiler automatiquement au seul centre bâti. | Non certifiée ; noyau historique identifié, mais absence d'appariement fiable avec le bitmap. |
| Bielsko/Bielitz | 3 397, S1 p. 197 et S2 p. 41. | Inclusion d'une juridiction distincte ; ne prouve pas que tout son duché est dans une seule ligne urbaine. | Non certifiée ; diagnostic MAP1B Teschen/Bielsko, pas un relevé de localités du RGB. |
| Frýdek | 2 490, S1 p. 197 et S2 p. 41. | Ville, pas total de toute la seigneurie. | Non certifiée entre le RGB cible et ses voisins occidentaux. |
| Fryštát | 1 046, S2 p. 41. | Seigneurie distincte incluse dans l'espace recensé. | Non certifiée. |
| Skoczów ; Strumień | 1 294 ; 1 316, S2 p. 41. | Villes du duché central. | Non certifiée. |
| Jablunkov et dépendances | 1 461 ; S1 indique 1 712 avec Biała. S2 p. 42 indique jusqu'à 1 962 selon inclusion de Bělá et de Písečná. | Bases spatiales différentes ; ne pas prendre ces valeurs pour trois recensements comparables ni confondre Bělá avec Biała près de Bielsko. | Non certifiée ; le choix des faubourgs pourrait influer sur une future correspondance. |
| Wisła ; Morávka ; Brenna ; Czechowice | Respectivement 2 078 ; 1 993 ; 1 775 ; 1 772, S1 p. 197. | Grandes localités rurales ; ne pas additionner un village à une paroisse qui le comprend déjà. | Non certifiée. |
| Bludovice, Vendryně, Těrlicko, Šenov, Meziříčí | Localités expressément citées par S2 p. 41. | La liste montre une couverture régionale, sans fournir ici le tableau intégral ni tous les rattachements politiques. | Non certifiée. |
| Ustroń, Mosty, Morávka, Istebna, Suchá | S2 emploie aussi le classement ultérieur en nouvelles paroisses et chapellenies locales. | Une structure paroissiale joséphiste de classement n'est pas une juridiction politique existant sous cette forme en 1770 ou 1776. | Non certifiée. |

S3, chapitre 5.8, date notamment le doyenné de Skoczów de **1777** et celui de Jablunkov de **1806**. Ces dates empêchent de traiter toutes les divisions ecclésiastiques du tableau publié comme des circonscriptions contemporaines de 1770. Le tableau des domaines de **1754** reproduit par S2 p. 40 fournit une piste de distinction des seigneuries, pas une population de 1776 à réutiliser par proportion.

## Écarts calculés et contradictions conservées

- Mod moins politique : **22 903**, soit **20,30 %** du total de 112 850.
- Mod moins ecclésiastique : **23 001**, soit **20,40 %** du total de 112 752.
- Différence des deux totaux historiques : **98**, alors que S2 p. 41 imprime **108**.
- Décomposition confessionnelle S1 : 78 406 + 34 346 = **112 752**. S2 imprime 34 342, donnant **112 748**, quatre de moins que son total annoncé. Vérifié sur l'image PDF p. 43, pas une simple erreur d'extraction de notre outil.

Les 98 habitants de différence nominale ne démontrent donc pas une identité de méthode. L'exclusion des Juifs du relevé ecclésiastique et leur inclusion dans le relevé politique sont une différence de catégorie substantielle. Ajouter mécaniquement les 680 à 112 752 serait tout aussi injustifié : les dates exactes, les omissions et les catégories de présence ne sont pas démontrées équivalentes.

Les calculs sont conservés dans `DEMOGRAPHIC_ARITHMETIC.json`. Ils ne fixent **aucun seuil de tolérance historique B**.

## Peut-on expliquer l'écart par une croissance jusqu'en 1776 ?

S2 p. 42 décrit une accélération qualitative en 1772–1776, associée notamment à l'activité textile, tout en rappelant les imprécisions des listes. Aucun taux local couvrant le même territoire n'y permet de calculer un total de départ 1776.

Atteindre 135 753 depuis 112 850 exigerait mécaniquement environ **3,13 % par an sur six ans**, ou **3,76 % sur cinq ans**. Ce calcul inverse est un diagnostic, **pas une estimation historique adoptée**. Il ne doit pas être remplacé par un taux choisi pour retrouver le nombre du mod.

S1 p. 200 donne ensuite **109 252 en 1780**, environ **115 263 en 1781**, et **121 753 en 1789**. Ces valeurs invitent à vérifier les séries et leurs catégories, pas à interpoler un 1776 prétendument exact. Les effectifs de toute la Silésie discutés par S2 p. 42 ne sont pas des taux spécifiques à Teschen ; les catégories « présents », « domiciliés », « étrangers » et les circonscriptions changent. Les chiffres du XIXe siècle ne sont pas extrapolés vers 1776.

## Réserve démographique proposée pour une conservation B

« Les 135 753 habitants sont conservés provisoirement pour éviter une redistribution sans périmètre comparable. Ils ne sont pas homologués comme population recensée au 1er janvier 1776. Le total régional de 1770–1771, plus faible, comprend déjà des seigneuries distinctes ; la différence n'est ni imputée automatiquement à une erreur du mod, ni expliquée par une croissance non mesurée. Les compositions culturelles et religieuses techniques ne sont pas validées par les seuls totaux retrouvés. »

Cette proposition est soumise au joueur. Elle n'est pas un reçu, une correction installée ou une clôture. Voir [l'arbitrage recommandé](ARBITRATION_PROPOSAL.md).
