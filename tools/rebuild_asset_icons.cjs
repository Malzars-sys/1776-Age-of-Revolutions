"use strict";
// Deterministic export from preserved final masters. No AI generation or retouch.
// No tiny PNG variants: mipmaps remain inside the DDS. Default exports go to cache.
// Explicit --install-approved --asset=filename installs one hash-locked approved asset.
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const {nativeIconDds} = require("./native_icon_dds.cjs");
const sharp = require(require.resolve("sharp", {paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]}));
const root = path.resolve(__dirname, "..");
const registryPath = path.join(root, "docs/reports/assets/source_registry.json");
const cache = path.join(root, ".asset-cache");
const hash = b => crypto.createHash("sha256").update(b).digest("hex");
function inside(base, relative) {
  const p = path.resolve(base, relative), r = path.relative(base, p);
  if (!r || r.startsWith("..") || path.isAbsolute(r)) throw Error("Path outside expected directory: " + relative);
  return p;
}
async function encode(e) {
  const width=e.width??e.size, height=e.height??e.size;
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||height<1)throw Error("Invalid asset dimensions");
  const source = fs.readFileSync(inside(root, e.source));
  if (hash(source) !== e.source_sha256) throw Error("Master hash changed: " + e.source);
  let pipeline = sharp(source);
  if (e.crop) pipeline = pipeline.extract(e.crop);
  if (e.padding) pipeline = pipeline.extend({top:e.padding,bottom:e.padding,left:e.padding,right:e.padding,background:{r:0,g:0,b:0,alpha:0}});
  // Materialize preprocessing: Sharp otherwise applies extend after resize.
  if (e.crop || e.padding) pipeline = sharp(await pipeline.png().toBuffer());
  const base = await pipeline.resize(width, height, {fit: "contain", background: {r:0,g:0,b:0,alpha:0}, kernel: "lanczos3"}).ensureAlpha().raw().toBuffer();
  const levels = [];
  for (let w=width,h=height;;w=Math.max(1,w>>1),h=Math.max(1,h>>1)) {
    levels.push(await sharp(base, {raw: {width,height,channels:4}}).resize(w,h,{kernel:"lanczos3"}).raw().toBuffer());
    if(w===1&&h===1) break;
  }
  const h = Buffer.alloc(128); h.write("DDS ",0,"ascii");
  for (const [o,v] of [[4,124],[8,0x2100f],[12,height],[16,width],[20,width*4],[28,levels.length],[76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]]) h.writeUInt32LE(v,o);
  return nativeIconDds(Buffer.concat([h,...levels]));
}
async function discover() {
  const evidence = JSON.parse(fs.readFileSync(path.join(cache,"cleanup/evidence.json"),"utf8"));
  const entries=[], missing=[];
  for (const [dds,candidates] of Object.entries(evidence).sort(([a],[b])=>a.localeCompare(b))) {
    const runtime=fs.readFileSync(inside(path.join(root,"gfx"),path.relative(path.join(root,"gfx"),inside(root,dds))));
    const size=runtime.readUInt32LE(16), tried=new Set();
    let found;
    for (const c of candidates.sort((a,b)=>(a.key==="master"?-1:1)-(b.key==="master"?-1:1))) {
      const token=c.source+JSON.stringify(c.crop)+JSON.stringify(c.padding); if(tried.has(token)) continue; tried.add(token);
      const e={...c,size,mips:runtime.readUInt32LE(28)};
      if ((await encode(e)).equals(runtime)) {found=e; break;}
    }
    if (found) entries.push({dds,size,mips:found.mips,source:found.source,source_sha256:found.source_sha256,
      dds_sha256:hash(runtime),crop:found.crop || undefined,padding:found.padding || undefined,provenance:found.evidence});
    else missing.push({dds,candidates:[...tried]});
  }
  fs.writeFileSync(path.join(cache,"cleanup/discovery.json"),JSON.stringify({entries,missing},null,2)+"\n");
  if(missing.length) throw Error("Unresolved regeneration recipes: "+JSON.stringify(missing));
  fs.writeFileSync(registryPath,JSON.stringify({schema:1,description:"Final approved sources only; regenerated files belong in .asset-cache, not version control.",format:"native BGRA8 A8R8G8B8",entries},null,2)+"\n");
  console.log(JSON.stringify({status:"PASS_DISCOVERY",assets:entries.length,missing:0}));
}
async function main() {
  if(process.argv.includes("--discover-cache")) {await discover(); return;}
  const verify=process.argv.includes("--verify"), exportCache=process.argv.includes("--export-cache"), installApproved=process.argv.includes("--install-approved");
  if([verify,exportCache,installApproved].filter(Boolean).length!==1) throw Error("Usage: node tools/rebuild_asset_icons.cjs --verify|--export-cache|--install-approved [--asset=filename]");
  const select=process.argv.find(a=>a.startsWith("--asset="))?.slice(8);
  if(installApproved&&!select) throw Error("Installing an approved asset requires an exact --asset=filename selector");
  const registry=JSON.parse(fs.readFileSync(registryPath,"utf8"));
  const entries=registry.entries.filter(e=>!select||path.basename(e.dds,".dds")===select);
  if(!entries.length) throw Error("No matching registered asset");
  if(installApproved&&entries.length!==1) throw Error("Approved installation must resolve to exactly one asset");
  let verified=0;
  for(const e of entries) {
    const bytes=await encode(e), target=inside(root,e.dds);
    inside(path.join(root,"gfx"),path.relative(path.join(root,"gfx"),target));
    if(hash(bytes)!==e.dds_sha256) throw Error("Rebuild differs from approved DDS: "+e.dds);
    if(installApproved) {fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,bytes);}
    else if(!bytes.equals(fs.readFileSync(target))) throw Error("Current runtime file differs: "+e.dds);
    if(exportCache) {const out=inside(cache,"regenerated/"+e.dds);fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,bytes);}
    verified++;
  }
  console.log(JSON.stringify({status:"PASS_EXACT_REBUILD",assets:verified,runtime_modified:installApproved,
    output:exportCache?".asset-cache/regenerated/":null,per_mip_png_written:false}));
}
module.exports={encode};
if(require.main===module) main().catch(e=>{console.error(e);process.exitCode=1;});
