// Deterministic vector-to-raster export; no repainting or generated artwork.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const sharp=require('sharp');
const root=process.cwd();
const out=path.join(root,'docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU');
const svg=fs.readFileSync(path.join(out,'Wappen_Passau.svg'));
await sharp(svg,{density:192}).resize(256,256,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toFile(path.join(out,'PASSAU_FLAG_EMBLEM.png'));
console.log('Rendered public-domain vector emblem, 256×256, transparent padding.');
