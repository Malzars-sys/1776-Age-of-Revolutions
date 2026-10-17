// Requested CSV outputs only, with typed round-trip validation and previews.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const {Workbook}=await import(pathToFileURL('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs'));
const out=path.resolve('docs/reports/map/MAP2U');
const datasets=JSON.parse(await fs.readFile(path.join(out,'CSV_TABLES.json'),'utf8'));
const wb=Workbook.create();const tables=[];
for(const [filename,{fields,rows}] of Object.entries(datasets)){
  const matrix=[fields,...rows.map(row=>fields.map(field=>row[field]??null))];
  const sh=wb.worksheets.add(['Transferts','Population','Restant'][tables.length]);
  const used=sh.getRangeByIndexes(0,0,matrix.length,fields.length);used.values=matrix;
  used.format.font={name:'Arial',size:10};used.format.columnWidthPx=190;used.format.rowHeight=55;
  used.format.wrapText=true;used.format.verticalAlignment='center';
  const header=sh.getRangeByIndexes(0,0,1,fields.length);header.format.fill='#25374B';
  header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
  header.format.rowHeight=45;header.format.horizontalAlignment='center';
  if(filename==='UNRESOLVED.csv'){
    sh.getRangeByIndexes(0,0,matrix.length,1).format.columnWidthPx=225;
    sh.getRangeByIndexes(0,1,matrix.length,1).format.columnWidthPx=65;
    sh.getRangeByIndexes(0,2,matrix.length,2).format.columnWidthPx=470;
    used.format.rowHeight=100;header.format.rowHeight=45;
  }
  for(let col=0;col<fields.length;col++)if(rows.some(row=>typeof row[fields[col]]==='number'))sh.getRangeByIndexes(1,col,rows.length,1).setNumberFormat('#,##0');
  sh.showGridLines=false;sh.freezePanes.freezeRows(1);tables.push({filename,sheet:sh.name,matrix,rows,fields});
}
wb.recalculate();
const quote=v=>{const s=v==null?'':String(v);return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
const results=[];
for(const t of tables){
  const sh=wb.worksheets.getItem(t.sheet);const actual=sh.getRangeByIndexes(0,0,t.matrix.length,t.fields.length).values;
  if(JSON.stringify(actual)!==JSON.stringify(t.matrix))throw Error('Typed round trip changed '+t.filename);
  await fs.writeFile(path.join(out,t.filename),'\ufeff'+actual.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n');
  const end=String.fromCharCode(64+Math.min(t.fields.length,9));
  const inspection=await wb.inspect({kind:'table',range:`${t.sheet}!A1:${end}${Math.min(t.matrix.length,7)}`,include:'values,formulas',maxChars:1600,tableMaxRows:7});
  const png=await wb.render({sheetName:t.sheet,range:`A1:${end}${Math.min(t.matrix.length,7)}`,scale:1,format:'png'});
  await fs.writeFile(path.join(out,t.filename+'.preview.png'),new Uint8Array(await png.arrayBuffer()));
  results.push({filename:t.filename,records:t.rows.length,typed_roundtrip:'PASS',inspection});
}
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1000});
await fs.writeFile(path.join(out,'CSV_VALIDATION.json'),JSON.stringify({status:'PASS_TYPED_TABLE_ROUND_TRIP',tool:'@oai/artifact-tool',tables:results,error_scan:errors,workbook_exported:false},null,2)+'\n');
console.log('Three requested CSV files exported and inspected.');
