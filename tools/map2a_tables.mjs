import fs from 'node:fs/promises';
import { Workbook } from 'file:///C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const wb = Workbook.create();
if (process.argv.includes('--discover')) {
  console.log(wb.help('CSV export', {search:'CSV|csv',include:'index,examples,notes',maxChars:4000}).ndjson);
  process.exit(0);
}
const out = new URL('../docs/reports/map/MAP2A/',import.meta.url);
const data = JSON.parse(await fs.readFile(new URL('MAP2A_TABLE_DATA.json',out),'utf8'));
const sources = {
  leagues:'https://hls-dhs-dss.ch/it/articles/026840/2004-04-14/',
  bormio:'https://www.lombardiabeniculturali.it/docs/istituzioni/Sondrio-s.pdf',
  silesia:'https://zaranieslaskie.bs.katowice.pl/en/article/download/44/18/36',
};
const territorial = [
  ['Province_RGB','Old_State_Region','Old_Owner','New_State_Region','New_Owner','Decision_Class','Historical_Authority_1776','Population_Method','Dependencies','Evidence','Limits'],
  ['x9AC196','STATE_LOMBARDY','VEN','STATE_LOMBARDY','SWI','DOCUMENTED_GAMEPLAY_APPROXIMATION','Three Leagues; SWI proxy for an associated republic, not a modern canton',
   '5000 moved from VEN pool: 4999 north_italian default Catholic; 1 Jewish; informed by Bormio aggregate 4832 in 1807, not a 1776 census',
   'No existing VEN building or recruitment declaration in Lombardy; Austrian buildings unchanged',sources.leagues+' | '+sources.bormio,
   'Northern Bormio vicinity from MAP1C; game polygon imperfect; no separate Three Leagues TAG'],
  ['x71E080','STATE_UPPER_SILESIA','AUS|PRU','STATE_MORAVIA','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Retained Austrian Silesian districts towards Opava/Troppau',
   'Existing Austrian Silesian pool shared linguistically with Teschen; combined totals exact',
   'Remove duplicate ownership and wrong regional scope; retained Austrian assets located in Teschen',sources.silesia,
   'Boundary approximation at game scale; physical region membership exact, historical local boundary not cadastral'],
  ['xF0E080','STATE_UPPER_SILESIA','AUS|PRU','STATE_MORAVIA','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Retained Austrian Silesian districts towards Opava/Krnov',
   '191139 of existing Austrian pool added to Moravia jointly with x71E080; not allocated by province count',
   'Remove duplicate ownership and wrong regional scope; no Prussian population or building transfer',sources.silesia,
   'Local border follows existing province geometry; cannot resolve every village'],
  ['x9061E0','STATE_UPPER_SILESIA','AUS','STATE_WEST_GALICIA','AUS','DOCUMENTED_GAMEPLAY_APPROXIMATION','Duchy of Teschen retained by Austria; not transferred to GAL',
   '135753 of existing Austrian pool assigned to Teschen, all original cultures/religions retained',
   'AUS textile 2 levels and infrastructure 1 level relocated; one conscript recruitment selector; overlay textile retained',sources.silesia,
   'West Galicia is a game region name, not a claim that Teschen historically belonged to Galicia; demographic shares are gameplay assumptions'],
];
const unresolved = [
  ['Case','State_Region','Province_RGB','Current_Owner','Reason_Deferred','Evidence_Or_Research','Next_Action'],
  ['Brescia/Crema/Cremona','STATE_LOMBARDY','x4713EE','AUS','Province overlaps Austrian and Venetian districts; hub/city alone insufficient','MAP1C; R1-0008/0009','One focused border comparison; preserve VEN x867A90'],
  ['Como/Chiavenna','STATE_LOMBARDY','xA40CE9','AUS','Province mixes Milanese and Three Leagues territories','MAP1C; Lombardy institutional histories','Compare playable northern boundary; do not allocate entire Como region from a city label'],
  ['Trentino / Venetian Alpine fringe','STATE_SOUTH_TYROL','xD0BF60|x1120FF','VEN','Trent bishopric and Habsburg courts are documented, but southern Venetian fringe and whole polygons not adequately reconciled','R2-0006/0007; https://archiviodistatotrento.cultura.gov.it/antichi-regimi/','Priority next lot; retain existing population and economic records rather than proclaiming split historically verified'],
  ['Interior Istria / Trieste','STATE_ISTRIA','x56C78A and neighbours','AUS|VEN','Existing selectors and populations valid; geographic allocation remains a provisional inherited compromise','R2-0004/0005','Focused interior/costal boundary check, no new demographic redistribution yet'],
  ['Budjak / Ottoman forts','STATE_BESSARABIA','','MOL','Git tokens removed from candidate only; Ottoman forts and southern authority warrant separate mapping, not syntax-driven sovereignty change','R2-0008; Treaty of Kucuk Kaynarca 1774','Separate Moldavian interior, Budjak and fortified enclaves in R2/R3 next lot'],
  ['Avignon / Comtat','STATE_PROVENCE|STATE_RHONE','','FRA','Papal authority documented; game polygons can absorb sizeable French hinterlands; candidate RGB not yet defensible','R1-0016/0017','Prioritise manageable PAP transfer with local geographic comparison and existing Provence buildings preserved'],
  ['Benevento / Pontecorvo','STATE_CAMPANIA','','SIC','Papal enclaves documented; no defensible whole province attribution in current files','R1-0018/0019','Test smallest existing provinces against enclave extents'],
  ['Liege / Stavelot / Bouillon','STATE_WALLONIA','','BEO','Separate historical entities not represented by suitable existing tags; no new tags authorised','R1-0002/0003/0035','Leave approved BEO/Luxembourg integration untouched; request later representation decision'],
  ['Courland / Holy Roman microstates','R2 multiple','','PLC and existing German states','Autonomous polities or mixed province borders; broad redistribution would exceed simple lot','R2 regional originals; MAP1_PRIORITY_ARBITRATION.csv','Later coherent lot; no automatic new TAG'],
  ['Remaining preexisting map anomalies','WORLD','','UNCHANGED','62 duplicate RGBs and 14 critical static region/reference anomalies remain; none introduced by MAP2A','MAP2A_VALIDATION.json','Treat independently by region; not silently mark all 410 cases solved'],
  ['Candidate branch not merge-ready','CANDIDATE','','UNCHANGED','Old Luxembourg population loss, Ottoman reversions and candidate Austrian x9AC196 decision are not integrated','3126bac / 0e018d9','Do not merge wholesale; retain approved main workspace corrections'],
];
const population = [['State_Region','Political_Owner','Culture','Religion_Explicit_Or_Default','Before','After','Delta'],...data.population];
const jobs = [
  ['Territorial','MAP2A_TERRITORIAL_CHANGES.csv',territorial],
  ['Population','MAP2A_POPULATION_VALIDATION.csv',population],
  ['Unresolved','MAP2A_UNRESOLVED.csv',unresolved],
];
const sheets = new Map();
for (const [name,file,matrix] of jobs) {
  const sheet = wb.worksheets.add(name);
  sheets.set(name,sheet);
  sheet.getRange('A1').write(matrix);
  const range = sheet.getRange('A1:'+String.fromCharCode(64+matrix[0].length)+matrix.length);
  range.format.columnWidthPx = 235;
  range.format.wrapText = true;
  range.format.rowHeightPx = name==='Population' ? 30 : 190;
  sheet.getRange('A1:'+String.fromCharCode(64+matrix[0].length)+'1').format.rowHeightPx = 52;
}
await wb.recalculate();
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1800})).ndjson);
// CSVs have no style/formula surface. Export verified literal cell values,
// preserving numeric values and using RFC4180 escaping. No XLSX requested.
for (const [name,file,matrix] of jobs) {
  const sheet = sheets.get(name);
  const end = String.fromCharCode(64+matrix[0].length)+matrix.length;
  const values = sheet.getRange('A1:'+end).values;
  if (JSON.stringify(values)!==JSON.stringify(matrix)) throw new Error('Cell verification failed: '+file);
  const quote = v => '"'+String(v??'').replaceAll('"','""')+'"';
  await fs.writeFile(new URL(file,out),values.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n','utf8');
  console.log(JSON.stringify({file,rows:values.length-1,columns:values[0].length,verified:true}));
  await fs.mkdir(new URL('QA/',out),{recursive:true});
  const preview = await wb.render({sheetName:name,range:'A1:'+end,scale:1});
  await fs.writeFile(new URL('QA/'+name+'.png',out),new Uint8Array(await preview.arrayBuffer()));
}
