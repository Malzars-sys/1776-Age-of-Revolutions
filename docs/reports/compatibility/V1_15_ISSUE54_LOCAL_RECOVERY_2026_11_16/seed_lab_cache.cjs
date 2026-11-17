const fs=require('node:fs'),path=require('node:path');
const base='C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111';
const source=path.join(base,'runtime_ui_controlled/A1/user_data');
const target=path.join(base,'local_recovery_20261116/user_data');
const marker=path.join(target,'STOP_TEST_REQUESTED.json');
const exit=path.join(__dirname,'CONTROL1_20261116T230727464Z/EXIT.json');
if(!fs.existsSync(exit))throw new Error('Wait for the owned game to exit.');
fs.renameSync(marker,path.join(__dirname,'UNMEASURED_SHADER_ATTEMPT_STOP.json'));
let copied=0,existing=0;
function add(from,to){fs.mkdirSync(to,{recursive:true});for(const entry of fs.readdirSync(from,{withFileTypes:true})){const a=path.join(from,entry.name),b=path.join(to,entry.name);if(entry.isDirectory())add(a,b);else if(fs.existsSync(b))existing++;else{fs.copyFileSync(a,b,fs.constants.COPYFILE_EXCL);copied++;}}}
for(const name of ['shadercache','user_bindings'])if(fs.existsSync(path.join(source,name)))add(path.join(source,name),path.join(target,name));
fs.writeFileSync(path.join(__dirname,'CACHE_SEED.json'),JSON.stringify({utc:new Date().toISOString(),source,target,copied,existing,overwrite:false,normal_profile_used:false},null,2),{flag:'wx'});
console.log({copied,existing});
