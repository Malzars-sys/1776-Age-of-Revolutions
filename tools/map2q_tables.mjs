// MAP-2Q typed CSV verification; no workbook added to the game's runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const modulePath='C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const {Workbook}=await import(pathToFileURL(modulePath));
const out=path.resolve('docs/reports/map/MAP2Q');
const datasets=JSON.parse(await fs.readFile(path.join(out,'CSV_TABLES.json'),'utf8'));
const book=Workbook.create();const records=[];
for (const [filename,rows] of Object.entries(datasets)) {
  const fields=Object.keys(rows[0]);
  const matrix=[fields,...rows.map(row=>fields.map(field=>row[field]??null))];
  const sheet=book.worksheets.add('Table'+records.length);
  sheet.getRangeByIndexes(0,0,matrix.length,fields.length).values=matrix;
  sheet.getRangeByIndexes(0,0,matrix.length,fields.length).format.columnWidth=22;
  sheet.getRangeByIndexes(0,1,matrix.length,1).format.columnWidth=36;
  records.push({filename,sheet:sheet.name,matrix,fields,rows:rows.length});
}
await book.recalculate();
const quote=v=>{const s=v==null?'':String(v);return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
for (const record of records) {
  const sheet=book.worksheets.getItem(record.sheet);
  const actual=sheet.getRangeByIndexes(0,0,record.matrix.length,record.fields.length).values;
  if(JSON.stringify(actual)!==JSON.stringify(record.matrix))throw new Error('Typed cell mismatch '+record.filename);
  const csv='\ufeff'+actual.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n';
  await fs.writeFile(path.join(out,record.filename),csv,'utf8');
}
const inspection=await book.inspect({kind:'table',range:'Table0!A1:H7',include:'values,formulas',maxChars:4000});
await fs.writeFile(path.join(out,'TABLE_INSPECTION.json'),JSON.stringify(inspection,null,2));
const preview=await book.render({sheetName:'Table0',range:'A1:E7',scale:1,format:'png'});
await fs.writeFile(path.join(out,'TABLE_QA_PREVIEW.png'),new Uint8Array(await preview.arrayBuffer()));
await fs.writeFile(path.join(out,'CSV_VALIDATION.json'),JSON.stringify({
  status:'PASS_TYPED_TABLE_ROUND_TRIP',tool:'@oai/artifact-tool',
  tables:records.map(({filename,rows,fields})=>({filename,rows,columns:fields.length})),
  unknown_historical_population:'blank, not zero',workbook_exported:false
},null,2)+'\n');
console.log('Five CSV tables verified; unknown historical counts left blank.');
