"""MAP-1B report-only qualification. Never writes MAP1 or game runtime files."""
from pathlib import Path
import csv, json, subprocess
import xml.etree.ElementTree as ET
from PIL import Image
from map1_prepare import protected, digest, GAME, EXPECTED

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'docs/reports/map/MAP1'
OUT=ROOT/'docs/reports/map/MAP1B'
E=OUT/'MAP1B_GEOGRAPHIC_EVIDENCE'
def table(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def writecsv(p,rows,fields):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

# Individual reading of diagnostic overlays, not automated sovereignty assignment.
# A named town/district identifies a historical reference, NOT the entire RGB.
notes={
 'lux':{
 'x2D32D7':('Habsbourg / principauté de Liège : secteurs à départager','Charleroi et abords de Namur; polygone traversant plusieurs limites colorées','Limites de Hainaut, Namur et Liège autour de Charleroi; feuilles Ferraris avec juridictions.'),
 'x3A5FB9':('Habsbourg; Bouillon et Liège à distinguer','Saint-Hubert, Chiny et Semois dans le voisinage diagnostique','Frontière Chiny–Bouillon, villages et enclaves; cadastre A-XIV et feuilles Ferraris locales.'),
 'x5180A0':('Habsbourg : duché de Luxembourg, étendue RGB non établie','Arlon/Bastogne au nord de Luxembourg-ville','Limites nord et orientales du duché et changements 1769; Ferraris et clauses territoriales de 1769.'),
 'x8080A0':('Hainaut habsbourgeois, frange occidentale non attribuée','Hainaut occidental; bord de la fenêtre de comparaison','Limite Hainaut–France et enclaves; Ferraris/accord 1769, pas frontière belge actuelle.'),
 'x916574':('Habsbourg / principauté de Liège à départager','Namur/Dinant; Meuse et territoires imbriqués','Villages de Namur et Liège sur les deux rives; feuilles Ferraris avec limites politiques.'),
 'xB0A0C0':('Hainaut habsbourgeois, couverture RGB non établie','Mons et Hainaut; extrémités du polygone','Limites administratives locales et franges françaises; Ferraris local.'),
 'xD001A0':('Habsbourg : duché de Luxembourg, pas souveraineté LUX indépendante','Luxembourg-ville; 47 pixels, boîte 9 × 8 pixels','Le RGB entier tient-il dans le duché au 01-01-1776? Ferraris local + traité 1769; choix distinct du statut jouable LUX.'),
 'xEF2040':('Liège / Habsbourg / autres autorités ardennaises à départager','Liège, Huy, Durbuy et La Roche; polygone multi-juridiction possible','Limites de Liège/Namur/Luxembourg et Stavelot; atlas politique documenté et Ferraris local.')},
 'lombardy':{
 'x3F1E38':('Habsbourg à Como; limites alpines non attribuées','Como et lacs, prolongement septentrional','Séparer Como et territoires suisses; carte de districts de 1757 et limite alpine.'),
 'x4713EE':('VEN à Brescia; AUS à Crémone; totalité RGB non attribuée','Brescia–Crémone, Oglio; recoupe plusieurs territoires dans le diagnostic','Tracer frontière Brescia–Crémone et enclaves; cadastre milanais/Carte des districts antérieure à 1776.'),
 'x50C060':('Mantouan habsbourgeois à vérifier pour ce RGB','Bord oriental de la carte occidentale; feuillet oriental nécessaire','Alignement local du feuillet oriental sur Mantoue, Vérone et Pô; frontière Mantoue–Ferrare.'),
 'x70B8A9':('Habsbourg à Mantoue; franges non attribuées','Mantoue/Bozzolo et Pô','Frontières du Mantouan avec Venise et Parme; feuillet oriental à géoréférencer localement.'),
 'x867A90':('VEN à Bergame; extension septentrionale non attribuée','Bergame et vallées; Adda, Iseo; grande emprise alpine','Territoire des vallées bergamasques/brescianes et bord nord; carte administrative vénitienne, district par district.'),
 'x9AC196':('NON ÉTABLIE; aucune identification à Mantoue','79 pixels; ancre au-dessus du cadre cartographique occidental','Carte alpine couvrant ce polygone et raccordement indépendant. Ne pas attribuer ce RGB à Mantoue sur son TAG.'),
 'xA40CE9':('NON ÉTABLIE pour le polygone entier','Lacs et Valtellina; plusieurs juridictions possibles','Carte administrative Valtellina/Grisons/Como datée pour 1776; comparaison locale.'),
 'xD04060':('Habsbourg : noyau milanais/pavesan','Milan–Pavie; à l’ouest du domaine vénitien principal','Vérifier bord oriental sur Adda et enclave de Crema; plan cadastral/administratif du Milanais, pas divisions de 1786.')},
 'silesia':{
 'x1B72C9':('NON ÉTABLIE; Silésie / Lusace / Brandebourg à distinguer','Bord nord-ouest; polygone sortant des limites silésiennes dessinées','Carte politique Silésie–Lusace–Brandebourg après 1763, annexes territoriales locales.'),
 'x272E48':('NON ÉTABLIE; Lusace et Silésie à distinguer','Görlitz et marge occidentale; écart de contrôle 9,429 pixels','Carte politique de Lusace en 1776 et frontière avec Silésie; ne pas projeter la situation après 1815.'),
 'x5E9091':('PRU / Habsbourg à départager','Rybnik–Teschen, bord de la partition méridionale','Démarcation 1743 et confirmation 1763, villages de la frontière; meilleur calage local requis.'),
 'x614121':('NON ÉTABLIE; pas automatiquement PRU','Emprise occidentale hors de la zone détaillée de Silésie','Carte politique de Lusace datée avant 1776 et feuille de raccordement géographique.'),
 'x6E617F':('Prusse : noyau de Breslau','Breslau et intérieur de Basse-Silésie; Oder','Contrôle indépendant local supplémentaire au nord/est; annexes de 1763 pour exclure toute enclave.'),
 'x71E080':('Habsbourg à Teschen; totalité RGB non établie','Teschen, partie méridionale; géométrie MORAVIA, écritures AUS|PRU','Frontière de Teschen village par village et calage méridional; corriger scope seulement après arbitrage propriétaire.'),
 'x732DC0':('Prusse à Glogau; frange nord non attribuée','Glogau et frontière septentrionale de Silésie','Carte politique nord-silésienne après 1763, limite avec territoires voisins; contrôle Glogau 6,632 pixels.'),
 'x7B2F62':('PRU / Habsbourg / autorité orientale à départager','Gleiwitz–Pless et bord oriental','Frontière Pless–Teschen et limite orientale après 1772; source locale applicable au 01-01-1776.'),
 'x821F52':('Prusse au centre; bord oriental non attribué','Lublinitz/Beuthen, bord de Silésie','Limite orientale de Haute-Silésie après 1772; villages et enclaves, contrôle indépendant.'),
 'x88194B':('PRU / Habsbourg à départager','Neisse/Nysa et marge sud','Partage du duché de Neisse dans les annexes 1742/1743 confirmées en 1763.'),
 'x9061E0':('Habsbourg dans le secteur de Teschen; emprise entière non établie','Teschen/Bielsko, déborde la carte; géométrie WEST_GALICIA','Carte locale après partition de 1772 et définition frontière Teschen/Galicie; scope UPPER_SILESIA erroné ≠ preuve souveraineté.'),
 'x90B12B':('Prusse à Oppeln; totalité RGB non établie','Oppeln, Oder, large polygone de Haute-Silésie','Contrôle indépendant à l’est et carte des limites politiques post-1763/post-1772.'),
 'x94D624':('Prusse dans la Silésie intérieure; frange ouest non attribuée','Sagan/Hirschberg et bord lusacien','Limite Lusace–Silésie et piémont; carte administrative politique datée.'),
 'xAF9F20':('PRU / Habsbourg à départager','Ratibor, Troppau; bord de la partition','Démarcation Oder/Opava de 1743, villages frontaliers; calage méridional amélioré.'),
 'xC00121':('PRU à Glatz; Habsbourg aux marges sud à distinguer','Glatz et piémont de Neisse; couleurs ≠ souveraineté','Frontière du comté de Glatz et duché de Neisse selon annexes de 1743/1763.'),
 'xC108EA':('Prusse : noyau de Liegnitz','Liegnitz et intérieur de Basse-Silésie','Contrôle local indépendant supplémentaire et exclusion des enclaves; les contours entiers restent proposés.'),
 'xCE74AB':('Prusse dans le piémont intérieur; totalité RGB non établie','Schweidnitz et montagnes','Limite Silésie–Bohême et enclaves; source administrative confirmée après 1763.'),
 'xF0E080':('PRU / Habsbourg à départager','Troppau et Neisse, géométrie MORAVIA, écritures AUS|PRU','Démarcation sud-Silésie 1743/1763 et contrôle méridional; doublon moteur à traiter séparément.')}
}
proposed={'xD04060':'AUS','x6E617F':'PRU','xC108EA':'PRU'}
fields=['Dossier_ID','Province_ID','State_ID','Current_Owner_TAGs','Ownership_History_State_IDs','Historical_Authority_1776_01_01','De_Jure_Assessment','Effective_Control_Assessment','Claims_Assessment','Proposed_Owner_TAG','Sources_And_Pages','Source_URLs','Geographic_Proof','Geographic_Reading','Confidence','Technical_Method','Remaining_Uncertainty','Document_Needed','Proposed_Decision','Mapping_Status','Apply_To_Mod','Approved_By_User']
base=table(OLD/'MAP1_BASELINE_PROVINCE_INDEX.csv')
urls={
 'lux':'https://commons.wikimedia.org/wiki/File:1771_Janvier_Map_of_Belgium_and_Luxembourg_-_Geographicus_-_BelgiumLuxembourg-janvier-1771.jpg | https://anlux.public.lu/dam-assets/actualites/2016/pdf/anlux-cp-a-45-beschreibung-von-karte-und-akte.pdf',
 'lombardy':'https://commons.wikimedia.org/wiki/File:Partie_occidentale_de_la_Lombardie_et_pays_circonvoisins_..._-_par_le_Sr_Robert_-_btv1b530425827.jpg | https://www.lombardiabeniculturali.it/istituzioni/schede/8000357/ | https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.03',
 'silesia':'https://commons.wikimedia.org/wiki/File:Silesia_1758.jpg | https://zaranieslaskie.bs.katowice.pl/en/article/download/44/18/36'}
refs={'lux':'LUX-01, planche 6, carte entière et secteur Luxembourg–Chiny; LUX-02, PDF pp. 2–3,5,7–10 (étude, pas scans CP-A-45/46)', 'lombardy':'LOM-01, feuillet occidental, carte entière et secteur Milan–Adda; LOM-02, feuillet oriental, secteur Mantoue; LOM-03, alinéas 1748/édit 10-06-1757; LOM-04, sections 03.03.01–03 et 03.03.03.01', 'silesia':'SIL-01, carte entière, toponymes et limites de duchés; SIL-02, p. imprimée 19 = PDF 11/15, section Rok 1742'}
rows=[]
metrics=json.loads((E/'ALIGNMENT_METRICS.json').read_text())
for case,case_notes in notes.items():
    legend=table(E/(case+'_overlay_legend.csv'))
    assert set(case_notes)=={r['Province_ID'] for r in legend}
    summary=[]
    for l in legend:
        pid=l['Province_ID']; authority,reading,need=case_notes[pid]
        b=[r for r in base if r['Province_ID']==pid]
        assert {r['Owner_TAG'] for r in b}==set(l['Current_Owners'].split('|'))
        prop=pid in proposed
        uncertainty=f"Diagnostic affine; contrôle maximal {metrics[case]['check_max_game_px']} pixels jeu, lecture source ±5 pixels non statistique; aucune frontière historique vectorisée. " + need
        r=dict(zip(fields,['']*len(fields)))
        r.update(Dossier_ID={'lux':'MAP1-P0-001','lombardy':'MAP1-P0-002','silesia':'MAP1-P0-003'}[case],Province_ID=pid,State_ID=l['State_ID'],Current_Owner_TAGs=l['Current_Owners'],Ownership_History_State_IDs='|'.join(sorted({s for q in b for s in q['Ownership_History_State_IDs'].split('|')})),Historical_Authority_1776_01_01=authority,De_Jure_Assessment='Établi au noyau nommé seulement; non démontré pour tous les pixels',Effective_Control_Assessment='Autorité civile régionale corroborée au noyau; contrôle de chaque village non vérifié',Claims_Assessment='Revendications non assimilées à la propriété; limites/disputes locales à consulter',Proposed_Owner_TAG=proposed.get(pid,''),Sources_And_Pages=refs[case],Source_URLs=urls[case],Geographic_Proof=f'MAP1B_GEOGRAPHIC_EVIDENCE/{case}_historical_overlay.png; {case}_detail.png; {case}_overlay_legend.csv, label {l["Label"]}; {case.upper()}_READING.md',Geographic_Reading=reading,Confidence='MEDIUM_CORE_LOW_BOUNDARY' if prop else 'UNRESOLVED_WHOLE_POLYGON',Technical_Method='A_EXISTING_PROVINCES' if prop else 'UNDETERMINED',Remaining_Uncertainty=uncertainty,Document_Needed=need,Proposed_Decision='CONSERVER_PROPOSÉ' if prop else 'SUSPENDRE',Mapping_Status='MAPPING_PROPOSED' if prop else 'MAPPING_REQUIRED',Apply_To_Mod='NO',Approved_By_User='NO')
        rows.append(r)
        l['Historical_Status']=r['Mapping_Status']
        summary.append(f'| {l["Label"]} | {pid} | {l["Current_Owners"]} | {reading} | {r["Proposed_Decision"]} | {need} |')
    intro=(E/(case.upper()+'_READING.md')).read_text(encoding='utf-8')
    # Deterministic replacement of generated table, never append duplicate tables.
    intro=intro.split('<!-- PER_PROVINCE_TABLE -->')[0]
    (E/(case.upper()+'_READING.md')).write_text(intro+'<!-- PER_PROVINCE_TABLE -->\n\n| Repère | RGB | Écritures actuelles | Lecture géographique (diagnostic) | Décision | Preuve supplémentaire nécessaire |\n|---|---|---|---|---|---|\n'+'\n'.join(summary)+'\n',encoding='utf-8')
    writecsv(E/(case+'_overlay_legend.csv'),legend,list(legend[0]))
assert len(rows)==34 and len({r['Province_ID'] for r in rows})==34
# Required VERIFIED register is intentionally EMPTY, not a misleading proposed list.
writecsv(OUT/'MAP1B_VERIFIED_PROVINCES.csv',[],fields)
writecsv(OUT/'MAP1B_UNRESOLVED.csv',rows,fields)

# Provenance for all evidence (including explicitly rejected access-wall content).
provenance=[]
for p in sorted(E.iterdir()):
    if not p.is_file() or p.name=='EVIDENCE_SHA256.csv': continue
    provenance.append({'File':p.name,'Bytes':p.stat().st_size,'SHA256':digest(p)})
writecsv(E/'EVIDENCE_SHA256.csv',provenance,['File','Bytes','SHA256'])

before=json.loads((OUT/'MAP1B_RUNTIME_BEFORE.json').read_text(encoding='utf-8'))
assert before==protected(), 'STOP: runtime changed'
assert digest(GAME/'map_data/provinces.png')==EXPECTED
oldhashes=table(OLD/'MAP1_DELIVERABLE_HASHES.csv')
for r in oldhashes:
    p=OLD/r['File']; assert p.is_file() and digest(p)==r['SHA256'], 'MAP1 changed: '+r['File']
for name in ['lux','lombardy','silesia']:
    for suffix in ['_historical_overlay.png','_detail.png']:
        with Image.open(E/(name+suffix)) as im: im.verify()
for r in rows:
    assert r['Apply_To_Mod']=='NO' and r['Approved_By_User']=='NO'
    assert r['Technical_Method']!='C_GEOMETRY'
    assert (E/(next(k for k in notes if r['Province_ID'] in notes[k])+'_overlay_legend.csv')).is_file()
for sid in ['STATE_WALLONIA','STATE_LOMBARDY','MAP1-P0-003']:
    ET.parse(OLD/'MAP1_GEOGRAPHIC_EVIDENCE/STATE_ATLAS'/(sid+'.svg'))
for name,expected in [('MAP1B_VERIFIED_PROVINCES.csv',0),('MAP1B_UNRESOLVED.csv',34)]:
    assert len(table(OUT/name))==expected
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:
        assert all(len(r)==len(fields) for r in csv.reader(f))
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head=='c891b1d9bb2a21bc42409acbdccc268518110260'
required=['MAP1B_HISTORICAL_SOURCES.md','MAP1B_TECHNICAL_METHOD.md','MAP1B_EXECUTIVE_SUMMARY.md','MAP1B_VERIFIED_PROVINCES.csv','MAP1B_UNRESOLVED.csv']
assert all((OUT/p).is_file() for p in required)
validation={'Date':'2026-10-10','Scope_Dossiers':3,'Unique_RGBs':34,'Verified':0,'Proposed':3,'Mapping_Required':31,'Admissible_Transfers':0,'Administrative_State_Scope_Anomalies':['x71E080','xF0E080','x9061E0'],'Runtime_Files_Unchanged':len(before),'MAP1_Manifest_Entries_Unchanged':len(oldhashes),'Bitmap_SHA256':EXPECTED,'HEAD_Unchanged':head,'CSV_Columns':len(fields),'CSV_Unique_RGB_Check':'PASS','Existing_SVGs_Parsed_Read_Only':3,'Lower_Silesia_Geometry_Source':'Existing MAP1 exact RLE; no existing dedicated Lower Silesia SVG','Overlay_PNGs_Verified':6,'In_Game_Test':'NOT_RUN_REPORT_ONLY','Historical_Whole_Polygon_Verification':'NOT_ESTABLISHED','Commit_Merge_Push':'NOT_PERFORMED'}
(OUT/'MAP1B_VALIDATION.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(validation,indent=2,ensure_ascii=False))
