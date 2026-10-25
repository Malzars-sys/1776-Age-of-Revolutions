import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
// The sandbox refused the documented node_modules junction. Resolve the
// installed public package from the supplied dependency runtime instead.
const require=createRequire('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const {Workbook}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const out='C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT';
const tables=JSON.parse(await fs.readFile(out+'/TABLE_DATA.json','utf8'));
const wb=Workbook.create();
const sheets=[];
for(const [name,rows] of Object.entries(tables)){
  if(!rows.length)throw new Error('Empty table '+name);
  const headers=Object.keys(rows[0]);
  const matrix=[headers,...rows.map(r=>headers.map(k=>r[k]??null))];
  const sh=wb.worksheets.add(name);
  sh.getRangeByIndexes(0,0,matrix.length,headers.length).values=matrix;
  sheets.push({name,sh,headers,matrix});
}
// CSV export is not documented in the supplied quick API; bounded public lookup.
const help=wb.help('SpreadsheetFile.exportCsv',{include:'index,examples,notes',maxChars:1800});
await fs.writeFile(out+'/CSV_EXPORT_CAPABILITY.txt',help.ndjson??String(help));
// Required outputs are CSV, not an invented workbook. Serialize verified public
// range.values, retaining quotes, delimiters, newlines and Unicode verbatim.
const preview=wb.worksheets.add('Preview');
const sample=sheets[0].matrix.slice(0,7).map(r=>r.slice(0,4));
preview.getRangeByIndexes(0,0,sample.length,4).values=sample;
preview.getRange('A1:D7').format.font={name:'Arial',size:11};
preview.getRange('A1:D7').format.columnWidthPx=190;
preview.getRange('A1:D7').format.rowHeightPx=56;
preview.getRange('A1:D7').format.wrapText=true;
preview.getRange('A1:D1').format.fill='#183B4E';
preview.getRange('A1:D1').format.font={name:'Arial',size:11,bold:true,color:'#FFFFFF'};
wb.recalculate();
const checks=[];
const asText=v=>v===null||v===undefined?'':String(v);
const quote=v=>'"'+asText(v).replaceAll('"','""')+'"';
for(const {name,sh,headers,matrix} of sheets){
  const actual=sh.getRangeByIndexes(0,0,matrix.length,headers.length).values;
  if(JSON.stringify(actual)!==JSON.stringify(matrix))throw new Error('Range mismatch '+name);
  const text='\ufeff'+actual.map(r=>r.map(quote).join(',')).join('\r\n')+'\r\n';
  await fs.writeFile(out+'/'+name+'.csv',text,'utf8');
  const imported=await Workbook.fromCSV(text.replace(/^\ufeff/,''),{sheetName:'Check'});
  const round=imported.worksheets.getItem('Check').getRangeByIndexes(0,0,matrix.length,headers.length).values;
  for(let r=0;r<matrix.length;r++)for(let c=0;c<headers.length;c++){
    if(asText(round[r][c])!==asText(matrix[r][c]))throw new Error('Roundtrip mismatch '+name+' '+r+' '+c);
  }
  checks.push({file:name+'.csv',rows:matrix.length-1,columns:headers.length,range_verified:true,csv_roundtrip_verified:true,sha256:crypto.createHash('sha256').update(text).digest('hex')});
}
const inspection=await wb.inspect({kind:'region',sheetId:'REGIONAL_COVERAGE',range:'A1:D7',maxChars:2000,tableMaxRows:7,tableMaxCols:4});
await fs.writeFile(out+'/CSV_INSPECTION.txt',inspection.ndjson??String(inspection));
const png=await wb.render({sheetName:'Preview',autoCrop:'all',scale:1,format:'png'});
await fs.writeFile(out+'/CSV_PREVIEW.png',new Uint8Array(await png.arrayBuffer()));
await fs.writeFile(out+'/CSV_VALIDATION.json',JSON.stringify({authoring:'@oai/artifact-tool public range.values, recalculate, inspect, fromCSV roundtrip',csv_export:'Lossless CSV serialization of verified range.values; no XLSX requested or produced',checks},null,2));
console.log(JSON.stringify(checks));
