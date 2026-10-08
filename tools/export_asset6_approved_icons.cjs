#!/usr/bin/env node
// Record the actual working-tree baseline and export explicitly approved petroleum icons.
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const {nativeIconDds}=require("./native_icon_dds.cjs");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const root=path.resolve(__dirname,".."),pack=path.join(root,"docs/reports/assets/asset6_preview_2026-10-02");
const keys=["refined_fuels","lubricants","heavy_petroleum_products","fractional_distillation_refinery","thermal_catalytic_cracking_refinery"];
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const write=(name,value)=>fs.writeFileSync(path.join(pack,name),JSON.stringify(value,null,2)+"\n");
const walk=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>{const p=path.join(dir,e.name);return e.isDirectory()?walk(p):[path.relative(root,p).replaceAll("\\","/")];});
const manifestPath=path.join(pack,"integration_manifest.json");

function prepare(){
  if(fs.existsSync(manifestPath))throw Error("Baseline already recorded; refusing to replace it.");
  const previews=JSON.parse(fs.readFileSync(path.join(pack,"preview_manifest.json"),"utf8"));
  const entries=keys.map(key=>{
    const e=previews.entries.find(row=>row.key===key);
    if(!e||fs.existsSync(path.join(root,e.target_dds)))throw Error("Unknown asset / existing target: "+key);
    const preview=key==="thermal_catalytic_cracking_refinery"?"previews/thermal_catalytic_cracking_refinery_v2_open_fire.png":e.preview;
    const digest=hash(fs.readFileSync(path.join(pack,preview)));
    if(key!=="thermal_catalytic_cracking_refinery"&&digest!==e.master_sha256)throw Error("Approved original changed: "+key);
    return {key,id:e.id,family:e.family,label:e.label_fr,definition:e.definition,field:"texture",previous_texture:e.current_texture,preview,source_sha256:digest,dds:e.target_dds,size:e.target_size,mips:e.mips};
  });
  const baseline=Object.fromEntries(["common","gfx"].flatMap(d=>walk(path.join(root,d))).sort().map(f=>[f,hash(fs.readFileSync(path.join(root,f)))]));
  const definitions=Object.fromEntries([...new Set(entries.map(e=>e.definition))].map(f=>[f,{sha256:baseline[f],text:fs.readFileSync(path.join(root,f),"utf8")} ]));
  write("integration_gameplay_and_gfx_baseline.json",baseline);
  write("integration_manifest.json",{date:"2026-10-03",mode:"BUILTIN_IMAGE_GEN",approval:{approved:true,user_request:"tu peut integré le rest",clarification:"je parle de la rafinierie",additional_requested_edit:"etre aussi transparent le noir autour du feu"},status:"APPROVED_FIVE_ICONS_AWAITING_EXPORT",protected_baseline:"integration_gameplay_and_gfx_baseline.json",definition_baseline:definitions,entries,excluded_pending_asset:"oil_refinery",technical_warning:"Generated near-opaque metal pixels can have alpha 250-254/255. The generated source alpha is preserved; no automatic artistic/alpha correction. The refinery preview remains outside this integration."});
  console.log(JSON.stringify({status:"BASELINE_RECORDED",count:entries.length,protected_files:Object.keys(baseline).length,pending:"oil_refinery"}));
}

function prepareRefinery(){
  const manifest=JSON.parse(fs.readFileSync(manifestPath,"utf8"));
  if(manifest.entries.length!==5||manifest.status!=="FIVE_ICONS_INTEGRATED_AND_STATICALLY_VALIDATED")throw Error("Expected the previously validated five-icon integration");
  const previews=JSON.parse(fs.readFileSync(path.join(pack,"preview_manifest.json"),"utf8"));
  const e=previews.entries.find(row=>row.key==="oil_refinery");
  if(!e||e.preview!=="previews/oil_refinery_v3_foreground_contrast.png"||fs.existsSync(path.join(root,e.target_dds)))throw Error("Unexpected refinery source / existing destination");
  const source=fs.readFileSync(path.join(pack,e.preview));
  if(hash(source)!==e.master_sha256)throw Error("The validated refinery preview changed");
  const archive=["integration_manifest.json","integration_export_validation.json","integration_static_validation.json","LOT_3_DDS_INTEGRES_QA.png"];
  for(const name of archive)if(fs.existsSync(path.join(pack,"five_icons_"+name)))throw Error("Previous integration already archived");
  const baseline=Object.fromEntries(["common","gfx"].flatMap(d=>walk(path.join(root,d))).sort().map(f=>[f,hash(fs.readFileSync(path.join(root,f)))]));
  for(const name of archive)fs.copyFileSync(path.join(pack,name),path.join(pack,"five_icons_"+name));
  manifest.entries.push({key:e.key,id:e.id,family:e.family,label:e.label_fr,definition:e.definition,field:"icon",previous_texture:e.current_texture,preview:e.preview,source_sha256:hash(source),dds:e.target_dds,size:e.target_size,mips:e.mips,opacity_note_accepted:true});
  manifest.definition_baseline=Object.fromEntries([...new Set(manifest.entries.map(row=>row.definition))].map(f=>[f,{sha256:baseline[f],text:fs.readFileSync(path.join(root,f),"utf8")} ]));
  manifest.protected_baseline="refinery_integration_gameplay_and_gfx_baseline.json";
  manifest.stage_allowed_changed=[e.definition];
  manifest.approval.refinery={approved:true,date:"2026-10-03",user_request:"Hop, c'est mieux, tu peux l'intégrer.",validated_source:e.preview,opacity_note_accepted:true};
  manifest.status="APPROVED_REFINERY_AWAITING_EXPORT";
  delete manifest.excluded_pending_asset;
  manifest.technical_warning="Source alpha is preserved, including the refinery's noted slight interior translucency (minimum 250/255 in the master), explicitly accepted with approval of the displayed version. No automatic recoloring or alpha correction.";
  write(manifest.protected_baseline,baseline);
  write("integration_manifest.json",manifest);
  console.log(JSON.stringify({status:"REFINERY_BASELINE_RECORDED",protected_files:Object.keys(baseline).length,source:e.preview,previous_five_integration_archived:true}));
}

