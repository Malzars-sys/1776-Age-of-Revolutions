"""Prepare or explicitly apply the bounded provisional Agra scenario.

Not a demographic finding. --apply-provisional is reserved for an explicit user
choice to keep current population and stabilize employment by adding land units.
"""
from pathlib import Path
import argparse,json,math
from audit_arable_population_1776 import ROOT,digest,parse
from hbc06_integrate import edit,encoded

OUT=ROOT/'docs/reports/economy/ARABLE_POPULATION_1776/ARABLE-01'
REL='map_data/state_regions/10_india.txt'

def prepare():
 assert not (OUT/'AGRA_PROVISIONAL_PLAN.json').exists(),'Keep prior proposal intact'
 data=json.loads((OUT/'final/DIAGNOSIS.json').read_text(encoding='utf8'))
 r=next(r for r in data['native']['states'] if r['state']=='STATE_AGRA' and r['owner']=='MARATH')
 s=next(r for r in data['states'] if r['state']=='STATE_AGRA' and r['owner']=='MARATH')
 extra=math.ceil(r['unemployed']/s['subsistence_jobs_per_level_max'])
 required=r['arable_land']+extra
 new=math.ceil(required*s['region_provinces']/s['owner_provinces'])
 p=ROOT/REL;before=p.read_bytes();raw=before.decode('utf-8-sig')
 n=next(n for n in parse(raw) if n.key=='STATE_AGRA');q=n.children('arable_land');assert len(q)==1 and q[0].value=='483'
 after=encoded(p,edit(raw,[(q[0].start,q[0].end,'arable_land = '+str(new))]))
 oldcopy=OUT/'proposal/preimages'/REL;oldcopy.parent.mkdir(parents=True,exist_ok=True);oldcopy.write_bytes(before)
 proposed=OUT/'proposal/staged'/REL;proposed.parent.mkdir(parents=True,exist_ok=True);proposed.write_bytes(after)
 plan=dict(status='PROPOSAL_PENDING_USER_CHOICE',file=REL,before_sha256=digest(p),after_sha256=digest(proposed),before_arable=483,proposed_arable=new,extra_owner_subsistence_levels=extra,observed_unemployed=r['unemployed'],jobs_per_subsistence_level=s['subsistence_jobs_per_level_max'],native_date=data['native']['date'],native_save_sha256=data['native']['sha256'],historical_population_confirmed=False,hypotheses=['Current 23,928,236 inhabitants retained provisionally, not certified as historical.','Unemployment divided by 10,000 jobs per rice-subsistence level, rounded up.','Other employment, population and province shares fixed for scenario.','Additional land permits more commercial agriculture later; not merely an invisible unemployment fix.','No prediction that wages, food prices, all starvation or future mortality are solved.'])
 (OUT/'AGRA_PROVISIONAL_PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps(plan,ensure_ascii=False))

def apply():
 assert not (OUT/'AGRA_PROVISIONAL_APPLIED.json').exists(),'Already applied; do not overwrite proof'
 plan=json.loads((OUT/'AGRA_PROVISIONAL_PLAN.json').read_text(encoding='utf8'));p=ROOT/plan['file']
 assert digest(p)==plan['before_sha256'],'Shared region file changed: review current file before a fresh scoped proposal'
 staged=OUT/'proposal/staged'/plan['file'];assert digest(staged)==plan['after_sha256']
 before=p.read_bytes();after=staged.read_bytes();a=before.decode('utf-8-sig');b=after.decode('utf-8-sig')
 n=next(n for n in parse(a) if n.key=='STATE_AGRA');q=n.children('arable_land')[0]
 assert edit(a,[(q.start,q.end,'arable_land = '+str(plan['proposed_arable']))])==b
 assert digest(p)==plan['before_sha256']
 p.write_bytes(after)
 assert digest(p)==plan['after_sha256']
 receipt=dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',file=plan['file'],before_sha256=plan['before_sha256'],after_sha256=plan['after_sha256'],before_arable=plan['before_arable'],after_arable=plan['proposed_arable'],historical_population_confirmed=False,runtime_post_fix_validated=False,scope='One arable_land value only; all other State_Region fields byte-preserved. New game required, current session unchanged.')
 (OUT/'AGRA_PROVISIONAL_APPLIED.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps(receipt,ensure_ascii=False))

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',action='store_true');g.add_argument('--apply-provisional',action='store_true');args=ap.parse_args()
 if args.prepare:prepare()
 else:apply()
