#!/usr/bin/env node
// Original petroleum previews: reductions, native comparison, alpha and protection checks.
"use strict";
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const sharp = require(require.resolve("sharp", {paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const root = path.resolve(__dirname,"..");
const pack = path.join(root,"docs/reports/assets/asset6_preview_2026-10-02");
const manifest = JSON.parse(fs.readFileSync(path.join(pack,"preview_manifest.json"),"utf8"));
const refs = JSON.parse(fs.readFileSync(path.join(pack,"native_references.json"),"utf8"));
const baseline = JSON.parse(fs.readFileSync(path.join(pack,"gameplay_and_gfx_baseline.json"),"utf8"));
const hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const esc = s => s.replaceAll("&","&amp;").replaceAll("<","&lt;");
const labels = (rows,w,h,size=18) => Buffer.from(`<svg width="${w}" height="${h}">${rows.map((s,i)=>`<text x="12" y="${size+6+i*(size+5)}" fill="#eee5d4" font-family="Segoe UI" font-size="${size}">${esc(s)}</text>`).join("")}</svg>`);
const nativeLabel = {oil:"Pétrole vanilla",engines:"Moteurs vanilla",steel:"Acier vanilla",building_chemical_plant:"Usine chimique vanilla",building_steel_mill:"Aciérie vanilla",pm_patent_stills:"Alambics brevetés vanilla",pm_open_hearth_process:"Four à sole vanilla"};
const walk = dir => fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>{const p=path.join(dir,e.name);return e.isDirectory()?walk(p):[path.relative(root,p).replaceAll("\\","/")];});

(async()=>{
  if(manifest.entries.length!==6 || manifest.approval_required_before_integration!==true) throw Error("Expected six approval-gated previews");
  const changed = Object.entries(baseline).filter(([file,h])=>!fs.existsSync(path.join(root,file))||hash(fs.readFileSync(path.join(root,file)))!==h).map(([file])=>file);
  const newGameFiles = ["common","gfx"].flatMap(d=>walk(path.join(root,d))).filter(p=>!(p in baseline));
  if(changed.length||newGameFiles.length) throw Error("Gameplay/textures changed during preview generation: "+JSON.stringify({changed,newGameFiles}));
  fs.mkdirSync(path.join(pack,"target_size_png"),{recursive:true});
  const board=[], comparisons=[], results=[], warnings=[];
  const cellW=450,cellH=550,qaW=1050,qaH=216;
  for(const [i,entry] of manifest.entries.entries()) {
    const bytes=fs.readFileSync(path.join(pack,entry.preview)), meta=await sharp(bytes).metadata();
    if(!meta.hasAlpha || meta.width!==meta.height || meta.width<1024) throw Error("Invalid master dimensions/alpha: "+entry.key);
    const {data,info}=await sharp(bytes).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    let transparent=0,partial=0,opaque=0,interiorTransparent=0,minInteriorAlpha=255;
    const bounds=[info.width,info.height,0,0];
    for(let y=0;y<info.height;y++) for(let x=0;x<info.width;x++) {
      const a=data[(y*info.width+x)*4+3];
      if(a===0) transparent++; else if(a===255) opaque++; else partial++;
      if(a>=16) {bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y);}
      if(x>info.width*.15&&x<info.width*.85&&y>info.height*.15&&y<info.height*.85) {minInteriorAlpha=Math.min(minInteriorAlpha,a);if(a!==255) interiorTransparent++;}
    }
    const cornerAlpha=[[0,0],[info.width-1,0],[0,info.height-1],[info.width-1,info.height-1]].map(([x,y])=>data[(y*info.width+x)*4+3]);
    if(!transparent || cornerAlpha.some(a=>a!==0)) throw Error("No genuine transparent exterior: "+entry.key);
    if(fs.existsSync(path.join(root,entry.target_dds))) throw Error("Unapproved target DDS exists: "+entry.key);
    if(entry.family==="BUILDING"&&interiorTransparent) warnings.push({key:entry.key,message:"Building interior not perfectly opaque; retain original master and require correction/explicit acceptance before integration.",minInteriorAlpha});
    const targetPng=`target_size_png/${entry.key}.png`;
    await sharp(bytes).resize(entry.target_size,entry.target_size).png().toFile(path.join(pack,targetPng));
    results.push({key:entry.key,sha256:hash(bytes),dimensions:[info.width,info.height],transparent,partial,opaque,cornerAlpha,bounds,interiorTransparent:entry.family==="BUILDING"?interiorTransparent:null,minInteriorAlpha:entry.family==="BUILDING"?minInteriorAlpha:null,target_png:targetPng,target_dds_exists:false});
    const x=(i%3)*cellW,y=Math.floor(i/3)*cellH;
    const title=entry.key==="thermal_catalytic_cracking_refinery"?["Craquage thermique","et catalytique"]:[entry.label_fr];
    board.push({input:labels(title,cellW,54,19),left:x,top:y+6});
    board.push({input:await sharp(bytes).resize(360,360).flatten({background:"#303436"}).png().toBuffer(),left:x+45,top:y+65});
    const sizes=entry.family==="BUILDING"?[48,64,96]:[32,48];
    let sx=8;
    for(const size of sizes) for(const bg of ["#443c30","#d8d1c1"]) {
      board.push({input:await sharp(bytes).resize(size,size).flatten({background:bg}).png().toBuffer(),left:x+sx,top:y+440});sx+=size+5;
    }
    comparisons.push({input:labels([entry.label_fr],qaW,32,16),left:0,top:i*qaH});
    const compare=[{file:path.join(pack,entry.preview),name:"Nouveau"},...refs.filter(r=>r.family===entry.family).slice(0,2).map(r=>({file:path.join(pack,r.preview),name:nativeLabel[r.id]}))];
    for(const [j,r] of compare.entries()) {
      const bx=j*340,by=i*qaH+36;
      comparisons.push({input:labels([r.name],330,28,13),left:bx,top:by});
      for(const [bgIndex,bg] of ["#443c30","#d8d1c1"].entries()) comparisons.push({input:await sharp(r.file).resize(128,128,{fit:"contain"}).flatten({background:bg}).png().toBuffer(),left:bx+8+bgIndex*143,top:by+28});
    }
  }
  board.push({input:labels(["Lot pétrole — six aperçus non intégrés, validation visuelle requise."],cellW*3,42,18),left:0,top:cellH*2});
  await sharp({create:{width:cellW*3,height:cellH*2+42,channels:3,background:"#22282b"}}).composite(board).png().toFile(path.join(pack,"LOT_3_APERCU.png"));
  await sharp({create:{width:qaW,height:qaH*6,channels:3,background:"#22282b"}}).composite(comparisons).png().toFile(path.join(pack,"LOT_3_COMPARAISON_VANILLA.png"));
  // Checkerboard inspection is diagnostic only; no master is retouched here.
  const checker=Buffer.alloc(256*256*4);
  for(let y=0;y<256;y++) for(let x=0;x<256;x++) {const c=((x>>4)+(y>>4))%2?190:230;const k=(y*256+x)*4;checker[k]=checker[k+1]=checker[k+2]=c;checker[k+3]=255;}
  const checkerLayers=[];
  for(const [i,e] of manifest.entries.entries()) {
    const combined=await sharp(checker,{raw:{width:256,height:256,channels:4}}).composite([{input:await sharp(path.join(pack,e.preview)).resize(256,256).png().toBuffer()}]).png().toBuffer();
    checkerLayers.push({input:combined,left:(i%3)*256,top:Math.floor(i/3)*256});
  }
  await sharp({create:{width:768,height:512,channels:3,background:"white"}}).composite(checkerLayers).png().toFile(path.join(pack,"LOT_3_ALPHA_DAMIER.png"));
  const status=warnings.length?"PREVIEWS_WITH_OPACITY_WARNING":"PASS_PNG_ALPHA_AND_NO_INTEGRATION";
  fs.writeFileSync(path.join(pack,"preview_validation.json"),JSON.stringify({status,mode:"BUILTIN_IMAGE_GEN",protected_files:Object.keys(baseline).length,game_files_unchanged:true,new_game_files:newGameFiles,visual_review_required:true,dds_export_allowed:false,warnings,results},null,2)+"\n");
  manifest.status="GENERATED_AWAITING_USER_APPROVAL";
  for(const e of manifest.entries) {e.status="GENERATED_AWAITING_USER_APPROVAL";e.master_sha256=results.find(r=>r.key===e.key).sha256;}
  fs.writeFileSync(path.join(pack,"preview_manifest.json"),JSON.stringify(manifest,null,2)+"\n");
  console.log(JSON.stringify({status,count:results.length,protected_files:Object.keys(baseline).length,warnings,images:results.map(r=>({key:r.key,dimensions:r.dimensions,cornerAlpha:r.cornerAlpha,minInteriorAlpha:r.minInteriorAlpha}))},null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
