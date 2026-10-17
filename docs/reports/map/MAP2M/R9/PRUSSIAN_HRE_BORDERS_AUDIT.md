# Autres possessions prussiennes — audit R9 sans nouveau transfert

L'audit effectif trouve **124 références de RGB sous PRU**, réparties sur14State_ID ;96figurent au registre impérial actif. Les28autres sont les19RGB de Prusse-Orientale,8de Prusse-Occidentale et1de Posen. Ce comptage porte sur des références natives ; les doublons et scopes hérités restent indiqués, sans les transformer en souverainetés historiques certifiées.

`PRUSSIAN_RGB_INVENTORY.csv` contient chaque RGB, State_ID déclaré, géométrie effective, propriétaire, taille, voisins RGB/propriétaires, présence et bénéficiaire au registre. `STATE_OWNER_PIXEL_INVENTORY.csv` ajoute le contexte des autres pays. Ces fichiers sont des inventaires réels, pas une reconstruction par noms de villes.

| Ensemble de1776 | Contrôle actuel | Bilan et limites |
| --- | --- | --- |
| Brandebourg / Neumark |16RGB PRU, STATE_BRANDENBURG | Noyau prussien impérial conservé ; aucune preuve nouvelle de frontière locale justifiant un transfert. Les six niveaux d'armement sont protégés. |
| Poméranie prussienne |17RGB PRU, STATE_POMERANIA, dont parent xE1A03A réduit à290cellules | Côte et séparation suédoise traitées dans R9 ; autres portions conservées, pas de cession globale à SWE. |
| Magdebourg / Halberstadt et voisinage d'Anhalt |9RGB PRU dans STATE_ANHALT,2dans STATE_BRUNSWICK | Les duchés/principautés historiques ne se confondent pas avec les régions économiques ; les enquêtes R2-0039 à0043 n'établissent pas encore chaque enclave du Harz. Pas de transfert arbitraire à ANH ou BRA. |
| Minden | xBBA504, xEDAA00, xEDAA01 et propriétés antérieures |76cellules restaurées intactes. Le reçu initial excluait ce sous-lot ; aucun reçu ultérieur spécifique ne permet de certifier exhaustivement Minden. |
| Lingen / Tecklenburg | xEDAC04 xEDAC0C et x4D62A0, STATE_HANNOVER |65cellules prussiennes de la continuation conservées ; souverainetés1702/1707 déjà documentées. Ne pas les redonner à Osnabrück/Hanovre. |
| Clèves / Mark / Ravensberg |5RGB PRU NORTH_RHINE,8RUHR,15WESTPHALIA ; périmètres historiques non équivalents | Acquis prussiens authentiques conservés. Franges voisines de Münster, Paderborn, Cologne, Lippe, Schaumburg-Lippe et villes/abbayes restent partielles. |
| Gueldre prussienne et enclaves rhénanes | PRU/NET/BEO et voisins dans les régions partagées ;3RGB PRU RHINELAND | Carte Schenk antérieure au partage1713 insuffisante pour attribuer toutes les franges1776 ; ne pas rétroprojeter1815 ni annuler le partage ancien. |
| Frise orientale / Emden | Hub portuaire natif Emden dans xF9DCA2 **HAN**, STATE_HANNOVER | **Anomalie manifeste de souveraineté** : la Frise orientale est prussienne depuis1744. Contour de restitution non appliqué, voir ci-dessous. |
| Silésie et Glatz |9RGB PRU LOWER_SILESIA,6UPPER_SILESIA dans les déclarations | Majorité prussienne après1742 et reliquats autrichiens à distinguer. Aucun transfert des RGB de Lusace sur le seul diagnostic ancien, ni importation1815. |
| Prusses orientale/occidentale et district de Netze | PRU, hors registre pour les RGB considérés | Monarchie prussienne distincte de l'appartenance territoriale impériale ; aucun ajout automatique au registre. |

## Frise orientale : problème reconnu, pas correction imaginaire

Le RGB portuaire `xF9DCA2` comporte **319cellules**, boîte X4251–4274, Y743–765. Il est attribué à HAN dans `common/history/states/00_states.txt` (ligne8182 lors de l'inspection) et déclaré dans `STATE_HANNOVER`, ID69. Le registre en conserve encore le bénéficiaire gelé HAN. La présence du hub Emden ne suffit pas à prouver que ses319cellules correspondent exactement à toute la Frise orientale prussienne, à l'exclusion de Jever et des franges d'Oldenbourg/Münster.

Une vérification historique ponctuelle, sans nouvelle campagne générale, confirme1744 et l'anachronisme d'une attribution hanovrienne pour ce noyau. L'[Ostfriesische Landschaft](https://www.ostfriesischelandschaft.de/beitraege/geschichte-der-ostfriesischen-landschaft/) confirme l'avènement de Frédéric en1744 ; la [ville d'Aurich](https://www.aurich.de/stadtinformationen/stadtgeschichte) distingue la période prussienne du rattachement à Hanovre après le congrès de Vienne. Pages institutionnelles consultées pendant R9. Elles attestent la souveraineté et la chronologie, **pas le contour complet du RGB**.

R9 ne transfère donc pas les319cellules sur la seule foi du nom Emden. Le correctif reste précisément localisé, prioritaire et ouvert : confronter ce seul parent et ses voisins à une frontière territoriale identifiable, conserver Jever et les domaines voisins, puis mettre à jour bénéficiaire impérial et historiques selon le contour retenu. `PRUSSIAN_HRE_BORDER_CHANGES.csv` reste vide de données appliquées.

## Silésie et anomalies héritées

La lecture conservée `MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/SILESIA_READING.md` distingue partition1742/1743, confirmation1763, frange lusacienne et erreurs de scope. Ses erreurs de contrôle atteignent6.632pixels à Glogau,9.429à Görlitz et27.864à Olomouc : ce modèle n'est pas réutilisé pour dessiner une nouvelle limite.

`x71E080` et `xF0E080` sont géométriquement en MORAVIA, mais déclarés sous UPPER_SILESIA avec écritures AUS/PRU ; `x9061E0` est géométriquement WEST_GALICIA et écrit sous UPPER_SILESIA pour AUS. Ces erreurs héritées ne prouvent pas un propriétaire légitime à elles seules. Elles ne sont pas « réparées » en choisissant un souverain arbitraire.

Le registre impérial est un instrument de gameplay existant. Ses96références prussiennes ne certifient ni le statut juridique impérial de toute la Silésie ni un rattachement uniforme à un cercle. L'appartenance institutionnelle de chaque territoire doit rester distincte de sa souveraineté prussienne ; les cercles ne sont pas redéfinis dans R9. Les parts hors Empire de la monarchie ne sont pas annexées à son registre par leur seul TAG.

## Limites de l'audit

Les petits territoires de Bentheim, Steinfurt, Rietberg, Corvey, Essen-Werden, Dortmund et Nassau restent les questions déjà listées dans `RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv`. Un voisin PRU n'autorise ni l'annexion à Münster ni la création d'un pays à partir d'un point.

La liste des124références est un audit des possessions écrites sous **PRU**, pas une prétention à résoudre toutes les unions dynastiques ou les institutions des autres pays. Aucune frontière voisine n'est changée par opportunité. Erfurt–Eichsfeld reste entièrement gelée.

Bilan : noyaux acquis et corrections antérieures préservés ; **Frise orientale explicitement non corrigée**, limites silésiennes/rhénanes encore ouvertes ; zéro nouveau transfert dans ce sous-audit. Ce n'est pas un certificat que toutes les frontières prussiennes du SERG sont historiquement exactes.
