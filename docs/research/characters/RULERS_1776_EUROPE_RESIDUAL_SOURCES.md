# RULERS_1776_EUROPE_RESIDUAL_SOURCES

Research baseline for the **remaining active European polities on 1 January 1776** after CLEANUP-2B-1 and CLEANUP-2B-2.

The packet covers **20 rows**:
- the 19 active European tags still receiving engine-generated rulers in CLEANUP-2B-2.5;
- `IREK`, the sole scripted-but-unverified shared-monarch case.

## Method

Institutional archives, national/regional biographies, parliamentary history and specialist reference works were preferred. Exact dates are used only where sufficiently supported. Year-only or uncertain chronology is deliberately encoded as an approximate `age`, not a fabricated birthday.

Four fork tags (`ANH`, `HOH`, `NAS`, `SCW`) are historical abstractions whose exact local meaning must be resolved from the fork before implementation. Three tags (`CRI`, `LUX`, `UBD`) are map-sensitive, but their historical research is included now so they are not forgotten.

## German dynastic / territorial cases

### ANH — Anhalt
Landesarchiv Sachsen-Anhalt confirms that Anhalt was divided into the principalities of Bernburg, Dessau, Köthen and Zerbst:
https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=190133

Leopold III Friedrich Franz of Anhalt-Dessau:
https://www.deutsche-biographie.de/sfz68642.html

Born 10 August 1740; Prince in 1776 (only Duke from 1807). Use him only if local fork evidence shows `ANH` means Anhalt-Dessau. If the tag is a combined Anhalt abstraction, do not pretend the four principalities were historically united.

### HOH — Hohenzollern
LEO-BW, Karl Friedrich of Hohenzollern-Sigmaringen:
https://www.leo-bw.de/detail/-/Detail/details/PERSON/wlbblb_personen/131601458/Hohenzollern-Sigmaringen%2BKarl%2BFriedrich%3B%2BF%C3%BCrst%2Bvon

Born 9 January 1724; Prince 1769–1785. Candidate only if `HOH` maps to Sigmaringen; Hohenzollern-Hechingen was a separate polity.

### NAS — Nassau
Deutsche Biographie, Karl Wilhelm of Nassau-Usingen:
https://www.deutsche-biographie.de/sfz39944.html

Born 9 November 1735; succeeded his father in government in 1775. Candidate only if `NAS` means Nassau-Usingen; Nassau-Weilburg also existed.

### SCM — Schaumburg-Lippe
Deutsche Biographie, Wilhelm Friedrich Ernst:
https://www.deutsche-biographie.de/sfz85621.html

Born 24 January 1724; Count of Schaumburg-Lippe and territorial ruler. Direct recommendation: age 51, **Count**.

### SCW — Schwarzburg
Residenzschloss Heidecksburg ruler chronology:
https://www.heidecksburg.de/historie/regenten/
https://www.heidecksburg.de/en/palace_complex/regents/

Ludwig Günther II (1708–1790) ruled Schwarzburg-Rudolstadt from 1767 to 1790. Candidate only if `SCW` maps to Rudolstadt; Schwarzburg-Sondershausen was separate. Use `age = 67`, not a fabricated exact birthday.

### WLD — Waldeck-Pyrmont
Niedersächsische Personen:
https://personen.niedersaechsische-bibliographie.de/person/gnd/102035202/

Deutsche Biographie:
https://www.deutsche-biographie.de/gnd102035202.html

Friedrich Carl August was born 25 October 1743 and was Prince of Waldeck and Pyrmont. Direct recommendation: age 32, Prince.

## Free cities / collective republican executives

### HAM — Hamburg
Deutsche Biographie, Nicolaus Schuback:
https://www.deutsche-biographie.de/sfz79265.html

Born 18 February 1700; Mayor from 1754 and Generalissimus from 1774. Use him as a single-character Victoria 3 abstraction of Hamburg's collective republican executive. Preserve republican laws.

### BRE — Bremen
Staats- und Universitätsbibliothek Bremen, Hermann von Line's 1773 accession:
https://brema.suub.uni-bremen.de/suubcasual/content/titleinfo/3697924

