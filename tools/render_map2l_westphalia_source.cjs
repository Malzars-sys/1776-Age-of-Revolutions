// Lossless local reading derivative of a retained source, not a new map asset.
const sharp=require('C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const path=require('path');
const root=path.resolve(__dirname,'..');
const input=path.join(root,'docs/reports/map/MAP2L/EVIDENCE/Holy_Roman_Empire_1789_comparison.svg');
const output=path.join(root,'docs/reports/map/MAP2L/RHINE_WESTPHALIA/COMPARISON_1789.png');
sharp(input).png().toFile(output).then(info=>console.log(info)).catch(error=>{console.error(error);process.exitCode=1;});
