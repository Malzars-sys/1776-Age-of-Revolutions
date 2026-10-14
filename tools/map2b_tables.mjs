import fs from 'node:fs/promises';
import { Workbook } from 'file:///C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const out=new URL('../docs/reports/map/MAP2B/',import.meta.url);
const data=JSON.parse(await fs.readFile(new URL('TABLE_DATA.json',out),'utf8'));
const month=JSON.parse(await fs.readFile(new URL('OBSERVATEUR_3_COMPARISON.json',out),'utf8'));
const trento='https://archiviodistatotrento.cultura.gov.it/antichi-regimi/';
const rovereto='https://www.bibliotecacivica.rovereto.tn.it/Patrimonio-e-risorse/Archivi-storici/Fondi-e-documenti-del-periodo-veneziano';
const pazin='https://www.pazin.hr/wp-content/uploads/Obrazlo%C5%BEenje-Plana-UPU-Lindar.pdf';
const lombardy='https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.03';
const avignon='https://francearchives.gouv.fr/fr/article/350923806';
const territorial=[
 ['Province_RGB','State_Region','Previous_Owner','New_Owner','Decision_Class','Historical_Authority_1776','Population_Allocation','Building_Dependencies','Evidence','Approximation_Limits'],
 ['xD0BF60','STATE_SOUTH_TYROL','VEN','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Trent bishopric and Habsburg districts; Rovereto no longer Venetian after 1509','Joint transfer with x1120FF: 245500 existing inhabitants, all groups retained','Wheat 1 and vineyard 1 territorially AUS; Venetian investors retained, owner holder relocated to Venetia; conscript selector to VEN Lombardy',trento+' | '+rovereto,'AUS is an imperial/Habsburg proxy for bishoprics, not a claim of direct annexation before secularisation in 1803; polygon also covers a southern fringe'],
 ['x1120FF','STATE_SOUTH_TYROL','VEN','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Western Trentino / imperial and Habsburg jurisdictions','Included in the same 245500 transfer; no duplicate population','VEN South Tyrol subdivision removed only after moving its people/buildings/recruitment',trento+' | R2-0006/0007','Mixed alpine/Garda fringe; not village-exact; no new bishopric TAG'],
 ['x3060BF','STATE_ISTRIA','VEN','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Habsburg Trieste and Karst','Joint northern/interior allocation with xF0A040: 226500 inhabitants','Port 2, fishing 2, trade centre 1, government shipyard 1 moved territorially; VEN economic owners remain',pazin+' | R2-0004/0005','Coarse Karst/coastal polygon; city authority does not prove every village'],
 ['xF0A040','STATE_ISTRIA','VEN','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Habsburg northeastern/eastern Istrian possessions; Pazin provides historical context','Included in same 226500 allocation: Italian 40000, Hungarian 500, Slovene 140000, German 6000, Croat 40000','AUS public traditional roads 2; western and southern VEN coast retained',pazin+' | R2-0004/0005','Northeastern/Kvarner proxy, not exact Pazin town boundary: x36B2E3 remains mixed and deferred'],
 ['x4713EE','STATE_LOMBARDY','AUS','VEN','DOCUMENTED_GAMEPLAY_APPROXIMATION','Venetian Brescia and Crema; Austrian Milan and Mantua retained','350000 north_italian plus 58 Jewish transferred; not a census','Vineyard 1 and silk 1 transferred; AUS investors retained; AUS rice 2 unchanged; VEN roads 2',lombardy+' | R1-0008/0009','Eastern polygon contains Cremona fringe; accepted game-scale compromise, not cadastral verification; x867A90 VEN and x9AC196 SWI protected'],
 ['xB0C0E0','STATE_PROVENCE','FRA','PAP','DOCUMENTED_GAMEPLAY_APPROXIMATION','Papal Avignon and Comtat Venaissin restored in 1774','99500: Occitan 96000, French 2000, Sephardic 1500; all original French Protestants retained in FRA','Food industry 1 moved with FRA investors; PAP roads 1; FRA silk 6/cotton 4 and SAR Nice unchanged',avignon+' | R1-0016/0017','Province includes some French hinterland; enclave micro-boundaries unavailable; rounded allocation is gameplay assumption, not a 1776 census'],
];
const population=[['State_Region','Political_Owner','Culture','Religion_Explicit_Or_Default','Before','After','Delta'],...data.population];
const unresolved=[
 ['Case','State_Region','Province_RGB','Current_Owner','Status','Reason','Next_Action'],
 ['Pazin micro-boundary','STATE_ISTRIA','x36B2E3','VEN','UNRESOLVED','Town/interior and Venetian coast share a large polygon; eastern AUS proxy is not exact Pazin placement','Keep current partition; only revisit if an important coastal/interior dispute warrants geometry work'],
 ['Como / Chiavenna','STATE_LOMBARDY','xA40CE9','AUS','UNRESOLVED','Province mixes Milanese Como and Three Leagues Chiavenna; moving entire polygon would absorb substantial Milanese territory','Retain AUS; protect accepted Bormio x9AC196 SWI'],
 ['Benevento / Pontecorvo','STATE_CAMPANIA','','SIC','UNRESOLVED','Papal sovereignty documented, but smallest existing provinces include disproportionate Neapolitan hinterland','Defer rather than annex a broad Naples district or create new geometry/TAG'],
 ['Trent / Brixen independent bishoprics','STATE_SOUTH_TYROL','xD0BF60|x1120FF','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','No direct Habsburg annexation asserted; imperial bishoprics represented under AUS proxy','Consider political representation separately, without automatic TAG creation'],
 ['Other Holy Roman enclaves','R1/R2 multiple','','UNCHANGED','DEFERRED','Would require broader tag/subject restructuring beyond this Alpine/northern Italy lot','Separate authorised lot'],
 ['Old map anomalies','WORLD','','UNCHANGED','PREEXISTING','62 duplicate RGB assignments and 14 old reference anomalies; none introduced and none remaining in this lot','Treat in coherent subsequent regional lots, not a wholesale candidate merge'],
 ['East Prussia loaded level mismatch','STATE_EAST_PRUSSIA','','PRU','NATIVE_TEST_MISMATCH','observateur_3 loads 1 road level, current histories request 3; cannot infer demolition versus intermediate startup snapshot','Fresh game after final files, confirm 3 and track any subsequent demolition'],
 ['Understaffed original deficit networks','USA DC/Georgia; GBR Florida/Bermuda/Jamaica; SPA West Indies; CHI Alxa/Amur; SWE Aland','','MULTIPLE','NATIVE_DEFICIT_REMAINS','Nine of the original 69 remain negative with fewer staff than road capacity; eight traditional networks have no goods inputs','Diagnose labour availability, qualifications and competing hiring separately; do not grant free infrastructure or alter conserved populations'],
 ...month.all_negative_states.filter(s=>!month.comparison_69.some(r=>r.country===s.country&&r.region===s.region)).map(s=>[
   'Additional February deficit',s.region,'',s.country,'OBSERVED_OUTSIDE_ORIGINAL_69',`Loaded infrastructure ${s.infrastructure}; used ${s.usage}; balance ${s.balance}. `+(s.networks.length?'PM/staffing and possibly newly constructed demand differ from January.':'No regional network loaded.'),'Separate diagnosis; not automatically extend the 69-state patch']),
];
const infrastructure=[['Country','State_Region','Initial_Saved_Levels','Current_Prepatch_History_Levels','Planned_Levels','Road_PM','Initial_Cache_Balance','Projected_FullStaff_Reserve','February_Loaded_Levels','February_Staffing_LevelEquivalent','February_Infrastructure','February_Usage','February_Balance','February_Result','Source'],
 ...data.infrastructure.map(p=>{
   const r=month.comparison_69.find(r=>r.country===p.country&&r.region===p.region),s=r?.month;
   const levels=s?s.networks.reduce((v,b)=>v+b.levels,0):'n.a.';
   const staff=s?s.networks.reduce((v,b)=>v+b.staffing,0):'n.a.';
   const status=!s?'NOT_FOUND':s.balance>=0?'NONNEGATIVE':levels!==p.new_levels?'LOADED_LEVEL_MISMATCH':staff<levels?'UNDERSTAFFED_DEFICIT':'CAPACITY_DEFICIT';
   return [p.country,p.region,p.saved_levels,p.current_written_levels,p.new_levels,p.road_pm,p.saved_cache_delta,p.reserve_estimate,levels,staff,s?.infrastructure??'n.a.',s?.usage??'n.a.',s?.balance??'n.a.',status,'observateur_2 1776.1.1 / observateur_3 1776.2.1; projections assume full employment'];
 })];
