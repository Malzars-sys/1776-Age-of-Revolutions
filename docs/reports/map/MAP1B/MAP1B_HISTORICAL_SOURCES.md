# MAP-1B — Sources effectivement consultées

Date de consultation : **10 octobre 2026**. Date historique cible : **1er janvier 1776**. Périmètre limité aux dossiers MAP1-P0-001/002/003. Les fichiers bruts restent dans `MAP1B_GEOGRAPHIC_EVIDENCE/`; leur empreinte est enregistrée dans `EVIDENCE_SHA256.csv`. Les nouveaux tracés sont des diagnostics, pas des frontières historiques certifiées.

## Reprise des recherches régionales

R1 : `R1_WESTERN_EUROPE_RECOMMENDATIONS.csv`, lignes -0001 (Luxembourg), -0004 (Pays-Bas autrichiens), -0035 (Bouillon), -0008 (Venise), -0009 (Milan/Mantoue), et `R1_WESTERN_EUROPE_UNCERTAINTIES.md`, sections P0 Luxembourg et Lombardie. Sources régionales S001–003, S008–010, S034, S037. Documents conservés dans `../MAP1/inputs/regional_originals/`.

R2 : `R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv`, -0001/-0002 (partition méridionale), -0003 (Basse-Silésie), -0135 (Moravie); `R2_NORTHERN_CENTRAL_EASTERN_EUROPE_UNCERTAINTIES.md`, section P0; source SRC-0001. Les réserves des chercheurs ne sont pas transformées en preuves RGB.

## Luxembourg et Wallonie

### LUX-01 — Janvier, carte méridionale des Pays-Bas, notice datée 1771

