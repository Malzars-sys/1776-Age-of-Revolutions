#!/usr/bin/env node
// Mechanical preview checks only: never alter masters, game files or DDS.
"use strict";
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const sharp = require(require.resolve("sharp", {paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const root = path.resolve(__dirname,".."), pack = path.join(root,"docs/reports/assets/asset9_preview_2026-10-04");
const rev = path.join(pack,"user_revision_v2");
const req = JSON.parse(fs.readFileSync(path.join(rev,"generation_requests.json"),"utf8"));
const plan = JSON.parse(fs.readFileSync(path.join(pack,"generation_plan.json"),"utf8"));
const hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const walk = dir => fs.readdirSync(dir,{withFileTypes:true}).flatMap(e => { const p=path.join(dir,e.name); return e.isDirectory()?walk(p):[path.relative(root,p).replaceAll("\\","/")]; });
const snapshot = () => Object.fromEntries(["common","gfx"].flatMap(d=>walk(path.join(root,d))).map(p=>[p,hash(fs.readFileSync(path.join(root,p)))]));
const write = (name,value) => fs.writeFileSync(path.join(rev,name),JSON.stringify(value,null,2)+"\n");
const esc = s => s.replaceAll("&","&amp;").replaceAll("<","&lt;");
const label = (s,w=440) => Buffer.from(`<svg width="${w}" height="38"><text x="10" y="27" fill="#eee5d4" font-family="Segoe UI" font-size="20">${esc(s)}</text></svg>`);

async function main() {
  if(req.requests.length!==2 || !req.approval_required_before_integration || req.third_proposal.status!=="CONCEPT_PROPOSAL_ONLY_NOT_GENERATED") throw Error("Unexpected revision scope");
  const baseline=JSON.parse(fs.readFileSync(path.join(pack,"gameplay_and_gfx_baseline.json"),"utf8")), current=snapshot();
  const changed=Object.keys(baseline).filter(p=>current[p]!==baseline[p]), added=Object.keys(current).filter(p=>!(p in baseline));
  if(changed.length || added.length) throw Error("Protected files changed: "+JSON.stringify({changed,added}));
  for(const e of plan.entries) if(fs.existsSync(path.join(root,e.target_dds))) throw Error("Unapproved DDS exists: "+e.key);
  fs.mkdirSync(path.join(rev,"target_size_png"),{recursive:true});
  const overview=[], compare=[], checkerLayers=[], results=[];
  const checker=Buffer.alloc(256*256*4);
  for(let y=0;y<256;y++) for(let x=0;x<256;x++) { const k=(y*256+x)*4,c=((x>>4)+(y>>4))%2?185:228; checker[k]=checker[k+1]=checker[k+2]=c; checker[k+3]=255; }
  for(const [i,e] of req.requests.entries()) {
    const original=path.join(pack,e.output), originalBytes=fs.readFileSync(original);
    const preview=e.selected_preview || e.output, source=path.join(pack,preview);
    if(e.mechanical_padding_px) {
      const p=e.mechanical_padding_px;
      await sharp(originalBytes).extend({top:p,bottom:p,left:p,right:p,background:{r:0,g:0,b:0,alpha:0}}).png().toFile(source);
    }
    const bytes=fs.readFileSync(source), meta=await sharp(bytes).metadata();
    if(!meta.hasAlpha || meta.width!==meta.height || meta.width<1024) throw Error("Invalid square alpha master: "+e.key);
    const {data,info}=await sharp(bytes).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    let transparent=0, partial=0, opaque=0;
    const bounds=[info.width,info.height,0,0];
    for(let y=0;y<info.height;y++) for(let x=0;x<info.width;x++) { const a=data[(y*info.width+x)*4+3]; if(a===0) transparent++; else if(a===255) opaque++; else partial++; if(a>=16) { bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y); } }
    const corners=[[0,0],[info.width-1,0],[0,info.height-1],[info.width-1,info.height-1]].map(([x,y])=>data[(y*info.width+x)*4+3]);
    if(!transparent || corners.some(a=>a!==0)) throw Error("Missing transparent exterior: "+e.key);
    const target=`target_size_png/${e.key}.png`;
    await sharp(bytes).resize(256,256).png().toFile(path.join(rev,target));
    const reduced=await sharp(path.join(rev,target)).ensureAlpha().raw().toBuffer();
    if([0,255,256*255,256*256-1].some(p=>reduced[p*4+3]!==0)) throw Error("Reduced corners not transparent");
    if(hash(fs.readFileSync(source))!==hash(bytes)) throw Error("Master unexpectedly changed");
    if(hash(fs.readFileSync(original))!==hash(originalBytes)) throw Error("Generated original unexpectedly changed");
    if(e.mechanical_padding_px) {
      const p=e.mechanical_padding_px, om=await sharp(originalBytes).metadata();
      const rawOriginal=await sharp(originalBytes).ensureAlpha().raw().toBuffer();
      const cropped=await sharp(source).extract({left:p,top:p,width:om.width,height:om.height}).ensureAlpha().raw().toBuffer();
      if(!rawOriginal.equals(cropped)) throw Error("Padding changed original image pixels");
    }
    results.push({key:e.key,source:preview,sha256:hash(bytes),generated_original_copy:e.output,generated_original_sha256:hash(originalBytes),mechanical_padding_px:e.mechanical_padding_px || 0,original_pixels_unchanged:true,dimensions:[info.width,info.height],transparent,partial,opaque,bounds,cornerAlpha:corners,target_png:"user_revision_v2/"+target,dds_exported:false});
    const bx=i*440;
    overview.push({input:label(e.label_fr),left:bx,top:4});
    overview.push({input:await sharp(bytes).resize(380,380).flatten({background:"#303436"}).png().toBuffer(),left:bx+30,top:50});
    overview.push({input:label("Lecture réduite : 32 / 48 / 64 px"),left:bx,top:445});
    let x=bx+15;
    for(const size of [32,48,64]) for(const bg of ["#443c30","#d8d1c1"]) { overview.push({input:await sharp(bytes).resize(size,size).flatten({background:bg}).png().toBuffer(),left:x,top:497}); x+=size+8; }
    checkerLayers.push({input:await sharp(checker,{raw:{width:256,height:256,channels:4}}).composite([{input:await sharp(bytes).resize(256,256).png().toBuffer()}]).png().toBuffer(),left:i*256,top:0});
    compare.push({input:label(e.label_fr,1280),left:0,top:i*240});
    const subjects=[{file:path.join(pack,e.source),name:"Ancienne proposition"},{file:source,name:"Version demandée"},...plan.style_references.slice(0,2).map((p,j)=>({file:path.join(root,p),name:plan.style_reference_labels[j]}))];
    for(const [j,s] of subjects.entries()) { compare.push({input:label(s.name,320),left:j*320,top:i*240+38}); for(const [b,bg] of ["#443c30","#d8d1c1"].entries()) compare.push({input:await sharp(s.file).resize(144,144).flatten({background:bg}).png().toBuffer(),left:j*320+8+b*152,top:i*240+80}); }
  }
  overview.push({input:label("Deux retouches proposées — aucune intégration au jeu.",880),left:0,top:570});
  await sharp({create:{width:880,height:610,channels:3,background:"#22282b"}}).composite(overview).png().toFile(path.join(rev,"APERCU.png"));
  await sharp({create:{width:1280,height:480,channels:3,background:"#22282b"}}).composite(compare).png().toFile(path.join(rev,"COMPARAISON.png"));
  await sharp({create:{width:512,height:256,channels:3,background:"white"}}).composite(checkerLayers).png().toFile(path.join(rev,"ALPHA_DAMIER.png"));
  const validation={status:"PASS_TECHNICAL_PREVIEW_CHECKS",mode:req.mode,protected_files:Object.keys(baseline).length,game_files_unchanged:true,game_tested:false,visual_review_required:true,approval_required_before_integration:true,third_proposal_only:true,results};
  write("preview_validation.json",validation);
  console.log(JSON.stringify(validation,null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
