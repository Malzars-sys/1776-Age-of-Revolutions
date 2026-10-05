// Deterministic previews and checks only; no artistic edits and no DDS exports.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert');
const sharp = require(require.resolve('sharp', {paths:[__dirname,path.resolve(path.dirname(process.execPath),'..')]}));
const root = path.resolve(__dirname,'..');
const pack = path.join(root,'docs/reports/assets/asset8_pm_grain_revision_2026-10-03');
const read = f => JSON.parse(fs.readFileSync(path.join(pack,f),'utf8').replace(/^\uFEFF/,''));
const write = (f,obj) => fs.writeFileSync(path.join(pack,f),JSON.stringify(obj,null,2)+'\n');
const hash = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const text = (x,y,s,size=18,color='#e6dec9') => `<text x="${x}" y="${y}" font-family="Segoe UI, sans-serif" font-size="${size}" fill="${color}">${esc(s)}</text>`;
const rect = (x,y,w,h,color) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${color}"/>`;
const svg = (w,h,body) => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${body}</svg>`);
const plan = read('revision_plan.json');
const baseline = read('baseline.json');
const untouched = read('untouched_other_assets.json');
const current = {};
function walk(d){for(const e of fs.readdirSync(d,{withFileTypes:true})){
  const f=path.join(d,e.name); if(e.isDirectory()) walk(f);
  else if(e.isFile()) current[path.relative(root,f).replace(/\\/g,'/')]=hash(f);
}}
walk(path.join(root,'common'));walk(path.join(root,'gfx'));
const changed=Object.keys(baseline).filter(f=>baseline[f]!==current[f]);
const added=Object.keys(current).filter(f=>!baseline[f]);
assert.deepStrictEqual(changed,[]); assert.deepStrictEqual(added,[]);
assert.strictEqual(hash(path.join(root,untouched.building_file)),untouched.building_file_sha256);
assert.strictEqual(hash(path.join(pack,untouched.technology_preview)),untouched.technology_preview_sha256);
for(const e of plan.entries) assert.strictEqual(hash(path.join(pack,e.edit_input)),e.input_sha256);
for(const e of plan.entries){
  if(e.current_dds) assert.strictEqual(hash(path.join(root,e.current_dds)),e.current_dds_sha256);
  if(e.proposed_dds) assert(!fs.existsSync(path.join(root,e.proposed_dds)),'Unapproved generated DDS already integrated');
}
function enclosedTransparentRegions(data,w,h){
  const seen=new Uint8Array(w*h), areas=[];
  for(let i=0;i<w*h;i++){
    if(seen[i] || data[i*4+3]>8) continue;
    const stack=[i]; seen[i]=1; let area=0,edge=false;
    while(stack.length){const q=stack.pop(),x=q%w,y=Math.floor(q/w);area++;
      if(x===0||y===0||x===w-1||y===h-1)edge=true;
      for(const n of [x>0?q-1:-1,x<w-1?q+1:-1,y>0?q-w:-1,y<h-1?q+w:-1])
        if(n>=0&&!seen[n]&&data[n*4+3]<=8){seen[n]=1;stack.push(n);}
    }
    if(!edge&&area>=6) areas.push(area);
  }
  return areas.sort((a,b)=>b-a);
}
async function alphaInfo(f){
  const m=await sharp(f).metadata();assert(m.hasAlpha,'No real alpha: '+f);
  const {data,info}=await sharp(f).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const w=info.width,h=info.height;let transparent=0,visible=0;let box=[w,h,-1,-1];
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    const a=data[(y*w+x)*4+3];if(a===0)transparent++;
    if(a>8){visible++;box=[Math.min(box[0],x),Math.min(box[1],y),Math.max(box[2],x),Math.max(box[3],y)];}
  }
  const corners=[0,w-1,w*(h-1),w*h-1].map(i=>data[i*4+3]);
  assert(corners.every(a=>a===0),'Opaque corners: '+f);assert(transparent>0&&visible>0);
  return {width:w,height:h,hasAlpha:m.hasAlpha,fully_transparent_pixels:transparent,
    visible_fraction:visible/(w*h),visible_bounds:box,corner_alpha:corners};
}
async function thumbnail(f,n){return sharp(f).resize(n,n,{fit:'contain',background:'#00000000'}).png().toBuffer();}
async function groupedBoard(entries,title,out,cols=3){
  const cw=400,ch=500,w=cw*cols,h=100+Math.ceil(entries.length/cols)*ch;
  let body=rect(0,0,w,h,'#182428')+text(20,33,title,25)+text(20,64,'Grain fin · haut clair / bas sombre · aperçus non intégrés · 32 / 48 / 64 px',16);
  const composites=[];
  for(let i=0;i<entries.length;i++){
    const e=entries[i],x=(i%cols)*cw,y=100+Math.floor(i/cols)*ch;
    body+=rect(x+8,y+8,cw-16,ch-16,'#24383c');
    let line='',lines=[];for(const word of e.label_fr.split(' ')){
      if((line+' '+word).trim().length>34){lines.push(line);line=word;}else line=(line+' '+word).trim();
    }if(line)lines.push(line);
    lines.forEach((s,j)=>{body+=text(x+18,y+33+j*22,s,19);});
    const f=e.source||path.join(pack,e.preview);
    composites.push({input:await thumbnail(f,250),left:x+75,top:y+83});
    for(let b=0;b<2;b++){
      body+=rect(x+18,y+345+b*62,cw-36,58,b?'#d5d4c9':'#15242a');
      let dx=x+40;for(const n of [32,48,64]){
        composites.push({input:await thumbnail(f,n),left:dx,top:y+344+b*62+Math.floor((60-n)/2)});dx+=110;
      }
    }
    body+=text(x+18,y+483,e.family==='NATIVE'?'Vanilla repris sans retouche — intégré':'Validation visuelle requise',13);
  }
  await sharp(svg(w,h,body)).composite(composites).png().toFile(path.join(pack,out));
}
async function comparisonPage(entries,num){
  const w=1020,rh=182,h=100+rh*entries.length;
  let body=rect(0,0,w,h,'#19282d')+text(18,30,'Grain et dégradé — comparaison à 64 px — page '+num,24);
  const xs=[305,445,585,725,865];
  ['Version plate','Grain + dégradé','Vanilla 1','Vanilla 2','Vanilla 3'].forEach((s,i)=>body+=text(xs[i]-5,70,s,17));
  const composites=[];
  for(let i=0;i<entries.length;i++){
    const e=entries[i],y=100+i*rh;
    const words=e.label_fr.split(' ');let line='',ln=0;
    for(const word of words){if((line+' '+word).trim().length>25){body+=text(18,y+35+ln*24,line,16);line=word;ln++;}else line=(line+' '+word).trim();}
    body+=text(18,y+35+ln*24,line,16);
    const files=[path.join(pack,e.edit_input),path.join(pack,e.preview),...Array.from({length:3},(_,j)=>path.join(pack,`references/user_pm_${j+1}.png`))];
    for(let j=0;j<5;j++)for(let b=0;b<2;b++){
      body+=rect(xs[j]-12,y+6+b*80,90,76,b?'#d5d4c9':'#102025');
      composites.push({input:await thumbnail(files[j],64),left:xs[j],top:y+12+b*80});
    }
  }
  body+=text(18,h-8,'Références vanilla fournies conservées sans retouche ; toutes les vignettes ont le même format.',12);
  await sharp(svg(w,h,body)).composite(composites).png().toFile(path.join(pack,`PM_COMPARAISON_VANILLA_${num}.png`));
}
async function checkerBoard(entries){
  const cw=240,ch=270,cols=6,w=cw*cols,h=60+Math.ceil(entries.length/cols)*ch;
  let body=rect(0,0,w,h,'#1f2e31')+text(16,34,'Contrôle de la transparence réelle — damier',22);const comps=[];
  for(let i=0;i<entries.length;i++){
    const x=(i%cols)*cw,y=60+Math.floor(i/cols)*ch;
    for(let yy=0;yy<240;yy+=16)for(let xx=0;xx<240;xx+=16)body+=rect(x+xx,y+yy,16,16,((xx+yy)/16)%2?'#b9b7ac':'#e7e4d9');
    comps.push({input:await thumbnail(path.join(pack,entries[i].preview),224),left:x+8,top:y+8});
    body+=text(x+8,y+260,entries[i].label_fr.slice(0,30),12);
  }
  await sharp(svg(w,h,body)).composite(comps).png().toFile(path.join(pack,'TRANSPARENCE_DAMIER.png'));
}
async function main(){
  fs.mkdirSync(path.join(pack,'target_size_png'),{recursive:true});const checks=[];
  for(const e of plan.entries){
    const f=path.join(pack,e.preview),master=await alphaInfo(f);
    assert(master.width===master.height&&master.width>=1024,'Unexpected generated master dimensions');
    const dest=path.join(pack,'target_size_png',e.key+'.png');
    await sharp(f).resize(e.target_size,e.target_size).png().toFile(dest);
    const target=await alphaInfo(dest);
    const raw=await sharp(dest).resize(64,64).ensureAlpha().raw().toBuffer();
    checks.push({key:e.key,preview:e.preview,sha256:hash(f),master,target,
      enclosed_transparent_regions_at_64px:enclosedTransparentRegions(raw,64,64),integration:'WAITING_USER_APPROVAL'});
  }
  await groupedBoard(plan.entries.filter(e=>e.key.endsWith('_road_network')),'Routes — grain et dégradé','PM_ROUTES_GRAIN_DEGRADE.png',2);
  await groupedBoard(plan.entries.filter(e=>e.key.startsWith('laboratory_')),'Laboratoires — grain et dégradé','PM_LABORATOIRE_GRAIN_DEGRADE.png',4);
  await groupedBoard(plan.entries.filter(e=>!e.key.startsWith('laboratory_')&&!e.key.endsWith('_road_network')),'Industrie — grain et dégradé','PM_INDUSTRIE_GRAIN_DEGRADE.png');
  const pms=plan.entries.filter(e=>e.family==='PM');
  for(let n=0;n<3;n++)await comparisonPage(pms.slice(n*6,(n+1)*6),n+1);
  await checkerBoard(plan.entries);
  write('preview_validation.json',{status:'PASS_TECHNICAL_CHECKS_VISUAL_APPROVAL_REQUIRED',
    protected_files:Object.keys(baseline).length,changed_game_files:changed,added_game_files:added,
    generated_dds_exported:false,existing_pm_dds_unchanged:13,technology_preview_unchanged:true,native_building_unchanged:true,game_tested:false,
    artistic_changes:'Built-in imagegen only; deterministic resize and contact sheets only afterwards',checks});
  write('preview_manifest.json',{status:'GENERATED_AWAITING_USER_APPROVAL',approval_required:true,
    native_building:'UNCHANGED',technology:'UNCHANGED',entries:checks,
    boards:['PM_ROUTES_GRAIN_DEGRADE.png','PM_LABORATOIRE_GRAIN_DEGRADE.png','PM_INDUSTRIE_GRAIN_DEGRADE.png',
      'PM_COMPARAISON_VANILLA_1.png','PM_COMPARAISON_VANILLA_2.png','PM_COMPARAISON_VANILLA_3.png','TRANSPARENCE_DAMIER.png']});
  console.log(JSON.stringify({status:'PASS_TECHNICAL',generated_previews:checks.length,
    protected_files:Object.keys(baseline).length,changed_game_files:changed,dds_exported:false}));
}
main().catch(e=>{console.error(e);process.exit(1);});
