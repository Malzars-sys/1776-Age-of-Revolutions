import fs from 'node:fs/promises';
import { Workbook } from 'file:///C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const out=new URL('../docs/reports/map/MAP2C/',import.meta.url);
const data=JSON.parse(await fs.readFile(new URL('TABLE_DATA.json',out),'utf8'));
const friuli='https://www.regionestoriafvg.eu/tematiche/tema/240/Confine-tra-Venezia-e-Austria';
const comtat='https://memento.vaucluse.fr/toutes-les-ressources/revendication-de-propriete-sur-le-rhone';
const before=JSON.parse(await fs.readFile(new URL('MAP2C_BASELINE.json',out),'utf8')).inventory;
const owner=new Map(before.owners.map(r=>[r.key[0],r.key[2]]));
const territorial=[
 ['Old_RGB','New_RGB','State_Region','Old_Owner','New_Owner','Pixels_Changed','Decision_Class','Implemented_Change','Population_Handling','Source','Limit'],
 ...data.geometry.changes.map(r=>{
   const ven=r.old_rgb==='x56C78A';
   return [r.old_rgb,r.new_rgb,ven?'STATE_ISTRIA':'STATE_PROVENCE',owner.get(r.old_rgb),owner.get(r.new_rgb),r.pixels,'DOCUMENTED_GAMEPLAY_APPROXIMATION',
     ven?'Separate Udine from Gorizia: extend existing Venetian Friuli RGB, retain Gorizia and Trieste under AUS':'Compact Avignon/Comtat outline and contiguous adjacent French subdivisions',
     'Existing owner/State Region population groups unchanged. No per-pixel census or population migration asserted.',ven?friuli:comtat,
     ven?'Simplified mainland boundary, not the exact 1756 boundary or all historical enclaves':'Papal sovereignty retained; small enclaves including Valreas and village borders simplified'];
 }),
 ['xB0C0E0','xB0C0E0','STATE_PROVENCE','PAP','PAP',0,'NAMING','Avignon et Comtat Venaissin / Avignon and the Comtat Venaissin','99500 unchanged',comtat,'Only the papal subdivision renamed; French Provence and Sardinian Nice unchanged'],
 ['x108021|xB061C0|x36B2E3','same','STATE_ISTRIA','VEN','VEN',0,'NAMING','Frioul et Istrie venitiens / Venetian Friuli and Istria','340246 unchanged',friuli,'Shared State Region retained'],
 ['x56C78A|x3060BF|xF0A040','same','STATE_ISTRIA','AUS','AUS',0,'NAMING','Littoral habsbourgeois / Habsburg Littoral','339850 unchanged',friuli,'Geographic descriptive name, not creation of the formal 1849 crownland'],
 ['VEN','VEN','STATE_VENETIA','VEN','VEN',0,'NAMING','Venetia state name enforced; capital-derived country fallback disabled; republic name localized in both languages','1857196 unchanged','common/history/countries/ven - venetia.txt; existing republican dynamic-name trigger','No changes to laws or government'],
 ['NONE','transit_rights','STATE_PROVENCE','FRA','PAP',0,'USER_REQUESTED_TREATY','France grants commercial transit rights to PAP on 1776.1.1; five-year withdrawal lock','All population groups unchanged','C:/Games/Victoria 3/game/common/treaty_articles/24_transit_rights.txt; explicit user request','World-market hub access, not military access or a guaranteed domestic connection to Latium; PAP pays vanilla 50 influence upkeep'],
];
const population=[['State_Region','Owner','Culture','Religion_Explicit_Or_Default','Before_People','After_People','Delta_People'],...data.population];
const unresolved=[
 ['Case','State_Region','Status','Remaining_Limit','Action'],
 ['Comtat micro-enclaves','STATE_PROVENCE','DOCUMENTED_GAMEPLAY_APPROXIMATION','Valreas and small interlocking jurisdictions not separately represented; outline not a cadastral reconstruction','Keep compact existing-RGB abstraction; inspect visual result in a fresh game'],
 ['Friuli border enclaves','STATE_ISTRIA','DOCUMENTED_GAMEPLAY_APPROXIMATION','Village boundaries and enclave patterns of the 1756 agreement not reproduced','Keep Udine VEN, Gorizia AUS; revisit only a material disagreement'],
 ['Pazin and mixed coast','STATE_ISTRIA','PREEXISTING_APPROXIMATION','MAP2B northeastern/interior proxy retained; western/southern coastal RGB x36B2E3 remains mixed','No wider Istrian or Dalmatian reassignment in this lot'],
 ['Population geographic allocation','STATE_PROVENCE|STATE_ISTRIA','PRESERVED_NOT_REESTIMATED','Demographics attach to owner/State Region, not individual RGB pixels. Existing MAP2B allocation retained, not a new historical census','No demographic adjustment requested or applied'],
 ['Provence wood locator','STATE_PROVENCE','PREEXISTING_MISMATCH','Vanilla physical wood locator falls on x5080E0 although the inherited definition uses x3040E0','Left unchanged; not caused by this patch'],
 ['Global old map references','WORLD','PREEXISTING','62 duplicate owner assignments and 14 reference errors in the saved baseline are unchanged','Do not enlarge this focused lot'],
 ['Native engine load and names','STATE_PROVENCE|STATE_ISTRIA|STATE_VENETIA','NOT_RUN','Static checks and source-driven previews do not establish game loading, naming refresh or generated map rendering','Restart Victoria 3; start a new 1776 game and inspect the two zones and ports'],
 ['Avignon domestic versus world-market access','STATE_PROVENCE','NOT_RUN','Requested FRA -> PAP transit treaty concerns French world-market hubs. Domestic Avignon -> Latium connectivity is not guaranteed by this article','Check the treaty, domestic market access and world-market access separately in a new game; no automatic annexation or new port'],
];
const jobs=[['Territorial','MAP2C_TERRITORIAL_CHANGES.csv',territorial],['Population','MAP2C_POPULATION_VALIDATION.csv',population],['Unresolved','MAP2C_UNRESOLVED.csv',unresolved]];
const wb=Workbook.create();
const col=n=>{let a='';while(n){n--;a=String.fromCharCode(65+n%26)+a;n=Math.floor(n/26);}return a;};
for(const [name,,matrix] of jobs){
 const s=wb.worksheets.add(name);s.getRange('A1').write(matrix);
 const r=s.getRange(`A1:${col(matrix[0].length)}${matrix.length}`);
 r.format.columnWidthPx=180;r.format.wrapText=true;r.format.rowHeightPx=name==='Population'?42:150;
 s.getRange(`A1:${col(matrix[0].length)}1`).format.rowHeightPx=54;
 if(name==='Population'){
   s.getRange('D:D').format.columnWidthPx=260;
   s.getRange(`G2:G${matrix.length}`).formulas=matrix.slice(1).map((_,i)=>[`=F${i+2}-E${i+2}`]);
 }
}
await wb.recalculate();
const inspection=await wb.inspect({kind:'table',range:'Population!A1:G8',include:'values,formulas',tableMaxRows:8,tableMaxCols:7});
await fs.mkdir(new URL('QA/',out),{recursive:true});
await fs.writeFile(new URL('QA/WORKBOOK_INSPECTION.ndjson',out),inspection.ndjson,'utf8');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:300},summary:'Final error scan'});
await fs.writeFile(new URL('QA/FORMULA_ERROR_SCAN.ndjson',out),errors.ndjson,'utf8');
for(const [name,file,matrix] of jobs){
 const s=wb.worksheets.getItem(name),values=s.getRange(`A1:${col(matrix[0].length)}${matrix.length}`).values;
 if(JSON.stringify(values)!==JSON.stringify(matrix))throw Error('Export value mismatch: '+name);
 if(values.flat().some(v=>typeof v==='string'&&/^#(REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|NULL!|SPILL!|CALC!)/.test(v)))throw Error('Unexpected error: '+name);
 const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
 const csv=values.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n';
 await fs.writeFile(new URL(file,out),csv,'utf8');
 const columns=name==='Population'?7:name==='Territorial'?7:4;
 const render=await wb.render({sheetName:name,range:`A1:${col(columns)}${Math.min(matrix.length,6)}`,scale:1});
 await fs.writeFile(new URL('QA/'+name+'.png',out),new Uint8Array(await render.arrayBuffer()));
 console.log(JSON.stringify({file,rows:matrix.length-1,columns:matrix[0].length,all_cells_verified:true}));
}
