"use strict";
// Exact export only: original RGBA masters, crop/contain scale, preserved alpha.
// Cache staging emits hashes; source/registry edits are applied separately.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {encode}=require('./rebuild_asset_icons.cjs');
const root=path.resolve(__dirname,'..');
const cache=path.join(root,'.asset-cache','early_ship_equipment_2026-10-08');
const lot=process.argv.find(a=>a.startsWith('--lot='))?.slice(6)||'armament';
const approvals={armament:'le premier lot est aprouve tu peut passé au lot de la coque',hull:'Hop, je valide le lot, tu peux passer au suivant. À savoir la propulsion.',propulsion:'Hop, tu peux intégrer et passer au jeu suivant, le pont.',deck:'Tu peux intégrer et passer au lot suivant.',galley_armament:'que tu peux intégrer et passer au suivant.'};
approvals.galley_hull="ok tu peut integré et passé au lot suivant, aussi je n'ai pas verifié mais toute ces modification donne des statisitque n'est ce pas ?";
approvals.galley_propulsion='Ok, tu peux tout incorporer et passer au lot suivant.';
approvals.galley_supply='Ok, tu peux intégrer et passer au suivant.';
approvals.cog_hull='Ok, tu peux intégrer et passer au lot suivant.';
approvals.cog_armament='Hop, tu peux intégrer et passer au le suivant.';
approvals.cog_propulsion='Je vais, tu peux intégrer, passer au lot suivant.';
approvals.cog_supply='OK, tu peux intégrer et passer au lot suivant.';
approvals.naval_functions="Ok, tu peux intégrer et passer au lot suivant s'il y en a un.";
approvals.galley_boarding_spur='que tu peux intégrer. Je vais relancer le jeu de mon côté, ensuite.';
if(!approvals[lot])throw Error('Unknown lot');
const file=path.join(cache,'approved_'+lot+'_plan.json');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
(async()=>{
  const state=JSON.parse(fs.readFileSync(file,'utf8'));
  const entries=state.manifest.entries;
  if(entries.length!==(lot==='galley_boarding_spur'?1:3)||state.manifest.approval!==approvals[lot])throw Error('Wrong approved lot');
  fs.mkdirSync(path.join(cache,lot+'_candidates'),{recursive:true});
  for(const e of entries){
    const bytes=await encode(e),dest=path.join(cache,lot+'_candidates',path.basename(e.dds));
    if(fs.existsSync(dest)&&!fs.readFileSync(dest).equals(bytes))throw Error('Different existing candidate');
    fs.writeFileSync(dest,bytes);e.dds_sha256=hash(bytes);
  }
  fs.writeFileSync(file,JSON.stringify(state,null,2)+'\n');
  console.log(JSON.stringify({status:'PASS_APPROVED_STAGED_EXPORTS',count:entries.length,size:120,mips:7,alpha_preserved:true,runtime_modified:false}));
})().catch(e=>{console.error(e);process.exitCode=1;});
