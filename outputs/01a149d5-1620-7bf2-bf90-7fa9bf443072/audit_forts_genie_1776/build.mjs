import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const out = path.dirname(fileURLToPath(import.meta.url));
const audit = JSON.parse(await fs.readFile(path.join(out, 'audit.json'), 'utf8'));
const wb = Workbook.create();
const pays = wb.worksheets.add('Pays');
const sources = wb.worksheets.add('Sources');
const last = audit.rows.length + 5;
const ink = '#24364B';
const muted = '#576779';
const font = 'Arial';

function base(sheet, end, widths) {
  sheet.showGridLines = false;
  sheet.getRange(`A1:G${end}`).format.font = { name: font, size: 10, color: ink };
  sheet.getRange(`A1:G${end}`).format.verticalAlignment = 'center';
  sheet.getRange(`A1:G${end}`).format.rowHeight = 22;
  for (const [col, width] of Object.entries(widths)) {
    sheet.getRange(`${col}1:${col}${end}`).format.columnWidth = width;
  }
  sheet.getRange('A1:G1').format.rowHeight = 12;
  sheet.getRange('A2').format.font = { name: font, size: 14, bold: true, color: ink };
  sheet.getRange('A2:G2').format.rowHeight = 28;
  sheet.getRange('A3:D3').format.borders = { bottom: { style: 'thin', color: '#9AA9B7' } };
  sheet.freezePanes.freezeRows(5);
}

function header(sheet, range) {
  const r = sheet.getRange(range);
  r.format.fill = ink;
  r.format.font = { name: font, size: 10, bold: true, color: '#FFFFFF' };
  r.format.horizontalAlignment = 'center';
  r.format.rowHeight = 28;
  r.format.borders = { insideVertical: { style: 'thin', color: '#FFFFFF' } };
}

base(pays, last, { A: 60, B: 11, C: 23, D: 23, E: 4, F: 51, G: 9 });
pays.tabColor = ink;
pays.getRange('A2').values = [['Forts et génie : technologies de départ']];
pays.getRange('A5:D5').values = [['Pays', 'Tag', 'Technologie forts', 'Technologie génie']];
pays.getRange(`A6:D${last}`).values = audit.rows.map(r => [r.pays, r.tag, r.forts ? 'Oui' : 'Non', r.genie ? 'Oui' : 'Non']);
const table = pays.tables.add(`A5:D${last}`, true, 'TechnologiesDepart');
table.style = 'TableStyleMedium2';
table.showFilterButton = true;
header(pays, 'A5:D5');
pays.getRange(`B6:D${last}`).format.horizontalAlignment = 'center';
pays.getRange(`A6:A${last}`).format.wrapText = true;
audit.rows.forEach((r, i) => {
  if (r.pays.length > 54) pays.getRange(`A${i+6}:D${i+6}`).format.rowHeight = 36;
});
const statuses = pays.getRange(`C6:D${last}`);
statuses.conditionalFormats.add('containsText', {
  text: 'Oui', format: { fill: '#E6F2E9', font: { color: '#24613C', bold: true } }
});
statuses.conditionalFormats.add('containsText', {
  text: 'Non', format: { fill: '#F6E9E8', font: { color: '#993D36' } }
});
pays.getRange('F2').values = [['Au 1er janvier 1776']];
pays.getRange('F2').format.font = { name: font, size: 10, bold: true, color: ink };
for (const [cell, text] of Object.entries({
  F4: `Forts : ${audit.technology_names[0]}`,
  F5: `Génie : ${audit.technology_names[1]}`,
  F7: 'Oui = technologie acquise au départ.',
  F8: 'Les forts exigent aussi un État intérieur.',
  F10: 'Références détaillées dans l’onglet Sources.',
  F11: 'Audit des fichiers du mod au 19 octobre 2026.'
})) pays.getRange(cell).values = [[text]];
pays.getRange('F4:F11').format.font = { name: font, size: 10, color: muted };
pays.getRange('F4:F11').format.wrapText = false;
pays.getRange('F13:F18').values = [
  ['Pays présents'], ['Technologie forts'], ['Technologie génie'],
  ['Les deux technologies'], ['Forts uniquement'], ['Génie uniquement']
];
pays.getRange('G13:G18').formulas = [
  [`=COUNTA(B6:B${last})`],
  [`=COUNTIFS(C6:C${last},"Oui")`],
  [`=COUNTIFS(D6:D${last},"Oui")`],
  [`=COUNTIFS(C6:C${last},"Oui",D6:D${last},"Oui")`],
  [`=COUNTIFS(C6:C${last},"Oui",D6:D${last},"Non")`],
  [`=COUNTIFS(C6:C${last},"Non",D6:D${last},"Oui")`]
];
pays.getRange('F19').values = [['Aucune des deux']];
pays.getRange('G19').formulas = [[`=COUNTIFS(C6:C${last},"Non",D6:D${last},"Non")`]];
pays.getRange('G13:G19').setNumberFormat('#,##0');
pays.getRange('G13:G19').format.font = { name: font, size: 10, bold: true, color: ink };
pays.getRange('F13:G13').format.borders = { top: { style: 'thin', color: '#9AA9B7' } };
pays.getRange('F19:G19').format.borders = { bottom: { style: 'thin', color: '#9AA9B7' } };