async function exportIcons(onlyRefinery=false){
  const manifest=JSON.parse(fs.readFileSync(manifestPath,"utf8"));
  const expected=manifest.entries.length===6?[...keys,"oil_refinery"]:keys;
  if(!manifest.approval.approved||manifest.entries.length!==expected.length||new Set(manifest.entries.map(e=>e.key)).size!==expected.length||expected.some(k=>!manifest.entries.some(e=>e.key===k)))throw Error("Expected explicitly approved icons only");
  if(expected.length===6&&!manifest.approval.refinery?.approved)throw Error("Refinery approval missing");
  const selected=onlyRefinery?manifest.entries.filter(e=>e.key==="oil_refinery"):manifest.entries;
  if(onlyRefinery&&selected.length!==1)throw Error("Refinery has not been approved");
  const prepared=[];
  for(const e of selected){
    const source=fs.readFileSync(path.join(pack,e.preview));
    if(hash(source)!==e.source_sha256)throw Error("Source changed: "+e.key);
    const m=await sharp(source).metadata();
    if(!m.hasAlpha||m.width!==m.height||m.width<1024||e.size!==(e.family==="PM"?208:256))throw Error("Invalid dimensions: "+e.key);
    const base=await sharp(source).resize(e.size,e.size,{kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
    const levels=[];
    for(let size=e.size;size>=1;size>>=1)levels.push(await sharp(base,{raw:{width:e.size,height:e.size,channels:4}}).resize(size,size,{kernel:"lanczos3"}).raw().toBuffer());
    const header=Buffer.alloc(128);header.write("DDS ",0,"ascii");
    for(const [offset,value] of [[4,124],[8,0x2100f],[12,e.size],[16,e.size],[20,e.size*4],[28,levels.length],[76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]])header.writeUInt32LE(value,offset);
    const rawDds=Buffer.concat([header,...levels]);
    const dds=nativeIconDds(rawDds);
    if(levels.length!==e.mips||dds.length!==(e.size===208?230828:349652))throw Error("Invalid mip chain");
    const dest=path.resolve(root,e.dds);
    if(!dest.startsWith(path.join(root,"gfx")+path.sep))throw Error("Export outside gfx");
    if(fs.existsSync(dest)&&!fs.readFileSync(dest).equals(dds))throw Error("Refusing to overwrite different artwork: "+e.key);
    prepared.push({e,base,dds,dest});
  }
  fs.mkdirSync(path.join(pack,"integrated_target_png"),{recursive:true});
  const results=[];
  for(const {e,base,dds,dest} of prepared){
    fs.mkdirSync(path.dirname(dest),{recursive:true});
    if(!fs.existsSync(dest))fs.writeFileSync(dest,dds);
    const png=`integrated_target_png/${e.key}.png`;
    await sharp(base,{raw:{width:e.size,height:e.size,channels:4}}).png().toFile(path.join(pack,png));
    results.push({key:e.key,dds:e.dds,dds_sha256:hash(dds),source:e.preview,source_sha256:e.source_sha256,target_png:png,dimensions:[e.size,e.size],mips:e.mips,bytes:dds.length,format:"DDS BGRA8 native asset layout"});
  }
  const previous=onlyRefinery?JSON.parse(fs.readFileSync(path.join(pack,"integration_export_validation.json"),"utf8")).results:[];
  const combined=[...previous.filter(row=>!results.some(e=>e.key===row.key)),...results];
  combined.sort((a,b)=>expected.indexOf(a.key)-expected.indexOf(b.key));
  if(combined.length!==expected.length)throw Error("Missing export records");
  const status=expected.length===6?"PASS_SIX_DDS_EXPORTS":"PASS_FIVE_DDS_EXPORTS";
  write("integration_export_validation.json",{status,source_alpha_preserved:true,game_tested:false,results:combined});
  console.log(JSON.stringify({status,exported_this_run:results},null,2));
}

(async()=>{
  if(process.argv.length!==3)throw Error("Usage: export_asset6_approved_icons.cjs --prepare|--export|--prepare-refinery|--export-refinery");
  if(process.argv[2]==="--prepare")prepare();else if(process.argv[2]==="--prepare-refinery")prepareRefinery();else if(process.argv[2]==="--export")await exportIcons();else if(process.argv[2]==="--export-refinery")await exportIcons(true);else throw Error("Unknown action");
})().catch(e=>{console.error(e);process.exitCode=1;});
