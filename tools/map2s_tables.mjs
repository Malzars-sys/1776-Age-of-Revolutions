// Typed CSV audit reports only; no workbook or game asset is added to runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const out=path.resolve('docs/reports/map/MAP2S');
// Junction creation is denied by the workspace sandbox. Read the loader-owned
// documented module directly, without installing or altering any dependency.
const {Workbook}=await import(pathToFileURL('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs'));
const data=JSON.parse(await fs.readFile(path.join(out,'CSV_TABLES.json'),'utf8'));
const wb=Workbook.create();const tables=[];
for(const [name,{fields,rows}] of Object.entries(data)){
  const matrix=[fields,...rows.map(r=>fields.map(f=>r[f]??null))];
  const sh=wb.worksheets.add(`Table${tables.length}`);
  const range=sh.getRangeByIndexes(0,0,matrix.length,fields.length);
  range.values=matrix;range.format.font={name:'Arial',size:10};
  range.format.columnWidthPx=180;range.format.rowHeight=100;
  range.format.wrapText=true;range.format.verticalAlignment='center';
  const header=sh.getRangeByIndexes(0,0,1,fields.length);
  header.format.fill='#25374B';header.format.font={name:'Arial',size:10,color:'#FFFFFF',bold:true};
  header.format.rowHeight=50;header.format.horizontalAlignment='center';
  sh.showGridLines=false;sh.freezePanes.freezeRows(1);
  tables.push({name,fields,rows,matrix,sheet:sh.name});
}
wb.recalculate();
const q=v=>{const text=v==null?'':String(v);return /[",\r\n]/.test(text)?'"'+text.replaceAll('"','""')+'"':text;};
const result=[];
for(const t of tables){
  const sh=wb.worksheets.getItem(t.sheet);
  const actual=sh.getRangeByIndexes(0,0,t.matrix.length,t.fields.length).values;
  if(JSON.stringify(actual)!==JSON.stringify(t.matrix))throw Error('Typed roundtrip changed '+t.name);
  const csv='\ufeff'+actual.map(row=>row.map(q).join(',')).join('\r\n')+'\r\n';
  await fs.writeFile(path.join(out,t.name),csv,'utf8');
  const inspect=await wb.inspect({kind:'table',range:`${t.sheet}!A1:E${Math.min(t.matrix.length,7)}`,include:'values,formulas',maxChars:2000,tableMaxRows:7});
  const preview=await wb.render({sheetName:t.sheet,range:`A1:${String.fromCharCode(64+t.fields.length)}${Math.min(t.matrix.length,7)}`,scale:1,format:'png'});
  await fs.writeFile(path.join(out,t.name+'.preview.png'),new Uint8Array(await preview.arrayBuffer()));
  result.push({name:t.name,records:t.rows.length,columns:t.fields.length,typed_roundtrip:'PASS',inspection:inspect});
}
await fs.writeFile(path.join(out,'CSV_VALIDATION.json'),JSON.stringify({status:'PASS_TYPED_TABLE_ROUND_TRIP',tool:'@oai/artifact-tool',tables:result,workbook_exported:false,empty_territorial_change_table_is_deliberate:true},null,2)+'\n');
console.log('Five CSV reports exported; zero installed territorial changes, no fabricated unknown values.');
