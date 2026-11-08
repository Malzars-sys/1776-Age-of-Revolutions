"""Content-only integration. Never mutates Git, sources, launcher or vanilla."""
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/integration/WORKTREES_TO_MAIN_2026_11_05'
ROOTS={'main':Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork'),
       'massa':ROOT,'map0':Path('C:/Users/simeo/.codex/worktrees/map-0-collaborator-integration/1776_Age_of_Revolutions_fork')}
HEADS={'main':'52c42808bdb0748e69fbde3423bb5004b5b1f20a','massa':'52c42808bdb0748e69fbde3423bb5004b5b1f20a','map0':'c891b1d9bb2a21bc42409acbdccc268518110260'}
SKIP={'.git','.asset-cache','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','.venv','venv','node_modules','.colgrep'}
TEXT={'.txt','.json','.yml','.yaml','.py','.ps1','.md','.csv','.tsv','.mod','.gui','.gfx','.asset','.shader','.fxh','.vfx','.ini','.xml','.html','.svg','.sh','.toml','.js','.mjs','.cjs'}


def dump(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def load(name):
    return json.loads((OUT/name).read_text(encoding='utf-8-sig'))


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()


def git(*args):
    return subprocess.run(['git','--no-optional-locks',*args],cwd=ROOT,stdin=subprocess.DEVNULL,capture_output=True,check=True).stdout


def inventory():
    for label,base in ROOTS.items():
        assert base.is_dir() and (base/'.git').exists(),'Worktree missing: '+str(base)
        destination=OUT/(label.upper()+'_INVENTORY.json')
        assert not destination.exists(),'Do not replace a completed baseline'
        start=time.time();tracked={}
        for row in git('ls-tree','-rz',HEADS[label]).split(b'\0'):
            if row:
                meta,path=row.split(b'\t',1);tracked[path.decode('utf8')]=meta.split()[2].decode()
        files={};links=[];total=0
        print('Reading',label,flush=True)
        for directory,dirs,names in os.walk(base,followlinks=False):
            d=Path(directory)
            dirs[:]=[n for n in dirs if n not in SKIP and not (d/n).is_symlink() and not (d/n).is_junction() and (d/n).relative_to(base).as_posix()!='docs/reports/integration/WORKTREES_TO_MAIN_2026_11_05']
            for name in names:
                if name in SKIP:continue
                p=d/name;rel=p.relative_to(base).as_posix()
                if p.is_symlink():links.append(rel);continue
                st=p.stat();h=sha(p);oid=None;lf=None
                if rel in tracked:
                    data=p.read_bytes();oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();lf=oid
                    if (p.suffix.lower() in TEXT or p.name in {'AGENTS.md','.gitignore','.gitattributes'}) and b'\r\n' in data:
                        data=data.replace(b'\r\n',b'\n');lf=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
                assert (st.st_size,st.st_mtime_ns)==(p.stat().st_size,p.stat().st_mtime_ns),'Concurrent change while reading '+str(p)
                files[rel]=dict(sha256=h,size=st.st_size,mtime_ns=st.st_mtime_ns,tracked=rel in tracked,
                    changed_from_head=rel not in tracked or tracked[rel] not in {oid,lf})
                total+=st.st_size
                if len(files)%1000==0:print(label,len(files),'files',round(total/1e9,2),'GB;',rel[:110],flush=True)
        deleted=sorted(set(tracked)-set(files));changed=[p for p,v in files.items() if v['changed_from_head']]
        dump(label.upper()+'_INVENTORY.json',dict(root=str(base),head=HEADS[label],tracked=tracked,files=files,deleted=deleted,links=links,excluded_cache_names=sorted(SKIP)))
        (OUT/(label.upper()+'_CHANGED.txt')).write_text('\n'.join(changed)+'\n',encoding='utf8')
        print('Completed',label,'files',len(files),'GB',round(total/1e9,2),'changed',len(changed),'runtime',sum(p.split('/')[0] in {'common','events','gfx','gui','map_data','localization','music'} for p in changed),'deleted',len(deleted),'seconds',round(time.time()-start,1),flush=True)


def normal(data):
    return data.decode('utf-8-sig').replace('\r\n','\n')


def restore_style(merged,current,source):
    import difflib
    original=current.decode('utf8');bom=original.startswith('\ufeff') or source.startswith(b'\xef\xbb\xbf')
    original=original.lstrip('\ufeff');old=original.splitlines(True);oldkeys=[s.rstrip('\r\n') for s in old]
    new=merged.splitlines(True);newkeys=[s.rstrip('\r\n') for s in new]
    eol='\r\n' if original.count('\r\n')>original.count('\n')/2 else '\n';parts=[]
    for op,a,b,c,d in difflib.SequenceMatcher(None,oldkeys,newkeys,autojunk=True).get_opcodes():
        if op=='equal':parts.extend(old[a:b])
        else:parts.extend(s.rstrip('\r\n')+(eol if s.endswith('\n') else '') for s in new[c:d])
    return (('\ufeff' if bom else '')+''.join(parts)).encode('utf8')


class Blobs:
    def __init__(self):
        self.process=subprocess.Popen(['git','--no-optional-locks','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.directory=OUT/'base_objects';self.directory.mkdir(exist_ok=True)
    def get(self,oid):
        path=self.directory/oid
        if path.exists():return path.read_bytes()
        self.process.stdin.write((oid+'\n').encode());self.process.stdin.flush();header=self.process.stdout.readline().split()
        assert header[1]==b'blob',header
        size=int(header[2]);data=self.process.stdout.read(size);assert len(data)==size and self.process.stdout.read(1)==b'\n'
        path.write_bytes(data);return data
    def close(self):
        self.process.stdin.close();self.process.wait()


def pixel_merge(current,base,source,rel):
    import io
    import numpy as np
    from PIL import Image
    ims=[Image.open(io.BytesIO(b)).convert('RGB') for b in [current,base,source]]
    assert len({im.size for im in ims})==1,'Map dimensions differ'
    c,b,s=[np.asarray(im) for im in ims];change=np.any(s!=b,axis=2);conflict=change&np.any(c!=b,axis=2)&np.any(c!=s,axis=2)
    ys,xs=np.where(conflict)
    detail=dict(changed_source_cells=int(change.sum()),conflict_cells=int(conflict.sum()),conflict_sample=[[int(x),int(y)] for y,x in list(zip(ys,xs))[:100]])
    if conflict.any():return None,detail
    out=c.copy();out[change]=s[change];buf=io.BytesIO();Image.fromarray(out).save(buf,format='PNG');return buf.getvalue(),detail


def text_merge(current,base,source):
    try:c,b,s=map(normal,[current,base,source])
    except UnicodeError:return None,dict(reason='binary_or_non_UTF8')
    if c==s:return current,dict(method='same_text_preserve_target_style')
    if b==s:return current,dict(method='source_only_line_endings')
    if c==b:return source,dict(method='target_text_unchanged')
    import difflib
    lines=b.splitlines(True);edits=[]
    for branch,text in [('main',c),('agent',s)]:
        other=text.splitlines(True)
        for op,i,j,k,l in difflib.SequenceMatcher(None,lines,other,autojunk=False).get_opcodes():
            if op!='equal':edits.append(dict(start=i,end=j,value=other[k:l],branch=branch))
    edits.sort(key=lambda e:(e['start'],e['end']));groups=[]
    def overlap(a,b):
        if a['start']==a['end'] and b['start']==b['end']:return a['start']==b['start']
        if a['start']==a['end']:return b['start']<a['start']<b['end']
        if b['start']==b['end']:return a['start']<b['start']<a['end']
        return max(a['start'],b['start'])<min(a['end'],b['end'])
    for edit in edits:
        if groups and any(overlap(edit,e) for e in groups[-1]):groups[-1].append(edit)
        else:groups.append([edit])
    output=[];cursor=0;conflicts=[]
    for group in groups:
        start=min(e['start'] for e in group);end=max(e['end'] for e in group);output.extend(lines[cursor:start])
        def render(branch):
            result=[];at=start
            for e in group:
                if e['branch']!=branch:continue
                result.extend(lines[at:e['start']]);result.extend(e['value']);at=e['end']
            result.extend(lines[at:end]);return result
        cm,sm=render('main'),render('agent');original=lines[start:end]
        if cm==sm:output.extend(cm)
        elif cm==original:output.extend(sm)
        elif sm==original:output.extend(cm)
        else:
            conflicts.append(dict(base_start=start+1,base_end=end))
            output.extend(['<<<<<<< PRINCIPAL\n',*cm,'||||||| BASE\n',*original,'=======\n',*sm,'>>>>>>> AGENT\n'])
        cursor=end
    output.extend(lines[cursor:]);merged=''.join(output)
    if conflicts:return None,dict(reason='overlapping_text_edits',preview=merged,groups=conflicts)
    return restore_style(merged,current,source),dict(method='nonoverlapping_three_way_text')


def stage():
    assert not (OUT/'STAGING_ACTIONS.json').exists(),'Keep the initial plan immutable; resolve explicitly'
    snapshots={k:load(k.upper()+'_INVENTORY.json') for k in ROOTS};main=snapshots['main'];blobs=Blobs()
    candidate=OUT/'candidate';candidate.mkdir(exist_ok=True);actions={};conflicts=[];decisions=[]
    maintracked=main['tracked']
    try:
        for label in ['massa','map0']:
            snap=snapshots[label];pending=sorted(p for p,v in snap['files'].items() if v['changed_from_head'])+snap['deleted']
            print('Staging',label,len(pending),'paths',flush=True)
            for i,rel in enumerate(pending):
                if i%1000==0:print(label,i,'/',len(pending),rel[:100],flush=True)
                target=ROOTS['main']/rel;staged=candidate/rel;entry=actions.get(rel)
                current=staged.read_bytes() if staged.exists() else (target.read_bytes() if target.is_file() and not (entry and entry['action']=='delete') else None)
                srcfile=ROOTS[label]/rel;source=srcfile.read_bytes() if srcfile.is_file() else None
                if source is not None:
                    actual=hashlib.sha256(source).hexdigest()
                    if label=='massa' and rel=='tools/integrate_three_worktrees.py' and actual!=snap['files'][rel]['sha256']:
                        decisions.append(dict(source=label,file=rel,method='integration_tool_authored_during_current_mission',inventory_sha256=snap['files'][rel]['sha256'],current_sha256=actual))
                    else:assert actual==snap['files'][rel]['sha256'],'Concurrent source change '+label+'/'+rel
                if source==current:
                    decisions.append(dict(source=label,file=rel,method='already_identical'));continue
                oid=snap['tracked'].get(rel);base=blobs.get(oid) if oid else None
                if source is not None and base is not None and srcfile.suffix.lower() in TEXT:
                    try:only_eol=normal(source)==normal(base) and source.startswith(b'\xef\xbb\xbf')==base.startswith(b'\xef\xbb\xbf')
                    except UnicodeError:only_eol=False
                    if only_eol:
                        decisions.append(dict(source=label,file=rel,method='ignore_source_line_ending_only_change'));continue
                if oid is None and rel in maintracked:
                    base=blobs.get(maintracked[rel])
                    if source==base or (source is not None and srcfile.suffix.lower() in TEXT and normal(source)==normal(base)):
                        decisions.append(dict(source=label,file=rel,method='untracked_source_is_already_committed_in_main'));continue
                if label=='map0' and rel in maintracked and source is not None:
                    committed=blobs.get(maintracked[rel])
                    if source==committed or (srcfile.suffix.lower() in TEXT and normal(source)==normal(committed)):
                        decisions.append(dict(source=label,file=rel,method='source_content_already_integrated_in_main_history'));continue
                if source is None:
                    if rel.startswith('docs/'):
                        decisions.append(dict(source=label,file=rel,method='preserve_archived_document_despite_source_deletion'));continue
                    if current==base:
                        if staged.exists():staged.unlink()
                        actions[rel]=dict(action='delete',source=label,before=main['files'].get(rel,{}).get('sha256'),after=None);continue
                    detail=dict(reason='delete_vs_modified_target');merged=None
                elif current is None or current==base:
                    merged=source;detail=dict(method='new_file' if current is None else 'only_source_changed')
                elif base is not None and rel=='map_data/provinces.png':
                    merged,detail=pixel_merge(current,base,source,rel)
                elif base is not None and (srcfile.suffix.lower() in TEXT or srcfile.name in {'AGENTS.md','.gitignore','.gitattributes'}):
                    merged,detail=text_merge(current,base,source)
                else:merged=None;detail=dict(reason='different_independent_additions' if base is None else 'overlapping_binary_changes')
                if merged is None:
                    record=dict(file=rel,source=label,base_oid=oid,detail=detail)
                    folder=OUT/'conflicts'/label/rel;folder.parent.mkdir(parents=True,exist_ok=True)
                    if source is not None:folder.with_name(folder.name+'.agent').write_bytes(source)
                    if current is not None:folder.with_name(folder.name+'.main').write_bytes(current)
                    if base is not None:folder.with_name(folder.name+'.base').write_bytes(base)
                    if detail.get('preview'):folder.with_name(folder.name+'.diff3').write_text(detail.pop('preview'),encoding='utf8')
                    conflicts.append(record);continue
                if merged==current:
                    decisions.append(dict(source=label,file=rel,**detail));continue
                staged.parent.mkdir(parents=True,exist_ok=True);staged.write_bytes(merged)
                contributors=list(actions.get(rel,{}).get('contributors',[]))+[label]
                actions[rel]=dict(action='write',source=label,contributors=contributors,before=main['files'].get(rel,{}).get('sha256'),after=hashlib.sha256(merged).hexdigest(),size=len(merged),detail=detail)
    finally:blobs.close()
    dump('STAGING_ACTIONS.json',actions);dump('CONFLICTS.json',conflicts);dump('DECISIONS.json',decisions)
    print('Staged',len(actions),'paths; conflicts',len(conflicts),'runtime conflicts',sum(r['file'].split('/')[0] in {'common','events','gfx','gui','localization','map_data','music'} for r in conflicts),flush=True)


if __name__=='__main__':
    {'inventory':inventory,'stage':stage}[sys.argv[1]]()