base(sources, last, { A: 11, B: 51, C: 75, D: 75, E: 4, F: 12, G: 9 });
sources.getRange('A2').values = [['Sources des technologies initiales']];
sources.getRange('A3').values = [['Historiques de pays et paliers de départ. Les pays absents de la carte initiale sont exclus.']];
sources.getRange('A3').format.font = { name: font, size: 10, color: muted, italic: true };
sources.getRange('A5:D5').values = [['Tag', 'Historique chargé', 'Technologie forts : preuve', 'Technologie génie : preuve']];
const proofRows = audit.rows.map(r => [
  r.tag,
  r.histories.map(p => path.basename(p)).join(' ; ') || 'Aucun historique de pays : aucune technologie attribuée',
  r.sources_forts,
  r.sources_genie
]);
sources.getRange(`A6:D${last}`).values = proofRows;
const proofTable = sources.tables.add(`A5:D${last}`, true, 'PreuvesTechnologies');
proofTable.style = 'TableStyleMedium2';
proofTable.showFilterButton = true;
header(sources, 'A5:D5');
sources.getRange(`B6:D${last}`).format.wrapText = true;
proofRows.forEach((r, i) => {
  const lines = Math.max(2, Math.ceil(r[1].length/48)+1, Math.ceil(r[2].length/70)+1, Math.ceil(r[3].length/70)+1);
  sources.getRange(`A${i+6}:D${i+6}`).format.rowHeight = lines*14+6;
});

// Final calculation, checks and export. Counts must match the independent
// source audit, not constants written over spreadsheet formula results.
wb.recalculate();
const expected = [audit.counts.pays,audit.counts.forts,audit.counts.genie,audit.counts.deux,audit.counts.forts_seuls,audit.counts.genie_seul,audit.counts.aucune];
const actual = pays.getRange('G13:G19').values.map(r => Number(r[0]));
if (JSON.stringify(actual) !== JSON.stringify(expected)) throw new Error(`Counts differ: ${actual} vs ${expected}`);
const scan = await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: { useRegex: true, maxResults: 30 }, maxChars: 2500 });
await fs.writeFile(path.join(out,'formula_check.ndjson'), scan.ndjson);
const view = await wb.inspect({ kind: 'table', range: 'Pays!F13:G19', include: 'values,formulas', tableMaxRows: 8, tableMaxCols: 2, maxChars: 3200 });
await fs.writeFile(path.join(out,'summary_check.ndjson'), view.ndjson);
for (const [sheetName,range,filename] of [
  ['Pays','A1:G25','pays_preview.png'],
  ['Sources','A1:D14','sources_preview.png']
]) {
  const preview = await wb.render({sheetName,range,scale:1.5,format:'png'});
  await fs.writeFile(path.join(out,filename),new Uint8Array(await preview.arrayBuffer()));
}
const longest = audit.rows.reduce((m,r,i) => r.pays.length>audit.rows[m].pays.length ? i : m,0)+6;
const longPreview = await wb.render({sheetName:'Pays',range:`A${Math.max(5,longest-1)}:D${Math.min(last,longest+2)}`,scale:1.5,format:'png'});
await fs.writeFile(path.join(out,'long_name_preview.png'),new Uint8Array(await longPreview.arrayBuffer()));
const filename = path.join(out,'Pays_forts_et_genie_1776.xlsx');
await (await SpreadsheetFile.exportXlsx(wb)).save(filename);
await fs.writeFile(path.join(out,'workbook_validation.json'),JSON.stringify({counts:actual,expected,worksheets:['Pays','Sources'],rows:audit.rows.length,formula_scan:scan.ndjson,rendered:true,output:filename},null,2)+'\n');
console.log(JSON.stringify({output:filename,rows:audit.rows.length,counts:actual,formula_scan:scan.ndjson},null,2));
