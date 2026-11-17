// Read-only audit of the retained inputs. Writes exclusive, new receipts here only.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const { DatabaseSync } = require('node:sqlite');
const root = process.cwd();
const here = __dirname;
const lab = 'C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111';
const old = path.join(root, 'docs/reports/compatibility/V1_15_ISSUE54_INTERACTIVE_2026_11_11');
const expressions = path.join(root, 'docs/reports/compatibility/V1_15_ISSUE54_EXPRESSIONS_2026_11_12');
const read = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const walk = d => fs.readdirSync(d, {withFileTypes:true}).flatMap(e => e.isDirectory() ? walk(path.join(d,e.name)) : [path.join(d,e.name)]);
const relative = (d,p) => path.relative(d,p).split(path.sep).join('/');
const write = (name,data) => fs.writeFileSync(path.join(here,name), JSON.stringify(data,null,2), {flag:'wx'});
const mode = process.argv[2] || 'before';
const originals = read(path.join(old,'NORMAL_INPUTS_BEFORE.json'));
const originalDrift = Object.entries(originals).filter(([p,h]) => !fs.existsSync(p) || sha(p)!==h).map(([p])=>p);
const manifest = read(path.join(lab,'evidence/FROZEN_MANIFEST.json')).files;
const armChecks = {};
for (const arm of ['A_current','B_vanilla_gui','C_simplified_gui','expression_probe']) {
  const dir = path.join(lab,arm);
  const expected = Object.keys(manifest).filter(p => arm !== 'B_vanilla_gui' || p !== 'gui/tech_tree.gui');
  const actual = new Set(walk(dir).map(p=>relative(dir,p)));
  const drift = expected.filter(p=>!fs.existsSync(path.join(dir,p)) || sha(path.join(dir,p))!==manifest[p].sha256);
  armChecks[arm] = {expected:expected.length,actual:actual.size,missing:expected.filter(p=>!actual.has(p)),extra:[...actual].filter(p=>!expected.includes(p)),changed:drift,gui:fs.existsSync(path.join(dir,'gui/tech_tree.gui'))?sha(path.join(dir,'gui/tech_tree.gui')):null};
}
const normal = path.dirname(path.dirname(root));
const tables = ['playsets','playsets_mods','playsets_dlcs'];
const dbRows = p => { const db = new DatabaseSync(p,{readOnly:true}); try {return Object.fromEntries(tables.map(t=>[t,db.prepare('SELECT * FROM '+t).all()]));} finally {db.close();} };
const current = dbRows(path.join(normal,'launcher-v2.sqlite'));
const reference = dbRows(path.join(lab,'runtime_ui_controlled/B2/user_data/launcher-v2.sqlite'));
const testIds = new Set(reference.playsets.filter(r=>r.name.startsWith('TECHPERF 54 ')).map(r=>r.id));
const dbComparisons = {};
for (const t of tables) {
  const refs = reference[t].filter(r=>!testIds.has(t==='playsets'?r.id:r.playsetId));
  const key = r=>t==='playsets'?r.id:JSON.stringify(Object.entries(r).filter(([k])=>k!=='lastSyncAttemptAt').sort());
  const clean = r=>Object.fromEntries(Object.entries(r).filter(([k])=>k!=='lastSyncAttemptAt').sort());
  const norm = rows=>JSON.stringify(rows.map(clean).sort((a,b)=>key(a).localeCompare(key(b))));
  dbComparisons[t]={current:current[t].length,reference:refs.length,equalIgnoringSyncTimestamp:norm(current[t])===norm(refs)};
}
console.log(JSON.stringify({stage:'frozen_inputs_checked',armChecks,dbComparisons}));
const files = cp.execFileSync('git',['--no-optional-locks','ls-files','-c','-o','--exclude-standard','-z'],{cwd:root,maxBuffer:64*1024*1024}).toString().split('\0').filter(Boolean).filter(p=>!path.resolve(root,p).startsWith(here)).filter(p=>!p.startsWith('docs/reports/')&&!p.startsWith('.asset-cache/'));
const protectedFiles = Object.fromEntries(files.filter(p=>fs.statSync(path.join(root,p)).isFile()).map(p=>[p,sha(path.join(root,p))]));
protectedFiles['.git/index']=sha(path.join(root,'.git/index'));
const normalFiles = walk(path.join(normal,'save games')).concat(['pdx_settings.json','launcher-v2.sqlite','dlc_load.json','content_load.json'].map(p=>path.join(normal,p)).filter(fs.existsSync));
const protectedNormal = Object.fromEntries(normalFiles.map(p=>[p,sha(p)]));
const exps = read(path.join(expressions,'PLAN.json'));
const variants = Object.fromEntries(Object.entries(exps.variants).map(([k,v])=>[k,{expected:v.sha256,actual:sha(v.path),matches:sha(v.path)===v.sha256}]));
const installations = Object.fromEntries(['C:/Games/Victoria 3','C:/Program Files (x86)/Steam/steamapps/common/Victoria 3'].map(p=>[p,{version:read(path.join(p,'launcher/launcher-settings.json')).rawVersion,exe_sha256:sha(path.join(p,'binaries/victoria3.exe')),gui_sha256:sha(path.join(p,'game/gui/tech_tree.gui')),dlcFolders:fs.readdirSync(path.join(p,'game/dlc'))}]));
const save = read(path.join(old,'AUTHORIZED_RETRY_2026_11_12/SAVE_BASELINE.json'));
const steamDir = 'C:/Program Files (x86)/Steam/userdata';
const steamOptions = walk(steamDir).filter(p=>p.endsWith('localconfig.vdf')).map(p=>{const text=fs.readFileSync(p,'utf8');const start=text.indexOf('"529340"');const snippet=start<0?'':text.slice(start,start+1200);return {path:p,first_match_found:start>=0,first_match_length:snippet.length,first_match_sha256:crypto.createHash('sha256').update(snippet).digest('hex'),raw_contents_retained:false,launch_options_unverified_in_this_snippet:true};});
const receipt={utc:new Date().toISOString(),host:process.env.COMPUTERNAME,root,mode,originalDrift,armChecks,variants,dbComparisons,installations,save:{...save,actual:sha(save.path)},settings:{expected:exps.settings_sha256,actual:sha(path.join(exps.shared_profile,'pdx_settings.json'))},steamOptions,protectedFiles,protectedNormal,gitStatus:cp.execFileSync('git',['--no-optional-locks','status','--short'],{cwd:root}).toString()};
if(mode==='after') {
 const before=read(path.join(here,'BEFORE.json'));
 receipt.changedDuringRecovery=Object.keys(before.protectedFiles).filter(p=>!fs.existsSync(path.join(root,p))||sha(path.join(root,p))!==before.protectedFiles[p]);
 receipt.changedNormalDuringRecovery=Object.keys(before.protectedNormal).filter(p=>!fs.existsSync(p)||sha(p)!==before.protectedNormal[p]);
}
write(mode.toUpperCase()+'.json',receipt);
console.log(JSON.stringify({utc:receipt.utc,host:receipt.host,originalDrift,armChecks,variants,dbComparisons,installations,save:receipt.save,settings:receipt.settings,protectedCount:files.length,normalFiles:normalFiles.length,changedDuringRecovery:receipt.changedDuringRecovery,changedNormalDuringRecovery:receipt.changedNormalDuringRecovery,steamOptionsReview:'Use STEAM_PARAMETERS_REVIEW.json; raw VDF snippets are not retained.'},null,2));
