const fs=require('node:fs'),path=require('node:path');
const here=__dirname,plan=JSON.parse(fs.readFileSync(path.join(here,'PLAN.json'),'utf8').replace(/^\uFEFF/,''));
const source='C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/runtime_ui_controlled/A1/user_data';
const target='C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/manual_relay_20261116/user_data';
if(fs.existsSync(target))throw new Error('Preserve the existing handoff profile.');
fs.mkdirSync(path.join(target,'save games'),{recursive:true});
for(const name of ['pdx_settings.json','continue_game.json','console_history.txt'])fs.copyFileSync(path.join(source,name),path.join(target,name),fs.constants.COPYFILE_EXCL);
fs.copyFileSync(plan.save,path.join(target,'save games',path.basename(plan.save)),fs.constants.COPYFILE_EXCL);
let files=0;
function copy(from,to){fs.mkdirSync(to,{recursive:true});for(const entry of fs.readdirSync(from,{withFileTypes:true})){const a=path.join(from,entry.name),b=path.join(to,entry.name);if(entry.isDirectory())copy(a,b);else{fs.copyFileSync(a,b,fs.constants.COPYFILE_EXCL);files++;}}}
for(const name of ['shadercache','user_bindings'])if(fs.existsSync(path.join(source,name)))copy(path.join(source,name),path.join(target,name));
plan.profile=target;plan.save=path.join(target,'save games',path.basename(plan.save));
fs.writeFileSync(path.join(here,'PLAN_MANUAL.json'),JSON.stringify(plan,null,2),{flag:'wx'});
const script=path.join(here,'Assistant_Test.ps1');const raw=fs.readFileSync(script,'utf8').replace(/^\uFEFF/,'');fs.writeFileSync(script,'\uFEFF'+raw);
fs.writeFileSync(path.join(here,'MANUAL_PREPARATION.json'),JSON.stringify({utc:new Date().toISOString(),profile:target,additional_cache_binding_files:files,normal_profile_written:false,execution_policy_changed:false},null,2),{flag:'wx'});
console.log({profile:target,copied:files});
