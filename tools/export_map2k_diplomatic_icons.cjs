"use strict";
// Supplied PNGs already contain alpha. Only native sizing/storage conversion.
const fs=require("node:fs"),path=require("node:path");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const {nativeIconDds}=require("./native_icon_dds.cjs");
const root=path.resolve(__dirname,".."),game="C:/Games/Victoria 3/game";
async function emit(source,folder,key,reference){
 const im=sharp(source),meta=await im.metadata();if(!meta.hasAlpha)throw Error("Supplied image lacks alpha: "+source);
 const r=fs.readFileSync(path.join(game,reference)),size=r.readUInt32LE(16);
 const pixels=await im.resize(size,size,{fit:"contain",background:{r:0,g:0,b:0,alpha:0},kernel:"lanczos3"}).ensureAlpha().raw().toBuffer();
 if(pixels[3]!==0)throw Error("Background not transparent");
 const levels=[];for(let s=size;s>=1;s=Math.floor(s/2))levels.push(await sharp(pixels,{raw:{width:size,height:size,channels:4}}).resize(s,s,{kernel:"lanczos3"}).raw().toBuffer());
 const header=Buffer.alloc(128);header.write("DDS ",0,"ascii");
 for(const [o,v] of [[4,124],[8,0x2100f],[12,size],[16,size],[20,size*4],[28,levels.length],[76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]])header.writeUInt32LE(v,o);
 fs.mkdirSync(path.join(root,folder),{recursive:true});fs.writeFileSync(path.join(root,folder,key+".dds"),nativeIconDds(Buffer.concat([header,...levels])));
 console.log(key,folder,size,"BGRA8 with complete mipmaps; alpha preserved");
}
async function main(){
 const request=path.join(root,"workshop_assets/source/map2k_hre_restitution_request.png");
 const war=path.join(root,"workshop_assets/source/map2k_hre_restitution_war.png");
 const bond=path.join(root,"workshop_assets/source/map2k_hre_imperial_bond_v2.png");
 const territory=path.join(root,"workshop_assets/source/map2k_hre_state_marker.png");
 const mapIcon=path.join(root,"workshop_assets/source/map2k_hre_map_access_v2.png");
 await emit(request,"gfx/interface/icons/lens_toolbar_icons","aor1776_hre_request_restitution","gfx/interface/icons/lens_toolbar_icons/trade_states.dds");
 await emit(request,"gfx/interface/icons/diplomatic_action_icons","aor1776_hre_request_restitution","gfx/interface/icons/diplomatic_action_icons/grant_state.dds");
 await emit(bond,"gfx/interface/icons/diplomatic_action_icons","aor1776_imperial_obligation","gfx/interface/icons/diplomatic_action_icons/grant_state.dds");
 await emit(territory,"gfx/interface/icons/timed_modifier_icons","aor1776_hre_registered_territory","gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds");
 await emit(mapIcon,"gfx/interface/icons/map_mode_icons","aor1776_hre_territories","gfx/interface/icons/map_mode_icons/states.dds");
 await emit(war,"gfx/interface/icons/war_goals","aor1776_hre_restitution","gfx/interface/icons/war_goals/return_state.dds");
 await emit(war,"gfx/interface/icons/lens_toolbar_icons","dp_aor1776_hre_restitution","gfx/interface/icons/lens_toolbar_icons/trade_states.dds");
 await emit(request,"gfx/interface/icons/lens_toolbar_icons","aor1776_hre_request_subject_release","gfx/interface/icons/lens_toolbar_icons/trade_states.dds");
 await emit(request,"gfx/interface/icons/diplomatic_action_icons","aor1776_hre_request_subject_release","gfx/interface/icons/diplomatic_action_icons/grant_state.dds");
 await emit(war,"gfx/interface/icons/war_goals","aor1776_hre_subject_release","gfx/interface/icons/war_goals/return_state.dds");
 await emit(war,"gfx/interface/icons/lens_toolbar_icons","dp_aor1776_hre_subject_release","gfx/interface/icons/lens_toolbar_icons/trade_states.dds");
}
module.exports={emit};
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
