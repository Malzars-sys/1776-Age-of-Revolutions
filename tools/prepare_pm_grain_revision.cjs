// Input copies and protection hashes only. No artistic modifications.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const pack=path.join(root,'docs/reports/assets/asset8_pm_grain_revision_2026-10-03');
const old=path.join(root,'docs/reports/assets/asset8_flat_revision_2026-10-03');
const hash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const write=(n,o)=>fs.writeFileSync(path.join(pack,n),JSON.stringify(o,null,2)+'\n');
if(fs.existsSync(path.join(pack,'baseline.json')))throw Error('Baseline exists; refusing to overwrite');
for(const d of ['inputs','references','previews','target_size_png'])fs.mkdirSync(path.join(pack,d),{recursive:true});
const p=JSON.parse(fs.readFileSync(path.join(old,'revision_plan.json'),'utf8'));
const entries=p.entries.filter(e=>e.family==='PM');
for(const e of entries){
 const src=path.join(old,e.preview),dest=path.join(pack,'inputs',e.key+'.png');
 fs.copyFileSync(src,dest,fs.constants.COPYFILE_EXCL);
 e.source_previous_preview='../asset8_flat_revision_2026-10-03/'+e.preview;
 e.edit_input='inputs/'+e.key+'.png';e.input_sha256=hash(src);
 e.preview='previews/'+e.key+'_grain_gradient.png';e.integration='WAITING_USER_APPROVAL';
}
for(let i=1;i<=3;i++)fs.copyFileSync(path.join(old,'references',`user_pm_${i}.png`),path.join(pack,'references',`user_pm_${i}.png`),fs.constants.COPYFILE_EXCL);
const baseline={};
function walk(d){for(const e of fs.readdirSync(d,{withFileTypes:true})){
 const f=path.join(d,e.name);if(e.isDirectory())walk(f);else if(e.isFile())baseline[path.relative(root,f).replace(/\\/g,'/')]=hash(f);
}}
walk(path.join(root,'common'));walk(path.join(root,'gfx'));write('baseline.json',baseline);
write('revision_plan.json',{status:'INPUTS_READY',date:'2026-10-03',mode:'BUILTIN_IMAGE_GEN',approval_required:true,
 scope:'17 previously revised PM only; grain and top-light to bottom-dark graphic gradient; silhouettes retained',
 technology_unchanged:true,vanilla_building_unchanged:true,game_mutations_authorized:false,entries});
write('untouched_other_assets.json',{technology_preview:'../asset8_flat_revision_2026-10-03/previews/improved_road_engineering_cobblestones.png',
 technology_preview_sha256:hash(path.join(old,'previews/improved_road_engineering_cobblestones.png')),
 building_file:'common/buildings/11_private_infrastructure.txt',building_file_sha256:hash(path.join(root,'common/buildings/11_private_infrastructure.txt'))});
console.log(JSON.stringify({pm_count:entries.length,protected_files:Object.keys(baseline).length,game_changed:false}));
