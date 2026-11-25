"""Explain native PRE serialization differences; no save is rewritten."""
from pathlib import Path
import hashlib,json,difflib
from simperf56_ai_cohorts import LAB,write
from simperf56_save_state import sections

def read(label):
    proof=json.loads((LAB/(label+'_PRE_AI_PROOF.json')).read_text(encoding='utf-8'))
    text=Path(proof['save']).read_text(encoding='utf-8-sig');return text,sections(text)
reference,rs=read('AI_ON3');out={}
for label in ('AI_OFF3R','AI_DEC2','AI_OTHER1'):
    text,ss=read(label);diff={}
    for name in sorted(set(rs)|set(ss)):
        a=reference[slice(*rs[name])] if name in rs else ''
        b=text[slice(*ss[name])] if name in ss else ''
        if a==b:continue
        v=dict(before_characters=len(a),after_characters=len(b))
        if max(len(a),len(b))<20000:
            v['diff']=list(difflib.unified_diff(a.splitlines(),b.splitlines(),n=2))
        diff[name]=v
    out[label]=diff
write(LAB/'NATIVE_PRE_SECTION_DIFFERENCES.json',out)
print(json.dumps(out,indent=2,ensure_ascii=True))
