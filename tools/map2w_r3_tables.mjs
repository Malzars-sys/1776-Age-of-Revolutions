// Typed historical research tables; CSVs are the requested deliverables.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const {Workbook}=await import(pathToFileURL('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs'));
const out=path.resolve('docs/reports/map/MAP2W/R3');
const datasets=JSON.parse(await fs.readFile(path.join(out,'CSV_TABLES.json'),'utf8'));
if(Object.keys(datasets).length!==4)throw Error('Four outputs required');
const wb=Workbook.create(),tables=[];
for(const [filename,{fields,rows}] of Object.entries(datasets)){
 const matrix=[fields,...rows.map(r=>fields.map(k=>r[k]??null))];
 const sh=wb.worksheets.add(['Inventaire','Ecarts','Restant','Changements'][tables.length]);
 const used=sh.getRangeByIndexes(0,0,matrix.length,fields.length);used.values=matrix;
 used.format.font={name:'Arial',size:10};used.format.columnWidthPx=220;used.format.rowHeight=100;used.format.wrapText=true;used.format.verticalAlignment='center';
 fields.forEach((field,col)=>{if(['Juridiction','Territoire','Source','Probleme','Observations'].includes(field))sh.getRangeByIndexes(0,col,matrix.length,1).format.columnWidthPx=430;});
 const header=sh.getRangeByIndexes(0,0,1,fields.length);header.format.fill='#25374B';header.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};header.format.rowHeight=44;header.format.horizontalAlignment='center';
 for(let c=0;c<fields.length;c++)if(rows.some(r=>typeof r[fields[c]]==='number'))sh.getRangeByIndexes(1,c,rows.length,1).setNumberFormat('#,##0');
 sh.showGridLines=false;sh.freezePanes.freezeRows(1);tables.push({filename,sheet:sh.name,matrix,fields,rows});
}
wb.recalculate();
const quote=v=>{const s=v==null?'':String(v);return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
const results=[];
for(const t of tables){
 const sh=wb.worksheets.getItem(t.sheet),actual=sh.getRangeByIndexes(0,0,t.matrix.length,t.fields.length).values;
 if(JSON.stringify(actual)!==JSON.stringify(t.matrix))throw Error('Typed roundtrip changed '+t.filename);
 await fs.writeFile(path.join(out,t.filename),'\ufeff'+actual.map(r=>r.map(quote).join(',')).join('\r\n')+'\r\n');
 const inspection=await wb.inspect({kind:'table',range:`${t.sheet}!A1:F5`,include:'values,formulas',maxChars:1200,tableMaxRows:5});
 const png=await wb.render({sheetName:t.sheet,range:t.fields.length>5?'A1:F5':'A1:D5',scale:1,format:'png'});
 await fs.writeFile(path.join(out,t.filename+'.preview.png'),new Uint8Array(await png.arrayBuffer()));
 results.push({filename:t.filename,records:t.rows.length,typed_roundtrip:'PASS',inspection});
}
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1000});
await fs.writeFile(path.join(out,'CSV_VALIDATION.json'),JSON.stringify({status:'PASS_TYPED_TABLE_ROUND_TRIP',tool:'@oai/artifact-tool',tables:results,error_scan:errors,workbook_exported:false},null,2)+'\n');
console.log('Four typed R3 CSV tables rendered, verified and exported.');
