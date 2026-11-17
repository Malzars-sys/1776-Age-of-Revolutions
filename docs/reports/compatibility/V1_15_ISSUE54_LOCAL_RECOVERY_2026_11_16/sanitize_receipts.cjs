// Keep hashes of diagnostic snippets, never raw Steam ticket material.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
for(const name of ['BEFORE.json','AFTER.json']){
 const p=path.join(__dirname,name),raw=fs.readFileSync(p,'utf8'),data=JSON.parse(raw);
 data.steamOptions=data.steamOptions.map(row=>{
  if(!Object.hasOwn(row,'appBlock'))return row;
  const snippet=row.appBlock||'';
  return {path:row.path,first_match_found:row.appBlock!==null,first_match_length:snippet.length,first_match_sha256:crypto.createHash('sha256').update(snippet).digest('hex'),raw_contents_retained:false,launch_options_unverified_in_this_snippet:true};
 });
 if(fs.readFileSync(p,'utf8')!==raw)throw new Error('Receipt changed concurrently.');
 fs.writeFileSync(p,JSON.stringify(data,null,2));
}
console.log('Retained snippet hashes only; all preservation checks unchanged.');
