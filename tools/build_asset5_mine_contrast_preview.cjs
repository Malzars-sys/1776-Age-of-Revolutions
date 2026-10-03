#!/usr/bin/env node
// Mechanical before/after layout and native-size reductions only; no art/alpha edits.
"use strict";
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const sharp = require(require.resolve("sharp", {paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]}));
const pack = path.resolve(__dirname, "../docs/reports/assets/asset5_preview_2026-10-02");
const esc = s => s.replaceAll("&", "&amp;").replaceAll("<", "&lt;");
const text = (s, w, h, size=18) => Buffer.from(`<svg width="${w}" height="${h}"><text x="0" y="${size+5}" font-family="Segoe UI" font-size="${size}" fill="#eee5d4">${esc(s)}</text></svg>`);
const sha = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
(async () => {
  const sunrise = process.argv[2] === "sunrise";
  const output = sunrise ? "MINE_AMBIANCE_V3_LEVER_DE_SOLEIL.png" : "MINE_CONTRASTE_V2_V3.png";
  const files = (sunrise ? ["previews/phosphate_mine_v3.png", "previews/phosphate_mine_v4_sunrise.png"] : ["previews/phosphate_mine_v2.png", "previews/phosphate_mine_v3.png"]).map(f => path.join(pack, f));
  const parts = [], results = [];
  parts.push({input: text(sunrise ? "Mine de phosphate — essai de lever du soleil" : "Mine de phosphate — contraste avant / après", 890, 40, 24), left: 25, top: 15});
  for (const [i, file] of files.entries()) {
    const x = 45 + i*460;
    const caption = sunrise ? (i ? "V4 : variante au lever du soleil" : "V3 : version précédente conservée") : (i ? "V3 : fond froid et sombre" : "V2 : fond proche du minerai");
    parts.push({input: text(caption, 415, 30), left: x, top: 55});
    parts.push({input: await sharp(file).resize(350,350).flatten({background:"#303436"}).png().toBuffer(), left: x, top: 90});
    for (const [j, size] of [48,64,96].entries()) {
      const y = [470,535,620][j];
      parts.push({input: text(`${size} × ${size} px`, 130, 28, 16), left: x, top: y+10});
      for (const [b,bg] of ["#443c30", "#d8d1c1"].entries())
        parts.push({input: await sharp(file).resize(size,size).flatten({background:bg}).png().toBuffer(), left:x+135+b*135, top:y});
    }
    const {data,info} = await sharp(file).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    let min=255, max=0, alphaZero=0, alphaFull=0, interiorMin=255, interiorMax=0;
    for (let y=0; y<info.height; y++) for(let x2=0; x2<info.width; x2++) {
      const a=data[(y*info.width+x2)*4+3];
      min=Math.min(min,a); max=Math.max(max,a); if(a===0)alphaZero++; if(a===255)alphaFull++;
      if(x2>info.width*.15 && x2<info.width*.85 && y>info.height*.15 && y<info.height*.85) {
        interiorMin=Math.min(interiorMin,a); interiorMax=Math.max(interiorMax,a);
      }
    }
    results.push({file:path.relative(pack,file).replaceAll("\\","/"),sha256:sha(file),dimensions:[info.width,info.height],alpha:[min,max],alpha_zero:alphaZero,alpha_full:alphaFull,interior_alpha:[interiorMin,interiorMax]});
  }
  parts.push({input:text("Miniatures à leur taille réelle ; aucun fichier intégré au jeu.",890,30,16),left:25,top:735});
  await sharp({create:{width:920,height:780,channels:3,background:"#22282b"}}).composite(parts).png().toFile(path.join(pack,output));
  console.log(JSON.stringify({comparison:output,results},null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
