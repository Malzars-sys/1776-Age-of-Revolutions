"use strict";
// Exact corrected masters only. No generation, recolouring, or alpha cleanup.
// Default: stage three DDS. --install-approved installs this complete lot only.
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const {nativeIconDds} = require("./native_icon_dds.cjs");
const sharp = require(require.resolve("sharp", {paths:[__dirname,path.resolve(path.dirname(process.execPath),".."),process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES].filter(Boolean)}));
const root = path.resolve(__dirname,"..");
const pack = path.join(root,"docs/reports/assets/NAVAL_PM_ICONS_2026_11_08/revision_v2");
const hash = data => crypto.createHash("sha256").update(data).digest("hex");
const entries = [
  {key:"artisanal_shipbuilding", name:"Coque de bateau et herminette.png", bytes:662202,
   library_file_id:"libfile_c534b3feb5a4819190dbf19710b4b964", palette:"ochre",
   PM:"pm_1776_artisanal_shipbuilding", definition:"common/production_methods/01_industry.txt"},
  {key:"copper_sheathing", name:"Icône de coque violette en relief.png", bytes:564985,
   library_file_id:"libfile_c86c0896d3288191b8731200724646ad", palette:"purple",
   PM:"pm_copper_sheathing_building_shipyard", definition:"common/production_methods/13_tech6c5b_copper_production_and_consumers.txt"},
  {key:"no_copper_sheathing", name:"Icône de coque violette barrée.png", bytes:1210883,
   library_file_id:"libfile_de9bf3a72a0481919d61cafbe7d0d853", palette:"purple",
   PM:"pm_no_copper_sheathing_building_shipyard", definition:"common/production_methods/13_tech6c5b_copper_production_and_consumers.txt"}
];

async function encode(source) {
  const meta=await sharp(source).metadata();
  if(meta.width!==1254||meta.height!==1254||!meta.hasAlpha) throw Error("Expected original 1254px square alpha master");
  const base=await sharp(source).resize(208,208,{fit:"contain",background:{r:0,g:0,b:0,alpha:0},kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
  const levels=[];
  for(let size=208;;size=Math.max(1,size>>1)){
    levels.push(await sharp(base,{raw:{width:208,height:208,channels:4}}).resize(size,size,{kernel:"lanczos3"}).raw().toBuffer());
    if(size===1)break;
  }
  const header=Buffer.alloc(128);header.write("DDS ",0,"ascii");
  for(const [o,v]of [[4,124],[8,0x2100f],[12,208],[16,208],[20,832],[28,8],[76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]])header.writeUInt32LE(v,o);
  const dds=nativeIconDds(Buffer.concat([header,...levels]));
  if(dds.length!==230828)throw Error("Unexpected native DDS payload");
  return dds;
}

function bind(raw,key,texture){
  const pattern=new RegExp("(^|\\n)("+key+"\\s*=\\s*\\{[\\s\\S]*?\\n\\})");
  const match=raw.match(pattern);if(!match)throw Error("Missing PM "+key);
  const old=match[2];
  const changed=old.replace(/texture\s*=\s*"gfx\/error_deer\.dds"[^\r\n]*/,`texture = "${texture}"`);
  if(changed===old&&!old.includes(`texture = "${texture}"`))throw Error("Unexpected existing texture for "+key);
  return raw.replace(old,changed);
}

async function main(){
  const install=process.argv.includes("--install-approved");
  if(process.argv.length>2&&!install)throw Error("Usage: node tools/export_naval_pm_icons_20261108.cjs [--install-approved]");
  const prepared=[];
  // Resolve and validate every input before any runtime write.
  for(const entry of entries){
    const candidates=[path.join(pack,"masters",entry.key+".png"),path.join(pack,"masters",entry.name)];
    const source=candidates.find(p=>fs.existsSync(p));
    if(!source)throw Error("Corrected master missing: "+entry.name+" (never substitute rejected R1 artwork)");
    const bytes=fs.readFileSync(source);
    if(bytes.length!==entry.bytes)throw Error("Original master byte size differs: "+source);
    const dds=await encode(bytes);
    prepared.push({...entry,source:path.relative(root,source).replaceAll("\\","/"),source_sha256:hash(bytes),
      dds:"gfx/interface/icons/production_method_icons/1776_"+entry.key+"_paper.dds",dds_sha256:hash(dds),data:dds});
  }
  fs.mkdirSync(path.join(pack,"staged_dds"),{recursive:true});
  for(const entry of prepared)fs.writeFileSync(path.join(pack,"staged_dds",path.basename(entry.dds)),entry.data);
  const registryFile=path.join(root,"docs/reports/assets/source_registry.json");
  const registryBefore=fs.readFileSync(registryFile),registry=JSON.parse(registryBefore);
  const definitions=new Map();
  for(const entry of prepared){
    const p=path.join(root,entry.definition);
    if(!definitions.has(p)){const before=fs.readFileSync(p);definitions.set(p,{before,raw:before.toString("utf8")});}
    const item=definitions.get(p);item.raw=bind(item.raw,entry.PM,entry.dds);
    const existing=registry.entries.find(e=>e.dds===entry.dds);
    if(existing&&existing.dds_sha256!==entry.dds_sha256)throw Error("Registry artwork conflict");
    if(!existing)registry.entries.push({dds:entry.dds,size:208,mips:8,source:entry.source,
      source_sha256:entry.source_sha256,dds_sha256:entry.dds_sha256,
      provenance:"docs/reports/assets/NAVAL_PM_ICONS_2026_11_08/revision_v2/EXPORT.json"});
  }
  if(install){
    for(const entry of prepared){const dest=path.join(root,entry.dds);if(fs.existsSync(dest)&&hash(fs.readFileSync(dest))!==entry.dds_sha256)throw Error("Existing DDS differs");}
    for(const [p,item]of definitions)if(!fs.readFileSync(p).equals(item.before))throw Error("Concurrent PM edit");
    if(!fs.readFileSync(registryFile).equals(registryBefore))throw Error("Concurrent registry edit");
    for(const entry of prepared)fs.writeFileSync(path.join(root,entry.dds),entry.data);
    for(const [p,item]of definitions)fs.writeFileSync(p,item.raw,"utf8");
    fs.writeFileSync(registryFile,JSON.stringify(registry,null,2)+"\n","utf8");
  }
  const report={status:install?"IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION":"STAGED_THREE_ICONS",runtime_installed:install,
    format:"208x208 native BGRA8 A8R8G8B8; 8 complete mip levels",game_tested:false,
    entries:prepared.map(({data,...rest})=>rest)};
  fs.writeFileSync(path.join(pack,install?"EXPORT.json":"STAGED.json"),JSON.stringify(report,null,2)+"\n","utf8");
  console.log(JSON.stringify({status:report.status,count:prepared.length}));
}
main().catch(error=>{console.error(error.message);process.exitCode=1;});
