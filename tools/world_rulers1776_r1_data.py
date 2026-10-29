"""Curated research data, not an automatic historical inference engine.

Writes only the two private research JSON files. See PLAN.md for authority/scope.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reports/characters/WORLD_RULERS_1776_R1'
SOURCES = {}
PROFILES = []

def source(key, title, url, locator, access):
    SOURCES[key] = dict(title=title, url=url, locator=locator, consulted=access)

source('WAL', 'Mark Hengerer, Waldburg, article de généalogie et histoire dynastique',
       'https://epub.ub.uni-muenchen.de/17499/1/Hengerer_Waldburg.pdf',
       'p. 1596, succession des quatre branches ; transcription research/Hengerer_Waldburg.txt, lignes 1195–1245',
       'PDF téléchargé ; paragraphes de succession lus, pas lecture intégrale des 44 pages.')
source('MAT', 'Fernando Campos, Conflitos na Dinastia Guterres através da sua cronologia, África 27/28 (2006/07), p. 23–43',
       'https://revistas.usp.br/africa/article/download/96061/95298',
       'p. 37–39, §§ 12–14 ; résumé anglais p. 42 ; research/Campos_Guterres.txt',
       'PDF téléchargé ; passages 1767–1810 et conclusion lus.')
source('KAZ', 'Giacomo Macola, The History of the Eastern Lunda Royal Capitals to c.1900 (2002)',
       'https://iris.uniroma1.it/handle/11573/1332481',
       'résumé institutionnel, période du troisième Kazembe : 1760/70–1804/5',
       'Résumé institutionnel consulté, pas le texte intégral du chapitre.')
source('KAZBIO', 'Encyclopaedia Africana, Lukwesa Ilunga',
       'https://encyclopaediaafricana.com/lukwesa-ilunga/',
       'notice, premier paragraphe et succession ; naissance vers 1740',
       'Notice accessible consultée ; datations approximatives conservées.')
source('SHW', 'Solomon Gebreyes, ʾAsfā Wasan, Beta maṣāḥǝft, Université de Hambourg (2016)',
       'https://betamasaheft.awhamburg.de/persons/PRS2110AsfaWas/main',
       'rubriques Names, Period of Activity, Dates : vers 1775–1808',
       'Passage de la notice restitué par le moteur de recherche ; ouverture directe en échec.')
source('GJM', 'Samson et Geremew, Ethiopian Journal of Social Sciences 10/1 (mai 2024)',
       'https://journals.bdu.edu.et/index.php/ejss/article/download/1800/1275/',
       'p. 102 et notes 84–88 : Hailu Yosedeq, Godjam propre dès 1759, reconnaissance élargie en 1777',
       'Passage indexé consulté. Comparé à EJSS 6/2 (2020), p. 65, qui date le pouvoir local de 1770 ; les deux couvrent 1776.')
source('KFA', 'Nordiska Afrikainstitutet, Local History of Ethiopia, Keda–Keltu Mesha (2005)',
       'https://nai.uu.se/download/18.39fca04516faedec8b248e02/1580829012619/ORTKED05.pdf',
       'entrée Käfa, paragraphe Shagi Sherocho, renvoi à Pankhurst 1997 p. 351',
       'Extrait indexé consulté : règne vers 1775–1795 et sept conseillers ; non lecture intégrale.')
source('MADK', 'Raymond K. Kent, Madagascar et les îles de l’océan Indien, Histoire générale de l’Afrique V, UNESCO, chap. 28',
       'https://unesdoc.unesco.org/ark:/48223/pf0000184394',
       'p. 944 (Boina), 946–947 (Antankarana), 948–949 (Isandra), 950 (Ambohimanga). Copie locale MADAGASCAR-02/sources/UNESCO_KENT_MADAGASCAR.txt',
       'Passages de la copie locale téléchargée lus. Les chronologies divergentes sont conservées, sans certifier les dates orales au jour près.')
source('MADA40', 'Mémoires de l’Académie malgache, fascicule XL, tableau des souverains merina',
       'https://madadoc.irenala.edu.mg/documents/10691_MAM%20FASCICULE%20XL.pdf',
       'table : Tananarive 1774–1794, Ambohimanga 1770–1787',
       'Tableau indexé consulté ; téléchargement et ouverture intégrale en échec. Ne pas prétendre avoir lu le fascicule entier.')
source('IMR', 'Bibliothèque nationale parlementaire de Géorgie, dictionnaire biographique : Solomon I, no 00018537',
       'https://www.nplg.gov.ge/bios/ka/00018537/',
       'naissance 1735 ; roi 1752–1784 ; politique envers nobles, Église et captifs',
       'Notice géorgienne indexée consultée ; ouverture directe en boucle de redirection. Corroborée par NPLG Wiki Dictionaries et une étude universitaire de 2018.')
source('ARM', 'Persian Decrees of the Matenadaran, vol. IV',
       'https://www.matenadaran.am/ftp/el_gradaran/Persian_Decrees_of_Matenadaran_vol_IV.pdf',
       'p. 123–124, note 293 et documents 1759/1763 : Husayn Ali, khan 1759–1783',
       'Passages indexés de l’édition archivistique lus ; pas lecture de tous les décrets.')
source('AZB', 'Gubalı Fethali Han ve İskender Hacınski: Azerbaycan Tarihinde Siyaset, Mücadele ve Kültür, BENGİ',
       'https://dergipark.org.tr/tr/pub/bengi/article/1769667',
       'résumé : Fathali 1736–1789, accession Quba 1758 ; analyse d’un biographe du XIXe siècle',
       'Résumé scientifique consulté, pas le texte intégral.')
source('KRB', 'George A. Bournoutian, Ebrāhīm Ḵalīl Khan Javānšīr, Encyclopaedia Iranica VIII/1 (1997), p. 71–73',
       'https://www.iranicaonline.org/articles/ebrahim-kalil-khan-javansir/',
       'premiers paragraphes : naissance 1730, succession 1760 ; autres chronologies 1763, toutes antérieures à 1776',
       'Texte de la notice ouvert et lu. Naissance 1730 retenue comme année de cette source, avec divergence signalée.')
source('SHK', 'Karim Agha Fateh, Brève histoire des khans de Chaki, chronique du XIXe siècle, traduction russe',
       'https://www.drevlit.ru/texts/k/kerim_text.php',
       'passages Muhammad Husayn, petit-fils de Haji Chalabi, règne jusqu’à sa déposition de 1780',
       'HTML de la traduction téléchargé dans research/Fateh_Sheki.html ; passages vérifiés avant installation. Chronique rétrospective, pas témoignage direct de chaque événement.')
source('SHG', 'David Brophy, “The Boundary Disputes of Villagers”: the Qing Empire and the Micropolitics of the Pamirs, Journal of Central Asian History 4 (2025), p. 1–30',
       'https://brill.com/view/journals/jcah/4/1/article-p1_1.pdf',
       'paragraphe Shah Wanji II et notes 51–52 : lettre de 1773 disant régner depuis quatre ans ; incident de 1776, p. 22',
       'Passages indexés de l’article scientifique lus ; PDF en accès direct refusé (403). Aucun prétendu dépouillement intégral des archives Qing.')
source('SEN', 'Charles Becker et Victor Martin, Kayor et Baol, royaumes sénégalais et traite des esclaves au XVIIIe siècle, Outre-Mers 62 (1975), p. 270–300',
       'https://www.persee.fr/doc/outre_0300-9513_1975_num_62_226_1832',
       'tableau 1 et p. 286–287, documents de 1773 et 1777 sur le damel-tègn Makodu Kumba Diaring',
       'Texte des passages et tableau consultés ; fin du règne 1777 ou 1778 selon les chronologies, sans effet sur janvier 1776.')
source('BND', 'Michael A. Gomez, Pragmatism in the Age of Jihad: the Precolonial State of Bundu (Cambridge, 1992), chap. 6 et annexe A',
       'https://www.cambridge.org/core/books/abs/pragmatism-in-the-age-of-jihad/structure-of-the-bundunke-almaamate/91AAA2577D1DD81A65161F3CA6D15162',
       'résumé chap. 6 : Amadi Gai 1764–1786 ; annexe A indexée dans copie universitaire',
       'Résumé éditeur lu et tableau de chronologie corrigée consulté via https://ndl.ethernet.edu.et/bitstream/123456789/18924/1/14.pdf.pdf ; téléchargement de cette copie en échec.')
source('KNN', 'H. R. Palmer, The Kano Chronicle, traduction publiée en 1908',
       'https://zenodo.org/records/2415833/files/article.pdf',
       '§ XLI, p. 92–93 : Babba Zaki, A.H. 1182–1190 / A.D. 1768–1776 ; § XLII son successeur',
       'Texte indexé des sections consulté. A.H. 1190 commence après janvier 1776 ; la transition n’est pas placée artificiellement au 1er janvier. Jour de décès non établi.')
source('NGN', 'Cục Du lịch Quốc gia Việt Nam, Trịnh–Nguyễn phân tranh',
       'https://vietnamtourism.vn/index.php/about/items/1982/1',
       'section Nguyễn Phúc Thuần (1765–1777), naissance en 1754 ; corroboration chronologie de la ville de Đà Nẵng',
       'Passage institutionnel consulté ; année seule, pas date précise. Destitution au cours de 1776 non rétroprojetée au 1er janvier.')
source('VIE', 'Edward Van Roy, Under Duress: Lao War Captives, Siamese Melting Pot (2017), p. 105–130 ; et thèse Kent State University',
       'https://www.cambridge.org/core/books/abs/siamese-melting-pot/under-duress-lao-war-captives/52843C585AEDB96558D5138C1DF16836',
       'résumé du chapitre ; notice historique de Siribunyasan, r. 1767–1778/79 dans thèse kent1305593335',
       'Résumé scientifique et passage de thèse indexés consultés. Année de début parfois 1760 ; les deux chronologies couvrent 1776. https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=kent1305593335&disposition=inline')
source('TSN', 'Lê Đình Phụng, Nguyễn Nhạc với vương triều Tây Sơn, Musée national d’histoire du Vietnam (13 septembre 2012)',
       'https://baotanglichsu.vn/vi/Articles/2001/66314/nguyen-nhac-voi-vuong-trieu-tay-son.html',
       'paragraphes révolte 1771, opérations 1773–1775, titre impérial seulement en 1778',
       'Article ouvert et lu ; distinguer chef insurgé de l’empereur futur.')
source('C81', 'Christina Welch et Niall Finneran, Chatoyer’s Punch Ladle, Journal of African Diaspora Archaeology and Heritage 11/3 (2022), p. 181–204',
       'https://www.tandfonline.com/doi/full/10.1080/21619441.2022.2096960',
       'paragraphes documents 1768, 1769 et traité 1773 ; distinction chef de Grand Sable / commandement de 1795',
       'Texte accessible des passages lu ; corroboré par estampe de 1773 conservée à la Bibliothèque nationale de Jamaïque, https://nljdigital.nlj.gov.jm/items/show/295 .')
source('HMA', 'Bishop Museum, Hawaiian-language newspapers: Timeline and Commentary',
       'https://blog.bishopmuseum.org/nupepa/timeline-and-commentary/',
       'chronologie 1776 : Kahekili à Maui, face à Kalaniopuu ; récit de Kamakau',
       'Passage de la chronologie et extraits de Kamakau consultés ; pas de naissance exacte attestée dans ces passages.')
source('TNG', 'Te Papa Tongarewa, Poulaho, King of the Friendly Islands, objet 2020-0012-3',
       'https://collections.tepapa.govt.nz/object/1870940',
       'identification Fatafehi Paulaho, Tuʻi Tonga ; rencontre du 27 mai 1777',
       'Notice muséale lue ; recoupée avec étude des royautés polynésiennes et chronologie 1770–1784. Le seul portrait de 1777 ne suffit pas à fixer une naissance.')
source('TNGCH', 'World Statesmen, Tonga ; chronologie comparée des trois dignités',
       'https://worldstatesmen.org/Tonga.html',
       'Tuʻi Tonga Fatafehi Paulaho 1770–1784, distinct du Tuʻi Kanokupolu et du Tuʻi Haʻatakalaua',
       'Liste compilée consultée comme chronologie complémentaire à la notice muséale et à la recherche sur la royauté sacrée ; âge circa1749 non adopté.')
source('CHE', 'Gerald F. Schroedl, Oconastota, Tennessee Historical Society, Tennessee Encyclopedia (2017/18)',
       'https://tennesseeencyclopedia.net/entries/oconastota/',
       'chef de Chota et dirigeant politique/militaire, actif avant et pendant 1776 ; naissance vers 1710',
       'Notice lue, recoupée avec James C. Kelly, American National Biography, DOI 10.1093/anb/9780198606697.article.2000736 (extrait, naissance vers1712, probablement Chota). Divergences conservées.')

def add(tag, name, office, tenure, fact, sources, *, birth=None, place=None, culture=None,
        religion='animist', ig='ig_landowners', ideology='ideology_traditionalist',
        traits=None, traits_basis=None, note='', female=False, age=None):
    PROFILES.append(dict(TAG=tag, full_name=name, office=office, tenure=tenure, historical_fact=fact,
        source_ids=sources.split(), birth=birth or 'Non établie dans les sources consultées',
        birthplace=place or 'Non établi dans les sources consultées', age=age, culture=culture,
        religion=religion, interest_group=ig, ideology=ideology, traits=traits or ['basic_political_operator'],
        traits_basis=traits_basis or 'Calibration de gameplay : compétence politique de base pour un titulaire établi. La source n’atteste pas un test de compétence ni un trait psychologique.',
        interest_group_basis='Rattachement de gameplay à la cour et aux élites foncières/héréditaires ; pas appartenance historique à un groupe d’intérêt de Victoria 3.' if ig=='ig_landowners' else 'Rattachement de gameplay à la fonction exercée, pas organisation historique au sens du jeu.',
        ideology_basis='Approximation de gameplay du maintien de l’autorité et de ses usages ; aucune profession de foi idéologique moderne n’est attribuée à la personne.',
        female=female, uncertainties=note, birth_date=None))

for tag,name,years,age in [
 ('SWF','Ferdinand Maria de Waldburg-Wolfegg-Wolfegg','1736',39),
 ('SWW','Gebhard Xaver de Waldburg-Wolfegg-Waldsee','1727',48),
 ('SWX','Franz Ernst de Waldburg-Zeil-Wurzach','1704',71),
 ('SWY','Franz Anton de Waldburg-Zeil-Trauchburg','1714',61)]:
    add(tag,name,'Comte régnant','Succession dynastique établie avant 1776 ; fin de vie respectivement 1779, 1791, 1781, 1790',
        'La succession publiée des branches identifie le titulaire vivant au départ.','WAL',birth=years+' (année seule)',age=age,
        culture='south_german',religion='catholic',note='Âge estimé à partir de l’année ; aucun faux anniversaire. Autorité patrimoniale, pas un nouvel État ni une nouvelle union.')
add('MTM','Francisco II Kaluete ka Mbandi','Roi de Matamba','Après le coup de 1767 ; pouvoir dans le Matamba jusqu’au début du XIXe siècle',
    'Francisco II tient Matamba, tandis que Kamana conserve un pouvoir rival dans les îles du Kwanza. Baptême catholique et mariage attestés après 1767.','MAT',
    culture='ovimbundu',religion='catholic',traits=['ambitious'],traits_basis='Interprétation de gameplay de la prise de pouvoir attestée de 1767 ; aucune qualification morale ajoutée.',
    note='Personne historiquement mbundu ; ovimbundu est le proxy culturel existant du TAG, non une identification ethnographique. Ne pas lui attribuer tout le Ndongo rival.')
add('KZM','Lukwesa Ilunga','Mwata Kazembe','Vers 1760/70–1804/05','Le troisième Kazembe est en fonction durant 1776.','KAZ KAZBIO',
    birth='Vers 1740, estimation de la notice',age=35,culture='lunda',note='Les échanges portugais de 1790–1798 ne sont pas des acquis de 1776. Numérotation et bornes du règne divergent ; identité au départ stable.')
add('SHW','Asfa Wossen','Meridazmach du Shewa','Vers 1775–1808','Succède à son père Amha Iyasus avant le départ.','SHW',culture='amhara',religion='orthodox',
    note='Pas de titre impérial ; date de naissance non établie. Les réformes de l’ensemble du règne ne sont pas déclarées déjà accomplies en 1776.')
add('GJM','Hailu Yosedeq','Dirigeant du Godjam propre','Pouvoir local daté de 1759 ou 1770 ; reconnaissance élargie en 1777',
    'Les deux datations scientifiques consultées placent Hailu au pouvoir dans le Godjam propre en 1776.','GJM',culture='amhara',religion='orthodox',
    note='Représentant dominant du noyau, pas affirmation d’une autorité uniforme sur toute la province avant 1777. Aucun autre gouverneur ni frontière modifié.')
add('KFA','Shagi Sherocho','Tato de Kaffa','Vers 1775–1795','Le règne donné par le Nordiska Afrikainstitutet couvre le départ.','KFA',culture='sidama',
    note='Sidama est le proxy existant pour les populations de Kaffa, pas une nouvelle identification de l’ethnie du souverain. Le pouvoir royal demeure limité par les conseillers ; pas de centralisation supplémentaire.')
add('BOI','Ravahiny','Reine de Boina','Vers 1767–1808','Kent identifie la souveraine durant la période.','MADK',culture='malagasy',female=True,
    note='Nom personnel et sexe attestés, naissance inconnue. Le successeur masculin du XVIIIe siècle évoqué dans certaines listes n’est pas substitué à cette reine.')
add('ATK','Lamboina','Roi antankarana','1710–1790 ou vers1750–1802 selon les traditions','Le traité de 1775 confirme l’identité malgré le télescopage des règnes oraux.','MADK',
    culture='malagasy',traits=['tactful'],traits_basis='Traduction de gameplay de la négociation attestée de 1775.',
    note='Aucune longévité légendaire ni anniversaire inventé. Pas de conversion islamique de la dynastie, postérieure au départ.')
add('ISD','Andriamanalina I','Roi d’Isandra','Du milieu du XVIIIe siècle à1790','Kent décrit le roi et son usage de la persuasion.','MADK',culture='malagasy',
    traits=['charismatic'],traits_basis='Interprétation de gameplay de l’aptitude à convaincre par l’humour rapportée par Kent.',note='Les provinces du règne entier ne sont pas de nouveaux transferts territoriaux.')
add('AVR','Andrianjafy','Roi d’Ambohimanga','1770–1787 dans le tableau ; succession finale plus précoce chez Kent',
    'Le titulaire précède Andrianampoinimerina dans les chronologies consultées.','MADK MADA40',culture='malagasy',
    note='Fin de règne contestée (1777/78 ou1787), sans effet sur le titulaire du 1er janvier1776. Aucun trait de cruauté déduit des récits de succession.')
add('MAD','Andriamboatsimarofy','Roi d’Antananarivo','1774–1794 dans le tableau de succession','Le tableau distingue ce roi des souverains d’Ambohimanga.','MADA40',culture='malagasy',
    note='Variante Andrianamboatsimarofy. Tableau consulté par indexation, fascicule intégral inaccessible ; aucun anniversaire repris de listes non recoupées.')
add('IMR','Solomon I Bagrationi','Roi d’Iméréthie','1752–1784 avec interruption1766–1768','Le roi a recouvré son pouvoir avant1776.','IMR',birth='1735 (année seule)',age=40,
    culture='georgian',religion='orthodox',traits=['persistent'],traits_basis='Interprétation de gameplay de la reconquête du trône et de l’opposition durable à la sujétion ottomane.',
    note='Aucune date précise de naissance ni lieu déduit de la capitale.')
add('ARM','Husayn Ali Khan','Khan d’Erevan','1759–1783','L’édition des décrets confirme le khan nommé en1759 et1763.','ARM',culture='azerbaijani',religion='shiite',
    traits=['basic_diplomat'],traits_basis='Compétence de base inspirée des négociations attestées avec le catholicos et les autorités voisines avant1776.',
    note='Le TAG ARM représente ici Erevan ; pas un souverain arménien de toute l’Arménie. Les accords géorgiens de1778/79 restent futurs. Religion : représentation du milieu dynastique, pas attestation d’une pratique individuelle.')
add('AZB','Fath Ali Khan','Khan de Quba','1758–1789','Le résumé scientifique donne accession et année de naissance.','AZB',birth='1736 (année seule)',age=39,
    culture='azerbaijani',religion=None,traits=['basic_diplomat','ambitious'],traits_basis='Interprétation de gameplay de la diplomatie et du projet de domination régionale étudiés par l’article.',
    note='Le TAG AZB est le noyau de Quba. Jour et lieu de naissance non confirmés ; aucun rassemblement territorial exécuté. Confession individuelle non établie dans le passage lu.')
add('KRB','Ibrahim Khalil Khan Javanshir','Khan du Karabakh','Succession1760 chez Iranica, souvent1763 ailleurs ; jusqu’en1806',
    'Les chronologies comparées le placent au pouvoir en1776.','KRB',birth='1730 chez Bournoutian ; d’autres listes donnent1732',age=45,
    culture='azerbaijani',religion=None,note='Âge estimé d’après la source retenue, incertitude de deux ans signalée. Confession individuelle non établie dans le passage vérifié, laissée au mécanisme natif.')
add('SHK','Muhammad Husayn Khan Mushtaq','Khan de Chaki','1759–1780','La chronique rétrospective identifie le dirigeant avant sa déposition de1780.','SHK',culture='azerbaijani',religion=None,
    note='Pas de naissance connue ni confession individuelle établie. Aucun poème ni trait littéraire ajouté sur la seule foi d’une notice dérivée.')
add('SHG','Shah Wanji II','Shah de Choughnan','Depuis1769, déduit d’une lettre de1773','L’article recoupe une lettre Qing et la chronique du Badakhshan.','SHG',culture='tajik',religion=None,
    traits=['basic_diplomat'],traits_basis='Compétence diplomatique minimale inspirée de la correspondance attestée de1773.',
    note='Pas de shah absolu de tous les Pamirs : Ghund a notamment un autre chef. Aucune foi individuelle déduite du proxy chiite du pays ; religion laissée au mécanisme natif. Anniversaire inconnu.')
for tag,office in [('CAY','Damel du Cayor'),('BAO','Tègne du Baol')]:
    add(tag,'Makodu Kumba Diaring Fall',office,'Au Cayor dès1766 ; union de fait des deux couronnes avant1776, fin1777/78',
        'Les documents de1773 et1777 désignent le même damel-tègn.','SEN',culture='wolof',
        note='Deux pays représentés séparément par le mod : même personne historique, deux représentations techniques. Aucune nouvelle union personnelle ni synchronisation des décès créée. Variante Macodou Coumba Diarigne Fall.')
add('BND','Amadi Gai','Dirigeant du Bundu','1764–1786','Gomez et sa chronologie corrigée couvrent le départ.','BND',culture='fulbe',religion='sunni',
    traits=['basic_diplomat'],traits_basis='Interprétation de gameplay de la politique d’accords et de contrôle commercial étudiée par Gomez.',
    note='Le titre évolue d’eliman vers almamy au cours de la période ; ne pas inventer le jour de changement.')
add('KNN','Babba Zaki','Sarkin Kano','A.H.1182–1190, soit1768–1776','La chronique place la fin du règne en1190H, après le 1er janvier1776.','KNN',culture='hausa',religion='sunni',
    traits=['basic_political_operator','charismatic'],traits_basis='Compétence politique et éloquence traduisent les qualités rapportées par la chronique ; aucune promotion au rang de général.',
    note='Babba Zaki est un nom de règne/surnom, pas un prénom civil établi. Le jour exact de succession n’est pas programmé.')
add('NGN','Nguyễn Phúc Thuần','Seigneur Nguyễn','1765–1776/77','La notice institutionnelle identifie le seigneur encore en place au départ.','NGN',birth='1754 (année seule vérifiée)',age=21,
    culture='vietnamese',religion='mahayana',
    note='Aucun faux anniversaire. La destitution de1776 ne devient pas une destitution au1er janvier. Confession bouddhiste du contexte de cour, pas preuve d’une pratique privée.')
add('VIE','Siribounyasan','Roi de Vientiane','1760 ou1767–1778/79 selon les chronologies','Les études le placent au pouvoir pendant les années1770.','VIE',culture='lao',religion='theravada',
    note='Variante Si Bunyasan / Ong Boun. Début du règne et jour de naissance non fixés ; aucune sujétion au Siam de1779 rétroprojetée.')
add('TSN','Nguyễn Nhạc','Chef de l’insurrection Tây Sơn','Chef insurgé depuis1771 ; empereur seulement en1778',
    'L’étude du musée décrit son commandement effectif en1773–1775.','TSN',culture='vietnamese',religion='mahayana',ig='ig_rural_folk',
    traits=['ambitious','basic_diplomat'],traits_basis='Prise de pouvoir et compromis avec les Trịnh avant1776 traduits en traits vanilla.',
    note='Groupe rural : base insurrectionnelle, pas origine sociale exclusive du chef, ancien marchand/collecteur. Pas de titre impérial anticipé. Naissance inconnue dans le passage vérifié.')
add('C81','Joseph Chatoyer','Chef caraïbe de Saint-Vincent','Chef attesté en1768–1773 ; actif jusqu’en1795',
    'Documents et estampe le montrent comme chef et signataire avant1776.','C81',culture='afro_caribbean',
    traits=['basic_diplomat'],traits_basis='Compétence diplomatique de base inspirée du traité de1773.',
    note='Représentant du noyau de Saint-Vincent, pas chef unique de toutes les Caraïbes ; suprématie de1795 non projetée intégralement en1776. Culture afro_caribbean : proxy existant du TAG pour Garifuna.')
add('HMA','Kahekili II','Aliʻi de Maui','Depuis1766 ; titulaire pendant1776','La chronologie du Bishop Museum le situe face à Kalaniopuu en1776.','HMA',culture='hawaiian',
    note='Ne pas prendre les futures conquêtes d’Oʻahu pour des possessions initiales ; naissance contestée dans les listes dérivées, non codée.')
add('TNG','Fatafehi Paulaho','Tuʻi Tonga','Vers1770–1784','Titulaire de la dignité sacrée, distinct des deux autres grandes dignités.','TNG TNGCH',culture='polynesian',ig='ig_devout',
    note='La représentation du roi sacré ne transforme pas Tonga en monarchie centralisée moderne. La pluralité des autorités est conservée. Naissance contradictoire dans les généalogies, omise.')
add('CHE','Oconostota','Chef de Chota et dirigeant cherokee','Autorité attestée avant1776, retrait vers1780/81',
    'La notice scientifique et les documents de1775 attestent son rôle politique et diplomatique.','CHE',birth='Vers1710 ou1712 selon les notices',age=64,
    place='Probablement Chota, d’après Kelly (ANB), non certifié au village près',culture='cherokee',
    traits=['basic_diplomat'],traits_basis='Interprétation de gameplay des négociations attestées avant1776.',
    note='Pas d’État unitaire imposé aux villes cherokees. Dates du titre de chef principal discutées ; représentant dominant, pas autorité absolue. Âge approximatif choisi au milieu des deux estimations, sans anniversaire.')

if __name__ == '__main__':
    for name, data in [('SOURCES.json',SOURCES),('CURATED_PROFILES.json',PROFILES)]:
        (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'{len(PROFILES)} country profiles; {len(SOURCES)} source records')
