import fs from 'node:fs/promises';
import { Workbook } from 'file:///C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const out=new URL('../docs/reports/map/MAP2E/',import.meta.url);
const data=JSON.parse(await fs.readFile(new URL('TABLE_DATA.json',out),'utf8'));
const src={
 georgia:'https://www.iranicaonline.org/articles/erekle-ii/',
 west:'https://iverieli.nplg.gov.ge/bitstream/1234/371920/2/Annotachia%20G.K.%20%28%E1%83%A5%E1%83%90%E1%83%A0%E1%83%97.%20%E1%83%98%E1%83%9C%E1%83%92.%29.pdf',
 north:'https://belleten.gov.tr/eng/full-text/3701/tur',
 quba:'https://isamveri.org/pdfdkm/11/DKM111707.pdf',
 shirvan:'https://islamansiklopedisi.org.tr/sirvan',
 erivan:'https://www.iranicaonline.org/articles/erevan-1/',
 nakh:'https://nakhchivan.preslib.az/en_b2.html',
 khanates:'https://www.orientalnumismaticsociety.org/archive/ONS_Supplement_197.pdf',
 karabakh:'https://www.iranicaonline.org/articles/ebrahim-kalil-khan-javansir/',
 talysh:'https://e-book.adpu.edu.az/rrs-web/db/MEDIA/6d846702-12a1-4c08-8889-178e643d9fdc',
};
function explanation(r){
 const [rgb,state,,tag,type]=r;
 if(type==='DUPLICATE_RESOLVED')return [state==='STATE_KUBAN'?'Circassian foothills south of Kuban':'Northern Caucasus mountain communities','Competing broad native owner claims cannot both hold the same RGB. Retain the geographically consistent existing CIR/CHC subdivision.','Technical ownership cleanup. Existing population pools unchanged, not a demographic transfer.',src.north+'; regional R3 and native RGB evidence'];
 if(tag==='RUS')return [state==='STATE_DAGESTAN'?'Kizliar Russian fort district':'Mozdok Russian fort district','Russian fort foundations precede 1776. No extension to the 1777 fortified line or 19th-century mountain conquests.','Whole RGB larger than fortified footprint. Local grid fit and existing locators constrain placement, not exact district boundaries.',src.north];
 if(state==='STATE_GREATER_CAUCASUS')return tag==='ABK'?['Abkhazian local principality','Separate western authority, not eastern Kartli-Kakheti territory.','Regional coastal approximation. Ottoman influence is not converted to direct ownership or a new invented treaty.',src.west]:tag==='IMR'?['Imereti and western Georgian principalities','Eastern kingdom and western Georgian authorities were distinct.','Mingrelia, Guria and Svaneti grouped for gameplay, not proof of a unified sovereign kingdom. Existing Abkhazia TAG reused separately.',src.georgia+'; '+src.west]:['Ottoman Akhaltsikhe and Samtskhe','Ottoman provincial authority south-west of the eastern Georgian kingdom.','Whole-RGB frontier proxy. xC0CF80 includes an uncertain eastern Javakheti edge; no cadastral claim.',src.west];
 if(state==='STATE_ARMENIA')return tag==='ARM'?['Erivan local khanate','Separate local court with shifting Iranian and Georgian influence, not uniform direct Zand administration.','Whole-RGB northern district. Existing Armenian/Azerbaijani population fields preserved without a new demographic estimate.',src.erivan]:['Nakhchivan local khanate','Local Kangarli authority distinct from Erivan.','Whole-RGB southern district and imperfect border. No later Russian census imported.',src.nakh+'; '+src.erivan];
 if(state==='STATE_ELIZAVETPOL')return tag==='KRB'?['Karabakh khanate','Javanshir local authority under Ebrahim Khalil, rather than direct Zand territorial administration.','Armenian melik autonomy abstracted inside a regional khanate. No assertion that every local court was directly administered.',src.karabakh]:tag==='GJA'?['Ganja khanate and western districts','Ganja was a separate local authority amid Georgian and Iranian influence.','Gazakh/Shamshaddin interfaces simplified; local sultanates not given extra TAGs.',src.khanates+'; '+src.karabakh]:['Sheki and adjacent north-eastern districts','Sheki local authority represented separately from other eastern khanates.','Jar/Ilisu communities grouped geographically, not proven fully subject to Sheki. These limits remain documented.',src.khanates];
 if(tag==='SRV')return ['Shirvan local administration','Fat Ali of Quba reappointed local Shirvan khans in 1774. Direct abolition of the local dynasty is later (1786).','Separate administrative TAG under strong Quba influence. Native independence is a gameplay abstraction, not a claim of unrestricted sovereignty; no unsupported protectorate invented.',src.shirvan];
 if(tag==='TAL')return ['Talysh local khanate','Lankaran/Talysh local authority emerged before 1776.','Northern whole-RGB proxy only. Southern Gilan border untouched; existing Persian culture used as game proxy, no Talysh census invented.',src.talysh];
 return [state==='STATE_DAGESTAN'?'Derbent and Samur under Quba':'Quba with Baku and Salyan','Fat Ali controlled Derbent before 1776. Quba regional influence is distinct from Iranian direct government or Russian annexation.','Dependent/local Baku and Salyan courts grouped with Quba; exact local administration and northern frontier simplified.',src.quba+'; '+src.shirvan];
}
const changes=[['Province_RGB','State_Region','Before_Owner','After_Owner','Decision_Class','Land_Pixels','Min_X','Min_Y','Max_X','Max_Y','Case','Authority_Basis_1776','Approximation_Limit','Sources'],...data.territorial.map(r=>[...r,...explanation(r)])];
const pops=[['State_Region','Owner','Culture','Religion_Explicit_Or_Default','Before_People','After_People','Delta_People'],...data.population];
const popBefore=data.population.reduce((s,r)=>s+r[4],0),popAfter=data.population.reduce((s,r)=>s+r[5],0);
if(popBefore!==popAfter)throw Error('Population source totals differ');
pops.push(['TOTAL_STUDIED_REGIONS','ALL','ALL','ALL',popBefore,popAfter,0]);
const unresolved=[['Case','State_Region','Status','Remaining_Limit','Action'],
 ['Western Georgian grouping','STATE_GREATER_CAUCASUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Imereti, Mingrelia, Guria and Svaneti are not one uniformly administered historical kingdom. Abkhazia remains separate.','Review the western outline and local name. Do not add every minor TAG in this lot.'],
 ['Quba, Baku and Salyan','STATE_AZERBAIJAN|STATE_DAGESTAN','DOCUMENTED_GAMEPLAY_APPROXIMATION','Local courts and allegiance simplified under AZB/Quba. Russian assistance in 1775 does not establish Russian territorial ownership.','Inspect coastal ownership, especially Derbent. Later invasions and annexations excluded.'],
 ['Shirvan relationship with Quba','STATE_AZERBAIJAN','DOCUMENTED_GAMEPLAY_APPROXIMATION','Local khans appointed under Quba influence in 1774; native independent TAG does not capture that influence. Direct absorption in 1786 is not applied.','A justified native tributary relationship could be considered in a separate political pass. No invented guarantee or protectorate.'],
 ['Akhaltsikhe frontier','STATE_GREATER_CAUCASUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','xC27075 and x74A861 cover approximate Ottoman districts. Eastern edge xC0CF80 remains uncertain at whole-RGB scale.','Inspect Georgian/Ottoman frontier. No additional bitmap edit unless a significant visual disagreement appears.'],
 ['Kizliar and Mozdok extent','STATE_DAGESTAN|STATE_STAVROPOL','DOCUMENTED_GAMEPLAY_APPROXIMATION','Whole RGBs represent wider districts than the fortified settlements. Market connectivity not proven by ownership validation.','Inspect two Russian northern fort districts. Keep mountains local and exclude the post-1776 fort line.'],
 ['Kabardia and northern communities','STATE_NORTH_CAUCASUS|STATE_STAVROPOL','REGIONAL_AUTHORITY_ABSTRACTION','CAUC remains an abstract regional authority, not evidence of a single Kabardian/Nogai state or direct imperial administration.','Retained grouping avoids uniform Russian sovereignty. Existing population pools conserved.'],
 ['Chechen/Dagestani political framework','STATE_NORTH_CAUCASUS|STATE_DAGESTAN','PREEXISTING_FRAMEWORK_NOT_REBUILT','Dynamic name removes the 19th-century imamate label at start, but inherited CHC theocratic law and Caucasian-war journal references remain.','Political/event modernization requires a separate scoped pass. No change to existing Russian journal systems here.'],
 ['Ganja, Sheki and Karabakh local autonomy','STATE_ELIZAVETPOL','DOCUMENTED_GAMEPLAY_APPROXIMATION','Gazakh/Shamshaddin, Jar/Ilisu and Armenian meliks are simplified inside three regional powers.','Review outlines and names. Do not interpret grouped local jurisdictions as uniform direct khan rule.'],
 ['Erivan/Nakhchivan and Talysh margins','STATE_ARMENIA|STATE_AZERBAIJAN','DOCUMENTED_GAMEPLAY_APPROXIMATION','Whole-RGB boundaries, southern Talysh extent and existing culture proxies are not historical demographic reconstructions.','Retain world and regional totals. Do not import 19th-century populations.'],
 ['New rulers, flags and starting armies','IMR|KRB|GJA|SHK|NAK|TAL|SRV','INHERITED_OR_GENERATED_SETUP','Seven new TAGs use generic native flags and generated rulers. No new units invented; national preexisting forces conserved.','Historical portraits, ruler biographies and additional local armies deferred. Check flags and country generation in a new game.'],
 ['Civilian recruitment and market access','CAUCASUS|STATE_TABRIZ','NATIVE_TEST_PENDING','Static data cannot establish employment, local prices, tax budgets, generated manor placement or effective market access. Several small new subdivisions have no roads.','Inspect day one and after one month, including Tabriz receiving Persian recruitment. Do not promise full market access.'],
 ['Inherited later place names','CAUCASUS','PREEXISTING_ANACHRONISTIC_NAMES','Four hub RGB references repaired without moving locators; several native hub labels still refer to later foundations or renamings.','Do not treat a locator label as proof that the named city existed in 1776. Separate toponym pass if requested.'],
 ['Unrelated old defects','WORLD','PREEXISTING_NOT_REGRESSION','53 owner duplicates and 13 historic reference defects remain outside this focused correction.','Retain the exact list in validation JSON. No global repair or merge.'],
];
const jobs=[['Territorial','MAP2E_TERRITORIAL_CHANGES.csv',changes],['Population','MAP2E_POPULATION_VALIDATION.csv',pops],['Unresolved','MAP2E_UNRESOLVED.csv',unresolved]];
const wb=Workbook.create();
const col=n=>{let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);}return s;};
for(const [name,,matrix] of jobs){
 const sheet=wb.worksheets.add(name);sheet.showGridLines=false;
 const range=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`);range.values=matrix;
 range.format.font={name:'Arial',size:10};range.format.verticalAlignment='center';range.format.columnWidthPx=190;range.format.rowHeightPx=name==='Population'?32:82;range.format.wrapText=true;
 const header=sheet.getRange(`A1:${col(matrix[0].length)}1`);header.format.fill='#303E4C';header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};header.format.rowHeightPx=52;
 sheet.freezePanes.freezeRows(1);
 if(name==='Population'){
  sheet.getRange('D:D').format.columnWidthPx=255;sheet.getRange(`E2:G${matrix.length}`).setNumberFormat('#,##0');
  sheet.getRange(`G2:G${matrix.length}`).formulas=matrix.slice(1).map((_,i)=>[`=F${i+2}-E${i+2}`]);
  sheet.getRange(`E${matrix.length}:F${matrix.length}`).formulas=[[`=SUM(E2:E${matrix.length-1})`,`=SUM(F2:F${matrix.length-1})`]];
 }else if(name==='Territorial'){
  sheet.getRange(`F2:J${matrix.length}`).setNumberFormat('#,##0');sheet.getRange('B:B').format.columnWidthPx=270;sheet.getRange('E:E').format.columnWidthPx=325;
 }else{
  sheet.getRange('A:A').format.columnWidthPx=265;sheet.getRange('B:B').format.columnWidthPx=350;sheet.getRange('C:C').format.columnWidthPx=360;sheet.getRange('D:E').format.columnWidthPx=620;sheet.getRange(`A2:E${matrix.length}`).format.rowHeightPx=120;
 }
}
await wb.recalculate();await fs.mkdir(new URL('QA/',out),{recursive:true});
const inspection=await wb.inspect({kind:'table',range:'Population!A1:G9',include:'values,formulas',tableMaxRows:9,tableMaxCols:7,maxChars:3500});
await fs.writeFile(new URL('QA/WORKBOOK_INSPECTION.ndjson',out),inspection.ndjson,'utf8');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:300},summary:'Final error scan'});
await fs.writeFile(new URL('QA/FORMULA_ERROR_SCAN.ndjson',out),errors.ndjson,'utf8');
for(const [name,file,matrix] of jobs){
 const sheet=wb.worksheets.getItem(name),values=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`).values;
 if(JSON.stringify(values)!==JSON.stringify(matrix))throw Error('Value mismatch: '+name);
 if(values.flat().some(v=>typeof v==='string'&&/^#(REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|NULL!|SPILL!|CALC!)/.test(v)))throw Error('Formula error: '+name);
 if(name==='Population'){
  for(const rr of [2,Math.floor(matrix.length/2),matrix.length-1]){
   const cell=sheet.getRange('F'+rr),prior=cell.values;cell.values=[[prior[0][0]+1]];await wb.recalculate();
   if(sheet.getRange('G'+rr).values[0][0]!==matrix[rr-1][6]+1||sheet.getRange('G'+matrix.length).values[0][0]!==1)throw Error('Recalculation test failed');
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
await fs.writeFile(new URL('QA/TABLE_VALIDATION.json',out),JSON.stringify({status:'PASS',csvs:3,territorial_records:54,population_records:data.population.length,studied_population:popBefore,delta:0,recalculation:'first/middle/last rows and sum restored',engine:'Artifact Tool, not Victoria 3'}));
