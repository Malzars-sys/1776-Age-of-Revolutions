#!/usr/bin/env node
// Audit all affected export families before a lossless, backed-up format migration.
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const {nativeIconDds,RGBA,BGRA,masks}=require("./native_icon_dds.cjs");
const root=path.resolve(__dirname,".."),report="docs/reports/assets/all_asset_color_layout_2026-10-03",pack=path.join(root,report);
const nativeRoot="C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game";
const references={
  GOODS:"gfx/interface/icons/goods_icons/aeroplanes.dds",
  TECH:"gfx/interface/icons/invention_icons/academia.dds",
  PM:"gfx/interface/icons/production_method_icons/aeroplanes.dds",
  UNIT:"gfx/unit_illustrations/artillery_african_cannon.dds",
  BUILDING:"gfx/interface/icons/building_icons/coal_mine.dds"
};
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const read=p=>fs.readFileSync(path.join(root,p));
const json=p=>JSON.parse(read(p).toString("utf8"));
const relative=p=>path.relative(root,p).replaceAll("\\","/");
const family=p=>p.includes("goods_icons/")?"GOODS":p.includes("invention_icons/")?"TECH":p.includes("production_method_icons/")?"PM":p.includes("unit_illustrations/")?"UNIT":"BUILDING";
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);return e.isDirectory()?walk(p):[relative(p)];});
function snapshot(){return Object.fromEntries(["common","gfx","events","gui","localization","map"].filter(d=>fs.existsSync(path.join(root,d))).flatMap(d=>walk(path.join(root,d))).map(p=>[p,hash(read(p))]));}
const write=(name,value)=>fs.writeFileSync(path.join(pack,name),JSON.stringify(value,null,2)+"\n");
function rgba(bytes,forceNative=false){
  const data=Buffer.from(bytes.subarray(128));
  if(forceNative||masks(bytes).join()===BGRA.join())for(let i=0;i<data.length;i+=4){const b=data[i];data[i]=data[i+2];data[i+2]=b;}
  else assert.deepEqual(masks(bytes),RGBA);
  return data;
}
function historicalHashMatches(bytes,expected){
  if(!expected)return true;
  if(hash(bytes)===expected.toLowerCase())return true;
  assert.deepEqual(masks(bytes),BGRA);
  const old=Buffer.from(bytes);for(const [i,offset] of [92,96,100,104].entries())old.writeUInt32LE(RGBA[i],offset);
  rgba(bytes).copy(old,128);
  return hash(old)===expected.toLowerCase();
}
function collect(){
  const entries=[],a4="docs/reports/assets/asset4_import_2026-10-01";
  const manifest=json(a4+"/manifest.json");
  for(const e of json(a4+"/export_validation.json").results){
    entries.push({key:e.id,label:manifest.entries.find(x=>x.id===e.id).label,dds:e.output,png:e.master,
      export_hash:e.sha256,pinned_sources:[{path:e.source,sha256:e.sourceSha256},{path:e.master,sha256:e.masterSha256}]});
  }
  for(const e of json(a4+"/approved_unit_export_validation.json").results){
    entries.push({key:e.key,label:e.key,dds:e.target_dds,png:e.preview,export_hash:e.export_sha256,pinned_sources:[{path:e.preview,sha256:e.sha256}]});
  }
  for(const name of ["asset5_preview_2026-10-02","asset6_preview_2026-10-02"]){
    const folder="docs/reports/assets/"+name,manifest=json(folder+"/integration_manifest.json");
    for(const e of json(folder+"/integration_export_validation.json").results){
      const png=relative(path.resolve(root,folder,e.target_png)),source=relative(path.resolve(root,folder,e.source));
      entries.push({key:e.key,label:manifest.entries.find(x=>x.key===e.key).label,dds:e.dds,png,export_hash:e.dds_sha256,
        pinned_sources:[{path:source,sha256:e.source_sha256},{path:png,sha256:hash(read(png))}]});
    }
  }
  for(const e of json("docs/reports/assets/tech8c_laboratory_pm_icons.json").entries){
    entries.push({key:"laboratory_"+e.name,label:e.label,dds:e.output,png:e.cutout,pinned_sources:[
      {path:e.source,sha256:e.sourceSha256},{path:e.cutout,sha256:e.cutoutSha256}]});
  }
  const lab=json("docs/reports/assets/building_color_layout_2026-10-03/diagnosis.json").entries.find(x=>x.key==="research_laboratory");
  entries.push({key:lab.key,label:lab.label,dds:lab.dds,png:lab.png,export_hash:lab.before,pinned_sources:[{path:lab.png,sha256:lab.source_sha256}]});
  assert.equal(entries.length,42);assert.equal(new Set(entries.map(e=>e.dds)).size,42);assert.equal(new Set(entries.map(e=>e.key)).size,42);
  for(const e of entries){
    assert.ok(e.dds.startsWith("gfx/")&&!e.dds.includes("..")&&path.basename(e.dds).startsWith("1776_"));
    e.family=family(e.dds);
    for(const source of e.pinned_sources){assert.ok(source.path.startsWith("docs/reports/assets/")&&!source.path.includes(".."));assert.equal(hash(read(source.path)),source.sha256.toLowerCase(),"Approved source changed: "+source.path);}
  }
  return entries;
}
function inventory(){
  const rows=[];
  for(const p of walk(path.join(root,"gfx")).filter(p=>p.endsWith(".dds"))){
    const fd=fs.openSync(path.join(root,p),"r"),header=Buffer.alloc(128);let size;try{size=fs.readSync(fd,header,0,128,0);}finally{fs.closeSync(fd);}
    if(size===128&&header.toString("ascii",0,4)==="DDS "&&header.readUInt32LE(80)===0x41&&header.readUInt32LE(88)===32){
      rows.push({dds:p,masks:masks(header),width:header.readUInt32LE(16),height:header.readUInt32LE(12),mips:header.readUInt32LE(28)});
    }
  }
  return rows;
}
async function inspect(e,bytes){
  assert.ok(historicalHashMatches(bytes,e.export_hash),"Historical export changed: "+e.dds);
  const size=bytes.readUInt32LE(16),count=bytes.readUInt32LE(28),corrected=nativeIconDds(bytes),pixels=rgba(bytes);
  const expected=await sharp(read(e.png)).resize(size,size,{fit:"contain",background:{r:0,g:0,b:0,alpha:0},kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
  assert.ok(pixels.subarray(0,expected.length).equals(expected),"Approved PNG pixel mismatch: "+e.dds);
  assert.ok(rgba(corrected).equals(pixels)&&rgba(corrected,true).equals(pixels),"Pixel or alpha change: "+e.dds);
  assert.ok(nativeIconDds(corrected).equals(corrected),"Conversion must be idempotent");
  return {...e,size,mips:count,bytes:bytes.length,before:hash(bytes),after:hash(corrected),changed:!bytes.equals(corrected),
    expected,old_native:rgba(bytes,true),new_native:rgba(corrected,true),corrected};
}
const clean=r=>{const {expected,old_native,new_native,corrected,...record}=r;return record;};
const escape=s=>s.replaceAll("&","&amp;").replaceAll("<","&lt;");
async function tile(pixels,size,out){return sharp(pixels.subarray(0,size*size*4),{raw:{width:size,height:size,channels:4}}).resize(out,out).flatten({background:"#3b3630"}).png().toBuffer();}
async function sheets(rows){
  const sampleKeys=["limestone","cement","hydraulic_cements","stone_crushing_screening","lubricants","laboratory_manual"];
  const examples=sampleKeys.map(key=>rows.find(r=>r.key===key)).filter(Boolean);
  examples.push(rows.find(r=>r.family==="UNIT"));
  const text=(s,width=1020)=>Buffer.from(`<svg width="${width}" height="36"><text x="12" y="25" fill="#f2e8d4" font-family="Segoe UI" font-size="18">${escape(s)}</text></svg>`);
  const layers=[{input:text("PNG approuvé — Ancien stockage lu en BGRA (simulation) — DDS corrigé"),left:0,top:0}];
  for(const [i,r] of examples.entries()){
    layers.push({input:text(r.label),left:0,top:40+i*265});
    for(const [j,p] of [r.expected,r.old_native,r.new_native].entries()){
      layers.push({input:await tile(p,r.size,190),left:30+j*340,top:80+i*265});
      layers.push({input:await tile(p,r.size,48),left:245+j*340,top:155+i*265});
    }
  }
  await sharp({create:{width:1020,height:40+examples.length*265,channels:3,background:"#22282b"}}).composite(layers).png().toFile(path.join(pack,"COMPARAISON_COULEURS.png"));
  const gallery=[];
  for(const [i,r] of rows.entries()){
    const x=i%6*210,y=Math.floor(i/6)*235;
    gallery.push({input:await tile(r.new_native,r.size,175),left:x+17,top:y+40});
    gallery.push({input:text(r.key.slice(0,23),210),left:x,top:y});
  }
  await sharp({create:{width:1260,height:Math.ceil(rows.length/6)*235,channels:3,background:"#22282b"}}).composite(gallery).png().toFile(path.join(pack,"TOUS_LES_DDS_CORRIGES.png"));
}
async function main(){
  const action=process.argv[2];assert.ok(["--audit","--fix","--verify"].includes(action),"Usage: --audit|--fix|--verify");
  const nativeReferences=Object.fromEntries(Object.entries(references).map(([group,p])=>{
    const bytes=fs.readFileSync(path.join(nativeRoot,p));assert.deepEqual(masks(bytes),BGRA,"Native reference differs: "+group);
    return [group,{path:path.join(nativeRoot,p),masks:masks(bytes),sha256:hash(bytes)}];
  }));
  fs.mkdirSync(pack,{recursive:true});
  if(action==="--audit"){
    assert.ok(!fs.existsSync(path.join(pack,"diagnosis.json")),"Do not overwrite initial diagnosis");
    const rows=[];for(const e of collect())rows.push(await inspect(e,read(e.dds)));
    const inv=inventory(),remaining=inv.filter(e=>e.masks.join()===RGBA.join()).map(e=>e.dds).sort();
    assert.deepEqual(remaining,rows.filter(r=>r.changed).map(r=>r.dds).sort(),"Uninventoried RGBA assets: stop");
    assert.equal(remaining.length,38);assert.equal(rows.filter(r=>!r.changed).length,4);
    write("baseline.json",snapshot());write("diagnosis.json",{status:"CONFIRMED_ALL_FAMILY_EXPORT_LAYOUT_MISMATCH",game_tested:false,
      native_references:nativeReferences,inventory:inv,entries:rows.map(clean)});
    await sheets(rows);console.log(JSON.stringify({status:"AUDIT_COMPLETE_NO_GAME_FILES_CHANGED",remaining:38,already_corrected_buildings:4}));return;
  }
  const diagnosis=json(report+"/diagnosis.json"),baseline=json(report+"/baseline.json"),rows=[];
  if(action==="--fix")assert.deepEqual(snapshot(),baseline,"Game files changed since audit; stop");
  for(const e of diagnosis.entries){
    for(const source of e.pinned_sources)assert.equal(hash(read(source.path)),source.sha256.toLowerCase(),"Approved source changed");
    const original=e.changed&&action!=="--fix"?fs.readFileSync(path.join(pack,"backups",`${e.key}_${e.before}.dds`)):read(e.dds);
    assert.equal(hash(original),e.before);const r=await inspect(e,original);assert.equal(r.after,e.after);rows.push(r);
  }
  if(action==="--fix"){
    fs.mkdirSync(path.join(pack,"backups"),{recursive:true});
    for(const r of rows.filter(r=>r.changed)){
      const backup=path.join(pack,"backups",`${r.key}_${r.before}.dds`);
      if(fs.existsSync(backup))assert.equal(hash(fs.readFileSync(backup)),r.before);else fs.copyFileSync(path.join(root,r.dds),backup);
    }
    for(const r of rows.filter(r=>r.changed))fs.writeFileSync(path.join(root,r.dds),r.corrected);
  }
  const current=snapshot();assert.deepEqual(Object.keys(current).sort(),Object.keys(baseline).sort(),"Game files added/deleted");
  const changed=Object.keys(current).filter(p=>current[p]!==baseline[p]);assert.deepEqual(changed.sort(),rows.filter(r=>r.changed).map(r=>r.dds).sort(),"Unexpected game changes");
  for(const r of rows){
    const now=read(r.dds);assert.equal(hash(now),r.after);assert.deepEqual(masks(now),BGRA);assert.ok(rgba(now,true).equals(rgba(r.corrected)));
    await sharp(rgba(now,true).subarray(0,r.size*r.size*4),{raw:{width:r.size,height:r.size,channels:4}}).png().toFile(path.join(pack,`${r.key}_native_decoded.png`));
  }
  assert.deepEqual(inventory().filter(e=>e.masks.join()===RGBA.join()),[],"Remaining legacy RGBA export");
  await sheets(rows);
  const counts={};for(const r of rows.filter(r=>r.changed))counts[r.family]=(counts[r.family]||0)+1;
  write("validation.json",{status:"PASS_ALL_FAMILIES_LOSSLESS_NATIVE_LAYOUT",game_tested:false,converted:changed.length,
    already_corrected_buildings:4,family_counts:counts,gameplay_unchanged:true,other_game_files_unchanged:Object.keys(current).length-changed.length,
    source_colors_and_alpha_unchanged:true,changed_files:changed,entries:rows.map(r=>({...clean(r),all_mips_logically_identical:true}))});
  console.log(JSON.stringify({status:"PASS_ALL_FAMILIES_LOSSLESS_NATIVE_LAYOUT",converted:changed.length,family_counts:counts,
    other_game_files_unchanged:Object.keys(current).length-changed.length,remaining_rgba_exports:0,game_tested:false},null,2));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
