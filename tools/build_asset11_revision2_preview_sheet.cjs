#!/usr/bin/env node
// Preview-only workflow: no master retouching, DDS export or gameplay writes.
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const root=path.resolve(__dirname,".."),pack=path.join(root,"docs/reports/assets/asset11_preview_2026-10-04/revision_2");
const plan=JSON.parse(fs.readFileSync(path.join(pack,"generation_plan.json"),"utf8"));
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const walk=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>{const p=path.join(dir,e.name);return e.isDirectory()?walk(p):[path.relative(root,p).replaceAll("\\","/")];});
const snapshot=()=>Object.fromEntries(["common","gfx"].flatMap(d=>walk(path.join(root,d))).map(p=>[p,hash(fs.readFileSync(path.join(root,p)))]));
const write=(name,value)=>fs.writeFileSync(path.join(pack,name),JSON.stringify(value,null,2)+"\n");
const esc=s=>s.replaceAll("&","&amp;").replaceAll("<","&lt;");
const label=(s,w=440,h=38)=>Buffer.from(`<svg width="${w}" height="${h}"><text x="10" y="27" fill="#eee5d4" font-family="Segoe UI" font-size="20">${esc(s)}</text></svg>`);

async function main(){
  if(plan.entries.length!==3||!plan.approval_required_before_integration)throw Error("Expected three approval-gated technology previews");
  if(process.argv[2]==="--prepare"){
    const baselineName=plan.protected_baseline||"gameplay_and_gfx_baseline.json";
    if(path.basename(baselineName)!==baselineName)throw Error("Baseline must be a filename inside the pack");
    const dest=path.join(pack,baselineName);
    if(fs.existsSync(dest))throw Error("Baseline already exists; do not overwrite");
    fs.mkdirSync(path.join(pack,"previews"),{recursive:true});
    fs.mkdirSync(path.join(pack,"target_size_png"),{recursive:true});
    for(const e of plan.entries)if(fs.existsSync(path.join(root,e.target_dds)))throw Error("Target already exists: "+e.target_dds);
    write(baselineName,snapshot());
    console.log("Prepared preview-only baseline; no game files changed.");return;
  }
  if(process.argv[2]!=="--verify")throw Error("Usage: --prepare or --verify");
  const baselineName=plan.protected_baseline||"gameplay_and_gfx_baseline.json";
  if(path.basename(baselineName)!==baselineName)throw Error("Baseline must be a filename inside the pack");
  const baseline=JSON.parse(fs.readFileSync(path.join(pack,baselineName),"utf8")),current=snapshot();
  const changed=Object.keys(baseline).filter(p=>current[p]!==baseline[p]),added=Object.keys(current).filter(p=>!(p in baseline));
  if(changed.length||added.length)throw Error("Protected game files changed: "+JSON.stringify({changed,added}));
  const board=[],compare=[],checkerLayers=[],results=[];
  const cellW=440,cellH=610,checkSize=256;
  const checker=Buffer.alloc(checkSize*checkSize*4);
  for(let y=0;y<checkSize;y++)for(let x=0;x<checkSize;x++){const k=(y*checkSize+x)*4,c=((x>>4)+(y>>4))%2?185:228;checker[k]=checker[k+1]=checker[k+2]=c;checker[k+3]=255;}
  for(const [i,e] of plan.entries.entries()){
    const source=path.join(pack,e.preview),bytes=fs.readFileSync(source),meta=await sharp(bytes).metadata();
    if(e.approved_sha256 && hash(bytes)!==e.approved_sha256)throw Error("Approved flags altered");
    if(!meta.hasAlpha||meta.width!==meta.height||meta.width<1024)throw Error("Invalid square alpha master: "+e.key);
    if(fs.existsSync(path.join(root,e.target_dds)))throw Error("Unapproved DDS exists: "+e.key);
    const {data,info}=await sharp(bytes).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    let transparent=0,partial=0,opaque=0;const bounds=[info.width,info.height,0,0];
    for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++){const a=data[(y*info.width+x)*4+3];if(a===0)transparent++;else if(a===255)opaque++;else partial++;if(a>=16){bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y);}}
    const cornerAlpha=[[0,0],[info.width-1,0],[0,info.height-1],[info.width-1,info.height-1]].map(([x,y])=>data[(y*info.width+x)*4+3]);
    if(!transparent||cornerAlpha.some(a=>a!==0))throw Error("Transparent exterior missing: "+e.key);
    const target=`target_size_png/${e.key}.png`;await sharp(bytes).resize(256,256).png().toFile(path.join(pack,target));
    const reduced=await sharp(path.join(pack,target)).ensureAlpha().raw().toBuffer();
    if([0,255,256*255,256*256-1].some(p=>reduced[p*4+3]!==0))throw Error("Reduced corners not transparent");
    results.push({key:e.key,source:e.preview,sha256:hash(bytes),dimensions:[info.width,info.height],transparent,partial,opaque,bounds,cornerAlpha,target_png:target,target_size:256,dds_exported:false});
    const bx=i*cellW;board.push({input:label(e.label_fr),left:bx,top:4});
    board.push({input:await sharp(bytes).resize(380,380).flatten({background:"#303436"}).png().toBuffer(),left:bx+30,top:50});
    board.push({input:label("Lecture réduite : 32 / 48 / 64 px"),left:bx,top:445});
    let x=bx+15;for(const size of [32,48,64])for(const bg of ["#443c30","#d8d1c1"]){board.push({input:await sharp(bytes).resize(size,size).flatten({background:bg}).png().toBuffer(),left:x,top:497});x+=size+8;}
    const checked=await sharp(checker,{raw:{width:256,height:256,channels:4}}).composite([{input:await sharp(bytes).resize(256,256).png().toBuffer()}]).png().toBuffer();checkerLayers.push({input:checked,left:i*256,top:0});
    compare.push({input:label(e.label_fr,1280),left:0,top:i*240});
    const subjects=[{file:source,name:"Nouveau"},...plan.style_references.map((p,j)=>({file:path.join(root,p),name:plan.style_reference_labels[j]}))];
    for(const [j,s] of subjects.entries()){compare.push({input:label(s.name,320),left:j*320,top:i*240+38});for(const [b,bg] of ["#443c30","#d8d1c1"].entries())compare.push({input:await sharp(s.file).resize(144,144,{fit:"contain"}).flatten({background:bg}).png().toBuffer(),left:j*320+8+b*152,top:i*240+80});}
  }
  board.push({input:label("Lot 8, révision 2 — drapeaux validés ; les deux coques restent à valider.",cellW*3),left:0,top:cellH-40});
  await sharp({create:{width:cellW*3,height:cellH,channels:3,background:"#22282b"}}).composite(board).png().toFile(path.join(pack,"LOT_8_APERCU.png"));
  await sharp({create:{width:1280,height:720,channels:3,background:"#22282b"}}).composite(compare).png().toFile(path.join(pack,"LOT_8_COMPARAISON_VANILLA.png"));
  await sharp({create:{width:768,height:256,channels:3,background:"white"}}).composite(checkerLayers).png().toFile(path.join(pack,"LOT_8_ALPHA_DAMIER.png"));
  write("preview_validation.json",{status:"PASS_TECHNICAL_PREVIEW_CHECKS",mode:plan.mode,protected_files:Object.keys(baseline).length,game_files_unchanged:true,game_tested:false,visual_review_required:true,approval_required_before_integration:true,results});
  write("preview_manifest.json",{...plan,status:"GENERATED_AWAITING_USER_APPROVAL",results});
  console.log(JSON.stringify({status:"PASS_TECHNICAL_PREVIEW_CHECKS",protected_files:Object.keys(baseline).length,results},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
