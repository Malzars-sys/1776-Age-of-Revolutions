#!/usr/bin/env node
// Mechanical alpha-canvas padding only. No painting, masking, recoloring or cropping.
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const sharp=require(require.resolve("sharp",{paths:[__dirname,path.resolve(path.dirname(process.execPath),"..")]}));
const pack=path.resolve(__dirname,"../docs/reports/assets/asset11_preview_2026-10-04");
const plan=JSON.parse(fs.readFileSync(path.join(pack,"generation_plan.json"),"utf8"));
const qa=JSON.parse(fs.readFileSync(path.join(pack,"preview_validation.json"),"utf8"));
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
async function main(){
 const results=[];
 for(const e of plan.entries){
  const input=path.join(pack,e.preview),q=qa.results.find(q=>q.key===e.key);
  const {data,info}=await sharp(input).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const pad=96,width=info.width+2*pad,height=info.height+2*pad;
  const left=Math.round((width-1)/2-(q.bounds[0]+q.bounds[2])/2);
  const top=Math.round((height-1)/2-(q.bounds[1]+q.bounds[3])/2);
  const right=width-info.width-left,bottom=height-info.height-top;
  if(Math.min(left,top,right,bottom)<0)throw Error("Invalid mechanical padding");
  const selected="previews/"+e.key+"_padded.png",output=path.join(pack,selected);
  if(fs.existsSync(output))throw Error("Padded preview already exists");
  await sharp(input).extend({left,right,top,bottom,background:{r:0,g:0,b:0,alpha:0}}).png().toFile(output);
  const expanded=await sharp(output).ensureAlpha().raw().toBuffer();
  for(let y=0;y<info.height;y++){
   const oldRow=data.subarray(y*info.width*4,(y+1)*info.width*4);
   const newRow=expanded.subarray(((y+top)*width+left)*4,((y+top)*width+left+info.width)*4);
   if(!oldRow.equals(newRow))throw Error("Original pixels altered by padding");
  }
  results.push({key:e.key,source:e.preview,source_sha256:hash(fs.readFileSync(input)),selected_preview:selected,sha256:hash(fs.readFileSync(output)),padding:{left,right,top,bottom},source_rgba_pixels_exactly_preserved:true,retouched:false,dimensions:[width,height]});
 }
 fs.writeFileSync(path.join(pack,"canvas_padding.json"),JSON.stringify({operation:"ADD_TRANSPARENT_CANVAS_AND_CENTER_VISIBLE_OBJECT_WITHOUT_CROPPING",results},null,2)+"\n");
 console.log(JSON.stringify(results,null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});

