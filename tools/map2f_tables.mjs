import fs from 'node:fs/promises';
import { Workbook } from 'file:///C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const out=new URL('../docs/reports/map/MAP2F/',import.meta.url);
const data=JSON.parse(await fs.readFile(new URL('TABLE_DATA.json',out),'utf8'));
const plan=JSON.parse(await fs.readFile(new URL('PLAN.json',out),'utf8'));
const geo=JSON.parse(await fs.readFile(new URL('GEOGRAPHY.json',out),'utf8'));
const local='docs/reports/map/MAP1/inputs/regional_originals/R4_SOUTH_ASIA_RECOMMENDATIONS.csv';
const sources={
 STATE_BOMBAY:'https://mumbaicity.gov.in/en/history/; https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Thana%20District/Thane-II/histroy_marathas.html; R4_SOUTH_ASIA-S048|R4_SOUTH_ASIA-S057; '+local,
 STATE_CIRCARS:'https://guntur.ap.gov.in/history/; R4_SOUTH_ASIA-S005; '+local,
 STATE_MADRAS:'https://tamildigitallibrary.in/assets/docs/uploads/primary_files/book/TVA_BOK_0058898/TVA_BOK_0058898_History_of_the_Madras_Army_Vol_1_1882.pdf; https://upload.wikimedia.org/wikipedia/commons/c/c1/The_Imperial_Gazetteer_of_India_-_Volume_12_%282nd_edition%29.pdf; '+local,
 STATE_GUJARAT:'https://www.orientalnumismaticsociety.org/archive/ONS_184.pdf; R4_SOUTH_ASIA-S021|R4_SOUTH_ASIA-S022|R4_SOUTH_ASIA-S047; '+local,
 STATE_RAJPUTANA:'R4_SOUTH_ASIA-S046|R4_SOUTH_ASIA-S049; https://chms.rajasthan.gov.in/Home/Know_Rajasthan; '+local,
 STATE_ASSAM:'R4_SOUTH_ASIA-S055; https://kamrup.assam.gov.in/sites/default/files/public_utility/Census-2011-District_Census_Handbook_Part-XII-B.pdf; '+local,
 STATE_CEYLON:'https://www.archives.gov.lk/online-exhibits/path-to-freedom/1-1815-convention; https://www.jaffnahistory.com/Eastern_Province/Links/DutchKandian_Treaty_1776.html; R4_SOUTH_ASIA-S010|R4_SOUTH_ASIA-S011',
 STATE_BALUCHISTAN:'R4_SOUTH_ASIA-S012|R4_SOUTH_ASIA-S013|R4_SOUTH_ASIA-S054; '+local,
 STATE_BUNDELKHAND:'R4_SOUTH_ASIA-S025|R4_SOUTH_ASIA-S026; '+local,
};
const territory=[['Province_RGB','State_Region','Before_Owner','After_Owner','Decision_Class','Land_Pixels','Min_X','Min_Y','Max_X','Max_Y','Case','Historical_Basis_And_Limit','Sources'],
 ...data.territorial.map(r=>[r.rgb,r.state,r.before,r.after,r.decision,r.pixels,...r.bbox,r.source_case,r.note,sources[r.state]])];
