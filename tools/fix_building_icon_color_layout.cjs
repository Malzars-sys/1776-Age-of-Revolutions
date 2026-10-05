#!/usr/bin/env node
// Read-only diagnosis first, then lossless native-layout conversion of four exact DDS.
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const {nativeBuildingDds,RGBA,BGRA,masks}=require("./native_building_dds.cjs");
const root=path.resolve(__dirname,".."),pack=path.join(root,"docs/reports/assets/building_color_layout_2026-10-03");
const native="C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gfx/interface/icons/building_icons/coal_mine.dds";
const entries=[
  {key:"limestone_quarry",label:"Carrière de calcaire",dds:"gfx/interface/icons/building_icons/1776_limestone_quarry.dds",png:"docs/reports/assets/asset4_import_2026-10-01/masters/building_limestone_quarry.png"},
  {key:"research_laboratory",label:"Laboratoire expérimental",dds:"gfx/interface/icons/building_icons/1776_research_laboratory.dds",png:"docs/reports/assets/tech8c_research_laboratory_preview.png"},
  {key:"phosphate_mine",label:"Mine de phosphate",dds:"gfx/interface/icons/building_icons/1776_phosphate_mine.dds",png:"docs/reports/assets/asset5_preview_2026-10-02/integrated_target_png/phosphate_mine.png"},
  {key:"oil_refinery",label:"Raffinerie de pétrole",dds:"gfx/interface/icons/building_icons/1776_oil_refinery.dds",png:"docs/reports/assets/asset6_preview_2026-10-02/integrated_target_png/oil_refinery.png"}
];
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);return e.isDirectory()?walk(p):[path.relative(root,p).replaceAll("\\","/")];});
const snapshot=()=>Object.fromEntries(["common","gfx"].flatMap(d=>walk(path.join(root,d))).map(p=>[p,hash(fs.readFileSync(path.join(root,p)))]));
const write=(n,v)=>fs.writeFileSync(path.join(pack,n),JSON.stringify(v,null,2)+"\n");
function logicalRgba(dds,forceNative=false){
  const out=Buffer.from(dds.subarray(128));
  if(forceNative||masks(dds).join()===BGRA.join())for(let i=0;i<out.length;i+=4){const b=out[i];out[i]=out[i+2];out[i+2]=b;}
  else assert.deepEqual(masks(dds),RGBA);
  return out;
}
async function thumb(data,size){return sharp(data.subarray(0,256*256*4),{raw:{width:256,height:256,channels:4}}).resize(size,size).flatten({background:"#373c3d"}).png().toBuffer();}
async function sheet(rows,name){
  const layers=[],width=1050,rowH=315;
  const text=(s,w=1050)=>Buffer.from(`<svg width="${w}" height="40"><text x="10" y="28" fill="#eee5d4" font-family="Segoe UI" font-size="19">${s}</text></svg>`);
  layers.push({input:text("PNG validé / Ancien stockage lu en BGRA / DDS corrigé en BGRA"),left:0,top:0});
  for(const [i,r] of rows.entries()){
    layers.push({input:text(r.e.label),left:0,top:45+i*rowH});
    for(const [j,data] of [r.expected,r.oldNative,r.correctNative].entries()){
      layers.push({input:await thumb(data,240),left:20+j*350,top:85+i*rowH});
      layers.push({input:await thumb(data,48),left:275+j*350,top:185+i*rowH});
    }
  }
  await sharp({create:{width,height:45+rows.length*rowH,channels:3,background:"#22282b"}}).composite(layers).png().toFile(path.join(pack,name));
}
async function inspect(e,bytes){
  assert.equal(bytes.readUInt32LE(16),256);assert.equal(bytes.readUInt32LE(12),256);assert.equal(bytes.readUInt32LE(28),9);assert.equal(bytes.length,349652);
  const expected=await sharp(path.join(root,e.png)).resize(256,256,{fit:"contain",background:{r:0,g:0,b:0,alpha:0},kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
  const rgba=logicalRgba(bytes);assert.ok(rgba.subarray(0,expected.length).equals(expected),"DDS does not match approved PNG: "+e.key);
  const corrected=nativeBuildingDds(bytes);assert.ok(logicalRgba(corrected).equals(rgba),"Logical color changed");
  assert.ok(logicalRgba(corrected,true).equals(rgba),"Native byte interpretation differs");
  assert.ok(nativeBuildingDds(corrected).equals(corrected),"Not idempotent");
  return {e,expected,oldNative:logicalRgba(bytes,true),correctNative:logicalRgba(corrected,true),before:hash(bytes),after:hash(corrected),source_sha256:hash(fs.readFileSync(path.join(root,e.png))),corrected};
}
async function main(){
  const action=process.argv[2];if(!["--audit","--fix","--verify"].includes(action))throw Error("Usage: --audit|--fix|--verify");
  assert.deepEqual(masks(fs.readFileSync(native)),BGRA,"Installed native reference differs");
  fs.mkdirSync(pack,{recursive:true});
  if(action==="--audit"){
    if(fs.existsSync(path.join(pack,"diagnosis.json")))throw Error("Existing diagnosis must not be overwritten");
    const rows=[];for(const e of entries)rows.push(await inspect(e,fs.readFileSync(path.join(root,e.dds))));
    write("baseline.json",snapshot());
    write("diagnosis.json",{status:"CONFIRMED_LAYOUT_MISMATCH_PROBABLE_RENDERING_CAUSE",game_tested:false,native_reference:native,native_masks:BGRA,old_masks:RGBA,entries:rows.map(r=>({...r.e,before:r.before,after:r.after,source_sha256:r.source_sha256}))});
    await sheet(rows,"DIAGNOSTIC_ET_CORRECTION_PROPOSEE.png");
    console.log("Diagnosis saved: four DDS match approved PNGs but use non-native channel layout; no game file modified.");return;
  }
  const diagnosis=JSON.parse(fs.readFileSync(path.join(pack,"diagnosis.json"),"utf8")),baseline=JSON.parse(fs.readFileSync(path.join(pack,"baseline.json"),"utf8"));
  if(action==="--fix"){
    const current=snapshot();assert.deepEqual(current,baseline,"Files changed since diagnosis; stop instead of overwriting user work");
    const rows=[];for(const e of diagnosis.entries){const old=fs.readFileSync(path.join(root,e.dds));assert.equal(hash(old),e.before);const r=await inspect(e,old);assert.equal(r.after,e.after);rows.push(r);}
    fs.mkdirSync(path.join(pack,"backups"),{recursive:true});
    for(const r of rows){const backup=path.join(pack,"backups",`${r.e.key}_${r.before}.dds`);if(fs.existsSync(backup))assert.ok(fs.readFileSync(backup).equals(fs.readFileSync(path.join(root,r.e.dds))));else fs.copyFileSync(path.join(root,r.e.dds),backup);}
    for(const r of rows)fs.writeFileSync(path.join(root,r.e.dds),r.corrected);
  }
  const current=snapshot(),allowed=new Set(entries.map(e=>e.dds));assert.deepEqual(Object.keys(current).sort(),Object.keys(baseline).sort(),"Game files added or deleted");
  const changed=Object.keys(baseline).filter(p=>baseline[p]!==current[p]);assert.deepEqual(changed.sort(),[...allowed].sort(),"Unexpected game changes");
  const rows=[],results=[];
  for(const e of diagnosis.entries){
    const backup=fs.readFileSync(path.join(pack,"backups",`${e.key}_${e.before}.dds`)),now=fs.readFileSync(path.join(root,e.dds));assert.equal(hash(backup),e.before);assert.equal(hash(now),e.after);assert.deepEqual(masks(now),BGRA);
    assert.equal(hash(fs.readFileSync(path.join(root,e.png))),e.source_sha256,"Approved PNG changed");
    assert.ok(logicalRgba(backup).equals(logicalRgba(now)));assert.ok(logicalRgba(now,true).equals(logicalRgba(backup)));
    rows.push(await inspect(e,backup));
    results.push({...e,logical_rgba_identical_for_all_mips:true,alpha_identical_for_all_mips:true,native_masks_match:true,mips:9});
    await sharp(logicalRgba(now,true).subarray(0,256*256*4),{raw:{width:256,height:256,channels:4}}).png().toFile(path.join(pack,`${e.key}_dds_native_decoded.png`));
  }
  await sheet(rows,"DDS_CORRIGES_COMPARAISON.png");
  write("validation.json",{status:"PASS_LOSSLESS_NATIVE_BUILDING_LAYOUT",game_tested:false,probable_cause_reproduced_by_byte_interpretation:true,gameplay_unchanged:true,masters_unchanged:true,other_game_files_unchanged:Object.keys(baseline).length-changed.length,changed_files:changed,entries:results});
  console.log(JSON.stringify({status:"PASS_LOSSLESS_NATIVE_BUILDING_LAYOUT",changed_files:changed,other_game_files_unchanged:Object.keys(baseline).length-changed.length,logical_pixels_and_alpha_preserved:true,game_tested:false},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