const jobs=[['Territorial','MAP2B_TERRITORIAL_CHANGES.csv',territorial],['Population','MAP2B_POPULATION_VALIDATION.csv',population],['Unresolved','MAP2B_UNRESOLVED.csv',unresolved],['Infrastructure','MAP2B_INFRASTRUCTURE_CHANGES.csv',infrastructure]];
const wb=Workbook.create();
const col=n=>{let a='';while(n){n--;a=String.fromCharCode(65+n%26)+a;n=Math.floor(n/26);}return a;};
for(const [name,,matrix] of jobs){
 const sheet=wb.worksheets.add(name);sheet.getRange('A1').write(matrix);
 const range=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`);
 range.format.columnWidthPx=210;range.format.wrapText=true;range.format.rowHeightPx=name==='Population'?32:name==='Infrastructure'?64:225;
 sheet.getRange(`A1:${col(matrix[0].length)}1`).format.rowHeightPx=65;
}
await wb.recalculate();
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1600})).ndjson);
await fs.mkdir(new URL('QA/',out),{recursive:true});
for(const [name,file,matrix] of jobs){
 const sheet=wb.worksheets.getItem(name),values=sheet.getRange(`A1:${col(matrix[0].length)}${matrix.length}`).values;
 if(JSON.stringify(values)!==JSON.stringify(matrix))throw Error('Matrix mismatch: '+file);
 if(values.flat().some(v=>typeof v==='string'&&/^#(REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!)/.test(v)))throw Error('Unexpected cell error');
 const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
 await fs.writeFile(new URL(file,out),values.map(r=>r.map(quote).join(',')).join('\r\n')+'\r\n','utf8');
 const endrow=Math.min(matrix.length,name==='Population'||name==='Infrastructure'?7:4);
 const preview=await wb.render({sheetName:name,range:`A1:${col(matrix[0].length)}${endrow}`,scale:1});
 await fs.writeFile(new URL('QA/'+name+'.png',out),new Uint8Array(await preview.arrayBuffer()));
 console.log(JSON.stringify({file,rows:matrix.length-1,columns:matrix[0].length,all_cells_verified:true}));
}
