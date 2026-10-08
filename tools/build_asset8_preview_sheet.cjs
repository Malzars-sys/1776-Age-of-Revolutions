#!/usr/bin/env node
// Preview QA only: deterministic resizing/contact sheets, no artwork retouching or game writes.
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const root=path.resolve(__dirname,".."),pack=path.join(root,"docs/reports/assets/asset8_preview_2026-10-03");
const plan=JSON.parse(fs.readFileSync(path.join(pack,"generation_plan.json"),"utf8"));
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const walk=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>{const p=path.join(dir,e.name);return e.isDirectory()?walk(p):[path.relative(root,p).replaceAll("\\","/")];});
const snapshot=()=>Object.fromEntries(["common","gfx"].flatMap(d=>walk(path.join(root,d))).map(p=>[p,hash(fs.readFileSync(path.join(root,p)))]));
const write=(name,value)=>fs.writeFileSync(path.join(pack,name),JSON.stringify(value,null,2)+"\n");
const esc=s=>s.replaceAll("&","&amp;").replaceAll("<","&lt;");
const label=(s,w=440,h=36,font=19)=>Buffer.from(`<svg width="${w}" height="${h}"><text x="10" y="26" fill="#eee5d4" font-family="Segoe UI" font-size="${font}">${esc(s)}</text></svg>`);
async function main(){
  if(plan.entries.length!==6||!plan.approval_required_before_integration)throw Error("Expected six approval-gated previews");
  const baselineName=plan.protected_baseline;
  if(!baselineName||path.basename(baselineName)!==baselineName)throw Error("Invalid baseline filename");
  if(process.argv[2]==="--prepare"){
    if(fs.existsSync(path.join(pack,baselineName)))throw Error("Baseline already exists; do not overwrite");
    for(const e of plan.entries){
      if(fs.existsSync(path.join(root,e.target_dds)))throw Error("Target already exists: "+e.target_dds);
      if(!fs.readFileSync(path.join(root,e.definition),"utf8").includes(e.current_texture))throw Error("Current placeholder absent: "+e.key);
    }
    for(const d of ["previews","target_size_png"])fs.mkdirSync(path.join(pack,d),{recursive:true});
    write(baselineName,snapshot());console.log("Prepared current common/gfx baseline after requested technology changes; no game writes.");return;
  }
  if(process.argv[2]!=="--verify")throw Error("Usage: --prepare or --verify");
  const baseline=JSON.parse(fs.readFileSync(path.join(pack,baselineName),"utf8")),current=snapshot();
  const changed=Object.keys(baseline).filter(p=>current[p]!==baseline[p]),added=Object.keys(current).filter(p=>!(p in baseline));
  if(changed.length||added.length)throw Error("Protected files changed during previews: "+JSON.stringify({changed,added}));
  const board=[],compare=[],checkerLayers=[],results=[];
  const cellW=440,cellH=552,checkSize=256;
  const checker=Buffer.alloc(checkSize*checkSize*4);
  for(let y=0;y<checkSize;y++)for(let x=0;x<checkSize;x++){const k=(y*checkSize+x)*4,c=((x>>4)+(y>>4))%2?185:228;checker[k]=checker[k+1]=checker[k+2]=c;checker[k+3]=255;}
  for(const [i,e] of plan.entries.entries()){
    const source=path.join(pack,e.preview),bytes=fs.readFileSync(source),meta=await sharp(bytes).metadata();
    if(!meta.hasAlpha||meta.width!==meta.height||meta.width<1024)throw Error("Invalid square alpha master: "+e.key);
    if(fs.existsSync(path.join(root,e.target_dds)))throw Error("Unapproved DDS exists: "+e.key);
    const {data,info}=await sharp(bytes).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    let transparent=0,partial=0,opaque=0;const bounds=[info.width,info.height,0,0];
    let interiorMin=255;
    for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++){
      const a=data[(y*info.width+x)*4+3];if(a===0)transparent++;else if(a===255)opaque++;else partial++;
      if(a>=16){bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y);}
      if(e.family==="BUILDING"&&x>info.width*.16&&x<info.width*.84&&y>info.height*.16&&y<info.height*.84)interiorMin=Math.min(interiorMin,a);
    }
    const cornerAlpha=[[0,0],[info.width-1,0],[0,info.height-1],[info.width-1,info.height-1]].map(([x,y])=>data[(y*info.width+x)*4+3]);
    if(!transparent||cornerAlpha.some(a=>a!==0))throw Error("Transparent exterior missing: "+e.key);
    if(e.family==="BUILDING"&&interiorMin<240)throw Error("Building interior not opaque: "+interiorMin);
    const target=`target_size_png/${e.key}.png`,size=e.target_size;
    await sharp(bytes).resize(size,size).png().toFile(path.join(pack,target));
    const reduced=await sharp(path.join(pack,target)).ensureAlpha().raw().toBuffer();
    if([0,size-1,size*(size-1),size*size-1].some(p=>reduced[p*4+3]!==0))throw Error("Reduced corners not transparent: "+e.key);
    results.push({key:e.key,family:e.family,source:e.preview,sha256:hash(bytes),dimensions:[info.width,info.height],transparent,partial,opaque,bounds,cornerAlpha,...(e.family==="BUILDING"?{central_interior_alpha_min:interiorMin}:{}),target_png:target,target_size:size,dds_exported:false});
    const bx=(i%3)*cellW,by=Math.floor(i/3)*cellH;
    board.push({input:label(e.label_fr),left:bx,top:by+4});
    board.push({input:label(e.family+(e.era?" · "+e.era:""),440,30,15),left:bx,top:by+38});
    board.push({input:await sharp(bytes).resize(350,350).flatten({background:"#303436"}).png().toBuffer(),left:bx+45,top:by+74});
    board.push({input:label("32 / 48 / 64 px — fond sombre / clair",440,36,16),left:bx,top:by+430});
    let x=bx+15;for(const s of [32,48,64])for(const bg of ["#443c30","#d8d1c1"]){board.push({input:await sharp(bytes).resize(s,s).flatten({background:bg}).png().toBuffer(),left:x,top:by+474});x+=s+8;}
    const checked=await sharp(checker,{raw:{width:256,height:256,channels:4}}).composite([{input:await sharp(bytes).resize(256,256).png().toBuffer()}]).png().toBuffer();
    checkerLayers.push({input:checked,left:(i%3)*256,top:Math.floor(i/3)*256});
    compare.push({input:label(e.label_fr+" — "+e.family,960),left:0,top:i*240});
    const subjects=[{file:source,name:"Nouveau"},...plan.style_references[e.family].map((p,j)=>({file:path.join(root,p),name:"Référence vanilla "+(j+1)}))];
    for(const [j,s] of subjects.entries()){
      compare.push({input:label(s.name,320),left:j*320,top:i*240+38});
      for(const [b,bg] of ["#443c30","#d8d1c1"].entries())compare.push({input:await sharp(s.file).resize(144,144,{fit:"contain"}).flatten({background:bg}).png().toBuffer(),left:j*320+8+b*152,top:i*240+80});
    }
  }
  board.push({input:label("Lot 5 — aperçus uniquement : aucune intégration avant validation.",1320,42),left:0,top:cellH*2});
  await sharp({create:{width:1320,height:cellH*2+42,channels:3,background:"#22282b"}}).composite(board).png().toFile(path.join(pack,"LOT_5_APERCU.png"));
  await sharp({create:{width:960,height:1440,channels:3,background:"#22282b"}}).composite(compare).png().toFile(path.join(pack,"LOT_5_COMPARAISON_VANILLA.png"));
  await sharp({create:{width:768,height:512,channels:3,background:"white"}}).composite(checkerLayers).png().toFile(path.join(pack,"LOT_5_ALPHA_DAMIER.png"));
  write("preview_validation.json",{status:"PASS_TECHNICAL_PREVIEW_CHECKS",mode:plan.mode,protected_files:Object.keys(baseline).length,game_files_unchanged:true,game_tested:false,visual_review_required:true,approval_required_before_integration:true,results});
  write("preview_manifest.json",{...plan,status:"GENERATED_AWAITING_USER_APPROVAL",results});
  console.log(JSON.stringify({status:"PASS_TECHNICAL_PREVIEW_CHECKS",protected_files:Object.keys(baseline).length,results},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
