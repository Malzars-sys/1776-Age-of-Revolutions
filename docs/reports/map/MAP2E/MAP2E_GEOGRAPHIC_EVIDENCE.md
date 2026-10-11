# MAP-2E — Sources, méthode et limites

Date de référence : **1er janvier 1776**. Les conclusions régionales R3, les inventaires MAP-1 et le workspace réellement présent après MAP-2D sont réutilisés. La comparaison ciblée avec `georg3mx-map-rework` est conservée dans `COLLABORATOR_COMPARISON.json`. Aucun import global de cette branche n'a été effectué.

## Preuves historiques retenues

Les liens ci-dessous soutiennent l'existence des autorités et leur chronologie. Ils ne constituent pas une preuve cadastrale de chaque contour RGB.

| Cas | Source consultée et passage pertinent | Portée et limite |
| --- | --- | --- |
| Kartl-Kakhétie | Keith Hitchins, *Erekle II*, Encyclopaedia Iranica, VIII/5, 1998, p. 541–542. [Article](https://www.iranicaonline.org/articles/erekle-ii/) | Règne d'Héraclius II sur le royaume oriental à partir de 1762. Le protectorat de 1783 et l'annexion de 1801 ne sont pas transposés à 1776. Ne prouve pas les limites de chaque province. |
| Iméréthie et frontière ottomane | Université d'État Shota Rustaveli de Batoumi, résumé de thèse sur les rapports géorgiens, russes et ottomans au XVIIIe siècle. [Résumé bilingue](https://iverieli.nplg.gov.ge/bitstream/1234/371920/2/Annotachia%20G.K.%20%28%E1%83%A5%E1%83%90%E1%83%A0%E1%83%97.%20%E1%83%98%E1%83%9C%E1%83%92.%29.pdf), sections sur 1770–1774 | Distingue les autorités occidentales, les campagnes de Salomon Ier et le pacha d'Akhaltsikhé. Le résumé indexé a été consulté ; l'ouverture intégrale du PDF par le navigateur de recherche a échoué. Le regroupement occidental et la frontière de Javakhétie restent des approximations. |
| Kizliar et Mozdok | Tekin Aycan Taşçı, *Belleten*, vol. 86, n° 306, 2022, section 1.c. [Texte intégral](https://belleten.gov.tr/eng/full-text/3701/tur) | Positions russes antérieures à 1776 : Kizliar en 1735, Mozdok en 1763. La ligne fortifiée développée à partir de 1777 ne justifie pas une extension générale en 1776. Les forts n'établissent pas une souveraineté sur toutes les montagnes. |
| Terek et expansion russe | Magaramov, 2024, article de recherche sur la ligne du Terek. [Article](https://ojs3.caucasushistory.ru/2618-6772/article/view/17204) | Corrobore la distinction entre positions militaires septentrionales et conquêtes postérieures. Utilisé pour la chronologie, pas comme carte exhaustive. |
| Kouba et Derbent | *Encyclopaedia of Islam*, 2e édition, V, 1979, entrée « Kubba », p. 296–297. [Extrait académique](https://isamveri.org/pdfdkm/11/DKM111707.pdf) | Autorité de Fat Ali et contrôle de Derbent antérieur à 1776. L'aide russe de 1775 ne doit pas être transformée en annexion. Le texte indexé fournit la chronologie ; le regroupement Bakou/Salyan reste une abstraction. |
| Chirvan | Mustafa Aydın, « Şirvan », TDV İslâm Ansiklopedisi, 2010, sections sur Fat Ali. [Article](https://islamansiklopedisi.org.tr/sirvan) | Des khans locaux sont nommés sous l'influence de Kouba en 1774. L'abolition de la dynastie locale et l'administration directe de 1786 sont postérieures. Le TAG séparé représente l'autorité locale ; son indépendance native simplifie une influence réelle de Kouba. |
| Karabakh | George Bournoutian, *Ebrahim Khalil Khan Javanshir*, Encyclopaedia Iranica, VIII/1, 1997, p. 71–73. [Article](https://www.iranicaonline.org/articles/ebrahim-kalil-khan-javansir/) | Pouvoir régional des Javanshir, alliances et influence sur les voisins durant le dernier quart du XVIIIe siècle. Les relations ne sont pas converties en une souveraineté uniforme sur tous les melikats et khanats voisins. |
| Erevan | George Bournoutian, *Erevan*, Encyclopaedia Iranica, passage sur les khans de la fin du XVIIIe siècle et les relations avec la Géorgie et le Karabakh. [Article](https://www.iranicaonline.org/articles/erevan-1/) | Autorité locale et dépendances changeantes. Les données de recensements du XIXe siècle de l'article ne sont pas importées dans les populations de 1776. |
| Nakhitchevan | Bibliothèque présidentielle, histoire du khanat et de la dynastie Kangarli. [Dossier historique](https://nakhchivan.preslib.az/en_b2.html) | Autorité locale distincte après 1747. Utilisé pour identifier le khanat, sans reprendre les revendications modernes ni les chiffres démographiques tardifs. |
| Gandja, Chaki, juridictions voisines | Recherche numismatique de l'Oriental Numismatic Society, supplément du n° 197, carte et commentaire des autorités de la fin du XVIIIe siècle. [Étude](https://www.orientalnumismaticsociety.org/archive/ONS_Supplement_197.pdf) | Appuie la fragmentation en khanats et sultanats. La carte de fin de siècle ne prouve pas à elle seule tous les contours au 1er janvier 1776. Jar/Ilisu, Gazakh et les melikats sont explicitement signalés comme simplifiés. Le texte indexé a été utilisé, l'ouverture directe du PDF ayant échoué. |
| Talysh | Ouvrage universitaire sur les khanats, dépôt ADPU, section sur la formation du khanat de Lankaran/Talysh après 1747. [Ouvrage](https://e-book.adpu.edu.az/rrs-web/db/MEDIA/6d846702-12a1-4c08-8889-178e643d9fdc) | Appuie l'existence de l'autorité locale avant 1776. Le seul RGB retenu ne prétend pas restituer toute son extension méridionale. La culture persane existante reste un proxy du jeu. |

## Correspondance au jeu

`GEOGRAPHY_before.json` et `GEOGRAPHY_after.json` enregistrent les RGB, propriétaires, surfaces en pixels, boîtes englobantes, centroïdes et locators physiques. Les locators du jeu ne sont pas assimilés à des frontières historiques ni à une preuve de fondation urbaine en 1776.

Une transformation quadratique locale, conservant **les onze points de contrôle** et tous leurs résidus, est enregistrée dans `LOCAL_GEOGRAPHIC_FIT.json`. Les coordonnées géographiques modernes sont des repères arrondis ; ce ne sont pas des mesures cadastrales ou des observations GPS inédites.

- Erreur quadratique moyenne : environ **4,54 pixels**.
- Plus mauvais résidu : **Poti, environ 7,86 pixels**. Erevan et Choucha présentent aussi des résidus défavorables conservés.
- Beaucoup de RGB concernés ne font que 10 à 25 pixels de large. Ces erreurs excluent une prétention à la précision au pixel près.
- Mozdok est placé dans `x891792` de `STATE_STAVROPOL`, et non dans la province voisine initialement envisagée.
- Akhaltsikhé et Akhalkalaki guident `xC27075` et `x74A861`. L'extension `xC0CF80` reste une approximation de frontière orientale ottomane.
- Le repère de Lankaran soutient `x007060` pour Talysh sans imposer une modification du Gilan.

**Tous les 45 transferts sont classés DOCUMENTED_GAMEPLAY_APPROXIMATION.** La documentation historique soutient les autorités retenues ; le découpage du jeu et les limites de projection ne permettent pas de certifier chaque province comme une juridiction exacte.

Les neuf suppressions de doubles attributions sont distinguées des transferts. `xBCF376`, au sud du Kouban entre les secteurs de Maïkop et Armavir, reste à CIR. Huit RGB des montagnes septentrionales conservent leur propriétaire CIR ou CHC au lieu du second scope CAUC concurrent. Aucun bassin démographique n'est supprimé à cette occasion.

## Aperçus et géométrie

`north_before.png`, `north_after.png`, `south_before.png` et `south_after.png` sont des **aperçus techniques des propriétaires**, pas des captures de Victoria 3. Les petits points jaunes indiquent les locators existants. Le magenta indique les doubles attributions dans l'aperçu initial. Les couleurs sont propres à ces aperçus.

Le bitmap, les contours des RGB et les listes de provinces des State Regions n'ont pas changé. Quatre références de hubs ont été corrigées pour correspondre aux locators physiques existants : Telavi, Bolnisi, Armavir et Blagodarny. Aucun locator n'a été déplacé.
