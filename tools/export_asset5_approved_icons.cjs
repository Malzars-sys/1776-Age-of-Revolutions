#!/usr/bin/env node
// Format-only export of approved lot 2. No regeneration, recoloring or alpha correction.
"use strict";
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const { nativeIconDds } = require("./native_icon_dds.cjs");
const sharp = require(require.resolve("sharp", {paths:[__dirname, path.resolve(path.dirname(process.execPath), "..")]}));
const root = path.resolve(__dirname, "..");
const pack = path.join(root, "docs/reports/assets/asset5_preview_2026-10-02");
const manifest = JSON.parse(fs.readFileSync(path.join(pack, "integration_manifest.json"), "utf8"));
const hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const expectedKeys = ["phosphates", "phosphate_mine", "applied_mineralogy", "geological_surveying", "manual_ore_sorting", "ore_concentration"];
// Replacing existing art is opt-in, restricted to one explicitly re-approved key.
const args = process.argv.slice(2);
if (args.length > 1 || args.some(arg => !/^--replace=[a-z_]+$/.test(arg)))
  throw new Error("Usage: export_asset5_approved_icons.cjs [--replace=approved_key]");
const replacementKey = args.length ? args[0].slice("--replace=".length) : null;

(async () => {
  if (!manifest.approval.approved || manifest.entries.length !== 6 ||
      new Set(manifest.entries.map(e=>e.key)).size !== 6 ||
      expectedKeys.some(k=>!manifest.entries.some(e=>e.key===k)) ||
      new Set(manifest.entries.map(e=>e.dds)).size !== 6)
    throw new Error("Explicit six-asset approval required.");
  const selected = replacementKey ? manifest.entries.filter(e=>e.key===replacementKey) : manifest.entries;
  if (replacementKey && (selected.length !== 1 || !selected[0].replacement_approval?.approved))
    throw new Error("This exact asset has no explicit replacement approval.");
  const prepared = [];
  for (const entry of selected) {
    const source = fs.readFileSync(path.join(pack, entry.preview));
    if (hash(source) !== entry.source_sha256) throw new Error("Approved painting changed: " + entry.key);
    if (entry.key === "phosphate_mine" && entry.preview !== "previews/phosphate_mine_v4_sunrise.png")
      throw new Error("Only the approved sunrise variant may be exported.");
    const metadata = await sharp(source).metadata();
    if (!metadata.hasAlpha || metadata.width !== metadata.height || metadata.width < 1024)
      throw new Error("Invalid square RGBA master: " + entry.key);
    const size = entry.size;
    if (size !== (entry.family === "PM" ? 208 : 256)) throw new Error("Invalid native-size export.");
    const base = await sharp(source).resize(size,size,{kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
    let transparent=0, nearOpaque=0;
    for (let i=3; i<base.length; i+=4) {
      if (base[i] === 0) transparent++;
      if (base[i] >= 240) nearOpaque++;
    }
    if (!transparent || nearOpaque < size*size*.05) throw new Error("Missing exterior alpha / solid subject: " + entry.key);
    const levels=[];
    for (let n=size; n>=1; n>>=1) levels.push(await sharp(base,{raw:{width:size,height:size,channels:4}}).resize(n,n,{kernel:"lanczos3"}).raw().toBuffer());
    const header=Buffer.alloc(128);
    header.write("DDS ",0,"ascii");
    for (const [offset,value] of [[4,124],[8,0x2100f],[12,size],[16,size],[20,size*4],[28,levels.length],
      [76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]])
      header.writeUInt32LE(value,offset);
    const rawDds=Buffer.concat([header,...levels]);
    const dds=nativeIconDds(rawDds);
    if (levels.length !== entry.mips || dds.length !== (size===208 ? 230828 : 349652))
      throw new Error("Invalid mipmap payload: " + entry.key);
    const destination=path.join(root,entry.dds);
    if (!destination.startsWith(path.join(root,"gfx")+path.sep)) throw new Error("Export outside gfx.");
    if (fs.existsSync(destination) && !fs.readFileSync(destination).equals(dds)) {
      if (entry.key !== replacementKey || hash(fs.readFileSync(destination)) !== entry.replacement_approval.previous_dds_sha256)
        throw new Error("Refusing to overwrite different or unexpectedly changed art: " + entry.dds);
    }
    prepared.push({entry,base,dds,transparent,nearOpaque});
  }
  const results=[];
  for (const {entry,base,dds,transparent,nearOpaque} of prepared) {
    const destination=path.join(root,entry.dds);
    fs.mkdirSync(path.dirname(destination),{recursive:true});
    if (fs.existsSync(destination) && !fs.readFileSync(destination).equals(dds)) {
      const before = fs.readFileSync(destination);
      const backup = path.join(pack,"backups",`${entry.key}_before_${hash(before)}.dds`);
      fs.mkdirSync(path.dirname(backup),{recursive:true});
      if (fs.existsSync(backup) && !fs.readFileSync(backup).equals(before))
        throw new Error("Backup collision; original has not been replaced.");
      if (!fs.existsSync(backup)) fs.copyFileSync(destination,backup);
      fs.writeFileSync(destination,dds);
    } else if (!fs.existsSync(destination)) fs.writeFileSync(destination,dds);
    const png=`integrated_target_png/${entry.key}.png`;
    fs.mkdirSync(path.join(pack,"integrated_target_png"),{recursive:true});
    await sharp(base,{raw:{width:entry.size,height:entry.size,channels:4}}).png().toFile(path.join(pack,png));
    results.push({key:entry.key,id:entry.id,dds:entry.dds,target_png:png,source:entry.preview,source_sha256:entry.source_sha256,
      dds_sha256:hash(dds),dimensions:[entry.size,entry.size],mips:entry.mips,bytes:dds.length,
      transparent_pixels:transparent,near_opaque_pixels:nearOpaque,format:"DDS BGRA8 native asset layout",alpha_policy:"Unmodified source alpha; only native-size resampling and mip generation"});
  }
  const previousPath = path.join(pack,"integration_export_validation.json");
  const previousResults = replacementKey && fs.existsSync(previousPath) ? JSON.parse(fs.readFileSync(previousPath,"utf8")).results : [];
  const combined = [...previousResults.filter(r=>!results.some(n=>n.key===r.key)),...results];
  combined.sort((a,b)=>expectedKeys.indexOf(a.key)-expectedKeys.indexOf(b.key));
  const report={status:"PASS_EXPORT_WITH_DECLARED_OPACITY_WARNING",results:combined,warning:manifest.technical_warning,game_tested:false};
  fs.writeFileSync(path.join(pack,"integration_export_validation.json"),JSON.stringify(report,null,2)+"\n");
  console.log(JSON.stringify(replacementKey ? {status:"PASS_TARGETED_APPROVED_REPLACEMENT",results,game_tested:false} : report,null,2));
})().catch(error=>{console.error(error);process.exitCode=1;});
