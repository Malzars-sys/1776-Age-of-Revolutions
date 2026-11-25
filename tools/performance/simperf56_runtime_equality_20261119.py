"""Check native resolved resources and launch settings for a matched AI-flag pair."""
import argparse, json, re
from simperf56_ai_cohorts import LAB

ap=argparse.ArgumentParser();ap.add_argument('control');ap.add_argument('other');a=ap.parse_args()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def run(label):
    paths=list((LAB/'runs').glob(label+'_*'));assert len(paths)==1
    p=paths[0];assert (p/'EXIT.json').exists()
    launch=read(p/'LAUNCH.json')
    text=(p/'stdout.txt').read_text(encoding='utf-8-sig',errors='replace')
    matches=re.findall(r'\[Checksum Builder\] \[[^\]]+\] (.+?) \[Contents Checksum\]: ([0-9a-fA-F]+)',text)
    hashes={k.replace('\\','/').lower():v.lower() for k,v in matches};assert len(hashes)>1000
    return launch,hashes
c,ch=run(a.control);o,oh=run(a.other)
checks={k:c[k]==o[k] for k in ('executable_sha256','settings_sha256','mods')}
changed=sorted(k for k in ch.keys()&oh.keys() if ch[k]!=oh[k])
added=sorted(oh.keys()-ch.keys());removed=sorted(ch.keys()-oh.keys())
out=dict(control=a.control,other=a.other,launch_checks=checks,virtual_file_counts=[len(ch),len(oh)],
         changed=changed,added=added,removed=removed,
         runtime_resources_equal=all(checks.values()) and not changed and not added and not removed,
         scope='Native resolved resource content and launch configuration only; seed flags and native POST controller proofs are separate. Not a CPU attribution.')
with (LAB/(a.control+'_'+a.other+'_RUNTIME_EQUALITY.json')).open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));assert out['runtime_resources_equal']
