"""Guarded local law variants: no global prerequisites or late technology gifts."""
from dp01_install import *
def repair():
 m=load('APPLIED.json');changes={};lawfile='common/laws/1776_dp01.txt';body=text(ROOT/lawfile)
 for rel,key,newkey,allowed in [('common/laws/02_slavery.txt','law_debt_slavery','law_aor1776_dp01_customary_bondage',['KAL','PTA']),('common/laws/00_church_and_state.txt','law_freedom_of_conscience','law_aor1776_dp01_toleration',['PTA'])]:
  raw=text(ROOT/rel);n=next(n for n in parse(raw) if n.key==key);snippet=raw[n.start:n.end];prefix=snippet.index('{');snippet=newkey+' = '+snippet[prefix:]
  ns=parse(snippet)[0];patch=[]
  for z in ns.children('unlocking_technologies'):patch.append((z.start,z.end,'unlocking_technologies = { international_relations }'))
  gate=' OR = { '+' '.join('c:'+t+' ?= this' for t in allowed)+' } '
  patch.append((ns.end-1,ns.end-1,'\n parent = '+key+'\n is_visible = { '+gate+' }\n can_enact = { '+gate+' }\n'))
  body+='\n# Bounded starting abstraction retaining the existing law effects, not a claim of modern constitutional institutions.\n'+edit(snippet,patch)+'\n'
 changes[lawfile]=encoded(ROOT/lawfile,body)
 for tag,name in [('KAL','kal - kalat.txt'),('PTA','pta - patiala.txt')]:
  rel='common/history/countries/'+name;raw=text(ROOT/rel).replace('law_debt_slavery','law_aor1776_dp01_customary_bondage').replace('law_freedom_of_conscience','law_aor1776_dp01_toleration');changes[rel]=encoded(ROOT/rel,raw)
 for lang in ['french','english']:
  rel='localization/'+lang+'/replace/1776_dp01_l_'+lang+'.yml';raw=text(ROOT/rel);fr=lang=='french'
  names={'law_aor1776_dp01_customary_bondage':('Servitude coutumière','Customary bondage'),'law_aor1776_dp01_customary_bondage_desc':('La servitude subsiste dans les usages locaux et les rapports de dépendance entre maisons et familles.','Bondage persists in local custom and relations of dependency between households and families.'),'law_aor1776_dp01_toleration':('Tolérance des cultes','Religious toleration'),'law_aor1776_dp01_toleration_desc':('Les communautés conservent leurs pratiques religieuses sous un gouvernement qui soutient la foi de son souverain.','Communities retain their religious practices under a government that supports its ruler’s faith.')}
  raw+=''.join(' '+k+':0 "'+v[0 if fr else 1]+'"\n' for k,v in names.items());changes[rel]=b'\xef\xbb\xbf'+raw.encode()
 receipts=[]
 for rel,data in changes.items():
  p=ROOT/rel;z=next(z for z in m['files'] if z['file']==rel);assert sha(p)==z['after_sha256'],('Concurrent write',rel)
  if p.suffix=='.txt':parse(data.decode('utf-8-sig'))
  q=OUT/'profile_repair_preimages'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());before=sha(p);p.write_bytes(data);z['after_sha256']=sha(p);receipts.append(dict(file=rel,before_sha256=before,after_sha256=sha(p)))
 dump('PROFILE_REPAIR.json',dict(reason='Remove activation-only requirements for constitutional government and institutionalized scientific exchange; bounded variants preserve intended existing-law mechanics without late technology grants.',files=receipts));dump('APPLIED.json',m)
 print('Bounded restored-profile repair installed.')
if __name__=='__main__':repair()
