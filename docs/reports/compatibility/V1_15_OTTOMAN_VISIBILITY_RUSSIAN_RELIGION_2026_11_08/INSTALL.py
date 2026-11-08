"""One-use, hash-guarded local delivery. No Git or native game writes."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[4]
LOT=Path(__file__).resolve().parent
GAME=Path('C:/Games/Victoria 3/game')
sys.path.insert(0,str(ROOT/'tools/compatibility'))
from issue27_journal_outcomes_audit import fields,one
assert not (LOT/'INSTALLATION.json').exists(),'Already installed'
before=json.loads((LOT/'BEFORE.json').read_text(encoding='utf8'))
paths=before['scope'][:4];newpaths=before['scope'][4:]
source={p:(LOT/'before'/p).read_bytes() for p in paths}
changes={}
p=paths[0];old=source[p]
needle=b'\tgroup = je_group_1776_imperial_crises\r\n\r\n'
assert old.count(needle)==8
insert='''\tis_shown_when_inactive = {
\t\tc:TUR = THIS
\t\thas_variable = ottoman_1776_initialized
\t\tNOR = {
\t\t\thas_variable = ottoman_1776_political_complete
\t\t\thas_variable = sick_man_complete
\t\t}
\t}
\tpossible = {
\t\tcustom_tooltip = {
\t\t\ttext = aor1776_sick_man_activation_tt
\t\t\thas_variable = ottoman_1776_sick_man_started
\t\t}
\t}

'''.replace('\n','\r\n').encode()
new=old.replace(needle,needle+insert,1)
needle=b'\tcurrent_value = {\r\n\t\tvalue = var:sick_man_var\r\n\t}'
assert new.count(needle)==1
new=new.replace(needle,b'\tcurrent_value = {\r\n\t\tvalue = 0\r\n\t\tif = {\r\n\t\t\tlimit = { has_variable = sick_man_var }\r\n\t\t\tadd = var:sick_man_var\r\n\t\t}\r\n\t}',1)
changes[p]=new
p=paths[1];old=source[p]
needle=b'\t\tadd_journal_entry = { type = je_sick_man_main }\n'
assert old.count(needle)==1
insert='''\t\t# The visible inactive entry activates through eligibility. Keep a
\t\t# manual fallback only when no active or inactive instance exists.
\t\tif = {
\t\t\tlimit = {
\t\t\t\tNOR = {
\t\t\t\t\thas_journal_entry = je_sick_man_main
\t\t\t\t\thas_inactive_journal_entry = je_sick_man_main
\t\t\t\t}
\t\t\t}
\t\t\tadd_journal_entry = { type = je_sick_man_main }
\t\t}
'''.encode()
changes[p]=old.replace(needle,insert,1)
p=paths[2];old=source[p]
needle=b'\t\t\thas_law = law_type:law_people_of_the_book\r\n\t\t}\r\n'
assert old.count(needle)==1
native=(GAME/p).read_bytes().decode('utf-8-sig')
assert hashlib.sha256((GAME/p).read_bytes()).hexdigest()==before['native_hashes'][p]
law=one(fields(native),'law_state_religion');vis=one(fields(law.body),'is_visible');nand=one(fields(vis.body),'NAND')
clause=vis.body[nand.start:nand.end]
changes[p]=old.replace(needle,needle+b'\t\t'+clause.encode()+b'\r\n',1)
p=paths[3];old=source[p]
needle=b'activate_law = law_type:law_state_religion'
assert old.count(needle)==1
changes[p]=old.replace(needle,b'activate_law = law_type:law_caesaropapism',1)
native_law=one(fields(native),'law_caesaropapism')
changes[newpaths[0]]=b'# Native 1.15 Caesaropapism restored as a separate definition.\n'+native[native_law.start:native_law.end].encode()+b'\n'
for lang,text in [('french','L’échec de « $je_1776_many_masters$ » a ouvert la crise des réformes.'),('english','Failure of “$je_1776_many_masters$” has opened the reform crisis.')]:
 p=f'localization/{lang}/1776_ottoman_sick_man_visibility_l_{lang}.yml'
 changes[p]=b'\xef\xbb\xbf'+f'l_{lang}:\n aor1776_sick_man_activation_tt:0 "{text}"\n'.encode('utf8')
for p,blob in changes.items():
 dest=ROOT/p
 if p in source:assert dest.read_bytes()==source[p],f'Concurrent edit: {p}'
 else:assert not dest.exists(),f'Concurrent creation: {p}'
for p,blob in changes.items():(ROOT/p).write_bytes(blob)
(LOT/'INSTALLATION.json').write_text(json.dumps(dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',changed=[dict(path=p,before_sha256=hashlib.sha256(source[p]).hexdigest() if p in source else None,after_sha256=hashlib.sha256(blob).hexdigest()) for p,blob in changes.items()],engine_tested=False,git_write=False,vanilla_write=False),indent=2)+'\n',encoding='utf8')
print('Installed bounded edits:',len(changes),'files')
