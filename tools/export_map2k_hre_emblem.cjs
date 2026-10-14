"use strict";
// Storage conversion only. The image tool supplied the cutout alpha.
// No background-removal threshold and no recoloring of dark feathers.
const fs=require("node:fs"),path=require("node:path");
const {nativeIconDds}=require("./native_icon_dds.cjs");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const root=path.resolve(__dirname,"..");
async function main(){
 const source=path.join(root,"workshop_assets/source/map2k_hre_emblem_v2.png");
 const native=path.join("C:/Games/Victoria 3/game/gfx/interface/icons/central_identity_pillars_icons/sovereign_empire.dds");
 const reference=fs.readFileSync(native),size=reference.readUInt32LE(16);
 if(size!==reference.readUInt32LE(12))throw Error("Native identity icon is not square");
 const meta=await sharp(source).metadata();
 if(!meta.hasAlpha)throw Error("Image tool output lacks alpha");
 const base=await sharp(source).resize(size,size,{fit:"contain",background:{r:0,g:0,b:0,alpha:0},kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
 if(base[3]!==0||!base.some((v,i)=>i%4===3&&v>240))throw Error("Missing transparent background or opaque subject");
 const levels=[];
 for(let side=size;side>=1;side=Math.floor(side/2))levels.push(await sharp(base,{raw:{width:size,height:size,channels:4}}).resize(side,side,{kernel:"lanczos3"}).raw().toBuffer());
 const header=Buffer.alloc(128);header.write("DDS ",0,"ascii");
 for(const [o,v] of [[4,124],[8,0x2100f],[12,size],[16,size],[20,size*4],[28,levels.length],[76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]])header.writeUInt32LE(v,o);
 const folder=path.join(root,"gfx/interface/icons/central_identity_pillars_icons");fs.mkdirSync(folder,{recursive:true});
 const dds=nativeIconDds(Buffer.concat([header,...levels]));
 fs.writeFileSync(path.join(folder,"aor1776_imperial_federation_v2.dds"),dds);
 const rgba=await sharp(source).ensureAlpha().raw().toBuffer();
 let zero=0,opaque=0;for(let i=3;i<rgba.length;i+=4){if(rgba[i]===0)zero++;if(rgba[i]===255)opaque++;}
 const report={preferred_input:"codex-clipboard-ea2c7d93-6cb8-458e-9afa-d50d458ccf7b.png",method:"Built-in image tool: background-extraction only; lossless BGRA8 DDS storage conversion and native-size resampling",master:{width:meta.width,height:meta.height,hasAlpha:meta.hasAlpha,fully_transparent_pixels:zero,fully_opaque_pixels:opaque},dds:{size,mipmaps:levels.length,bytes:dds.length,channel_layout:"BGRA8"},runtime_binding:"Bound to identity_aor1776_imperial_federation; appearance pending engine test; no vanilla identity overwritten"};
 const out=path.join(root,"docs/reports/map/MAP2K");fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,"EMBLEM_V2_VALIDATION.json"),JSON.stringify(report,null,2)+"\n");console.log(JSON.stringify(report));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
