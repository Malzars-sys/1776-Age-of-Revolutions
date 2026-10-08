#!/usr/bin/env node
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const {nativeIconDds}=require("./native_icon_dds.cjs");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const root=path.resolve(__dirname,".."),pack=path.join(root,"docs/reports/assets/asset12_preview_2026-10-04/revision_2");
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const write=(name,data)=>fs.writeFileSync(path.join(pack,name),JSON.stringify(data,null,2)+"\n");
const walk=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.relative(root,path.join(dir,e.name)).replaceAll("\\","/")]);
const expected=["condensing_steam_engines","rotative_steam_power","high_pressure_steam"];
const manifestFile=path.join(pack,"integration_manifest.json");
function prepare(){
  if(fs.existsSync(manifestFile))throw Error("Integration baseline already exists; refusing overwrite");
  const plan=JSON.parse(fs.readFileSync(path.join(pack,"generation_plan.json"),"utf8"));
  const proof=JSON.parse(fs.readFileSync(path.join(pack,"preview_validation.json"),"utf8"));
  if(plan.entries.length!==3||proof.status!=="PASS_TECHNICAL_PREVIEW_CHECKS")throw Error("Expected validated three-icon lot");
  const baseline=Object.fromEntries(["common","gfx"].flatMap(d=>walk(path.join(root,d))).sort().map(p=>[p,hash(fs.readFileSync(path.join(root,p)))]));
  const previewBaseline=JSON.parse(fs.readFileSync(path.join(pack,plan.protected_baseline),"utf8"));
  if(JSON.stringify(baseline)!==JSON.stringify(Object.fromEntries(Object.entries(previewBaseline).sort(([a],[b])=>a.localeCompare(b))))) {
    if(Object.keys(baseline).length!==Object.keys(previewBaseline).length||Object.entries(previewBaseline).some(([p,h])=>baseline[p]!==h))throw Error("Game files changed since approved preview");
  }
  const entries=expected.map(key=>{
    const e=plan.entries.find(x=>x.key===key),p=proof.results.find(x=>x.key===key);
    if(!e||!p||e.preview!==p.source||hash(fs.readFileSync(path.join(pack,e.preview)))!==p.sha256||fs.existsSync(path.join(root,e.target_dds)))throw Error("Unapproved source / occupied destination: "+key);
    return {key,id:key,label:e.label_fr,family:"TECH",definition:e.definition,field:"texture",previous_texture:e.current_texture,preview:e.preview,source_sha256:p.sha256,dds:e.target_dds,size:256,mips:9};
  });
  const approval=JSON.parse(fs.readFileSync(path.join(pack,"user_approval.json"),"utf8"));
  if(!approval.approved||approval.entries.length!==3||entries.some(e=>!approval.entries.some(a=>a.key===e.key&&a.preview===e.preview&&a.sha256===e.source_sha256)))throw Error("Missing exact approved master hashes");
  const definitions=Object.fromEntries([...new Set(entries.map(e=>e.definition))].map(p=>[p,{sha256:baseline[p],text:fs.readFileSync(path.join(root,p),"utf8")} ]));
  write("integration_gameplay_and_gfx_baseline.json",baseline);
  write("integration_manifest.json",{date:"2026-10-04",mode:"BUILTIN_IMAGE_GEN",status:"APPROVED_AWAITING_EXPORT",approval,protected_baseline:"integration_gameplay_and_gfx_baseline.json",definition_baseline:definitions,entries,game_tested:false});
  console.log(JSON.stringify({status:"BASELINE_RECORDED",count:entries.length,protected_files:Object.keys(baseline).length}));
}
async function exportIcons(){
  const m=JSON.parse(fs.readFileSync(manifestFile,"utf8"));
  if(!m.approval.approved||m.entries.length!==3||expected.some(k=>!m.entries.some(e=>e.key===k)))throw Error("Missing exact lot approval");
  const prepared=[];
  for(const e of m.entries){
    const source=fs.readFileSync(path.join(pack,e.preview));
    if(hash(source)!==e.source_sha256)throw Error("Approved master changed");
    const meta=await sharp(source).metadata();
    if(!meta.hasAlpha||meta.width!==meta.height||meta.width<1024)throw Error("Invalid square alpha master");
    const base=await sharp(source).resize(256,256,{kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
    const levels=[],mipHashes=[];
    for(let size=256;size>=1;size>>=1){const rgba=await sharp(base,{raw:{width:256,height:256,channels:4}}).resize(size,size,{kernel:"lanczos3"}).raw().toBuffer();levels.push(rgba);mipHashes.push({size,rgba_sha256:hash(rgba)});}
    const header=Buffer.alloc(128);header.write("DDS ",0,"ascii");
    for(const [o,v] of [[4,124],[8,0x2100f],[12,256],[16,256],[20,1024],[28,9],[76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]])header.writeUInt32LE(v,o);
    const dds=nativeIconDds(Buffer.concat([header,...levels]));
    const dest=path.resolve(root,e.dds);
    if(!dest.startsWith(path.join(root,"gfx")+path.sep)||dds.length!==349652)throw Error("Invalid export");
    if(fs.existsSync(dest)&&!fs.readFileSync(dest).equals(dds))throw Error("Refusing overwrite of different artwork");
    prepared.push({e,base,dds,dest,mipHashes});
  }
  fs.mkdirSync(path.join(pack,"integrated_target_png"),{recursive:true});
  const results=[];
  for(const {e,base,dds,dest,mipHashes} of prepared){
    if(!fs.existsSync(dest))fs.writeFileSync(dest,dds);
    const png="integrated_target_png/"+e.key+".png";
    await sharp(base,{raw:{width:256,height:256,channels:4}}).png().toFile(path.join(pack,png));
    results.push({key:e.key,dds:e.dds,dds_sha256:hash(dds),source:e.preview,source_sha256:e.source_sha256,target_png:png,dimensions:[256,256],mips:9,mip_hashes:mipHashes,format:"BGRA8 legacy native A8R8G8B8",bytes:dds.length});
  }
  write("integration_export_validation.json",{status:"PASS_THREE_NATIVE_DDS_EXPORTS",source_alpha_preserved:true,game_tested:false,results});
  console.log(JSON.stringify({status:"PASS_THREE_NATIVE_DDS_EXPORTS",count:results.length}));
}
(async()=>{if(process.argv[2]==="--prepare")prepare();else if(process.argv[2]==="--export")await exportIcons();else throw Error("Usage: --prepare|--export");})().catch(e=>{console.error(e);process.exitCode=1;});
