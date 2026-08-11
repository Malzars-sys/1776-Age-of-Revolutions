# RULERS_1776_SOURCES

Research baseline for the **1 January 1776** starting-ruler reconstruction of the Victoria 3 mod *1776 - Age of Revolutions Fork*.

## Method
- Prefer institutional, museum, archive, national-biographical, or specialist academic references.
- Exact dates are used only when the source support is strong.
- Where reliable sources disagree or only provide an approximate year, the implementation recommendation is `age = X` rather than an invented exact `birth_date`.
- This file is historical research, not a Victoria 3 syntax reference. Codex should map culture/religion/home-region values to IDs that already exist in the mod/vanilla.

## Core sources by polity

### Great Britain — George III
- Royal Family: https://www.royal.uk/george-iii
- Royal Archives: https://www.royal.uk/royal-archives-coronation

### France — Louis XVI
- Bibliothèque nationale de France: https://catalogue.bnf.fr/ark:/12148/cb120081657.public
- Château de Versailles: https://www.chateauversailles.fr/decouvrir/histoire/grands-personnages/louis-xvi

### Spain — Charles III
- Museo del Ejército / Spanish Ministry of Defence: https://ejercito.defensa.gob.es/museo/en/HECHOS_HISTORICOS/HECHOS_HISTORICOS/01.20_enero_Nacimiento_Carlos_III.html
- PARES / Archivos Españoles: https://pares.mcu.es/ParesBusquedas20/catalogo/autoridad/46852/imprimir

### Portugal — José I
- Arquivo Nacional da Torre do Tombo: https://antt.dglab.gov.pt/exposicoes-virtuais-2/nascimento-d-jose/
- Assembleia da República: https://www.parlamento.pt/VisitaParlamento/Paginas/BiogDJose.aspx

### Russia — Catherine II
- State Russian Museum: https://virtual.rusmuseumvrm.ru/mikh_palace/collection/russkoe_iskusstvo_xviii_veka/portret_ekaterini_ii/index.php?lang=ru
- British Museum: https://www.britishmuseum.org/collection/term/BIOG22234

### Prussia — Frederick II
- University of Oxford, Frederick the Great project: https://frederick.mml.ox.ac.uk/history
- Deutsche Biographie: https://www.deutsche-biographie.de/sfz56983.html

### Habsburg Monarchy — Maria Theresa / Joseph II
- Die Welt der Habsburger, Maria Theresa: https://www.habsburger.net/en/persons/habsburg-emperor/maria-theresa
- Joseph II: https://www.habsburger.net/en/persons/habsburg-emperor/joseph-ii
- Co-regency: https://www.habsburger.net/en/chapter/joseph-ii-co-regent

### Sweden — Gustav III
- Nationalmuseum Sweden: https://collection.nationalmuseum.se/sv/artists/artist/5609/
- Encyclopædia Universalis: https://www.universalis.fr/encyclopedie/gustave-iii/

### Denmark–Norway — Christian VII
- The Royal Danish Collection: https://denkongeligesamling.dk/en/the-collection/persons/christian-vii-1749-1808/

### Polish–Lithuanian Commonwealth — Stanisław August Poniatowski
- National Museum in Krakow: https://mnk.pl/en/wystawy/stanislaw-august-poniatowski-the-enlightened-king/
- British Museum: https://www.britishmuseum.org/collection/term/BIOG144349

### Ottoman Empire — Abdülhamid I
- TDV İslâm Ansiklopedisi: https://islamansiklopedisi.org.tr/abdulhamid-i
- Larousse: https://www.larousse.fr/encyclopedie/personnage/Abd%C3%BClhamid_I_er/103767

### Qing Empire — Qianlong / Hongli
- Saint Louis Art Museum: https://www.slam.org/collection/constituents/4032/
- British Museum: https://www.britishmuseum.org/collection/term/BIOG132266
- National Palace Museum: https://www.npm.gov.tw/Exhibition-Content.aspx?l=2&sno=04014494

### Tokugawa Japan — Tokugawa Ieharu
- PBS timeline: https://www.pbs.org/empires/japan/timeline_1700.html
- Japan Reference: https://jref.com/articles/tokugawa-ieharu-1737-1786.931/

### Joseon — Yeongjo
- Academy of Korean Studies Encyclopedia: https://encykorea.aks.ac.kr/Article/E0037669
- National Museum of Korea: https://www.museum.go.kr/ENG/contents/E0202010000.do?exhiSpThemId=650179&listType=list&menuId=&schM=relic_view

### Mughal Empire — Shah Alam II
- Encyclopaedia Iranica: https://www.iranicaonline.org/articles/alam-ii-shah-mughal-emperor-1173-1253-1759-1806/
- 1911 Encyclopaedia Britannica transcription: https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Shah_Alam

### Maratha Confederacy — Madhavrao II / Regency
- Maharashtra Gazetteer, Poona history: https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Poona%20District/Poona-II/history_marathas.html

### Hyderabad — Nizam Ali Khan / Asaf Jah II
- Chowmahalla Palace: https://www.chowmahalla.in/faqs/hh-asaf-jah-ii/

### Mysore — Hyder Ali
- British Museum: https://www.britishmuseum.org/collection/term/BIOG10364
- EBSCO Research Starter: https://www.ebsco.com/research-starters/history/hyder-ali

### Persia — Karim Khan Zand
- Encyclopaedia Iranica: https://www.iranicaonline.org/articles/karim-khan-zand/
- British Museum, Zand dynasty: https://www.britishmuseum.org/collection/term/x113402

### Dutch Republic — William V
- Royal House of the Netherlands: https://www.royal-house.nl/topics/history/stadholders/prince-william-v-1748-1806
- Rijksmuseum: https://www.rijksmuseum.nl/en/collection/object/Stadtholder-Prince-William-v--9b3966d0a022d2977695f7281a1cc4c6

### Naples and Sicily — Ferdinand
- BnF authority record: https://catalogue.bnf.fr/ark:/12148/cb119567368.public
- British Museum: https://www.britishmuseum.org/collection/term/BIOG69450

### Montenegro — Sava Petrović
- Montenegrina cultural-history source: https://montenegrina.net/okf-i-pobjeda-nova-knjiga-vladimira-jovanovica-crnogorska-pravoslavna-crkva-i-vaseljena-1766-1925/
- Government of Montenegro historical-statehood discussion: https://www.gov.me/clanak/20662--11082

## Known uncertainty flags
- **Shah Alam II**: exact June 1728 birth day conflicts across secondary references. Use `age = 47`.
- **Hyder Ali**: birth is generally given circa 1720, with some references giving 1722. Use documented approximate age.
- **Karim Khan Zand**: Iranica gives birth circa 1705. Use documented approximate age.
- **Sava Petrović**: identity is suitable for 1776, but exact date evidence is weaker in this first-pass packet. Keep confidence MEDIUM and use approximate age.
- **Madhavrao II**: historical identity is certain, but the polity is a genuine child-ruler/regency case. Do not erase the regency complexity merely to avoid a child portrait.
