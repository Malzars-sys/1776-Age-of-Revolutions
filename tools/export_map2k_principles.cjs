"use strict";
const path=require('node:path');
const {emit}=require('./export_map2k_diplomatic_icons.cjs');
async function main(){
 for(const family of ['diet','administration','circles','justice']){
  await emit(path.resolve(__dirname,'../workshop_assets/source/map2k_hre_principle_'+family+'.png'),
   'gfx/interface/icons/principles_icons','aor1776_hre_'+family,
   'gfx/interface/icons/principles_icons/defensive_coorperation.dds');
 }
}
main().catch(e=>{console.error(e);process.exitCode=1;});