SuUB records the 28 November 1776 succession by Daniel Tidemann:
https://brema.suub.uni-bremen.de/suubcasual/name/list?alpha=t

SuUB person index gives Hermann von Line's birth year as 1705:
https://brema.suub.uni-bremen.de/suubcasual/name/list?alpha=l

Therefore Hermann von Line is a valid mayor on 1 January 1776. Use `age = 70`; preserve the free-city republican structure.

### FRM — Frankfurt
Frankfurter Patriziat, mayors by year:
https://www.frankfurter-patriziat.de/node/26911

The 1776 row lists Hieronymus Maximilian von Glauburg and Johann Christian Lucius. Use Hieronymus Maximilian as the single `Älterer Bürgermeister` / Senior Mayor abstraction. Exact birth date is not secure in this packet; use `age = 60`. Do not confuse him with Johann Hieronymus von Glauburg (1654–1727).

### LUB — Lübeck
Official Lübeck city page:
https://www.luebeck.de/de/presse/pressemeldungen/view/117538

Mayor chronology:
https://dewiki.de/Lexikon/L%C3%BCbecker_B%C3%BCrgermeister

Bernhard von Wickede was Mayor from 1773 and died in 1776. Use `age = 70`, preserve republican laws. The fork's current Swedish puppet relation is outside this character phase.

## Switzerland

### SWI — Old Swiss Confederacy
Deutsche Biographie, Johann Konrad Heidegger:
https://www.deutsche-biographie.de/sfz27368.html

Historical Dictionary of Switzerland material reflecting the old `Vorort` concept:
https://hls-dhs-dss.ch/fr/articles/016467/

Heidegger became Mayor of Zürich in 1768 and Deutsche Biographie describes him as standing at the head of Zürich and indirectly Switzerland. He is therefore a reasonable **Victoria 3 abstraction**, not a historical “President of Switzerland”. Use title `Bürgermeister of Zürich (Vorort)` / `Bourgmestre de Zurich (Vorort)` and approximate `age = 65`.

## Italy

### LUC — Republic of Lucca
Archivio di Stato di Lucca / SIAS:
https://sias-archivi.cultura.gov.it/cgi-bin/pagina.pl?Chiave=90097&RicProgetto=as-lucca&TipoPag=prodente

Archival fonds:
https://sias-archivi.cultura.gov.it/cgi-bin/pagina.pl?Chiave=423720&RicProgetto=as-lucca&TipoPag=comparc

The `Collegio degli anziani` was the executive of the Republic until 1799. Ten Anziani served two-month terms and one was selected rotationally as `Gonfaloniere di giustizia`.

Targeted research did **not** establish the exact Gonfaloniere on 1 January 1776 with sufficient confidence. The correct historical solution is therefore:
- restore republican/oligarchic government;
- use title `Gonfaloniere di Giustizia`;
- **do not invent a named officeholder**;
- allow a procedural officeholder and document it as historically justified by the very short rotating office.

## Habsburg crown lands and dependencies

### BEO — Austrian Netherlands
Deutsche Biographie, Charles Alexander of Lorraine:
https://www.deutsche-biographie.de/sfz70325.html

Born 12 December 1712; Governor/Statthalter of the Netherlands, died 1780. Use him as visible Governor-General while Maria Theresa remains sovereign and `BEO -> AUS` remains a crown land.

### HUN — Kingdom of Hungary
Magyar Nemzeti Levéltár:
https://mnl.gov.hu/mnl/ol/hirek/idegen_herceg_a_magyar_helytartoi_szekben

Maria Theresa appointed Albert Casimir as governor/lieutenant after the Palatine's death; he entered Pressburg in January 1766. Born 11 July 1738. Use age 37 and a delegated title such as Royal Governor/Lieutenant (`Helytartó`), not King.

### TRS — Transylvania
Deutsche Biographie, Samuel von Brukenthal:
https://www.deutsche-biographie.de/sfz5996.html

