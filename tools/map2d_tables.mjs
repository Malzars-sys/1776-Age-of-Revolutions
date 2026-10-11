import fs from 'node:fs/promises';
import { Workbook } from 'file:///C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const out=new URL('../docs/reports/map/MAP2D/',import.meta.url);
const data=JSON.parse(await fs.readFile(new URL('TABLE_DATA.json',out),'utf8'));
const treaty='https://www.vostlit.info/Texts/Dokumenty/Turk/XVIII/1760-1780/Traktat_Kucuk_Karnaji_1774/text.phtml';
const cossacks='https://www.museum.dp.ua/uk/cossacksborder/';
const changes=[['Province_RGB','State_Region','Before_Owner','After_Owner','Decision_Class','Land_Pixels','Min_X','Min_Y','Max_X','Max_Y','Case','Method','Limit','Source'],...data.territorial.map(r=>{
 const [rgb,state,,tag]=r;
 const label=state==='STATE_BESSARABIA'?(tag==='CRI'?'Budjak Tatar inland proxy':rgb==='x1E1DEF'?'Bender/Tighina district proxy':rgb==='x23621B'?'Akkerman fortress district':rgb==='x6BF7B8'?'Izmail and Kilia district proxy':'Lower Budjak Ottoman fortress coast'):state==='STATE_CRIMEA'?'Kerch and Yeni-Kale Russian treaty enclave':state==='STATE_TAURIDA'?'Kinburn Russian treaty district':tag==='TUR'?(rgb==='x716121'?'Hadjibey coastal district proxy':'Ochakiv fortress district proxy'):'Russian Bug-Dnieper lands and pre-1776 northern holdings';
 return [...r,label,'Whole existing RGB. Game river courses, coast, independent regional research and native locators. No pixel edits.',state==='STATE_CRIMEA'?'Whole Kerch RGB broader than the exact 1774 fortress district':state==='STATE_TAURIDA'?'Whole Kinburn RGB abstracts the adjoining left-bank district':state==='STATE_BESSARABIA'?'Fortress rayas and nomad pasture jurisdictions simplified; Hotin deferred':'Simplified river boundary; local mixed RGBs and Ochakiv rayon not cadastral',tag==='RUS'&&state==='STATE_CHERSON'?treaty+' (Art.18); '+cossacks:treaty+(state==='STATE_BESSARABIA'?' (Art.3,16,24)':state==='STATE_CRIMEA'?' (Art.19)':state==='STATE_TAURIDA'?' (Art.18)':' (Art.3)')];
})];
const pops=[['State_Region','Owner','Culture','Religion_Explicit_Or_Default','Before_People','After_People','Delta_People'],...data.population];
const unresolved=[['Case','State_Region','Status','Remaining_Limit','Action'],
 ['Hotin/Khotyn Ottoman raya','STATE_BESSARABIA','UNRESOLVED_NOT_CHANGED','Northern RGB x79D62E also includes Balti and extensive Moldavian lands. Whole transfer would be disproportionate. Exact raya boundary not resolved at game scale.','Future targeted local subdivision, not annexation of the entire north. Current Hotin abstraction remains inaccurate.'],
 ['Fortress rayas and Budjak autonomy','STATE_BESSARABIA','DOCUMENTED_GAMEPLAY_APPROXIMATION','Four Ottoman fortress-district RGBs and one Crimean-administered Tatar proxy. Local authorities and pasture rights simplified.','Inspect Bender, Akkerman, Izmail/Kilia and the adjacent Tatar inland area. No separate new TAG.'],
 ['Kinburn district','STATE_TAURIDA','DOCUMENTED_GAMEPLAY_APPROXIMATION','x8A09FD represents a wider left-bank district than the narrow fort and spit. No general annexation of Taurida.','Inspect Russian Kinburn against the preserved independent Crimean steppe.'],
 ['Kerch treaty district','STATE_CRIMEA','DOCUMENTED_GAMEPLAY_APPROXIMATION','Whole x706060 RGB broader than the exact Kerch-Yeni-Kale district. Rest of peninsula remains CRI.','Inspect Russian eastern tip and retained Crimean heartland.'],
 ['Inherited population geography','STATE_BESSARABIA|STATE_CHERSON|STATE_CRIMEA|STATE_TAURIDA','PRESERVED_NOT_REESTIMATED','Uniform integer allocation by transferred land-pixel area for each original cultural/religious group. Not a 1776 census. Remainder stays with original owner.','Keep existing world and regional totals. Do not add demographic subsidies to new subdivisions.'],
 ['Inherited hub place names','STATE_CHERSON|STATE_CRIMEA','PREEXISTING_ANACHRONISTIC_NAMES','Several vanilla hub labels refer to later foundations or Russian renamings. Physical locations preserved; no new historical town invented.','Separate historical toponym pass if requested. Do not interpret every inherited hub as a town already founded in 1776.'],
 ['Kuban shared RGB','STATE_KUBAN','PREEXISTING_UNRESOLVED','xBCF376 is shared by CRI and CIR. No adequate evidence in this focused lot for sole ownership.','Preserved and reported among 62 old duplicates. Do not force a transfer.'],
 ['Other old reference defects','WORLD','PREEXISTING','62 owner duplicates remain. Historical selector errors fall from 14 to 13 because Russian Crimea ownership makes the inherited Russian tobacco manor valid.','No broader repair or global merge.'],
 ['New subdivision employment and markets','STATE_BESSARABIA|STATE_CHERSON|STATE_CRIMEA|STATE_TAURIDA','NOT_MEASURED_IN_ENGINE','Static conservation cannot prove recruitment, generated manor placement, budgets or market access. No new roads or buildings added.','Check day-one panels and a one-month new-game save. Enclave connectivity remains a separate development.'],
 ['Early Russian protectorate','STATE_CRIMEA','NATIVE_TEST_PENDING','Evaluation chance 1 and priority 1000 before 1783, but original eligibility, cohesion >=50%, prestige and peace gates remain. No guaranteed date.','Observe Russia-controlled AI; confirm protectorate only, no annexation or reduction of Crimean territory.'],
 ['Polish Russian bloc retention','PLC|RUS','NATIVE_TEST_PENDING','Guarantee and law commitment plus AI acceptance floor -75 while same bloc, oligarchy, non-poor relations, no mutual diplomatic play and before 1788. Native leave threshold -100. Human departure is not locked.','Observe at least three months. Verify both treaty articles, Russian influence upkeep and no forced rejoin.'],
];
const jobs=[['Territorial','MAP2D_TERRITORIAL_CHANGES.csv',changes],['Population','MAP2D_POPULATION_VALIDATION.csv',pops],['Unresolved','MAP2D_UNRESOLVED.csv',unresolved]];
const wb=Workbook.create();
const col=n=>{let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);}return s;};
for(const [name,,matrix] of jobs){
 const sheet=wb.worksheets.add(name);sheet.showGridLines=false;
 const range=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`);range.values=matrix;
 range.format.font={name:'Arial',size:10};range.format.verticalAlignment='center';range.format.columnWidthPx=name==='Population'?185:185;range.format.rowHeightPx=name==='Population'?32:82;range.format.wrapText=true;
 const header=sheet.getRange(`A1:${col(matrix[0].length)}1`);header.format.fill='#303E4C';header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};header.format.rowHeightPx=52;
 sheet.freezePanes.freezeRows(1);
 if(name==='Population'){
   sheet.getRange('D:D').format.columnWidthPx=255;
   sheet.getRange(`E2:G${matrix.length}`).setNumberFormat('#,##0');
   sheet.getRange(`G2:G${matrix.length}`).formulas=matrix.slice(1).map((_,i)=>[`=F${i+2}-E${i+2}`]);
 }else if(name==='Territorial'){
   sheet.getRange(`F2:J${matrix.length}`).setNumberFormat('#,##0');
   sheet.getRange('E:E').format.columnWidthPx=325;
 }else{
   sheet.getRange('A:A').format.columnWidthPx=265;
   sheet.getRange('B:B').format.columnWidthPx=290;
   sheet.getRange('C:C').format.columnWidthPx=295;
   sheet.getRange('D:E').format.columnWidthPx=555;
   sheet.getRange(`A2:E${matrix.length}`).format.rowHeightPx=120;
 }
}
await wb.recalculate();
await fs.mkdir(new URL('QA/',out),{recursive:true});
const inspection=await wb.inspect({kind:'table',range:'Population!A1:G9',include:'values,formulas',tableMaxRows:9,tableMaxCols:7,maxChars:3500});
await fs.writeFile(new URL('QA/WORKBOOK_INSPECTION.ndjson',out),inspection.ndjson,'utf8');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:300},summary:'Final error scan'});
await fs.writeFile(new URL('QA/FORMULA_ERROR_SCAN.ndjson',out),errors.ndjson,'utf8');
for(const [name,file,matrix] of jobs){
 const sheet=wb.worksheets.getItem(name),values=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`).values;
 if(JSON.stringify(values)!==JSON.stringify(matrix))throw Error('Value mismatch: '+name);
 if(values.flat().some(v=>typeof v==='string'&&/^#(REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|NULL!|SPILL!|CALC!)/.test(v)))throw Error('Formula error: '+name);
 if(name==='Population'){
  const cell=sheet.getRange('F2');const prior=cell.values;cell.values=[[prior[0][0]+1]];await wb.recalculate();
  if(sheet.getRange('G2').values[0][0]!==matrix[1][6]+1)throw Error('Recalculation test failed');
  cell.values=prior;await wb.recalculate();
  if(sheet.getRange('G2').values[0][0]!==matrix[1][6])throw Error('Restore failed');
 }
 const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
 await fs.writeFile(new URL(file,out),values.map(r=>r.map(quote).join(',')).join('\r\n')+'\r\n','utf8');
 const preview=await wb.render({sheetName:name,range:`A1:${name==='Population'?'G':name==='Territorial'?'E':'D'}${Math.min(matrix.length,6)}`,scale:1});
 await fs.writeFile(new URL('QA/'+name+'.png',out),new Uint8Array(await preview.arrayBuffer()));
 console.log(JSON.stringify({file,rows:matrix.length-1,columns:matrix[0].length,all_cells_verified:true}));
}