for(const rgb of plan.duplicates_removed){const g=geo.provinces[rgb];territory.push([rgb,'STATE_ORISSA','NAG|NAG','NAG','TECHNICAL_DUPLICATE_REMOVED',g.pixels,...g.bbox,'ODISHA_DUPLICATE','Repeated same-owner token removed. Sovereignty, population and all buildings unchanged. Diwani rights do not imply effective Company administration over Maratha Odisha.',local]);}
const pops=[['State_Region','Owner_TAG','Culture','Religion_Explicit_Or_Default','Before_People','After_People','Delta_People'],...data.population];
const popBefore=data.population.reduce((s,r)=>s+r[4],0),popAfter=data.population.reduce((s,r)=>s+r[5],0);
if(popBefore!==popAfter)throw Error('Population conservation failed');
pops.push(['TOTAL_AFFECTED_REGIONS','ALL','ALL','ALL',popBefore,popAfter,0]);
const pending=[['Case','State_Region','Status','Limit','Action'],
 ['Bombay and Salsette','STATE_BOMBAY','DOCUMENTED_GAMEPLAY_APPROXIMATION','Two native RGBs include more mainland coastline than historical islands. Area allocation would move 1.5m people; bounded technical pool moves approximately 200,000 instead, conserving all demographic fields. Not a 1776 population estimate.','Inspect coastal footprint. A later local subdivision edit could improve it; no post-January treaty imposed.'],
 ['Madras and Pudukkottai','STATE_MADRAS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Madras city RGB includes a larger district; Company receives about 408,500, not the whole Carnatic. PUD retains one interior province, about 278,800 people and its national troops.','Inspect one-province PUD recruitment and markets after one month. Do not add artificial residents.'],
 ['Mysore and Carnatic','STATE_MADRAS|STATE_CIRCARS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Whole-province Salem/Baramahal and Coimbatore corridor, Guntur/Krishna and Nellore borders are approximate. Tanjore remains Arcot in January, not its April 1776 restoration.','Inspect the southern map and Hyderabad tributary link. Local jagirs and poligar autonomy remain simplified.'],
 ['Kathiawar and Surat','STATE_GUJARAT','PARTIALLY_CORRECTED','BER/Gaekwad restored around Baroda and Ahmedabad; much of Kathiawar is still represented by the broad inherited BHV subdivision. Surat dual Nawab/Company castle control is not equated with Company annexation.','Further local princely subdivision requires a separate focused correction. Goa, Daman and Diu unchanged.'],
 ['Rajput frontier and Bundi','STATE_RAJPUTANA','DOCUMENTED_GAMEPLAY_APPROXIMATION','Six native courts replace uniform GWA ownership. Broad desert borders are not exact historic polygons; Kota also groups neighbouring Bundi. Ajmer remains Scindia. Variable Maratha tribute is not turned into a universal treaty.','Inspect six-country outline. No uniform direct Maratha administration or later British protectorates.'],
 ['Bundelkhand','STATE_BUNDELKHAND','DOCUMENTED_GAMEPLAY_APPROXIMATION','Company territorial administration removed; MARATH remains an umbrella for influence and local Bundela jurisdictions. Not all local courts are claimed as direct Peshwa administration.','A future local-principality refinement should keep these population totals and distinguish administration from revenue.'],
 ['Ahom and frontier populations','STATE_ASSAM','DOCUMENTED_GAMEPLAY_APPROXIMATION','ASM represents Lakshmi Singha and the valley. Existing cultural composition remains verbatim, including inherited broad TIP/NGA allocations; no invented Assamese population. Southern and eastern hill frontiers approximate.','Inspect new Ahom country; Moamaria rebellion not newly modelled. Manipur remains an inherited KKI abstraction.'],
 ['Kandy and Dutch coastal rights','STATE_CEYLON','DOCUMENTED_GAMEPLAY_APPROXIMATION','Four interior provinces returned to Kandy. Dutch cinnamon rights and retained foreign plantation ownership are not confused with direct sovereignty. Coastal strip widths remain coarser than the 1766 treaty.','Inspect Colombo, Galle, Trincomalee and Kandy. No invented Dutch protectorate.'],
 ['Tiny British island','STATE_CEYLON','UNRESOLVED','x5B5C22 is geographically southwest of Sri Lanka near the Chagos area, not Kandyan territory. Existing British assignment has not been treated as proof of 1776 administration.','Retained pending specific island identification and administration evidence. Never transfer to Kandy based on the State Region label.'],
 ['Gwadar and Makran','STATE_BALUCHISTAN','DOCUMENTED_GAMEPLAY_APPROXIMATION','1784 Omani grant excluded; MAK groups local Gichki/Makran authority. Kalat internal revenue arrangements and wider Durrani/Baloch borders not redrawn without adequate basis.','Inspect Gwadar. Ten inherited Omani regular units now recruit in owned Oman, preserving types, formations and national counts.'],
 ['Mughal and Awadh interfaces','STATE_DELHI|STATE_AGRA|STATE_AWADH','RETAINED_PENDING_FOCUSED_EVIDENCE','Existing Shah Alam II and Asaf-ud-Daula remain. Wider Delhi/Agra and Rohilla revenue/control interfaces retained. Inherited DUR/MUG tributary relationship is not verified as direct Afghan administration.','Do not extend Moghul or Company sovereignty by nominal claims. Political dependency merits targeted follow-up.'],
 ['Punjab, Kashmir and hill polities','STATE_PUNJAB|STATE_HILL_PUNJAB|STATE_KASHMIR','PARTIAL_NAME_CORRECTION','PAN receives a pre-1801 Sikh-confederacy name, with Jassa Singh preserved. Afghan western subdivisions and Kashmir remain; misls not individually reconstructed.','Inspect name and leader. Existing laws/tiers remain inherited approximations; no premature Ranjit Singh empire.'],
 ['Himalayan interfaces','STATE_EASTERN_HIMALAYAS|STATE_WESTERN_HIMALAYAS|STATE_HIMALAYAS','RETAINED_UNRESOLVED','Nepal, Bhutan, Sikkim and Tibet broad borders retained where exact 1776 control is uncertain. COO capital corrected to its owned West Bengal subdivision.','No modern border import and no transregional ownership expansion.'],
 ['European minor settlements','SOUTH_ASIA','RETAINED_ABSTRACTION','French, Portuguese and Danish existing enclave subdivisions preserved; Yanaon, Karikal, Mahe and other tiny factories are not all distinct RGBs.','No millions of new colonial residents for a trading post. Native factory footprints remain approximate.'],
 ['Employment and effective access','ALL_AFFECTED_REGIONS','NATIVE_TEST_PENDING','Static checks do not establish hiring, market access, prices or budgets. Roads conserved and apportioned, not automatically increased; some small new subdivisions have no road level.','Start a new game, inspect day one, advance one month and inspect logs and deficits.'],
 ['Inherited anomalies','WORLD','PREEXISTING_NOT_REGRESSION','50 double attributions and 13 inherited reference errors remain; detailed list preserved in validation JSON. No new orphan introduced.','Outside this focused R4 correction. Do not block or globally repair unrelated continents.'],
 ['Revived rulers and Kandy flag','REVIVED_TAGS','PROVISIONAL_VISUAL_SETUP','Three new historical ruler entries use approximate year-based ages; existing Rajput/Baroda rulers use native generation if no historical record exists. KND flag is a native-component identification flag, not a reconstructed historic banner.','Verify country generation and flag display. No existing rulers or commanders replaced.'],
];
const jobs=[['Territorial','MAP2F_TERRITORIAL_CHANGES.csv',territory],['Population','MAP2F_POPULATION_VALIDATION.csv',pops],['Unresolved','MAP2F_UNRESOLVED.csv',pending]];
const wb=Workbook.create();
const col=n=>{let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);}return s;};
for(const [name,,matrix] of jobs){
 const sheet=wb.worksheets.add(name);sheet.showGridLines=false;
 const range=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`);range.values=matrix;
 range.format.font={name:'Arial',size:10};range.format.verticalAlignment='center';range.format.columnWidthPx=180;range.format.rowHeightPx=name==='Population'?32:90;range.format.wrapText=true;
 const header=sheet.getRange(`A1:${col(matrix[0].length)}1`);header.format.fill='#303E4C';header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};header.format.rowHeightPx=50;
 sheet.freezePanes.freezeRows(1);
 if(name==='Population'){
  sheet.getRange('A:A').format.columnWidthPx=250;sheet.getRange('D:D').format.columnWidthPx=235;sheet.getRange(`E2:G${matrix.length}`).setNumberFormat('#,##0');
  sheet.getRange(`G2:G${matrix.length}`).formulas=matrix.slice(1).map((_,i)=>[`=F${i+2}-E${i+2}`]);
  sheet.getRange(`E${matrix.length}:F${matrix.length}`).formulas=[[`=SUM(E2:E${matrix.length-1})`,`=SUM(F2:F${matrix.length-1})`]];
 }else if(name==='Territorial'){
  sheet.getRange(`F2:J${matrix.length}`).setNumberFormat('#,##0');sheet.getRange('B:B').format.columnWidthPx=250;sheet.getRange('E:E').format.columnWidthPx=325;
 }else{
  sheet.getRange('A:A').format.columnWidthPx=250;sheet.getRange('B:B').format.columnWidthPx=300;sheet.getRange('C:C').format.columnWidthPx=300;sheet.getRange('D:E').format.columnWidthPx=600;sheet.getRange(`A2:E${matrix.length}`).format.rowHeightPx=140;
 }
}
await wb.recalculate();await fs.mkdir(new URL('QA/',out),{recursive:true});
const inspection=await wb.inspect({kind:'table',range:'Population!A1:G9',include:'values,formulas',tableMaxRows:9,tableMaxCols:7,maxChars:3500});
await fs.writeFile(new URL('QA/WORKBOOK_INSPECTION.ndjson',out),inspection.ndjson,'utf8');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:300},summary:'Final error scan'});
await fs.writeFile(new URL('QA/FORMULA_ERROR_SCAN.ndjson',out),errors.ndjson,'utf8');
for(const [name,file,matrix] of jobs){
 const sheet=wb.worksheets.getItem(name),values=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`).values;
 if(JSON.stringify(values)!==JSON.stringify(matrix))throw Error('Value mismatch '+name);
 if(name==='Population'){
  for(const rr of [2,Math.floor(matrix.length/2),matrix.length-1]){
   const cell=sheet.getRange('F'+rr),prior=cell.values;cell.values=[[prior[0][0]+1]];await wb.recalculate();
   if(sheet.getRange('G'+rr).values[0][0]!==matrix[rr-1][6]+1||sheet.getRange('G'+matrix.length).values[0][0]!==1)throw Error('Recalculation failed');
   cell.values=prior;await wb.recalculate();
   if(sheet.getRange('G'+rr).values[0][0]!==matrix[rr-1][6]||sheet.getRange('G'+matrix.length).values[0][0]!==0)throw Error('Restore failed');
  }
 }
 const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
 await fs.writeFile(new URL(file,out),values.map(r=>r.map(quote).join(',')).join('\r\n')+'\r\n','utf8');
 const preview=await wb.render({sheetName:name,range:`A1:${name==='Population'?'G':name==='Territorial'?'E':'D'}${Math.min(matrix.length,6)}`,scale:1});
 await fs.writeFile(new URL('QA/'+name+'.png',out),new Uint8Array(await preview.arrayBuffer()));
 console.log(JSON.stringify({file,rows:matrix.length-1,columns:matrix[0].length,all_cells_verified:true}));
}
await fs.writeFile(new URL('QA/TABLE_VALIDATION.json',out),JSON.stringify({status:'PASS',csvs:3,territorial_records:territory.length-1,population_records:data.population.length,studied_population:popBefore,delta:0,recalculation:'first/middle/last rows and sum restored',engine:'Artifact Tool; not Victoria 3'},null,2));