Born 26 July 1721. The biography states that in **1774** he became royal plenipotentiary commissioner and president of the Transylvanian Gubernium, and only **three years later** became actual Governor. Therefore on 1 January 1776 use a pre-governor title such as `President of the Gubernium / Imperial Plenipotentiary Commissioner`, age 54.

### GAL — Galicia and Lodomeria
Deutsche Digitale Bibliothek, Heinrich Joseph Johann von Auersperg:
https://www.deutsche-digitale-bibliothek.de/person/gnd/122020545

Iryna Vushko, *The Politics of Cultural Retreat: Imperial Bureaucracy in Austrian Galicia, 1772–1867*, Yale University Press:
https://yalebooks.yale.edu/book/9780300207279/the-politics-of-cultural-retreat/

Birth: 24 June 1697. Specialist scholarship places Auersperg in the Galician governorship in 1774–1780. Use age 78, Governor; Maria Theresa remains sovereign.

### LUX — Luxembourg
Official Luxembourg history:
https://luxembourg.public.lu/en/society-and-culture/history/400-ans-occupation.html

Luxembourg Government on modern sovereign statehood:
https://gouvernement.lu/content/gouvernement/en/systeme-politique.html

In the eighteenth century Luxembourg belonged under Austrian Habsburg rule within the southern/Austrian Netherlands framework. The fork currently represents it as a separate independent monarchy; this is a map/setup issue.

Recommendation: `MAP_REWORK_DEFERRED`. Do not create a fake independent 1776 dynasty.

## Black Sea / Baltic

### CRI — Crimean Khanate
TDV İslâm Ansiklopedisi, Şahin Giray:
https://islamansiklopedisi.org.tr/sahin-giray

Numista ruler authority:
https://en.numista.com/catalogue/ruler.php?id=1870

TDV establishes that Devlet Giray replaced Sahib Giray and that Şahin Giray was recognised as Khan only in January 1777 after Russian intervention. Devlet IV Giray's second reign is 1775–1777. Authority data gives birth year 1728; use `age = 47`, not an exact date.

Implement ruler/title only. Do not alter borders, subject status, Russia/Ottoman diplomacy or state ownership.

### UBD — Russian Baltic abstraction
Deutsche Digitale Bibliothek, George Browne:
https://www.deutsche-digitale-bibliothek.de/person/gnd/136490611

Baltic provincial chronology cross-check:
https://www.historyfiles.co.uk/KingListsEurope/EasternBaltics.htm

George Browne was born 15 June 1698 and served as governor/general-governor in the Russian Baltic provinces. The fork `UBD` polity itself is an anachronistic map abstraction.

If technically safe without implying sovereignty, Browne may be used temporarily as `Governor-General of Livonia and Estonia`, age 77. Otherwise defer the character together with the map representation. Never make Browne a monarch.

## Ireland verification

### IREK — Kingdom of Ireland
UK Parliament, key dates:
https://www.parliament.uk/about/living-heritage/evolutionofparliament/legislativescrutiny/parliamentandireland/key-dates/

UK Parliament, eighteenth-century constitutional relations:
https://www.parliament.uk/about/living-heritage/evolutionofparliament/legislativescrutiny/parliamentandireland/overview/meeting-irelands-terms/

Ireland retained its own Parliament while sharing the Crown; before 1782 British legislative supremacy was asserted. Use the same George III already scripted for Great Britain through the personal union; create no duplicate Irish George III.

The audit also found `activate_law = law_type:state_religion`. This is a **technical Victoria 3 question**, not a historical one. Codex must compare local 1.13 law IDs and fix it only if the intended valid key is unambiguous.

## Source-quality flags

- `FRM`: 1776 office-holder identification is strong; age is deliberately approximate.
- `LUB`: office is supported; exact birthday is deliberately not encoded.
- `CRI`: ruler chronology is strong; age uses year-only secondary authority data.
- `GAL`: identity/date are strong; office chronology comes from specialist scholarship.
- `UBD`: George Browne is historically grounded; the fork polity is not.
- `LUC`: constitution is high-confidence; exact 1 January officeholder is unresolved and must not be invented.
