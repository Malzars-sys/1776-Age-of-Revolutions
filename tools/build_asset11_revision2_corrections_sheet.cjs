#!/usr/bin/env node
// Contact-sheet layout only; the underlying generated images are unchanged.
"use strict";
const path=require("node:path");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const pack=path.resolve(__dirname,"../docs/reports/assets/asset11_preview_2026-10-04/revision_2");
async function main(){
 const pair=await sharp(path.join(pack,"LOT_8_APERCU.png")).extract({left:440,top:0,width:880,height:570}).png().toBuffer();
 const label=Buffer.from('<svg width="880" height="40"><text x="10" y="28" fill="#eee5d4" font-family="Segoe UI" font-size="18">Révision 2 — deux corrections proposées ; aucune intégration.</text></svg>');
 await sharp({create:{width:880,height:610,channels:3,background:"#22282b"}}).composite([{input:pair,left:0,top:0},{input:label,left:0,top:570}]).png().toFile(path.join(pack,"DEUX_CORRECTIONS_APERCU.png"));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
