# MAP‑2H — Asie du Sud-Est et Océanie, 1er janvier 1776

Intégration locale terminée. **67 RGB changent de propriétaire**, six attributions répétées sont retirées et six nouveaux TAGs sont définis. Le seul redessin concerne Hawaï : **705 pixels**, trois RGB déjà existants, sept îles connectées examinées. Aucun nouveau RGB, changement de côte ou ajout de population.

Les contrôles sont **statiques**, pas des observations dans Victoria 3. Le joueur doit lancer une nouvelle partie puis vérifier l'emploi et les marchés après un mois. MAP‑2H n'a pas été poussé. Aucun commit, merge, changement de HEAD/index du dépôt principal ou lancement du jeu.

## Corrections territoriales intégrées

| Secteur | Modification | RGB réattribués |
| --- | --- | ---: |
| Arakan | KKI → ARK, royaume de Mrauk‑U distinct avant la conquête birmane | 6 |
| Laos | Sept provinces siamoises → VIE, royaume de Vientiane | 7 |
| Viêt Nam central | Quatre provinces d'Annam DAI → TSN | 4 |
| Viêt Nam méridional | Une province du Mékong → TSN, quatorze → NGN | 15 |
| Java central | Deux provinces intérieures DEI → YOG et SRK | 2 |
| Malacca | Province côtière x8080B0 JOH → DEI | 1 |
| Nouvelle-Guinée | Province intérieure x817083 TID → PPU | 1 |
| Palaos | x6E4206 PHI → MCR ; Mariannes espagnoles méridionales conservées | 1 |
| Tasmanie | WTI continental remplacé par les communautés palawa PLW | 21 |
| Nouvelle-Zélande | Six provinces NTO → TTI au nord de l'île du Sud ; Wellington NTO → UNT | 7 |
| Hawaï | x6090C0 → HMA et xB5403E → HWA après regroupement des îles | 2 |
| **Total** | Liste exhaustive et limites dans le manifeste CSV | **67** |

Nouveaux TAGs : **TSN, NGN, PLW, TTI, HMA, HWA**. TAGs natifs réactivés : **ARK, VIE**. UNT devient un regroupement maori décentralisé ; LAN désigne les communautés minières de Mandor ; DAI représente la cour des Trịnh, et HAW l'île d'Hawaï. Toutes ces appellations ont une localisation française et anglaise. Les bannières ajoutées sont des identifiants génériques, pas des drapeaux historiques authentifiés.

### Indochine

Mrauk‑U est conservé indépendant : la conquête birmane appartient à 1784–1785. Le compte rendu d'Arakan de juin 1777 confirme la distinction politique, sans tracer les RGB du jeu. [Leider, Aséanie, introduction p.125 et commentaire du document](https://www.persee.fr/doc/asean_0859-9009_1999_num_3_1_1625).

