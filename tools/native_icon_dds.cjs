"use strict";
// Lossless storage conversion for all our UI icons and unit illustrations.
// Installed native goods, tech, PM, building and unit textures use A8R8G8B8.
const RGBA=[0xff,0xff00,0xff0000,0xff000000];
const BGRA=[0xff0000,0xff00,0xff,0xff000000];
const masks=b=>[92,96,100,104].map(o=>b.readUInt32LE(o));
const is=(a,b)=>a.every((v,i)=>v===b[i]);
function nativeIconDds(input){
  if(input.length<128||input.toString("ascii",0,4)!=="DDS "||input.readUInt32LE(4)!==124||input.readUInt32LE(76)!==32||input.readUInt32LE(80)!==0x41||input.readUInt32LE(88)!==32)throw Error("Only uncompressed legacy 32-bit alpha DDS is supported");
  const size=input.readUInt32LE(16),height=input.readUInt32LE(12),count=input.readUInt32LE(28);
  if(size!==height||count!==Math.floor(Math.log2(size))+1)throw Error("Expected square asset with complete mipmaps");
  let expected=128,n=size;for(let i=0;i<count;i++){expected+=n*n*4;n=Math.max(1,n>>1);}
  if(expected!==input.length||n!==1)throw Error("Invalid complete DDS payload");
  const before=masks(input);if(is(before,BGRA))return Buffer.from(input);
  if(!is(before,RGBA))throw Error("Unknown channel layout; refusing to guess");
  const output=Buffer.from(input);
  // Swap STORAGE bytes AND masks; logical colors and alpha are unchanged.
  for(let i=128;i<output.length;i+=4){const red=output[i];output[i]=output[i+2];output[i+2]=red;}
  for(const [i,offset] of [92,96,100,104].entries())output.writeUInt32LE(BGRA[i],offset);
  return output;
}
module.exports={nativeIconDds,RGBA,BGRA,masks};
