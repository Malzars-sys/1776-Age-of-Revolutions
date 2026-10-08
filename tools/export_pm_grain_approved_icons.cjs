"use strict";
// Format-only export of the ten approved PMs. Laboratory textures are protected.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const {nativeIconDds}=require('./native_icon_dds.cjs');
const sharp=require(require.resolve('sharp',{paths:[__dirname,path.resolve(path.dirname(process.execPath),'..')]}));
const root=path.resolve(__dirname,'..'),pack=path.join(root,'docs/reports/assets/asset8_pm_grain_revision_2026-10-03');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=f=>JSON.parse(fs.readFileSync(path.join(pack,f),'utf8'));
const write=(f,data)=>fs.writeFileSync(path.join(pack,f),JSON.stringify(data,null,2)+'\n');
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):[path.relative(root,path.join(d,e.name)).replaceAll('\\','/')]);
const snapshot=()=>Object.fromEntries(['common','gfx'].flatMap(d=>walk(path.join(root,d))).sort().map(f=>[f,hash(fs.readFileSync(path.join(root,f)))]));
const manifestFile=path.join(pack,'integration_manifest.json');
function prepare(){
  assert(!fs.existsSync(manifestFile),'Integration baseline already exists');
  const approval=read('user_approval.json'),plan=read('revision_plan.json'),proof=read('preview_validation.json');
  assert(approval.status==='PARTIALLY_APPROVED_EXCLUDING_LABORATORY'&&approval.approved_keys.length===10&&approval.rejected_keys.length===7);
  const baseline=snapshot(),previewBaseline=read('baseline.json');
  assert(Object.keys(baseline).length===Object.keys(previewBaseline).length&&Object.entries(previewBaseline).every(([f,h])=>baseline[f]===h),'Game files changed since preview');
  const excluded=plan.entries.filter(e=>e.key.startsWith('laboratory_'));
  assert(excluded.length===7&&excluded.every(e=>approval.rejected_keys.includes(e.key)&&baseline[e.current_dds]===e.current_dds_sha256));
  const entries=approval.approved_keys.map(key=>{
    const e=plan.entries.find(x=>x.key===key),p=proof.checks.find(x=>x.key===key);
    assert(e&&!key.startsWith('laboratory_')&&p&&e.bindings.length===1);
    assert(hash(fs.readFileSync(path.join(pack,e.preview)))===p.sha256,'Preview changed');
    const dds=e.current_dds||e.proposed_dds;
    assert(path.resolve(root,dds).startsWith(path.join(root,'gfx')+path.sep));
    if(e.current_dds)assert(baseline[dds]===e.current_dds_sha256);else assert(!fs.existsSync(path.join(root,dds)));
    return {key,label:e.label_fr,id:e.bindings[0].id,definition:e.bindings[0].file,previous_texture:e.current_dds||e.current_texture,
      preview:e.preview,source_sha256:p.sha256,dds,previous_dds_sha256:e.current_dds_sha256||null,size:208,mips:8};
  });
  const definitions=Object.fromEntries([...new Set(entries.map(e=>e.definition))].map(f=>[f,{sha256:baseline[f],text:fs.readFileSync(path.join(root,f),'utf8')} ]));
  write('integration_gameplay_and_gfx_baseline.json',baseline);
  write('integration_manifest.json',{date:'2026-10-04',status:'TEN_PM_APPROVED_READY_FOR_EXPORT',mode:'BUILTIN_IMAGE_GEN',approval,protected_baseline:'integration_gameplay_and_gfx_baseline.json',definition_baseline:definitions,entries,
    retained_laboratory:excluded.map(e=>({key:e.key,dds:e.current_dds,sha256:e.current_dds_sha256,bindings:e.bindings})),game_tested:false});
  console.log(JSON.stringify({status:'BASELINE_RECORDED',approved:10,retained_laboratory:7,protected_files:Object.keys(baseline).length}));
}
async function exportIcons(){
  const m=read('integration_manifest.json'),baseline=read(m.protected_baseline),before=snapshot();
  assert(m.entries.length===10&&m.retained_laboratory.length===7&&m.entries.every(e=>m.approval.approved_keys.includes(e.key)));
  assert(Object.keys(before).length===Object.keys(baseline).length&&Object.entries(baseline).every(([f,h])=>before[f]===h),'Game files changed since integration baseline');
  const prepared=[];
  for(const e of m.entries){
    const source=fs.readFileSync(path.join(pack,e.preview));assert(hash(source)===e.source_sha256);
    const meta=await sharp(source).metadata();assert(meta.hasAlpha&&meta.width===meta.height&&meta.width>=1024);
    const base=await sharp(source).resize(208,208,{kernel:'lanczos3'}).ensureAlpha().raw().toBuffer();
    assert([0,207,208*207,208*208-1].every(p=>base[p*4+3]===0),'Opaque corners');
    const levels=[],mipHashes=[];
    for(let n=208;n>=1;n>>=1){const rgba=await sharp(base,{raw:{width:208,height:208,channels:4}}).resize(n,n,{kernel:'lanczos3'}).raw().toBuffer();levels.push(rgba);mipHashes.push({size:n,rgba_sha256:hash(rgba)});}
    const header=Buffer.alloc(128);header.write('DDS ',0,'ascii');
    for(const [o,v]of [[4,124],[8,0x2100f],[12,208],[16,208],[20,832],[28,8],[76,32],[80,0x41],[88,32],[92,0xff],[96,0xff00],[100,0xff0000],[104,0xff000000],[108,0x401008]])header.writeUInt32LE(v,o);
    const dds=nativeIconDds(Buffer.concat([header,...levels]));assert(dds.length===230828&&levels.length===8);
    const dest=path.resolve(root,e.dds);assert(dest.startsWith(path.join(root,'gfx')+path.sep));
    if(e.previous_dds_sha256)assert(hash(fs.readFileSync(dest))===e.previous_dds_sha256);else assert(!fs.existsSync(dest));
    prepared.push({e,base,dds,dest,mipHashes});
  }
  for(const d of ['backups','integrated_target_png'])fs.mkdirSync(path.join(pack,d),{recursive:true});
  const results=[];
  for(const {e,base,dds,dest,mipHashes}of prepared){
    let backup=null;
    if(e.previous_dds_sha256){backup='backups/'+e.key+'_'+e.previous_dds_sha256+'.dds';assert(!fs.existsSync(path.join(pack,backup)));fs.copyFileSync(dest,path.join(pack,backup));}
    fs.writeFileSync(dest,dds);
    const png='integrated_target_png/'+e.key+'.png';await sharp(base,{raw:{width:208,height:208,channels:4}}).png().toFile(path.join(pack,png));
    results.push({key:e.key,dds:e.dds,dds_sha256:hash(dds),source:e.preview,source_sha256:e.source_sha256,target_png:png,backup,dimensions:[208,208],mips:8,mip_hashes:mipHashes,format:'BGRA8 legacy native A8R8G8B8',bytes:dds.length});
  }
  assert(m.retained_laboratory.every(e=>hash(fs.readFileSync(path.join(root,e.dds)))===e.sha256));
  write('integration_export_validation.json',{status:'PASS_TEN_NATIVE_PM_DDS_EXPORTS',retained_laboratory_unchanged:true,game_tested:false,results});
  console.log(JSON.stringify({status:'PASS_TEN_NATIVE_PM_DDS_EXPORTS',count:results.length,retained_laboratory:7}));
}
(async()=>{if(process.argv[2]==='--prepare')prepare();else if(process.argv[2]==='--export')await exportIcons();else throw Error('Usage: --prepare|--export');})().catch(e=>{console.error(e);process.exitCode=1;});