Le Tonkin et Huế restent aux Trịnh ; les Nguyễn conservent le sud ; les Tây Sơn reçoivent une approximation de leur foyer rebelle et de leurs conquêtes attestées avant janvier 1776. La proclamation royale ultérieure de 1776, l'empire de 1778 et l'unification de 1802 ne sont pas appliqués au départ. L'autorité nominale des Lê est représentée par la cour effective des Trịnh, sans créer un second souverain superposé. Les limites des grosses provinces côtières restent approximatives. [Musée national d'histoire du Viêt Nam, Nguyễn Nhạc et les Tây Sơn, événements 1774–1775](https://baotanglichsu.vn/vi/Articles/3096/12424/nguyen-nhac-voi-vuong-trieu-tay-son.html).

Vientiane devient distinct. Les pactes de sujétion Siam → Champassak et Siam → Luang Prabang sont retirés pour ne pas anticiper les campagnes de 1778. Une alliance native Siam–Luang Prabang représente l'accord de 1774. Le pacte DAI → Cambodge est supprimé : la cour du nord ne représente plus un Viêt Nam unifié. Aucun nouveau protectorat cambodgien n'est inventé. Les franges laotiennes vietnamiennes, les districts cambodgiens déjà attribués au Siam et les principautés shans sont conservés lorsqu'une correction précise n'est pas suffisamment établie. [Larousse, division du Laos, accord de 1774 et campagne de 1778](https://www.larousse.fr/archives/grande-encyclopedie/page/7827).

### Possessions néerlandaises, Malaisie et Bornéo

Les deux provinces intérieures voisines des cours de Yogyakarta et Surakarta reviennent à ces cours. Les ports de la côte nord restent VOC. Le traité de Giyanti établit la division politique, mais ne prouve pas les contours exacts de chaque province numérique ; Mangkunegaran reste regroupé dans l'abstraction de la cour orientale. Surakarta reçoit une couleur distincte. [Archives nationales d'Indonésie, exposition Java central et traité Djocja No42/1 du 13 février 1755](https://anri.go.id/page/pameran-virtual-jawa-tengah).

Malacca néerlandaise est représentée par une province côtière existante, avec une part inévitable d'arrière-pays malais. Le nom de la subdivision néerlandaise devient **Malacca**, sans rebaptiser le Johor ou la Malaisie entière. Un niveau de port déjà présent à Batavia y est déplacé ; deux restent à Batavia. Aucun établissement britannique de Penang ou Singapour n'est ajouté. [National Library Board, Malacca sous contrôle néerlandais, 1641–1795](https://biblioasia.nlb.gov.sg/all-sections/vol-5-issue-3-oct-2009-malacca-early-european-modern-period/).

LAN ne porte plus un nom anticipant la république de Lanfang fondée en 1777 : **Communautés minières de Mandor**. Son pacte tributaire Qing et la date électorale de 1838 sont retirés. Le mécanisme républicain natif restant est une abstraction de collectif minier, pas une preuve d'une république formelle en 1776. Les sultanats et les communautés intérieures existants de Bornéo sont conservés. [Robert Y. Eng, étude sur les communautés et principautés chinoises des frontières](https://journals.gmu.edu/whc/article/view/3678/2073).

Sumatra, Sulawesi, les Moluques, Bali et Timor ont été examinés à partir de l'inventaire R6, des recherches et des locators. Aucun transfert forcé de grande province pour représenter un seul comptoir. **Bengkulu britannique reste un cas non intégré** ; la frontière fine de Timor et l'autonomie de Maubara restent ouvertes. Le locator de Dili est dans le fragment portugais et celui de Kupang dans le fragment néerlandais. Le découpage actuel n'est pas certifié comme une reproduction exacte des juridictions de 1776.

### Philippines, Papouasie et Micronésie

Le RGB litigieux **xE90347** reste uniquement Maguindanao : suppression de la revendication MND concurrente, pas transfert à l'Espagne. Trois autres répétitions internes MND et deux répétitions polynésiennes à Tahiti sont retirées. Lumad, Sulu, Maguindanao et possessions espagnoles restent distincts. Les sélecteurs de port et de bois de Mindanao sont corrigés pour correspondre aux locators physiques existants.

En Papouasie, seul le RGB intérieur **x817083** rejoint les communautés PPU. Les 33 provinces côtières et insulaires de Tidore restent une abstraction du réseau tributaire, sans prétendre à une administration territoriale uniforme. L'existence d'une colonisation néerlandaise ultérieure ne sert pas à prouver les limites précises de Tidore en 1776. [Université d'Auckland, contexte de la revendication néerlandaise de 1828](https://www.auckland.ac.nz/en/news/2020/01/03/whats-at-stake-in-west-papua.html).

Palaos rejoint les communautés locales MCR : l'administration coloniale espagnole relève de 1885–1899, pas de 1776. Les Mariannes espagnoles méridionales sont conservées. **xEF50C0**, situé dans les Mariannes septentrionales, demeure un ancien RGB terrestre sans propriétaire : aucune attribution impériale arbitraire pour combler ce trou. [Belau National Museum, période coloniale espagnole](https://palaunationalmuseum.pw/exhibits/).

### Australie, Nouvelle-Zélande et Hawaï

Les groupes australiens existants sont conservés sans colonisation britannique anticipée. La Tasmanie passe de WTI, groupe continental, à **PLW, communautés palawa décentralisées**. Ses **200 habitants hérités sont conservés**, mais constituent une insuffisance démographique connue, pas une estimation historique validée. La carte de l'AIATSIS sert de référence générale sur les peuples et ne fournit pas des frontières cadastrales de 1776. [AIATSIS, peuples d'Australie](https://aiatsis.gov.au/explore/first-peoples-australia).

Au nord de l'île du Sud, le contrôle anticipé des Ngāti Toa est remplacé par un regroupement régional **Te Tau Ihu**, sans attribuer tout le territoire à un seul iwi. Wellington rejoint le regroupement maori du Nord UNT, qui n'est plus la fédération de 1835. Les Ngāi Tahu existants du sud restent en place. [NZ History, migration de Te Rauparaha](https://nzhistory.govt.nz/people/te-rauparaha), [Te Ara, communautés de Te Tau Ihu](https://teara.govt.nz/en/te-tau-ihu-tribes), [NZ History, déclaration de 1835](https://nzhistory.govt.nz/page/declaration-independence-signed-northern-chiefs).

Hawaï comporte trois ensembles : île d'Hawaï **HAW** sous Kalaniʻōpuʻu ; Maui et Lānaʻi **HMA** ; autres îles **HWA**, regroupement décentralisé sans monarque commun inventé. Les RGB natifs mélangeaient plusieurs îles et partageaient l'île d'Hawaï : 705 substitutions entre les mêmes trois couleurs corrigent ce problème. Dimensions 8192 × 3616, mode RGB, côtes et ensemble des couleurs inchangés. Le locator de Lahaina passe sur Maui ; celui de Kailua-Kona, auparavant désactivé, devient valide sur Hawaï. La possession hawaïenne de Hana/Kauiki sur Maui en 1775 n'est pas séparée avec seulement trois RGB : limite explicitement conservée. [NPS, pouvoir de Kalaniʻōpuʻu et unification ultérieure](https://www.nps.gov/people/kamehameha-the-great.htm), [DLNR, histoire foncière de Hana](https://dlnr.hawaii.gov/wp-content/uploads/2021/01/C-1.pdf).

## Conservation des populations et de l'économie

Population mondiale **835 804 980 → 835 804 980**. Les douze State Regions affectées totalisent **8 329 443 habitants**, avant comme après. Chaque profil démographique, avec cultures, religions, statut libre/esclave, alphabétisation et qualifications explicitement écrites, est conservé mondialement et par State Region. Les répartitions internes emploient l'arrondi au plus fort reste selon les surfaces terrestres des provinces natives ; elles ne sont pas des recensements.

| Nouveau fragment ou partage | Habitants après |
| --- | ---: |
| Arakan ARK | 182 073 |
| Vientiane VIE | 151 094 |
| Annam DAI / TSN | 1 906 158 / 500 467 |
| Mékong NGN / TSN | 1 471 473 / 285 715 |
| Java central DEI / SRK / YOG | 1 100 019 / 382 859 / 172 786 |
| Malacca DEI | 22 772 |
| Papouasie PPU / Tidore | 265 161 / 61 389 |
| Micronésie MCR / PHI | 19 632 / 5 530 |
| Tasmanie PLW | 200 |
| Île du Nord UNT | 87 000 |
| Nord de l'île du Sud TTI | 12 428 |
| Hawaï HAW / HMA / HWA | 67 225 / 20 833 / 50 257 |

Les groupes chrétiens, han et autres anachronismes démographiques préexistants du Pacifique ne sont **pas convertis**. La religion d'un gouvernement peut changer sans modifier celle de ses habitants.

Tous les niveaux par type de bâtiment, PM, réserves et propriétaires économiques déclarés sont conservés. Changements nécessaires :

- Les **15 niveaux de casernes DAI du Mékong** sont répartis entre Tonkin (+8) et Annam (+7), restant DAI : **28 et 27**, total 55. Deux régions peuplées reçoivent ces capacités, pas un comptoir insulaire. Demande d'infrastructure supplémentaire théorique : +1,6 et +1,4, selon le groupe militaire natif à 0,2 par niveau.
- Un des trois niveaux routiers d'Annam dessert la nouvelle subdivision TSN ; deux restent DAI. Le propriétaire économique DAI reste inchangé.
- Les bâtiments civils déjà présents dans le sud du Mékong restent physiquement dans le sud NGN. Deux références de sièges économiques DAI deviennent Tonkin, toujours DAI.
- Un niveau de port DEI quitte Batavia pour Malacca, avec mêmes propriétaire, PM et réserve. Aucune augmentation globale de ports.

Les historiques de formations, unités, services, lieux de recrutement et commandants sont **strictement identiques**. L'inventaire ne trouve pas de groupes de combat DAI explicites dans les fichiers effectifs ; il trouve bien 55 niveaux de casernes. Cette distinction doit être vérifiée dans le jeu, dont la génération n'est pas simulée par le validateur. Aucun soldat ni formation supplémentaire créé.

## Vérifications et limites

Le validateur contrôle les propriétaires RGB exacts, la géométrie, la population et tous ses champs, les niveaux économiques et détenteurs, les unités, les capitales, les nouvelles technologies/lois référencées, les locators corrigés et les localisations. Les modèles logiques des journaux ottomans et de l'IA des infrastructures ont été réexécutés. Les fichiers protégés MAP‑2A à MAP‑2G restent identiques.

Les six répétitions pertinentes sont corrigées : **50 → 44 doubles attributions mondiales**. Les douze références orphelines héritées hors R6 ne sont pas de nouvelles régressions. Le détail et le résultat des contrôles figurent dans **MAP2H_VALIDATION.json**.

Les gouvernants Trịnh Sâm et Kalaniʻōpuʻu remplacent les modèles natifs du XIXe siècle concernés. Les autres nouveaux gouvernements organisés utilisent la génération native de dirigeants : leurs personnes ne sont pas présentées comme identifiées historiquement. Les commandes de nomenclature existantes sont préservées ; l'ajout ne nomme Malacca que dans la subdivision néerlandaise de Malaya.

La comparaison en lecture seule avec `georg3mx-map-rework` n'a trouvé aucune différence dans les scopes d'État R6 retenus. Pas de fusion globale ou remplacement de ses corrections précédentes.

### À inspecter dans une nouvelle partie

1. Mrauk‑U, Ava, Shan ; Taksin et Thonburi, trois cours laotiennes et Cambodge distinct.
2. Cour des Trịnh au Tonkin et à Huế, foyer Tây Sơn autour de Quy Nhơn, Nguyễn au sud ; casernes 28/27, routes et sièges privés.
3. Yogyakarta/Surakarta, VOC côtière, Malacca néerlandaise et ses ports ; Mandor sans tribut Qing.
4. Mindanao, Sulu, Maguindanao ; Dili/Kupang et les autorités locales conservées.
5. Intérieur papou, côte Tidore, Palaos et Mariannes méridionales.
6. Palawa, communautés maories, Hawaï/Maui/îles décentralisées ; noms, couleurs, dirigeants et bannières.
7. Après un mois : accès aux marchés, emploi, subsistance, budgets, recrutement et stabilité des pactes. Les économies à très faible population restent des risques hérités explicitement acceptés, pas des garanties de fonctionnement.

## Sauvegarde distante et nettoyage

Checkpoint **MAP‑2G validé**, retouche d'Ili incluse : [98f0c049959abb933f7472ea326093f0632027a8](https://github.com/Malzars-sys/1776-Age-of-Revolutions/commit/98f0c049959abb933f7472ea326093f0632027a8), sur `backup/1776-checkpoints`. Restauration fraîche de 5 740 fichiers, empreintes SHA‑256 correspondantes et intégrité Git vérifiées. `main` n'a pas changé.

Points distincts conservés : MAP‑2F **9383096**, MAP‑2E **49377485**, MAP‑2D validé **cb401334**, ancien MAP‑2D **0e164270** contenant les étapes A/B/C. Pas de prétention à des checkpoints A/B/C séparés reconstitués exactement.

Après restauration vérifiée, seules les copies temporaires `prepared`, `restored` et les trois fichiers de transfert `outgoing-0eeb…` ont été retirés : **5 061 517 459 octets logiques**, environ **5,06 Go**. Ces données sont récupérables depuis le checkpoint distant. Les anciens ZIPs et le workspace principal ne sont pas supprimés. Les reçus légers **BACKUP_PREREQUISITE_VALIDATION.json** et **BACKUP_TEMP_CLEANUP.json** détaillent les opérations. Aucun snapshot complet volumineux supplémentaire pour MAP‑2H.

## Livrables

**MAP2H_TERRITORIAL_CHANGES.csv** : 67 transferts et six lignes techniques de nettoyage, avec preuves et limites. **MAP2H_POPULATION_VALIDATION.csv** : 133 profils avant/après et total vérifié. **MAP2H_UNRESOLVED.csv** : 19 limites ciblées, dont Bengkulu, Timor, démographie héritée et essais natifs. Les tables ont été recalculées, perturbées puis restaurées, contrôlées cellule par cellule et rendues pour vérification visuelle conformément au skill Spreadsheets.

Les comparatifs `indochina`, `java`, `malaya`, `mindanao`, `papua`, `micronesia`, `tasmania`, `aotearoa`, `pacific` portent les suffixes `_before.png` et `_after.png`. Ce sont des rendus techniques des propriétaires et du bitmap, **pas des captures du jeu**. La photographie des pixels avant retouche est décrite dans **SUPPLEMENTAL_BASELINE.json**, avec chacune des 705 substitutions et leur inverse ; le bitmap original exact reste restaurable depuis le checkpoint GitHub MAP‑2G.
