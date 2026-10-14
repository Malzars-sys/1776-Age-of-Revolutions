import fs from 'node:fs/promises';
import { Workbook } from 'file:///C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const out=new URL('../docs/reports/map/MAP2G/',import.meta.url);
const verificationOnly=process.argv.includes('--verify-only');
const data=JSON.parse(await fs.readFile(new URL('TABLE_DATA.json',out),'utf8'));
const plan=JSON.parse(await fs.readFile(new URL('PLAN.json',out),'utf8'));
const sourceRefs={YUNGUI:'R5-S01,S22,S23,S26; Qing Shi Gao 198/200',ILI:'R5-S01,S02,S03; Qing Shi Gao 206, Qianlong 40',KHALKHA:'R5-S04,S24,S28; Qing Shi Gao 206, Qianlong 40',AINU:'R5-S07,S08; Walker 2001; native geometry',MATSUMAE:'R5-S07,S19; Walker 2001; native Hakodate locator',NORTHERN_KURILS:'Postnikov 1998, pp.39-40, RGADA fond7 no2539; LOC Krasheninnikov 1755',CHUKOTKA:'R5-S14; Zuev 2006, 1776/1778 chronology',TAIWAN:'R5-S12; Chen and Ka 2015, Taiwan Historical Research22(2)'};
const territory=[['Province_RGB','State_Region','Before_Owner','After_Owner','Decision_Class','Case','Evidence_References','Limits_Document'],...data.territorial.map(r=>[r.rgb,r.state,r.before,r.after,r.decision,r.case,sourceRefs[r.case],'MAP2G_EXECUTIVE_SUMMARY.md; MAP2G_UNRESOLVED.csv'])];
territory.push(['xBD5671','STATE_GANSU','CHI','LAKE_NO_LAND_OWNER','TECHNICAL_INVALID_SELECTOR_REMOVED','GANSU_LAKE','MAP0-0052; effective default.map and State Region','No bitmap/RGB definition deleted; no sovereign transfer.']);
const pops=[['State_Region','Owner_TAG','Culture','Religion_Explicit_Or_Default','Before_People','After_People','Delta_People'],...data.population];
const totalBefore=data.population.reduce((n,r)=>n+r[4],0),totalAfter=data.population.reduce((n,r)=>n+r[5],0);
if(totalBefore!==totalAfter)throw Error('Affected regional population changed');
pops.push(['TOTAL_AFFECTED_REGIONS','ALL','ALL','ALL',totalBefore,totalAfter,0]);
const unresolved=[['Case','State_Regions','Status','Remaining_Limit','Player_Check_Or_Future_Action'],
 ['Remote Qing administrations','YUNNAN|GUIZHOU|DZUNGARIA|TIANSHAN|ULIASTAI|URGA|TUVA','DOCUMENTED_GAMEPLAY_APPROXIMATION','Three native vassals stand for appointed administrations and banner authority, not independent states. Boundaries group existing regions rather than individual tusi, begs and banners. Central provinces and Canton remain direct Qing.','Inspect subjects, shared markets, generated governors and finances. Existing Qing ruler, armies and imperial trade capital are unchanged.'],
 ['Taiwan frontier','STATE_FORMOSA','DOCUMENTED_GAMEPLAY_APPROXIMATION','One eastern RGB also includes some western mountain fringe; not the exact Ai line. Existing yuanzhumin pool split 70% east / 30% Qing plains, not a census. No Han/Manchu conversion or relocation to mountains. All existing farms and roads remain in Qing lowlands.','Inspect eastern communities, Taipei, Keelung and Takow. Qing conscript pool remains where it was. Native road availability may be low; do not add invented residents.'],
 ['Matsumae and Ainu','STATE_HOKKAIDO','DOCUMENTED_GAMEPLAY_APPROXIMATION','Three southwest RGBs approximate Wajinchi. Ainu collective is not a unitary modern nation. Contract fisheries and scattered Japanese traders outside Wajinchi remain an economic/influence abstraction.','Inspect southern Matsumae, Ainu Mosir, existing ruler and Japanese vassal link. One existing fishery retains its EZO economic holder.'],
 ['Sakhalin Indigenous boundaries','STATE_SAKHALIN','RETAINED_APPROXIMATION','Existing Ainu/Ulta/Sakhalin community allocations on the island are retained, not claimed as exact ethnic frontiers. EZO and ALK old provinces in this State Region are actually Kuril islands, not Sakhalin proper.','Inspect Indigenous island territories. No Japanese or Russian annexation of Sakhalin; original cultures and religions conserved.'],
 ['Northern and central Kurils','STATE_SAKHALIN','DOCUMENTED_GAMEPLAY_APPROXIMATION','Two Russian-American RGB groups now use RUS, unincorporated. Limited posts/yasak and the 1775 expedition are not proof of uniform administration over every island in a compound RGB. Southern three EZO RGBs become Ainu.','Inspect island groups. No 1778-1779 mission or 1855/1875 treaty frontier imposed. Alaska and the ALK country itself are untouched.'],
 ['Chukchi communities','STATE_CHUKOTKA','CORRECTED_TAG_LEGACY_CULTURES_RETAINED','CKC decentralized replaces ATB/Athabaska only in R5. Broad siberian culture is an inherited generic category, not a new Chukchi ethnographic census. Existing Inuit and Russian groups remain.','Inspect Chukchi label and decentralized status. No Russian 1778 subjection in January 1776. North American ATB territory unchanged.'],
 ['Manchuria and Amur','AMUR|NORTHERN_MANCHURIA|SOUTHERN_MANCHURIA|OUTER_MANCHURIA|SHENGJING','RETAINED_QING','No premature Russian 1858/1860 ownership was found in these current State Regions. Direct CHI still abstracts sparse local institutions, tribute networks and Indigenous autonomy.','Inspect russo-Qing frontier and Amur garrison. More local entities require specific evidence; no forced changes just for map continuity.'],
 ['Tibet and Joseon','LHASA|NGARI|KOREAN_REGIONS','RETAINED_DOCUMENTED_DEPENDENCIES','TIB already a Qing vassal; KOR already Qing tributary with Yeongjo at Jan1. Existing valley frontiers and native diplomatic categories are approximations.','Inspect distinct Tibet/Korea; no annexation or change of established rulers and forces.'],
 ['Ryukyu and Amami','STATE_RYUKYU_ISLANDS','RETAINED_PARTIAL_DIPLOMATIC_MODEL','Okinawa/Sakishima remain RYU; Amami RGB remains JAP. Existing Japanese tributary pact abstracts Satsuma. Secondary Qing tribute is not represented by a second overlord or an invented commercial treaty.','Inspect Shuri/Naha and Amami. Four hub selectors corrected to existing physical locators. Ryukyu remains distinct, not annexed in advance of 1879.'],
 ['Interior Japan','JAPANESE_CENTRAL_REGIONS','RETAINED','Tokugawa Japan retained. Individual han are not recreated as dozens of new tags; no Meiji-era changes.','Inspect Tokugawa ruler, formations and unchanged main islands.'],
 ['Russian Siberia and Kazakh interfaces','R5_RUSSIAN_INTERIOR|CHELYABINSK|ALTAI','RETAINED_UNRESOLVED_LOCAL_AUTHORITY','Established Russian towns are preserved; extent of fiscal control across sparse interior provinces remains a broad inherited abstraction. No blanket annexation, decolonization or forced transfer of borderland valleys.','A later focused post-and-tribute map can refine major disputed sectors. Alaska is explicitly outside MAP2G.'],
 ['Economic headquarters','STATE_YUNNAN|STATE_HUNAN','NECESSARY_REFERENCE_REPAIR','Four declared Chinese holder references formerly in Yunnan now point to Hunan, still CHI. Economic holders, levels and reserves unchanged. No new bureaucracy or road level.','Inspect Hunan hiring/access and governorate budgets after a month; static profile conservation does not establish effective market access.'],
 ['Historical rulers and flags','YUN|XIN|MGL|CKC|FRS','PROVISIONAL_NATIVE_GENERATION','Existing Qianlong, Matsumae, Yeongjo, Shō Boku and Tibetan characters unchanged. New organized governments use native ruler generation, not invented named historical governors. Five native-component flags are identification banners, not authentic reconstructions.','Check governor titles, flags and colors in game. Appointed rule remains a vassal-mechanic abstraction.'],
 ['Inherited outside-scope anomalies','WORLD_OUTSIDE_R5','PREEXISTING_NOT_REGRESSION','50 preexisting double assignments unchanged. Twelve remaining inherited orphan references are outside R5; removed Gansu lake error was the thirteenth.','Detailed list in MAP2G_VALIDATION.json. Do not repair unrelated continents within this lot.'],
 ['Engine, markets and employment','ALL_AFFECTED','NATIVE_TEST_PENDING','Static AST/model checks cannot validate engine loading, foreign holder processing, budgets, hiring or diplomatic stability.','Player: new Jan1 campaign, then one month. Supply save/logs if any issue; no automated game interaction.'],
 ];
