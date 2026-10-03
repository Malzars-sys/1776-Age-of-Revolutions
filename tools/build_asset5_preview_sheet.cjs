#!/usr/bin/env node
// Preview-only reductions, comparison boards, alpha QA and no-integration check.
"use strict";
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const sharp = require(require.resolve("sharp", { paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")] }));
const root = path.resolve(__dirname, "..");
const pack = path.join(root, "docs/reports/assets/asset5_preview_2026-10-02");
const manifest = JSON.parse(fs.readFileSync(path.join(pack, "preview_manifest.json"), "utf8"));
const refs = JSON.parse(fs.readFileSync(path.join(pack, "native_references.json"), "utf8"));
const baseline = JSON.parse(fs.readFileSync(path.join(pack, "gameplay_and_gfx_baseline.json"), "utf8"));
const hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const esc = s => s.replaceAll("&", "&amp;").replaceAll("<", "&lt;");
const label = (s, w, h, size = 18) => Buffer.from(`<svg width="${w}" height="${h}"><text x="10" y="${size + 9}" fill="#eee5d4" font-family="Segoe UI" font-size="${size}">${esc(s)}</text></svg>`);
const nativeLabel = {
  coal: "Charbon vanilla", iron: "Fer vanilla", mechanical_tools: "Outils mécaniques vanilla", academia: "Monde académique vanilla",
  building_coal_mine: "Mine de charbon vanilla", building_iron_mine: "Mine de fer vanilla",
  pm_picks_and_shovels_building_coal_mine: "Pics et pelles vanilla", pm_atmospheric_engine_pump_building_coal_mine: "Pompe atmosphérique vanilla"
};

(async () => {
  if (manifest.entries.length !== 6 || manifest.approval_required_before_integration !== true)
    throw new Error("Expected exactly six approval-gated previews.");
  const unchanged = Object.entries(baseline).every(([file, expected]) => {
    const p = path.join(root, file);
    return fs.existsSync(p) && hash(fs.readFileSync(p)) === expected;
  });
  const walk = dir => fs.readdirSync(dir, {withFileTypes: true}).flatMap(e => {
    const p = path.join(dir, e.name); return e.isDirectory() ? walk(p) : [path.relative(root, p).replaceAll("\\", "/")];
  });
  const newGameFiles = ["common", "gfx"].flatMap(d => walk(path.join(root, d))).filter(p => !(p in baseline));
  if (!unchanged || newGameFiles.length) throw new Error("Game definitions/textures changed during preview generation.");
  fs.mkdirSync(path.join(pack, "target_size_png"), {recursive: true});
  const board = [], comparisons = [], results = [];
  const cellW = 460, cellH = 550, qaW = 1050, qaH = 212;
  for (const [i, entry] of manifest.entries.entries()) {
    const bytes = fs.readFileSync(path.join(pack, entry.preview));
    const metadata = await sharp(bytes).metadata();
    const {data, info} = await sharp(bytes).ensureAlpha().raw().toBuffer({resolveWithObject: true});
    if (!metadata.hasAlpha || metadata.width !== metadata.height || metadata.width < 1024)
      throw new Error("Invalid master dimensions/alpha: " + entry.key);
    let transparent = 0, partial = 0, opaque = 0, interiorTransparent = 0;
    const bounds = [info.width, info.height, 0, 0];
    for (let y=0; y<info.height; y++) for (let x=0; x<info.width; x++) {
      const a=data[(y*info.width+x)*4+3];
      if(a===0) transparent++; else if(a===255) opaque++; else partial++;
      if(a>=16) {bounds[0]=Math.min(bounds[0],x); bounds[1]=Math.min(bounds[1],y); bounds[2]=Math.max(bounds[2],x); bounds[3]=Math.max(bounds[3],y);}
      if(x>info.width*.15 && x<info.width*.85 && y>info.height*.15 && y<info.height*.85 && a!==255) interiorTransparent++;
    }
    const cornerAlpha = [[0,0],[info.width-1,0],[0,info.height-1],[info.width-1,info.height-1]].map(([x,y])=>data[(y*info.width+x)*4+3]);
    if (!transparent || cornerAlpha.some(a=>a!==0)) throw new Error("Background is not genuine transparent alpha: " + entry.key);
    const fullSceneOpacityPass = entry.family === "BUILDING" ? interiorTransparent === 0 : null;
    const targetPng = `target_size_png/${entry.key}.png`;
    await sharp(bytes).resize(entry.target_size, entry.target_size).png().toFile(path.join(pack,targetPng));
    results.push({key:entry.key,sha256:hash(bytes),dimensions:[info.width,info.height],transparent,partial,opaque,cornerAlpha,bounds,interiorTransparent:entry.family==="BUILDING"?interiorTransparent:null,full_scene_opacity_pass:fullSceneOpacityPass,target_png:targetPng,target_dds_exists:fs.existsSync(path.join(root,entry.target_dds))});
    if(results.at(-1).target_dds_exists) throw new Error("An unapproved target DDS exists: " + entry.key);
    const x=(i%3)*cellW, y=Math.floor(i/3)*cellH;
    board.push({input:label(entry.label_fr,cellW,40),left:x,top:y});
    board.push({input:label(entry.family==="PM"?"Méthode de production":entry.family==="GOOD"?"Bien":entry.family==="TECH"?"Technologie":"Bâtiment",cellW,28,13),left:x,top:y+33});
    board.push({input:await sharp(bytes).resize(370,370).flatten({background:"#303436"}).png().toBuffer(),left:x+45,top:y+63});
    const sizes=entry.family==="BUILDING"?[48,64,96]:entry.family==="TECH"?[48,64]:[32,48];
    let sx=8;
    for(const size of sizes) {
      for(const bg of ["#443c30","#d8d1c1"]) {
        board.push({input:await sharp(bytes).resize(size,size).flatten({background:bg}).png().toBuffer(),left:x+sx,top:y+440});
        sx+=size+5;
      }
    }
    comparisons.push({input:label(entry.label_fr,qaW,32,16),left:0,top:i*qaH});
    const compareFiles=[{file:path.join(pack,entry.preview),name:"Nouveau"},...refs.filter(r=>r.family===entry.family).slice(0,2).map(r=>({file:path.join(pack,r.preview),name:nativeLabel[r.id]||r.id}))];
    for(const [j,r] of compareFiles.entries()) {
      const bx=j*340, by=i*qaH+36;
      comparisons.push({input:label(r.name,330,28,13),left:bx,top:by});
      for(const [b,bg] of ["#443c30","#d8d1c1"].entries()) comparisons.push({input:await sharp(r.file).resize(128,128,{fit:"contain"}).flatten({background:bg}).png().toBuffer(),left:bx+8+b*143,top:by+28});
    }
  }
  // Keep the building's larger QA samples clear of the row boundary.
  const deliveryH = cellH*2+42;
  board.push({input:label("Aperçus non intégrés — mine : opacité intérieure à finaliser avant export.",cellW*3,40,16),left:0,top:cellH*2});
  await sharp({create:{width:cellW*3,height:deliveryH,channels:3,background:"#22282b"}}).composite(board).png().toFile(path.join(pack,"LOT_2_APERCU.png"));
  await sharp({create:{width:qaW,height:qaH*6,channels:3,background:"#22282b"}}).composite(comparisons).png().toFile(path.join(pack,"LOT_2_COMPARAISON_VANILLA.png"));
  const warnings = results.filter(r=>r.full_scene_opacity_pass===false).map(r=>({key:r.key,message:"Building interior is still slightly translucent; exact opaque interior required before DDS export."}));
  const status = warnings.length ? "PREVIEWS_READY_WITH_BUILDING_OPACITY_WARNING" : "PASS_PNG_ALPHA_AND_NO_INTEGRATION";
  fs.writeFileSync(path.join(pack,"preview_validation.json"),JSON.stringify({status,mode:"BUILTIN_IMAGE_GEN",game_files_unchanged:unchanged,protected_files:Object.keys(baseline).length,new_game_files:newGameFiles,visual_review_required:true,dds_export_allowed:false,warnings,results},null,2)+"\n");
  console.log(JSON.stringify({status,count:results.length,game_files_unchanged:unchanged,warnings,results},null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
