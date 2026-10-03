#!/usr/bin/env node
// Diagnostic reductions/composites only. Never alters any source painting or alpha.
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const pack=path.resolve(__dirname,"../docs/reports/assets/asset6_preview_2026-10-02");
const rows=[
  {key:"oil_refinery",label:"Raffinerie : contraste derriere les produits",old:"previews/oil_refinery_v2.png",edited:"previews/oil_refinery_v3_foreground_contrast.png"},
  {key:"thermal_catalytic_cracking_refinery",label:"Craquage : ouverture autour de la flamme",old:"previews/thermal_catalytic_cracking_refinery.png",edited:"previews/thermal_catalytic_cracking_refinery_v2_open_fire.png"}
];
const esc=s=>s.replaceAll("&","&amp;").replaceAll("<","&lt;");
const title=s=>Buffer.from(`<svg width="1280" height="38"><text x="12" y="27" font-family="Segoe UI" font-size="20" fill="#eee5d4">${esc(s)}</text></svg>`);
(async()=>{
  const layers=[],reports=[];
  for(const [i,row] of rows.entries()){
    const input=fs.readFileSync(path.join(pack,row.edited));
    const {data,info}=await sharp(input).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    const at=(x,y)=>Array.from(data.subarray((Math.floor(y*info.height)*info.width+Math.floor(x*info.width))*4,(Math.floor(y*info.height)*info.width+Math.floor(x*info.width))*4+4));
    let minCore=255,nonOpaqueCore=0;
    if(row.key==="oil_refinery")for(let y=Math.ceil(info.height*.15);y<info.height*.85;y++)for(let x=Math.ceil(info.width*.15);x<info.width*.85;x++){
      const a=data[(y*info.width+x)*4+3];minCore=Math.min(minCore,a);if(a!==255)nonOpaqueCore++;
    }
    const probes=row.key==="oil_refinery"?null:{opening_left:at(.30,.70),opening_right:at(.49,.72),opening_top:at(.35,.67),flame:at(.407,.729),plinth:at(.45,.833),reactor:at(.40,.45),droplet:at(.88,.80)};
    const report={key:row.key,source:row.edited,sha256:crypto.createHash("sha256").update(input).digest("hex"),dimensions:[info.width,info.height],corner_alpha:[at(0,0)[3],at(.999,0)[3],at(0,.999)[3],at(.999,.999)[3]],interior_alpha_min:row.key==="oil_refinery"?minCore:null,non_opaque_core:row.key==="oil_refinery"?nonOpaqueCore:null,probes};
    if(report.corner_alpha.some(a=>a!==0))throw Error("Exterior not transparent: "+row.key);
    if(probes&&["opening_left","opening_right","opening_top"].some(k=>probes[k][3]!==0))throw Error("Flame opening is not fully transparent");
    reports.push(report);
    const y=i*420;
    layers.push({input:title(row.label),left:0,top:y});
    const columns=[{file:row.old,bg:"#383e43",label:"Avant"},{file:row.edited,bg:"#383e43",label:"Apres / fond sombre"},{file:row.edited,bg:"#d8d1c1",label:"Apres / fond clair"}];
    for(const [j,col] of columns.entries()){
      const x=j*420;
      layers.push({input:Buffer.from(`<svg width="410" height="30"><text x="12" y="23" font-family="Segoe UI" font-size="16" fill="#eee5d4">${esc(col.label)}</text></svg>`),left:x,top:y+38});
      layers.push({input:await sharp(path.join(pack,col.file)).resize(320,320).flatten({background:col.bg}).png().toBuffer(),left:x+40,top:y+74});
    }
  }
  await sharp({create:{width:1280,height:840,channels:3,background:"#22282b"}}).composite(layers).png().toFile(path.join(pack,"LOT_3_RETOUCHES_QA.png"));
  fs.writeFileSync(path.join(pack,"requested_retouches_validation.json"),JSON.stringify({mode:"BUILTIN_IMAGE_GEN",diagnostic_only:true,source_alpha_unmodified:true,results:reports},null,2)+"\n");
  console.log(JSON.stringify(reports,null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