const jobs=[['Territorial','MAP2G_TERRITORIAL_CHANGES.csv',territory],['Population','MAP2G_POPULATION_VALIDATION.csv',pops],['Unresolved','MAP2G_UNRESOLVED.csv',unresolved]];
const wb=Workbook.create(),col=n=>{let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);}return s;};
for(const [name,,matrix] of jobs){
 const s=wb.worksheets.add(name);s.showGridLines=false;
 const r=s.getRange(`A1:${col(matrix[0].length)}${matrix.length}`);r.values=matrix;r.format.font={name:'Arial',size:10};r.format.wrapText=true;r.format.verticalAlignment='center';r.format.columnWidthPx=170;r.format.rowHeightPx=name==='Population'?30:65;
 const header=s.getRange(`A1:${col(matrix[0].length)}1`);header.format.fill='#303E4C';header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};header.format.rowHeightPx=45;s.freezePanes.freezeRows(1);
 if(name==='Population'){
  s.getRange('A:A').format.columnWidthPx=250;s.getRange('D:D').format.columnWidthPx=210;s.getRange(`E2:G${matrix.length}`).setNumberFormat('#,##0');
  s.getRange(`G2:G${matrix.length}`).formulas=matrix.slice(1).map((_,i)=>[`=F${i+2}-E${i+2}`]);
  s.getRange(`E${matrix.length}:F${matrix.length}`).formulas=[[`=SUM(E2:E${matrix.length-1})`,`=SUM(F2:F${matrix.length-1})`]];
 }else if(name==='Territorial'){
  s.getRange('B:B').format.columnWidthPx=250;s.getRange('E:E').format.columnWidthPx=300;s.getRange('G:H').format.columnWidthPx=500;
 }else{
  s.getRange('A:A').format.columnWidthPx=200;s.getRange('B:B').format.columnWidthPx=280;s.getRange('C:C').format.columnWidthPx=260;s.getRange('D:E').format.columnWidthPx=540;s.getRange(`A2:E${matrix.length}`).format.rowHeightPx=140;
 }
}
await wb.recalculate();await fs.mkdir(new URL('QA/',out),{recursive:true});
const inspection=await wb.inspect({kind:'table',range:'Population!A1:G9',include:'values,formulas',tableMaxRows:9,tableMaxCols:7,maxChars:4500});
await fs.writeFile(new URL('QA/POPULATION_INSPECTION.ndjson',out),inspection.ndjson,'utf8');
for(const [name,file,matrix] of jobs){
 const s=wb.worksheets.getItem(name);
 if(name==='Population')for(const rr of [2,Math.floor(matrix.length/2),matrix.length-1]){
  const cell=s.getRange('F'+rr),prior=cell.values;cell.values=[[prior[0][0]+1]];await wb.recalculate();
  if(s.getRange('G'+rr).values[0][0]!==matrix[rr-1][6]+1||s.getRange('G'+matrix.length).values[0][0]!==1)throw Error('Recalculation failed');
  cell.values=prior;await wb.recalculate();if(s.getRange('G'+matrix.length).values[0][0]!==0)throw Error('Restoration failed');
 }
 const values=s.getRange(`A1:${col(matrix[0].length)}${matrix.length}`).values;
 if(JSON.stringify(values)!==JSON.stringify(matrix))throw Error('Mismatch '+name);
 const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"',serialized=values.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n';
 if(verificationOnly){if(await fs.readFile(new URL(file,out),'utf8')!==serialized)throw Error('Saved CSV mismatch '+name);}
 else{
  await fs.writeFile(new URL(file,out),serialized,'utf8');
  const preview=await wb.render({sheetName:name,range:`A1:${name==='Population'?'G':name==='Territorial'?'E':'D'}${Math.min(matrix.length,5)}`,scale:1});await fs.writeFile(new URL('QA/'+name+'.png',out),new Uint8Array(await preview.arrayBuffer()));
 }
 console.log(JSON.stringify({file,rows:matrix.length-1,all_cells_verified:true}));
}
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'Formula errors'});await fs.writeFile(new URL('QA/FORMULA_ERROR_SCAN.ndjson',out),errors.ndjson,'utf8');
await fs.writeFile(new URL('QA/TABLE_VALIDATION.json',out),JSON.stringify({status:'PASS',csvs:3,owner_transfers:data.territorial.length,technical_lake_rows:1,affected_population:totalBefore,population_delta:0,recalculation:'first/middle/last rows and sum restored',engine:'Artifact Tool, not Victoria 3'},null,2));
