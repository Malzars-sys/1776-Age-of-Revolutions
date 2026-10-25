import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const sharp=require('sharp');
const out=path.join(process.cwd(),'docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG');
await sharp(fs.readFileSync(path.join(out,'EVIDENCE/FREISING_ARMS.svg')),{density:192}).resize(256,256,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toFile(path.join(out,'FREISING_FLAG_EMBLEM.png'));
console.log('Public-domain historical arms vector rendered at 256×256.');
