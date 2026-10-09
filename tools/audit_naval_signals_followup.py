"""Audit the authorized Signaux navals -> Charpente diagonale follow-up."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import build_start_1776_research_input_pack as cat
import plan_oct09_balance_revision as revision

ROOT=Path(__file__).resolve().parents[1]
REL='common/technology/technologies/25_tech3a_naval.txt'
RECORD=ROOT/'.asset-cache/oct09_balance_revision/naval_signals_followup.json'

def expected_from(before):
    before=before.replace('\r\n','\n')
    def add_parent(block):
        old='unlocking_technologies = {\n\t\tscientific_naval_architecture\n\t}'
        assert block.count(old)==1, 'Unexpected diagonal framing prerequisites'
        return block.replace(old,'unlocking_technologies = {\n\t\tscientific_naval_architecture\n\t\tstandardized_naval_signals\n\t}',1)
    return revision.edit_object(before,'diagonal_ship_framing',add_parent)

def prepare():
    assert not RECORD.exists(), 'Do not overwrite this follow-up baseline'
    binary=(ROOT/REL).read_bytes()
    before=binary.decode('utf-8-sig').replace('\r\n','\n')
    # If the edit is already present, reconstruct only that single added edge
    # and require its original bytes to match the earlier immutable protection.
    if 'standardized_naval_signals' in cat.tokens_flat(cat.braced_tokens(cat.effective_objects('common/technology/technologies',r'[A-Za-z0-9_]+')['diagonal_ship_framing'].text,'unlocking_technologies')):
        before=revision.edit_object(before,'diagonal_ship_framing',lambda t:t.replace('\n\t\tstandardized_naval_signals','',1))
    protected=json.loads((RECORD.parent/'baseline.json').read_text(encoding='utf-8'))['protected'][REL]
    # apply_patch normalizes mixed line endings. The file's pre-edit content is
    # tracked and unchanged from HEAD, checked after removing the single edge.
    # Retain the earlier byte hash as provenance, not as a reconstructed hash.
    tracked=subprocess.check_output(['git','show','HEAD:'+REL],cwd=ROOT).decode('utf-8-sig').replace('\r\n','\n')
    assert before==tracked, 'Reconstructed content differs from the tracked pre-edit technology file'
    record={'path':REL,'before':before,'prior_protected_sha256':protected,
            'before_normalized_sha256':hashlib.sha256(before.encode('utf-8')).hexdigest(),
            'expected':expected_from(before),'request':'Add Signaux navals as a parent of Charpente diagonale; preserve all other technology definitions.'}
    RECORD.parent.mkdir(parents=True,exist_ok=True)
    RECORD.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Follow-up reference recorded; no runtime files changed.')

def check():
    record=json.loads(RECORD.read_text(encoding='utf-8'))
    assert record['expected']==expected_from(record['before']), 'Change exceeds the authorized single edge'
    actual=(ROOT/REL).read_text(encoding='utf-8-sig')
    assert actual==record['expected'], 'Unexpected naval technology edits'
    objects=cat.effective_objects('common/technology/technologies',r'[A-Za-z0-9_-]+')
    parents={key:cat.tokens_flat(cat.braced_tokens(obj.text,'unlocking_technologies')) for key,obj in objects.items()}
    unknown=[(key,p) for key,ps in parents.items() for p in ps if p not in objects]
    assert not unknown, ('Unknown prerequisites',unknown)
    seen=set();active=set()
    def visit(key):
        if key in active:raise AssertionError('Technology cycle at '+key)
        if key in seen:return
        active.add(key)
        for p in parents[key]:visit(p)
        active.remove(key);seen.add(key)
    for key in objects:visit(key)
    assert 'standardized_naval_signals' in parents['diagonal_ship_framing']
    assert 'scientific_naval_architecture' in parents['diagonal_ship_framing']
    assert 'diagonal_ship_framing' in parents['iron_hull_construction']
    hulls=cat.effective_objects('common/ship_types',r'ship_type_\w+')
    successor=RECORD.parent/'gbr_agriculture_followup.json'
    gate='standardized_naval_signals'
    if successor.exists():
        amendment=json.loads(successor.read_text(encoding='utf-8'))
        rel='common/ship_types/00_ship_types.txt'
        if rel in amendment['expected']:
            assert (ROOT/rel).read_text(encoding='utf-8-sig')==amendment['expected'][rel]
            assert 'unlocking_technologies = { standardized_naval_signals }' in amendment['before'][rel]
            gate='marine_chronometry'
    assert cat.tokens_flat(cat.braced_tokens(hulls['ship_type_ship_of_the_line'].text,'unlocking_technologies'))==[gate]
    result={'status':'PASS_NAVAL_SIGNALS_FOLLOWUP','technology_nodes':len(objects),'cycles':0,
            'changed_edges':1,'chain':['standardized_naval_signals','diagonal_ship_framing','iron_hull_construction'],'engine_tested':False}
    print(json.dumps(result))
    return record

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');args=parser.parse_args()
    prepare() if args.prepare else check()