[Notice et scan](https://commons.wikimedia.org/wiki/File:1771_Janvier_Map_of_Belgium_and_Luxembourg_-_Geographicus_-_BelgiumLuxembourg-janvier-1771.jpg). Fichiers : `lux_1771.html`, `lux_1771.jpg`, dérivé `lux_1771_1600.png`. Carte attribuée au sieur Janvier, publiée à Paris chez Lattré; cartouche « Partie méridionale des Pays Bas… », planche **6**. La date 1771 provient de la notice consultée; elle n'est pas présentée comme une mise à jour garantie de chaque frontière du cuivre.

**Consultation réelle :** reproduction entière, puis détail Luxembourg–Chiny–Namur–Liège. Villes lisibles, Meuse/Semois/Moselle et bandes de limites. Carte antérieure de cinq ans à la cible : utile pour situer des juridictions, insuffisante pour les rectifications de détail. La coloration ne doit pas être convertie directement en TAG. C'est une carte d'époque, non un traité ni un relevé cadastral.

### LUX-02 — Martin Uhrmacher, étude des cartes de la frontière avec Trèves

[PDF complet, 10 pages](https://anlux.public.lu/dam-assets/actualites/2016/pdf/anlux-cp-a-45-beschreibung-von-karte-und-akte.pdf); [notice des Archives nationales](https://anlux.public.lu/fr/actualites/2016/Carte.html), publiée le **20 décembre 2016**, mise à jour le 22 mars 2017. Date d'édition du PDF non indiquée; ne pas dater l'étude elle-même de 1776. Fichier `uhrmacher.pdf`; pages 2 et 3 rendues pour contrôle visuel.

Passages consultés : pp. **2–3, 5, 7–10**. L'étude distingue limites, prétentions et condominium; elle signale des négociations et règlements postérieurs à la cible. Les cartes CP-A-45/46 et le dossier A-XI-11-02 sont des pièces de **1776**, dont un document du **2 mai** : ni une notice ni l'étude ne remplacent leur scan. Le cas Pronsfeld est une juridiction partagée, pas une raison de donner toute la région à une seule puissance.

### LUX-03 — ANLux, fonds anciens et cadastre

[Fonds anciens](https://anlux.public.lu/fr/rechercher/fonds-collections/fonds-anciens.html) et [notice du cadastre de Marie-Thérèse, 4 mai 2023](https://anlux.public.lu/fr/actualites/2023/mise-en-ligne-cadastre-marie-therese.html), repris de R1 S002/S003. **Notices archivistiques seulement**, pas dépouillement des 342 dossiers A-XIV. Elles documentent les institutions et indiquent où obtenir des listes de villages de Luxembourg/Chiny; aucune frontière RGB n'est validée par ces seules notices.

### LUX-04 — Vaugondy, duché de Luxembourg, 1753

[Notice Rumsey](https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~3944~490020), atlas publié en 1757, planche 52, références 3353.052 / 3353052. **Scan non accessible dans cette session** : la réponse téléchargée `lux_notice.html` est une page de contrôle d'accès, pas le document annoncé. Notice consultable par l'outil de recherche, mais **exclue de l'ajustement et de la preuve de frontière**. Antérieure aux accords de 1769.

## Lombardie austro-vénitienne

### LOM-01 — Robert de Vaugondy, partie occidentale de la Lombardie, 1750

[Notice BnF reproduite sur Commons et scan](https://commons.wikimedia.org/wiki/File:Partie_occidentale_de_la_Lombardie_et_pays_circonvoisins_..._-_par_le_Sr_Robert_-_btv1b530425827.jpg). Identifiant BnF **btv1b530425827**, cote **GE DD-2987(5003,1)**. Fichiers `lombardy_west_1750.html`, `.jpg`, `_1600.png`. Date **1750** lue au cartouche; ne pas confondre avec la date 1757 d'un atlas contenant des tirages comparables.

Carte entière et détail Milan–Como–Bergame–Brescia–Plaisance consultés. Repères : lacs, Adda, Oglio, Pô; Gênes/Parme utilisés comme ancrages externes. Ce feuillet n'offre pas une démarcation village par village et ses limites doivent être corroborées pour 1776.

### LOM-02 — Robert de Vaugondy, partie orientale de la Lombardie, 1750

[Notice et scan](https://commons.wikimedia.org/wiki/File:Partie_orientale_de_la_Lombardie,_qui_comprend_la_république_de_Venise,_le_Mantouan,_le_Cremonese,_l%27évêché_de_Trente..._-_par_le_Sr_Robert..._-_btv1b530292980.jpg). Identifiant BnF **btv1b530292980**. Fichiers `lombardy_1750.html`, `.jpg`, `_1600.png`. Cartouche : privilège **1750**. Consultation entière et détail Crémone/Mantoue/Pô/Garda. **Pas d'ajustement affine de ce feuillet** : il fournit une lecture complémentaire, non une seconde validation indépendante des pixels.

### LOM-03 — Regione Lombardia, « Lombardia austriaca, 1749–1796 »

[Fiche institutionnelle 8000357](https://www.lombardiabeniculturali.it/istituzioni/schede/8000357/), dernière modification affichée **29 mai 2006**; fichier `lbc_8000357.html`. Page complète accessible et passages territoriaux lus : alinéa paix de 1748 et **édit du 10 juin 1757**, six provinces et terres séparées; alinéas ultérieurs datés 1786 exclus de l'état de départ. Confirme le cadre administratif habsbourgeois à la cible, sans prouver tous les contours RGB.

### LOM-04 — Regione Lombardia, Terre Ferme vénitienne

[Bergame, Brescia, Crema, XVe siècle–1797](https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.03); fichier `lbc_venice.html`. Document institutionnel rétrospectif, sans date de publication historique 1776. Sections consultées **03.03.01–03**, surtout **03.03.03.01** (enclave de Crema et strada cremasca) et 03.03.03.02 (territoire). Contrôle régional vénitien corroboré; les communes et vallées imposent une vérification locale. Correspond aux références R1 S008/S009, désormais confrontées à de véritables scans.

## Haute et Basse Silésie

### SIL-01 — Tobias Conrad Lotter, carte du duché de Silésie, 1758

[Notice et scan entier](https://commons.wikimedia.org/wiki/File:Silesia_1758.jpg); [reproduction originale téléchargée](https://upload.wikimedia.org/wikipedia/commons/2/26/Silesia_1758.jpg). Fichiers `silesia_notice.html`, `silesia_1758.jpg` (13 700 × 11 631), dérivé 1600 px. Cartouche : **1758**, Augsbourg, « Nova Mappa Geographica Totius Ducatus Silesiae Tam Superioris Quam Inferioris… ».

Consultation entière et détail Oppeln–Ratibor. Cartouche, duchés, Oder/Neisse et localités lisibles. Reproduction publique, provenance de conservation moins détaillée que les deux feuillets BnF; pas une carte de souveraineté 1776 certifiée par un dépôt d'archives. **1758 est pendant la guerre de Sept Ans** : contours de duchés et toponymie ne prouvent ni occupation ni frontières politiques finales. Le comté de Glatz a une couleur distincte sans cesser pour cela d'être prussien.

### SIL-02 — Arkadiusz Kuzio-Podrucki, étude sur les Schaffgotsch, 2022

[Article](https://zaranieslaskie.bs.katowice.pl/en/article/view/44), [PDF intégral](https://zaranieslaskie.bs.katowice.pl/en/article/download/44/18/36), **22 décembre 2022**, Zaranie Śląskie 8, pp. **9–23**, DOI 10.24917/ZaranieSlaskie.8.1. Fichier `silesia_article.pdf`, 15 pages; lecture du texte territorial **p. 19 imprimée = PDF page 11**, rendu `silesia_article-11.png`, et passages de contexte. Nouveau par rapport au seul résumé référencé en R2.

L'article situe les accords de 1742, la démarcation du **20 janvier 1743**, puis les confirmations de **1745** et **15 février 1763**. Source académique du partage durable, **pas consultation des originaux des traités ni de leurs annexes villageoises**. Cette limite est conservée pour les provinces méridionales.

## Accès insuffisants et documents à obtenir

| Document | Accès / insuffisance constatée | Ce qu'il faut encore obtenir |
|---|---|---|
| Luxembourg 1753, Rumsey | Réponse locale de contrôle d'accès; aucune carte téléchargée | Reproduction légitime; utile historiquement mais trop ancienne pour les accords 1769 |
| CP-A-45/46, ANLux | Étude détaillée lue; originaux non consultés en pleine définition | Scans et annexes A-XI-11-02, dater chaque limite avant/après janvier 1776 |
| Ferraris 1771–1777 | Corpus identifié, feuilles locales non dépouillées | Feuilles Luxembourg/Chiny/Namur/Liège, date des levés et lecture des enclaves |
| Cadastre A-XIV | Notice seulement | Listes de villages et juridictions, non simple existence du fonds |
| Gallica/IIIF, tentative lombarde | Requête rejetée HTTP 403 | Accès non contourné; scans publics BnF via Commons utilisés à la place |
| Édits/cadastres milanais et limites vénitiennes | Fiches institutionnelles et cartes générales accessibles, pas plans administratifs fins | Limites Adda/Crema et Alpes applicables après 1757 et avant 1776 |
| Démarcation silésienne 1743, annexes des traités | Étude académique consultée, annexes primaires non obtenues | Villages de Neisse/Troppau/Teschen/Glatz et limites orientales après 1772 |

Des téléchargements Python ont échoué sur les certificats de deux sites institutionnels; ils ont réussi via la chaîne TLS normale de Windows. Aucun contrôle TLS ni contrôle d'accès n'a été désactivé. Les documents non obtenus ne comptent jamais comme preuves consultées.
