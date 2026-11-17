const fs=require('node:fs'),path=require('node:path');
const read=name=>JSON.parse(fs.readFileSync(path.join(__dirname,name),'utf8'));
const location=read('AFTER.json').steamOptions[0].path;
const tokens=fs.readFileSync(location,'utf8').match(/"(?:\\.|[^"\\])*"|[{}]/g);let index=0;
const unquote=t=>t.slice(1,-1).replace(/\\(["\\])/g,'$1');
function object(){const out={};while(index<tokens.length){if(tokens[index]==='}'){index++;return out;}const key=unquote(tokens[index++]);const token=tokens[index++];out[key]=token==='{'?object():unquote(token);}return out;}
const data=object();
function get(o,key){const actual=Object.keys(o).find(k=>k.toLowerCase()===key.toLowerCase());if(actual===undefined)throw new Error('Missing VDF section '+key);return o[actual];}
let app=data;for(const key of ['UserLocalConfigStore','Software','Valve','Steam','apps','529340'])app=get(app,key);
const launchKey=Object.keys(app).find(k=>k.toLowerCase()==='launchoptions');
const options=launchKey?app[launchKey]:'';
if(typeof options!=='string')throw new Error('Unexpected launch options type');
const result={recorded_utc:new Date().toISOString(),scope:'UserLocalConfigStore/Software/Valve/Steam/apps/529340',current_launch_options:options,launch_options_empty:options==='',agent_wrote_steam_config:false,old_observed_restoration_value:'',matches_old_observed_restoration:options==='',initial_vdf_snippet_limitation:'The first textual app-id occurrence may belong to app tickets; the 1200-character snippets in BEFORE/AFTER are not treated as an app-settings equality proof.'};
fs.writeFileSync(path.join(__dirname,'STEAM_PARAMETERS_REVIEW.json'),JSON.stringify(result,null,2),{flag:'wx'});console.log(result);
