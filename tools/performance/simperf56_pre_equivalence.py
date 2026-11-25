"""Compare native PRE saves in memory after normalizing only controller flags."""
import hashlib,json
from pathlib import Path
from simperf56_ai_cohorts import LAB,db_chunks,write
from simperf56_save_state import sections

out={}
for label in ('AI_ON3','AI_OFF3R','AI_DEC1','AI_DEC2','AI_OTHER1','AI_ON4R'):
    proof=json.loads((LAB/(label+'_PRE_AI_PROOF.json')).read_text(encoding='utf-8'))
    raw=Path(proof['save']).read_bytes();assert hashlib.sha256(raw).hexdigest()==proof['sha256']
    text=raw.decode('utf-8-sig');edits=[]
    for rid,a,b,n in db_chunks(text,sections(text)['ai']):
        flags=n.children('enabled');assert len(flags)==1
        f=flags[0];assert f.value in ('yes','no')
        if f.value=='no':edits.append((a+f.start,a+f.end))
    normalized=text
    for a,b in sorted(edits,reverse=True):
        assert normalized[a:b]=='enabled=no'
        normalized=normalized[:a]+'enabled=yes'+normalized[b:]
    payload=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+normalized.encode('utf-8')
    out[label]=dict(source_sha256=proof['sha256'],flags_normalized_in_memory=len(edits),
        normalized_sha256=hashlib.sha256(payload).hexdigest())
reference=out['AI_ON3']['normalized_sha256']
for v in out.values():v['native_PRE_byte_equal_except_enabled_flags']=v['normalized_sha256']==reference
write(LAB/'NATIVE_PRE_EQUIVALENCE.json',out)
print(json.dumps(out,indent=2))
