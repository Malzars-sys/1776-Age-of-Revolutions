// Execute the delivered dashboard's real script against an offline DOM fixture.
// No browser navigation, network, local URL permission bypass or game mutation.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const target = process.argv[2];
if (!target) throw new Error('Pass the generated TABLEAU.html path');
const source = fs.readFileSync(target, 'utf8');
const match = source.match(/<script>([\s\S]*?)<\/script>/);
assert(match, 'Dashboard script missing');
const elements = new Map();
const get = id => {
  if (!elements.has(id)) elements.set(id, {value: '', innerHTML: '', textContent: ''});
  return elements.get(id);
};
get('mode').value='all';get('ratio').value='.30';
const context=vm.createContext({document:{getElementById:get,querySelectorAll:()=>[]}});
new vm.Script(match[1], {filename:'delivered_arable_dashboard.js'}).runInContext(context,{timeout:20000});
const checks=[];
function check(name, f) { f();checks.push({name,result:'PASS'}); }
function rowCount() { return (get('rows').innerHTML.match(/<tr /g)||[]).length; }
const expected=JSON.parse(fs.readFileSync(path.join(path.dirname(target),'DIAGNOSIS.json'),'utf8'));
check('initial renders all source portions',()=>assert.equal(rowCount(),expected.states.length));
get('q').value='Agra';get('q').oninput();
check('Agra stays split by proprietor',()=>assert.equal(rowCount(),2));
check('UI unemployment and famine percentages are visible',()=>{
 const text=get('rows').innerHTML.replace(/[\s\u202f\u00a0]/g,'');
 assert(text.includes('2571967'));assert(text.includes('98/36'));
});
get('q').value='';get('mode').value='famine';get('mode').oninput();
check('native famine filter agrees with save manager',()=>assert.equal(rowCount(),expected.native.famine_states));
get('mode').value='mismatch';get('mode').oninput();
check('famine without capacity shortage is retained',()=>assert.equal(rowCount(),expected.reconciliation.categories.FAMINE_SANS_SATURATION_DEMONTREE));
get('native').onclick();
check('static-only mode does not invent native famine flags',()=>assert.equal(rowCount(),0));
get('mode').value='all';get('mode').oninput();get('q').value='Agra';get('q').oninput();
check('static-only model retains both Agra portions',()=>assert.equal(rowCount(),2));
get('q').value='<not an existing state>';get('q').oninput();
check('empty query result is safe',()=>assert.equal(rowCount(),0));
const result={status:'PASS_OFFLINE_SCRIPT',checks,browser_visual_validation:false,note:'Actual delivered script executed offline. Browser file:// navigation was denied by its URL policy; no workaround attempted.'};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
